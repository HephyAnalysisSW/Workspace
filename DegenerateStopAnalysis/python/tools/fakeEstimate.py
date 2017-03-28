
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
import Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo as sampleInfo
import pickle
#sig2           =   'T2-4bd-300-220'
#sig1           =   'T2-4bd-300-270'

#ylds     = pickle.load( file(cfg.yieldPkls[ cfg.cutInstList[0].fullName]) )


bin_FR_basic_map = {
                         'ptVL' : [ 'r1vla', 'r1vlb', 'r1vlc' , 'r2vl' ] ,
                         'ptL'  : [ 'r1la',  'r1lb' , 'r1lc'  , 'r2l'  ] ,
                         'ptM'  : [ 'r1ma',  'r1mb' , 'r1mc'  , 'r2m'  ] ,
                         'ptH'  : [ 'r1ha',  'r1hb' , 'r1hc'  , 'r2h'  ] ,
                     'pt_gt_30' : [ 'cr1', 'cr2' , 'crtt', ] ,
                       }

bin_mt_map = {
                         'r1a' : [ 'r1vla', 'r1la' , 'r1ma' , 'r1ha' ] ,
                         'r1b' : [ 'r1vlb', 'r1lb' , 'r1mb' , 'r1hb' ] ,
                         'r1c' : [ 'r1vlc', 'r1lc' , 'r1mc' , 'r1hc' ] ,
                         'r2'  : [ 'r2vl' , 'r2l'  , 'r2m'  , 'r2h' ] ,
                       }

def findPtBinFromRegionName( region_name, ptBinRegionMap = bin_FR_basic_map ):
    foundIt = None
    for ptb, region_templates in ptBinRegionMap.items():
        if degTools.anyIn( region_templates , region_name):
            if foundIt:
                raise Exception("Had already found this (%s), but now found this one (%s) too!!"%(foundIt, ptb))
            else:
                foundIt = ptb 
    return foundIt    


bin_FR_basic_map = {
                         'ptVL' : [ 'r1vla', 'r1vlb', 'r1vlc' , 'r2vl' ] ,
                         'ptL'  : [ 'r1la',  'r1lb' , 'r1lc'  , 'r2l'  ] ,
                         'ptM'  : [ 'r1ma',  'r1mb' , 'r1mc'  , 'r2m'  ] ,
                         'ptH'  : [ 'r1ha',  'r1hb' , 'r1hc'  , 'r2h'  ] ,
                     'pt_gt_30' : [ 'cr1', 'cr2' , 'crtt', ] ,
                       }




