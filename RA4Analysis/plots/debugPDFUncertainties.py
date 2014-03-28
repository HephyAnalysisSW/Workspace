import ROOT, pickle
from math import *
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)
ROOT.tdrStyle.SetPadRightMargin(0.16)

ROOT.gROOT.ProcessLine(".L ../limits/TriangularInterpolation.C+")
ROOT.gROOT.ProcessLine(".L ../limits/SmoothingUtils.C+")

ROOT.gStyle.SetOptStat()

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

for sr in signalRegions[2:3]:
  pdfUncert = {}
  eff = {}
  for pdft in ["cteq", "mstw","nnpdf"]:
    print pdft, sr 
    htb = sr['htb'];metb = sr['metb'];btb = sr['btb']
    iname = "h_"+pdft+"_btb"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])
    filename = '/data/schoef/results2012/pdfUncertainty/T1tttt/'+iname+'.pkl'
    h = pickle.load(file(filename))
    inameRef = "h_"+pdft+"_btbnone_ht_0_2500_met_0_2500"
    filenameRef = '/data/schoef/results2012/pdfUncertainty/T1tttt/'+inameRef+'.pkl'
    hRef = pickle.load(file(filenameRef)) 
    h.Divide(hRef)
    pdfUncert[pdft]  = ROOT.TH2D("Uncertainty_"+pdft, "Uncertainty_"+pdft, h.GetNbinsX(), h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax(),  h.GetNbinsY(), h.GetYaxis().GetXmin(), h.GetYaxis().GetXmax())
    eff[pdft]  = ROOT.TH1D("eff_"+pdft, "eff_"+pdft, 20, 0.5, 1.5)
#    pdfUncertPlus  = ROOT.TH2D("UncertaintyPlus_"+pdft, "UncertaintyPlus_"+pdft, h.GetNBinsX(), h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax(),  h.GetNBinsY(), h.GetYaxis().GetXmin(), h.GetYaxis().GetXmax())
#    pdfUncertMinus = ROOT.TH2D("UncertaintyMinus_"+pdft, "UncertaintyPlus_"+pdft, h.GetNBinsX(), h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax(),  h.GetNBinsY(), h.GetYaxis().GetXmin(), h.GetYaxis().GetXmax())
    for ix in range(1, h.GetNbinsX() + 1):
      for iy in range(1, h.GetNbinsY() +1):
        mgl = h.GetXaxis().GetBinLowEdge(ix)
        mn  = h.GetYaxis().GetBinLowEdge(iy)
        if not (mgl==1400 and mn == 1000): continue
        x0 = h.GetBinContent(h.FindBin(mgl, mn, 0))
        Delta2XMaxPlus  = 0
        Delta2XMaxMinus = 0
        for iUnc in range(l[pdft]/2):
          nPlus =  1 + 2*iUnc
          nMinus = 2 + 2*iUnc
          xip = h.GetBinContent(h.FindBin(mgl, mn, nPlus))
          xim = h.GetBinContent(h.FindBin(mgl, mn, nMinus))
          Delta2XMaxPlus  += max(xip - x0, xim - x0, 0)**2
          Delta2XMaxMinus += max(x0 - xip, x0 - xim, 0)**2
          eff[pdft].Fill(xip/x0)
          eff[pdft].Fill(xim/x0)
          print xip/x0 - xim/x0
#        print "Setting", ix, iy, x0, 0.5*(sqrt(Delta2XMaxPlus) - sqrt(Delta2XMaxMinus)) 
        if x0>0.:
          pdfUncert[pdft].SetBinContent(pdfUncert[pdft].FindBin(mgl, mn),  abs(0.5*(sqrt(Delta2XMaxPlus) - sqrt(Delta2XMaxMinus)) / x0))

eff['cteq'].Draw()
eff['mstw'].SetLineColor(ROOT.kRed)
eff['mstw'].Draw("same")
eff['nnpdf'].SetLineColor(ROOT.kBlue)
eff['nnpdf'].Draw("same")

