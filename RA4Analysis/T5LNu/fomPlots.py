import os,sys,ROOT,pickle
from array import array
from math import sqrt, pi
from localConfig import afsUser, nfsUser, localPlotDir
#import operator

ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/useNiceColorPalette.C")

ROOT.gStyle.SetOptStat(0)
ROOT.setTDRStyle()
#ROOT.gStyle.SetPadRightMargin(0.10);
if type(ROOT.tdrStyle)!=type(ROOT.gStyle):
  del ROOT.tdrStyle
  ROOT.setTDRStyle()
ROOT.tdrStyle.SetPadRightMargin(0.18)
ROOT.useNiceColorPalette(255)

from Workspace.HEPHYPythonTools.nnAnalysisHelpers import getEList, getYieldFromChain
from defaultConvertedTuples import *
import copy, sys

colors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kOrange, ROOT.kMagenta]

cSignal = ROOT.TChain("Events")
cSignal.Add("/data/schoef/convertedTuples_v22//copy/T5LNu_1200_100/histo_T5LNu_1200_100.root")

cBkg    = ROOT.TChain("Events")
cBkg.Add("/data/schoef/convertedTuples_v22//copy/WJetsHT150v2/histo_WJetsHT150v2_from*")
cBkg.Add("/data/schoef/convertedTuples_v22//copy/TTJetsPowHeg/histo_TTJetsPowHeg_from*")

prepreprefix = 'cutFomPlot_'
presel = "njets>=4&&ht>400&&nTightMuons+nTightElectrons==1&&nbtags==0&&type1phiMet>150.&&ht>750&&type1phiMet>300"

colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kGreen-4, ROOT.kMagenta, ROOT.kCyan, ROOT.kYellow+3, ROOT.kOrange, ROOT.kGreen + 3, ROOT.kRed - 7, ROOT.kGray + 2]

toBeStored = ["mT", 'htThrustLepSideRatio','cosDeltaPhi', 'weight', 'ht']
events={}
for t, chain, elist in [["sig", cSignal, getEList(cSignal, presel)], ['bkg', cBkg, getEList(cBkg, presel)]]:
  events[t]=[]
  n = elist.GetN()
  for i in range(n):
    if i%1000==0:
      print "At",i,"/",n
    chain.GetEntry(elist.GetEntry(i))
    ev = {}
    for var in toBeStored:
      ev[var] = chain.GetLeaf(var).GetValue()
    events[t].append(ev)

def getConstSoverSqrtBFunc(nPreB, nPreS, relSys, sigLevel):
  formula =  '1. + 0.5*1./(nPreB*sys**2) - sqrt(0.25/nPreB**2/sys**4 + nPreS**2*x**2/(sig*nPreB*sys)**2)'
  replacements = [['nPreB', str(nPreB)], ['nPreS', str(nPreS)], ['sys', str(relSys)], ['sig', str(sigLevel)]]
  for a,b in replacements:
    formula = formula.replace(a,b)
  print formula
  return ROOT.TF1('func', formula, 0, 1)

cutType = {'mT':'lower', 'cosDeltaPhi':'upper', 'htThrustLepSideRatio':'lower'}
nThresh=2000
zeros = array('d',[0. for i in range(nThresh)])
sigTot = len(events['sig'])
bkgTot = len(events['bkg'])
sigYield = sum(e['weight'] for e in events['sig'])
bkgYield = sum(e['weight'] for e in events['bkg'])
stuff=[]
for htThresh in [700, 750, 800, 900, 1000]:
#for htThresh in [700]:
  l = ROOT.TLegend(.16, .13, 0.63, 0.4)
  l.SetFillColor(ROOT.kWhite)
  l.SetShadowColor(ROOT.kWhite)
  l.SetBorderSize(1)
  c = ROOT.TCanvas()
  drawopt="al"
  for iv, v in enumerate(['htThrustLepSideRatio','cosDeltaPhi', 'mT']):
    vals = [e[v] for e in events['sig']+events['bkg']]
    minimum = min(vals)
    maximum = max(vals)
    thresholds = [ minimum + (maximum-minimum)*i/float(nThresh-1) for i in range(nThresh)]

    sigEff = []
    sigEffPlus = []
    sigEffMinus = []
    bkgEff = []
    bkgEffPlus = []
    bkgEffMinus = []
    for thresh in thresholds:
      if cutType[v]=='lower': 
        sigPassed = filter(lambda e: e[v]>thresh and e['ht']>htThresh, events['sig'])
        bkgPassed = filter(lambda e: e[v]>thresh and e['ht']>htThresh, events['bkg'])
      else:
        sigPassed = filter(lambda e: e[v]<thresh and e['ht']>htThresh, events['sig'])
        bkgPassed = filter(lambda e: e[v]<thresh and e['ht']>htThresh, events['bkg'])

      sigEff.append(len(sigPassed)/float(sigTot))
