import copy, os, sys


data_ele={\
"name" : "SingleElectron_Run2015B",
"chunkString" : "SingleElectron_Run2015B",
'dir'  :"/data/easilar/cmgTuples/crab_Spring15/SingleElectron_Run2015B/",
}

data_mu={\
"name" : "SingleMuon_Run2015B",
"chunkString" : "SingleMuon_Run2015B",
'dir'  :"/data/easilar/cmgTuples/crab_Spring15/SingleMuon_Run2015B/",
}

data_doubleMu={\
"name" : "DoubleMuon_Run2015B",
"chunkString" : "DoubleMuon_Run2015B",
'dir'  :"/data/easilar/cmgTuples/crab_Spring15/DoubleMuon_Run2015B/",
}

data_doubleMu={\
"name" : "DoubleMuon_Run2015B",
"chunkString" : "DoubleMuon_Run2015B",
'dir' : "/data/easilar/cmgTuples/",
}

DYJetsToLL_M_50={\
"name" : "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"chunkString" : "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
'dir':"/data/easilar/cmgTuples/crab_Spring15/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
'dbsName':'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-AsymptFlat10to50bx25Raw_MCRUN2_74_V9-v1'
}

WJetsToLNu_HT100to200={\
"name" : "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"chunkString" :"WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 
'dir':'/data/easilar/cmgTuples/crab_Spring15/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'dbsName':'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
}

WJetsToLNu_HT200to400={\
"name" : "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"chunkString" :"WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 
'dir':'/data/easilar/cmgTuples/crab_Spring15/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'dbsName':'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
}

WJetsToLNu_HT400to600={\
"name" : "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"chunkString" :"WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 
'dir':'/data/easilar/cmgTuples/crab_Spring15/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'dbsName':'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
}

WJetsToLNu_HT600toInf={\
"name" : "WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"chunkString" :"WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 
'dir':'/data/easilar/cmgTuples/crab_Spring15/WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'dbsName':'WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
}


