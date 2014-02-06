import copy, os, sys
allSamples = []

path = os.path.abspath('../../HEPHYCommonTools/python')
if not path in sys.path:
    sys.path.insert(1, path)
del path
from createPUReweightingHisto import getPUReweightingUncertainty

S10rwHisto = getPUReweightingUncertainty("S10", dataFile = "/data/schoef/results2012/PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_Sys0.root")
S10rwPlusHisto = getPUReweightingUncertainty("S10", dataFile = "/data/schoef/results2012/PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_SysPlus5.root")
S10rwMinusHisto = getPUReweightingUncertainty("S10", dataFile = "/data/schoef/results2012/PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_SysMinus5.root")

dataZmumu={}
dataZmumu["name"]     = "dataZmumu";
dataZmumu["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/MET_050214/" 
dataZmumu["bins"]    = ["DoubleMuon-Run2012A-22Jan2013", "DoubleMuon-Run2012B-22Jan2013", "DoubleMuon-Run2012C-22Jan2013", "DoubleMuon-Run2012D-22Jan2013"]
dataZmumu["Chain"] = "Events"
dataZmumu["Counter"] = "bool_EventCounter_passed_PAT.obj"
allSamples.append(dataZmumu)
dataZee={}
dataZee["name"]     = "dataZee";
dataZee["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/MET_050214/" 
dataZee["bins"]    = ["DoubleElectron-Run2012A-22Jan2013", "DoubleElectron-Run2012B-22Jan2013", "DoubleElectron-Run2012C-22Jan2013", "DoubleElectron-Run2012D-22Jan2013"]
dataZee["Chain"] = "Events"
dataZee["Counter"] = "bool_EventCounter_passed_PAT.obj"
allSamples.append(dataZee)


mc={}
mc["name"]     = "mc";
mc["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/MET_050214/"
mc["Chain"] = "Events"

ttbar_ee = copy.deepcopy(mc)
ttbar_ee['reweightingHistoFile'] = S10rwHisto 
ttbar_ee['reweightingHistoFileSysPlus'] = S10rwPlusHisto
ttbar_ee['reweightingHistoFileSysMinus'] = S10rwMinusHisto
ttbar_ee["bins"] = ["Ele-TTJets"]
ttbar_ee["name"] = "TTJets" 
ttbar_mumu = copy.deepcopy(mc)
ttbar_mumu['reweightingHistoFile'] = S10rwHisto 
ttbar_mumu['reweightingHistoFileSysPlus'] = S10rwPlusHisto
ttbar_mumu['reweightingHistoFileSysMinus'] = S10rwMinusHisto
ttbar_mumu["bins"] = ["Mu-TTJets"]
ttbar_mumu["name"] = "TTJets" 

wjets_ee = copy.deepcopy(mc)
wjets_ee["bins"] = ["Ele-WJetsToLNu-v2"] 
wjets_ee["name"] = "WJetsToLNu" 
wjets_ee['reweightingHistoFile'] = S10rwHisto
wjets_ee['reweightingHistoFileSysPlus'] = S10rwPlusHisto
wjets_ee['reweightingHistoFileSysMinus'] = S10rwMinusHisto
wjets_mumu = copy.deepcopy(mc)
wjets_mumu["bins"] = ["Mu-WJetsToLNu-v2"] 
wjets_mumu["name"] = "WJetsToLNu" 
wjets_mumu['reweightingHistoFile'] = S10rwHisto
wjets_mumu['reweightingHistoFileSysPlus'] = S10rwPlusHisto
wjets_mumu['reweightingHistoFileSysMinus'] = S10rwMinusHisto

drellYan_ee = copy.deepcopy(mc)
drellYan_ee["bins"] = ["Ele-DYJetsToLL-M50", "Ele-DYJetsToLL-M10to50"] 
drellYan_ee["name"] = "DY"
drellYan_ee['reweightingHistoFile'] = S10rwHisto
drellYan_ee['reweightingHistoFileSysPlus'] = S10rwPlusHisto
drellYan_ee['reweightingHistoFileSysMinus'] = S10rwMinusHisto
drellYan_mumu = copy.deepcopy(mc)
drellYan_mumu["bins"] = ["Mu-DYJetsToLL-M50", "Mu-DYJetsToLL-M10to50"] 
drellYan_mumu["name"] = "DY"
drellYan_mumu['reweightingHistoFile'] = S10rwHisto
drellYan_mumu['reweightingHistoFileSysPlus'] = S10rwPlusHisto
drellYan_mumu['reweightingHistoFileSysMinus'] = S10rwMinusHisto

singleTop_ee = copy.deepcopy(mc)
singleTop_ee["bins"] = ["Ele-T-t", "Ele-T-s", "Ele-T-tW", "Ele-Tbar-t", "Ele-Tbar-s", "Ele-Tbar-tW"] 
singleTop_ee["name"] = "singleTop"
singleTop_ee['reweightingHistoFile'] = S10rwHisto
singleTop_ee['reweightingHistoFileSysPlus'] = S10rwPlusHisto
singleTop_ee['reweightingHistoFileSysMinus'] = S10rwMinusHisto
singleTop_mumu = copy.deepcopy(mc)
singleTop_mumu["bins"] = ["Mu-T-t", "Mu-T-s", "Mu-T-tW", "Mu-Tbar-t", "Mu-Tbar-s", "Mu-Tbar-tW"] 
singleTop_mumu["name"] = "singleTop"
singleTop_mumu['reweightingHistoFile'] = S10rwHisto
singleTop_mumu['reweightingHistoFileSysPlus'] = S10rwPlusHisto
singleTop_mumu['reweightingHistoFileSysMinus'] = S10rwMinusHisto

diboson_ee = copy.deepcopy(mc)
diboson_ee["bins"] = ["Ele-WW", "Ele-WZ", "Ele-ZZ"]
diboson_ee["name"] = "diboson"
diboson_ee['reweightingHistoFile'] = S10rwHisto
diboson_ee['reweightingHistoFileSysPlus'] = S10rwPlusHisto
diboson_ee['reweightingHistoFileSysMinus'] = S10rwMinusHisto
diboson_mumu = copy.deepcopy(mc)
diboson_mumu["bins"] = ["Mu-WW", "Mu-WZ", "Mu-ZZ"]
diboson_mumu["name"] = "diboson"
diboson_mumu['reweightingHistoFile'] = S10rwHisto
diboson_mumu['reweightingHistoFileSysPlus'] = S10rwPlusHisto
diboson_mumu['reweightingHistoFileSysMinus'] = S10rwMinusHisto

