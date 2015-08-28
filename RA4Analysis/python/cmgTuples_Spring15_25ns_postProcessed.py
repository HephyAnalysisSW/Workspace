import copy, os, sys
#from StopsDilepton.tools.localInfo import dataDir
dir = '/data/rschoefbeck/cmgTuples/postProcessed_Spring15_25ns/HT400ST200/hard/' 
#"ZJetsToNuNu_HT-200To400_13TeV-madgraph_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
#"ZJetsToNuNu_HT-400To600_13TeV-madgraph_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
#"ZJetsToNuNu_HT-600ToInf_13TeV-madgraph_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",

TTJets_25ns={\
"name" : "tt+Jets",
"bins" : ["TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1"],
'dir' : dir,
}
WJetsHTToLNu_25ns={\
"name" : "W+Jets",
"bins" : [
"WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3",
"WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
],
'dir' : dir,
}

diBosons_25ns={\
"name" : "WW/WZ/ZZ",
"bins" : [
"WWTo2L2Nu_13TeV-powheg_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"ZZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3",
],
'dir' : dir,
}
singleTop_25ns={\
"name" : "single top",
"bins" : [
"ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
],
'dir' : dir,
}
DY_25ns={\
"name" : "DY",
"bins" : [
"DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
],
'dir' : dir,
}
DYM10to50_25ns={\
"name" : "DY M10-50",
"bins" : [
"DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
],
'dir' : dir,
}
QCDMu_25ns={\
"name" : "QCD (MuPt5 enriched)",
"bins" : [
"QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2"
],
'dir' : dir,
}


QCDEle_25ns={\
"name" : "QCD (Ele)",
"bins" : [
"QCD_Pt_15to20_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt_20to30_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt_30to80_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt_80to170_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt_170to250_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt_250toInf_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3",
"QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
"QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
],
'dir' : dir,
}

allSignalStrings=[\
"SMS_T2tt_2J_mStop425_mLSP325",
"SMS_T2tt_2J_mStop500_mLSP325",
"SMS_T2tt_2J_mStop650_mLSP325",
"SMS_T2tt_2J_mStop850_mLSP100",
]

def getSignalSample(signal):
  if signal in allSignalStrings:
    return {
      "name" : signal,
      #'dir' : dir,
      'dir' : "/afs/cern.ch/work/w/wvandrie/public/STOPS/CMSSW_7_4_7/src/CMGTools/TTHAnalysis/cfg/phys14/",
      'bins':[signal]}
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

allSignals=[]
for s in allSignalStrings:
  sm = getSignalSample(s)
  exec(s+"=sm")
  exec("allSignals.append(s)")
