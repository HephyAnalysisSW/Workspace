# SigSystsTable.py
# Script for creating signal systematics table
# Mateusz Zarucki 2016

import ROOT
import os, sys
import argparse
import pickle
#import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import makeSimpleLatexTable, makeDir, setup_style
#from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--makeTable", dest = "makeTable",  help = "Make table", type = int, default = 1)
parser.add_argument("--save", dest = "save",  help = "Toggle save", type = int, default = 1)
parser.add_argument("--verbose", dest = "verbose",  help = "Verbosity switch", type = int, default = 0)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
makeTable = args.makeTable
save = args.save
verbose = args.verbose

print makeDoubleLine()
print "Making Signal Systematics table" 
print makeDoubleLine()
 
#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   tag = "8012_mAODv2_v3/80X_postProcessing_v10"
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/SigSysPlots/"%tag
   savedir2 = savedir + "/table"
   if not os.path.exists("%s/root"%(savedir2)): os.makedirs("%s/root"%(savedir2))
   if not os.path.exists("%s/pdf"%(savedir2)): os.makedirs("%s/pdf"%(savedir2))

avgSys = pickle.load(open("%s/avgSys.pkl"%savedir))

SigSys = ['PU', 'jec', 'jer', 'BTag_l', 'BTag_b', 'BTag_FS', 'ISR', 'met', 'Q2']#, 'lepEff']
SigSys2 = ['PU', 'JEC/JER', 'BTag', 'ISR', 'met', 'Q2']#, 'lepEff']
#BkgSys = ['WPtShape', 'ttPtShape', 'ttpt', 'WPt', 'QCDEst', 'ZInvEst', 'DibosonXSec', 'DYJetsM50XSec', 'STXSec', 'WPol']
SRs = ['SR1a', 'SR1b', 'SR1c', 'SR2']

avgSysCombined = avgSys.copy()

del avgSysCombined['jec']
del avgSysCombined['jer']
del avgSysCombined['BTag_l']
del avgSysCombined['BTag_b']
del avgSysCombined['BTag_FS']

avgSysCombined['BTag'] = {}
avgSysCombined['JEC/JER'] = {}

for SR in SRs:
   avgSysCombined['BTag'][SR] = math.sqrt(avgSys['BTag_l'][SR]**2 + avgSys['BTag_b'][SR]**2 + avgSys['BTag_FS'][SR]**2)
   avgSysCombined['JEC/JER'][SR] = math.sqrt(avgSys['jec'][SR]**2 + avgSys['jer'][SR]**2)

if makeTable:
   print "Making table"
   rows = []
   listTitle = ['$\mathbf{Systematic Effect}$', '$\mathbf{SR1a}$', '$\mathbf{SR1b}$', '$\mathbf{SR1c}$', '$\mathbf{SR2}$']
   rows.append(listTitle)
   for sys in SigSys:
      #rows.append([reg, str(avgSys[reg]['original'].round(2)), str(avgSys[reg]['corrected'].round(2)), str(ratios[reg]['original'].round(2)), str(ratios[reg]['corrected'].round(2)), str(ratios[reg]['ratio'].round(2))])
      rows.append([sys, "$%.2f$"%(avgSys[sys]['SR1a']), "$%.2f$"%(avgSys[sys]['SR1b']), "$%.2f$"%(avgSys[sys]['SR1c']), "$%.2f$"%(avgSys[sys]['SR2'])]) 
   rows.append(["Lep. Eff.", "$%.2f$"%(5), "$%.2f$"%(5), "$%.2f$"%(5), "$%.2f$"%(5)]) 
   rows.append(["Lumi", "$%.2f$"%(6.2), "$%.2f$"%(6.2), "$%.2f$"%(6.2), "$%.2f$"%(6.2)]) 
   rows.append(["FastSim/FullSim Lep. Eff.", "$%.2f$"%(5), "$%.2f$"%(5), "$%.2f$"%(5), "$%.2f$"%(5)]) 
   makeSimpleLatexTable(rows, "SignalSystsTable", savedir2)

   rows = []
   listTitle = ['$\mathbf{Systematic Effect}$', '$\mathbf{SR1a}$', '$\mathbf{SR1b}$', '$\mathbf{SR1c}$', '$\mathbf{SR2}$']
   rows.append(listTitle)
   for sys in SigSys2:
      #rows.append([reg, str(avgSys[reg]['original'].round(2)), str(avgSys[reg]['corrected'].round(2)), str(ratios[reg]['original'].round(2)), str(ratios[reg]['corrected'].round(2)), str(ratios[reg]['ratio'].round(2))])
      rows.append([sys, "$%.2f$"%(avgSysCombined[sys]['SR1a']), "$%.2f$"%(avgSysCombined[sys]['SR1b']), "$%.2f$"%(avgSysCombined[sys]['SR1c']), "$%.2f$"%(avgSysCombined[sys]['SR2'])]) 
   rows.append(["Lep. Eff.", "$%.2f$"%(5), "$%.2f$"%(5), "$%.2f$"%(5), "$%.2f$"%(5)]) 
   rows.append(["Lumi", "$%.2f$"%(6.2), "$%.2f$"%(6.2), "$%.2f$"%(6.2), "$%.2f$"%(6.2)]) 
   rows.append(["FastSim/FullSim Lep. Eff.", "$%.2f$"%(5), "$%.2f$"%(5), "$%.2f$"%(5), "$%.2f$"%(5)]) 
   makeSimpleLatexTable(rows, "SignalSystsTableCombined", savedir2)