#      sigEffPlus.append(ROOT.TEfficiency.ClopperPearson(sigTot, len(sigPassed), 0.683,1))
#      sigEffMinus.append(ROOT.TEfficiency.ClopperPearson(sigTot, len(sigPassed), 0.683,0))
      bkgEff.append(1.-len(bkgPassed)/float(bkgTot))
#      bkgEffPlus.append(ROOT.TEfficiency.ClopperPearson(bkgTot, len(bkgPassed), 0.683,1))
#      bkgEffMinus.append(ROOT.TEfficiency.ClopperPearson(bkgTot, len(bkgPassed), 0.683,0))

    h= ROOT.TGraphErrors(nThresh, array('d', sigEff), array('d', bkgEff), zeros, zeros)

#  for i, [v, h] in enumerate(tGraphs):
    h.SetLineColor(colors[iv])
    h.GetXaxis().SetLabelSize(0.04)
    h.GetYaxis().SetLabelSize(0.04)
    h.SetMarkerColor(colors[iv])
    h.SetMarkerStyle(0)
    h.SetMarkerSize(0)
    h.GetXaxis().SetRangeUser(0., 0.4)
    h.GetYaxis().SetRangeUser(0.95,1.0)
    h.GetYaxis().SetTitle("Background rejection")
    h.GetXaxis().SetTitle("Signal efficiency")
    h.Draw(drawopt)
    stuff.append(h)
    drawopt="lsame"
    l.AddEntry(h, v, "LP")

  f2_20=getConstSoverSqrtBFunc(nPreB=bkgYield, nPreS=sigYield,relSys=0.2,sigLevel=2)
  f3_20=getConstSoverSqrtBFunc(nPreB=bkgYield, nPreS=sigYield,relSys=0.2,sigLevel=3)
  f2_50=getConstSoverSqrtBFunc(nPreB=bkgYield, nPreS=sigYield,relSys=0.5,sigLevel=2)
  f3_50=getConstSoverSqrtBFunc(nPreB=bkgYield, nPreS=sigYield,relSys=0.5,sigLevel=3)

  f2_20.SetLineStyle(ROOT.kDashed)
  f3_20.SetLineStyle(ROOT.kDashed)

  l.Draw()
  f2_50.SetLineWidth(1)
  f3_50.SetLineWidth(1)
  f2_20.SetLineWidth(1)
  f3_20.SetLineWidth(1)
  f2_50.Draw('same')
  f3_50.Draw('same')
  f2_20.Draw('same')
  f3_20.Draw('same')
#  del l, f2_20, f3_20, f2_50, f3_50
  c.Print('/afs/hephy.at/user/s/schoefbeck/www/pngT5LNu/fomComparison_presel_ht_'+str(htThresh)+'.png')