def fakeEstimate( cfg, args ):
    """
        Calculate contribution due to fake backgrounds
        Need to have el, mu yields, and the FRs
    """


    yld_pkl_file_lep   = cfg.yieldPkls[ cfg.cutInstList[0].fullName]
    saveDir            = cfg.saveDirs[cfg.cutInstList[0].fullName ]
    if not "lep" in yld_pkl_file_lep or 'loose' in yld_pkl_file_lep:
        raise Exception("Run with the lep=lep option")
    
    
    yld_pkls_files = {
                       'lep': yld_pkl_file_lep , 
                        'mu': yld_pkl_file_lep.replace("lep", "mu") ,
                        'el': yld_pkl_file_lep.replace("lep", "el") ,
                     }
    
    FR_file_template = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/final/{cmgTag}/{ppTag}/measurement1/tightToLooseRatio_measurement1_data-EWK_%s.pkl".format(cmgTag = cfg.cmgTag, ppTag = cfg.ppTag)
    
    flavors = ['mu', 'el']
    FR_pkls_files = { flav: FR_file_template%flav for flav in flavors }
    FR_pkls     = degTools.dict_function( FR_pkls_files  , lambda f: pickle.load(file(f)) )
    
    
    
    
    yld_pkls    = degTools.dict_function( yld_pkls_files , lambda f: pickle.load(file(f)) ) 
    yld_dicts   = degTools.dict_function( yld_pkls       , lambda yld: yld.getNiceYieldDict() ) 
    yldsByBin   = degTools.dict_function( yld_pkls       , lambda yld: yld.getByBins( yld.getNiceYieldDict()) ) 
    
    
    ylds_lep = yld_pkls['lep']
    
    LnTTag = "_LnT"
    all_regions = ylds_lep.cutNames
    LnT_regions = [ x for x in all_regions if LnTTag in x]
    tight_regions = [ x for x in all_regions if LnTTag not in x] 
    sr_pt_regions = [x for x in tight_regions if 'sr' in x]
    
    main_sub_regions = {}
    for region in sr_pt_regions:
        mtr_ = findPtBinFromRegionName(region,  ptBinRegionMap = bin_mt_map)
        if not mtr_:
            print region
            continue
        prefix = region.split('r')[0]
        mtr = prefix + mtr_
        if not main_sub_regions.has_key(mtr):
            main_sub_regions[mtr] = []
        main_sub_regions[mtr].append( region ) 
    
    tight_LnT_map = { lnt.replace(LnTTag,""):lnt for lnt in LnT_regions }
    
    
    sampleNames = ylds_lep.sampleNames
    bkgList  = ylds_lep.bkgList
    w        = [bkg for bkg in bkgList if 'w' in bkg]
    tt       = [bkg for bkg in bkgList if 'tt' in bkg]
    others   = [bkg for bkg in bkgList if bkg not in w+tt]
    sigs     = ylds_lep.sigList
    data     = ylds_lep.dataList
    
    samps = {
             'w'     : w        ,
             'tt'    : tt       ,
             'others': others   ,
             'sigs'  : sigs     ,
             'data'  : data     ,
            data[0]  : data     ,
          't2tt300_270' : ['t2tt300_270'], 
            }
    
    def getRegionFakeEstimate( binYlds ,  FR ):
        return degTools.dict_operator( binYlds, sampleNiceNames['data'] + ['Total'] , lambda data, prompts  : (data-prompts) * FR/(degTools.u_float(1)-FR) )
    sampleNiceNames = { s: [ sampleNames[s_] for s_ in samps[s] ]  for s in samps}
    
    flav = 'lep'
    
    
    sig = [ "t2tt300_270" ]
    
    prompt_fake_yields = {'mu':{},'lep':{}, 'el':{}}
    
    for tight_region , LnT_region in tight_LnT_map.iteritems():
        for flav in ['mu', 'el']:
            yields_LnT      = yldsByBin[flav][LnT_region] 
            yields_prompt   = yldsByBin[flav][tight_region] 
            ptBin        = findPtBinFromRegionName( LnT_region)
            if not ptBin:
                print flav, LnT_region
                continue
            FR           = FR_pkls[flav].get(ptBin)
            #assert FR.val > 0 , "Negative FakeRate %s"%FR
            if not FR:
                print "no FR found", flav, LnT_region, ptBin
                FR = degTools.u_float(0,0)
            fakeEstimate = getRegionFakeEstimate( yields_LnT , FR)
            #fakeEstimate = degTools.u_float( 0 ) if  fakeEstimate.val < 0 else fakeEstimate 
            #fakeEstimate = degTools.u_float( 0 ) if  fakeEstimate.val < 0 else fakeEstimate 
            prompt_fake_yields[flav][tight_region] = {}
            for prompt_samp in ['w', 'tt', 'others' ] + data + ['t2tt300_270'] :
                sname = sampleInfo.sampleName( prompt_samp )
                slist = sampleNiceNames[ prompt_samp ] 
                prompt_fake_yields[flav][tight_region][ sname ] = degTools.dict_operator( yields_prompt , slist ) 
            prompt_fake_yields[flav][tight_region]['Fakes'] = fakeEstimate
            prompt_fake_yields[flav][tight_region]['Total'] = degTools.dict_operator( prompt_fake_yields[flav][tight_region] , ['Fakes']+[sampleInfo.sampleName(s_) for s_ in ['w','tt','others']] ) 
    #comb SR1s
    for flav in ['mu', 'el']:
        for main_region, sub_regions in main_sub_regions.items():
            prompt_fake_yields[flav][main_region] = degTools.dict_manipulator(  
                                                    [ prompt_fake_yields[flav][r] for r in sub_regions ] , func = lambda *args: sum(args) )


    prompt_fake_yields['lep'] = degTools.dict_manipulator( [prompt_fake_yields['mu'] , prompt_fake_yields['el']], degTools.yield_adder_func ) 
    fake_yields_summary = { flav:{b:prompt_fake_yields[flav][b]['Fakes'] for b in prompt_fake_yields[flav].keys()} for flav in ['mu','el', 'lep']  }

    outputDir = cfg.results_dir+"/"+cfg.baseCutSaveDir
    pickle.dump( fake_yields_summary, file("%s/fake_yields_summary.pkl"%outputDir,"w"))
    pickle.dump( prompt_fake_yields, file("%s/yields_summary.pkl"%outputDir,"w"))
    print "FakeEstimation Results:\n %s"%outputDir


    ret = {
            'fake_yields_summary': fake_yields_summary,
            'prompt_fake_yields' : prompt_fake_yields, 
            'FRs':FR_pkls
          }

    return ret

if __name__ == "__main__":
    ## after running degStop.py
    fakeEstimateOutput = fakeEstimate(cfg,args)
    
    
    if False:
        prompt_fake_yields = fakeEstimateOutput['prompt_fake_yields']
        

        sample_list = prompt_fake_yields['lep']['vcr1a'].keys()
        yldByBin  = prompt_fake_yields['lep']
        yieldDict = { samp: { b: yldByBin[b][samp] for b in yldByBin.keys()}  for samp in sample_list}
        bkgList= ["WJets","TTJets","Fakes", "Others" ]#,"Others"] 
        
        from Workspace.DegenerateStopAnalysis.tools.CombineCard import CombinedCard
        map_name_niceName  = {
                          'w'       :  'WJets'      ,
                          'tt'      :  'TTJets'   ,
                          'z'       :  'ZJetsInv' ,
                          'qcd'     :  'QCD'     ,
                          'dy'      :  'DYJetsM50',
                          'vv'      :  'Diboson'  ,
                          'st'      :   'ST'      ,
                          #'other'   :   'Other'      ,
                          }
        niceProcessNames = map_name_niceName
    
        bins_order = tight_LnT_map.keys()
        CombineCard = Workspace.DegenerateStopAnalysis.tools.CombineCard.CombinedCard 
        cfw   =  CombinedCard( niceProcessNames = niceProcessNames  );
        cfw.addBins( bkgList , yieldDict['WJets'].keys() )
    
        cfw.specifyObservations(           yieldDict , "DataBlind")
        cfw.specifyBackgroundExpectations( yieldDict , bkgList )
        cfw.specifySignalExpectations(     yieldDict , "T2tt300_270"  )
        cfw.specifyUncertaintiesFromDict( {'wpt':syst_dict}, ['wpt'], bkgList)
        #cfw.addStatisticalUncertainties(yieldDict= yieldDict)
        cfw.writeToFile("testcard.txt")
