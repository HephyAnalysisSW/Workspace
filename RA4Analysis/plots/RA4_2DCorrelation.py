import ROOT
from math import *
ROOT.gROOT.ProcessLine(".L ../scripts/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/useNiceColorPalette.C")
ROOT.useNiceColorPalette(20)
ROOT.tdrStyle.SetPadRightMargin(0.18)
ROOT.tdrStyle.SetPadBottomMargin(0.18)

cBkg = ROOT.TChain("Events")
cBkg.Add("/data/schoef/convertedTuples_v21/copyMET/Mu/TTJets-PowHeg/histo_TTJets-PowHeg.root")
cBkg.Add("/data/schoef/convertedTuples_v21/copyMET/Ele/TTJets-PowHeg/histo_TTJets-PowHeg.root")
cSig = ROOT.TChain("Events")
cSig.Add("/data/schoef/convertedTuples_v21/copyMET/Mu/T1tttt_1300_850/histo_T1tttt_1300_850.root")
cSig.Add("/data/schoef/convertedTuples_v21/copyMET/Ele/T1tttt_1300_850/histo_T1tttt_1300_850.root")

prefix = "red1_ht400-met150-6j-bt2"

cut = "weight*(ht>400&&type1phiMet>150&&njets>=6&&nbtags>=2&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoElectrons==1&&nvetoMuons==0))"

nbins=100
vars = [\
  [ "thrust"            , "thrust"        , [nbins,0,1]],
  [ "c2DLepMET"         , "c2DLepMET"     , [nbins,0,1]],
  [ "linC2DLepMET"      , "linC2DLepMET"  , [nbins,0,1]],
  [ "FWMT2LepMET"       , "FWMT2LepMET"   , [nbins,0,1]],
  [ "FWMT2"             , "FWMT2"         , [nbins,0,1]],
  [ "linC2D"            , "linC2D"        , [nbins,0,1]],
  [ "C2D"               , "C2D"           , [nbins,0,1]],
  [ "FWMT4LepMET"       , "FWMT4LepMET"   , [nbins,0,1]],
  [ "FWMT4"             , "FWMT4"         , [nbins,0,1]],
  [ "FWMT3LepMET"       , "FWMT3LepMET"   , [nbins,0,1]],
  [ "FWMT3"             , "FWMT3"         , [nbins,0,1]],
  [ "htThrustLepSide/ht", "htThrustLepSide/ht", [nbins,0,1]],
  [ "cosDeltaPhiLepW2", "0.5*(1 + ((leptonPt*cos(leptonPhi) + type1phiMetpx)*cos(leptonPhi) + (leptonPt*sin(leptonPhi) + type1phiMetpy)*sin(leptonPhi) )/sqrt((leptonPt*cos(leptonPhi) + type1phiMetpx)**2 + (leptonPt*sin(leptonPhi) + type1phiMetpy)**2))", [nbins,0,1]],
  [ "FWMT1"             , "FWMT1"         , [nbins,0,1]],
  [ "htRatio"           , "htRatio"       , [nbins,0,1]],
  [ "C3D"               , "C3D"           , [nbins,0,1]],
  [ "S3D"               , "S3D"           , [nbins,0,1]],
  [ "linS3D"            , "linS3D"        , [nbins,0,1]],
  [ "linC3D"            , "linC3D"        , [nbins,0,1]],
#  [ "FWMT1LepMET"       , "FWMT1LepMET"  , [nbins,0,1] ],
  [ "minDeltaPhiOverPi" , "minDeltaPhi/pi", [nbins,0,1]],
]
vars = [\
  [ "thrust"            , "thrust"        , [nbins,0,1]],
#  [ "c2DLepMET"         , "c2DLepMET"     , [nbins,0,1]],
#  [ "linC2DLepMET"      , "linC2DLepMET"  , [nbins,0,1]],
#  [ "FWMT2LepMET"       , "FWMT2LepMET"   , [nbins,0,1]],
#  [ "FWMT2"             , "FWMT2"         , [nbins,0,1]],
#  [ "linC2D"            , "linC2D"        , [nbins,0,1]],
#  [ "C2D"               , "C2D"           , [nbins,0,1]],
  [ "FWMT4LepMET"       , "FWMT4LepMET"   , [nbins,0,1]],
#  [ "FWMT4"             , "FWMT4"         , [nbins,0,1]],
#  [ "FWMT3LepMET"       , "FWMT3LepMET"   , [nbins,0,1]],
#  [ "FWMT3"             , "FWMT3"         , [nbins,0,1]],
  [ "htThrustLepSide/ht", "htThrustLepSide/ht", [nbins,0,1]],
  [ "cosDeltaPhiLepW2", "((leptonPt*cos(leptonPhi) + type1phiMetpx)*cos(leptonPhi) + (leptonPt*sin(leptonPhi) + type1phiMetpy)*sin(leptonPhi) )/sqrt((leptonPt*cos(leptonPhi) + type1phiMetpx)**2 + (leptonPt*sin(leptonPhi) + type1phiMetpy)**2)", [nbins,-1,1]],
#  [ "FWMT1"             , "FWMT1"         , [nbins,0,1]],
#  [ "htRatio"           , "htRatio"       , [nbins,0,1]],
#  [ "C3D"               , "C3D"           , [nbins,0,1]],
#  [ "S3D"               , "S3D"           , [nbins,0,1]],
  [ "linS3D"            , "linS3D"        , [nbins,0,1]],
#  [ "linC3D"            , "linC3D"        , [nbins,0,1]],
#  [ "FWMT1LepMET"       , "FWMT1LepMET"  , [nbins,0,1] ],
  [ "minDeltaPhiOverPi"  , "minDeltaPhi/pi", [nbins,0,1]],
  [ "met"                , "met",            [nbins,0,700]],
  [ "mT"                , "mT",            [nbins,0,500]],
  [ "mt2w"              , "mt2w",            [nbins,0,600]],
]
#vars = ["FWMT1", "FWMT2", "FWMT3", "FWMT4", "FWMT1LepMET", "FWMT2LepMET", "FWMT3LepMET", "FWMT4LepMET"]
#vars = ["thrust", "FWMT1LepMET", "FWMT2LepMET", "FWMT3LepMET", "FWMT4LepMET"]
c1 = ROOT.TCanvas()
SoverSqrtB = {}
for i, var in enumerate(vars):
  hname = "hBkg_"+str(i)
  cBkg.Draw(var[1]+">>"+hname+"(10,"+",".join(str(x) for x in var[2][1:])+")", cut)
  hBkg = ROOT.gDirectory.Get(hname)
  hname = "hSig_"+str(i)
  cSig.Draw(var[1]+">>"+hname+"(10,"+",".join(str(x) for x in var[2][1:])+")", cut, "hsame")
  hSig = ROOT.gDirectory.Get(hname)
  hSig.SetLineColor(ROOT.kRed)
  if hBkg.Integral()>0:
    hBkg.Scale(1./hBkg.Integral())
  if hSig.Integral()>0:
    hSig.Scale(hBkg.Integral()/hSig.Integral())
  nbins = hSig.GetNbinsX()
