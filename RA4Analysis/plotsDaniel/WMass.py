import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import *# getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *

from math import sqrt, pi, cosh
from array import array

def getWMass(c):
  para = ['pt','phi','eta','pdgId','motherId']
  genPartAll = [getObjDict(c, 'genPartAll_', para, j) for j in range(int(c.GetLeaf('ngenPartAll').GetValue()))]
  Neutrinos = []
  Leptons = []
  NeutrinosFromW = []
  LeptonsFromW = []
  for Neutrino in filterParticles(genPartAll, [12,14], 'pdgId'):
    Neutrinos.append(Neutrino)
  for NeutrinoFromW in filterParticles(Neutrinos, [24], 'motherId'):
    NeutrinosFromW.append(NeutrinoFromW)
  for Lepton in filterParticles(genPartAll, [11,13], 'pdgId'):
    Leptons.append(Lepton)
  for LeptonFromW in filterParticles(Leptons, [24], 'motherId'):
    LeptonsFromW.append(LeptonFromW)
  WMass = 0.
  if len(NeutrinosFromW)>0:
    if len(NeutrinosFromW)>1: print 'this should not have happened'
    if len(LeptonsFromW)>0:
      if len(LeptonsFromW)>1: print 'this should not have happened'
      LeptonPt = LeptonsFromW[0]['pt']
      LeptonPhi = LeptonsFromW[0]['phi']
      LeptonEta = LeptonsFromW[0]['eta']
      NeutrinoPt = NeutrinosFromW[0]['pt']
      NeutrinoPhi = NeutrinosFromW[0]['phi']
      NeutrinoEta = NeutrinosFromW[0]['eta']
      WMass = sqrt(2*LeptonPt*NeutrinoPt*(cosh(LeptonEta-NeutrinoEta)-cos(LeptonPhi-NeutrinoPhi)))
  if WMass < 1.:
    WMass = float('nan')
  return WMass

lepSel = 'hard'

WJETS  = getChain(WJetsHTToLNu[lepSel],histname='')

streg = [[(450,-1), 1.]]#, [(350, 450), 1.],  [(450, -1), 1.] ]
htreg = [(500,750)]#,(750,1000),(1000,-1)]#,(1000,1250),(1250,-1)]#,(1250,-1)]
btreg = (0,0)
njreg = [(2,2),(3,3),(4,4),(5,5),(6,7),(8,-1)]#,(7,7),(8,8),(9,9)]
nbjreg = [(0,0),(1,1),(2,2)]

presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&(sqrt((-met_genPt*cos(met_genPhi)+met_pt*cos(met_phi))**2+(-met_genPt*sin(met_genPhi)+met_pt*sin(met_phi))**2)/met_genPt)<1'
colors = [ROOT.kBlue+2, ROOT.kBlue-7, ROOT.kCyan-9, ROOT.kCyan-2, ROOT.kGreen-6, ROOT.kOrange-4, ROOT.kOrange+8, ROOT.kRed+1]
first = True

can = ROOT.TCanvas('c1','c1',800,600)
can.SetLogy()
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
      Whists[stb][htb][njb] = {'hist':ROOT.TH1F('h'+str(i_njb),str(njb),50,0,500)}
      Whists[stb][htb][njb]['hist'].Sumw2()
      counter = 0.
      total = 0.
      for i in range(number_events):
        WJETS.GetEntry(elist.GetEntry(i))
        weight = getVarValue(WJETS,"weight")
        deltaPhi = WJETS.GetLeaf(dPhiStr).GetValue()
        WMass = getWMass(WJETS)
        deltaPhi = WJETS.GetLeaf(dPhiStr).GetValue()
        if WMass>100.:
          #print WMass, deltaPhi, weight
          if deltaPhi>1.:
            counter += weight
          total += weight
        #if abs(neutrinoPt-genMetPt)<5:
        #  h.Fill(deltaPhi, weight)
        Whists[stb][htb][njb]['hist'].Fill(WMass, weight)
      Whists[stb][htb][njb]['hist'].SetLineColor(colors[i_njb])
      totalL.AddEntry(Whists[stb][htb][njb]['hist'])
      print 'Ratio of deltaPhi>1 in M(W)>100', counter/(total-counter)
      if first:
        Whists[stb][htb][njb]['hist'].Draw('hist')
        first = False
      else: Whists[stb][htb][njb]['hist'].Draw('hist same')
      
