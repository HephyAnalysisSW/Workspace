import copy, os, sys

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

soft_ttJetsCSA1450ns={\
"name" : "ttJetsCSA1450ns",
"bins" : ["ttJetsCSA1450ns"],
'dir' : "/data/schoef/cmgTuples/postProcessed_v3/soft/",
}

soft_WJetsHTToLNu={\
"name" : "WJetsHTToLNu",
"bins" : ["WJetsToLNu_HT100to200", "WJetsToLNu_HT200to400", "WJetsToLNu_HT400to600", "WJetsToLNu_HT600toInf"],
'dir' : "/data/schoef/cmgTuples/postProcessed_v3/soft/",
}

allSignalStrings=[\
  "T5Full_1200_1000_800",
  "T5Full_1500_800_100",
#  "SMS_T1qqqq_2J_mGl1000_mLSP800_PU_S14_POSTLS170", #resubmitted
  "SMS_T1qqqq_2J_mGl1400_mLSP100_PU_S14_POSTLS170",
  "SMS_T1bbbb_2J_mGl1000_mLSP900_PU_S14_POSTLS170",
  "SMS_T1bbbb_2J_mGl1500_mLSP100_PU_S14_POSTLS170",
  "SMS_T1tttt_2J_mGl1200_mLSP800_PU_S14_POSTLS170",
  "SMS_T1tttt_2J_mGl1500_mLSP100_PU_S14_POSTLS170",
  "SMS_T2tt_2J_mStop425_mLSP325_PU_S14_POSTLS170",
  "SMS_T2tt_2J_mStop500_mLSP325_PU_S14_POSTLS170",
  "SMS_T2tt_2J_mStop650_mLSP325_PU_S14_POSTLS170",
  "SMS_T2tt_2J_mStop850_mLSP100_PU_S14_POSTLS170",
  "SMS_T2bb_2J_mStop600_mLSP580_PU_S14_POSTLS170",
  "SMS_T2bb_2J_mStop900_mLSP100_PU_S14_POSTLS170",
  "SMS_T2qq_2J_mStop600_mLSP550_PU_S14_POSTLS170",
  "SMS_T2qq_2J_mStop1200_mLSP100_PU_S14_POSTLS170",
  "T5WW_2J_mGo1200_mCh1000_mChi800",
  "T5WW_2J_mGo1500_mCh800_mChi100",
  "T5WW_2J_mGo1400_mCh315_mChi300",
  "T1tttt_2J_mGo1300_mStop300_mCh285_mChi280",
  "T1tttt_2J_mGo1300_mStop300_mChi280",
  "T1tttt_2J_mGo800_mStop300_mCh285_mChi280",
  "T1tttt_2J_mGo800_mStop300_mChi280",
  "T6ttWW_2J_mSbot600_mCh425_mChi50",
  "T6ttWW_2J_mSbot650_mCh150_mChi50",
  "T1ttbb_2J_mGo1500_mChi100",

  #from ACD
#  "SqGltttt_Gl_1300_Sq_1300_LSP_100", whatever this is...
  "T1ttbbWW_2J_mGo1000_mCh725_mChi715_3bodydec",
  "T1ttbbWW_2J_mGo1000_mCh725_mChi720_3bodydec",
  "T1ttbbWW_2J_mGo1300_mCh300_mChi290_3bodydec",
  "T1ttbbWW_2J_mGo1300_mCh300_mChi295_3bodydec",
  "T1tttt_gluino_1300_LSP_100",
  "T1tttt_gluino_800_LSP_450",
  "T5qqqqWW_Gl_1400_LSP_100_Chi_325",
  "T5qqqqWW_Gl_1400_LSP_300_Chi_315",
  "T6qqWW_Sq_950_LSP_300_Chi_350",
]

def getSignalSample(signal, subDir='soft'):
  if signal in allSignalStrings:
    return {\
      "name" : signal,
#      "chunkString": signal,
      'dir' : "/data/schoef/cmgTuples/postProcessed_v3/"+subDir+'/',
      'bins':[signal]
      }
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

allSignals=[]
for s in allSignalStrings:
  exec("soft_"+s+"=getSignalSample('"+s+"', 'soft')")
  exec("allSignals.append(soft_"+s+")")
  exec("hard_"+s+"=getSignalSample('"+s+"', 'hard')")
  exec("allSignals.append(hard_"+s+")")
  
