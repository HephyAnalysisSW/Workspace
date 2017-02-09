# baselineSamplesInfo.py
# Baseline Lumis, Triggers (Filters), Cuts and Weight Options

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
                    'vv': {'latexName': "VV",                          'niceName':'VV',         'shortName':'vv'},     
                    'z' : {'latexName':  r'#Z\rightarrow \nu\nu+jets', 'niceName':'ZInv',       'shortName':'z'},     
                    'st': {'latexName': 'Single top',                  'niceName':'Single top', 'shortName':'st'}, 
                    'dy': {'latexName': r'#Z/\gamma^{*} +jets',        'niceName':'DY',         'shortName':'dy'},
                    'w' : {'latexName': 'WJets',                       'niceName':'WJets',      'shortName':'w' },     
                    'tt': {'latexName': 'TTJets',                      'niceName':'TTJets',     'shortName':'tt'},     
                   'qcd': {'latexName': 'QCD',                         'niceName':'QCD',        'shortName':'qcd'},      
                 }

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
    return wantedName


### Luminosities ###

lumis = {
            'DataBlind_lumi':           36416.8,
            'SingleMuDataBlind_lumi':   36416.8,
            'SingleElDataBlind_lumi':   36416.8,
            'JetHTDataBlind_lumi':      36416.8,
            #'DataICHEP_lumi':           12864.4,
            'DataUnblind_lumi':         4303.0,
            'SingleMuDataUnblind_lumi': 4303.0,
            'SingleElDataUnblind_lumi': 4303.0,
            'JetHTDataUnblind_lumi':    4303.0,
            'MC_lumi':                  10000.0,
        }

lumis['target_lumi'] = lumis['DataBlind_lumi']

data_runs = {
                 'B': {'lumi': 5667.931, 'runs': ('272007', '275376')},
                 'C': {'lumi': 2638.567, 'runs': ('275657', '276283')},
                 'D': {'lumi': 4353.448, 'runs': ('276315', '276811')},
                 'E': {'lumi': 3204.684, 'runs': ('276831', '277420')},
                 'F': {'lumi': 3185.971, 'runs': ('277772', '278808')},
                 'G': {'lumi': 7721.057, 'runs': ('278820', '280385')},
                 'H': {'lumi': 8635.591 + 221.442, 'runs': ('280919', '284044')}
                }

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

for dataset_name , runs , name_dict, in data_sets_info:
    lumi = getDataRunsLumi(runs, data_runs)
    lumis[dataset_name+"_lumi"] = lumi
    latexBaseName = name_dict['latexName'] if name_dict['latexName'] else 'Data' 
    name_dict['latexName']=latexBaseName+"(%s)"%makeLumiTag(lumi,latex=False)
    sample_names_db[name_dict['shortName']] = name_dict
sample_names_db['d'] = {'latexName':'Data(%s)'%makeLumiTag( lumis['DataUnblind_lumi'],latex=False), 'shortName':'d', 'niceName':'DataUnblind' }

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
cutWeightOptions['options']     = ['isr', 'sf']
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
