import ROOT
from array import array
from math import *
import os, copy, sys

ROOT.TH1F().SetDefaultSumw2()

from Workspace.HEPHYPythonTools.helpers import getObjFromFile
#from Workspace.RA4Analysis.simplePlotsCommon import *
from Workspace.RA4Analysis.simplePlotHelpers import plot, stack, loopAndFill, drawNMStacks
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v5_Phys14V2 import *
small = False
mode = 'hard'

#prefix = 'mTSel_ht500-met250-6j-0b-diLepVeto'
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&met_pt>250&&htJet40ja>500&&nBJetMedium25==0&&nJet40a>=6"

#prefix = 'ht500-st250-4j-0b-diLepVeto'
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&st>250&&htJet40ja>500&&nBJetMedium25==0&&nJet40a>=4"

#prefix = 'ht500-st250-4j-geq1b-diLepVeto'
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&st>250&&htJet40ja>500&&nBJetMedium25>=1&&nJet40a>=4"

signalScale=1
#prefix = 'ht400-st250-1j-0b-diLepVeto'
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&st>250&&htJet40ja>400&&nBJetMedium25==0&&nJet40a>=1"

cutBranches = ["weight", "single*", "nLoose*", "nTight*", "leptonPt", "met_phi", \
               "htJet40ja", "nBJetMedium25", "nJet40a",'st','met', 'Jet_pt', 'Jet_btagCMVA', "Jet_id"]
subdir = "/pngCMG2/"+mode+'/'

def dPhi1(c): return cmgDPhi(c)>1.

cutFunc=None
prefix = mode+'_mu_ht500-st200-6j-2j80-0b-diLepVeto'
presel="singleMuonic&&nLooseSoftLeptons==0&&nTightHardLeptons==1&&nLooseHardLeptons==1&&st>200"\
      +"&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCMVA>0.732)==0"\
      +"&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=6"\
      +"&&Sum$(Jet_pt>80&&abs(Jet_eta)<2.4&&Jet_id)>=2"\
      +"&&Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>=500"\
#      +"&&Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))<1000"\

#cutFunc=dPhi1
#prefix = mode+'_eleMu_ht500-750-st200-6j-2j80-0b-dPhi1-diLepVeto'
#presel="singleMuonic&&nLooseSoftLeptons==0&&nTightHardLeptons==1&&nLooseHardLeptons==1&&st>200"\
#      +"&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCMVA>0.732)==0"\
#      +"&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=6"\
#      +"&&Sum$(Jet_pt>80&&abs(Jet_eta)<2.4&&Jet_id)>=2"\
#      +"&&Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>=1000"\
##      +"&&Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))<750"\

#cutFunc=dPhi1
#prefix = mode+'_eleMu_ht1000-st200-6j-2j80-0b-dPhi1-diLepVeto'
#presel="singleMuonic&&nLooseSoftLeptons==0&&nTightHardLeptons==1&&nLooseHardLeptons==1&&st>200"\
#      +"&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCMVA>0.732)==0"\
#      +"&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=6"\
#      +"&&Sum$(Jet_pt>80&&abs(Jet_eta)<2.4&&Jet_id)>=2"\
#      +"&&Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>=1000"\
##      +"&&Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))<750"\
#
#cutFunc=dPhi1
#prefix = mode+'_eleMu_ht500-st200-6j-2j80-0b-dPhi1-diLepVeto'
#presel="singleMuonic&&nLooseSoftLeptons==0&&nTightHardLeptons==1&&nLooseHardLeptons==1&&st>200"\
#      +"&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCMVA>0.732)==0"\
#      +"&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=6"\
#      +"&&Sum$(Jet_pt>80&&abs(Jet_eta)<2.4&&Jet_id)>=2"\
#      +"&&Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>=500"\
##      +"&&Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))<750"\

cutString=presel

