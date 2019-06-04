# baselineSamplesInfo.py
# Baseline Lumis, Triggers, Filters, Cuts and Weight Options
import os, re
import collections

### sample names ###
sample_names = {
    # data
    'data'   :{'niceName':'Data'      , 'latexName':"Data"                    },

    # background mc
    'w'      :{'niceName':'WJets'      , 'latexName':'W+Jets'                 },
    'tt'     :{'niceName':'tt+Jets'    , 'latexName':'t#bar{t}'               },
    'tt_1l'  :{'niceName':'tt (1l)'    , 'latexName':'t#bar{t}(1l)'           },
    'tt_2l'  :{'niceName':'tt (2l)'    , 'latexName':'t#bar{t}(2l)'           }, 
    'tt_pow' :{'niceName':'tt (pow)'   , 'latexName':'t#bar{t}(Powheg)'       },
    'ttx'    :{'niceName':'ttX'        , 'latexName':'t#bar{t}X'              },
    'fakes'  :{'niceName':'Fakes'      , 'latexName':"Nonprompt"              },
    'z'      :{'niceName':'Zinv'       , 'latexName':'Z#rightarrow#nu#nu+Jets'},
    'qcd'    :{'niceName':'QCD'        , 'latexName':'QCD'                    },
    'dy'     :{'niceName':'DY (M50)'   , 'latexName':'Z#gamma*+Jets (M50)'    },
    'dy5to50':{'niceName':'DY (M5to50)', 'latexName':'Z#gamma*+Jets (M5to50)' },
    'vv'     :{'niceName':'Diboson'    , 'latexName':"VV"                     },
    'st'     :{'niceName':'Single Top' , 'latexName':'Single Top'             },
    'others' :{'niceName':'Others'     , 'latexName':"Rare"                   },
    'total'  :{'niceName':'Total'      , 'latexName':"Total"                  },
    
    # signals
    't2tt'   :{'niceName':'T2tt_'      , 'latexName':'T2tt'                   },
    't2bw'   :{'niceName':'T2bW_'      , 'latexName':'T2bW'                   },
    'hino'   :{'niceName':'Hino_'      , 'latexName':'Hino'                   },
    'n2c1h'  :{'niceName':'N2C1H_'     , 'latexName':'N2C1'                   },
    'c1c1h'  :{'niceName':'C1C1H_'     , 'latexName':'C1C1'                   },
    'c1n1h'  :{'niceName':'C1N1H_'     , 'latexName':'C1N1'                   },
    'n2n1h'  :{'niceName':'N2N1H_'     , 'latexName':'N2N1'                   },
    'tchiwz' :{'niceName':'TChiWZ_'    , 'latexName':'TChiWZ'                 },
    'allSig' :{'niceName':'All Signals', 'latexName':"All Signals"            },
}


for vv in ['vvinc','vv2', 'ww','zz','wz','wwNLO','wzNLO','zzNLO']:
    sample_names[vv]= {'latexName':vv.upper(), 'niceName':vv.upper() }

for short_name, sample_name in sample_names.items():
    sample_name['shortName'] = short_name

### luminosities ###
# bril calc res : /afs/cern.ch/user/n/nrad/public/bril_res/8025_mAODv2_v7/lumis.pkl

