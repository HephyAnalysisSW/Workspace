import copy, os, sys

data_path = "/data/rschoefbeck/cmgTuples/Spring15/MC50ns_1l/"

TTJets_50ns={\
"name" : "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString":"TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"dbsName" : "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

DYJetsToLL_M_10to50_50ns={\
'name' : "DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
'chunkString' : "DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
'dir':data_path,
'dbsName':'/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

DYJetsToLL_M_50_50ns={\
"name" : "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"chunkString" : "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
'dir':data_path,
'dbsName':'/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

DYJetsToLL_M_50_HT100to200_50ns={\
"name" : "DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString" : "DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
'dir':data_path,
'dbsName':'/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

DYJetsToLL_M_50_HT200to400_50ns={\
"name" : "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString" : "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
'dir':data_path,
'dbsName':'/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

DYJetsToLL_M_50_HT400to600_50ns={\
"name" : "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString" : "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
'dir':data_path,
'dbsName':'/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

DYJetsToLL_M_50_HT600toInf_50ns={\
"name" : "DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString" : "DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
'dir':data_path,
'dbsName':'/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_50ns={\
"name" : "WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString" :"WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
'dir':data_path,
'dbsName':'/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

TToLeptons_tch_50ns={\
"name" : "ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString":"ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"dbsName" : "/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

TBar_tWch_50ns={\
"name" : "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"chunkString":"ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"dir" : data_path,
"dbsName" : "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

T_tWch_50ns={\
"name" : "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString":"ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"dbsName" : "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt15to20_50ns={\
"name" : "QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3",
"chunkString":"QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3",
"dir" : data_path,
"dbsName" : "/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt20to30_50ns={\
"name" : "QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"chunkString":"QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"dir" : data_path,
"dbsName" : "/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt30to50_50ns={\
"name" : "QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString":"QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"dbsName" : "/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt50to80_50ns={\
"name" : "QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString":"QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"dbsName" : "/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt80to120_50ns={\
"name" : "QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString":"QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"dbsName" : "/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt120to170_50ns={\
"name" : "QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString":"QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"dbsName" : "/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt170to300_50ns={\
"name" : "QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"chunkString":"QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"dir" : data_path,
"dbsName" : "/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt300to470_50ns={\
"name" : "QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3",
"chunkString":"QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3",
"dir" : data_path,
"dbsName" : "/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt470to600_50ns={\
"name" : "QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3",
"chunkString":"QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3",
"dir" : data_path,
"dbsName" : "/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt600to800_50ns={\
"name" : "QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"chunkString":"QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"dir" : data_path,
"dbsName" : "/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt800to1000_50ns={\
"name" : "QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"chunkString":"QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"dir" : data_path,
"dbsName" : "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt1000toInf_50ns={\
"name" : "QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"chunkString":"QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"dbsName" : "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt_10to15={
"dbsName":     "/QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"name":        "QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString": "QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt_15to30_50ns={
"dbsName":     "/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"name":        "QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString": "QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt_30to50_50ns={
"dbsName":     "/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"name":        "QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"chunkString": "QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt_50to80_50ns={
"dbsName":     "/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"name":        "QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString": "QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt_80to120_50ns={
"dbsName":     "/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"name":        "QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString": "QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt_120to170_50ns={
"dbsName":     "/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"name":        "QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString": "QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt_170to300_50ns={
"name":        "QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"chunkString": "QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"dbsName":     "/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt_300to470_50ns={
"dbsName":     "/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"name":        "QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString": "QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt_470to600_50ns={
"dbsName":     "/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"name":        "QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"chunkString": "QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt_600to800_50ns={
"dbsName":     "/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"name":        "QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"chunkString": "QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt_800to1000_50ns={
"dbsName":     "/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"name":        "QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"chunkString": "QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt_1000to1400_50ns={
"dbsName":     "/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"name":        "QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"chunkString": "QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt_1400to1800_50ns={
"dbsName":     "/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"name":        "QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString": "QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt_1800to2400_50ns={
"dbsName":     "/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"name":        "QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString": "QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt_2400to3200_50ns={
"dbsName":     "/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"name":        "QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString": "QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt_3200toInf_50ns={
"dbsName":     "/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"name":        "QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString": "QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"dir" : data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}


WZ_50ns={\
"name" : "WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"chunkString":"WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"dir" : data_path,
"dbsName" : "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WWTo2L2Nu_50ns={\
"name" : "WWTo2L2Nu_13TeV-powheg_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"chunkString":"WWTo2L2Nu_13TeV-powheg_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"dir" : data_path,
"dbsName" : "/WWTo2L2Nu_13TeV-powheg/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

ZZ_50ns={\
"name" : "ZZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"chunkString":"ZZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2",
"dir" : data_path,
"dbsName" : "/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

allSamples_Spring15_50ns = [TTJets_50ns, DYJetsToLL_M_10to50_50ns, DYJetsToLL_M_50_HT100to200_50ns, DYJetsToLL_M_50_HT200to400_50ns, DYJetsToLL_M_50_HT400to600_50ns, DYJetsToLL_M_50_HT600toInf_50ns, WJetsToLNu_50ns, TToLeptons_tch_50ns, TBar_tWch_50ns, T_tWch_50ns, QCD_MuEnriched_Pt15to20_50ns, QCD_MuEnriched_Pt20to30_50ns, QCD_MuEnriched_Pt30to50_50ns, QCD_MuEnriched_Pt50to80_50ns, QCD_MuEnriched_Pt80to120_50ns, QCD_MuEnriched_Pt120to170_50ns, QCD_MuEnriched_Pt170to300_50ns, QCD_MuEnriched_Pt300to470_50ns, QCD_MuEnriched_Pt470to600_50ns, QCD_MuEnriched_Pt600to800_50ns, QCD_MuEnriched_Pt800to1000_50ns, QCD_MuEnriched_Pt1000toInf_50ns, WZ_50ns, WWTo2L2Nu_50ns, ZZ_50ns, ]
