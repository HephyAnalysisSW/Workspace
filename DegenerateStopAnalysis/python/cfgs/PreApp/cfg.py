import os

from Workspace.DegenerateStopAnalysis.tools.TaskConfig import TaskConfig

## Specific cuts and weights for this config file
#from cuts import cuts


import Workspace.DegenerateStopAnalysis.tools.cfgFunctions as cfgFunctions
from Workspace.DegenerateStopAnalysis.tools.massPoints import MassPoints
from Workspace.DegenerateStopAnalysis.tools.degCuts import Cuts
from Workspace.DegenerateStopAnalysis.tools.degPlots import DegPlots
from Workspace.DegenerateStopAnalysis.scripts.degStop import args


import Workspace.DegenerateStopAnalysis.tools.weights_pu as weights_pu
import Workspace.DegenerateStopAnalysis.tools.weights_pu2 as weights_pu2
import Workspace.DegenerateStopAnalysis.tools.weights_wpt as weights_wpt
import Workspace.DegenerateStopAnalysis.tools.weights_pu_wpt as weights_pu_wpt
import Workspace.DegenerateStopAnalysis.tools.weights_pu_ttpt as weights_pu_ttpt
import Workspace.DegenerateStopAnalysis.tools.weights_base as weights_base
#import weights import weights_base



dmOpt = "allDM"
massPoints = MassPoints(dmOpt)
massPointsFull = MassPoints(dmOpt, (100,601,25))





bkgList = ['st', 'vv' , 'dy', 'qcd', 'z', 'tt', 'w' ]
#bkgList = [ 'dy', 'qcd', 'z', 'tt', 'w' ]
sigList = ['s60FS', 's30FS', 's10FS' , 's30']
sigList = []


#signalList    = massPoints.sigList 
#mstop_lsps = massPoints.mstop_lsps
# 
#signalListFull  = massPointsFull.sigList
#mstop_lspsFull  = massPointsFull.mstop_lsps



#plotMStopLSPs   = [ (300,270), (300,290), (300,220)]
#plotSignalList  = ["s%s_%s"%(x[0],x[1]) for x in plotMStopLSPs]


plotMStopLSPs = []
plotSignalList = sigList


sampleList = bkgList + sigList 

#sampleList = ['tt']

print args






lepCol = getattr( args, "lepCol", "LepAll")
lep    = getattr( args, "lep", "lep")

lepTag = lepCol+"_" + lep

btag   = getattr( args, 'btag', 'btag')

sr1c_opts = [ 
                "Reload" ,               #0 
                "MT95" ,                 #1   
                "MT95_IncCharge",        #2   
                "MT105_IncCharge_CT250"  #3       
            ]

sr1c_opt = sr1c_opts[2]


cuts = Cuts(lepCol, lep, sr1c_opt = sr1c_opt, isrpt=100, btag = btag )
plots = DegPlots( lepCol, lep)

limitCuts = cuts.bins 
plotCuts  = [ cuts.presel, cuts.sr1IncCharge , cuts.cr1IncCharge , cuts.sr1, cuts.cr1] #cuts.sr1, cuts.sr2, cuts.sr1a, cuts.sr1b, cuts.sr1c, cuts.cr1, cuts.cr2, cuts.crtt2 ]
flowCuts  = [ cuts.cutflow ]

crCuts = [ cuts.crs ] 

#bPlots = ["nBJets", "bJetPt", "bSoftJetPt", "bHardJetPt"]



