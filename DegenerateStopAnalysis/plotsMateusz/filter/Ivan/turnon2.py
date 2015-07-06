from ROOT import *
import sys


effl = []
f = TFile("out100110/out.root")
hh1 = f.Get("hhrjpt2")
hh2 = f.Get("hhrjpt1")
hh3 = f.Get("hhrjpt3")
hh4 = f.Get("hhrjpt4")
effl.append(TEfficiency(hh1,hh2))
effl.append(TEfficiency(hh3,hh4))
    
op = ""
for i,eff in enumerate(effl):
    print i
    eff.SetMarkerColor(i+3)
    eff.SetMarkerStyle(20+i+2)
    eff.SetLineColor(i+3)
    eff.Draw(op)
    op = "same"
    
gPad.SetGrid(1,1)
gPad.Update()
