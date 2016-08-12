import pickle
import os
#from Workspace.DegenerateStopAnalysis.tools.degTools import fixForLatex, dict_manipulator, Yield
from Workspace.DegenerateStopAnalysis.tools.degTools import fixForLatex , u_float, dict_manipulator, makeSimpleLatexTable, dict_operator, drawYields, setup_style#, dict_manipulator, Yield
from copy import deepcopy
import math
relsys = lambda a,b : abs(1.- (a/b).val) if b.val else 0

results_path = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/BkgSysts/"
#yields_pkl   = "/afs/hephy.at/work/n/nrad/results/cards_and_limits/8011_mAODv2_v1/80X_postProcessing_v6/13TeV/HT/PreApp_Mt95_Inccharge_LepAll_lep_pu_SF/AdjustedSys/presel/Yields_12864pbm1_PreApp_Mt95_Inccharge_LepAll_lep_pu_SF_presel_BinsSummary.pkl"
yields_pkl   = "/afs/hephy.at/work/n/nrad/results/cards_and_limits/8011_mAODv2_v1/80X_postProcessing_v6/13TeV/HT/PreApp_Mt95_Inccharge_LepAll_lep_pu_SF/AdjustedSys/presel/Yields_4303pbm1_PreApp_Mt95_Inccharge_LepAll_lep_pu_SF_presel_SRs_PtBinnedSum.pkl"

lumitag_ = [x for x in yields_pkl.rsplit("_") if 'pbm1' in x]
if not len(lumitag_)==1:
    raise Exception("cant determine lumitag from the pickle yield")
lumitag = lumitag_[0]
if lumitag == "4303pbm1":   
    blinded = True
else:
    blinded = False


tt_sf     = u_float(0.72,0.2) 
w_sf_sr1a = u_float(0.99,0.04) 
w_sf_sr1b = u_float(0.96,0.05) 
w_sf_sr1c = u_float(1.24,0.07) 
w_sf_sr2  = u_float(0.91,0.08) 


tt             =   'TTJets'
w              =   "WJets"
qcd            =   "QCD"
z              =   "ZJetsInv"
otherBkg       =   ['DYJetsM50' , "ST", "Diboson"]
mainBkg        =   [w,tt,z,qcd]
allBkg         =   [w,tt, z, qcd] + otherBkg



 
CR_SFs={ 
 'SRL1a':{qcd:1.0 , z:1.0 , w: w_sf_sr1a , tt: tt_sf }, 
 'SRH1a':{qcd:1.0 , z:1.0 , w: w_sf_sr1a , tt: tt_sf }, 
 'SRV1a':{qcd:1.0 , z:1.0 , w: w_sf_sr1a , tt: tt_sf }, 
 'SR1a' :{qcd:1.0 , z:1.0 , w: w_sf_sr1a , tt: tt_sf }, 
 'SRL1b':{qcd:1.0 , z:1.0 , w: w_sf_sr1b , tt: tt_sf }, 
 'SRH1b':{qcd:1.0 , z:1.0 , w: w_sf_sr1b , tt: tt_sf }, 
 'SRV1b':{qcd:1.0 , z:1.0 , w: w_sf_sr1b , tt: tt_sf }, 
 'SR1b' :{qcd:1.0 , z:1.0 , w: w_sf_sr1b , tt: tt_sf }, 
 'SRL1c':{qcd:1.0 , z:1.0 , w: w_sf_sr1c , tt: tt_sf }, 
 'SRH1c':{qcd:1.0 , z:1.0 , w: w_sf_sr1c , tt: tt_sf }, 
 'SRV1c':{qcd:1.0 , z:1.0 , w: w_sf_sr1c , tt: tt_sf },
 'SR1c' :{qcd:1.0 , z:1.0 , w: w_sf_sr1c , tt: tt_sf },
 'SRL2' :{qcd:1.0 , z:1.0 , w: w_sf_sr2  , tt: tt_sf },
 'SRH2' :{qcd:1.0 , z:1.0 , w: w_sf_sr2  , tt: tt_sf },
 'SRV2' :{qcd:1.0 , z:1.0 , w: w_sf_sr2  , tt: tt_sf },
 'SR2'  :{qcd:1.0 , z:1.0 , w: w_sf_sr2  , tt: tt_sf },
}









regions =  [\
             'SRL1a',
             'SRH1a',
             'SRV1a',
             '\hline',
             'SR1a',
             '\hline',
             'SRL1b',
             'SRH1b',
             'SRV1b',
             '\hline',
             'SR1b',
             '\hline',
             'SRL1c',
             'SRH1c',
             'SRV1c',
             '\hline',
             'SR1c',
             '\hline',
             'SRL2',
             'SRH2',
             'SRV2',
             '\hline',
             'SR2',
             '\hline',
             '\hline',
             'CR1a',
             'CR1b',
             'CR1c',
             'CR2',
             'CRTT2',
            ]

