import ROOT
from array import array
from math import sqrt, cosh, cos, sin
import os, copy, sys
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getObjDict, getVarValue
from Workspace.HEPHYPythonTools.xsec import xsec

from Workspace.RA4Analysis.cmgTuples_Spring15_150809 import *
from Workspace.metAnalysis.performanceTools import makeMETPerformanceHistos 
from Workspace.RA4Analysis.simplePlotHelpers import plot, stack, drawNMStacks

lumi=100.
small = False

samples=[ 
  {"name":"DY", "bins":[DYJetsToLL_M50_25ns], "legendText":"Drell-Yan"}
]

maxN = 10 if small else -1
for s in samples:
  totalYield=0
  for b in s["bins"]:
    chunks, sumWeight = getChunks(b, maxN=maxN)
#    print "Chunks:" , chunks
    lumiScale = xsec[b['dbsName']]*lumi/float(sumWeight)
    b["lumiScale"] = lumiScale
    b["chain"]     = getChain(chunks,  histname="", treeName = b["treeName"])
    print b["name"],"xsec",xsec[b['dbsName']],"sumWeight",sumWeight


nvtxBinning=range(0,50,5)
qtBinning=range(0,400,40)
sumETBinning=range(0,3000,100)
variables = {
  'nVert':{"func":lambda c:getVarValue(c,"nVert"), "legendText":"vertex multiplicity", "binning":nvtxBinning},
  'qt':{"func":"qt", "legendText":"p_{T,Z} (GeV)", "binning":qtBinning},
  'sumEt':{"func":lambda c:getVarValue(c,"met_sumEt"), "legendText":"\Sigma E_{T} (GeV)", "binning":sumETBinning},
}
metVariables = {
  'type1':{'ptFunc':lambda c:getVarValue(c,"met_pt"), 'phiFunc':lambda c:getVarValue(c,"met_phi")},
  'noHF': {'ptFunc':lambda c:getVarValue(c,"metNoHF_pt"), 'phiFunc':lambda c:getVarValue(c,"metNoHF_phi")}
}

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

