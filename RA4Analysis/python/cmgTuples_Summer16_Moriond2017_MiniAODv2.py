path     = "/afs/hephy.at/data/easilar01/Moriond2017/cmgTuples/MC/"

bkg_samples = [
'DYJetsToLL_M50_HT1200to2500',\
'DYJetsToLL_M50_HT2500toInf',\
'DYJetsToLL_M50_HT400to600',\
'DYJetsToLL_M50_HT600to800',\
'DYJetsToLL_M50_HT800to1200',\
'QCD_HT1000to1500',\
'QCD_HT1500to2000',\
'QCD_HT2000toInf',\
'QCD_HT300to500',\
'QCD_HT500to700',\
'QCD_HT700to1000',\
'TTWToLNu',\
'TTWToQQ',\
'TTZToLLNuNu',\
'TTZToQQ',\
'WJetsToLNu_HT1200to2500',\
'WJetsToLNu_HT2500toInf',\
'WJetsToLNu_HT400to600',\
'WJetsToLNu_HT600to800',\
'WJetsToLNu_HT800to1200',\
'WWTo2L2Nu',\
'WWToLNuQQ',\
'WZTo1L1Nu2Q',\
'WZTo1L3Nu',\
'WZTo2L2Q',\
'ZZTo2L2Nu',\
'ZZTo2L2Q',\
'TBar_tWch',\
'TBar_tch_powheg',\
'TTJets_DiLepton',\
'TTJets_LO_HT1200to2500',\
'TTJets_LO_HT2500toInf',\
'TTJets_LO_HT600to800',\
'TTJets_LO_HT800to1200',\
'TTJets_SingleLeptonFromT',\
'TTJets_SingleLeptonFromTbar'
          ]


for bkg in bkg_samples:
  exec(bkg+'={"name":bkg,"chunkString":bkg,"dir":path,"dbsName":"","skimAnalyzerDir":"skimAnalyzerCount/",\
              "rootFileLocation":"treeProducerSusySingleLepton/tree.root",\
              "treeName":"tree","isData":False\
              }')

create_run_file = True
if create_run_file :
  for bkg in bkg_samples:
    print 'python cmgPostProcessing.py --overwrite --skim="HT350" --calcbtagweights  --samples='+bkg

SMS_T5qqqqVV_TuneCUETP8M1 ={\
"name" : "SMS_T5qqqqVV_TuneCUETP8M1",
"chunkString":"SMS_T5qqqqVV_TuneCUETP8M1",
"dir": "/afs/hephy.at/data/easilar01/Moriond2017/cmgTuples/signals/",
"dbsName" : "",
"skimAnalyzerDir":"skimAnalyzerCount",
"rootFileLocation":"/treeProducerSusySingleLepton/tree.root",
"treeName":"tree",
'isData':False
}

SMS_T1tttt_TuneCUETP8M1 ={\
"name" : "SMS_T1tttt_TuneCUETP8M1",
"chunkString":"SMS_T1tttt_TuneCUETP8M1",
"dir": "/afs/hephy.at/data/easilar01/Moriond2017/cmgTuples/signals/",
"dbsName" : "",
"skimAnalyzerDir":"skimAnalyzerCount",
"rootFileLocation":"/treeProducerSusySingleLepton/tree.root",
"treeName":"tree",
'isData':False
}

