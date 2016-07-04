import ROOT
import pickle
import copy, os, sys

ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/WPolarizationVariation.C+")
#ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
#ROOT.TH1F().SetDefaultSumw2()
#ROOT.setTDRStyle()
ROOT.gStyle.SetMarkerStyle(1)
ROOT.gStyle.SetOptTitle(0)

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *

from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_antiSel_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_postProcessed import *
from Workspace.RA4Analysis.signalRegions import *
from math import *
from Workspace.HEPHYPythonTools.user import username


picklePath = '/data/'+username+'/Results2016/WPolarizationEstimation/'
picklePresel = 'Wjets_uncertainties_pkl'

cTT = getChain(TTJets_Comb,histname='')
cW  = getChain(WJetsHTToLNu,histname='')

uncertaintyDict = {
'tt':   {'chain':cTT,'a':0.05, 'normUp':1, 'normDown':1, 'charge':'both', 'uncertainties':{}},
'W':    {'chain':cW,  'a':0.1,  'normUp':1, 'normDown':1, 'charge':'both', 'uncertainties':{}},
'W_p':  {'chain':cW, 'a':0.1,  'normUp':1, 'normDown':1, 'charge':'pos', 'uncertainties':{}},
#'W_m':  {'chain':cW, 'a':0.1,  'normUp':1, 'normDown':1, 'charge':'neg', 'uncertainties':{}}
}

#presel = 'nLep==1&&nVeto==0&&leptonPt>25&&Jet2_pt>80&&Selected==1'
presel = "singleLeptonic" + "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>2 && htJet30j>500"

