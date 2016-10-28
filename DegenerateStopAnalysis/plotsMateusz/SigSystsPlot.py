# SigSystsPlot.py
# Script for plotting the signal systematics
# Mateusz Zarucki 2016

import ROOT
import os, sys
import argparse
import pickle
#import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import makeDir, setup_style
#from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--SR", dest = "SR",  help = "Signal region", type = str, default = "SR1a")
parser.add_argument("--syst", dest = "syst",  help = "Systematic", type = str, default = "PU")
parser.add_argument("--plot", dest = "plot",  help = "Plot", type = int, default = 0)
parser.add_argument("--makeProjection", dest = "makeProjection",  help = "Make projection", type = int, default = 0)
parser.add_argument("--logy", dest = "logy",  help = "Toggle logy", type = int, default = 1)
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
SR = args.SR
syst = args.syst
logy = args.logy
plot = args.plot
makeProjection = args.makeProjection
save = args.save
verbose = args.verbose

print makeDoubleLine()
print "Plotting Signal Systematics for", syst, "in", SR 
print makeDoubleLine()
 
#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   tag = "8012_mAODv2_v3/80X_postProcessing_v10"
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/SigSysPlots"%tag
   savedir2 = savedir + "/" + syst + "/" + SR 
   if not os.path.exists("%s/root"%(savedir2)): os.makedirs("%s/root"%(savedir2))
   if not os.path.exists("%s/pdf"%(savedir2)): os.makedirs("%s/pdf"%(savedir2))

path = "/afs/hephy.at/user/n/nrad/public/WPolQ2ZInvFix_v0/SystDict.pkl"
#path = "/afs/hephy.at/work/m/mzarucki/CMSSW/CMSSW_8_0_7/src/Workspace/DegenerateStopAnalysis/results/2016/8012_mAODv2_v3/80X_postProcessing_v10/ApprovalSys_Mt95_Inccharge_LepAll_lep_pu_SF/SystDict.pkl"

SystDict = pickle.load(open(path))

#SRs = ['SR1a', 'SR1b', 'SR1c', 'SR2']
#SigSys = ['PU', 'jec', 'jer', 'BTag_l', 'BTag_b', 'BTag_FS', 'ISR', 'met', 'Q2']#, 'lepEff'] 
#BkgSys = ['WPtShape', 'ttPtShape', 'ttpt', 'WPt', 'QCDEst', 'ZInvEst', 'DibosonXSec', 'DYJetsM50XSec', 'STXSec', 'WPol']

if not os.path.isfile("%s/avgSys.pkl"%savedir):
   avgSys = {syst:{}}
else:
   avgSys = pickle.load(open("%s/avgSys.pkl"%savedir))

total = 0.
counter = 0.
for sig in SystDict[syst]:
   if 'T2tt' in sig:
      total += SystDict[syst][sig][SR]
      counter += 1.
      #print "Total: ", counter, ":", total 

avgSys[syst][SR] = total/counter

pickleFile = open("%s/avgSys.pkl"%savedir, "w")
pickle.dump(avgSys, pickleFile)
pickleFile.close()

print "Average sys. :", avgSys[syst][SR]

if plot:
   hist = empty2Dhist(52, 200, 850, 18, 0, 90)
   
   for sig in SystDict[syst]:
      if 'T2tt' in sig:
         nameList = sig.split('-')
         del nameList[0]
         mStop, mLSP = nameList
   
         hist.Fill(int(mStop), int(mStop) - int(mLSP), round(SystDict[syst][sig][SR],1))
         #print "mStop, mLSP, sys: ", sig, mStop, mLSP, SystDict[syst][sig][SR]
   
   canv = ROOT.TCanvas("canv", "Canvas", 1800, 1500)
   
   hist.SetName("hist")
   hist.SetTitle(syst + "_" + SR)
   hist.GetXaxis().SetTitle("m_{stop}")
   hist.GetYaxis().SetTitle("#Deltam")
   #hist.SetFillColor(samples['w'].color)
   #hist.SetFillColorAlpha(hist.GetFillColor(), 0.7)
   #hist.SetLineColor(ROOT.kBlack)
   #hist.SetLineWidth(3)
   hist.SetMinimum(0.1)
   
   #hist.SetLineColor(ROOT.kBlack)
   #hist.SetLineWidth(3)
   hist.Draw('colz text')
   
   latex = ROOT.TLatex()
   latex.SetNDC()
   latex.SetTextSize(0.04)
   latex.DrawLatex(0.16,0.96,"#font[22]{CMS Preliminary}")
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
  
   if makeProjection: 
      canv2 = ROOT.TCanvas("canv2", "Canvas 2", 1800, 1500)
      hist_x = hist.ProjectionX()
      #hist_x = hist.ProfileX()
      hist_x.Scale(float(1)/float(8))
      #Divide(hist_x, 23)
      hist_x.Draw('p')

      canv3 = ROOT.TCanvas("canv3", "Canvas 3", 1800, 1500)
      hist_y = hist.ProjectionY()
      #hist_y = hist.ProfileY()
      #Divide(hist_y, 8)
      hist_y.Scale(float(1)/float(23))
      hist_y.Draw('p')

   #Save canvas
   if save: #web address: http://www.hephy.at/user/mzarucki/plots
      canv.SaveAs("%s/SigSystsPlot_%s_%s.png"%(savedir2, syst, SR))
      canv.SaveAs("%s/root/SigSystsPlot_%s_%s.root"%(savedir2, syst, SR))
      canv.SaveAs("%s/pdf/SigSystsPlot_%s_%s.pdf"%(savedir2, syst, SR))
   
      if makeProjection:
         canv2.SaveAs("%s/SigSystsProjectionX_%s_%s.png"%(savedir2, syst, SR))
         canv2.SaveAs("%s/root/SigSystsProjectionX_%s_%s.root"%(savedir2, syst, SR))
         canv2.SaveAs("%s/pdf/SigSystsProjectionX_%s_%s.pdf"%(savedir2, syst, SR))
         canv3.SaveAs("%s/SigSystsProjectionY_%s_%s.png"%(savedir2, syst, SR))
         canv3.SaveAs("%s/root/SigSystsProjectionY_%s_%s.root"%(savedir2, syst, SR))
         canv3.SaveAs("%s/pdf/SigSystsProjectionY_%s_%s.pdf"%(savedir2, syst, SR))
