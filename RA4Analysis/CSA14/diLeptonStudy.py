import ROOT
from Workspace.RA4Analysis.stage2Tuples import ttJetsCSA1450ns
from localInfo import username
from objectSelection import tightPOGMuID , vetoMuID , getLooseMuStage2
from math import sqrt, cos, sin, atan2
from array import array
from getmuon import getMu

Lumi=2000 #pb-1
xsec=689.1 #pb ?
#nevents is later

c50 = ROOT.TChain('Events')
c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from0To10.root')
#c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/*')

#number_events50 = c50.GetEntries()

#weight = Lumi*xsec/number_events50
weight = 0.436738650483
preselection = "ht>300 && njets>=3"    ##no met cut !!
c50.Draw(">>List",preselection)
List = ROOT.gDirectory.Get("List")
number_events = List.GetN()

Filetake = ROOT.TFile('EffSmall.root')
File = ROOT.TFile('MtSmall.root','RECREATE')

h_GenPt = ROOT.TH1F('h_GenPt', 'h_GenPt',25,0,800)
h_GenMet = ROOT.TH1F('h_GenMet', 'h_GenMet',25,0,800)
h_GenMt = ROOT.TH1F('h_GenMt', 'h_GenMt',25,0,800)

h_Pt = ROOT.TH1F('h_Pt', 'h_Pt',25,0,800)
h_Met = ROOT.TH1F('h_Met', 'h_Met',25,0,800)
h_MtPred = ROOT.TH1F('h_MtPred', 'h_MtPred',25,0,800)

