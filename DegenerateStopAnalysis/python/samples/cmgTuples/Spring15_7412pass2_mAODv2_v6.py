import CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 as cmgSampleComponents

# temporary solution for CMG components and cross-section of signal or samples not in the CMG sample file
import PhysicsTools.HeppyCore.framework.config as cfg
from Workspace.HEPHYPythonTools.xsec import xsec

sample_path = "/data/nrad/cmgTuples/7412pass2_mAODv2_v6/RunIISpring15MiniAODv2/"
import pickle
#mass_dict_path  = "/data/nrad/cmgTuples/RunII/7412pass2_mAODv2_v4/RunIISpring15MiniAODv2/mass_dict_all.pkl"
import os
mass_dict_all_file = sample_path+"/mass_dict.pkl"
mass_dict_samples_file = sample_path+"/mass_dict_samples.pkl"
if os.path.isfile(mass_dict_all_file):
    mass_dict = pickle.load(open(mass_dict_all_file,"r"))   
else:
    mass_dict = {}

if os.path.isfile(mass_dict_samples_file ):
    mass_dict_samples = pickle.load(open(mass_dict_samples_file,"r"))   
else:
    mass_dict_samples = {}

TTJets_LO = {\
"cmgComp":cmgSampleComponents.TTJets_LO,
"name" : "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path ,
"dbsName" : cmgSampleComponents.TTJets_LO.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False,
}

TTJets_LO_HT600to800 ={\
"cmgComp":cmgSampleComponents.TTJets_LO_HT600to800,
"name": "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString": "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path ,
"dbsName" : cmgSampleComponents.TTJets_LO_HT600to800.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False,
}

