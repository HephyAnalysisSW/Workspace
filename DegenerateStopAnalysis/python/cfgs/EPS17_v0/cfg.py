import os

import sys
from Workspace.DegenerateStopAnalysis.tools.TaskConfig import TaskConfig

## Specific cuts and weights for this config file
#from cuts import cuts


import Workspace.DegenerateStopAnalysis.tools.cfgFunctions as cfgFunctions
import Workspace.DegenerateStopAnalysis.tools.fakeEstimate as fakeEstimate
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


import Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo as sampleInfo
#import Workspace.DegenerateStopAnalysis.tools.degWeights as degWeights


from copy import deepcopy
import pickle


import ROOT
#ROOT.gROOT.ProcessLineSync(".L /afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/python/scripts/validations/badMu/deltaR.C")
deltaR_script = os.path.expandvars("$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/python/tools/deltaR.C")
ROOT.gROOT.ProcessLineSync(".L  %s"%deltaR_script)


#defBkgList = [ 'vv',  'qcd', 'st', 'z','dy', 'tt', 'w' ]
defBkgList = [ 'qcd', 'st', 'z','dy', 'tt', 'w' ]


useData = getattr(args, "data")

try:
    lumiWeight = sampleInfo.sampleName( useData) +"_lumi"
except:
    lumiWeight = "target_lumi"
#if useData == 'd':
#    lumiWeight = 'DataUnblind'
#elif useData =='dblind':
#    lumiWeight = 'DataBlind'
#elif useData =='dichep':
#    lumiWeight = 'DataICHEP'
#
#else:
#    lumiWeight = 'target_lumi'    


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




dmOpt = "allDM"
massPoints      = MassPoints(dmOpt)
massPointsFull  = MassPoints(dmOpt, (250,801,25))
massPointsFull2 = MassPoints(dmOpt, (250,801,25) , prefix="t2bw")
massPointsFull3 = MassPoints(dmOpt, (250,801,25) , prefix="t2ttold")

if sigOpt.lower() =='bm0':
    sigList = ['t2tt300_270', 't2tt300_290', 't2tt300_220']
if sigOpt.lower() =='bm1':
    sigList = ['t2tt300_270', 't2tt300_290', 't2tt300_220']
    #sigList = ['t2tt300_270' ]
elif sigOpt.lower() =='bm':
    #sigList = ['t2tt300_270', 't2ttold300_270' , 't2tt300_290', 't2ttold300_290' ]
    sigList  = ['t2tt300_270', 't2tt500_470', 't2tt500_490', 't2tt450_440', 't2tt500_420']
    sigList += ['t2bw300_270', 't2bw500_470', 't2bw500_490', 't2bw450_440', 't2bw500_420']
elif sigOpt.lower() =='bm3':
    sigList = ['t2ttold300_270', 't2ttold300_290', 't2ttold300_220']
elif sigOpt.lower() == 't2tt': 
    sigList = massPointsFull.sigList
elif sigOpt.lower() == 't2bw': 
    sigList = massPointsFull2.sigList
elif sigOpt.lower() == 't2ttold': 
    sigList = massPointsFull3.sigList
elif sigOpt.lower() == 'all': 
    sigList = massPointsFull.sigList
    sigList.extend( massPointsFull2.sigList)
elif sigOpt.lower() == 'all2': 
    sigList = massPointsFull.sigList
    sigList.extend( massPointsFull2.sigList)
    sigList.extend( massPointsFull3.sigList)
elif sigOpt.lower() == 'test':
    sigList = ["t2tt375_305"]
elif sigOpt.lower() == 'nosig':
    sigList = []
elif sigOpt.lower() == 'ewk':
    sigList=[ 
              'c1c1h150_120',
              'c1c1h225_205',
              'c1n1h220_200',
              'c1n1h140_110',
              'c1n1h180_173',
              'n2n1h140_110',
              'n2n1h160_153',
              'n2n1h180_160', 
            ]
else:
    massPointsFull = MassPoints(dmOpt, (750,801,25))
    sigList = massPointsFull.sigList
print "Signal Opt: ", sigOpt
print "Signals to be used:", sigList


plotMStopLSPs =[ (300,270), (300,290), (300,220)]
plotSignalList = sigList


print args


lepCol = getattr( args, "lepCol", "LepAll")
lep    = getattr( args, "lep", "lep")
lepTag = lepCol+"_" + lep

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


mvaId   = getattr(args, "mvaId" )
bdtcut  = getattr(args, "bdtcut")

mva_params =[ mvaId, bdtcut ] 

if any( mva_params):
    if not all( mva_params):
        raise Exception("MVA Parameters set partially! need both bdtCut and mvaId %s"%mva_params)
    isMVA = True