signalPrefix="" if signalScale==1 else str(signalScale)+"x "
#  #HARD
if mode=='hard':
  SMS_T5qqqqWW_Gl1200_Chi1000_LSP800['hard']['style'] \
      = {'legendText':"T5q^{4} (1.2/1/0.8)",   'style':"l", 'lineThickness':2, 'errorBars':False, 'color':ROOT.kRed, 'markerStyle':None, 'markerSize':None}
  SMS_T5qqqqWW_Gl1500_Chi800_LSP100['hard']['style']  \
      = {'legendText':"T5q^{4} (1.5/0.8/0.1)",   'style':"l", 'lineThickness':2, 'errorBars':False, 'color':ROOT.kBlack, 'markerStyle':None, 'markerSize':None}
  #  T1tttt_2J_mGo1300_mStop300_mCh285_mChi280['style']  = {'legendText':signalPrefix+T1tttt_2J_mGo1300_mStop300_mCh285_mChi280['name'],   'style':"l", 'lineThickness':2, 'errorBars':False, 'color':ROOT.kGreen, 'markerStyle':None, 'markerSize':None}
  #  signals = [SMS_T5qqqqWW_Gl1200_Chi1000_LSP800['hard'], SMS_T5qqqqWW_Gl1500_Chi800_LSP100['hard'], T1tttt_2J_mGo1300_mStop300_mCh285_mChi280]
  signals = [SMS_T5qqqqWW_Gl1200_Chi1000_LSP800['hard'], SMS_T5qqqqWW_Gl1500_Chi800_LSP100['hard']]
#  hard_T6qqWW_Sq_950_LSP_300_Chi_350['style'] = {'legendText':signalPrefix+hard_T6qqWW_Sq_950_LSP_300_Chi_350['name'],   'style':"l", 'lineThickness':2, 'errorBars':False, 'color':ROOT.kBlue, 'markerStyle':None, 'markerSize':None}
#  hard_T5qqqqWW_Gl_1400_LSP_300_Chi_315['style']  = {'legendText':signalPrefix+hard_T5qqqqWW_Gl_1400_LSP_300_Chi_315['name'],   'style':"l", 'lineThickness':2, 'errorBars':False, 'color':ROOT.kBlack, 'markerStyle':None, 'markerSize':None}
#  hard_T1tttt_2J_mGo1300_mStop300_mCh285_mChi280['style']  = {'legendText':signalPrefix+hard_T1tttt_2J_mGo1300_mStop300_mCh285_mChi280['name'],   'style':"l", 'lineThickness':2, 'errorBars':False, 'color':ROOT.kGreen, 'markerStyle':None, 'markerSize':None}
#  signals = [hard_T6qqWW_Sq_950_LSP_300_Chi_350, hard_T5qqqqWW_Gl_1400_LSP_300_Chi_315, hard_T1tttt_2J_mGo1300_mStop300_mCh285_mChi280]

for s in signals:
  s['scale'] = signalScale
#ratioOps = {'yLabel':'A/B', 'numIndex':0, 'denIndex':1 ,'yRange':None, 'logY':False, 'color':ROOT.kBlack, 'yRange':(0.5,1.5)}
ratioOps = None


