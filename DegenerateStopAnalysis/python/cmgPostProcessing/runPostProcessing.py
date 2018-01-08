''' Run in multiprocessing the CMG post-processing script for the samples defined here.

https://docs.python.org/2/library/multiprocessing.html


You can get the number of Chunks for each data sample with:

for f in `ls -d *`; do echo "'"$f"'" ":" `ls -d $f/* | grep -c Chunk` ; done


'''

# imports python standard modules or functions

import os
import sys
import argparse
import logging
import tempfile
import subprocess
import pprint
import copy
import multiprocessing
import errno
import pickle
import pprint as pp
import importlib

# imports user modules or functions

import Workspace.DegenerateStopAnalysis.cmgPostProcessing.cmgPostProcessing_parser as cmgPostProcessing_parser
import Workspace.DegenerateStopAnalysis.tools.helpers as helpers

# logger
logger = logging.getLogger(__name__)
logger.propagate = False

pprint_cust = pprint.PrettyPrinter(indent=3, depth=5 , width=140)

def getSampleSets(args):
    
    cmgTuplesName = args.cmgTuples
    cmgTuplesFullName = 'Workspace.DegenerateStopAnalysis.samples.cmgTuples.' + cmgTuplesName

    try:
       cmgTuples = importlib.import_module(cmgTuplesFullName)
    except ImportError, err:
       print "\nImport error from {0} \n ".format(cmgTuplesFullName) + \
           "\nCorrect the name and re-run the script. \n Exiting."
       sys.exit()
    
    sampleSets = {
       'signals':{
                   'samples':[
                               'SMS_T2tt_genHT_160_genMET_80_mStop_275_mLSP_205',
                               'SMS_T2tt_genHT_160_genMET_80_mStop_350_mLSP_330',
                               'SMS_T2tt_genHT_160_genMET_80_mStop_400_mLSP_350'
                             ],
                   },
       'w600':{
                   'samples':   [
                                 'WJetsToLNu_HT600to800',
                                 'WJetsToLNu_HT600to800_ext',
                                ],

                   },
       'wjets_ht':{
                   'samples':   [
                                 'WJetsToLNu_HT70to100',
                                 'WJetsToLNu_HT100to200',
                                 'WJetsToLNu_HT100to200_ext',
                                 'WJetsToLNu_HT100to200_ext2',
                                 'WJetsToLNu_HT200to400',
                                 'WJetsToLNu_HT200to400_ext',
                                 'WJetsToLNu_HT200to400_ext2',
                                 'WJetsToLNu_HT400to600',
                                 'WJetsToLNu_HT400to600_ext',
                                 'WJetsToLNu_HT600to800',
                                 'WJetsToLNu_HT600to800_ext',
                                 'WJetsToLNu_HT800to1200',
                                 'WJetsToLNu_HT800to1200_ext',
                                 'WJetsToLNu_HT1200to2500',
                                 'WJetsToLNu_HT1200to2500_ext',
                                 'WJetsToLNu_HT2500toInf',
                                 'WJetsToLNu_HT2500toInf_ext',
                                ],

                   },
       'wjets':{
                   'samples':   [
                                 'WJetsToLNu',
                                 'WJetsToLNu_LO',
                                 'WJetsToLNu_HT70to100',
                                 'WJetsToLNu_HT100to200',
                                 'WJetsToLNu_HT100to200_ext',
                                 'WJetsToLNu_HT100to200_ext2',
                                 'WJetsToLNu_HT200to400',
                                 'WJetsToLNu_HT200to400_ext',
                                 'WJetsToLNu_HT200to400_ext2',
                                 'WJetsToLNu_HT400to600',
                                 'WJetsToLNu_HT400to600_ext',
                                 'WJetsToLNu_HT600to800',
                                 'WJetsToLNu_HT600to800_ext',
                                 'WJetsToLNu_HT800to1200',
                                 'WJetsToLNu_HT800to1200_ext',
                                 'WJetsToLNu_HT1200to2500',
                                 'WJetsToLNu_HT1200to2500_ext',
                                 'WJetsToLNu_HT2500toInf',
                                 'WJetsToLNu_HT2500toInf_ext',
                                ],

                   },

       'wjets_pt':{
                   'samples':   [
                                 'WJetsToLNu_Pt_100to250',
                                 'WJetsToLNu_Pt_100to250_ext',
                                 'WJetsToLNu_Pt_250to400',
                                 'WJetsToLNu_Pt_250to400_ext',
                                 'WJetsToLNu_Pt_400to600',
                                 'WJetsToLNu_Pt_400to600_ext',
                                 'WJetsToLNu_Pt_600toInf',
                                 'WJetsToLNu_Pt_600toInf_ext',
                                ],

                   },
       
       'ttjets':{
                   'samples':[
                               ## "TTJets_LO",
                               ## ["TTJets_LO",                "--skimGeneral=lheHTlow"],
                               ## ["TTJets_LO_HT600to800_ext", "--skimGeneral=lheHThigh"],
                               ## 'TTJets_LO_HT600to800_ext'       ,
                               ## "TTJets_LO_HT800to1200_ext"      ,
                               ## "TTJets_LO_HT1200to2500_ext"     ,
                               ## "TTJets_LO_HT2500toInf_ext"      ,

                               'TTJets_DiLepton'                ,
                               'TTJets_DiLepton_ext'            ,
                               'TTJets_SingleLeptonFromT'       ,
                               'TTJets_SingleLeptonFromT_ext'   ,
                               'TTJets_SingleLeptonFromTbar'    ,
                               'TTJets_SingleLeptonFromTbar_ext',
                               'TTJets'                         ,
                               'TT_pow'                         ,
                               'TT_pow_backup'                  ,
                             ],
                  },
       'ttjetslep':{
                   'samples':[
                               'TTJets_DiLepton'                ,
                               'TTJets_DiLepton_ext'            ,
                               'TTJets_SingleLeptonFromT'       ,
                               'TTJets_SingleLeptonFromT_ext'   ,
                               'TTJets_SingleLeptonFromTbar'    ,
                               'TTJets_SingleLeptonFromTbar_ext',
                             ],
                   },
       
       'ttx':{
                   'samples':[
                               'TTGJets',
                               'TTWToLNu_ext',
                               'TTWToLNu_ext2',
                               'TTWToQQ',
                               'TTW_LO',
                               'TTZToLLNuNu_m1to10',
                               'TTZToQQ',
                               'TTZ_LO',
                             ],
                   },
       
       'dyjets':{
                   'samples':[
                               #M50
                                "DYJetsToLL_M50_HT70to100"   ,
                                "DYJetsToLL_M50_HT100to200",
                                "DYJetsToLL_M50_HT100to200_ext",
                                "DYJetsToLL_M50_HT200to400",
                                "DYJetsToLL_M50_HT200to400_ext",
                                "DYJetsToLL_M50_HT400to600",
                                "DYJetsToLL_M50_HT400to600_ext",
                                "DYJetsToLL_M50_HT600to800"  ,
                                "DYJetsToLL_M50_HT800to1200" ,
                                "DYJetsToLL_M50_HT1200to2500",
                                "DYJetsToLL_M50_HT2500toInf" ,
                              

 
                               #M5to50
                               'DYJetsToLL_M5to50_HT100to200',
                               'DYJetsToLL_M5to50_HT100to200_ext',
                               'DYJetsToLL_M5to50_HT200to400',
                               'DYJetsToLL_M5to50_HT200to400_ext',
                               'DYJetsToLL_M5to50_HT400to600',
                               'DYJetsToLL_M5to50_HT600toInf',
                               'DYJetsToLL_M5to50_HT600toInf_ext',
                             ],
                   },
       
       'zjets':{
                   'samples':[
                              'ZJetsToNuNu_HT100to200',
                              'ZJetsToNuNu_HT100to200_ext',
                              'ZJetsToNuNu_HT200to400',
                              'ZJetsToNuNu_HT200to400_ext',
                              'ZJetsToNuNu_HT400to600',
                              'ZJetsToNuNu_HT400to600_ext',
                              'ZJetsToNuNu_HT600to800',
                              'ZJetsToNuNu_HT800to1200',
                              'ZJetsToNuNu_HT1200to2500',
                              'ZJetsToNuNu_HT1200to2500_ext',
                              'ZJetsToNuNu_HT2500toInf',
                             ]
                   },
       
       'z200':{
                   'samples':[
                              'ZJetsToNuNu_HT200to400',
                              'ZJetsToNuNu_HT200to400_ext',
                             ]
                   },
       
       'qcd':{
                   'samples':[
                               'QCD_HT50to100',
                               'QCD_HT100to200',
                               'QCD_HT200to300',
                               'QCD_HT200to300_ext',
                               'QCD_HT300to500',
                               'QCD_HT300to500_ext',
                               'QCD_HT500to700',
                               'QCD_HT500to700_ext',
                               'QCD_HT700to1000',
                               'QCD_HT700to1000_ext',
                               'QCD_HT1000to1500',
                               'QCD_HT1000to1500_ext',
                               'QCD_HT1500to2000',
                               'QCD_HT1500to2000_ext',
                               'QCD_HT2000toInf',
                               'QCD_HT2000toInf_ext'
                             ],
                   },
       
       'qcd_pt':{
                   'samples':[
                             ],
                   },
       
       'qcdpt_em':{
                   'samples':[
                             ],
                   },
       
       'vv':{
                   'samples':[
                               'WW',
                               'WZ',
                               'ZZ',
                             ],
                   },
       'vv_nlo':{
                   'samples':[
                               'WWTo2L2Nu',
                               'WWToLNuQQ',
                               'WWToLNuQQ_ext',
                               'WWTo1L1Nu2Q',
                               'ZZTo2L2Nu',
                               'ZZTo2L2Q',
                               'ZZTo2Q2Nu',
                               'ZZTo4L',
                               'WZTo1L3Nu',
                               'WZTo1L1Nu2Q',
                               'WZTo2L2Q',
                               'WZTo3LNu',
                               'WZTo3LNu_amcatnlo',
                             ],
                   },
       'other':{
                   'samples':[
                               'WW',
                               'WZ',
                               'ZZ',
                              ## 'TBar_tch',
                              ## #'TBarToLeptons_tch_powheg', 
                              ## 'T_tch',
                              ## #'TToLeptons_tch_powheg',
                              ## 'TBar_tWch',
                              ## 'T_tWch',

                               'T_tWch_ext',
                               'T_tch_powheg',
                               'TBar_tWch_ext', 
                               'TBar_tch_powheg',

                             ],
                   },
       
       
                                ############################
                                ############DATA############
                                ############################
       
      
       ### Re-miniAOD (03Feb) ###

      'data_met':{'samples':[
                              "MET_Run2016B_03Feb2017_v2",  "MET_Run2016D_03Feb2017" , "MET_Run2016F_03Feb2017" , "MET_Run2016H_03Feb2017_v2",
                              "MET_Run2016C_03Feb2017"   ,  "MET_Run2016E_03Feb2017" , "MET_Run2016G_03Feb2017" , "MET_Run2016H_03Feb2017_v3"  
                            ],
                 },

      'data_el':{ 'samples':[
                              "SingleElectron_Run2016B_03Feb2017_v2",  "SingleElectron_Run2016D_03Feb2017" , "SingleElectron_Run2016F_03Feb2017" , "SingleElectron_Run2016H_03Feb2017_v2",
                              "SingleElectron_Run2016C_03Feb2017"   ,  "SingleElectron_Run2016E_03Feb2017" , "SingleElectron_Run2016G_03Feb2017" , "SingleElectron_Run2016H_03Feb2017_v3",
                            ],
                },

      'data_mu':{ 'samples':[
                              "SingleMuon_Run2016B_03Feb2017_v2",  "SingleMuon_Run2016D_03Feb2017" , "SingleMuon_Run2016F_03Feb2017" , "SingleMuon_Run2016H_03Feb2017_v2",
                              "SingleMuon_Run2016C_03Feb2017"   ,  "SingleMuon_Run2016E_03Feb2017" , "SingleMuon_Run2016G_03Feb2017" , "SingleMuon_Run2016H_03Feb2017_v3",
                            ]
                },

      'data_jet':{'samples':[
                              "JetHT_Run2016B_03Feb2017_v2",  "JetHT_Run2016D_03Feb2017" , "JetHT_Run2016F_03Feb2017" , "JetHT_Run2016H_03Feb2017_v2",
                              "JetHT_Run2016C_03Feb2017"   ,  "JetHT_Run2016E_03Feb2017" , "JetHT_Run2016G_03Feb2017" , "JetHT_Run2016H_03Feb2017_v3",
                            ]
                 },

       ### Re-Reco (23 Sep) ### NOTE: H Re-Reco not available
       
       # MET PD
       'data_met_23Sep':{
                   'samples':[
                               "MET_Run2016B_23Sep2016", #NOTE: v3
                               "MET_Run2016C_23Sep2016",
                               "MET_Run2016D_23Sep2016",
                               "MET_Run2016E_23Sep2016",
                               "MET_Run2016F_23Sep2016",
                               "MET_Run2016G_23Sep2016",
                               "MET_Run2016H_PromptReco_v2",
                               "MET_Run2016H_PromptReco_v3",
                             ],
                      },
       
      
     
       # SingleElectron PD
       
       'data_el_23Sep':{
                   'samples':[
                               "SingleElectron_Run2016B_23Sep2016", #NOTE: v3
                               "SingleElectron_Run2016C_23Sep2016",
                               "SingleElectron_Run2016D_23Sep2016",
                               "SingleElectron_Run2016E_23Sep2016",
                               "SingleElectron_Run2016F_23Sep2016",
                               "SingleElectron_Run2016G_23Sep2016",
                               "SingleElectron_Run2016H_PromptReco_v2",
                               "SingleElectron_Run2016H_PromptReco_v3",
                             ],
                      },
       
       # SingleMuon PD
       
       'data_mu_23Sep':{
                   'samples':[
                               "SingleMuon_Run2016B_23Sep2016", #NOTE: v3
                               "SingleMuon_Run2016C_23Sep2016",
                               "SingleMuon_Run2016D_23Sep2016",
                               "SingleMuon_Run2016E_23Sep2016",
                               "SingleMuon_Run2016F_23Sep2016",
                               "SingleMuon_Run2016G_23Sep2016",
                               "SingleMuon_Run2016H_PromptReco_v2",
                               "SingleMuon_Run2016H_PromptReco_v3",
                             ],
                      },
       
       # JetHT PD
       'data_jet_23Sep':{
                   'samples':[
                               "JetHT_Run2016B_23Sep2016", #NOTE: v3
                               "JetHT_Run2016C_23Sep2016",
                               "JetHT_Run2016D_23Sep2016",
                               "JetHT_Run2016E_23Sep2016",
                               "JetHT_Run2016F_23Sep2016",
                               "JetHT_Run2016G_23Sep2016",
                               "JetHT_Run2016H_PromptReco_v2",
                               "JetHT_Run2016H_PromptReco_v3",
                             ],
                      },
       
       
       ### PromptReco (PR) ###
       
       # MET PD
       'data_met_PR':{
                   'samples':[
                               "MET_Run2016B_PromptReco_v2",
                               "MET_Run2016C_PromptReco_v2",
                               "MET_Run2016D_PromptReco_v2",
                               "MET_Run2016E_PromptReco_v2",
                               #"MET_Run2016F_PromptReco_v1",
                               "MET_Run2016G_PromptReco_v1",
                               "MET_Run2016H_PromptReco_v2",
                               "MET_Run2016H_PromptReco_v3",
                             ],
                      },
       
       # SingleElectron PD
       
       'data_el_PR':{
                   'samples':[
                               "SingleElectron_Run2016B_PromptReco_v2",
                               "SingleElectron_Run2016C_PromptReco_v2",
                               "SingleElectron_Run2016D_PromptReco_v2",
                               #"SingleElectron_Run2016E_PromptReco_v2",
                               #"SingleElectron_Run2016F_PromptReco_v1",
                               #"SingleElectron_Run2016G_PromptReco_v1",
                               "SingleElectron_Run2016H_PromptReco_v2",
                               "SingleElectron_Run2016H_PromptReco_v3",
                             ],
                   },
       
       # SingleMuon PD
       
       'data_mu_PR':{
                   'samples':[
                               "SingleMuon_Run2016B_PromptReco_v2",
                               "SingleMuon_Run2016C_PromptReco_v2",
                               "SingleMuon_Run2016D_PromptReco_v2",
                               "SingleMuon_Run2016E_PromptReco_v2",
                               "SingleMuon_Run2016F_PromptReco_v1",
                               "SingleMuon_Run2016G_PromptReco_v1",
                               "SingleMuon_Run2016H_PromptReco_v2",
                               "SingleMuon_Run2016H_PromptReco_v3",
                             ],
                   },
       
       # JetHT PD
       'data_jet_PR':{
                   'samples':[
                               #"JetHT_Run2016B_PromptReco_v2",
                               #"JetHT_Run2016C_PromptReco_v2",
                               #"JetHT_Run2016D_PromptReco_v2",
                               #"JetHT_Run2016E_PromptReco_v2",
                               #"JetHT_Run2016F_PromptReco_v1",
                               #"JetHT_Run2016G_PromptReco_v1",
                               "JetHT_Run2016H_PromptReco_v2",
                               "JetHT_Run2016H_PromptReco_v3",
                             ],
                      },

       
       # 2015 Data 
       'data_2015':{
                   'samples':[
                               "MET_Run2015D_05Oct",
                               "MET_Run2015D_v4",
                               "SingleElectron_Run2015D_05Oct",
                               "SingleElectron_Run2015D_v4",
                               "SingleMuon_Run2015D_05Oct",
                               "SingleMuon_Run2015D_v4",
                               ]},
    
         }
    
    
    ### Signal ###
    
    #mstops = [250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800]
    #dms    = [10, 20, 30, 40, 50, 60, 70, 80]
    
    def getSignalMassDict(args, signalSampleName):
    
        cmgTuplesName = args.cmgTuples
    
        cmgTuplesFullName = 'Workspace.DegenerateStopAnalysis.samples.cmgTuples.' + cmgTuplesName
        try:
           cmgTuples = importlib.import_module(cmgTuplesFullName)
        except ImportError, err:
           print "\nImport error from {0} \n ".format(cmgTuplesFullName) + \
               "\nCorrect the name and re-run the script. \n Exiting."
           sys.exit()
        
        cmgDir = cmgTuples.sample_path
    
        try:
            signalComponent = getattr(cmgTuples, signalSample )
            mass_dict_file  = signalComponent.get("mass_dict","")
            mass_dict       = pickle.load( file( mass_dict_file ))
        except:
            print "mass dict not found for %s"%signalSample
            mass_dict = {}

        return mass_dict
    
    
    
    
    signalOpts = ["--processEventVetoFastSimJets"]
    signalSamples = {
                        "SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1"    : {'opts': signalOpts , 'name':'T2tt'      } ,  
                        "SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1": {'opts': signalOpts , 'name':'T2bW'      } , 
                        #"SMS_T2tt_dM_10to80_genHT_160_genMET_80"              : {'opts': signalOpts , 'name':'T2tt_old'  } , ## This is the old signal before the mWMin fix... should only be for comparisons 
                    }
    
    
    for signalSample, signalSampleInfo in signalSamples.items():
        mass_dict = getSignalMassDict(args, signalSample)
    
        signalSets = {}
        opts = signalSampleInfo['opts']
        name = signalSampleInfo['name']
        for mstop in mass_dict.keys():
            signalSet =  {'samples': [[signalSample, '--processSignalScan', str(mstop), str(mlsp)] + opts for mlsp in mass_dict[mstop].keys()]}
            signalSets.update({"%s%s"%(name,mstop):signalSet})
        sampleSets.update(signalSets)
        
    
    mc_samps     = ['ttjetslep', 'wjets', 'qcd', 'dyjets', 'zjets', 'ttx', 'other']
    signal_samps = [x for x in sampleSets.keys() if 'T2tt' in x or 'T2bW' in x]
    data_samps   = ['data_met']#, 'data_el', 'data_mu', 'data_jet'
    
    all_samps = mc_samps #+ signal_samps # + data_samps #FIXME: mc and data cannot be run simulatneously
   
    composite_samp_definitions = {
                    'lepskimdata'      : ['data_el' , 'data_mu']            ,
                    'alldata'      : ['data_met', 'data_el', 'data_jet', 'data_mu']            ,
                    'all'      : mc_samps + signal_samps + data_samps              ,
                    'allmc'    : mc_samps + signal_samps              ,
                    'bkg'      : mc_samps              ,
                    'T2tt_old' : [x for x in sampleSets.keys() if 'T2tt_old' in x and "mWMin" not in x] ,
                    'T2tt'     : [x for x in sampleSets.keys() if 'T2tt'     in x and "T2tt_old" not in x    ]  ,
                    'T2bW'     : [x for x in sampleSets.keys() if 'T2bW'     in x    ],
                    'allsig'   : signal_samps,

                    'bkg_2'       : ['ttjetslep', 'wjets_ht', 'qcd', 'dyjets', 'zjets',  'other'],
                    'rest'     : ['ttx', 'zjets', 'wjets' ] 
                 }
    
     
    for composite_samp_name , composite_samples in composite_samp_definitions.iteritems() :
        composite_set = []
        for s in composite_samples:
            composite_set.extend(sampleSets[s]['samples'])
    
        sampleSets[composite_samp_name] = { 
                                'samples': composite_set 
                            }
        
    #
    return sampleSets


