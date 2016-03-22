import ROOT
import pickle 
import copy, os, sys
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.TH1F().SetDefaultSumw2()
ROOT.setTDRStyle()
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
#from Workspace.RA4Analysis.signalRegions import *
#from draw_helpers import *
from math import *
from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed_antiSel import *
from Workspace.RA4Analysis.cmgTuples_Data_25ns_postProcessed_antiSel import *

preprefix = 'QCDestimation/final2p3fb/MC'
#wwwDir = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/RunII/Spring15_25ns/'+preprefix+'/'
wwwDir = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/RunII/Spring15_25ns/'+preprefix+'/'
prefix = ''
picklePath = '/data/dhandl/results2015/QCDEstimation/'
picklePresel = '20151216_QCDestimation_2p1fb_pkl'
picklePreselMC = '20151216_QCDestimation_MC2p1fb_pkl'
#pickleFit    = '20151201_fitResult_MC2p1fb_pkl'
#resEle = pickle.load(file(picklePath+picklePresel))
resEle = pickle.load(file('/data/dspitzbart/Results2016/QCDEstimation/20160212_QCDestimation_data2p25fb_pkl'))
#resEleMC = pickle.load(file(picklePath+picklePreselMC))
resEleMC = pickle.load(file('/data/dspitzbart/Results2016/QCDEstimation/20160212_QCDestimation_MC2p25fb_pkl'))
#fitRes = pickle.load(file(picklePath+pickleFit))

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

def makeWeight(lumi=3., sampleLumi=3.,debug=False):
  reWeight = 'lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*0.94*TopPtWeight'
  if debug:
    print 'No lumi-reweighting done!!'
    return 'weight', 'weight*weight'
  else:
    weight_str = '((weight/'+str(sampleLumi)+')*'+str(lumi)+'*'+reWeight+')'
    weight_err_str = '('+weight_str+'*'+weight_str+')'
    return weight_str, weight_err_str
lumi = 2.3
sampleLumi = 2.25
debugReweighting = True
weight_str, weight_err_str = makeWeight(lumi, sampleLumi=sampleLumi)

def getRCS(c, cut, dPhiCut, useWeight = True, weight = weight_str):
#  dPhiStr = 'acos((LepGood_pt+met_pt*cos(LepGood_phi-met_phi))/sqrt(LepGood_pt**2+met_pt**2+2*met_pt*LepGood_pt*cos(LepGood_phi-met_phi)))'
  dPhiStr = 'deltaPhi_Wl'
  if useWeight:
    h = getPlotFromChain(c, dPhiStr, [0,dPhiCut,pi], cutString=cut, binningIsExplicit=True, weight =  weight)
  else:
    h = getPlotFromChain(c, dPhiStr, [0,dPhiCut,pi], cutString=cut, binningIsExplicit=True, weight='(1)')
  h.Sumw2()
  if h.GetBinContent(1)>0:
    rcs = h.GetBinContent(2)/h.GetBinContent(1)
    if h.GetBinContent(2)>0:
      rCSE_sim = rcs*sqrt(h.GetBinError(2)**2/h.GetBinContent(2)**2 + h.GetBinError(1)**2/h.GetBinContent(1)**2)
      rCSE_pred = rcs*sqrt(1./h.GetBinContent(2) + 1./h.GetBinContent(1))
      del h
      return {'rCS':rcs, 'rCSE_pred':rCSE_pred, 'rCSE_sim':rCSE_sim}
    else:
      del h
      return {'rCS':rcs, 'rCSE_pred':float('nan'), 'rCSE_sim':float('nan')}
  else:
    del h
    return {'rCS':float('nan'), 'rCSE_pred':float('nan'), 'rCSE_sim':float('nan')}

def getFraction(Bkg, Bkg_err, QCD, QCD_err):
  try: res = QCD/Bkg
  except ZeroDivisionError: res = float('nan')
  try: res_err = res*sqrt(Bkg_err**2/Bkg**2 + QCD_err**2/QCD**2)
  except ZeroDivisionError: res_err = float('nan')
  return res, res_err

#trigger and filters for real Data
trigger = "&&(HLT_EleHT350||HLT_MuHT350)"
#filters = "&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter_fix&&Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter"
#filters = "&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter_fix&&Flag_HBHENoiseIsoFilter&&Flag_goodVertices&&Flag_eeBadScFilter"
filters = "&& Flag_CSCTightHaloFilter && Flag_HBHENoiseFilter_fix && Flag_HBHENoiseIsoFilter && Flag_goodVertices && Flag_eeBadScFilter"

preselMuon = 'nLep==1&&nVeto==0&&nMu==1&&leptonPt>25&&Jet2_pt>80'
preselEle = 'nLep==1&&nVeto==0&&nEl==1&&leptonPt>25&&Jet2_pt>80'
antiSelStrEle = preselEle+'&&Selected==-1'
SelStrEle = preselEle+'&&Selected==1'
antiSelStrMuon = preselMuon+'&&Selected==-1'
SelStrMuon = preselMuon+'&&Selected==1'

cQCD  = getChain(QCDHT_25ns,histname='')
cEWK  = getChain([WJetsHTToLNu_25ns, TTJets_combined_2, singleTop_25ns, DY_25ns, TTV_25ns],histname='')
cMC = getChain([WJetsHTToLNu_25ns, TTJets_combined_2, singleTop_25ns, DY_25ns, TTV_25ns, QCDHT_25ns], histname='')
cDataEle = getChain(single_ele_Run2015D , histname='')
cDataMuon = getChain(single_mu_Run2015D , histname='')

#define SR
inclusiveTemplate = {(3, 4): {(250,  -1): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}}}} #use inclusive LT,HT region to get the shape for the fit template

fitCR =  {(3, 4): {(250,  -1): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}},
                   (250, 350): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}}, #QCD CR exclusive in LT and inclusive in HT, where the fits are performed
                   (350,  -1): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}},
                   (350, 450): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}},
                   (450,  -1): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}}}}
CR = {
                (3, 4): {(250, 350): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}, #3-4jets W+jets control region
                                      (500, 750):  {(1.0):    {'deltaPhi': 1.0}},
                                      (750, -1):   {(1.0):    {'deltaPhi': 1.0}}},
                         (350, -1):  {(500, -1):   {(0.75):   {'deltaPhi': 0.75}}},
                         (350, 450): {(500, -1):   {(1.0):    {'deltaPhi': 1.0},
                                                    (0.75):   {'deltaPhi': 0.75}},
                                      (500, 750):  {(1.0):    {'deltaPhi': 1.0}},
                                      (750, -1):   {(1.0):    {'deltaPhi': 1.0}}},
                         (450, -1):  {(500, -1):   {(1.0):    {'deltaPhi': 1.0},
                                                    (0.75):   {'deltaPhi': 0.75}},
                                      (500, 750):  {(0.75):   {'deltaPhi': 0.75}},
                                      (750, -1):   {(0.75):   {'deltaPhi': 0.75}},
                                      (500, 1000): {(0.75):   {'deltaPhi': 0.75}},
                                      (1000, -1):  {(0.75):   {'deltaPhi': 0.75}}}}
}

