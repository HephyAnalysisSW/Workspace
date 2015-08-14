import copy, os, sys
from Workspace.HEPHYPythonTools.helpers import getChunks

sampleDir="/afs/hephy.at/work/n/nrad/cmgTuples/withTracks/"


#WJetsToLNu_50ns={\
#"name" : "WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
#"chunkString" :"WJetsToLNu_50ns", 
#'dir': "/afs/hephy.at/work/n/nrad/cmgTuples/withTracks/_WJetsToLNu_50ns/Chunks/",
#'dbsName':'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
#"treeName":"treeProducerSusySingleLepton",
#"rootFileLocation":"treeProducerSusySingleLepton/tree.root",
#"skimAnalyzerDir":"skimAnalyzerCount",
#'isData':False
#}


WJetsToLNu={\
"name" : "WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"chunkString" :"WJetsToLNu", 
'dir': "/afs/hephy.at/work/n/nrad/cmgTuples/withTracks/WJetsToLNu/",
'dbsName':'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
"treeName":"treeProducerSusySingleLepton",
"rootFileLocation":"treeProducerSusySingleLepton/tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
'isData':False
}

#TTJets={\
#"name" : "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
#"chunkString":"TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
#"dir" : "/data/easilar/cmgTuples/crab_Spring15/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
#"dbsName" : "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
#"rootFileLocation":"tree.root",
#"treeName":"tree",
#'isData':False
#}




allSignalData=[\
#["/data/nrad/cmgTuples/dxy0fix/T2DegStop_300_270_miniIso/T2DegStop_300_270", "T2DegStop_300_270"],
#["/afs/hephy.at/work/n/nrad/cmgTuples/RunII/","T2DegStop_300_270"]
#["/data/nrad/cmgTuples/RunII/T2DegStop_300_270/","T2DegStop_300_270"]
[sampleDir+"T2DegStop_300_270","T2DegStop_300_270"]
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
      #"treeName":"treeProducerSusySingleLepton",
      "skimAnalyzerDir":"skimAnalyzerCount",
      }
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

allSignals=[]
for d,s in allSignalData:
  exec(s+"=getSignalSample('"+d+"','"+s+"')")
  allSignals.append(s)
  #exec("allSignals.append("+s+")")
