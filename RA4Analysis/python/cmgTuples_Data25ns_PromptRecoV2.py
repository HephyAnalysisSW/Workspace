import copy, os, sys

#data_path = '/afs/hephy.at/data/easilar01/Ra40b/cmgTuples/4fb_HT350Skim_WithMETFilters_V2/'
data_path = '/afs/hephy.at/data/easilar01/cmgTuples/data/'

SingleElectron_Run2016B_PromptReco_v2 = {"name":"SingleElectron_Run2016B_PromptReco_v2"}
SingleElectron_Run2016C_PromptReco_v2 = {"name":"SingleElectron_Run2016C_PromptReco_v2"}
SingleElectron_Run2016D_PromptReco_v2 = {"name":"SingleElectron_Run2016D_PromptReco_v2"}

SingleMuon_Run2016B_PromptReco_v2 = {"name":"SingleMuon_Run2016B_PromptReco_v2"}
SingleMuon_Run2016C_PromptReco_v2 = {"name":"SingleMuon_Run2016C_PromptReco_v2"}
SingleMuon_Run2016D_PromptReco_v2 = {"name":"SingleMuon_Run2016D_PromptReco_v2"}

MET_Run2016B_PromptReco_v2 = {"name":"MET_Run2016B_PromptReco_v2"}
MET_Run2016C_PromptReco_v2 = {"name":"MET_Run2016C_PromptReco_v2"}
MET_Run2016D_PromptReco_v2 = {"name":"MET_Run2016D_PromptReco_v2"}

allSamples_Data25ns_0l = [SingleElectron_Run2016B_PromptReco_v2, SingleElectron_Run2016C_PromptReco_v2, SingleElectron_Run2016D_PromptReco_v2,\
                          SingleMuon_Run2016B_PromptReco_v2, SingleMuon_Run2016C_PromptReco_v2, SingleMuon_Run2016D_PromptReco_v2,\
                          MET_Run2016B_PromptReco_v2,MET_Run2016C_PromptReco_v2,MET_Run2016D_PromptReco_v2]


for s in allSamples_Data25ns_0l:
  s['chunkString'] = s['name']
  s.update({ 
    "rootFileLocation":"treeProducerSusySingleLepton/tree.root",
    "skimAnalyzerDir":"skimAnalyzerCount",
    "treeName":"tree",
    'isData':True,
    "dir":data_path,
  })
