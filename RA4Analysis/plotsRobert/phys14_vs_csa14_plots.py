import ROOT
from array import array
from math import *
import os, copy, sys

ROOT.TH1F().SetDefaultSumw2()

from Workspace.HEPHYPythonTools.helpers import getObjFromFile
#from Workspace.RA4Analysis.simplePlotsCommon import *
from Workspace.RA4Analysis.simplePlotHelpers import plot, stack, loopAndFill, drawNMStacks
from Workspace.RA4Analysis.helpers import *


sampleName = "WJets"

preselPHYS14 = "singleMuonic&&nTightHardLeptons==1&&nLooseHardLeptons==1&&nBJetMedium25==0"
preselCSA14 = "singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&nBJetMedium25==0"

small = False
if sampleName=="WJets":
  from Workspace.RA4Analysis.cmgTuplesPostProcessed_v4_Phys14V1 import WJetsHTToLNu as phys14_WJetsHTToLNu 
  phys14_sample=  phys14_WJetsHTToLNu['hard']
  phys14_sample['small']=small
  if 'PHYS14' not in  phys14_sample['name']:phys14_sample['name']=phys14_sample['name']+"_PHYS14"
  from Workspace.RA4Analysis.cmgTuplesPostProcessed import WJetsHTToLNu as csa14_WJetsHTToLNu
  csa14_sample =  csa14_WJetsHTToLNu
  csa14_sample['small']=small
  if 'CSA14' not in csa14_sample['name']:csa14_sample['name']=csa14_sample['name']+"_CSA14"


prefix = 'test'
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&st>250&&htJet40ja>500&&nBJetMedium25>=1&&nJet40a>=4"

signalScale=1
#prefix = 'ht400-st250-1j-0b-diLepVeto'
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&st>250&&htJet40ja>400&&nBJetMedium25==0&&nJet40a>=1"

cutBranches = ["single*", "nLoose*", "nTight*", "leptonPt", "met_phi", "htJet40ja", "nBJetMedium25", "nJet40a",'st','met', 'nVetoMuons', 'nVetoElectrons']
subdir = "/pngPHYS14vsCSA14/"+sampleName+'/'

commonCut="(1)"

#ratioOps = None 
ratioOps = {'yLabel':'A/B', 'numIndex':0, 'denIndex':1 ,'yRange':None, 'logY':False, 'color':ROOT.kBlack, 'yRange':(0, 10)}

def cutFunc(c):
  return True

def getStack(labels, var, binning, cut, options={}):
  
  style_csa14        = {'legendText':csa14_sample['name'],   'style':"l", 'lineThickness':1, 'errorBars':True, 'color':ROOT.kBlack, 'markerStyle':None, 'markerSize':None}
  style_phys14       = {'legendText':phys14_sample['name'],  'style':"l", 'linethickNess':1, 'errorBars':True, 'color':ROOT.kRed, 'markerStyle':None, 'markerSize':None}
  phys14_cut = copy.deepcopy(cut)
  phys14_cut['string']=phys14_cut['string']+"&&"+preselPHYS14
  MC_phys14          = plot(var, binning, phys14_cut, sample=phys14_sample, style=style_phys14, weight={'string':'weight'}) 
  csa14_cut = copy.deepcopy(cut)
  csa14_cut['string']=csa14_cut['string']+"&&"+preselCSA14
  MC_csa14    = plot(var, binning, csa14_cut, sample=csa14_sample, style=style_csa14, weight={'string':'weight'})
  
  plotLists = [[MC_phys14], [MC_csa14]]

  opt = {'small':small, 'yHeadRoomFac':12, 'labels':labels, 'logX':False, 'logY':True, 'yRange':[0.007, "auto"], 'ratio':ratioOps, 'fileName':var['name']}
  opt['texLines'] = [{'pos':(0.15, 0.95),'text':'CMS Simulation',        'options':{'size':0.045}},\
                     {'pos':(0.7, 0.95), 'text':'L=1fb{}^{-1} (13 TeV)', 'options':{'size':0.045}}]
  opt['legend'] = {'coordinates':[0.42,0.95 - len(plotLists)*0.08,.98,.93],'boxed':True}

  if options.has_key('ratio') and options['ratio']:
    options['texLines'] = [{'pos':(0.15, 0.95),'text':'CMS Simulation',        'options':{'size':0.045}},\
                           {'pos':(0.7, 0.95), 'text':'L=1fb{}^{-1} (13 TeV)', 'options':{'size':0.045}}]
    options['legend'] = {'coordinates':[0.42,0.95 - len(plotLists)*0.08,.98,.93],'boxed':True}
  else:
    options['texLines'] = [{'pos':(0.16, 0.965), 'text':'CMS Simulation',       'options':{'size':0.038}},\
                           {'pos':(0.7, 0.965),  'text':'L=1fb{}^{-1} (13 TeV)','options':{'size':0.038}}]
    options['legend'] = {'coordinates':[0.42,0.95 - len(plotLists)*0.08,.95,.95],'boxed':True}

  for k in options.keys():
    assert opt.has_key(k),"Stack option %s unknown!" %k
    opt[k]=options[k]
  res = stack(plotLists, options = opt)
  res.usedBranches = cutBranches
  return res

