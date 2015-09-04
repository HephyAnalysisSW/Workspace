import ROOT
from array import array
from math import *
import os, copy, sys

ROOT.TH1F().SetDefaultSumw2()

from Workspace.HEPHYPythonTools.helpers import getObjFromFile
#from Workspace.RA4Analysis.simplePlotsCommon import *
from Workspace.RA4Analysis.simplePlotHelpers import plot, stack, loopAndFill, drawNMStacks
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.cmgTuples_Data50ns_1l_HT400ST200_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Spring15_50ns_HT400ST200_postProcessed import * 
#from Workspace.RA4Analysis.cmgTuples_Data50ns_1l_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_50ns_postProcessed import * 
small = False
#from Workspace.RA4Analysis.cmgTuples_Data50ns_1l_HT400ST200_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT400ST200_postProcessed import QCDHT_25ns 
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_50ns_HT400ST200_postProcessed import *

cutBranches = ["weight", "single*", "nLoose*", "nTight*", "leptonPt", "met_phi", \
               "htJet40ja", "nBJetMedium25", "nJet40a",'st','met', 'Jet_pt', 'Jet_btagCMVA', "Jet_id", "Jet_eta", "Jet_btagCSV", "LepGood*", 
               "Flag_*", "HLT_*"]
subdir = "/png50ns/"


#&&((Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4)))>500)
#&&(Sum$(((LepGood_pt[0]+met_pt)>250))==1)
#&&((Sum$(Jet_pt>30&&abs(Jet_eta)<2.4))>=2)
#&&(Jet_pt[1]>80)
#&&(Flag_HBHENoiseFilterMinZeroPatched&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_eeBadScFilter)
#&&(HLT_EleHT350MET70 || HLT_ElNoIso)

cutFunc=None
lumiScaleFac = 42./3000.
mode = "Ele"
prefix = 'presel_'+mode

filterCut = "(Flag_HBHENoiseFilterMinZeroPatched&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_eeBadScFilter)"

preselMu=""\
  +"((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0))==1)"\
  +"&&Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=10)==1"\
  +"&&Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10)==0"
triggerMu = "(HLT_MuHT350MET70 || HLT_Mu50NoIso)"

preselEle=""\
  "(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.5&&LepGood_miniRelIso<0.1&&((abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>0.73)||((abs(LepGood_eta)>=0.8&&abs(LepGood_eta)<1.44)&&LepGood_mvaIdPhys14>0.57)||((abs(LepGood_eta)>=1.57)&&LepGood_mvaIdPhys14>0.05))&&LepGood_lostHits==0&&LepGood_convVeto&&LepGood_sip3d<4.0)==1)"\
  +"&&Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=10)==0"\
  +"&&Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10)==1"
triggerEle = "(HLT_EleHT350MET70 || HLT_ElNoIso)"

preselHad=""\
  +"((Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)))>500)"\
  +"&&(Sum$(((LepGood_pt[0]+met_pt)>250))==1)"\
  +"&&((Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>=2)"\
  +"&&(Jet_pt[1]>80)"

if mode=="Mu":
  presel = "&&".join([preselMu, preselHad])
  dataCut = "&&".join([triggerMu, filterCut])
  dataSample = SingleMuon_Run2015B_PromptReco
if mode=="Ele":
  presel = "&&".join([preselEle, preselHad])
  dataCut = "&&".join([triggerEle, filterCut])
  dataSample = SingleElectron_Run2015B_PromptReco

cutString=presel

ratioOps = {'yLabel':'Data/MC', 'numIndex':1, 'denIndex':0 ,'yRange':None, 'logY':False, 'color':ROOT.kBlack, 'yRange':(0.1, 2.1)}

def getStack(labels, var, binning, cut, options={}):

  style_Data         = {'legendText':'Single Muon',      'style':"e", 'lineThickness':0, 'errorBars':True, 'color':color("data"), 'markerStyle':20, 'markerSize':1}

  style_WJets        = {'legendText':'W + Jets',         'style':"f", 'lineThickness':0, 'errorBars':False, 'color':color("WJetsHTToLNu"), 'markerStyle':None, 'markerSize':None}
  style_TTJets       = {'legendText':'t#bar{t} + Jets',  'style':"f", 'linethickNess':0, 'errorBars':False, 'color':color("TTJets"), 'markerStyle':None, 'markerSize':None}

  style_DY           = {'legendText':'DY + Jets',  'style':"f", 'linethickNess':0, 'errorBars':False,       'color':color("DY"), 'markerStyle':None, 'markerSize':None}
  style_TTVH         = {'legendText':'t#bar{t} + W/Z/H',  'style':"f", 'linethickNess':0, 'errorBars':False, 'color':color("TTVH"), 'markerStyle':None, 'markerSize':None}
  style_QCD          = {'legendText':'QCD',  'style':"f", 'linethickNess':0, 'errorBars':False,             'color':color("QCD"), 'markerStyle':None, 'markerSize':None}
  style_singleTop    = {'legendText':'single top',  'style':"f", 'linethickNess':0, 'errorBars':False,      'color':color("singleTop"), 'markerStyle':None, 'markerSize':None}
  
  data               = plot(var, binning, cut, sample=dataSample,       style=style_Data)
  MC_TTJets          = plot(var, binning, cut, sample=TTJets_50ns,       style=style_TTJets, weight={'string':'weight'})
  MC_WJetsToLNu      = plot(var, binning, cut, sample=WJetsToLNu_50ns,   style=style_WJets, weight={'string':'weight'})
  MC_DY              = plot(var, binning, cut, sample=DYHT_50ns,           style=style_DY, weight={'string':'weight'})