def getGenWandLepton(c):
  genPartAll = [getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex'], j) for j in range(int(c.GetLeaf('nGenPart').GetValue()))]
  lepton = filter(lambda l:abs(l['pdgId']) in [11,13,15], genPartAll)
  if len(lepton)==0:
    print "no generated lepton found (hadronic ttjets event)!"
    p4w=False
    p4lepton=False
    return p4w, p4lepton
  lFromW = filter(lambda w:abs(w['motherId'])==24, lepton)
  if len(lFromW)==0:
    test = filter(lambda w:w['motherId']==24, lepton)
    if len(test)==0: print 'No lepton from W found (hadronic ttjets event)'
    p4w=False
    p4lepton=False
    return p4w, p4lepton
  elif len(lFromW)>0:
    Ws = []
    leps = []
    for i in range(len(lFromW)):
      if abs(lFromW[i]['motherId'])!=24: print '4)this should not have happened'
      genW = getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex'], int(lFromW[i]['motherIndex']))
      if abs(genW['pdgId'])!=24: '5)this should not have happened'
      W = ROOT.TLorentzVector()
      W.SetPtEtaPhiM(genW['pt'],genW['eta'],genW['phi'],genW['mass'])
      lep = ROOT.TLorentzVector()
      lep.SetPtEtaPhiM(lFromW[i]['pt'],lFromW[i]['eta'],lFromW[i]['phi'],lFromW[i]['mass'])
      p4lepton = ROOT.LorentzVector(lep.Px(),lep.Py(),lep.Pz(),lep.E())
      p4w = ROOT.LorentzVector(W.Px(),W.Py(),W.Pz(),W.E())
      Ws.append(p4w)
      leps.append(p4lepton)
    if len(lFromW)>2:
      print '3)this should not have happened'
    #if abs(lFromW[0]['motherId'])!=24: print '4)this should not have happened'
    #genW = getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex'], int(lFromW[0]['motherIndex']))
    #lep = ROOT.TLorentzVector()
    #lep.SetPtEtaPhiM(lFromW[0]['pt'],lFromW[0]['eta'],lFromW[0]['phi'],lFromW[0]['mass'])
  #if abs(genW['pdgId'])!=24: '5)this should not have happened'
  #W = ROOT.TLorentzVector()
  #W.SetPtEtaPhiM(genW['pt'],genW['eta'],genW['phi'],genW['mass'])
  #p4lepton = ROOT.LorentzVector(lep.Px(),lep.Py(),lep.Pz(),lep.E())
  #p4w = ROOT.LorentzVector(W.Px(),W.Py(),W.Pz(),W.E())
  #return p4w, p4lepton
  return Ws, leps


signalRegion = signalRegions2016


for u in uncertaintyDict:
  unc = uncertaintyDict[u]
  print 'Will determine the normalization after preselection now'
  preselName, preselCut = nameAndCut((250,-1), (500,-1), (5,-1), btb=(0,0), presel=presel, charge=unc['charge'], btagVar = 'nBJetMediumCSV30')#, stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean')
  unc["chain"].Draw(">>eList",preselCut) #Get the event list 'eList' which has all the events satisfying the cut
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  print "Will loop over", number_events,"events"

  yNormUp = 0.
  yNormVarUp = 0.
  yNormDown = 0.
  yNormVarDown = 0.

  y = 0.
  yVar = 0.
  noVecCount = 0
  
  for i in range(number_events): #Loop over those events
    if i%10000==0:
      print "At %i of %i"%(i,number_events)
    unc["chain"].GetEntry(elist.GetEntry(i))
    #find gen W
    p4w, p4lepton = getGenWandLepton(unc['chain'])
    weight = getVarValue(unc["chain"], "weight")
    topPt  = getVarValue(unc["chain"], "TopPtWeight")
    weight *= topPt

    if not p4w and not p4lepton:
      noVecCount += 1
      y += weight
      yVar += (weight)**2
      yNormUp += weight
      yNormVarUp += (weight)**2
      yNormDown += weight
      yNormVarDown += (weight)**2
      continue
    normWeightUp = weight
    normWeightDown = weight
    for ilep, lep in enumerate(p4lepton):
      cosTheta = ROOT.WjetPolarizationAngle(p4w[ilep], p4lepton[ilep])
      normWeightUp *= (1. + unc['a']*(1.-cosTheta)**2)
      normWeightDown *= (1. - unc['a']*(1.-cosTheta)**2)

    yNormUp += normWeightUp
    yNormDown += normWeightDown

    yNormVarUp += (normWeightUp)**2
    yNormVarDown += (normWeightDown)**2

    y += weight
    yVar += (weight)**2
  
  normUp, normErrorUp = getPropagatedError(y, sqrt(yVar), yNormUp, sqrt(yNormVarUp), returnCalcResult=True)
  normDown, normErrorDown = getPropagatedError(y, sqrt(yVar), yNormDown, sqrt(yNormVarDown), returnCalcResult=True)

  
  print round(normUp,3), round(normErrorUp,3)
  print round(normDown,3), round(normErrorDown,3)
  
  unc['normUp'] = normUp
  unc['normDown'] = normDown


#  bins = {}
#  for srNJet in signalRegion:
#    bins[srNJet] = {}
#    for stb in signalRegion[srNJet]:
#      bins[srNJet][stb] = {}
#      for htb in signalRegion[srNJet][stb]:
#        bins[srNJet][stb][htb] = {}
#        deltaPhiCut = signalRegion[srNJet][stb][htb]['deltaPhi']
#        
#        cN, cC = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, charge=unc['charge'], btagVar = 'nBJetMediumCSV30', stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean')
#        unc["chain"].Draw(">>eList",cC) #Get the event list 'eList' which has all the events satisfying the cut
#        elist = ROOT.gDirectory.Get("eList")
#        number_events = elist.GetN()
#        print "Will loop over", number_events,"events"
#      
#        yUp = 0.
#        yVarUp = 0.
#        yDown = 0.
#        yVarDown = 0.
#
#        y = 0.
#        yVar = 0.
#        noVecCount = 0
#      
#        for i in range(number_events): #Loop over those events
#          if i%10000==0:
#            print "At %i of %i"%(i,number_events)
#          unc["chain"].GetEntry(elist.GetEntry(i))
#          #find gen W
#          p4w, p4lepton = getGenWandLepton(unc['chain'])
#          weight = getVarValue(unc["chain"], "weight")
#      
#          if not p4w and not p4lepton:
#            noVecCount += 1
#            y += weight
#            yVar += (weight)**2
#            yNorm += weight
#            yNormVar += (weight)**2
#            continue
#          
#          normWeightUp = weight
#          normWeightDown = weight
#          for ilep, lep in enumerate(p4lepton):
#            cosTheta = ROOT.WjetPolarizationAngle(p4w[ilep], p4lepton[ilep])
#            normWeightUp *= (1. + unc['a']*(1.-cosTheta)**2)
#            normWeightDown *= (1. - unc['a']*(1.-cosTheta)**2)
#      
#          yUp += normWeightUp
#          yDown += normWeightDown
#      
#          yVarUp += (normWeightUp)**2
#          yVarDown += (normWeightDown)**2
#      
#          y += weight
#          yVar += (weight)**2
#        
#        yUp = yUp*normUp
#        yDown = yDown*normDown
#        Up, ErrorUp = getPropagatedError(y, sqrt(yVar), yUp, sqrt(yVarUp), returnCalcResult=True)
#        Down, ErrorDown = getPropagatedError(y, sqrt(yVar), yDown, sqrt(yVarDown), returnCalcResult=True)
#        
#        bins[srNJet][stb][htb] = {'up':Up, 'up_err':ErrorUp, 'down':Down, 'down_err':ErrorDown}
#
#  unc['uncertainties'] = bins
#  unc['chain'] = 'ready'


#pickle.dump(uncertaintyDict, file(picklePath+picklePresel,'w'))