lumis = {
    '2016': {
        'Unblind': 4303.0,
        
        # MET PD
        #'MET':       35854.9, 
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

def makeLumiTag(lumi, latex=False):
    """ lumi given in pb """
    if latex:
        tag = "%0.1ffb^{-1}"%(round(lumi/1000.,2))
    else:
        tag = "%0.1ffbm1"%(round(lumi/1000.,2))
    return tag

for year in lumis:
    for dataset in lumis[year]:
        sample_names.update({dataset:{'niceName':dataset, 'latexName':"Data %s"%dataset}})
        lumiTag = makeLumiTag(lumis[year][dataset],latex=True) 
                
        if not sample_names[dataset]['latexName']:
            sample_names[dataset]['latexName'] = 'Data %s'%dataset 
        if not sample_names[dataset]['niceName']:
            sample_names[dataset]['niceName'] = dataset
                
        sample_names[dataset]['latexName'] += " (%s)"%lumiTag

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

def getDataLumi(lumi_dict, eras):
    lumi = sum([lumi_dict[era]['lumi'] for era in eras])
    return round(lumi,1)

names_dict = {}
for pd in dataset_info:
    for dataset_name, eras, name_dict in dataset_info[pd]:
        for year in dataset_dict[pd]:
            for camp in dataset_dict[pd][year]:
                dataset_name_final = '%s_Run%s_%s'%(dataset_name, year, camp)
                names_dict[dataset_name_final] = dict(name_dict)
 
                lumi = getDataLumi(dataset_dict[pd][year][camp], eras)
                lumis[year][dataset_name_final] = lumi
                lumiTag = makeLumiTag(lumi,latex=True) 

                if not names_dict[dataset_name_final]['latexName']:
                    names_dict[dataset_name_final]['latexName'] = 'Data %s'%dataset_name_final 
                if not names_dict[dataset_name_final]['niceName']:
                    names_dict[dataset_name_final]['niceName'] = dataset_name_final

                names_dict[dataset_name_final]['latexName'] += " (%s)"%lumiTag
                sample_names.update(names_dict)

### filters ###

filters = ["Flag_Filters"] # NOTE: combination of filters as defined in post-processing

### triggers ###
triggers = {}

triggers['MET'] = [ # MET PD
                 'HLT_PFMET100_PFMHT100_IDTight',
                 'HLT_PFMET110_PFMHT110_IDTight',
                 'HLT_PFMET120_PFMHT120_IDTight',
                 'HLT_PFMET90_PFMHT90_IDTight'
                  ]

triggers['Mu'] = "HLT_Mu50" # non-isolated trigger for SingleMu PD 
triggers['Mu2'] = "HLT_IsoMu24" # SingleMu PD

triggers['El'] = "HLT_Ele27_WPTight_Gsf" # SingleEl PD

triggers['Lep'] = [triggers['Mu2'], triggers['El']]

triggers['Jet'] = [ # JetHT PD
                      "HLT_PFHT800", 
                      "HLT_PFJet450", 
                      "HLT_AK8PFJet450"
                  ]

if type(filters) == type([]):
   filters = '(' + ' && '.join(filters) + ')' #NOTE: assuming we always want to use an 'AND' of filters

for pd in triggers:
    if type(triggers[pd]) == type([]):
        safetrigs = []
        for trig in triggers[pd]:
            safetrigs.append("Alt$(%s,0)"%trig) #NOTE: safety net if trigger is missing, setting it to zero. See https://root-forum.cern.ch/t/issue-when-adding-two-tchains-with-one-containing-a-subset-of-branches-and-using-the-draw-method/
        triggers[pd] = '(' + ' || '.join(safetrigs) + ')' #NOTE: assuming we always want to use an 'OR' of triggers
    else:
        triggers[pd] = "Alt$(%s,0)"%triggers[pd]

sample_info_default = {
    "sampleList" : ["ttx", "st", "vv", "dy5to50", "dy", "qcd", "z", "tt_2l", "tt_1l", "w"],
    "wtau"       : False,
    "useHT"      : True,
    "skim"       : 'preIncLep',
    "scan"       : True,
    "getData"    : True,
    "triggers"   : triggers,
    "filters"    : filters,
    }


### cuts and weights options ###
def getCutWeightOptions(
    dataset = "MET",
    campaign = "05Feb2018",
    year = "2016",
    lepCol = "Lepton",
    lep = "lep",
    lepTag = "def",
    tightWP = "",
    jetCol = "JetClean",
    jetTag = "def",
    tauCol = "TauClean",
    btagSF = "SF",
    mvaId = None,
    bdtcut_sr = None,
    bdtcut_cr = None,
    lumis = lumis,
    cmgVars = False,
    options = ['isr_sig', 'sf', 'STXSECFIX', 'pu', 'isr_nIsr', 'isr_Wpt', 'trig_eff'],
    ):

    cutWeightOptions = {}
    cutWeightOptions['options']  = options 
    
    cutWeightOptions['settings'] = {
                'dataset':   dataset,
                'campaign':  campaign,
                'year':      year,
                'lepCol':    lepCol,
                'lep':       lep,
                'lepTag':    lepTag,
                'tightWP':   tightWP,
                'jetCol':    jetCol,
                'jetTag':    jetTag,
                'tauCol':    tauCol,
                'btagSF':    btagSF,
                'mvaId':     mvaId,
                'bdtcut_sr': bdtcut_sr,
                'bdtcut_cr': bdtcut_cr,
                'cmgVars':   cmgVars,
            }
    
    if campaign:
        datasetFull = '%s_Run%s_%s'%(dataset, year, campaign)
    else:
        datasetFull = dataset   
 
    # setting dataset lumi to target lumi
    lumis['target_lumi'] = lumis[year][datasetFull]
    cutWeightOptions['settings']['lumis'] = lumis
    cutWeightOptions['def_weights'] = ['weight_lumi', datasetFull]

    return cutWeightOptions
