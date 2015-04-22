import ROOT
from Workspace.RA4Analysis.makeCompPlotDilep import DrawClosure
#from Workspace.RA4Analysis.makeNicePlot import DrawNicePlot
from Workspace.RA4Analysis.cmgObjectSelection import get_cmg_jets, get_cmg_index_and_DR, get_cmg_genLeps, get_cmg_recoMuons, get_cmg_recoElectrons
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


ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

c = ROOT.TChain('tree')

c.Add('/data/dspitzbart/Phys14/T5qqqqWWDeg_mGo1000_mCh325_mChi300_1/treeProducerSusySingleLepton/tree.root')
#c.Add('/data/easilar/Phys14_V3/T5qqqqWW_mGo1000_mCh800_mChi700/treeProducerSusySingleLepton/tree.root')

plotName = 'IDEff_genLep_'

sample_name = "T5qqqqWW1000_325_300"
small = False
maxN = 10000
pdgId_Cut = 13
pt_Cut = (5, 100)
eta_Cut = 2.4
dz_Cut = 0.5
dxy_Cut = 0.2
relIso_Cut = 0.2
#presel = "Sum$(abs(GenPart_pdgId)==14&&abs(GenPart_motherId)==1000024)==2"#)==2&&Sum$(abs(GenPart_pdgId)==12&&abs(GenPart_motherId)==1000024)==0" #&&Sum$(abs(genPart_pdgId)==16)==0"
presel = "abs(genLep_pdgId)=="+str(pdgId_Cut)+"&&abs(genLep_motherId)==1000024"
path = '/afs/hephy.at/user/d/dspitzbart/www/softLepEff/'
if not os.path.exists(path):
  os.makedirs(path)

if pdgId_Cut == 13:
  filename = plotName+'mu'
if pdgId_Cut == 11:
  filename = plotName+'ele'


#ptBins = array('d', [float(x) for x in range(10, 50,10)+range(50,150,25)+range(150,200,50)+range(200,500,100)])
ptBins = (5,0,25)
etaBins = array('d', [float(x)/10. for x in [-30,-25]+range(-21,22,6)+[25,30]])

