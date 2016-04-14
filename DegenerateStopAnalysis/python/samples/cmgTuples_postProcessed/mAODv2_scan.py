import copy, os, sys
#spring15_soft_sample_dir = "/data/nrad/cmgTuples/postProcessed_Spring15/"
#spring15_inc_sample_dir = "/data/nrad/cmgTuples/postProcessed_Spring15_vasile_v1/"

 
MC_path     = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v2/RunIISpring15DR74_25ns" 
SIGNAL_path = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v2/RunIISpring15DR74_25ns" 
DATA_path   = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v2/Data_25ns" 
#MC_path = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_7412pass2_Preselection_v0"

#
#Luminosity with which the weight for the tuples was created
#
lumi = 10000    #pb-1

def makeSample(sample):
  i = copy.deepcopy(sample)
  i['dir']=i['dir']+'/inc/'
  s = copy.deepcopy(sample)
  s['dir']=s['dir']+'/preselection/inc/'
  return {'inc':i, 'presel':s}


TTJetsInc=makeSample({\
"name" : "TTJetsInc",
#"bins" : ["TBarToLeptons_sch", "TBarToLeptons_tch", "TBar_tWch", "TToLeptons_sch", "TToLeptons_tch", "T_tWch"],
"bins" : [
            "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",  ## this has a lhehtincoming cut of 600
],
'dir' : MC_path
})

TTJetsHTLow=makeSample({\
"name" : "TTJetsHTLow",
#"bins" : ["TBarToLeptons_sch", "TBarToLeptons_tch", "TBar_tWch", "TToLeptons_sch", "TToLeptons_tch", "T_tWch"],
"bins" : [
            "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",  ## this has a lhehtincoming cut of 600
],
'dir' : MC_path+"/lheHTlow/"
})

TTJetsHTHigh=makeSample({\
"name" : "TTJetsHTHigh",
#"bins" : ["TBarToLeptons_sch", "TBarToLeptons_tch", "TBar_tWch", "TToLeptons_sch", "TToLeptons_tch", "T_tWch"],
"bins" : [
            "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
],
'dir' : MC_path+"/lheHThigh/"
})
TTJetsHTRest=makeSample({\
"name" : "TTJetsHT",
#"bins" : ["TBarToLeptons_sch", "TBarToLeptons_tch", "TBar_tWch", "TToLeptons_sch", "TToLeptons_tch", "T_tWch"],
"bins" : [
            "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
],
'dir' : MC_path 
})








WJetsHT=makeSample({\
"name" : "WJetsHT",
"bins" : [
            "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            #"WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1 ",
            "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
        ],
'dir' : MC_path
})


WJetsNoTauHT=makeSample({\
"name" : "WJetsNoTauHT",
"bins" : [
            "NoTauWJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "NoTauWJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "NoTauWJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "NoTauWJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            #NoTau"WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1 ",
            "NoTauWJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "NoTauWJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "NoTauWJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
        ],
'dir' : MC_path
})


WJetsTauHT=makeSample({\
"name" : "WJetsTauHT",
"bins" : [
            "TauWJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "TauWJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "TauWJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "TauWJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            #Tau"WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1 ",
            "TauWJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "TauWJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "TauWJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
        ],
'dir' : MC_path
})



WJetsInc=makeSample({\
"name" : "WJetsInc",
"bins" : [
            "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
        ],
'dir' : MC_path
})



WJetsTauInc=makeSample({\
"name" : "WJetsTauInc",
"bins" : [
            "TauWJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
        ],
'dir' : MC_path
})

WJetsNoTauInc=makeSample({\
"name" : "WJetsNoTauInc",
"bins" : [
            "NoTauWJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
        ],
'dir' : MC_path
})


QCD=makeSample({\
"name" : "QCD",
"bins" :  [
            "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
          ], 
'dir' : MC_path 
})



ZJetsHT=makeSample({\
"name" : "ZJetsHT",
"bins" :  [
                "ZJetsToNuNu_HT-100To200_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                "ZJetsToNuNu_HT-200To400_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                "ZJetsToNuNu_HT-400To600_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                "ZJetsToNuNu_HT-600ToInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2",
          ] ,
'dir' : MC_path 
})




######################################################################################################
#####################################                  ###############################################
#####################################       DATA       ###############################################
#####################################                  ###############################################
######################################################################################################

dataSamples=[
              [  "MET_v4"      , "MET_Run2015D-PromptReco-v4"],
              [  "MET_Oct05"      , "MET_Run2015D-05Oct2015-v1"],
              [  "SingleMu_v4"      , "SingleMuon_Run2015D-PromptReco-v4"],
              [  "SingleMu_Oct05"      , "SingleMuon_Run2015D-05Oct2015-v1"],
              [  "SingleEl_v4"      , "SingleElectron_Run2015D-PromptReco-v4"],
              [  "SingleEl_Oct05"      , "SingleElectron_Run2015D-05Oct2015-v1"], 
            ]


def getDataSample(name,sample):
    s = makeSample({ 
                "name" : name,
                "bins" : [sample],
                'dir' : DATA_path,
                    })
    return s


allData=[]
for data in dataSamples:
    sample = getDataSample(*data)
    exec('{name}=sample'.format(name=data[0]) )




#T1qqqq_1400_325_300={\
#"name" : "T1qqqq_1400_325_300",
#"bins": ["T1qqqq_1400_325_300"],
#'dir' : "/data/easilar/cmgTuples/postProcessed_v0/singleLepton/",
#}
#
#T5Full_1200_1000_800={\
#"name" : "T5Full_1200_1000_800",
#"bins": ["T5Full_1200_1000_800"],
#'dir' : "/data/easilar/cmgTuples/postProcessed_v0/singleLepton/",
#}
#
#T5Full_1500_800_100={\
#"name" : "T5Full_1500_800_100",
#"bins": ["T5Full_1500_800_100"],
#'dir' : "/data/easilar/cmgTuples/postProcessed_v0/singleLepton/",
#}













#############################


allSignalStrings=[\
"T2DegStop_300_270",
"T2DegStop_300_290_FastSim",
"T2DegStop_300_270_FastSim",
"T2DegStop_300_240_FastSim",
"T2tt_300_270_FastSim",
]

def getSignalSample(signal):
  if signal in allSignalStrings:
    return {
      "name" : signal,
#      "chunkString": signal,
      'dir' : SIGNAL_path,
      #'dir' : "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/mAODv2_v4_SMSScan_v1/RunIISpring15DR74_25ns",
      'bins':[signal]}
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)



for s in allSignalStrings:
  sm = makeSample(getSignalSample(s))
  exec(s+"=sm")


import pickle
mass_dict_pickle = "/afs/hephy.at/user/n/nrad/CMSSW/fork/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/cmgPostProcessing/mass_dict_all.pkl"
mass_dict = pickle.load(open(mass_dict_pickle,"r"))
mass_scan={}
for mstop in mass_dict:
    for mlsp in mass_dict[mstop]:
        mass_point = "SMS_T2_4bd_mStop_%s_mLSP_%s"%(mstop,mlsp)
        mass_scan[mass_point] = {\
                                    "name" : mass_point,
                                    "bins": [mass_point],
                                    'dir' : SIGNAL_path,
                                }


for sig in mass_scan:
    sm = makeSample(mass_scan[sig])
    exec(sig+"=sm")


