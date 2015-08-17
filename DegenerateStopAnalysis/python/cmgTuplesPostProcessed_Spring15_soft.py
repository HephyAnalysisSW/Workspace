import copy, os, sys
#spring15_soft_sample_dir = "/data/nrad/cmgTuples/postProcessed_Spring15/"
spring15_soft_sample_dir = "/afs/hephy.at/work/n/nrad/cmgTuplesPostProcessed/Spring15_v0"



def makeSample(sample):
  h = copy.deepcopy(sample)
  h['dir']=h['dir']+'/hard/'
  s = copy.deepcopy(sample)
  s['dir']=s['dir']+'/soft/'
  return {'hard':h, 'soft':s}

TTJets=makeSample({\
"name" : "TTJets",
#"bins" : ["TBarToLeptons_sch", "TBarToLeptons_tch", "TBar_tWch", "TToLeptons_sch", "TToLeptons_tch", "T_tWch"],
"bins" : ["TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"],
'dir' : spring15_soft_sample_dir
})
WJets=makeSample({\
"name" : "WJets",
"bins" : [
              "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
              "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
              "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
              "WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        ],
'dir' : spring15_soft_sample_dir
})


allSignalStrings=[\
"T2DegStop_300_270",
]


def getSignalSample(signal):
  if signal in allSignalStrings:
    return {
      "name" : signal,
#      "chunkString": signal,
      'dir' : spring15_soft_sample_dir,
      'bins':[signal]}
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

allSignals=[]
for s in allSignalStrings:
  sm = makeSample(getSignalSample(s))
  exec(s+"=sm")









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


allSignalStrings=[\
"T2DegStop_300_270",
]