lep_Eff = ROOT.TH1F('lep_Eff', 'lep_Eff',*ptBins)
lep_Eff.Sumw2()
num = ROOT.TH1F('num', 'Lepton Efficiency',*ptBins)
num.Sumw2()
den = ROOT.TH1F('den', 'den',*ptBins)
den.Sumw2()
lep_Eff_mini = ROOT.TH1F('lep_Eff_mini', 'lep_Eff_mini',*ptBins)
lep_Eff_mini.Sumw2()
num_mini = ROOT.TH1F('num_mini', 'Lepton Efficiency',*ptBins)
num_mini.Sumw2()

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
  if pdgId_Cut == 13:
    recoLeps = get_cmg_recoMuons(c)
  if pdgId_Cut == 11:
    recoLeps = get_cmg_recoElectrons(c)
  #print "reco muons" , recoMuons
  #print "NEW LOOP"
  #print "ngenLeps:" , len(genLeps) , "nreco muons:" , len(recoMuons)
  for p in range(len(genLeps)):
    gLep = genLeps[p]
    if abs(gLep['pdgId']) == pdgId_Cut and gLep['pt'] > pt_Cut[0] and gLep['pt'] < pt_Cut[1]  and abs(gLep['eta'])< eta_Cut:
      #print "gLep:" , gLep
      gLepInd , gLepDR = get_cmg_index_and_DR(recoLeps,gLep['phi'],gLep['eta'])
      #print "index:" , gLepInd
      #den.Fill(ht)
      #print 'filling den'
      if gLepInd>=0 and gLepDR<0.4 :
        recolepton = recoLeps[gLepInd]
        #print "reco muon after matching: ", recomuon
        if pdgId_Cut == 13:
          if recolepton['pt'] > pt_Cut[0] and recolepton['pt'] < pt_Cut[1] and abs(recolepton['eta'])< eta_Cut:# and recolepton['mediumMuonId'] ==1 and recolepton['sip3d'] < 4.0:# and abs(recomuon['dxy'])< dxy_Cut and abs(recomuon['dz'])< dz_Cut and abs(1-recomuon['pt']/gLep['pt'])<0.07: #recomuon['looseId'] and
          #if recomuon['pt']> pt_Cut and abs(recomuon['eta'])< eta_Cut and abs(recomuon['dxy'])< dxy_Cut and abs(recomuon['dz'])< dz_Cut and abs(1-recomuon['pt']/gLep['pt'])<0.07:
            #print 'filling num'
            den.Fill(gLep['pt'])
            #print gLep['pt']
            #den.Fill(ht)
            if recolepton['mvaSusy']> 0.53:# and recolepton['miniRelIso']<0.2:
              num.Fill(gLep['pt'])
              #print gLep['pt']
              #num.Fill(ht)
              #continue
            if recolepton['mediumMuonId'] == 1 and recolepton['sip3d'] < 4.0 and recolepton['miniRelIso'] < 0.4:# and recolepton['miniRelIso']<0.2:
              #print "mini mini"
              num_mini.Fill(gLep['pt'])
              #num_mini.Fill(ht)
            #if recolepton['miniRelIso']<0.2 and gLep['pt']>15 :
            #  num_mini.Fill(gLep['pt'])
        if pdgId_Cut == 11:
          if recolepton['pt'] > pt_Cut[0] and recolepton['pt'] < pt_Cut[1] and abs(recolepton['eta'])< eta_Cut:# and recolepton['mvaSusy']>0.53:# and abs(recomuon['dxy'])< dxy_Cut and abs(recomuon['dz'])< 
            den.Fill(gLep['pt'])
            if recolepton['mvaSusy']> 0.53 :
              num.Fill(gLep['pt'])
            if recolepton['sip3d'] < 4.0 and recolepton['lostHits'] == 0 and recolepton['convVeto']:
              num_mini.Fill(gLep['pt'])
            #if recolepton['miniRelIso']<0.2 and gLep['pt']>15 :
            #  num_mini.Fill(gLep['pt'])
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
lep_Eff.GetYaxis().SetTitle("Efficiency")
#lep_Eff.GetXaxis().SetTitle("gen #mu P_{T}")
lep_Eff.GetXaxis().SetTitle("p_{T}")
lep_Eff.Draw('e1')
#DrawNicePlot(lep_Eff,'lep Eff','#mu Efficiency RelIso','p_{T}',path,'LepEff_cmg_vs_pT.png')
#DrawNicePlot(lep_Eff,'lep Eff1','#mu Efficiency RelIso','p_{T}',path,'LepEff_cmg_vs_pT.pdf')
#DrawNicePlot(lep_Eff,'lep Eff2','#mu Efficiency RelIso','p_{T}',path,'LepEff_cmg_vs_pT.root')
lep_Eff_mini = num_mini.Clone()
lep_Eff_mini.Divide(den)
lep_Eff_mini.SetMarkerColor(ROOT.kRed)
lep_Eff_mini.SetLineColor(ROOT.kRed)
lep_Eff_mini.Draw('e1 same')
lep_Eff_mini.SaveAs(sample_name+'_reject.root')
leg.AddEntry(lep_Eff, "MVA ID","l")
leg.AddEntry(lep_Eff_mini, "ID","l")
leg.Draw()
latex.DrawLatex(0.16,0.96,"CMS Simulation")
latex.DrawLatex(0.71,0.96,"L=4 fb^{-1} (13 TeV)")
latex.DrawLatex(0.55,0.8,sample_name)
#DrawNicePlot(lep_Eff_mini,'lep Eff','#mu Efficiency Mini Iso','p_{T}',path,'LepEff_mini_cmg_vs_pT.png')
#DrawNicePlot(lep_Eff_mini,'lep Eff1','#mu Efficiency Mini Iso','p_{T}',path,'LepEff_mini_cmg_vs_pT.pdf')
#DrawNicePlot(lep_Eff_mini,'lep Eff2','#mu Efficiency Mini Iso','p_{T}',path,'LepEff_mini_cmg_vs_pT.root')
#DrawNicePlot(EffMap,'lep Eff','Eff','ptvseta',path,'LepEff_cmg_2D.png')
#DrawNicePlot(EffMap,'lep Eff','Eff','ptvseta',path,'LepEff_cmg_2D.pdf')
#DrawNicePlot(EffMap,'lep Eff','Eff','ptvseta',path,'LepEff_cmg_2D.root')
#can.SaveAs(path+"/eff_comp_ht_0_1_TTJEts.png")
#can.SaveAs(path+"/eff_comp_ht_0_1_TTJEts.root")
#can.SaveAs(path+"/eff_comp_ht_0_1_TTJEts.pdf")

can.Print(path+filename+sample_name+'.png')

print "Written", path
