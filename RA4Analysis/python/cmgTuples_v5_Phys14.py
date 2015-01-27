import copy, os, sys


ttJets_PU20bx25={\
"name" : "TTJets",
'chunkString' : '',
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_TTJets/TTJets",
'dir' : "/data/schoef/cmgTuples/v5_Phys14V1/TTJets",
'fromDPM':True,
'dbsName':'/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
ttWJets_PU20bx25={\
"name" : "TTWJets",
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_BkgsAndSig/TTWJets",
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/TTWJets',
'fromDPM':True,
'chunkString' : '',
'dbsName':'/TTWJets_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
ttZJets_PU20bx25={\
"name" : "TTZJets",
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_BkgsAndSig/TTZJets",
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/TTZJets',
'fromDPM':True,
'chunkString' : '',
'dbsName':'/TTZJets_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
ttH_PU20bx25={\
"name" : "TTH",
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_BkgsAndSig/TTH",
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/TTH/',
'fromDPM':True,
'chunkString' : '',
'dbsName':'/TTbarH_M-125_13TeV_amcatnlo-pythia8-tauola/Phys14DR-PU40bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT100to200_PU20bx25={\
"name" : "WJetsToLNu_HT100to200",
"chunkString": "WJetsToLNu_HT100to200",
'dir' : "/data/schoef/cmgTuples/v5_Phys14V1/",
'dbsName':'/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT200to400_PU20bx25={\
"name" : "WJetsToLNu_HT200to400",
"chunkString": "WJetsToLNu_HT200to400",
'dir' : "/data/schoef/cmgTuples/v5_Phys14V1/",
'dbsName':'/WJetsToLNu_HT-200to400_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT400to600_PU20bx25={\
"name" : "WJetsToLNu_HT400to600",
"chunkString": "WJetsToLNu_HT400to600",
'dir' : "/data/schoef/cmgTuples/v5_Phys14V1/",
'dbsName':'/WJetsToLNu_HT-400to600_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
WJetsToLNu_HT600toInf_PU20bx25={\
"name" : "WJetsToLNu_HT600toInf",
"chunkString": "WJetsToLNu_HT600toInf",
'dir' : "/data/schoef/cmgTuples/v5_Phys14V1/",
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
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/DYJetsToLL_M50_HT200to400_PU20bx25/',
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
TBarToLeptons_sChannel_PU20bx25={\
"name" : "TBarToLeptons_sChannel",
"chunkString": "",
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_BkgsAndSig/TBarToLeptons_sch",
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/TBarToLeptons_sch/',
'fromDPM':True,
'dbsName':'/TBarToLeptons_s-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
TBarToLeptons_tChannel_PU20bx25={\
"name" : "TBarToLeptons_tChannel",
"chunkString": "",
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_BkgsAndSig/TBarToLeptons_tch",
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/TBarToLeptons_tch/',
'fromDPM':True,
'dbsName':'/TBarToLeptons_t-channel_Tune4C_CSA14_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
TToLeptons_sChannel_PU20bx25={\
"name" : "TToLeptons_sChannel",
"chunkString": "",
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_BkgsAndSig/TToLeptons_sch",
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/TToLeptons_sch/',
'fromDPM':True,
'dbsName':'/TToLeptons_s-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
TToLeptons_tChannel_PU20bx25={\
"name" : "TToLeptons_tChannel",
"chunkString": "",
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_BkgsAndSig/TToLeptons_tch",
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/TToLeptons_tch/',
'fromDPM':True,
'dbsName':'/TToLeptons_t-channel_Tune4C_CSA14_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
T_tWChannel_PU20bx25={\
"name" : "",
"chunkString": "T_tWch",
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_BkgsAndSig/T_tWch",
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/T_tWch/',
'fromDPM':True,
'dbsName':'/T_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
TBar_tWChannel_PU20bx25={\
"name" : "TBar_tWChannel",
"chunkString": "",
#'dir' : "/dpm/oeaw.ac.at/home/cms/store/user/schoef/phys14_BkgsAndSig/TBar_tWch",
'dir': '/data/schoef/cmgTuples/v5_Phys14V2_fromDPM/TBar_tWch/',
'fromDPM':True,
'dbsName':'/Tbar_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
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
#
allSignalData=[\
["/data/schoef/cmgTuples/v5_Phys14V2/", "SMS_T5qqqqWW_Gl1500_Chi800_LSP100"],
["/data/schoef/cmgTuples/v5_Phys14V2/", "SMS_T5qqqqWW_Gl1200_Chi1000_LSP800"],
["/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/","SMS_T1tttt_2J_mGl1500_mLSP100"], 
["/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/","SMS_T1tttt_2J_mGl1200_mLSP800"], 
#["/data/schoef/cmgTuples/v5_Phys14V2/","SMS_T1tttt_2J_mGl1300_mLSP100"], 
#["/data/schoef/cmgTuples/v5_Phys14V2/","SMS_T1tttt_2J_mGl800_mLSP450"], 
["/data/schoef/cmgTuples/v5_Phys14V2/","SMS_T2tt_2J_mStop425_mLSP325"], 
["/data/schoef/cmgTuples/v5_Phys14V2/","SMS_T2tt_2J_mStop500_mLSP325"], 
["/data/schoef/cmgTuples/v5_Phys14V2/","SMS_T2tt_2J_mStop650_mLSP325"], 
["/data/schoef/cmgTuples/v5_Phys14V2/","SMS_T2tt_2J_mStop850_mLSP100"], 
#["/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/","SMS_T5qqqqWW_2J_mGo1400_mCh315_mChi300"], 
#["/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/","SMS_T6qqWW_mSq950_mChi325_mLSP300"], 
#["/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/","T1ttbb_mGo1500_mChi100"], 
["/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/","T1ttbbWW_mGo1000_mCh725_mChi715"], 
["/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/","T1ttbbWW_mGo1000_mCh725_mChi720"], 
["/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/","T1ttbbWW_mGo1300_mCh300_mChi290"], 
["/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/","T1ttbbWW_mGo1300_mCh300_mChi295"], 
["/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/","T5ttttDeg_mGo1000_mStop300_mCh285_mChi280"], 
["/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/","T5ttttDeg_mGo1000_mStop300_mChi280"], 
["/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/","T5ttttDeg_mGo1300_mStop300_mCh285_mChi280"], 
["/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/","T5ttttDeg_mGo1300_mStop300_mChi280"], 
#["/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/","T6ttWW_mSbot600_mCh425_mChi50"], 
#["/data/schoef/cmgTuples/v5_Phys14V2_fromEOS/","T6ttWW_mSbot650_mCh150_mChi50"], 
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
  