TTJets_LO_HT800to1200 ={\
"cmgComp":cmgSampleComponents.TTJets_LO_HT800to1200,
"name" : "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.TTJets_LO_HT800to1200.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False,
}
TTJets_LO_HT1200to2500 ={\
"cmgComp":cmgSampleComponents.TTJets_LO_HT1200to2500,
"name" : "TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.TTJets_LO_HT1200to2500.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False,
}
TTJets_LO_HT2500toInf ={\
"cmgComp":cmgSampleComponents.TTJets_LO_HT2500toInf,
"name" : "TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.TTJets_LO_HT2500toInf.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}


WJetsToLNu ={\
"cmgComp":cmgSampleComponents.WJetsToLNu,
"name" : "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.WJetsToLNu.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT100to200 ={\
"cmgComp":cmgSampleComponents.WJetsToLNu_HT100to200,
"name" : "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.WJetsToLNu_HT100to200.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT200to400 ={\
"cmgComp":cmgSampleComponents.WJetsToLNu_HT200to400,
"name" : "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.WJetsToLNu_HT200to400.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT400to600 ={\
"cmgComp":cmgSampleComponents.WJetsToLNu_HT400to600,
"name" : "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.WJetsToLNu_HT400to600.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT600toInf ={\
"cmgComp":cmgSampleComponents.WJetsToLNu_HT600toInf,
"name" : "WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.WJetsToLNu_HT600toInf.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT600to800 ={\
"cmgComp":cmgSampleComponents.WJetsToLNu_HT600to800,
"name" : "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.WJetsToLNu_HT600to800.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT800to1200 ={\
"cmgComp":cmgSampleComponents.WJetsToLNu_HT800to1200,
"name" : "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.WJetsToLNu_HT800to1200.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}


WJetsToLNu_HT1200to2500 ={\
"cmgComp":cmgSampleComponents.WJetsToLNu_HT1200to2500,
"name" : "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.WJetsToLNu_HT1200to2500.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT2500toInf ={\
"cmgComp":cmgSampleComponents.WJetsToLNu_HT2500toInf,
"name" : "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.WJetsToLNu_HT2500toInf.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}





ZJetsToNuNu_HT100to200 ={\
"cmgComp":cmgSampleComponents.ZJetsToNuNu_HT100to200,
"name" :"ZJetsToNuNu_HT-100To200_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1", 
"chunkString":"ZJetsToNuNu_HT-100To200_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.ZJetsToNuNu_HT100to200.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

ZJetsToNuNu_HT200to400 ={\
"cmgComp":cmgSampleComponents.ZJetsToNuNu_HT200to400,
"name" :"ZJetsToNuNu_HT-200To400_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1", 
"chunkString":"ZJetsToNuNu_HT-200To400_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.ZJetsToNuNu_HT200to400.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}


ZJetsToNuNu_HT400to600 ={\
"cmgComp":cmgSampleComponents.ZJetsToNuNu_HT400to600,
"name" :"ZJetsToNuNu_HT-400To600_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1", 
"chunkString":"ZJetsToNuNu_HT-400To600_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.ZJetsToNuNu_HT400to600.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}



ZJetsToNuNu_HT600toInf ={\
"cmgComp":cmgSampleComponents.ZJetsToNuNu_HT600toInf,
"name" :"ZJetsToNuNu_HT-600ToInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2", 
"chunkString":"ZJetsToNuNu_HT-600ToInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2",
"dir": sample_path,
"dbsName" : cmgSampleComponents.ZJetsToNuNu_HT600toInf.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}


QCD_HT200to300 = {
"cmgComp": cmgSampleComponents.QCD_HT200to300   ,
"dbsName" : cmgSampleComponents.QCD_HT200to300.dataset,
"name" : "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString" : "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT300to500   ={
"cmgComp": cmgSampleComponents.QCD_HT300to500   ,
"dbsName" : cmgSampleComponents.QCD_HT300to500.dataset,
"name" : "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString" : "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT500to700   ={
"cmgComp":   cmgSampleComponents.QCD_HT500to700 ,
"dbsName" : cmgSampleComponents.QCD_HT500to700.dataset,
"name" : "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString" : "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}


QCD_HT700to1000   ={
"cmgComp":  cmgSampleComponents.QCD_HT700to1000  ,
"dbsName" : cmgSampleComponents.QCD_HT700to1000.dataset,
"name" : "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString" : "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT1000to1500   ={
"cmgComp": cmgSampleComponents.QCD_HT1000to1500   ,
"dbsName" : cmgSampleComponents.QCD_HT1000to1500.dataset,
"name" : "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString" : "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"rootFileLocation":"tree.root",
"dir": sample_path,
"treeName":"tree",
'isData':False
}

QCD_HT1500to2000   ={
"cmgComp":  cmgSampleComponents.QCD_HT1500to2000  ,
"dbsName" : cmgSampleComponents.QCD_HT1500to2000.dataset,
"name" : "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString" : "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT2000toInf   ={
"cmgComp":  cmgSampleComponents.QCD_HT2000toInf  ,
"dbsName" : cmgSampleComponents.QCD_HT2000toInf.dataset,
"name" : "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString" : "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

#### QCD Pt:


QCD_Pt15to30 ={
"cmgComp":cmgSampleComponents.QCD_Pt15to30,
"name" : "QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt15to30.name,
"chunkString":"QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt15to30.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt30to50 ={
"cmgComp":cmgSampleComponents.QCD_Pt30to50,
"name" : "QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt30to50.name,
"chunkString":"QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt30to50.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt50to80 ={
"cmgComp":cmgSampleComponents.QCD_Pt50to80,
"name" : "QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt50to80.name,
"chunkString":"QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt50to80.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt80to120 ={
"cmgComp":cmgSampleComponents.QCD_Pt80to120,
"name" : "QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt80to120.name,
"chunkString":"QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt80to120.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt120to170 ={
"cmgComp":cmgSampleComponents.QCD_Pt120to170,
"name" : "QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt120to170.name,
"chunkString":"QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt120to170.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt170to300 ={
"cmgComp":cmgSampleComponents.QCD_Pt170to300,
"name" : "QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt170to300.name,
"chunkString":"QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt170to300.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt300to470 ={
"cmgComp":cmgSampleComponents.QCD_Pt300to470,
"name" : "QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt300to470.name,
"chunkString":"QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt300to470.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt470to600 ={
"cmgComp":cmgSampleComponents.QCD_Pt470to600,
"name" : "QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt470to600.name,
"chunkString":"QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt470to600.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt600to800 ={
"cmgComp":cmgSampleComponents.QCD_Pt600to800,
"name" : "QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt600to800.name,
"chunkString":"QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt600to800.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt800to1000 ={
"cmgComp":cmgSampleComponents.QCD_Pt800to1000,
"name" : "QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt800to1000.name,
"chunkString":"QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt800to1000.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt1000to1400 ={
"cmgComp":cmgSampleComponents.QCD_Pt1000to1400,
"name" : "QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt1000to1400.name,
"chunkString":"QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt1000to1400.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt1400to1800 ={
"cmgComp":cmgSampleComponents.QCD_Pt1400to1800,
"name" : "QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt1400to1800.name,
"chunkString":"QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt1400to1800.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt1800to2400 ={
"cmgComp":cmgSampleComponents.QCD_Pt1800to2400,
"name" : "QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt1800to2400.name,
"chunkString":"QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt1800to2400.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt2400to3200 ={
"cmgComp":cmgSampleComponents.QCD_Pt2400to3200,
"name" : "QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt2400to3200.name,
"chunkString":"QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt2400to3200.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}



### QCD PT EM Enriched

QCD_Pt15to20_EMEnriched ={
"cmgComp":cmgSampleComponents.QCD_Pt15to20_EMEnriched,
"name" : "QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt15to20_EMEnriched.name,
"chunkString":"QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt15to20_EMEnriched.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt20to30_EMEnriched ={
"cmgComp":cmgSampleComponents.QCD_Pt20to30_EMEnriched,
"name" : "QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt20to30_EMEnriched.name,
"chunkString":"QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt20to30_EMEnriched.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt30to50_EMEnriched ={
"cmgComp":cmgSampleComponents.QCD_Pt30to50_EMEnriched,
"name" : "QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt30to50_EMEnriched.name,
"chunkString":"QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt30to50_EMEnriched.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt50to80_EMEnriched ={
"cmgComp":cmgSampleComponents.QCD_Pt50to80_EMEnriched,
"name" : "QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt50to80_EMEnriched.name,
"chunkString":"QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt50to80_EMEnriched.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt80to120_EMEnriched ={
"cmgComp":cmgSampleComponents.QCD_Pt80to120_EMEnriched,
"name" : "QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt80to120_EMEnriched.name,
"chunkString":"QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt80to120_EMEnriched.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt120to170_EMEnriched ={
"cmgComp":cmgSampleComponents.QCD_Pt120to170_EMEnriched,
"name" : "QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt120to170_EMEnriched.name,
"chunkString":"QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt120to170_EMEnriched.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt170to300_EMEnriched ={
"cmgComp":cmgSampleComponents.QCD_Pt170to300_EMEnriched,
"name" : "QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt170to300_EMEnriched.name,
"chunkString":"QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt170to300_EMEnriched.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


QCD_Pt300toInf_EMEnriched ={
"cmgComp":cmgSampleComponents.QCD_Pt300toInf_EMEnriched,
"name" : "QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.QCD_Pt300toInf_EMEnriched.name,
"chunkString":"QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.QCD_Pt300toInf_EMEnriched.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}

#sample_path2 = '/data/nrad/cmgTuples/7412pass2_mAODv2_v6/RunIISpring15MiniAODv2'



DYJetsToLL_M5to50_LO ={
"cmgComp":cmgSampleComponents.DYJetsToLL_M5to50_LO,
"name" : "DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.DYJetsToLL_M5to50_LO.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


DYJetsToNuNu_M50 ={
"cmgComp":cmgSampleComponents.DYJetsToNuNu_M50,
"name" : "DYJetsToNuNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"DYJetsToNuNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.DYJetsToNuNu_M50.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


DYJetsToLL_M5to50_HT100to200 ={
"cmgComp":cmgSampleComponents.DYJetsToLL_M5to50_HT100to200,
"name" : "DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.DYJetsToLL_M5to50_HT100to200.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


DYJetsToLL_M5to50_HT200to400 ={
"cmgComp":cmgSampleComponents.DYJetsToLL_M5to50_HT200to400,
"name" : "DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.DYJetsToLL_M5to50_HT200to400.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


DYJetsToLL_M5to50_HT400to600 ={
"cmgComp":cmgSampleComponents.DYJetsToLL_M5to50_HT400to600,
"name" : "DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.DYJetsToLL_M5to50_HT400to600.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


DYJetsToLL_M5to50_HT600toInf ={
"cmgComp":cmgSampleComponents.DYJetsToLL_M5to50_HT600toInf,
"name" : "DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.DYJetsToLL_M5to50_HT600toInf.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}

DYJetsToLL_M50_HT100to200 ={
"cmgComp":cmgSampleComponents.DYJetsToLL_M50_HT100to200,
"name" : "DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.DYJetsToLL_M50_HT100to200.name,
"chunkString":"DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.DYJetsToLL_M50_HT100to200.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


DYJetsToLL_M50_HT200to400 ={
"cmgComp":cmgSampleComponents.DYJetsToLL_M50_HT200to400,
"name" : "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.DYJetsToLL_M50_HT200to400.name,
"chunkString":"DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.DYJetsToLL_M50_HT200to400.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


DYJetsToLL_M50_HT400to600 ={
"cmgComp":cmgSampleComponents.DYJetsToLL_M50_HT400to600,
"name" : "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2",
#"name" : cmgSampleComponents.DYJetsToLL_M50_HT400to600.name,
"chunkString":"DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2",
"dir": sample_path,
"dbsName" : cmgSampleComponents.DYJetsToLL_M50_HT400to600.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}


DYJetsToLL_M50_HT600toInf ={
"cmgComp":cmgSampleComponents.DYJetsToLL_M50_HT600toInf,
"name" : "DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#"name" : cmgSampleComponents.DYJetsToLL_M50_HT600toInf.name,
"chunkString":"DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": sample_path,
"dbsName" : cmgSampleComponents.DYJetsToLL_M50_HT600toInf.dataset,
"rootFileLocation":"tree.root",
"treeName":"tree",
"isData":False
}





TTJets = [TTJets_LO, TTJets_LO_HT600to800, TTJets_LO_HT800to1200, TTJets_LO_HT1200to2500, TTJets_LO_HT2500toInf]
WJetsInc = [WJetsToLNu]
WJetsHT  = [
    WJetsToLNu_HT100to200, 
    WJetsToLNu_HT200to400, 
    WJetsToLNu_HT400to600, 
    WJetsToLNu_HT600toInf, 
    WJetsToLNu_HT600to800, 
    WJetsToLNu_HT800to1200, 
    WJetsToLNu_HT1200to2500 , 
    WJetsToLNu_HT2500toInf,
    ]

ZJetsHT  = [
    ZJetsToNuNu_HT100to200,
    ZJetsToNuNu_HT200to400,
    ZJetsToNuNu_HT400to600,
    ZJetsToNuNu_HT600toInf
    ]

QCDPT = [

    #QCD_Pt5to10,
    QCD_Pt15to30,
    QCD_Pt30to50,
    QCD_Pt50to80,
    QCD_Pt80to120,
    QCD_Pt120to170,
    QCD_Pt170to300,
    QCD_Pt300to470,
    QCD_Pt470to600,
    QCD_Pt600to800,
    QCD_Pt800to1000,
    QCD_Pt1000to1400,
    QCD_Pt1400to1800,
    QCD_Pt1800to2400,
    QCD_Pt2400to3200,
    #QCD_Pt3200toInf,

    ]

QCDPT_EM = [

    QCD_Pt15to20_EMEnriched,
    QCD_Pt20to30_EMEnriched,
    QCD_Pt30to50_EMEnriched,
    QCD_Pt50to80_EMEnriched,
    QCD_Pt80to120_EMEnriched,
    QCD_Pt120to170_EMEnriched,
    QCD_Pt170to300_EMEnriched,
    QCD_Pt300toInf_EMEnriched,

    ]

QCDHT = [

    QCD_HT200to300,
    QCD_HT300to500,
    QCD_HT500to700,
    QCD_HT700to1000,
    QCD_HT1000to1500,
    QCD_HT1500to2000,
    QCD_HT2000toInf,

    ]

DY=[
    DYJetsToLL_M5to50_LO,
    DYJetsToNuNu_M50 ,

    DYJetsToLL_M5to50_HT100to200,
    DYJetsToLL_M5to50_HT200to400,
    DYJetsToLL_M5to50_HT400to600,
    DYJetsToLL_M5to50_HT600toInf,


    DYJetsToLL_M50_HT100to200,
    DYJetsToLL_M50_HT200to400,
    DYJetsToLL_M50_HT400to600,
    DYJetsToLL_M50_HT600toInf,
    ]

samples = TTJets + WJetsInc + WJetsHT + ZJetsHT + QCDHT + QCDPT + QCDPT_EM + DY

for sample in samples:
#  print sample
  sample['xsec'] =   sample['cmgComp'].xSection
  sample['dir'] = sample['dir']+"/"+sample['name']


# signal samples

import CMGTools.RootTools.samples.samples_13TeV_signals as signals

signal_scan = [

        [ sample_path +"/",   "SMS-T2-4bd_mStop-100_mLSP-20to90_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",              "SMS_T2_4bd_mStop_100_mLSP_20to90",              signals.SMS_T2_4bd_mStop_100_mLSP_20to90               ],
        [ sample_path +"/",   "SMS-T2-4bd_mStop-125_mLSP-45to115_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",             "SMS_T2_4bd_mStop_125_mLSP_45to115",             signals.SMS_T2_4bd_mStop_125_mLSP_45to115              ],
        [ sample_path +"/",   "SMS-T2-4bd_mStop-150_mLSP-70to140_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",             "SMS_T2_4bd_mStop_150_mLSP_70to140",             signals.SMS_T2_4bd_mStop_150_mLSP_70to140              ],
        [ sample_path +"/",   "SMS-T2-4bd_mStop-175_mLSP-95to165_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",             "SMS_T2_4bd_mStop_175_mLSP_95to165",             signals.SMS_T2_4bd_mStop_175_mLSP_95to165              ],
        [ sample_path +"/",   "SMS-T2-4bd_mStop-200_mLSP-120to190_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",            "SMS_T2_4bd_mStop_200_mLSP_120to190",            signals.SMS_T2_4bd_mStop_200_mLSP_120to190             ],
        [ sample_path +"/",   "SMS-T2-4bd_mStop-225_mLSP-145to225_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",            "SMS_T2_4bd_mStop_225_mLSP_145to225",            signals.SMS_T2_4bd_mStop_225_mLSP_145to225             ],
        [ sample_path +"/",   "SMS-T2-4bd_mStop-250_mLSP-170to240_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",            "SMS_T2_4bd_mStop_250_mLSP_170to240",            signals.SMS_T2_4bd_mStop_250_mLSP_170to240             ],
        [ sample_path +"/",   "SMS-T2-4bd_mStop-275_mLSP-195to265_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",            "SMS_T2_4bd_mStop_275_mLSP_195to265",            signals.SMS_T2_4bd_mStop_275_mLSP_195to265             ],
        [ sample_path +"/",   "SMS-T2-4bd_mStop-300_mLSP-220to290_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",            "SMS_T2_4bd_mStop_300_mLSP_220to290",            signals.SMS_T2_4bd_mStop_300_mLSP_220to290             ],
        [ sample_path +"/",   "SMS-T2-4bd_mStop-325_mLSP-245to315_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",            "SMS_T2_4bd_mStop_325_mLSP_245to315",            signals.SMS_T2_4bd_mStop_325_mLSP_245to315             ],
        [ sample_path +"/",   "SMS-T2-4bd_mStop-350_mLSP-270to340_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",            "SMS_T2_4bd_mStop_350_mLSP_270to340",            signals.SMS_T2_4bd_mStop_350_mLSP_270to340             ],
        [ sample_path +"/",   "SMS-T2-4bd_mStop-375_mLSP-295to365_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",            "SMS_T2_4bd_mStop_375_mLSP_295to365",            signals.SMS_T2_4bd_mStop_375_mLSP_295to365             ],
        [ sample_path +"/",   "SMS-T2-4bd_mStop-400_mLSP-320to390_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",            "SMS_T2_4bd_mStop_400_mLSP_320to390",            signals.SMS_T2_4bd_mStop_400_mLSP_320to390             ],
        [ sample_path +"/",   "SMS-T2-4bd_mStop-425to475_mLSP-345to465_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",       "SMS_T2_4bd_mStop_425to475_mLSP_345to465",       signals.SMS_T2_4bd_mStop_425to475_mLSP_345to465         ],
        [ sample_path +"/",   "SMS-T2-4bd_mStop-500to550_mLSP-420to540_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",       "SMS_T2_4bd_mStop_500to550_mLSP_420to540",        signals.SMS_T2_4bd_mStop_500to550_mLSP_420to540         ],
        [ sample_path +"/",   "SMS-T2-4bd_mStop-550to600_mLSP-470to590_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",       "SMS_T2_4bd_mStop_550to600_mLSP_470to590",        signals.SMS_T2_4bd_mStop_550to600_mLSP_470to590         ],
        #[ sample_path +"/",   "SMS-T2mixed_mStop-100_mLSP-20to90_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",             "SMS_T2mixed_mStop_100_mLSP_20to90",             signals.SMS_T2mixed_mStop_100_mLSP_20to90             ],
        #[ sample_path +"/",   "SMS-T2mixed_mStop-125_mLSP-45to115_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",            "SMS_T2mixed_mStop_125_mLSP_45to115",            signals.SMS_T2mixed_mStop_125_mLSP_45to115            ],
        #[ sample_path +"/",   "SMS-T2mixed_mStop-275_mLSP-195to265_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1",           "SMS_T2mixed_mStop_275_mLSP_195to265",           signals.SMS_T2mixed_mStop_275_mLSP_195to265           ],



    ]         
         
         

import CMGTools.RootTools.samples.samples_13TeV_74X_susyT2DegStopPriv as signals_priv
allSignalData=[
    [
     sample_path+"T2DegStop_300_270_GEN-SIM/",
    "nrad-T2DegStop_300_270_MINIAODv2-RunIISpring15-MCRUN2_74_V9-25ns-4dc17ff0fe241c35c03aa547f2361414",
    "T2DegStop_300_270", 
    signals_priv.T2DegStop_300_270
    ],
    [
     sample_path+"T2DegStop_300_240_FastSim_v3/",
     "nrad-T2DegStop_300_240FS-eb69b0448a13fda070ca35fd76ab4e24" ,
     "T2DegStop_300_240_FastSim", 
     signals_priv.T2DegStop_300_240_FastSim 
     ],
    [
     sample_path+"T2DegStop_300_270_FastSim_v3/",
     "nrad-T2DegStop_300_270FS-eb69b0448a13fda070ca35fd76ab4e24",
     "T2DegStop_300_270_FastSim", 
     signals_priv.T2DegStop_300_270_FastSim 
     ],
    [
     sample_path+"T2DegStop_300_290_FastSim_v3/",
     "nrad-T2DegStop_300_290FS-eb69b0448a13fda070ca35fd76ab4e24" ,
     "T2DegStop_300_290_FastSim", 
     signals_priv.T2DegStop_300_290_FastSim
     ],
    [
     sample_path+"T2tt_stop300_LSP270/",
     "nrad-CMSSW_7_4_4_FastSim_PU25ns_MCRUN2_74_V9_7414_MINIAODv2-eb69b0448a13fda070ca35fd76ab4e24" ,
     "T2tt_300_270_FastSim", 
     signals_priv.T2tt_300_270_FastSim
     ],
    ]

allSignalData.extend(signal_scan)

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


samples.extend(allSignals)

