def getStack(labels, var, binning, cut, options={}):

  style_WJetsHTToLNu = {'legendText':'W + Jets',         'style':"f", 'lineThickness':0, 'errorBars':False, 'color':color("WJetsHTToLNu"), 'markerStyle':None, 'markerSize':None}
  style_TTJets       = {'legendText':'t#bar{t} + Jets',  'style':"f", 'linethickNess':0, 'errorBars':False, 'color':color("TTJets"), 'markerStyle':None, 'markerSize':None}
  style_DY           = {'legendText':'DY + Jets',  'style':"f", 'linethickNess':0, 'errorBars':False,       'color':color("DY"), 'markerStyle':None, 'markerSize':None}
  style_TTVH         = {'legendText':'t#bar{t} + W/Z/H',  'style':"f", 'linethickNess':0, 'errorBars':False, 'color':color("TTVH"), 'markerStyle':None, 'markerSize':None}
  style_QCD          = {'legendText':'QCD',  'style':"f", 'linethickNess':0, 'errorBars':False,             'color':color("QCD"), 'markerStyle':None, 'markerSize':None}
  style_singleTop    = {'legendText':'single top',  'style':"f", 'linethickNess':0, 'errorBars':False,      'color':color("singleTop"), 'markerStyle':None, 'markerSize':None}
  MC_TTJets          = plot(var, binning, cut, sample=ttJets[mode], style=style_TTJets, weight={'string':'weight'})
  MC_WJetsHTToLNu    = plot(var, binning, cut, sample=WJetsHTToLNu[mode], style=style_WJetsHTToLNu, weight={'string':'weight'})
  MC_DY              = plot(var, binning, cut, sample=DY[mode], style=style_DY, weight={'string':'weight'})
  MC_TTVH              = plot(var, binning, cut, sample=TTVH[mode], style=style_TTVH, weight={'string':'weight'})
  MC_singleTop       = plot(var, binning, cut, sample=singleTop[mode], style=style_singleTop, weight={'string':'weight'})
  MC_QCD             = plot(var, binning, cut, sample=QCD[mode], style=style_QCD, weight={'string':'weight'})

  plotLists = [[MC_TTJets, MC_singleTop, MC_WJetsHTToLNu, MC_DY, MC_TTVH,  MC_QCD]]
  for s in signals:
    plotLists.append([plot(var, binning, cut, sample=s, style=s['style'], weight={'string':'weight'})])

  for pL in plotLists:
    for p in pL:
      p.sample['small']=small

  opt = {'small':small, 'yHeadRoomFac':12, 'labels':labels, 'logX':False, 'logY':True, 'yRange':[0.007, "auto"], 'ratio':ratioOps, 'fileName':var['name']}
#  opt['texLines'] = [{'pos':(0.15, 0.95),'text':'CMS Simulation',        'options':{'size':0.045}},\
#                     {'pos':(0.7, 0.95), 'text':'L=4fb{}^{-1} (13 TeV)', 'options':{'size':0.045}}]
#  opt['legend'] = {'coordinates':[0.6,0.95 - len(plotLists)*0.09,.98,.93],'boxed':True}
  if options.has_key('ratio') and options['ratio']:
    opt['texLines'] = [{'pos':(0.15, 0.95),'text':'CMS Simulation',        'options':{'size':0.045}},\
                       {'pos':(0.7, 0.95), 'text':'L=4fb{}^{-1} (13 TeV)', 'options':{'size':0.045}}]
    opt['legend'] = {'coordinates':[0.55,0.95 - len(plotLists)*0.09,.98,.93],'boxed':True}
  else:
    opt['texLines'] = [{'pos':(0.16, 0.965), 'text':'CMS Simulation',       'options':{'size':0.038}},\
                       {'pos':(0.7, 0.965),  'text':'L=4fb{}^{-1} (13 TeV)','options':{'size':0.038}}]
    opt['legend'] = {'coordinates':[0.55,0.95 - len(plotLists)*0.09,.95,.95],'boxed':True}

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
    cut={'string':cutString,'func':cutFunc},
    )
allStacks.append(met_stack)