def get_parser():
    ''' Argument parser for running the post processing module.
    
    Include all the options from cmgPostProcessing_parser, which are also used in 
    cmgPostProcessing_v2 script.
    
    '''
        
    argParser = argparse.ArgumentParser(
        description="Argument parser for runPostProcessing",
        parents=[cmgPostProcessing_parser.get_parser()]
        )
        
    # define all arguments which are added on top of cmgPostProcessing_parser arguments
    # collect them in argsRun group
    
    argsRun = argParser.add_argument_group('argsRun')
    
    argsRun.add_argument('--sampleSet',
        action='store',
        type=str,
        default='ttjets',
        help="Set of samples to run the post processing on"
        )
        
    argsRun.add_argument('--numberOfProcesses',
        action='store',
        type=int,
        default='10',
        help="Number of processes to run in parallel"
        )

    argsRun.add_argument('--splitChunks',
        action='store',
        type=int,
        default=0,
        help="Split processing over chunks automatically. Argument is the size of the chunk splitting."
        )

    argsRun.add_argument('--batchScript',
        action='store_true',
        help="Create batch script"
        )
    
    argsRun.add_argument('--batchScriptName',
        action='store',
        type=str,
        default=None,
        help="Name of batch script"
        )

    argsRun.add_argument('--run',
        action='store_true',
        help="Run Post processing!"
        )
    
    return argParser, argsRun