signalRegion = {
                (3, 4): {
                         (250, 350): {(500,  -1): {(0,0): {'deltaPhi':1.0, 'label':['LT1','HTi','NB0','NJ34']}},  #3-4jets W+jets control region inclusive in LT
                                      (500, 750): {(0,0): {'deltaPhi':1.0, 'label':['LT1','HT1','NB0','NJ34']}}, 
                                      (750,  -1): {(0,0): {'deltaPhi':1.0, 'label':['LT1','HT2i','NB0','NJ34']}}},  
                         (350, -1):  {(500,  -1): {(0,0): {'deltaPhi':0.75, 'label':['LT2i','HTi','NB0','NJ34']}}},
                         (350, 450): {(500,  -1): {(0,0): {'deltaPhi':1.0, 'label':['LT2','HTi','NB0','NJ34']}},  
                                      (500, 750): {(0,0): {'deltaPhi':1.0, 'label':['LT2','HT1','NB0','NJ34']}}, 
                                      (750,  -1): {(0,0): {'deltaPhi':1.0, 'label':['LT2','HT2i','NB0','NJ34']}}},  
                         (450, -1):  {(500,  -1): {(0,0): {'deltaPhi':0.75, 'label':['LT3i','HTi','NB0','NJ34']}},  
                                      (500, 750): {(0,0): {'deltaPhi':0.75, 'label':['LT3i','HT1','NB0','NJ34']}}, 
                                      (750,  -1): {(0,0): {'deltaPhi':0.75, 'label':['LT3i','HT2i','NB0','NJ34']}}}},  
                (4, 5): {(250, 350): {(500,  -1): {(1,1): {'deltaPhi':1.0, 'label':['LT1','HTi','NB1','NJ45']}},  #4-5jets TTbar control region
                                      (500, 750): {(1,1): {'deltaPhi':1.0, 'label':['LT1','HT1','NB1','NJ45']}}, 
                                      (750,  -1): {(1,1): {'deltaPhi':1.0, 'label':['LT1','HTi','NB1','NJ45']}}},  
                         (350, -1):  {(500,  -1): {(1,1): {'deltaPhi':0.75, 'label':['LT2i','HTi','NB1','NJ45']}}},  
                         (350, 450): {(500,  -1): {(1,1): {'deltaPhi':1.0, 'label':['LT2','HTi','NB1','NJ45']}},  
                                      (500, 750): {(1,1): {'deltaPhi':1.0, 'label':['LT2','HT1','NB1','NJ45']}}, 
                                      (750,  -1): {(1,1): {'deltaPhi':1.0, 'label':['LT2','HT2i','NB1','NJ45']}}},  
                         (450, -1):  {(500,  -1): {(1,1): {'deltaPhi':0.75, 'label':['LT3i','HTi','NB1','NJ45']}},  
                                      (500, 750): {(1,1): {'deltaPhi':0.75, 'label':['LT3i','HT1','NB1','NJ45']}}, 
                                      (750,  -1): {(1,1): {'deltaPhi':0.75, 'label':['LT3i','HT2i','NB1','NJ45']}}}},  
#                (5, 5): {(250, 350): {(500,  -1): {(0,0): {'label':['LT1','HTi','NB0','NJ5']}}},   #signal regions
#                         (350, 450): {(500,  -1): {(0,0): {'label':['LT2','HTi','NB0','NJ5']}}},  
#                         (450,  -1): {(500,  -1): {(0,0): {'label':['LT3i','HTi','NB0','NJ5']}}}}, 
#                (6, 7): {(250, 350): {(500, 750): {(0,0): {'label':['LT1','HT1','NB0','NJ67']}}, 
#                                      (750,  -1): {(0,0): {'label':['LT1','HT2i','NB0','NJ67']}}},  
#                         (350, 450): {(500, 750): {(0,0): {'label':['LT2','HT1','NB0','NJ67']}}, 
#                                      (750,  -1): {(0,0): {'label':['LT2','HT2i','NB0','NJ67']}}},  
#                          (450, -1): {(500, 750): {(0,0): {'label':['LT3i','HT1','NB0','NJ67']}}, 
#                                      (750,  -1): {(0,0): {'label':['LT3i','HT2i','NB0','NJ67']}}}},  
#                (8, -1): {(250, 350):{(500, 750): {(0,0): {'label':['LT1','HT1','NB0','NJ8']}},
#                                      (750,  -1): {(0,0): {'label':['LT1','HT2i','NB0','NJ8']}}},
#                          (350, -1): {(500,  -1): {(0,0): {'label':['LT2i','HTi','NB0','NJ8']}}}},
}

signalRegion_combined = {
                (3, 4): {
                         (250, 350): {(500,  -1): {(0,0): {'sys':0.25, 'deltaPhi':1.0, 'label':['LT1','HTi','NB0','NJ34']}},  #3-4jets W+jets control region inclusive in LT
                                      (500, 750): {(0,0): {'sys':0.25, 'deltaPhi':1.0, 'label':['LT1','HT1','NB0','NJ34']}}, 
                                      (750,  -1): {(0,0): {'sys':0.5,  'deltaPhi':1.0, 'label':['LT1','HT2i','NB0','NJ34']}}},  
                         (350, -1):  {(500,  -1): {(0,0): {'sys':0.25, 'deltaPhi':0.75, 'label':['LT2i','HTi','NB0','NJ34']}}},
                         (350, 450): {(500,  -1): {(0,0): {'sys':0.25, 'deltaPhi':1.0, 'label':['LT2','HTi','NB0','NJ34']}},  
                                      (500, 750): {(0,0): {'sys':0.25, 'deltaPhi':1.0, 'label':['LT2','HT1','NB0','NJ34']}}, 
                                      (750,  -1): {(0,0): {'sys':0.5,  'deltaPhi':1.0, 'label':['LT2','HT2i','NB0','NJ34']}}},  
                         (450, -1):  {(500,  -1): {(0,0): {'sys':0.25, 'deltaPhi':0.75, 'label':['LT3i','HTi','NB0','NJ34']}},  
                                      (500, 750): {(0,0): {'sys':0.25, 'deltaPhi':0.75, 'label':['LT3i','HT1','NB0','NJ34']}}, 
                                      (750,  -1): {(0,0): {'sys':0.5,  'deltaPhi':0.75, 'label':['LT3i','HT1i','NB0','NJ34']}}}},  
                (4, 5): {(250, 350): {(500,  -1): {(1,1): {'sys':0.25, 'deltaPhi':1.0, 'label':['LT1','HTi','NB1','NJ45']}},  #4-5jets TTbar control region
                                      (500, 750): {(1,1): {'sys':0.25, 'deltaPhi':1.0, 'label':['LT1','HT1','NB1','NJ45']}}, 
                                      (750,  -1): {(1,1): {'sys':0.5,  'deltaPhi':1.0, 'label':['LT1','HTi','NB1','NJ45']}}},  
                         (350, -1):  {(500,  -1): {(1,1): {'sys':0.25, 'deltaPhi':0.75, 'label':['LT2i','HTi','NB1','NJ45']}}},  
                         (350, 450): {(500,  -1): {(1,1): {'sys':0.25, 'deltaPhi':1.0, 'label':['LT2','HTi','NB1','NJ45']}},  
                                      (500, 750): {(1,1): {'sys':0.25, 'deltaPhi':1.0, 'label':['LT2','HT1','NB1','NJ45']}}, 
                                      (750,  -1): {(1,1): {'sys':0.5,  'deltaPhi':1.0, 'label':['LT2','HT2i','NB1','NJ45']}}},  
                         (450, -1):  {(500,  -1): {(1,1): {'sys':0.25, 'deltaPhi':0.75, 'label':['LT3i','HTi','NB1','NJ45']}},  
                                      (500, 750): {(1,1): {'sys':0.25, 'deltaPhi':0.75, 'label':['LT3i','HT1','NB1','NJ45']}}, 
                                      (750,  -1): {(1,1): {'sys':0.5,  'deltaPhi':0.75, 'label':['LT3i','HT2i','NB1','NJ45']}}}},  
                (5, 5): {(250, 350): {(500,  -1): {(0,0): {'sys':0.25, 'deltaPhi':1.0, 'label':['LT1','HTi','NB0','NJ5']}}},   #signal regions
                         (350, 450): {(500,  -1): {(0,0): {'sys':0.25, 'deltaPhi':1.0, 'label':['LT2','HTi','NB0','NJ5']}}},  
                         (450,  -1): {(500,  -1): {(0,0): {'sys':0.25, 'deltaPhi':0.75, 'label':['LT3i','HTi','NB0','NJ5']}}}}, 
                (6, 7): {(250, 350): {(500, 750): {(0,0): {'sys':0.5,  'deltaPhi':1.0, 'label':['LT1','HT1','NB0','NJ67']}}, 
                                      (750,  -1): {(0,0): {'sys':0.5,  'deltaPhi':1.0, 'label':['LT1','HT2i','NB0','NJ67']}}},  
                         (350, 450): {(500, 750): {(0,0): {'sys':0.5,  'deltaPhi':1.0, 'label':['LT2','HT1','NB0','NJ67']}}, 
                                      (750,  -1): {(0,0): {'sys':0.5,  'deltaPhi':1.0, 'label':['LT2','HT2i','NB0','NJ67']}}},  
                          (450, -1): {(500, 750): {(0,0): {'sys':0.5,  'deltaPhi':0.75, 'label':['LT3i','HT1','NB0','NJ67']}}, 
                                      (750,  -1): {(0,0): {'sys':0.5,  'deltaPhi':0.75, 'label':['LT3i','HT2i','NB0','NJ67']}}}},  
                (8, -1): {(250, 350):{(500, 750): {(0,0): {'sys':1.0,  'deltaPhi':1.0, 'label':['LT1','HT1','NB0','NJ8']}},
                                      (750,  -1): {(0,0): {'sys':1.0,  'deltaPhi':1.0, 'label':['LT1','HT2i','NB0','NJ8']}}},
                          (350, -1): {(500,  -1): {(0,0): {'sys':1.0,  'deltaPhi':0.75, 'label':['LT2i','HTi','NB0','NJ8']}}}},
}

signalRegionInclusiveLT = {
                (3, 4): {(250,  -1): {(500,  -1)}},  #QCD inclusive template
                (3, 4): {(250,  -1): {(500,  -1):{'sys':0.025},  
                                      (500, 750):{'sys':0.025}, #3-4jets W+jets control region inclusive in LT 
                                      (750,  -1):{'sys':0.05}}},  
                (4, 5): {(250,  -1): {(500,  -1):{'sys':0.025},  #4-5jets TTbar control region
                                      (500, 750):{'sys':0.025}, 
                                      (750,  -1):{'sys':0.05}}},  
                (5, 5): {(250,  -1): {(500,  -1):{'sys':0.025}}},   #signal regions
                (6, 7): {(250,  -1): {(500, 750):{'sys':0.05}, 
                                      (750,  -1):{'sys':0.05}}},  
                (8, -1):{(250,  -1): {(500,  -1):{'sys':0.1},
                                      (500, 750):{'sys':0.1},
                                      (750,  -1):{'sys':0.1}}}
}

njreg = [(3,3),(4,4),(5,5),(6,6),(7,7),(8,-1)]
SRnjreg = [(3,4),(5,5),(6,7),(8,-1)]
ltreg = [(250,-1)]
htreg = [(500,750),(750,1000),(1000,-1)]
btreg = [(0,0)]#, (1,1), (2,2)] #1b and 2b estimates are needed for the btag fit

