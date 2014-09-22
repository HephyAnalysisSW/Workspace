import copy
import ROOT
from Workspace.RA4Analysis.simplePlotsCommon import *
from math import *
import os, copy, array

def drawComp(c,d, var, cut1, cut2, binning=[100,0,1000], normalize = False):
  bstring = repr(binning).replace("[","(").replace("]",")")
  htmp1=ROOT.TH1F("htmpSPK1","htmpSPK",*binning)
  htmp2=ROOT.TH1F("htmpSPK2","htmpSPK",*binning)
  c.Draw(var+">>htmpSPK1"+bstring, cut1)
  d.Draw(var+">>htmpSPK2"+bstring, cut2)
  ha = ROOT.gDirectory.Get("htmpSPK1")
  hb = ROOT.gDirectory.Get("htmpSPK2")
  ha.Draw()
  if normalize:
    hb.Scale(ha.Integral()/hb.Integral())
  hb.SetLineColor(ROOT.kRed)
  hb.Draw("same")
  del ha
  del hb

#c = ROOT.TChain("pfRA4Analyzer/Events")
#c.Add("/scratch/schoef/pat_110917/Mu/TTJets-noTrig/histo_*.root")
#d = ROOT.TChain("RA4MCAnalyzer/Events")
#d.Add("/scratch/schoef/pat_110924/pythia6/TTJets-met50/histo_*.root")
#
#htvals = [[0,100000],[300,400],[400,500],[500,600],[600,700],[700,800],[800,900],[900,1000],[1000,1200],[1200,1400]]
#for htInterval in htvals:
#  cutstring = "ht>"+str(htInterval[0])+"&&ht<"+str(htInterval[1])+"&&genmet>50"
#  c1 = ROOT.TCanvas()
#  drawComp(c,d,"genmet",cutstring,cutstring, [100,0,1000], True)
#  ROOT.gPad.SetLogy()
#  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngMC/TT_MCVSPYTHIA_genmet_ht_"+str(htInterval[0])+"_"+str(htInterval[1])+".png")
#
#c1 = ROOT.TCanvas()
#drawComp(c,d,"ht","genmet>50","genmet>50", [100,0,1000], True)
#ROOT.gPad.SetLogy()
#c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngMC/TT_MCVSPYTHIA_htVSgenHT_for_genmet50.png")

def drawXA(c, cut=""):
  c.Draw("sqrt(top_m0_pt*top_m0_pt + top_m0_pz*top_m0_pz)/3500.>>hg(100,0,1)",addCutString(cut, "(abs(top_m0_pdgId)==21)"))
  c.Draw("sqrt(top_m0_pt*top_m0_pt + top_m0_pz*top_m0_pz)/3500.>>hu(100,0,1)",addCutString(cut, "(abs(top_m0_pdgId)==1)" ))
  c.Draw("sqrt(top_m0_pt*top_m0_pt + top_m0_pz*top_m0_pz)/3500.>>hd(100,0,1)",addCutString(cut, "(abs(top_m0_pdgId)==2)" ))
  hg = ROOT.hg
  hu = ROOT.hu
  hd = ROOT.hd
  hu.SetLineColor(ROOT.kRed)
  hd.SetLineColor(ROOT.kBlue)
  hg.Draw()
  hu.Draw("same")
  hd.Draw("same")
  del ROOT.hg 
  del ROOT.hu
  del ROOT.hd

def getExpParameter(c, htInterval, cut="", lowerMETcut = 100, upperMETcut=1000):
  cutstring = addCutString(cut, "ht>"+str(htInterval[0])+"&&ht<"+str(htInterval[1]))
  print "Using",cutstring
  htmp=ROOT.TH1F("htmpSPK","htmpSPK",100,0,1000)
  c.Draw("genmet>>htmpSPK", cutstring)
  resWOFit = htmp.Clone()
  res = htmp.Clone()
  myfunc = ROOT.TF1("g","[0]*exp([1]*x+[2]*x*x)",0,1000)
  myfunc.SetParameters(100,-0.01, 0.0)
  htmp.Fit(myfunc,"","",lowerMETcut, upperMETcut)
  res = htmp.Clone()
  del htmp
  return [myfunc.GetParameter(1), resWOFit, myfunc]

import ROOT, array
from Workspace.RA4Analysis.simplePlotsCommon import *

#c = ROOT.TChain("pfRA4Analyzer/Events")
#c.Add("/scratch/schoef/pat_110815/Mu/WJetsToLNu/histo_*.root")
c = ROOT.TChain("RA4MCAnalyzer/Events")
#c.Add("/scratch/schoef/pat_110924/pythia6/TTJets-met50/histo_*.root")
c.Add("/scratch/schoef/pat_110924/pythia6/WJets-met50/histo_*.root")
cut = "jet2pt>40&&singleMuonic"
#ROOT.gPad.SetLogy()

allres = []
htvals = [[300,400],[400,500],[500,600],[600,700],[700,800],[800,900],[900,1000],[1000,1200],[1200,1400]]
binning=[]
for htval in htvals:
  binning.append(htval[0])
  allres.append(getExpParameter(c,htval,cut,100,1000))

binning.append(htvals[-1][1])
 
hp1 = ROOT.TH1F("p1","p1", 12,300,1500)
hp1.SetBins(len(binning) - 1, array('d',binning))
for nhval in range(len(htvals)):
  hp1.SetBinContent (hp1.FindBin(htvals[nhval][0]), allres[nhval][2].GetParameter(1))
  hp1.SetBinError   (hp1.FindBin(htvals[nhval][0]), allres[nhval][2].GetParError(1))

hp2 = ROOT.TH1F("p1","p1", 12,300,1500)
hp2.SetBins(len(binning) - 1, array('d',binning))
for nhval in range(len(htvals)):
  hp2.SetBinContent (hp2.FindBin(htvals[nhval][0]), allres[nhval][2].GetParameter(2))
  hp2.SetBinError   (hp2.FindBin(htvals[nhval][0]), allres[nhval][2].GetParError(2))

#c1 = ROOT.TCanvas()
#ROOT.gPad.SetLogy(0)
#hp1.Draw("")
##ROOT.c1.Print("hp1_ttbar.pdf")
#colors = [ROOT.kBlack, ROOT.kRed+1, ROOT.kBlue+1, ROOT.kMagenta+1, ROOT.kOrange+1,ROOT.kRed-1, ROOT.kBlue-1, ROOT.kMagenta-1, ROOT.kOrange-1 ]
#ROOT.gPad.SetLogy()
#allres[0][1].GetYaxis().SetRangeUser(0.5, 2*allres[0][1].GetMaximum())
#allres[0][1].Draw()
#for nr in range(0, len(allres[1:])):
#   allres[1:][nr][1].SetLineColor(colors[nr+1])
#   allres[1:][nr][1].Draw("same") 

for r in allres:
  r[1].Scale(1./r[1].Integral()) 

allres[0][1].GetYaxis().SetRangeUser(0.5, 2*allres[0][1].GetMaximum())
allres[0][1].Draw()
for nr in range(0, len(allres[1:-3])):
   allres[1:][nr][1].SetLineColor(colors[nr+1])
   allres[1:][nr][1].Draw("same")
