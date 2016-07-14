import copy, os, sys

#data_path = '/afs/hephy.at/data/easilar01/Ra40b/cmgTuples/4fb_HT350Skim_WithMETFilters_V2/'
data_path = '/afs/hephy.at/data/easilar01/Ra40b/cmgTuples/RunIIMiniAOD_Data/'

SingleElectron_Run2016B_PromptReco_v2     = {"name":"SingleElectron_Run2016B-PromptReco-v2"}
SingleElectron_Run2016B_PromptReco_v2_1   = {"name":"SingleElectron_Run2016B-PromptReco-v2_1"}
SingleElectron_Run2016B_PromptReco_v2_1_a = {"name":"SingleElectron_Run2016B-PromptReco-v2_1_a"}
SingleElectron_Run2016B_PromptReco_v2_1_b = {"name":"SingleElectron_Run2016B-PromptReco-v2_1_b"}
SingleElectron_Run2016B_PromptReco_v2_2   = {"name":"SingleElectron_Run2016B-PromptReco-v2_2"}
SingleElectron_Run2016C_PromptReco_v2     = {"name":"SingleElectron_Run2016C-PromptReco-v2"}

SingleMuon_Run2016B_PromptReco_v2     = {"name":"SingleMuon_Run2016B-PromptReco-v2"}
SingleMuon_Run2016B_PromptReco_v2_1   = {"name":"SingleMuon_Run2016B-PromptReco-v2_1"}
SingleMuon_Run2016B_PromptReco_v2_1_a = {"name":"SingleMuon_Run2016B-PromptReco-v2_1_a"}
SingleMuon_Run2016B_PromptReco_v2_1_b = {"name":"SingleMuon_Run2016B-PromptReco-v2_1_b"}
SingleMuon_Run2016B_PromptReco_v2_2   = {"name":"SingleMuon_Run2016B-PromptReco-v2_2"}
SingleMuon_Run2016C_PromptReco_v2     = {"name":"SingleMuon_Run2016C-PromptReco-v2"}

allSamples_Data25ns_0l = [SingleElectron_Run2016B_PromptReco_v2,SingleElectron_Run2016B_PromptReco_v2_1,SingleElectron_Run2016B_PromptReco_v2_1_a,SingleElectron_Run2016B_PromptReco_v2_1_b,SingleElectron_Run2016B_PromptReco_v2_2,SingleElectron_Run2016C_PromptReco_v2,SingleMuon_Run2016B_PromptReco_v2,SingleMuon_Run2016B_PromptReco_v2_1,SingleMuon_Run2016B_PromptReco_v2_1_a,SingleMuon_Run2016B_PromptReco_v2_1_b,SingleMuon_Run2016B_PromptReco_v2_2,SingleMuon_Run2016C_PromptReco_v2]

for s in allSamples_Data25ns_0l:
  s['chunkString'] = s['name']
  s.update({ 
    "rootFileLocation":"treeProducerSusySingleLepton/tree.root",
    "skimAnalyzerDir":"skimAnalyzerCount",
    "treeName":"tree",
    'isData':True,
    "dir":data_path, #+s['name'],
  })
