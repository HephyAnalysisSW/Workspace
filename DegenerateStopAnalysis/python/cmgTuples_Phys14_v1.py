import copy, os, sys




sampleDir="/data/nrad/cmgTuples/crab_cmg_v3/"

TTJets_PU20bx25={\
"name" : "TTJets",
'chunkString' : 'TTJets',
'dir' : sampleDir+'/TTJets',
'dbsName':'/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
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



#WJetsToLNu_HT100to200={\
#"name" : "WJetsToLNu_HT100to200",
#'chunkString' : 'WJetsToLNu_HT100to200',
#'dir' : sampleDir+'WJetsToLNu_HT100to200',
#'dbsName':'/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#WJetsToLNu_HT200to400={\
#"name" : "WJetsToLNu_HT200to400",
#'chunkString' : 'WJetsToLNu_HT200to400',
#'dir' : sampleDir+'WJetsToLNu_HT200to400',
#'dbsName':'/WJetsToLNu_HT-200to400_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#WJetsToLNu_HT400to600={\
#"name" : "WJetsToLNu_HT400to600",
#'chunkString' : 'WJetsToLNu_HT400to600',
#'dir' : sampleDir+'WJetsToLNu_HT400to600',
#'dbsName':'/WJetsToLNu_HT-400to600_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#WJetsToLNu_HT600toInf={\
#"name" : "WJetsToLNu_HT600toInf",
#"chunkString": "WJetsToLNu_HT600toInf",
#'dir' : sampleDir+'WJetsToLNu_HT600toInf',
#'dbsName':'/WJetsToLNu_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#
#
#
#
#
#ttJets_PU20bx25={\
#"name" : "TTJets",
#'chunkString' : 'TTJets',
#'dir' : "/data/easilar/tuples_from_batool/TTJETS/",
#'dbsName':'/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#
#WJetsToLNu_HT100to200_PU20bx25={\
#"name" : "WJetsToLNu_HT100to200",
#'chunkString' : 'WJetsToLNu_HT100to200',
#'dir' : "/data/easilar/tuples_from_batool/WJETS",
#'dbsName':'/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#WJetsToLNu_HT200to400_PU20bx25={\
#"name" : "WJetsToLNu_HT200to400",
#'chunkString' : 'WJetsToLNu_HT200to400',
#'dir' : "/data/easilar/tuples_from_batool/WJETS",
#'dbsName':'/WJetsToLNu_HT-200to400_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#WJetsToLNu_HT400to600_PU20bx25={\
#"name" : "WJetsToLNu_HT400to600",
#'chunkString' : 'WJetsToLNu_HT400to600',
#'dir' : "/data/easilar/tuples_from_batool/WJETS",
#'dbsName':'/WJetsToLNu_HT-400to600_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#WJetsToLNu_HT600toInf_PU20bx25={\
#"name" : "WJetsToLNu_HT600toInf",
#"chunkString": "WJetsToLNu_HT600toInf",
#'dir' : "/data/easilar/tuples_from_batool/WJETS",
#'dbsName':'/WJetsToLNu_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#
#
#
#
#
#ttWJets_PU20bx25={\
#"name" : "TTWJets",
#'chunkString' : 'TTWJets',
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/TTWJets_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#ttZJets_PU20bx25={\
#"name" : "TTZJets",
#'chunkString' : 'TTZJets',
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/TTZJets_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#ttH_PU20bx25={\
#"name" : "TTH",
#'chunkString' : 'TTH',
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/TTbarH_M-125_13TeV_amcatnlo-pythia8-tauola/Phys14DR-PU40bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#
#DYJetsToLL_M50_HT100to200_PU20bx25={\
#"name" : "DYJetsToLL_M50_HT100to200",
#"chunkString": "DYJetsToLL_M50_HT100to200",
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/DYJetsToLL_M-50_HT-100to200_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#DYJetsToLL_M50_HT200to400_PU20bx25={\
#"name" : "DYJetsToLL_M50_HT200to400",
#"chunkString": "DYJetsToLL_M50_HT200to400",
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/DYJetsToLL_M-50_HT-200to400_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#DYJetsToLL_M50_HT400to600_PU20bx25={\
#"name" : "DYJetsToLL_M50_HT400to600",
#"chunkString": "DYJetsToLL_M50_HT400to600",
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/DYJetsToLL_M-50_HT-400to600_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#DYJetsToLL_M50_HT600toInf_PU20bx25={\
#"name" : "DYJetsToLL_M50_HT600toInf",
#"chunkString": "DYJetsToLL_M50_HT600toInf",
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/DYJetsToLL_M-50_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#
#QCD_HT_100To250_PU20bx25={\
#"name" : "QCD_HT_100To250",
#"chunkString": "QCD_HT_100To250",
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/QCD_HT_100To250_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#
#QCD_HT_250To500_PU20bx25={\
#"name" : "QCD_HT_250To500",
#"chunkString": "QCD_HT_250To500",
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/QCD_HT_250To500_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#QCD_HT_500To1000_PU20bx25={\
#"name" : "QCD_HT_500To1000",
#"chunkString": "QCD_HT_500To1000",
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/QCD_HT_500To1000_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#QCD_HT_1000ToInf_PU20bx25={\
#"name" : "QCD_HT_1000ToInf",
#"chunkString": "QCD_HT_1000ToInf",
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/QCD_HT_1000ToInf_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#TBarToLeptons_sChannel_PU20bx25={\
#"name" : "TBarToLeptons_sch",
#"chunkString": "TBarToLeptons_sch",
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/TBarToLeptons_s-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#TBarToLeptons_tChannel_PU20bx25={\
#"name" : "TBarToLeptons_tch",
#"chunkString": "TBarToLeptons_tch",
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/TBarToLeptons_t-channel_Tune4C_CSA14_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#TToLeptons_sChannel_PU20bx25={\
#"name" : "TToLeptons_sch",
#"chunkString": "TToLeptons_sch",
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/TToLeptons_s-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#TToLeptons_tChannel_PU20bx25={\
#"name" : "TToLeptons_tch",
#"chunkString": "TToLeptons_tch",
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/TToLeptons_t-channel_Tune4C_CSA14_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#T_tWChannel_PU20bx25={\
#"name" : "T_tWch",
#"chunkString": "T_tWch",
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/T_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}
#TBar_tWChannel_PU20bx25={\
#"name" : "TBar_tWch",
#"chunkString": "TBar_tWch",
#'dir' : "/data/easilar/Phys14_V3/",
#'dbsName':'/Tbar_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
#}

 


allSignalData=[\
#["/data/nrad/cmgTuples/T2DegStop300_270", "T2DegStop_test"],
#["/data/nrad/cmgTuples/T2DegStop300_270", "T2DegStop_300_270"],
["/data/nrad/cmgTuples/dxy0fix/T2DegStop_300_270_miniIso/T2DegStop_300_270", "T2DegStop_300_270"],
#["/data/schoef/cmgTuples/v5_Phys14V2/", "SMS_T5qqqqWW_Gl1500_Chi800_LSP100"],
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
  
