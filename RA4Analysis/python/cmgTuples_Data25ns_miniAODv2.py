import copy, os, sys

#data_path = "/data/easilar/tuples_from_Artur/JECv6recalibrateMET_eleCBID_1550pb"
#data_path = "/data/easilar/tuples_from_Artur/JECv6recalibrateMET_2100pb/trig_skim/"
#data_path = '/data/easilar/tuples_from_Artur/JECv6recalibrateMET_2p2fb/'
data_path = '/data/easilar/tuples_from_Artur/TrigSkim_noHBHEfix/'
SingleMuon_Run2015D_v4 = {"name":"SingleMuon_Run2015D_v4",}
SingleMuon_Run2015D_05Oct= {"name":"SingleMuon_Run2015D_05Oct",}
SingleElectron_Run2015D_v4= {"name":"SingleElectron_Run2015D_v4",}
SingleElectron_Run2015D_05Oct= {"name":"SingleElectron_Run2015D_05Oct",}
#JetHT_Run2015D_PromptReco = { "name" : "JetHT_Run2015D-PromptReco-v3",}

allSamples_Data25ns_0l = [SingleMuon_Run2015D_v4 , SingleMuon_Run2015D_05Oct , SingleElectron_Run2015D_v4 , SingleElectron_Run2015D_05Oct ]

for s in allSamples_Data25ns_0l:
  s['chunkString'] = s['name']
  s.update({ 
    "rootFileLocation":"/treeProducerSusySingleLepton/tree.root",
    "skimAnalyzerDir":"skimAnalyzerCount",
    "treeName":"tree",
    'isData':True,
    'dir' : data_path
  })
