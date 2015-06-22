import ROOT
import pickle
from math import pi
from Workspace.RA4Analysis.stage2Tuples import ttJetsCSA1450nsInc, T5Full_1200_1000_800, T5Full_1500_800_100, ttJetsCSA1450ns
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v3 import *
#from Workspace.HEPHYPythonTools.helpers import getPlotFromChain
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain

from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *

ROOT_colors = [ROOT.kBlack, ROOT.kRed-7, ROOT.kBlue-2, ROOT.kGreen+3, ROOT.kOrange+1,ROOT.kRed-3, ROOT.kAzure+6, ROOT.kCyan+3, ROOT.kOrange , ROOT.kRed-10]
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()

lepSel = 'hard'
path = '/afs/hephy.at/user/e/easilar/www/Phys14v3/toConvener/dilep_split/'
if not os.path.exists(path):
  os.makedirs(path)



c = getChain(ttJets[lepSel],histname='')
s1200 = getChain(SMS_T5qqqqWW_Gl1200_Chi1000_LSP800[lepSel],histname='')
s1500 =  getChain(SMS_T5qqqqWW_Gl1500_Chi800_LSP100[lepSel],histname='')
#c = getChain(WJetsHTToLNu[lepSel],histname='')

#c = ROOT.TChain('tree')
#c.Add('/data/schoef/cmgTuples/v5_Phys14V2_fromDPM_lateProcessingTauFix/TTJets/tree_Chunk49*.root')
#c.Add('/data/schoef/cmgTuples/v5_Phys14V2_fromDPM_lateProcessingTauFix/TTJets/tree_Chunk12*.root')
#c = getChain(hard_ttJetsCSA1450ns)
#c.Add('/data/schoef/cmgTuples/postProcessed_v5_Phys14V2//inc/hard/TTJets/*.root')
#file = ROOT.TFile('/afs/cern.ch/work/e/easilar/small_TTJET/TTJets/treeProducerSusySingleLepton/tree.root')
#c = file.Get('tree')
#c.Add('/afs/cern.ch/work/e/easilar/small_TTJET/TTJets/treeProducerSusySingleLepton/tree.root')
#ttJetsample = ttJetsCSA1450nsInc
#for b in ttJetsample['bins']:
#  c.Add(ttJetsample['dirname']+'/'+b+'/h*0To10.root')
#  c.Add(ttJetsample['dirname']+'/'+b+'/h*.root')
#c.Add('/data/schoef/cmgTuples/postProcessed_v5_Phys14V2//inc/hard/TTJets/*.root')

#T5Full_1200_1000_800['color'] = ROOT.kBlue
#T5Full_1500_800_100['color'] = ROOT.kRed

#signals = [T5Full_1200_1000_800,T5Full_1500_800_100]
#for sig in signals:
#  sig['c'] = ROOT.TChain('Events')
#  for b in sig['bins']:
#    sig['c'].Add(sig['dirname']+'/'+b+'/h*.root')
ngNuEFromW = "Sum$(abs(genPart_pdgId)==12&&abs(genPart_motherId)==24)"
ngNuMuFromW = "Sum$(abs(genPart_pdgId)==14&&abs(genPart_motherId)==24)"
ngNuTauFromW = "Sum$(abs(genPart_pdgId)==16&&abs(genPart_motherId)==24)"
#nBtagCMVA = "Sum$(Jet_id&&Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_btagCMVA>0.732)"
#nBtagCMVA = "Sum$(Jet_id&&Jet_pt>40&&abs(Jet_eta)<2.4&&Jet_btagCMVA>0.732)"
#ngoodMuons = 'Sum$(abs(LepGood_pdgId)==13)'
#ngoodElectrons = 'Sum$(abs(LepGood_pdgId)==11)'
tot_lumi = 4000
nevents = c.GetEntries()
weight = "("+str(tot_lumi)+"*xsec)/"+str(nevents)
print weight
#weight = '0.1'
#lTau_H  = "ngNuEFromW+ngNuMuFromW==0&&ngNuTauFromW==1"
#lTau_H  = "ngNuEFromW+ngNuMuFromW==0&&ngNuTauFromW==1&&Sum$(gTauNENu+gTauNMuNu==1&&gTauNTauNu==1)==1"
lTau_H  = ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==1"\
          +"&&Sum$(genTau_nNuE+genTau_nNuMu==1&&genTau_nNuTau==1)==1"
