import ROOT
import os, sys, copy
import pickle

#ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
#ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import *#getVarValue, getChain, deltaPhi, getYieldFromChain
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_softLepton import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.eventShape import *

presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&abs(genPartAll_pdgId)==24&&abs(genPartAll_motherId)<10"


def getDeltaPhiMetGenMet(c):
  metPhi = c.GetLeaf('met_phi').GetValue()
  metGenPhi = c.GetLeaf('met_genPhi').GetValue()
  return deltaPhiNA(metPhi,metGenPhi)

def getU(c):
  #jets = cmgGetJets(c, ptMin=0., etaMax=999.)
  metPhi = c.GetLeaf('met_phi').GetValue()
  metPt = c.GetLeaf('met_pt').GetValue()
  metGenPhi = c.GetLeaf('met_genPhi').GetValue()
  metGenPt = c.GetLeaf('met_genPt').GetValue()
  WPt = c.GetLeaf('genPartAll_pt').GetValue()
  WPhi = c.GetLeaf('genPartAll_phi').GetValue()
  x = WPt*cos(WPhi)-metGenPt*cos(metGenPhi)+metPt*cos(metPhi)
  y = WPt*sin(WPhi)-metGenPt*sin(metGenPhi)+metPt*sin(metPhi)
  #for jet in jets:
  #  x += jet['pt']*cos(jet['phi'])
  #  y += jet['pt']*sin(jet['phi'])
  Upara = x*cos(WPhi)+y*sin(WPhi)
  Uperp = x*sin(WPhi)-y*cos(WPhi)
  return Uperp, Upara

def projectFakeMetToW(c):
  metPhi = c.GetLeaf('met_phi').GetValue()
  metPt = c.GetLeaf('met_pt').GetValue()
  metGenPhi = c.GetLeaf('met_genPhi').GetValue()
  metGenPt = c.GetLeaf('met_genPt').GetValue()
  WPt = c.GetLeaf('genPartAll_pt').GetValue()
  WPhi = c.GetLeaf('genPartAll_phi').GetValue()
  return (metPt*cos(metPhi)-metGenPt*cos(metGenPhi))*cos(WPhi)+(metPt*sin(metPhi)-metGenPt*sin(metGenPhi))*sin(WPhi)

def projectFakeMetToGenMet(c):
  metPhi = c.GetLeaf('met_phi').GetValue()
  metPt = c.GetLeaf('met_pt').GetValue()
  metGenPhi = c.GetLeaf('met_genPhi').GetValue()
  metGenPt = c.GetLeaf('met_genPt').GetValue()
  return (metPt*cos(metPhi)-metGenPt*cos(metGenPhi))*cos(metGenPhi)+(metPt*sin(metPhi)-metGenPt*sin(metGenPhi))*sin(metGenPhi)

def getDeltaPhiJet(c):
  leadingNJets = cmgGetJets(c, ptMin=30., etaMax=999.)[:2]
  return deltaPhi(leadingNJets[0]['phi'],leadingNJets[1]['phi'])

varstring="deltaPhi_Wl"
plotDir='/afs/hephy.at/user/d/dspitzbart/www/WjetKin/'

if not os.path.exists(plotDir):
  os.makedirs(plotDir)


lepSel='hard'
WJETS = getChain(WJetsHTToLNu[lepSel],histname='')

stReg=[(250,350),(350,450),(450,-1)]#,(350,450),(450,-1)]
htReg=[(500,750),(750,1000),(1000,-1)]#,(750,1000),(1000,-1)]#,(1250,-1)]#,(1250,-1)]
jetReg = [(2,3),(4,4),(5,5),(6,7),(8,-1)]#,(8,-1)]#,(6,-1)]#,(8,-1)]#,(6,-1),(8,-1)]
btb = (0,0)

can1 = ROOT.TCanvas('c1','c1',800,600)
#hist = ROOT.TH1F('hist','hist',len(jetReg),0,len(jetReg))
#hist.Sumw2()

## project onto genMet
#for st in stReg:
#  print
#  print 'Processing ST bin',st
#  for ht in htReg:
#    print 'Processing HT bin',ht
#    for i_jet, jet in enumerate(jetReg):
#      metHist = ROOT.TH1F('metHist','metHist',100,-500,500)
#      print 'Processing njet',jet
#      cutname, cut = nameAndCut(st, ht, jet, btb=btb, presel=presel, btagVar = 'nBJetMediumCSV30')
#      RMSself = 0.
#      totalWeight = 0.
#      WJETS.Draw('>>eList','weight*('+cut+')')
#      elist = ROOT.gDirectory.Get("eList")
#      number_events = elist.GetN()
#      for i in range(number_events):
#        WJETS.GetEntry(elist.GetEntry(i))
#        weight=getVarValue(WJETS,"weight")
#        fakeMetOnW = projectFakeMetToGenMet(WJETS)
#        metHist.Fill(fakeMetOnW,weight)
#      metHist.Draw()
#      can1.Print('/afs/hephy.at/user/d/dspitzbart/www/WjetKin/fakeMetOnGenMet'+cutname+'.png')
#      del metHist

