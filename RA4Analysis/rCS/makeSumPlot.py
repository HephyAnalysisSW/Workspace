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

prefix = 'singleLeptonic_Spring15_'
#path = '/data/'+username+'/Results2015/Prediction_SFTemplate_MC_fullSR_lep_3.0/'

#res = pickle.load(file(path+prefix+'_estimationResults_pkl_kappa_corrected'))
#pickleDir = '/data/dspitzbart/Results2015/Prediction_SFtemplates_validation_lep_data_2.1/'
res = pickle.load(file(pickleDir+prefix+'_estimationResults_pkl'))
#res = pickle.load(file(pickleDir+prefix+'_estimationResults_pkl'))
#res = pickle.load(file('/data/dspitzbart/Results2015/Prediction_SFTemplate_MC_fullSR_lep_3.0/singleLeptonic_Spring15__estimationResults_pkl'))

#signalRegions = validationRegion
#signalRegions = signalRegionCRonly

#triggers = "(HLT_EleHT350||HLT_MuHT350)"
#filters = "Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_CSCTightHaloFilter && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter"
#presel = "((!isData&&singleLeptonic)||(isData&&"+triggers+"&&((muonDataSet&&singleMuonic)||(eleDataSet&&singleElectronic))&&"+filters+"))"
#presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>2 && htJet30j>500"


def getValErrString(val,err, precision=3):
  return str(round(val,precision))+' +/- '+str(round(err,precision))

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

data_truth_H = ROOT.TH1F('data_truth_H','data',bins,0,bins)
data_truth_H.SetLineColor(ROOT.kBlack)
data_truth_H.SetLineWidth(2)
data_truth_H.SetMarkerColor(ROOT.kBlack)
data_truth_H.SetMarkerSize(1.3)


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

pred_H.SetLineColor(ROOT.kGray+1)
pred_H.SetMarkerStyle(1)
pred_H.SetLineWidth(2)

#truth_H.SetLineColor(ROOT.kRed+2)
truth_H.SetLineColor(ROOT.kBlack)
truth_H.SetLineWidth(2)
#truth_H.SetMarkerStyle(29)
truth_H.SetMarkerStyle(8)
truth_H.SetMarkerColor(ROOT.kBlack)
#truth_H.SetMarkerColor(ROOT.kRed+2)
truth_H.SetMarkerSize(1)

kappa = ROOT.TH1F('kappa','kappa_b', bins,0,bins)
kappa.SetLineWidth(2)


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
      if unblinded or validation:
        dcn, dc = nameAndCut(stb, htb, srNJet, (0,0), presel+'&&deltaPhi_Wl>'+str(signalRegions[srNJet][stb][htb]['deltaPhi']))
        data_yield = getYieldFromChain(cData, dc)
        data_truth_H.SetBinContent(i,data_yield)
        data_truth_H.SetBinError(i, sqrt(data_yield))
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
      
      #kappa.SetBinContent(i,res[srNJet][stb][htb]['TT_rCS_fits_MC']['k_0b/1b_btag'])
      #kappa.SetBinError(i,res[srNJet][stb][htb]['TT_rCS_fits_MC']['k_0b/1b_btag_err'])
      
      pred_H.SetBinContent(i, res[srNJet][stb][htb]['tot_pred'])
      pred_H.SetBinError(i,   res[srNJet][stb][htb]['tot_pred_err'])
      predYErr.append(res[srNJet][stb][htb]['tot_pred_err'])
      predXErr.append(0.5)
      predY.append(res[srNJet][stb][htb]['tot_pred'])
      predX.append(i-0.5)
      print 'Predicted:', getValErrString(res[srNJet][stb][htb]['tot_pred'], res[srNJet][stb][htb]['tot_pred_err'])
      if unblinded or validation: print 'Measured: ', getValErrString(data_yield, sqrt(data_yield))
      truth_H.SetBinContent(i,res[srNJet][stb][htb]['tot_truth'])
      truth_H.SetBinError(i,  res[srNJet][stb][htb]['tot_truth_err'])
      truth_H.GetXaxis().SetBinLabel(i, str(i))
      pred_H.GetXaxis().SetBinLabel(i,'#splitline{'+signalRegions[srNJet][stb][htb]['njet']+'}{#splitline{'+signalRegions[srNJet][stb][htb]['LT']+'}{'+signalRegions[srNJet][stb][htb]['HT']+'}}')
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
h_Stack.SetMaximum(100)
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
if unblinded or validation:
  leg.AddEntry(data_truth_H, 'data')

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
if unblinded or validation:
  data_truth_H.Draw('e1p same')

leg.Draw()

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.15,0.96,'CMS #bf{#it{preliminary}}')
latex1.DrawLatex(0.78,0.96,"L=2.1fb^{-1} (13TeV)")

pad1.SetLogy()

can.cd()

ratio = ROOT.TH1F('ratio_mc','ratio pred/mc truth',bins,0,bins)
ratio.Sumw2()
#ratio = pred_H.Clone()
ratio = truth_H.Clone()
#ratio.Divide(truth_H)
ratio.Divide(pred_H)
ratio.SetMarkerStyle(29)
ratio.SetMarkerColor(ROOT.kRed+2)
ratio.SetMarkerSize(2)
ratio.SetLineColor(ROOT.kRed+2)
ratio.GetXaxis().SetTitle('')

setNiceBinLabel(ratio, validationRegionAll)

ratio2 = ROOT.TH1F('ratio_d','ratio pred/data',bins,0,bins)
ratio2.Sumw2()
#ratio2 = pred_H.Clone()
ratio2 = truth_H.Clone()
#ratio2.Divide(data_truth_H)
ratio2.Divide(pred_H)
ratio2.SetLineColor(ROOT.kBlack)
ratio2.SetMarkerStyle(8)
ratio2.SetMarkerSize(1.3)
ratio2.GetXaxis().SetTitle('')

setNiceBinLabel(ratio2, signalRegion3fb)

pad2=ROOT.TPad("pad2","datavsMC",0.,0.,1.,.3)
pad2.SetLeftMargin(0.15)
pad2.SetBottomMargin(0.3)
pad2.SetTopMargin(0.02)
pad2.SetGrid()
pad2.Draw()
pad2.cd()
#ratio.GetXaxis().SetTitle('Signal Region #')
ratio2.GetXaxis().SetTitleSize(0.13)
ratio2.GetXaxis().SetLabelSize(0.11)
ratio2.GetXaxis().SetNdivisions(508)
ratio2.GetYaxis().SetTitle('data/pred.')
ratio2.GetYaxis().SetTitleSize(0.13)
ratio2.GetYaxis().SetLabelSize(0.13)
ratio2.GetYaxis().SetTitleOffset(0.4)
ratio2.GetYaxis().SetNdivisions(508)
ratio2.SetMinimum(0.)
ratio2.SetMaximum(2.2)
ratio2.Draw('e1p')
#ratio2.Draw('e1p same')

can.cd()

can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2015/Prediction_'+predictionName+'_'+str(lumi)+'.png')
can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2015/Prediction_'+predictionName+'_'+str(lumi)+'.root')
can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2015/Prediction_'+predictionName+'_'+str(lumi)+'.pdf')

can2 = ROOT.TCanvas('can2','can2',700,700)

kappa.Draw('e1 hist')
