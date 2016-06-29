''' Sample definition file for 2016 data and MC samples.

TODO Add the rest of the samples when available.
'''

import copy
import os
import sys
import pickle



# most recent paths, can be replaced when initializing the cmgTuplesPostProcessed class

mc_path = "/afs/hephy.at/data/vghete02/cmgTuples/postProcessed_mAODv2/8011_mAODv2_v0/80X_postProcessing_v1/analysisHephy_13TeV_2016_v0/step1/RunIISpring16MiniAODv2_v0"
signal_path = "/afs/hephy.at/data/vghete02/cmgTuples/postProcessed_mAODv2/8011_mAODv2_v0/80X_postProcessing_v1/analysisHephy_13TeV_2016_v0/step1/RunIISpring16MiniAODv2_v0"
data_path = "/afs/hephy.at/data/vghete02/cmgTuples/postProcessed_mAODv2/8011_mAODv2_v0/80X_postProcessing_v1/analysisHephy_13TeV_2016_v0/step1/Data2016_v0"

# Lumi that was used in the weight calculation of PostProcessing in pb-1
lumi_mc = 10000.

class cmgTuplesPostProcessed():

    def makeSample(self, sample):
        i = copy.deepcopy(sample)
        i['dir'] = os.path.join(i['dir'], 'inc')

        pold = copy.deepcopy(sample)
        pold['dir'] = os.path.join(pold['dir'], 'preselection', 'inc')

        p = copy.deepcopy(sample)
        p['dir'] = os.path.join(p['dir'], 'skimPreselect', 'inc')

        il = copy.deepcopy(sample)
        il['dir'] = os.path.join(il['dir'], 'incLep')

        ol = copy.deepcopy(sample)
        ol['dir'] = os.path.join(ol['dir'], 'oneLep')

        pil = copy.deepcopy(sample)
        pil['dir'] = os.path.join(pil['dir'], 'skimPreselect', 'incLep')

        pol = copy.deepcopy(sample)
        pol['dir'] = os.path.join(pol['dir'], 'skimPreselect', 'oneLep')

        return {
            'inc': i,
            'presel': pold,
            'skimPresel': p,
            'incLep': il,
            'oneLep': ol,
            'preIncLep': pil,
            'preOneLep':  pol
            }

    def getDataSample(self, name, sample):
        s = self.makeSample({
            "name" : name,
            "bins" : [sample],
            'dir' : self.data_path,
            })
        #
        return s

    def getSignalSample(self, signal, sampleId=0):
        return {
            "name" : signal,
            "chunkString": signal,
            'dir' : self.signal_path,
            'bins':[signal],
            'sampleId' : sampleId,
            }

    def __init__(self, mc_path=mc_path, signal_path=signal_path, data_path=data_path, lumi_mc=lumi_mc):

        self.mc_path = mc_path
        self.signal_path = signal_path
        self.data_path = data_path
        self.lumi = lumi_mc

        print "MC DIR:      ", self.mc_path
        print "SIGNAL DIR:  ", self.signal_path
        print "DATA DIR:    ", self.data_path


        self.TTJetsInc = self.makeSample({
            "name" : "TTJetsInc",
            "bins" : [
                "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",  # # this has a lhehtincoming cut of 600
                ],
            'dir' : self.mc_path,
            'sampleId' : 20,
            })

        self.TTJets_LO = self.TTJetsInc

        self.TTJetsHTLow = self.makeSample({
            "name" : "TTJetsHTLow",
            "bins" : [
                "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",  # # this has a lhehtincoming cut of 600
                ],
            'dir' : self.mc_path + "/lheHTlow/",
            'sampleId': 20,
            })

        self.TTJetsHTHigh = self.makeSample({
            "name" : "TTJetsHTHigh",
            "bins" : [
                "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
                ],
            'dir' : self.mc_path + "/lheHThigh/",
            'sampleId': 20,
            })

        self.TTJetsHTRest = self.makeSample({
            "name" : "TTJetsHT",
            "bins" : [
                "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
                "TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
                "TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
                ],
            'dir' : self.mc_path,
            'sampleId': 20,
            })


        self.WJetsHT = self.makeSample({
            "name" : "WJetsHT",
            "bins" : [
                    "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
                    "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
                    "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
                    "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
                    "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
                    "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1",
                    "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
                    "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
                    ],
            'dir' : self.mc_path,
            'sampleId' : 10,
            })

        self.WJetsToLNu_HT = self.WJetsHT


