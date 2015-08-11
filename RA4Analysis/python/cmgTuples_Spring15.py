import copy, os, sys


data_ele={\
"name" : "SingleElectron_Run2015B",
"chunkString" : "SingleElectron_Run2015B",
'dir'  :"/data/easilar/cmgTuples/crab_Spring15/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':True
}

data_mu={\
"name" : "SingleMuon_Run2015B",
"chunkString" : "SingleMuon_Run2015B",
'dir'  :"/data/easilar/cmgTuples/crab_Spring15/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':True
}

data_doubleMu={\
"name" : "DoubleMuon_Run2015B",
"chunkString" : "DoubleMuon_Run2015B",
'dir'  :"/data/easilar/cmgTuples/crab_Spring15/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':True
}

data_doubleMu={\
"name" : "DoubleMuon_Run2015B",
"chunkString" : "DoubleMuon_Run2015B",
'dir' : "/data/easilar/cmgTuples/",
}

DYJetsToLL_M_50_25ns={\
"name" : "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3_MC25ns",
'dir':"/data/nrad/cmgTuples/Spring15_v0/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3_MC25ns",
'dbsName':'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

DYJetsToLL_M_50={\
"name" : "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"chunkString" : "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
'dir':"/data/easilar/cmgTuples/crab_Spring15/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
'dbsName':'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-AsymptFlat10to50bx25Raw_MCRUN2_74_V9-v1',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT100to200={\
"name" : "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"chunkString" :"WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 
'dir':'/data/easilar/cmgTuples/crab_Spring15/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'dbsName':'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT200to400={\
"name" : "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"chunkString" :"WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 
'dir':'/data/easilar/cmgTuples/crab_Spring15/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'dbsName':'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT400to600={\
"name" : "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"chunkString" :"WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 
'dir':'/data/easilar/cmgTuples/crab_Spring15/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'dbsName':'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT600toInf={\
"name" : "WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"chunkString" :"WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 
'dir':'/data/easilar/cmgTuples/crab_Spring15/WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'dbsName':'WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

TToLeptons_sch={\
"name" : "ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
"chunkString":"ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
"dir" : "/data/easilar/cmgTuples/crab_Spring15/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
"dbsName" : "ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

TToLeptons_tch={\
"name" : "ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
"chunkString":"ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
"dir" : "/data/easilar/cmgTuples/crab_Spring15/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
"dbsName" : "ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

TBar_tWch={\
"name" : "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
"chunkString":"ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
"dir" : "/data/easilar/cmgTuples/crab_Spring15/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
"dbsName" : "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

T_tWch={\
"name" : "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
"chunkString":"ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
"dir" : "/data/easilar/cmgTuples/crab_Spring15/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
"dbsName" : "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

TTJets={\
"name" : "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"chunkString":"TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"dir" : "/data/easilar/cmgTuples/crab_Spring15/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"dbsName" : "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_Pt10to15_50ns={\
"name" : "QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8",
"chunkString" :"QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8",
'dir':'/data/easilar/cmgTuples/crab_Spring15/',
'dbsName':'/QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt15to30_50ns={\
"name" : "QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8",
"chunkString" :"QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8",
'dir':'/data/easilar/cmgTuples/crab_Spring15/',
'dbsName':'/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt30to50_50ns={\
"name" : "QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8",
"chunkString" :"QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8",
'dir':'/data/easilar/cmgTuples/crab_Spring15/',
'dbsName':'/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt50to80_50ns={\
"name" : "QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8",
"chunkString" :"QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8",
'dir':'/data/easilar/cmgTuples/crab_Spring15/',
'dbsName':'/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt80to120_50ns={\
"name" : "QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8",
"chunkString" :"QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8",
'dir':'/data/easilar/cmgTuples/crab_Spring15/',
'dbsName':'/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt120to170_50ns={\
"name" : "QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8",
"chunkString" :"QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8",
'dir':'/data/easilar/cmgTuples/crab_Spring15/',
'dbsName':'/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt170to300_50ns={\
"name" : "QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8",
"chunkString" :"QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8",
'dir':'/data/easilar/cmgTuples/crab_Spring15/',
'dbsName':'/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt300to470_50ns={\
"name" : "QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8",
"chunkString" :"QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8",
'dir':'/data/easilar/cmgTuples/crab_Spring15/',
'dbsName':'/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt470to600_50ns={\
"name" : "QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8",
"chunkString" :"QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8",
'dir':'/data/easilar/cmgTuples/crab_Spring15/',
'dbsName':'/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt600to800_50ns={\
"name" : "QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8",
"chunkString" :"QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8",
'dir':'/data/easilar/cmgTuples/crab_Spring15/',
'dbsName':'/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt800to1000_50ns={\
"name" : "QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8",
"chunkString" :"QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8",
'dir':'/data/easilar/cmgTuples/crab_Spring15/',
'dbsName':'/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt1000to1400_50ns={\
"name" : "QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8",
"chunkString" :"QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8",
'dir':'/data/easilar/cmgTuples/crab_Spring15/',
'dbsName':'/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt1400to1800_50ns={\
"name" : "QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8",
"chunkString" :"QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8",
'dir':'/data/easilar/cmgTuples/crab_Spring15/',
'dbsName':'/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt1800to2400_50ns={\
"name" : "QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8",
"chunkString" :"QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8",
'dir':'/data/easilar/cmgTuples/crab_Spring15/',
'dbsName':'/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt2400to3200_50ns={\
"name" : "QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8",
"chunkString" :"QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8",
'dir':'/data/easilar/cmgTuples/crab_Spring15/',
'dbsName':'/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
QCD_Pt3200toInf_25ns ={\
"name" : "QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8",
"chunkString" :"QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8",
'dir':'/data/easilar/cmgTuples/crab_Spring15/',
'dbsName':'/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
