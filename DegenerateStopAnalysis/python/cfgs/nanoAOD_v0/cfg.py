import os, sys
import ROOT
import pickle
from copy import deepcopy

from Workspace.DegenerateStopAnalysis.scripts.degStop import args
from Workspace.DegenerateStopAnalysis.tools.TaskConfig import TaskConfig
import Workspace.DegenerateStopAnalysis.tools.cfgFunctions as cfgFunctions
import Workspace.DegenerateStopAnalysis.tools.fakeEstimate as fakeEstimate

from Workspace.DegenerateStopAnalysis.tools.degTools import *
from Workspace.DegenerateStopAnalysis.tools.massPoints import MassPoints
from Workspace.DegenerateStopAnalysis.tools.degPlots import DegPlots
from Workspace.DegenerateStopAnalysis.tools.degCuts import Cuts
import Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo as sampleInfo

# TDR style
setup_style()

# sample names
sample_names = sampleInfo.sample_names
defBkgList = ["ttx", "st", "vv", "dy5to50", "dy", "qcd", "z", "tt_2l", "tt_1l", "w"]

generalTag = args.generalTag
sysTag     = args.sysTag
dataset    = args.dataset
nanoAOD    = args.nanoAOD 
year       = args.year
getData    = args.getData
lepCol     = args.lepCol
jetCol     = args.jetCol
tauCol     = args.tauCol
lep        = args.lep

lepTag = lepCol + "_" + lep

lepThresh = getattr(args, "lepThresh", "def")
jetThresh = getattr(args, "jetThresh", "def")


if nanoAOD:
    dataEra = "Run" + year
    if year == "2016":
        mcEra = "Summer16"
        campaign = "05Feb2018"
    elif year == "2017":
        mcEra = "Fall17"
        campaign = "14Dec2018"
    elif year == "2018":
        mcEra = "Autumn18"
        campaign = "14Sep2018"
    else:
        print "Wrong year %s. Exiting."%year
        sys.exit()
else:
    campaign = None
    mcEra    = None
    dataEra  = None
    
sr1c_opts = [ 
                "Reload" ,               #0 
                "MT95" ,                 #1   
                "MT95_IncCharge",        #2   
                "MT105_IncCharge_CT250"  #3       
            ]

sr1c_opt = sr1c_opts[2]

mcMatch = args.mcMatch
mcMatchTag = "_mcMatch" if mcMatch else ""
if lepCol == "LepAll" and mcMatch: assert False, "mcMatchId not compatible with LepAll for now!"

### luminosities ###
# bril calc res : /afs/cern.ch/user/n/nrad/public/bril_res/8025_mAODv2_v7/lumis.pkl

lumis = {
    '2016': {
        'Unblind': 4303.0,
        
        # MET PD
        'MET':       35854.9, 
        #'MET_ICHEP': 12864.4,
       
        # SingleMu PD
        'SingleMu': 35808.7,

        # SingleEl PD
        'SingleEl': 35725.2,
        
        # SingleLep
        'SingleLep': 35767.0,
        
        # JetHT PD
        'JetHT': 35865.2,
    },

    '2017': {
        'Unblind': 4303.0,
        
        # MET PD
        'MET_Run2017_14Dec2018': 41529.0, # NOTE: from Twiki 
    }    
}

for yr in lumis:
    for dataset_name in lumis[yr]:
        sample_names.update({dataset_name:{'niceName':dataset_name, 'latexName':"Data %s"%dataset_name}})
        lumiTag = sampleInfo.makeLumiTag(lumis[yr][dataset_name],latex=True) 
                
        if not sample_names[dataset_name]['latexName']:
            sample_names[dataset_name]['latexName'] = 'Data %s'%dataset_name 
        if not sample_names[dataset_name]['niceName']:
            sample_names[dataset_name]['niceName'] = dataset_name