print "RMS:", eff['cteq'].GetRMS(), eff['mstw'].GetRMS(), eff['nnpdf'].GetRMS()

#    c1 = ROOT.TCanvas()
#    pdfUncert[pdft].Draw("COLZ")
#    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".png")
#    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".pdf")
#    res = ROOT.doSmooth(pdfUncert[pdft],"ka3",2,0)
#    res.Draw("COLZ")
#    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+"_smoothed.png")
#    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+"_smoothed.pdf")
#    del c1


#        pdfUncert[htb][metb][btb][pdf] = {}
#        pdfUncert[htb][metb][btb][pdf]["+"] =  pdfAccUncertMap[htb][metb][btb][pdf][0].Clone(pdfAccUncertMap[htb][metb][btb][pdf][0].GetName().replace("_Efficiency", "_PDFUncertaintyPlus"))
#        pdfUncert[htb][metb][btb][pdf]["-"] =  pdfAccUncertMap[htb][metb][btb][pdf][0].Clone(pdfAccUncertMap[htb][metb][btb][pdf][0].GetName().replace("_Efficiency", "_PDFUncertaintyMinus"))
#        pdfUncert[htb][metb][btb][pdf]["relErr"] =  pdfAccUncertMap[htb][metb][btb][pdf][0].Clone(pdfAccUncertMap[htb][metb][btb][pdf][0].GetName().replace("_Efficiency", "_PDFUncertaintyMinus"))
#        pdfUncert[htb][metb][btb][pdf]["+"].Reset()
#        pdfUncert[htb][metb][btb][pdf]["-"].Reset()
#        pdfUncert[htb][metb][btb][pdf]["relErr"].Reset()
#        for ix in range(1, pdfAccUncertMap[htb][metb][btb][pdf][0].GetNbinsX() + 1):
#          for iy in range(1, pdfAccUncertMap[htb][metb][btb][pdf][0].GetNbinsY() +1):
#            x0 = pdfAccUncertMap[htb][metb][btb][pdf][0].GetBinContent(ix, iy)
#            Delta2XMaxPlus  = 0
#            Delta2XMinusMax = 0
#            for iUnc in range(l[pdf]/2):
#              nPlus =  1 + 2*iUnc
#              nMinus = 2 + 2*iUnc
#              xip = pdfAccUncertMap[htb][metb][btb][pdf][nPlus].GetBinContent(ix, iy)
#              xim = pdfAccUncertMap[htb][metb][btb][pdf][nMinus].GetBinContent(ix, iy)
#              Delta2XMaxPlus  += max(xip - x0, xim - x0, 0)**2
#              Delta2XMinusMax += max(x0 - xip, x0 - xim, 0)**2
#            pdfUncert[htb][metb][btb][pdf]["+"].SetBinContent(ix, iy, sqrt(Delta2XMaxPlus))
#            pdfUncert[htb][metb][btb][pdf]["-"].SetBinContent(ix, iy, sqrt(Delta2XMinusMax))
#        pdfUncert[htb][metb][btb][pdf]["relErr"] = pdfUncert[htb][metb][btb][pdf]["-"].Clone(pdfUncert[htb][metb][btb][pdf]["-"].GetName().replace("_PDFUncertaintyMinus", "relError"))
#        pdfUncert[htb][metb][btb][pdf]["relErr"].Scale(-1)
#        pdfUncert[htb][metb][btb][pdf]["relErr"].Add(pdfUncert[htb][metb][btb][pdf]["+"])
#        pdfUncert[htb][metb][btb][pdf]["relErr"].Divide(pdfAccUncertMap[htb][metb][btb][pdf][0])
#        pdfUncert[htb][metb][btb][pdf]["relErr"].Scale(0.5)
#
#pickle.dump(pdfUncert, file('/data/schoef/results2012/pdfUncert.pkl', 'w'))

