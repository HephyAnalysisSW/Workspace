import copy, os, sys
#dir = '/data/dhandl/cmgTuples/postProcessed_Spring15_antiSelection_final2p1fb_V6/none/'
dir2 = '/data/dspitzbart/cmgTuples/postProcessed_Spring15_antiSelection_final2p25fb_v2/'
dir = dir2+'none/'

single_mu_Run2015D = {\
"name" : "single_mu_Run215D",
"bins" : [
"SingleMuon_Run2015D_05Oct",
"SingleMuon_Run2015D_v4",
],
'dir' : dir,
}


single_ele_Run2015D = {\
"name" : "single_ele_Run215D",
"bins" : [
"SingleElectron_Run2015D_05Oct",
"SingleElectron_Run2015D_v4",
],
'dir' : dir,
}

####usual HT combination####
TTJets_HTLO_25ns={\
"name" : "tt+Jets_LO",
"bins" : [
"LHE_FullHadronic_inc/none/TTJets_LO",
"LHE_FullHadronic/none/TTJets_LO_HT600to800",
"LHE_FullHadronic/none/TTJets_LO_HT800to1200",
"LHE_FullHadronic/none/TTJets_LO_HT1200to2500",
"LHE_FullHadronic/none/TTJets_LO_HT2500toInf",
],
'dir' : dir,
}
#####diLep+SemiLep+HT binned samples####
TTJets_combined = {\
"name" : "TTJets_combined",
"bins" : [
"TTJets_DiLepton_full",
"TTJets_LO",
"TTJets_LO_HT1200to2500",
"TTJets_LO_HT2500toInf",
"TTJets_LO_HT600to800",
"TTJets_LO_HT800to1200",
"TTJets_SingleLeptonFromT_full",
"TTJets_SingleLeptonFromTbar_full",
],
'dir' : dir,
}
#####(diLep+SemiLep+HT binned samples) for LHE_HT<=1000 & (HT binned samples) for LHE_HT>1000 
TTJets_combined_2 = {\
"name" : "TTJets_combined",
"bins" : [
"diLep/none/TTJets_DiLepton_full",
"LHE_FullHadronic_inc/none/TTJets_LO",
"LHE_FullHadronic/none/TTJets_LO_HT1200to2500",
"LHE_FullHadronic/none/TTJets_LO_HT2500toInf",
"LHE_FullHadronic/none/TTJets_LO_HT600to800",
"LHE_FullHadronic/none/TTJets_LO_HT800to1200",
"semiLep/none/TTJets_SingleLeptonFromT_full",
#"semiLep/none/TTJets_SingleLeptonFromTbar_full",
],
'dir' : dir2,#'/data/dhandl/cmgTuples/postProcessed_Spring15_antiSelection_final2p1fb_V6/',
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