else:
    isMVA = False

settings = {
                'lepCol':             lepCol             ,
                'lep':                lep                 ,
                #'lepTag':             "lowpt"                ,
                #'jetTag':             "lowpt"                ,
                'lepTag':             lepThresh                ,
                'jetTag':             jetThresh                ,
                'btagSF':             'btag'                     ,
                #'dataBlindLumi':       "12864.4"            ,
                'lumis': { 
                            #'DataBlind_lumi':       "36416.8"            ,
                            #'DataUnblind_lumi':     "4303.0"              ,
                            'MC_lumi':              "10000"              ,
                            'target_lumi'           :   "35700.0"   ,
                         },
            }
if isMVA:
    settings.update({
                'mvaId' :              mvaId,
                'bdtcut':              bdtcut               ,
                    })


lepTag = lepTag +"_" +settings['lepTag'] if settings['lepTag'] else lepTag
lepTag = lepTag +"_Jet_" +settings['jetTag'] if settings['jetTag'] else lepTag


#pu = args.pu 

alternative_variables = {
                        }



weights_input = getattr( args, "weights" , [] )


weights_info = sampleInfo.evalInputWeights( weights_input  , lumiWeight )

options = weights_info['options']
def_weights = weights_info['def_weights']
weight_tag  = weights_info['weight_tag']
settings_update = weights_info['settings_update']
settings.update(settings_update)

#cuts        = degCuts.Cuts( settings, def_weights, options  )

print settings
cuts = degCuts.Cuts( settings, def_weights, options , alternative_variables)

print def_weights
print weight_tag

plots = DegPlots( lepCol, lep , lepThresh = lepThresh, jetThresh = jetThresh)


limitCuts = cuts.bins_sum

plotCuts  = [ cuts.presel , cuts.sr1, cuts.cr1] #cuts.sr1, cuts.sr2, cuts.sr1a, cuts.sr1b, cuts.sr1c, cuts.cr1, cuts.cr2, cuts.crtt2 ]
crCuts = [cuts.bins_cr]

tasks_info =  {
            'bkg_est':    {'taskList' : [ 'bkg_est' ]  ,         'sigList': plotSignalList    , 'massPoints':   []                        , 'cutInstList':  crCuts            ,'plotList':plots.plots.keys()           , 'data': useData        },
            'yields':     {'taskList' : [ 'yields' ]  ,          'sigList': plotSignalList    , 'massPoints':   []                        , 'cutInstList':  crCuts            ,'plotList':plots.plots.keys()           , 'data': useData        },
            'cut_flow':     {'taskList' : [ 'cut_flow' ]  ,          'sigList': plotSignalList    , 'massPoints':   []                        , 'cutInstList':  crCuts           ,'plotList':[]           , 'data': useData        },
            'explimits':     {'taskList' : [ 'calc_sig_limit' ]  ,  'sigList':  massPointsFull.sigList , 'massPoints':   massPointsFull.mstop_lsps   , 'cutInstList':  limitCuts         ,'plotList':plots.plots.keys()                   },
            'plots':     {'taskList' : [ 'draw_plots'  ]     , 'sigList':  plotSignalList     , 'massPoints':   plotMStopLSPs           , 'cutInstList':  plotCuts[:]       ,'plotList':plots.plots.keys()[:]                },
            'data':      {'taskList' : [ 'data_plots' ]      , 'sigList':  plotSignalList     , 'massPoints':   plotMStopLSPs           , 'cutInstList':  plotCuts[:]       ,'plotList': plots.plots.keys()[:]   , 'data':useData},
              }


task = getattr( args, "task", "data")
task_info=tasks_info[task]


postFuncs = getattr(args, "postFuncs" )
print postFuncs
task_info['taskList'].extend(postFuncs)
print task_info

sampleList = bkgList + task_info['sigList']

ppSets = [
            ( "80X_postProcessing_v1" , "nrad01"   , '8025_mAODv2_v7' , 'analysisHephy_13TeV_2016_v2_3', 'Data2016' , 'RunIISummer16MiniAODv2', "step1"),
            ( "80X_postProcessing_v0" , "nrad01"   , '8025_mAODv2_v7' , 'analysisHephy_13TeV_2016_v2_3', 'Data2016' , 'RunIISummer16MiniAODv2', "step1"),
            ( "80X_postProcessing_v0" , "nrad01"   , '8020_mAODv2_v5' , 'analysisHephy_13TeV_2016_v2_1', 'Data2016' , 'RunIISpring16MiniAODv2', "step1"),
            ( "80X_postProcessing_v10" , "vghete02"   , '8012_mAODv2_v3' , 'analysisHephy_13TeV_2016_v0', 'Data2016' , 'RunIISpring16MiniAODv2' , 'step2_v3' ),
            ( "80X_postProcessing_v0" , "nrad01"   , '8020_mAODv2_v0' , 'analysisHephy_13TeV_2016_v2_0', 'Data2016' , 'RunIISpring16MiniAODv2', 'step1' ),
            ( "80X_postProcessing_v10" , "nrad01"   , '8012_mAODv2_v3' , 'analysisHephy_13TeV_2016_v0', 'Data2016' , 'RunIISpring16MiniAODv2' , 'step1' ),
            ("74X_postProcessing_v4" , "vghete01"   , '7412pass2_mAODv2_v6', 'analysisHephy_13TeV_v0', 'Data25ns', 'Spring15_7412pass2_mAODv2'),
         ]

