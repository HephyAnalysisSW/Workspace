import copy, os, sys
#spring15_soft_sample_dir = "/data/nrad/cmgTuples/postProcessed_Spring15/"
#spring15_inc_sample_dir = "/data/nrad/cmgTuples/postProcessed_Spring15_vasile_v1/"


mc_path     = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v2/RunIISpring15DR74_25ns" 
signal_path = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v2/RunIISpring15DR74_25ns" 
data_path   = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v2/Data_25ns" 

class cmgTuplesPostProcessed():

    def makeSample(self, sample):
      i = copy.deepcopy(sample)
      i['dir']=i['dir']+'/inc/'
      s = copy.deepcopy(sample)
      s['dir']=s['dir']+'/preselection/inc/'
      return {'inc':i, 'presel':s}

    def getDataSample(self, name,sample ):
        s = self.makeSample({ 
                    "name" : name,
                    "bins" : [sample],
                    'dir' : self.data_path,
                        })
        return s

    def getSignalSample(self, signal):
      return {
          "name" : signal,
          "chunkString": signal,
          'dir' : self.signal_path,
          #'dir' : "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/mAODv2_v4_SMSScan_v1/RunIISpring15DR74_25ns",
          'bins':[signal]}

    def __init__(self, mc_path=mc_path, signal_path=signal_path, data_path=data_path):

        self.mc_path    =   mc_path
        self.signal_path=   signal_path
        self.data_path  =   data_path
    

        print "MC DIR:      ",   mc_path
        print "SIGNAL DIR:  ",   signal_path
        print "DATA DIR:    ",   data_path
        
        self.TTJetsInc=self.makeSample({\
        "name" : "TTJetsInc",
        #"bins" : ["TBarToLeptons_sch", "TBarToLeptons_tch", "TBar_tWch", "TToLeptons_sch", "TToLeptons_tch", "T_tWch"],
        "bins" : [
                    "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",  ## this has a lhehtincoming cut of 600
        ],
        'dir' : self.mc_path
        })
        
        self.TTJetsHTLow=self.makeSample({\
        "name" : "TTJetsHTLow",
        #"bins" : ["TBarToLeptons_sch", "TBarToLeptons_tch", "TBar_tWch", "TToLeptons_sch", "TToLeptons_tch", "T_tWch"],
        "bins" : [
                    "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",  ## this has a lhehtincoming cut of 600
        ],
        'dir' : self.mc_path+"/lheHTlow/"
        })
        
        self.TTJetsHTHigh=self.makeSample({\
        "name" : "TTJetsHTHigh",
        #"bins" : ["TBarToLeptons_sch", "TBarToLeptons_tch", "TBar_tWch", "TToLeptons_sch", "TToLeptons_tch", "T_tWch"],
        "bins" : [
                    "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
        ],
        'dir' : self.mc_path+"/lheHThigh/"
        })
        self.TTJetsHTRest=self.makeSample({\
        "name" : "TTJetsHT",
        #"bins" : ["TBarToLeptons_sch", "TBarToLeptons_tch", "TBar_tWch", "TToLeptons_sch", "TToLeptons_tch", "T_tWch"],
        "bins" : [
                    "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                    "TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                    "TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
        ],
        'dir' : self.mc_path 
        })
        
        
        
        
        
        
        
        
        self.WJetsHT=self.makeSample({\
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
        'dir' : self.mc_path
        })
        
        
        self.WJetsNoTauHT=self.makeSample({\
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
        'dir' : self.mc_path
        })
        
        
        self.WJetsTauHT=self.makeSample({\
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
        'dir' : self.mc_path
        })
        
        
        
        self.WJetsInc=self.makeSample({\
        "name" : "WJetsInc",
        "bins" : [
                    "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                ],
        'dir' : self.mc_path
        })
        
        
        
        self.WJetsTauInc=self.makeSample({\
        "name" : "WJetsTauInc",
        "bins" : [
                    "TauWJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                ],
        'dir' : self.mc_path
        })
        
        self.WJetsNoTauInc=self.makeSample({\
        "name" : "WJetsNoTauInc",
        "bins" : [
                    "NoTauWJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                ],
        'dir' : self.mc_path
        })
        
        
        self.QCD=self.makeSample({\
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
        'dir' : self.mc_path 
        })
        
        
        
        self.ZJetsHT=self.makeSample({\
        "name" : "ZJetsHT",
        "bins" :  [
                        "ZJetsToNuNu_HT-100To200_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                        "ZJetsToNuNu_HT-200To400_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                        "ZJetsToNuNu_HT-400To600_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                        "ZJetsToNuNu_HT-600ToInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2",
                  ] ,
        'dir' : self.mc_path 
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
        
        
        
        allData=[]
        for data in dataSamples:
            sample = self.getDataSample(*data )
            #exec('{name}=sample'.format(name=data[0]) )
            setattr(self,data[0],sample)
            #exec('{name}=sample'.format(name=data[0]) )
        
        
        
        
        
        allSignalStrings=[\
        "T2DegStop_300_270",
        "T2DegStop_300_290_FastSim",
        "T2DegStop_300_270_FastSim",
        "T2DegStop_300_240_FastSim",
        "T2tt_300_270_FastSim",
        ]
        
        
        for s in allSignalStrings:
          sm = self.makeSample(self.getSignalSample(s))
          #exec(s+"=sm")
          setattr(self,s,sm)
        
        
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
                                            'dir' : self.signal_path,
                                        }
        
        
        for sig in mass_scan:
            sm = self.makeSample(mass_scan[sig])
            #exec(sig+"=sm")
            setattr(self,sig,sm)
        
        
