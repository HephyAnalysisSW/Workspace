import os,sys,ROOT,pickle
from array import array
from math import sqrt, pi, cos, sin, atan2
#from localInfo import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getVarValue
from commons import pfTypes, label

ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/useNiceColorPalette.C")

ROOT.gStyle.SetOptStat(0)
ROOT.setTDRStyle()
#ROOT.gStyle.SetPadRightMargin(0.10);
if type(ROOT.tdrStyle)!=type(ROOT.gStyle):
  del ROOT.tdrStyle
  ROOT.setTDRStyle()
ROOT.tdrStyle.SetPadRightMargin(0.18)
ROOT.useNiceColorPalette(255)

sample = 'dy53X'
t = 'h'
c = ROOT.TChain('Events')
c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from0To1.root')
c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from1To2.root')
c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from2To3.root')
c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from3To4.root')
c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from4To5.root')
c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from5To6.root')
c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from6To7.root')
c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from7To8.root')
c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from8To9.root')
c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from9To10.root')

for ptBin in [[0,1],[1,2],[2,3], [3,10], [10,25]]:

  ifile = '/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+sample+'_occ_'+t+'_pt_'+str(ptBin[0])+'_'+str(ptBin[1])+'.root'
  f = ROOT.TFile(ifile)
  k = f.GetListOfKeys()[0].GetName()
  f.Close()
  canv = getObjFromFile(ifile, k)
  occ = canv.GetPrimitive('occ_'+t).Clone()

  ifile = '/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+sample+'_en_'+t+'_pt_'+str(ptBin[0])+'_'+str(ptBin[1])+'.root'
  f = ROOT.TFile(ifile)
  k = f.GetListOfKeys()[0].GetName()
  f.Close()
  canv = getObjFromFile(ifile, k)
  en = canv.GetPrimitive('en_'+t).Clone()

  a = occ.GetXaxis()
  etaBinning = [a.GetNbins(), a.GetXmin(),  a.GetXmax()]

  projOcc={}
  projPt={}
  for i in range(1,1+etaBinning[0]):
    h=occ.ProjectionY('occ_'+str(i),i,i)
    integr = h.Integral()
    if integr>0:
      h.Scale(h.GetNbinsX()/integr)
    projOcc[i] = h
    h=en.ProjectionY('en_'+str(i),i,i)
    integr = h.Integral()
    if integr>0:
      h.Scale(h.GetNbinsX()/integr)
    projPt[i] = h

  metPhi = ROOT.TH1F('metPhi','metPhi',30,-pi,pi)
  metPhiCorr = ROOT.TH1F('metPhiCorr','metPhiCorr',30,-pi,pi)
  metPhiCorrPt = ROOT.TH1F('metPhiCorrPt','metPhiCorrPt',30,-pi,pi)
  met = ROOT.TH1F('met','met',100,0,100)
  metCorr = ROOT.TH1F('metCorr','metCorr',100,0,100)
  metCorrPt = ROOT.TH1F('metCorrPt','metCorrPt',100,0,100)
  metx = ROOT.TH1F('metx','metx',100,-100,100)
  metxCorr = ROOT.TH1F('metxCorr','metxCorr',100,-100,100)
  metxCorrPt = ROOT.TH1F('metxCorrPt','metxCorrPt',100,-100,100)
  mety = ROOT.TH1F('mety','mety',100,-100,100)
  metyCorr = ROOT.TH1F('metyCorr','metyCorr',100,-100,100)
  metyCorrPt = ROOT.TH1F('metyCorrPt','metyCorrPt',100,-100,100)

  nEvents = min([30000, c.GetEntries()])
  for i in range(nEvents):
    if i%100==0:print "At",i,"/",nEvents
    mexUncorr = 0.
    meyUncorr = 0.
    mexCorr = 0.
    meyCorr = 0.
    mexCorrPt = 0.
    meyCorrPt = 0.
    c.GetEntry(i)
    nCand = getVarValue (c, 'nCand')
    counter=0
    for j in range(int(nCand)):
      if label[getVarValue(c, 'candId', j)] == t:
        pt = getVarValue (c, 'candPt', j)
        if pt>=ptBin[0] and pt<ptBin[1]:
          counter+=1
          eta = getVarValue (c, 'candEta', j)
          etaBin =  a.FindBin(eta)
          phi = getVarValue (c, 'candPhi', j)
          phiBin = projOcc[etaBin].FindBin(phi)
          resOcc = projOcc[etaBin].GetBinContent(phiBin)
          weightOcc=1.
          if resOcc>0:
            weightOcc=1./resOcc
          resPt = projPt[etaBin].GetBinContent(phiBin)
          weightPt=1.
          if resPt>0:
            weightPt=1./resPt
  #        print i,j,weight,'pt',pt,'eta',eta,'phi',phi
          cp = cos(phi)
          sp = sin(phi)
          dmx=cp*pt
          dmy=sp*pt
          mexUncorr-=dmx
          meyUncorr-=dmy
          mexCorr-=dmx*weightOcc
          meyCorr-=dmy*weightOcc
          mexCorrPt-=dmx*weightPt
          meyCorrPt-=dmy*weightPt
    if counter>0:
      metPhi.Fill(atan2(meyUncorr, mexUncorr))
      metPhiCorr.Fill(atan2(meyCorr, mexCorr))
      metPhiCorrPt.Fill(atan2(meyCorrPt, mexCorrPt))
      met.Fill(sqrt(mexUncorr**2+meyUncorr**2))
      metCorr.Fill(sqrt(mexCorr**2+meyCorr**2))
      metCorrPt.Fill(sqrt(mexCorrPt**2+meyCorrPt**2))
      metx.Fill(mexUncorr)
      metxCorr.Fill(mexCorr)
      metxCorrPt.Fill(mexCorrPt)
      mety.Fill(meyUncorr)
      metyCorr.Fill(meyCorr)
      metyCorrPt.Fill(meyCorrPt)

  c1 = ROOT.TCanvas()
  metPhi.SetLineColor(ROOT.kBlue)
  metPhi.Draw()
  metPhiCorr.SetLineColor(ROOT.kRed)
  metPhiCorr.Draw('same')
  metPhiCorrPt.SetLineColor(ROOT.kGreen)
  metPhiCorrPt.Draw('same')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/metPhi_comparison_'+sample+'_'+t+'_pt_'+str(ptBin[0])+'_'+str(ptBin[1])+'.png')

  c1 = ROOT.TCanvas()
  met.SetLineColor(ROOT.kBlue)
  met.Draw()
  metCorr.SetLineColor(ROOT.kRed)
  metCorr.Draw('same')
  metCorrPt.SetLineColor(ROOT.kGreen)
  metCorrPt.Draw('same')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/met_comparison_'+sample+'_'+t+'_pt_'+str(ptBin[0])+'_'+str(ptBin[1])+'.png')

  c1 = ROOT.TCanvas()
  metx.SetLineColor(ROOT.kBlue)
  metx.Draw()
  metxCorr.SetLineColor(ROOT.kRed)
  metxCorr.Draw('same')
  metxCorrPt.SetLineColor(ROOT.kGreen)
  metxCorrPt.Draw('same')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/metx_comparison_'+sample+'_'+t+'_pt_'+str(ptBin[0])+'_'+str(ptBin[1])+'.png')

  c1 = ROOT.TCanvas()
  mety.SetLineColor(ROOT.kBlue)
  mety.Draw()
  metyCorrPt.SetLineColor(ROOT.kGreen)
  metyCorrPt.Draw('same')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/mety_comparison_'+sample+'_'+t+'_pt_'+str(ptBin[0])+'_'+str(ptBin[1])+'.png')
