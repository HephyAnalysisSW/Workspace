import copy, os, sys

ttJetsCSA1450ns={\
"name" : "ttJetsCSA1450ns",
"chunkString": "TTJets_PUS14",
'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/cmg121214_6/TTJets_PUS14",
'dbsName':'/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU_S14_POSTLS170_V6-v1/MINIAODSIM'
}

WJetsToLNu_HT100to200={\
"name" : "WJetsToLNu_HT100to200",
#"chunkString": "WJetsToLNu_HT100to200_PU_S14_POSTLS170",
'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/cmg121214_5/WJetsToLNu_HT100to200_PU_S14_POSTLS170",
'dbsName':'/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola/Spring14dr-PU_S14_POSTLS170_V6-v1/AODSIM'
}
WJetsToLNu_HT200to400={\
"name" : "WJetsToLNu_HT200to400",
#"chunkString": "WJetsToLNu_HT200to400_PU_S14_POSTLS170",
'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/cmg121214_5/WJetsToLNu_HT200to400_PU_S14_POSTLS170",
'dbsName':'/WJetsToLNu_HT-200to400_Tune4C_13TeV-madgraph-tauola/Spring14dr-PU_S14_POSTLS170_V6-v1/AODSIM'
}
WJetsToLNu_HT400to600={\
"name" : "WJetsToLNu_HT400to600",
#"chunkString": "WJetsToLNu_HT400to600_PU_S14_POSTLS170",
'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/cmg121214_5/WJetsToLNu_HT400to600_PU_S14_POSTLS170",
'dbsName':'/WJetsToLNu_HT-400to600_Tune4C_13TeV-madgraph-tauola/Spring14dr-PU_S14_POSTLS170_V6-v1/AODSIM'
}
WJetsToLNu_HT600toInf={\
"name" : "WJetsToLNu_HT600toInf",
#"chunkString": "WJetsToLNu_HT600toInf_PU_S14_POSTLS170",
'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/cmg121214_5/WJetsToLNu_HT600toInf_PU_S14_POSTLS170",
'dbsName':'/WJetsToLNu_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Spring14dr-PU_S14_POSTLS170_V6-v1/AODSIM'
}
#
#T5Full_1200_1000_800={\
#"name" : "T5Full_1200_1000_800",
#"chunkString": "T5Full-1200-1000-800_",
#'dir' : "/data/schoef/cmgTuples/v3/signals/",
#'dbsName':'/T5Full_T5Full-1200-1000-800-Decay-MGMMatch50/schoef-T5Full_T5Full-1200-1000-800-Decay-MGMMatch50-miniAOD-92bfc1aa0ef8c674e0edabb945b19298/USER'
#}
#
#T5Full_1500_800_100={\
#"name" : "T5Full_1500_800_100",
#"chunkString": "T5Full-1500-800-100_",
#'dir' : "/data/schoef/cmgTuples/v3/signals/",
#'dbsName':'/T5Full_T5Full-1500-800-100-Decay-MGMMatch50/schoef-T5Full_T5Full-1500-800-100-Decay-MGMMatch50-miniAOD-92bfc1aa0ef8c674e0edabb945b19298/USER'
#}
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

def getSignalSample(signal):
  if signal in allSignalStrings:
    return {\
      "name" : signal,
      "chunkString": signal,
      'dir' : "/data/schoef/cmgTuples/v3/signals/",
      'dbsName':signal
      }
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

allSignals=[]
for s in allSignalStrings:
  exec(s+"=getSignalSample('"+s+"')")
  exec("allSignals.append("+s+")")
  


