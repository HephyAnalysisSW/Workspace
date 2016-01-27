import copy, os, sys
dirData = '/data/easilar/cmgTuples/postProcessed_PUreweight/HT500ST250/hard/'

SingleElectron_Run2015D ={\
'name':'SingleElectron',
'bins': [
'SingleElectron_Run2015D_v4',
'SingleElectron_Run2015D_05Oct',
],
'dir': dirData,
}

SingleMuon_Run2015D ={\
'name':'SingleMuon',
'bins': [
'SingleMuon_Run2015D_05Oct',
'SingleMuon_Run2015D_v4',
],
'dir': dirData,
}

TTJets_HTLO_25ns={\
"name" : "tt+Jets_LO",
"bins" : [
#"TTJets_HT-0to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"TTJets_LO_25ns",
"TTJets_HT600to800",
"TTJets_HT800to1200",
"TTJets_HT1200to2500",
"TTJets_HT2500toInf",
],
'dir' : dirData,
}

WJetsHT_25ns={\
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
'dir' : dirData,
}


singleTop_25ns={\
"name" : "singleTop",
"bins" : [
"TBar_tWch",
"TToLeptons_sch",
"TToLeptons_tch",
"T_tWch",
],
'dir' : dirData,
}

DY_25ns={\
"name" : "DY",
"bins" : [
"DYJetsToLL_M50_HT100to200",
"DYJetsToLL_M50_HT200to400",
"DYJetsToLL_M50_HT400to600",
"DYJetsToLL_M50_HT600toInf",
],
'dir' : dirData,
}


QCDHT_25ns = {
"name":"QCD",
"bins":[
"QCD_HT1000to1500",
"QCD_HT1500to2000",
"QCD_HT2000toInf",
"QCD_HT200to300",
"QCD_HT300to500",
"QCD_HT500to700",
"QCD_HT700to1000",
],
'dir' : dirData,
}

TTV_25ns = {
"name":"TTVH_HT",
"bins":[
"TTWJetsToLNu_25ns",
"TTWJetsToQQ_25ns",
"TTZToLLNuNu_25ns",
"TTZToQQ_25ns",
],
'dir' : dirData,
}


