import copy, os, sys
#dirDaniel = '/data/dspitzbart/cmgTuples/postProcessed_Spring16_antiSelection_3fb/none/'
#dirDaniel = '/data/dspitzbart/cmgTuples/postProcessing_Spring16_JECv6_antiSelection/none/'
dirDaniel = '/afs/hephy.at/data/dspitzbart01/cmgTuples/postProcessed_Spring16_antiSelection_isoTrack_v2/HT500/'
#dirDaniel2 = '/data/dspitzbart/cmgTuples/postProcessed_Spring16_antiSelection_TTJetsComb/none/'


TTJets_Comb_antiSel = {\
"name" : "TTJets_singleLep",
"bins" : [
"TTJets_SingleLeptonFromT_full",
"TTJets_SingleLeptonFromTbar_full",
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
"WJetsToLNu_HT200to400",
"WJetsToLNu_HT400to600",
"WJetsToLNu_HT600to800",
"WJetsToLNu_HT800to1200",
"WJetsToLNu_HT1200to2500",
"WJetsToLNu_HT2500toInf",
],
'dir' : dirDaniel,
}

#singleTop_inclusive = {\
#"name" : "singleTop_inclusive",
#"bins" : [
#"ST_tchannel_antitop_4f_inclusiveDecays_powheg",
#"ST_tW_antitop_5f_inclusiveDecays_powheg",
#],
#'dir' : dirDaniel,
#}

singleTop_lep_antiSel = {\
"name" : "singleTop_lep",
"bins" : [
"ST_schannel_4f_leptonDecays",
"ST_tchannel_antitop_4f_leptonDecays_powheg",
"ST_tchannel_top_4f_leptonDecays_powheg",#fake sample
"ST_tW_antitop_5f_inclusiveDecays_powheg",
"ST_tW_top_5f_inclusiveDecays_powheg",
],
'dir' : dirDaniel,
}

DY_HT_antiSel = {\
"name" : "DY_HT",
"bins" : [
"DYJetsToLL_M_50_HT_100to200",
"DYJetsToLL_M_50_HT_200to400",
"DYJetsToLL_M_50_HT_400to600",
"DYJetsToLL_M_50_HT_600toInf",
],
'dir' : dirDaniel,
}

QCDHT_antiSel = {\
"name":"QCD",
"bins":[
"QCD_HT1000to1500",
"QCD_HT1500to2000",
"QCD_HT2000toInf",
#"QCD_HT200to300",
"QCD_HT300to500",
"QCD_HT500to700",
"QCD_HT700to1000",
],
'dir' : dirDaniel,
}

QCDHT_antiSel_test = {\
"name":"QCD",
"bins":[
"QCD_HT300to500",
],
'dir' : dirDaniel,
}


#diBoson = {\
#"name":"diBoson",
#"bins":[
#"DiBoson_WW",
#"DiBoson_WZ",
#"DiBoson_ZZ",
#],
#'dir': dirDaniel,
#}

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

