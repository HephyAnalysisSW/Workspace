import os

from Workspace.DegenerateStopAnalysis.tools.TaskConfig import TaskConfig

## Specific cuts and weights for this config file
#from cuts import cuts


import Workspace.DegenerateStopAnalysis.tools.cfgFunctions as cfgFunctions
import Workspace.DegenerateStopAnalysis.tools.Systematics as Systematics

from Workspace.DegenerateStopAnalysis.tools.massPoints import MassPoints
#from Workspace.DegenerateStopAnalysis.tools.degCuts_var import Cuts
#CutVars = Cuts
#from Workspace.DegenerateStopAnalysis.tools.degCuts import Cuts
from Workspace.DegenerateStopAnalysis.tools.degPlots import DegPlots
from Workspace.DegenerateStopAnalysis.scripts.degStop import args


from Workspace.DegenerateStopAnalysis.tools.weights import Weights
#import weights import weights_base


import Workspace.DegenerateStopAnalysis.tools.degCuts2 as degCuts

#import Workspace.DegenerateStopAnalysis.tools.degWeights as degWeights


from copy import deepcopy
import pickle

dmOpt = "allDM"
massPoints = MassPoints(dmOpt)
massPointsFull = MassPoints(dmOpt, (250,801,25))
massPointsFull2 = MassPoints(dmOpt, (250,801,25) , prefix="t2bw")
massPointsFull3 = MassPoints(dmOpt, (250,801,25) , prefix="t2ttold")



#defBkgList = [ 'vv',  'qcd', 'st', 'z','dy', 'tt', 'w' ]
defBkgList = [ 'qcd', 'st', 'z','dy', 'tt', 'w' ]


useData = getattr(args, "data", 'd')
if useData == 'd':
    lumiWeight = 'DataUnblind'
elif useData =='dblind':
    lumiWeight = 'DataBlind'
elif useData =='dichep':
    lumiWeight = 'DataICHEP'
else:
    lumiWeight = 'target_lumi'    


bkgList = getattr(args, "bkgs")
if not bkgList: bkgList = defBkgList
sigOpt = getattr(args,"sigOpt")

def getSigListFromMassDict(mass_dict, sig_prefix):
    sigList = []
    for m1 in mass_dict.keys():
        for m2 in mass_dict[m1].keys():
            if m1-m2 > 100: 
                continue
            sigList.append("%s%s_%s"%(sig_prefix, m1, m2))
    return sigList


if sigOpt.lower() =='bm':
    sigList = ['t2tt300_270', 't2tt300_290', 't2tt300_220']
    #sigList = ['s300_270' ,'s300_290','cwz300_290','cwz300_270' ,'cww300_290','cww300_270']
elif sigOpt.lower() == 'all': 
    sigList = massPointsFull.sigList
    sigList.extend( massPointsFull2.sigList)
    sigList.extend( massPointsFull3.sigList)
elif sigOpt.lower() == 'nosig':
    sigList = []
else:
    massPointsFull = MassPoints(dmOpt, (750,801,25))
    sigList = massPointsFull.sigList
print "Signal Opt: ", sigOpt
print "Signals to be used:", sigList


plotMStopLSPs = []
plotSignalList = sigList

print args


lepCol = getattr( args, "lepCol", "LepAll")
lep    = getattr( args, "lep", "lep")
lepTag = lepCol+"_" + lep
btag   = getattr( args, 'btag', 'btag')


lepThresh = getattr(args, "lepThresh", "def")
jetThresh = getattr(args, "jetThresh", "def")



sr1c_opts = [ 
                "Reload" ,               #0 
                "MT95" ,                 #1   
                "MT95_IncCharge",        #2   
                "MT105_IncCharge_CT250"  #3       
            ]

sr1c_opt = sr1c_opts[2]

mcMatch = getattr(args, 'mcMatch', False)
mcMatchTag = "_mcMatch" if mcMatch else ""
if lepCol=="LepAll" and mcMatch: assert False, "mcMatchId not compatible with LepAll for now!"



settings = {
                'lepCol':             lepCol             ,
                'lep':                lep                 ,
                #'lepTag':             "lowpt"                ,
                #'jetTag':             "lowpt"                ,
                'lepTag':             lepThresh                ,
                'jetTag':             jetThresh                ,
                'btagSF':             btag                 ,
                #'dataBlindLumi':       "12864.4"            ,
                'dataBlindLumi':       "36416.8"            ,
                'dataUnblindLumi':     "4303.0"              ,
                'mcLumi':              "10000"              ,
            }


