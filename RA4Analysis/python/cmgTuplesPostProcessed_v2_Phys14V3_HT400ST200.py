import copy, os, sys

def makeSample(sample):
  h = copy.deepcopy(sample)
  h['dir']=h['dir']+'/hard/'
  s = copy.deepcopy(sample)
  s['dir']=s['dir']+'/soft/'
  return {'hard':h, 'soft':s}

ttJets=makeSample({\
"name" : "ttJets",
"bins" : ["TTJets"],
'dir' : "/data/easilar/cmgTuples/postProcessed_v2_Phys14V3/HT400ST200/",
})
WJetsHTToLNu=makeSample({\
"name" : "WJetsHTToLNu",
"bins" : ["WJetsToLNu_HT100to200", "WJetsToLNu_HT200to400", "WJetsToLNu_HT400to600", "WJetsToLNu_HT600toInf"],
'dir' : "/data/easilar/cmgTuples/postProcessed_v2_Phys14V3/HT400ST200/",
})
TTVH=makeSample({\
"name" : "TTVH",
"bins" : ["TTH", "TTWJets", "TTZJets"],
'dir' : "/data/easilar/cmgTuples/postProcessed_v2_Phys14V3/HT400ST200/",
})
singleTop=makeSample({\
"name" : "singleTop",
"bins" : ["TBarToLeptons_sch", "TBarToLeptons_tch", "TBar_tWch", "TToLeptons_sch", "TToLeptons_tch", "T_tWch"],
'dir' : "/data/easilar/cmgTuples/postProcessed_v2_Phys14V3/HT400ST200/",
})
DY=makeSample({\
"name" : "DY",
"bins" : ["DYJetsToLL_M50_HT100to200", "DYJetsToLL_M50_HT200to400", "DYJetsToLL_M50_HT400to600", "DYJetsToLL_M50_HT600toInf"],
'dir' : "/data/easilar/cmgTuples/postProcessed_v2_Phys14V3/HT400ST200/",
})
QCD=makeSample({\
"name" : "QCD",
"bins" : ["QCD_HT_100To250","QCD_HT_250To500", "QCD_HT_500To1000", "QCD_HT_1000ToInf"],
'dir' : "/data/easilar/cmgTuples/postProcessed_v2_Phys14V3/HT400ST200/",
})


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


allSignalStrings=[\
"T5qqqqWW_mGo1000_mCh800_mChi700",\
"T5qqqqWW_mGo1200_mCh1000_mChi800",\
"T5qqqqWW_mGo1500_mCh800_mChi100",\
#"SMS_T1tttt_2J_mGl1500_mLSP100",\
#"SMS_T1tttt_2J_mGl1200_mLSP800",\
]


def getSignalSample(signal):
  if signal in allSignalStrings:
    return {
      "name" : signal,
#      "chunkString": signal,
      'dir' : "/data/easilar/cmgTuples/postProcessed_v2_Phys14V3_signals/HT400ST200/",
      'bins':[signal]}
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

allSignals=[]
for s in allSignalStrings:
  sm = makeSample(getSignalSample(s))
  exec(s+"=sm")
  exec("allSignals.append(s)")
  
