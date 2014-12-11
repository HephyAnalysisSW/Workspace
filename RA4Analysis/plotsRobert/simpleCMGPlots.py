import ROOT
from array import array
from math import *
import os, copy, sys

ROOT.TH1F().SetDefaultSumw2()

from Workspace.HEPHYPythonTools.helpers import getObjFromFile
#from Workspace.RA4Analysis.simplePlotsCommon import *
from Workspace.RA4Analysis.simplePlotHelpers import plot, stack, loopAndFill, drawNMStacks
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v3 import * 

subdir = "/pngCMGSoft/"

#prefix = 'mTSel_ht500-met250-6j-0b-diLepVeto'
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&met_pt>250&&htJet40ja>500&&nBJetMedium25==0&&nJet40a>=6"

#prefix = 'ht500-st250-4j-0b-diLepVeto'
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&st>250&&htJet40ja>500&&nBJetMedium25==0&&nJet40a>=4"

#prefix = 'ht500-st250-4j-geq1b-diLepVeto'
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&st>250&&htJet40ja>500&&nBJetMedium25>=1&&nJet40a>=4"

signalScale=1
#prefix = 'ht400-st250-1j-0b-diLepVeto'
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&st>250&&htJet40ja>400&&nBJetMedium25==0&&nJet40a>=1"

for i in range(3):
#  if i==0:
#    prefix = 'soft_ht500-st250-6j-0b-diLepVeto'
#    presel="singleMuonic&&nLooseSoftLeptons==1&&nTightSoftLeptons==1&&nTightHardLeptons==0&&st>250&&htJet40ja>500&&nBJetMedium25==0&&nJet40a>=6"
#
#  if i==1:
#    prefix = 'soft_ht500-st250-4j-0b-diLepVeto'
#    presel="singleMuonic&&nLooseSoftLeptons==1&&nTightSoftLeptons==1&&nTightHardLeptons==0&&st>250&&htJet40ja>500&&nBJetMedium25==0&&nJet40a>=4"
#
#  if i==2:
#    prefix = 'soft_ht500-st250-2j-0b-diLepVeto'
#    presel="singleMuonic&&nLooseSoftLeptons==1&&nTightSoftLeptons==1&&nTightHardLeptons==0&&st>250&&htJet40ja>500&&nBJetMedium25==0&&nJet40a>=2"

#  if i==3:
#    prefix = 'soft_ht500-st250-6j-geq2b-diLepVeto'
#    presel="singleMuonic&&nLooseSoftLeptons==1&&nTightSoftLeptons==1&&nTightHardLeptons==0&&st>250&&htJet40ja>500&&nBJetMedium25>=2&&nJet40a>=6"
#    
#  if i==4:
#    prefix = 'soft_ht500-st250-4j-geq2b-diLepVeto'
#    presel="singleMuonic&&nLooseSoftLeptons==1&&nTightSoftLeptons==1&&nTightHardLeptons==0&&st>250&&htJet40ja>500&&nBJetMedium25>=2&&nJet40a>=4"
#    
#  if i==5:
#    prefix = 'soft_ht500-st250-2j-geq2b-diLepVeto'
#    presel="singleMuonic&&nLooseSoftLeptons==1&&nTightSoftLeptons==1&&nTightHardLeptons==0&&st>250&&htJet40ja>500&&nBJetMedium25>=2&&nJet40a>=2"
##HARD
  if i==0:
    prefix = 'hard_ht500-st250-6j-0b-diLepVeto'
    presel="singleMuonic&&nLooseSoftLeptons==0&&nTightHardLeptons==1&&nTightLooseLeptons==1&&st>250&&htJet40ja>500&&nBJetMedium25==0&&nJet40a>=6"

  if i==1:
    prefix = 'hard_ht500-st250-4j-0b-diLepVeto'
    presel="singleMuonic&&nLooseSoftLeptons==0&&nTightHardLeptons==1&&nTightLooseLeptons==1&&st>250&&htJet40ja>500&&nBJetMedium25==0&&nJet40a>=4"

  if i==2:
    prefix = 'hard_ht500-st250-2j-0b-diLepVeto'
    presel="singleMuonic&&nLooseSoftLeptons==0&&nTightHardLeptons==1&&nTightLooseLeptons==1&&st>250&&htJet40ja>500&&nBJetMedium25==0&&nJet40a>=2"

  cutString=presel
  wjetsSample = hard_WJetsHTToLNu
  ttJetsPowHeg = hard_ttJetsCSA1450ns
