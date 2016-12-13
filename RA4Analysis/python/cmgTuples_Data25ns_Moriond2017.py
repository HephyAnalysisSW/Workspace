import copy, os, sys

data_path = '/afs/hephy.at/data/easilar01/Moriond2017/cmgTuples/data/'

singleElectron_samples = [\
                        "SingleElectron_Run2016B_23Sep2016",\
                        "SingleElectron_Run2016C_23Sep2016_v1",\
                        "SingleElectron_Run2016D_23Sep2016_v1",\
                        "SingleElectron_Run2016E_23Sep2016_v1",\
                        "SingleElectron_Run2016F_23Sep2016_v1",\
                        "SingleElectron_Run2016G_23Sep2016_v1",\
                        "SingleElectron_Run2016H_PromptReco_v2",\
                        "SingleElectron_Run2016H_PromptReco_v3"\
                        ]

singleMuon_samples = [\
                        "SingleMuon_Run2016B_23Sep2016",\
                        "SingleMuon_Run2016C_23Sep2016_v1",\
                        "SingleMuon_Run2016D_23Sep2016_v1",\
                        "SingleMuon_Run2016E_23Sep2016_v1",\
                        "SingleMuon_Run2016F_23Sep2016_v1",\
                        "SingleMuon_Run2016G_23Sep2016_v1",\
                        "SingleMuon_Run2016H_PromptReco_v2",\
                        "SingleMuon_Run2016H_PromptReco_v3"\
                        ]


allSamples_Data = singleElectron_samples+singleMuon_samples


for s in allSamples_Data:
  exec(s+'={"name":s,"chunkString":s,"rootFileLocation":"treeProducerSusySingleLepton/tree.root","skimAnalyzerDir":"skimAnalyzerCount",\
            "treeName":"tree",\
            "isData":True,\
            "dir":"/".join([data_path,s.split("_")[0]]),\
            }')

create_run_file = True
if create_run_file :
  for s in allSamples_Data:
    print 'python cmgPostProcessing.py --overwrite  --skim=""  --samples='+s

