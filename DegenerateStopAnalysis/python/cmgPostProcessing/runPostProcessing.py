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

# imports user modules or functions

import Workspace.DegenerateStopAnalysis.cmgPostProcessing.cmgPostProcessing_parser as cmgPostProcessing_parser
import Workspace.DegenerateStopAnalysis.tools.helpers as helpers

pprint_cust = pprint.PrettyPrinter(indent=3, depth=5 , width=140)

sampleSets = {
   'signals':{
               'samples':[ 
                           "T2tt_300_270_FastSim",
                           "T2DegStop_300_270",
                           "T2DegStop_300_290_FastSim",
                           "T2DegStop_300_240_FastSim",
                           "T2DegStop_300_270_FastSim",
                         ],
               },
   
   'wjets':{
               'samples':[
                           "WJetsToLNu_HT100to200",
                           "WJetsToLNu_HT100to200_ext",
                           "WJetsToLNu_HT200to400",
                           "WJetsToLNu_HT200to400_ext",
                           "WJetsToLNu_HT400to600",
                           "WJetsToLNu_HT600to800",
                           "WJetsToLNu_HT800to1200_ext",
                           "WJetsToLNu_HT1200to2500",
                           "WJetsToLNu_HT2500toInf",
                         ],
               },
   
   'wjets_chunks':{
               'samples':[
                           ["WJetsToLNu_HT100to200",],
                           ["WJetsToLNu_HT100to200_ext",  "--runChunks", "0",   "100"],
                           ["WJetsToLNu_HT100to200_ext",  "--runChunks", "101", "200"],
                           ["WJetsToLNu_HT100to200_ext",  "--runChunks", "201", "300"],
                           ["WJetsToLNu_HT100to200_ext",  "--runChunks", "301", "300"],
                           ["WJetsToLNu_HT100to200_ext",  "--runChunks", "401", "500"],
                           ["WJetsToLNu_HT100to200_ext",  "--runChunks", "501", "600"],
                           ["WJetsToLNu_HT100to200_ext",  "--runChunks", "601", "700"],
                           
                           ["WJetsToLNu_HT200to400",],
                           ["WJetsToLNu_HT200to400_ext", "--runChunks", "0",   "100"],
                           ["WJetsToLNu_HT200to400_ext", "--runChunks", "101", "200"],
                           ["WJetsToLNu_HT200to400_ext", "--runChunks", "201", "300"],
                           ["WJetsToLNu_HT200to400_ext", "--runChunks", "301", "400"],
                           
                           ["WJetsToLNu_HT400to600",],
                           ["WJetsToLNu_HT600to800",],
                           ["WJetsToLNu_HT800to1200_ext",],
                           ["WJetsToLNu_HT1200to2500",],
                           ["WJetsToLNu_HT2500toInf",],
                         ],
               },
   
   'ttjets':{
               'samples':[
                           ["TTJets_LO",],
                           ["TTJets_LO",                "--skimGeneral=lheHTlow"],
                           ["TTJets_LO_HT600to800_ext", "--skimGeneral=lheHThigh"],
                           ["TTJets_LO_HT800to1200_ext",],
                           ["TTJets_LO_HT1200to2500_ext",],
                           ["TTJets_LO_HT2500toInf",],
                           #["TTJets_FastSIM",          "--runChunks", "0",   "100"],
                           #["TTJets_FastSIM",          "--runChunks", "101", "200"],
                           #["TTJets_FastSIM",          "--runChunks", "201", "300"],
                           #["TTJets_FastSIM",          "--runChunks", "301", "400"],
                         ],
               },
   
   'ttjets_chunks':{
               'samples':[
                           ["TTJets_LO",                "--runChunks", "0",   "100" ],
                           ["TTJets_LO",                "--runChunks", "101", "200" ],
                           ["TTJets_LO",                "--runChunks", "201", "300" ],
                           ["TTJets_LO",                "--runChunks", "301", "400" ],
                           ["TTJets_LO",                                             "--skimGeneral=lheHTlow"],
                           ["TTJets_LO_HT600to800_ext", "--runChunks", "0",   "100", "--skimGeneral=lheHThigh"],
                           ["TTJets_LO_HT600to800_ext", "--runChunks", "101", "200", "--skimGeneral=lheHThigh"],
                           ["TTJets_LO_HT600to800_ext", "--runChunks", "201", "300", "--skimGeneral=lheHThigh"],
                           ["TTJets_LO_HT600to800_ext", "--runChunks", "301", "400", "--skimGeneral=lheHThigh"],
                           ["TTJets_LO_HT800to1200_ext",],
                           ["TTJets_LO_HT1200to2500_ext",],
                           ["TTJets_LO_HT2500toInf",],
                           #["TTJets_FastSIM",          "--runChunks", "0",   "100"],
                           #["TTJets_FastSIM",          "--runChunks", "101", "200"],
                           #["TTJets_FastSIM",          "--runChunks", "201", "300"],
                           #["TTJets_FastSIM",          "--runChunks", "301", "400"],
                         ],
               },
   
   'ttjets_lep':{
               'samples':[
                           "TTJets_SingleLeptonFromT",   
                           "TTJets_SingleLeptonFromTbar",
                           "TTJets_DiLepton",            
                         ],
               },
   
   'dyjets':{
               'samples':[
                           #M50
                           'DYJetsToLL_M50_HT100to200_ext',
                           'DYJetsToLL_M50_HT200to400_ext',
                           'DYJetsToLL_M50_HT400to600_ext',
                           'DYJetsToLL_M50_HT600toInf',
                           'DYJetsToLL_M50_HT600toInf_ext',
                           
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
   
   'dyjets_chunks':{
               'samples':[
                           ['DYJetsToLL_M50_HT100to200_ext', "--runChunks", "0",   "100"],
                           ['DYJetsToLL_M50_HT100to200_ext', "--runChunks", "101", "200"],
                           
                           ['DYJetsToLL_M50_HT200to400_ext', "--runChunks", "0",   "100"],
                           ['DYJetsToLL_M50_HT200to400_ext', "--runChunks", "101", "200"],
                           ['DYJetsToLL_M50_HT200to400_ext', "--runChunks", "201", "300"],
                           
                           ['DYJetsToLL_M50_HT400to600_ext', "--runChunks", "0",   "100"],
                           ['DYJetsToLL_M50_HT400to600_ext', "--runChunks", "101", "200"],
                           
                           ['DYJetsToLL_M50_HT600toInf',],
                           ['DYJetsToLL_M50_HT600toInf_ext',],
   
                           ['DYJetsToLL_M5to50_HT100to200',],
                           ['DYJetsToLL_M5to50_HT100to200_ext',],
                           ['DYJetsToLL_M5to50_HT200to400',],
                           ['DYJetsToLL_M5to50_HT200to400_ext',],
                           ['DYJetsToLL_M5to50_HT400to600',],
                           ['DYJetsToLL_M5to50_HT600toInf',],
                           ['DYJetsToLL_M5to50_HT600toInf_ext',],
                         ],
               },
   
   'zjets':{
               'samples':[ 
                           "ZJetsToNuNu_HT100to200_ext",
                           "ZJetsToNuNu_HT200to400_ext",
                           "ZJetsToNuNu_HT400to600",
                           "ZJetsToNuNu_HT600to800",
                           "ZJetsToNuNu_HT800to1200",
                           "ZJetsToNuNu_HT1200to2500",
                           "ZJetsToNuNu_HT1200to2500_ext",
                           "ZJetsToNuNu_HT2500toInf",
                         ],
               },
   
   'qcd':{
               'samples':[
                           "QCD_HT300to500",
                           "QCD_HT300to500_ext",
                           "QCD_HT500to700_ext",
                           "QCD_HT700to1000",
                           "QCD_HT700to1000_ext",
                           "QCD_HT1000to1500",
                           "QCD_HT1000to1500_ext",
                           "QCD_HT1500to2000",
                           "QCD_HT1500to2000_ext",
                           "QCD_HT2000toInf",
                           "QCD_HT2000toInf_ext",
                         ],
               },
   
   'qcd_pt':{
               'samples':[
                           #"QCD_Pt5to10",
                           #"QCD_Pt10to15",
                           "QCD_Pt15to30",
                           "QCD_Pt30to50",
                           "QCD_Pt50to80",
                           "QCD_Pt80to120",
                           "QCD_Pt120to170",
                           "QCD_Pt170to300",
                           "QCD_Pt300to470",
                           "QCD_Pt470to600",
                           "QCD_Pt600to800",
                           "QCD_Pt800to1000",
                           "QCD_Pt1000to1400",
                           "QCD_Pt1400to1800",
                           "QCD_Pt1800to2400",
                           "QCD_Pt2400to3200",
                           #"QCD_Pt3200toInf",
                         ],
               },
   
   'qcdpt_em':{
               'samples':[
                           'QCD_Pt15to20_EMEnriched',
                           'QCD_Pt20to30_EMEnriched',
                           'QCD_Pt30to50_EMEnriched',
                           'QCD_Pt50to80_EMEnriched',
                           'QCD_Pt80to120_EMEnriched',
                           'QCD_Pt120to170_EMEnriched',
                           'QCD_Pt170to300_EMEnriched',
                           'QCD_Pt300toInf_EMEnriched',
                         ],
               },
   
   'other':{
               'samples':[
                           'WW',
                           'WZ',
                           'ZZ',
                           'TBar_tch',
                           'TBarToLeptons_tch_powheg', 
                           'T_tch',
                           'TToLeptons_tch_powheg',
                           'TBar_tWch',
                           'T_tWch',
                         ],
               },
   
   
                            ############################
                            ############DATA############
                            ############################
   
   ### ReReco ###
   
   # MET PD
   'data_met':{
               'samples':[
                           "MET_Run2016B_23Sep2016_v3", #NOTE: v3
                           "MET_Run2016C_23Sep2016_v1",
                           "MET_Run2016D_23Sep2016_v1",
                           "MET_Run2016E_23Sep2016_v1",
                           "MET_Run2016F_23Sep2016_v1",
                           "MET_Run2016G_23Sep2016_v1",
                         ],
                  },
   
   'data_met_chunks':{
               'samples':[
                           #B (v3)
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "0",    "100"], 
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "101",  "200"], 
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "201",  "300"], 
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "301",  "400"], 
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "401",  "500"], 
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "501",  "600"], 
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "601",  "700"], 
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "701",  "800"], 
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "801",  "900"], 
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "901",  "1000"], 
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "1001", "1100"], 
                           #C  
                           ["MET_Run2016C_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["MET_Run2016C_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["MET_Run2016C_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["MET_Run2016C_23Sep2016_v1", "--runChunks", "301", "400"],
                           #D
                           ["MET_Run2016D_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["MET_Run2016D_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["MET_Run2016D_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["MET_Run2016D_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["MET_Run2016D_23Sep2016_v1", "--runChunks", "401", "500"],
                           ["MET_Run2016D_23Sep2016_v1", "--runChunks", "501", "600"],
                           #E
                           ["MET_Run2016E_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["MET_Run2016E_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["MET_Run2016E_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["MET_Run2016E_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["MET_Run2016E_23Sep2016_v1", "--runChunks", "401", "500"],
                           #F
                           ["MET_Run2016F_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["MET_Run2016F_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["MET_Run2016F_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["MET_Run2016F_23Sep2016_v1", "--runChunks", "301", "400"],
                           #G
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "401", "500"],
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "501", "600"],
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "601", "700"],
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "701", "800"],
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "801", "900"],
                         ]},
   
   'data_met_b':{
               'samples':[
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "0",    "100"],
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "101",  "200"],
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "201",  "300"],
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "301",  "400"],
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "401",  "500"],
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "501",  "600"],
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "601",  "700"],
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "701",  "800"],
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "801",  "900"],
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "901",  "1000"],
                           ["MET_Run2016B_23Sep2016_v3", "--runChunks", "1001", "1100"],
                         ]},
   
   'data_met_c':{
               'samples':[
                           ["MET_Run2016C_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["MET_Run2016C_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["MET_Run2016C_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["MET_Run2016C_23Sep2016_v1", "--runChunks", "301", "400"],
                         ]},
   
   'data_met_d':{
               'samples':[
                           ["MET_Run2016D_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["MET_Run2016D_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["MET_Run2016D_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["MET_Run2016D_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["MET_Run2016D_23Sep2016_v1", "--runChunks", "401", "500"],
                           ["MET_Run2016D_23Sep2016_v1", "--runChunks", "501", "600"],
                         ]},
   
   'data_met_e':{
               'samples':[
                           ["MET_Run2016E_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["MET_Run2016E_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["MET_Run2016E_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["MET_Run2016E_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["MET_Run2016E_23Sep2016_v1", "--runChunks", "401", "500"],
                         ]},
   
   'data_met_f':{
               'samples':[
                           ["MET_Run2016F_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["MET_Run2016F_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["MET_Run2016F_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["MET_Run2016F_23Sep2016_v1", "--runChunks", "301", "400"],
                         ]},
   
   'data_met_g':{
               'samples':[
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "401", "500"],
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "501", "600"],
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "601", "700"],
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "701", "800"],
                           ["MET_Run2016G_23Sep2016_v1", "--runChunks", "801", "900"],
                         ]},
   
   #NOTE: H Re-Reco not available
  
 
   # SingleElectron PD
   
   'data_el':{
               'samples':[
                           "SingleElectron_Run2016B_23Sep2016_v3", #NOTE: v3
                           "SingleElectron_Run2016C_23Sep2016_v1",
                           "SingleElectron_Run2016D_23Sep2016_v1",
                           "SingleElectron_Run2016E_23Sep2016_v1",
                           "SingleElectron_Run2016F_23Sep2016_v1",
                           "SingleElectron_Run2016G_23Sep2016_v1",
                         ],
                  },
   
   'data_el_chunks':{
               'samples':[
                           #B (v3)
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "0",    "100"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "101",  "200"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "201",  "300"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "301",  "400"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "401",  "500"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "501",  "600"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "601",  "700"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "701",  "800"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "801",  "900"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "901",  "1000"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "1001", "1100"],
                           #C  
                           ["SingleElectron_Run2016C_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleElectron_Run2016C_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleElectron_Run2016C_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleElectron_Run2016C_23Sep2016_v1", "--runChunks", "301", "400"],
                           #D
                           ["SingleElectron_Run2016D_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleElectron_Run2016D_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleElectron_Run2016D_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleElectron_Run2016D_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["SingleElectron_Run2016D_23Sep2016_v1", "--runChunks", "401", "500"],
                           ["SingleElectron_Run2016D_23Sep2016_v1", "--runChunks", "501", "600"],
                           #E
                           ["SingleElectron_Run2016E_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleElectron_Run2016E_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleElectron_Run2016E_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleElectron_Run2016E_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["SingleElectron_Run2016E_23Sep2016_v1", "--runChunks", "401", "500"],
                           #F
                           ["SingleElectron_Run2016F_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleElectron_Run2016F_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleElectron_Run2016F_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleElectron_Run2016F_23Sep2016_v1", "--runChunks", "301", "400"],
                           #G
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "401", "500"],
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "501", "600"],
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "601", "700"],
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "701", "800"],
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "801", "900"],
                         ]},
   
   'data_el_b':{
               'samples':[
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "0",    "100"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "101",  "200"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "201",  "300"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "301",  "400"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "401",  "500"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "501",  "600"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "601",  "700"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "701",  "800"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "801",  "900"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "901",  "1000"],
                           ["SingleElectron_Run2016B_23Sep2016_v3", "--runChunks", "1001", "1100"],
                         ]},
   
   'data_el_c':{
               'samples':[
                           ["SingleElectron_Run2016C_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleElectron_Run2016C_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleElectron_Run2016C_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleElectron_Run2016C_23Sep2016_v1", "--runChunks", "301", "400"],
                         ]},
   
   'data_el_d':{
               'samples':[
                           ["SingleElectron_Run2016D_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleElectron_Run2016D_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleElectron_Run2016D_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleElectron_Run2016D_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["SingleElectron_Run2016D_23Sep2016_v1", "--runChunks", "401", "500"],
                           ["SingleElectron_Run2016D_23Sep2016_v1", "--runChunks", "501", "600"],
                         ]},
   
   'data_el_e':{
               'samples':[
                           ["SingleElectron_Run2016E_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleElectron_Run2016E_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleElectron_Run2016E_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleElectron_Run2016E_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["SingleElectron_Run2016E_23Sep2016_v1", "--runChunks", "401", "500"],
                         ]},
   
   'data_el_f':{
               'samples':[
                           ["SingleElectron_Run2016F_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleElectron_Run2016F_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleElectron_Run2016F_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleElectron_Run2016F_23Sep2016_v1", "--runChunks", "301", "400"],
                         ]},
   
   'data_el_g':{
               'samples':[
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "401", "500"],
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "501", "600"],
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "601", "700"],
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "701", "800"],
                           ["SingleElectron_Run2016G_23Sep2016_v1", "--runChunks", "801", "900"],
                         ]},
   
   #NOTE: H Re-Reco not available
   
   # SingleMuon PD
   
   'data_mu':{
               'samples':[
                           "SingleMuon_Run2016B_23Sep2016_v3", #NOTE: v3
                           "SingleMuon_Run2016C_23Sep2016_v1",
                           "SingleMuon_Run2016D_23Sep2016_v1",
                           "SingleMuon_Run2016E_23Sep2016_v1",
                           "SingleMuon_Run2016F_23Sep2016_v1",
                           "SingleMuon_Run2016G_23Sep2016_v1",
                         ],
                  },
   
   'data_mu_chunks':{
               'samples':[
                           #B (v3)
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "0",    "100"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "101",  "200"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "201",  "300"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "301",  "400"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "401",  "500"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "501",  "600"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "601",  "700"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "701",  "800"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "801",  "900"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "901",  "1000"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "1001", "1100"],
                           #C  
                           ["SingleMuon_Run2016C_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016C_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016C_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016C_23Sep2016_v1", "--runChunks", "301", "400"],
                           #D
                           ["SingleMuon_Run2016D_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016D_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016D_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016D_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["SingleMuon_Run2016D_23Sep2016_v1", "--runChunks", "401", "500"],
                           ["SingleMuon_Run2016D_23Sep2016_v1", "--runChunks", "501", "600"],
                           #E
                           ["SingleMuon_Run2016E_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016E_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016E_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016E_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["SingleMuon_Run2016E_23Sep2016_v1", "--runChunks", "401", "500"],
                           #F
                           ["SingleMuon_Run2016F_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016F_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016F_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016F_23Sep2016_v1", "--runChunks", "301", "400"],
                           #G
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "401", "500"],
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "501", "600"],
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "601", "700"],
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "701", "800"],
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "801", "900"],
                         ]},
   
   'data_mu_b':{
               'samples':[
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "0",    "100"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "101",  "200"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "201",  "300"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "301",  "400"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "401",  "500"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "501",  "600"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "601",  "700"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "701",  "800"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "801",  "900"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "901",  "1000"],
                           ["SingleMuon_Run2016B_23Sep2016_v3", "--runChunks", "1001", "1100"],
                         ]},
   
   'data_mu_c':{
               'samples':[
                           ["SingleMuon_Run2016C_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016C_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016C_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016C_23Sep2016_v1", "--runChunks", "301", "400"],
                         ]},
   
   'data_mu_d':{
               'samples':[
                           ["SingleMuon_Run2016D_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016D_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016D_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016D_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["SingleMuon_Run2016D_23Sep2016_v1", "--runChunks", "401", "500"],
                           ["SingleMuon_Run2016D_23Sep2016_v1", "--runChunks", "501", "600"],
                         ]},
   
   'data_mu_e':{
               'samples':[
                           ["SingleMuon_Run2016E_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016E_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016E_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016E_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["SingleMuon_Run2016E_23Sep2016_v1", "--runChunks", "401", "500"],
                         ]},
   
   'data_mu_f':{
               'samples':[
                           ["SingleMuon_Run2016F_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016F_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016F_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016F_23Sep2016_v1", "--runChunks", "301", "400"],
                         ]},
   
   'data_mu_g':{
               'samples':[
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "401", "500"],
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "501", "600"],
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "601", "700"],
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "701", "800"],
                           ["SingleMuon_Run2016G_23Sep2016_v1", "--runChunks", "801", "900"],
                         ]},
   
   #NOTE: H Re-Reco not available
   
   # JetHT PD
   'data_jet':{
               'samples':[
                           "JetHT_Run2016B_23Sep2016_v3", #NOTE: v3
                           "JetHT_Run2016C_23Sep2016_v1",
                           "JetHT_Run2016D_23Sep2016_v1",
                           "JetHT_Run2016E_23Sep2016_v1",
                           "JetHT_Run2016F_23Sep2016_v1",
                           "JetHT_Run2016G_23Sep2016_v1",
                         ],
                  },
   
   'data_jet_chunks':{
               'samples':[
                           #B (v3)
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "0",    "100"], 
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "101",  "200"], 
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "201",  "300"], 
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "301",  "400"], 
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "401",  "500"], 
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "501",  "600"], 
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "601",  "700"], 
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "701",  "800"], 
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "801",  "900"], 
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "901",  "1000"], 
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "1001", "1100"], 
                           #C  
                           ["JetHT_Run2016C_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["JetHT_Run2016C_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["JetHT_Run2016C_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["JetHT_Run2016C_23Sep2016_v1", "--runChunks", "301", "400"],
                           #D
                           ["JetHT_Run2016D_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["JetHT_Run2016D_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["JetHT_Run2016D_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["JetHT_Run2016D_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["JetHT_Run2016D_23Sep2016_v1", "--runChunks", "401", "500"],
                           ["JetHT_Run2016D_23Sep2016_v1", "--runChunks", "501", "600"],
                           #E
                           ["JetHT_Run2016E_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["JetHT_Run2016E_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["JetHT_Run2016E_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["JetHT_Run2016E_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["JetHT_Run2016E_23Sep2016_v1", "--runChunks", "401", "500"],
                           #F
                           ["JetHT_Run2016F_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["JetHT_Run2016F_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["JetHT_Run2016F_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["JetHT_Run2016F_23Sep2016_v1", "--runChunks", "301", "400"],
                           #G
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "401", "500"],
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "501", "600"],
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "601", "700"],
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "701", "800"],
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "801", "900"],
                         ]},
   
   'data_jet_b':{
               'samples':[
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "0",    "100"],
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "101",  "200"],
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "201",  "300"],
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "301",  "400"],
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "401",  "500"],
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "501",  "600"],
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "601",  "700"],
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "701",  "800"],
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "801",  "900"],
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "901",  "1000"],
                           ["JetHT_Run2016B_23Sep2016_v3", "--runChunks", "1001", "1100"],
                         ]},
   
   'data_jet_c':{
               'samples':[
                           ["JetHT_Run2016C_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["JetHT_Run2016C_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["JetHT_Run2016C_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["JetHT_Run2016C_23Sep2016_v1", "--runChunks", "301", "400"],
                         ]},
   
   'data_jet_d':{
               'samples':[
                           ["JetHT_Run2016D_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["JetHT_Run2016D_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["JetHT_Run2016D_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["JetHT_Run2016D_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["JetHT_Run2016D_23Sep2016_v1", "--runChunks", "401", "500"],
                           ["JetHT_Run2016D_23Sep2016_v1", "--runChunks", "501", "600"],
                         ]},
   
   'data_jet_e':{
               'samples':[
                           ["JetHT_Run2016E_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["JetHT_Run2016E_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["JetHT_Run2016E_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["JetHT_Run2016E_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["JetHT_Run2016E_23Sep2016_v1", "--runChunks", "401", "500"],
                         ]},
   
   'data_jet_f':{
               'samples':[
                           ["JetHT_Run2016F_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["JetHT_Run2016F_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["JetHT_Run2016F_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["JetHT_Run2016F_23Sep2016_v1", "--runChunks", "301", "400"],
                         ]},
   
   'data_jet_g':{
               'samples':[
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "0",   "100"],
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "101", "200"],
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "201", "300"],
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "301", "400"],
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "401", "500"],
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "501", "600"],
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "601", "700"],
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "701", "800"],
                           ["JetHT_Run2016G_23Sep2016_v1", "--runChunks", "801", "900"],
                         ]},
   
   #NOTE: H Re-Reco not available
   
   
   ### PromptReco (PR) ###
   
   # MET PD
   'data_PR_met':{
               'samples':[
                           "MET_Run2016B_PromptReco_v2",
                           "MET_Run2016C_PromptReco_v2",
                           "MET_Run2016D_PromptReco_v2",
                           "MET_Run2016E_PromptReco_v2",
                           #"MET_Run2016F_PromptReco_v1",
                           "MET_Run2016G_PromptReco_v1",
                           #"MET_Run2016H_PromptReco_v1", #NOTE: use?
                           "MET_Run2016H_PromptReco_v2",
                           "MET_Run2016H_PromptReco_v3", #NOTE: use?
                         ],
                  },
   
   'data_PR_met_chunks':{
               'samples':[
                           #B
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "0",    "100"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "101",  "200"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "201",  "300"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "301",  "400"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "401",  "500"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "501",  "600"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "601",  "700"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "701",  "800"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "801",  "900"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "901",  "1000"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "1001", "1100"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "1100", "1200"],
                           #C 
                           ["MET_Run2016C_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["MET_Run2016C_PromptReco_v2", "--runChunks", "101", "200"],
                           ["MET_Run2016C_PromptReco_v2", "--runChunks", "201", "300"],
                           ["MET_Run2016C_PromptReco_v2", "--runChunks", "301", "400"],
                           #D
                           ["MET_Run2016D_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["MET_Run2016D_PromptReco_v2", "--runChunks", "101", "200"],
                           ["MET_Run2016D_PromptReco_v2", "--runChunks", "201", "300"],
                           ["MET_Run2016D_PromptReco_v2", "--runChunks", "301", "400"],
                           ["MET_Run2016D_PromptReco_v2", "--runChunks", "401", "500"],
                           ["MET_Run2016D_PromptReco_v2", "--runChunks", "501", "600"],
                           #E
                           ["MET_Run2016E_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["MET_Run2016E_PromptReco_v2", "--runChunks", "101", "200"],
                           ["MET_Run2016E_PromptReco_v2", "--runChunks", "201", "300"],
                           ["MET_Run2016E_PromptReco_v2", "--runChunks", "301", "400"],
                           ["MET_Run2016E_PromptReco_v2", "--runChunks", "401", "500"],
                           ##F 
                           #["MET_Run2016F_PromptReco_v1", "--runChunks", "0",   "100"],
                           #["MET_Run2016F_PromptReco_v1", "--runChunks", "101", "200"],
                           #["MET_Run2016F_PromptReco_v1", "--runChunks", "201", "300"],
                           #["MET_Run2016F_PromptReco_v1", "--runChunks", "301", "400"],
                           #["MET_Run2016F_PromptReco_v1", "--runChunks", "401", "500"],
                           #["MET_Run2016F_PromptReco_v1", "--runChunks", "501", "600"],
                           #G 
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "0",   "100"],
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "101", "200"],
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "201", "300"],
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "301", "400"],
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "401", "500"],
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "501", "600"],
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "601", "700"],
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "701", "800"],
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "801", "900"],
                           #H 
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "0",   "100"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "101", "200"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "201", "300"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "301", "400"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "401", "500"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "501", "600"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "601", "700"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "701", "800"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "801", "900"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "901", "1000"],
                           
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "101", "200"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "201", "300"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "301", "400"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "401", "500"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "501", "600"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "601", "700"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "701", "800"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "801", "900"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "901", "1000"],
                           
                           ["MET_Run2016H_PromptReco_v3", "--runChunks", "0",   "30"],
                         ]},
   
   'data_PR_met_b':{
               'samples':[
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "0",    "100"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "101",  "200"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "201",  "300"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "301",  "400"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "401",  "500"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "501",  "600"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "601",  "700"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "701",  "800"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "801",  "900"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "901",  "1000"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "1001", "1100"],
                           ["MET_Run2016B_PromptReco_v2", "--runChunks", "1100", "1200"],
                         ]},
   
   'data_PR_met_c':{
               'samples':[
                           ["MET_Run2016C_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["MET_Run2016C_PromptReco_v2", "--runChunks", "101", "200"],
                           ["MET_Run2016C_PromptReco_v2", "--runChunks", "201", "300"],
                           ["MET_Run2016C_PromptReco_v2", "--runChunks", "301", "400"],
                         ]},
   
   'data_PR_met_d':{
               'samples':[
                           ["MET_Run2016D_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["MET_Run2016D_PromptReco_v2", "--runChunks", "101", "200"],
                           ["MET_Run2016D_PromptReco_v2", "--runChunks", "201", "300"],
                           ["MET_Run2016D_PromptReco_v2", "--runChunks", "301", "400"],
                           ["MET_Run2016D_PromptReco_v2", "--runChunks", "401", "500"],
                           ["MET_Run2016D_PromptReco_v2", "--runChunks", "501", "600"],
                         ]},
   
   'data_PR_met_e':{
               'samples':[
                           ["MET_Run2016E_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["MET_Run2016E_PromptReco_v2", "--runChunks", "101", "200"],
                           ["MET_Run2016E_PromptReco_v2", "--runChunks", "201", "300"],
                           ["MET_Run2016E_PromptReco_v2", "--runChunks", "301", "400"],
                           ["MET_Run2016E_PromptReco_v2", "--runChunks", "401", "500"],
                         ]},
   
   #'data_PR_met_f':{
   #            'samples':[
   #                        ["MET_Run2016F_PromptReco_v1", "--runChunks", "0",   "100"],
   #                        ["MET_Run2016F_PromptReco_v1", "--runChunks", "101", "200"],
   #                        ["MET_Run2016F_PromptReco_v1", "--runChunks", "201", "300"],
   #                        ["MET_Run2016F_PromptReco_v1", "--runChunks", "301", "400"],
   #                        ["MET_Run2016F_PromptReco_v1", "--runChunks", "401", "500"],
   #                        ["MET_Run2016F_PromptReco_v1", "--runChunks", "501", "600"],
   #                      ]},
   
   'data_PR_met_g':{
               'samples':[
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "0",   "100"],
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "101", "200"],
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "201", "300"],
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "301", "400"],
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "401", "500"],
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "501", "600"],
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "601", "700"],
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "701", "800"],
                           ["MET_Run2016G_PromptReco_v1", "--runChunks", "801", "900"],
                         ]},
   
   'data_PR_met_h':{
               'samples':[
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "0",   "100"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "101", "200"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "201", "300"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "301", "400"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "401", "500"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "501", "600"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "601", "700"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "701", "800"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "801", "900"],
                           #["MET_Run2016H_PromptReco_v1", "--runChunks", "901", "1000"],
                           
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "101", "200"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "201", "300"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "301", "400"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "401", "500"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "501", "600"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "601", "700"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "701", "800"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "801", "900"],
                           ["MET_Run2016H_PromptReco_v2", "--runChunks", "901", "1000"],
                           
                           ["MET_Run2016H_PromptReco_v3", "--runChunks", "0",   "30"],
                         ]},
   
   # SingleElectron PD
   
   'data_PR_el':{
               'samples':[
                           "SingleElectron_Run2016B_PromptReco_v2",
                           "SingleElectron_Run2016C_PromptReco_v2",
                           "SingleElectron_Run2016D_PromptReco_v2",
                           #"SingleElectron_Run2016E_PromptReco_v2",
                           #"SingleElectron_Run2016F_PromptReco_v1",
                           #"SingleElectron_Run2016G_PromptReco_v1",
                           #"SingleElectron_Run2016H_PromptReco_v1", #NOTE: use?
                           "SingleElectron_Run2016H_PromptReco_v2",
                           "SingleElectron_Run2016H_PromptReco_v3", #NOTE: use?
                         ],
               },
   
   'data_PR_el_chunks':{
               'samples':[
                           #B
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "0",    "100"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "101",  "200"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "201",  "300"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "301",  "400"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "401",  "500"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "501",  "600"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "601",  "700"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "701",  "800"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "801",  "900"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "901",  "1000"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "1001", "1100"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "1100", "1200"],
                           #C
                           ["SingleElectron_Run2016C_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["SingleElectron_Run2016C_PromptReco_v2", "--runChunks", "101", "200"],
                           ["SingleElectron_Run2016C_PromptReco_v2", "--runChunks", "201", "300"],
                           ["SingleElectron_Run2016C_PromptReco_v2", "--runChunks", "301", "400"],
                           #D 
                           ["SingleElectron_Run2016D_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["SingleElectron_Run2016D_PromptReco_v2", "--runChunks", "101", "200"],
                           ["SingleElectron_Run2016D_PromptReco_v2", "--runChunks", "201", "300"],
                           ["SingleElectron_Run2016D_PromptReco_v2", "--runChunks", "301", "400"],
                           ["SingleElectron_Run2016D_PromptReco_v2", "--runChunks", "401", "500"],
                           ["SingleElectron_Run2016D_PromptReco_v2", "--runChunks", "501", "600"],
                           ##E 
                           #["SingleElectron_Run2016E_PromptReco_v2", "--runChunks", "0",   "100"],
                           #["SingleElectron_Run2016E_PromptReco_v2", "--runChunks", "101", "200"],
                           #["SingleElectron_Run2016E_PromptReco_v2", "--runChunks", "201", "300"],
                           #["SingleElectron_Run2016E_PromptReco_v2", "--runChunks", "301", "400"],
                           #["SingleElectron_Run2016E_PromptReco_v2", "--runChunks", "401", "500"],
                           ##F 
                           #["SingleElectron_Run2016F_PromptReco_v1", "--runChunks", "0",   "100"],
                           #["SingleElectron_Run2016F_PromptReco_v1", "--runChunks", "101", "200"],
                           #["SingleElectron_Run2016F_PromptReco_v1", "--runChunks", "201", "300"],
                           #["SingleElectron_Run2016F_PromptReco_v1", "--runChunks", "301", "400"],
                           #["SingleElectron_Run2016F_PromptReco_v1", "--runChunks", "401", "500"],
                           #["SingleElectron_Run2016F_PromptReco_v1", "--runChunks", "501", "600"],
                           ##G 
                           #["SingleElectron_Run2016G_PromptReco_v1", "--runChunks", "0",   "100"],
                           #["SingleElectron_Run2016G_PromptReco_v1", "--runChunks", "101", "200"],
                           #["SingleElectron_Run2016G_PromptReco_v1", "--runChunks", "201", "300"],
                           #["SingleElectron_Run2016G_PromptReco_v1", "--runChunks", "301", "400"],
                           #["SingleElectron_Run2016G_PromptReco_v1", "--runChunks", "401", "500"],
                           #["SingleElectron_Run2016G_PromptReco_v1", "--runChunks", "501", "600"],
                           #H
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "0",   "100"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "101", "200"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "201", "300"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "301", "400"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "401", "500"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "501", "600"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "601", "700"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "701", "800"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "801", "900"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "901", "1000"],
                           
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "101", "200"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "201", "300"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "301", "400"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "401", "500"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "501", "600"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "601", "700"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "701", "800"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "801", "900"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "901", "1000"],
                           
                           ["SingleElectron_Run2016H_PromptReco_v3", "--runChunks", "0",   "30"],
                         ],
               },
   
   'data_PR_el_b':{
               'samples':[
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "0",    "100"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "101",  "200"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "201",  "300"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "301",  "400"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "401",  "500"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "501",  "600"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "601",  "700"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "701",  "800"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "801",  "900"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "901",  "1000"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "1001", "1100"],
                           ["SingleElectron_Run2016B_PromptReco_v2", "--runChunks", "1100", "1200"],
                         ]},
   
   'data_PR_el_c':{
               'samples':[
                           ["SingleElectron_Run2016C_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["SingleElectron_Run2016C_PromptReco_v2", "--runChunks", "101", "200"],
                           ["SingleElectron_Run2016C_PromptReco_v2", "--runChunks", "201", "300"],
                           ["SingleElectron_Run2016C_PromptReco_v2", "--runChunks", "301", "400"],
                         ]},
   
   'data_PR_el_d':{
               'samples':[
                           ["SingleElectron_Run2016D_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["SingleElectron_Run2016D_PromptReco_v2", "--runChunks", "101", "200"],
                           ["SingleElectron_Run2016D_PromptReco_v2", "--runChunks", "201", "300"],
                           ["SingleElectron_Run2016D_PromptReco_v2", "--runChunks", "301", "400"],
                           ["SingleElectron_Run2016D_PromptReco_v2", "--runChunks", "401", "500"],
                           ["SingleElectron_Run2016D_PromptReco_v2", "--runChunks", "501", "600"],
                         ]},
   
   #'data_PR_el_e':{
   #            'samples':[
   #                        ["SingleElectron_Run2016E_PromptReco_v2", "--runChunks", "0",   "100"],
   #                        ["SingleElectron_Run2016E_PromptReco_v2", "--runChunks", "101", "200"],
   #                        ["SingleElectron_Run2016E_PromptReco_v2", "--runChunks", "201", "300"],
   #                        ["SingleElectron_Run2016E_PromptReco_v2", "--runChunks", "301", "400"],
   #                        ["SingleElectron_Run2016E_PromptReco_v2", "--runChunks", "401", "500"],
   #                      ]},
   
   #'data_PR_el_f':{
   #            'samples':[
   #                        ["SingleElectron_Run2016F_PromptReco_v1", "--runChunks", "0",   "100"],
   #                        ["SingleElectron_Run2016F_PromptReco_v1", "--runChunks", "101", "200"],
   #                        ["SingleElectron_Run2016F_PromptReco_v1", "--runChunks", "201", "300"],
   #                        ["SingleElectron_Run2016F_PromptReco_v1", "--runChunks", "301", "400"],
   #                        ["SingleElectron_Run2016F_PromptReco_v1", "--runChunks", "401", "500"],
   #                        ["SingleElectron_Run2016F_PromptReco_v1", "--runChunks", "501", "600"],
   #                      ]},
   
   #'data_PR_el_g':{
   #            'samples':[
   #                        ["SingleElectron_Run2016G_PromptReco_v1", "--runChunks", "0",   "100"],
   #                        ["SingleElectron_Run2016G_PromptReco_v1", "--runChunks", "101", "200"],
   #                        ["SingleElectron_Run2016G_PromptReco_v1", "--runChunks", "201", "300"],
   #                        ["SingleElectron_Run2016G_PromptReco_v1", "--runChunks", "301", "400"],
   #                        ["SingleElectron_Run2016G_PromptReco_v1", "--runChunks", "401", "500"],
   #                        ["SingleElectron_Run2016G_PromptReco_v1", "--runChunks", "501", "600"],
   #                      ]},
   
   'data_PR_el_h':{
               'samples':[
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "0",   "100"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "101", "200"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "201", "300"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "301", "400"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "401", "500"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "501", "600"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "601", "700"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "701", "800"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "801", "900"],
                           #["SingleElectron_Run2016H_PromptReco_v1", "--runChunks", "901", "1000"],
                           
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "101", "200"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "201", "300"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "301", "400"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "401", "500"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "501", "600"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "601", "700"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "701", "800"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "801", "900"],
                           ["SingleElectron_Run2016H_PromptReco_v2", "--runChunks", "901", "1000"],
                           
                           ["SingleElectron_Run2016H_PromptReco_v3", "--runChunks", "0",   "30"],
                         ]},
   
   # SingleMuon PD
   
   'data_PR_mu':{
               'samples':[
                           "SingleMuon_Run2016B_PromptReco_v2",
                           "SingleMuon_Run2016C_PromptReco_v2",
                           "SingleMuon_Run2016D_PromptReco_v2",
                           "SingleMuon_Run2016E_PromptReco_v2",
                           "SingleMuon_Run2016F_PromptReco_v1",
                           "SingleMuon_Run2016G_PromptReco_v1",
                           #"SingleMuon_Run2016H_PromptReco_v1", #NOTE: use?
                           "SingleMuon_Run2016H_PromptReco_v2",
                           "SingleMuon_Run2016H_PromptReco_v3", #NOTE: use?
                         ],
               },
   
   'data_PR_mu_chunks':{
               'samples':[
                           #B
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "0",    "100"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "101",  "200"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "201",  "300"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "301",  "400"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "401",  "500"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "501",  "600"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "601",  "700"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "701",  "800"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "801",  "900"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "901",  "1000"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "1001", "1100"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "1100", "1200"],
                           #C
                           ["SingleMuon_Run2016C_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016C_PromptReco_v2", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016C_PromptReco_v2", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016C_PromptReco_v2", "--runChunks", "301", "400"],
                           #D
                           ["SingleMuon_Run2016D_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016D_PromptReco_v2", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016D_PromptReco_v2", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016D_PromptReco_v2", "--runChunks", "301", "400"],
                           ["SingleMuon_Run2016D_PromptReco_v2", "--runChunks", "401", "500"],
                           ["SingleMuon_Run2016D_PromptReco_v2", "--runChunks", "501", "600"],
                           #E
                           ["SingleMuon_Run2016E_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016E_PromptReco_v2", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016E_PromptReco_v2", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016E_PromptReco_v2", "--runChunks", "301", "400"],
                           ["SingleMuon_Run2016E_PromptReco_v2", "--runChunks", "401", "500"],
                           #F 
                           ["SingleMuon_Run2016F_PromptReco_v1", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016F_PromptReco_v1", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016F_PromptReco_v1", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016F_PromptReco_v1", "--runChunks", "301", "400"],
                           ["SingleMuon_Run2016F_PromptReco_v1", "--runChunks", "401", "500"],
                           #G
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "301", "400"],
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "401", "500"],
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "501", "600"],
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "601", "700"],
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "701", "800"],
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "801", "900"],
                           #H
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "0",   "100"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "101", "200"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "201", "300"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "301", "400"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "401", "500"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "501", "600"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "601", "700"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "701", "800"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "801", "900"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "901", "1000"],
                           
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "301", "400"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "401", "500"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "501", "600"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "601", "700"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "701", "800"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "801", "900"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "901", "1000"],
                           
                           ["SingleMuon_Run2016H_PromptReco_v3", "--runChunks", "0",   "30"],
                         ],
               },
   
   'data_PR_mu_b':{
               'samples':[
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "0",    "100"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "101",  "200"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "201",  "300"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "301",  "400"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "401",  "500"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "501",  "600"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "601",  "700"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "701",  "800"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "801",  "900"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "901",  "1000"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "1001", "1100"],
                           ["SingleMuon_Run2016B_PromptReco_v2", "--runChunks", "1100", "1200"],
                         ]},
   
   'data_PR_mu_c':{
               'samples':[
                           ["SingleMuon_Run2016C_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016C_PromptReco_v2", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016C_PromptReco_v2", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016C_PromptReco_v2", "--runChunks", "301", "400"],
                         ]},
   
   'data_PR_mu_d':{
               'samples':[
                           ["SingleMuon_Run2016D_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016D_PromptReco_v2", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016D_PromptReco_v2", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016D_PromptReco_v2", "--runChunks", "301", "400"],
                           ["SingleMuon_Run2016D_PromptReco_v2", "--runChunks", "401", "500"],
                           ["SingleMuon_Run2016D_PromptReco_v2", "--runChunks", "501", "600"],
                        ]},
   
   'data_PR_mu_e':{
               'samples':[
                           ["SingleMuon_Run2016E_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016E_PromptReco_v2", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016E_PromptReco_v2", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016E_PromptReco_v2", "--runChunks", "301", "400"],
                           ["SingleMuon_Run2016E_PromptReco_v2", "--runChunks", "401", "500"],
                         ]},
   
   'data_PR_mu_f':{
               'samples':[
                           ["SingleMuon_Run2016F_PromptReco_v1", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016F_PromptReco_v1", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016F_PromptReco_v1", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016F_PromptReco_v1", "--runChunks", "301", "400"],
                           ["SingleMuon_Run2016F_PromptReco_v1", "--runChunks", "401", "500"],
                         ]},
   
   'data_PR_mu_g':{
               'samples':[
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "301", "400"],
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "401", "500"],
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "501", "600"],
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "601", "700"],
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "701", "800"],
                           ["SingleMuon_Run2016G_PromptReco_v1", "--runChunks", "801", "900"],
                         ]},
   
   'data_PR_mu_h':{
               'samples':[
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "0",   "100"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "101", "200"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "201", "300"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "301", "400"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "401", "500"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "501", "600"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "601", "700"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "701", "800"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "801", "900"],
                           #["SingleMuon_Run2016H_PromptReco_v1", "--runChunks", "901", "1000"],
                           
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "101", "200"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "201", "300"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "301", "400"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "401", "500"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "501", "600"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "601", "700"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "701", "800"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "801", "900"],
                           ["SingleMuon_Run2016H_PromptReco_v2", "--runChunks", "901", "1000"],
                           
                           ["SingleMuon_Run2016H_PromptReco_v3", "--runChunks", "0",   "30"],
                         ]},
   
   # JetHT PD
   'data_PR_jet':{
               'samples':[
                           #"JetHT_Run2016B_PromptReco_v2",
                           #"JetHT_Run2016C_PromptReco_v2",
                           #"JetHT_Run2016D_PromptReco_v2",
                           #"JetHT_Run2016E_PromptReco_v2",
                           #"JetHT_Run2016F_PromptReco_v1",
                           #"JetHT_Run2016G_PromptReco_v1",
                           #"JetHT_Run2016H_PromptReco_v1", #NOTE: use?
                           "JetHT_Run2016H_PromptReco_v2",
                           "JetHT_Run2016H_PromptReco_v3", #NOTE: use?
                         ],
                  },
   
   'data_PR_jet_h':{
               'samples':[
                           #["JetHT_Run2016H_PromptReco_v1", "--runChunks", "0",   "100"],
                           #["JetHT_Run2016H_PromptReco_v1", "--runChunks", "101", "200"],
                           #["JetHT_Run2016H_PromptReco_v1", "--runChunks", "201", "300"],
                           #["JetHT_Run2016H_PromptReco_v1", "--runChunks", "301", "400"],
                           #["JetHT_Run2016H_PromptReco_v1", "--runChunks", "401", "500"],
                           #["JetHT_Run2016H_PromptReco_v1", "--runChunks", "501", "600"],
                           #["JetHT_Run2016H_PromptReco_v1", "--runChunks", "601", "700"],
                           #["JetHT_Run2016H_PromptReco_v1", "--runChunks", "701", "800"],
                           #["JetHT_Run2016H_PromptReco_v1", "--runChunks", "801", "900"],
                           #["JetHT_Run2016H_PromptReco_v1", "--runChunks", "901", "1000"],
                           
                           ["JetHT_Run2016H_PromptReco_v2", "--runChunks", "0",   "100"],
                           ["JetHT_Run2016H_PromptReco_v2", "--runChunks", "101", "200"],
                           ["JetHT_Run2016H_PromptReco_v2", "--runChunks", "201", "300"],
                           ["JetHT_Run2016H_PromptReco_v2", "--runChunks", "301", "400"],
                           ["JetHT_Run2016H_PromptReco_v2", "--runChunks", "401", "500"],
                           ["JetHT_Run2016H_PromptReco_v2", "--runChunks", "501", "600"],
                           ["JetHT_Run2016H_PromptReco_v2", "--runChunks", "601", "700"],
                           ["JetHT_Run2016H_PromptReco_v2", "--runChunks", "701", "800"],
                           ["JetHT_Run2016H_PromptReco_v2", "--runChunks", "801", "900"],
                           ["JetHT_Run2016H_PromptReco_v2", "--runChunks", "901", "1000"],
                           
                           ["JetHT_Run2016H_PromptReco_v3", "--runChunks", "0",   "30"],
                         ]},
  
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



