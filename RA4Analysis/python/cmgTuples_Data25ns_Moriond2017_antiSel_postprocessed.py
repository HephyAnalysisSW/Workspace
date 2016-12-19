
import copy, os, sys

datadir = '/afs/hephy.at/data/dspitzbart01/cmgTuples/postProcessed_Run2016_antiSelection_isoTrack_v6/HT500/'

singleElectron_samples = [\
                        "SingleElectron_Run2016B_23Sep2016",\
                        "SingleElectron_Run2016C_23Sep2016_v1",\
                        "SingleElectron_Run2016D_23Sep2016_v1",\
                        "SingleElectron_Run2016E_23Sep2016_v1",\
                        "SingleElectron_Run2016F_23Sep2016_v1",\
                        "SingleElectron_Run2016G_23Sep2016_v1",\
                        "SingleElectron_Run2016H_PromptReco_v2",\
                        "SingleElectron_Run2016H_PromptReco_v3"\
                        ]

singleMuon_samples = [\
                        "SingleMuon_Run2016B_23Sep2016",\
                        "SingleMuon_Run2016C_23Sep2016_v1",\
                        "SingleMuon_Run2016D_23Sep2016_v1",\
                        "SingleMuon_Run2016E_23Sep2016_v1",\
                        "SingleMuon_Run2016F_23Sep2016_v1",\
                        "SingleMuon_Run2016G_23Sep2016_v1",\
                        "SingleMuon_Run2016H_PromptReco_v2",\
                        "SingleMuon_Run2016H_PromptReco_v3"\
                        ]
met_samples = [\
                        "MET_Run2016B_23Sep2016",\
                        "MET_Run2016C_23Sep2016_v1",\
                        "MET_Run2016D_23Sep2016_v1",\
                        "MET_Run2016E_23Sep2016_v1",\
                        "MET_Run2016F_23Sep2016_v1",\
                        "MET_Run2016G_23Sep2016_v1",\
                        "MET_Run2016H_PromptReco_v2",\
                        "MET_Run2016H_PromptReco_v3"\
                        ]

single_mu_antiSel = {\
"name" : "SingleMuon",
"bins" : singleMuon_samples ,
'dir' : datadir,
}

single_ele_antiSel = {\
"name" : "SingleElectron",
"bins" : singleElectron_samples ,
'dir' : datadir,
}

met_antiSel = {\
"name" : "MET",
"bins" : met_samples ,
'dir' : datadir,
}