allStacks=[]

met_stack  = getStack(
    labels={'x':'#slash{E}_{T} (GeV)','y':'Number of Events / 50 GeV'}, 
    var={'name':'met','leaf':'met', 'overFlow':'upper'}, 
    binning={'binning':[1050/50,0,1050]}, 
    cut={'string':commonCut,'func':None},
    )
allStacks.append(met_stack)

ht_stack  = getStack(
    labels={'x':'H_{T} (GeV)','y':'Number of Events / 50 GeV'}, 
    var={'name':'ht','leaf':'htJet40ja', 'overFlow':'upper'}, 
    binning={'binning':[1650/50,0,1650]}, 
    cut={'string':commonCut,'func':None})
allStacks.append(ht_stack)

st_stack  = getStack(
    labels={'x':'S_{T} (GeV)','y':'Number of Events / 50 GeV'}, 
    var={'name':'st','func':cmgST, 'branches':cmgST('branches'), 'overFlow':'upper'}, 
    binning={'binning':[750/50,0,750]}, 
    cut={'string':commonCut,'func':None})
allStacks.append(st_stack)

leptonPt_stack  = getStack(
    labels={'x':'p_{T}(l) (GeV)','y':'Number of Events / 20 GeV'}, 
    var={'name':'leptonPt','leaf':'leptonPt', 'overFlow':'upper'}, 
    binning={'binning':[750/20,0,760]}, 
    cut={'string':commonCut,'func':None})
allStacks.append(leptonPt_stack)

leptonEta_stack  = getStack(
    labels={'x':'#eta(l)','y':'Number of Events'}, 
    var={'name':'leptonEta','leaf':'leptonEta', 'overFlow':'both'}, 
    binning={'binning':[24,-2.4,2.4]}, 
    cut={'string':commonCut,'func':None})
allStacks.append(leptonEta_stack)

softleptonPt_stack  = getStack(
    labels={'x':'p_{T}(l) (GeV)','y':'Number of Events / 20 GeV'}, 
    var={'name':'softleptonPt','leaf':'leptonPt', 'overFlow':'upper'}, 
    binning={'binning':[20,0,100]}, 
    cut={'string':commonCut,'func':None})
allStacks.append(softleptonPt_stack)

jet0pt_stack  = getStack(
    labels={'x':'p_{T}(leading jet) (GeV)','y':'Number of Events / 10 GeV'}, 
    var={'name':'jet0pt','leaf':'Jet_pt','ind':0, 'overFlow':'upper'}, 
    binning={'binning':[16,0,1600]}, 
    cut={'string':commonCut,'func':None})
allStacks.append(jet0pt_stack)
jet1pt_stack  = getStack(
    labels={'x':'p_{T}(2^{nd.} leading jet) (GeV)','y':'Number of Events / 10 GeV'}, 
    var={'name':'jet1pt','leaf':'Jet_pt','ind':1, 'overFlow':'upper'}, 
    binning={'binning':[16,0,1600]}, 
    cut={'string':commonCut,'func':None})
