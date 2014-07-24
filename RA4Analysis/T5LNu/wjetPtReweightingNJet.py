import ROOT
from array import array
from math import *
import os, copy, sys
from localConfig import localPlotDir
ROOT.TH1F().SetDefaultSumw2()
from helpers import wGenPt, wRecoPt

from Workspace.HEPHYPythonTools.helpers import getObjFromFile, passPUJetID, getISRweight, minDeltaRLeptonJets#, findClosestJet, invMass 
from helpers import nameAndCut
from Workspace.RA4Analysis.simplePlotsCommon import *
#from monoJetFuncs import *
#from monoJetEventShapeVars import circularity2D, foxWolframMoments, thrust

from Workspace.HEPHYPythonTools.xsec import xsec
small = False

targetLumi = 19700.

from defaultConvertedTuples import * 

wjetsSample = wJetsHT150v2 
allSamples = [wjetsSample]

allVars=[]
allStacks=[]

## plots for studying preselection 
minimum=10**(-2.5)

chmode = "copy"
presel = "refSelNoNJet"
ver = "v5"
preprefix = ver
addSignals = True
normalizeToData = False
normalizeSignalToMCSum = False

#if region == "signal3j":
#  #isrjet>350, met>250, mT<70
#  additionalCut = "(ht>750&&type1phiMet>350)"

subdir = "/pngT5LNu_wGenPTRW/"

chainstring = "Events"
commoncf = "(0)"
prefix="empty_"
if presel == "refSelNoNJet":
  commoncf="ht>400&&nTightMuons+nTightElectrons==1&&nbtags==0&&type1phiMet>150"

prefix = "T5Lnu_"+preprefix+"_"+presel+"_"+chmode+"_"

def getT5LNu(mgl, mn, color = ROOT.kBlue):
  res = {} 
  res["dirname"] = ["/data/schoef/convertedTuples_v22/copy/"]
  res["bins"] = ["T5LNu_"+str(mgl)+"_"+str(mn)]
  res["hasWeight"] = True
  res["weight"] = "weight"
  res["color"] = color
  res["name"] = res["bins"][0]
  return res

signals=[]
#signals=[getT5LNu(1000,100, ROOT.kBlue + 3), getT5LNu(1000, 600, ROOT.kRed + 3)]
#if addSignals:
#  allSamples += signals

for sample in allSamples:
  sample["Chain"] = chainstring
  sample["dirname"] = "/data/schoef/convertedTuples_v22/"+chmode+"/"
for sample in allSamples:
  sample["weight"] = "puWeight"

def getStack(varstring, binning, cutstring, signals, varfunc = None, additionalCutFunc = "", reweightFunc=None):

  MC_WJETS                     = variable(varstring,binning, cutstring, additionalCutFunc=additionalCutFunc, binningIsExplicit=True) 
  MC_WJETS.sample              = wjetsSample
  MC_WJETS.legendText          = "W + Jets"
  MC_WJETS.style               = "f0"
  MC_WJETS.color               = ROOT.kYellow
  MC_WJETS.add                 = []
  res = [MC_WJETS]
  for v in res:
    v.legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
  getLinesForStack(res, targetLumi)
  if varfunc:
    for var in res:
      var.varfunc = varfunc
  if reweightFunc:
    for var in res:
      var.reweightVar = reweightFunc
  return res

htBins =  [[400, 750], [500, 750], [750, -1]]
metBins = [[150, 350], [350, -1] ]
njetCRBins = [[2,2], [3,3], [2,3]]
njetSRBins = [[4,4], [5,-1], [4,-1]]

#htBins =  [[750, -1]]
#metBins = [[350, -1] ]
#njetCRBins = [[3,3], [2,3]]
#njetSRBins = [[4,4], [4,-1]]