def make_list_options(args, argsRun):
    ''' Create the list of options for post-processing script.
        
    The list of options is created from the arguments of the cmgPostProcessing_v2.py
    given on the command line for runPostProcessing and the default values of the cmgPostProcessing_v2.py 
    arguments (for arguments not given on the command line). 
    
    The arguments specific to runPostProcessing script only, given in argsRun group, are not considered.
    '''

    logger = logging.getLogger('runPostProcessing.make_list_options')

    options_list = []

    argsRunList = []
    for a in argsRun._group_actions:
        argsRunList.extend(a.option_strings)
        
    logger.debug("\n List of arguments from the argsRun group: \n %s \n", pprint_cust.pformat(argsRunList))
        
    for arg in vars(args):
        argWm = '--' + arg
        if argWm not in argsRunList:
            argValue = getattr(args, arg)
            if isinstance(argValue, bool):
                if argValue:
                    argWmStr = argWm
                else:
                    continue
            else:
                argWmStr = argWm + "={}".format(argValue)
                
            options_list.append(argWmStr)
           
    logger.debug("\n options_list: \n %s \n", pprint_cust.pformat(options_list))

    return options_list

def getSampleDir(args, sampleName):
    ''' Gets directory of CMG sample from the cmgTuples sample definition file. '''

    cmgTuplesName = args.cmgTuples

    cmgTuplesFullName = 'Workspace.DegenerateStopAnalysis.samples.cmgTuples.' + cmgTuplesName
    try:
       cmgTuples = importlib.import_module(cmgTuplesFullName)
    except ImportError, err:
       print "\nImport error from {0} \n ".format(cmgTuplesFullName) + \
           "\nCorrect the name and re-run the script. \n Exiting."
       sys.exit()
   
    sampleDict = {}
    for samp in cmgTuples.allComponents:
       sampleDict[samp['cmgName']] = samp

    try:
       path = sampleDict[sampleName]['dir']
    except KeyError:
       print "\nKey Error with {0} \n ".format(sampleName) + \
       "\nCheck if sample exists in {0} \n Exiting.".format(cmgTuples.__file__.replace(".pyc",".py"))
       sys.exit()
  
    return path


