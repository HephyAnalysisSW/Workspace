import ROOT
from array import array
from math import *
import os, copy, sys

ROOT.TH1F().SetDefaultSumw2()

from Workspace.RA4Analysis.simplePlotHelpers import plot, stack, loopAndFill, drawNMStacks

from Workspace.METAnalysis.cmgTuples_hcalStudy import *

from localInfo import afsuser
subdir = "/pngHCAL/"
small = False
cutFunc=None

#prefix = 'met150'
#presel= "HLT_HT750&&met_pt>150"

prefix = 'lepVeto'
presel= "HLT_HT750&&Sum$(LepGood_pt>10)==0"

#'HLT_HT750&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=2&&Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>750'
#'           Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=2&&Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>=750&&HLT_HT750==1
cutString=presel

usedBranches = ["*"]

def getStack(labels, var, binning, cut, options={}):

  style_hltht750   = {'legendText':'HLT_HT750',         'style':"l", 'lineThickness':1, 'errorBars':False, 'color':ROOT.kGray, 'markerStyle':None, 'markerSize':None}
  style_filters    = {'legendText':'filters',    'style':"l", 'linethickNess':1, 'errorBars':False, 'color':ROOT.kRed,  'markerStyle':None, 'markerSize':None}
  style_2jht750    = {'legendText':'H_{T}>750, n_{j}#geq 2',    'style':"l", 'linethickNess':1, 'errorBars':False, 'color':ROOT.kBlack,  'markerStyle':None, 'markerSize':None}
  style_met150     = {'legendText':'#slash{E}_{T}>150',    'style':"l", 'linethickNess':1, 'errorBars':False, 'color':ROOT.kBlue,  'markerStyle':None, 'markerSize':None}
  MC_hltht750        = plot(var, binning, cut, sample=JetHT_HcalExtValid_jet2012D_v2, style=style_hltht750, weight=None)
  
  filters="Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_ecalLaserCorrFilter&&Flag_hcalLaserEventFilter&&Flag_trackingFailureFilter&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_eeBadScFilter"
  MC_filters   = plot(var, binning, {'string':"&&".join([cut['string'],filters]),'func':None}, \
                       sample=JetHT_HcalExtValid_jet2012D_v2, style=style_filters, weight=None)

  htnjCut = "Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=2&&Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>750"
  MC_2jht750   = plot(var, binning, {'string':"&&".join([cut['string'],filters, htnjCut]),'func':None}, \
                       sample=JetHT_HcalExtValid_jet2012D_v2, style=style_2jht750, weight=None)
#  metCut = "met_pt>150"
#  MC_met150   = plot(var, binning, {'string':"&&".join([cut['string'],filters, htnjCut, metCut]),'func':None}, \
#                       sample=JetHT_HcalExtValid_jet2012D_v2, style=style_met150, weight=None)


  plotLists = [[MC_hltht750], [MC_filters],[MC_2jht750]]
#  plotLists = [[MC_2jht750], [MC_hltht750]]

  for pL in plotLists:
    for p in pL:
      p.sample['small']=small

  opt = {'small':small, 'yHeadRoomFac':12, 'labels':labels, 'logX':False, 'logY':True, 'yRange':[0.7, "auto"], 'ratio':None, 'fileName':var['name']}
  if options.has_key('ratio') and options['ratio']:
    opt['texLines'] = [{'pos':(0.15, 0.95),'text':'HCAL validation',        'options':{'size':0.045}},\
                       {'pos':(0.7, 0.95), 'text':'JetHT dataset', 'options':{'size':0.045}}]
    opt['legend'] = {'coordinates':[0.5,0.95 - len(plotLists)*0.08,.98,.93],'boxed':True}
  else:
    opt['texLines'] = [{'pos':(0.16, 0.965), 'text':'HCAL validation',       'options':{'size':0.038}},\
                       {'pos':(0.7, 0.965),  'text':'JetHT dataset','options':{'size':0.038}}]
    opt['legend'] = {'coordinates':[0.5,0.95 - len(plotLists)*0.08,.95,.95],'boxed':True}

  for k in options.keys():
    assert opt.has_key(k),"Stack option %s unknown!" %k
    opt[k]=options[k]
  res = stack(plotLists, options = opt)
  res.usedBranches = usedBranches
  return res