dataset_dict = {
    'MET' : {
        '2016': {
            '05Feb2018' : { # set same as 03Feb2017 #FIXME: recalculate
                'B':{'lumi':5787.968           , 'runs': ('272007', '275376')}, 
                'C':{'lumi':2573.399           , 'runs': ('275657', '276283')}, 
                'D':{'lumi':4248.384           , 'runs': ('276315', '276811')}, 
                'E':{'lumi':4008.663           , 'runs': ('276831', '277420')}, 
                'F':{'lumi':3101.618           , 'runs': ('277772', '278808')}, 
                'G':{'lumi':7529.196           , 'runs': ('278820', '280385')}, 
                'H':{'lumi':8390.540 + 215.149 , 'runs': ('280919', '284044')},
            },
 
            '03Feb2017' : {
                'B':{'lumi':5787.968           , 'runs': ('272007', '275376')}, 
                'C':{'lumi':2573.399           , 'runs': ('275657', '276283')}, 
                'D':{'lumi':4248.384           , 'runs': ('276315', '276811')}, 
                'E':{'lumi':4008.663           , 'runs': ('276831', '277420')}, 
                'F':{'lumi':3101.618           , 'runs': ('277772', '278808')}, 
                'G':{'lumi':7529.196           , 'runs': ('278820', '280385')}, 
                'H':{'lumi':8390.540 + 215.149 , 'runs': ('280919', '284044')}, 
            },

            '23Sep2016' : {
                'B': {'lumi': 5667.931          , 'runs': ('272007', '275376')},
                'C': {'lumi': 2638.567          , 'runs': ('275657', '276283')},
                'D': {'lumi': 4353.448          , 'runs': ('276315', '276811')},
                'E': {'lumi': 3204.684          , 'runs': ('276831', '277420')},
                'F': {'lumi': 3185.971          , 'runs': ('277772', '278808')},
                'G': {'lumi': 7721.057          , 'runs': ('278820', '280385')},
                'H': {'lumi': 8635.591 + 221.442, 'runs': ('280919', '284044')},
            },
        }
    }
}

dataset_info = {
    'MET':
        [
        ['MET',        ['B','C','D','E','F','G','H'], {'shortName':'dBlind', 'niceName':'', 'latexName':''}],
        ['MET_ICHEP',  ['B','C','D']                , {'shortName':'dICHEP', 'niceName':'', 'latexName':''}],
        ['MET_BCDE',   ['B','C','D','E']            , {'shortName':'dBCDE' , 'niceName':'', 'latexName':''}],
        ['MET_BCDEF',  ['B','C','D','E','F']        , {'shortName':'dBCDEF', 'niceName':'', 'latexName':''}],
        ['MET_GH',     ['G', 'H']                   , {'shortName':'dGH'   , 'niceName':'', 'latexName':''}],
    ]
}

names_dict = {}
for pd in dataset_info:
    for dataset_name, eras, name_dict in dataset_info[pd]:
        for yr in dataset_dict[pd]:
            for camp in dataset_dict[pd][yr]:
                dataset_name_final = '%s_Run%s_%s'%(dataset_name, yr, camp)
                names_dict[dataset_name_final] = dict(name_dict)

                lumi = sampleInfo.getDataLumi(dataset_dict[pd][yr][camp], eras)
                lumis[yr][dataset_name_final] = lumi
                lumiTag = sampleInfo.makeLumiTag(lumi,latex=True)

                if not names_dict[dataset_name_final]['latexName']:
                    names_dict[dataset_name_final]['latexName'] = 'Data %s'%dataset_name_final
                if not names_dict[dataset_name_final]['niceName']:
                    names_dict[dataset_name_final]['niceName'] = dataset_name_final

                names_dict[dataset_name_final]['latexName'] += " (%s)"%lumiTag
                sample_names.update(names_dict)

# samples
ppSets = {
    "nanoAOD_v6_0-0": {'user':"mzarucki02", 'analysisPackage':"DegenerateStopAnalysis", 'parameterSet':"processing_RunII_v6_0",         'mcDir':"%s_%s"%(mcEra, campaign),    'dataDir':"%s_%s"%(dataEra, campaign), 'ppTag':'nanoAOD_v6_0-0',        'cmgTag':None, 'ppStep':None}, 
    "cmgPP_v10":      {'user':"mzarucki02", 'analysisPackage':None,                     'parameterSet':"analysisHephy_13TeV_2016_v2_6", 'mcDir':"RunIISummer16MiniAODv2_v10", 'dataDir':"Data2016_v10",              'ppTag':"80X_postProcessing_v0", 'cmgTag':"8025_mAODv2_v10", 'ppStep':"step1"},
    "cmgPP_v7":       {'user':"nrad01",     'analysisPackage':None,                     'parameterSet':"analysisHephy_13TeV_2016_v2_3", 'mcDir':"RunIISummer16MiniAODv2_v7",  'dataDir':"Data2016_v7",                  'ppTag':"80X_postProcessing_v1", 'cmgTag':"8025_mAODv2_v7", 'ppStep':"step1"},
    }

ppSet = args.ppSet
ppUser          = ppSets[ppSet]['user']
analysisPackage = ppSets[ppSet]['analysisPackage']
parameterSet    = ppSets[ppSet]['parameterSet']
ppTag           = ppSets[ppSet]['ppTag']
cmgTag          = ppSets[ppSet]['cmgTag']
ppStep          = ppSets[ppSet]['ppStep']
dataDir         = ppSets[ppSet]['dataDir']
mcDir           = ppSets[ppSet]['mcDir']

if nanoAOD:
    ppDir = "/afs/hephy.at/data/{ppUser}/nanoAOD/{analysisPackage}/postProcessing/{parameterSet}/{ppTag}"
