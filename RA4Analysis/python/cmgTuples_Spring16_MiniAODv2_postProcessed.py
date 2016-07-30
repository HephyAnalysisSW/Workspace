import copy, os, sys
#dirEce = '/data/easilar/cmgTuples/postProcessing_Spring16_V6/HT500LT250Skim/'
#dirEce2 = '/data/easilar/cmgTuples/postProcessing_Spring16_FIXED_v2/'
dirDaniel = '/afs/hephy.at/data/dspitzbart01/cmgTuples/postProcessing_Spring16_JECv6_v1/HT500LT250Skim/'
#dirDaniel = '/data/dspitzbart/cmgTuples/postProcessing_Spring16_JECv6/HT500LT250Skim/'
dirEce = '/data/easilar/cmgTuples/postProcessing_Spring16_JECv6/HT500LT250Skim/'

####usual HT combination####

#TTJets_HTLO_25ns={\
#"name" : "tt+Jets_LO",
#"bins" : [
#"TTJets_LO",
#"TTJets_LO_HT600to800",
#"TTJets_LO_HT800to1200",
#"TTJets_LO_HT1200to2500",
#"TTJets_LO_HT2500toInf",
#],
#'dir' : '/data/easilar/cmgTuples/postProcessed_miniAODv2_fix/HT500LT250/hard/',
#}
#
######(diLep+SemiLep+HT binned samples) for LHE_HT<=1000 & (HT binned samples) for LHE_HT>1000
TTJets_combined = {\
"name" : "TTJets_combined",
"bins" : [
"TTJets_DiLepton",
"TTJets_LO",
"TTJets_LO_HT1200to2500",
"TTJets_LO_HT2500toInf",
"TTJets_LO_HT600to800",
"TTJets_LO_HT800to1200",
"TTJets_SingleLeptonFromT_full",
"TTJets_SingleLeptonFromTbar_full",
#'TTJets_SingleLepton'
],
'dir' : "/data/easilar/cmgTuples/postProcessing_Spring16_JECv3//HT500LT250Skim/",
}

TTJets_singleLep = {\
"name" : "TTJets_singleLep",
"bins" : [
"TTJets_SingleLeptonFromT_full",
"TTJets_SingleLeptonFromTbar_full",
],
'dir' : dirDaniel,
}

TTJets_diLep = {\
"name" : "TTJets_singleLep",
"bins" : [
"TTJets_DiLepton",
],
'dir' : dirDaniel,
}

TTJets_Lep = {\
"name" : "TTJets_Lep",
"bins" : [
"TTJets_SingleLeptonFromT_full",
"TTJets_SingleLeptonFromTbar_full",
"TTJets_DiLepton",
],
'dir' : dirDaniel,
}

TTJets_Comb = {\
"name" : "TTJets_Comb",
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


WJetsHTToLNu = {\
"name" : "W+Jets",
"bins" : [
#"WJetsToLNu_HT100to200",
"WJetsToLNu_HT200to400",
"WJetsToLNu_HT400to600",
#"WJetsToLNu_HT600toInf",
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

singleTop_lep = {\
"name" : "singleTop_lep",
"bins" : [
"ST_schannel_4f_leptonDecays",
"ST_tchannel_antitop_4f_leptonDecays_powheg",
"ST_tchannel_top_4f_leptonDecays_powheg",   ##This is a fake sample with inversed leptonPdg, fix asap!!!
"ST_tW_antitop_5f_inclusiveDecays_powheg",
"ST_tW_top_5f_inclusiveDecays_powheg",
],
'dir' : dirDaniel,
}


DY_HT = {\
"name" : "DY_HT",
"bins" : [
"DYJetsToLL_M_50_HT_100to200",
"DYJetsToLL_M_50_HT_200to400",
"DYJetsToLL_M_50_HT_400to600",
"DYJetsToLL_M_50_HT_600toInf",
],
'dir' : dirDaniel,
}


QCDHT = {\
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

diBoson = {\
"name":"diBoson",
"bins":[
"DiBoson_WW",
"DiBoson_WZ",
"DiBoson_ZZ",
],
'dir': dirDaniel,
}

TTV = {
"name":"TTV",
"bins":[
"TTWToLNu",
"TTWToQQ",
"TTZToLLNuNu",
"TTZToQQ",
],
'dir' : dirDaniel,
}

allSignalStrings=[\
#"T5qqqqVV_mGluino_600To675_mLSP_1to550",\
#"T5qqqqVV_mGluino_700To775_mLSP_1To650",\
#"T5qqqqVV_mGluino_800To975_mLSP_1To850",\
#"T5qqqqVV_mGluino_1000To1075_mLSP_1To950",\
#"T5qqqqVV_mGluino_1100To1175_mLSP_1to1050",\
#"T5qqqqVV_mGluino_1200To1275_mLSP_1to1150",\
#"T5qqqqVV_mGluino_1300To1375_mLSP_1to1250",\
#"T5qqqqVV_mGluino_1400To1550_mLSP_1To1275",\
#"T5qqqqVV_mGluino_1600To1750_mLSP_1To950",\
"SMS_T5qqqqVV_TuneCUETP8M1",\
]

from Workspace.HEPHYPythonTools.user import username
import pickle

#pickleDir = '/data/easilar/Spring15/25ns/'
pickleDir = '/afs/hephy.at/data/easilar01/Ra40b/pickleDir/T5qqqqWW_mass_nEvents_xsec_pkl'
#signal_dir = '/data/easilar/cmgTuples/postProcessing_Signals/signal/'
#signal_dir = '/data/easilar/cmgTuples/postProcessing_Signals_v4/signal/'
#signal_dir = '/data/easilar/cmgTuples/postProcessing_Signals_v4/signal/'
signal_dir = '/afs/hephy.at/data/easilar01/cmgTuples/postProcessing_Signals_batch_no_Cut/signal/'

def getSignalSample(signal):
  if signal in allSignalStrings:
    sig = {}
    mass_dict = pickle.load(file(pickleDir))
    for mglu in mass_dict.keys() :
      sig[mglu] = {}
      for mlsp in mass_dict[mglu].keys() :
        sig[mglu][mlsp] = mass_dict[mglu][mlsp]
        sig[mglu][mlsp]['file']="/".join([signal_dir,signal,str(mglu)+"_"+str(mlsp),"*.root"])
        sig[mglu][mlsp]['name'] ="_".join([signal,str(mglu),str(mlsp)])
    return sig
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

allSignals=[]
for s in allSignalStrings:
  sm = getSignalSample(s)
  exec(s+"=sm")
  allSignals.append(sm)

