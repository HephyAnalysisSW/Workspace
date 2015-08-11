import ROOT
from array import array
from math import sqrt, cosh, cos, sin
import os, copy, sys
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getObjDict, getVarValue
from Workspace.HEPHYPythonTools.xsec import xsec

from Workspace.RA4Analysis.cmgTuples_Spring15 import *
from Workspace.metAnalysis.performanceTools import makeMETPerformanceHistos 

lumi=100.
small = True

samples=[ 
  {"name":"DY", "bins":[DYJetsToLL_M_50], "title":"Drell-Yan"}
]

nvtxBinning=[0,10,20,30,40,50]
qtBinning=range(0,100,10)
variables = {
  'nVert':{"func":lambda c:getVarValue(c,"nVert"), "title":"vertex multiplicity", "binning":nvtxBinning},
}
metVariables = {
  'type1':{'ptFunc':lambda c:getVarValue(c,"met_pt"), 'phiFunc':lambda c:getVarValue(c,"met_phi")}
}

for s in samples:
  totalYield=0
  for b in s["bins"]:
    chunks, sumWeight = getChunks(b)
#    print "Chunks:" , chunks
    lumiScale = xsec[b['dbsName']]*lumi/float(sumWeight)

    b["lumiScale"] = lumiScale
    b["chain"]     = getChain(chunks,  histname="", treeName = b["treeName"])
    print b["name"],"xsec",xsec[b['dbsName']],"sumWeight",sumWeight

presel = "1"
dilepton = "Sum$(LepGood_pt>20&&LepGood_mediumMuonId==1)>=2" 
cut = "&&".join(['('+x+')' for x in [presel, dilepton]])


def massWindow(l0,l1):
#  return sqrt(2.*l0['pt']*l1['pt']*(cosh(l0['eta']-l1['eta']) - cos(l0['phi']-l1['phi'])))
  mll = sqrt(2.*l0['pt']*l1['pt']*(cosh(l0['eta']-l1['eta']) - cos(l0['phi']-l1['phi'])))
  return abs(mll-90.2)<15.

#def mvaEleIdEta(l):
#  if abs(l["eta"]) < 0.8 and l["mvaIdPhys14"] > 0.35 : return True
#  elif abs(l["eta"]) > 0.8 and abs(l["eta"]) < 1.44 and l["mvaIdPhys14"] > 0.20 : return True
#  elif abs(l["eta"]) > 1.57 and l["mvaIdPhys14"] > -0.52 : return True
#  return False
#
#def looseEleID(l):
#  return l["pt"]>=20 and (abs(l["eta"])<1.44 or abs(l["eta"])>1.57) and abs(l["eta"])<2.4 and l["miniRelIso"]<0.4 and mvaEleIdEta(l) and l["lostHits"]<=1 and l["convVeto"] and l["sip3d"] < 4.0

def looseMuID(l):
  return l["pt"]>=20 and l["eta"]<2.1 and l["mediumMuonId"]==1 and l["miniRelIso"]<0.4 and l["sip3d"]<4.0

def getMuons(c):
  leptons = [getObjDict(c, "LepGood_", ["pt", "eta", "phi", "dxy", "dz", "relIso03", "mediumMuonId", "pdgId", "miniRelIso", "sip3d"], i) for i in range(int(getVarValue(c,'nLepGood')))]
  return [l for l in leptons if abs(l["pdgId"])==13 and looseMuID(l)]

setup = {
    'variables':variables,
    'metVariables':metVariables,
    'samples':samples,
    'preselection':cut,
    'leptons':getMuons,
    'massWindow':massWindow,
    'small':True
    }

setup = makeMETPerformanceHistos(setup) 
