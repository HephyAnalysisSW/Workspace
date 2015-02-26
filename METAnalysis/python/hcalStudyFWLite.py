import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *
import sys, os, copy, random, subprocess, datetime

#subDir = "convertedTuples_v26"

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

#from optparse import OptionParser
#parser = OptionParser()
#parser.add_option("--file", dest="file", default="", type="string", action="store", help="file:Which file.")
#(options, args) = parser.parse_args()

files = ['root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_3_2_patch1/DoubleMuParked/RECO/GR_R_73_V0_HcalExtValid_RelVal_zMu2012D-v1/00000/F4C7B64A-DFB3-E411-B76E-002590593878.root']

edmCollections = [ {'name':'pfMet', 'label':("pfMet"), 'edmType':"vector<reco::PFMET>"} ]
edmCollections.append({'name':'pf', 'label':("packedPFCandidates"), 'edmType':"vector<pat::PackedCandidate>"})
edmCollections.append( {'name':'gps', 'label':("prunedGenParticles"), 'edmType':"vector<reco::GenParticle>"})
edmCollections.append({'name':'puppi', 'label':("puppi","Puppi"), 'edmType':"vector<reco::PFCandidate>"})
edmCollections.append({'name':'genMet', 'label':("genMetTrue"), 'edmType':"vector<reco::GenMET>"})

events = Events(files)
for nev in range(start, stop):
  events.to(nev)

  for v in loadEDMCollections:
    events.getByLabel(v['label'],handles[v['name']])
    products[v['name']] =handles[v['name']].product()

