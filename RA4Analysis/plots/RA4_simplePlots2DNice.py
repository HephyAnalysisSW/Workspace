import ROOT
from array import array
from math import *
import os, copy

from simplePlotsCommon import *
import xsec
small = False

from defaultMuSamples import *

presel = "pf-4j30"
subdir = "/pngMu2D/"
chainstring = "empty"
commoncf = "(0)"
prefix="empty_"

#infilename = "/afs/hephy.at/user/s/schoefbeck/www/pngMu2D/pf-4j30_mc_htVSkinMetSig.root"
infilename = "/afs/hephy.at/user/s/schoefbeck/www/pngEle2D/pf-4j30_mc_htVSkinMetSig.root"
file = ROOT.TFile(infilename)
canv=file.Get("ROOT.c1")

ROOT.gStyle.SetOptStat(0)
ROOT.setTDRStyle()
#ROOT.gStyle.SetPadRightMargin(0.10);
if type(ROOT.tdrStyle)!=type(ROOT.gStyle):
  del ROOT.tdrStyle
  ROOT.setTDRStyle()

ROOT.tdrStyle.SetPadRightMargin(0.16)
ROOT.gROOT.ProcessLine(".L ../../EarlyMETAnalysis/aclic/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)
canv.Draw()
drawExclusionRegions(ROOT.ht_vs_kinMetSig, [300,650,650], [2.5,5.5,5.5])
lines = [[0.4,0.27,"A"],[0.7,0.27,"B"],[0.4,0.7,"C"],[0.7,0.7,"D"]]
#drawExclusionRegions(ROOT.ht_vs_kinMetSig, [300,350,400], [2.5,4.5,4.5])
#lines = [[0.33,0.25,"A"],[0.7,0.25,"B"],[0.33,0.7,"C"],[0.7,0.7,"D"]]

latex = ROOT.TLatex();
latex.SetNDC();
latex.SetTextSize(0.07);

latex.SetTextAlign(11); # align right

for line in lines:
  stuff.append(latex.DrawLatex(line[0],line[1],line[2]))
#  var.data_histo.GetYaxis().SetLabelSize(0.04)
#  var.data_histo.GetXaxis().SetLabelSize(0.04)
#  var.data_histo.GetZaxis().SetRangeUser(10**(-3.9), .9)
#data_htVSkinMetSig.data_histo.GetZaxis().SetRangeUser(10**(-2), 9)

