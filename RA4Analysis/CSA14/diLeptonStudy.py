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

ptBins  = array('d', [float(x) for x in range(10, 20)+range(20,50,3)+range(50,100,10)+range(100,300,30)])
#etaBins = array('d', [int(x)+30 for x in range(-30,32,2)])
etaBins = array('d', [float(x)/10. for x in range(-30,32,2)])

ptBinsCoarse  = array('d', [float(x) for x in range(10, 20)+range(20,50,5)+range(50,100,20)+range(100,310,50)])
etaBinsCoarse = array('d', [float(x)/10. for x in [-30,-25]+range(-21,22,6)+[25,30]])
##################OPENFile to take EFF######
Filetake = ROOT.TFile('LetsSee.root')
h_Eff03 = Filetake.Get('Iso03PtEtaEff')
h_Eff02 = Filetake.Get('Iso02PtEtaEff')
h_Eff01 = Filetake.Get('Iso01PtEtaEff')

h_EffinDiLep03 = Filetake.Get('Iso03PtEtaEffDiLep') #Finding eff in DiLep Events
h_EffinDiLep02 = Filetake.Get('Iso02PtEtaEffDiLep') #Finding eff in DiLep Events
h_EffinDiLep01 = Filetake.Get('Iso01PtEtaEffDiLep') #Finding eff in DiLep Events

###################HISTOGRAMS to FILL########
File = ROOT.TFile('MTFriday.root','RECREATE')
h_GenPt = ROOT.TH1F('h_GenPt', 'h_GenPt',25,0,800)
h_GenMet = ROOT.TH1F('h_GenMet', 'h_GenMet',25,0,800)

h_Pt03 = ROOT.TH1F('h_Pt03', 'h_Pt03',25,0,800)
h_Pt02 = ROOT.TH1F('h_Pt02', 'h_Pt02',25,0,800)
h_Pt01 = ROOT.TH1F('h_Pt01', 'h_Pt01',25,0,800)

h_Met03 = ROOT.TH1F('h_Met03', 'h_Met03',25,0,800)
h_Met02 = ROOT.TH1F('h_Met02', 'h_Met02',25,0,800)
h_Met01 = ROOT.TH1F('h_Met01', 'h_Met01',25,0,800)

h_MTDilepton03 = ROOT.TH1F('h_MTDilepton03', 'h_MTDilepton03',25,0,800)
h_MTDilepton02 = ROOT.TH1F('h_MTDilepton02', 'h_MTDilepton02',25,0,800)
h_MTDilepton01 = ROOT.TH1F('h_MTDilepton01', 'h_MTDilepton01',25,0,800)

h_MTGen = ROOT.TH1F('h_MTGen', 'h_MTGen',25,0,800)

c50 = ROOT.TChain('Events')
c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from0To10.root')
#c50.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/*')

number_events50 = c50.GetEntries()

