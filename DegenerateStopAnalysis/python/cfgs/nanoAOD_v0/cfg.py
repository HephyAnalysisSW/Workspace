import os, sys
import ROOT
import pickle
from copy import deepcopy

from Workspace.DegenerateStopAnalysis.scripts.degStop import args
import Workspace.DegenerateStopAnalysis.scripts.fakeEstimate as fakeEstimate
from Workspace.DegenerateStopAnalysis.tools.TaskConfig import TaskConfig
import Workspace.DegenerateStopAnalysis.tools.cfgFunctions as cfgFunctions

from Workspace.DegenerateStopAnalysis.tools.degTools import setup_style, makeLumiTag, getDataLumi 
from Workspace.DegenerateStopAnalysis.tools.massPoints import MassPoints
from Workspace.DegenerateStopAnalysis.tools.degPlots import DegPlots
from Workspace.DegenerateStopAnalysis.tools.degCuts import Cuts
from Workspace.DegenerateStopAnalysis.tools.degVars import evalInputWeights
from Workspace.DegenerateStopAnalysis.samples.samplesInfo import sample_names, getCutWeightOptions

# TDR style
setup_style()

# sample names
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
    era = "Run" + year
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
    era  = None
    mcEra    = None
    campaign = None
    
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

allDataEras = {
    '2016': ['B', 'C', 'D', 'E', 'F', 'G', 'H'],
    '2017': ['B', 'C', 'D', 'E', 'F'],
    '2018': ['A', 'B', 'C', 'D'],
}

dataset_dict = {
    '2016': {
        'MET' : {
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
        },
    },

    '2017': { # approx values taken from https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2017Analysis#Data
        'MET':{
            '14Dec2018':{
                'B':{'lumi': 4823.0, 'runs':('297046', '299329')},
                'C':{'lumi': 9664.0, 'runs':('299368', '302029')},
                'D':{'lumi': 4252.0, 'runs':('302030', '303434')},
                'E':{'lumi': 9278.0, 'runs':('303824', '304797')},
                'F':{'lumi':13540.0, 'runs':('305040', '306462')},
            },
        },
    },

    '2018': { # approx values taken from https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2018Analysis#DATA
        'MET':{
            '14Dec2018':{
                'A':{'lumi':14000.0, 'runs':('315252', '316995')},
                'B':{'lumi': 7100.0, 'runs':('317080', '319310')},
                'C':{'lumi': 6940.0, 'runs':('315252', '316995')},
                'D':{'lumi':31930.0, 'runs':('320673', '325175')},
            },
        },
    },
}


# FIXME: re-calculate
dataset_dict['2016']['MET']['05Feb2018'] =        dataset_dict['2016']['MET']['03Feb2017']
dataset_dict['2018']['SingleMuon'] = {'14Dec2018':dataset_dict['2018']['MET']['14Dec2018']}
dataset_dict['2018']['DoubleMuon'] = {'14Dec2018':dataset_dict['2018']['MET']['14Dec2018']}
dataset_dict['2018']['EGamma']     = {'14Dec2018':dataset_dict['2018']['MET']['14Dec2018']}
dataset_dict['2018']['Charmonium'] = {'14Dec2018':dataset_dict['2018']['MET']['14Dec2018']}

dataEras = {
    'ICHEP':{'bins':['B','C','D'],         'name_dict':{'shortName':'dICHEP', 'niceName':'', 'latexName':''}},
    'BCDE' :{'bins':['B','C','D','E'],     'name_dict':{'shortName':'dBCDE',  'niceName':'', 'latexName':''}},
    'BCDEF':{'bins':['B','C','D','E','F'], 'name_dict':{'shortName':'dBCDEF', 'niceName':'', 'latexName':''}},
    'GH'   :{'bins':['G', 'H'],            'name_dict':{'shortName':'dGH',    'niceName':'', 'latexName':''}},
}

dataset_info = {}

for yr in dataset_dict:
    dataset_info[yr] = {}
    
    if yr not in lumis:
        lumis[yr] = {}

    for pd in dataset_dict[yr]:
        dataset_info[yr][pd] = {}

        for camp in dataset_dict[yr][pd]:
            # total lumi
            dataset_name = '%s_Run%s_%s'%(pd, yr, camp)
            lumi = getDataLumi(dataset_dict[yr][pd][camp], allDataEras[yr])

            lumis[yr][dataset_name] = lumi

            dataset_info[yr][pd].update({dataset_name:{'bins':allDataEras[yr], 'name_dict':{'shortName':'d', 'niceName':'', 'latexName':''}, 'lumi':lumi}})

            # specific era bins       
            for dataEra in dataEras:
                dataset_name_final = '%s_Run%s%s_%s'%(pd, yr, dataEra, camp)

                try:
                    lumi = getDataLumi(dataset_dict[yr][pd][camp], dataEras[dataEra]['bins'])
                except KeyError as err:
                    #print "KeyError:", err 
                    continue

                lumis[yr][dataset_name_final] = lumi

                dataset_info[yr][pd].update({dataset_name_final:{'bins':dataEras[dataEra]['bins'], 'name_dict':dataEras[dataEra]['name_dict'], 'lumi':lumi}})

        for name in dataset_info[yr][pd]:
            sample_names[name] = {}
            #sample_names.update({name: dataset_info[yr][pd][name]['name_dict']})
            lumiTag = makeLumiTag(dataset_info[yr][pd][name]['lumi'], latex = True)

            #if not sample_names[name]['latexName']:
            sample_names[name]['latexName'] = 'Data %s'%name
            #if not sample_names[name]['niceName']:
            sample_names[name]['niceName'] = name

            sample_names[name]['latexName'] += " (%s)"%lumiTag