allStacks.append(jet1pt_stack)
jet2pt_stack  = getStack(
    labels={'x':'p_{T}(3^{rd.} leading jet) (GeV)','y':'Number of Events / 10 GeV'}, 
    var={'name':'jet2pt','leaf':'Jet_pt','ind':2, 'overFlow':'upper'}, 
    binning={'binning':[16,0,1600]}, 
    cut={'string':commonCut,'func':None})
allStacks.append(jet2pt_stack)
jet3pt_stack  = getStack(
    labels={'x':'p_{T}(4^{th.} leading jet) (GeV)','y':'Number of Events / 10 GeV'}, 
    var={'name':'jet3pt','leaf':'Jet_pt','ind':3, 'overFlow':'upper'}, 
    binning={'binning':[16,0,1600]}, 
    cut={'string':commonCut,'func':None})
allStacks.append(jet3pt_stack)
jet4pt_stack  = getStack(
    labels={'x':'p_{T}(5^{th.} leading jet) (GeV)','y':'Number of Events / 10 GeV'}, 
    var={'name':'jet4pt','leaf':'Jet_pt','ind':4, 'overFlow':'upper'}, 
    binning={'binning':[16,0,1600]}, 
    cut={'string':commonCut,'func':None})
allStacks.append(jet4pt_stack)

binningMTCoarse = [0,120,220,320,420,800]
mT_stack  = getStack(
    labels={'x':'m_{T} (GeV)','y':'Number of Events / 10 GeV'}, 
    var={'name':'mT','func':cmgMT, 'branches':cmgMT('branches'), 'overFlow':'upper'}, 
    binning={'binning':binningMTCoarse, 'isExplicit':True}, 
    cut={'string':commonCut,'func':None})
allStacks.append(mT_stack)
mT_stack_zoomed  = getStack(
    labels={'x':'m_{T} (GeV)','y':'Number of Events / 10 GeV'}, 
    var={'name':'mTzoomed','func':cmgMT, 'branches':cmgMT('branches'), 'overFlow':'upper'}, 
    binning={'binning':[15,0,300], 'isExplicit':False}, 
    cut={'string':commonCut,'func':None})
allStacks.append(mT_stack_zoomed)

dPhi_stack  = getStack(
    labels={'x':'#Delta#Phi(W,l)','y':'Number of Events'}, 
    var={'name':'dPhi','func':cmgDPhi, 'branches':cmgDPhi('branches'), 'overFlow':'both'}, 
    binning={'binning':[0,0.5,1,1.5,pi], 'isExplicit':True}, 
    cut={'string':commonCut,'func':None})
dPhi_stack.options['yRange']=[0.007, 10**2.7]
allStacks.append(dPhi_stack)

dPhiZoomed_stack  = getStack(
    labels={'x':'#Delta#Phi(W,l)','y':'Number of Events'}, 
    var={'name':'dPhizoomed','func':cmgDPhi, 'branches':cmgDPhi('branches'), 'overFlow':'both'}, 
    binning={'binning':[20, 0,pi], 'isExplicit':False}, 
    cut={'string':commonCut,'func':None})
allStacks.append(dPhiZoomed_stack)

nbtags_stack  = getStack(
    labels={'x':'number of b-tags (CSVM)','y':'Number of Events'}, 
    var={'name':'nMediumBTags','leaf':"nBJetMedium25", 'overFlow':'upper'}, 
    binning={'binning':[10,0,10]}, 
    cut={'string':commonCut,'func':None})
allStacks.append(nbtags_stack)

njets_stack  = getStack(
    labels={'x':'number of jets','y':'Number of Events'}, 
    var={'name':'njets','leaf':"nJet40a", 'overFlow':'upper'}, 
    binning={'binning':[18,0,18]}, 
    cut={'string':commonCut,'func':None})
allStacks.append(njets_stack)

nLooseBTags_stack  = getStack(
    labels={'x':'number of b-tags (CSVL)','y':'Number of Events'}, 
    var={'name':'nLooseBTags','leaf':"nBJetLoose25", 'overFlow':'upper'}, 
    binning={'binning':[10,0,10]}, 
    cut={'string':commonCut,'func':None})
allStacks.append(nLooseBTags_stack)

