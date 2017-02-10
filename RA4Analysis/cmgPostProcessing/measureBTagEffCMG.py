import ROOT
import pickle
import sys, os, copy, random, subprocess, datetime
from array import array
from Workspace.RA4Analysis.cmgObjectSelection import cmgLooseLepIndices, splitIndList, get_cmg_jets_fromStruct, splitListOfObjects, cmgTightMuID, cmgTightEleID , get_cmg_genParts_fromStruct , get_cmg_JetsforMEt_fromStruct , get_cmg_genLeps , get_cmg_genTaus
from Workspace.HEPHYPythonTools.xsec import xsec
from Workspace.HEPHYPythonTools.convertHelpers import compileClass, readVar, printHeader, typeStr, createClassString

from math import *
from Workspace.HEPHYPythonTools.user import username

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.cmgTuples_Summer16_Moriond2017_MiniAODv2 import *
from btagEfficiency import *
import time, hashlib


singleLeptonic = "Sum$((abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0)||(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.1&&LepGood_eleCBID_SPRING15_25ns_ConvVetoDxyDz==4))==1"

leptonVeto = '(Sum$(LepGood_pt>=10&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.4)==1)'

stStr = 'Sum$(LepGood_pt[0]+met_pt)'
htStr = 'Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))'
btagStr = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>0.8484)'
njetStr = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)'
cut_WW = "Sum$(abs(GenPart_pdgId)==1000022&&abs(GenPart_motherId)==1000024&&abs(GenPart_grandmotherId)==1000021)==2&&(Sum$(abs(GenPart_pdgId)==24)==2)"

#presel = singleLeptonic+'&&'+leptonVeto+'&&'+njetStr+'>2&&'+stStr+'>250&&'+htStr+'>500&&Jet_pt[1]>80&&'+cut_WW
presel = '(' + singleLeptonic + ') &&' + leptonVeto + '&&' +njetStr+'>2 &&' + stStr+'>250 &&' + htStr + '>500 && Jet_pt[1]>80'

wjetsSamples = [
            WJetsToLNu_HT1200to2500,
            WJetsToLNu_HT2500toInf,
            WJetsToLNu_HT400to600,
            WJetsToLNu_HT600to800,
            WJetsToLNu_HT800to1200,
            ]

ttjetsSamples = [
            TTJets_DiLepton,
            TTJets_SingleLeptonFromT,
            TTJets_SingleLeptonFromTbar
            ]



ttjetsChunks = []
wjetsChunks = []

for sample in ttjetsSamples:
    ch, sw = getChunks(sample)
    ttjetsChunks.append(ch)

ttjetsChunksAll = [ x[0] for x in ttjetsChunks ]
cTT = getChain(ttjetsChunksAll, histname='', treeName='tree')

for sample in wjetsSamples:
    ch, sw = getChunks(sample)
    wjetsChunks.append(ch)

wjetsChunksAll = [ x[0] for x in wjetsChunks ]
cW = getChain(wjetsChunksAll, histname='', treeName='tree')

dataDir = '/afs/hephy.at/data/dspitzbart02/RA4/btagEfficiency/'
bTagEffFile = dataDir + 'Moriond17_v3_BU.pkl'

effs = {}
effs['none']    = getDummyEfficiencies()
pickle.dump(effs, file(bTagEffFile,'w'))


print "Measuring wjets"
effW = getBTagMCTruthEfficiencies(cW, cut=presel)
effs['WJets'] = effW
pickle.dump(effs, file(bTagEffFile,'w'))

print "Measuring ttjets"
effTT = getBTagMCTruthEfficiencies(cTT, cut=presel)
effs['TTJets'] = effTT
pickle.dump(effs, file(bTagEffFile,'w'))

#chunks1, sumweight1 = getChunks(SMS_T5qqqqVV_TuneCUETP8M1_v1)
#chunks2, sumweight2 = getChunks(SMS_T5qqqqVV_TuneCUETP8M1_v2)
#allChunks = chunks1+chunks2
#
#cSignal = getChain(allChunks, histname='', treeName='tree')

#cSignal = getChain(chunks1[0:100], histname='', treeName='tree')

#massPoints = pickle.load(file('/afs/hephy.at/data/easilar01/Ra40b/pickleDir/T5qqqqWW_mass_nEvents_xsec_pkl'))
#
#allMassPoints = []
#
#for mgluino in massPoints.keys():
#  for mneutralino in massPoints[mgluino]:
#    allMassPoints.append((mgluino,mneutralino))
#
#deltaM = [1000,800,600,400,200,0]
#
#massPointDict = {}
#
#for dM in deltaM:
#  massPointDict[dM] = []
#
#for massPoint in allMassPoints:
#  for dM in deltaM:
#    if dM < (massPoint[0]-massPoint[1]): break
#  massPointDict[dM].append(massPoint)
#
#debug = False
#
#binBorders = [0,1000000]
##binBorders = [0,100000]
##if debug: binBorders = [0,5]
#bins = []
#
#for i,b in enumerate(binBorders):
#  lowerBound = binBorders[i]
#  print i
#  if i>len(binBorders)-2: upperBound = -1
#  else: upperBound = binBorders[i+1]
#  bins.append((lowerBound, upperBound))
#
#effs = {}
#
#for i,b in enumerate(bins):
#  print 'Measuring efficiencies for (mgl-mN) in',b
#  massWindowCut = '(GenSusyMGluino-GenSusyMNeutralino)>='+str(b[0])
#  if b[1]>0: massWindowCut += '&&(GenSusyMGluino-GenSusyMNeutralino)<'+str(b[1])
#  cut = presel + '&&' + massWindowCut
#  print 'Using this mass window cut',massWindowCut
#  #print cut
#  effs[b] = getBTagMCTruthEfficiencies2D(cSignal, cut = cut)
#  pickle.dump(effs, file('/data/dspitzbart/Spring16/btagEfficiency/FS_intermediate_pkl','w'))
#  print effs[b]
#  #if debug:
#  #  if i>0: break
#    
#
#pickle.dump(effs, file('/data/dspitzbart/Spring16/btagEfficiency/FS_full_pkl','w'))
#
#effs_update = {}
#for b in enumerate(bins):
#  newKey = 'Signal_deltaM_'
#  newKey += str(b[0])
#  if b[1]>0: newKey += 'to'+str(b[1])
#  else: newKey += 'plus'
#  effs_update[newKey] = effs[b]
#
#pickle.dump(effs_update, file('/data/dspitzbart/Spring16/btagEfficiency/FS_full_pkl','w'))
