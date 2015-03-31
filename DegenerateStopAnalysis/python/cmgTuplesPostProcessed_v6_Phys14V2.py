import copy, os, sys


ttJets={\
"name" : "ttJets",
"bins" : ["TTJets"],
'dir' : "/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/",
}
WJetsToLNu_HT100to200={\
"name" : "WJetsToLNu_HT100to200",
"bins" : ["WJetsToLNu_HT100to200"],
'dir' : "/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/",
}
WJetsToLNu_HT200to400={\
"name" : "WJetsToLNu_HT200to400",
"bins" : ["WJetsToLNu_HT200to400"],
'dir' : "/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/",
}
WJetsToLNu_HT400to600={\
"name" : "WJetsToLNu_HT400to600",
"bins" : ["WJetsToLNu_HT400to600"],
'dir' : "/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/",
}
WJetsToLNu_HT600toInf={\
"name" : "WJetsToLNu_HT600toInf",
"bins" : ["WJetsToLNu_HT600toInf"],
'dir' : "/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/",
}
TTH={\
"name" : "TTH",
"bins" : ["TTH"] 
'dir' : "/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/",
}
TTWJets={\
"name" : "TTWJets",
"bins" : ["TTWJets"] 
'dir' : "/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/",
}
TTZJets={\
"name" : "TTZJets",
"bins" : ["TTZJets"] 
'dir' : "/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/",
}
singleTop={\
"name" : "singleTop",
"bins" : ["TBarToLeptons_sChannel", "TBarToLeptons_tChannel", "TBar_tWChannel", "TToLeptons_sChannel", "TToLeptons_tChannel", "T_tWChannel"],
'dir' : "/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/",
}
DY={\
"name" : "DY",
"bins" : ["DYJetsToLL_M50_HT100to200", "DYJetsToLL_M50_HT200to400", "DYJetsToLL_M50_HT400to600", "DYJetsToLL_M50_HT600toInf"],
'dir' : "/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/",
}
QCD={\
"name" : "QCD",
"bins" : ["QCD_HT_250To500", "QCD_HT_500To1000", "QCD_HT_1000ToInf"],
'dir' : "/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/",
}


#T1qqqq_1400_325_300={\
#"name" : "T1qqqq_1400_325_300",
#"bins": ["T1qqqq_1400_325_300"],
#'dir' : "/data/schoef/cmgTuples/postProcessed_v0/singleLepton/",
#}
#
#T5Full_1200_1000_800={\
#"name" : "T5Full_1200_1000_800",
#"bins": ["T5Full_1200_1000_800"],
#'dir' : "/data/schoef/cmgTuples/postProcessed_v0/singleLepton/",
#}
#
#T5Full_1500_800_100={\
#"name" : "T5Full_1500_800_100",
#"bins": ["T5Full_1500_800_100"],
#'dir' : "/data/schoef/cmgTuples/postProcessed_v0/singleLepton/",
#}



allSignalStrings=[\
"SMS_T1tttt_2J_mGl1200_mLSP800",
"SMS_T1tttt_2J_mGl1500_mLSP100",
"SMS_T2tt_2J_mStop425_mLSP325",
"SMS_T2tt_2J_mStop500_mLSP325",
"SMS_T2tt_2J_mStop650_mLSP325",
"SMS_T2tt_2J_mStop850_mLSP100",
"SMS_T5qqqqWW_Gl1200_Chi1000_LSP800",
"SMS_T5qqqqWW_Gl1500_Chi800_LSP100",
"T1ttbbWW_mGo1000_mCh725_mChi715",
"T1ttbbWW_mGo1000_mCh725_mChi720",
"T1ttbbWW_mGo1300_mCh300_mChi290",
"T1ttbbWW_mGo1300_mCh300_mChi295",
"T5ttttDeg_mGo1000_mStop300_mCh285_mChi280",
"T5ttttDeg_mGo1000_mStop300_mChi280",
"T5ttttDeg_mGo1300_mStop300_mCh285_mChi280",
"T5ttttDeg_mGo1300_mStop300_mChi280",
]


def getSignalSample(signal):
  if signal in allSignalStrings:
    return {
      "name" : signal,
#      "chunkString": signal,
      'dir' : "/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/",
      'bins':[signal]}
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

allSignals=[]
for s in allSignalStrings:
  sm = makeSample(getSignalSample(s))
  exec(s+"=sm")
  exec("allSignals.append(s)")
  
