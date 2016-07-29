import ROOT
import sys,os
from CanvasUtilities import *

#ROOT.gStyle.SetOptStat(0)
fncolor = os.path.expandvars("$WORK/susy/CMSSW_7_4_14/src/Workspace/HEPHYPythonTools/scripts/root/useNiceColorPalette.C")
ROOT.gROOT.ProcessLine(".L "+fncolor)
ROOT.useNiceColorPalette()


tf1 = ROOT.TFile(sys.argv[1])
tf2 = ROOT.TFile(sys.argv[2])

histos1 = getObjectsFromDirectory(tf1,ROOT.TH2.Class())
histos2 = getObjectsFromDirectory(tf2,ROOT.TH2.Class())

histosIn = { }
for h in histos1:
    n = h.GetName()
    assert not n in histosIn
    histosIn[n] = [ h ]
for h in histos2:
    n = h.GetName()
    assert  n in histosIn
    histosIn[n].append(h)

ROOT.gROOT.cd()
histosOut = [ ]
for n in histosIn:
    h1,h2 = histosIn[n]
    h = h1.Clone()
    h.Divide(h2)
    h.SetMinimum(0.5)
    h.SetMaximum(2.)
    histosOut.append(h)

cnvs = [ ]
histos1D = [ ]
for h in histosOut:
    n = h.GetName()
    cn = "c_"+n
#    cnvs.append(ROOT.TCanvas(cn,cn))
#    h.Draw("zcol")
##    cnvs[-1].SetLogz(1)
#    cnvs[-1].Update()
    h1 = ROOT.TH1F(n+"1D",n+"1D",100,0.,2.5)
    histos1D.append(h1)
    for ix in range(h.GetXaxis().GetNbins()):
        for iy in range(h.GetYaxis().GetNbins()):
            v = h.GetBinContent(ix,iy)
            if v>1.e-6:
                h1.Fill(v)
    cn = "c_"+n+"1D"
    cnvs.append(ROOT.TCanvas(cn,cn))
    h1.Draw()
    cnvs[-1].Update()

        
