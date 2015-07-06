import copy, os, sys

#dir1="/afs/hephy.at/work/n/nrad/data/postProcessed_v3_Phys14V1/"
dir1="/data/nrad/cmgTuples/postProcessed_v1_Phys14V5/"

def makeSample(sample):
  n = copy.deepcopy(sample)
  n['dir']=n['dir']+'/none/'
  h = copy.deepcopy(sample)
  h['dir']=h['dir']+'/hard/'
  s = copy.deepcopy(sample)
  s['dir']=s['dir']+'/soft/'
  return {'hard':h, 'soft':s, 'none':n}

ttJets=makeSample({\
"name" : "ttJets",
"bins" : ["TTJets"],
'dir' : dir1,
})
WJetsHTToLNu=makeSample({\
"name" : "WJetsHTToLNu",
"bins" : ["WJetsToLNu_HT100to200", "WJetsToLNu_HT200to400", "WJetsToLNu_HT400to600", "WJetsToLNu_HT600toInf"],
'dir' : dir1,
})
TTVH=makeSample({\
"name" : "TTVH",
"bins" : ["TTH", "TTWJets", "TTZJets"],
'dir' : dir1,
})
singleTop=makeSample({\
"name" : "singleTop",
"bins" : ["TBarToLeptons_sch", "TBarToLeptons_tch", "TBar_tWch", "TToLeptons_sch", "TToLeptons_tch", "T_tWch"],
'dir' : dir1,
})
DY=makeSample({\
"name" : "DY",
"bins" : ["DYJetsToLL_M50_HT100to200", "DYJetsToLL_M50_HT200to400", "DYJetsToLL_M50_HT400to600", "DYJetsToLL_M50_HT600toInf"],
'dir' : dir1,
})
QCD=makeSample({\
"name" : "QCD",
"bins" : ["QCD_HT_100To250","QCD_HT_250To500", "QCD_HT_500To1000", "QCD_HT_1000ToInf"],
'dir' : dir1,
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
"T2DegStop_300_270",
]


def getSignalSample(signal):
  if signal in allSignalStrings:
    return {
      "name" : signal,
#      "chunkString": signal,
      'dir' : dir1,
      'bins':[signal]}
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

allSignals=[]
for s in allSignalStrings:
  sm = makeSample(getSignalSample(s))
  exec(s+"=sm")
  exec("allSignals.append(s)")
  
