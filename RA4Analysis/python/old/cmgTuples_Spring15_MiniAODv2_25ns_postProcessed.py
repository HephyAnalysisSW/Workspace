import copy, os, sys
#dir = '/data/easilar/cmgTuples/postProcessing_MC_hadrFlav_btag_Eff/HT500LT250/'
dir = '/data/easilar/cmgTuples/postProcessing_MC/HT500LT250Skim/'
#dir = '/data/easilar/cmgTuples/postProcessed_Unblinding/hard/'
####usual HT combination####

TTJets_HTLO_25ns={\
"name" : "tt+Jets_LO",
"bins" : [
"TTJets_LO",
"TTJets_LO_HT600to800",
"TTJets_LO_HT800to1200",
"TTJets_LO_HT1200to2500",
"TTJets_LO_HT2500toInf",
],
'dir' : '/data/easilar/cmgTuples/postProcessed_miniAODv2_fix/HT500LT250/hard/',
}

#####(diLep+SemiLep+HT binned samples) for LHE_HT<=1000 & (HT binned samples) for LHE_HT>1000
TTJets_combined_25ns = {\
"name" : "TTJets_combined",
"bins" : [
"TTJets_DiLepton",
"TTJets_LO",
"TTJets_LO_HT1200to2500",
"TTJets_LO_HT2500toInf",
"TTJets_LO_HT600to800",
"TTJets_LO_HT800to1200",
#"TTJets_SingleLeptonFromT_full",
#"TTJets_SingleLeptonFromTbar_full",
'TTJets_SingleLepton'
],
'dir' : dir,
}


WJetsHTToLNu_25ns={\
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
'dir' : dir,
}

singleTop_25ns={\
"name" : "singleTop",
"bins" : [
"TBar_tWch",
"TToLeptons_sch",
"TToLeptons_tch_amcatnlo",
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
'dir' : dir,# '/data/dspitzbart/cmgTuples/postProcessing_Data_with_filters_already_vetoed/HT500LT250Skim/',
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

allSignalStrings=[\
"T5qqqqVV_mGluino_600To675_mLSP_1to550",\
"T5qqqqVV_mGluino_700To775_mLSP_1To650",\
"T5qqqqVV_mGluino_800To975_mLSP_1To850",\
"T5qqqqVV_mGluino_1000To1075_mLSP_1To950",\
"T5qqqqVV_mGluino_1100To1175_mLSP_1to1050",\
"T5qqqqVV_mGluino_1200To1275_mLSP_1to1150",\
"T5qqqqVV_mGluino_1300To1375_mLSP_1to1250",\
"T5qqqqVV_mGluino_1400To1550_mLSP_1To1275",\
"T5qqqqVV_mGluino_1600To1750_mLSP_1To950",\
]

from Workspace.HEPHYPythonTools.user import username
import pickle

pickleDir = '/data/easilar/Spring15/25ns/'
#signal_dir = '/data/easilar/cmgTuples/postProcessing_Signals/signal/'
signal_dir = '/data/easilar/cmgTuples/postProcessing_Signals_v4/signal/'

def getSignalSample(signal):
  if signal in allSignalStrings:
    sig = {}
    mass_dict = pickle.load(file(pickleDir+signal+'_mass_nEvents_xsec_pkl'))
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

