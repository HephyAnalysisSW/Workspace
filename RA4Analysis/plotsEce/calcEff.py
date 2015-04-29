import ROOT
from Workspace.RA4Analysis.makeCompPlotDilep import DrawClosure
from Workspace.RA4Analysis.makeNicePlot import DrawNicePlot
from Workspace.RA4Analysis.cmgObjectSelection import get_cmg_jets, get_cmg_index_and_DR, get_cmg_genLeps, get_cmg_recoMuons
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
ROOT.gROOT.LoadMacro("/afs/hephy.at/scratch/e/easilar/CMSSW_7_2_3/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.TH1F.SetDefaultSumw2()
#c = ROOT.TChain('Events')
c = ROOT.TChain('tree')
#c.Add('/data/schoef/cmgTuples/v5_Phys14V2_fromDPM_lateProcessingTauFix/TTJets/tree_Chunk49*.root')
###c.Add('/data/schoef/cmgTuples/v5_Phys14V2_fromDPM_lateProcessingTauFix/TTJets/*.root')
#c.Add('/data/easilar/tuples_from_batool/SMS_T1tttt_2J_mGl1200_mLSP800/treeProducerSusySingleLepton/tree.root')
#c.Add('/data/easilar/tuples_from_batool/TTJETS/TTJets/treeProducerSusySingleLepton/tree.root')
#c.Add('/data/easilar/tuples_from_batool/SMS_T1tttt_2J_mGl1500_mLSP100/treeProducerSusySingleLepton/tree.root')
#c.Add('/data/schoef/cmgTuples/postProcessed_v5_Phys14V2/hard/TTJets/*.root')
#c.Add('/data/schoef/cmgTuples/postProcessed_v5_Phys14V2//inc/hard/TTJets/*.root')
#from Workspace.HEPHYPythonTools.helpers import getChain
#c = getChain(hard_ttJetsCSA1450ns)
sample_name = "TTJETS"
small = False
maxN = 10000

pdgId_Cut = 13
pt_Cut = 25
eta_Cut = 2.4
dz_Cut = 0.5
dxy_Cut = 0.2
relIso_Cut = 0.4
presel = "Sum$(abs(genPart_pdgId)==14&&abs(genPart_motherId)==24)==2&&Sum$(abs(genPart_pdgId)==12&&abs(genPart_motherId)==24)==0" #&&Sum$(abs(genPart_pdgId)==16)==0"
path = '/afs/hephy.at/user/e/easilar/www/mini_Iso_study/lepton_Efficiency_Results/'
if not os.path.exists(path):
  os.makedirs(path)

#ptBins  = array('d', [float(x) for x in range(10, 50,10)+range(50,150,25)+range(150,200,50)+range(200,500,100)])
ptBins  = array('d', [float(x) for x in range(0,200,200)+range(200,2000,200)+range(2000,3000,500)])
etaBins = array('d', [float(x)/10. for x in [-30,-25]+range(-21,22,6)+[25,30]])

lep_Eff = ROOT.TH1F('lep_Eff', 'lep_Eff',len(ptBins)-1,ptBins)
num = ROOT.TH1F('num', 'Lepton Efficiency',len(ptBins)-1,ptBins)
den = ROOT.TH1F('den', 'den',len(ptBins)-1,ptBins)

lep_Eff_mini = ROOT.TH1F('lep_Eff_mini', 'lep_Eff_mini',len(ptBins)-1,ptBins)
num_mini = ROOT.TH1F('num_mini', 'Lepton Efficiency',len(ptBins)-1,ptBins)


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
  
  jets = get_cmg_jets(c)
  ht = sum([j['pt'] for j in jets]) 
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
         #den.Fill(ht)
         #print 'filling den'
         if gLepInd>=0 and  gLepDR<0.4 :
           recomuon = recoMuons[gLepInd]
           #print "reco muon after matching: ", recomuon
           if recomuon['pt']> pt_Cut and abs(recomuon['eta'])< eta_Cut and abs(recomuon['dxy'])< dxy_Cut and abs(recomuon['dz'])< dz_Cut and abs(1-recomuon['pt']/gLep['pt'])<0.07: #recomuon['looseId'] and  
           #print 'filling num'
             #den.Fill(gLep['pt'])
             den.Fill(ht)
             if recomuon['relIso03']>= relIso_Cut :
                #num.Fill(gLep['pt'])
                num.Fill(ht)
                 #continue
             if recomuon['miniRelIso']>= relIso_Cut : 
                #print "mini mini" 
                 #num_mini.Fill(gLep['pt'])
                num_mini.Fill(ht)
  del ht
can = ROOT.TCanvas("c","Eff",800,800)
can.cd()
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.035)
latex.SetTextAlign(11)
leg = ROOT.TLegend(0.55,0.85,0.95,0.95)
leg.SetFillColor(0)
lep_Eff = num.Clone()
lep_Eff.Divide(den)
lep_Eff.SetAxisRange(0, 1.4,"Y")
lep_Eff.SetLineColor(ROOT.kBlack)
lep_Eff.GetYaxis().SetTitle("#mu Iso Eff")
#lep_Eff.GetXaxis().SetTitle("gen #mu P_{T}")
lep_Eff.GetXaxis().SetTitle("H_{T}")
lep_Eff.Draw('C')
#DrawNicePlot(lep_Eff,'lep Eff','#mu Efficiency RelIso','p_{T}',path,'LepEff_cmg_vs_pT.png')
#DrawNicePlot(lep_Eff,'lep Eff1','#mu Efficiency RelIso','p_{T}',path,'LepEff_cmg_vs_pT.pdf')
#DrawNicePlot(lep_Eff,'lep Eff2','#mu Efficiency RelIso','p_{T}',path,'LepEff_cmg_vs_pT.root')