#
#def getConstSoverSqrtBFunc(nPreB, nPreS, relSys, sigLevel):
#  formula =  '1. + 0.5*1./(nPreB*sys**2) - sqrt(0.25/nPreB**2/sys**4 + nPreS**2*x**2/(sig*nPreB*sys)**2)'
#  replacements = [['nPreB', str(nPreB)], ['nPreS', str(nPreS)], ['sys', str(relSys)], ['sig', str(sigLevel)]]
#  for a,b in replacements:
#    formula = formula.replace(a,b)
#  print formula
#  return ROOT.TF1('func', formula, 0, 1)
#
#
#for d in data.values():
#  del d
#del data
#
#f2_05=getConstSoverSqrtBFunc(nPreB=nPreB, nPreS=nPreS,relSys=0.05,sigLevel=2)
#f3_05=getConstSoverSqrtBFunc(nPreB=nPreB, nPreS=nPreS,relSys=0.05,sigLevel=3)
#f2_10=getConstSoverSqrtBFunc(nPreB=nPreB, nPreS=nPreS,relSys=0.1,sigLevel=2)
#f3_10=getConstSoverSqrtBFunc(nPreB=nPreB, nPreS=nPreS,relSys=0.1,sigLevel=3)
#
#f2_10.SetLineStyle(ROOT.kDashed)
#f3_10.SetLineStyle(ROOT.kDashed)
#
#xRange = [0., 0.2]
#yRange = [0.975, 1.0]
#
#l = ROOT.TLegend(.16, .13, 0.63, 0.55)
#l.SetFillColor(ROOT.kWhite)
#l.SetShadowColor(ROOT.kWhite)
#l.SetBorderSize(1)
#c = ROOT.TCanvas()
#drawopt="al"
#for i,[h,n] in enumerate(reversed(toPlotTGraphErrors)):
#  h.SetLineColor(colors[i])
#  h.GetXaxis().SetLabelSize(0.04)
#  h.GetYaxis().SetLabelSize(0.04)
#  h.SetMarkerColor(colors[i])
#  h.SetMarkerStyle(0)
#  h.SetMarkerSize(0)
#  h.GetXaxis().SetRangeUser(*xRange)
#  h.GetYaxis().SetRangeUser(*yRange)
#  h.GetYaxis().SetTitle("Background rejection")
#  h.GetXaxis().SetTitle("Signal efficiency")
#  h.Draw(drawopt)
#  drawopt="lsame"
#  l.AddEntry(h, n, "LP")
#
#toPlotTGraphErrors[-1][0].Draw('lsame')
#
#l.Draw()
#
#f2_05.SetLineWidth(1)
#f3_05.SetLineWidth(1)
#f2_10.SetLineWidth(1)
#f3_10.SetLineWidth(1)
#f2_05.Draw('same')
#f3_05.Draw('same')
#f2_10.Draw('same')
#f3_10.Draw('same')
#c.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMJ/Comparison_'+prefix+'.png')
#
#for relSys in [0.05, 0.08]:
#  yRange = [0.5, 4.0]
#  l = ROOT.TLegend(.6, .6, 1.0, 1.0)
#  l.SetFillColor(ROOT.kWhite)
#  l.SetShadowColor(ROOT.kWhite)
#  l.SetBorderSize(1)
#  c = ROOT.TCanvas()
#  drawopt="al"
#  for i,[h,n] in enumerate(reversed(toPlotFOMTGraphErrors[relSys])):
#    h.SetLineColor(colors[i])
#    h.GetXaxis().SetLabelSize(0.04)
#    h.GetYaxis().SetLabelSize(0.04)
#    h.SetMarkerColor(colors[i])
#    h.SetMarkerStyle(0)
#    h.SetMarkerSize(0)
#    h.GetXaxis().SetRangeUser(*xRange)
#    h.GetYaxis().SetRangeUser(*yRange)
#    h.GetYaxis().SetTitle("FOM")
#    h.GetXaxis().SetTitle("Signal efficiency")
#    h.Draw(drawopt)
#    drawopt="lsame"
#    l.AddEntry(h, n, "LP")
#  toPlotFOMTGraphErrors[relSys][-1][0].Draw('lsame')
#  l.Draw()
#  c.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMJ/ComparisonFOM_'+str(relSys)+'_'+prefix+'.png')