tasks_info =  {
            'limits10fb':    {'taskList' : [ 'calc_mva_limit' ]  , 'sigList':  massPointsFull.sigList , 'massPoints':   massPointsFull.mstop_lsps   , 'cutInstList':  limitCuts    ,'plotList':plots.plots.keys()  , 'lumi_target' : 10000 }   ,
            'limits':    {'taskList' : [ 'calc_mva_limit' ]  , 'sigList':  massPoints.sigList , 'massPoints':   massPoints.mstop_lsps   , 'cutInstList':  limitCuts         ,'plotList':plots.plots.keys()                   },
            'bkg_est':    {'taskList' : [ 'bkg_est' ]  ,         'sigList': plotSignalList    , 'massPoints':   []                      , 'cutInstList':  crCuts            ,'plotList':plots.plots.keys()           , 'data': True        },
            'plots':     {'taskList' : [ 'draw_plots'  ]     , 'sigList':  plotSignalList     , 'massPoints':   plotMStopLSPs           , 'cutInstList':  plotCuts[:]       ,'plotList':plots.plots.keys()[:]                },
            'cutflow':   {'taskList' : [ 'cut_flow' ]        , 'sigList':  plotSignalList     , 'massPoints':   plotMStopLSPs           , 'cutInstList':  flowCuts          ,'plotList':plots.plots.keys()[:]             },
            'data':      {'taskList' : [ 'data_plots' ]      , 'sigList':  plotSignalList     , 'massPoints':   plotMStopLSPs           , 'cutInstList':  plotCuts[:]       ,'plotList': plots.plots.keys()[:]   , 'data':True},
            'limits2':    {'taskList' : [ 'calc_mva_limit' ]  , 'sigList':  massPoints.sigList , 'massPoints':   massPoints.mstop_lsps   , 'cutInstList':  limitCuts        ,'plotList':plots.plots.keys()[:]         , 'data':True},
              }
#task = 'cutflow'
#task = 'limits10fb'
#task = 'plots'
#task = 'data'
#task = 'limits'

task = getattr( args, "task", "data")
task_info=tasks_info[task]

#ppTag = "74X_postProcessing_v4"

ppSets = [
            ( "80X_postProcessing_v5" , "mzarucki01"   , '8011_mAODv2_v1'),
            ( "80X_postProcessing_v4" , "nrad01"       , '8011_mAODv2_v1'),
            ( "80X_postProcessing_v3" , "nrad01"       , '8011_mAODv2_v1'),
         ]

ppSet  = 0 
ppTag  = ppSets[ppSet][0]
ppUser = ppSets[ppSet][1]
cmgTag = ppSets[ppSet][2]



def make_match_func(tothis):
    def match_func(x):
        ##      should use search instead, and then replace to make things less messy!
        ##      re.search( ".*%s"%(tothis.replace("(","\(").replace(")","\)").replace("*","\*")), x )
        ##
        return re.match( ".*%s"%(tothis.replace("(","\(").replace(")","\)").replace("*","\*")), x )
    return match_func



from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import btag_to_sf , sf_to_btag
import re
def_weights = {

            "cuts": dict( [ (sf, (sf, make_match_func(sf))  )  for sf in sf_to_btag.keys()  ]) , 
            "baseWeight":"puReweight*weight",
            #"baseWeight":"puWeight2*weight",
            "lumis":{
                            "mc_lumi"               :   10000   ,
                            'target_lumi'           :   13000.   ,
                            'DataBlind_lumi'      :   12430    ,
                            'DataUnblind_lumi'    :   804.2   ,
                    },
                }

print "arg cut:", getattr(args, "cutInst", "False")
cutInstList = [] 
if hasattr(args,"cutInst") and args.cutInst:
    for cutInstName in args.cutInst:
        if hasattr(cuts, cutInstName):
            cutInstList.append( getattr(cuts,cutInstName))
        else:
            print args.cut ,"was not found as a attribute of cuts"
            cutInstList = task_info['cutInstList']
else:
    cutInstList = task_info['cutInstList']

plotList = []
if getattr(args,"plot",[]):
    for p in args.plot:
        if hasattr(plots.plots, p):
            plotList.append( p )
        else:
            print "Skipping plot: %s , not found in %s"%(p, plots.plots.keys() )
else:
    plotList = task_info['plotList']




#if hasattr(args,"plot") and args.plot:
#    if plots.plots.has_key( args.plot ):
#        plotList = [ args.plot ]
#    else:
#        print args.plot ,"was not found as a attribute of plots keys", plots.plots.keys()
#        plotList = task_info['plotList']
#else:
#    plotList    = task_info['plotList']






