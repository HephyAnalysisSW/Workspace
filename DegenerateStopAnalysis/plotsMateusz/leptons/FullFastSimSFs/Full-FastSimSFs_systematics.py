# Full-FastSimSFs_systematics.py
# Script combinding factored and central Full-FastSim SFs (with extra systematic) 
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
parser.add_argument("--addSys", dest = "addSys",  help = "Add systematic", type = int, default = 1)
parser.add_argument("--plot", dest = "plot",  help = "Toggle plot", type = int, default = 1)
parser.add_argument("--save", dest="save",  help="Toggle save", type=int, default=1)
parser.add_argument("--verbose", dest="verbose",  help="Verbosity switch", type=int, default=1)
parser.add_argument("-b", dest="batch",  help="Batch mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
addSys = args.addSys
plot = args.plot
save = args.save
verbose = args.verbose

tag = "8012_mAODv2_v3_1/80X_postProcessing_v10"

path1 = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/leptonSFs/factored/ID_base/HI+IP"%tag
path2 = "/afs/hephy.at/data/mzarucki01/leptonSFs/FullSim-FastSim"
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/leptonSFs/systematics"%tag
publicdir = "/afs/hephy.at/user/m/mzarucki/public"

makeDir(savedir + "/pdf")
makeDir(savedir + "/root")

ROOT.gStyle.SetOptStat(0)

regions = ['SRL', 'SRH', 'SRV']

SFs = {'factored':{'el':{}, 'mu':{}}, 'central':{'el':{}, 'mu':{}}, 'total':{'el':{}, 'mu':{}}}
hists = {'factored':{'el':{}, 'mu':{}}, 'central':{'el':{}, 'mu':{}}, 'total':{'el':{}, 'mu':{}}}

hists['factored']['el'] = pickle.load(open(path1 + "/standardBins/varBins/Electron/FullSim-FastSim_SFs_factored_ratios_HI+IP_el.pkl", "r"))
hists['factored']['mu'] = pickle.load(open(path1 + "/standardBins/varBins/Muon/FullSim-FastSim_SFs_factored_ratios_HI+IP_mu.pkl", "r"))
hists['factored']['el']['pt'] = hists['factored']['el']['Full-Fast']['pt']
hists['factored']['mu']['pt'] = hists['factored']['mu']['Full-Fast']['pt']
#hists['factored']['el']['2D'] = hists['factored']['el']['Full-Fast']['2D']
#hists['factored']['mu']['2D'] = hists['factored']['mu']['Full-Fast']['2D']

#SFs['factored']['el']['pt'] = pickle.load(open(path1 + "/standardBins/varBins/Electron/FullSim-FastSim_SFs_factored_HI+IP_el.pkl", "r"))
#SFs['factored']['mu']['pt'] = pickle.load(open(path1 + "/standardBins/varBins/Muon/FullSim-FastSim_SFs_factored_HI+IP_mu.pkl", "r"))

f1 = ROOT.TFile(path2 + "/Full-FastSimSFs_mu_LooseID.root")
f2 = ROOT.TFile(path2 + "/Full-FastSimSFs_el_VetoID.root")
hists['central']['mu']['2D'] = f1.Get("histo2D")
hists['central']['el']['2D'] = f2.Get("histo2D")

#NOTE: If you intend to use the errors of this histogram later you should call Sumw2 before making this operation. This is particularly important if you fit the histogram after TH1::Divide

for lep in ['el', 'mu']:
   if lep == 'el': lepton = 'Electron'
   elif lep == 'mu': lepton = 'Muon'

   hists['central'][lep]['pt'] = ROOT.TH1D()
   hists['central'][lep]['2D'].ProjectionX().Copy(hists['central'][lep]['pt'])#ProfileX()
   hists['central'][lep]['pt'].Sumw2()

   if addSys: hists['central'][lep]['pt'] = addSystematicHist(hists['central'][lep]['pt'], 2)

   if lep == 'el': hists['central'][lep]['pt'].Scale(1./3.)
   elif lep == 'mu': hists['central'][lep]['pt'].Scale(1./4.)

   hists['factored'][lep]['pt'].SetTitle("%ss: Factorised HI & IP FullSim-FastSim SFs in TTJets Sample"%(lepton))
   hists['central'][lep]['pt'].SetTitle("%ss: Central %s ID FullSim-FastSim SFs in TTJets Sample"%(lepton, lepton))
   hists['central'][lep]['pt'].SetMinimum(0.8)
   hists['central'][lep]['pt'].SetMaximum(1.1)
   hists['central'][lep]['pt'].GetXaxis().SetTitle("%s p_{T}"%lepton)
   hists['central'][lep]['pt'].GetYaxis().SetTitle("FullSim-FastSim SF")
   hists['central'][lep]['pt'].GetXaxis().CenterTitle()
   hists['central'][lep]['pt'].GetYaxis().CenterTitle()
   #hists['total']['pt'].GetXaxis().SetLimits(0,200)

   hists['factored'][lep]['pt'].Sumw2()
   hists['central'][lep]['pt'].Sumw2()

   hists['total'][lep]['pt'] = multiplyHists(hists['factored'][lep]['pt'], hists['central'][lep]['pt'])
   #hists['total'][lep]['pt'] = hists['factored'][lep]['pt'].Clone()*hists['central'][lep]['pt'].Clone()
   hists['total'][lep]['pt'].SetName("2D_SF_total")
   hists['total'][lep]['pt'].SetTitle("%ss: Total FullSim-FastSim SFs in TTJets Sample"%(lepton))
   hists['total'][lep]['pt'].GetXaxis().SetTitle("%s p_{T}"%lepton)
   hists['total'][lep]['pt'].GetYaxis().SetTitle("FullSim-FastSim SF")
   hists['total'][lep]['pt'].SetMinimum(0.8)
   hists['total'][lep]['pt'].SetMaximum(1.1)
   
   c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
   c1.Divide(1,3)
    
   c1.cd(1)
   hists['central'][lep]['pt'].Draw() 
   #alignStats(hists['central'][lep]['pt'])
   c1.cd(2)
   hists['factored'][lep]['pt'].Draw() 
   c1.cd(3)
   hists['total'][lep]['pt'].Draw() 
   #alignStats(hists['total'][lep]['pt'])
   
   c1.Modified()
   c1.Update()
   
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      c1.SaveAs("%s/FullSim-FastSimSFs_total_%s.png"%(savedir, lep))
      c1.SaveAs("%s/pdf/FullSim-FastSimSFs_total_%s.png"%(savedir, lep))
      c1.SaveAs("%s/pdf/FullSim-FastSimSFs_total_%s.png"%(savedir, lep))