bins = [x for x in regions if 'hline' not in x]


main_sr =[
            'SR1a',
            'SR1b',
            'SR1c',
            'SR2',
         ]

main_cr =[
            'CR1a',
            'CR1b',
            'CR1c',
            'CR2',
         ]



pt_srs = [x for x in bins if 'SR' in x and x not in main_sr]










systs_pkl_dict = {
                    'JEC'    : 'JEC.pkl',
                    'JER'    : 'JER.pkl',
                    'Bb'     : 'BTag_b.pkl',
                    'Bl'     : 'BTag_l.pkl',
                    'BTag'   : 'BTag.pkl',
                    'ttpt Reweight'   : 'ttpt.pkl',
                    'ttptTT' : 'ttpt_ttonly.pkl',
                    'WptW'   : 'Wpt_wonly.pkl',
                    'Wpt Reweight'    : 'Wpt_fullbkg.pkl', 
                }

yld = pickle.load(file(yields_pkl))
yieldDict = yld.getNiceYieldDict()
bkgList = ['Total', 'WJets' ]


flat_systs = { 
                'lepEff': 5.,
                'Lumi': 6.2,
             }




lepEff={}
lumiUnc={}
wptShape_bins ={ '1a': 10 , '1b': 20, '1c':30, '2':20}
ttptShape_bins={ '1a': 20 , '1b': 20, '1c':20, '2':20}

wptShape_uncert = {}
ttptShape_uncert = {}



#
#   Propegating shape systematics to the total bkg yield
#
for b in bins:
    lepEff[b]=flat_systs['lepEff']
    lumiUnc[b]=flat_systs['Lumi']
    for wptbin in wptShape_bins:
        if wptbin in b:
            if wptShape_uncert.get(b): raise Exception("Multiple matching Bins!!! %s,%s"%(wptShape_bins, bins))
            wptShape_uncert[b]=wptShape_bins[wptbin]
    if not wptShape_uncert.get(b): raise Exception("No Match found!")
    for ttptbin in ttptShape_bins:
        if ttptbin in b:
            if ttptShape_uncert.get(b): raise Exception("Multiple matching Bins!!! %s,%s"%(ttptShape_bins, bins))
            ttptShape_uncert[b]=ttptShape_bins[ttptbin]
    if not ttptShape_uncert.get(b): raise Exception("No Match found!")




tot_wpt_up     = dict_manipulator( [yieldDict['Total'], yieldDict['WJets'], wptShape_uncert ], lambda a,b,c:a-b + (1+c/100.)*b )
tot_wpt_down   = dict_manipulator( [yieldDict['Total'], yieldDict['WJets'], wptShape_uncert ], lambda a,b,c:a-b + (1-c/100.)*b )
tot_wpt_uncert = dict_manipulator( [ tot_wpt_up, tot_wpt_down ,  yieldDict['Total']], lambda a,b,c:   ( relsys(a,c) + relsys(b,c))/2. * 100  ) 


tot_ttpt_up     = dict_manipulator( [yieldDict['Total'], yieldDict['TTJets'], ttptShape_uncert ], lambda a,b,c:a-b + (1+c/100.)*b )
tot_ttpt_down   = dict_manipulator( [yieldDict['Total'], yieldDict['TTJets'], ttptShape_uncert ], lambda a,b,c:a-b + (1-c/100.)*b )
tot_ttpt_uncert = dict_manipulator( [ tot_ttpt_up, tot_ttpt_down ,  yieldDict['Total']], lambda a,b,c: ( relsys(a,c) + relsys(b,c))/2. * 100  ) 


ZInvUncert = 0.5
tot_zinv_up      =  dict_manipulator( [yieldDict['Total'], yieldDict['ZJetsInv'] ], lambda a,b: a-b + ((1+ZInvUncert)*b)  )
tot_zinv_down    =  dict_manipulator( [yieldDict['Total'], yieldDict['ZJetsInv'] ], lambda a,b: a-b + ((1-ZInvUncert)*b)  )
tot_zinv_uncert  =  dict_manipulator( [ tot_zinv_up, tot_zinv_down, yieldDict['Total'] ], lambda a,b,c: ( relsys(a,c) + relsys(b,c))/2. * 100)  