binningWPt = range(0,1000,100)+[1100,2000]
wGenPt_stacks={} 
wPlusGenPt_stacks={} 
wMinusGenPt_stacks={} 
wRecoPt_stacks={} 
wPlusRecoPt_stacks={} 
wMinusRecoPt_stacks={} 
for metb in metBins:
  for htb in htBins:
    for njetb in njetCRBins+njetSRBins:
      for pdgSign in ['', 'pos','neg']:
        name, cut = nameAndCut(metb, htb, njetb, pdgSign) 
        print name, cut

        wGenPt_stacks[name] = getStack(":XXX;gen. p_{T,W} (GeV);Number of Events", binningWPt, cut, signals, varfunc = wGenPt)
        wGenPt_stacks[name][0].addOverFlowBin = "upper"
        allStacks.append(wGenPt_stacks[name])

        wRecoPt_stacks[name] = getStack(":XXX;reco p_{T,W} (GeV);Number of Events", binningWPt, cut, signals, varfunc = wRecoPt)
        wRecoPt_stacks[name][0].addOverFlowBin = "upper"
        allStacks.append(wRecoPt_stacks[name])

execfile("../../RA4Analysis/plots/simplePlotsLoopKernel.py")


wGenPt_rwHisto={} 
wRecoPt_rwHisto={} 
for metb in metBins:
  for htb in htBins:
#  for htb in [ [750, -1]]:
    for njetSRb in njetSRBins:
      for pdgSign in ['', 'pos','neg']:
        bnameSR, cut = nameAndCut(metb, htb, njetSRb, pdgSign) 
        h_wGenPt = wGenPt_stacks[bnameSR][0].data_histo.Clone()
        h_wGenPt.Scale(1./h_wGenPt.Integral())
        h_wRecoPt = wRecoPt_stacks[bnameSR][0].data_histo.Clone()
        h_wRecoPt.Scale(1./h_wRecoPt.Integral())
        for njetb in njetCRBins:
          bnameCR, cut = nameAndCut(metb, htb, njetb, pdgSign) 
    #    for njetb in [[2,2]]:
          namePostFix='_to_njet'+str(njetSRb[0])
          if len(njetSRb)>1 and njetSRb[1]>0:
            namePostFix+='-'+str(njetSRb[1])
          h_wGenPtnj = wGenPt_stacks[bnameCR][0].data_histo.Clone()
          h_wGenPtnj.Scale(1./h_wGenPtnj.Integral())
          wGenPt_rwHisto[bnameCR+namePostFix] = h_wGenPt.Clone()
          wGenPt_rwHisto[bnameCR+namePostFix].Divide(h_wGenPtnj)
          h_wRecoPtnj = wRecoPt_stacks[bnameCR][0].data_histo.Clone()
          h_wRecoPtnj.Scale(1./h_wRecoPtnj.Integral())
          wRecoPt_rwHisto[bnameCR+namePostFix] = h_wRecoPt.Clone()
          wRecoPt_rwHisto[bnameCR+namePostFix].Divide(h_wRecoPtnj)


for name in wGenPt_rwHisto.keys():
  c1 = ROOT.TCanvas()
  wGenPt_rwHisto[name].Draw()
  c1.Print(localPlotDir+'/'+subdir+prefix+name+"_wGenPt_rwHisto.png")
  c1.Print(localPlotDir+'/'+subdir+prefix+name+"_wGenPt_rwHisto.pdf")
  c1.Print(localPlotDir+'/'+subdir+prefix+name+"_wGenPt_rwHisto.root")
  wRecoPt_rwHisto[name].Draw()
  c1.Print(localPlotDir+'/'+subdir+prefix+name+"_wRecoPt_rwHisto.png")
  c1.Print(localPlotDir+'/'+subdir+prefix+name+"_wRecoPt_rwHisto.pdf")
  c1.Print(localPlotDir+'/'+subdir+prefix+name+"_wRecoPt_rwHisto.root")

for name in wGenPt_stacks.keys():
  drawNMStacks(1,1,[wGenPt_stacks[name]],             subdir+prefix+name+'_'+"wGenPt", False)
  drawNMStacks(1,1,[wRecoPt_stacks[name]],             subdir+prefix+name+'_'+"wRecoPt", False)


f = ROOT.TFile('/afs/hephy.at/user/s/schoefbeck/www/'+subdir+prefix+'reweightingHistos.root', 'recreate')
for nPrefix, s in [\
   ['genPt', wGenPt_rwHisto], ['recoPt', wRecoPt_rwHisto]]:
  for k in s.keys(): 
    h = s[k].Clone(nPrefix+'_'+k)
    h.Write()

f.Close()
