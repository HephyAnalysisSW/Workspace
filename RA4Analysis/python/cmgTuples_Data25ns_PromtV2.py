import copy, os, sys

#data_path = "/data/easilar/tuples_from_Artur/JECv6recalibrateMET_eleCBID_1550pb"
#data_path = "/data/easilar/tuples_from_Artur/JECv6recalibrateMET_2100pb/trig_skim/"
#data_path = '/data/easilar/tuples_from_Artur/JECv6recalibrateMET_2p2fb/'
#data_path = '/data/easilar/tuples_from_Artur/JECv7_lumi2p2fb/TrigSkim/'
#data_path_1 = '/data/easilar/cmgTuples/Run2016B-PromptReco-v2/cmgTuples_SingleElectron_Run2016B-PromptReco-v2_heppy/'
#data_path_2 = '/data/dspitzbart/cmgTuples/Run2016B-PromptReco-v2/cmgTuples_SingleMuon_Run2016B-PromptReco-v2_heppy/'
#data_path = '/data/easilar/cmgTuples/Run2016B-PromptReco-v2/fromHenning_804/'
#data_path = '/afs/hephy.at/data/easilar01/cmgTuples/'
data_path = '/data/easilar/cmgTuples/Run2016B-PromptReco-v2/lumi_2p5fb/'

SingleElectron_Run2016B_PromptReco_v2 ={"name":"SingleElectron_Run2016B_PromptReco_v2",}
SingleMuon_Run2016B_PromptReco_v2 ={"name":"SingleMuon_Run2016B_PromptReco_v2",}

allSamples_Data25ns_0l = [SingleElectron_Run2016B_PromptReco_v2 , SingleMuon_Run2016B_PromptReco_v2]

for s in allSamples_Data25ns_0l:
  s['chunkString'] = s['name']
  s.update({ 
    "rootFileLocation":"treeProducerSusySingleLepton/tree.root",
    "skimAnalyzerDir":"skimAnalyzerCount",
    "treeName":"tree",
    'isData':True,
    "dir":data_path, #+s['name'],
  })