cfgPPSet =getattr(args, 'ppSet','80x')
if cfgPPSet.lower() == '80x':
    ppSet  = 0 
elif cfgPPSet.lower() =='74x':
    ppSet  = ppSets.index( ("74X_postProcessing_v4" , "vghete01"   , '7412pass2_mAODv2_v6', 'analysisHephy_13TeV_v0', 'Data25ns', 'Spring15_7412pass2_mAODv2') )
    sampleList = ['tt','w','z','qcd','dy'] + task_info['sigList']
else:
    ppSet = int(cfgPPSet)
ppTag  = ppSets[ppSet][0]
ppUser = ppSets[ppSet][1]
cmgTag = ppSets[ppSet][2]
parameterSet = ppSets[ppSet][3]
dataDir      = ppSets[ppSet][4]
mcDir        = ppSets[ppSet][5]
ppStep       = ppSets[ppSet][6]
ppSkim       = 'skimPresel' if '74' in ppTag else 'preIncLep'
ppSkim       = getattr(args, 'skim', ppSkim)



if isMVA:

    mva_step2_dict = {
                      #'lip' : "step2_mvaLip_job_2017-v2_0_1_LipWeights/mvaSet_30/"  ,
                      'hephy'      : "step2_mvaLip_job_2017-v2_0_1_Hephy/mvaSet_30/"       ,
                      'hephy_old'  : "step2_Lip_2017_v0/mvaSet_30/",
                      "lip"        :  "step2_mvaLip_job_2017-v2_2_0_LipWeights_pre_none_loose/mvaSet_30" ,
                     }
    
    step2 = getattr(args, "step2", 'hephy_old')
    
    
    mva_step2 = mva_step2_dict[step2]
    
    mva_friendtree_map  = [
                            ["nrad01" ,  "vghete02" ]   ,   
                            ["step1"  ,  mva_step2  ]   ,  
                          ]
    




#lumis=              {
#                            "mc_lumi"               :   10000   ,
#                            'target_lumi'           :   12864.0   ,
#                            'DataICHEP_lumi'        :   12864.4    ,
#                            'DataBlind_lumi'        :   36416.8     ,
#                            'DataUnblind_lumi'      :   4303.0  ,
#                    }


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







mc_filters_list = [ 
                        'Flag_Filters'
                        #"!mva_trainingEvent"
                    ]
data_filters_list = mc_filters_list




weights = cuts.weights

if isMVA:
    def_generalTag = mva_friendtree_map[1][1].replace("/","__")
else:
    #generalTag = "Mar17v18"
    #def_generalTag = "May17_v3"
    def_generalTag = "June17_v3"

generalTag = getattr(args, "generalTag")
generalTag = generalTag if generalTag else def_generalTag


if sigOpt.lower() == 'ewk':
    generalTag += "_EWK_"

cfgTag     = os.path.basename(os.path.dirname(os.path.realpath(__file__)) )