#  wjetsSample = soft_WJetsHTToLNu
#  ttJetsPowHeg = soft_ttJetsCSA1450ns

  signalPrefix="" if signalScale==1 else str(signalScale)+"x "
  #HARD
  hard_T5Full_1200_1000_800['style'] = {'legendText':signalPrefix+hard_T5Full_1200_1000_800['name'],   'style':"l", 'lineThickness':2, 'errorBars':False, 'color':ROOT.kBlue, 'markerStyle':None, 'markerSize':None}
  hard_T5Full_1500_800_100['style']  = {'legendText':signalPrefix+hard_T5Full_1500_800_100['name'],   'style':"l", 'lineThickness':2, 'errorBars':False, 'color':ROOT.kBlack, 'markerStyle':None, 'markerSize':None}
  hard_T1tttt_2J_mGo1300_mStop300_mCh285_mChi280['style']  = {'legendText':signalPrefix+hard_T1tttt_2J_mGo1300_mStop300_mCh285_mChi280['name'],   'style':"l", 'lineThickness':2, 'errorBars':False, 'color':ROOT.kGreen, 'markerStyle':None, 'markerSize':None}
  signals = [hard_T5Full_1200_1000_800, hard_T5Full_1500_800_100, hard_T1tttt_2J_mGo1300_mStop300_mCh285_mChi280]

