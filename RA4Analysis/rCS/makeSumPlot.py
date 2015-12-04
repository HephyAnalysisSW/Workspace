import ROOT
import pickle

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from rCShelpers import *
import math
from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from array import array

from predictionConfig import *

ROOT.gStyle.SetOptTitle(0);
ROOT.gStyle.SetOptStat('')

useWcorrection = False
useTTcorrection = False
signal = False

#prefix = 'singleLeptonic_Spring15_'
#path = '/data/'+username+'/Results2015/Prediction_SFTemplate_MC_fullSR_lep_3.0/'

#res = pickle.load(file(path+prefix+'_estimationResults_pkl_kappa_corrected'))
res = pickle.load(file(pickleDir+prefix+'_estimationResults_pkl_kappa_btag_corrected'))
res = pickle.load(file(pickleDir+prefix+'_estimationResults_pkl'))

signalRegions = signalRegion3fbReduced
#signalRegions = signalRegionCRonly


rowsNJet = {}
rowsSt = {}
bins = 0
for srNJet in sorted(signalRegions):
  rowsNJet[srNJet] = {}
  rowsSt[srNJet] = {}
  rows = 0
  for stb in sorted(signalRegions[srNJet]):
    rows += len(signalRegions[srNJet][stb])
    rowsSt[srNJet][stb] = {'n':len(signalRegions[srNJet][stb])}
  rowsNJet[srNJet] = {'nST':len(signalRegions[srNJet]), 'n':rows}
  bins += rows



tt_pred_H  = ROOT.TH1F('tt_pred_H','t#bar{t}+Jets pred.',bins,0,bins)
tt_truth_H = ROOT.TH1F('tt_truth_H','tt+Jets truth',bins,0,bins)
tt_pred_H.SetLineColor(color('ttJets'))
tt_pred_H.SetFillColor(color('ttJets')-2)
tt_pred_H.SetLineWidth(2)
tt_truth_H.SetLineColor(color('ttJets')-1)
tt_truth_H.SetLineWidth(2)

w_pred_H  = ROOT.TH1F('w_pred_H','W+Jets pred.', bins,0,bins)
w_truth_H = ROOT.TH1F('w_truth_H','W+Jets truth', bins,0,bins)
w_pred_H.SetLineColor(color('wJets')+1)
w_pred_H.SetFillColor(color('wJets'))
w_pred_H.SetLineWidth(2)
w_truth_H.SetLineColor(color('wJets')-1)
w_truth_H.SetLineWidth(2)

rest_H = ROOT.TH1F('rest_H','EWK rest', bins,0,bins)
rest_H.SetLineColor(color('TTVH')+1)
rest_H.SetFillColor(color('TTVH'))
rest_H.SetLineWidth(2)
w_truth_H.SetLineColor(color('DY'))

pred_H  = ROOT.TH1F('pred_H','total pred.', bins,0,bins)
pred_H.SetBarWidth(0.4)
pred_H.SetBarOffset(0.1)
truth_H = ROOT.TH1F('truth_H','Total MC truth',bins,0,bins)
truth_H.SetBarWidth(0.4)
truth_H.SetBarOffset(0.1)
pred_H.SetLineColor(ROOT.kGray+1)
pred_H.SetMarkerStyle(1)
pred_H.SetLineWidth(2)
truth_H.SetLineColor(ROOT.kBlack)
truth_H.SetLineWidth(2)



drawOption = 'hist ][ e1'
drawOptionSame = drawOption + 'same'

predXErr = []
predYErr = []
predX = []
predY = []