dataChunks = {
'JetHT_Run2016B-23Sep2016-v3' : 1043  ,
'JetHT_Run2016C-23Sep2016-v1' : 348  ,
'JetHT_Run2016D-23Sep2016-v1' : 583  ,
'JetHT_Run2016F-23Sep2016-v1' : 369  ,
'JetHT_Run2016G-23Sep2016-v1' : 857  ,
'JetHT_Run2016H-PromptReco-v2' : 926  ,
'JetHT_Run2016H-PromptReco-v3' : 25  ,
'MET_Run2016B-23Sep2016-v3' : 1046  ,
'MET_Run2016B-PromptReco-v2' : 1045  ,
'MET_Run2016C-23Sep2016-v1' : 348  ,
'MET_Run2016C-PromptReco-v2' : 348  ,
'MET_Run2016D-23Sep2016-v1' : 584  ,
'MET_Run2016D-PromptReco-v2' : 584  ,
'MET_Run2016E-23Sep2016-v1' : 496  ,
'MET_Run2016E-PromptReco-v2' : 491  ,
'MET_Run2016F-23Sep2016-v1' : 368  ,
'MET_Run2016G-23Sep2016-v1' : 854  ,
'MET_Run2016G-PromptReco-v1' : 832  ,
'MET_Run2016H-PromptReco-v2' : 926  ,
'MET_Run2016H-PromptReco-v3' : 25  ,
'SingleElectron_Run2016B-23Sep2016-v3' : 1054  ,
'SingleElectron_Run2016B-PromptReco-v2' : 1046  ,
'SingleElectron_Run2016C-23Sep2016-v1' : 347  ,
'SingleElectron_Run2016C-PromptReco-v2' : 348  ,
'SingleElectron_Run2016D-23Sep2016-v1' : 589  ,
'SingleElectron_Run2016D-PromptReco-v2' : 584  ,
'SingleElectron_Run2016E-23Sep2016-v1' : 496  ,
'SingleElectron_Run2016F-23Sep2016-v1' : 362  ,
'SingleElectron_Run2016G-23Sep2016-v1' : 854  ,
'SingleElectron_Run2016H-PromptReco-v2' : 926  ,
'SingleElectron_Run2016H-PromptReco-v3' : 25  ,
'SingleMuon_Run2016B-23Sep2016-v3' : 1045  ,
'SingleMuon_Run2016B-PromptReco-v2' : 1045  ,
'SingleMuon_Run2016C-23Sep2016-v1' : 348  ,
'SingleMuon_Run2016C-PromptReco-v2' : 348  ,
'SingleMuon_Run2016D-23Sep2016-v1' : 584  ,
'SingleMuon_Run2016D-PromptReco-v2' : 584  ,
'SingleMuon_Run2016E-23Sep2016-v1' : 496  ,
'SingleMuon_Run2016E-PromptReco-v2' : 219  ,
'SingleMuon_Run2016F-23Sep2016-v1' : 361  ,
'SingleMuon_Run2016F-PromptReco-v1' : 351  ,
'SingleMuon_Run2016G-23Sep2016-v1' : 856  ,
'SingleMuon_Run2016G-PromptReco-v1' : 844  ,
'SingleMuon_Run2016H-PromptReco-v2' : 925  ,
'SingleMuon_Run2016H-PromptReco-v3' : 25  ,
}

