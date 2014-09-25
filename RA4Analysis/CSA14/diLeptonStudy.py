import ROOT
from Workspace.RA4Analysis.stage2Tuples import ttJetsCSA1450ns
from localInfo import username
from objectSelection import tightPOGMuID , vetoMuID , getLooseMuStage2
from math import sqrt, cos, sin, atan2
from array import array
from getmuon import getMu

print 'MT for reliso<0.2'
Lumi=2000 #pb-1
xsec=689.1 #pb ?
#nevents is later

ptBins  = array('d', [float(x) for x in range(10, 20)+range(20,50,3)+range(50,100,10)+range(100,300,30)])
#etaBins = array('d', [int(x)+30 for x in range(-30,32,2)])
etaBins = array('d', [float(x)/10. for x in range(-30,32,2)])

ptBinsCoarse  = array('d', [float(x) for x in range(10, 20)+range(20,50,5)+range(50,100,20)+range(100,310,50)])
etaBinsCoarse = array('d', [float(x)/10. for x in [-30,-25]+range(-21,22,6)+[25,30]])
##################OPENFile to take EFF######
Filetake = ROOT.TFile('EffMapDiLep02.root')
h_Eff = Filetake.Get('Iso03PtEtaEff')
h_EffinDiLep = Filetake.Get('Iso03PtEtaEffDiLep') #Finding eff in DiLep Events
h_EffDiLep = Filetake.Get('Iso03PtEtaEffFindDiLep') ##Find probability of having dilep
h_Eff01 = Filetake.Get('Iso02PtEtaEff')

###################HISTOGRAMS to FILL########
File = ROOT.TFile('MT02OO.root','RECREATE')
h_GenPt = ROOT.TH1F('h_GenPt', 'h_GenPt',25,0,800)
h_GenMet = ROOT.TH1F('h_GenMet', 'h_GenMet',25,0,800)

h_Pt = ROOT.TH1F('h_Pt', 'h_Pt',25,0,800)
h_Met = ROOT.TH1F('h_Met', 'h_Met',25,0,800)

h_MTDilepton = ROOT.TH1F('h_MTDilepton', 'h_MTDilepton',25,0,800)
h_MTGen = ROOT.TH1F('h_MTGen', 'h_MTGen',25,0,800)
h_MTDileptonWithDiLepScale = ROOT.TH1F('h_MTDileptonWithDiLepScale', 'h_MTDileptonWithDiLepScale',25,0,800)
h_MTDileptonProb = ROOT.TH1F('h_MTDileptonProb', 'h_MTDileptonProb',25,0,800)
h_Trial = ROOT.TH1F('h_Trial', 'h_Trial',25,0,800)
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
      if m2['isTight']==1 and m['relIso']<0.3 and abs(m['eta'])<2.1 and m['pt']>20 and ht>300 and njets>=3:
        Eff = h_Eff.GetBinContent(h_Eff.FindBin(m['pt'],m['eta']))
        Eff01 = h_Eff01.GetBinContent(h_Eff.FindBin(m['pt'],m['eta']))
        EffDiLep = h_EffinDiLep.GetBinContent(h_EffinDiLep.FindBin(m['pt'],m['eta']))
        Scale = Eff01*EffDiLep
        DiLepProb = h_EffDiLep.GetBinContent(h_EffDiLep.FindBin(m['pt'],m['eta']))
        lostProb = 1-DiLepProb
        Try2 = DiLepProb*EffDiLep
        metAdd=m['pt']
        Metx = met*cos(metphi)+cos(m['phi'])*metAdd
        Mety = met*sin(metphi)+sin(m['phi'])*metAdd
        metPred = sqrt(Metx**2+Mety**2)
        metphiPred = atan2(Mety,Metx)
        mtPred = sqrt(2*metPred*m2['pt']*(1-cos(m2['phi']-metphiPred)))
        if metPred >150:
          if Eff !=0:
            Seff =  (1-Eff)/Eff
            Try_ =(1-(Eff*Eff))/(Eff*Eff) 
            h_MTDilepton.Fill(mtPred,weight*Seff)
            h_Met.Fill(metPred,weight*Seff)
            h_Pt.Fill(m2['pt'],weight*Seff)
          if Eff01 !=0:
            h_Trial.Fill(mtPred,weight*((1-Eff01)/Eff01))
          if Scale != 0:
            SScale = (1-Scale)/Scale
            h_MTDileptonWithDiLepScale.Fill(mtPred,weight*SScale)
          if DiLepProb != 0:
            h_MTDileptonProb.Fill(mtPred,weight*(lostProb/DiLepProb))

File.cd() 

canMT = ROOT.TCanvas('MT')
canMT.cd()
h_MTDilepton.SetLineColor(ROOT.kBlue)
#h_MTDilepton.Scale(h_MTGen.Integral()/h_MTDilepton.Integral())
h_MTDilepton.Draw()
h_MTGen.SetLineColor(ROOT.kRed)
h_MTGen.Draw('same')
leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
leg.AddEntry(h_MTDilepton, "Calculated","l")
leg.AddEntry(h_MTGen, "PtGen","l")
leg.SetFillColor(0)
leg.Draw()
canMT.SetLogy()
canMT.Write()

canMTDiLep = ROOT.TCanvas('MTDiLep')
canMTDiLep.cd()
h_MTDileptonWithDiLepScale.SetLineColor(ROOT.kBlue)
h_MTDileptonWithDiLepScale.Draw()
h_MTGen.SetLineColor(ROOT.kRed)
h_MTGen.Draw('same')
leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
leg.AddEntry(h_MTDileptonWithDiLepScale, "Calculated","l")
leg.AddEntry(h_MTGen, "PtGen","l")
leg.SetFillColor(0)
leg.Draw()
canMTDiLep.SetLogy()
canMTDiLep.Write()

canMTofDiLep = ROOT.TCanvas('MTofDiLep')
canMTofDiLep.cd()
h_MTDileptonProb.SetLineColor(ROOT.kBlue)
h_MTDileptonProb.Draw()
h_MTGen.SetLineColor(ROOT.kRed)
h_MTGen.Draw('same')
leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
leg.AddEntry(h_MTDileptonProb, "Calculated","l")
leg.AddEntry(h_MTGen, "PtGen","l")
leg.SetFillColor(0)
leg.Draw()
canMTofDiLep.SetLogy()
canMTofDiLep.Write()

cT = ROOT.TCanvas('Trial')
cT.cd()
h_Trial.SetLineColor(ROOT.kBlue)
h_Trial.Draw()
h_MTGen.SetLineColor(ROOT.kRed)
h_MTGen.Draw('same')
leg = ROOT.TLegend(0.6,0.6,0.9,0.7)
leg.AddEntry(h_Trial, "Calculated","l")
leg.AddEntry(h_MTGen, "PtGen","l")
leg.SetFillColor(0)
leg.Draw()
cT.SetLogy()
cT.Write()

canPT = ROOT.TCanvas('PT')
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


canMet = ROOT.TCanvas('Met')
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

