# ZinvCorrection.py
# Script summarising the correction factors for each SR in a table 
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
parser.add_argument("--CT2", dest = "CT2",  help = "CT2 cut", type = str, default = "75")
parser.add_argument("--lepEta", dest = "lepEta",  help = "Extra soft lepton eta", type = str, default = "2.5")
#parser.add_argument("--channel", dest = "channel",  help = "Channel to be used for correction", type = str, default = "combined") #Zmumu, Zee, combined
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
CT2 = args.CT2
lepEta = args.lepEta
#channel = args.channel

tag = "8012_mAODv2_v3/80X_postProcessing_v10"
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/Zinv/corrections/lepEta%s"%(tag,lepEta)
makeDir(savedir)

regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1', 'SRH1', 'SRV1', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']
 
ZinvRows = []
listTitle = ['SR', 'Zmumu: Correction electrons', 'Zmumu: Correction muons', 'Zee: Correction electrons', 'Zee: Correction muons', 'Combined: Correction electrons', 'Combined: Correction muons']
ZinvRows.append(listTitle)

corrections = {}
for SR in regions:
   path = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/Zinv/systematics/lepEta%s/%s"%(tag,lepEta,SR)
   corrections[SR] = pickle.load(open("%s/ZinvCorrections_%s.pkl"%(path,SR), "r"))

   ZinvRow = [SR, corrections[SR]['Zmumu']['CT' + CT2]['electrons'].round(2), corrections[SR]['Zmumu']['CT' + CT2]['muons'].round(2),
                  corrections[SR]['Zee']['CT' + CT2]['electrons'].round(2), corrections[SR]['Zee']['CT' + CT2]['muons'].round(2),
                  corrections[SR]['combined']['CT' + CT2]['electrons'].round(2), corrections[SR]['combined']['CT' + CT2]['muons'].round(2)]
   #ZinvRow.extend([x.round(4) for x in ZinvRatios[channel]['CT' + CT2].values()])
   ZinvRows.append(ZinvRow)

makeSimpleLatexTable(ZinvRows, "ZinvCorrectionsTable", savedir)