cfg = TaskConfig(
                   #runTag         =  os.path.basename(os.path.dirname(os.path.realpath(__file__)) ) + "_"  + sr1c_opt.title()  + "_"+lepTag + "_"+weight_tag + ( "_%s"%btag.upper() ) +mcMatchTag,   ## should be the same as the name of the directory that the cfg is in
                   #runTag         =  cfgTag  + "_" + generalTag + "_"+lepTag + "_"+weight_tag,  # + ( "_%s"%btag.upper() ) +mcMatchTag , 
                   cfgTag         =   cfgTag , 
                   runTag         =   lepTag + "_"+weight_tag,  # + ( "_%s"%btag.upper() ) +mcMatchTag , 
                   generalTag     =   generalTag , 
                   taskList       =   task_info['taskList'],
                   ppTag          =   ppTag , 
                   ppStep         =   ppStep,    ## step1 for mva
                   ppUser         =   ppUser , 
                   cmgTag         =   cmgTag , 
                   parameterSet   =   parameterSet,
                   dataDir        =   dataDir,
                   mcDir          =   mcDir, 
                   saveDirBase    =   "%s/www/T2Deg13TeV/"%(os.path.expandvars("$HOME")  ) ,
                   cutInst        =   cutInstList,
                   plots          =   plots.plots         , 
                   plotList       =   plotList, 
                   nminus1s       =   plots.nminus1s,
                   taskModules     =  [ cfgFunctions , Systematics , fakeEstimate ],  
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
                                        #"getData"      :    task_info.get("data",)    ,
                                        "getData"      :   bool(args.data) , 
                                        "weights"      :    weights     ,
                                        "def_weights"  :    def_weights     ,
                                        #"data_triggers":    'HLT_PFMET100_PFMHT100_IDTight || HLT_PFMET110_PFMHT110_IDTight || HLT_PFMET120_PFMHT120_IDTight || HLT_PFMET90_PFMHT90_IDTight'             if '80' in cmgTag  else '' ,
                                        "data_filters" :    ' && '.join(data_filters_list) if '80' in cmgTag else '', 
                                        "mc_filters"   :    ' && '.join(mc_filters_list) if '80' in cmgTag else '',
                                        #"applyMCTriggers": False,# "data_met"
                                      } , 
                   lumi_info       = settings['lumis'],
                   nProc          =  15, 
                )

cfg.weight_tag_list = weights_info['weight_tag_list']
cfg.weight_tag = weights_info['weight_tag']
cfg.lumiWeight = lumiWeight
cfg.cuts = cuts
cfg.cuts._update()
cfg.generalTag = generalTag
cfg.cfgTag     = cfgTag
cfg.skim       = ppSkim
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



if isMVA:
    def getMVATrainWeightCorr(sample, train_var="mva_trainingEvent"):
        if sample.isData:
            return

        isLIPWeights =  step2=='lip'
        mvaIdIndex = "%s"%cfg.cuts.vars.mvaIdIndex


        if isLIPWeights:
            if not any(y in sample.name for y in ['WJets','TTJets']):
                return 
            str_presel               = cfg.cuts.presel_train_LIP.combined
            sample.tree.SetAlias(   "mva_train_presel", str_presel)
            str_odd_evt              =  "(evNumber%2)"
            str_even_evt              =  "((evNumber+1)%2)"
            str_trained              =  str_odd_evt
            str_presel_not_trained   =  "(!{trained})*(mva_train_presel)".format(trained=str_trained)
            str_mva_weight           =  "( ({{mvaLumiCorFactor:0.4f}}* (!{trained})*(mva_train_presel)) +( !mva_train_presel)  )".format(mvaIdIndex = mvaIdIndex, trained= str_trained)
    
        else:
            str_presel               = 'mva_preselectedEvent[{mvaIdIndex}]'.format(mvaIdIndex = mvaIdIndex)
            str_presel_not_trained   = "(!mva_trainingEvent[{mvaIdIndex}])*(mva_preselectedEvent[{mvaIdIndex}])".format(mvaIdIndex = mvaIdIndex)
            str_mva_weight           = "( ({{mvaLumiCorFactor:0.4f}}* (!mva_trainingEvent[{mvaIdIndex}])*(mva_preselectedEvent[{mvaIdIndex}])) +(!mva_preselectedEvent[{mvaIdIndex}])  )".format(mvaIdIndex = mvaIdIndex)


        presel_events  = sample.tree.Draw("(1)", str_presel ,'goff')
    
        if not presel_events and not isLIPWeights:
            return 
    
        presel_not_trained_events = sample.tree.Draw("(1)", str_presel_not_trained, 'goff')
        if int(presel_not_trained_events)==int(presel_events):
            return 
        lumiWeightCorr =  float(presel_events)/ presel_not_trained_events
        #sample.weight = "( ({mvaLumiCorFactor:0.4f}* (!mva_trainingEvent[{mvaIdIndex}])*(mva_preselectedEvent[{mvaIdIndex}]))  )".format(mvaLumiCorFactor = lumiWeightCorr , mvaIdIndex = mvaIdIndex)
        sample.weight  = str_mva_weight.format( mvaLumiCorFactor = lumiWeightCorr )
        print sample.name, sample.weight
        return 
    
    for s in cfg.signalList + cfg.bkgList + ( [cfg.data] if cfg.data else [] ):
        if not s in cfg.samples.keys():
            continue
        print "Adding Friend Trees for :", cfg.samples[s].name
        cfg.samples[s].addFriendTrees( "Events", mva_friendtree_map , check_nevents=False, alias=step2)
        getMVATrainWeightCorr( cfg.samples[s] )


#tasks = [cfg, ]  submit multiple tasks TO BE IMPLEMENTED
