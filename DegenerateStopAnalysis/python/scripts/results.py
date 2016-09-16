import pickle
import os
#from Workspace.DegenerateStopAnalysis.tools.degTools import fixForLatex, dict_manipulator, Yield
from Workspace.DegenerateStopAnalysis.tools.degTools import makeDir, fixForLatex , u_float, make_dict_manipulator , dict_manipulator, makeSimpleLatexTable, dict_operator, drawYields, setup_style#, dict_manipulator, Yield
from Workspace.DegenerateStopAnalysis.scripts.BkgSysts.Systematics import regions, main_cr, main_sr, bins , card_bins, pt_srs , getPkl, tagParams, Systematics
from copy import deepcopy
import math
import numpy

relsys = lambda a,b : abs(1.- (a/b).val) if b.val else 0


def applySyst(value, syst) :
    """ syst should be in percent """
    for v in [value, syst]:
        if not hasattr(v,"val"):
            v = u_float(v)
    print value, syst
    return value  


import itertools
def addInQuad(l):
    s = 0
    for v in l:
        s += v**2
    return math.sqrt(s) 
def addInQuad100PerctCorr(l):
    s = 0
    for v in l:
        s += v**2
    chi = 0
    for e1,e2 in itertools.combinations(l,2):
        print e1,e2
        chi += e1*e2
    chi = 2*chi
    print 'math.sqrt(%s+%s)'%(s,chi)
    return math.sqrt(s+chi) 



fixSystNameDict={
                'ttPtShape': "CR/SF transf. fact. W",
                'WPtShape' : "CR/SR transf. fact. tt",
                'ttpt'     : "tt $p_{T}$",
                'WPt'      : "W $p_{T}$",
                'jec'      : "JEC",
                'jer'      : "JER",
            'DYJetsM50XSec': 'Drell-Yan xsec',
            'STXSec'       : 'Single top xsec',
            'DibosonXSec'  : 'Diboson xsec',
            'ZInvEst'      : '$Z_{Inv}$ estimation',
            'QCDEst'       : 'QCD estimation',
            'lepEff'       : "Lepton efficiency" ,
            'PU'           : "Pile-up",
            }
def fixSystName(name):
    return fixSystNameDict.get(name,name)
    






try:
    cfg
except NameError:
    raise Exception("Run this script after loading the cfg")



tt             =   'TTJets'
w              =   "WJets"
qcd            =   "QCD"
z              =   "ZJetsInv"
total          =   "Total"
otherBkg       =   ['DYJetsM50' , "ST", "Diboson"]
mainBkg        =   [w,tt,z,qcd]
allBkg         =   [w,tt, z, qcd] + otherBkg

cut_name = 'presel_BinsSummary'
yields_pkl   = cfg.yieldPkls[cut_name]
#yields_pkl   = "/afs/hephy.at/work/n/nrad/results/cards_and_limits/8011_mAODv2_v1/80X_postProcessing_v6/13TeV/HT/PreApp_Mt95_Inccharge_LepAll_lep_pu_SF/AdjustedSys/presel/Yields_12864pbm1_PreApp_Mt95_Inccharge_LepAll_lep_pu_SF_presel_BinsSummary.pkl"
#yields_pkl   = "/afs/hephy.at/work/n/nrad/results/cards_and_limits/8011_mAODv2_v1/80X_postProcessing_v6/13TeV/HT/PreApp_Mt95_Inccharge_LepAll_lep_pu_SF/AdjustedSys/presel/Yields_4303pbm1_PreApp_Mt95_Inccharge_LepAll_lep_pu_SF_presel_SRs_PtBinnedSum.pkl"

lumitag_ = [x for x in yields_pkl.rsplit("_") if 'pbm1' in x]
if not len(lumitag_)==1:
    raise Exception("cant determine lumitag from the pickle yield")
lumitag = lumitag_[0]
if lumitag == "4303pbm1":   
    blinded = True
elif lumitag == "12864pbm1":
    blinded = False