ROOT_colors = [ROOT.kBlack, ROOT.kRed-4, ROOT.kBlue, ROOT.kGreen+2, ROOT.kOrange+1, ROOT.kAzure+6, ROOT.kCyan+3, ROOT.kOrange , ROOT.kRed-10]
text = ROOT.TLatex()
text.SetNDC()
text.SetTextSize(0.04)
text.SetTextAlign(11)

canv = ROOT.TCanvas('canv','canv',1200,600)
pad1 = ROOT.TPad('pad1','pad1',0.,0.3,1.,1.)
pad1.SetBottomMargin(0.01)
pad1.Draw()
pad1.cd()
leg = ROOT.TLegend(0.8,0.65,0.97,0.85)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetShadowColor(ROOT.kWhite)

drawOption = 'hist ][ e1'
drawOptionSame = drawOption + 'same'
#
#totXErr = []
#totYErr = []
#totX = []
#totY = []
#qcdXErr = []
#qcdYErr = []
#qcdX = []
#qcdY = []

totHistEle=ROOT.TH1F('totHistEle','totHistEle',20,0,20)
totHistEle.SetLineWidth(2)
totHistEle.SetLineColor(ROOT.kOrange+1)
totHistEle.SetMarkerColor(ROOT.kOrange+1)
totHistEle.SetMarkerStyle(20)

totHistMuon=ROOT.TH1F('totHistMuon','totHistMuon',20,0,20)
totHistMuon.SetLineWidth(2)
totHistMuon.SetLineColor(ROOT.kCyan-6)
totHistMuon.SetMarkerColor(ROOT.kCyan-6)
totHistMuon.SetMarkerStyle(20)

qcdHistEle=ROOT.TH1F('qcdHistEle','qcdHistEle',20,0,20)
qcdHistEle.SetLineWidth(2)
qcdHistEle.SetLineColor(ROOT.kRed)
qcdHistEle.SetMarkerColor(ROOT.kRed)
qcdHistEle.SetMarkerStyle(20)

qcdHistMuon=ROOT.TH1F('qcdHistMuon','qcdHistMuon',20,0,20)
qcdHistMuon.SetLineWidth(2)
qcdHistMuon.SetLineColor(ROOT.kBlue)
qcdHistMuon.SetMarkerColor(ROOT.kBlue)
qcdHistMuon.SetMarkerStyle(20)

dataHistEle=ROOT.TH1F('dataHistEle','dataHistEle',20,0,20)
dataHistEle.SetLineWidth(2)
dataHistEle.SetLineColor(ROOT.kOrange+1)
dataHistEle.SetMarkerColor(ROOT.kOrange+1)
dataHistEle.SetMarkerStyle(20)

dataHistMuon=ROOT.TH1F('dataHistMuon','dataHistMuon',20,0,20)
dataHistMuon.SetLineWidth(2)
dataHistMuon.SetLineColor(ROOT.kCyan-6)
dataHistMuon.SetMarkerColor(ROOT.kCyan-6)
dataHistMuon.SetMarkerStyle(20)

qcdPredEle=ROOT.TH1F('qcdPredEle','qcdPredEle',20,0,20)
qcdPredEle.SetLineWidth(2)
qcdPredEle.SetLineColor(ROOT.kRed)
qcdPredEle.SetMarkerColor(ROOT.kRed)
qcdPredEle.SetMarkerStyle(20)

qcdPredMuon=ROOT.TH1F('qcdPredMuon','qcdPredMuon',20,0,20)
qcdPredMuon.SetLineWidth(2)
qcdPredMuon.SetLineColor(ROOT.kBlue)
qcdPredMuon.SetMarkerColor(ROOT.kBlue)
qcdPredMuon.SetMarkerStyle(20)

#qcdAntiHist=ROOT.TH1F('qcdAntiHist','qcdAntiHist',21,0,21)
#qcdAntiHist.SetLineWidth(2)
#qcdAntiHist.SetLineColor(color('qcd'))
#qcdAntiHist.SetMarkerColor(color('qcd'))

j=1
#antiSelname, antiSelCut = nameAndCut((250,-1),(500,-1),(3,4),(0,0), presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30')
#Selname, SelCut         = nameAndCut((250,-1),(500,-1),(3,4),(0,0), presel=SelStr, charge="", btagVar = 'nBJetMediumCSV30')
#nSel,nSel_err           = getYieldFromChain(cQCD, SelCut, weight = weight_str, returnError=True)
#nAntiSel,nAntiSel_err   = getYieldFromChain(cQCD, antiSelCut, weight = weight_str, returnError=True)
#X=nSel/nAntiSel
#X_err= F*sqrt(nSel_err**2/nSel**2+nAntiSel_err**2/nAntiSel**2)
#Fhist.SetBinContent(1,X)
#Fhist.SetBinError(1,X_err)
#Fhist.GetXaxis().SetBinLabel(1, '#splitline{QCD CR}{incl. HT}')
for i_njb, njb in enumerate(sorted(signalRegion)):
  for i_ltb, ltb in enumerate(sorted(signalRegion[njb])):
    for i_htb,htb in enumerate(sorted(signalRegion[njb][ltb])):
      for i_btb, btb in enumerate(sorted(signalRegion[njb][ltb][htb])):
        label = signalRegion[njb][ltb][htb][btb]['label']
        deltaPhi = signalRegion[njb][ltb][htb][btb]['deltaPhi']