# FIXME definition of missing MC samples

        self.WJetsNoTauHT = self.makeSample({
        "name" : "WJetsNoTauHT",
        "bins" : [
#                     "NoTauWJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     "NoTauWJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     "NoTauWJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     "NoTauWJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     # NoTau"WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1 ",
#                     "NoTauWJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     "NoTauWJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     "NoTauWJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                ],
        'dir' : self.mc_path
        })


        self.WJetsTauHT = self.makeSample({
        "name" : "WJetsTauHT",
        "bins" : [
#                     "TauWJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     "TauWJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     "TauWJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     "TauWJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     # Tau"WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1 ",
#                     "TauWJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     "TauWJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     "TauWJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                ],
        'dir' : self.mc_path
        })



        self.WJetsInc = self.makeSample({
        "name" : "WJetsInc",
        "bins" : [
#                     "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                ],
        'dir' : self.mc_path,
        'sampleId': 10,
        })



        self.WJetsTauInc = self.makeSample({
        "name" : "WJetsTauInc",
        "bins" : [
#                     "TauWJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                ],
        'dir' : self.mc_path
        })

        self.WJetsNoTauInc = self.makeSample({
        "name" : "WJetsNoTauInc",
        "bins" : [
#                     "NoTauWJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                ],
        'dir' : self.mc_path
        })


        self.QCD = self.makeSample({
        "name" : "QCD",
        "bins" :  [
#                     "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                     "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
                  ],
        'dir' : self.mc_path,
        'sampleId' : 30,

        })



        self.QCDPT = self.makeSample({
        "name" : "QCDPT",
        "bins" :  [
#                     'QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
                  ],
        'dir' : self.mc_path
        })



        self.QCDPT_EM = self.makeSample({
        "name" : "QCDPT_EM",
        "bins" :  [

#                     'QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                     'QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',

                  ],
        'dir' : self.mc_path
        })


        self.ZJetsHT = self.makeSample({
        "name" : "ZJetsHT",
        "bins" :  [
#                         "ZJetsToNuNu_HT-100To200_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                         "ZJetsToNuNu_HT-200To400_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                         "ZJetsToNuNu_HT-400To600_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                         "ZJetsToNuNu_HT-600ToInf_13TeV-madgraph_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2",
                  ] ,
        'dir' : self.mc_path ,
        'sampleId': 40,
        })



        self.DYJetsM5to50HT = self.makeSample({
        "name" : "DYJetsM5to50HT",
        "bins" :  [
#                         "DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                         "DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                         "DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                         "DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
#                         # 'DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
                  ] ,
        'dir' : self.mc_path,
        })


        self.DYJetsM5to50 = self.makeSample({
        "name" : "DYJetsM5to50",
        "bins" :  [
#                         'DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
                  ] ,
        'dir' : self.mc_path
        })


        self.DYJetsM50HT = self.makeSample({
        "name" : "DYJetsM50HT",
        "bins" :  [
#                         'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                         'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
#                         'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2',
#                         'DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
                  ] ,
        'dir' : self.mc_path,
        'sampleId': 50,
        })


        self.DYJetsToNuNu = self.makeSample({
        "name" : "DYJetsToNuNu",
        "bins" :  [
#                         'DYJetsToNuNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1',
                  ] ,
        'dir' : self.mc_path
        })


        ######################################################################################################
        #####################################                  ###############################################
        #####################################       DATA       ###############################################
        #####################################                  ###############################################
        ######################################################################################################

        dataSamples = [
            ["MET_v2", "MET_Run2016B_PromptReco_v2"],
            ["SingleMu_v2", "SingleMuon_Run2016B_PromptReco_v2"],
            ["SingleEl_v2", "SingleElectron_Run2016B_PromptReco_v2"],
            ]

        allData = []
        for data in dataSamples:
            sample = self.getDataSample(*data)
            setattr(self, data[0], sample)


        # signal samples

        allSignalStrings = [
            "T2DegStop_300_270",
            "T2DegStop_300_290_FastSim",
            "T2DegStop_300_270_FastSim",
            "T2DegStop_300_240_FastSim",
            "T2tt_300_270_FastSim",
            ]

        for s in allSignalStrings:
            sm = self.makeSample(self.getSignalSample(s))
            setattr(self, s, sm)


        # mass_dict_pickle = "/afs/hephy.at/user/n/nrad/CMSSW/fork/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/cmgPostProcessing/mass_dict_all.pkl"

        mass_dict_pickle1 = "/data/nrad/cmgTuples/7412pass2_mAODv2_v6/RunIISpring15MiniAODv2//mass_dict.pkl"
        mass_dict_pickle2 = "/afs/hephy.at/work/n/nrad/results/mass_dicts/mass_dict.pkl"
        if os.path.isfile(mass_dict_pickle1):
            mass_dict_pickle = mass_dict_pickle1
        elif os.path.isfile(mass_dict_pickle2):
            mass_dict_pickle = mass_dict_pickle2
        else:
            print "!!!!! WARNING !!!!! NO MASS DICT FOUND!"
            mass_Dict_pickle = None

        mass_dict = pickle.load(open(mass_dict_pickle, "r"))

        self.mass_dict = mass_dict
        mass_scan = {}

        for mstop in mass_dict:
            for mlsp in mass_dict[mstop]:
                mass_point = "SMS_T2_4bd_mStop_%s_mLSP_%s" % (mstop, mlsp)
                mass_scan[mass_point] = {
                    "name" : mass_point,
                    "bins": [mass_point],
                    'dir' : self.signal_path,
                    'sampleId': "%s%s" % (mstop, mlsp)
                    }


        for sig in mass_scan:
            sm = self.makeSample(mass_scan[sig])
            setattr(self, sig, sm)


