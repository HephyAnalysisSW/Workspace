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

def makeLumiTag(lumi, latex=False):
    """ lumi given in pb """
    if latex:
        tag = "%0.1ffb^{-1}"%(round(lumi/1000.,2))
    else:
        tag = "%0.1ffbm1"%(round(lumi/1000.,2))
    return tag

allDataEras = {
    '2016': ['B', 'C', 'D', 'E', 'F', 'G', 'H'],
    '2017': ['B', 'C', 'D', 'E', 'F'],
    '2018': ['A', 'B', 'C', 'D'],
}

dataset_dict = {
    '2016':{
        'MET':{
            '03Feb2017':{
                'B':{'lumi':5787.968,           'runs':('272007', '275376')}, 
                'C':{'lumi':2573.399,           'runs':('275657', '276283')}, 
                'D':{'lumi':4248.384,           'runs':('276315', '276811')}, 
                'E':{'lumi':4008.663,           'runs':('276831', '277420')}, 
                'F':{'lumi':3101.618,           'runs':('277772', '278808')}, 
                'G':{'lumi':7529.196,           'runs':('278820', '280385')}, 
                'H':{'lumi':8390.540 + 215.149, 'runs':('280919', '284044')},
            },

            '23Sep2016':{
                'B':{'lumi': 5667.931,           'runs':('272007', '275376')},
                'C':{'lumi': 2638.567,           'runs':('275657', '276283')},
                'D':{'lumi': 4353.448,           'runs':('276315', '276811')},
                'E':{'lumi': 3204.684,           'runs':('276831', '277420')},
                'F':{'lumi': 3185.971,           'runs':('277772', '278808')},
                'G':{'lumi': 7721.057,           'runs':('278820', '280385')},
                'H':{'lumi': 8635.591 + 221.442, 'runs':('280919', '284044')},
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
    'BCDE' :{'bins':['B','C','D','E'],     'name_dict':{'shortName':'dBCDE',  'niceName':'', 'latexName':''}},
    'BCDEF':{'bins':['B','C','D','E','F'], 'name_dict':{'shortName':'dBCDEF', 'niceName':'', 'latexName':''}},
    'GH'   :{'bins':['G', 'H'],            'name_dict':{'shortName':'dGH',    'niceName':'', 'latexName':''}},
}

for dataEra in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
    dataEras[dataEra] = {'bins':[dataEra], 'name_dict':{'shortName':'d' + dataEra,    'niceName':'', 'latexName':''}}

def getDataLumi(lumi_dict, eras):
    lumi = sum([lumi_dict[era]['lumi'] for era in eras])
    return round(lumi,1)

lumis = {}
dataset_info = {}
names_dict = {}

for year in dataset_dict:
    lumis[year] = {}
    dataset_info[year] = {}
    for pd in dataset_dict[year]:
        dataset_info[year][pd] = {}
        for camp in dataset_dict[year][pd]:
            # total lumi
            dataset_name = '%s_Run%s_%s'%(pd, year, camp)
            lumi = getDataLumi(dataset_dict[year][pd][camp], allDataEras[year])

            lumis[year][dataset_name] = lumi

            dataset_info[year][pd].update({dataset_name:{'bins':allDataEras[year], 'name_dict':{'shortName':'d', 'niceName':'', 'latexName':''}, 'lumi':lumi}})

            # specific era bins       
            for dataEra in dataEras:
                dataset_name_final = '%s_Run%s%s_%s'%(pd, year, dataEra, camp)

                try: 
                    lumi = getDataLumi(dataset_dict[year][pd][camp], dataEras[dataEra]['bins'])
                except KeyError as err:
                    #print "KeyError:", err 
                    continue
                
                lumis[year][dataset_name_final] = lumi
                
                dataset_info[year][pd].update({dataset_name_final:{'bins':dataEras[dataEra]['bins'], 'name_dict':dataEras[dataEra]['name_dict'], 'lumi':lumi}})

        for name in dataset_info[year][pd]:
            sample_names[name] = {}
            #sample_names.update({name: dataset_info[year][pd][name]['name_dict']})
            lumiTag = makeLumiTag(dataset_info[year][pd][name]['lumi'], latex = True)
                    
            #if not sample_names[name]['latexName']:
            sample_names[name]['latexName'] = 'Data %s'%name 
            #if not sample_names[name]['niceName']:
            sample_names[name]['niceName'] = name
                    
            sample_names[name]['latexName'] += " (%s)"%lumiTag

# FIXME: re-calculate # NOTE: from latest PdmV table (https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVAnalysisSummaryTable)
lumis['2017']['MET_Run2017_14Dec2018'] = 41529.0
lumis['2018']['MET_Run2018_14Dec2018'] = 59740.0
lumis['2017']['SingleMuon_Run2017_14Dec2018'] = 41529.0
lumis['2018']['SingleMuon_Run2018_14Dec2018'] = 59740.0
lumis['2017']['DoubleMuon_Run2017_14Dec2018'] = 41529.0
lumis['2018']['DoubleMuon_Run2018_14Dec2018'] = 59740.0
lumis['2017']['EGamma_Run2017_14Dec2018'] = 41529.0
lumis['2018']['EGamma_Run2018_14Dec2018'] = 59740.0
lumis['2017']['Charmonium_Run2017_14Dec2018'] = 41529.0
lumis['2018']['Charmonium_Run2018_14Dec2018'] = 59740.0

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

triggers['SingleMuon'] = "HLT_IsoMu24" # "HLT_Mu50" = non-isolated trigger
    
triggers['DoubleMuon'] = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL", "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ", "HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL", "HLT_TkMu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ", "HLT_Mu30_TkMu11"]

triggers['EGamma'] = "HLT_Ele32_WPTight_Gsf"

triggers['Charmonium'] = "HLT_DoubleMu4_3_Jpsi"

triggers['SingleLepton'] = [triggers['SingleMuon'], triggers['EGamma']]

triggers['JetHT'] = [ # JetHT PD
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
