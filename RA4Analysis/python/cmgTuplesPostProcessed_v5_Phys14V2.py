import copy, os, sys

def bookSample(sample):
  h = copy.deepcopy(sample)
  h['dir']=h['dir']+'/hard/'
  s = copy.deepcopy(sample)
  s['dir']=s['dir']+'/soft/'
  return {'hard':h, 'soft':s}

ttJets=bookSample({\
"name" : "ttJets",
"bins" : ["TTJets"],
'dir' : "/data/schoef/cmgTuples/postProcessed_v5_Phys14V2/",
})
WJetsHTToLNu=bookSample({\
"name" : "WJetsHTToLNu",
"bins" : ["WJetsToLNu_HT100to200", "WJetsToLNu_HT200to400", "WJetsToLNu_HT400to600", "WJetsToLNu_HT600toInf"],
'dir' : "/data/schoef/cmgTuples/postProcessed_v5_Phys14V2/",
})
#TTVH=bookSample({\
#"name" : "TTVH",
#"bins" : ["TTH", "TTWJets", "TTZJets"],
#'dir' : "/data/schoef/cmgTuples/postProcessed_v4_Phys14V2/",
#})
#singleTop=bookSample({\
#"name" : "singleTop",
#"bins" : ["TBarToLeptons_sChannel", "TBarToLeptons_tChannel", "TBar_tWChannel", "TToLeptons_sChannel", "TToLeptons_tChannel", "T_tWChannel"],
#'dir' : "/data/schoef/cmgTuples/postProcessed_v4_Phys14V2/",
#})
#DY=bookSample({\
#"name" : "DY",
#"bins" : ["DYJetsToLL_M50_HT100to200", "DYJetsToLL_M50_HT200to400", "DYJetsToLL_M50_HT400to600", "DYJetsToLL_M50_HT600toInf"],
#'dir' : "/data/schoef/cmgTuples/postProcessed_v4_Phys14V2/",
#})
#QCD=bookSample({\
#"name" : "QCD",
#"bins" : ["QCD_HT_250To500", "QCD_HT_500To1000", "QCD_HT_1000ToInf"],
#'dir' : "/data/schoef/cmgTuples/postProcessed_v4_Phys14V2/",
#})


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

#allSignalStrings=[\
#  "T5Full_1200_1000_800",
#  "T5Full_1500_800_100",
##  "SMS_T1qqqq_2J_mGl1000_mLSP800_PU_S14_POSTLS170", #resubmitted
#  "SMS_T1qqqq_2J_mGl1400_mLSP100_PU_S14_POSTLS170",
#  "SMS_T1bbbb_2J_mGl1000_mLSP900_PU_S14_POSTLS170",
#  "SMS_T1bbbb_2J_mGl1500_mLSP100_PU_S14_POSTLS170",
#  "SMS_T1tttt_2J_mGl1200_mLSP800_PU_S14_POSTLS170",
#  "SMS_T1tttt_2J_mGl1500_mLSP100_PU_S14_POSTLS170",
#  "SMS_T2tt_2J_mStop425_mLSP325_PU_S14_POSTLS170",
#  "SMS_T2tt_2J_mStop500_mLSP325_PU_S14_POSTLS170",
#  "SMS_T2tt_2J_mStop650_mLSP325_PU_S14_POSTLS170",
#  "SMS_T2tt_2J_mStop850_mLSP100_PU_S14_POSTLS170",
#  "SMS_T2bb_2J_mStop600_mLSP580_PU_S14_POSTLS170",
#  "SMS_T2bb_2J_mStop900_mLSP100_PU_S14_POSTLS170",
#  "SMS_T2qq_2J_mStop600_mLSP550_PU_S14_POSTLS170",
#  "SMS_T2qq_2J_mStop1200_mLSP100_PU_S14_POSTLS170",
#  "T5WW_2J_mGo1200_mCh1000_mChi800",
#  "T5WW_2J_mGo1500_mCh800_mChi100",
#  "T5WW_2J_mGo1400_mCh315_mChi300",
#  "T1tttt_2J_mGo1300_mStop300_mCh285_mChi280",
#  "T1tttt_2J_mGo1300_mStop300_mChi280",
#  "T1tttt_2J_mGo800_mStop300_mCh285_mChi280",
#  "T1tttt_2J_mGo800_mStop300_mChi280",
#  "T6ttWW_2J_mSbot600_mCh425_mChi50",
#  "T6ttWW_2J_mSbot650_mCh150_mChi50",
#  "T1ttbb_2J_mGo1500_mChi100",
#
#  #from ACD
##  "SqGltttt_Gl_1300_Sq_1300_LSP_100", whatever this is...
#  "T1ttbbWW_2J_mGo1000_mCh725_mChi715_3bodydec",
#  "T1ttbbWW_2J_mGo1000_mCh725_mChi720_3bodydec",
#  "T1ttbbWW_2J_mGo1300_mCh300_mChi290_3bodydec",
#  "T1ttbbWW_2J_mGo1300_mCh300_mChi295_3bodydec",
#  "T1tttt_gluino_1300_LSP_100",
#  "T1tttt_gluino_800_LSP_450",
#  "T5qqqqWW_Gl_1400_LSP_100_Chi_325",
#  "T5qqqqWW_Gl_1400_LSP_300_Chi_315",
#  "T6qqWW_Sq_950_LSP_300_Chi_350",
#]
#

#allSignalStrings=[\
#"SMS_T1tttt_2J_mGl1500_mLSP100",
#"SMS_T1tttt_2J_mGl1200_mLSP800",
#"SMS_T5qqqqWW_Gl1500_Chi800_LSP100",
#"SMS_T5qqqqWW_Gl1200_Chi1000_LSP800"]
#
#
#def getSignalSample(signal):
#  if signal in allSignalStrings:
#    return {\
#      "name" : signal,
##      "chunkString": signal,
#      'dir' : "/data/schoef/cmgTuples/postProcessed_v5_Phys14V2/",
#      'bins':[signal]
#      }
#  else:
#    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)
#
#allSignals=[]
#for s in allSignalStrings:
#  bookSample(getSignalSample(s))
##  exec("soft_"+s+"=getSignalSample('"+s+"', 'soft')")
##  exec("allSignals.append(soft_"+s+")")
##  exec("hard_"+s+"=getSignalSample('"+s+"', 'hard')")
##  exec("allSignals.append(hard_"+s+")")
#  