qcdUncert = 0.3
tot_qcd_up      =  dict_manipulator( [yieldDict['Total'], yieldDict['QCD'] ], lambda a,b: a-b + ((1+qcdUncert)*b)  )
tot_qcd_down    =  dict_manipulator( [yieldDict['Total'], yieldDict['QCD'] ], lambda a,b: a-b + ((1-qcdUncert)*b)  )
tot_qcd_uncert  =  dict_manipulator( [ tot_qcd_up, tot_qcd_down, yieldDict['Total'] ], lambda a,b,c: ( relsys(a,c) + relsys(b,c))/2. * 100)  



systs_for_sum = ['JEC','JER', 'BTag','ttpt Reweight', 'Wpt Reweight' ] 



def addInQuad(l):
    s = 0
    for v in l:
        s += v**2
    return math.sqrt(s) 



summary_systs = {}
for syst_name in systs_for_sum:
    pkl_file    =   os.path.expandvars( results_path) +"/"+ systs_pkl_dict[syst_name]
    summary_systs[syst_name] = pickle.load(file(pkl_file))


summary_systs['QCDEst']   = tot_qcd_uncert
summary_systs['ZInvEst']   = tot_zinv_uncert
summary_systs['WPtShape']   = tot_wpt_uncert
summary_systs['ttPtShape']  = tot_ttpt_uncert
summary_systs['Lep. Eff']     = lepEff
summary_systs['Lumi']     = lumiUnc

other_corr_systs = ['Lep. Eff', 'Lumi']
uncorr_systs = [ 'WPtShape' , 'ttPtShape' , 'ZInvEst', 'QCDEst']

import numpy as np

total_systs = {}
allsysts = systs_for_sum + other_corr_systs + uncorr_systs
for region in bins:
    total_systs[region] = addInQuad([ summary_systs[syst_name][region] for syst_name in allsysts if region in summary_systs[syst_name] ] )