i=1
for srNJet in sorted(signalRegions):
  for stb in sorted(signalRegions[srNJet]):
    for htb in sorted(signalRegions[srNJet][stb]):
      #print 1
      tt_pred_H.SetBinContent(i, res[srNJet][stb][htb]['TT_pred'])
      tt_pred_H.SetBinError(i,   res[srNJet][stb][htb]['TT_pred_err'])
      tt_truth_H.SetBinContent(i,res[srNJet][stb][htb]['TT_truth'])
      tt_truth_H.SetBinError(i,  res[srNJet][stb][htb]['TT_truth_err'])
      
      w_pred_H.SetBinContent(i, res[srNJet][stb][htb]['W_pred'])
      w_pred_H.SetBinError(i,   res[srNJet][stb][htb]['W_pred_err'])
      w_truth_H.SetBinContent(i,res[srNJet][stb][htb]['W_truth'])
      w_truth_H.SetBinError(i,  res[srNJet][stb][htb]['W_truth_err'])
      
      rest_H.SetBinContent(i,res[srNJet][stb][htb]['Rest_truth'])
      rest_H.SetBinError(i,  res[srNJet][stb][htb]['Rest_truth_err'])

      pred_H.SetBinContent(i, res[srNJet][stb][htb]['tot_pred'])
      pred_H.SetBinError(i,   res[srNJet][stb][htb]['tot_pred_err'])
      predYErr.append(res[srNJet][stb][htb]['tot_pred_err'])
      predXErr.append(0.5)
      predY.append(res[srNJet][stb][htb]['tot_pred'])
      predX.append(i-0.5)
      truth_H.SetBinContent(i,res[srNJet][stb][htb]['tot_truth'])
      truth_H.SetBinError(i,  res[srNJet][stb][htb]['tot_truth_err'])
      truth_H.GetXaxis().SetBinLabel(i, str(i))
      pred_H.GetXaxis().SetBinLabel(i, str(i))
      i+=1

ax = array('d',predX)
ay = array('d',predY)
aexh = array('d',predXErr)
aexl = array('d',predXErr)
aeyh = array('d',predYErr)
aeyl = array('d',predYErr)

can = ROOT.TCanvas('can','can',700,700)

pad1=ROOT.TPad("pad1","MyTitle",0.,0.3,1.,1.)
pad1.SetLeftMargin(0.15)
pad1.SetBottomMargin(0.02)
pad1.Draw()
pad1.cd()

h_Stack = ROOT.THStack('h_Stack','Stack')
h_Stack.Add(rest_H)
h_Stack.Add(w_pred_H)
h_Stack.Add(tt_pred_H)
h_Stack.SetMaximum(30)
h_Stack.SetMinimum(0.080)

#h_Stack.GetYaxis().SetTitle('Signal Region #')

truth_H.SetMaximum(20)
truth_H.GetYaxis().SetTitle('Events')
truth_H.GetXaxis().SetTitle('Signal Region #')
truth_H.GetYaxis().SetTitleSize(0.06)
truth_H.GetYaxis().SetLabelSize(0.06)

leg = ROOT.TLegend(0.65,0.7,0.98,0.95)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.045)
leg.AddEntry(truth_H)
leg.AddEntry(tt_pred_H,'','f')
leg.AddEntry(w_pred_H,'','f')
leg.AddEntry(rest_H,'','f')

h_Stack.Draw('hist')
h_Stack.GetYaxis().SetTitle('Events')
h_Stack.GetXaxis().SetBinLabel(1,'')

h_Stack.GetYaxis().SetTitleOffset(0.8)
h_Stack.GetYaxis().SetNdivisions(508)
#predError = ROOT.TGraphError(pred_H)
#pred_H.Draw('e1 same')
pred_err = ROOT.TGraphAsymmErrors(bins, ax, ay, aexl, aexh, aeyl, aeyh)
pred_err.SetFillColor(ROOT.kGray+1)
pred_err.SetFillStyle(3244)
pred_err.Draw('2 same')
truth_H.Draw('e1p same')


leg.Draw()

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.15,0.96,'CMS Simulation')
latex1.DrawLatex(0.73,0.96,"L=1.55fb^{-1} (13TeV)")

pad1.SetLogy()

can.cd()

ratio = ROOT.TH1F('ratio','ratio',bins,0,bins)
ratio.Sumw2()
ratio = pred_H.Clone()
ratio.Divide(truth_H)

pad2=ROOT.TPad("pad2","datavsMC",0.,0.,1.,.3)
pad2.SetLeftMargin(0.15)
pad2.SetBottomMargin(0.3)
pad2.SetTopMargin(0.02)
pad2.SetGrid()
pad2.Draw()
pad2.cd()
ratio.SetLineColor(ROOT.kBlack)
ratio.SetMarkerStyle(8)
ratio.GetXaxis().SetTitle('Signal Region #')
ratio.GetXaxis().SetTitleSize(0.13)
ratio.GetXaxis().SetLabelSize(0.21)
ratio.GetXaxis().SetNdivisions(508)
ratio.GetYaxis().SetTitle('pred./truth')
ratio.GetYaxis().SetTitleSize(0.13)
ratio.GetYaxis().SetLabelSize(0.13)
ratio.GetYaxis().SetTitleOffset(0.4)
ratio.GetYaxis().SetNdivisions(508)
ratio.SetMinimum(0.)
ratio.SetMaximum(2.2)
ratio.Draw('e1p')

can.cd()