def countChunks(args, root_path, dpm_samples = None, sampleName = None):

    logger = logging.getLogger('runPostProcessing.countChunks')

    if args.readFromDPM:
        if type(sampleName) == type([]): #NOTE: fix for signal where sampleName is a list with options
            sampleName = sampleName[0]
        numChunksDict = {samp:len(dpm_samples.from_heppy_samplename(samp)['filesAndNorms'])  for samp in dpm_samples.heppy_sample_names}
        numChunks = numChunksDict[sampleName]
        maxChunk = numChunks
    else:
        if os.path.exists(root_path):
            chunkFiles = [f for f in os.listdir(root_path) if "Chunk" in f]

            try:
                # for CMG tuples, get a poor-man list of chunks (see getChunkIndex
                # for a proper way)
                chunkNumbers = [int(f.rsplit("Chunk_")[1]) for f in chunkFiles]
            except:
                # for step1 files it throws an exception, so set it to None as there every file is processed
                # separately, and 'chunk' in that context means the index of the
                # file in the list of files sorted after name
                chunkNumbers = None

        else:
            print "\nPath {0} does not exist. Exiting.".format(root_path)
            sys.exit()

        numChunks = len(chunkFiles)

        maxChunk = max(chunkNumbers) if chunkNumbers is not None else numChunks

    logger.debug(
        "\n Path \n {root_path} \n has {maxChunk} 'chunks' \n".format(
            root_path=root_path, maxChunk=maxChunk
        )
    )

    return maxChunk