lep_Eff_mini = num_mini.Clone()
lep_Eff_mini.Divide(den)
lep_Eff_mini.SetMarkerColor(ROOT.kRed)
lep_Eff_mini.SetLineColor(ROOT.kRed)
lep_Eff_mini.Draw('C same')
lep_Eff_mini.SaveAs(sample_name+'_reject.root')
leg.AddEntry(lep_Eff, "Rel Iso < "+str(relIso_Cut),"l")
leg.AddEntry(lep_Eff_mini, "Mini Rel Iso <"+str(relIso_Cut),"l")
leg.Draw()
latex.DrawLatex(0.16,0.96,"CMS Simulation")
latex.DrawLatex(0.71,0.96,"L=4 fb^{-1} (13 TeV)")
latex.DrawLatex(0.71,0.8,sample_name)
#DrawNicePlot(lep_Eff_mini,'lep Eff','#mu Efficiency Mini Iso','p_{T}',path,'LepEff_mini_cmg_vs_pT.png')
#DrawNicePlot(lep_Eff_mini,'lep Eff1','#mu Efficiency Mini Iso','p_{T}',path,'LepEff_mini_cmg_vs_pT.pdf')
#DrawNicePlot(lep_Eff_mini,'lep Eff2','#mu Efficiency Mini Iso','p_{T}',path,'LepEff_mini_cmg_vs_pT.root')

#DrawNicePlot(EffMap,'lep Eff','Eff','ptvseta',path,'LepEff_cmg_2D.png')
#DrawNicePlot(EffMap,'lep Eff','Eff','ptvseta',path,'LepEff_cmg_2D.pdf')
#DrawNicePlot(EffMap,'lep Eff','Eff','ptvseta',path,'LepEff_cmg_2D.root')
#can.SaveAs(path+"/eff_comp_ht_0_1_TTJEts.png")
#can.SaveAs(path+"/eff_comp_ht_0_1_TTJEts.root")
#can.SaveAs(path+"/eff_comp_ht_0_1_TTJEts.pdf")

print "Written",  path
