''' Sample definition file for CMG tuples of background MC samples.


Note: samples which have extended datasets have the key "ext" which is a list of all datasets
contributing to the sample, including the dataset which is defined.

Example: 
    "ext": [WJetsToLNu_HT200to400, WJetsToLNu_HT200to400_ext] 
    appears in both WJetsToLNu_HT200to400 and WJetsToLNu_HT200to400_ext definition.
'''
import PhysicsTools.HeppyCore.framework.config as cfg

import CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 as cmgSampleComponents

def wikiPrint(sample):
    
    sampleName = sample['cmgComp'].name
    dasString = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2F"
    dbsString = sample['dbsName'][1:]
    datasetShort = sample['dbsName'].replace("RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0", "*")
    
    print "|-"
    print "|| {0} || {1} || - || [{2}{3} {4}]".format(sampleName, sample['xsec'], dasString, dbsString, datasetShort)
    print "|| Done || Done || DIRECTORY ||  ||"


sample_dir = "/data/nrad/cmgTuples/8011_mAODv2_v0/RunIISpring16MiniAODv2"

allComponents = []

TTJets_LO ={
"cmgComp":cmgSampleComponents.TTJets_LO,
"name" : "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
#"name" : cmgSampleComponents.TTJets_LO.name,
"chunkString":"TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_dir +"/" + "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 831.76,

}
allComponents.append(TTJets_LO)


TTJets_LO_HT600to800_ext ={
"cmgComp":cmgSampleComponents.TTJets_LO_HT600to800_ext,
"name" : "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
#"name" : cmgSampleComponents.TTJets_LO_HT600to800_ext.name,
"chunkString":"TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dir": sample_dir +"/" + "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dbsName" : "/TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 2.66653444843,

}
allComponents.append(TTJets_LO_HT600to800_ext)


TTJets_LO_HT800to1200_ext ={
"cmgComp":cmgSampleComponents.TTJets_LO_HT800to1200_ext,
"name" : "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
#"name" : cmgSampleComponents.TTJets_LO_HT800to1200_ext.name,
"chunkString":"TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dir": sample_dir +"/" + "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dbsName" : "/TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 1.09808219833,

}
allComponents.append(TTJets_LO_HT800to1200_ext)


TTJets_LO_HT1200to2500_ext ={
"cmgComp":cmgSampleComponents.TTJets_LO_HT1200to2500_ext,
"name" : "TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
#"name" : cmgSampleComponents.TTJets_LO_HT1200to2500_ext.name,
"chunkString":"TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dir": sample_dir +"/" + "TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dbsName" : "/TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 0.1987479092,

}
allComponents.append(TTJets_LO_HT1200to2500_ext)


TTJets_LO_HT2500toInf ={
"cmgComp":cmgSampleComponents.TTJets_LO_HT2500toInf,
"name" : "TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
#"name" : cmgSampleComponents.TTJets_LO_HT2500toInf.name,
"chunkString":"TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_dir +"/" + "TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 0.00236841258463,

}
allComponents.append(TTJets_LO_HT2500toInf)


TTJets_SingleLeptonFromT ={
"cmgComp":cmgSampleComponents.TTJets_SingleLeptonFromT,
"name" : "TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
#"name" : cmgSampleComponents.TTJets_SingleLeptonFromT.name,
"chunkString":"TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_dir +"/" + "TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 182.17540224,

}
allComponents.append(TTJets_SingleLeptonFromT)


TTJets_SingleLeptonFromTbar ={
"cmgComp":cmgSampleComponents.TTJets_SingleLeptonFromTbar,
"name" : "TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
#"name" : cmgSampleComponents.TTJets_SingleLeptonFromTbar.name,
"chunkString":"TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_dir +"/" + "TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 182.17540224,

}
allComponents.append(TTJets_SingleLeptonFromTbar)


TTJets_DiLepton ={
"cmgComp":cmgSampleComponents.TTJets_DiLepton,
"name" : "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v4",
#"name" : cmgSampleComponents.TTJets_DiLepton.name,
"chunkString":"TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v4",
"dir": sample_dir +"/" + "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v4",
"dbsName" : "/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v4/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 87.31483776,

}
allComponents.append(TTJets_DiLepton)