lepTag = lepTag +"_" +settings['lepTag'] if settings['lepTag'] else lepTag
lepTag = lepTag +"_Jet_" +settings['jetTag'] if settings['jetTag'] else lepTag


pu = args.pu 

def_weights = ['weight', pu  , lumiWeight ]
def_weights = filter( lambda x: x , def_weights )
options     = [ 'isr', 'sf']

cuts        = degCuts.Cuts( settings, def_weights, options  )

weight_tag_list = [ pu, btag , mcMatchTag  ]
weight_tag_list = filter( lambda x: x, weight_tag_list )


weight_tag = "_".join(wgt for wgt in weight_tag_list if wgt)



plots = DegPlots( lepCol, lep , lepThresh = lepThresh, jetThresh = jetThresh)


limitCuts = cuts.bins_sum

plotCuts  = [ cuts.presel , cuts.sr1, cuts.cr1] #cuts.sr1, cuts.sr2, cuts.sr1a, cuts.sr1b, cuts.sr1c, cuts.cr1, cuts.cr2, cuts.crtt2 ]
crCuts = [cuts.bins_cr]

tasks_info =  {
            'bkg_est':    {'taskList' : [ 'bkg_est' ]  ,         'sigList': plotSignalList    , 'massPoints':   []                        , 'cutInstList':  crCuts            ,'plotList':plots.plots.keys()           , 'data': useData        },
            'explimits':     {'taskList' : [ 'calc_sig_limit' ]  ,  'sigList':  massPointsFull.sigList , 'massPoints':   massPointsFull.mstop_lsps   , 'cutInstList':  limitCuts         ,'plotList':plots.plots.keys()                   },
            'plots':     {'taskList' : [ 'draw_plots'  ]     , 'sigList':  plotSignalList     , 'massPoints':   plotMStopLSPs           , 'cutInstList':  plotCuts[:]       ,'plotList':plots.plots.keys()[:]                },
            'data':      {'taskList' : [ 'data_plots' ]      , 'sigList':  plotSignalList     , 'massPoints':   plotMStopLSPs           , 'cutInstList':  plotCuts[:]       ,'plotList': plots.plots.keys()[:]   , 'data': useData},
              }

task = getattr( args, "task", "data")
task_info=tasks_info[task]


postFuncs = getattr(args, "postFuncs" )
print postFuncs
task_info['taskList'].extend(postFuncs)
print task_info

sampleList = bkgList + task_info['sigList']

ppSets = [
            ( "80X_postProcessing_v0" , "nrad01"   , '8020_mAODv2_v5' , 'analysisHephy_13TeV_2016_v2_1', 'Data2016' , 'RunIISpring16MiniAODv2'),
            ( "80X_postProcessing_v0" , "nrad01"   , '8020_mAODv2_v0' , 'analysisHephy_13TeV_2016_v2_0', 'Data2016' , 'RunIISpring16MiniAODv2'),
            ( "80X_postProcessing_v10" , "nrad01"   , '8012_mAODv2_v3' , 'analysisHephy_13TeV_2016_v0', 'Data2016' , 'RunIISpring16MiniAODv2'),
            ( "80X_postProcessing_v9" , "nrad01"   , '8011_mAODv2_v1'),
            ( "80X_postProcessing_v8" , "nrad01"   , '8011_mAODv2_v1'),
            ( "80X_postProcessing_v6" , "nrad01"   , '8011_mAODv2_v1'),
            ( "80X_postProcessing_v7" , "nrad01"   , '8011_mAODv2_v1'),
            ( "80X_postProcessing_v5" , "mzarucki01"   , '8011_mAODv2_v1'),
            ( "80X_postProcessing_v4" , "nrad01"       , '8011_mAODv2_v1'),
            ( "80X_postProcessing_v3" , "nrad01"       , '8011_mAODv2_v1'),
            ("74X_postProcessing_v4" , "vghete01"   , '7412pass2_mAODv2_v6', 'analysisHephy_13TeV_v0', 'Data25ns', 'Spring15_7412pass2_mAODv2'),
         ]

cfgPPSet =getattr(args, 'ppSet','80x')
if cfgPPSet.lower() == '80x':
    ppSet  = 0 
elif cfgPPSet.lower() =='74x':
    ppSet  = ppSets.index( ("74X_postProcessing_v4" , "vghete01"   , '7412pass2_mAODv2_v6', 'analysisHephy_13TeV_v0', 'Data25ns', 'Spring15_7412pass2_mAODv2') )
    sampleList = ['tt','w','z','qcd','dy'] + task_info['sigList']
