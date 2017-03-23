# baselineSamplesInfo.py
# Baseline Lumis, Triggers (Filters), Cuts and Weight Options
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
### Samples Names ###
sample_names = {
                    'vv': "VV",
                    'z':  r'#Z\rightarrow \nu\nu+jets',
                    'st': 'Single top',
                    'dy': r'#Z/\gamma^{*} +jets',
                    'w' :  'WJets',
                    'tt': 'TTJets',
                }

sample_names_db = {
                'Total'  : {'latexName': "Total",                       'niceName':'Total',     },#'shortName':'vv'     },     
                'others' : {'latexName': "Others",                      'niceName':'Others',     },#'shortName':'vv'     },     
                    'vv' : {'latexName': "VV",                          'niceName':'VV',         },#'shortName':'vv'     },     
                    'z'  : {'latexName':  r'#Z\rightarrow \nu\nu+jets', 'niceName':'ZInv',       },#'shortName':'z'      },     
                    'st' : {'latexName': 'Single top',                  'niceName':'Single top', },#'shortName':'st'     }, 
                    'dy' : {'latexName': r'#Z/\gamma^{*} +jets',        'niceName':'DY',         },#'shortName':'dy'     },
                    'w'  : {'latexName': 'WJets',                       'niceName':'WJets',      },#'shortName':'w'      },     
                    'tt' : {'latexName': 'TTJets',                      'niceName':'TTJets',     },#'shortName':'tt'     },                        'tt_1l': {'latexName': 'TT_1l',                      'niceName':'TT_1l',    },# 'shortName':'tt_1l'    },     
                 'tt_1l' : {'latexName': 'TT_1l',                       'niceName':'TT_1l',      },# 'shortName':'tt_1l'    },     
                 'tt_2l' : {'latexName': 'TT_2l',                       'niceName':'TT_2l',      },# 'shortName':'tt_2l'    },     
                'tt_pow' : {'latexName': 'TT_Pow',                      'niceName':'TT_Pow',     },#    'shortName':'tt_pow' },     
                   'qcd' : {'latexName': 'QCD',                         'niceName':'QCD',        },#'shortName':'qcd'    },      
                  't2tt' : {'latexName': 'T2tt',                        'niceName':'T2tt',       },#'shortName':'qcd'    },      
                  't2bw' : {'latexName': 'T2bW',                        'niceName':'T2bW',       },#'shortName':'qcd'    },      
                 }








for short_name, sample_name_db in sample_names_db.items():
    sample_name_db['shortName'] = short_name

data_sets_info = [\
           ['DataBlind',  ['B','C','D','E','F','G','H'], {'latexName':'',   'shortName':'dblind',   'niceName':'DataBlind'} ],
           ['DataICHEP',  ['B','C','D']                , {'latexName':'',   'shortName':'dichep',   'niceName':'DataICHEP'} ],
           ['DataBCDE',   ['B','C','D','E']            , {'latexName':'',   'shortName':'dbcde',    'niceName':'DataBCDE' } ],
           ['DataBCDEF',  ['B','C','D','E','F']        , {'latexName':'',   'shortName':'dbcdef',   'niceName':'DataBCDEF'} ],
           ['DataGH',     ['G', 'H']                   , {'latexName':'',   'shortName':'dgh',      'niceName':'DataGH'   } ],
         ]

def sampleName( name, name_opt="niceName"):
    """
    name_opt should be one of ['niceName', 'latexName', 'shortName']
    """ 
    isSignal = degTools.getMasses( name, returnModel = True ) 
    if isSignal:
        model, m1, m2 = isSignal
        name = model

    possibleNames = {}
    for n , ndict in sample_names_db.iteritems():
        possibleNames[n] = ndict.values()
    foundIt = False 
    print possibleNames
    for n, pNames in possibleNames.iteritems():
        if name in pNames:
            if foundIt:
                raise Exception("found multiple matches to the name %s"%name)
            foundIt = n
    if not foundIt:
        raise Exception("Did not found a sample corresponding to: %s"%name)
    wantedName = sample_names_db[foundIt][name_opt]
    if isSignal:
        wantedName = "%s%s_%s"%( wantedName, m1, m2 )

    return wantedName


### Luminosities ###
# bril calc res : /afs/cern.ch/user/n/nrad/public/bril_res/8025_mAODv2_v7/lumis.pkl

lumis = {
            'DataBlind_lumi':           35854.9 , #8020_v5: 35628.7, # NOTE: calculated with getDataRunsLumi
            'SingleMuDataBlind_lumi':   35808.6 , #8020_v5: 36809.6 
            'SingleElDataBlind_lumi':   35725.18, #8020_v5: 36726.8
            'SingleLepDataBlind_lumi':  36800.0,
            'JetHTDataBlind_lumi':      33781.6, #NOTE: 8020_v5
            #'DataICHEP_lumi':           12864.4,
            'DataUnblind_lumi':         4303.0,
            'SingleMuDataUnblind_lumi': 4303.0,
            'SingleElDataUnblind_lumi': 4303.0,
            'JetHTDataUnblind_lumi':    4303.0,
            'MC_lumi':                  10000.0, #NOTE: Should be taken directly from samples
        }