WJetsToLNu_HT100to200_ext ={
"cmgComp":cmgSampleComponents.WJetsToLNu_HT100to200_ext,
"name" : "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
#"name" : cmgSampleComponents.WJetsToLNu_HT100to200_ext.name,
"chunkString":"WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dir": sample_dir +"/" + "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dbsName" : "/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 1627.45,

}
allComponents.append(WJetsToLNu_HT100to200_ext)


WJetsToLNu_HT200to400 ={
"cmgComp":cmgSampleComponents.WJetsToLNu_HT200to400,
"name" : "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
#"name" : cmgSampleComponents.WJetsToLNu_HT200to400.name,
"chunkString":"WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_dir +"/" + "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 435.237,
"ext": ['WJetsToLNu_HT200to400', 'WJetsToLNu_HT200to400_ext'],

}
allComponents.append(WJetsToLNu_HT200to400)


WJetsToLNu_HT200to400_ext ={
"cmgComp":cmgSampleComponents.WJetsToLNu_HT200to400_ext,
"name" : "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
#"name" : cmgSampleComponents.WJetsToLNu_HT200to400_ext.name,
"chunkString":"WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dir": sample_dir +"/" + "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dbsName" : "/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 435.237,
"ext": ['WJetsToLNu_HT200to400', 'WJetsToLNu_HT200to400_ext'],

}
allComponents.append(WJetsToLNu_HT200to400_ext)


WJetsToLNu_HT400to600 ={
"cmgComp":cmgSampleComponents.WJetsToLNu_HT400to600,
"name" : "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
#"name" : cmgSampleComponents.WJetsToLNu_HT400to600.name,
"chunkString":"WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_dir +"/" + "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 59.1811,

}
allComponents.append(WJetsToLNu_HT400to600)


WJetsToLNu_HT600to800 ={
"cmgComp":cmgSampleComponents.WJetsToLNu_HT600to800,
"name" : "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
#"name" : cmgSampleComponents.WJetsToLNu_HT600to800.name,
"chunkString":"WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_dir +"/" + "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 14.5805,

}
allComponents.append(WJetsToLNu_HT600to800)


WJetsToLNu_HT800to1200_ext ={
"cmgComp":cmgSampleComponents.WJetsToLNu_HT800to1200_ext,
"name" : "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
#"name" : cmgSampleComponents.WJetsToLNu_HT800to1200_ext.name,
"chunkString":"WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dir": sample_dir +"/" + "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dbsName" : "/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 6.65621,

}
allComponents.append(WJetsToLNu_HT800to1200_ext)


WJetsToLNu_HT1200to2500 ={
"cmgComp":cmgSampleComponents.WJetsToLNu_HT1200to2500,
"name" : "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
#"name" : cmgSampleComponents.WJetsToLNu_HT1200to2500.name,
"chunkString":"WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_dir +"/" + "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 1.60809,

}
allComponents.append(WJetsToLNu_HT1200to2500)


WJetsToLNu_HT2500toInf ={
"cmgComp":cmgSampleComponents.WJetsToLNu_HT2500toInf,
"name" : "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
#"name" : cmgSampleComponents.WJetsToLNu_HT2500toInf.name,
"chunkString":"WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_dir +"/" + "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 0.0389136,

}
allComponents.append(WJetsToLNu_HT2500toInf)


QCD_HT300to500 ={
"cmgComp":cmgSampleComponents.QCD_HT300to500,
"name" : "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
#"name" : cmgSampleComponents.QCD_HT300to500.name,
"chunkString":"QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_dir +"/" + "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 351300,
"ext": ['QCD_HT300to500', 'QCD_HT300to500_ext'],

}
allComponents.append(QCD_HT300to500)

