from ROOT import *
import sys
from DataFormats.FWLite import Events, Handle
from math import *
import array


sd = '.'
if len(sys.argv)>1: sd = sys.argv[1]
f = TFile(sd+"/out.root")

def drawhh(hname):
    exec('hh{0}1.Draw()'.format(hname))
    exec('hh{0}2.SetLineColor(2)'.format(hname))
    exec('hh{0}2.Draw("same")'.format(hname))
    exec('hh{0}3.SetLineColor(3)'.format(hname))
    exec('hh{0}3.Draw("same")'.format(hname))
    gPad.Update()

eff = TEfficiency(hhrjpt1,hhrjpt1)
def turnon(hn1,hn2,op=""):
    global eff
    exec('eff.SetPassedHistogram(hh{0},"f")'.format(hn1))
    exec('eff.SetTotalHistogram(hh{0},"f")'.format(hn2))
    eff.GetEfficiency(100)
    eff.Draw(op)
    gPad.SetGrid(1,1)
    gPad.Update()

gDirectory.ls()
