import ROOT
import pickle
import itertools
from collections import OrderedDict

import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
from Workspace.DegenerateStopAnalysis.tools.CombineCard import convertAsymFloatToSym
from Workspace.DegenerateStopAnalysis.tools.regionsInfo import *
from Workspace.DegenerateStopAnalysis.tools.fakeCombine import getFakeEstimateParal, compareCombineVsSimpleFakes

MINFAKEVAL = 0.1
SYMMETRIZEFAKES = True
FAKEMCPROXY     = '$Z/\\gamma^{*} +jets$' #DY 

bin_FR_basic_map = {
                         'ptVL' : [ 'ptVL' , 'r1vla', 'r1vlb', 'r1vlc' , 'r2vl' ] ,
                         'ptL'  : [ 'ptL'  , 'r1la',  'r1lb' , 'r1lc'  , 'r2l'  ] ,
                         'ptM'  : [ 'ptM'  , 'r1ma',  'r1mb' , 'r1mc'  , 'r2m'  ] ,
                         'ptH'  : [ 'ptH'  , 'r1ha',  'r1hb' , 'r1hc'  , 'r2h'  ] ,
                     #'pt_gt_30' : [ 'cr1', 'cr2' , 'crtt', ] ,
                     # '30-80'  : [ '_30to80' ] ,
                     '30-50'  : [ '_30to50' ] , 
                     '50-80'  : [ '_50to80' ] , 
                     '80-200' : [ '_80to200'] , 
                     '>200'   : [ '_gt_200' ] ,
                    } 
                     #'pt_gt_30' : [ 'cr1', 'cr2' , 'crtt', ] ,
bin_FR_eta_map =    {
                    "eta_gt_1p5" : ['_endcap'],
                    "eta_lt_1p5" : ['_barrel', 'r1' ],

                       }