ppTag  = ppSets[ppSet][0]
ppUser = ppSets[ppSet][1]
cmgTag = ppSets[ppSet][2]
parameterSet = ppSets[ppSet][3]
dataDir      = ppSets[ppSet][4]
mcDir        = ppSets[ppSet][5]
ppSkim       = 'skimPresel' if '74' in ppTag else 'preIncLep'

def make_match_func(tothis):
    def match_func(x):
        return re.match( ".*%s"%(tothis.replace("(","\(").replace(")","\)").replace("*","\*")), x )
    return match_func






lumis=              {
                            "mc_lumi"               :   10000   ,
                            'target_lumi'           :   12864.0   ,
                            'DataICHEP_lumi'        :   12864.4    ,
                            'DataBlind_lumi'        :   36416.8     ,
                            'DataUnblind_lumi'      :   4303.0  ,
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

mc_filters_list = [ 'Flag_Filters']
data_filters_list = mc_filters_list




weights = cuts.weights
generalTag = "Jan17v0"
cfgTag     = os.path.basename(os.path.dirname(os.path.realpath(__file__)) )


cfg = TaskConfig(
                   #runTag         =  os.path.basename(os.path.dirname(os.path.realpath(__file__)) ) + "_"  + sr1c_opt.title()  + "_"+lepTag + "_"+weight_tag + ( "_%s"%btag.upper() ) +mcMatchTag,   ## should be the same as the name of the directory that the cfg is in
                   #runTag         =  cfgTag  + "_" + generalTag + "_"+lepTag + "_"+weight_tag,  # + ( "_%s"%btag.upper() ) +mcMatchTag , 
                   cfgTag         =  cfgTag , 
                   runTag         =  lepTag + "_"+weight_tag,  # + ( "_%s"%btag.upper() ) +mcMatchTag , 
                   generalTag     =  generalTag , 
                   taskList       =  task_info['taskList'],
                   ppTag          =  ppTag , 
                   ppStep         =  'step1',    ## step1 for mva
                   ppUser         =  ppUser , 
                   cmgTag         =  cmgTag , 
                   parameterSet    =  parameterSet,
                   dataDir        =  dataDir,
                   mcDir          =  mcDir, 
                   saveDirBase    =  "%s/www/T2Deg13TeV/"%(os.path.expandvars("$HOME")  ) ,
                   cutInst        =  cutInstList,
                   plots          =  plots.plots         , 
                   plotList       =  plotList, 
                   nminus1s       =  plots.nminus1s,
                   taskModules     =  [ cfgFunctions , Systematics],  
                   #calc_sig_limit =  cfgFunctions.calc_sig_limit , 
                   #cut_flow       =  cfgFunctions.cut_flow       ,
                   #data_plots     =  cfgFunctions.data_plots , 
                   #bkg_est        =  cfgFunctions.bkg_est , 
                   signalList     =  task_info['sigList']          ,
                   bkgList        =  bkgList , 
                   data           =  args.data, 
                   sys_pkl        =  "/data/nrad/results/systs/8TeVSysts.json"              ,
                   sample_info    =  {
                                        "sampleList"   :    sampleList  ,
                                        "wtau"         :    False       , 
                                        "useHT"        :    True        , 
                                        "skim"         :    ppSkim, 
                                        "kill_low_qcd_ht":  False       ,
                                        "scan"         :    len(sigList)>0       ,
                                        "getData"      :    task_info.get("data",False)    ,
                                        "weights"      :    weights     ,
                                        "def_weights"  :    def_weights     ,
                                        "data_triggers":    'HLT_PFMET100_PFMHT100_IDTight || HLT_PFMET110_PFMHT110_IDTight || HLT_PFMET120_PFMHT120_IDTight || HLT_PFMET90_PFMHT90_IDTight'             if '80' in cmgTag  else '' ,
                                        "data_filters" :    ' && '.join(data_filters_list) if '80' in cmgTag else '', 
                                        "mc_filters"   :    ' && '.join(mc_filters_list) if '80' in cmgTag else '',
                                      } , 
                   lumi_info       = lumis,
                   nProc          =  15, 
                )


cfg.cuts = cuts
cfg.generalTag = generalTag
cfg.cfgTag     = cfgTag
print "............................................"
print ""
print "cfg Tag:"         , cfg.cfgTag
print "General Tag:"     , cfg.generalTag
print "RunTag:"          , cfg.runTag
print "Tasks:"           , cfg.taskList
print "sample tags:"   , ppUser, cmgTag, ppTag
print "cutInstList:"   , cutInstList
print "plotList:"      , plotList
print ""
print "............................................"






