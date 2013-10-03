import ROOT, pickle
from math import *
ROOT.gROOT.ProcessLine(".L ../scripts/tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.ProcessLine(".L ../scripts/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)
ROOT.tdrStyle.SetPadRightMargin(0.18)

ROOT.gROOT.ProcessLine(".L ../limits/TriangularInterpolation.C+")
ROOT.gROOT.ProcessLine(".L ../limits/SmoothingUtils.C+")
ROOT.gROOT.ProcessLine(".L ../limits/interpolate.h")

#sms = "T1t1t"
#sms = "T5tttt"
sms = "T1tttt-madgraph"
#sms = "T1tttt"

maxZ={}
maxZ["T1tttt-madgraph"] = 0.6
maxZ["T1tttt"] = 0.6
maxZ["T1t1t"] = 0.3
maxZ["T5tttt"] = 0.4

signalRegions = [ \
  {'btb':'2', 'htb':(750,2500), 'metb':(250,350)},
  {'btb':'2', 'htb':(750,2500), 'metb':(350,450)},
  {'btb':'2', 'htb':(750,2500), 'metb':(450,2500)},
  {'btb':'3p', 'htb':(750,2500), 'metb':(150,250)},
  {'btb':'3p', 'htb':(750,2500), 'metb':(250,350)},
  {'btb':'3p', 'htb':(750,2500), 'metb':(350,450)},
  {'btb':'3p', 'htb':(750,2500), 'metb':(450,2500)},
  {'btb':'3p', 'htb':(400,750), 'metb':(150,250)},
  {'btb':'3p', 'htb':(400,750), 'metb':(250,2500)},
]

l={"cteq":44, "mstw":40, "nnpdf":100}
from smsInfo import xAxisTitle, yAxisTitle, th2Binning

for sr in signalRegions:
  htb = sr['htb'];metb = sr['metb'];btb = sr['btb']
  pdfUncert = {}
  pdfUncertPlus = {}
  pdfUncertMinus = {}

  for pdft in ["cteq", "mstw","nnpdf"]:
    print pdft, sr
    iname = "h_"+sms+'_'+pdft+"_btb"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])
    filename = '/data/schoef/results2012/pdfUncertainty/'+sms+'/'+iname+'.pkl'
    h = pickle.load(file(filename))
    inameRef = "h_"+sms+'_'+pdft+"_btbnone_ht_0_2500_met_0_2500"
    filenameRef = '/data/schoef/results2012/pdfUncertainty/'+sms+'/'+inameRef+'.pkl'
    hRef = pickle.load(file(filenameRef))
    h.Divide(hRef)
    pdfUncert[pdft]  = ROOT.TH2D("Uncertainty_"+pdft, "Uncertainty_"+pdft, h.GetNbinsX(), h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax(),  h.GetNbinsY(), h.GetYaxis().GetXmin(), h.GetYaxis().GetXmax())
    pdfUncert[pdft].GetXaxis().SetTitle(xAxisTitle[sms])
    pdfUncert[pdft].GetYaxis().SetTitle(yAxisTitle[sms])
    pdfUncertPlus[pdft] = pdfUncert[pdft].Clone()
    pdfUncertMinus[pdft] = pdfUncert[pdft].Clone()
#    pdfUncertPlus  = ROOT.TH2D("UncertaintyPlus_"+pdft, "UncertaintyPlus_"+pdft, h.GetNBinsX(), h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax(),  h.GetNBinsY(), h.GetYaxis().GetXm
#    pdfUncertMinus = ROOT.TH2D("UncertaintyMinus_"+pdft, "UncertaintyPlus_"+pdft, h.GetNBinsX(), h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax(),  h.GetNBinsY(), h.GetYaxis().GetX
    for ix in range(1, h.GetNbinsX() + 1):
      for iy in range(1, h.GetNbinsY() +1):
        varX = h.GetXaxis().GetBinLowEdge(ix)
        varY  = h.GetYaxis().GetBinLowEdge(iy)
        x0 = h.GetBinContent(h.FindBin(varX, varY, 0))
        Delta2XMaxPlus  = 0
        Delta2XMaxMinus = 0
        for iUnc in range(l[pdft]/2):
          nPlus =  1 + 2*iUnc
          nMinus = 2 + 2*iUnc
          xip = h.GetBinContent(h.FindBin(varX, varY, nPlus))
          xim = h.GetBinContent(h.FindBin(varX, varY, nMinus))
          Delta2XMaxPlus  += max(xip - x0, xim - x0, 0)**2
          Delta2XMaxMinus += max(x0 - xip, x0 - xim, 0)**2
#        print "Setting", ix, iy, x0, 0.5*(sqrt(Delta2XMaxPlus) - sqrt(Delta2XMaxMinus))
        if x0>0.:
          pdfUncert[pdft].SetBinContent(pdfUncert[pdft].FindBin(varX, varY),  abs(0.5*(sqrt(Delta2XMaxPlus) + sqrt(Delta2XMaxMinus)) / x0))
          pdfUncertPlus[pdft].SetBinContent(pdfUncert[pdft].FindBin(varX, varY),  abs(sqrt(Delta2XMaxPlus) / x0))
          pdfUncertMinus[pdft].SetBinContent(pdfUncert[pdft].FindBin(varX, varY),  abs(sqrt(Delta2XMaxMinus) / x0))

