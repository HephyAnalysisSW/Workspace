import copy, os, sys

data_path = '/afs/hephy.at/data/easilar01/Moriond2017/cmgTuples/data/'

singleElectron_samples = [\
                        "SingleElectron_Run2016B",\
                        "SingleElectron_Run2016C",\
                        "SingleElectron_Run2016D",\
                        "SingleElectron_Run2016E",\
                        "SingleElectron_Run2016F",\
                        "SingleElectron_Run2016G",\
                        "SingleElectron_Run2016H_v2",\
                        "SingleElectron_Run2016H_v3"\
                        ]

singleMuon_samples = [\
                        "SingleMuon_Run2016B",\
                        "SingleMuon_Run2016C",\
                        "SingleMuon_Run2016D",\
                        "SingleMuon_Run2016E",\
                        "SingleMuon_Run2016F",\
                        "SingleMuon_Run2016G",\
                        "SingleMuon_Run2016H_v2",\
                        "SingleMuon_Run2016H_v3"\
                        ]

MET_samples = [\
                        "MET_Run2016B",\
                        "MET_Run2016C",\
                        "MET_Run2016D",\
                        "MET_Run2016E",\
                        "MET_Run2016F",\
                        "MET_Run2016G",\
                        "MET_Run2016H_v2",\
                        "MET_Run2016H_v3"\
                        ]


allSamples_Data = singleElectron_samples+singleMuon_samples+MET_samples


for s in allSamples_Data:
  exec(s+'={"name":s,"chunkString":s,"rootFileLocation":"treeProducerSusySingleLepton/tree.root","skimAnalyzerDir":"skimAnalyzerCount",\
            "treeName":"tree",\
            "isData":True,\
            "dir":"/".join([data_path,s.split("_")[0]]),\
            }')

create_run_file = False
if create_run_file :
  for s in allSamples_Data:
    print 'python cmgPostProcessing.py --overwrite  --skim=""  --samples='+s

