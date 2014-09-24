import ROOT
from array import array
from math import *
import os, copy, sys

ROOT.TH1F().SetDefaultSumw2()

from Workspace.HEPHYPythonTools.helpers import getObjFromFile
#from Workspace.RA4Analysis.simplePlotsCommon import *
from Workspace.RA4Analysis.simplePlotHelpers import plot, stack, loopAndFill, drawNMStacks
from helpers import *
from stage2Tuples import ttJetsCSA1450ns, WJetsHTToLNu

subdir = "/pngTMP/"
prefix = 'looseVeto'
#presel="met>250&&ht>750&&singleMuonic&&nbtags==0&&njets>=3&&Sum$(jetBTag>0.244&&abs(jetEta)<2.4)<=1"

prefix = 'mediumVeto-ht750-met350-6j'
presel="met>350&&ht>750&&singleMuonic&&nbtags==0&&njets>=6"

#prefix = 'mediumVeto'
#presel="met>250&&ht>750&&singleMuonic&&nbtags==0&&njets>=3"

cutString=presel
wjetsSample = WJetsHTToLNu
ttJetsPowHeg = ttJetsCSA1450ns

#ratioOps = {'yLabel':'A/B', 'numIndex':0, 'denIndex':1 ,'yRange':None, 'logY':False, 'color':ROOT.kBlack, 'yRange':(0.5,1.5)}
ratioOps = None 

def cutFunc(c):
  return True

def getStack(labels, var, binning, cut, options={}):
  
  style_WJets   = {'legendText':'W + Jets',         'style':"f", 'lineThickNess':0, 'errorBars':False, 'color':ROOT.kYellow, 'markerStyle':None, 'markerSize':None}
  style_TTJets =  {'legendText':'t#bar{t} + Jets',  'style':"f", 'linethickNess':0, 'errorBars':False, 'color':ROOT.kRed-3, 'markerStyle':None, 'markerSize':None}
  MC_WJETS   = plot(var, binning, cut, sample=wjetsSample, style=style_WJets, weight={'string':'weight'}) 
  MC_TTJETS  = plot(var, binning, cut, sample=ttJetsPowHeg, style=style_TTJets, weight={'string':'weight'})
  
  plotLists = [[MC_WJETS, MC_TTJETS]]
  opt = {'labels':labels, 'logX':False, 'logY':True, 'yRange':None, 'ratio':ratioOps, 'fileName':var['name']}
  opt['texLines'] = [{'pos':(0.15, 0.95),'text':'CMS Simulation',        'options':{'size':0.045}},\
                     {'pos':(0.7, 0.95), 'text':'L=2fb{}^{-1} (13 TeV)', 'options':{'size':0.045}}]
  opt['legend'] = {'coordinates':[0.6,0.95 - len(plotLists)*0.08,.98,.93],'boxed':True}

  if options.has_key('ratio') and options['ratio']:
    options['texLines'] = [{'pos':(0.15, 0.95),'text':'CMS Simulation',        'options':{'size':0.045}},\
                           {'pos':(0.7, 0.95), 'text':'L=2fb{}^{-1} (13 TeV)', 'options':{'size':0.045}}]
    options['legend'] = {'coordinates':[0.6,0.95 - len(plotLists)*0.08,.98,.93],'boxed':True}
  else:
    options['texLines'] = [{'pos':(0.16, 0.965), 'text':'CMS Simulation',       'options':{'size':0.038}},\
                           {'pos':(0.7, 0.965),  'text':'L=2fb{}^{-1} (13 TeV)','options':{'size':0.038}}]
    options['legend'] = {'coordinates':[0.6,0.95 - len(plotLists)*0.1,.95,.95],'boxed':True}


  for k in options.keys():
    assert opt.has_key(k),"Stack option %s unknown!" %k
    opt[k]=options[k]
  res = stack(plotLists, options = opt)
  return res

allStacks=[]

met_stack  = getStack(
    labels={'x':'p_{T}(l) (GeV)','y':'Number of Events / 10 GeV'}, 
    var={'name':'met','var':'met', 'overFlow':'upper'}, 
    binning={'binning':[21,300,720]}, 
    cut={'string':cutString,'func':None})
allStacks.append(met_stack)

jet0pt_stack  = getStack(
    labels={'x':'p_{T}(leading jet) (GeV)','y':'Number of Events / 10 GeV'}, 
    var={'name':'jet0pt','var':'jetPt','ind':0, 'overFlow':'upper'}, 
    binning={'binning':[29,200,1650]}, 
    cut={'string':cutString,'func':None})
allStacks.append(jet0pt_stack)

leptonPt_stack  = getStack(
    labels={'x':'p_{T}(l) (GeV)','y':'Number of Events / 10 GeV'}, 
    var={'name':'leptonPt','var':'leptonPt', 'overFlow':'upper'}, 
    binning={'binning':[21,0,420]}, 
    cut={'string':cutString,'func':None})
allStacks.append(leptonPt_stack)

binningMTCoarse = [0,120,220,320,420,800]
mT_stack  = getStack(
    labels={'x':'m_{T} (GeV)','y':'Number of Events / 10 GeV'}, 
    var={'name':'mT','var':stage2MT, 'overFlow':'upper'}, 
    binning={'binning':binningMTCoarse, 'isExplicit':True}, 
    cut={'string':cutString,'func':None},
    options={'yRange':[0.2,None]})
allStacks.append(mT_stack)

nbtags_stack  = getStack(
    labels={'x':'number of b-tags (CSVM)','y':'Number of Events'}, 
    var={'name':'nMediumBTags','var':"ROOT.TTreeFormula('nCSVMTags', 'Sum$(jetBTag>0.679&&abs(jetEta)<2.4)', c)", 'overFlow':'upper'}, 
    binning={'binning':[10,0,10]}, 
    cut={'string':cutString,'func':None},
    options={'yRange':[0.07,None]})
allStacks.append(nbtags_stack)

nLooseBTags_stack  = getStack(
    labels={'x':'number of b-tags (CSVL)','y':'Number of Events'}, 
    var={'name':'nLooseBTags','var':"ROOT.TTreeFormula('nCSVLTags', 'Sum$(jetBTag>0.244&&abs(jetEta)<2.4)', c)", 'overFlow':'upper'}, 
    binning={'binning':[10,0,10]}, 
    cut={'string':cutString,'func':None},
    options={'yRange':[0.07,None]})
allStacks.append(nLooseBTags_stack)


loopAndFill(allStacks)

stuff=[]
for stk in allStacks:
  stuff.append(drawNMStacks(1,1,[stk],         subdir+prefix+"_"+stk.options['fileName']))
