import PhysicsTools.HeppyCore.framework.config as cfg
import CMGTools.RootTools.samples.samples_13TeV_DATA2016 as cmgSampleComponents

sample_dir = '/data/nrad/cmgTuples/8011_mAODv2_v0/Data25ns'

SingleMuon_Run2016B_PromptReco_v2 ={
"cmgComp":cmgSampleComponents.SingleMuon_Run2016B_PromptReco_v2,
"name" : "SingleMuon_Run2016B-PromptReco-v2",
#"name" : SingleMuon_Run2016B_PromptReco_v2.name,
"chunkString":"SingleMuon_Run2016B-PromptReco-v2",
"dir": sample_dir +"/" + "SingleMuon_Run2016B-PromptReco-v2",
"dbsName" : "/SingleMuon/Run2016B-PromptReco-v2/MINIAOD",
"rootFileLocation":"/tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":True,
"xsec" : None,

}


MET_Run2016B_PromptReco_v2 ={
"cmgComp":cmgSampleComponents.MET_Run2016B_PromptReco_v2,
"name" : "MET_Run2016B-PromptReco-v2",
#"name" : MET_Run2016B_PromptReco_v2.name,
"chunkString":"MET_Run2016B-PromptReco-v2",
"dir": sample_dir +"/" + "MET_Run2016B-PromptReco-v2",
"dbsName" : "/MET/Run2016B-PromptReco-v2/MINIAOD",
"rootFileLocation":"/tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":True,
"xsec" : None,

}


SingleElectron_Run2016B_PromptReco_v2 ={
"cmgComp":cmgSampleComponents.SingleElectron_Run2016B_PromptReco_v2,
"name" : "SingleElectron_Run2016B-PromptReco-v2",
#"name" : SingleElectron_Run2016B_PromptReco_v2.name,
"chunkString":"SingleElectron_Run2016B-PromptReco-v2",
"dir": sample_dir +"/" + "SingleElectron_Run2016B-PromptReco-v2",
"dbsName" : "/SingleElectron/Run2016B-PromptReco-v2/MINIAOD",
"rootFileLocation":"/tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":True,
"xsec" : None,

}
