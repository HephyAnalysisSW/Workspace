import ROOT
from Workspace.RA4Analysis.stage2Tuples import ttJetsCSA1450ns
from localInfo import username
from objectSelection import tightPOGMuID , vetoMuID , getLooseMuStage2
from math import sqrt, cos, sin, atan2
from array import array
from getmuon import getMu , getGenLep

Lumi=2000 #pb-1
xsec=689.1 #pb ?
#nevents is later

c50 = ROOT.TChain('Events')
#c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from0To10.root')
c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/*')

#number_events50 = c50.GetEntries()

#weight = Lumi*xsec/number_events50
#weight = 0.436738650483
preselection = "ht>300 && njets>=3"
selection1="&&ngNuMuFromW==2&&ngNuEFromW==0"
selection2="&&ntauCount==0"

c50.Draw(">>List",preselection+selection1)
List = ROOT.gDirectory.Get("List")
number_events = List.GetN()

Filetake = ROOT.TFile('Eff.root')
File = ROOT.TFile('MtT1V1.root','RECREATE')

h_GenPt = ROOT.TH1F('h_GenPt', 'h_GenPt',25,0,800)
h_GenMet = ROOT.TH1F('h_GenMet', 'h_GenMet',25,0,800)
h_GenMt = ROOT.TH1F('h_GenMt', 'h_GenMt',25,0,800)
h_GenDeltaPhi = ROOT.TH1F('h_GenDeltaPhi', 'h_GenDeltaPhi',25,-3,3)

h_Pt = ROOT.TH1F('h_Pt', 'h_Pt',25,0,800)
h_Met = ROOT.TH1F('h_Met', 'h_Met',25,0,800)
h_MtPred = ROOT.TH1F('h_MtPred', 'h_MtPred',25,0,800)
h_DeltaPhi = ROOT.TH1F('h_DeltaPhi', 'h_DeltaPhi',25,-3,3)

for relIso in [0.12,0.2,0.3]:
#for relIso in [0.3]:
  h_EffinDiLep = Filetake.Get("2D"+str(relIso)) #Finding eff in DiLep Events
  print 'For relIso:',"2D"+str(relIso)
  for i in range(number_events):
    weight = c50.GetLeaf('weight').GetValue()
    c50.GetEntry(List.GetEntry(i))
    print number_events-i,'events left'
    ntauCount = c50.GetLeaf('ntauCount').GetValue()
    #print 'ntauCount before: ',ntauCount 
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
    gLeps=[]
    #Get all genLeps
    for p in range(int(ngLep)):
      genLep = getGenLep(c50,p)
      if genLep:
        gLeps.append(genLep)  
    for j in range(nmuCount):
      muon=getMu(c50,j)
      #muon=getLooseMuStage2(c50,j)
      if muon:
        isTight=tightPOGMuID(muon)
        isLoose=vetoMuID(muon,relIso)
        muon['isTight'] = isTight
        muon['isLoose'] = isLoose
        if isTight: ntmuons+=1
        if isLoose: nlmuons+=1
        hasMatch = False
        # for gl in genLepts: 
        #  if gl['gLepInd']==j:
        #    hasMatch=True
        # muon['hasMatch']=hasMatch
        for gl in gLeps:
          if gl['gLepInd']==j and gl['gLepDR']<0.4: hasMatch=True
        muon['hasMatch']=hasMatch  
        muons.append(muon)
    #print 'enter ngLep loop'
    if met>150:
      # for truth (1 tight mu reco'd, 1 gen mu not reco'd, ngMuNuFromW==2<->gendiLep ):
      # 1. get all reco muons, store loose/tight -> Done
      # 2. require ntmuons==1->tightMuon, nlmuons==1 
      #    tightMatchedMuons = filter(lambda x:x['hasMatch'] and x['isTight'], muons) 
      #    muon = tightMatchedMuons[0]
      #     if len(tightMatchedMuons!=1) print "Warning"
      # 3. calculate mT(met, tightMuon)
      # for genlepmatch: require also tightMuon['hasMatch'] 
      tightMatchedMuons = filter(lambda x:x['hasMatch'] and x['isTight'], muons)
      if ntmuons==1 and nlmuons==1 and len(tightMatchedMuons)==1:
        if len(tightMatchedMuons) >1 : print "Warning"
        TightMatchedMuon = tightMatchedMuons[0]
        h_GenMt.Fill(sqrt(2*met*TightMatchedMuon['pt']*(1-cos(TightMatchedMuon['phi']-metphi))), weight)
        h_GenMet.Fill(met, weight)
        h_GenPt.Fill(TightMatchedMuon['pt'], weight)
        h_GenDeltaPhi.Fill(cos(TightMatchedMuon['phi']-metphi), weight)

    if len(muons)<2: continue
    if len(muons)==2 and ntmuons>=1:
      for perm in [muons, reversed(muons)]:
        m,m2 = perm
        if m2['isTight']==1:
          EffDiLep = h_EffinDiLep.GetBinContent(h_EffinDiLep.FindBin(m['pt'],m['eta']))
          if abs(m['eta'])<2.5 and m['pt']>15:
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
                h_DeltaPhi.Fill(cos(m2['phi']-metphiPred),weight*Seff)

  canMT = ROOT.TCanvas("MT"+str(relIso))
  canMT.cd()
  Pad1 = ROOT.TPad("Pad1", "Pad1", 0, 0.1, 1, 1.0)
  Pad1.Draw()
  Pad1.cd()
  h_GenMt.SetLineColor(ROOT.kRed)
  h_GenMt.Draw()
  h_MtPred.SetLineColor(ROOT.kBlue)
  h_MtPred.Draw('same')
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
  h_GenPt.SetLineColor(ROOT.kRed)
  h_GenPt.Draw()
  h_Pt.SetLineColor(ROOT.kBlue)
  h_Pt.Draw('same')
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
  h_GenMet.SetLineColor(ROOT.kRed)
  h_GenMet.Draw()
  h_Met.SetLineColor(ROOT.kBlue)
  h_Met.Draw('same')
  leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
  leg.AddEntry(h_Met, "Calculated","l")
  leg.AddEntry(h_GenMet, "MetGen","l")
  leg.SetFillColor(0)
  leg.Draw()
  canMet.SetLogy()
  canMet.Update()
  canMet.Write()

  canDeltaPhi = ROOT.TCanvas("DeltaPhi"+str(relIso))
  canDeltaPhi.cd()
  h_GenDeltaPhi.SetLineColor(ROOT.kRed)
  h_GenDeltaPhi.Draw()
  h_DeltaPhi.SetLineColor(ROOT.kBlue)
  h_DeltaPhi.Draw('same')
  leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
  leg.AddEntry(h_DeltaPhi, "Calculated","l")
  leg.AddEntry(h_GenDeltaPhi, "DeltaPhiGen","l")
  leg.SetFillColor(0)
  leg.Draw()
  canDeltaPhi.SetLogy()
  canDeltaPhi.Update()
  canDeltaPhi.Write()

File.Write()
File.Close()

