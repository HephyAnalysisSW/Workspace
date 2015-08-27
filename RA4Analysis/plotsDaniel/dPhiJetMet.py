import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import *# getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import *#nameAndCut, nJetBinName, nBTagBinName, varBinName
from Workspace.RA4Analysis.cmgTuplesPostProcessed_Spring15_hard import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *

from math import sqrt, pi, cosh
from array import array

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

def getdPhiMetJet(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  met = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  JetPt = jets[0]['pt']
  JetPhi = jets[0]['phi']
  SubJetPt = jets[1]['pt']
  SubJetPhi = jets[1]['phi']
#  dPhi = acos((met*JetPt*cos(metPhi-JetPhi))/(met*JetPt))
  dPhi = cos(JetPhi-metPhi)
#  dPhi = max([abs(cos(JetPhi-metPhi)),abs(cos(SubJetPhi-metPhi))]
  return dPhi

def getMetPt(c):
  metPhi = c.GetLeaf('met_phi').GetValue()
  metPt = c.GetLeaf('met_pt').GetValue()
  metGenPhi = c.GetLeaf('met_genPhi').GetValue()
  metGenPt = c.GetLeaf('met_genPt').GetValue()
  dPhi = c.GetLeaf('deltaPhi_Wl').GetValue()
  x = -metGenPt*cos(metGenPhi)+metPt*cos(metPhi)
  y = -metGenPt*sin(metGenPhi)+metPt*sin(metPhi)
  fakeMet = sqrt(x*x + y*y)
  return metGenPt, fakeMet, dPhi, metPt, metPhi, metGenPhi

lepSel = 'hard'

WJETS  = getChain(WJetsHTToLNu[lepSel],histname='')

streg = [[(250,350), 1.], [(350, 450), 1.]]#,  [(450, -1), 1.] ]
htreg = [(1000,-1),(500,750),(750,1000)]#,(1250,-1)]#,(1250,-1)]
btreg = (0,0)
njreg = [(2,2),(3,3),(4,4),(5,5),(6,7),(8,-1)]#,(7,7),(8,8),(9,9)]
nbjreg = [(0,0),(1,1),(2,2)]

presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80'
#presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&(sqrt((-met_genPt*cos(met_genPhi)+met_pt*cos(met_phi))**2+(-met_genPt*sin(met_genPhi)+met_pt*sin(met_phi))**2)/met_genPt)<1'
colors = [ROOT.kBlue+2, ROOT.kBlue-7, ROOT.kCyan-9, ROOT.kCyan-2, ROOT.kGreen-6, ROOT.kOrange-4, ROOT.kOrange+8, ROOT.kRed+1]
first = True

can = ROOT.TCanvas('c1','c1',700,600)
can.SetLogy()
Whists = {}

for stb, dPhiCut in streg:
  Whists[stb] = {}
  for i_htb, htb in enumerate(htreg):
    Whists[stb][htb] = {}
    #totalL = ROOT.TLegend(0.2,0.6,0.5,0.93)
    #totalL.SetFillColor(ROOT.kWhite)
    #totalL.SetShadowColor(ROOT.kWhite)
    #totalL.SetBorderSize(1)
    for i_njb, njb in enumerate(njreg):
      totalL = ROOT.TLegend(0.5,0.79,0.95,0.93)
      totalL.SetFillColor(ROOT.kWhite)
      totalL.SetShadowColor(ROOT.kWhite)
      totalL.SetBorderSize(1)
      print 'Processing njet',njb
      first = True
      cname, cut = nameAndCut(stb,htb,njb, btb=btreg ,presel=presel)
      dPhiStr = 'deltaPhi_Wl'
      WJETS.Draw('>>eList',cut)
      elist = ROOT.gDirectory.Get("eList")
      number_events = elist.GetN()
      Whists[stb][htb][njb] = {'hist':ROOT.TH1F('h'+str(i_njb),"#slashed{E}_{T}^{fake} < 50 GeV && < #slashed{E}_{T}^{gen}",64,0,3.2), 'histFake':ROOT.TH1F('h'+str(i_njb),"#slasehd{E}_{T}^{fake} > 50 GeV || > #slashed{E}_{T}^{gen}",64,0,3.2), 'histFakeDP1':ROOT.TH1F('h'+str(i_njb),"#slashed{E}_{T}^{fake} > 50 GeV || > #slashed{E}_{T}^{gen}, #Delta#Phi(W,l) > 1",64,0,3.2), 'histDP1':ROOT.TH1F('h'+str(i_njb),"#slashed{E}_{T}^{fake} < 50 GeV && < #slashed{E}_{T}^{gen}, #Delta#Phi(W,l) > 1",64,0,3.2)}
      Whists[stb][htb][njb]['hist'].Sumw2()
      Whists[stb][htb][njb]['histFake'].Sumw2()
      Whists[stb][htb][njb]['histLowGen'].Sumw2()
      counter = 0.
      total = 0.
      for i in range(number_events):
        WJETS.GetEntry(elist.GetEntry(i))
        weight = getVarValue(WJETS,"weight")
        dPJM = cmgMinDPhiJet(WJETS, nJets=2)
        #dPJM = getdPhiMetJet(WJETS)
        metGenPt, fakeMet, dPhi, metPt, metPhi, metGenPhi = getMetPt(WJETS)
        if metGenPt>1.:# and dPhi>1.:
          if fakeMet>50. or fakeMet>metGenPt:
            Whists[stb][htb][njb]['histFake'].Fill(dPJM, weight)
            if dPhi>1.: Whists[stb][htb][njb]['histFakeDP1'].Fill(dPJM, weight)
          else:
            Whists[stb][htb][njb]['hist'].Fill(dPJM, weight)
            if dPhi>1.: Whists[stb][htb][njb]['histDP1'].Fill(dPJM, weight)
          #if metGenPt<100. and fakeMet>100:
          #  Whists[stb][htb][njb]['histLowGen'].Fill(dPJM, weight)
          
        #if WMass>100.:
        #  #print WMass, deltaPhi, weight
        #  if deltaPhi>1.:
        #    counter += weight
        #  total += weight
        ##if abs(neutrinoPt-genMetPt)<5:
        ##  h.Fill(deltaPhi, weight)
        #Whists[stb][htb][njb]['hist'].Fill(dPJM, weight)
      Whists[stb][htb][njb]['hist'].SetLineColor(colors[1])
      Whists[stb][htb][njb]['hist'].GetXaxis().SetTitle("#phi(met,jet)")
      Whists[stb][htb][njb]['hist'].GetYaxis().SetTitle("Events")
      Whists[stb][htb][njb]['hist'].SetMinimum(0.002)
      Whists[stb][htb][njb]['hist'].SetMaximum(10)
      Whists[stb][htb][njb]['hist'].SetLineWidth(2)
      Whists[stb][htb][njb]['hist'].SetMarkerStyle(0)
      Whists[stb][htb][njb]['histDP1'].SetLineWidth(2)
      Whists[stb][htb][njb]['histDP1'].SetMarkerStyle(0)
      Whists[stb][htb][njb]['histDP1'].SetLineColor(colors[1])
      Whists[stb][htb][njb]['histFake'].SetLineWidth(2) 
      Whists[stb][htb][njb]['histFake'].SetMarkerStyle(0)
      Whists[stb][htb][njb]['histFake'].SetLineColor(colors[-1])
      Whists[stb][htb][njb]['histFakeDP1'].SetLineWidth(2)
      Whists[stb][htb][njb]['histFakeDP1'].SetMarkerStyle(0)
      Whists[stb][htb][njb]['histFakeDP1'].SetLineColor(colors[-1])
      totalL.AddEntry(Whists[stb][htb][njb]['hist'])
      totalL.AddEntry(Whists[stb][htb][njb]['histFake'])
      #totalL.AddEntry(Whists[stb][htb][njb]['histLowGen'])
      #print 'Ratio of deltaPhi>1 in M(W)>100', counter/(total-counter)
      if first:
        Whists[stb][htb][njb]['hist'].Draw('hist')
        first = False
      else: Whists[stb][htb][njb]['hist'].Draw('hist same')
      Whists[stb][htb][njb]['histFake'].Draw('hist same')
      Whists[stb][htb][njb]['histFakeDP1'].Draw('hist same')
      Whists[stb][htb][njb]['histDP1'].Draw('hist same')
      #Whists[stb][htb][njb]['histLowGen'].Draw('hist same')
      totalL.Draw()
      can.Print('/afs/hephy.at/user/d/dspitzbart/www/Spring15/dPhiJetMetStudies/2jets/'+cname+'.png')
      can.Print('/afs/hephy.at/user/d/dspitzbart/www/Spring15/dPhiJetMetStudies/2jets/'+cname+'.root')
