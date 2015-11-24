import copy, os, sys
dir  = '/data/easilar/cmgTuples/postProcessed_miniAODv2_fix/HT500LT250/hard/'

TTJets_HTLO_25ns={\
"name" : "tt+Jets_LO",
"bins" : [
"TTJets_LO",
"TTJets_LO_HT600to800",
"TTJets_LO_HT800to1200",
"TTJets_LO_HT1200to2500",
"TTJets_LO_HT2500toInf",
],
'dir' : dir,
}

TTJets_diLep = {\
"name" : "TTJets_diLep",
"bins" : [
"TTJets_DiLepton_full",
],
'dir' : dir,
}

TTJets_SemiLep = {\
"name" : "TTJets_SemiLep",
"bins" : [
"TTJets_SingleLeptonFromT_full",
"TTJets_SingleLeptonFromTbar_full",
],
'dir' : dir,
}

TTJets_combined = {\
"name" : "TTJets_combined",
"bins" : [
"TTJets_LO_HT1200to2500_Had_LHE",
"TTJets_LO_HT2500toInf_Had_LHE",
"TTJets_LO_HT600to800_Had_LHE",
"TTJets_LO_HT800to1200_Had_LHE",
"TTJets_LO_Had_LHE",
"TTJets_DiLepton_full",
"TTJets_SingleLeptonFromT_full",
"TTJets_SingleLeptonFromTbar_full",
],
'dir' : dir,
}
WJetsHTToLNu_25ns={\
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
'dir' : dir,
}


singleTop_25ns={\
"name" : "singleTop",
"bins" : [
"TBar_tWch",
"TToLeptons_sch",
"TToLeptons_tch_amcatnlo_full",
"T_tWch",
],
'dir' : dir,
}

DY_25ns={\
"name" : "DY",
"bins" : [
"DYJetsToLL_M50_HT100to200",
"DYJetsToLL_M50_HT200to400",
"DYJetsToLL_M50_HT400to600",
"DYJetsToLL_M50_HT600toInf",
],
'dir' : dir,
}


QCDHT_25ns = {
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
'dir' : dir,
}

TTV_25ns = {
"name":"TTVH_HT",
"bins":[
"TTWToLNu",
"TTWToQQ",
"TTZToLLNuNu",
"TTZToQQ",
],
'dir' : dir,
}



