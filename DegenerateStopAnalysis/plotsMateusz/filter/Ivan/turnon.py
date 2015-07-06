from ROOT import *
import sys


effl = []
for sd in ["out7090","out90100","out100110"]:
    f = TFile(sd+"/out.root")
    hh1 = f.Get("hhrmet3")
    hh2 = f.Get("hhrmet2")
    effl.append(TEfficiency(hh1,hh2))
    
op = ""
for i,eff in enumerate(effl):
    print i
    eff.SetMarkerColor(i+1)
    eff.SetMarkerStyle(20+i)
    eff.SetLineColor(i+1)
    eff.Draw(op)
    op = "same"
    
gPad.SetGrid(1,1)
gPad.Update()