lepCol = None
for lc in ["LepAll","LepGood","LepOther"]:
    if lc in cfg.runTag:
        lepCol = lc
if not lepCol: raise Exception("No LepCol")
    
lep = None
for l in ["lep", "mu", "el"]:
    if l in cfg.runTag:
        lep = l
if not lep: raise Exception("No Lep")



saveDirBase  = cfg.saveDir
#saveDirBase = "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/8011_mAODv2_v1/80X_postProcessing_v6/SUS_16_031_v0_3/"



#results_path = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/BkgSysts/" + cfg.runTag
#results_path = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/BkgSysts/%s_%s_%s/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag)

base_res_path = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s/%s/%s/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag)
base_res_path = os.path.expandvars(base_res_path)
bkg_est_path  = "%s/BkgEst"%base_res_path
bkg_systs_path  = "%s/BkgSysts"%base_res_path
sig_systs_path  = "%s/SigSysts"%base_res_path


dict_pkls = {
            'bkg_pred'      :"BkgPredWithVars.pkl"          ,
            'bkg_sfs'       :"BkgSFs.pkl"                   ,
            'card_systs'    :"SystDictForCards.pkl"         ,
            'syst_dict'     :"SystDict.pkl"                 ,   
            'bkg_mctruth'   :"YieldDictWithVars.pkl"        ,
        }

dicts={}
for name, pkl in dict_pkls.iteritems():
    pkl_path    = base_res_path +"/" + pkl
    dicts[name] = getPkl( pkl_path )
    #dicts[name] = pickle.load( file(pkl_path)) 

yld = getPkl( base_res_path + "/YieldInsts/YieldInst_PU_central.pkl" )

systs     = dicts['syst_dict']
syst_list = dicts['syst_dict'].keys()
corr_systs_original   = ['PU','jec' , 'jer', 'BTag_l', 'BTag_b' , 'lepEff', 'WPt', 'ttpt']
uncorr_systs_original = ['WPtShape', 'ttPtShape', 'QCDEst', 'ZInvEst','STXSec', 'DYJetsM50XSec', 'DibosonXSec',  ]
signal_systs          = ['Lumi', ]  
#uncorr_systs_original =

corr_systs_list = [x for x in corr_systs_original if x in syst_list ] 
uncorr_systs_list= [x for x in uncorr_systs_original if x in syst_list and not x == "central" and not x =="Lumi" and not x=='SmallBkg']




sig_systs = ['jer','jec', 'PU', 'Lumi', 'Btag_b', 'BTag_l', 'lepEff', ] # QCD, FastSim/FullSim SF


yieldDictCentral = dicts['bkg_pred']['PU_central']
sampleList       = [x for x in yieldDictCentral.keys() if "FOM" not in x]
dataList         = [x for x in sampleList if "data" in x.lower() ] 
sigList          = [x for x in sampleList if ("T2tt" in x or "SMS" in x)]
bkgTotList       = [x for x in sampleList if x not in dataList and x not in sigList ]
sortlist         = ['WJets', 'TTJets', 'ZJetsInv', 'QCD', 'DYJetsM50', 'Diboson', 'ST', "Total"]
bkgTotList       = sortBy(bkgTotList, sortlist, reverse=False)
bkgList          = [x for x in bkgTotList if "Total" not in x]

import numpy as np

#total_systs_uncorr = {}
#total_systs  = {}
#corr_systs   = [ x for x in systs.keys() if any( [y.lower() in x.lower() for y in corr_systs_list])      ]
#uncorr_systs = [ x for x in systs.keys() if any( [y.lower() in x.lower() for y in uncorr_systs_list])    ]


#
#   Combining Systs for Bkg and Signal
#

total_syst_labels = ["%s_CorrSysts"%total, "%s_UncorrSysts"%total, "%s_Systs"%total]
for total_syst_label in total_syst_labels:
    systs[total_syst_label] = {}