def fakeEstimate( cfg, args ):
#if True:
    """
        Calculate contribution due to fake backgrounds
        Need to have el, mu yields, and the FRs
    """

    ret = {}

    yld_pkl_file_lep   = cfg.yieldPkls[ cfg.cutInstList[0].fullName]
    cutName            = cfg.cutInstList[0].name 
    saveDir            = cfg.saveDirs[cfg.cutInstList[0].fullName ] 
    if not "lep" in yld_pkl_file_lep or 'loose' in yld_pkl_file_lep:
        raise Exception("Run with the lep=lep option")
    #
    # getting Yield Instance pickles for lep, mu, el (lep will not be used for the final results) 
    #
    yld_pkls_files = {
                       'lep': yld_pkl_file_lep , 
                        'mu': yld_pkl_file_lep.replace("_lep_", "_mu_") ,
                        'el': yld_pkl_file_lep.replace("_lep_", "_el_") ,
                     }
    yld_pkls    = degTools.dict_function( yld_pkls_files , lambda f: pickle.load(file(f)) ) 
    yld_dicts   = degTools.dict_function( yld_pkls       , lambda yld: yld.getNiceYieldDict() ) 
    yldsByBin   = degTools.dict_function( yld_pkls       , lambda yld: yld.getByBins( yld.getNiceYieldDict()) ) 
    ylds_lep = yld_pkls['lep']
    
    
    LnTTag = "_LnT"
    all_regions = ylds_lep.cutNames


    regions_info = RegionsInfo( all_regions ) 
    card_regions_map =  regions_info.card_regions_map
    tight_LnT_map    =  regions_info.tight_LnT_map 
    sorted_regions   =  regions_info.sort_regions( regions_info.final_regions )  

    sampleNames = ylds_lep.sampleNames
    bkgList  = ylds_lep.bkgList

    #w        = [bkg for bkg in bkgList if 'w' in bkg]
    #tt       = [bkg for bkg in bkgList if 'tt' in bkg]
    #others   = [bkg for bkg in bkgList if bkg not in w+tt]

    w        = ['w']
    tt       = ['tt_2l', 'tt_1l']
    others   = ['dy','st', 'vv', 'ttx']

    sigs     = ylds_lep.sigList
    data     = ylds_lep.dataList
    
    samps = {
             'w'     : w        ,
             'tt'    : tt       ,
          #'qcd'      : ['qcd']  ,
          #'st'       : ['st']   ,
          #'vv'       : ['vv']   ,
          #'dy'       : ['dy']   ,
          #'ttx'      : ['ttx']  ,  
             'others': others   ,
             'sigs'  : sigs     ,
          #'t2tt300_270' : ['t2tt300_270'], 
            }
    hasData=False
    if data:
        samps.update( {
             'data'  : data     ,
            data[0]  : data     ,
                    })
        hasData=True
    for sig in sigs:
        samps[sig] = [sig]
    
    #
    # Getting the FakeRate pickles
    #
    #FR_file_template = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/final/{cmgTag}/{ppTag}/measurement1/tightToLooseRatio_measurement1_data-EWK_%s.pkl".format(cmgTag = cfg.cmgTag, ppTag = cfg.ppTag)
    #FR_file_template = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/final/{cmgTag}/{ppTag}/measurement1/tightToLooseRatio_measurement1_MC_%s.pkl".format(cmgTag = cfg.cmgTag, ppTag = cfg.ppTag)
    #FR_file_template = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/final/{cmgTag}/{ppTag}/MR14/tightToLooseRatios_MR14_data-EWK_stat.pkl".format(cmgTag = cfg.cmgTag, ppTag = cfg.ppTag)   
    FR_file_template = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/final/{cmgTag}/80X_postProcessing_v0/MR14/tightToLooseRatios_MR14_data-EWK_stat.pkl".format(cmgTag = cfg.cmgTag, ppTag = cfg.ppTag)   
 
    flavors = ['mu', 'el']
    #FR_pkls_files = { flav: FR_file_template%flav for flav in flavors }
    #FR_pkls_files = { flav: FR_file_template for flav in flavors }
    #FR_pkls     = degTools.dict_function( FR_pkls_files  , lambda f: pickle.load(file(f)) )

    FR_pkls     = { flav: pickle.load(file( FR_file_template ) )[flav] for flav in flavors }


    sampleNiceNames = { s: [ sampleNames[s_] for s_ in samps[s] ]  for s in samps}
    def getRegionFakeEstimate( binYlds ,  FR ):
        return degTools.dict_operator( binYlds, sampleNiceNames['data'] + ['Total'] , lambda data, prompts  : (data-prompts) * FR/(1-FR.val) )

    def getRegionFakeEstimateData( binYlds ,  FR ):
        return degTools.dict_operator( binYlds, sampleNiceNames['data'] , 
                                       lambda data   : data * FR/(1-FR.val) )
    def getRegionFakeEstimatePrompts( binYlds ,  FR ):
        return degTools.dict_operator( binYlds, ['Total'] , 
                                       lambda prompts   : prompts * FR/(1-FR.val) )
    
    flav = 'lep'
    
    #sig = [ "t2tt300_270" ]
    
    prompt_fake_yields = {'mu':{},'lep':{}, 'el':{}}
    prompt_fake_yields_all = {'mu':{},'lep':{}, 'el':{}}
    FR_dicts = {'mu':{}, 'el':{} } 
    for tight_region , LnT_region in tight_LnT_map.iteritems():
        for flav in ['mu', 'el']:
            yields_LnT      = yldsByBin[flav][LnT_region] 
            yields_prompt   = yldsByBin[flav][tight_region] 
            ptBin        = findPtBinFromRegionName( LnT_region )
            etaBin       = findPtBinFromRegionName( LnT_region , bin_FR_eta_map )
            FR=0
            if etaBin and ptBin: 
                FReta           = FR_pkls[flav].get(etaBin)
                if FReta: 
                    FR           = FReta.get(ptBin)
            #assert FR.val > 0 , "Negative FakeRate %s"%FR
            else:
                print "didn't find a pt or eta bin for: " , flav, LnT_region
            if not FR:
                print "no FR found", flav, LnT_region, ptBin, etaBin
                FR = degTools.u_float(-9999999,-9999999)
            FR_dicts[flav][tight_region] = FR
            if hasData: 
                fakeEstimate = getRegionFakeEstimate( yields_LnT , FR)
                fakeEstimateData = getRegionFakeEstimateData( yields_LnT , FR)
                fakeEstimatePrompts = getRegionFakeEstimatePrompts( yields_LnT , FR)
            else:
                fakeEstimate , fakeEstimateData , fakeEstimatePrompts = ( degTools.u_float(999), degTools.u_float(999), degTools.u_float(999) )
                fakeEstimate = yldsByBin[flav][tight_region][FAKEMCPROXY]
            #fakeEstimate = degTools.u_float( 0 ) if  fakeEstimate.val < 0 else fakeEstimate 
            #fakeEstimate = degTools.u_float( 0 ) if  fakeEstimate.val < 0 else fakeEstimate 
            prompt_fake_yields_all[flav][tight_region] = {}
            #for prompt_samp in ['w', 'tt', 'others' ] + data + sigs +['qcd','dy','st','vv','ttx']:
            for prompt_samp in ['w', 'tt', 'others' ] + data + sigs :
                sname = degTools.sampleName( prompt_samp )
                slist = sampleNiceNames[ prompt_samp ] 
                prompt_fake_yields_all[flav][tight_region][ sname ] = degTools.dict_operator( yields_prompt , slist , func  = lambda *x: sum(x) if x else degTools.u_float(0) ) 
            prompt_fake_yields_all[flav][tight_region]['SimpleFakes'] = fakeEstimate
            prompt_fake_yields_all[flav][tight_region]['__Data_X_TL'] = fakeEstimateData
            prompt_fake_yields_all[flav][tight_region]['__Prompts_X_TL'] = fakeEstimatePrompts
            #print tight_region
            #print ['SimpleFakes']+[degTools.sampleName(s_) for s_ in ['w','tt','others']]
            #print [ prompt_fake_yields_all[flav][tight_region][x] for x in  ['SimpleFakes']+[degTools.sampleName(s_) for s_ in ['w','tt','others']]   ]
            prompt_fake_yields_all[flav][tight_region]['SimpleTotal'] = degTools.dict_operator( prompt_fake_yields_all[flav][tight_region] , ['SimpleFakes']+[degTools.sampleName(s_) for s_ in ['w','tt','others']] ) 
 


    #comb main SR1s
    for flav in ['mu', 'el']:
        #for main_region, sub_regions in main_sub_sr_regions_all.items():
        for main_region, sub_regions in card_regions_map.items():
            if main_region in  prompt_fake_yields_all[flav]:
                #print main_region
                continue #False
            #print main_region, sub_regions
            prompt_fake_yields_all[flav][main_region] = degTools.dict_manipulator(  
                                                    [ prompt_fake_yields_all[flav][r] for r in sub_regions ] , func = lambda *args: sum(args) )
    # combine for final regions
    for flav in ['mu', 'el']:
        for main_region, sub_regions in card_regions_map.items():
            prompt_fake_yields[flav][main_region] = degTools.dict_manipulator(
                                                    [ prompt_fake_yields_all[flav][r] for r in sub_regions ] , func = lambda *args: sum(args) )        

    prompt_fake_yields_all['lep'] = degTools.dict_manipulator( [prompt_fake_yields_all['mu'] , prompt_fake_yields_all['el']], degTools.yield_adder_func ) 
    prompt_fake_yields['lep'] = degTools.dict_manipulator( [prompt_fake_yields['mu'] , prompt_fake_yields['el']], degTools.yield_adder_func ) 


 


    ##
    ## Taking Care of Bins w Negative Fakes
    ##
    only_neg_bins = True

    sorted_fake_regions = regions_info.sort_regions( prompt_fake_yields['lep'].keys() )
    neg_bins = [ b for b in sorted_fake_regions if prompt_fake_yields['lep'][b]['SimpleFakes'].val - prompt_fake_yields['lep'][b]['SimpleFakes'].sigma <= 0 ] 


    bins_to_run_mlf_on = sorted_fake_regions if hasData else []
    if only_neg_bins:
        bins_to_run_mlf_on = neg_bins

    print "getting the fake ests from MLF for: %s"%bins_to_run_mlf_on

    fakeEstRes = getFakeEstimateParal( prompt_fake_yields['lep'], bins= bins_to_run_mlf_on , data_key = "__Data_X_TL", prompt_key = "__Prompts_X_TL" )
    #fakeEstRes = getFakeEstimateParal( prompt_fake_yields['lep'], bins=neg_bins, data_key = "__Data_X_TL", prompt_key = "__Prompts_X_TL" )
    simple_output              = fakeEstRes['simple_output']
    combine_output             = fakeEstRes['combine_output']
    #prompt_fake_yields['lep'] = combine_output
    
    for b in prompt_fake_yields['lep'].keys():
        #if not b in neg_bins:
        #    continue
        #print 'dealing with neg  bins', b, b in neg_bins

        # Symmetrizing the errors:


        if b in bins_to_run_mlf_on:
            if SYMMETRIZEFAKES:
                oldCentralVal = combine_output[b]['central'] 
                newCentralVal = (abs(combine_output[b]['up']) +  abs(combine_output[b]['down']) )/2
                diff          = newCentralVal - oldCentralVal
                newVals       = ( oldCentralVal + diff, combine_output[b]['up'] - diff, abs(combine_output[b]['down']) + diff )
                fake_val_from_fit  = degTools.u_float( *newVals[:2])
                #centralVal = max( combine_output[b]['central'], MINFAKEVAL )
                fake_val_from_fit = degTools.AsymFloatProxy( newVals[0] , newVals[1], newVals[1] ) ## I set up and down the same as a trick to force CombineCard  to use lnN
            else:
                oldCentralVal = combine_output[b]['central'] 
                newCentralVal = max( oldCentralVal , MINFAKEVAL )
                diff          = newCentralVal - oldCentralVal
                newVals       = ( oldCentralVal + diff, combine_output[b]['up'] - diff, abs(combine_output[b]['down']) + diff )
                fake_val_from_fit = degTools.AsymFloatProxy( *newVals )
            fake_val = fake_val_from_fit 
            if not simple_output[b]['obs-exp'].round(2).__str__() == prompt_fake_yields['lep'][b]['SimpleFakes'].round(2).__str__():
                print "!!!!!!!!!!!!!!!!"
                print simple_output[b]['obs-exp'].round(3).__str__(), prompt_fake_yields['lep'][b]['SimpleFakes'].round(3).__str__()
                print "!!!!!!!!!!!!!! THINGS DONT MATCH!!", b, simple_output[b], prompt_fake_yields['lep'][b]['SimpleFakes']
        else:
            fake_val = prompt_fake_yields['lep'][b]['SimpleFakes'] 
        #fake_val = prompt_fake_yields['lep'][b]['SimpleFakes'] if not b in neg_bins else fake_val_from_fit 
        prompt_fake_yields['lep'][b]['Fakes'] = fake_val 


    flav = "lep"
    #print neg_bins
    for tight_region  in sorted_fake_regions:
            ##print prompt_fake_yields[flav][tight_region]
            #print ['Fakes']+[degTools.sampleName(s_) for s_ in ['w','tt','others'] ]
            prompt_fake_yields[flav][tight_region]['Total'] = degTools.dict_operator( 
                                                                 prompt_fake_yields[flav][tight_region] ,
                                                                 ['Fakes']+[degTools.sampleName(s_) for s_ in ['w','tt','others']] ,
                                                                 lambda *x : sum([ convertAsymFloatToSym(v_, "max" ) for v_ in x ]) 
                                                        ) 

    print 'made it this far'
    if bins_to_run_mlf_on:
        simple_hist_allbins , combine_graph_allbins = compareCombineVsSimpleFakes( simple_output, combine_output  , bins = bins_to_run_mlf_on ) 
        simple_hist_negbins , combine_graph_negbins = compareCombineVsSimpleFakes( simple_output, combine_output  , bins = neg_bins) 
        ret['combine'] = [simple_hist_allbins , combine_graph_allbins,simple_hist_negbins , combine_graph_negbins,simple_output,combine_output] 

        canv = ROOT.TCanvas( "canv","canv", 1000,800)
        for bname, h,g in ( ("AllBins",simple_hist_allbins, combine_graph_allbins), ("NegBins", simple_hist_negbins, combine_graph_negbins) ):
            h.Draw("E2")
            g.Draw("p")
            degTools.saveCanvas( canv, saveDir, "Fakes_%s"%bname) 
    else:
        ret['combine'] = [None, None, None, None, None, None]


    #print prompt_fake_yields_all['mu'].keys()
    #print prompt_fake_yields_all['mu'][ prompt_fake_yields_all['mu'].keys()[4] ] .keys()
    #for flav in prompt_fake_yields_all.keys():
    #    for b in prompt_fake_yields_all[flav].keys():
    #        if "Fakes" not in prompt_fake_yields_all[flav][b].keys():
    #            print flav, b
        
    fake_yields_summary_all = { flav:{b:prompt_fake_yields_all[flav][b]['SimpleFakes'] for b in prompt_fake_yields_all[flav].keys()} for flav in ['mu','el', 'lep']  }
    fake_yields_summary     = { flav:{b:prompt_fake_yields[flav][b]['SimpleFakes'] for b in prompt_fake_yields[flav].keys()} for flav in ['mu','el', 'lep']  }

    outputDir = cfg.results_dir+"/"+cfg.baseCutSaveDir
    pickle.dump( fake_yields_summary, file("%s/fake_yields_summary_%s.pkl"%( outputDir, cutName) ,"w"))
    pickle.dump( prompt_fake_yields_all, file("%s/yields_summary_allregions_%s.pkl"%(outputDir , cutName) ,"w"))
    pickle.dump( prompt_fake_yields, file("%s/yields_summary_%s.pkl"%(outputDir, cutName),"w"))
    print "FakeEstimation Results:\n %s"%outputDir


    ret.update({
            'FR_regions_dict'    : FR_dicts,
            'fake_yields_summary': fake_yields_summary,
            #'prompt_fake_yields_all' : prompt_fake_yields_all, 
            'prompt_fake_yields' : prompt_fake_yields, 
            'FRs':FR_pkls ,
            'regions_info':regions_info  ,
          })
    pickle.dump( ret, file( '%s/fakeEstimateOutput_%s.pkl'%(outputDir, cutName) , "w") )

    return ret

if __name__ == "__main__":
    ## after running degStop.py
    fakeEstimateOutput = fakeEstimate(cfg,args)
 
