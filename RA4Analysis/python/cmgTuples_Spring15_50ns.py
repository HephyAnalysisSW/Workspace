import copy, os, sys

data_path = "/data/easilar/cmgTuples/crab_Spring15/Summer15_50nsV4_Data/"
print data_path

data_mu_50ns={\
"name" : "cmgTuples_SingleMuon_Run2015B-PromptReco-v1_Summer15_50nsV4_lumi",
"chunkString" : "cmgTuples_SingleMuon_Run2015B-PromptReco-v1_Summer15_50nsV4_lumi",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"",
"treeName":"tree",
'isData':True,
'dir' : data_path+"/SingleMuon_Run2015B-PromptReco-v1/"
}
data_ele_50ns={\
"name" : "cmgTuples_SingleElectron_Run2015B-PromptReco-v1_Summer15_50nsV4_lumi",
"chunkString" : "cmgTuples_SingleElectron_Run2015B-PromptReco-v1_Summer15_50nsV4_lumi",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"",
"treeName":"tree",
'isData':True,
'dir' : data_path+"/SingleElectron_Run2015B-PromptReco-v1/"
}

data_mu_17July_50ns={\
"name" : "cmgTuples_SingleMuon_Run2015B-17Jul2015-v1_Summer15_50nsV4_lumi2",
"chunkString" : "cmgTuples_SingleMuon_Run2015B-17Jul2015-v1_Summer15_50nsV4_lumi2",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"",
"treeName":"tree",
'isData':True,
'dir' : data_path+"/SingleMuon_Run2015B-17Jul2015-v1"
}

data_ele_17July_50ns={\
"name" : "cmgTuples_SingleElectron_Run2015B-17Jul2015-v1_Summer15_50nsV4_lumi2",
"chunkString" : "cmgTuples_SingleElectron_Run2015B-17Jul2015-v1_Summer15_50nsV4_lumi2",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"",
"treeName":"tree",
'isData':True,
'dir' : data_path+"/SingleElectron_Run2015B-17Jul2015-v1/"
}

TTJets_50ns={\
"name" : "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"chunkString":"TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/Chunks/",
"dbsName" : "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

DYJetsToLL_M_10to50_50ns={\
'name' : "DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
'chunkString' : "DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
'dir':"/data/nrad/cmgTuples/RunII/Spring15_v1/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/",
'dbsName':'/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

DYJetsToLL_M_50_HT100to200_50ns={\
"name" : "DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
"chunkString" : "DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1",
'dir':"/data/nrad/cmgTuples/RunII/Spring15_v1/",
'dbsName':'/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

DYJetsToLL_M_50_HT200to400_50ns={\
"name" : "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"chunkString" : "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
'dir':"/data/nrad/cmgTuples/RunII/Spring15_v1/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/",
'dbsName':'/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

DYJetsToLL_M_50_HT400to600_50ns={\
"name" : "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"chunkString" : "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
'dir':"/data/nrad/cmgTuples/RunII/Spring15_v1/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/",
'dbsName':'/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

DYJetsToLL_M_50_HT600toInf_50ns={\
"name" : "DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"chunkString" : "DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
'dir':"/data/nrad/cmgTuples/RunII/Spring15_v1/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/",
'dbsName':'/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_50ns={\
"name" : "WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"chunkString" :"WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
'dir':'/data/nrad/cmgTuples/RunII/Spring15_v1/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/',
'dbsName':'/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM',
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

TToLeptons_tch_50ns={\
"name" : "ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"chunkString":"ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/",
"dbsName" : "/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

TBar_tWch_50ns={\
"name" : "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"chunkString":"ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test/",
"dbsName" : "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

T_tWch_50ns={\
"name" : "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"chunkString":"ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/",
"dbsName" : "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt15to20_50ns={\
"name" : "QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3_test",
"chunkString":"QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3_test/",
"dbsName" : "/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt20to30_50ns={\
"name" : "QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"chunkString":"QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test/",
"dbsName" : "/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt30to50_50ns={\
"name" : "QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"chunkString":"QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/",
"dbsName" : "/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt50to80_50ns={\
"name" : "QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"chunkString":"QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/",
"dbsName" : "/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt80to120_50ns={\
"name" : "QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"chunkString":"QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/",
"dbsName" : "/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt120to170_50ns={\
"name" : "QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"chunkString":"QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/",
"dbsName" : "/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt170to300_50ns={\
"name" : "QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"chunkString":"QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test/",
"dbsName" : "/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt300to470_50ns={\
"name" : "QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3_test",
"chunkString":"QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3_test/",
"dbsName" : "/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt470to600_50ns={\
"name" : "QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3_test",
"chunkString":"QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3_test/",
"dbsName" : "/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt600to800_50ns={\
"name" : "QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"chunkString":"QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test/",
"dbsName" : "/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt800to1000_50ns={\
"name" : "QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"chunkString":"QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test/",
"dbsName" : "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_MuEnriched_Pt1000toInf_50ns={\
"name" : "QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"chunkString":"QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test/",
"dbsName" : "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WZ_50ns={\
"name" : "WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"chunkString":"WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test/",
"dbsName" : "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WWTo2L2Nu_50ns={\
"name" : "WWTo2L2Nu_13TeV-powheg_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"chunkString":"WWTo2L2Nu_13TeV-powheg_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/WWTo2L2Nu_13TeV-powheg_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test/",
"dbsName" : "/WWTo2L2Nu_13TeV-powheg/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

ZZ_50ns={\
"name" : "ZZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"chunkString":"ZZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"dir" : "/data/nrad/cmgTuples/RunII/Spring15_v1/ZZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test/",
"dbsName" : "/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

