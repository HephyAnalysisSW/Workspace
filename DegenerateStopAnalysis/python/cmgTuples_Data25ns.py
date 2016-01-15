#data_path = "/data/nrad/cmgTuples/RunII/7412pass2/Data25ns" 
from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import *

# temporary solution for CMG components and cross-section of signal or samples not in the CMG sample file
import PhysicsTools.HeppyCore.framework.config as cfg


data_path = "/data/nrad/cmgTuples/RunII/7412pass2_v4/Data25ns_Run2015D_Nov13Json/"


SingleMuon_Run2015D_v4 ={\
"cmgComp":SingleMuon_Run2015D_Promptv4,
"chunkString":"SingleMuon_Run2015D-05Oct2015-v1",
"name" : "SingleMuon_Run2015D-PromptReco-v4",
"dir": data_path,
"rootFileLocation":"/tree.root",
"treeName":"tree",
'isData':True,
}

SingleMuon_Run2015D_05Oct ={\
"cmgComp":SingleMuon_Run2015D_05Oct,
"chunkString":"SingleMuon_Run2015D-05Oct2015-v1",
"name" : "SingleMuon_Run2015D-05Oct2015-v1",
"dir": data_path,
"rootFileLocation":"/tree.root",
"treeName":"tree",
'isData':True,
}

SingleElectron_Run2015D_v4 ={\
"cmgComp":  SingleElectron_Run2015D_Promptv4   ,
"chunkString":"SingleElectron_Run2015D-PromptReco-v4",
"name" : "SingleElectron_Run2015D-PromptReco-v4",
"dir": data_path,
"rootFileLocation":"/tree.root",
"treeName":"tree",
'isData':True,
}
SingleElectron_Run2015D_05Oct ={\
"cmgComp":  SingleElectron_Run2015D_05Oct   ,
"chunkString":"SingleElectron_Run2015D-05Oct2015-v1",
"name" : "SingleElectron_Run2015D-05Oct2015-v1",
"dir": data_path,
"rootFileLocation":"/tree.root",
"treeName":"tree",
'isData':True,
}
MET_Run2015D_v4 ={\
"cmgComp":  MET_Run2015D_Promptv4   ,
"chunkString":"MET_Run2015D-PromptReco-v4",
"name" : "MET_Run2015D-PromptReco-v4",
"dir": data_path,
"rootFileLocation":"/tree.root",
"treeName":"tree",
'isData':True,
}
MET_Run2015D_05Oct ={\
"cmgComp":  MET_Run2015D_05Oct   ,
"chunkString":"MET_Run2015D-05Oct2015-v1",
"name" : "MET_Run2015D-05Oct2015-v1",
"dir": data_path,
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':True,
}


samples = [MET_Run2015D_05Oct, MET_Run2015D_v4, SingleElectron_Run2015D_05Oct, SingleElectron_Run2015D_v4, SingleMuon_Run2015D_05Oct, SingleMuon_Run2015D_v4]

for sample in samples:
  sample['dir'] = sample['dir']+"/"+sample['name']







