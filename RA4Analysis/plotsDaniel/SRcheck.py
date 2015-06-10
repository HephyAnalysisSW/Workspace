import ROOT
import os, sys, copy

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import getVarValue, getChain, deltaPhi
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.helpers import *
from rCShelpers import *


binning=[30,0,1500]

prepresel = 'singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80'

bVar = 'nBJetMediumCSV30'

deltaPhiCut=1.
varstring='deltaPhi_Wl'
vartex = '#Delta#Phi(W,l)'
twoBin=[0,deltaPhiCut,3.2]
lepSel = 'hard'

nBtagReg=[(0,0),(1,1)]#,(2,-1)]
nJetReg=[(5,5),(6,7),(8,-1)]
stReg=[(250,350),(350,450),(450,-1)]
htReg=[(500,750),(750,1000),(1000,1250),(1250,-1)]

targetLumi = 3. #fb^-1
sampleLumi = 4. #fb^-1
threshold = 1.


scaleFactor = targetLumi/sampleLumi

#Load the Background Chain
cBkg = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel], DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')
signal1 = getChain(T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],histname='')
signal2 = getChain(T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel],histname='')
signal3 = getChain(T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],histname='')

bkgH = ROOT.TH1F('bkgH','',len(twoBin)-1, array('d', twoBin))
sig1H = ROOT.TH1F('sig1H','',len(twoBin)-1, array('d', twoBin))
sig2H = ROOT.TH1F('sig2H','',len(twoBin)-1, array('d', twoBin))
sig3H = ROOT.TH1F('sig3H','',len(twoBin)-1, array('d', twoBin))

bins = []
yields = {}

#Get the yields
for njb in nJetReg:
  yields[njb] = {}
  for htb in htReg:
    yields[njb][htb] = {}
    for stb in stReg:
      name, cut = nameAndCut(stb, htb, njb, btb=(0,0), presel=prepresel, btagVar=bVar)
      cBkg.Draw(varstring+'>>bkgH','('+cut+')*weight')
      signal1.Draw(varstring+'>>sig1H','('+cut+')*weight')
      signal2.Draw(varstring+'>>sig2H','('+cut+')*weight')
      signal3.Draw(varstring+'>>sig3H','('+cut+')*weight')
      yBkg = bkgH.GetBinContent(2)
      yS1 = sig1H.GetBinContent(2)
      yS2 = sig2H.GetBinContent(2)
      yS3 = sig3H.GetBinContent(2)
      rd = {'Jets':njb, 'HT':htb, 'ST':stb, 'Bkg':yBkg, 'Model1':yS1, 'Model2':yS2, 'Model3':yS3}
      yields[njb][htb][stb] = rd
      bins.append(rd)
      print rd

#Reduce ST Bins
regions = {}
yieldPklST = []

for njb in reversed(nJetReg):
  regions[njb] = {}
  yS1 = 0.
  yS2 = 0.
  yS3 = 0.
  yBkg = 0.
  #bin = [njb]
  for htb in reversed(htReg):
    regions[njb][htb] = {}
    #bin.append(htb)
    bin = []
    yS1 = 0.
    yS2 = 0.
    yS3 = 0.
    yBkg = 0.
    bin = []
    for stb in reversed(stReg):
      flag = False
      yS1 += yields[njb][htb][stb]['Model1']*scaleFactor
      yS2 += yields[njb][htb][stb]['Model2']*scaleFactor
      yS3 += yields[njb][htb][stb]['Model3']*scaleFactor
      yBkg += yields[njb][htb][stb]['Bkg']*scaleFactor
      bin.append(stb)
      if yS1>threshold or yS2>threshold or yS3>threshold:
        flag = True
        lowerBound = bin[0][0]
        upperBound = bin [0][1]
        for sts in bin:
          if sts[0] < lowerBound: lowerBound = sts[0]
          if sts[1] > upperBound and upperBound > 0.: upperBound = sts[1]
        newStBin = (lowerBound, upperBound)
        regions[njb][htb][newStBin] = {'Jets':njb, 'HT':htb, 'ST':newStBin, 'Bkg':yBkg, 'Model1':yS1, 'Model2':yS2, 'Model3':yS3}
        yieldPklST.append({'nJet':njb, 'HT':htb, 'ST':newStBin, 'B':yBkg, 'S1000':yS1, 'S1200':yS2, 'S1500':yS3})
        bin = []
        yS1 = 0.
        yS2 = 0.
        yS3 = 0.
        yBkg = 0.
      #else:
      #  flag = False
    if not flag:
      lowerBound = bin[0][0]
      upperBound = bin [0][1]
      for sts in bin:
        if sts[0] < lowerBound: lowerBound = sts[0]
        if sts[1] > upperBound and upperBound > 0.: upperBound = sts[1]
      newStBin = (lowerBound, upperBound)
      regions[njb][htb][newStBin] = {'Jets':njb, 'HT':htb, 'ST':newStBin, 'Bkg':yBkg, 'Model1':yS1, 'Model2':yS2, 'Model3':yS3}
      yieldPklST.append({'nJet':njb, 'HT':htb, 'ST':newStBin, 'B':yBkg, 'S1000':yS1, 'S1200':yS2, 'S1500':yS3})