data_filters_list = [
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_goodVertices",
                        "Flag_eeBadScFilter",
                        "Flag_globalTightHalo2016Filter",
                        "Flag_badChargedHadronFilter",
                        "Flag_badMuonFilter",
                    ]
mc_filters_list   = [
                        "Flag_badChargedHadronFilter",
                        "Flag_badMuonFilter",
                    ]



weights = {
            'base': weights_base,
            'pu':   weights_pu,
            'pu2':   weights_pu2,
            'wpt':  weights_wpt, 
            'pu_wpt': weights_pu_wpt,
            'pu_ttpt': weights_pu_ttpt,
          }

weight = getattr(args , "weight", "base") 
weight_tag = '' if weight == 'base' else "_%s"%weight

task_weight = weights[weight]


cfg = TaskConfig(
                   runTag         =  os.path.basename(os.path.dirname(os.path.realpath(__file__)) ) + "_"  + sr1c_opt.title()  + "_"+lepTag + weight_tag + ( "_%s"%btag.upper() ),   ## should be the same as the name of the directory that the cfg is in
                   taskList       =  task_info['taskList'],
                   ppTag          =  ppTag , 
                   ppStep         =  'step1',    ## step1 for mva
                   ppUser         =  ppUser , 
                   cmgTag         =  cmgTag , 
                   #saveDirBase   =  "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2_v6/Studies_v1/" ,
                   saveDirBase    =  "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/%s/%s/SUS_16_031/"%(cmgTag, ppTag) ,
                   #saveDirBase    =  "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/%s/%s/Studies_v0_puWeight_wptrwgt/"%(cmgTag, ppTag) ,
                   #saveDirBase    =  "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/%s/%s/Studies_v0_puWeight_wptrwgt/"%(cmgTag, ppTag) ,
                   cutInst        =  cutInstList,
                   plots          =  plots.plots         , 
                   plotList       =  plotList, 
                   nminus1s       =  plots.nminus1s, 
                   calc_mva_limit =  cfgFunctions.calc_mva_limit , 
                   cut_flow       =  cfgFunctions.cut_flow       ,
                   data_plots     =  cfgFunctions.data_plots , 
                   bkg_est        =  cfgFunctions.bkg_est , 
                   signalList     =  task_info['sigList']          ,
                   bkgList        =  bkgList , 
                
                   sys_pkl        =  "/data/nrad/results/systs/8TeVSysts.json"              ,
                   sample_info    =  {
                                        "sampleList"   :    sampleList  ,
                                        "wtau"         :    False       , 
                                        "useHT"        :    True        , 
                                        "skim"         :    'preIncLep', 
                                        "kill_low_qcd_ht":  False       ,
                                        "scan"         :    False        ,
                                        #"massPoints"   :    task_info['massPoints']  ,
                                        "getData"      :    task_info.get("data",False)    ,
                                        "weights"      :    task_weight.weights     ,
                                        "def_weights"  :    def_weights     ,
                                        "data_triggers":    'HLT_PFMET100_PFMHT100_IDTight || HLT_PFMET110_PFMHT110_IDTight || HLT_PFMET120_PFMHT120_IDTight || HLT_PFMET90_PFMHT90_IDTight'                ,
                                        "data_filters" :    ' && '.join(data_filters_list), 
                                        "mc_filters"   :    ' && '.join(mc_filters_list),
                                        'lumis':def_weights['lumis'],
                                      } , 
                   lumi_info       = def_weights['lumis'],
                   #lumi_info      = task_info.get("lumi_info",{}),
                   nProc          =  15, 
                )

cfg.cuts = cuts


print "............................................"
print ""
print "RunTag:"  , cfg.runTag
print "Tasks:"   , cfg.taskList
print "sample tags:"   , ppUser, cmgTag, ppTag
print "cutInstList:"   , cutInstList
print "plotList:"      , plotList
print ""
print "............................................"






#tasks = [cfg, ]  submit multiple tasks TO BE IMPLEMENTED