for relIso in [0.12,0.2,0.3]:
  h_EffinDiLep = Filetake.Get("2D"+str(relIso)) #Finding eff in DiLep Events

  for i in range(number_events):
    c50.GetEntry(List.GetEntry(i))
    nmuCount = int(c50.GetLeaf('nmuCount').GetValue())
    ngoodMuons = c50.GetLeaf('ngoodMuons').GetValue()
    nvetoMuons = c50.GetLeaf('nvetoMuons').GetValue()
    nvetoElectrons = c50.GetLeaf('nvetoElectrons').GetValue()
    njets = c50.GetLeaf('njets').GetValue()
    met = c50.GetLeaf('met').GetValue()
    genMet = c50.GetLeaf('genMet').GetValue()
    ht = c50.GetLeaf('ht').GetValue()
    metphi = c50.GetLeaf('metphi').GetValue()
    genMetphi = c50.GetLeaf('genMetphi').GetValue()
    ngLep = int(c50.GetLeaf('ngLep').GetValue())
    ngNuMuFromW = c50.GetLeaf('ngNuMuFromW').GetValue() 
    ngNuEFromW = c50.GetLeaf('ngNuEFromW').GetValue()
    ntmuons=0
    nlmuons=0
    muons=[]
    for j in range(nmuCount):
      #muon=getMu(c50,j)
      muon=getLooseMuStage2(c50,j)
      if muon:
        isTight=tightPOGMuID(muon)
        isLoose=vetoMuID(muon,relIso)
        muon['isTight'] = isTight
        muon['isLoose'] = isLoose
        if isTight: ntmuons+=1
        if isLoose: nlmuons+=1
        muons.append(muon)
    #print 'enter ngLep loop'
    if met>150:
      for p in range(int(ngLep)):
        gLepPdg = c50.GetLeaf('gLepPdg').GetValue(p)
        gLepDR = c50.GetLeaf('gLepDR').GetValue(p)
        gLepPt = c50.GetLeaf('gLepPt').GetValue(p)
        gLepEta = c50.GetLeaf('gLepEta').GetValue(p)
        gLepInd = c50.GetLeaf('gLepInd').GetValue(p)
        gLepPhi = c50.GetLeaf('gLepPhi').GetValue(p)
        if abs(gLepPdg) == 13 and gLepPt>20 and abs(gLepEta)<2.1:
          if gLepInd>=0 and gLepDR<0.4 and ngNuMuFromW==2 and ngNuEFromW==0:
            k=int(gLepInd)
            if muons[k]['isLoose'] == 1 and muons[k]['pt']>20 and abs(1-muons[k]['pt']/gLepPt)<0.9:
              if ngoodMuons==1 and nvetoMuons==1 and nvetoElectrons==0:
                #h_MTGen.Fill(sqrt(2*genMet*gLepPt*(1-cos(gLepPhi-genMetphi))))
                h_GenMt.Fill(sqrt(2*met*muons[k]['pt']*(1-cos(muons[k]['phi']-metphi))))
                h_GenMet.Fill(met)
                h_GenPt.Fill(muons[k]['pt'])
    if len(muons)<2: continue
    if len(muons)==2 and ntmuons>=1:
      for perm in [muons, reversed(muons)]:
        m,m2 = perm
        if m2['isTight']==1:
          EffDiLep = h_EffinDiLep.GetBinContent(h_EffinDiLep.FindBin(m['pt'],m['eta']))
          if abs(m['eta'])<2.1 and m['pt']>20:
            metAdd=m['pt']
            Metx = met*cos(metphi)+cos(m['phi'])*metAdd
            Mety = met*sin(metphi)+sin(m['phi'])*metAdd
            metPred = sqrt(Metx**2+Mety**2)
            metphiPred = atan2(Mety,Metx)
            mtPred = sqrt(2*metPred*m2['pt']*(1-cos(m2['phi']-metphiPred)))
            if metPred >150:
              if EffDiLep !=0:
                Seff =  (1-EffDiLep)/(EffDiLep)
                h_MtPred.Fill(mtPred,weight*Seff)
                h_Met.Fill(metPred,weight*Seff)
                h_Pt.Fill(m2['pt'],weight*Seff)

  canMT = ROOT.TCanvas("MT"+str(relIso))
  canMT.cd()
  Pad1 = ROOT.TPad("Pad1", "Pad1", 0, 0.1, 1, 1.0)
  Pad1.Draw()
  Pad1.cd()
  h_MtPred.SetLineColor(ROOT.kBlue)
  h_MtPred.Draw()
  h_GenMt.SetLineColor(ROOT.kRed)
  h_GenMt.Draw('same')
  leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
  leg.AddEntry(h_MtPred, "Calculated","l")
  leg.AddEntry(h_GenMt, "MtGen","l")
  leg.SetFillColor(0)
  leg.Draw()
  Pad1.SetLogy()
  Pad2 = ROOT.TPad("Pad2", "Pad2", 0, 0, 1, 0.098)
  Pad2.Draw()
  Pad2.cd()
  h_ratio = h_MtPred.Clone("h_ratio")
  h_ratio.SetMinimum(0.0)
  h_ratio.SetMaximum(2.0)
  h_ratio.Sumw2()
  h_ratio.SetStats(0)
  h_ratio.Divide(h_GenMt)
  h_ratio.Draw("ep")
  canMT.Write()

  canPT = ROOT.TCanvas("PT"+str(relIso))
  canPT.cd()
  h_Pt.SetLineColor(ROOT.kBlue)
  h_Pt.Draw()
  h_GenPt.SetLineColor(ROOT.kRed)
  h_GenPt.Draw('same')
  leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
  leg.AddEntry(h_Pt, "Calculated","l")
  leg.AddEntry(h_GenPt, "PtGen","l")
  leg.SetFillColor(0)
  leg.Draw()
  canPT.SetLogy()
  canPT.Update()
  canPT.Write()

  canMet = ROOT.TCanvas("Met"+str(relIso))
  canMet.cd()
  h_Met.SetLineColor(ROOT.kBlue)
  h_Met.Draw()
  h_GenMet.SetLineColor(ROOT.kRed)
  h_GenMet.Draw('same')
  leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
  leg.AddEntry(h_Met, "Calculated","l")
  leg.AddEntry(h_GenMet, "MetGen","l")
  leg.SetFillColor(0)
  leg.Draw()
  canMet.SetLogy()
  canMet.Update()
  canMet.Write()


File.Write()
File.Close()