#hTau_l  = "ngNuEFromW+ngNuMuFromW==1&&ngNuTauFromW==1&&Sum$(gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"
hTau_l=     "Sum$((abs(genPart_pdgId)==14||abs(genPart_pdgId)==12)&&abs(genPart_motherId)==24)==1"\
            +"&&Sum$(abs(genPart_pdgId)==16&&abs(genPart_motherId)==24)==1"\
            +"&&Sum$(genTau_nNuE+genTau_nNuMu==0&&genTau_nNuTau==1)==1"
#diLep   = "ngNuEFromW+ngNuMuFromW==2&&ngNuTauFromW==0"
#diLepEff   = "ngNuEFromW+ngNuMuFromW==2&&ngNuTauFromW==0&&Sum$(gLepPt>10&&(abs(gLepEta)<2.1&&abs(gLepPdg)==13||abs(gLepEta)<2.4&&abs(gLepPdg)==11))==2"
diLepEff   = ngNuEFromW+"+"+ngNuMuFromW+"==2&&"+ngNuTauFromW+"==0&&Sum$(genLep_pt>10&&(abs(genLep_eta)<2.1&&abs(genLep_pdgId)==13||abs(genLep_eta)<2.4&&abs(genLep_pdgId)==11))==2"
#diLepAcc   = "ngNuEFromW+ngNuMuFromW==2&&ngNuTauFromW==0&&Sum$(gLepPt>10&&(abs(gLepEta)<2.1&&abs(gLepPdg)==13||abs(gLepEta)<2.4&&abs(gLepPdg)==11))!=2"
diLepAcc   = ngNuEFromW+"+"+ngNuMuFromW+"==2&&"+ngNuTauFromW+"==0&&Sum$(genLep_pt>10&&(abs(genLep_eta)<2.1&&abs(genLep_pdgId)==13||abs(genLep_eta)<2.4&&abs(genLep_pdgId)==11))!=2"

#lTau_l  = "ngNuEFromW+ngNuMuFromW==1&&ngNuTauFromW==1&&Sum$(gTauNENu+gTauNMuNu==1&&gTauNTauNu==1)==1"
lTau_l  = ngNuEFromW+"+"+ngNuMuFromW+"==1&&"+ngNuTauFromW+"==1&&Sum$(genTau_nNuE+genTau_nNuMu==1&&genTau_nNuTau==1)==1"
#diTau   = "ngNuEFromW+ngNuMuFromW==0&&ngNuTauFromW==2"
diTau   = ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==2"
#l_H     = "ngNuEFromW+ngNuMuFromW==1&&ngNuTauFromW==0"
l_H     =  ngNuEFromW+"+"+ngNuMuFromW+"==1&&"+ngNuTauFromW+"==0"

