from CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 import *

# temporary solution for CMG components and cross-section of signal or samples not in the CMG sample file
import PhysicsTools.HeppyCore.framework.config as cfg
from Workspace.HEPHYPythonTools.xsec import xsec

data_path = "/data/nrad/cmgTuples/RunII/7412pass2/RunIISpring15MiniAODv2"


TTJets_LO = {\
"cmgComp":TTJets_LO,
"name" : "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": data_path ,
"dbsName" : TTJets_LO.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False,
}

TTJets_LO_HT600to800 ={\
"cmgComp":TTJets_LO_HT600to800,
"name": "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"chunkString": "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"dir": data_path ,
"dbsName" : TTJets_LO_HT600to800.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False,
}

TTJets_LO_HT800to1200 ={\
"cmgComp":TTJets_LO_HT800to1200,
"name" : "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"chunkString":"TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"dir": data_path,
"dbsName" : TTJets_LO_HT800to1200.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False,
}
TTJets_LO_HT1200to2500 ={\
"cmgComp":TTJets_LO_HT1200to2500,
"name" : "TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"chunkString":"TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"dir": data_path,
"dbsName" : TTJets_LO_HT1200to2500.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False,
}
TTJets_LO_HT2500toInf ={\
"cmgComp":TTJets_LO_HT2500toInf,
"name" : "TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"chunkString":"TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"dir": data_path,
"dbsName" : TTJets_LO_HT2500toInf.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}


WJetsToLNu ={\
"cmgComp":WJetsToLNu,
"name" : "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"chunkString":"WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"dir": data_path,
"dbsName" : WJetsToLNu.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT100to200 ={\
"cmgComp":WJetsToLNu_HT100to200,
"name" : "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"chunkString":"WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"dir": data_path,
"dbsName" : WJetsToLNu_HT100to200.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT200to400 ={\
"cmgComp":WJetsToLNu_HT200to400,
"name" : "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"chunkString":"WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"dir": data_path,
"dbsName" : WJetsToLNu_HT200to400.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT400to600 ={\
"cmgComp":WJetsToLNu_HT400to600,
"name" : "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"chunkString":"WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"dir": data_path,
"dbsName" : WJetsToLNu_HT400to600.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT600toInf ={\
"cmgComp":WJetsToLNu_HT600toInf,
"name" : "WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": data_path,
'dbsName':'/WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM',
"dbsName" : WJetsToLNu_HT600toInf.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT600to800 ={\
"cmgComp":WJetsToLNu_HT600to800,
"name" : "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"chunkString":"WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"dir": data_path,
"dbsName" : WJetsToLNu_HT600to800.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT800to1200 ={\
"cmgComp":WJetsToLNu_HT800to1200,
"name" : "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"chunkString":"WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"dir": data_path,
"dbsName" : WJetsToLNu_HT800to1200.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}


WJetsToLNu_HT1200to2500 ={\
"cmgComp":WJetsToLNu_HT1200to2500,
"name" : "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"chunkString":"WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2",
"dir": data_path,
"dbsName" : WJetsToLNu_HT1200to2500.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJetsToLNu_HT2500toInf ={\
"cmgComp":WJetsToLNu_HT2500toInf,
"name" : "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"chunkString":"WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
"dir": data_path,
"dbsName" : WJetsToLNu_HT2500toInf.dataset, 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}


TTJets = [TTJets_LO, TTJets_LO_HT600to800, TTJets_LO_HT800to1200, TTJets_LO_HT1200to2500, TTJets_LO_HT2500toInf]
WJetsInc = [WJetsToLNu]
WJetsHT  = [WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf, WJetsToLNu_HT600to800, WJetsToLNu_HT800to1200, WJetsToLNu_HT1200to2500 , WJetsToLNu_HT2500toInf]

samples = TTJets + WJetsInc + WJetsHT

for sample in samples:
#  print sample
  sample['xsec'] =   sample['cmgComp'].xSection
  sample['dir'] = sample['dir']+"/"+sample['name']


# signal samples

allSignalData=[
    [data_path+"/T2DegStop_300_270","T2DegStop_300_270"]
    ]


allSignalStrings = [s[1] for s in allSignalData]
def getSignalSample(dir, signal):
  if signal in allSignalStrings:
     
    # dirty way of creating a CMG component        
    component = cfg.MCComponent(
        dataset=signal,
        name = signal,
        files = [],
        xSection = 0.0,
        nGenEvents = 1,
        triggers = [],
        effCorrFactor = 1,
        )
      
    return {\
      'cmgComp': component,
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
  
for sample in allSignals:
    sample['xsec'] = xsec[sample['dbsName']]
    sample['cmgComp'].xSection = xsec[sample['dbsName']]