def roundup(x):
    return x if x % 100 == 0 else x + 100 - x % 100


data_names = {
                "JetHT":"jet",
                "MET"  :'met',
           "SingleMuon":"mu" ,
       "SingleElectron":"el" ,
             }

for data_samp , nChunk in dataChunks.iteritems():
    name = ""
    for data_name, nameTag in data_names.items():
        if data_name in data_samp:
            name = nameTag            
            break
    n = name + " " +  ""
    n = name + " " +  ""     
 

    #maxChunkSplit = roundup(nChunk)  


### Signal ###

#mstops = [250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800]
#dms    = [10, 20, 30, 40, 50, 60, 70, 80]

signalOpts = ["--skimPreselect", "--processEventVetoFastSimJets"]
signalSample = "SMS_T2tt_dM_10to80_genHT_160_genMET_80"

signalSets = {}
mass_dict = pickle.load(file("/data/nrad/cmgTuples/8020_mAODv2_v0/RunIISpring16MiniAODv2/%s_mass_dict.pkl"%signalSample))
for mstop in mass_dict.keys():
    signalSet =  {  'samples': [ [signalSample, '--processSignalScan', str(mstop), str(mlsp)]+signalOpts for mlsp in mass_dict[mstop].keys() ] }
    signalSets.update({ 'T2tt_old%s'%mstop:signalSet})