#diHad   = "ngNuEFromW+ngNuMuFromW==0&&ngNuTauFromW==0"
diHad   = ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==0"
#hTau_H  = "ngNuEFromW+ngNuMuFromW==0&&ngNuTauFromW==1&&Sum$(gTauNENu+gTauNMuNu==0&&gTauNTauNu==1)==1"
hTau_H  = ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==1&&Sum$(genTau_nNuE+genTau_nNuMu==0&&genTau_nNuTau==1)==1"
#hTau_H  = "ngNuEFromW+ngNuMuFromW==0&&ngNuTauFromW==1"
allHad = "("+diHad+"||"+hTau_H+")"
#prefix='EffAcc_nHybridMediumSel_met250'
#presel="ngoodMuons==1&&ngoodElectrons==0&&nvetoElectrons==0&&ht>500&&met>250&&nbtags==0&&njets>=4"
#presel="ngoodMuons==1&&ngoodElectrons==0&&nvetoElectrons==0&&ht>500&&met+leptonPt>250&&nbtags==0&&njets>=4"
#presel= "singleMuonic&&htJet25>500&&Jet_pt>30&&Jet_pt[1]>80&&st>250&&"+nBtagCMVA+"==0&&nJet>=6"
#singleMuonic = "nLepOther==0&&Sum$(abs(LepGood_pdgId)==13&&LepGood_relIso03<0.12&&LepGood_tightId==1)==1&&Sum$(abs(LepGood_pdgId)==11)==0" #&&nLepGood==1&&nLepOther==0"
#presel= singleMuonic+"&&"+nBtagCMVA+"==0" #"&&(met_pt+LepGood_pt)>=250&&htJet40>=400&&nJet>=4"
#singleMuonic = "(nLepOther==0&&Sum$(abs(LepGood_pdgId)==13&&LepGood_relIso03<0.12&&LepGood_tightId==1)==1&&Sum$(abs(LepGood_pdgId)==11)==0&&nLepGood==1)"
#presel = "(htJet40>=0&&(met_pt+LepGood_pt)>=0&&"+nBtagCMVA+">=0"+"&&nJet>=0)&&"+singleMuonic
#presel = "htJet40>=400&&(met_pt+LepGood_pt)>=150&&"+nBtagCMVA+"==0"+"&&nJet>=6"
#presel = singleMuonic+"&&nJet>=1"
prepresel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&"
stCutList = [(150,250),(250,350),(350,450),(450,10000000)]
htCutList = [(400,500),(500,750),(750,1000),(1000,1250),(1250,10000000)]
#for htCut in htCutList[0]:
#for stCut in stCutList:
presel = prepresel+"htJet30j>=500&&st>=250&&nJet30>=2&&nBJetMediumCMVA30==0" 
prefix= ''.join(presel.split('&&')[5:]).replace("&&","_").replace(">=","le_").replace("==","eq_") #.replace("&&","_").replace(">=","le_").replace("==","eq_")
#prefix = "trial"
plots = [ 
         # ['sqrt(2*leptonPt*met*(1-cos(metPhi-leptonPhi)))', [20,0,800], 'mt'],\
    ##    ['sqrt(2*LepGood_pt*met_pt*(1-cos(met_phi-LepGood_phi)))',[20,0,800],'mt'],\
         # ['acos((leptonPt + met*cos(leptonPhi - metPhi))/sqrt(leptonPt**2 + met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))', [16,0,3.2], 'dphi']
          #['acos((LepGood_pt+met_pt*cos(LepGood_phi-met_phi))/sqrt(LepGood_pt**2+met_pt**2+2*met_pt*LepGood_pt*cos(LepGood_phi-met_phi)))', [16,0,3.2], 'dphi'],\
          ['deltaPhi_Wl', [16,0,3.2], '#Delta#Phi'],\
          #['st', [30,0,1000], '#S_{T}'],\
    ##      ['htJet40',[20,0,1000],'ht'],\
    ##      ['met_pt+LepGood_pt',[20,0,1000],'st'],\
    ##      ['nJet',[16,0,16],'n_jets']
 ]