#  totB = 0.
#  totS = 0.
#  maxSOverSqrtB = 1
  diffM = 0.
  for i in range(1, nbins+1):
    b = hBkg.GetBinContent(i)
    s = hSig.GetBinContent(i)
#    if b>0 and s>=b: 
#      totB+=b
#      totS+=s
    diffM+=abs(s-b)
  SoverSqrtB[var[0]] = diffM
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngESV/"+prefix+"_SigVsBkg_"+var[0]+".png")

del c1
#  if totB>0.:
##    SoverSqrtB[var[0]] = totS/sqrt(totB) 
#    SoverSqrtB[var[0]] = totS/totB
#  else:
#    if totS>0.:
#      SoverSqrtB[var[0]] =  float('inf')
#    else:
#      SoverSqrtB[var[0]] = float('nan')
#  del hSig, hBkg
#
#def bestSOverBBothSides(hSig, hBkg):
#  return max(bestSOverB(hSig, hBkg,True), bestSOverB(hSig, hBkg,False))
#

corr={}
for i, var1 in enumerate(vars):
  corr[i]={}
  for j, var2 in enumerate(vars):
    if i==j:
      corr[i][j]={'bkg':1.,'sig':1.}
      continue
    if j<i:
      continue
    hname = "hBkg_"+str(i)+"_"+str(j)
    cBkg.Draw(var2[1]+":"+var1[1]+">>"+hname+"("+",".join([str(x) for x in var1[2]+var2[2]])+")", cut, "COLZ")
    hBkg = ROOT.gDirectory.Get(hname)

    hname = "hSig_"+str(i)+"_"+str(j)
    cSig.Draw(var2[1]+":"+var1[1]+">>"+hname+"("+",".join([str(x) for x in var1[2]+var2[2]])+")", cut, "COLZ")
    hSig = ROOT.gDirectory.Get(hname)
    corr[i][j] = {'bkg':hBkg.GetCorrelationFactor(), 'sig':hSig.GetCorrelationFactor()}
    print i,var1[0],j,var2[0],corr[i][j]
    if not corr.has_key(j):
      corr[j]={}
    corr[j][i] = corr[i][j]

absCorrBkgHist = ROOT.TH2F("absCorrBkg", "absCorrBkg", len(vars),0, len(vars),len(vars),0, len(vars))
absCorrBkgHist.GetXaxis().SetLabelSize(0.03)
absCorrBkgHist.GetYaxis().SetLabelSize(0.03)
absCorrSigHist = ROOT.TH2F("absCorrSig", "absCorrSig", len(vars),0, len(vars),len(vars),0, len(vars))
absCorrSigHist.GetXaxis().SetLabelSize(0.03)
absCorrSigHist.GetYaxis().SetLabelSize(0.03)

pairs = []
for i, var1 in enumerate(vars):
  for j, var2 in enumerate(vars):
    if j<i:
      continue
    absCorrBkgHist.Fill(var2[0],var1[0], abs(corr[i][j]['bkg']))
    absCorrSigHist.Fill(var2[0],var1[0], abs(corr[i][j]['sig']))
    pairs.append([abs(corr[i][j]['bkg']), corr[i][j]['bkg']/abs(corr[i][j]['bkg']), abs(corr[i][j]['sig']), corr[i][j]['sig']/abs(corr[i][j]['sig']), var1[0],var2[0],i,j])

c1 = ROOT.TCanvas()
for plot in [absCorrBkgHist, absCorrSigHist]:
  plot.Draw("COLZ")
  c1.Update()
  palette = plot.GetListOfFunctions().FindObject("palette");
  palette.SetX1NDC(0.83);
  palette.SetX2NDC(0.87);
  plot.GetXaxis().LabelsOption('v')
  plot.Draw("COLZ")
  latex = ROOT.TLatex();
#  latex.SetTextAngle(90)
#  latex.SetNDC();
  latex.SetTextSize(0.02);
  latex.SetTextAlign(11); 
  for i, var in enumerate(vars):
    latex.DrawLatex( i,i+1, str(round(SoverSqrtB[var[0]],2)))
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngESV/"+prefix+"_"+plot.GetName()+".png")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngESV/"+prefix+"_"+plot.GetName()+".root")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngESV/"+prefix+"_"+plot.GetName()+".pdf")

del c1

#pairs.sort()
#pairs.reverse()
#for p in pairs:
#  print p

