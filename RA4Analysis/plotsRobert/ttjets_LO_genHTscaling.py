import ROOT
from array import array
from math import *
import os, copy, sys

ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()

from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks
import Workspace.HEPHYPythonTools.xsec as xsec
from Workspace.RA4Analysis.helpers import *

from draw_helpers import *

from Workspace.RA4Analysis.cmgTuples_Spring15_25ns import TTJets_LO_25ns,  TTJets_LO_HT600to800_25ns, TTJets_LO_HT800to1200_25ns, TTJets_LO_HT1200to2500_25ns, TTJets_LO_HT2500toInf_25ns
ROOT_colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kCyan]
samples=[TTJets_LO_25ns,  TTJets_LO_HT600to800_25ns, TTJets_LO_HT800to1200_25ns, TTJets_LO_HT1200to2500_25ns, TTJets_LO_HT2500toInf_25ns]

lumi = 1000

for s in samples:
  cs=getChunks(s)
  s['chain'] = ROOT.TChain('tree')
  for c in cs[0]:
    s['chain'].Add(c['file'])
  s['weight'] = lumi*xsec.xsec[s['dbsName']]/float(cs[1])
  print "Sample %s has %i chunks and %i events and weight %f"%(s['name'], len(cs[0]), s['chain'].GetEntries(), s['weight'])

for i, s in enumerate(samples):
  s['h'] = ROOT.TH1F('lheHTIncoming_'+s['name'],'lheHTIncoming',40,0,4000)
  s['h'].SetLineColor(ROOT_colors[i])
  s['h'].SetMarkerStyle(0)
  s['h'].SetMarkerSize(0)
  s['h'].SetMarkerColor(ROOT_colors[i])

for i, s in enumerate(samples):
  s['chain'].Draw("lheHTIncoming>>lheHTIncoming_"+s['name'],str(s['weight']))

c1 = ROOT.TCanvas()
for i, s in enumerate(samples):
  if i==0:
    s['h'].Draw('h')
    c1.SetLogy()
  else: 
    s['h'].Draw('hsame')


c1.Print('/afs/hephy.at/user/r/rschoefbeck/www/etc/lheIncoming.png')
