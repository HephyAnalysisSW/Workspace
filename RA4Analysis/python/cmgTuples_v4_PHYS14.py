import copy, os, sys

#QCD_HT_1000ToInf
#QCD_HT_250To500
#QCD_HT_500To1000
#TTH
#TTWJets
#TTZJets
#TToLeptons_sch
#TToLeptons_tch
#T_tWch
#TBarToLeptons_sch
#TBarToLeptons_tch
#TBar_tWch

ttJets_PU20bx25={\
"name" : "TTJets",
'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/Phys14_2/TTJets" #"/data/schoef/cmgTuples/v4_Phys14V1/",
'chunkString' : '',
'dbsName':'/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
ttWJets_PU20bx25={\
"name" : "TTWJets",
'dir' : "/data/schoef/cmgTuples/v4_Phys14V1/",
'chunkString' : 'TTWJets',
'dbsName':'/TTWJets_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
ttZJets_PU20bx25={\
"name" : "TTZJets",
'dir' : "/data/schoef/cmgTuples/v4_Phys14V1/",
'chunkString' : 'TTZJets',
'dbsName':'/TTZJets_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
ttH_PU20bx25={\
"name" : "TTH",
'dir' : "/data/schoef/cmgTuples/v4_Phys14V1/",
'chunkString' : 'TTH',
'dbsName':'/TTbarH_M-125_13TeV_amcatnlo-pythia8-tauola/Phys14DR-PU40bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT100to200_PU20bx25={\
"name" : "WJetsToLNu_HT100to200",
"chunkString": "",
'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/Phys14_4/WJetsToLNu_HT100to200",
'dbsName':'/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT200to400_PU20bx25={\
"name" : "WJetsToLNu_HT200to400",
"chunkString": "",
'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/Phys14_4/WJetsToLNu_HT100to200",
'dbsName':'/WJetsToLNu_HT-200to400_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT400to600_PU20bx25={\
"name" : "WJetsToLNu_HT400to600",
"chunkString": "",
'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/Phys14_4/WJetsToLNu_HT100to200",
'dbsName':'/WJetsToLNu_HT-400to600_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT600toInf_PU20bx25={\
"name" : "WJetsToLNu_HT600toInf",
"chunkString": "",
'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/Phys14_4/WJetsToLNu_HT100to200",
'dbsName':'/WJetsToLNu_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
DYJetsToLL_M50_HT100to200_PU20bx25={\
"name" : "DYJetsToLL_M50_HT100to200",
"chunkString": "",
'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/easilar/Phys14/DYJetsToLL_M50_HT100to200",
'dbsName':'/DYJetsToLL_M-50_HT-100to200_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
DYJetsToLL_M50_HT200to400_PU20bx25={\
"name" : "DYJetsToLL_M50_HT200to400",
"chunkString": "",
'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/easilar/Phys14/DYJetsToLL_M50_HT100to200",
'dbsName':'/DYJetsToLL_M-50_HT-200to400_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
DYJetsToLL_M50_HT400to600_PU20bx25={\
"name" : "DYJetsToLL_M50_HT400to600",
"chunkString": "",
'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/easilar/Phys14/DYJetsToLL_M50_HT100to200",
'dbsName':'/DYJetsToLL_M-50_HT-400to600_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
DYJetsToLL_M50_HT600toInf_PU20bx25={\
"name" : "DYJetsToLL_M50_HT600toInf",
"chunkString": "",
'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/easilar/Phys14/DYJetsToLL_M50_HT100to200",
'dbsName':'/DYJetsToLL_M-50_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
QCD_HT_250To500_PU20bx25={\
"name" : "QCD_HT_250To500",
"chunkString": "QCD_HT_250To500",
'dir' : "/data/schoef/cmgTuples/v4_Phys14V1/",
'dbsName':'/QCD_HT_250To500_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
QCD_HT_500To1000_PU20bx25={\
"name" : "QCD_HT_500To1000",
"chunkString": "QCD_HT_500To1000",
'dir' : "/data/schoef/cmgTuples/v4_Phys14V1/",
'dbsName':'/QCD_HT_500To1000_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
QCD_HT_1000ToInf_PU20bx25={\
"name" : "QCD_HT_1000ToInf",
"chunkString": "QCD_HT_1000ToInf",
'dir' : "/data/schoef/cmgTuples/v4_Phys14V1/",
'dbsName':'/QCD_HT_1000ToInf_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
TBarToLeptons_sChannel_PU20bx25={\
"name" : "TBarToLeptons_sChannel",
"chunkString": "TBarToLeptons_sch",
'dir' : "/data/schoef/cmgTuples/v4_Phys14V1/",
'dbsName':'/TBarToLeptons_s-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
TBarToLeptons_tChannel_PU20bx25={\
"name" : "TBarToLeptons_tChannel",
"chunkString": "TBarToLeptons_tch",
'dir' : "/data/schoef/cmgTuples/v4_Phys14V1/",
'dbsName':'/TBarToLeptons_t-channel_Tune4C_CSA14_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
TToLeptons_sChannel_PU20bx25={\
"name" : "TToLeptons_sChannel",
"chunkString": "TToLeptons_sch",
'dir' : "/data/schoef/cmgTuples/v4_Phys14V1/",
'dbsName':'/TToLeptons_s-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
TToLeptons_tChannel_PU20bx25={\
"name" : "TToLeptons_tChannel",
"chunkString": "TToLeptons_tch",
'dir' : "/data/schoef/cmgTuples/v4_Phys14V1/",
'dbsName':'/TToLeptons_t-channel_Tune4C_CSA14_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
T_tWChannel_PU20bx25={\
"name" : "T_tWChannel",
"chunkString": "T_tWch",
'dir' : "/data/schoef/cmgTuples/v4_Phys14V1/",
'dbsName':'/T_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
TBar_tWChannel_PU20bx25={\
"name" : "TBar_tWChannel",
"chunkString": "TBar_tWch",
'dir' : "/data/schoef/cmgTuples/v4_Phys14V1/",
'dbsName':'/Tbar_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}

#WJetsToLNu_HT600toInf_PU20bx25={\
#"name" : "WJetsToLNu_HT600toInf",
#"chunkString": "",
#'dir' : "/data/schoef/cmgTuples/v4_Phys14V1/WJets",
#'dbsName':'/WJetsToLNu_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}

#allSignalStrings=[\
#SMS_T1tttt_2J_mGl1200_mLSP800
#SMS_T1tttt_2J_mGl1500_mLSP100
#SMS_T2tt_2J_mStop425_mLSP325
#SMS_T2tt_2J_mStop500_mLSP325
#SMS_T2tt_2J_mStop650_mLSP325
#SMS_T2tt_2J_mStop850_mLSP100

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

#def getSignalSample(signal):
#  if signal in allSignalStrings:
#    return {\
#      "name" : signal,
#      "chunkString": signal,
#      'dir' : "/data/schoef/cmgTuples/v3/signals/",
#      'dbsName':signal
#      }
#  else:
#    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)
#
#allSignals=[]
#for s in allSignalStrings:
#  exec(s+"=getSignalSample('"+s+"')")
#  exec("allSignals.append("+s+")")
#  