allStacks=[]

met_stack  = getStack(
    labels={'x':'#slash{E}_{T} (GeV)','y':'Number of Events / 5 GeV'},
    var={'name':'met_pt','leaf':'met_pt', 'overFlow':'upper'},
    binning={'binning':[950/5,0,950]},
    cut={'string':cutString,'func':cutFunc},
    )
allStacks.append(met_stack)

ht_stack  = getStack(
    labels={'x':'H_{T} (GeV)','y':'Number of Events / 10 GeV'},
#    var={'name':'ht','leaf':'htJet40ja', 'overFlow':'upper'},
    var={'name':'ht','TTreeFormula':'Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))', 'overFlow':'upper'},
    binning={'binning':[4900/10,0,4900]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(ht_stack)

jet0pt_stack  = getStack(
    labels={'x':'p_{T}(leading jet) (GeV)','y':'Number of Events / 10 GeV'},
    var={'name':'jet0pt','leaf':'Jet_pt','ind':0, 'overFlow':'upper'},
    binning={'binning':[1600/10,0,1600]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(jet0pt_stack)
jet1pt_stack  = getStack(
    labels={'x':'p_{T}(2^{nd.} leading jet) (GeV)','y':'Number of Events / 10 GeV'},
    var={'name':'jet1pt','leaf':'Jet_pt','ind':1, 'overFlow':'upper'},
    binning={'binning':[1600/10,0,1600]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(jet1pt_stack)
jet2pt_stack  = getStack(
    labels={'x':'p_{T}(3^{rd.} leading jet) (GeV)','y':'Number of Events / 10 GeV'},
    var={'name':'jet2pt','leaf':'Jet_pt','ind':2, 'overFlow':'upper'},
    binning={'binning':[800/10,0,800]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(jet2pt_stack)
jet3pt_stack  = getStack(
    labels={'x':'p_{T}(4^{th.} leading jet) (GeV)','y':'Number of Events / 10 GeV'},
    var={'name':'jet3pt','leaf':'Jet_pt','ind':3, 'overFlow':'upper'},
    binning={'binning':[800/10,0,800]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(jet3pt_stack)
jet4pt_stack  = getStack(
    labels={'x':'p_{T}(5^{th.} leading jet) (GeV)','y':'Number of Events / 10 GeV'},
    var={'name':'jet4pt','leaf':'Jet_pt','ind':4, 'overFlow':'upper'},
    binning={'binning':[800/10,0,800]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(jet4pt_stack)


jet0neHEF_stack  = getStack(
    labels={'x':'neutral had. ef','y':'Number of Events'},
    var={'name':'jet0neHEF','leaf':'Jet_neHEF','ind':0, 'overFlow':'upper'},
    binning={'binning':[100,0,1]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(jet0neHEF_stack)
jet1neHEF_stack  = getStack(
    labels={'x':'neutral had. ef','y':'Number of Events'},
    var={'name':'jet1neHEF','leaf':'Jet_neHEF','ind':1, 'overFlow':'upper'},
    binning={'binning':[100,0,1]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(jet1neHEF_stack)

maxJetneHEF_stack  = getStack(
    labels={'x':'max(Jet_neHEF) for p_{T,j}>100','y':'Number of Events'},
#    var={'name':'ht','leaf':'htJet40ja', 'overFlow':'upper'},
    var={'name':'maxJetneHEF','TTreeFormula':'Max$(Jet_neHEF*(Jet_pt>100&&abs(Jet_eta)<2.4&&Jet_id))', 'overFlow':'upper'},
    binning={'binning':[100,0,1]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(maxJetneHEF_stack)

loopAndFill(allStacks)

stuff=[]
for stk in allStacks:
  stuff.append(drawNMStacks(1,1,[stk],         subdir+prefix+"_"+stk.options['fileName']))