#  MC_TTVH            = plot(var, binning, cut, sample=TTVH,       style=style_TTVH, weight={'string':'weight'})
  MC_singleTop       = plot(var, binning, cut, sample=singleTop_50ns,    style=style_singleTop, weight={'string':'weight'})
  MC_QCD             = plot(var, binning, cut, sample=QCDHT_25ns,        style=style_QCD, weight={'string':'weight'})

  mcStack = [MC_TTJets, MC_WJetsToLNu,  MC_QCD, MC_singleTop, MC_DY]
  for s in mcStack:
    s.sample['scale'] = lumiScaleFac

  plotLists = [mcStack, [data]]

  for pL in plotLists:
    for p in pL:
      p.sample['small']=small

  opt = {'small':small, 'yHeadRoomFac':12, 'labels':labels, 'logX':False, 'logY':True, 'yRange':[0.11, "auto"], 'ratio':ratioOps, 'fileName':var['name']}
#  opt['texLines'] = [{'pos':(0.15, 0.95),'text':'CMS Simulation',        'options':{'size':0.045}},\
#                     {'pos':(0.7, 0.95), 'text':'L=4fb{}^{-1} (13 TeV)', 'options':{'size':0.045}}]
#  opt['legend'] = {'coordinates':[0.6,0.95 - len(plotLists)*0.09,.98,.93],'boxed':True}
  if opt.has_key('ratio') and opt['ratio']:
    opt['texLines'] = [{'pos':(0.15, 0.95),'text':'CMS Preliminary', 'options':{'size':0.052}},\
                       {'pos':(0.7, 0.95), 'text':'L=42pb{}^{-1} (13 TeV)', 'options':{'size':0.052}}]
    opt['legend'] = {'coordinates':[0.55,0.90 - len(mcStack)*0.05,.98,.93],'boxed':True}
  else:
    opt['texLines'] = [{'pos':(0.16, 0.965), 'text':'CMS Preliminary',       'options':{'size':0.038}},\
                       {'pos':(0.7, 0.965),  'text':'L=42pb{}^{-1} (13 TeV)','options':{'size':0.038}}]
    opt['legend'] = {'coordinates':[0.55,0.90 - len(mcStack)*0.05,.98,.95],'boxed':True}

  opt.update(options)
  res = stack(plotLists, options = opt)
  res.usedBranches = cutBranches
  return res

allStacks=[]

met_stack  = getStack(
    labels={'x':'#slash{E}_{T} (GeV)','y':'Number of Events / 50 GeV'},
    var={'name':'met','leaf':'met', 'overFlow':'upper'},
    binning={'binning':[1050/50,0,1050]},
    cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
    )
allStacks.append(met_stack)

