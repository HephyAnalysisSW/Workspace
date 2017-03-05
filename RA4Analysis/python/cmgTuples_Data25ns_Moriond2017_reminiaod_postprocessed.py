import copy, os, sys

#datadir = '/afs/hephy.at/data/easilar01/cmgTuples/postProcessing_Data_Moriond2017_v9_Trigskimmed/HT350/'
datadir = '/afs/hephy.at/data/easilar01/cmgTuples/postProcessing_Data_Moriond2017_reMiniaod/HT350/'

singleElectron_samples = [\
                        "SingleElectron_Run2016B",\
                        "SingleElectron_Run2016C",\
                        "SingleElectron_Run2016D",\
                        "SingleElectron_Run2016E",\
                        "SingleElectron_Run2016F",\
                        "SingleElectron_Run2016G",\
                        "SingleElectron_Run2016H_v2",\
                        "SingleElectron_Run2016H_v3"\
                        ]

singleMuon_samples = [\
                        "SingleMuon_Run2016B",\
                        "SingleMuon_Run2016C",\
                        "SingleMuon_Run2016D",\
                        "SingleMuon_Run2016E",\
                        "SingleMuon_Run2016F",\
                        "SingleMuon_Run2016G",\
                        "SingleMuon_Run2016H_v2",\
                        "SingleMuon_Run2016H_v3"\
                        ]
met_samples = [\
                        "MET_Run2016B",\
                        "MET_Run2016C",\
                        "MET_Run2016D",\
                        "MET_Run2016E",\
                        "MET_Run2016F",\
                        "MET_Run2016G",\
                        "MET_Run2016H_v2",\
                        "MET_Run2016H_v3"\
                        ]

single_mu = {\
"name" : "SingleMuon",
"bins" : singleMuon_samples ,
'dir' : datadir,
}

single_ele = {\
"name" : "SingleElectron",
"bins" : singleElectron_samples ,
'dir' : datadir,
}

met = {\
"name" : "MET",
"bins" : met_samples ,
'dir' : datadir,
}

single_mu_unblind = {\
"name" : "SingleMuon_unblind",
"bins" : ["SingleMuon_Run2016G_23Sep2016_v1"],
'dir' : datadir,
}

single_ele_unblind = {\
"name" : "SingleElectron_unblind",
"bins" : ["SingleElectron_Run2016G_23Sep2016_v1"],
'dir' : datadir,
}

met_unblind = {\
"name" : "MET_unblind",
"bins" : ["MET_Run2016G_23Sep2016_v1"] ,
'dir' : datadir,
}

