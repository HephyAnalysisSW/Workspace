import copy, os, sys


ttJets_PU20bx25={\
"name" : "TTJets",
'chunkString' : 'TTJets',
'dir' : "/data/nrad/cmgTuples/crab_cmg_v3/TTJets/",
'dbsName':'/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
ttWJets_PU20bx25={\
"name" : "TTWJets",
'chunkString' : 'TTWJets',
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/TTWJets/",
'dbsName':'/TTWJets_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
ttZJets_PU20bx25={\
"name" : "TTZJets",
'chunkString' : 'TTZJets',
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/TTZJets/",
'dbsName':'/TTZJets_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
ttH_PU20bx25={\
"name" : "TTH",
'chunkString' : 'TTH',
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/TTH",
'dbsName':'/TTbarH_M-125_13TeV_amcatnlo-pythia8-tauola/Phys14DR-PU40bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT100to200_PU20bx25={\
"name" : "WJetsToLNu_HT100to200",
'chunkString' : 'WJetsToLNu_HT100to200',
'dir' : "/data/nrad/cmgTuples/crab_cmg_v3/WJetsToLNu_HT100to200/",
'dbsName':'/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT200to400_PU20bx25={\
"name" : "WJetsToLNu_HT200to400",
'chunkString' : 'WJetsToLNu_HT200to400',
'dir' : "/data/nrad/cmgTuples/crab_cmg_v3/WJetsToLNu_HT200to400",
'dbsName':'/WJetsToLNu_HT-200to400_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT400to600_PU20bx25={\
"name" : "WJetsToLNu_HT400to600",
'chunkString' : 'WJetsToLNu_HT400to600',
'dir' : "/data/nrad/cmgTuples/crab_cmg_v3/WJetsToLNu_HT400to600/",
'dbsName':'/WJetsToLNu_HT-400to600_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT600toInf_PU20bx25={\
"name" : "WJetsToLNu_HT600toInf",
"chunkString": "WJetsToLNu_HT600toInf",
'dir' : "/data/nrad/cmgTuples/crab_cmg_v3/WJetsToLNu_HT600toInf/",
'dbsName':'/WJetsToLNu_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
DYJetsToLL_M50_HT100to200_PU20bx25={\
"name" : "DYJetsToLL_M50_HT100to200",
"chunkString": "DYJetsToLL_M50_HT100to200",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/DYJetsToLL_M50_HT100to200/",
'dbsName':'/DYJetsToLL_M-50_HT-100to200_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
DYJetsToLL_M50_HT200to400_PU20bx25={\
"name" : "DYJetsToLL_M50_HT200to400",
"chunkString": "DYJetsToLL_M50_HT200to400",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/DYJetsToLL_M50_HT200to400/",
'dbsName':'/DYJetsToLL_M-50_HT-200to400_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
DYJetsToLL_M50_HT400to600_PU20bx25={\
"name" : "DYJetsToLL_M50_HT400to600",
"chunkString": "DYJetsToLL_M50_HT400to600",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/DYJetsToLL_M50_HT400to600/",
'dbsName':'/DYJetsToLL_M-50_HT-400to600_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
DYJetsToLL_M50_HT600toInf_PU20bx25={\
"name" : "DYJetsToLL_M50_HT600toInf",
"chunkString": "DYJetsToLL_M50_HT600toInf",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/DYJetsToLL_M50_HT600toInf/",
'dbsName':'/DYJetsToLL_M-50_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}

QCD_HT_100To250_PU20bx25={\
"name" : "QCD_HT_100To250",
"chunkString": "QCD_HT_100To250",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/QCD_HT_100To250/",
'dbsName':'/QCD_HT_100To250_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}

QCD_HT_250To500_PU20bx25={\
"name" : "QCD_HT_250To500",
"chunkString": "QCD_HT_250To500",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/QCD_HT_250To500/",
'dbsName':'/QCD_HT_250To500_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
QCD_HT_500To1000_PU20bx25={\
"name" : "QCD_HT_500To1000",
"chunkString": "QCD_HT_500To1000",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/QCD_HT_500To1000/",
'dbsName':'/QCD_HT_500To1000_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
QCD_HT_1000ToInf_PU20bx25={\
"name" : "QCD_HT_1000ToInf",
"chunkString": "QCD_HT_1000ToInf",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/QCD_HT_1000ToInf/",
'dbsName':'/QCD_HT_1000ToInf_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
TBarToLeptons_sChannel_PU20bx25={\
"name" : "TBarToLeptons_sch",
"chunkString": "TBarToLeptons_sch",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/TBarToLeptons_sch/",
'dbsName':'/TBarToLeptons_s-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
TBarToLeptons_tChannel_PU20bx25={\
"name" : "TBarToLeptons_tch",
"chunkString": "TBarToLeptons_tch",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/TBarToLeptons_tch/",
'dbsName':'/TBarToLeptons_t-channel_Tune4C_CSA14_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
TToLeptons_sChannel_PU20bx25={\
"name" : "TToLeptons_sch",
"chunkString": "TToLeptons_sch",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/TToLeptons_sch/",
'dbsName':'/TToLeptons_s-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
TToLeptons_tChannel_PU20bx25={\
"name" : "TToLeptons_tch",
"chunkString": "TToLeptons_tch",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/TToLeptons_tch/",
'dbsName':'/TToLeptons_t-channel_Tune4C_CSA14_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
T_tWChannel_PU20bx25={\
"name" : "T_tWch",
"chunkString": "T_tWch",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/T_tWch/",
'dbsName':'/T_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
TBar_tWChannel_PU20bx25={\
"name" : "TBar_tWch",
"chunkString": "TBar_tWch",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/TBar_tWch",
'dbsName':'/Tbar_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}

allSignalData=[\
["/data/easilar/cmgTuples/crab_cmg_v1/test2/T5qqqqWW_mGo1000_mCh800_mChi700", "T5qqqqWW_mGo1000_mCh800_mChi700"], ##OK
["/data/easilar/cmgTuples/crab_cmg_v1/test2/T5qqqqWW_mGo1200_mCh1000_mChi800", "T5qqqqWW_mGo1200_mCh1000_mChi800"], ##OK
["/data/easilar/cmgTuples/crab_cmg_v1/test2/T5qqqqWW_mGo1500_mCh800_mChi100", "T5qqqqWW_mGo1500_mCh800_mChi100"], ##OK 
["/data/easilar/cmgTuples/crab_cmg_v1/test2/SMS_T1tttt_2J_mGl1500_mLSP100", "SMS_T1tttt_2J_mGl1500_mLSP100"], ##OK 
["/data/easilar/cmgTuples/crab_cmg_v1/test2/SMS_T1tttt_2J_mGl1200_mLSP800", "SMS_T1tttt_2J_mGl1200_mLSP800"], ##OK 
["/data/nrad2/cmgTuples/crab_cmg_v1/SMS_T2tt_2J_mStop425_mLSP325", "SMS_T2tt_2J_mStop425_mLSP325"], ##OK 
["/data/nrad2/cmgTuples/crab_cmg_v1/SMS_T2tt_2J_mStop500_mLSP325", "SMS_T2tt_2J_mStop500_mLSP325"], ##OK 
["/data/nrad2/cmgTuples/crab_cmg_v1/SMS_T2tt_2J_mStop650_mLSP325", "SMS_T2tt_2J_mStop650_mLSP325"], ##OK 
["/data/nrad2/cmgTuples/crab_cmg_v1/SMS_T2tt_2J_mStop850_mLSP100", "SMS_T2tt_2J_mStop850_mLSP100"], ##OK 

]
allSignalStrings = [s[1] for s in allSignalData]
def getSignalSample(dir, signal):
  if signal in allSignalStrings:
    return {\
      "name" : signal,
      "chunkString": signal,
      'dir' : dir,
      'dbsName':signal
      }
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

allSignals=[]
for d,s in allSignalData:
  exec(s+"=getSignalSample('"+d+"','"+s+"')")
  exec("allSignals.append("+s+")")
  
