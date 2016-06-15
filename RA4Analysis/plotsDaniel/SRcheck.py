import ROOT
import os, sys, copy

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import getVarValue, getChain, deltaPhi
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *

from Workspace.RA4Analysis.helpers import *
from rCShelpers import *


binning=[30,0,1500]

#prepresel = 'singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80'
prepresel = 'singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80'

bVar = 'nBJetMediumCSV30'

deltaPhiCut=0.75
varstring='deltaPhi_Wl'
vartex = '#Delta#Phi(W,l)'
twoBin=[0,deltaPhiCut,3.2]
lepSel = 'hard'

nBtagReg=[(0,0),(1,1)]#,(2,-1)]
nJetReg=[(5,5),(6,7),(8,-1)]
stReg=[(250,350),(350,450),(450,-1)]
htReg=[(500,750),(750,1000),(1000,-1)]

targetLumi = 10. #fb^-1
sampleLumi = 3. #fb^-1
threshold = 1.


scaleFactor = targetLumi/sampleLumi

#Load the Background Chain
#cBkg = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel], DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')
cBkg = getChain([TTJets_combined_25ns, WJetsHTToLNu_25ns, singleTop_25ns, DY_25ns, TTV_25ns],histname='')

#signal1 = getChain(T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],histname='')
#signal2 = getChain(T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel],histname='')
#signal3 = getChain(T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],histname='')

signal1 = getChain(T5qqqqVV_mGluino_1000To1075_mLSP_1To950[1000][700], histname='')
signal2 = getChain(T5qqqqVV_mGluino_1200To1275_mLSP_1to1150[1200][800],histname='')
signal3 = getChain(T5qqqqVV_mGluino_1400To1550_mLSP_1To1275[1500][100],histname='')



bkgH = ROOT.TH1F('bkgH','',len(twoBin)-1, array('d', twoBin))
bkgWSBH = ROOT.TH1F('bkgWSBH','',len(twoBin)-1, array('d', twoBin))
bkgTTSBH = ROOT.TH1F('bkgTTSBH','',len(twoBin)-1, array('d', twoBin))

sig1H = ROOT.TH1F('sig1H','',len(twoBin)-1, array('d', twoBin))
sig2H = ROOT.TH1F('sig2H','',len(twoBin)-1, array('d', twoBin))
sig3H = ROOT.TH1F('sig3H','',len(twoBin)-1, array('d', twoBin))

weight = 'weight*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*TopPtWeight*0.94'
signalWeight = 'weight*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*0.94'

bins = []
yields = {}

