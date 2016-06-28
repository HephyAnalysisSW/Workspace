
sample_dir = '/data/nrad/cmgTuples/Data25ns/'

SingleMuon_Run2016B_PromptReco_v2 ={
#"cmgComp":cmgSampleComponents.SingleMuon_Run2016B_PromptReco_v2,
"name" : "SingleMuon_Run2016B-PromptReco-v2",
#"name" : cmgSampleComponents.SingleMuon_Run2016B_PromptReco_v2.name,
"chunkString":"SingleMuon_Run2016B-PromptReco-v2",
"dir": sample_dir +"/" + "SingleMuon_Run2016B-PromptReco-v2",
"dbsName" : "/SingleMuon/Run2016B-PromptReco-v2/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : None,

}


MET_Run2016B_PromptReco_v2 ={
#"cmgComp":cmgSampleComponents.MET_Run2016B_PromptReco_v2,
"name" : "MET_Run2016B-PromptReco-v2",
#"name" : cmgSampleComponents.MET_Run2016B_PromptReco_v2.name,
"chunkString":"MET_Run2016B-PromptReco-v2",
"dir": sample_dir +"/" + "MET_Run2016B-PromptReco-v2",
"dbsName" : "/MET/Run2016B-PromptReco-v2/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : None,

}


SingleElectron_Run2016B_PromptReco_v2 ={
#"cmgComp":cmgSampleComponents.SingleElectron_Run2016B_PromptReco_v2,
"name" : "SingleElectron_Run2016B-PromptReco-v2",
#"name" : cmgSampleComponents.SingleElectron_Run2016B_PromptReco_v2.name,
"chunkString":"SingleElectron_Run2016B-PromptReco-v2",
"dir": sample_dir +"/" + "SingleElectron_Run2016B-PromptReco-v2",
"dbsName" : "/SingleElectron/Run2016B-PromptReco-v2/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : None,

}

 #All Done, but These Samples are Missing ['TTJets_LO', 'TTJets_LO_HT600to800_ext', 'TTJets_LO_HT800to1200_ext', 'TTJets_LO_HT1200to2500_ext', 'TTJets_LO_HT2500toInf', 'TTJets_LO_HT600to800', 'TTJets_LO_HT800to1200', 'TTJets_LO_HT1200to2500', 'TTJets_SingleLeptonFromT', 'TTJets_SingleLeptonFromTbar', 'TTJets_DiLepton', 'WJetsToLNu_LO', 'WJetsToLNu_HT100to200', 'WJetsToLNu_HT100to200_ext', 'WJetsToLNu_HT200to400', 'WJetsToLNu_HT200to400_ext', 'WJetsToLNu_HT400to600', 'WJetsToLNu_HT600to800', 'WJetsToLNu_HT800to1200', 'WJetsToLNu_HT800to1200_ext', 'WJetsToLNu_HT1200to2500', 'WJetsToLNu_HT2500toInf', 'ZJetsToNuNu_HT100to200', 'ZJetsToNuNu_HT200to400', 'ZJetsToNuNu_HT400to600', 'ZJetsToNuNu_HT600toInf', 'QCD_HT100to200', 'QCD_HT200to300', 'QCD_HT300to500', 'QCD_HT500to700', 'QCD_HT700to1000', 'QCD_HT1000to1500', 'QCD_HT1500to2000', 'QCD_HT2000toInf', 'DYJetsToLL_M5to50_LO', 'DYJetsToNuNu_M50', 'DYJetsToLL_M5to50_HT100to200', 'DYJetsToLL_M5to50_HT200to400', 'DYJetsToLL_M5to50_HT400to600', 'DYJetsToLL_M5to50_HT600toInf', 'DYJetsToLL_M50_HT100to200', 'DYJetsToLL_M50_HT200to400', 'DYJetsToLL_M50_HT400to600', 'DYJetsToLL_M50_HT600toInf']
