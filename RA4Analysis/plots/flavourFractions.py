#
# fit flavour fractions on discriminator histograms from input file
#   (iterate and add MC errors according to fractions)
#
import ROOT
from math import sqrt

ROOT.gROOT.ProcessLine(".L f1FlavourFractions.C+")

hFile = ROOT.TFile.Open("hDisc.root")
hDisc0 = hFile.Get("hDisc0")
hDiscC = hFile.Get("hDiscC")
hDiscB = hFile.Get("hDiscB")
hDisc0.Draw()
f = ROOT.TF1("f",ROOT.f1FlavourFractions,0.,1.,3)
ROOT.setHistograms(hDisc0,hDiscC,hDiscB)

norm = 1000.
cFraction = 0.1
bFraction = 0.4
for i in range(3):
    f.SetParameters(norm,bFraction,cFraction)
    hD = hFile.Get("hDataTarget").Clone()
    for j in range(hD.GetNbinsX()):
	ibin = j + 1
	ed = hD.GetBinError(ibin)
	e0 = (1.-cFraction-bFraction)*hDisc0.GetBinError(ibin)
	ec = cFraction*hDiscC.GetBinError(ibin)
	eb = bFraction*hDiscB.GetBinError(ibin)
        ed = sqrt(ed*ed+e0*e0+ec*ec+eb*eb)
	hD.SetBinError(ibin,ed)
    hD.Fit(f)
    norm = f.GetParameter(0)
    cFraction = f.GetParameter(1)
    bFraction = f.GetParameter(2)
   	
hD.SetMarkerStyle(20)
hD0s = hDisc0.Clone("hD0s")
hDCs = hDiscC.Clone("hDCs")
hDCs.SetLineColor(4)
hDBs = hDiscB.Clone("hDBs")
hDBs.SetLineColor(2)
hD0s.Scale(f.GetParameter(0)*(1-f.GetParameter(1)-f.GetParameter(2)))
hDCs.Scale(f.GetParameter(0)*f.GetParameter(1))
hDBs.Scale(f.GetParameter(0)*f.GetParameter(2))
hmax = hD.GetMaximum()
if hD0s.GetMaximum()>hmax:  hmax = hD0s.GetMaximum()
if hDCs.GetMaximum()>hmax:  hmax = hDCs.GetMaximum()
if hDBs.GetMaximum()>hmax:  hmax = hDBs.GetMaximum()
hD.SetMaximum(hmax*1.05)
hD.Draw()
hD0s.Draw("same")
hD0s.Draw("same hist")
hDCs.Draw("same hist")
hDBs.Draw("same hist")
