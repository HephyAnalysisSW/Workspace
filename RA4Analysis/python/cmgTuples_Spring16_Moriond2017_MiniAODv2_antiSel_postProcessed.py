import copy, os, sys
#dirDaniel = '/data/dspitzbart/cmgTuples/postProcessed_Spring16_antiSelection_3fb/none/'
#dirDaniel = '/data/dspitzbart/cmgTuples/postProcessing_Spring16_JECv6_antiSelection/none/'
dirDaniel = '/afs/hephy.at/data/dspitzbart02/cmgTuples/postProcessed_Moriond2017_antiSel_v2/HT500/'
#dirDaniel2 = '/data/dspitzbart/cmgTuples/postProcessed_Spring16_antiSelection_TTJetsComb/none/'


TTJets_Comb_antiSel = {\
"name" : "TTJets_singleLep",
"bins" : [
"TTJets_SingleLeptonFromT",
"TTJets_SingleLeptonFromTbar",
"TTJets_DiLepton",
"TTJets_LO_HT600to800",
"TTJets_LO_HT800to1200",
"TTJets_LO_HT1200to2500",
"TTJets_LO_HT2500toInf",
],
'dir' : dirDaniel,
}

WJetsHTToLNu_antiSel = {\
"name" : "W+Jets",
"bins" : [
"WJetsToLNu_HT400to600",
"WJetsToLNu_HT600to800",
"WJetsToLNu_HT800to1200",
"WJetsToLNu_HT1200to2500",
"WJetsToLNu_HT2500toInf",
],
'dir' : dirDaniel,
}

singleTop_lep_antiSel = {\
"name" : "singleTop_lep",
"bins" : [
"TToLeptons_sch",
"T_tWch",
"TBar_tWch",
"T_tch_powheg",
"TBar_tch_powheg",
],
'dir' : dirDaniel,
}

DY_HT_antiSel = {\
"name" : "DY_HT",
"bins" : [
"DYJetsToLL_M50_HT400to600",
"DYJetsToLL_M50_HT600to800",
"DYJetsToLL_M50_HT800to1200",
"DYJetsToLL_M50_HT1200to2500",
"DYJetsToLL_M50_HT2500toInf",
],
'dir' : dirDaniel,
}

QCDHT_antiSel = {\
"name":"QCD",
"bins":[
"QCD_HT1000to1500",
"QCD_HT1500to2000",
"QCD_HT2000toInf",
"QCD_HT300to500",
"QCD_HT500to700",
"QCD_HT700to1000",
],
'dir' : dirDaniel,
}

diBoson = {\
"name":"diBoson",
"bins":[
"WWTo2L2Nu",
"WWToLNuQQ",
"WZTo1L1Nu2Q",
"WZTo1L3Nu",
"WZTo2L2Q",
"ZZTo2L2Nu",
"ZZTo2L2Q",
],
'dir': dirDaniel,
}

TTV_antiSel = {
"name":"TTV",
"bins":[
"TTWToLNu",
"TTWToQQ",
"TTZToLLNuNu",
"TTZToQQ",
],
'dir' : dirDaniel,
}

