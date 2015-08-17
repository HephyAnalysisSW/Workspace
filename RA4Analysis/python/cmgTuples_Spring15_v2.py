import copy, os, sys


#artur_path = "/afs/cern.ch/work/e/easilar/Aug06_GoldenJSON/"
artur_path = "/afs/cern.ch/work/e/easilar/data/data_from_Artur_newMET_13Aug/Aug12_GoldenJson_METnoHF/"

navid_path = "/data/nrad/cmgTuples/RunII/Spring15_v1/"

data_ele={\
"name" : "SingleElectron_Run2015B",
"chunkString" : "SingleElectron_Run2015B",
"rootFileLocation":"/treeProducerSusySingleLepton/tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
'isData':True,
'dir' : artur_path+"/"
}

data_mu={\
"name" : "SingleMuon_Run2015B",
"chunkString" : "SingleMuon_Run2015B",
"rootFileLocation":"/treeProducerSusySingleLepton/tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
'isData':True,
'dir' : artur_path+"/"
}


data_ele_17July={\
"name" : "SingleElectron_Run2015B_17Jul",
"chunkString" : "SingleElectron_Run2015B_17Jul",
"rootFileLocation":"/treeProducerSusySingleLepton/tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
'isData':True,
'dir' : artur_path+"/"
}

data_mu_17July={\
"name" : "SingleMuon_Run2015B_17Jul",
"chunkString" : "SingleMuon_Run2015B_17Jul",
"rootFileLocation":"/treeProducerSusySingleLepton/tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
'isData':True,
'dir' : artur_path+"/"
}
################

TTJets={\
"chunkString" : "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
"name" : "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test",
'dir' : navid_path+"/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test/", 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

#DY={\
##"name" : "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
#"chunkString" : "RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_plzworkheplx",
#"name" : "RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_plzworkheplx",
##'dir' : "/tmp/easilar/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_plzworkheplx/", 
#'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8//", 
#"rootFileLocation":"tree.root",
#"treeName":"tree",
#'isData':False
#}

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
'''
QCD_HT200to300={\
#"name" : "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT300to500={\
#"name" : "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT500to700={\
#"name" : "/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT700to1000={\
#"name" : "/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT1000to1500={\
#"name" : "/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT1500to2000={\
#"name" : "/QCD_HT1000to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT2000toInf={\
#"name" : "/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

#print QCD_HT500to700
'''