#    res = ROOT.doSmooth(pdfUncert[pdft],"ka3",2,0)
    c1 = ROOT.TCanvas()   
    pdfUncert[pdft].GetZaxis().SetRangeUser(0, maxZ[sms])
    pdfUncert[pdft].Draw("COLZ")
    c1.Update()
    palette = pdfUncert[pdft].GetListOfFunctions().FindObject("palette");
    palette.SetX1NDC(0.83);
    palette.SetX2NDC(0.87);
    c1.Modified();
    c1.Update();
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".png")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".pdf")
#    res.Draw("COLZ")
#    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+"_smoothed.png")
#    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+"_smoothed.root")
#    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+"_smoothed.pdf")
    del c1


  pdfUncert['max'] = pdfUncert['cteq'].Clone("hist2DSFunc")
  pdfUncert['max'].Reset()
  for ix in range(1, pdfUncert['max'].GetNbinsX() + 1):
    for iy in range(1, pdfUncert['max'].GetNbinsY() +1):
      for pdft in ["cteq", "mstw","nnpdf"]:
        maxPlus = 0
        maxMinus = 0
        if maxPlus<pdfUncertPlus[pdft].GetBinContent(ix,iy):
          maxPlus = pdfUncertPlus[pdft].GetBinContent(ix,iy)
        if maxMinus<pdfUncertMinus[pdft].GetBinContent(ix,iy):
          maxMinus = pdfUncertMinus[pdft].GetBinContent(ix,iy)
        pdfUncert['max'].SetBinContent(ix, iy, 0.5*(maxPlus + maxMinus))


  c1 = ROOT.TCanvas()
  iname = "sigPDFSys_"+sms+"_btb"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])
  pdfUncert['max'].GetXaxis().SetRangeUser(th2Binning[sms][1], th2Binning[sms][2])
  pdfUncert['max'].GetYaxis().SetRangeUser(th2Binning[sms][4], th2Binning[sms][5])
  pdfUncert['max'].GetZaxis().SetRangeUser(0, maxZ[sms])
  pdfUncert['max'].Draw("COLZ")
  c1.Update()
  palette = pdfUncert['max'].GetListOfFunctions().FindObject("palette");
  palette.SetX1NDC(0.83);
  palette.SetX2NDC(0.87);
  c1.Modified();
  c1.Update();
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".png")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".pdf")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".root")

  pdfUncert['mean'] = pdfUncert['cteq'].Clone("hist2DSFunc")
  pdfUncert['mean'].GetXaxis().SetTitle(xAxisTitle[sms])
  pdfUncert['mean'].GetYaxis().SetTitle(yAxisTitle[sms])
  pdfUncert['mean'].Add(pdfUncert['mstw'])
  pdfUncert['mean'].Add(pdfUncert['nnpdf'])
  pdfUncert['mean'].Scale(1./3.)

  c1 = ROOT.TCanvas()
  iname = "sigPDFMeanSys_"+sms+"_btb"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])
  pdfUncert['mean'].GetXaxis().SetRangeUser(th2Binning[sms][1], th2Binning[sms][2])
  pdfUncert['mean'].GetYaxis().SetRangeUser(th2Binning[sms][4], th2Binning[sms][5])
  pdfUncert['mean'].GetZaxis().SetRangeUser(0, maxZ[sms])
  pdfUncert['mean'].Draw("COLZ")
  c1.Update()
  palette = pdfUncert['mean'].GetListOfFunctions().FindObject("palette");
  palette.SetX1NDC(0.83);
  palette.SetX2NDC(0.87);
  c1.Modified();
  c1.Update();
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".png")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".pdf")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".root")

#  res = ROOT.doSmooth(pdfUncert['mean'],"ka3",2,0).Clone("hist2DSFunc")
  res = ROOT.interpolate(pdfUncert['max'].Clone(), "SW")
  iname = "sigPDFSys_"+sms+"_btb"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+"_interpolated"
  res.GetXaxis().SetRangeUser(th2Binning[sms][1], th2Binning[sms][2])
  res.GetYaxis().SetRangeUser(th2Binning[sms][4], th2Binning[sms][5])
  res.GetZaxis().SetRangeUser(0, maxZ[sms])
  res.Draw("COLZ")
  c1.Update()
  palette = res.GetListOfFunctions().FindObject("palette");
  palette.SetX1NDC(0.83);
  palette.SetX2NDC(0.87);
  c1.Modified();
  c1.Update();
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".png")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".pdf")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".root")

  res2 = ROOT.doSmooth(ROOT.interpolate(pdfUncert['max'].Clone(), "SW"), "ka3",2,0).Clone('hist2DSFunc')
  iname = "sigPDFSys_"+sms+"_btb"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+"_interpolated_smoothed"
  res2.GetXaxis().SetRangeUser(th2Binning[sms][1], th2Binning[sms][2])
  res2.GetYaxis().SetRangeUser(th2Binning[sms][4], th2Binning[sms][5])
  res2.GetZaxis().SetRangeUser(0, maxZ[sms])
  res2.Draw("COLZ")
  c1.Update()
  palette = res2.GetListOfFunctions().FindObject("palette");
  palette.SetX1NDC(0.83);
  palette.SetX2NDC(0.87);
  c1.Modified();
  c1.Update();
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".png")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".pdf")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".root")
  del c1

