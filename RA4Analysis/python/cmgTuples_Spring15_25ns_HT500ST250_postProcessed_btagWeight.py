import copy, os, sys
dirDaniel = '/data/dspitzbart/cmgTuples/postProcessed_Spring15_CB/HT400ST200/hard/'
dirNew = '/data/dspitzbart/cmgTuples/postProcessed_PUreweight/HT500ST250/hard/'

TTJets_LO_25ns_btagweight={\
"name" : "tt+Jets_LO",
"bins" : [
"TTJets_LO_25ns",
"TTJets_HT600to800",
"TTJets_HT800to1200",
"TTJets_HT1200to2500",
"TTJets_HT2500toInf",
],
'dir' : dirNew,
}

WJetsHT_25ns_btagweight={\
"name" : "W+Jets",
"bins" : [
"WJetsToLNu_HT100to200",
"WJetsToLNu_HT200to400",
"WJetsToLNu_HT400to600",
#"WJetsToLNu_HT600toInf",
"WJetsToLNu_HT600to800",
"WJetsToLNu_HT800to1200",
"WJetsToLNu_HT1200to2500",
"WJetsToLNu_HT2500toInf",
],
'dir' : dirNew,
}

