import copy, os, sys
eventsInSample={}
eventsInSample['DYJetsToLL-M50'] = 30459503
eventsInSample['DYJetsToLL-M10to50'] = 7132223
eventsInSample['TTJets']  = 6923750
eventsInSample['T-tW']  = 497658
eventsInSample['T-s']  = 259961
eventsInSample['T-t']  = 99876
eventsInSample['Tbar-tW']  = 493460
eventsInSample['Tbar-s']  = 139974
eventsInSample['Tbar-t']  = 1935072
eventsInSample['WJetsToLNu-v2'] = 57709905 
eventsInSample['WJetsToLNu-v1'] = 18393090 
eventsInSample['WW'] = 10000431 
eventsInSample['WZ'] = 10000283 
eventsInSample['ZZ'] = 9799908 

path = os.path.abspath('../../HEPHYPythonTools/python')
if not path in sys.path:
    sys.path.insert(1, path)
del path
from createPUReweightingHisto import getPUReweightingUncertainty

S10rwHisto = getPUReweightingUncertainty("S10", dataFile = "/data/schoef/results2012/PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_Sys0.root")
S10rwPlusHisto = getPUReweightingUncertainty("S10", dataFile = "/data/schoef/results2012/PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_SysPlus5.root")
S10rwMinusHisto = getPUReweightingUncertainty("S10", dataFile = "/data/schoef/results2012/PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_SysMinus5.root")

data_mumu={}
data_mumu["name"]     = "data_mumu";
data_mumu["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/MET_050214/" 
data_mumu["bins"]    = ["DoubleMu-Run2012A-22Jan2013", "DoubleMu-Run2012B-22Jan2013", "DoubleMu-Run2012C-22Jan2013", "DoubleMu-Run2012D-22Jan2013"]
data_mumu["Chain"] = "Events"
data_mumu["Counter"] = "bool_EventCounter_passed_PAT.obj"
data_ee={}
data_ee["name"]     = "data_ee";
data_ee["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/MET_050214/" 
data_ee["bins"]    = ["DoubleElectron-Run2012A-22Jan2013", "DoubleElectron-Run2012B-22Jan2013", "DoubleElectron-Run2012C-22Jan2013", "DoubleElectron-Run2012D-22Jan2013"]
data_ee["Chain"] = "Events"
data_ee["Counter"] = "bool_EventCounter_passed_PAT.obj"


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
wjets_ee["bins"] = ["Ele-WJetsToLNu-v1+2"]
wjets_ee["subDirs"] = {"Ele-WJetsToLNu-v1+2":["Ele-WJetsToLNu-v1", "Ele-WJetsToLNu-v2"]}
wjets_ee["name"] = "WJetsToLNu" 
wjets_ee['reweightingHistoFile'] = S10rwHisto
wjets_ee['reweightingHistoFileSysPlus'] = S10rwPlusHisto
wjets_ee['reweightingHistoFileSysMinus'] = S10rwMinusHisto
wjets_mumu = copy.deepcopy(mc)
wjets_mumu["bins"] = ["Mu-WJetsToLNu-v1+2"]
wjets_mumu["subDirs"] = {"Mu-WJetsToLNu-v1+2":["Mu-WJetsToLNu-v1", "Mu-WJetsToLNu-v2"]}
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

