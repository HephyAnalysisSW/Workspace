sample_path = '/data/nrad/cmgTuples/8011_mAODv2_v1/Data25ns'   
allComponents=[] 


MET_Run2016B_PromptReco_v2 ={
'cmgName':"MET_Run2016B_PromptReco_v2",
"name" : "MET_Run2016B-PromptReco-v2",
#"name" : comp.name,
"chunkString":"MET_Run2016B-PromptReco-v2",
"dir": sample_path +"/" + "MET_Run2016B-PromptReco-v2",
"dbsName" : "/MET/Run2016B-PromptReco-v2/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,

}
allComponents.append(MET_Run2016B_PromptReco_v2)



SingleElectron_Run2016B_PromptReco_v2 ={
'cmgName':"SingleElectron_Run2016B_PromptReco_v2",
"name" : "SingleElectron_Run2016B-PromptReco-v2",
#"name" : comp.name,
"chunkString":"SingleElectron_Run2016B-PromptReco-v2",
"dir": sample_path +"/" + "SingleElectron_Run2016B-PromptReco-v2",
"dbsName" : "/SingleElectron/Run2016B-PromptReco-v2/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,

}
allComponents.append(SingleElectron_Run2016B_PromptReco_v2)



SingleMuon_Run2016B_PromptReco_v2 ={
'cmgName':"SingleMuon_Run2016B_PromptReco_v2",
"name" : "SingleMuon_Run2016B-PromptReco-v2",
#"name" : comp.name,
"chunkString":"SingleMuon_Run2016B-PromptReco-v2",
"dir": sample_path +"/" + "SingleMuon_Run2016B-PromptReco-v2",
"dbsName" : "/SingleMuon/Run2016B-PromptReco-v2/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,

}
allComponents.append(SingleMuon_Run2016B_PromptReco_v2)