## project onto W direction
#for st in stReg:
#  print
#  print 'Processing ST bin',st
#  for ht in htReg:
#    hist = ROOT.TH1F('hist','hist',len(jetReg),0,len(jetReg))
#    hist.Sumw2()
#    print 'Processing HT bin',ht
#    for i_jet, jet in enumerate(jetReg):
#      dPhiHist = ROOT.TH1F('dPhiHist','dPhiHist',64,-3.2,3.2)
#      dPhiHist.Sumw2()
#      print 'Processing njet',jet
#      cutname, cut = nameAndCut(st, ht, jet, btb=btb, presel=presel, btagVar = 'nBJetMediumCSV30')
#      RMSself = 0.
#      totalWeight = 0.
#      WJETS.Draw('>>eList','weight*('+cut+')')
#      elist = ROOT.gDirectory.Get("eList")
#      number_events = elist.GetN()
#      for i in range(number_events):
#        WJETS.GetEntry(elist.GetEntry(i))
#        weight=getVarValue(WJETS,"weight")
#        varvalue = getDeltaPhiMetGenMet(WJETS)
#        dPhiHist.Fill(varvalue,weight)
#        #RMSself += varvalue**2*weight
#        totalWeight += weight
#      dPhiHist.Draw()
#      RMS = dPhiHist.GetRMS()
#      #print RMS
#      dPhiHist.Fit('gaus','','same')
#      FitFunc = dPhiHist.GetFunction('gaus')
#      FitFunc.Draw('same')
#      can1.Print('/afs/hephy.at/user/d/dspitzbart/www/WjetKin/metDPhi'+cutname+'.png')
#      #RMSself = sqrt(RMSself/totalWeight)
#      #print RMSself
#      hist.SetBinContent(i_jet+1,RMS)
#      hist.SetBinError(i_jet+1,dPhiHist.GetRMSError())
#      hist.GetXaxis().SetBinLabel(i_jet+1, nJetBinName(jet))
#      del dPhiHist
#    hist.GetXaxis().SetTitle('jet multiplicity')
#    hist.GetYaxis().SetTitle('RMS')
#    hist.SetMaximum(1.5)
#    hist.SetMinimum(0.)
#    hist.SetMarkerSize(0)
#    hist.SetLineColor(ROOT.kAzure)
#    hist.SetLineWidth(2)
#    hist.Fit('pol1','','same')
#    FitFunc     = hist.GetFunction('pol1')
#    FitParD     = FitFunc.GetParameter(0)
#    FitParDError = FitFunc.GetParError(0)
#    FitParK = FitFunc.GetParameter(1)
#    FitParKError = FitFunc.GetParError(1)
#    FitFunc.SetLineColor(ROOT.kOrange+10)
#    FitFunc.SetLineStyle(2)
#    FitFunc.SetLineWidth(2)
#    
#    hist.Draw('e hist')
#    FitFunc.Draw('same')
#    can1.Print('/afs/hephy.at/user/d/dspitzbart/www/WjetKin/metRMS'+cutname+'.png')
#    del hist

# upara
for st in stReg:
  print
  print 'Processing ST bin',st
  for ht in htReg:
    hist = ROOT.TH1F('hist','hist',len(jetReg),0,len(jetReg))
    hist.Sumw2()
    print 'Processing HT bin',ht
    for i_jet, jet in enumerate(jetReg):
      UparaHist = ROOT.TH1F('UparaHist','UparaHist',100,-500,500)
      UparaHist.Sumw2()
      print 'Processing njet',jet
      cutname, cut = nameAndCut(st, ht, jet, btb=btb, presel=presel, btagVar = 'nBJetMediumCSV30')
      WJETS.Draw('>>eList','weight*('+cut+')')
      elist = ROOT.gDirectory.Get("eList")
      number_events = elist.GetN()
      for i in range(number_events):
        WJETS.GetEntry(elist.GetEntry(i))
        weight=getVarValue(WJETS,"weight")
        Upara, Uperp = getU(WJETS)
        UparaHist.Fill(Uperp,weight)
      UparaHist.Draw('e hist')
      RMS = UparaHist.GetRMS()
      Mean = UparaHist.GetMean()
      UparaHist.Fit('gaus','','same')
      FitFunc = UparaHist.GetFunction('gaus')
      FitFunc.Draw('same')
      can1.Print('/afs/hephy.at/user/d/dspitzbart/www/WjetKin/Uperp_'+cutname+'.png')
      hist.SetBinContent(i_jet+1,RMS)
      hist.SetBinError(i_jet+1,UparaHist.GetRMSError())
      hist.GetXaxis().SetBinLabel(i_jet+1, nJetBinName(jet))
      del UparaHist
    hist.GetXaxis().SetTitle('jet multiplicity')
    hist.GetYaxis().SetTitle('UperpRMS')
    hist.SetMaximum(80)
    hist.SetMinimum(0.)
    hist.SetMarkerSize(0)
    hist.SetLineColor(ROOT.kAzure)
    hist.SetLineWidth(2)
    hist.Fit('pol1','','same')
    FitFunc     = hist.GetFunction('pol1')
    FitParD     = FitFunc.GetParameter(0)
    FitParDError = FitFunc.GetParError(0)
    FitParK = FitFunc.GetParameter(1)
    FitParKError = FitFunc.GetParError(1)
    FitFunc.SetLineColor(ROOT.kOrange+10)
    FitFunc.SetLineStyle(2)
    FitFunc.SetLineWidth(2)
    
    hist.Draw('e hist')
    FitFunc.Draw('same')
    can1.Print('/afs/hephy.at/user/d/dspitzbart/www/WjetKin/UperpRMS_'+cutname+'.png')
    del hist