def make_command(args, sampleSets, dpm_samples = None, options_list=[], procScript='cmgPostProcessing_v2.py', sample_paths=[]):
    ''' Create the final command for post-processing script.
    
    The command is created using the list of options, replacing the "--processSample=..." argument 
    with the sample specific argument. Optional arguments included in the "samples" definition  
    replace also the arguments from the list of options. 
    '''
    logger = logging.getLogger('runPostProcessing.make_command')
   
    sampleSet = args.sampleSet   
 
    commands = []
   
    for samp in sampleSets[sampleSet]['samples']:
        options_current = []
        extraOptions = []

        if type(samp) == type(""):
            sampName = samp
        elif type(samp) == type([]):
            sampName = samp[0]
            extraOptions = samp[1:]
        else:
            raise Exception("\nType not recognized for %s" % samp)
        
        logger.debug(
            "\nExtra options from sample definition for sample %s: \n %s \n",
            sampName, pprint_cust.pformat(extraOptions)
            )
    
        # add the arguments from options_list to options_current
        # if necessary, replace the existing arguments from options_list with the arguments from the file
        for idx, arg in enumerate(options_list):
            logger.trace ('\n argument: %s\n', arg)
            if 'processSample' in arg:
                options_current.append("--processSample={}".format(sampName))
                continue
            
            addOption = True
            for idxExtra, opt in enumerate(extraOptions):
                if (opt.split('=')[0]) == (arg.split('=')[0]):
                    if "'" in opt:
                        optWithArg = opt.translate(None, "'")
                    elif '"' in opt:
                        optWithArg = opt.translate(None, '"')
                    else:
                        optWithArg = opt
                                                            
                    options_current.append(optWithArg)
                    logger.trace (
                        '\n     added option from file: %s \n', optWithArg
                        ) 
                    addOption = False
                    
                    # check if next item is an option or an argument to an option, based on the first character ('-')
                    for idxExtraNext in range(idxExtra + 1, len(extraOptions)):
                        if extraOptions[idxExtraNext].startswith('-'):
                            break
                        else:
                            options_current.append(extraOptions[idxExtraNext])
                            logger.trace (
                                '\n     option with arguments: %s %s \n', 
                                optWithArg, 
                                extraOptions[idxExtraNext]
                                ) 
                else:
                    if opt not in options_current:
                        options_current.append(opt)
                        logger.trace (
                            '\n     added option from file: %s \n', opt
                            ) 
                                               
            if addOption:
                if not 'None' in arg:        
                    options_current.append(arg)
                    logger.trace (
                        '\n     added option from initial list: %s \n', arg
                        ) 
        commandPostProcessing = [
            'python',
            procScript,
            ]
        
        commandPostProcessing.extend(options_current)

        #Automatic chunk splitting
        chunkSplitting = args.splitChunks

        if '--processSignalScan' in commandPostProcessing: #NOTE: Hardcoded so that signal samples are not split in chunks (mass and size splitting should be sufficient)
            chunkSplitting = False
        
        if chunkSplitting:
              
           if sample_paths:
               sampDir = ''
               for s_path in sample_paths:
                   if s_path['sample'] == samp:
                       sampDir = s_path['samplePath']
           elif not args.readFromDPM:
               sampDir = getSampleDir(args, sampName) 
           else:    
               sampDir = ''
         
           maxChunk = countChunks(args, sampDir, dpm_samples, sampleName = samp)
           
           print "\n**********************************************************************************************************************************************************************************************************"
           print "\nSplitting post-processing of sample %s with %s chunks into %s chunk intervals.\n"%(sampName, maxChunk, chunkSplitting),
           print "Directory: ", sampDir 
           logger.info(
              "\nSplitting post-processing of sample %s with %s chunks into %s-chunk intervals.\nDirectory: %s"%(sampName, maxChunk, chunkSplitting, sampDir),
              )
           
           print "\nCommands:" 
              
           firstChunk = 0
           for n in range(maxChunk):
              
              baseCommand = commandPostProcessing[:]
              
              lastChunk = firstChunk + chunkSplitting - 1              
              baseCommand.extend(["--runChunks", str(firstChunk), str(lastChunk)])
              
              pprint_cust.pprint(" ".join(baseCommand))
              
              logger.info(
                  "\nCommand to be processed: \n %s \n",
                  pprint_cust.pformat(" ".join(baseCommand))
                  )
              
              commands.append(baseCommand)
              
              firstChunk = lastChunk + 1
              if firstChunk > maxChunk:
                  break
              
        else:
           
           print "\nCommands:" 
           
           pprint_cust.pprint(" ".join(commandPostProcessing))

           logger.info(
               "\nCommand to be processed: \n %s \n",
               pprint_cust.pformat(" ".join(commandPostProcessing))
               )

           commands.append(commandPostProcessing)
 
    return commands
    