#        antiSelnameEle, antiSelCutEle = nameAndCut(ltb, htb, njb, btb, presel=antiSelStrEle, charge="", btagVar = 'nBJetMediumCSV30')
        SelnameEle, SelCutEle         = nameAndCut(ltb, htb, njb, btb, presel=SelStrEle, charge="", btagVar = 'nBJetMediumCSV30' , stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean')
        nMCEle,nMCEle_err             = getYieldFromChain(cMC, SelCutEle, weight = weight_str, returnError=True)
        nDataEle,nDataEle_err         = getYieldFromChain(cDataEle, SelCutEle+trigger+filters, weight = '(1)', returnError=True)
        nSelEle,nSelEle_err           = getYieldFromChain(cQCD, SelCutEle, weight = weight_str, returnError=True)
        nPredEle, nPredEle_err        = resEle[njb][ltb][htb][btb][deltaPhi]['NQCDpred'], resEle[njb][ltb][htb][btb][deltaPhi]['NQCDpred_err']
#        nAntiSelEle,nAntiSelEle_err   = getYieldFromChain(cQCD, antiSelCutEle, weight = weight_str, returnError=True)
        SelnameMuon, SelCutMuon         = nameAndCut(ltb, htb, njb, btb, presel=SelStrMuon, charge="", btagVar = 'nBJetMediumCSV30',stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean')
        nMCMuon,nMCMuon_err             = getYieldFromChain(cMC, SelCutMuon, weight = weight_str, returnError=True)
        nDataMuon,nDataMuon_err         = getYieldFromChain(cDataMuon, SelCutMuon+trigger+filters, weight = '(1)', returnError=True)
        nSelMuon,nSelMuon_err           = getYieldFromChain(cQCD, SelCutMuon, weight = weight_str, returnError=True)
        antiSelnameMuon, antiSelCutMuon = nameAndCut(ltb, htb, njb, btb, presel=antiSelStrMuon, charge="", btagVar = 'nBJetMediumCSV30',stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean')
        nAntiSelMuon,nAntiSelMuon_err   = getYieldFromChain(cDataMuon, antiSelCutMuon+trigger+filters, weight = '(1)', returnError=True)
        totHistEle.SetBinContent(j,nMCEle)
        totHistEle.SetBinError(j,nMCEle_err)
        dataHistEle.SetBinContent(j,nDataEle)
        dataHistEle.SetBinError(j,nDataEle_err)
        qcdHistEle.SetBinContent(j,nSelEle)
        qcdHistEle.SetBinError(j,nSelEle_err)
        qcdPredEle.SetBinContent(j,nPredEle)
        qcdPredEle.SetBinError(j,nPredEle_err)
        totHistMuon.SetBinContent(j,nMCMuon)
        totHistMuon.SetBinError(j,nMCMuon_err)
        dataHistMuon.SetBinContent(j,nDataMuon)
        dataHistMuon.SetBinError(j,nDataMuon_err)
        qcdHistMuon.SetBinContent(j,nSelMuon)
        qcdHistMuon.SetBinError(j,nSelMuon_err)
        qcdPredMuon.SetBinContent(j,nAntiSelMuon*0.1)
        qcdPredMuon.SetBinError(j,nAntiSelMuon_err*0.1)

        totHistEle.GetXaxis().SetBinLabel(j, '#splitline{#splitline{'+label[0]+'}{'+label[1]+'}}{#splitline{'+label[2]+'}{'+label[3]+'}}')
        dataHistEle.GetXaxis().SetBinLabel(j, '#splitline{#splitline{'+label[0]+'}{'+label[1]+'}}{#splitline{'+label[2]+'}{'+label[3]+'}}')
        qcdHistEle.GetXaxis().SetBinLabel(j, '#splitline{#splitline{'+label[0]+'}{'+label[1]+'}}{#splitline{'+label[2]+'}{'+label[3]+'}}')
        qcdPredEle.GetXaxis().SetBinLabel(j, '#splitline{#splitline{'+label[0]+'}{'+label[1]+'}}{#splitline{'+label[2]+'}{'+label[3]+'}}')
        totHistMuon.GetXaxis().SetBinLabel(j, '#splitline{#splitline{'+label[0]+'}{'+label[1]+'}}{#splitline{'+label[2]+'}{'+label[3]+'}}')
        dataHistMuon.GetXaxis().SetBinLabel(j, '#splitline{#splitline{'+label[0]+'}{'+label[1]+'}}{#splitline{'+label[2]+'}{'+label[3]+'}}')
        qcdHistMuon.GetXaxis().SetBinLabel(j, '#splitline{#splitline{'+label[0]+'}{'+label[1]+'}}{#splitline{'+label[2]+'}{'+label[3]+'}}')
        qcdPredMuon.GetXaxis().SetBinLabel(j, '#splitline{#splitline{'+label[0]+'}{'+label[1]+'}}{#splitline{'+label[2]+'}{'+label[3]+'}}')

        j+=1

totHistEle.GetYaxis().SetTitle('# of Events')
qcdHistEle.GetYaxis().SetTitle('# of Events')
totHistEle.Draw('ep')
qcdHistEle.Draw('ep same')
totHistEle.SetMinimum(0.)
totHistEle.SetLabelSize(0.02)
qcdHistEle.SetMinimum(0.)
qcdHistEle.SetLabelSize(0.02)
totHistMuon.GetYaxis().SetTitle('# of Events')
qcdHistMuon.GetYaxis().SetTitle('# of Events')
totHistMuon.Draw('ep same')
qcdHistMuon.Draw('ep same')
totHistMuon.SetMinimum(0.)
totHistMuon.SetLabelSize(0.02)
qcdHistMuon.SetMinimum(0.)
qcdHistMuon.SetLabelSize(0.02)
leg.AddEntry(totHistEle,'QCD+EWK(ele)')
leg.AddEntry(totHistMuon,'QCD+EWK(#mu)')
leg.AddEntry(qcdHistEle,'QCD(ele)')
leg.AddEntry(qcdHistMuon,'QCD(#mu)')

#text.DrawLatex(0.16,.96,"CMS #bf{#it{Preliminary}}")
text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
text.DrawLatex(0.86,0.96,"#bf{L="+str(lumi)+"fb^{-1} (13 TeV)}")
#text.DrawLatex(0.2,0.86,"#bf{incl. L_{T}>250}")

#ax = array('d',sysX)
#ay = array('d',sysY)
#aexh = array('d',sysXErr)
#aexl = array('d',sysXErr)
#aeyh = array('d',sysYErr)
#aeyl = array('d',sysYErr)
#sys_err = ROOT.TGraphAsymmErrors(12, ax, ay, aexl, aexh, aeyl, aeyh)
#sys_err.SetFillColor(ROOT.kGray+1)
#sys_err.SetFillStyle(3244)
#sys_err.Draw('2 same')
#leg.AddEntry(sys_err,'sys. unc.','f')

#l = ROOT.TLine(0,X,12,X)
#l.SetLineColor(ROOT.kBlack)
#l.SetLineStyle(ROOT.kDashed)
#l.Draw()
#line = ROOT.TLine(1,0,1,1900)
#line.SetLineColor(ROOT.kBlack)
#line.SetLineStyle(ROOT.kDashed)
#line.Draw()
line2 = ROOT.TLine(10,0,10,1400)
line2.SetLineColor(ROOT.kBlack)
line2.SetLineStyle(ROOT.kDashed)
line2.Draw()
#line3 = ROOT.TLine(7,0,7,0.35)
#line3.SetLineColor(ROOT.kBlack)
#line3.SetLineStyle(ROOT.kDashed)
#line3.Draw()
#line4 = ROOT.TLine(9,0,9,0.35)
#line4.SetLineColor(ROOT.kBlack)
#line4.SetLineStyle(ROOT.kDashed)
#line4.Draw()
text.DrawLatex(0.7,0.88,"#bf{QCD vs MC in CR N_{j}#in[3,4];0b and N_{j}#in[4,5];1b}")
leg.Draw()
canv.cd()
pad2 = ROOT.TPad("ratio","ratio",0.,0.,1.,0.3)
pad2.SetTopMargin(0.01)
pad2.SetBottomMargin(0.3)
pad2.SetGrid()
pad2.Draw()
pad2.cd()
h_ratioEle = qcdHistEle.Clone()
h_ratioEle.SetMinimum(0.)
h_ratioEle.SetMaximum(0.45)
h_ratioEle.Sumw2()
h_ratioEle.SetStats(0)
h_ratioEle.Divide(totHistEle)
h_ratioEle.SetMarkerStyle(20)
h_ratioEle.SetLineStyle(1)
h_ratioEle.SetLineWidth(1)
h_ratioEle.Draw("ep")
#h_ratioEle.GetXaxis().SetTitle(var['legendName'])
h_ratioEle.GetYaxis().SetTitle("#frac{QCD}{QCD+EWK}")
h_ratioEle.GetYaxis().SetNdivisions(505)
h_ratioEle.GetYaxis().SetTitleSize(23)
h_ratioEle.GetYaxis().SetTitleFont(43)
h_ratioEle.GetYaxis().SetTitleOffset(1.8)
h_ratioEle.GetYaxis().SetLabelFont(43)
h_ratioEle.GetYaxis().SetLabelSize(20)
h_ratioEle.GetYaxis().SetLabelOffset(0.015)
h_ratioEle.GetXaxis().SetNdivisions(510)
h_ratioEle.GetXaxis().SetTitleSize(23)
h_ratioEle.GetXaxis().SetTitleFont(43)
h_ratioEle.GetXaxis().SetTitleOffset(3.4)
h_ratioEle.GetXaxis().SetLabelFont(43)
h_ratioEle.GetXaxis().SetLabelSize(10)
h_ratioEle.GetXaxis().SetLabelOffset(0.04)

h_ratioMuon = qcdHistMuon.Clone()
h_ratioMuon.SetMinimum(0.)
h_ratioMuon.SetMaximum(0.45)
h_ratioMuon.Sumw2()
h_ratioMuon.SetStats(0)
h_ratioMuon.Divide(totHistMuon)
h_ratioMuon.SetMarkerStyle(20)
h_ratioMuon.SetLineStyle(1)
h_ratioMuon.SetLineWidth(1)
h_ratioMuon.Draw("ep same")
#h_ratioMuon.GetXaxis().SetTitle(var['legendName'])
h_ratioMuon.GetYaxis().SetTitle("#frac{QCD}{QCD+EWK}")
h_ratioMuon.GetYaxis().SetNdivisions(505)
h_ratioMuon.GetYaxis().SetTitleSize(23)
h_ratioMuon.GetYaxis().SetTitleFont(43)
h_ratioMuon.GetYaxis().SetTitleOffset(1.8)
h_ratioMuon.GetYaxis().SetLabelFont(43)
h_ratioMuon.GetYaxis().SetLabelSize(20)
h_ratioMuon.GetYaxis().SetLabelOffset(0.015)
h_ratioMuon.GetXaxis().SetNdivisions(510)
h_ratioMuon.GetXaxis().SetTitleSize(23)
h_ratioMuon.GetXaxis().SetTitleFont(43)
h_ratioMuon.GetXaxis().SetTitleOffset(3.4)
h_ratioMuon.GetXaxis().SetLabelFont(43)
h_ratioMuon.GetXaxis().SetLabelSize(10)
h_ratioMuon.GetXaxis().SetLabelOffset(0.04)
line2.Draw()
canv.cd()
canv.Print(wwwDir+prefix+'MCvsQCDsel.png')
canv.Print(wwwDir+prefix+'MCvsQCDsel.pdf')
canv.Print(wwwDir+prefix+'MCvsQCDsel.root')

###########################################

canv2 = ROOT.TCanvas('canv2','canv2',1200,600)
pad1 = ROOT.TPad('pad1','pad1',0.,0.3,1.,1.)
pad1.SetBottomMargin(0.01)
pad1.Draw()
pad1.cd()
leg2 = ROOT.TLegend(0.8,0.65,0.97,0.85)
leg2.SetFillColor(0)
leg2.SetBorderSize(0)
leg2.SetShadowColor(ROOT.kWhite)

dataHistEle.GetYaxis().SetTitle('# of Events')
qcdPredEle.GetYaxis().SetTitle('# of Events')
dataHistEle.Draw('ep')
qcdPredEle.Draw('ep same')
dataHistEle.SetMinimum(0.)
dataHistEle.SetLabelSize(0.02)
qcdPredEle.SetMinimum(0.)
qcdPredEle.SetLabelSize(0.02)
dataHistMuon.GetYaxis().SetTitle('# of Events')
qcdPredMuon.GetYaxis().SetTitle('# of Events')
dataHistMuon.Draw('ep same')
qcdPredMuon.Draw('ep same')
dataHistMuon.SetMinimum(0.)
dataHistMuon.SetLabelSize(0.02)
qcdPredMuon.SetMinimum(0.)
qcdPredMuon.SetLabelSize(0.02)
leg2.AddEntry(dataHistEle,'Data(ele)')
leg2.AddEntry(dataHistMuon,'Data(#mu)')
leg2.AddEntry(qcdPredEle,'QCD pred.(ele)')
leg2.AddEntry(qcdPredMuon,'QCD pred.(#mu)')

text.DrawLatex(0.16,.96,"CMS #bf{#it{Preliminary}}")
#text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
text.DrawLatex(0.86,0.96,"#bf{L="+str(lumi)+"fb^{-1} (13 TeV)}")
#text.DrawLatex(0.2,0.86,"#bf{incl. L_{T}>250}")

#l = ROOT.TLine(0,X,12,X)
#l.SetLineColor(ROOT.kBlack)
#l.SetLineStyle(ROOT.kDashed)
#l.Draw()
#line = ROOT.TLine(1,0,1,1900)
#line.SetLineColor(ROOT.kBlack)
#line.SetLineStyle(ROOT.kDashed)
#line.Draw()
line2 = ROOT.TLine(10,0,10,1400)
line2.SetLineColor(ROOT.kBlack)
line2.SetLineStyle(ROOT.kDashed)
line2.Draw()
#line3 = ROOT.TLine(7,0,7,0.35)
#line3.SetLineColor(ROOT.kBlack)
#line3.SetLineStyle(ROOT.kDashed)
#line3.Draw()
#line4 = ROOT.TLine(9,0,9,0.35)
#line4.SetLineColor(ROOT.kBlack)
#line4.SetLineStyle(ROOT.kDashed)
#line4.Draw()
text.DrawLatex(0.7,0.88,"#bf{Data vs QCD in CR N_{j}#in[3,4];0b and N_{j}#in[4,5];1b}")
leg2.Draw()

canv2.cd()
pad2 = ROOT.TPad("ratio","ratio",0.,0.,1.,0.3)
pad2.SetTopMargin(0.01)
pad2.SetBottomMargin(0.3)
pad2.SetGrid()
pad2.Draw()
pad2.cd()
h_ratioEle = qcdPredEle.Clone()
h_ratioEle.SetMinimum(0.)
h_ratioEle.SetMaximum(0.45)
h_ratioEle.Sumw2()
h_ratioEle.SetStats(0)
h_ratioEle.Divide(dataHistEle)
h_ratioEle.SetMarkerStyle(20)
h_ratioEle.SetLineStyle(1)
h_ratioEle.SetLineWidth(1)
h_ratioEle.Draw("ep")
#h_ratioEle.GetXaxis().SetTitle(var['legendName'])
h_ratioEle.GetYaxis().SetTitle("#frac{QCD pred.}{Data}")
h_ratioEle.GetYaxis().SetNdivisions(505)
h_ratioEle.GetYaxis().SetTitleSize(23)
h_ratioEle.GetYaxis().SetTitleFont(43)
h_ratioEle.GetYaxis().SetTitleOffset(1.8)
h_ratioEle.GetYaxis().SetLabelFont(43)
h_ratioEle.GetYaxis().SetLabelSize(20)
h_ratioEle.GetYaxis().SetLabelOffset(0.015)
h_ratioEle.GetXaxis().SetNdivisions(510)
h_ratioEle.GetXaxis().SetTitleSize(23)
h_ratioEle.GetXaxis().SetTitleFont(43)
h_ratioEle.GetXaxis().SetTitleOffset(3.4)
h_ratioEle.GetXaxis().SetLabelFont(43)
h_ratioEle.GetXaxis().SetLabelSize(10)
h_ratioEle.GetXaxis().SetLabelOffset(0.04)

h_ratioMuon = qcdPredMuon.Clone()
h_ratioMuon.SetMinimum(0.)
h_ratioMuon.SetMaximum(0.45)
h_ratioMuon.Sumw2()
h_ratioMuon.SetStats(0)
h_ratioMuon.Divide(dataHistMuon)
h_ratioMuon.SetMarkerStyle(20)
h_ratioMuon.SetLineStyle(1)
h_ratioMuon.SetLineWidth(1)
h_ratioMuon.Draw("ep same")
#h_ratioMuon.GetXaxis().SetTitle(var['legendName'])
h_ratioMuon.GetYaxis().SetTitle("#frac{QCD pred.}{Data}")
h_ratioMuon.GetYaxis().SetNdivisions(505)
h_ratioMuon.GetYaxis().SetTitleSize(23)
h_ratioMuon.GetYaxis().SetTitleFont(43)
h_ratioMuon.GetYaxis().SetTitleOffset(1.8)
h_ratioMuon.GetYaxis().SetLabelFont(43)
h_ratioMuon.GetYaxis().SetLabelSize(20)
h_ratioMuon.GetYaxis().SetLabelOffset(0.015)
h_ratioMuon.GetXaxis().SetNdivisions(510)
h_ratioMuon.GetXaxis().SetTitleSize(23)
h_ratioMuon.GetXaxis().SetTitleFont(43)
h_ratioMuon.GetXaxis().SetTitleOffset(3.4)
h_ratioMuon.GetXaxis().SetLabelFont(43)
h_ratioMuon.GetXaxis().SetLabelSize(10)
h_ratioMuon.GetXaxis().SetLabelOffset(0.04)
#line.Draw()
line2.Draw()
canv2.cd()

canv2.Print(wwwDir+prefix+'DataVsQCDpred.png')
canv2.Print(wwwDir+prefix+'DataVsQCDpred.pdf')
canv2.Print(wwwDir+prefix+'DataVsQCDpred.root')

##############################################

canv3 = ROOT.TCanvas('canv3','canv3',1200,600)
pad1 = ROOT.TPad('pad1','pad1',0.,0.3,1.,1.)
pad1.SetBottomMargin(0.01)
pad1.Draw()
pad1.cd()
leg3 = ROOT.TLegend(0.8,0.75,0.97,0.85)
leg3.SetFillColor(0)
leg3.SetBorderSize(0)
leg3.SetShadowColor(ROOT.kWhite)

drawOption = 'hist ][ e1'
drawOptionSame = drawOption + 'same'

qcdHistEle=ROOT.TH1F('qcdHistEle','qcdHistEle',32,0,32)
qcdHistEle.SetLineWidth(2)
qcdHistEle.SetLineColor(ROOT.kRed)
qcdHistEle.SetMarkerColor(ROOT.kRed)
qcdHistEle.SetMarkerStyle(20)

qcdPredEle=ROOT.TH1F('qcdPredEle','qcdPredEle',32,0,32)
qcdPredEle.SetLineWidth(2)
qcdPredEle.SetLineColor(ROOT.kBlue)
qcdPredEle.SetMarkerColor(ROOT.kBlue)
qcdPredEle.SetMarkerStyle(20)


j=1
for i_njb, njb in enumerate(sorted(signalRegion_combined)):
  for i_ltb, ltb in enumerate(sorted(signalRegion_combined[njb])):
    for i_htb,htb in enumerate(sorted(signalRegion_combined[njb][ltb])):
      for i_btb, btb in enumerate(sorted(signalRegion_combined[njb][ltb][htb])):
        label = signalRegion_combined[njb][ltb][htb][btb]['label']
        deltaPhi = signalRegion_combined[njb][ltb][htb][btb]['deltaPhi']
        sys = signalRegion_combined[njb][ltb][htb][btb]['sys']
        nEle, nEle_err          = resEleMC[njb][ltb][htb][btb][deltaPhi]['NQCDSelMC'], resEleMC[njb][ltb][htb][btb][deltaPhi]['NQCDSelMC_err']
        nPredEle, nPredEle_err  = resEleMC[njb][ltb][htb][btb][deltaPhi]['NQCDpred'], resEleMC[njb][ltb][htb][btb][deltaPhi]['NQCDpred_err']
        qcdHistEle.SetBinContent(j,nEle)
        qcdHistEle.SetBinError(j,nEle_err)
        qcdPredEle.SetBinContent(j,nPredEle)
        qcdPredEle.SetBinError(j,sqrt((nPredEle_err)**2 + (sys)**2))
        qcdHistEle.GetXaxis().SetBinLabel(j, '#splitline{#splitline{'+label[0]+'}{'+label[1]+'}}{#splitline{'+label[2]+'}{'+label[3]+'}}')
        qcdPredEle.GetXaxis().SetBinLabel(j, '#splitline{#splitline{'+label[0]+'}{'+label[1]+'}}{#splitline{'+label[2]+'}{'+label[3]+'}}')
        j+=1

qcdHistEle.GetYaxis().SetTitle('# of Events')
qcdHistEle.Draw('ep')
qcdHistEle.SetMinimum(0.)
qcdHistEle.SetLabelSize(0.02)
qcdPredEle.GetYaxis().SetTitle('# of Events')
qcdPredEle.Draw('ep same')
qcdPredEle.SetMinimum(0.)
qcdPredEle.SetLabelSize(0.02)
leg3.AddEntry(qcdHistEle,'QCD_{MC}(ele)')
leg3.AddEntry(qcdPredEle,'QCD_{pred.}(ele)')

#text.DrawLatex(0.16,.96,"CMS #bf{#it{Preliminary}}")
text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
text.DrawLatex(0.86,0.96,"#bf{L="+str(lumi)+"fb^{-1} (13 TeV)}")

line2 = ROOT.TLine(10,-3.5,10,450)
line2.SetLineColor(ROOT.kBlack)
line2.SetLineStyle(ROOT.kDashed)
line2.Draw()
line3 = ROOT.TLine(20,-3.5,20,450)
line3.SetLineColor(ROOT.kBlack)
line3.SetLineStyle(7)
line3.Draw()
#line4 = ROOT.TLine(0,0,31,0)
#line4.SetLineColor(ROOT.kBlack)
#line4.SetLineStyle(7)
#line4.Draw()
text.DrawLatex(0.82,0.88,"#bf{QCD closure}")
leg3.Draw()
canv3.cd()
pad2 = ROOT.TPad("ratio","ratio",0.,0.,1.,0.3)
pad2.SetTopMargin(0.01)
pad2.SetBottomMargin(0.3)
pad2.SetGrid()
pad2.Draw()
pad2.cd()
h_ratioEle = qcdPredEle.Clone()
h_ratioEle.Sumw2()
h_ratioEle.SetStats(0)
h_ratioEle.Add(qcdHistEle,-1)
h_ratioEle.Divide(qcdPredEle)
h_ratioEle.SetMarkerStyle(20)
h_ratioEle.SetLineStyle(1)
h_ratioEle.SetLineWidth(1)
h_ratioEle.Draw("ep")
h_ratioEle.SetMinimum(-3.5)
h_ratioEle.SetMaximum(3.5)
h_ratioEle.GetYaxis().SetTitle("#frac{QCD_{pred.}-QCD_{MC}}{QCD_{pred.}}")
h_ratioEle.GetYaxis().SetNdivisions(505)
h_ratioEle.GetYaxis().SetTitleSize(23)
h_ratioEle.GetYaxis().SetTitleFont(43)
h_ratioEle.GetYaxis().SetTitleOffset(1.8)
h_ratioEle.GetYaxis().SetLabelFont(43)
h_ratioEle.GetYaxis().SetLabelSize(20)
h_ratioEle.GetYaxis().SetLabelOffset(0.015)
h_ratioEle.GetXaxis().SetNdivisions(510)
h_ratioEle.GetXaxis().SetTitleSize(23)
h_ratioEle.GetXaxis().SetTitleFont(43)
h_ratioEle.GetXaxis().SetTitleOffset(3.4)
h_ratioEle.GetXaxis().SetLabelFont(43)
h_ratioEle.GetXaxis().SetLabelSize(10)
h_ratioEle.GetXaxis().SetLabelOffset(0.04)

line2.Draw()
line3.Draw()
canv3.cd()
canv3.Print(wwwDir+prefix+'QCDclosureEle.png')
canv3.Print(wwwDir+prefix+'QCDclosureEle.pdf')
canv3.Print(wwwDir+prefix+'QCDclosureEle.root')

###########################################



#canv2 = ROOT.TCanvas('canv2','canv2',600,600)
#
#ClosureHist=ROOT.TH1F('ClosureHist','ClosureHist',14,0,14)
#ClosureHist.SetLineWidth(2)
#k=0
#for i_CR, ltb in enumerate(sorted(CR[(3,4)])):
#  for i_htb,htb in enumerate(sorted(CR[(3,4)][ltb])):
#    for i_dP,dP in enumerate(sorted(CR[(3,4)][ltb][htb])):
#      k+=1
#      result, result_err = getFraction(res[(3,4)][ltb][htb][(0,0)][dP]['NQCDSelMC'],res[(3,4)][ltb][htb][(0,0)][dP]['NQCDSelMC_err'],res[(3,4)][ltb][htb][(0,0)][dP]['NQCDpred'],res[(3,4)][ltb][htb][(0,0)][dP]['NQCDpred_err'])
#      ClosureHist.SetBinContent(k,result)
#      ClosureHist.SetBinError(k,result_err)
#      ClosureHist.GetXaxis().SetBinLabel(k,str(k))
#      ClosureHist.GetYaxis().SetTitle('N^{pred}_{QCD}/N^{MC}_{QCD}')
#
#ClosureHist.Draw('L')
#ClosureHist.SetMinimum(0.)
#ClosureHist.SetMaximum(2.)
#text.DrawLatex(0.16,.96,"CMS #bf{#it{Preliminary}}")
##text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
#text.DrawLatex(0.7,0.96,"#bf{L="+str(lumi)+"fb^{-1} (13 TeV)}")
#
#line = ROOT.TLine()
#line.SetY1(1.0)
#line.SetX2(14)
#line.SetHorizontal()
#line.SetLineColor(ROOT.kBlack)
#line.SetLineStyle(ROOT.kDashed)
#line.Draw()
#
#canv2.Print(wwwDir+prefix+'FitClosure_inCR.png')
#canv2.Print(wwwDir+prefix+'FitClosure_inCR.pdf')
#canv2.Print(wwwDir+prefix+'FitClosure_inCR.root')

#canv3 = ROOT.TCanvas('canv3','canv3',600,600)
#
#ClosureHistSR=ROOT.TH1F('ClosureHistSR','ClosureHistSR',17,0,17)
#ClosureHistSR.SetLineWidth(2)
#k=0
#for i_njb, njb in enumerate(sorted(signalRegion)):
#  for i_CR, ltb in enumerate(sorted(signalRegion[njb])):
#    for i_htb,htb in enumerate(sorted(signalRegion[njb][ltb])):
#      for i_dP,dP in enumerate(sorted(signalRegion[njb][ltb][htb])):
#        k+=1
#        result, result_err = getFraction(res[njb][ltb][htb][(0,0)][dP]['NQCDSelMC'],res[njb][ltb][htb][(0,0)][dP]['NQCDSelMC_err'],res[njb][ltb][htb][(0,0)][dP]['NQCDpred'],res[njb][ltb][htb][(0,0)][dP]['NQCDpred_err'])
#        ClosureHistSR.SetBinContent(k,result)
#        ClosureHistSR.SetBinError(k,result_err)
#        ClosureHistSR.GetXaxis().SetBinLabel(k,str(k))
#        ClosureHistSR.GetYaxis().SetTitle('N^{pred}_{QCD}/N^{MC}_{QCD}')
#
#ClosureHistSR.Draw('L')
#ClosureHistSR.SetMinimum(0.)
#ClosureHistSR.SetMaximum(2.)
#text.DrawLatex(0.16,.96,"CMS #bf{#it{Preliminary}}")
##text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
#text.DrawLatex(0.65,0.96,"#bf{L="+str(lumi)+"fb^{-1} (13 TeV)}")
#
#line = ROOT.TLine()
#line.SetY1(1.0)
#line.SetX2(17)
#line.SetHorizontal()
#line.SetLineColor(ROOT.kBlack)
#line.SetLineStyle(ROOT.kDashed)
#line.Draw()
#
#canv3.Print(wwwDir+prefix+'FitClosure_inSR.png')
#canv3.Print(wwwDir+prefix+'FitClosure_inSR.pdf')
#canv3.Print(wwwDir+prefix+'FitClosure_inSR.root')


#plot F_sel-to-antisel binned in HT for SR Njets
#ratio_ht={}
#for stb in ltreg:
#  ratio_ht[stb]={}
#  first = True
#  canv = ROOT.TCanvas('canv','canv',600,600)
#  #canv.SetLogy()
#  l = ROOT.TLegend(0.65,0.85,0.98,0.95)
#  l.SetFillColor(0)
#  l.SetBorderSize(1)
#  l.SetShadowColor(ROOT.kWhite)
#  
#  t=ROOT.TLatex()
#  t.SetNDC()
#  t.SetTextSize(0.04)
#  t.SetTextAlign(11)
#  for i_njb, njb in enumerate(SRnjreg):
#    ratio_ht[stb][njb]={}
#    for btb in btreg:
#      ratio_ht[stb][njb][btb]=ROOT.TH1F('ratio_htHist','ratio_htHist',len(htreg),0,len(htreg))
#      ratio_ht[stb][njb][btb].SetLineColor(ROOT_colors[i_njb])
#      ratio_ht[stb][njb][btb].SetMarkerColor(ROOT_colors[i_njb])
#      ratio_ht[stb][njb][btb].SetLineWidth(2)
#      for i_htb, htb in enumerate(htreg):
#        antiSelname, antiSelCut = nameAndCut(stb, htb, njb, btb=btb, presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30')
#        Selname, SelCut         = nameAndCut(stb, htb, njb, btb=btb, presel=SelStr, charge="", btagVar = 'nBJetMediumCSV30')
#        nSel,nSel_err = getYieldFromChain(cQCD, SelCut, weight = weight_str, returnError=True)
#        nAntiSel,nAntiSel_err = getYieldFromChain(cQCD, antiSelCut, weight = weight_str, returnError=True)
#        try: F=nSel/nAntiSel
#        except ZeroDivisionError: F=float('nan')
#        try: F_err= F*sqrt(nSel_err**2/nSel**2+nAntiSel_err**2/nAntiSel**2)
#        except ZeroDivisionError: F_err=0
#        try:
#          ratio_ht[stb][njb][btb].SetBinContent(i_htb+1,F)
#          ratio_ht[stb][njb][btb].SetBinError(i_htb+1,F_err)
#        except KeyError: pass
#        ratio_ht[stb][njb][btb].GetXaxis().SetBinLabel(i_htb+1, varBinName(htb,'H_{T}'))
#        ratio_ht[stb][njb][btb].GetYaxis().SetTitle('F_{sel-to-antisel}')
#        ratio_ht[stb][njb][btb].GetYaxis().SetRangeUser(0.0,0.5)
##          ratio_ht[stb][njb].GetXaxis().SetTitle('F_{sel-to-antisel}')
#      l.AddEntry(ratio_ht[stb][njb][btb], nJetBinName(njb))
#      if first:
#        ratio_ht[stb][njb][btb].Draw()
#        first = False
#      else:
#        ratio_ht[stb][njb][btb].Draw('same') 
#      l.Draw()
#      t.DrawLatex(0.2,0.85,'#bf{'+varBinName(stb,'L_{T}')+'}')
#      text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
#      text.DrawLatex(0.75,0.96,"#bf{MC (13 TeV)}")
#      canv.Print(wwwDir+prefix+'FsaMC_ht_'+nameAndCut(stb, None, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
#      canv.Print(wwwDir+prefix+'FsaMC_ht_'+nameAndCut(stb, None, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
#      canv.Print(wwwDir+prefix+'FsaMC_ht_'+nameAndCut(stb, None, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')


#plot F_sel-to-antisel binned in ST for all Njets
#ratio_st={}
#for htb in htreg:
#  ratio_st[htb]={}
#  first = True
#  canv2= ROOT.TCanvas('canv2','canv2',600,600)
#  #canv.SetLogy()
#  l2 = ROOT.TLegend(0.65,0.85,0.95,0.95)
#  l2.SetFillColor(0)
#  l2.SetBorderSize(1)
#  l2.SetShadowColor(ROOT.kWhite)
#  
#  t=ROOT.TLatex()
#  t.SetNDC()
#  t.SetTextSize(0.04)
#  t.SetTextAlign(11)
#  for i_njb, njb in enumerate(njreg):
#    ratio_st[htb][njb]={}
#    for btb in btreg:
#      ratio_st[htb][njb][btb]=ROOT.TH1F('ratio_stHist','ratio_stHist',len(streg),0,len(streg))
#      ratio_st[htb][njb][btb].SetLineColor(ROOT_colors[i_njb])
#      ratio_st[htb][njb][btb].SetLineWidth(2)
#      for i_stb, stb in enumerate(streg):
#        nQCDsel = bins[njb][stb][htb][btb]['nQCDSelected'] 
#        nQCDselVar = bins[njb][stb][htb][btb]['nQCDSelectedVar'] 
#        nQCDantisel = bins[njb][stb][htb][btb]['nAntiSelected'] 
#        nQCDantiselVar = bins[njb][stb][htb][btb]['nAntiSelectedVar'] 
##          print nQCDsel, nQCDantisel
#        if nQCDantisel>0:
#          F=nQCDsel/nQCDantisel
#          print 'F_sel-to-anti-sel('+str(stb)+','+str(njb)+','+str(htb)+'):',F
#          if F>0:
#            F_err= F*sqrt(nQCDselVar/nQCDsel**2+nQCDantiselVar/nQCDantisel**2)
#            ratio_st[htb][njb][btb].SetBinContent(i_stb+1,F)
#            ratio_st[htb][njb][btb].SetBinError(i_stb+1,F_err)
#            print 'F_sel-to-anti-sel Error('+str(stb)+','+str(njb)+','+str(htb)+'):',F_err
#        ratio_st[htb][njb][btb].GetXaxis().SetBinLabel(i_stb+1, varBinName(stb,'S_{T}'))
#        ratio_st[htb][njb][btb].GetYaxis().SetTitle('F_{sel-to-antisel}')
#        ratio_st[htb][njb][btb].GetYaxis().SetRangeUser(0.0,1.0)
##        ratio_st[htb][njb].GetXaxis().SetTitle('F_{sel-to-antisel}')
#      l2.AddEntry(ratio_st[htb][njb][btb], nJetBinName(njb))
#      if first:
#        ratio_st[htb][njb][btb].Draw()
#        first = False
#      else:
#        ratio_st[htb][njb][btb].Draw('same') 
#      l2.Draw()
#      t.DrawLatex(0.175,0.85,varBinName(htb,'H_{T}'))
#      text.DrawLatex(0.15,.96,"CMS Simulation")
#      text.DrawLatex(0.65,0.96,"L="+str(targetLumi/1000)+" fb^{-1} (13 TeV)")
#      canv2.Print(wwwDir+presel+'Fsa_st_'+nameAndCut(None, htb, njetb=None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
#      canv2.Print(wwwDir+presel+'Fsa_st_'+nameAndCut(None, htb, njetb=None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
#      canv2.Print(wwwDir+presel+'Fsa_st_'+nameAndCut(None, htb, njetb=None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')

#plot F_sel-to-antisel binned in ST vs HT
#ratio_2d={}
#for njb in njreg:
#  ratio_2d[njb]={}
#  canv3= ROOT.TCanvas('canv3','canv3',600,600)
#  #canv.SetLogy()
##  l3 = ROOT.TLegend(0.65,0.75,0.95,0.95)
##  l3.SetFillColor(0)
##  l3.SetBorderSize(1)
##  l3.SetShadowColor(ROOT.kWhite)
#  
#  t=ROOT.TLatex()
#  t.SetNDC()
#  t.SetTextSize(0.04)
#  t.SetTextAlign(11)
#  for btb in btreg:
#    ratio_2d[njb][btb]={}
#    ratio_2d[njb][btb]=ROOT.TH2F('ratio_2dHist','ratio_2dHist',len(htreg),0,len(htreg),len(streg),0,len(streg))
#    for i_htb, htb in enumerate(htreg):
#      ratio_2d[njb][btb].GetXaxis().SetBinLabel(i_htb+1,varBinName(htb,'H_{T}'))
#    for i_stb, stb in enumerate(streg):
#      ratio_2d[njb][btb].GetYaxis().SetBinLabel(i_stb+1,varBinName(stb,'S_{T}'))
#
#    for i_htb, htb in enumerate(htreg):
#      for i_stb, stb in enumerate(streg):
#        nQCDsel = bins[njb][stb][htb][btb]['nQCDSelected'] 
#        nQCDselVar = bins[njb][stb][htb][btb]['nQCDSelectedVar'] 
#        nQCDantisel = bins[njb][stb][htb][btb]['nAntiSelected'] 
#        nQCDantiselVar = bins[njb][stb][htb][btb]['nAntiSelectedVar'] 
##          print nQCDsel, nQCDantisel
#        if nQCDantisel>0:
#          F=nQCDsel/nQCDantisel
#          print 'F_sel-to-anti-sel('+str(stb)+','+str(njb)+','+str(htb)+'):',F
#          if F>0:
#            F_err= F*sqrt(nQCDselVar/nQCDsel**2+nQCDantiselVar/nQCDantisel**2)
#            ratio_2d[njb][btb].SetBinContent(i_htb+1,i_stb+1,F)
#            ratio_2d[njb][btb].SetBinError(i_htb+1,i_stb+1,F_err)
#            print 'F_sel-to-anti-sel Error('+str(stb)+','+str(njb)+','+str(htb)+'):',F_err
##      l.AddEntry(ratio_2d[htb][njb][btb], nJetBinName(njb))
#        ratio_2d[njb][btb].Draw('COLZ TEXTE')
#      t.DrawLatex(0.175,0.85,nJetBinName(njb))
#      text.DrawLatex(0.15,.96,"CMS Simulation")
#      text.DrawLatex(0.65,0.96,"L="+str(targetLumi/1000)+" fb^{-1} (13 TeV)") 
#      canv3.Print(wwwDir+presel+'st_vs_ht_'+nameAndCut(None, None, njetb=njb, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
#      canv3.Print(wwwDir+presel+'st_vs_ht_'+nameAndCut(None, None, njetb=njb, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
#      canv3.Print(wwwDir+presel+'st_vs_ht_'+nameAndCut(None, None, njetb=njb, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')

#plot F_sel-to-antisel binned in nJets for all ST bins
#ratio_nj={}
#for htb in [(500,-1)]:
#  ratio_nj[htb]={}
#  first = True
#  canv4 = ROOT.TCanvas('canv','canv',600,600)
#  #canv.SetLogy()
#  l3 = ROOT.TLegend(0.65,0.80,0.98,0.95)
#  l3.SetFillColor(0)
#  l3.SetBorderSize(1)
#  l3.SetShadowColor(ROOT.kWhite)
#  text = ROOT.TLatex()
#  text.SetNDC()
#  text.SetTextSize(0.04)
#  text.SetTextAlign(11)
#  t3=ROOT.TLatex()
#  t3.SetNDC()
#  t3.SetTextSize(0.04)
#  t3.SetTextAlign(11)
#  for i_stb, stb in enumerate(ltreg):
#    ratio_nj[htb][stb]={}
#    for btb in btreg:
#      ratio_nj[htb][stb][btb]=ROOT.TH1F('ratio_njHist','ratio_njHist',len(njreg),0,len(njreg))
#      ratio_nj[htb][stb][btb].SetLineColor(ROOT_colors[i_stb])
#      ratio_nj[htb][stb][btb].SetMarkerColor(ROOT_colors[i_stb])
#      ratio_nj[htb][stb][btb].SetLineWidth(2)
#      for i_njb, njb in enumerate(njreg):
#        antiSelname, antiSelCut = nameAndCut(stb, htb, njb, btb=btb, presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30')
#        Selname, SelCut         = nameAndCut(stb, htb, njb, btb=btb, presel=SelStr, charge="", btagVar = 'nBJetMediumCSV30')
#        nSel,nSel_err = getYieldFromChain(cQCD, SelCut, weight = weight_str, returnError=True)
#        nAntiSel,nAntiSel_err = getYieldFromChain(cQCD, antiSelCut, weight = weight_str, returnError=True)
##        rcs = getRCS(cQCD, antiSelCut, 0.75, useWeight = True, weight = 'weight')
##        if rcs['rCS']!=float('nan') and rcs['rCS']> 0.: 
##          ratio_nj[htb][stb][btb].SetBinContent(i_njb+1,rcs['rCS'])
##          ratio_nj[htb][stb][btb].SetBinError(i_njb+1,rcs['rCSE_sim'])
#        try: F=nSel/nAntiSel
#        except ZeroDivisionError: F=float('nan')
#        try: F_err= F*sqrt(nSel_err**2/nSel**2+nAntiSel_err**2/nAntiSel**2)
#        except ZeroDivisionError: F_err=0
#        ratio_nj[htb][stb][btb].SetBinContent(i_njb+1,F)
#        ratio_nj[htb][stb][btb].SetBinError(i_njb+1,F_err)
#        ratio_nj[htb][stb][btb].GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb))
#        ratio_nj[htb][stb][btb].GetYaxis().SetTitle('F_{sel-to-antisel}')
##        ratio_nj[htb][stb][btb].GetYaxis().SetTitle('R^{antisel}_{CS}')
#        ratio_nj[htb][stb][btb].GetYaxis().SetRangeUser(0.0,0.5)
#      #l3.AddEntry(ratio_nj[htb][stb][btb], varBinName(stb,'L_{T}'))
#      if first:
#        ratio_nj[htb][stb][btb].Draw()
#        first = False
#      else:
#        ratio_nj[htb][stb][btb].Draw('same') 
#      #l3.Draw()
#      t3.DrawLatex(0.2,0.85,'#bf{'+varBinName(htb,'H_{T}')+'}')
#      t3.DrawLatex(0.2,0.8,'#bf{'+varBinName(stb,'L_{T}')+'}')
#      text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
#      text.DrawLatex(0.75,0.96,"#bf{MC (13 TeV)}")     
#      canv4.Print(wwwDir+prefix+'FsaMC_nj_'+nameAndCut(None, htb, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
#      canv4.Print(wwwDir+prefix+'FsaMC_nj_'+nameAndCut(None, htb, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
#      canv4.Print(wwwDir+prefix+'FsaMC_nj_'+nameAndCut(None, htb, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')

#plot F_sel-to-antisel binned in ST for all Njets
#ratio_st={}
#for htb in [(500,-1)]:
#  ratio_st[htb]={}
#  first = True
#  canv2= ROOT.TCanvas('canv2','canv2',600,600)
#  #canv.SetLogy()
#  l2 = ROOT.TLegend(0.65,0.85,0.98,0.95)
#  l2.SetFillColor(0)
#  l2.SetBorderSize(1)
#  l2.SetShadowColor(ROOT.kWhite)
#  
#  t=ROOT.TLatex()
#  t.SetNDC()
#  t.SetTextSize(0.04)
#  t.SetTextAlign(11)
#  for i_njb, njb in enumerate(SRnjreg):
#    ratio_st[htb][njb]={}
#    for btb in btreg:
#      ratio_st[htb][njb][btb]=ROOT.TH1F('ratio_stHist','ratio_stHist',3,0,3)
#      ratio_st[htb][njb][btb].SetLineColor(ROOT_colors[i_njb])
#      ratio_st[htb][njb][btb].SetMarkerColor(ROOT_colors[i_njb])
#      ratio_st[htb][njb][btb].SetLineWidth(2)
#      for i_stb, stb in enumerate([(250,350),(350,450),(450,-1)]):
#        antiSelname, antiSelCut = nameAndCut(stb, htb, njb, btb=btb, presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30')
#        rcs = getRCS(cQCD, antiSelCut, 0.75, useWeight = True, weight = 'weight')
#        if rcs['rCS']!=float('nan') and rcs['rCS']> 0.: 
#          ratio_st[htb][njb][btb].SetBinContent(i_stb+1,rcs['rCS'])
#          ratio_st[htb][njb][btb].SetBinError(i_stb+1,rcs['rCSE_sim'])
#        ratio_st[htb][njb][btb].GetXaxis().SetBinLabel(i_stb+1, varBinName(stb,'L_{T}'))
#        ratio_st[htb][njb][btb].GetYaxis().SetTitle('R^{antisel.}_{CS}')
#        ratio_st[htb][njb][btb].GetYaxis().SetRangeUser(0.0,0.05)
##        ratio_st[htb][njb].GetXaxis().SetTitle('F_{sel-to-antisel}')
#      l2.AddEntry(ratio_st[htb][njb][btb], nJetBinName(njb))
#      if first:
#        ratio_st[htb][njb][btb].Draw()
#        first = False
#      else:
#        ratio_st[htb][njb][btb].Draw('same') 
#      l2.Draw()
#      t.DrawLatex(0.2,0.85,'#bf{'+varBinName(htb,'H_{T}')+'}')
#      text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
#      text.DrawLatex(0.75,0.96,"#bf{MC (13 TeV)}")
#      canv2.Print(wwwDir+prefix+'rCS_lt_deltaPhi075'+nameAndCut(None, htb, njetb=None, btb=btb, presel="deltaPhiGT075", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
#      canv2.Print(wwwDir+prefix+'rCS_lt_deltaPhi075'+nameAndCut(None, htb, njetb=None, btb=btb, presel="deltaPhiGT075", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
#      canv2.Print(wwwDir+prefix+'rCS_lt_deltaPhi075'+nameAndCut(None, htb, njetb=None, btb=btb, presel="deltaPhiGT075", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')

#plot F_sel-to-antisel binned in nJets for all ST bins
#ratio_nj={}
#for htb in [(500,-1)]:
#  ratio_nj[htb]={}
#  first = True
#  canv4 = ROOT.TCanvas('canv','canv',600,600)
#  #canv.SetLogy()
#  l3 = ROOT.TLegend(0.65,0.80,0.98,0.95)
#  l3.SetFillColor(0)
#  l3.SetBorderSize(1)
#  l3.SetShadowColor(ROOT.kWhite)
#  text = ROOT.TLatex()
#  text.SetNDC()
#  text.SetTextSize(0.04)
#  text.SetTextAlign(11)
#  t3=ROOT.TLatex()
#  t3.SetNDC()
#  t3.SetTextSize(0.04)
#  t3.SetTextAlign(11)
#  for i_stb, stb in enumerate(ltreg):
#    ratio_nj[htb][stb]={}
#    for btb in btreg:
#      ratio_nj[htb][stb][btb]=ROOT.TH1F('ratio_njHist','ratio_njHist',len(njreg),0,len(njreg))
#      ratio_nj[htb][stb][btb].SetLineColor(ROOT_colors[i_stb])
#      ratio_nj[htb][stb][btb].SetMarkerColor(ROOT_colors[i_stb])
#      ratio_nj[htb][stb][btb].SetLineWidth(2)
#      for i_njb, njb in enumerate(njreg):
#        antiSelname, antiSelCut = nameAndCut(stb, htb, njb, btb=btb, presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30')
#        Selname, SelCut         = nameAndCut(stb, htb, njb, btb=btb, presel=SelStr, charge="", btagVar = 'nBJetMediumCSV30')
#        nSel,nSel_err = getYieldFromChain(cQCD, SelCut, weight = weight_str, returnError=True)
#        nAntiSel,nAntiSel_err = getYieldFromChain(cQCD, antiSelCut, weight = weight_str, returnError=True)
#        rcs = getRCS(cQCD, antiSelCut, 0.75, useWeight = True, weight = 'weight')
#        if rcs['rCS']!=float('nan') and rcs['rCS']> 0.: 
#          ratio_nj[htb][stb][btb].SetBinContent(i_njb+1,rcs['rCS'])
#          ratio_nj[htb][stb][btb].SetBinError(i_njb+1,rcs['rCSE_sim'])
##        try: F=nSel/nAntiSel
##        except ZeroDivisionError: F=float('nan')
##        try: F_err= F*sqrt(nSel_err**2/nSel**2+nAntiSel_err**2/nAntiSel**2)
##        except ZeroDivisionError: F_err=0
##        ratio_nj[htb][stb][btb].SetBinContent(i_njb+1,F)
##        ratio_nj[htb][stb][btb].SetBinError(i_njb+1,F_err)
#        ratio_nj[htb][stb][btb].GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb))
##        ratio_nj[htb][stb][btb].GetYaxis().SetTitle('F_{sel-to-antisel}')
#        ratio_nj[htb][stb][btb].GetYaxis().SetTitle('R^{antisel}_{CS}')
#        ratio_nj[htb][stb][btb].GetYaxis().SetRangeUser(0.0,0.1)
#      l3.AddEntry(ratio_nj[htb][stb][btb], varBinName(stb,'L_{T}'))
#      if first:
#        ratio_nj[htb][stb][btb].Draw()
#        first = False
#      else:
#        ratio_nj[htb][stb][btb].Draw('same') 
#      l3.Draw()
#      t3.DrawLatex(0.2,0.85,'#bf{'+varBinName(htb,'H_{T}')+'}')
#      text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
#      text.DrawLatex(0.75,0.96,"#bf{MC (13 TeV)}")     
#      canv4.Print(wwwDir+prefix+'rCS_nj_deltaPhi075'+nameAndCut(None, htb, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
#      canv4.Print(wwwDir+prefix+'rCS_nj_deltaPhi075'+nameAndCut(None, htb, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
#      canv4.Print(wwwDir+prefix+'rCS_nj_deltaPhi075'+nameAndCut(None, htb, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')

