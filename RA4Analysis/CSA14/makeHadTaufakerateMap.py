import ROOT
from Workspace.RA4Analysis.makeCompPlotDilep import DrawClosure
from Workspace.RA4Analysis.makeNicePlot import DrawNicePlot
from Workspace.RA4Analysis.objectSelection import getGoodJetsStage2,gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
from Workspace.HEPHYPythonTools.helpers import findClosestObject, deltaR,getVarValue, getObjFromFile
from Workspace.RA4Analysis.objectSelection import getGenLepsWithMatchInfo,getGenLeps, getMuons, getLooseMuStage2, getGenLep
from Workspace.RA4Analysis.stage2Tuples import *
from Workspace.RA4Analysis.helpers import deltaPhi
from math import *
import os, sys
import pickle
from array import array
from localInfo import username


small = False
maxN = 1000

c = ROOT.TChain('Events')
c.Add('/data/schoef/convertedTuples_v26/copyInc/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*.root')

presel = "ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0"
hadTau = "(gTauNENu+gTauNMuNu)==0&&gTauNTauNu==1"
oneHadTau     ="Sum$(gTauPt>15&&abs(gTauEta)<2.1&&gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"
path = '/afs/hephy.at/user/e/easilar/www/hadronicTau/'


ptBins  = array('d', [float(x) for x in range(10, 20)+range(20,50,3)+range(50,100,10)+range(100,310,30)])

fRate = ROOT.TH1F('fRate', 'fRate',25,0,800)
fRate.Sumw2()
num = ROOT.TH1F('num', 'fake Rate',len(ptBins)-1,ptBins)
num.Sumw2()
den = ROOT.TH1F('den', 'den',len(ptBins)-1,ptBins)
den.Sumw2()

c.Draw(">>eList", presel+'&&'+hadTau)
eList = ROOT.gDirectory.Get("eList")
number_events = eList.GetN()
if small:
  if number_events>maxN:
    number_events=maxN
number_events=min(number_events, eList.GetN())
countLeptons=0
for i in range(number_events):
  if (i%10000 == 0) and i>0 :
    print i,"/",number_events
  c.GetEntry(eList.GetEntry(i))

  jets = getGoodJetsStage2(c)
  ngTaus = c.GetLeaf('gTauCount').GetValue()
  for p in range(int(ngTaus)):
      gTauPdg = c.GetLeaf('gTauPdg').GetValue(p)
      gTauJetDR = c.GetLeaf('gTauJetDR').GetValue(p)
      gTauPt = c.GetLeaf('gTauPt').GetValue(p)
      gTauEta = c.GetLeaf('gTauEta').GetValue(p)
      gTauJetInd = c.GetLeaf('gTauJetInd').GetValue(p)
      gTauPhi = c.GetLeaf('gTauPhi').GetValue(p)
      if abs(gTauPdg) == 15 and gTauPt>15 and abs(gTauEta)<2.1:
        den.Fill(gTauPt)
        if gTauJetInd>=0 and  gTauJetDR<0.4 :
          k = int(gTauJetInd)
          if jets[k]['btag']>0.679 and abs(jets[k]['eta'])<2.4:
              num.Fill(gTauPt)


fRate = num.Clone()
fRate.Divide(den)
fRate.Draw()

DrawNicePlot(fRate,'tau fake Rate','fake Rate','gen Tau Pt',path,'Loop_FakeRate.png')