stuff=[]
for name, v in setup["variables"].iteritems():
  p_type1 = plot.fromHisto( v['upara']['type1']['scale'], style={'legendText':'DY+Jets, 25ns, type-1',  'style':"l", 'lineThickNess':2, 'errorBars':True, 'color':ROOT.kBlack, 'markerStyle':None, 'markerSize':None})
  p_noHF_type1 = plot.fromHisto( v['upara']['noHF']['scale'], style={'legendText':'DY+Jets, 25ns, noHF, type-1',  'style':"l", 'lineThickNess':2, 'errorBars':True, 'color':ROOT.kRed, 'markerStyle':None, 'markerSize':None})
  plotLists = [[p_type1], [p_noHF_type1]]
  labels={'x':v['legendText'],'y':'\langle u_{\parallel}\\rangle/\langle q_T \\rangle'}
  opt = {'labels':labels, 'logX':False, 'logY':False, 'yRange':[0,1.5], 'ratio':None}
  opt['texLines'] = [{'pos':(0.16, 0.96),'text':'CMS Simulation, 13 TeV',        'options':{'size':0.035}}]
  opt['legend'] = {'coordinates':[0.16,0.78,0.7,0.95],'boxed':True}
  stk = stack(plotLists, options = opt)
  stuff.append(drawNMStacks(1,1,[stk],         'pngMet/scale_vs_'+name+'.png'))

  p_type1 = plot.fromHisto( v['upara']['type1']['RMS'], style={'legendText':'DY+Jets, 25ns, type-1',  'style':"l", 'lineThickNess':2, 'errorBars':True, 'color':ROOT.kBlack, 'markerStyle':None, 'markerSize':None})
  p_noHF_type1 = plot.fromHisto( v['upara']['noHF']['RMS'], style={'legendText':'DY+Jets, 25ns, noHF, type-1',  'style':"l", 'lineThickNess':2, 'errorBars':True, 'color':ROOT.kRed, 'markerStyle':None, 'markerSize':None})
  plotLists = [[p_type1], [p_noHF_type1]]
  labels={'x':v['legendText'],'y':'\sigma(u_{\parallel}+q_{T})'}
  opt = {'labels':labels, 'logX':False, 'logY':False, 'yRange':[0,50], 'ratio':None}
  opt['texLines'] = [{'pos':(0.16, 0.96),'text':'CMS Simulation, 13 TeV',        'options':{'size':0.035}}]
  opt['legend'] = {'coordinates':[0.16,0.78,0.7,0.95],'boxed':True}
  stk = stack(plotLists, options = opt)
  stuff.append(drawNMStacks(1,1,[stk],         'pngMet/upara_RMS_vs_'+name+'.png'))

  p_type1 = plot.fromHisto( v['upara']['type1']['RMScorr'], style={'legendText':'DY+Jets, 25ns, type-1',  'style':"l", 'lineThickNess':2, 'errorBars':True, 'color':ROOT.kBlack, 'markerStyle':None, 'markerSize':None})
  p_noHF_type1 = plot.fromHisto( v['upara']['noHF']['RMScorr'], style={'legendText':'DY+Jets, 25ns, noHF, type-1',  'style':"l", 'lineThickNess':2, 'errorBars':True, 'color':ROOT.kRed, 'markerStyle':None, 'markerSize':None})
  plotLists = [[p_type1], [p_noHF_type1]]
  labels={'x':v['legendText'],'y':'\sigma (u_{\parallel}+q_{T}) / (\langle u_{\parallel}\\rangle/\langle q_T \\rangle)'}
  opt = {'labels':labels, 'logX':False, 'logY':False, 'yRange':[0,50], 'ratio':None}
  opt['texLines'] = [{'pos':(0.16, 0.96),'text':'CMS Simulation, 13 TeV',        'options':{'size':0.035}}]
  opt['legend'] = {'coordinates':[0.16,0.78,0.7,0.95],'boxed':True}
  stk = stack(plotLists, options = opt)
  stuff.append(drawNMStacks(1,1,[stk],         'pngMet/upara_RMScorr_vs_'+name+'.png'))

  p_type1 = plot.fromHisto( v['uperp']['type1']['RMS'], style={'legendText':'DY+Jets, 25ns, type-1',  'style':"l", 'lineThickNess':2, 'errorBars':True, 'color':ROOT.kBlack, 'markerStyle':None, 'markerSize':None})
  p_noHF_type1 = plot.fromHisto( v['uperp']['noHF']['RMS'], style={'legendText':'DY+Jets, 25ns, noHF, type-1',  'style':"l", 'lineThickNess':2, 'errorBars':True, 'color':ROOT.kRed, 'markerStyle':None, 'markerSize':None})
  plotLists = [[p_type1], [p_noHF_type1]]
  labels={'x':v['legendText'],'y':'\sigma(u_{\perp})'}
  opt = {'labels':labels, 'logX':False, 'logY':False, 'yRange':[0,50], 'ratio':None}
  opt['texLines'] = [{'pos':(0.16, 0.96),'text':'CMS Simulation, 13 TeV',        'options':{'size':0.035}}]
  opt['legend'] = {'coordinates':[0.16,0.78,0.7,0.95],'boxed':True}
  stk = stack(plotLists, options = opt)
  stuff.append(drawNMStacks(1,1,[stk],         'pngMet/uperp_RMS_vs_'+name+'.png'))

  p_type1 = plot.fromHisto( v['uperp']['type1']['RMScorr'], style={'legendText':'DY+Jets, 25ns, type-1',  'style':"l", 'lineThickNess':2, 'errorBars':True, 'color':ROOT.kBlack, 'markerStyle':None, 'markerSize':None})
  p_noHF_type1 = plot.fromHisto( v['uperp']['noHF']['RMScorr'], style={'legendText':'DY+Jets, 25ns, noHF, type-1',  'style':"l", 'lineThickNess':2, 'errorBars':True, 'color':ROOT.kRed, 'markerStyle':None, 'markerSize':None})
  plotLists = [[p_type1], [p_noHF_type1]]
  labels={'x':v['legendText'],'y':'\sigma(u_{\perp}) / (\langle u_{\parallel}\\rangle/\langle q_T \\rangle)'}
  opt = {'labels':labels, 'logX':False, 'logY':False, 'yRange':[0,50], 'ratio':None}
  opt['texLines'] = [{'pos':(0.16, 0.96),'text':'CMS Simulation, 13 TeV',        'options':{'size':0.035}}]
  opt['legend'] = {'coordinates':[0.16,0.78,0.7,0.95],'boxed':True}
  stk = stack(plotLists, options = opt)
  stuff.append(drawNMStacks(1,1,[stk],         'pngMet/uperp_RMScorr_vs_'+name+'.png'))