#  soft_T6qqWW_Sq_950_LSP_300_Chi_350['style'] = {'legendText':signalPrefix+soft_T6qqWW_Sq_950_LSP_300_Chi_350['name'],   'style':"l", 'lineThickness':2, 'errorBars':False, 'color':ROOT.kBlue, 'markerStyle':None, 'markerSize':None}
#  soft_T5qqqqWW_Gl_1400_LSP_300_Chi_315['style']  = {'legendText':signalPrefix+soft_T5qqqqWW_Gl_1400_LSP_300_Chi_315['name'],   'style':"l", 'lineThickness':2, 'errorBars':False, 'color':ROOT.kBlack, 'markerStyle':None, 'markerSize':None}
#  soft_T1tttt_2J_mGo1300_mStop300_mCh285_mChi280['style']  = {'legendText':signalPrefix+soft_T1tttt_2J_mGo1300_mStop300_mCh285_mChi280['name'],   'style':"l", 'lineThickness':2, 'errorBars':False, 'color':ROOT.kGreen, 'markerStyle':None, 'markerSize':None}
#  signals = [soft_T6qqWW_Sq_950_LSP_300_Chi_350, soft_T5qqqqWW_Gl_1400_LSP_300_Chi_315, soft_T1tttt_2J_mGo1300_mStop300_mCh285_mChi280]

  for s in signals:
    s['scale'] = signalScale
  #ratioOps = {'yLabel':'A/B', 'numIndex':0, 'denIndex':1 ,'yRange':None, 'logY':False, 'color':ROOT.kBlack, 'yRange':(0.5,1.5)}
  ratioOps = None 

  def cutFunc(c):
    return True

  def getStack(labels, var, binning, cut, options={}):
    
    style_WJets   = {'legendText':'W + Jets',         'style':"f", 'lineThickness':0, 'errorBars':False, 'color':ROOT.kYellow, 'markerStyle':None, 'markerSize':None}
    style_TTJets =  {'legendText':'t#bar{t} + Jets',  'style':"f", 'linethickNess':0, 'errorBars':False, 'color':ROOT.kRed-3, 'markerStyle':None, 'markerSize':None}
    MC_WJETS   = plot(var, binning, cut, sample=wjetsSample, style=style_WJets, weight={'string':'weight'}) 
    MC_TTJETS  = plot(var, binning, cut, sample=ttJetsPowHeg, style=style_TTJets, weight={'string':'weight'})
    
  #  plotLists = [[MC_WJETS]]
    plotLists = [[MC_TTJETS, MC_WJETS]]
    for s in signals:
      plotLists.append([plot(var, binning, cut, sample=s, style=s['style'], weight={'string':'weight'})])

    opt = {'yHeadRoomFac':12, 'labels':labels, 'logX':False, 'logY':True, 'yRange':[0.007, None], 'ratio':ratioOps, 'fileName':var['name']}
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
    return res

  allStacks=[]

  met_stack  = getStack(
      labels={'x':'#slash{E}_{T} (GeV)','y':'Number of Events / 50 GeV'}, 
      var={'name':'met','var':'met', 'overFlow':'upper'}, 
      binning={'binning':[1050/50,0,1050]}, 
      cut={'string':cutString,'func':None})
  allStacks.append(met_stack)

  ht_stack  = getStack(
      labels={'x':'H_{T} (GeV)','y':'Number of Events / 50 GeV'}, 
      var={'name':'ht','var':'htJet40ja', 'overFlow':'upper'}, 
      binning={'binning':[1650/50,0,1650]}, 
      cut={'string':cutString,'func':None})
  allStacks.append(ht_stack)

  st_stack  = getStack(
      labels={'x':'S_{T} (GeV)','y':'Number of Events / 50 GeV'}, 
      var={'name':'st','var':cmgST, 'overFlow':'upper'}, 
      binning={'binning':[750/50,0,750]}, 
      cut={'string':cutString,'func':None})
  allStacks.append(st_stack)

  leptonPt_stack  = getStack(
      labels={'x':'p_{T}(l) (GeV)','y':'Number of Events / 20 GeV'}, 
      var={'name':'leptonPt','var':'leptonPt', 'overFlow':'upper'}, 
      binning={'binning':[750/20,0,760]}, 
      cut={'string':cutString,'func':None})
  allStacks.append(leptonPt_stack)

  softleptonPt_stack  = getStack(
      labels={'x':'p_{T}(l) (GeV)','y':'Number of Events / 20 GeV'}, 
      var={'name':'softleptonPt','var':'leptonPt', 'overFlow':'upper'}, 
      binning={'binning':[20,0,100]}, 
      cut={'string':cutString,'func':None})
  allStacks.append(softleptonPt_stack)

  jet0pt_stack  = getStack(
      labels={'x':'p_{T}(leading jet) (GeV)','y':'Number of Events / 10 GeV'}, 
      var={'name':'jet0pt','var':'Jet_pt','ind':0, 'overFlow':'upper'}, 
      binning={'binning':[16,0,1600]}, 
      cut={'string':cutString,'func':None})
  allStacks.append(jet0pt_stack)
  jet1pt_stack  = getStack(
      labels={'x':'p_{T}(2^{nd.} leading jet) (GeV)','y':'Number of Events / 10 GeV'}, 
      var={'name':'jet1pt','var':'Jet_pt','ind':1, 'overFlow':'upper'}, 
      binning={'binning':[16,0,1600]}, 
      cut={'string':cutString,'func':None})
  allStacks.append(jet1pt_stack)
  jet2pt_stack  = getStack(
      labels={'x':'p_{T}(3^{rd.} leading jet) (GeV)','y':'Number of Events / 10 GeV'}, 
      var={'name':'jet2pt','var':'Jet_pt','ind':2, 'overFlow':'upper'}, 
      binning={'binning':[16,0,1600]}, 
      cut={'string':cutString,'func':None})
  allStacks.append(jet2pt_stack)
  jet3pt_stack  = getStack(
      labels={'x':'p_{T}(4^{th.} leading jet) (GeV)','y':'Number of Events / 10 GeV'}, 
      var={'name':'jet3pt','var':'Jet_pt','ind':3, 'overFlow':'upper'}, 
      binning={'binning':[16,0,1600]}, 
      cut={'string':cutString,'func':None})
  allStacks.append(jet3pt_stack)
  jet4pt_stack  = getStack(
      labels={'x':'p_{T}(5^{th.} leading jet) (GeV)','y':'Number of Events / 10 GeV'}, 
      var={'name':'jet4pt','var':'Jet_pt','ind':4, 'overFlow':'upper'}, 
      binning={'binning':[16,0,1600]}, 
      cut={'string':cutString,'func':None})
  allStacks.append(jet4pt_stack)

  binningMTCoarse = [0,120,220,320,420,800]
  mT_stack  = getStack(
      labels={'x':'m_{T} (GeV)','y':'Number of Events / 10 GeV'}, 
      var={'name':'mT','var':cmgMT, 'overFlow':'upper'}, 
      binning={'binning':binningMTCoarse, 'isExplicit':True}, 
      cut={'string':cutString,'func':None})
  allStacks.append(mT_stack)

  dPhi_stack  = getStack(
      labels={'x':'#Delta#Phi(W,l)','y':'Number of Events'}, 
      var={'name':'dPhi','var':cmgDPhi, 'overFlow':'both'}, 
      binning={'binning':[0,0.5,1,1.5,pi], 'isExplicit':True}, 
      cut={'string':cutString,'func':None})
  allStacks.append(dPhi_stack)

  nbtags_stack  = getStack(
      labels={'x':'number of b-tags (CSVM)','y':'Number of Events'}, 
      var={'name':'nMediumBTags','var':"nBJetMedium25", 'overFlow':'upper'}, 
      binning={'binning':[10,0,10]}, 
      cut={'string':cutString,'func':None})
  allStacks.append(nbtags_stack)

  njets_stack  = getStack(
      labels={'x':'number of jets','y':'Number of Events'}, 
      var={'name':'njets','var':"nJet40a", 'overFlow':'upper'}, 
      binning={'binning':[18,0,18]}, 
      cut={'string':cutString,'func':None})
  allStacks.append(njets_stack)

  nLooseBTags_stack  = getStack(
      labels={'x':'number of b-tags (CSVL)','y':'Number of Events'}, 
      var={'name':'nLooseBTags','var':"nBJetLoose25", 'overFlow':'upper'}, 
      binning={'binning':[10,0,10]}, 
      cut={'string':cutString,'func':None})
  allStacks.append(nLooseBTags_stack)

  mTClosestJetMET_stack  = getStack(
      labels={'x':'m_{T, closest jet, #slash{E}_{T}} (GeV)','y':'Number of Events / 10 GeV'}, 
      var={'name':'mTClosestJetMET','var':cmgMTClosestJetMET, 'overFlow':'upper'}, 
      binning={'binning':(20,0,800), 'isExplicit':False}, 
      cut={'string':cutString,'func':None})
  allStacks.append(mTClosestJetMET_stack)

  mTClosestJetMET_zoomed_stack  = getStack(
      labels={'x':'m_{T, closest jet, #slash{E}_{T}} (GeV)','y':'Number of Events / 10 GeV'}, 
      var={'name':'mTClosestJetMET_zoomed','var':cmgMTClosestJetMET, 'overFlow':'upper'}, 
      binning={'binning':(40,0,400), 'isExplicit':False}, 
      cut={'string':cutString,'func':None})
  allStacks.append(mTClosestJetMET_zoomed_stack)

  mTClosestBJetMET_stack  = getStack(
      labels={'x':'m_{T, closest b-jet, #slash{E}_{T}} (GeV)','y':'Number of Events / 10 GeV'}, 
      var={'name':'mTClosestBJetMET','var':cmgMTClosestBJetMET, 'overFlow':'upper'}, 
      binning={'binning':binningMTCoarse, 'isExplicit':True}, 
      cut={'string':cutString,'func':None})
  allStacks.append(mTClosestBJetMET_stack)

  mTClosestBJetMET_zoomed_stack  = getStack(
      labels={'x':'m_{T, closest b-jet, #slash{E}_{T}} (GeV)','y':'Number of Events / 10 GeV'}, 
      var={'name':'mTClosestBJetMET_zoomed','var':cmgMTClosestBJetMET, 'overFlow':'upper'}, 
      binning={'binning':(40,0,400), 'isExplicit':False}, 
      cut={'string':cutString,'func':None})
  allStacks.append(mTClosestBJetMET_zoomed_stack)

  mTTopClosestJetMET_stack  = getStack(
      labels={'x':'m_{T, closest jet, #slash{E}_{T}}^{top} (GeV)','y':'Number of Events / 10 GeV'}, 
      var={'name':'mTTopClosestJetMET','var':cmgMTTopClosestJetMET, 'overFlow':'upper'}, 
      binning={'binning':[20,0,2000], 'isExplicit':False}, 
      cut={'string':cutString,'func':None})
  allStacks.append(mTTopClosestJetMET_stack)

  mTTopClosestJetMET_zoomed_stack  = getStack(
      labels={'x':'m_{T, closest jet, #slash{E}_{T}}^{top} (GeV)','y':'Number of Events / 10 GeV'}, 
      var={'name':'mTTopClosestJetMET_zoomed','var':cmgMTTopClosestJetMET, 'overFlow':'upper'}, 
      binning={'binning':[40,0,400], 'isExplicit':False}, 
      cut={'string':cutString,'func':None})
  allStacks.append(mTTopClosestJetMET_zoomed_stack)

  mTTopClosestBJetMET_stack  = getStack(
      labels={'x':'m_{T, closest b-jet, #slash{E}_{T}}^{top} (GeV)','y':'Number of Events / 10 GeV'}, 
      var={'name':'mTTopClosestBJetMET','var':cmgMTTopClosestBJetMET, 'overFlow':'upper'}, 
      binning={'binning':[20,0,2000], 'isExplicit':False}, 
      cut={'string':cutString,'func':None})
  allStacks.append(mTTopClosestBJetMET_stack)

  mTTopClosestBJetMET_zoomed_stack  = getStack(
      labels={'x':'m_{T, closest b-jet, #slash{E}_{T}}^{top} (GeV)','y':'Number of Events / 10 GeV'}, 
      var={'name':'mTTopClosestBJetMET_zoomed','var':cmgMTTopClosestBJetMET, 'overFlow':'upper'}, 
      binning={'binning':[20,0,400], 'isExplicit':False}, 
      cut={'string':cutString,'func':None})
  allStacks.append(mTTopClosestBJetMET_zoomed_stack)

  minDPhiBJet_stack  = getStack(
      labels={'x':'min#Delta#Phi(#slash{E}_{T},b-j_{1})','y':'Number of Events'}, 
      var={'name':'minDPhiBJet','var':cmgMinDPhiBJet, 'overFlow':'both'}, 
      binning={'binning':[20,0,pi], 'isExplicit':False}, 
      cut={'string':cutString,'func':None})
  allStacks.append(minDPhiBJet_stack)

  minDPhi3Jet_stack  = getStack(
      labels={'x':'min#Delta#Phi(#slash{E}_{T},j_{1,2,3})','y':'Number of Events'}, 
      var={'name':'minDPhi3Jet','var':cmgMinDPhiJet, 'overFlow':'both'}, 
      binning={'binning':[20,0,pi], 'isExplicit':False}, 
      cut={'string':cutString,'func':None})
  allStacks.append(minDPhi3Jet_stack)


  loopAndFill(allStacks)

  stuff=[]
  for stk in allStacks:
    stuff.append(drawNMStacks(1,1,[stk],         subdir+prefix+"_"+stk.options['fileName']))