for samp in bkgTotList:
    for total_syst_label in total_syst_labels:
        systs[total_syst_label][samp] = {}
    for b in bins:
        #systs["%s_CorrSysts"%total][samp][b]    =    addInQuad100PerctCorr( [systs[syst_name][samp][b] for syst_name in corr_systs ] ) 
        systs["%s_CorrSysts"%total][samp][b]    =    addInQuad( [systs[syst_name][samp][b] for syst_name in corr_systs_list ] ) 
        systs["%s_UncorrSysts"%total][samp][b]  =    addInQuad( [systs[syst_name][samp][b] for syst_name in uncorr_systs_list ] )
        systs["%s_Systs"%total][samp][b]        =    addInQuad( [systs["%s_CorrSysts"%total][samp][b], systs["%s_UncorrSysts"%total][samp][b] ] )
systs["Signal_Systs"] = {}
for sig in sigList:
    systs["Signal_Systs"][sig] = {}
    for b in bins:
        systs["Signal_Systs"][sig][b]          = addInQuad( [ systs[syst_name][sig][b] for syst_name in signal_systs ] )


systs["Signal_SystsRange"]={}
for syst_name in signal_systs:
    systs["Signal_SystsRange"][syst_name]={}
    for b in bins:
        systs_range  =   [ systs[syst_name][sig][b] for sig in sigList ]
        systs["Signal_SystsRange"][b]= [min(systs_range), max(systs_range), sum(systs_range)/len(systs_range) ] 


if True: 
    first_row = True
    table_list = []
    nptable = np.array([])
    main_sr_table = []
    for region in regions:
        if region == "\hline":
            table_list.append([region])
            continue
        if not 'SR' in region: continue
        isMainSR = True if region in main_sr else False

        toPrint = [
                      ["Systematic Effect"                     ,  fixForLatex( region )         ],
                   ]
        #for syst_name in systs_for_sum + other_corr_systs:
        for syst_name in corr_systs_list  :
            toPrint.append( [  fixSystName(syst_name) , round (systs[syst_name]['Total'][region],1) ] )
        table_list.append( ["\hline"] )
        main_sr_table.append( ["\hline"])
        for syst_name in uncorr_systs_list :                                             
            toPrint.append( [  fixSystName(syst_name) , round (    systs[syst_name]['Total'][region],1) ] )
        toPrint.append( [  'Total'          , round ( systs["%s_Systs"%total]['Total'][region]       ,1) ] )
        toPrint.append( [  'Total (uncorr)' , round ( systs["%s_UncorrSysts"%total]['Total'][region] ,1) ] )
        toPrint.append( [  'Total (corr)'   , round ( systs["%s_CorrSysts"%total]['Total'][region]   ,1) ] )
        #toPrint.append( [  'Total (uncorr)' , round ( total_systs_uncorr[region] ,1) ] )
        #toPrint.append( [  'Total' , round ( total_systs[region] ,1) ] )
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
    #list_for_np = []
    #for row in main_sr_table:
    #    if 'hline' in row[0]:
    #        new_row = ['\hline'] + ['']*(len(main_sr_table[1])-1)
    #    else: 
    #        new_row = row
    #    print new_row
    #    list_for_np.append( [new_row])
    #main_sr_nptable = np.concatenate( list_for_np)
    main_sr_nptable = np.concatenate( [ [x] for x in main_sr_table if 'hline' not in x[0]]  )
    nptable = np.concatenate( [ [x] for x in table_list if 'hline' not in x[0]]  )

    makeDir(saveDirBase+"/Results/")
    table = makeSimpleLatexTable( table_list, "SystsSummary_%s.tex"%lumitag, saveDirBase+"/Results/", align_char = "c"        ,  align_func= lambda char, table: "c|"+ (char *(len(table[1])-4)).rstrip("|") + "||c|c|c" )

    main_sr_nptable_T = main_sr_nptable.T
    main_sr_nptable_T[0][0]='Systematic Effect'
    main_sr_nptable_T = numpy.insert( main_sr_nptable_T, -3-len(uncorr_systs_list),['\hline'] + ['']*(len(main_sr_nptable_T[0])-1), axis=0 )
    main_sr_nptable_T = numpy.insert( main_sr_nptable_T, -3,['\hline'] + ['']*(len(main_sr_nptable_T[0])-1), axis=0 )
    main_sr_nptable_T = numpy.insert( main_sr_nptable_T, -3,['\hline'] + ['']*(len(main_sr_nptable_T[0])-1), axis=0 )
    SRtable = makeSimpleLatexTable( main_sr_nptable_T, "SystsSummaryMainSRs_%s.tex"%lumitag, saveDirBase+"/Results/", align_char = "c"        ,  align_func= lambda char, table: "l|"+ (char *(len(table[1])-1)).rstrip("|") )

    