for var, binning, fname in plots:
  c1 = ROOT.TCanvas()
  hs1200 = getPlotFromChain(s1200, var, binning, presel, weight)
  hs1500 = getPlotFromChain(s1500, var, binning, presel, weight)
  hs1200.SetLineColor(ROOT.kRed)
  hs1200.SetLineWidth(3)
  hs1500.SetLineColor(ROOT.kYellow)
  hs1500.SetLineWidth(3)
  hPresel = getPlotFromChain(c, var, binning, presel, weight)
  hPresel.SetLineColor(ROOT.kBlack)
  hPresel.SetTitle("")
  #hPresel.GetYaxis().SetRangeUser(0.001, 1.5*hPresel.GetMaximum())
  hPresel.GetYaxis().SetRangeUser(0.001, 100000000)
  hPresel.Draw()

 # for sig in signals:
 #   sig['hPresel'] = getPlotFromChain(sig['c'], var, binning, presel, 'weight')
 #   sig['hPresel'].SetLineColor(sig['color'])
 #   sig['hPresel'].SetLineWidth(2)
 #   sig['hPresel'].SetTitle("")
 
  #hPresel_sum = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], 
  #                presel+"&&("+"||".join([l_H, lTau_H, hTau_l, diLep, lTau_l, diTau, allHad])+")", 'weight')
  #hPresel_sum.SetLineColor(ROOT.kMagenta)
  #hPresel_sum.Draw('same')

  l = ROOT.TLegend(0.5,0.6,0.95,0.95)
  l.SetFillColor(ROOT.kWhite)
  l.SetShadowColor(ROOT.kWhite)
  l.SetBorderSize(1)

  histos=[]
  l.AddEntry(hPresel, 'Total','l')
  previous = None
  for i, [cut,name,col] in enumerate([\
        [allHad, 'all hadronic', ROOT.kRed-7],
        [lTau_H,'W#rightarrow#tau#nu#rightarrow e/#mu+3#nu | W#rightarrow had.', ROOT.kBlue-2], 
        [diTau,'two #tau leptons', ROOT.kGreen+3], 
        [lTau_l,'W#rightarrow#tau#nu#rightarrow e/#mu+3#nu | W#rightarrow e/#mu+#nu', ROOT.kOrange+1], 
  #      [diLep,'dileptonic (e/#mu)'], 
        [diLepAcc,'dileptonic (e/#mu) Acc.',ROOT.kRed-3], 
        [diLepEff,'dileptonic (e/#mu) Eff.',ROOT.kRed-4], 
        [hTau_l,'W#rightarrow#tau#nu#rightarrow had.+2#nu | W#rightarrow e/#mu+#nu', ROOT.kAzure+6], 
        [l_H, 'single lep. (e/#mu)',ROOT.kCyan+3],  
      ]):
    print (c, var, binning, presel+"&&"+cut, weight)
    hPresel_cut = getPlotFromChain(c, var, binning, presel+"&&"+cut, weight)
    #hPresel_cut = ROOT.TH1F('hPresel_cut','hPresel_cut',16,0,pi) 
    #c.Draw('deltaPhi_Wl>>hPresel_cut','weight*('+cut+'&&'+presel+')') 
    if previous:  
      hPresel_cut.Add(previous)

    previous=hPresel_cut.Clone()
    hPresel_cut.SetLineColor(ROOT.kBlack)
    hPresel_cut.SetLineStyle(0)
    hPresel_cut.SetLineWidth(0)
    hPresel_cut.SetFillColor(col)
    hPresel_cut.SetMarkerColor(ROOT.kBlack);
    hPresel_cut.SetMarkerStyle(0);
    hPresel_cut.SetMarkerColor(col)
    hPresel_cut.SetMarkerStyle(0);
    #hPresel_cut.GetXaxis().SetTitle("#Delta#Phi")
    #hPresel_cut.GetYaxis().SetTitle("Number of Events/Bin")
    histos.append([hPresel_cut,name])
  
  for h,n in reversed(histos):
    #h.GetXaxis().SetTitle("#Delta#Phi")
    h.GetYaxis().SetTitle("Number of Events/Bin")
    h.Draw('same')
    l.AddEntry(h, n)

  hs1200.Draw('same')
  hs1500.Draw('same')
  l.AddEntry(hs1200, 'Gl1200_Chi1000_LSP800','l')
  l.AddEntry(hs1500, 'Gl1500_Chi800_LSP100','l')
  c1.SetLogy()
  #for sig in signals:
  #  l.AddEntry(sig['hPresel'], sig['name'],'l')
  #  sig['hPresel'].Draw('same')

  #hPresel.Draw('same')
  c1.RedrawAxis()
 # c1.SetXaxisTile("#Delta#Phi")
 # c1.SetYaxisTile("Number of events/Bin")
  latex1 = ROOT.TLatex()
  latex1.SetNDC()
  latex1.SetTextSize(0.035)
  latex1.SetTextAlign(11) # align right
  latex1.DrawLatex(0.16,0.96,"CMS Simulation")
  latex1.DrawLatex(0.7,0.96,"L=4 fb^{-1} (13 TeV)")
  l.Draw()
  c1.Print(path+fname+'_'+prefix+'notauRej.png')
  c1.Print(path+fname+'_'+prefix+'notauRej.root')

#hPresel_l_H = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], presel+"&&"+l_H, 'weight')
#hPresel_l_H.SetLineColor(ROOT.kRed)
#hPresel_l_H.Draw('same')
#
#hPresel_lTau_H = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], presel+"&&"+lTau_H, 'weight')
#hPresel_lTau_H.SetLineColor(ROOT.kBlue)
#hPresel_lTau_H.Draw('same')
#
#hPresel_hTau_l = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], presel+"&&"+hTau_l, 'weight')
#hPresel_hTau_l.SetLineColor(ROOT.kBlue)
#hPresel_hTau_l.Draw('same')
#
#hPresel_diLep = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], presel+"&&"+diLep, 'weight')
#hPresel_diLep.SetLineColor(ROOT.kGreen)
#hPresel_diLep.Draw('same')
#
#hPresel_lTau_l = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], presel+"&&"+lTau_l, 'weight')
#hPresel_lTau_l.SetLineColor(ROOT.kBlue)
#hPresel_lTau_l.Draw('same')
#
#hPresel_diTau = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], presel+"&&"+diTau, 'weight')
##hPresel_diTau.SetLineColor(ROOT.kGreen)
#hPresel_diTau.Draw('same')
#
#hPresel_diHad = getPlotFromChain(c, 'sqrt(2*leptonPt*met*(1-cos(metphi-leptonPhi)))', [20,0,800], presel+"&&"+diHad, 'weight')
##hPresel_diHad.SetLineColor(ROOT.kGreen)
#hPresel_diHad.Draw('same')
#