#weight = Lumi*xsec/number_events50
weight = 0.436738650483
print 'weight is:', weight
print number_events50
for i in range(number_events50):
#for i in range(3000):
  c50.GetEntry(i)
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
  relIso = 200  ##no Cut
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
  numerator = 0
  denominator = 0
  #print 'enter ngLep loop'
  for p in range(int(ngLep)):
    gLepPdg = c50.GetLeaf('gLepPdg').GetValue(p)
    gLepDR = c50.GetLeaf('gLepDR').GetValue(p)
    gLepPt = c50.GetLeaf('gLepPt').GetValue(p)
    gLepEta = c50.GetLeaf('gLepEta').GetValue(p)
    gLepInd = c50.GetLeaf('gLepInd').GetValue(p)
    gLepPhi = c50.GetLeaf('gLepPhi').GetValue(p)
    if gLepInd>=0:
      k=int(gLepInd)
      #print k
      #for k in range(len(muons)): 
      if abs(gLepPdg) == 13 and muons[k]['pt']>20 and gLepPt>20 and abs(gLepEta)<2.1 and ht>300 and met>150 and njets>=3: ###in ttjet sample we have more jets then Wjets sample
        if muons[k]['isLoose'] == 1 and gLepDR<0.4: # and abs(1-muons[k]['pt']/gLepPt)<0.9:
          if muons[k]['relIso']<0.3:
             if ngNuMuFromW==2 and ngNuEFromW==0 and ngoodMuons==1 and nvetoMuons==1 and nvetoElectrons==0:
               #h_MTGen.Fill(sqrt(2*genMet*gLepPt*(1-cos(gLepPhi-genMetphi))))
               h_MTGen.Fill(sqrt(2*met*muons[k]['pt']*(1-cos(muons[k]['phi']-metphi))))
               h_GenMet.Fill(met)
               h_GenPt.Fill(muons[k]['pt'])
  if len(muons)<2: continue
  if len(muons)==2 and ntmuons>=1:
    #print "Found two muons",len(muons)
    for perm in [muons, reversed(muons)]:
      m,m2 = perm
      if m2['isTight']==1:
        Eff03 = h_Eff03.GetBinContent(h_Eff03.FindBin(m['pt'],m['eta']))
        Eff02 = h_Eff02.GetBinContent(h_Eff02.FindBin(m['pt'],m['eta']))
        Eff01 = h_Eff01.GetBinContent(h_Eff01.FindBin(m['pt'],m['eta']))
        EffDiLep03 = h_EffinDiLep03.GetBinContent(h_EffinDiLep03.FindBin(m['pt'],m['eta']))
        EffDiLep02 = h_EffinDiLep02.GetBinContent(h_EffinDiLep02.FindBin(m['pt'],m['eta']))
        EffDiLep01 = h_EffinDiLep01.GetBinContent(h_EffinDiLep01.FindBin(m['pt'],m['eta']))
        if m['relIso']<0.3 and abs(m['eta'])<2.1 and m['pt']>20 and ht>300 and njets>=3:
          metAdd=m['pt']
          Metx = met*cos(metphi)+cos(m['phi'])*metAdd
          Mety = met*sin(metphi)+sin(m['phi'])*metAdd
          metPred = sqrt(Metx**2+Mety**2)
          metphiPred = atan2(Mety,Metx)
          mtPred = sqrt(2*metPred*m2['pt']*(1-cos(m2['phi']-metphiPred)))
          if metPred >150:
            if Eff03 !=0:
              Seff =  (1-Eff03)/Eff03
              h_MTDilepton03.Fill(mtPred,weight*Seff)
              h_Met03.Fill(metPred,weight*Seff)
              h_Pt03.Fill(m2['pt'],weight*Seff)
            if Eff02 !=0:
              Seff =  (1-Eff02)/Eff02
              h_MTDilepton02.Fill(mtPred,weight*Seff)
              h_Met02.Fill(metPred,weight*Seff)
              h_Pt02.Fill(m2['pt'],weight*Seff)
            if Eff01 !=0:
              Seff =  (1-Eff01)/Eff01
              h_MTDilepton01.Fill(mtPred,weight*Seff)
              h_Met01.Fill(metPred,weight*Seff)
              h_Pt01.Fill(m2['pt'],weight*Seff)

File.cd() 

canMT = ROOT.TCanvas('MT03')
canMT.cd()
h_MTDilepton03.SetLineColor(ROOT.kBlue)
#h_MTDilepton.Scale(h_MTGen.Integral()/h_MTDilepton.Integral())
h_MTDilepton03.Draw()
h_MTGen.SetLineColor(ROOT.kRed)
h_MTGen.Draw('same')
leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
leg.AddEntry(h_MTDilepton03, "Calculated","l")
leg.AddEntry(h_MTGen, "MtGen","l")
leg.SetFillColor(0)
leg.Draw()
canMT.SetLogy()
canMT.Write()

canMT02 = ROOT.TCanvas('MT02')
canMT02.cd()
h_MTDilepton02.SetLineColor(ROOT.kBlue)
#h_MTDilepton.Scale(h_MTGen.Integral()/h_MTDilepton.Integral())
h_MTDilepton02.Draw()
h_MTGen.SetLineColor(ROOT.kRed)
h_MTGen.Draw('same')
leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
leg.AddEntry(h_MTDilepton02, "Calculated","l")
leg.AddEntry(h_MTGen, "MtGen","l")
leg.SetFillColor(0)
leg.Draw()
canMT02.SetLogy()
canMT02.Write()