lumis['target_lumi'] = lumis['DataBlind_lumi']

data_runs_sep23 = {
                 'B': {'lumi': 5667.931          , 'runs': ('272007', '275376')},
                 'C': {'lumi': 2638.567          , 'runs': ('275657', '276283')},
                 'D': {'lumi': 4353.448          , 'runs': ('276315', '276811')},
                 'E': {'lumi': 3204.684          , 'runs': ('276831', '277420')},
                 'F': {'lumi': 3185.971          , 'runs': ('277772', '278808')},
                 'G': {'lumi': 7721.057          , 'runs': ('278820', '280385')},
                 'H': {'lumi': 8635.591 + 221.442, 'runs': ('280919', '284044')}
                }

data_met_feb03 = {
                 'B' : { 'lumi': 5787.968           , 'runs': ('272007', '275376')  }, 
                 'C' : { 'lumi': 2573.399           , 'runs': ('275657', '276283')  }, 
                 'D' : { 'lumi': 4248.384           , 'runs': ('276315', '276811')  }, 
                 'E' : { 'lumi': 4008.663           , 'runs': ('276831', '277420')  }, 
                 'F' : { 'lumi': 3101.618           , 'runs': ('277772', '278808')  }, 
                 'G' : { 'lumi': 7529.196           , 'runs': ('278820', '280385')  }, 
                 'H' : { 'lumi': 8390.540 + 215.149 , 'runs': ('280919', '284044')  }, 
                  }

data_runs = data_met_feb03

#data_runs = {
#                 'B': {'lumi': 5891.727, 'runs': ('272007', '275376')},
#                 'C': {'lumi': 2645.968, 'runs': ('275657', '276283')},
#                 'D': {'lumi': 4353.448, 'runs': ('276315', '276811')},
#                 'E': {'lumi': 4049.255, 'runs': ('276831', '277420')},
#                 'F': {'lumi': 3160.088, 'runs': ('277772', '278808')},
#                 'G': {'lumi': 7554.453, 'runs': ('278820', '280385')},
#                 'H': {'lumi': 8761.821, 'runs': ('280919', '284044')}
#                }

def getDataRunsLumi( runs, data_runs = data_runs) :
    lumi = sum([data_runs[x]['lumi'] for x in runs] )
    return round(lumi,1)

def getDataRunCut( runs, data_runs=data_runs):
    run_cut_list = []
    for run in runs:
        run_cut_list.append(run_cut)
    run_cuts = " || ".join(run_cut_list)
    return "(%s)"%run_cuts

make_lumi_tag = lambda l: "%0.0fpbm1"%(l)

def makeLumiTag(lumi , latex=False ):
    """ lumi given in pb """
    if latex:
        tag = "%0.1ffb^{-1}"%(lumi/1000.)
    else:
        tag = "%0.1ffbm1"%(lumi/1000.)
    return tag

for dataset_name, runs , name_dict, in data_sets_info:
    lumi = getDataRunsLumi(runs, data_runs)
    lumis[dataset_name+"_lumi"] = lumi
    latexBaseName = name_dict['latexName'] if name_dict['latexName'] else 'Data' 
    name_dict['latexName']=latexBaseName+"(%s)"%makeLumiTag(lumi,latex=True)
    sample_names_db[name_dict['shortName']] = name_dict
sample_names_db['d'] = {'latexName':'Data(%s)'%makeLumiTag( lumis['DataUnblind_lumi'],latex=False), 'shortName':'d', 'niceName':'DataUnblind' }

# Setting target lumi to data lumi
lumis['target_lumi'] = lumis['DataBlind_lumi']

### Baseline Filters ###

filters = "Flag_Filters" #NOTE: Combination of filters as defined in post-processing

### Baseline Triggers ###
triggers = {}

triggers['data_met'] = [ # MET PD
                      'HLT_PFMET100_PFMHT100_IDTight',
                      'HLT_PFMET110_PFMHT110_IDTight',
                      'HLT_PFMET120_PFMHT120_IDTight',
                      'HLT_PFMET90_PFMHT90_IDTight'
                       ]

triggers['data_mu'] = "HLT_IsoMu24" # SingleMu PD
triggers['data_el'] = "HLT_Ele27_WPTight_Gsf" # SingleEl PD

triggers['data_lep'] = [triggers['data_mu'], triggers['data_el']]

triggers['data_jet'] = [ # JetHT PD
                      "HLT_PFHT800", 
                      "HLT_PFJet450", 
                      "HLT_AK8PFJet450"
                       ]

for trig in triggers:
   if type(triggers[trig]) == type([]):
      triggers[trig] = '(' + ' || '.join(triggers[trig]) + ')' #NOTE: assuming we always want to use an 'OR' of triggers

### Cuts and Weights Options ###
cutWeightOptions = {}
cutWeightOptions['options']     = ['isr', 'sf', ]
cutWeightOptions['def_weights'] = ['weight', 'pu', 'DataBlind_lumi']
cutWeightOptions['settings'] = {
            'lepCol': "LepGood",
            'lep':    "lep",
            'lepTag': "def",
            'jetTag': "def",
            'btagSF': "SF",
            'mvaId':  None,
            'bdtcut': None,
            'lumis' : lumis,
        }