#mTClosestJetMET_stack  = getStack(
#    labels={'x':'m_{T, closest jet, #slash{E}_{T}} (GeV)','y':'Number of Events / 10 GeV'}, 
#    var={'name':'mTClosestJetMET','func':cmgMTClosestJetMET, 'overFlow':'upper'}, 
#    binning={'binning':(20,0,800), 'isExplicit':False}, 
#    cut={'string':commonCut,'func':None})
#allStacks.append(mTClosestJetMET_stack)
#
#mTClosestJetMET_zoomed_stack  = getStack(
#    labels={'x':'m_{T, closest jet, #slash{E}_{T}} (GeV)','y':'Number of Events / 10 GeV'}, 
#    var={'name':'mTClosestJetMET_zoomed','func':cmgMTClosestJetMET, 'branches':cmgMTClosestJetMET('branches'),'overFlow':'upper'}, 
#    binning={'binning':(40,0,400), 'isExplicit':False}, 
#    cut={'string':commonCut,'func':None})
#allStacks.append(mTClosestJetMET_zoomed_stack)
#
#  mTClosestBJetMET_stack  = getStack(
#      labels={'x':'m_{T, closest b-jet, #slash{E}_{T}} (GeV)','y':'Number of Events / 10 GeV'}, 
#      var={'name':'mTClosestBJetMET','func':cmgMTClosestBJetMET,'branches':cmgMTClosestBJetMET('branches'), 'overFlow':'upper'}, 
#      binning={'binning':binningMTCoarse, 'isExplicit':True}, 
#      cut={'string':commonCut,'func':None})
#  allStacks.append(mTClosestBJetMET_stack)
#
#  mTClosestBJetMET_zoomed_stack  = getStack(
#      labels={'x':'m_{T, closest b-jet, #slash{E}_{T}} (GeV)','y':'Number of Events / 10 GeV'}, 
#      var={'name':'mTClosestBJetMET_zoomed','func':cmgMTClosestBJetMET,'branches':cmgMTClosestBJetMET('branches'), 'overFlow':'upper'}, 
#      binning={'binning':(40,0,400), 'isExplicit':False}, 
#      cut={'string':commonCut,'func':None})
#  allStacks.append(mTClosestBJetMET_zoomed_stack)
#
#mTTopClosestJetMET_stack  = getStack(
#    labels={'x':'m_{T, closest jet, #slash{E}_{T}}^{top} (GeV)','y':'Number of Events / 10 GeV'}, 
#    var={'name':'mTTopClosestJetMET','func':cmgMTTopClosestJetMET, 'branches':cmgMTTopClosestJetMET('branches'), 'overFlow':'upper'}, 
#    binning={'binning':[20,0,2000], 'isExplicit':False}, 
#    cut={'string':commonCut,'func':None})
#allStacks.append(mTTopClosestJetMET_stack)
#
#mTTopClosestJetMET_zoomed_stack  = getStack(
#    labels={'x':'m_{T, closest jet, #slash{E}_{T}}^{top} (GeV)','y':'Number of Events / 10 GeV'}, 
#    var={'name':'mTTopClosestJetMET_zoomed','func':cmgMTTopClosestJetMET, 'branches':cmgMTTopClosestJetMET('branches'), 'overFlow':'upper'}, 
#    binning={'binning':[40,0,400], 'isExplicit':False}, 
#    cut={'string':commonCut,'func':None})
#allStacks.append(mTTopClosestJetMET_zoomed_stack)
#
#  mTTopClosestBJetMET_stack  = getStack(
#      labels={'x':'m_{T, closest b-jet, #slash{E}_{T}}^{top} (GeV)','y':'Number of Events / 10 GeV'}, 
#      var={'name':'mTTopClosestBJetMET','func':cmgMTTopClosestBJetMET, 'branches':cmgMTTopClosestBJetMET('branches'), 'overFlow':'upper'}, 
#      binning={'binning':[20,0,2000], 'isExplicit':False}, 
#      cut={'string':commonCut,'func':None})
#  allStacks.append(mTTopClosestBJetMET_stack)
#
#  mTTopClosestBJetMET_zoomed_stack  = getStack(
#      labels={'x':'m_{T, closest b-jet, #slash{E}_{T}}^{top} (GeV)','y':'Number of Events / 10 GeV'}, 
#      var={'name':'mTTopClosestBJetMET_zoomed','func':cmgMTTopClosestBJetMET, 'branches':cmgMTTopClosestBJetMET('branches'), 'overFlow':'upper'}, 
#      binning={'binning':[20,0,400], 'isExplicit':False}, 
#      cut={'string':commonCut,'func':None})
#  allStacks.append(mTTopClosestBJetMET_zoomed_stack)