if __name__ == "__main__":

    first_row = True
    table_list = []
    nptable = np.array([])
    main_sr_table = []
    for region in regions:
            if not 'SR' in region: continue
            isMainSR = True if region in main_sr else False

            if region == "\hline":
                table_list.append([region])
                continue
            toPrint = [
                          ["Region"                     ,  fixForLatex( region )         ],
                       ]
            for syst_name in systs_for_sum + other_corr_systs:
                toPrint.append( [  syst_name , round (summary_systs[syst_name][region],1) ] )
            for syst_name in uncorr_systs:
                toPrint.append( [  syst_name , round (summary_systs[syst_name][region],1) ] )
            toPrint.append( [  'Total' , round ( total_systs[region] ,1) ] )

            align = "{:<20}"*len(toPrint)
            if first_row:
                print align.format(*[x[0] for x in toPrint])
                first_row = False
                table_list.append( [x[0] for x in toPrint]  )
                main_sr_table.append( [x[0] for x in toPrint] )
            print align.format(*[x[1] for x in toPrint])
            table_list.append( [x[1] for x in toPrint])
            if isMainSR: main_sr_table.append( [x[1] for x in toPrint] )
            
                    
    #nptable = np.concatenate( [ [x] for x in table_list if 'hline' not in x[0]]  )
    main_sr_nptable = np.concatenate( [ [x] for x in main_sr_table if 'hline' not in x[0]]  )

    saveDirBase = "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/8011_mAODv2_v1/80X_postProcessing_v6/SUS_16_031_v0_3/"
    table = makeSimpleLatexTable( table_list, "SystsSummary_%s.tex"%lumitag, saveDirBase+"/Results/", align_char = "c"        ,  align_func= lambda char, table: "c|"+ (char *(len(table[1])-2)).rstrip("|") + "|c" )

    main_sr_nptable_T = main_sr_nptable.T
    main_sr_nptable_T[0][0]='Syst'
    SRtable = makeSimpleLatexTable( main_sr_nptable_T, "SystsSummaryMainSRs_%s.tex"%lumitag, saveDirBase+"/Results/", align_char = "c"        ,  align_func= lambda char, table: "c|"+ (char *(len(table[1])-1)).rstrip("|") )








    ##
    ##  Final Result Table
    ##

    finalYields  = deepcopy(yieldDict)
    yldsByBins   = yld.getByBins(yieldDict=yieldDict)

    finalYieldDict = {}
    for bkg in allBkg + ['Total']:
        finalYieldDict[bkg]= deepcopy( finalYields[bkg] )

    qcdEst= pickle.load(file("/afs/hephy.at/user/m/mzarucki/public/QCDsystematics_combined.pkl"))
    #for b, val in qcdEst.iteritems():
    #    finalYieldDict['QCD'][b]= u_float( val['val'], val['stat'] ) 
    finalYieldDict['Data'] = {}

    first_row = True
    result_table_list = []
    for region in regions:
            if region == "\hline":
                result_table_list.append([region])
                continue
            if not 'SR' in region: 
                continue
            otherTotal     = dict_operator ( yldsByBins[region] , keys =  otherBkg  , func = lambda *a: sum( a ).round(2)     )
            estTotal     = dict_operator ( yldsByBins[region] , keys = [ w, tt, z, qcd ] + otherBkg  , func = lambda a,b,c,d, *e: a*CR_SFs[region][w] + b*CR_SFs[region][tt] + c*CR_SFs[region][z] + d*CR_SFs[region][qcd]  + sum( e )     )
            mcTotal      = yldsByBins[region]['Total']
            toPrint = [
                          ["Region"     ,  fixForLatex( region )],
                      ]

            for bkg in ['QCD']:
                if region in qcdEst:
                    val = qcdEst[region]
                    if blinded:
                        val['val'] = val['val']*4.3/12.9 
                        val['stat'] = val['stat']*4.3/12.9
                    finalYieldDict[bkg][region] = u_float(val['val'], val['stat'] )
                    finalYields[bkg][region] = u_float(val['val'], val['stat'] )
                    yldsByBins[region][bkg] = u_float(val['val'], val['stat'] )
                    print ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;",region, yldsByBins[region][bkg]
    
            for bkg in mainBkg:
                SF = 1.0
                SF = CR_SFs[region][bkg]
                bkgYld  = (yldsByBins[region][bkg]*SF).round(2)
                #if bkg =="QCD" and region=="SR1c":
                #    assert False, bkgYld
                #bkgFracInv = estTotal.val /bkgYld.val if bkgYld.val else 0 
                bkgFrac = (2*estTotal.val- bkgYld.val)/estTotal.val if bkgYld.val else 0 
                bkgSyst = round( bkgFrac*    bkgYld.val * 1/100. * total_systs[region] ,2)
                finalYieldDict[bkg][region] = bkgYld + u_float(0, bkgSyst ) 
                toPrint.append( [bkg        ,   (yldsByBins[region][bkg]*SF).round(2).__str__()+"+-%s"%bkgSyst ]         ) 
            for bkg in otherBkg:
                bkgYld  = (yldsByBins[region][bkg]).round(2)
                bkgFrac = (2*estTotal.val- bkgYld.val)/estTotal.val if bkgYld.val else 0 
                bkgSyst = round( bkgFrac*    bkgYld.val * 1/100. * total_systs[region] ,2)
                finalYieldDict[bkg][region] = bkgYld + u_float(0, bkgSyst ) 


            otherFrac = (2*estTotal.val- otherTotal.val)/estTotal.val if otherTotal.val else 0 
            toPrint.append(     ["Other"    ,   otherTotal.__str__() + "+-%s"%round( otherFrac,2) ]                                    ) 
            #toPrint.append(    ["M.C. Total", mcTotal ]  )
            tot_rel_sys = estTotal.val * 1/100.* total_systs[region] 
            toPrint.append(     ["S.M Est." ,   estTotal.round(2).__str__() + "+-%s"%round( estTotal.val * 1/100.* total_systs[region],2) ]                              ) 
            finalYieldDict['Total'][region] = estTotal +u_float(0, tot_rel_sys)
            if blinded:
                observed     = int( yldsByBins[region]['DataUnblind'].val)
                toPrint.append( ["Data (4.3$fb^{-1}$)", observed] )
                finalYieldDict["Data"][region] = u_float(observed,math.sqrt( observed ) )
            align = "{:<20}"*len(toPrint)
            if first_row:
                print align.format(*[x[0] for x in toPrint])
                first_row = False
                result_table_list.append( [x[0] for x in toPrint]  )
    
            print align.format(*[x[1] for x in toPrint])
            result_table_list.append( [x[1] for x in toPrint])

    ResTable = makeSimpleLatexTable( result_table_list, "BkgEstSRSummary_%s.tex"%lumitag, saveDirBase+"/Results/", align_char = "r"        ,  align_func= lambda char, table: "r|"+ (char *(len(table[1])-1)).rstrip("|") )


    
    if blinded:
        setup_style()
        plt1= drawYields("Results_SRsPtBinned_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = pt_srs, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] )
        plt2= drawYields("Results_MainSRs_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = main_sr, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] )
        plt3= drawYields("Results_NoLog_SRsPtBinned_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = pt_srs, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] , logs=[0,0])
        plt4= drawYields("Results_NoLog_MainSRs_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = main_sr, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] , logs=[0,0])

