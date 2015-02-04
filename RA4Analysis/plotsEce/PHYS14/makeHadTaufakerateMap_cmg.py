import ROOT
from Workspace.RA4Analysis.makeCompPlotDilep import DrawClosure
from Workspace.RA4Analysis.makeNicePlot import DrawNicePlot
from Workspace.RA4Analysis.objectSelection import getGoodJetsStage2,gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
from Workspace.RA4Analysis.cmgObjectSelection import getGood_cmg_JetsStage2, get_cmg_index_and_DR
from Workspace.HEPHYPythonTools.helpers import findClosestObject, deltaR, deltaR2,getVarValue, getObjFromFile
from Workspace.RA4Analysis.objectSelection import getGenLepsWithMatchInfo,getGenLeps, getMuons, getLooseMuStage2, getGenLep
from Workspace.RA4Analysis.stage2Tuples import *
from Workspace.RA4Analysis.helpers import deltaPhi
from math import *
import os, sys
import pickle
from array import array
from localInfo import username
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v3 import *
from Workspace.RA4Analysis.helpers import *
from Workspace.HEPHYPythonTools.helpers import getChain

#c = getChain(hard_ttJetsCSA1450ns)

c = ROOT.TChain('Events')
#c.Add('/data/schoef/cmgTuples/postProcessed_v5_Phys14V2/hard/TTJets/*.root')
c.Add('/data/schoef/cmgTuples/postProcessed_v5_Phys14V2//inc/hard/TTJets/*.root')

small = False
maxN = 10000

#c = ROOT.TChain('Events')
#c.Add('/data/schoef/convertedTuples_v26/copyInc/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*.root')

#presel = "ngoodMuons==1&&nvetoMuons==1&&nvetoElectrons==0"
presel = "singleMuonic"
#hadTau = "(gTauNENu+gTauNMuNu)==0&&gTauNTauNu==1"
#hadTauReq = 'genTau_nMuNu+genTau_nMuE==0&&genTau_nMuTau==1'
hadTauReq = 'genTau_nNuE+genTau_nNuMu==0&&genTau_nNuTau==1'
#oneHadTau     ="Sum$(gTauPt>15&&abs(gTauEta)<2.1&&gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"
oneHadTau     ="Sum$(genTau_pt>15&&abs(genTau_eta)<2.1&&"+hadTauReq+")==1"
path = '/afs/hephy.at/user/e/easilar/www/hadronicTau_PHYS14_inc/fakeRate_Results/'
if not os.path.exists(path):
  os.makedirs(path)

ptBins  = array('d', [float(x) for x in range(10, 20)+range(20,50,3)+range(50,100,10)+range(100,500,30)])

fRate = ROOT.TH1F('fRate', 'fRate',25,0,800)
fRate.Sumw2()
num = ROOT.TH1F('num', 'fake Rate',len(ptBins)-1,ptBins)
num.Sumw2()
den = ROOT.TH1F('den', 'den',len(ptBins)-1,ptBins)
den.Sumw2()

c.Draw(">>eList", presel+'&&'+hadTauReq)
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

  #jets = getGoodJetsStage2(c)
  jets = getGood_cmg_JetsStage2(c)
  ngTaus = c.GetLeaf('ngenTau').GetValue()
  for p in range(int(ngTaus)):
      gTauPdg = c.GetLeaf('genTau_pdgId').GetValue(p)
      gTauPt = c.GetLeaf('genTau_pt').GetValue(p)
      gTauEta = c.GetLeaf('genTau_eta').GetValue(p)
      gTauPhi = c.GetLeaf('genTau_phi').GetValue(p)
     # if len(jets)>0: 
      gTauJetInd , gTauJetDR = get_cmg_index_and_DR(jets,gTauPhi,gTauEta)
      #print 'index:' ,  gTauJetInd, 'dr' , gTauJetDR

      if abs(gTauPdg) == 15 and gTauPt>15 and abs(gTauEta)<2.1:
        den.Fill(gTauPt)
        if gTauJetInd>=0 and  gTauJetDR<0.4 :
          k = int(gTauJetInd)
          if jets[k]['btag']>0.732 and abs(jets[k]['eta'])<2.4:  # and jets[k]['pt']>30 and jets[k]['jetId']==1:
              num.Fill(gTauPt)

fRate = num.Clone()
fRate.Divide(den)
fRate.Draw()
fRate.SaveAs(path+'Tau_btag_FakeRate.root')
#fRate.SaveAs('/afs/hephy.at/user/e/easilar/www/hadronicTau_cmg/Tau_btag_FakeRate.pdf')
fname='CSA14_TTJet_tauToBfakeRate_cmg_Phys14_inc.pkl'
pickle.dump(fRate, file(path+fname,'w'))
print "Written",  path+fname

DrawNicePlot(fRate,'taufakeRate','Fake Rate(#tau#rightarrow bjet)','gen #tau p_{T}',path,'Loop_FakeRate_cmg_inc.png')
DrawNicePlot(fRate,'taufakeRate','Fake Rate(#tau#rightarrow bjet)','gen #tau p_{T}',path,'Loop_FakeRate_cmg_inc.pdf')
DrawNicePlot(fRate,'taufakeRate','Fake Rate(#tau#rightarrow bjet)','gen #tau p_{T}',path,'Loop_FakeRate_cmg_inc.root')
