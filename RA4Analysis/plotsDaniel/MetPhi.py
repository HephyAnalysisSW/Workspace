import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import *# getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *

from math import sqrt, pi, cosh
from array import array

def getDeltaPhiMetGenMet(c):
  metPhi = c.GetLeaf('met_phi').GetValue()
  metGenPhi = c.GetLeaf('met_genPhi').GetValue()
  return deltaPhiNA(metPhi,metGenPhi)

lepSel = 'hard'

WJETS  = getChain(WJetsHTToLNu[lepSel],histname='')

streg = [[(250,350), 1.]]#, [(350, 450), 1.],  [(450, -1), 1.] ]
htreg = [(500,750),(750,1000),(1000,-1)]#,(750,1000),(1000,-1)]#,(1000,1250),(1250,-1)]#,(1250,-1)]
btreg = (0,0)
njreg = [(2,3),(4,4),(5,5),(6,7),(8,-1)]#,(7,7),(8,8),(9,9)]
nbjreg = [(0,0),(1,1),(2,2)]

presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&(sqrt((-met_genPt*cos(met_genPhi)+met_pt*cos(met_phi))**2+(-met_genPt*sin(met_genPhi)+met_pt*sin(met_phi))**2)/met_genPt)<1'
colors = [ROOT.kBlue+2, ROOT.kBlue-7, ROOT.kCyan-9, ROOT.kCyan-2, ROOT.kGreen-6, ROOT.kOrange-4, ROOT.kOrange+8, ROOT.kRed+1]
first = True

path = '/afs/hephy.at/user/d/dspitzbart/www/PHYS14v3/DPhiGenMetRecoMet/'

can = ROOT.TCanvas('c1','c1',800,600)
Whists = {}

for stb, dPhiCut in streg:
  Whists[stb] = {}
  for i_htb, htb in enumerate(htreg):
    Whists[stb][htb] = {}
    totalL = ROOT.TLegend(0.6,0.6,0.95,0.93)
    totalL.SetFillColor(ROOT.kWhite)
    totalL.SetShadowColor(ROOT.kWhite)
    totalL.SetBorderSize(1)
    for i_njb, njb in enumerate(njreg):
      print 'Processing njet',njb
      cname, cut = nameAndCut(stb,htb,njb, btb=btreg ,presel=presel)
      dPhiStr = 'deltaPhi_Wl'
      WJETS.Draw('>>eList',cut)
      elist = ROOT.gDirectory.Get("eList")
      number_events = elist.GetN()
      Whists[stb][htb][njb] = {'hist':ROOT.TH1F('h'+str(i_njb),str(njb),64,-3.2,3.2)}
      Whists[stb][htb][njb]['hist'].Sumw2()
      counter = 0.
      total = 0.
      for i in range(number_events):
        WJETS.GetEntry(elist.GetEntry(i))
        weight = getVarValue(WJETS,"weight")
        dPhiMet = getDeltaPhiMetGenMet(WJETS)
        deltaPhi = WJETS.GetLeaf(dPhiStr).GetValue()
        if deltaPhi<1.:
          Whists[stb][htb][njb]['hist'].Fill(dPhiMet, weight)
      Whists[stb][htb][njb]['hist'].SetLineColor(colors[i_njb])
      totalL.AddEntry(Whists[stb][htb][njb]['hist'])
      Whists[stb][htb][njb]['hist'].Draw('hist')
      can.Print(path+cname+'DPhiL1.png')
      can.Print(path+cname+'DPhiL1.root')