ht_stack  = getStack(
    labels={'x':'H_{T} (GeV)','y':'Number of Events / 100 GeV'},
#    var={'name':'ht','leaf':'htJet40ja', 'overFlow':'upper'},
    var={'name':'ht','TTreeFormula':'Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))', 'overFlow':'upper'},
    binning={'binning':[2600/100,0,2600]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(ht_stack)

st_stack  = getStack(
    labels={'x':'S_{T} (GeV)','y':'Number of Events / 50 GeV'},
    var={'name':'st','func':cmgST, 'branches':cmgST('branches'), 'overFlow':'upper'},
    binning={'binning':[1500/50,0,1500]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(st_stack)

leptonPt_stack  = getStack(
    labels={'x':'p_{T}(l) (GeV)','y':'Number of Events / 20 GeV'},
    var={'name':'leptonPt','leaf':'leptonPt', 'overFlow':'upper'},
    binning={'binning':[750/20,0,760]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(leptonPt_stack)

leptonEta_stack  = getStack(
    labels={'x':'#eta(l)','y':'Number of Events'},
    var={'name':'leptonEta','leaf':'leptonEta', 'overFlow':'both'},
    binning={'binning':[24,-2.4,2.4]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(leptonEta_stack)

softleptonPt_stack  = getStack(
    labels={'x':'p_{T}(l) (GeV)','y':'Number of Events / 20 GeV'},
    var={'name':'softleptonPt','leaf':'leptonPt', 'overFlow':'upper'},
    binning={'binning':[20,0,100]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(softleptonPt_stack)

jet0pt_stack  = getStack(
    labels={'x':'p_{T}(leading jet) (GeV)','y':'Number of Events / 10 GeV'},
    var={'name':'jet0pt','leaf':'Jet_pt','ind':0, 'overFlow':'upper'},
    binning={'binning':[16,0,1600]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(jet0pt_stack)
jet1pt_stack  = getStack(
    labels={'x':'p_{T}(2^{nd.} leading jet) (GeV)','y':'Number of Events / 10 GeV'},
    var={'name':'jet1pt','leaf':'Jet_pt','ind':1, 'overFlow':'upper'},
    binning={'binning':[16,0,1600]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(jet1pt_stack)
jet2pt_stack  = getStack(
    labels={'x':'p_{T}(3^{rd.} leading jet) (GeV)','y':'Number of Events / 10 GeV'},
    var={'name':'jet2pt','leaf':'Jet_pt','ind':2, 'overFlow':'upper'},
    binning={'binning':[16,0,1600]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(jet2pt_stack)
jet3pt_stack  = getStack(
    labels={'x':'p_{T}(4^{th.} leading jet) (GeV)','y':'Number of Events / 10 GeV'},
    var={'name':'jet3pt','leaf':'Jet_pt','ind':3, 'overFlow':'upper'},
    binning={'binning':[16,0,1600]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(jet3pt_stack)
jet4pt_stack  = getStack(
    labels={'x':'p_{T}(5^{th.} leading jet) (GeV)','y':'Number of Events / 10 GeV'},
    var={'name':'jet4pt','leaf':'Jet_pt','ind':4, 'overFlow':'upper'},
    binning={'binning':[16,0,1600]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(jet4pt_stack)

binningMTCoarse = [0,120,220,320,420,800]
mT_stack  = getStack(
    labels={'x':'m_{T} (GeV)','y':'Number of Events / 10 GeV'},
    var={'name':'mT','func':cmgMT, 'branches':cmgMT('branches'), 'overFlow':'upper'},
    binning={'binning':binningMTCoarse, 'isExplicit':True},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(mT_stack)
mT_stack_zoomed  = getStack(
    labels={'x':'m_{T} (GeV)','y':'Number of Events / 10 GeV'},
    var={'name':'mTzoomed','func':cmgMT, 'branches':cmgMT('branches'), 'overFlow':'upper'},
    binning={'binning':[15,0,300], 'isExplicit':False},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(mT_stack_zoomed)

dPhi_stack  = getStack(
    labels={'x':'#Delta#Phi(W,l)','y':'Number of Events'},
    var={'name':'dPhi','func':cmgDPhi, 'branches':cmgDPhi('branches'), 'overFlow':'both'},
    binning={'binning':[0,0.5,1,1.5,pi], 'isExplicit':True},
    cut={'string':cutString,'func':cutFunc})
#dPhi_stack.options['yRange']=[0.007, 10**2.7]
allStacks.append(dPhi_stack)

dPhiZoomed_stack  = getStack(
    labels={'x':'#Delta#Phi(W,l)','y':'Number of Events'},
    var={'name':'dPhizoomed','func':cmgDPhi, 'branches':cmgDPhi('branches'), 'overFlow':'both'},
    binning={'binning':[20, 0,pi], 'isExplicit':False},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(dPhiZoomed_stack)

nbtags_stack  = getStack(
    labels={'x':'number of b-tags (CSVM)','y':'Number of Events'},
    var={'name':'nMediumBTags','leaf':"nBJetMedium25", 'overFlow':'upper'},
    binning={'binning':[10,0,10]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(nbtags_stack)

njets_stack  = getStack(
    labels={'x':'number of jets','y':'Number of Events'},
#    var={'name':'njets','leaf':"nJet40a", 'overFlow':'upper'},
    var={'name':'njets','TTreeFormula':'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)', 'overFlow':'upper'},
    binning={'binning':[18,0,18]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(njets_stack)

nLooseBTags_stack  = getStack(
    labels={'x':'number of b-tags (CSVL)','y':'Number of Events'},
    var={'name':'nLooseBTags','leaf':"nBJetLoose25", 'overFlow':'upper'},
    binning={'binning':[10,0,10]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(nLooseBTags_stack)

mTClosestJetMET_stack  = getStack(
    labels={'x':'m_{T, closest jet, #slash{E}_{T}} (GeV)','y':'Number of Events / 10 GeV'},
    var={'name':'mTClosestJetMET','func':cmgMTClosestJetMET, 'overFlow':'upper', 'branches':cmgMTClosestJetMET('branches')},
    binning={'binning':(20,0,800), 'isExplicit':False},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(mTClosestJetMET_stack)

mTClosestJetMET_zoomed_stack  = getStack(
    labels={'x':'m_{T, closest jet, #slash{E}_{T}} (GeV)','y':'Number of Events / 10 GeV'},
    var={'name':'mTClosestJetMET_zoomed','func':cmgMTClosestJetMET, 'branches':cmgMTClosestJetMET('branches'),'overFlow':'upper'},
    binning={'binning':(40,0,400), 'isExplicit':False},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(mTClosestJetMET_zoomed_stack)

#  mTClosestBJetMET_stack  = getStack(
#      labels={'x':'m_{T, closest b-jet, #slash{E}_{T}} (GeV)','y':'Number of Events / 10 GeV'},
#      var={'name':'mTClosestBJetMET','func':cmgMTClosestBJetMET,'branches':cmgMTClosestBJetMET('branches'), 'overFlow':'upper'},
#      binning={'binning':binningMTCoarse, 'isExplicit':True},
#      cut={'string':cutString,'func':cutFunc})
#  allStacks.append(mTClosestBJetMET_stack)
#
#  mTClosestBJetMET_zoomed_stack  = getStack(
#      labels={'x':'m_{T, closest b-jet, #slash{E}_{T}} (GeV)','y':'Number of Events / 10 GeV'},
#      var={'name':'mTClosestBJetMET_zoomed','func':cmgMTClosestBJetMET,'branches':cmgMTClosestBJetMET('branches'), 'overFlow':'upper'},
#      binning={'binning':(40,0,400), 'isExplicit':False},
#      cut={'string':cutString,'func':cutFunc})
#  allStacks.append(mTClosestBJetMET_zoomed_stack)

#  mTTopClosestBJetMET_stack  = getStack(
#      labels={'x':'m_{T, closest b-jet, #slash{E}_{T}}^{top} (GeV)','y':'Number of Events / 10 GeV'},
#      var={'name':'mTTopClosestBJetMET','func':cmgMTTopClosestBJetMET, 'branches':cmgMTTopClosestBJetMET('branches'), 'overFlow':'upper'},
#      binning={'binning':[20,0,2000], 'isExplicit':False},
#      cut={'string':cutString,'func':cutFunc})
#  allStacks.append(mTTopClosestBJetMET_stack)
#
#  mTTopClosestBJetMET_zoomed_stack  = getStack(
#      labels={'x':'m_{T, closest b-jet, #slash{E}_{T}}^{top} (GeV)','y':'Number of Events / 10 GeV'},
#      var={'name':'mTTopClosestBJetMET_zoomed','func':cmgMTTopClosestBJetMET, 'branches':cmgMTTopClosestBJetMET('branches'), 'overFlow':'upper'},
#      binning={'binning':[20,0,400], 'isExplicit':False},
#      cut={'string':cutString,'func':cutFunc})
#  allStacks.append(mTTopClosestBJetMET_zoomed_stack)

#  minDPhiBJet_stack  = getStack(
#      labels={'x':'min#Delta#Phi(#slash{E}_{T},b-j_{1})','y':'Number of Events'},
#      var={'name':'minDPhiBJet','func':cmgMinDPhiBJet, 'branches':cmgMinDPhiJet('branches'), 'overFlow':'both'},
#      binning={'binning':[20,0,pi], 'isExplicit':False},
#      cut={'string':cutString,'func':cutFunc})
#  allStacks.append(minDPhiBJet_stack)

mTTopClosestJetMET_stack  = getStack(
    labels={'x':'m_{T, closest jet, #slash{E}_{T}}^{top} (GeV)','y':'Number of Events / 10 GeV'},
    var={'name':'mTTopClosestJetMET','func':cmgMTTopClosestJetMET, 'branches':cmgMTTopClosestJetMET('branches'), 'overFlow':'upper'},
    binning={'binning':[20,0,2000], 'isExplicit':False},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(mTTopClosestJetMET_stack)

mTTopClosestJetMET_zoomed_stack  = getStack(
    labels={'x':'m_{T, closest jet, #slash{E}_{T}}^{top} (GeV)','y':'Number of Events / 10 GeV'},
    var={'name':'mTTopClosestJetMET_zoomed','func':cmgMTTopClosestJetMET, 'branches':cmgMTTopClosestJetMET('branches'), 'overFlow':'upper'},
    binning={'binning':[40,0,400], 'isExplicit':False},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(mTTopClosestJetMET_zoomed_stack)

dPhiLeadingJet_stack  = getStack(
    labels={'x':'#Delta#Phi(#slash{E}_{T},j_{1})','y':'Number of Events'},
    var={'name':'dPhiLeadingJet','func':lambda c:cmgMinDPhiJet(c,1), 'branches':cmgMinDPhiJet('branches'), 'overFlow':'both'},
    binning={'binning':[20,0,pi], 'isExplicit':False},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(dPhiLeadingJet_stack)
minDPhi2Jet_stack  = getStack(
    labels={'x':'min#Delta#Phi(#slash{E}_{T},j_{1,2})','y':'Number of Events'},
    var={'name':'minDPhi2Jet','func':lambda c:cmgMinDPhiJet(c,2), 'branches':cmgMinDPhiJet('branches'), 'overFlow':'both'},
    binning={'binning':[20,0,pi], 'isExplicit':False},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(minDPhi2Jet_stack)
minDPhi3Jet_stack  = getStack(
    labels={'x':'min#Delta#Phi(#slash{E}_{T},j_{1,2,3})','y':'Number of Events'},
    var={'name':'minDPhi3Jet','func':lambda c:cmgMinDPhiJet(c,3), 'branches':cmgMinDPhiJet('branches'), 'overFlow':'both'},
    binning={'binning':[20,0,pi], 'isExplicit':False},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(minDPhi3Jet_stack)
minDPhi4Jet_stack  = getStack(
    labels={'x':'min#Delta#Phi(#slash{E}_{T},j_{1-4})','y':'Number of Events'},
    var={'name':'minDPhi4Jet','func':lambda c:cmgMinDPhiJet(c,4), 'branches':cmgMinDPhiJet('branches'), 'overFlow':'both'},
    binning={'binning':[20,0,pi], 'isExplicit':False},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(minDPhi4Jet_stack)

htOrthMET_stack  = getStack(
    labels={'x':'H_{T} (GeV)','y':'Number of Events / 50 GeV'},
    var={'name':'htOrthMET','func':cmgHTOrthMET, 'overFlow':'upper', 'branches':cmgHTOrthMET('branches')},
    binning={'binning':[1650/50,0,1650]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(htOrthMET_stack)

htRatio_stack  = getStack(
    labels={'x':'H_{T} (GeV)','y':'Number of Events / 50 GeV'},
    var={'name':'htRatio','func':cmgHTRatio, 'overFlow':'upper', 'branches':cmgHTRatio('branches')},
    binning={'binning':[20,0.4,1]},
    cut={'string':cutString,'func':cutFunc})
allStacks.append(htRatio_stack)

loopAndFill(allStacks)

stuff=[]
for stk in allStacks:
  stuff.append(drawNMStacks(1,1,[stk],         subdir+prefix+"_"+stk.options['fileName']))
