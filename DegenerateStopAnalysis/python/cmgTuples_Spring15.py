import copy, os, sys

sampleDir="/data/nrad/cmgTuples/crab_cmg_v3/"

#data_ele={\
#"name" : "SingleElectron_Run2015B",
#"chunkString" : "SingleElectron_Run2015B",
#'dir'  :"/data/easilar/cmgTuples/crab_Spring15/",
#"rootFileLocation":"tree.root",
#"treeName":"tree",
#'isData':True
#}
#
#data_mu={\
#"name" : "SingleMuon_Run2015B",
#"chunkString" : "SingleMuon_Run2015B",
#'dir'  :"/data/easilar/cmgTuples/crab_Spring15/",
#"rootFileLocation":"tree.root",
#"treeName":"tree",
#'isData':True
#}
#
#data_doubleMu={\
#"name" : "DoubleMuon_Run2015B",
#"chunkString" : "DoubleMuon_Run2015B",
#'dir'  :"/data/easilar/cmgTuples/crab_Spring15/",
#"rootFileLocation":"tree.root",
#"treeName":"tree",
#'isData':True
#}
#
#data_doubleMu={\
#"name" : "DoubleMuon_Run2015B",
#"chunkString" : "DoubleMuon_Run2015B",
#'dir' : "/data/easilar/cmgTuples/",
#}
#
#DYJetsToLL_M_50={\
#"name" : "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
#"chunkString" : "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
#'dir':"/data/easilar/cmgTuples/crab_Spring15/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
#'dbsName':'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-AsymptFlat10to50bx25Raw_MCRUN2_74_V9-v1',
#"rootFileLocation":"tree.root",
#"treeName":"tree",
#'isData':False
#}

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


TTJets={\
"name" : "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"chunkString":"TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"dir" : "/data/easilar/cmgTuples/crab_Spring15/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"dbsName" : "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}




allSignalData=[\
#["/data/nrad/cmgTuples/dxy0fix/T2DegStop_300_270_miniIso/T2DegStop_300_270", "T2DegStop_300_270"],
#["/afs/hephy.at/work/n/nrad/cmgTuples/RunII/","T2DegStop_300_270"]
["/data/nrad/cmgTuples/RunII/T2DegStop_300_270/","T2DegStop_300_270"]
]


allSignalStrings = [s[1] for s in allSignalData]
def getSignalSample(dir, signal):
  if signal in allSignalStrings:
    return {\
      "name" : signal,
      "chunkString": signal,
      'dir' : dir,
      'dbsName':signal,
      'isData':False,
      "rootFileLocation":"treeProducerSusySingleLepton/tree.root",
      "treeName":"tree",
      "skimAnalyzerDir":"skimAnalyzerCount",
      }
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

allSignals=[]
for d,s in allSignalData:
  exec(s+"=getSignalSample('"+d+"','"+s+"')")
  exec("allSignals.append("+s+")")