# FIXME: re-calculate # NOTE: from latest PdmV table (https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVAnalysisSummaryTable)
lumis['2017']['MET_Run2017_14Dec2018']        = 41529.0
lumis['2018']['MET_Run2018_14Dec2018']        = 59740.0
lumis['2017']['SingleMuon_Run2017_14Dec2018'] = 41529.0
lumis['2018']['SingleMuon_Run2018_14Dec2018'] = 59740.0
lumis['2017']['DoubleMuon_Run2017_14Dec2018'] = 41529.0
lumis['2018']['DoubleMuon_Run2018_14Dec2018'] = 59740.0
lumis['2017']['EGamma_Run2017_14Dec2018']     = 41529.0
lumis['2018']['EGamma_Run2018_14Dec2018']     = 59740.0
lumis['2017']['Charmonium_Run2017_14Dec2018'] = 41529.0
lumis['2018']['Charmonium_Run2018_14Dec2018'] = 59740.0

# samples
ppSets = {
    "nanoAOD_v6_0-0": {'user':"mzarucki01", 'analysisPackage':"DegenerateStopAnalysis", 'parameterSet':"processing_RunII_v6_0",         'mcDir':"%s_%s"%(mcEra, campaign),    'dataDir':"%s_%s"%(era, campaign), 'ppTag':'nanoAOD_v6_0-0',        'cmgTag':None, 'ppStep':None}, 
    "cmgPP_v10":      {'user':"mzarucki02", 'analysisPackage':None,                     'parameterSet':"analysisHephy_13TeV_2016_v2_6", 'mcDir':"RunIISummer16MiniAODv2_v10", 'dataDir':"Data2016_v10",              'ppTag':"80X_postProcessing_v0", 'cmgTag':"8025_mAODv2_v10", 'ppStep':"step1"},
    "cmgPP_v7":       {'user':"nrad01",     'analysisPackage':None,                     'parameterSet':"analysisHephy_13TeV_2016_v2_3", 'mcDir':"RunIISummer16MiniAODv2_v7",  'dataDir':"Data2016_v7",               'ppTag':"80X_postProcessing_v1", 'cmgTag':"8025_mAODv2_v7",  'ppStep':"step1"},
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
weights_info = evalInputWeights(weights_input, lumiWeight)

options     = weights_info['options']
def_weights = weights_info['def_weights']
weight_tag  = weights_info['weight_tag']

cutWeightOptions = getCutWeightOptions(
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

cuts = Cuts(settings, cutWeightOptions['def_weights'], cutWeightOptions['options'], alternative_variables)
weights = cuts.weights

lepTag = lepTag + "_"     + settings['lepTag'] if settings['lepTag'] else lepTag
lepTag = lepTag + "_Jet_" + settings['jetTag'] if settings['jetTag'] else lepTag

plots = DegPlots(lepCol, lep, lepThresh = lepThresh, jetThresh = jetThresh)

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

plotMStopLSPs = [(300,270), (300,290), (300,220)]
plotSignalList = sigList

# Pre-defined cuts
limitCuts = [cuts.bins_sum]
plotCuts  = [cuts.presel]
crCuts    = [cuts.bins_cr]

## Tasks

tasks_info = {
    'bkg_est':   {'taskList':['bkg_est'],        'sigList':plotSignalList,         'massPoints':[],                        'cutInstList':crCuts,      'plotList':plots.plots.keys(), 'data':dataset},
    'yields':    {'taskList':['yields'],         'sigList':plotSignalList,         'massPoints':[],                        'cutInstList':crCuts,      'plotList':plots.plots.keys(), 'data':dataset},
    'cut_flow':  {'taskList':['cut_flow'],       'sigList':plotSignalList,         'massPoints':[],                        'cutInstList':crCuts,      'plotList':[],                 'data':dataset},
    'explimits': {'taskList':['calc_sig_limit'], 'sigList':massPointsFull.sigList, 'massPoints':massPointsFull.mstop_lsps, 'cutInstList':limitCuts,   'plotList':plots.plots.keys(), 'data':None},
    'plots':     {'taskList':['draw_plots'],     'sigList':plotSignalList,         'massPoints':plotMStopLSPs,             'cutInstList':plotCuts,    'plotList':plots.plots.keys(), 'data':None},
    'dataMC':    {'taskList':['data_plots'],     'sigList':plotSignalList,         'massPoints':plotMStopLSPs,             'cutInstList':plotCuts,    'plotList':plots.plots.keys(), 'data':dataset},
    }

task = args.task
task_info = tasks_info[task]

postFuncs = args.postFuncs
task_info['taskList'].extend(postFuncs)

sigList = task_info['sigList']

if args.small:
    sigList = sigList[0]

cutInstList = [] 
if args.cuts:
    for cut in args.cuts:
        if hasattr(cuts, cut):
            cutInstList.append(getattr(cuts,cut))
        else:
            print cut, "was not found as a attribute of cuts. Exiting."
            sys.exit()
else:
    cutInstList = task_info['cutInstList']
    print "\nUsing pre-defined cutInstList for task %s:"%task, [c.name for c in cutInstList]

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
    settings         = settings, 
    mcEra            = mcEra, 
    sample_info      = sample_info, 
    dataset_info     = dataset_info, 
    bkgList          = bkgList,
    sigList          = sigList,
    nProc            = 15, 
    )