#  minDPhiBJet_stack  = getStack(
#      labels={'x':'min#Delta#Phi(#slash{E}_{T},b-j_{1})','y':'Number of Events'}, 
#      var={'name':'minDPhiBJet','func':cmgMinDPhiBJet, 'branches':cmgMinDPhiJet('branches'), 'overFlow':'both'}, 
#      binning={'binning':[20,0,pi], 'isExplicit':False}, 
#      cut={'string':commonCut,'func':None})
#  allStacks.append(minDPhiBJet_stack)
#
#dPhiLeadingJet_stack  = getStack(
#    labels={'x':'#Delta#Phi(#slash{E}_{T},j_{1})','y':'Number of Events'}, 
#    var={'name':'dPhiLeadingJet','func':lambda c:cmgMinDPhiJet(c,1), 'branches':cmgMinDPhiJet('branches'), 'overFlow':'both'}, 
#    binning={'binning':[20,0,pi], 'isExplicit':False}, 
#    cut={'string':commonCut,'func':None})
#allStacks.append(dPhiLeadingJet_stack)
#minDPhi2Jet_stack  = getStack(
#    labels={'x':'min#Delta#Phi(#slash{E}_{T},j_{1,2})','y':'Number of Events'}, 
#    var={'name':'minDPhi2Jet','func':lambda c:cmgMinDPhiJet(c,2), 'branches':cmgMinDPhiJet('branches'), 'overFlow':'both'}, 
#    binning={'binning':[20,0,pi], 'isExplicit':False}, 
#    cut={'string':commonCut,'func':None})
#allStacks.append(minDPhi2Jet_stack)
#minDPhi3Jet_stack  = getStack(
#    labels={'x':'min#Delta#Phi(#slash{E}_{T},j_{1,2,3})','y':'Number of Events'}, 
#    var={'name':'minDPhi3Jet','func':lambda c:cmgMinDPhiJet(c,3), 'branches':cmgMinDPhiJet('branches'), 'overFlow':'both'}, 
#    binning={'binning':[20,0,pi], 'isExplicit':False}, 
#    cut={'string':commonCut,'func':None})
#allStacks.append(minDPhi3Jet_stack)
#minDPhi4Jet_stack  = getStack(
#    labels={'x':'min#Delta#Phi(#slash{E}_{T},j_{1-4})','y':'Number of Events'}, 
#    var={'name':'minDPhi4Jet','func':lambda c:cmgMinDPhiJet(c,4), 'branches':cmgMinDPhiJet('branches'), 'overFlow':'both'}, 
#    binning={'binning':[40,0,pi], 'isExplicit':False}, 
#    cut={'string':commonCut,'func':None})
#allStacks.append(minDPhi4Jet_stack)
#
#htOrthMET_stack  = getStack(
#    labels={'x':'H_{T} (GeV)','y':'Number of Events / 50 GeV'}, 
#    var={'name':'htOrthMET','func':cmgHTOrthMET, 'overFlow':'upper'}, 
#    binning={'binning':[1650/50,0,1650]}, 
#    cut={'string':commonCut,'func':None})
#allStacks.append(htOrthMET_stack)
#htRatio_stack  = getStack(
#    labels={'x':'H_{T} (GeV)','y':'Number of Events / 50 GeV'}, 
#    var={'name':'htRatio','func':cmgHTRatio, 'overFlow':'upper'}, 
#    binning={'binning':[20,0.4,1]}, 
#    cut={'string':commonCut,'func':None})
#allStacks.append(htRatio_stack)

loopAndFill(allStacks)
if small:prefix = prefix+"_small"
stuff=[]
for stk in allStacks:
  stuff.append(drawNMStacks(1,1,[stk],         subdir+prefix+"_"+stk.options['fileName']))
