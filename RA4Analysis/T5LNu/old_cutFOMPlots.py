import os,sys,ROOT,pickle
from math import sqrt, pi
from localConfig import afsUser, nfsUser, localPlotDir
import operator
for path in [os.path.abspath(p) for p in ['../../HEPHYCommonTools/mva', '../../HEPHYCommonTools/cardFileWriter/', '../../HEPHYCommonTools/python/', '../python/']]:
  if not path in sys.path:
      sys.path.insert(1, path)

ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/tdrstyle.C")
ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/useNiceColorPalette.C")

ROOT.gStyle.SetOptStat(0)
ROOT.setTDRStyle()
#ROOT.gStyle.SetPadRightMargin(0.10);
if type(ROOT.tdrStyle)!=type(ROOT.gStyle):
  del ROOT.tdrStyle
  ROOT.setTDRStyle()
ROOT.tdrStyle.SetPadRightMargin(0.18)
ROOT.useNiceColorPalette(255)

from nnAnalysisHelpers import getEList, getYieldFromChain
from xsec import xsec
import copy, sys
from defaultConvertedTuples import stop300lsp270FastSim, stop200lsp170g100FastSim, stop300lsp240g150FastSim
from defaultConvertedTuples import stop300lsp270FullSim, stop200lsp170g100FullSim, stop300lsp240g150FullSim
from defaultConvertedTuples import wJetsToLNu
from monoJetFuncs import softIsolatedMT, pmuboost3d
from helpers import htRatio 

colors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kOrange, ROOT.kMagenta]

cSignal = ROOT.TChain("Events")
cSignal.Add("/data/schoef/monoJetTuples_v3/copy/stop300lsp270FullSim/histo_stop300lsp270FullSim.root")

cBkg    = ROOT.TChain("Events")
cBkg.Add("/data/schoef/monoJetTuples_v3/copy/W1JetsToLNu/histo_W1JetsToLNu.root")
cBkg.Add("/data/schoef/monoJetTuples_v3/copy/W2JetsToLNu/histo_W2JetsToLNu.root")
cBkg.Add("/data/schoef/monoJetTuples_v3/copy/W3JetsToLNu/histo_W3JetsToLNu.root")
cBkg.Add("/data/schoef/monoJetTuples_v3/copy/W4JetsToLNu/histo_W4JetsToLNu.root")
cBkg.Add("/data/schoef/monoJetTuples_v3/copy/TTJets/histo_TTJets.root")
cBkg.Add("/data/schoef/monoJetTuples_v3/copy/singleTop/histo_singleTop.root")
cBkg.Add("/data/schoef/monoJetTuples_v3/copy/ZJetsInv/histo_ZJetsInv.root")
cBkg.Add("/data/schoef/monoJetTuples_v3/copy/DY/histo_DY.root")
cBkg.Add("/data/schoef/monoJetTuples_v3/copy/QCD20to600/histo_QCD20to600.root")
cBkg.Add("/data/schoef/monoJetTuples_v3/copy/QCD600to1000/histo_QCD600to1000.root")
cBkg.Add("/data/schoef/monoJetTuples_v3/copy/QCD1000/histo_QCD1000.root")

import numpy as np
from scipy import optimize

#mTFormula = 'sqrt(2.0*softIsolatedMuPt*type1phiMet*(1 - cos(softIsolatedMuPhi - type1phiMetphi)))'
mTFormula = 'softIsolatedMT'

cuts = [
  {'var':'type1phiMet',   'type':'lower', 'startVal': 500, 'minVal':250},\
#  {'var': absDMTFormula,  'type':'lower', 'startVal': 12.,  'minVal':10., 'maxVal':80.},\
#  {'var': mTFormula,      'type':'lower', 'startVal': 70,   'minVal':0.,  'maxVal':80},\
  {'var': mTFormula,      'type':'upper', 'startVal': 70,   'minVal':0.,  'maxVal':80  },\
# {'var': 'softIsolatedpmuboost3d',      'type':'upper', 'startVal': 40,   'minVal':0.,  'maxVal':40  },\
  {'var':'isrJetPt',      'type':'lower', 'startVal': 250., 'minVal':110., 'maxVal':500}
  ]