canMT01 = ROOT.TCanvas('MT01')
canMT01.cd()
h_MTDilepton01.SetLineColor(ROOT.kBlue)
#h_MTDilepton.Scale(h_MTGen.Integral()/h_MTDilepton.Integral())
h_MTDilepton01.Draw()
h_MTGen.SetLineColor(ROOT.kRed)
h_MTGen.Draw('same')
leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
leg.AddEntry(h_MTDilepton01, "Calculated","l")
leg.AddEntry(h_MTGen, "MtGen","l")
leg.SetFillColor(0)
leg.Draw()
canMT01.SetLogy()
canMT01.Write()


canPT = ROOT.TCanvas('PT')
canPT.cd()
h_Pt03.SetLineColor(ROOT.kBlue)
h_Pt03.Draw()
h_GenPt.SetLineColor(ROOT.kRed)
h_GenPt.Draw('same')
leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
leg.AddEntry(h_Pt03, "Calculated","l")
leg.AddEntry(h_GenPt, "PtGen","l")
leg.SetFillColor(0)
leg.Draw()
canPT.SetLogy()
canPT.Update()
canPT.Write()

canPT02 = ROOT.TCanvas('PT02')
canPT02.cd()
h_Pt02.SetLineColor(ROOT.kBlue)
h_Pt02.Draw()
h_GenPt.SetLineColor(ROOT.kRed)
h_GenPt.Draw('same')
leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
leg.AddEntry(h_Pt02, "Calculated","l")
leg.AddEntry(h_GenPt, "PtGen","l")
leg.SetFillColor(0)
leg.Draw()
canPT02.SetLogy()
canPT02.Update()
canPT02.Write()

canPT01 = ROOT.TCanvas('PT01')
canPT01.cd()
h_Pt01.SetLineColor(ROOT.kBlue)
h_Pt01.Draw()
h_GenPt.SetLineColor(ROOT.kRed)
h_GenPt.Draw('same')
leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
leg.AddEntry(h_Pt01, "Calculated","l")
leg.AddEntry(h_GenPt, "PtGen","l")
leg.SetFillColor(0)
leg.Draw()
canPT01.SetLogy()
canPT01.Update()
canPT01.Write()


canMet03 = ROOT.TCanvas('Met03')
canMet03.cd()
h_Met03.SetLineColor(ROOT.kBlue)
h_Met03.Draw()
h_GenMet.SetLineColor(ROOT.kRed)
h_GenMet.Draw('same')
leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
leg.AddEntry(h_Met03, "Calculated","l")
leg.AddEntry(h_GenMet, "MetGen","l")
leg.SetFillColor(0)
leg.Draw()
canMet03.SetLogy()
canMet03.Update()
canMet03.Write()

canMet02 = ROOT.TCanvas('Met02')
canMet02.cd()
h_Met02.SetLineColor(ROOT.kBlue)
h_Met02.Draw()
h_GenMet.SetLineColor(ROOT.kRed)
h_GenMet.Draw('same')
leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
leg.AddEntry(h_Met02, "Calculated","l")
leg.AddEntry(h_GenMet, "MetGen","l")
leg.SetFillColor(0)
leg.Draw()
canMet02.SetLogy()
canMet02.Update()
canMet02.Write()

canMet01 = ROOT.TCanvas('Met01')
canMet01.cd()
h_Met01.SetLineColor(ROOT.kBlue)
h_Met01.Draw()
h_GenMet.SetLineColor(ROOT.kRed)
h_GenMet.Draw('same')
leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
leg.AddEntry(h_Met01, "Calculated","l")
leg.AddEntry(h_GenMet, "MetGen","l")
leg.SetFillColor(0)
leg.Draw()
canMet01.SetLogy()
canMet01.Update()
canMet01.Write()

File.Write()
File.Close()