def runPostProcessing(argv=None):
    
    if argv is None:
        argv = sys.argv[1:]

    # argument parser
    
    parser, argsRun = get_parser() 
    args = parser.parse_args()
    
    verbose = args.verbose
    
    cmgTuplesName = args.cmgTuples
    cmgTuplesFullName = 'Workspace.DegenerateStopAnalysis.samples.cmgTuples.' + cmgTuplesName

    try:
       cmgTuples = importlib.import_module(cmgTuplesFullName)
    except ImportError, err:
       print "\nImport error from {0} \n ".format(cmgTuplesFullName) + \
           "\nCorrect the name and re-run the script. \n Exiting."
       sys.exit()
    
    if args.readFromDPM:
        heppySamples = cmgTuples.getHeppyMap()
    else:
        heppySamples = None   
    
    # create the output top directory - here, it is used to write the logging messages
    # cmgPostProcessing_v2.py creates its own outputDirectory
    
    # WARNING: this directory must be in agreement with the directory created by  
    # cmgPostProcessing_v2.py
    
    outputDirectory = os.path.join(
        args.targetDir, 
        args.processingEra, args.cmgProcessingTag, args.cmgPostProcessingTag, 
        args.parameterSet, 'step1',
        args.cmgTuples
        )

    try:
        os.makedirs(outputDirectory)
        msg_logger_debug = \
            "\nRequested output directory \n {0} \n does not exist.".format(outputDirectory) + \
            "\nCreated new directory. \n"
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        else:
            msg_logger_debug = \
                "\nRequested output directory \n {0} \n already exists.\n".format(outputDirectory)

    # logging
    logLevel = args.logLevel
    
    # use a unique name for the log file, write file in the dataset directory
    prefixLogFile = 'runPostProcessing_' + args.sampleSet + \
         '_' + logLevel + '_'
    logFile = tempfile.NamedTemporaryFile(suffix='.log', prefix=prefixLogFile, dir=outputDirectory, delete=False) 

    get_logger_rtuple = helpers.get_logger('runPostProcessing', logLevel, logFile.name)
    logger = get_logger_rtuple.logger
    
    # get sampleSets
    sampleSets = getSampleSets(args)

    # check if the required sampleSet is defined in sampleSets
    if args.sampleSet not in sampleSets.keys():
        msg_exception = ''.join([
            "\n The requested sampleSet {sampleSet} is not defined in sampleSets".format(
                        sampleSet=args.sampleSet),
            "\n Available sampleSets: \n {sampleSets}".format(
                sampleSets=pprint_cust.pformat(sorted(sampleSets.keys())))
        ])

        print msg_exception
        raise Exception(msg_exception)
        sys.exit()
    

    if verbose:    
        print "{:-^80}".format(" Running Post Processing! ")
        print '\n Log file: ', logFile.name
        print "{:-^80}".format(" %s "%args.numberOfProcesses )
        print "\nSamples:"
        pprint_cust.pprint(sampleSets[args.sampleSet])
        print 
    
    
    logger.info(
        "\n runPostProcessing script arguments" + \
        "\n some arguments will be overwritten from sample definition: \n\n %s \n", 
        pprint.pformat(vars(args))
        )
    # write the debug message kept in the msg_logger_debug
    logger.debug(msg_logger_debug)
    

    logger.info("\n Samples: \n %s \n", pprint_cust.pformat(sampleSets[args.sampleSet]))

    options_list = make_list_options(args, argsRun)
    commands = make_command(args, sampleSets, heppySamples, options_list)
    
    logger.info(
        "\nFinal commands to be processed: \n %s \n",
        pprint_cust.pformat(commands)
        )

    if args.batchScript:
        if args.batchScriptName:
            fname = args.batchScriptName +".sh"
        else: 
            fname = "batchScript-%s-%s-%s.sh"%(args.cmgProcessingTag, args.cmgPostProcessingTag, args.sampleSet)
        
        print '%s written to current directory.'%fname
        
        f = file(fname, 'a')

        #new_commands = [] 
        #for c in commands:
        #    cset = set(c)
        #    new_commands.append(sorted(list(cset)))
        #commands = new_commands

        align_commands = False

        if align_commands:
            longest_command = max(commands, key = len)
            max_opt_lens = [1 for c in longest_command ]
            #print max_opt_lens
            #print commands[0]
            for i, c in enumerate(commands):
                for io, o in enumerate(c):
                    max_opt_lens[io] = max(len(o), max_opt_lens[io])
            #print max_opt_lens

            for c in commands:
                alignment_list = ['{:<%s}'%max_opt_lens[i] for i in range(len(c))]
                alignment = '  '.join(alignment_list)
                f.write(alignment.format(*c)+"\n")
        else:
            for c in commands:
                f.write('  '.join(c)+"\n")
        f.close()

    if args.run:
        pool = multiprocessing.Pool(processes=args.numberOfProcesses)
        results = pool.map(subprocess.call, commands)
        pool.close()
        pool.join()

        if verbose:    
            print "{:-^80}".format(" FIN ")
    else:
        # do not put this print unter verbose
        print "\nRun the script adding the option --run to actually run over the chosen sample.\n "
        
    logger.info(
        "\n" + \
        "\nEnd of runPostProcessing run on sample set %s. \n" + \
        "\n*******************************************************************************\n",
        args.sampleSet
        )

if __name__ == "__main__":
    sys.exit(runPostProcessing())