prepreprefix = 'cutFomPlot_'
presel = "isrJetPt>110&&isrJetBTBVetoPassed&&softIsolatedMuPt>5&&nHardElectrons+nHardMuons==0&&njet60<=2&&type1phiMet>150&&abs(softIsolatedMuEta)<1.5&&softIsolatedMT<70"
#presel = "isrJetPt>110&&isrJetBTBVetoPassed&&softIsolatedMuPt>5&&nHardElectrons+nHardMuons==0&&njet60<=2&&type1phiMet>150"
#  print "S:",yieldS, "B:",yieldB
postfix = 'FullSim_allBkgs'

def getFom(cutVals, relSysErr=0.05, lepCharge=0, verbose=False):
  cut = presel
  if lepCharge==-1:
    cut = presel+"&&softIsolatedMuPdg>0"
  if lepCharge==1:
    cut = presel+"&&softIsolatedMuPdg<0"
  cutFuncs = [] 
  for i, c in enumerate(cuts):
#    if (  c.has_key('minVal') and cutVals[i]<c['minVal']) or (c.has_key('maxVal') and cutVals[i]>c['maxVal']):
#      return -999
    if type(c['var'])==type(''):
      if c['type']=='lower':op='>='
      elif c['type']=='upper':op='<'
      else: 
        print "Problem in cut",c,"type not known:",c['type']
        return -999.

      cut+="&&"+c['var']+op+str(cutVals[i])
#    else:
#      print c, lambda chain: c['var'](chain)<c['maxVal'], cutFuncs 
#      if c['type']=='lower':  cutFuncs.append( lambda chain: c['var'](chain)>=c['minVal'] )
#      elif c['type']=='upper':cutFuncs.append( lambda chain: c['var'](chain)<c['maxVal'] )

  cutFunc = None
#  if len(cutFuncs)>0:
#    def cutfunc(chain):
#      for cf in cutFuncs:
#        if not cf(chain):return False
#      return True
#    cutFunc=cutfunc
#  print "Y",cutFuncs, cutFunc
      
  if verbose: print "cut:",cut
  yieldS = getYieldFromChain(cSignal, cut,  weight = "weight") 
  yieldB = getYieldFromChain(cBkg,    cut,  weight = "weight")
  if yieldB<=0 or yieldS<=0:
    return -999.
  fom = yieldS/sqrt(yieldB + (relSysErr*yieldB)**2)       
  if verbose: 
    sigeff = getYieldFromChain(cSignal, cut, weight = "weight")/getYieldFromChain(cSignal, presel, weight = "weight")
    bkgeff = getYieldFromChain(cBkg, cut, weight = "weight")/getYieldFromChain(cBkg, presel, weight = "weight")
    print "Values", cutVals,"fom:",fom,'bkgeff',bkgeff,'sigeff',sigeff, 'yieldB/S', yieldB, yieldS
  return fom

goodRes = []
c=0

metRange = [150,550,25]
#varRange  = [10,55,5]
#varName = "pmuboost3d"
varRange  = [40,90,10]
#varRange  = [0,70,10]
varName = "mT"
jptRange = [100,600,25]
def rootRange(pRange):
  return [int(pRange[1]-pRange[0])/pRange[2], pRange[0], pRange[1]]

vals =[250, 70, 425] 
fom = getFom(vals,relSysErr=0.05, lepCharge=-1,verbose=True)
print vals, fom

for varVal in range(*varRange):
  fomPlot = ROOT.TH2F("fom", "fom", *(rootRange(metRange)+rootRange(jptRange)))
  for met in range(*metRange):
    for jpt in range(*jptRange):
      vals = [met, varVal, jpt]
      fom = getFom(vals,relSysErr=0.05, lepCharge=-1,verbose=True)
      if fom>0.:
        fomPlot.Fill(met, jpt, fom)
      print vals, fom
  c1 = ROOT.TCanvas()
  fomPlot.GetZaxis().SetRangeUser(0.5, 2.3)
  fomPlot.Draw("COLZ")
  fomPlot.GetXaxis().SetTitle("MET cut")
  fomPlot.GetYaxis().SetTitle("isrJetPT cut")
  palette = fomPlot.GetListOfFunctions().FindObject("palette")
  if palette:
    palette.SetX1NDC(0.83)
    palette.SetX2NDC(0.87)
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngDegStop/fom_'+varName+'_above_'+str(varVal)+'_below_70_'+postfix+'.png')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngDegStop/fom_'+varName+'_below_'+str(varVal)+'_'+postfix+'.png')
  del palette
  del fomPlot
  del c1
  
