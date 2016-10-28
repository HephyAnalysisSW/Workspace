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
parser.add_argument("--saveYields", dest = "saveYields",  help = "Calculate final QCD yields", type = int, default = 0)
parser.add_argument("--makeProjection", dest = "makeProjection",  help = "Make projection", type = int, default = 0)
parser.add_argument("--makeTable", dest = "makeTable",  help = "Make table", type = int, default = 0)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
combineSys = args.combineSys
saveYields = args.saveYields
makeProjection = args.makeProjection
makeTable = args.makeTable

path = {}
EWKsys = {}
QCDest = {}

tag = "8012_mAODv2_v3/80X_postProcessing_v10"
path['mu'] = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/QCD/muon/2D/estimation/METloose/loosenedIP/HT400MET300METloose200"%tag
path['el'] = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/QCD/electron/2D/estimation/METloose/invertedSigmaEtaEta/HT400MET300METloose200"%tag
path['combined'] = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/QCD/combined"%tag
   
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/QCD/systematics"%tag
publicdir = "/afs/hephy.at/user/m/mzarucki/public/results/QCD" 
makeDir(savedir)
makeDir(publicdir)
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

   if saveYields:
   
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
     
      pickleFile4 = open("%s/QCDyields_stat.pkl"%(publicdir), "w")
      pickle.dump(QCDyields_stat, pickleFile4)
      pickleFile4.close()
      
      pickleFile5 = open("%s/QCDyields_sys.pkl"%(publicdir), "w")
      pickle.dump(QCDyields_sys, pickleFile5)
      pickleFile5.close()
      
      pickleFile6 = open("%s/QCDyields_sys1.pkl"%(publicdir), "w")
      pickle.dump(QCDyields_sys1, pickleFile6)
      pickleFile6.close()
      
      pickleFile7 = open("%s/QCDyields_sys2.pkl"%(publicdir), "w")
      pickle.dump(QCDyields_sys2, pickleFile7)
      pickleFile7.close()
      
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

if makeProjection:
   regions = ['SR1a', 'SR1b', 'SR1c', 'SRL1', 'SRH1', 'SRV1']
   
   QCDyields_stat = {}
   QCDyields_sys = {}
   
   for reg in regions:
      QCDyields_stat[reg] = u_float.u_float(QCDsys['combined'][reg]['val'], QCDsys['combined'][reg]['stat'])
      QCDyields_sys[reg] = u_float.u_float(QCDsys['combined'][reg]['val'], QCDsys['combined'][reg]['sys'])
  
   SRLHV_stat = QCDyields_stat['SRL1'] + QCDyields_stat['SRH1'] + QCDyields_stat['SRV1']

   L_stat = QCDyields_stat['SRL1']/SRLHV_stat
   H_stat = QCDyields_stat['SRH1']/SRLHV_stat
   V_stat = QCDyields_stat['SRV1']/SRLHV_stat
   
   QCDprojection_stat = {'SRL1a': QCDyields_stat['SR1a']*L_stat,
                         'SRL1b': QCDyields_stat['SR1b']*L_stat,
                         'SRL1c': QCDyields_stat['SR1c']*L_stat,
                         'SRH1a': QCDyields_stat['SR1a']*H_stat,
                         'SRH1b': QCDyields_stat['SR1b']*H_stat,
                         'SRH1c': QCDyields_stat['SR1c']*H_stat,
                         'SRV1a': QCDyields_stat['SR1a']*V_stat,
                         'SRV1b': QCDyields_stat['SR1b']*V_stat,
                         'SRV1c': QCDyields_stat['SR1c']*V_stat}
   
   SRLHV_sys = QCDyields_sys['SRL1'] + QCDyields_sys['SRH1'] + QCDyields_sys['SRV1']

   L_sys = QCDyields_sys['SRL1']/SRLHV_sys
   H_sys = QCDyields_sys['SRH1']/SRLHV_sys
   V_sys = QCDyields_sys['SRV1']/SRLHV_sys
   
   factors = {'stat':{'L':L_stat, 'H':H_stat, 'V':V_stat}, 'sys':{'L':L_sys, 'H':H_sys, 'V':V_sys}}

   QCDprojection_sys =  {'SRL1a': QCDyields_sys['SR1a']*L_sys,
                         'SRL1b': QCDyields_sys['SR1b']*L_sys,
                         'SRL1c': QCDyields_sys['SR1c']*L_sys,
                         'SRH1a': QCDyields_sys['SR1a']*H_sys,
                         'SRH1b': QCDyields_sys['SR1b']*H_sys,
                         'SRH1c': QCDyields_sys['SR1c']*H_sys,
                         'SRV1a': QCDyields_sys['SR1a']*V_sys,
                         'SRV1b': QCDyields_sys['SR1b']*V_sys,
                         'SRV1c': QCDyields_sys['SR1c']*V_sys}

   print "Making table"
   QCDrows = []
   listTitle = ['$\mathbf{Region}$', '$\mathbf{Total}~~[\pm (stat.) \pm (sys.)]$']
   #listTitle = ['Region', 'electron', 'muon', 'combined']
   QCDrows.append(listTitle)
   
   regions = ['SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']

   for reg in regions:
      QCDrow = [reg, 
      "$%.2f"%(QCDprojection_stat[reg].val) + "\pm" + "%.2f"%(QCDprojection_stat[reg].sigma) + " \pm" + "%.2f"%(QCDprojection_sys[reg].sigma) + "$"]
      QCDrows.append(QCDrow)

   makeSimpleLatexTable(QCDrows, "QCDprojection", savedir)
   
   if saveYields:
      
      pickleFile7 = open("%s/QCDprojection_stat.pkl"%(publicdir), "w")
      pickle.dump(QCDprojection_stat, pickleFile7)
      pickleFile7.close()
      
      pickleFile8 = open("%s/QCDprojection_sys.pkl"%(publicdir), "w")
      pickle.dump(QCDprojection_sys, pickleFile8)
      pickleFile8.close()
      
      pickleFile9 = open("%s/QCDprojection_factors.pkl"%(publicdir), "w")
      pickle.dump(factors, pickleFile9)
      pickleFile9.close()

