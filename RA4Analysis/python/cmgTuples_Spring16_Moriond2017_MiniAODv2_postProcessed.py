import copy, os, sys

dirEce = '/afs/hephy.at/data/easilar01/cmgTuples/postProcessing_MC_Moriond2017_v2/HT350/'


TTJets_diLep = {\
"name" : "TTJets_diLep",
"bins" : [
"TTJets_DiLepton",
],
'dir' : dirEce,
}

TTJets_semiLep = {\
"name" : "TTJets_semiLep",
"bins" : [
"TTJets_SingleLeptonFromT",
"TTJets_SingleLeptonFromTbar",
],
'dir' : dirEce,
}

TTJets_HTbinned = {\
"name" : "TTJets_HTbinned",
"bins" : [
'TTJets_LO_HT1200to2500_ext',
'TTJets_LO_HT2500toInf',
'TTJets_LO_HT600to800_ext',
'TTJets_LO_HT800to1200_ext',
],
'dir' : dirEce,
}


TTJets_Comb = {\
"name" : "TTJets_Comb",
"bins" : [
"TTJets_SingleLeptonFromT",
"TTJets_SingleLeptonFromTbar",
"TTJets_DiLepton",
#'TTJets_LO_HT1200to2500_ext',
#'TTJets_LO_HT2500toInf',
#'TTJets_LO_HT600to800_ext',
#'TTJets_LO_HT800to1200_ext',
],
'dir' : dirEce,
}


WJetsHTToLNu = {\
"name" : "W+Jets",
"bins" : [
  'WJetsToLNu_HT100to200',\
  #'WJetsToLNu_HT100to200_ext',\
  'WJetsToLNu_HT1200to2500',\
  #'WJetsToLNu_HT1200to2500_ext',\
  'WJetsToLNu_HT200to400',\
  #'WJetsToLNu_HT200to400_ext',\
  'WJetsToLNu_HT2500toInf',\
  #'WJetsToLNu_HT2500toInf_ext',\
  'WJetsToLNu_HT400to600',\
  #'WJetsToLNu_HT400to600_ext',\
  'WJetsToLNu_HT600to800',\
  'WJetsToLNu_HT800to1200',\
  #'WJetsToLNu_HT800to1200_ext',\
],
'dir' : dirEce,
}


singleTop_lep = {\
"name" : "singleTop_lep",
"bins" : [
  'ST_s_channel_4f_leptonDecays',\
  'ST_tW_antitop_5f_NoFullyHadronicDecays',\
  'ST_tW_top_5f_NoFullyHadronicDecays',\
  'ST_t_channel_antitop_4f_leptonDecays',\
  'ST_t_channel_top_4f_leptonDecays',\
],
'dir' : dirEce,
}


DY_HT = {\
"name" : "DY_HT",
"bins" : [
  'DYJetsToLL_M50_HT100to200',\
  #'DYJetsToLL_M50_HT100to200_ext',\
  'DYJetsToLL_M50_HT200to400',\
  #'DYJetsToLL_M50_HT200to400_ext',\
  'DYJetsToLL_M50_HT400to600',\
  #'DYJetsToLL_M50_HT400to600_ext',\
  'DYJetsToLL_M50_HT600toInf',\
  #'DYJetsToLL_M50_HT600toInf_ext',\
],
'dir' : dirEce,
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
'dir' : dirEce,
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
#"ZZTo2L2Q",
"ZZTo2Q2Nu",
],
'dir': dirEce,
}


TTV = {
"name":"TTV",
"bins":[
"TTWToLNu",
"TTWToQQ",
"TTZToLLNuNu",
"TTZToQQ",
],
'dir' : dirEce,
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
#signal_dir = '/afs/hephy.at/data/easilar01/cmgTuples/postProcessing_Signals_batch_no_Cut/signal/'
signal_dir = '/afs/hephy.at/data/easilar01/cmgTuples/postProcessing_Signals_Spring16_Moriond2017/signal/'

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

