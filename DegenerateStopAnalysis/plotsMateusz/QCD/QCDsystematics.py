# QCDsystematics.py
# Script calculating the final QCD yields and systematics 
# Mateusz Zarucki 2016

import os, sys
import ROOT
import argparse
import pickle
import math
import numpy as np
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import makeSimpleLatexTable, setup_style, makeDir
from Workspace.HEPHYPythonTools import u_float

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--combineSys", dest = "combineSys",  help = "Combine systematics", type = int, default = 1)
parser.add_argument("--makeTable", dest = "makeTable",  help = "Make table", type = int, default = 0)
parser.add_argument("--calcFinalYields", dest = "calcFinalYields",  help = "Calculate final QCD yields", type = int, default = 0)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
combineSys = args.combineSys
makeTable = args.makeTable
calcFinalYields = args.calcFinalYields

path = {}
EWKsys = {}
QCDest = {}

tag = "8012_mAODv2_v3/80X_postProcessing_v10"
path['mu'] = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/QCD/muon/2D/estimation/METloose/loosenedIP/HT400MET300METloose200"%tag
path['el'] = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/QCD/electron/2D/estimation/METloose/invertedSigmaEtaEta/HT400MET300METloose200"%tag
path['combined'] = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/QCD/combined"%tag
   
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/QCD/systematics"%tag
makeDir(savedir)
makeDir(path['combined'])

QCDest['mu'] = pickle.load(open(path['mu'] +  "/QCDest_muon_HT400_MET300_METloose200.pkl", "r"))
EWKsys['mu'] = pickle.load(open(path['mu'] + "/EWKsys_muon_HT400_MET300_METloose200.pkl", "r"))

QCDest['el'] = pickle.load(open(path['el'] +  "/QCDest_electron_HT400_MET300_METloose200.pkl", "r"))
EWKsys['el'] = pickle.load(open(path['el'] + "/EWKsys_electron_HT400_MET300_METloose200.pkl", "r"))

regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1', 'SRH1', 'SRV1','SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']

QCDsys = {}
for x in ['mu', 'el']:
   QCDsys[x] = {}
   for reg in regions:
      QCDsys[x][reg] = {}
      QCDsys[x][reg]['val'] = QCDest[x][reg].val
      QCDsys[x][reg]['stat'] = QCDest[x][reg].sigma
      QCDsys[x][reg]['sys1'] = EWKsys[x][reg].val
      QCDsys[x][reg]['sys2'] = 0.5*QCDest[x][reg].val
      QCDsys[x][reg]['sys'] = math.sqrt(QCDsys[x][reg]['sys1']**2 + QCDsys[x][reg]['sys2']**2) 
      QCDsys[x][reg]['err'] = math.sqrt(QCDsys[x][reg]['stat']**2 + QCDsys[x][reg]['sys']**2 + QCDsys[x][reg]['sys2']**2) 

print "Muon: ", QCDsys['mu']
print "Electron: ", QCDsys['el']