sampleSets.update(signalSets)


signalOpts = ["--skimPreselect", "--processEventVetoFastSimJets"]
signalSample = "SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1"
signalSets = {}
mass_dict = pickle.load(file("/data/nrad/cmgTuples/8020_mAODv2_v0/RunIISpring16MiniAODv2/%s_mass_dict.pkl"%signalSample))
for mstop in mass_dict.keys():
    signalSet =  {  'samples': [ [signalSample, '--processSignalScan', str(mstop), str(mlsp)]+signalOpts for mlsp in mass_dict[mstop].keys() ] }
    signalSets.update({ 'T2tt%s'%mstop:signalSet})
sampleSets.update(signalSets)


signalOpts = ["--skimPreselect", "--processEventVetoFastSimJets"]
signalSample = "SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1"
signalSets = {}
mass_dict = pickle.load(file("/data/nrad/cmgTuples/8020_mAODv2_v0/RunIISpring16MiniAODv2/%s_mass_dict.pkl"%signalSample))
for mstop in mass_dict.keys():
    signalSet =  {  'samples': [ [signalSample, '--processSignalScan', str(mstop), str(mlsp)]+signalOpts for mlsp in mass_dict[mstop].keys()] }
    signalSets.update({ 'T2bW%s'%mstop:signalSet})