sig_bkg_infos = { \
                            "BkgSysts":  { 'sampleList':bkgTotList  , 'total':True  , 'pkl':bkg_systs_path}  ,
                            #"SigSysts":  { 'sampleList':sigList   , 'total':False, 'pkl':sig_systs_path} ,
                 }
for sampleType, info in sig_bkg_infos.iteritems():

    ##
    ##  Final Result Table
    ##

    #finalYields  = deepcopy(yieldDict)
    yldsByBins   = yld.getByBins( yieldDict = yieldDictCentral )


    #finalYieldDict = {}
    #for bkg in allBkg + ['Total']:
    #    finalYieldDict[bkg]= deepcopy( finalYields[bkg] )

    #qcdEst= pickle.load(file("/afs/hephy.at/user/m/mzarucki/public/QCDsystematics_combined.pkl"))
    #for b, val in qcdEst.iteritems():
    #    finalYieldDict['QCD'][b]= u_float( val['val'], val['stat'] ) 
    #finalYieldDict['Data'] = {}

    first_row = True
    result_table_list = []
    for region in regions:
            if region == "\hline":
                result_table_list.append([region])
                continue
            if not 'SR' in region: 
                continue
            #otherTotal     = dict_operator ( yldsByBins[region] , keys =  otherBkg  , func = lambda *a: sum( a ).round(2)     )
            #estTotal       = dict_operator ( yldsByBins[region] , keys = [ w, tt, z, qcd ] + otherBkg  , func = lambda a,b,c,d, *e: a*CR_SFs[region][w] + b*CR_SFs[region][tt] + c*CR_SFs[region][z] + d*CR_SFs[region][qcd]  + sum( e )     )
            #mcTotal        = yldsByBins[region]['Total']
            toPrint = [
                          ["Region"     ,  fixForLatex( region )],
                      ]
            for bkg in bkgTotList:
                #toPrint.append( [bkg        ,   (yldsByBins[region][bkg]*SF).round(2).__str__()+"+-%s"%bkgSyst ]         ) 
                bkgSystPerc     =    systs["Total_Systs"][bkg][region]
                val             =    yieldDictCentral[bkg][region]
                centralValue    =    val.val
                stat            =    val.sigma
                syst            =    centralValue * bkgSystPerc/100.
                if bkg ==z:
                    print bkg, region, bkgSystPerc, val, stat, syst
                
                #toPrint.append( [bkg       ,   (centralVal).round(2).__str__()+"+-%s"%bkgSyst ]         ) 
                #toPrint.append( [bkg        ,  round(centralValue,2), "+-%s"%round(stat,2), "+-%s"%round(syst,2) ]         ) 
                toPrint.append( [bkg        ,  "%s"%round(centralValue,2)+ "+-%s"%round(stat,2)+ "+-%s"%round(syst,2) ]         ) 

            if blinded:
                observed     = int( yldsByBins[region]['DataUnblind'].val)
                toPrint.append( ["Data (4.3$fb^{-1}$)", observed] )
            else:
                #observed     = int( yldsByBins[region]['DataBlind'].val)
                observed     = int( yld.getNiceYieldDict()["DataBlind"][region].val)
                toPrint.append( ["Data (12.9$fb^{-1}$)", observed] )
                #finalYieldDict["Data"][region] = u_float(observed,math.sqrt( observed ) )
            align = "{:<20}"*len(toPrint)
            if first_row:
                print align.format(*[x[0] for x in toPrint])
                first_row = False
                result_table_list.append( [x[0] for x in toPrint]  )
    
            print align.format(*[x[1] for x in toPrint])
            result_table_list.append( [x[1] for x in toPrint])

    ResTable = makeSimpleLatexTable( result_table_list, "BkgEstSRSummary_%s.tex"%lumitag, saveDirBase+"/Results/", align_char = "r"        ,  align_func= lambda char, table: "r|"+ (char *(len(table[1])-1)).rstrip("|") )


    #finalYieldDict = yieldDictCentral
    finalYieldDict = {}
    for samp in yieldDictCentral.keys():
        finalYieldDict[samp]={}
        for b in yieldDictCentral[samp].keys():
            val = yieldDictCentral[samp][b]
            cent = val.val
            stat = val.sigma
            syst = systs['Total_Systs'][samp][b] if systs['Total_Systs'].has_key(samp) else 0
            final_value = u_float(cent,stat) + u_float(0,cent*syst/100)
            finalYieldDict[samp][b]=final_value
    
    if blinded:
        setup_style()
        plt1= drawYields("Results_SRsPtBinned_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['DataBlind'], keys = pt_srs, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] )
        plt2= drawYields("Results_MainSRs_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = main_sr, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] )
        plt3= drawYields("Results_NoLog_SRsPtBinned_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = pt_srs, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] , logs=[0,0])
        plt4= drawYields("Results_NoLog_MainSRs_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = main_sr, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] , logs=[0,0])
    elif True:
        #finalYieldDict = dicts['bkg_pred'][        
        data = "DataBlind"
        finalYieldDict[data] = yld.getNiceYieldDict()[data]
        
        sigs = [ 'T2tt-300-290' , 'T2tt-300-270', 'T2tt-300-220']

        setup_style()
        plt1= drawYields("Results_SRsPtBinned_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + [data], keys = pt_srs, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] )
        plt2= drawYields("Results_MainSRs_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + [data], keys = main_sr, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] )
        plt3= drawYields("Results_NoLog_SRsPtBinned_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + [data], keys = pt_srs, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] , logs=[0,0])
        plt4= drawYields("Results_NoLog_MainSRs_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + [data], keys = main_sr, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] , logs=[0,0])
        plt1s= drawYields("Results_withSigs_SRsPtBinned_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + [data] + sigs, keys = pt_srs, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] )
        plt2s= drawYields("Results_withSigs_MainSRs_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + [data] + sigs, keys = main_sr, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] )
        plt3s= drawYields("Results_withSigs_NoLog_SRsPtBinned_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + [data] + sigs, keys = pt_srs, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] , logs=[0,0])
        plt4s= drawYields("Results_withSigs_NoLog_MainSRs_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + [data] + sigs, keys = main_sr, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] , logs=[0,0])


#def makeSystPklForLimits( systs_dict ,  corr_keys, uncorr_keys, sample_names ):
#    card    =   { 'systs':{}, 'bins':{} }
#    return
#
#
#
#        
#
#def makeSystDictForCard( name,  syst_dict, sample_names, syst_type='lnN', bin_names = None):
#    if not bin_names:
#        bin_names = syst_dict.keys()
#    if sample_names:
#        pass
#    ret = { 'bins':{}, 'type':syst_type }
#    for b in bin_names:
#        pass        
#    return 




if __name__ == "":

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
        #for syst_name in systs_for_sum + other_corr_systs:
        for syst_name in corr_systs:
            toPrint.append( [ fixSystName( syst_name ), round (summary_systs[syst_name]['Total'][region],1) ] )
        table_list.append(["\hline"])
        for syst_name in uncorr_systs:                                             
            toPrint.append( [ fixSystName( syst_name ), round (summary_systs[syst_name]['Total'][region],1) ] )
        #toPrint.append( [  'Total (uncorr)' , round ( summary_systs["%s_UncorrSysts"%total]['Total'][region] ,1) ] )
        #toPrint.append( [  'Total (corr)'   , round ( summary_systs["%s_CorrSysts"%total]['Total'][region]   ,1) ] )
        toPrint.append( [  'Total'          , round ( summary_systs["%s_Systs"%total]['Total'][region]       ,1) ] )
        #toPrint.append( [  'Total (uncorr)' , round ( total_systs_uncorr[region] ,1) ] )
        #toPrint.append( [  'Total' , round ( total_systs[region] ,1) ] )
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

            for bkg in [qcd]:
                if region in qcdEst:
                    val = qcdEst[region]
                    if blinded:
                        val['val'] = val['val']*4.3/12.9 
                        val['stat'] = val['stat']*4.3/12.9
                    finalYieldDict[bkg][region] = u_float(val['val'], val['stat'] )
                    finalYields[bkg][region] = u_float(val['val'], val['stat'] )
                    yldsByBins[region][bkg] = u_float(val['val'], val['stat'] )
                    print ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;",region, yldsByBins[region][bkg]
            for bkg in [z]:
                if region in zinvEst:
                    val = zinvEst[region]
                    finalYieldDict[bkg][region] = val
                    finalYields[bkg][region] =    val 
                    yldsByBins[region][bkg] = val 
                    print ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;",region, yldsByBins[region][bkg]
    
            for bkg in mainBkg:
                SF = 1.0
                SF = CR_SFs[region][bkg]
                bkgYld  = (yldsByBins[region][bkg]*SF).round(2)
                bkgFrac = (2*estTotal.val- bkgYld.val)/estTotal.val if bkgYld.val else 0 
                #bkgSyst = round( bkgFrac*    bkgYld.val * 1/100. * total_systs[region] ,2)
                bkgSyst = round(  bkgYld.val * 1/100. * summary_systs["Total_Systs"][bkg][region] ,2)
                finalYieldDict[bkg][region] = bkgYld + u_float(0, bkgSyst ) 
                toPrint.append( [bkg        ,   (yldsByBins[region][bkg]*SF).round(2).__str__()+"+-%s"%bkgSyst ]         ) 
            for bkg in otherBkg:
                bkgYld  = (yldsByBins[region][bkg]).round(2)
                bkgFrac = (2*estTotal.val- bkgYld.val)/estTotal.val if bkgYld.val else 0 
                bkgSyst = round(  bkgYld.val * 1/100. * summary_systs["Total_Systs"][bkg][region] ,2)
                #bkgSyst = round( bkgFrac*    bkgYld.val * 1/100. * total_systs[region] ,2)
                finalYieldDict[bkg][region] = bkgYld + u_float(0, bkgSyst ) 


            otherFrac = (2*estTotal.val- otherTotal.val)/estTotal.val if otherTotal.val else 0 
            toPrint.append(     ["Other"    ,   otherTotal.__str__() + "+-%s"%round( otherFrac,2) ]                                    ) 
            #toPrint.append(    ["M.C. Total", mcTotal ]  )
            tot_rel_sys = estTotal.val * 1/100.* summary_systs["Total_Systs"]["Total"][region] 
            #   toPrint.append(     ["S.M Est." ,   estTotal.round(2).__str__() + "+-%s"%round( estTotal.val * 1/100.* total_systs[region],2) ]                              ) 
            finalYieldDict['Total'][region] = estTotal +u_float(0, tot_rel_sys)
            if blinded:
                observed     = int( yldsByBins[region]['DataUnblind'].val)
                toPrint.append( ["Data (4.3$fb^{-1}$)", observed] )
                finalYieldDict["Data"][region] = u_float(observed,math.sqrt( observed ) )
            else:
                observed     = int( yldsByBins[region]['DataBlind'].val)
                toPrint.append( ["Data (12.9$fb^{-1}$)", observed] )
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
    else:
        setup_style()
        plt1= drawYields("Results_SRsPtBinned_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = pt_srs, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] )
        plt2= drawYields("Results_MainSRs_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = main_sr, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] )
        plt3= drawYields("Results_NoLog_SRsPtBinned_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = pt_srs, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] , logs=[0,0])
        plt4= drawYields("Results_NoLog_MainSRs_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = main_sr, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] , logs=[0,0])





    ##
    ##  Mu_EL Composition
    ##
    do_mu_el_comp = True
    if do_mu_el_comp:
        first_row = True
        comp_table_list = []
        for region in regions:
                if region == "\hline":
                    comp_table_list.append([region])
                    continue
                if not 'SR' in region: 
                    continue
                #otherTotal     =    dict_operator ( yldsByBins[region] , keys =  otherBkg  , func = lambda *a: sum( a ).round(2)     )
                #estTotal       =    dict_operator ( yldsByBins[region] , keys = [ w, tt, z, qcd ] + otherBkg  , func = lambda a,b,c,d, *e: a*CR_SFs[region][w] + b*CR_SFs[region][tt] + c*CR_SFs[region][z] + d*CR_SFs[region][qcd]  + sum( e )     )
                mcTotal        =    yldsByBins[region]['Total']
                toPrint = [
                              ["Region"     ,  fixForLatex( region )],
                          ]
                for bkg in allBkg + ['Total']:
                    toPrint.append( [bkg        ,   muratio[bkg][region]    ]         )
                #toPrint.append(     ["S.M Est." ,   estTotal.round(2).__str__() + "+-%s"%round( estTotal.val * 1/100.* total_systs[region],2) ]                              ) 
                if blinded:
                    observed     = int( yldsByBins[region]['DataUnblind'].val)
                    toPrint.append( ["Data (4.3$fb^{-1}$)", observed] )
                else:
                    observed     = int( yldsByBins[region]['DataBlind'].val)
                    toPrint.append( ["Data (12.9$fb^{-1}$)", observed] )
                align = "{:<20}"*len(toPrint)
                if first_row:
                    print align.format(*[x[0] for x in toPrint])
                    first_row = False
                    comp_table_list.append( [x[0] for x in toPrint]  )
        
                print align.format(*[x[1] for x in toPrint])
                comp_table_list.append( [x[1] for x in toPrint])

        ResTable = makeSimpleLatexTable( comp_table_list, "MuonElRatio_%s.tex"%lumitag, saveDirBase+"/Results/", align_char = "r"        ,  align_func= lambda char, table: "r|"+ (char *(len(table[1])-1)).rstrip("|") )


        
        #if blinded:
        #    setup_style()
        #    plt1= drawYields("Results_SRsPtBinned_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = pt_srs, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] )
        #    plt2= drawYields("Results_MainSRs_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = main_sr, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] )
        #    plt3= drawYields("Results_NoLog_SRsPtBinned_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = pt_srs, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] , logs=[0,0])
        #    plt4= drawYields("Results_NoLog_MainSRs_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = main_sr, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] , logs=[0,0])
        #else:
        #    setup_style()
        #    plt1= drawYields("Results_SRsPtBinned_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = pt_srs, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] )
        #    plt2= drawYields("Results_MainSRs_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = main_sr, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] )
        #    plt3= drawYields("Results_NoLog_SRsPtBinned_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = pt_srs, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] , logs=[0,0])
        #    plt4= drawYields("Results_NoLog_MainSRs_%s"%lumitag, finalYieldDict , sampleList = ['ST', 'QCD', 'Diboson', 'DYJetsM50', 'ZJetsInv', 'TTJets', 'WJets']  + ['Data'], keys = main_sr, save= saveDirBase+"/Results/",ratioLimits=[0,2.5] , logs=[0,0])