#Reduce HT Bins
regionsHTcomb = {}
yieldPklHT = []
signalRegions = {}

for njb in reversed(nJetReg):
  regionsHTcomb[njb] = {}
  signalRegions[njb] = {}
  yS1 = 0.
  yS2 = 0.
  yS3 = 0.
  yBkg = 0.
  #bin = [njb]
  for stb in reversed(stReg):
    regionsHTcomb[njb][stb] = {}
    signalRegions[njb][stb] = {}
    #bin.append(htb)
    bin = []
    yS1 = 0.
    yS2 = 0.
    yS3 = 0.
    yBkg = 0.
    bin = []
    for htb in reversed(htReg):
      flag = False
      yS1 += yields[njb][htb][stb]['Model1']*scaleFactor
      yS2 += yields[njb][htb][stb]['Model2']*scaleFactor
      yS3 += yields[njb][htb][stb]['Model3']*scaleFactor
      yBkg += yields[njb][htb][stb]['Bkg']*scaleFactor
      bin.append(htb)
      if yS1>threshold or yS2>threshold or yS3>threshold:
        flag = True
        lowerBound = bin[0][0]
        upperBound = bin [0][1]
        for sts in bin:
          if sts[0] < lowerBound: lowerBound = sts[0]
          if sts[1] > upperBound and upperBound > 0.: upperBound = sts[1]
        newHtBin = (lowerBound, upperBound)
        regionsHTcomb[njb][stb][newHtBin] = {'Jets':njb, 'ST':stb, 'HT':newHtBin, 'Bkg':yBkg, 'Model1':yS1, 'Model2':yS2, 'Model3':yS3}
        signalRegions[njb][stb][newHtBin] = {'deltaPhi': 1.0}
        yieldPklHT.append({'nJet':njb, 'HT':newHtBin, 'ST':stb, 'B':yBkg, 'S1000':yS1, 'S1200':yS2, 'S1500':yS3})
        bin = []
        yS1 = 0.
        yS2 = 0.
        yS3 = 0.
        yBkg = 0.
      #else:
      #  flag = False
    if not flag:
      lowerBound = bin[0][0]
      upperBound = bin [0][1]
      for sts in bin:
        if sts[0] < lowerBound: lowerBound = sts[0]
        if sts[1] > upperBound and upperBound > 0.: upperBound = sts[1]
      newHtBin = (lowerBound, upperBound)
      regionsHTcomb[njb][stb][newHtBin] = {'Jets':njb, 'ST':stb, 'HT':newHtBin, 'Bkg':yBkg, 'Model1':yS1, 'Model2':yS2, 'Model3':yS3}
      signalRegions[njb][stb][newHtBin] = {'deltaPhi': 1.0}
      yieldPklHT.append({'nJet':njb, 'HT':newHtBin, 'ST':stb, 'B':yBkg, 'S1000':yS1, 'S1200':yS2, 'S1500':yS3})