if combineSys:
   QCDsys['combined'] = {}
         
   for reg in regions:
      QCDsys['combined'][reg] = {}
      QCDsys['combined'][reg]['val'] = QCDsys['mu'][reg]['val'] + QCDsys['el'][reg]['val']
      QCDsys['combined'][reg]['stat'] = math.sqrt(QCDsys['mu'][reg]['stat']**2 + QCDsys['el'][reg]['stat']**2)
      QCDsys['combined'][reg]['sys1'] = math.sqrt(QCDsys['mu'][reg]['sys1']**2 + QCDsys['el'][reg]['sys1']**2)
      QCDsys['combined'][reg]['sys2'] = math.sqrt(QCDsys['mu'][reg]['sys2']**2 + QCDsys['el'][reg]['sys2']**2)
      QCDsys['combined'][reg]['sys'] = math.sqrt(QCDsys['mu'][reg]['sys']**2 + QCDsys['el'][reg]['sys']**2) 
      QCDsys['combined'][reg]['err'] = math.sqrt(QCDsys['mu'][reg]['err']**2 + QCDsys['el'][reg]['err']**2)
   
   print "Combined: ", QCDsys['combined']
   
   pickleFile1 = open("%s/QCDsystematics_muon.pkl"%(path['combined']), "w")
   pickle.dump(QCDsys['mu'], pickleFile1)
   pickleFile1.close()
    
   pickleFile2 = open("%s/QCDsystematics_ele.pkl"%(path['combined']), "w")
   pickle.dump(QCDsys['el'], pickleFile2)
   pickleFile2.close()
   
   pickleFile3 = open("%s/QCDsystematics_combined.pkl"%(path['combined']), "w")
   pickle.dump(QCDsys['combined'], pickleFile3)
   pickleFile3.close()

   if calcFinalYields:
   
      QCDyields_stat = {}
      QCDyields_sys = {}
      QCDyields_sys1 = {}
      QCDyields_sys2 = {}
      
      regions = ['SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']
      
      for reg in regions:
         QCDyields_stat[reg] = u_float.u_float(QCDsys['combined'][reg]['val'], QCDsys['combined'][reg]['stat'])
         QCDyields_sys[reg] = u_float.u_float(QCDsys['combined'][reg]['val'], QCDsys['combined'][reg]['sys'])
         QCDyields_sys1[reg] = u_float.u_float(QCDsys['combined'][reg]['val'], QCDsys['combined'][reg]['sys1'])
         QCDyields_sys2[reg] = u_float.u_float(QCDsys['combined'][reg]['val'], QCDsys['combined'][reg]['sys2'])
     
      publicdir = "/afs/hephy.at/user/m/mzarucki/public/QCD" 
      makeDir(publicdir)
     
      pickleFile4 = open("%s/QCDyields_stat.pkl"%(publicdir), "w")
      pickle.dump(QCDyields_stat, pickleFile4)
      pickleFile4.close()
      
      pickleFile5 = open("%s/QCDyields_sys.pkl"%(publicdir), "w")
      pickle.dump(QCDyields_sys, pickleFile5)
      pickleFile5.close()
      
      pickleFile6 = open("%s/QCDyields_sys1.pkl"%(publicdir), "w")
      pickle.dump(QCDyields_sys1, pickleFile6)
      pickleFile6.close()
      
      pickleFile6 = open("%s/QCDyields_sys2.pkl"%(publicdir), "w")
      pickle.dump(QCDyields_sys2, pickleFile6)
      pickleFile6.close()
      
      #pickleFile2 = open("%s/Yields_12864pbm1_PreApp_Mt95_Inccharge_LepAll_lep_pu_SF_presel_BinsSummary_QCDest.pkl"%(savedir), "w")
      #pickle.dump(allYields, pickleFile2)
      #pickleFile2.close()

if makeTable:
   print "Making table"
   QCDrows = []
   listTitle = ['$\mathbf{Region}$', '$\mathbf{Electron~Channel}~[\pm (stat.) \pm (sys.)]$', '$\mathbf{Muon~Channel}~[\pm (stat.) \pm (sys.)]$', '$\mathbf{Total}~[\pm (stat.) \pm (sys.)]$']
   #listTitle = ['Region', 'electron', 'muon', 'combined']
   QCDrows.append(listTitle)
   for reg in regions:
      QCDrow = [reg,
      "$%.2f"%(QCDsys['el'][reg]['val']) +       "\pm" + "%.2f"%(QCDsys['el'][reg]['stat']) + " \pm" + "%.2f"%(QCDsys['el'][reg]['sys']) + "$", 
      "$%.2f"%(abs(QCDsys['mu'][reg]['val'])) +       "\pm" + "%.2f"%(QCDsys['mu'][reg]['stat']) + " \pm" + "%.2f"%(QCDsys['mu'][reg]['sys']) + "$", 
      "$%.2f"%(QCDsys['combined'][reg]['val']) + "\pm" + "%.2f"%(QCDsys['combined'][reg]['stat']) + "\pm" + "%.2f"%(QCDsys['combined'][reg]['sys']) + "$"] 
      #u_float.u_float(QCDsys['el'][reg]['val'], QCDsys['el'][reg]['err']).round(3), 
      #u_float.u_float(QCDsys['mu'][reg]['val'], QCDsys['mu'][reg]['err']).round(3), 
      #u_float.u_float(QCDsys['combined'][reg]['val'], QCDsys['combined'][reg]['err']).round(3)]
      QCDrows.append(QCDrow)

   makeSimpleLatexTable(QCDrows, "QCDyields", savedir)
