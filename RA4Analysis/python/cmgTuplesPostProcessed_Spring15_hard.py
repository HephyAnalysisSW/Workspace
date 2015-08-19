import copy, os, sys

def makeSample(sample):
  h = copy.deepcopy(sample)
  h['dir']=h['dir']+'/hard/'
  s = copy.deepcopy(sample)
  s['dir']=s['dir']+'/soft/'
  return {'hard':h, 'soft':s}

data_ele=makeSample({\
"name": "SingleElectron_Run2015B",
"bins" : ["SingleElectron_Run2015B"],
'dir' : "/data/easilar/cmgTuples/postProcessed_Spring15_AllFlags/",
})

data_mu=makeSample({\
"name": "SingleMuon_Run2015B",
"bins" : ["SingleMuon_Run2015B"],
'dir' : "/data/easilar/cmgTuples/postProcessed_Spring15_AllFlags/",
})

ttJets=makeSample({\
"name" : "ttJets",
"bins" : ["TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"],
'dir' : "/data/easilar/cmgTuples/postProcessed_Spring15_AllFlags/",
})

WJetsHTToLNu=makeSample({\
"name" : "WJetsHTToLNu",
"bins" : ["WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"],
'dir' : "/data/dspitzbart/cmgTuples/postProcessed_Spring15_AllFlags2/",
})

WJetsHTToLNuLow=makeSample({\
"name" : "WJetsHTToLNu",
"bins" : ["WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"],
'dir' : "/data/dspitzbart/cmgTuples/postProcessed_Spring15_AllFlags2/",
})

#TTVH=makeSample({\
#"name" : "TTVH",
#"bins" : ["TTH", "TTWJets", "TTZJets"],
#'dir' : "/data/easilar/cmgTuples/postProcessed_v8_Phys14v3/HT400ST200/",
#})
singleTop=makeSample({\
"name" : "singleTop",
#"bins" : ["TBarToLeptons_sch", "TBarToLeptons_tch", "TBar_tWch", "TToLeptons_sch", "TToLeptons_tch", "T_tWch"],
"bins" : ["ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1", "ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1", "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1", "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1"],
'dir' : "/data/easilar/cmgTuples/postProcessed_Spring15_AllFlags/",
})
#DY=makeSample({\
#"name" : "DY",
#"bins" : ["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"],
#'dir' : "/data/easilar/cmgTuples/postProcessed_Spring15_AllFlags/",
#})
DY=makeSample({\
"name" : "DY",
"bins" : ["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"],
'dir' : "/data/dspitzbart/cmgTuples/postProcessed_Spring15_AllFlags2/",
})


QCD=makeSample({\
"name" : "QCD",
"bins" : \
["QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8","QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8",\
"QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8","QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8",\
"QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8","QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8",\
"QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8","QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8",\
"QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8","QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8",\
"QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8","QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8",\
"QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8","QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8",\
"QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8","QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8"],
'dir' : "/data/easilar/cmgTuples/postProcessed_Spring15_AllFlags/",
})



#QCD=makeSample({\
#"name" : "QCD",
#"bins" : ["QCD_HT_100To250","QCD_HT_250To500", "QCD_HT_500To1000", "QCD_HT_1000ToInf"],
#'dir' : "/data/dspitzbart/cmgTuples/postProcessed_Phys14V3/HT400ST200/",
#})


#T1qqqq_1400_325_300={\
#"name" : "T1qqqq_1400_325_300",
#"bins": ["T1qqqq_1400_325_300"],
#'dir' : "/data/easilar/cmgTuples/postProcessed_v0/singleLepton/",
#}
#
#T5Full_1200_1000_800={\
#"name" : "T5Full_1200_1000_800",
#"bins": ["T5Full_1200_1000_800"],
#'dir' : "/data/easilar/cmgTuples/postProcessed_v0/singleLepton/",
#}
#
#T5Full_1500_800_100={\
#"name" : "T5Full_1500_800_100",
#"bins": ["T5Full_1500_800_100"],
#'dir' : "/data/easilar/cmgTuples/postProcessed_v0/singleLepton/",
#}




#allSignalStrings=[\
#"T5qqqqWW_mGo1000_mCh800_mChi700",\
#"T5qqqqWW_mGo1200_mCh1000_mChi800",\
#"T5qqqqWW_mGo1500_mCh800_mChi100",\
#"SMS_T1tttt_2J_mGl1500_mLSP100",\
#"SMS_T1tttt_2J_mGl1200_mLSP800",\
#]

'''
def getSignalSample(signal):
  if signal in allSignalStrings:
    return {
      "name" : signal,
#      "chunkString": signal,
      'dir' : "/data/easilar/cmgTuples/postProcessed_v8_Phys14v3/HT400ST200/",
      'bins':[signal]}
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

allSignals=[]
for s in allSignalStrings:
  sm = makeSample(getSignalSample(s))
  exec(s+"=sm")
  exec("allSignals.append(s)")
''' 