else:
    ppDir = '/afs/hephy.at/data/{ppUser}/cmgTuples/postProcessed_mAODv2/{cmgTag}/{ppTag}/{parameterSet}/{ppStep}'

ppDir = ppDir.format(ppUser = ppUser, analysisPackage = analysisPackage, parameterSet = parameterSet, ppTag = ppTag, cmgTag = cmgTag, ppStep = ppStep)

ppDirs = {
    'mc_path':     ppDir + "/" + mcDir,
    'signal_path': ppDir + "/" + mcDir,
    'data_path':   ppDir + "/" + dataDir,
    }

# cut and weight options
cmgVars = not nanoAOD

weights_input = args.weights
lumiWeight = 'target_lumi'
weights_info = sampleInfo.evalInputWeights(weights_input, lumiWeight)

options     = weights_info['options']
def_weights = weights_info['def_weights']
weight_tag  = weights_info['weight_tag']

cutWeightOptions = sampleInfo.getCutWeightOptions(
    dataset = dataset,
    campaign = campaign, 
    year = year,
    lepCol = lepCol,
    lep = "lep",
    lepTag = "def",
    tightWP = "",
    jetCol = jetCol,
    jetTag = "def",
    tauCol = tauCol,
    btagSF = "SF",
    mvaId = None,
    bdtcut_sr = None,
    bdtcut_cr = None,
    lumis = lumis,
    cmgVars = cmgVars,
    options = options,
    )

settings = cutWeightOptions['settings']
settings_update = weights_info['settings_update']
settings.update(settings_update)

if cutWeightOptions['settings']['year'] != "2016":
    cutWeightOptions['options'].remove('lepSF') # FIXME: update when rest of lepton SF are available

if cmgVars and parameterSet == 'analysisHephy_13TeV_2016_v2_3':
    cutWeightOptions['options'].append('STXSECFIX')
    if 'lepSF' in cutWeightOptions['options']:
        cutWeightOptions['options'].remove('lepSF')
        cutWeightOptions['options'].append('lepsffix')

alternative_variables = {}

cuts = Cuts(cutWeightOptions['settings'], cutWeightOptions['def_weights'], cutWeightOptions['options'], alternative_variables)
weights = cuts.weights

lepTag = lepTag + "_"     + settings['lepTag'] if settings['lepTag'] else lepTag
lepTag = lepTag + "_Jet_" + settings['jetTag'] if settings['jetTag'] else lepTag

plots = DegPlots(lepCol, lep, lepThresh = lepThresh, jetThresh = jetThresh)

limitCuts = cuts.bins_sum

plotCuts = [cuts.presel, cuts.sr1, cuts.cr1] #, cuts.sr2, cuts.sr1a, cuts.sr1b, cuts.sr1c, cuts.cr1, cuts.cr2, cuts.crtt2]
crCuts = [cuts.bins_cr]


mc_filters_list = ['Flag_Filters']

data_filters_list = mc_filters_list

bkgList = args.bkgs
if not bkgList: 
    bkgList = defBkgList

# signals

sigOpt = args.sigOpt

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
elif sigOpt.lower() =='bm1':
    sigList = ['t2tt300_270', 't2tt300_290', 't2tt300_220']
elif sigOpt.lower() =='bm2':
    sigList = ['t2tt375_365', 't2tt500_470' ]
    #sigList = ['t2tt300_270' ]
elif sigOpt.lower() =='bm4':
    sigList = ['t2tt500_470', 't2tt500_490', 't2tt500_420']
elif sigOpt.lower() =='bm':
    #sigList = ['t2tt300_270', 't2ttold300_270' , 't2tt300_290', 't2ttold300_290' ]
    sigList  = ['t2tt300_270', 't2tt500_470', 't2tt375_365', 't2tt375_295' ]
    sigList += ['t2bw300_270', 't2bw500_470', 't2bw375_365', 't2bw375_295' ]
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
elif sigOpt.lower() in ['c1c1', 'c1n1', 'hino', 'n2n1', 'tchiwz']:
    sigLists = {
          'c1c1': [  'c1c1h150_120',
                    'c1c1h175_167p5',
                    'c1c1h225_205'],
        'c1n1':   [  'c1n1h140_110',
                    'c1n1h180_172p5',
                    'c1n1h220_200'],
         'hino':  [  'hino120_1000',
                    'hino160_500',
                    'hino220_300'],
         'n2n1':  [  'n2n1h140_110',
                    'n2n1h160_152p5',
                    'n2n1h180_160'],
         'n2c1':[
                      'n2c1h140_125',
                      'n2c1h180_176p25',
                      'n2c1h220_210',
                ],
         'tchiwz':[  'tchiwz150_120',
                    'tchiwz175_167p5',
                    'tchiwz250_230'],
                }
    sigList = sigLists[sigOpt.lower()]
