import ROOT
import os, sys, copy
import pickle

#ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
#ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_Spring15 import *

from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.eventShape import *

#presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&deltaPhi_Wl>1."
presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80"

lepSel='hard'
WJETS = getChain(WJetsHTToLNu[lepSel],histname='')

btb = (0,0)
st = (250,350)
ht = (1000,-1)
jet = (2,3)

#st = float(st)
#ht = float(ht)
#jet = int(jet)

def getW(c):
  para = ['pt','phi','eta','pdgId','motherId']
  genPartAll = [getObjDict(c, 'genPartAll_', para, j) for j in range(int(c.GetLeaf('ngenPartAll').GetValue()))]
  Neutrinos = []
  Leptons = []
  NeutrinosFromW = []
  LeptonsFromW = []
  for Neutrino in filterParticles(genPartAll, [12,14], 'pdgId'):
    Neutrinos.append(Neutrino)
  for NeutrinoFromW in filterParticles(Neutrinos, [24], 'motherId'):
    NeutrinosFromW.append(NeutrinoFromW)
  for Lepton in filterParticles(genPartAll, [11,13], 'pdgId'):
    Leptons.append(Lepton)
  for LeptonFromW in filterParticles(Leptons, [24], 'motherId'):
    LeptonsFromW.append(LeptonFromW)
  WMass = 0.
  if len(NeutrinosFromW)>0:
    if len(NeutrinosFromW)>1: print 'this should not have happened'
    if len(LeptonsFromW)>0:
      if len(LeptonsFromW)>1: print 'this should not have happened'
      LeptonPt = LeptonsFromW[0]['pt']
      LeptonPhi = LeptonsFromW[0]['phi']
      LeptonEta = LeptonsFromW[0]['eta']
      NeutrinoPt = NeutrinosFromW[0]['pt']
      NeutrinoPhi = NeutrinosFromW[0]['phi']
      NeutrinoEta = NeutrinosFromW[0]['eta']
      WMass = sqrt(2*LeptonPt*NeutrinoPt*(cosh(LeptonEta-NeutrinoEta)-cos(LeptonPhi-NeutrinoPhi)))
  return WMass


cutname, cut = nameAndCut(st, ht, jet, btb=btb, presel=presel, btagVar = 'nBJetMediumCSV30')
WJETS.Draw('>>eList',cut)
elist = ROOT.gDirectory.Get("eList")
number_events = elist.GetN()

print 'Scanning with cut:'
print cut
print
print 'Event * Lumi * Run'
print
for i in range(number_events):
  WJETS.GetEntry(elist.GetEntry(i))
  evt = getVarValue(WJETS, 'evt')
  lumi = getVarValue(WJETS,'lumi')
  run = getVarValue(WJETS,'run')
  weight = getVarValue(WJETS,"weight")
  recoST = getVarValue(WJETS,"st")
  jets = cmgGetJets(WJETS,ptMin=0.)
  leptonPt = getVarValue(WJETS,'leptonPt')
  leptonPhi = getVarValue(WJETS,'leptonPhi')
  genLepPt = getVarValue(WJETS,'genLep_pt')
  genLepPhi = getVarValue(WJETS,'genLep_phi')
  recoMet = getVarValue(WJETS,'met_pt')
  genMet = getVarValue(WJETS,'met_genPt')
  genMetPhi = getVarValue(WJETS,'met_genPhi')
  totalJetPtX=0.
  totalJetPtY=0.
  for jet in jets:
    totalJetPtX += jet['mcPt']*cos(jet['phi'])
    totalJetPtY += jet['mcPt']*sin(jet['phi'])
  #myMet = sqrt((totalJetPtX + leptonPt*cos(leptonPhi))**2 + (totalJetPtY + leptonPt*sin(leptonPhi))**2)
  myMet = sqrt((totalJetPtX + genLepPt*cos(genLepPhi))**2 + (totalJetPtY + genLepPt*sin(genLepPhi))**2)
  myMetPhi = atan((totalJetPtY + genLepPt*sin(genLepPhi))/(totalJetPtX + genLepPt*cos(genLepPhi)))
  print int(evt), '*', int(lumi), '\t*', int(run), '*', totalJetPtX, '*', totalJetPtY, '*', sqrt(totalJetPtX**2+totalJetPtY**2), myMet, myMetPhi, recoMet, genMet, genMetPhi, leptonPt, genLepPt
  if i>0 and (i%20)==0:
    a = raw_input('any key to continue, q to stop: ')
    if str(a) == 'q': break
    else: print