#Get the yields
for njb in nJetReg:
  yields[njb] = {}
  for htb in htReg:
    yields[njb][htb] = {}
    for stb in stReg:
      name, cut = nameAndCut(stb, htb, njb, btb=(0,0), presel=prepresel, btagVar=bVar)
      n, WSBcut = nameAndCut(stb, htb, (3,4), btb=(0,0), presel=prepresel, btagVar=bVar)
      n, TTSBcut = nameAndCut(stb, htb, (4,5), btb=(1,1), presel=prepresel, btagVar=bVar)
      cBkg.Draw(varstring+'>>bkgH','('+cut+')*'+weight)
      cBkg.Draw(varstring+'>>bkgWSBH','('+WSBcut+')*'+weight)
      cBkg.Draw(varstring+'>>bkgTTSBH','('+TTSBcut+')*'+weight)
      signal1.Draw(varstring+'>>sig1H','('+cut+')*'+signalWeight)
      signal2.Draw(varstring+'>>sig2H','('+cut+')*'+signalWeight)
      signal3.Draw(varstring+'>>sig3H','('+cut+')*'+signalWeight)
      yBkg = bkgH.GetBinContent(2)
      yBkgCR = bkgH.GetBinContent(1)
      yWSB_SR = bkgWSBH.GetBinContent(2)
      yWSB_CR = bkgWSBH.GetBinContent(1)
      yTTSB_SR = bkgTTSBH.GetBinContent(2)
      yTTSB_CR = bkgTTSBH.GetBinContent(1)
      yS1 = sig1H.GetBinContent(2)
      yS2 = sig2H.GetBinContent(2)
      yS3 = sig3H.GetBinContent(2)
      rd = {'Jets':njb, 'HT':htb, 'ST':stb, 'Bkg':yBkg, 'BkgCR':yBkgCR, 'Model1':yS1, 'Model2':yS2, 'Model3':yS3, 'WSB_SR':yWSB_SR, 'WSB_CR':yWSB_CR, 'TTSB_SR':yTTSB_SR, 'TTSB_CR':yTTSB_CR}
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
  yBkgCR = 0.
  #bin = [njb]
  for htb in reversed(htReg):
    regions[njb][htb] = {}
    #bin.append(htb)
    bin = []
    yS1 = 0.
    yS2 = 0.
    yS3 = 0.
    yBkg = 0.
    yBkgCR = 0.
    bin = []
    for stb in reversed(stReg):
      flag = False
      yS1 += yields[njb][htb][stb]['Model1']*scaleFactor
      yS2 += yields[njb][htb][stb]['Model2']*scaleFactor
      yS3 += yields[njb][htb][stb]['Model3']*scaleFactor
      yBkg += yields[njb][htb][stb]['Bkg']*scaleFactor
      yBkgCR += yields[njb][htb][stb]['BkgCR']*scaleFactor
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
        yieldPklST.append({'nJet':njb, 'HT':htb, 'ST':newStBin, 'B':yBkg, 'S1000':yS1, 'S1200':yS2, 'S1500':yS3, 'BCR':yBkgCR})
        bin = []
        yS1 = 0.
        yS2 = 0.
        yS3 = 0.
        yBkg = 0.
        yBkgCR = 0.
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
      yieldPklST.append({'nJet':njb, 'HT':htb, 'ST':newStBin, 'B':yBkg, 'S1000':yS1, 'S1200':yS2, 'S1500':yS3, 'BCR':yBkgCR})


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
  yBkgCR = 0.
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
    yBkgCR = 0.
    
    yWSB_SR = 0.
    yWSB_CR = 0.
    yTTSB_SR = 0.
    yTTSB_CR = 0.
    bin = []
    for htb in reversed(htReg):
      flag = False
      yS1 += yields[njb][htb][stb]['Model1']*scaleFactor
      yS2 += yields[njb][htb][stb]['Model2']*scaleFactor
      yS3 += yields[njb][htb][stb]['Model3']*scaleFactor
      yBkg += yields[njb][htb][stb]['Bkg']*scaleFactor
      yBkgCR += yields[njb][htb][stb]['BkgCR']*scaleFactor
      
      yWSB_SR += yields[njb][htb][stb]['WSB_SR']*scaleFactor
      yWSB_CR += yields[njb][htb][stb]['WSB_CR']*scaleFactor
      yTTSB_SR += yields[njb][htb][stb]['TTSB_SR']*scaleFactor
      yTTSB_CR += yields[njb][htb][stb]['TTSB_CR']*scaleFactor

      bin.append(htb)
      if yS1>threshold or yS2>threshold or yS3>threshold:
        flag = True
        lowerBound = bin[0][0]
        upperBound = bin [0][1]
        for sts in bin:
          if sts[0] < lowerBound: lowerBound = sts[0]
          if sts[1] > upperBound and upperBound > 0.: upperBound = sts[1]
        newHtBin = (lowerBound, upperBound)
        newDict = {'nJet':njb, 'HT':newHtBin, 'ST':stb, 'B':yBkg, 'S1000':yS1, 'S1200':yS2, 'S1500':yS3, 'BCR':yBkgCR, 'FOM_S10':yS1/sqrt(yBkg+k*yS1), 'FOM_S12':yS2/sqrt(yBkg+k*yS2), 'FOM_S15':yS3/sqrt(yBkg+k*yS3), 'WSB_SR':yWSB_SR, 'WSB_CR':yWSB_CR, 'TTSB_SR':yTTSB_SR, 'TTSB_CR':yTTSB_CR}
        regionsHTcomb[njb][stb][newHtBin] = newDict
        signalRegions[njb][stb][newHtBin] = {'deltaPhi': 1.0}
        if yWSB_SR < 2: print 'WSB problematic!'
        if yTTSB_SR < 2: print 'TTSB problematic!'
        k = 0.3
        yieldPklHT.append(newDict)
        bin = []
        yS1 = 0.
        yS2 = 0.
        yS3 = 0.
        yBkg = 0.
        yBkgCR = 0.
        yWSB_SR = 0.
        yWSB_CR = 0.
        yTTSB_SR = 0.
        yTTSB_CR = 0.

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
      k = 0.3
      yieldPklHT.append({'nJet':njb, 'HT':newHtBin, 'ST':stb, 'B':yBkg, 'S1000':yS1, 'S1200':yS2, 'S1500':yS3, 'BCR':yBkgCR, 'FOM_S10':yS1/sqrt(yBkg+k*yS1), 'FOM_S12':yS2/sqrt(yBkg+k*yS2), 'FOM_S15':yS3/sqrt(yBkg+k*yS3)})