QCD_HT300to500_ext ={
"cmgComp":cmgSampleComponents.QCD_HT300to500_ext,
"name" : "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
#"name" : cmgSampleComponents.QCD_HT300to500_ext.name,
"chunkString":"QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dir": sample_dir +"/" + "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dbsName" : "/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 351300,
"ext": ['QCD_HT300to500', 'QCD_HT300to500_ext'],

}
allComponents.append(QCD_HT300to500_ext)

QCD_HT500to700_ext ={
"cmgComp":cmgSampleComponents.QCD_HT500to700_ext,
"name" : "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
#"name" : cmgSampleComponents.QCD_HT500to700_ext.name,
"chunkString":"QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dir": sample_dir +"/" + "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dbsName" : "/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 31630,

}
allComponents.append(QCD_HT500to700_ext)

QCD_HT700to1000 ={
"cmgComp":cmgSampleComponents.QCD_HT700to1000,
"name" : "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
#"name" : cmgSampleComponents.QCD_HT700to1000.name,
"chunkString":"QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_dir +"/" + "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 6802,
"ext": ['QCD_HT700to1000', 'QCD_HT700to1000_ext'],

}
allComponents.append(QCD_HT700to1000)

QCD_HT700to1000_ext ={
"cmgComp":cmgSampleComponents.QCD_HT700to1000_ext,
"name" : "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
#"name" : cmgSampleComponents.QCD_HT700to1000_ext.name,
"chunkString":"QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dir": sample_dir +"/" + "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dbsName" : "/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 6802,
"ext": ['QCD_HT700to1000', 'QCD_HT700to1000_ext'],

}
allComponents.append(QCD_HT700to1000_ext)

QCD_HT1000to1500 ={
"cmgComp":cmgSampleComponents.QCD_HT1000to1500,
"name" : "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2",
#"name" : cmgSampleComponents.QCD_HT1000to1500.name,
"chunkString":"QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2",
"dir": sample_dir +"/" + "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2",
"dbsName" : "/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 1206,
"ext": ['QCD_HT1000to1500', 'QCD_HT1000to1500_ext'],

}
allComponents.append(QCD_HT1000to1500)

QCD_HT1000to1500_ext ={
"cmgComp":cmgSampleComponents.QCD_HT1000to1500_ext,
"name" : "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
#"name" : cmgSampleComponents.QCD_HT1000to1500_ext.name,
"chunkString":"QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dir": sample_dir +"/" + "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dbsName" : "/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 1206,
"ext": ['QCD_HT1000to1500', 'QCD_HT1000to1500_ext'],

}
allComponents.append(QCD_HT1000to1500_ext)

QCD_HT1500to2000 ={
"cmgComp":cmgSampleComponents.QCD_HT1500to2000,
"name" : "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v3",
#"name" : cmgSampleComponents.QCD_HT1500to2000.name,
"chunkString":"QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v3",
"dir": sample_dir +"/" + "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v3",
"dbsName" : "/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v3/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 120.4,
"ext": ['QCD_HT1500to2000', 'QCD_HT1500to2000_ext'],

}
allComponents.append(QCD_HT1500to2000)

QCD_HT1500to2000_ext ={
"cmgComp":cmgSampleComponents.QCD_HT1500to2000_ext,
"name" : "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
#"name" : cmgSampleComponents.QCD_HT1500to2000_ext.name,
"chunkString":"QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dir": sample_dir +"/" + "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dbsName" : "/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 120.4,
"ext": ['QCD_HT1500to2000', 'QCD_HT1500to2000_ext'],

}
allComponents.append(QCD_HT1500to2000_ext)

QCD_HT2000toInf ={
"cmgComp":cmgSampleComponents.QCD_HT2000toInf,
"name" : "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
#"name" : cmgSampleComponents.QCD_HT2000toInf.name,
"chunkString":"QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_dir +"/" + "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 25.25,
"ext": ['QCD_HT2000toInf', 'QCD_HT2000toInf_ext'],

}
allComponents.append(QCD_HT2000toInf)

QCD_HT2000toInf_ext ={
"cmgComp":cmgSampleComponents.QCD_HT2000toInf_ext,
"name" : "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
#"name" : cmgSampleComponents.QCD_HT2000toInf_ext.name,
"chunkString":"QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dir": sample_dir +"/" + "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dbsName" : "/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 25.25,
"ext": ['QCD_HT2000toInf', 'QCD_HT2000toInf_ext'],

}
allComponents.append(QCD_HT2000toInf_ext)

