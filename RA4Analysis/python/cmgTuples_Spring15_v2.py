import copy, os, sys

navid_path = "/data/nrad/cmgTuples/RunII/Spring15_v1/"
ece_path = "/data/easilar/cmgTuples/crab_Spring15/Summer15_25nsV2_MC/"

TTJets={\
"chunkString" : "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"name" : "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
'dir' : navid_path+"/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/", 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}


DY_HT200to400={\
"chunkString" : "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"name" : "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
'dir' : navid_path+"/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/", 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

DY_HT400to600={\
"chunkString" : "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"name" : "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
'dir' : navid_path+"/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/", 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}
DY_HT600toInf={\
"chunkString" : "DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"name" : "DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
'dir' : navid_path+"/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/", 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

T_tWch={\
"chunkString" : "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"name" : "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
'dir' : navid_path+"/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/", 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

TBar_tWch={\
"chunkString" : "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
"name" : "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test",
'dir' : navid_path+"/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test/", 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

TToLeptons_tch={\
"chunkString" : "ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"name" : "ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
'dir' : navid_path+"/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/", 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJets={\
"chunkString" : "WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"name" : "WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
'dir' : navid_path+"/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/", 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

#QCD_HT100to200={\
#"name" : "QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
#"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
#'dir' : "/tmp/easilar/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx/",
#"rootFileLocation":"tree.root",
#"treeName":"tree",
#'isData':False
#}

QCD_HT200to300={\
#"name" : "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
'dir' : ece_path+"/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT300to500={\
#"name" : "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
'dir' : ece_path+"/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT500to700={\
#"name" : "/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
'dir' : ece_path+"/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT700to1000={\
#"name" : "/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
'dir' : ece_path+"/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT1000to1500={\
#"name" : "/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
'dir' : ece_path+"/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT1500to2000={\
#"name" : "/QCD_HT1000to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
'dir' : ece_path+"/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT2000toInf={\
#"name" : "/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
'dir' : ece_path+"/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}


