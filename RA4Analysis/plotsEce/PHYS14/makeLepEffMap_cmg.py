import ROOT
from Workspace.RA4Analysis.makeCompPlotDilep import DrawClosure
from Workspace.RA4Analysis.makeNicePlot import DrawNicePlot
from Workspace.RA4Analysis.cmgObjectSelection import getGood_cmg_JetsStage2, get_cmg_index_and_DR, get_cmg_genLeps, get_cmg_recoMuons
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
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v3 import *

ROOT.TH1F.SetDefaultSumw2()
c = ROOT.TChain('Events')
#c.Add('/data/schoef/cmgTuples/postProcessed_v5_Phys14V2/hard/TTJets/*.root')
c.Add('/data/schoef/cmgTuples/postProcessed_v5_Phys14V2//inc/hard/TTJets/*.root')
#from Workspace.HEPHYPythonTools.helpers import getChain
#c = getChain(hard_ttJetsCSA1450ns)

small = False
maxN = 10000

pdgId_Cut = 13
pt_Cut = 15
eta_Cut = 2.5
dz_Cut = 0.5
dxy_Cut = 0.2
relIso_Cut = 0.3
presel = "Sum$(abs(genPart_pdgId)==14&&abs(genPart_motherId)==24)==2&&Sum$(abs(genPart_pdgId)==12)==0" #&&Sum$(abs(genPart_pdgId)==16)==0"
path = '/afs/hephy.at/user/e/easilar/www/hadronicTau_PHYS14_inc/lepton_Efficiency_Results/'
if not os.path.exists(path):
  os.makedirs(path)

ptBins  = array('d', [float(x) for x in range(10, 20)+range(20,50,3)+range(50,100,10)+range(100,500,30)])
etaBins = array('d', [float(x)/10. for x in [-30,-25]+range(-21,22,6)+[25,30]])

lep_Eff = ROOT.TH1F('lep_Eff', 'lep_Eff',len(ptBins)-1,ptBins)
num = ROOT.TH1F('num', 'Lepton Efficiency',len(ptBins)-1,ptBins)
den = ROOT.TH1F('den', 'den',len(ptBins)-1,ptBins)

lep_Eff_eta = ROOT.TH1F('lep_Eff_eta', 'lep_Eff_eta',len(etaBins)-1,etaBins)
num_eta = ROOT.TH1F('num_eta', 'fake Rate',len(etaBins)-1,etaBins)
den_eta = ROOT.TH1F('den_eta', 'den_eta',len(etaBins)-1,etaBins)

PtEtaDen = ROOT.TH2F('PtEtaDen','PtEtaDen',len(ptBins)-1,ptBins,len(etaBins)-1,etaBins)
PtEtaNum = ROOT.TH2F('PtEtaNum','PtEtaNum',len(ptBins)-1,ptBins,len(etaBins)-1,etaBins)
EffMap = ROOT.TH2F('EffMap','EffMap',len(ptBins)-1,ptBins,len(etaBins)-1,etaBins) 

c.Draw(">>eList",presel)
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

  #jets = getGood_cmg_JetsStage2(c)
  genLeps = get_cmg_genLeps(c)
  recoMuons = get_cmg_recoMuons(c)   
  #print "reco muons" , recoMuons
  #print "NEW LOOP"
  #print "ngenLeps:" , len(genLeps) , "nreco muons:" , len(recoMuons)
  for p in range(len(genLeps)):
       gLep = genLeps[p]
       if abs(gLep['pdgId']) == pdgId_Cut and gLep['pt']> pt_Cut and abs(gLep['eta'])<  eta_Cut:
         #print "gLep:" , gLep
         gLepInd , gLepDR = get_cmg_index_and_DR(recoMuons,gLep['phi'],gLep['eta'])
         #print "index:" , gLepInd
         den.Fill(gLep['pt'])
         den_eta.Fill(gLep['eta'])
         PtEtaDen.Fill(gLep['pt'],gLep['eta'])
         #print 'filling den'
         if gLepInd>=0 and  gLepDR<0.4 :
           recomuon = recoMuons[gLepInd]
           #print "reco muon after matching: ", recomuon
           if recomuon['pt']> pt_Cut and abs(recomuon['eta'])< eta_Cut and recomuon['relIso03']< relIso_Cut and abs(recomuon['dxy'])< dxy_Cut and abs(recomuon['dz'])< dz_Cut and abs(1-recomuon['pt']/gLep['pt'])<0.07: #recomuon['looseId'] and  
           #print 'filling num'
             num.Fill(gLep['pt'])
             num_eta.Fill(gLep['eta'])
             PtEtaNum.Fill(gLep['pt'],gLep['eta'])
             continue

lep_Eff = num.Clone()
lep_Eff.Divide(den)
lep_Eff.Draw()
DrawNicePlot(lep_Eff,'lep Eff','#mu Efficiency','p_{T}',path,'LepEff_cmg_vs_pT.png')
DrawNicePlot(lep_Eff,'lep Eff1','#mu Efficiency','p_{T}',path,'LepEff_cmg_vs_pT.pdf')
DrawNicePlot(lep_Eff,'lep Eff2','#mu Efficiency','p_{T}',path,'LepEff_cmg_vs_pT.root')


lep_Eff_eta = num_eta.Clone()
lep_Eff_eta.Divide(den_eta)
lep_Eff_eta.Draw()
DrawNicePlot(lep_Eff_eta,'lepEffeta','#mu Efficiency','#eta',path,'LepEff_cmg_vs_eta.png')
DrawNicePlot(lep_Eff_eta,'lepEffeta1','#mu Efficiency','#eta',path,'LepEff_cmg_vs_eta.pdf')
DrawNicePlot(lep_Eff_eta,'lepEffeta2','#mu Efficiency','#eta',path,'LepEff_cmg_vs_eta.root')


EffMap = PtEtaNum.Clone()
EffMap.Divide(PtEtaDen)
EffMap.Draw()
EffMap.SaveAs(path+'LepEff_cmg_2D.root')
#DrawNicePlot(EffMap,'lep Eff','Eff','ptvseta',path,'LepEff_cmg_2D.png')
#DrawNicePlot(EffMap,'lep Eff','Eff','ptvseta',path,'LepEff_cmg_2D.pdf')
#DrawNicePlot(EffMap,'lep Eff','Eff','ptvseta',path,'LepEff_cmg_2D.root')

fname='CSA14_TTJet_LepEff_cmg_Large.pkl'
pickle.dump(EffMap, file(path+fname,'w'))
print "Written",  path+fname