ht_stack  = getStack(
    labels={'x':'H_{T} (GeV)','y':'Number of Events / 100 GeV'},
#    var={'name':'ht','leaf':'htJet40ja', 'overFlow':'upper'},
    var={'name':'ht','TTreeFormula':'Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))', 'overFlow':'upper'},
    binning={'binning':[2600/100,0,2600]},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
allStacks.append(ht_stack)

st_stack  = getStack(
    labels={'x':'S_{T} (GeV)','y':'Number of Events / 50 GeV'},
    var={'name':'st','func':cmgST, 'branches':cmgST('branches'), 'overFlow':'upper'},
    binning={'binning':[1500/50,0,1500]},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
allStacks.append(st_stack)

leptonPt_stack  = getStack(
    labels={'x':'p_{T}(l) (GeV)','y':'Number of Events / 25 GeV'},
    var={'name':'leptonPt','leaf':'leptonPt', 'overFlow':'upper'},
    binning={'binning':[975/25,0,975]},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
allStacks.append(leptonPt_stack)

lepGood_pt0_stack  = getStack(
    labels={'x':'p_{T}(l) (GeV)','y':'Number of Events / 25 GeV'},
    var={'name':'LepGood_pt0','leaf':'LepGood_pt','ind':0, 'overFlow':'upper'},
    binning={'binning':[975/25,0,975]},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
allStacks.append(lepGood_pt0_stack)

leptonEta_stack  = getStack(
    labels={'x':'#eta(l)','y':'Number of Events'},
    var={'name':'leptonEta','leaf':'leptonEta', 'overFlow':'both'},
    binning={'binning':[24,-2.4,2.4]},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
allStacks.append(leptonEta_stack)

jet0pt_stack  = getStack(
    labels={'x':'p_{T}(leading jet) (GeV)','y':'Number of Events / 100 GeV'},
    var={'name':'jet0pt','leaf':'Jet_pt','ind':0, 'overFlow':'upper'},
    binning={'binning':[12,0,1200]},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
allStacks.append(jet0pt_stack)
jet1pt_stack  = getStack(
    labels={'x':'p_{T}(2^{nd.} leading jet) (GeV)','y':'Number of Events / 100 GeV'},
    var={'name':'jet1pt','leaf':'Jet_pt','ind':1, 'overFlow':'upper'},
    binning={'binning':[12,0,1200]},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
allStacks.append(jet1pt_stack)
jet2pt_stack  = getStack(
    labels={'x':'p_{T}(3^{rd.} leading jet) (GeV)','y':'Number of Events / 100 GeV'},
    var={'name':'jet2pt','leaf':'Jet_pt','ind':2, 'overFlow':'upper'},
    binning={'binning':[12,0,1200]},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
allStacks.append(jet2pt_stack)
jet3pt_stack  = getStack(
    labels={'x':'p_{T}(4^{th.} leading jet) (GeV)','y':'Number of Events / 100 GeV'},
    var={'name':'jet3pt','leaf':'Jet_pt','ind':3, 'overFlow':'upper'},
    binning={'binning':[12,0,1200]},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
allStacks.append(jet3pt_stack)
jet4pt_stack  = getStack(
    labels={'x':'p_{T}(5^{th.} leading jet) (GeV)','y':'Number of Events / 100 GeV'},
    var={'name':'jet4pt','leaf':'Jet_pt','ind':4, 'overFlow':'upper'},
    binning={'binning':[12,0,1200]},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
allStacks.append(jet4pt_stack)

binningMTCoarse = range(0,500,20) 
mT_stack  = getStack(
    labels={'x':'m_{T} (GeV)','y':'Number of Events / 20 GeV'},
    var={'name':'mT','func':cmgMT, 'branches':cmgMT('branches'), 'overFlow':'upper'},
    binning={'binning':binningMTCoarse, 'isExplicit':True},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
allStacks.append(mT_stack)

mT_stack_zoomed  = getStack(
    labels={'x':'m_{T} (GeV)','y':'Number of Events / 20 GeV'},
    var={'name':'mTzoomed','func':cmgMT, 'branches':cmgMT('branches'), 'overFlow':'upper'},
    binning={'binning':[280/20,0,280], 'isExplicit':False},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
allStacks.append(mT_stack_zoomed)

dPhi_stack  = getStack(
    labels={'x':'#Delta#Phi(W,l)','y':'Number of Events'},
    var={'name':'dPhi','func':cmgDPhi, 'branches':cmgDPhi('branches'), 'overFlow':'both'},
    binning={'binning':[0,0.5,1,1.5,pi], 'isExplicit':True},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
#dPhi_stack.options['yRange']=[0.007, 10**2.7]
allStacks.append(dPhi_stack)

dPhiFine_stack  = getStack(
    labels={'x':'#Delta#Phi(W,l)','y':'Number of Events'},
    var={'name':'dPhiFine','func':cmgDPhi, 'branches':cmgDPhi('branches'), 'overFlow':'both'},
    binning={'binning':[20, 0,pi], 'isExplicit':False},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
allStacks.append(dPhiFine_stack)

nbtags_stack  = getStack(
    labels={'x':'number of b-tags (CSVM)','y':'Number of Events'},
    var={'name':'nBTags','TTreeFormula':"Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>0.890)", 'overFlow':'upper'},
    binning={'binning':[8,0,8]},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
allStacks.append(nbtags_stack)

njets_stack  = getStack(
    labels={'x':'number of jets','y':'Number of Events'},
    var={'name':'njets','TTreeFormula':'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)', 'overFlow':'upper'},
    binning={'binning':[14,0,14]},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
allStacks.append(njets_stack)

nVert_stack  = getStack(
    labels={'x':'vertex multiplicity','y':'Number of Events'},
    var={'name':'nVert','leaf':"nVert", 'overFlow':'upper'},
    binning={'binning':[50,0,50]},
    cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
allStacks.append(nVert_stack)

loopAndFill(allStacks)

stuff=[]
for stk in allStacks:
  stuff.append(drawNMStacks(1,1,[stk],         subdir+prefix+"_"+stk.options['fileName']))
