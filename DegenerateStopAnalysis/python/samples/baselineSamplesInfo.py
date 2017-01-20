# baselineSamplesInfo.py
# Baseline Lumis, Triggers (Filters), Cuts and Weight Options

import Workspace.DegenerateStopAnalysis.tools.degCuts2 as degCuts

### Samples Names ###
sample_names = {
                    'vv':"VV",
                    'z':r'#Z\rightarrow \nu\nu+jets',
                    'st':'Single top',
                    'dy':r'#Z/\gamma^{*} +jets',
                }

### Luminosities ###
lumis = {
            'DataBlind_lumi':           36416.8,
            'SingleMuDataBlind_lumi':   36416.8,
            'SingleElDataBlind_lumi':   36416.8,
            'JetHTDataBlind_lumi':      36416.8,
            'DataICHEP_lumi':           12864.4,
            'DataUnblind_lumi':          4303.0,
            'SingleMuDataUnblind_lumi':  4303.0,
            'SingleElDataUnblind_lumi':  4303.0,
            'JetHTDataUnblind_lumi':     4303.0,
            'mc_lumi':                  10000.0,
        }
            
lumis['target_lumi'] = lumis['DataBlind_lumi']

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
cutWeightOptions['def_weights'] = ['weight', 'pu', 'DataBlind']
cutWeightOptions['settings'] = {
            'lepCol':          "LepGood",
            'lep':             "lep",
            'lepTag':          "def",
            'jetTag':          "def",
            'btagSF':          "SF",
            'DataBlind_lumi':    str(lumis['DataBlind_lumi']),
            'DataUnblind_lumi':  str(lumis['DataUnblind_lumi']),
            'mc_lumi':           str(lumis['mc_lumi']),
        }
