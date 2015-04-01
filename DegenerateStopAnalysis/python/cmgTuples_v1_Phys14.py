import copy, os, sys

ttJets_PU20bx25={\
"name" : "TTJets",
'chunkString' : '',
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_TTJets/TTJets",
#'dir' : "/data/schoef/cmgTuples/v5_Phys14V2/TTJets",
'dir' : "/data/schoef/cmgTuples/v5_Phys14V2_fromDPM_lateProcessingTauFix/TTJets",
'fromDPM':True,
'dbsName':'/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT100to200_PU20bx25={\
"name" : "WJetsToLNu_HT100to200",
"chunkString": "WJetsToLNu_HT100to200",
'dir' : "/data/schoef/cmgTuples/v5_Phys14V2/",
'dbsName':'/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT200to400_PU20bx25={\
"name" : "WJetsToLNu_HT200to400",
"chunkString": "WJetsToLNu_HT200to400",
'dir' : "/data/schoef/cmgTuples/v5_Phys14V2/",
'dbsName':'/WJetsToLNu_HT-200to400_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT400to600_PU20bx25={\
"name" : "WJetsToLNu_HT400to600",
"chunkString": "WJetsToLNu_HT400to600",
'dir' : "/data/schoef/cmgTuples/v5_Phys14V2/",
'dbsName':'/WJetsToLNu_HT-400to600_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT600toInf_PU20bx25={\
"name" : "WJetsToLNu_HT600toInf",
"chunkString": "WJetsToLNu_HT600toInf",
'dir' : "/data/schoef/cmgTuples/v5_Phys14V2/",
'dbsName':'/WJetsToLNu_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
DYJetsToLL_M50_HT100to200_PU20bx25={\
"name" : "DYJetsToLL_M50_HT100to200",
"chunkString": "",
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_BkgsAndSig/DYJetsToLL_M50_HT100to200",
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/DYJetsToLL_M50_HT100to200/',
'fromDPM':True,
'dbsName':'/DYJetsToLL_M-50_HT-100to200_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
DYJetsToLL_M50_HT200to400_PU20bx25={\
"name" : "DYJetsToLL_M50_HT200to400",
"chunkString": "",
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_BkgsAndSig/DYJetsToLL_M50_HT200to400",
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/DYJetsToLL_M50_HT200to400/',
'fromDPM':True,
'dbsName':'/DYJetsToLL_M-50_HT-200to400_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
DYJetsToLL_M50_HT400to600_PU20bx25={\
"name" : "DYJetsToLL_M50_HT400to600",
"chunkString": "",
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_BkgsAndSig/DYJetsToLL_M50_HT400to600",
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/DYJetsToLL_M50_HT400to600/',
'fromDPM':True,
'dbsName':'/DYJetsToLL_M-50_HT-400to600_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
DYJetsToLL_M50_HT600toInf_PU20bx25={\
"name" : "DYJetsToLL_M50_HT600toInf",
"chunkString": "",
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_BkgsAndSig/DYJetsToLL_M50_HT600toInf",
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/DYJetsToLL_M50_HT600toInf/',
'fromDPM':True,
'dbsName':'/DYJetsToLL_M-50_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
QCD_HT_250To500_PU20bx25={\
"name" : "QCD_HT_250To500",
"chunkString": "",
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_BkgsAndSig/QCD_HT_250To500",
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/QCD_HT_250To500/',
'fromDPM':True,
'dbsName':'/QCD_HT_250To500_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
QCD_HT_500To1000_PU20bx25={\
"name" : "QCD_HT_500To1000",
"chunkString": "",
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_BkgsAndSig/QCD_HT_500To1000",
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/QCD_HT_500To1000/',
'fromDPM':True,
'dbsName':'/QCD_HT_500To1000_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
QCD_HT_1000ToInf_PU20bx25={\
"name" : "QCD_HT_1000ToInf",
"chunkString": "",
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_BkgsAndSig/QCD_HT_1000ToInf",
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/QCD_HT_1000ToInf/',
'fromDPM':True,
'dbsName':'/QCD_HT_1000ToInf_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT100to200_fromEOS={\
"name" : "WJetsToLNu_HT100to200",
"chunkString": "WJetsToLNu_HT100to200",
'dir' : "/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/",
'dbsName':'/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT200to400_fromEOS={\
"name" : "WJetsToLNu_HT200to400",
"chunkString": "WJetsToLNu_HT200to400",
'dir' : "/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/",
'dbsName':'/WJetsToLNu_HT-200to400_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT400to600_fromEOS={\
"name" : "WJetsToLNu_HT400to600",
"chunkString": "WJetsToLNu_HT400to600",
'dir' : "/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/",
'dbsName':'/WJetsToLNu_HT-400to600_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT600toInf_fromEOS={\
"name" : "WJetsToLNu_HT600toInf",
"chunkString": "WJetsToLNu_HT600toInf",
'dir' : "/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/",
'dbsName':'/WJetsToLNu_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
ttJets_fromEOS={\
"name" : "TTJets",
'chunkString' : 'TTJets',
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_TTJets/TTJets",
'dir' : "/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/",
'dbsName':'/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
#
allSignalData=[\
#["/data/nrad/cmgTuples/T2DegStop300_270", "T2DegStop_test"],
["/data/nrad/cmgTuples/T2DegStop300_270", "T2DegStop_300_270"],
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
  