sampleSets.update(signalSets)


all_samps = ['ttjets', 'wjets', 'dyjets','zjets', 'qcd', 'other' ] + [x for x in sampleSets.keys() if 'T2tt' in x or 'T2bW' in x]
all_samps = ['qcd', 'other']

sig_samps = [x for x in sampleSets.keys() if 'T2tt' in x and 'mWMin' not in x]
all_samps = sig_samps

all_samples = []
for samp in all_samps:
    all_samples.extend(sampleSets[samp]['samples'])

sampleSets['all'] = { 
                        'samples': all_samples,
                    }




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
        default='10',
        help="Number of processes to run in parallel"
        )

    argsRun.add_argument('--run',
        action='store_true',
        help="Run Post processing!"
        )
    
    argsRun.add_argument('--batchScript',
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
            'cmgPostProcessing_v2.py',
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
    if args.batchScript:
        fname = 'batch_script.sh'
        print 'writing batch script: %s'%fname
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
            print max_opt_lens
            print commands[0]
            for i, c in enumerate(commands):
                for io, o in enumerate(c):
                    max_opt_lens[io] = max(len(o), max_opt_lens[io])
            print max_opt_lens

            for c in commands:
                alignment_list = ['{:<%s}'%max_opt_lens[i] for i in range(len(c))]
                alignment = '  '.join(alignment_list)
                f.write("\n"+alignment.format(*c))
        else:
            for c in commands:
                f.write("\n"+'  '.join(c))
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
        print "\n Run the script adding the option --run to actually run over the chosen sample.\n "
        
    logger.info(
        "\n " + \
        "\n End of runPostProcessing run on sample set %s. \n" + \
        "\n *******************************************************************************\n",
        args.sampleSet
        )

        
if __name__ == "__main__":
    sys.exit(runPostProcessing())
