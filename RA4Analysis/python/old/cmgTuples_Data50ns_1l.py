import copy, os, sys

#data_path = "/data/easilar/cmgTuples/crab_Spring15/Summer15_50nsV4_Data/"
data_path = "/data/rschoefbeck/cmgTuples/Run2015B/50ns_1l/"

SingleMuon_Run2015B_17Jul2015 = { "name" : "SingleMuon_Run2015B-17Jul2015-v1",}
SingleMuon_Run2015B_PromptReco = { "name" : "SingleMuon_Run2015B-PromptReco-v1",}
SingleMu_Run2015B_17Jul2015 = { "name" : "SingleMu_Run2015B-17Jul2015-v1",}
SingleMu_Run2015B_PromptReco = { "name" : "SingleMu_Run2015B-PromptReco-v1",}
SingleElectron_Run2015B_17Jul2015 = { "name" : "SingleElectron_Run2015B-17Jul2015-v1",}
SingleElectron_Run2015B_PromptReco = { "name" : "SingleElectron_Run2015B-PromptReco-v1",}
DoubleEG_Run2015B_17Jul2015 = { "name" : "DoubleEG_Run2015B-17Jul2015-v1",}
DoubleEG_Run2015B_PromptReco = { "name" : "DoubleEG_Run2015B-PromptReco-v1",}
EGamma_Run2015B_17Jul2015 = { "name" : "EGamma_Run2015B-17Jul2015-v1",}
EGamma_Run2015B_PromptReco = { "name" : "EGamma_Run2015B-PromptReco-v1",}
DoubleMuon_Run2015B_17Jul2015 = { "name" : "DoubleMuon_Run2015B-17Jul2015-v1",}
DoubleMuon_Run2015B_PromptReco = { "name" : "DoubleMuon_Run2015B-PromptReco-v1",}
JetHT_Run2015B_17Jul2015 = { "name" : "JetHT_Run2015B-17Jul2015-v1",}
JetHT_Run2015B_PromptReco = { "name" : "JetHT_Run2015B-PromptReco-v1",}
MET_Run2015B_17Jul2015 = { "name" : "MET_Run2015B-17Jul2015-v1",}
MET_Run2015B_PromptReco = { "name" : "MET_Run2015B-PromptReco-v1",}

allSamples_Data50ns_1l = [SingleMuon_Run2015B_17Jul2015, SingleMuon_Run2015B_PromptReco, SingleMu_Run2015B_17Jul2015, SingleMu_Run2015B_PromptReco, SingleElectron_Run2015B_17Jul2015, SingleElectron_Run2015B_PromptReco, DoubleEG_Run2015B_17Jul2015, DoubleEG_Run2015B_PromptReco, EGamma_Run2015B_17Jul2015, EGamma_Run2015B_PromptReco, DoubleMuon_Run2015B_17Jul2015, DoubleMuon_Run2015B_PromptReco, JetHT_Run2015B_17Jul2015, JetHT_Run2015B_PromptReco, MET_Run2015B_17Jul2015, MET_Run2015B_PromptReco]

for s in allSamples_Data50ns_1l:
  s['chunkString'] = s['name']
  s.update({ 
    "rootFileLocation":"tree.root",
    "skimAnalyzerDir":"",
    "treeName":"tree",
    'isData':True,
    'dir' : data_path
  })