DYJetsToLL_M50_HT100to200_ext ={
"cmgComp":cmgSampleComponents.DYJetsToLL_M50_HT100to200_ext,
"name" : "DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
#"name" : cmgSampleComponents.DYJetsToLL_M50_HT100to200_ext.name,
"chunkString":"DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dir": sample_dir +"/" + "DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dbsName" : "/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 171.462,

}
allComponents.append(DYJetsToLL_M50_HT100to200_ext)

DYJetsToLL_M50_HT200to400_ext ={
"cmgComp":cmgSampleComponents.DYJetsToLL_M50_HT200to400_ext,
"name" : "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
#"name" : cmgSampleComponents.DYJetsToLL_M50_HT200to400_ext.name,
"chunkString":"DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dir": sample_dir +"/" + "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dbsName" : "/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 52.5825,

}
allComponents.append(DYJetsToLL_M50_HT200to400_ext)

DYJetsToLL_M50_HT400to600_ext ={
"cmgComp":cmgSampleComponents.DYJetsToLL_M50_HT400to600_ext,
"name" : "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
#"name" : cmgSampleComponents.DYJetsToLL_M50_HT400to600_ext.name,
"chunkString":"DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dir": sample_dir +"/" + "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dbsName" : "/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 6.76131,

}
allComponents.append(DYJetsToLL_M50_HT400to600_ext)

DYJetsToLL_M50_HT600toInf ={
"cmgComp":cmgSampleComponents.DYJetsToLL_M50_HT600toInf,
"name" : "DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
#"name" : cmgSampleComponents.DYJetsToLL_M50_HT600toInf.name,
"chunkString":"DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_dir +"/" + "DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 2.7183,
"ext": ['DYJetsToLL_M50_HT600toInf', 'DYJetsToLL_M50_HT600toInf_ext'],

}
allComponents.append(DYJetsToLL_M50_HT600toInf)

DYJetsToLL_M50_HT600toInf_ext ={
"cmgComp":cmgSampleComponents.DYJetsToLL_M50_HT600toInf_ext,
"name" : "DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
#"name" : cmgSampleComponents.DYJetsToLL_M50_HT600toInf_ext.name,
"chunkString":"DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dir": sample_dir +"/" + "DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
"dbsName" : "/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 2.7183,
"ext": ['DYJetsToLL_M50_HT600toInf', 'DYJetsToLL_M50_HT600toInf_ext'],

}
allComponents.append(DYJetsToLL_M50_HT600toInf_ext)


ZJetsToNuNu_HT600to800 ={
"cmgComp":cmgSampleComponents.ZJetsToNuNu_HT600to800,
"name" : "ZJetsToNuNu_HT-600To800_13TeV-madgraph_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
#"name" : cmgSampleComponents.ZJetsToNuNu_HT600to800.name,
"chunkString":"ZJetsToNuNu_HT-600To800_13TeV-madgraph_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_dir +"/" + "ZJetsToNuNu_HT-600To800_13TeV-madgraph_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/ZJetsToNuNu_HT-600To800_13TeV-madgraph/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 9.44271,

}
allComponents.append(ZJetsToNuNu_HT600to800)

ZJetsToNuNu_HT1200to2500 ={
"cmgComp":cmgSampleComponents.ZJetsToNuNu_HT1200to2500,
"name" : "ZJetsToNuNu_HT-1200To2500_13TeV-madgraph_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
#"name" : cmgSampleComponents.ZJetsToNuNu_HT1200to2500.name,
"chunkString":"ZJetsToNuNu_HT-1200To2500_13TeV-madgraph_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_dir +"/" + "ZJetsToNuNu_HT-1200To2500_13TeV-madgraph_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/ZJetsToNuNu_HT-1200To2500_13TeV-madgraph/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 0.359406,

}
allComponents.append(ZJetsToNuNu_HT1200to2500)