if combineWithProjection:
   tabledir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/QCD/systematics/finalTable"%tag
   
   makeDir(tabledir)
   
   QCDyields_stat = pickle.load(file("%s/QCDyields_stat.pkl"%(publicdir)))
   QCDyields_sys = pickle.load(file("%s/QCDyields_sys.pkl"%(publicdir)))
   #QCDyields_sys1 = pickle.load(file("%s/QCDyields_sys1.pkl"%(publicdir)))
   #QCDyields_sys2 = pickle.load(file("%s/QCDyields_sys2.pkl"%(publicdir)))
   
   QCDprojection_stat = pickle.load(file("%s/QCDprojection_stat.pkl"%(publicdir)))
   QCDprojection_sys = pickle.load(file("%s/QCDprojection_sys.pkl"%(publicdir)))
   #QCDprojection_sys1 = pickle.load(file("%s/QCDprojection_sys1.pkl"%(publicdir)))
   #QCDprojection_sys2 = pickle.load(file("%s/QCDprojection_sys2.pkl"%(publicdir)))

   regions = ['SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c', 'SR2', 'SRL2', 'SRH2', 'SRV2']

   for reg in regions:
      #print reg, " Before: ", QCDyields_stat[reg]
      if not QCDyields_stat[reg].val: #if yield = 0
         QCDyields_stat[reg] = QCDprojection_stat[reg]
         QCDyields_sys[reg] = QCDprojection_sys[reg]
   
      #print reg, " After: ", QCDyields_stat[reg]
   
   if makeTable:
   
      print "Making table"
      QCDrows = []
      listTitle = ['$\mathbf{Region}$', '$\mathbf{Total}~~[\pm (stat.) \pm (sys.)]$']
      #listTitle = ['Region', 'electron', 'muon', 'combined']
      QCDrows.append(listTitle)
   
      for reg in regions:
         QCDrow = [reg,
         "$%.2f"%(QCDyields_stat[reg].val) + "\pm" + "%.2f"%(QCDyields_stat[reg].sigma) + " \pm" + "%.2f"%(QCDyields_sys[reg].sigma) + "$"]
         QCDrows.append(QCDrow)
   
      makeSimpleLatexTable(QCDrows, "QCDfinalYields", tabledir)
   
   if saveYields:
      pickleFile4 = open("%s/QCDyields_final_stat.pkl"%(publicdir), "w")
      pickle.dump(QCDyields_stat, pickleFile4)
      pickleFile4.close()
   
      pickleFile5 = open("%s/QCDyields_final_sys.pkl"%(publicdir), "w")
      pickle.dump(QCDyields_sys, pickleFile5)
      pickleFile5.close()
   
      #pickleFile6 = open("%s/QCDyields_final_sys1.pkl"%(publicdir), "w")
      #pickle.dump(QCDyields_sys1, pickleFile6)
      #pickleFile6.close()
      #
      #pickleFile7 = open("%s/QCDyields_final_sys2.pkl"%(publicdir), "w")
      #pickle.dump(QCDyields_sys2, pickleFile7)
      #pickleFile7.close()
   
      #pickleFile2 = open("%s/Yields_12864pbm1_PreApp_Mt95_Inccharge_LepAll_lep_pu_SF_presel_BinsSummary_QCDest.pkl"%(savedir), "w")
      #pickle.dump(allYields, pickleFile2)
      #pickleFile2.close()
