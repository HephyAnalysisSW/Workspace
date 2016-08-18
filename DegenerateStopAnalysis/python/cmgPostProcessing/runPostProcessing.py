''' Run in multiprocessing the CMG post-processing script for the samples defined here.

https://docs.python.org/2/library/multiprocessing.html
'''

# imports python standard modules or functions

import argparse
import logging
import tempfile
import subprocess
import pprint
import copy
import multiprocessing
import errno
import os
import sys

# imports user modules or functions

import Workspace.DegenerateStopAnalysis.cmgPostProcessing.cmgPostProcessing_parser as cmgPostProcessing_parser
import Workspace.DegenerateStopAnalysis.tools.helpers as helpers

#

pprint_cust = pprint.PrettyPrinter(indent=3, depth=5 , width=140)


sampleSets = {
                'signals':{
                            'samples':[ 
                                        ["T2tt_300_270_FastSim",       "--skimPreselect"],
                                        ["T2DegStop_300_270",          "--skimPreselect"],
                                        ["T2DegStop_300_290_FastSim",  "--skimPreselect"],
                                        ["T2DegStop_300_240_FastSim",  "--skimPreselect"],
                                        ["T2DegStop_300_270_FastSim",  "--skimPreselect"],
                                      ],
                            },

                'wjets':{
                            'samples':[
                                        ["WJetsToLNu_HT100to200_ext",  "--skimPreselect"],
                                        ["WJetsToLNu_HT200to400",      "--skimPreselect"],
                                        ["WJetsToLNu_HT200to400_ext",  "--skimPreselect"],
                                        ["WJetsToLNu_HT400to600",      "--skimPreselect"],
                                        ["WJetsToLNu_HT600to800",      "--skimPreselect"],
                                        ["WJetsToLNu_HT800to1200_ext", "--skimPreselect"],
                                        ["WJetsToLNu_HT1200to2500",    "--skimPreselect"],
                                        ["WJetsToLNu_HT2500toInf",     "--skimPreselect"],
                                      ],
                            },
                
                'wjets_onelep':{
                            'samples':[
                                        ["WJetsToLNu_HT100to200_ext",  "--skimLepton=oneLep", "--runChunks", "0",   "100"],
                                        ["WJetsToLNu_HT100to200_ext",  "--skimLepton=oneLep", "--runChunks", "101", "200"],
                                        ["WJetsToLNu_HT100to200_ext",  "--skimLepton=oneLep", "--runChunks", "201", "300"],
                                        ["WJetsToLNu_HT100to200_ext",  "--skimLepton=oneLep", "--runChunks", "301", "300"],
                                        ["WJetsToLNu_HT100to200_ext",  "--skimLepton=oneLep", "--runChunks", "401", "500"],
                                        ["WJetsToLNu_HT100to200_ext",  "--skimLepton=oneLep", "--runChunks", "501", "600"],
                                        ["WJetsToLNu_HT100to200_ext",  "--skimLepton=oneLep", "--runChunks", "601", "700"],
                                        
                                        ["WJetsToLNu_HT200to400",      "--skimLepton=oneLep"],
                                        ["WJetsToLNu_HT200to400_ext",  "--skimLepton=oneLep", "--runChunks", "0",   "100"],
                                        ["WJetsToLNu_HT200to400_ext",  "--skimLepton=oneLep", "--runChunks", "101", "200"],
                                        ["WJetsToLNu_HT200to400_ext",  "--skimLepton=oneLep", "--runChunks", "201", "300"],
                                        ["WJetsToLNu_HT200to400_ext",  "--skimLepton=oneLep", "--runChunks", "301", "400"],
                                        
                                        ["WJetsToLNu_HT400to600",      "--skimLepton=oneLep"],
                                        ["WJetsToLNu_HT600to800",      "--skimLepton=oneLep"],
                                        ["WJetsToLNu_HT800to1200_ext", "--skimLepton=oneLep"],
                                        ["WJetsToLNu_HT1200to2500",    "--skimLepton=oneLep"],
                                        ["WJetsToLNu_HT2500toInf",     "--skimLepton=oneLep"],
                                      ],
                            },
                
                'ttjets':{
                            'samples':[
                                        ["TTJets_LO",                   "--skimPreselect"],
                                        ["TTJets_LO",                   "--skimPreselect",    "--skimGeneral=lheHTlow" ],
                                        ["TTJets_LO_HT600to800_ext",    "--skimPreselect",    "--skimGeneral=lheHThigh"],
                                        ["TTJets_LO_HT800to1200_ext",   "--skimPreselect"],
                                        ["TTJets_LO_HT1200to2500_ext",  "--skimPreselect"],
                                        ["TTJets_LO_HT2500toInf",       "--skimPreselect"],
                                      ],
                            },
                
                'ttjets_onelep':{
                            'samples':[
                                        ["TTJets_LO",                   "--skimLepton=oneLep", "--runChunks", "0",   "100"],
                                        ["TTJets_LO",                   "--skimLepton=oneLep", "--runChunks", "101", "200"],
                                        ["TTJets_LO",                   "--skimLepton=oneLep", "--runChunks", "201", "300"],
                                        
                                        ["TTJets_LO",                   "--skimLepton=oneLep",   "--skimGeneral=lheHTlow" ],
                                        ["TTJets_LO_HT600to800_ext",    "--skimLepton=oneLep",   "--skimGeneral=lheHThigh"],
                                        
                                        ["TTJets_LO_HT800to1200_ext",   "--skimLepton=oneLep", "--runChunks", "0",   "100"],
                                        ["TTJets_LO_HT800to1200_ext",   "--skimLepton=oneLep", "--runChunks", "101", "200"],
                                        ["TTJets_LO_HT800to1200_ext",   "--skimLepton=oneLep", "--runChunks", "201", "300"],
                                        
                                        ["TTJets_LO_HT1200to2500_ext",  "--skimLepton=oneLep"],
                                        ["TTJets_LO_HT2500toInf",       "--skimLepton=oneLep"],
                                      ],
                            },
                
                'ttjets_lep':{
                            'samples':[
                                        ["TTJets_SingleLeptonFromT",    "--skimPreselect"],
                                        ["TTJets_SingleLeptonFromTbar", "--skimPreselect"],
                                        ["TTJets_DiLepton",             "--skimPreselect"],
                                      ],
                            },
                
                'dyjets':{
                            'samples':[
                                        ['DYJetsToLL_M50_HT100to200_ext',    "--skimPreselect"],
                                        ['DYJetsToLL_M50_HT200to400_ext',    "--skimPreselect"],
                                        ['DYJetsToLL_M50_HT400to600_ext',    "--skimPreselect"],
                                        ['DYJetsToLL_M50_HT600toInf',        "--skimPreselect"],
                                        ['DYJetsToLL_M50_HT600toInf_ext',    "--skimPreselect"],

                                        ['DYJetsToLL_M5to50_HT100to200',     "--skimPreselect"],
                                        ['DYJetsToLL_M5to50_HT100to200_ext', "--skimPreselect"],
                                        ['DYJetsToLL_M5to50_HT200to400',     "--skimPreselect"],
                                        ['DYJetsToLL_M5to50_HT200to400_ext', "--skimPreselect"],
                                        ['DYJetsToLL_M5to50_HT400to600',     "--skimPreselect"],
                                        ['DYJetsToLL_M5to50_HT600toInf',     "--skimPreselect"],
                                        ['DYJetsToLL_M5to50_HT600toInf_ext', "--skimPreselect"],
                                      ],
                            },
                
                'dyjets_onelep':{
                            'samples':[
                                        ['DYJetsToLL_M50_HT100to200_ext', "--skimLepton=oneLep", "--runChunks", "0",   "100"],
                                        ['DYJetsToLL_M50_HT100to200_ext', "--skimLepton=oneLep", "--runChunks", "101", "200"],
                                        
                                        ['DYJetsToLL_M50_HT200to400_ext', "--skimLepton=oneLep", "--runChunks", "0",   "100"],
                                        ['DYJetsToLL_M50_HT200to400_ext', "--skimLepton=oneLep", "--runChunks", "101", "200"],
                                        ['DYJetsToLL_M50_HT200to400_ext', "--skimLepton=oneLep", "--runChunks", "201", "300"],
                                        
                                        ['DYJetsToLL_M50_HT400to600_ext', "--skimLepton=oneLep", "--runChunks", "0",   "100"],
                                        ['DYJetsToLL_M50_HT400to600_ext', "--skimLepton=oneLep", "--runChunks", "101", "200"],
                                        
                                        ['DYJetsToLL_M50_HT600toInf',     "--skimLepton=oneLep"],
                                        ['DYJetsToLL_M50_HT600toInf_ext', "--skimLepton=oneLep"],

                                        ['DYJetsToLL_M5to50_HT100to200',     "--skimLepton=oneLep"],
                                        ['DYJetsToLL_M5to50_HT100to200_ext', "--skimLepton=oneLep"],
                                        ['DYJetsToLL_M5to50_HT200to400',     "--skimLepton=oneLep"],
                                        ['DYJetsToLL_M5to50_HT200to400_ext', "--skimLepton=oneLep"],
                                        ['DYJetsToLL_M5to50_HT400to600',     "--skimLepton=oneLep"],
                                        ['DYJetsToLL_M5to50_HT600toInf',     "--skimLepton=oneLep"],
                                        ['DYJetsToLL_M5to50_HT600toInf_ext', "--skimLepton=oneLep"],
                                      ],
                            },


                'zjets':{
                            'samples':[ 
                                        ["ZJetsToNuNu_HT100to200_ext",    "--skimPreselect"],  
                                        ["ZJetsToNuNu_HT200to400_ext",    "--skimPreselect"],  
                                        ["ZJetsToNuNu_HT400to600",        "--skimPreselect"],  
                                        ["ZJetsToNuNu_HT600to800",        "--skimPreselect"],  
                                        ["ZJetsToNuNu_HT800to1200",       "--skimPreselect"],  
                                        ["ZJetsToNuNu_HT1200to2500",      "--skimPreselect"],      
                                        ["ZJetsToNuNu_HT1200to2500_ext",  "--skimPreselect"],      
                                        ["ZJetsToNuNu_HT2500toInf",       "--skimPreselect"],  
                                      ],
                            },
                'qcd':{
                            'samples':[

                                        ["QCD_HT300to500",       "--skimPreselect"],  
                                        ["QCD_HT300to500_ext",   "--skimPreselect"],  
                                        ["QCD_HT500to700_ext",   "--skimPreselect"],  
                                        ["QCD_HT700to1000",      "--skimPreselect"], 
                                        ["QCD_HT700to1000_ext",  "--skimPreselect"], 
                                        ["QCD_HT1000to1500",     "--skimPreselect"],
                                        ["QCD_HT1000to1500_ext", "--skimPreselect"],
                                        ["QCD_HT1500to2000",     "--skimPreselect"],
                                        ["QCD_HT1500to2000_ext", "--skimPreselect"],
                                        ["QCD_HT2000toInf",      "--skimPreselect"], 
                                        ["QCD_HT2000toInf_ext",  "--skimPreselect"], 
                                      ],
                             
                            },

                'qcd_onelep':{
                            'samples':[

                                        ["QCD_HT300to500",       "--skimLepton=oneLep"],  
                                        ["QCD_HT300to500_ext",   "--skimLepton=oneLep"],  
                                        ["QCD_HT500to700_ext",   "--skimLepton=oneLep"],  
                                        ["QCD_HT700to1000",      "--skimLepton=oneLep"], 
                                        ["QCD_HT700to1000_ext",  "--skimLepton=oneLep"], 
                                        ["QCD_HT1000to1500",     "--skimLepton=oneLep"],
                                        ["QCD_HT1000to1500_ext", "--skimLepton=oneLep"],
                                        ["QCD_HT1500to2000",     "--skimLepton=oneLep"],
                                        ["QCD_HT1500to2000_ext", "--skimLepton=oneLep"],
                                        ["QCD_HT2000toInf",      "--skimLepton=oneLep"], 
                                        ["QCD_HT2000toInf_ext",  "--skimLepton=oneLep"], 
                                      ],
                             
                            },
                'qcdpt':{
                            'samples':[
                                        #["QCD_Pt5to10",     "--skimPreselect"],
                                        #["QCD_Pt10to15",    "--skimPreselect"],
                                        ["QCD_Pt15to30",     "--skimPreselect"],
                                        ["QCD_Pt30to50",     "--skimPreselect"],
                                        ["QCD_Pt50to80",     "--skimPreselect"],
                                        ["QCD_Pt80to120",    "--skimPreselect"],
                                        ["QCD_Pt120to170",   "--skimPreselect"],
                                        ["QCD_Pt170to300",   "--skimPreselect"],
                                        ["QCD_Pt300to470",   "--skimPreselect"],
                                        ["QCD_Pt470to600",   "--skimPreselect"],
                                        ["QCD_Pt600to800",   "--skimPreselect"],
                                        ["QCD_Pt800to1000",  "--skimPreselect"],
                                        ["QCD_Pt1000to1400", "--skimPreselect"],
                                        ["QCD_Pt1400to1800", "--skimPreselect"],
                                        ["QCD_Pt1800to2400", "--skimPreselect"],
                                        ["QCD_Pt2400to3200", "--skimPreselect"],
                                        #["QCD_Pt3200toInf", "--skimPreselect"],
                                      ],
                            },
              
                'qcdpt_em':{
                            'samples':[
                                        ['QCD_Pt15to20_EMEnriched',   "--skimPreselect"],
                                        ['QCD_Pt20to30_EMEnriched',   "--skimPreselect"],
                                        ['QCD_Pt30to50_EMEnriched',   "--skimPreselect"],
                                        ['QCD_Pt50to80_EMEnriched',   "--skimPreselect"],
                                        ['QCD_Pt80to120_EMEnriched',  "--skimPreselect"],
                                        ['QCD_Pt120to170_EMEnriched', "--skimPreselect"],
                                        ['QCD_Pt170to300_EMEnriched', "--skimPreselect"],
                                        ['QCD_Pt300toInf_EMEnriched', "--skimPreselect"],
                                      ],
                            },
              
                'other':{
                            'samples':[
                                        ['WW',                       "--skimPreselect"],
                                        ['WZ',                       "--skimPreselect"],
                                        ['ZZ',                       "--skimPreselect"],
                                        ['TBar_tch',                 "--skimPreselect"],
                                        ['TBarToLeptons_tch_powheg', "--skimPreselect"],
                                        ['T_tch',                    "--skimPreselect"],
                                        ['TToLeptons_tch_powheg',    "--skimPreselect"],
                                        ['TBar_tWch',                "--skimPreselect"],
                                        ['T_tWch',                   "--skimPreselect"],
                                      ],
                            },

                'other_onelep':{
                            'samples':[
                                        ['WW',                       "--skimLepton=oneLep"],
                                        ['WZ',                       "--skimLepton=oneLep"],
                                        ['ZZ',                       "--skimLepton=oneLep"],
                                        ['TBar_tch',                 "--skimLepton=oneLep"],
                                        ['TBarToLeptons_tch_powheg', "--skimLepton=oneLep"],
                                        ['T_tch',                    "--skimLepton=oneLep"],
                                        ['TToLeptons_tch_powheg',    "--skimLepton=oneLep"],
                                        ['TBar_tWch',                "--skimLepton=oneLep"],
                                        ['T_tWch',                   "--skimLepton=oneLep"],
                                      ],
                            },

                                      ############################
                                      ############DATA############
                                      ############################
                
                'data_2015':{
                            'samples':[
                                        "MET_Run2015D_05Oct",
                                        "MET_Run2015D_v4",
                                        "SingleElectron_Run2015D_05Oct",
                                        "SingleElectron_Run2015D_v4",   
                                        "SingleMuon_Run2015D_05Oct",    
                                        "SingleMuon_Run2015D_v4",       
                                        ],
                             
                            },

                'data':{
                            'samples':[
                                        #"SingleMuon_Run2016B_PromptReco_v2",
                                        #"SingleElectron_Run2016B_PromptReco_v2",
                                        #"MET_Run2016B_PromptReco_v2",
                                        #"SingleMuon_Run2016C_PromptReco_v2",
                                        #"SingleElectron_Run2016C_PromptReco_v2",
                                        #"MET_Run2016C_PromptReco_v2",
                                        "SingleMuon_Run2016D_PromptReco_v2",
                                        "SingleElectron_Run2016D_PromptReco_v2",
                                        "MET_Run2016D_PromptReco_v2",
                                      ],
                            },




                'data_met':{
                            'samples':[
                                        ["MET_Run2016B_PromptReco_v2", "--skimPreselect"],
                                        ["MET_Run2016C_PromptReco_v2", "--skimPreselect"],
                                        ["MET_Run2016D_PromptReco_v2", "--skimPreselect"],
                                      ],
                            },



                'data_met_b':{
                            'samples':[
                                        ["MET_Run2016B_PromptReco_v2",   "--skimPreselect",   "--runChunks", "0",    "200"], 
                                        ["MET_Run2016B_PromptReco_v2",   "--skimPreselect",   "--runChunks", "201",  "400"], 
                                        ["MET_Run2016B_PromptReco_v2",   "--skimPreselect",   "--runChunks", "401",  "600"], 
                                        ["MET_Run2016B_PromptReco_v2",   "--skimPreselect",   "--runChunks", "601",  "800"], 
                                        ["MET_Run2016B_PromptReco_v2",   "--skimPreselect",   "--runChunks", "801",  "1000"], 
                                        ["MET_Run2016B_PromptReco_v2",   "--skimPreselect",   "--runChunks", "1001", "1200"], 
                                      ]},
                
                'data_met_c':{
                            'samples':[
                                        ["MET_Run2016C_PromptReco_v2",   "--skimPreselect",    "--runChunks", "0",   "100"],     
                                        ["MET_Run2016C_PromptReco_v2",   "--skimPreselect",    "--runChunks", "101", "200"],     
                                        ["MET_Run2016C_PromptReco_v2",   "--skimPreselect",    "--runChunks", "201", "300"],     
                                        ["MET_Run2016C_PromptReco_v2",   "--skimPreselect",    "--runChunks", "301", "400"],     
                                      ]},
                
                'data_met_d':{
                            'samples':[
                                        ["MET_Run2016D_PromptReco_v2",   "--skimPreselect",    "--runChunks", "0",   "100"],     
                                        ["MET_Run2016D_PromptReco_v2",   "--skimPreselect",    "--runChunks", "101", "200"],     
                                        ["MET_Run2016D_PromptReco_v2",   "--skimPreselect",    "--runChunks", "201", "300"],     
                                        ["MET_Run2016D_PromptReco_v2",   "--skimPreselect",    "--runChunks", "301", "400"],     
                                        ["MET_Run2016D_PromptReco_v2",   "--skimPreselect",    "--runChunks", "401", "500"],     
                                        ["MET_Run2016D_PromptReco_v2",   "--skimPreselect",    "--runChunks", "501", "600"],     
                                      ]},






                
                'data_mu':{
                            'samples':[
                                        "SingleMuon_Run2016B_PromptReco_v2",
                                        "SingleMuon_Run2016C_PromptReco_v2",
                                        "SingleMuon_Run2016D_PromptReco_v2",
                                      ],
                            },
                
                'data_el':{
                            'samples':[
                                        "SingleElectron_Run2016B_PromptReco_v2",
                                        "SingleElectron_Run2016C_PromptReco_v2",
                                        "SingleElectron_Run2016D_PromptReco_v2",
                                      ],
                            },

                'data_onelep':{
                            'samples':[
                                        ["SingleMuon_Run2016B_PromptReco_v2",     "--skimLepton=oneLep"], 
                                        ["SingleElectron_Run2016B_PromptReco_v2", "--skimLepton=oneLep"],    
                                        ["MET_Run2016B_PromptReco_v2",            "--skimLepton=oneLep"], 
                                        ["SingleMuon_Run2016C_PromptReco_v2",     "--skimLepton=oneLep"], 
                                        ["SingleElectron_Run2016C_PromptReco_v2", "--skimLepton=oneLep"],    
                                        ["MET_Run2016C_PromptReco_v2",            "--skimLepton=oneLep"],     
                                        ["SingleMuon_Run2016D_PromptReco_v2",     "--skimLepton=oneLep"], 
                                        ["SingleElectron_Run2016D_PromptReco_v2", "--skimLepton=oneLep"],    
                                        ["MET_Run2016D_PromptReco_v2",            "--skimLepton=oneLep"],     
                                      ],
                            },

                'data_mu_b_onelep':{
                            'samples':[
                                        ["SingleMuon_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "0" ,   "200" ], 
                                        ["SingleMuon_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "201",  "400" ], 
                                        ["SingleMuon_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "401",  "600" ], 
                                        ["SingleMuon_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "601",  "800" ],
                                        ["SingleMuon_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "801",  "1000"], 
                                        ["SingleMuon_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "1001", "1200"], 
                                      ]},
                
                'data_mu_c_onelep':{
                            'samples':[
                                        ["SingleMuon_Run2016C_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "0",   "100"], 
                                        ["SingleMuon_Run2016C_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "101", "200"], 
                                        ["SingleMuon_Run2016C_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "201", "300"], 
                                        ["SingleMuon_Run2016C_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "301", "400"], 
                                      ]},
                
                'data_mu_d_onelep':{
                            'samples':[
                                        ["SingleMuon_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "0",   "100"],     
                                        ["SingleMuon_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "101", "200"],     
                                        ["SingleMuon_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "201", "300"],     
                                        ["SingleMuon_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "301", "400"],     
                                        ["SingleMuon_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "401", "500"],     
                                        ["SingleMuon_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "501", "600"],     
                                     ]},
                
                'data_el_b_onelep':{
                            'samples':[
                                        ["SingleElectron_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "0",    "200"],    
                                        ["SingleElectron_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "201",  "400"],    
                                        ["SingleElectron_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "401",  "600"],    
                                        ["SingleElectron_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "601",  "800"],    
                                        ["SingleElectron_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "801",  "1000"],    
                                        ["SingleElectron_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "1001", "1200"],    
                                      ]},
                
                'data_el_c_onelep':{
                            'samples':[
                                        ["SingleElectron_Run2016C_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "0",   "100"],    
                                        ["SingleElectron_Run2016C_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "101", "200"],    
                                        ["SingleElectron_Run2016C_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "201", "300"],    
                                        ["SingleElectron_Run2016C_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "301", "400"],    
                                      ]},
                
                'data_el_d_onelep':{
                            'samples':[
                                        ["SingleElectron_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "0",   "100"],     
                                        ["SingleElectron_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "101", "200"],     
                                        ["SingleElectron_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "201", "300"],
                                        ["SingleElectron_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "301", "400"], 
                                        ["SingleElectron_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "401", "500"],     
                                        ["SingleElectron_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "501", "600"],     
                                      ]},
                
                'data_met_b_onelep':{
                            'samples':[
                                        ["MET_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "0",    "200"], 
                                        ["MET_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "201",  "400"], 
                                        ["MET_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "401",  "600"], 
                                        ["MET_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "601",  "800"], 
                                        ["MET_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "801",  "1000"], 
                                        ["MET_Run2016B_PromptReco_v2",   "--skimLepton=oneLep",   "--runChunks", "1001", "1200"], 
                                      ]},
                
                'data_met_c_onelep':{
                            'samples':[
                                        ["MET_Run2016C_PromptReco_v2",   "--skimLepton=oneLep",    "--runChunks", "0",   "100"],     
                                        ["MET_Run2016C_PromptReco_v2",   "--skimLepton=oneLep",    "--runChunks", "101", "200"],     
                                        ["MET_Run2016C_PromptReco_v2",   "--skimLepton=oneLep",    "--runChunks", "201", "300"],     
                                        ["MET_Run2016C_PromptReco_v2",   "--skimLepton=oneLep",    "--runChunks", "301", "400"],     
                                      ]},
                
                'data_met_d_onelep':{
                            'samples':[
                                        ["MET_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",    "--runChunks", "0",   "100"],     
                                        ["MET_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",    "--runChunks", "101", "200"],     
                                        ["MET_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",    "--runChunks", "201", "300"],     
                                        ["MET_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",    "--runChunks", "301", "400"],     
                                        ["MET_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",    "--runChunks", "401", "500"],     
                                        ["MET_Run2016D_PromptReco_v2",   "--skimLepton=oneLep",    "--runChunks", "501", "600"],     
                                      ]},
            }
    


mstops = [250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800]
dms    = [10, 20, 30, 40, 50, 60, 70, 80]

signalOpts = ["--skimPreselect", "--applyEventVetoFastSimJets"]
signalSample = "SMS_T2tt_dM_10to80_genHT_160_genMET_80"

signalSets = {}
for mstop in mstops:
    signalSet =  {  'samples': [ [signalSample, '--processSignalScan', str(mstop), str(mstop-dm)]+signalOpts for dm in dms ] }
    signalSets.update({ 'mStop%s'%mstop:signalSet})

sampleSets.update(signalSets)



def get_parser():
    ''' Argument parser for running the post processing module.
    
    Include all the options from cmgPostProcessing_parser, which are also used in 
    cmgPostProcessing_v1 script.
    
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
        choices=sampleSets.keys(),
        default='ttjets',
        help="Set of samples to run the post processing on"
        )
        
    argsRun.add_argument('--numberOfProcesses',
        action='store',
        type=int,
        default='7',
        help="Number of processes to run in parallel"
        )

    argsRun.add_argument('--run',
        action='store_true',
        help="Run Post processing!"
        )
    
    # 
    return argParser, argsRun


def make_list_options(args, argsRun):
    ''' Create the list of options for post-processing script.
        
    The list of options is created from the arguments of the cmgPostProcessing_v1.py
    given on the command line for runPostProcessing and the default values of the cmgPostProcessing_v1.py 
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

    #
    return options_list


def make_command(sampleSet, options_list=[]):
    ''' Create the final command for post-processing script.
    
    The command is created using the list of options, replacing the "--processSample=..." argument 
    with the sample specific argument. Optional arguments included in the "samples" definition  
    replace also the arguments from the list of options. 
    '''
    logger = logging.getLogger('runPostProcessing.make_command')
    
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
            raise Exception("\n type not recognized for %s" % samp)
        
        logger.debug(
            "\n Extra options from sample definition for sample %s: \n %s \n",
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
            'cmgPostProcessing_v1.py',
            ]
        
        commandPostProcessing.extend(options_current)

        pprint_cust.pprint(" ".join(commandPostProcessing))
        
        logger.info(
            "\n Command to be processed: \n %s \n",
            pprint_cust.pformat(" ".join(commandPostProcessing))
            )
        

        commands.append(commandPostProcessing)
    
    #
    return commands

def runPostProcessing(argv=None):
    
    if argv is None:
        argv = sys.argv[1:]

    # argument parser
    
    parser, argsRun = get_parser() 
    args= parser.parse_args()
    
    verbose = args.verbose
    
    # create the output top directory - here, it is used to write the logging messages
    # cmgPostProcessing_v1.py creates its own outputDirectory
    
    # WARNING: this directory must be in agreement with the directory created by  
    # cmgPostProcessing_v1.py
    
    outputDirectory = os.path.join(
        args.targetDir, 
        args.processingEra, args.cmgProcessingTag, args.cmgPostProcessingTag, 
        args.parameterSet, 'step1',
        args.cmgTuples
        )

    try:
        os.makedirs(outputDirectory)
        msg_logger_debug = \
            "\n Requested output directory \n {0} \n does not exists.".format(outputDirectory) + \
            "\n Created new directory. \n"
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        else:
            msg_logger_debug = \
                "\n Requested output directory \n {0} \n already exists.\n".format(outputDirectory)

    
    # logging
    
    logLevel = args.logLevel
    
    # use a unique name for the log file, write file in the dataset directory
    prefixLogFile = 'runPostProcessing_' + args.sampleSet + \
         '_' + logLevel + '_'
    logFile = tempfile.NamedTemporaryFile(suffix='.log', prefix=prefixLogFile, dir=outputDirectory, delete=False) 

    get_logger_rtuple = helpers.get_logger('runPostProcessing', logLevel, logFile.name)
    logger = get_logger_rtuple.logger

    #

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
    logger.info("\n Samples: \n %s \n", pprint_cust.pformat(sampleSets[args.sampleSet]))

    # write the debug message kept in the msg_logger_debug
    logger.debug(msg_logger_debug)

    options_list = make_list_options(args, argsRun)
    print options_list
    commands = make_command(args.sampleSet, options_list)
    
    logger.info(
        "\n Final commands to be processed: \n %s \n",
        pprint_cust.pformat(commands)
        )

    if args.run:
        pool = multiprocessing.Pool(processes=args.numberOfProcesses)
        results = pool.map(subprocess.call, commands)
        pool.close()
        pool.join()

        if verbose:    
            print "{:-^80}".format(" FIN ")
    else:
        # do not put this print unter verbose
        print "\n Run the script adding the option --run to actually run over the chosen sample.\n "
        
    logger.info(
        "\n " + \
        "\n End of runPostProcessing run on sample set %s. \n" + \
        "\n *******************************************************************************\n",
        args.sampleSet
        )


        
if __name__ == "__main__":
    sys.exit(runPostProcessing())
        