ZJetsToNuNu_HT2500toInf ={
"cmgComp":cmgSampleComponents.ZJetsToNuNu_HT2500toInf,
"name" : "ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
#"name" : cmgSampleComponents.ZJetsToNuNu_HT2500toInf.name,
"chunkString":"ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_dir +"/" + "ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount", 
"treeName":"tree",
"isData":False,
"xsec" : 0.00851652,

}
allComponents.append(ZJetsToNuNu_HT2500toInf)


# signal samples

# FIXME temporary solution, until 80X samples are available

import CMGTools.RootTools.samples.samples_13TeV_74X_susyT2DegStopPriv as signals_priv

sample_path_signal = "/data/mzarucki/cmgTuples/7412pass2_mAODv2_v7/RunIISpring15MiniAODv2/"

allSignalData=[
    [
     sample_path_signal+"T2DegStop_300_270_GEN-SIM/",
    "nrad-T2DegStop_300_270_MINIAODv2-RunIISpring15-MCRUN2_74_V9-25ns-4dc17ff0fe241c35c03aa547f2361414",
    "T2DegStop_300_270", 
    signals_priv.T2DegStop_300_270
    ],
    [
     sample_path_signal+"T2DegStop_300_240_FastSim_v3/",
     "nrad-T2DegStop_300_240FS-eb69b0448a13fda070ca35fd76ab4e24" ,
     "T2DegStop_300_240_FastSim", 
     signals_priv.T2DegStop_300_240_FastSim 
     ],
    [
     sample_path_signal+"T2DegStop_300_270_FastSim_v3/",
     "nrad-T2DegStop_300_270FS-eb69b0448a13fda070ca35fd76ab4e24",
     "T2DegStop_300_270_FastSim", 
     signals_priv.T2DegStop_300_270_FastSim 
     ],
    [
     sample_path_signal+"T2DegStop_300_290_FastSim_v3/",
     "nrad-T2DegStop_300_290FS-eb69b0448a13fda070ca35fd76ab4e24" ,
     "T2DegStop_300_290_FastSim", 
     signals_priv.T2DegStop_300_290_FastSim
     ],
    [
     sample_path_signal+"T2tt_stop300_LSP270/",
     "nrad-CMSSW_7_4_4_FastSim_PU25ns_MCRUN2_74_V9_7414_MINIAODv2-eb69b0448a13fda070ca35fd76ab4e24" ,
     "T2tt_300_270_FastSim", 
     signals_priv.T2tt_300_270_FastSim
     ],
    ]

allSignalStrings = [s[2] for s in allSignalData]
def getSignalSample(base_dir,chunk_dir, signal,component):
  if signal in allSignalStrings:
     
    # dirty way of creating a CMG component        
    #component = cfg.MCComponent(
    #    dataset=signal,
    #    name = signal,
    #    files = [],
    #    xSection = 0.0,
    #    nGenEvents = 1,
    #    triggers = [],
    #    effCorrFactor = 1,
    #    )
      
    return {\
      'cmgComp': component,
      "name" : signal,
      #"name" : component.name,
      "chunkString": chunk_dir,
      'dir' : base_dir+"/"+chunk_dir,
      'dbsName':component.dataset,
      'isData':False,
      #"rootFileLocation":"treeProducerSusySingleLepton/tree.root",
      "rootFileLocation":"tree.root",
      "treeName":"tree",
      #"skimAnalyzerDir":"skimAnalyzerCount",
      }
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

allSignals=[]
for sig in allSignalData:
  #exec(s+"=getSignalSample('"+d+"','"+s+"')")
  signal = getSignalSample(*sig)
  exec("{s}=signal".format(s=sig[2]))
  exec("allSignals.append({s})".format(s=sig[2]))
  
for sample in allSignals:
    if hasattr(sample['cmgComp'],"xSection"):
        sample['xsec'] = sample['cmgComp'].xSection

allComponents.extend(allSignals)


if __name__ == "__main__":
   import sys
   if "printWiki" in sys.argv:
       for comp in allComponents:
           wikiPrint(comp)