elif sigOpt.lower() == 'newsigs':
    sigList = [
             'c1c1h150_120',
             'c1c1h175_167p5',
             'c1c1h225_205',
             'c1n1h140_110',
             'c1n1h180_172p5',
             'c1n1h220_200',
             'hino120_1000',
             'hino160_500',
             'hino220_300',
             'n2n1h140_110',
             'n2n1h160_152p5',
             'n2n1h180_160',
             'n2c1h140_125',
             'n2c1h180_176p25',
             'n2c1h220_210',
             'tchiwz150_120',
             'tchiwz175_167p5',
             'tchiwz250_230'
            ]
else:
    massPointsFull = MassPoints(dmOpt, (750,801,25))
    sigList = massPointsFull.sigList

if sigOpt.lower() in ['ewk', 'newsigs']:
    generalTag += "_EWK_"
elif sigOpt.lower() in ['c1c1', 'c1n1', 'hino', 'n2n1', 'tchiwz', 'n2c1']:
    generalTag += '_%s_'%(sigOpt.upper())

plotMStopLSPs =[(300,270), (300,290), (300,220)]
plotSignalList = sigList

## Tasks

tasks_info = {
    'bkg_est':   {'taskList' : ['bkg_est'],        'sigList': plotSignalList,         'massPoints':[],                        'cutInstList':crCuts,      'plotList':plots.plots.keys(),     'data': dataset},
    'yields':    {'taskList' : ['yields'],         'sigList': plotSignalList,         'massPoints':[],                        'cutInstList':crCuts,      'plotList':plots.plots.keys(),     'data': dataset},
    'cut_flow':  {'taskList' : ['cut_flow'],       'sigList': plotSignalList,         'massPoints':[],                        'cutInstList':crCuts,      'plotList':[],                     'data': dataset},
    'explimits': {'taskList' : ['calc_sig_limit'], 'sigList': massPointsFull.sigList, 'massPoints':massPointsFull.mstop_lsps, 'cutInstList':limitCuts,   'plotList':plots.plots.keys(),     'data': None},
    'plots':     {'taskList' : ['draw_plots'],     'sigList': plotSignalList,         'massPoints':plotMStopLSPs,             'cutInstList':plotCuts[:], 'plotList':plots.plots.keys()[:],  'data': None},
    'data':      {'taskList' : ['data_plots'],     'sigList': plotSignalList,         'massPoints':plotMStopLSPs,             'cutInstList':plotCuts[:], 'plotList': plots.plots.keys()[:], 'data':dataset},
    }

task = args.task
task_info = tasks_info[task]

postFuncs = args.postFuncs
task_info['taskList'].extend(postFuncs)

sigList = task_info['sigList']

if args.small:
    sigList = sigList[0]

cutInstList = [] 
if args.cutInst:
    for cutInstName in args.cutInst:
        if hasattr(cuts, cutInstName):
            cutInstList.append(getattr(cuts,cutInstName))
        else:
            print args.cut ,"was not found as a attribute of cuts"
            cutInstList = task_info['cutInstList']
else:
    cutInstList = task_info['cutInstList']

plotList = []
if args.plot:
    for p in args.plot:
        if hasattr(plots.plots, p):
            plotList.append(p)
        else:
            print "Skipping plot %s, not found in %s"%(p, plots.plots.keys())
else:
    plotList = task_info['plotList']

cfgTag = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
runTag = lepTag + "_" + weight_tag
saveDirBase = "%s/www/plots/degStop/%s"%(os.path.expandvars("$HOME"), cfgTag)

getSignal = len(sigList) > 0
sampleList = bkgList + sigList 

sample_info = {
    "sampleList":      sampleList,
    "wtau":            False, 
    "useHT":           True, 
    "skim":            args.skim, 
    "scan":            getSignal,
    "getData":         getData, 
    "data_filters":    ' && '.join(data_filters_list), 
    "mc_filters":      ' && '.join(mc_filters_list),
    "kill_low_qcd_ht": False,
    }

cfg = TaskConfig(
    cfgTag           = cfgTag, 
    generalTag       = generalTag, 
    runTag           = runTag,
    sysTag           = sysTag,
    taskList         = task_info['taskList'],
    plotList         = plotList,
    nanoAOD          = nanoAOD,
    ppSet            = ppSet,
    ppDirs           = ppDirs,
    cutInst          = cutInstList,
    saveDirBase      = saveDirBase,
    taskModules      = [cfgFunctions, fakeEstimate],  
    plots            = plots.plots,
    cutWeightOptions = cutWeightOptions, 
    settings         = cutWeightOptions['settings'], 
    mcEra            = mcEra, 
    sample_info      = sample_info, 
    bkgList          = bkgList,
    sigList          = sigList,
    nProc            = 15, 
    )
