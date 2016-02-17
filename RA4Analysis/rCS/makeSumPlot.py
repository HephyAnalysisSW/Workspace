import ROOT
import pickle

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getPropagatedError
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from rCShelpers import *
import math
from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *
from array import array

from predictionConfig import *

cData = getChain([single_mu_Run2015D, single_ele_Run2015D], histname='')
isData = True
predictionName = 'SFtemplates_fullSR_lep_data'

ROOT.gStyle.SetOptTitle(0);
ROOT.gStyle.SetOptStat('')

useWcorrection  = False
useTTcorrection = False
signal          = False
withSystematics = True
applyKappa      = True

showMCtruth     = True
signal = True

weight_str, weight_err_str = makeWeight(lumi, sampleLumi, reWeight=MCweight)

prefix = 'singleLeptonic_Spring15_'
#path = '/data/'+username+'/Results2015/Prediction_SFTemplate_MC_fullSR_lep_3.0/'
#pickleDir = '/data/easilar/Results2016/Prediction_SFtemplates_fullSR_lep_data_2p25/'
#pickleDir = '/data/dspitzbart/Results2015/Prediction_SFtemplates_validation_lep_data_2.1/'
pickleDir = '/data/dspitzbart/Results2016/Prediction_SFtemplates_fullSR_lep_data_2p25/'
res = pickle.load(file(pickleDir+'resultsFinal_withSystematics_pkl'))
if withSystematics:
  sys = pickle.load(file(pickleDir+'resultsFinal_withSystematics_pkl'))

#sig = pickle.load(file('/data/easilar/Spring15/25ns/allSignals_2p3_v2_pkl'))
sig = pickle.load(file('/data/dspitzbart/Results2016/signal_unc_pkl'))

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
data_truth_H.SetBinErrorOption(ROOT.TH1F.kPoisson)


benchmark1_H = ROOT.TH1F('benchmark1_H','T5q^{4}WW 1.0/0.7',bins,0,bins)
benchmark2_H = ROOT.TH1F('benchmark2_H','T5q^{4}WW 1.2/0.8',bins,0,bins)
benchmark3_H = ROOT.TH1F('benchmark3_H','T5q^{4}WW 1.5/0.1',bins,0,bins)

benchmark1_H.SetLineColor(ROOT.kCyan-5)
benchmark2_H.SetLineColor(ROOT.kOrange+6)
benchmark3_H.SetLineColor(ROOT.kRed+1)

benchmark1_H.SetLineWidth(3)
benchmark2_H.SetLineWidth(3)
benchmark3_H.SetLineWidth(3)

benchmark1_H.SetMarkerSize(0)
benchmark2_H.SetMarkerSize(0)
benchmark3_H.SetMarkerSize(0)

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
truth_H.SetBinErrorOption(ROOT.TH1F.kPoisson)


pred_H.SetLineColor(ROOT.kGray+1)
pred_H.SetMarkerStyle(1)
pred_H.SetLineWidth(2)

truth_H.SetLineColor(ROOT.kBlack)
truth_H.SetLineWidth(2)
truth_H.SetMarkerStyle(8)
truth_H.SetMarkerColor(ROOT.kBlack)

kappa_tt = ROOT.TH1F('kappa_tt','kappa', bins,0,bins)
kappa_tt.SetLineWidth(1)
kappa_tt.SetMarkerStyle(21)
kappa_tt.SetMarkerSize(1.5)
kappa_tt.SetMarkerColor(color('ttjets'))
kappa_tt.SetLineColor(color('ttjets'))

kappa_W = ROOT.TH1F('kappa_W','kappa', bins,0,bins)
kappa_W.SetLineWidth(1)
kappa_W.SetMarkerStyle(22)
kappa_W.SetMarkerSize(1.5)
kappa_W.SetMarkerColor(color('wjets'))
kappa_W.SetLineColor(color('wjets'))

one = ROOT.TH1F('one','one', bins,0,bins)
one.SetLineStyle(2)

drawOption = 'hist ][ e0'
drawOptionSame = drawOption + 'same'

predXErr = []
predYErr = []
predX = []
predY = []

total_meas      = 0
total_yield     = 0
total_err       = 0
total_stat_var  = 0

fmt = '{0:30} {1:>6}'

ratioWithE = []

ratioXErr = []
ratioYUp = []
ratioYDown = []
ratioX = []
ratioY = []

i=1
for srNJet in sorted(signalRegions):
  for stb in sorted(signalRegions[srNJet]):
    for htb in sorted(signalRegions[srNJet][stb]):
      print
      print 'SR'+str(i)

      #calculate final tt yields and errors
      kappa_tt.SetBinContent(i,res[srNJet][stb][htb]['TT_kappa'])
      if withSystematics:
        kappa_tt.SetBinError(i, res[srNJet][stb][htb]['TT_kappa_err_syst'])
      else:
        kappa_tt.SetBinError(i, res[srNJet][stb][htb]['TT_kappa_err'])

      print fmt.format('tt w/o kappa, syst:', getValErrString(res[srNJet][stb][htb]['TT_pred'], res[srNJet][stb][htb]['TT_pred_err']))
      print fmt.format('tt with kappa, syst:',getValErrString(res[srNJet][stb][htb]['TT_pred_final'], res[srNJet][stb][htb]['TT_pred_final_err']))

      #calculate final W yields and errors
      kappa_W.SetBinContent(i,res[srNJet][stb][htb]['W_kappa'])
      if withSystematics:
        kappa_W.SetBinError(i, res[srNJet][stb][htb]['W_kappa_err_syst'])
      else:
        kappa_W.SetBinError(i, res[srNJet][stb][htb]['W_kappa_err'])
      print fmt.format('W w/o kappa, syst:', getValErrString(res[srNJet][stb][htb]['W_pred'], res[srNJet][stb][htb]['W_pred_err']))
      print fmt.format('W with kappa, syst:',getValErrString(res[srNJet][stb][htb]['W_pred_final'], res[srNJet][stb][htb]['W_pred_final_err']))
      
      #calculate final rest yields and errors
      print fmt.format('rest w/o syst:', getValErrString(res[srNJet][stb][htb]['Rest_truth'], res[srNJet][stb][htb]['Rest_truth_err']))
      print fmt.format('rest with syst:', getValErrString(res[srNJet][stb][htb]['Rest_truth_final'], res[srNJet][stb][htb]['Rest_truth_final_err']))

      print fmt.format('total MC', getValErrString(res[srNJet][stb][htb]['tot_truth'],res[srNJet][stb][htb]['tot_truth_err']))
      print fmt.format('- total pred w/o kappa, syst:', getValErrString(res[srNJet][stb][htb]['tot_pred'], res[srNJet][stb][htb]['tot_pred_err']))
      print fmt.format('- total pred with kappa, syst:', getValErrString(res[srNJet][stb][htb]['tot_pred_final'], res[srNJet][stb][htb]['tot_pred_final_err']))
      
      if not applyKappa:
        tt_pred_H.SetBinContent(i, res[srNJet][stb][htb]['TT_pred'])
        tt_pred_H.SetBinError(i,   res[srNJet][stb][htb]['TT_pred_err'])
        
        w_pred_H.SetBinContent(i, res[srNJet][stb][htb]['W_pred'])
        w_pred_H.SetBinError(i,   res[srNJet][stb][htb]['W_pred_err'])
      
      else:
        tt_pred_H.SetBinContent(i, res[srNJet][stb][htb]['TT_pred_final'])
        tt_pred_H.SetBinError(i,   res[srNJet][stb][htb]['TT_pred_final_err'])

        w_pred_H.SetBinContent(i, res[srNJet][stb][htb]['W_pred_final'])
        w_pred_H.SetBinError(i,   res[srNJet][stb][htb]['W_pred_final_err'])

      tt_truth_H.SetBinContent(i,res[srNJet][stb][htb]['TT_truth'])
      tt_truth_H.SetBinError(i,  res[srNJet][stb][htb]['TT_truth_err'])


      w_truth_H.SetBinContent(i,res[srNJet][stb][htb]['W_truth'])
      w_truth_H.SetBinError(i,  res[srNJet][stb][htb]['W_truth_err'])

      rest_H.SetBinContent(i, res[srNJet][stb][htb]['Rest_truth'])
      rest_H.SetBinError(i,   res[srNJet][stb][htb]['Rest_truth_err'])

      one.SetBinContent(i,1)
      if not applyKappa:
        pred_H.SetBinContent(i, res[srNJet][stb][htb]['tot_pred'])
        pred_H.SetBinError(i,   res[srNJet][stb][htb]['tot_pred_err'])
      else:
        pred_H.SetBinContent(i, res[srNJet][stb][htb]['tot_pred_final'])
        pred_H.SetBinError(i,   res[srNJet][stb][htb]['tot_pred_final_err'])
      
      if withSystematics:
        predYErr.append(res[srNJet][stb][htb]['tot_pred_final_err'])
      else:
        predYErr.append(res[srNJet][stb][htb]['tot_pred_err'])
      predXErr.append(0.5)
      if not applyKappa:
        predY.append(res[srNJet][stb][htb]['tot_pred'])
      else:
        predY.append(res[srNJet][stb][htb]['tot_pred_final'])
      predX.append(i-0.5)

      if unblinded or validation:
        if isData:
          weight = 'weight'
          dcn, dc = nameAndCut(stb, htb, srNJet, (0,0), presel+'&&deltaPhi_Wl>'+str(signalRegions[srNJet][stb][htb]['deltaPhi']))
        else:
          weight =weight_str+'*weightBTag0_SF'
          dcn, dc = nameAndCut(stb, htb, srNJet, (0,-1), presel+'&&deltaPhi_Wl>'+str(signalRegions[srNJet][stb][htb]['deltaPhi']))
        data_yield = getYieldFromChain(cData, dc,weight)
        data_truth_H.SetBinContent(i,data_yield)
        #data_truth_H.SetBinError(i, sqrt(data_yield))
        data_truth_H.GetBinErrorLow(i)
        data_truth_H.GetBinErrorUp(i)
        print fmt.format('- Measured: ', getValErrString(data_yield, sqrt(data_yield)))
        truth_H.SetBinContent(i,data_yield)
        #truth_H.SetBinError(i,  sqrt(data_yield))

        truth_H.GetXaxis().SetBinLabel(i, str(i))
        truthLowE = truth_H.GetBinErrorLow(i)
        truthUpE = truth_H.GetBinErrorUp(i)
        ratioUp = getPropagatedError(truth_H.GetBinContent(i), truthUpE, res[srNJet][stb][htb]['tot_pred_final'], res[srNJet][stb][htb]['tot_pred_final_err'], returnCalcResult=True)
        ratioLow = getPropagatedError(truth_H.GetBinContent(i), truthLowE, res[srNJet][stb][htb]['tot_pred_final'], res[srNJet][stb][htb]['tot_pred_final_err'], returnCalcResult=True)
        ratioWithE.append({'v': ratioUp[0],'up': ratioUp[1], 'down': ratioLow[1]})
        print {'v': ratioUp[0],'up': ratioUp[1], 'down': ratioLow[1]}

        ratioX.append(i-0.5)
        ratioY.append(ratioUp[0])
        ratioXErr.append(0.5)
        ratioYUp.append(ratioUp[1])
        ratioYDown.append(ratioLow[1])


      else:
        truth_H.SetBinContent(i,res[srNJet][stb][htb]['tot_truth'])
        truth_H.SetBinError(i,  res[srNJet][stb][htb]['tot_truth_err'])
        truth_H.GetXaxis().SetBinLabel(i, str(i))

      if signal:
        benchmark1_H.SetBinContent(i,res[srNJet][stb][htb]['tot_pred_final']+sig[srNJet][stb][htb][1000][700]['yield_MB_SR'])
        benchmark2_H.SetBinContent(i,res[srNJet][stb][htb]['tot_pred_final']+sig[srNJet][stb][htb][1200][800]['yield_MB_SR'])
        benchmark3_H.SetBinContent(i,res[srNJet][stb][htb]['tot_pred_final']+sig[srNJet][stb][htb][1500][100]['yield_MB_SR'])

      if unblinded:
        total_meas     += data_yield
        total_yield     += res[srNJet][stb][htb]['tot_pred_final']
        total_err       += res[srNJet][stb][htb]['systematics']['total']*res[srNJet][stb][htb]['tot_pred_final']
        total_stat_var  += res[srNJet][stb][htb]['tot_pred_final_err']**2

      pred_H.GetXaxis().SetBinLabel(i,'#splitline{'+signalRegions[srNJet][stb][htb]['njet']+'}{#splitline{'+signalRegions[srNJet][stb][htb]['LT']+'}{'+signalRegions[srNJet][stb][htb]['HT']+'}}')
      i+=1


if unblinded:
  print
  print
  print 'Sum over all SRs:'
  print fmt.format('- Predicted: ', getValErrString(total_yield, sqrt(total_err**2+total_stat_var)))
  print fmt.format('- Measured: ', getValErrString(total_meas, sqrt(total_meas)))

print
print
#pred error
ax = array('d',predX)
ay = array('d',predY)
aexh = array('d',predXErr)
aexl = array('d',predXErr)
aeyh = array('d',predYErr)
aeyl = array('d',predYErr)

#ratio errors
rx    = array('d',ratioX)
ry    = array('d',ratioY)
rexh  = array('d',ratioXErr)
rexl  = array('d',ratioXErr)
reyh  = array('d',ratioYErr)
reyl  = array('d',ratioYErr)

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
if isData:
  if unblinded or validation:
    leg.AddEntry(truth_H, 'data')
  else:
    leg.AddEntry(truth_H, 'MC truth')
else:
  if showMCtruth:
    leg.AddEntry(truth_H)
leg.AddEntry(tt_pred_H,'','f')
leg.AddEntry(w_pred_H,'','f')
leg.AddEntry(rest_H,'','f')

h_Stack.Draw('hist')
h_Stack.GetYaxis().SetTitle('Events')
h_Stack.GetXaxis().SetBinLabel(1,'')

if signal:
  benchmark1_H.Draw('hist same')
  benchmark2_H.Draw('hist same')
  benchmark3_H.Draw('hist same')

  leg3 = ROOT.TLegend(0.35,0.75,0.65,0.9)
  leg3.SetFillColor(ROOT.kWhite)
  leg3.SetShadowColor(ROOT.kWhite)
  leg3.SetBorderSize(0)
  leg3.SetTextSize(0.035)
  leg3.AddEntry(benchmark1_H)
  leg3.AddEntry(benchmark2_H)
  leg3.AddEntry(benchmark3_H)
  leg3.Draw()


h_Stack.GetYaxis().SetTitleOffset(0.8)
h_Stack.GetYaxis().SetNdivisions(508)
pred_err = ROOT.TGraphAsymmErrors(bins, ax, ay, aexl, aexh, aeyl, aeyh)
pred_err.SetFillColor(ROOT.kGray+1)
pred_err.SetFillStyle(3244)
pred_err.Draw('2 same')
truth_H.SetMarkerStyle(22)
if unblinded or validation:
  truth_H.SetMarkerStyle(20)
  truth_H.Draw('e0p same')
else:
  truth_H.Draw('hist e same')

leg.Draw()

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.15,0.96,'CMS #bf{#it{preliminary}}')
latex1.DrawLatex(0.78,0.96,"L="+printlumi+"fb^{-1} (13TeV)")

pad1.SetLogy()

can.cd()

ratio2 = ROOT.TH1F('ratio_d','ratio pred/data',bins,0,bins)
#ratio2.Sumw2()
ratio2 = truth_H.Clone()
ratio2.Divide(pred_H)
ratio2.SetLineColor(ROOT.kBlack)
ratio2.SetMarkerStyle(8)
ratio2.SetMarkerSize(1.3)
ratio2.GetXaxis().SetTitle('')

setNiceBinLabel(ratio2, signalRegions)

pad2=ROOT.TPad("pad2","datavsMC",0.,0.,1.,.3)
pad2.SetLeftMargin(0.15)
pad2.SetBottomMargin(0.3)
pad2.SetTopMargin(0.02)
pad2.SetGrid()
pad2.Draw()
pad2.cd()
ratio2.GetXaxis().SetTitleSize(0.13)
ratio2.GetXaxis().SetLabelSize(0.11)
ratio2.GetXaxis().SetNdivisions(508)
if validation or unblinded:
  ratio2.GetYaxis().SetTitle('data/pred.')
else:
  ratio2.GetYaxis().SetTitle('MC/pred.')
ratio2.GetYaxis().SetTitleSize(0.13)
ratio2.GetYaxis().SetLabelSize(0.13)
ratio2.GetYaxis().SetTitleOffset(0.4)
ratio2.GetYaxis().SetNdivisions(304)
ratio2.SetMinimum(0.)
ratio2.SetMaximum(3.2)
ratio2.Draw('e0p')

can.cd()

if not unblinded:
  suffix = '_blind'
else:
  suffix = ''

can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016/sumPlot/Prediction_'+predictionName+'_'+lumistr+suffix+'_update_p2.png')
can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016/sumPlot/Prediction_'+predictionName+'_'+lumistr+suffix+'_update_p2.root')
can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016/sumPlot/Prediction_'+predictionName+'_'+lumistr+suffix+'_update_p2.pdf')

can2 = ROOT.TCanvas('can2','can2',700,700)

one.SetMaximum(3.5)
one.SetMinimum(0.)

leg2 = ROOT.TLegend(0.75,0.85,0.98,0.95)
leg2.SetFillColor(ROOT.kWhite)
leg2.SetShadowColor(ROOT.kWhite)
leg2.SetBorderSize(1)
leg2.SetTextSize(0.04)
leg2.AddEntry(kappa_tt,'t#bar{t}+jets')
leg2.AddEntry(kappa_W,'W+jets')

setNiceBinLabel(one, signalRegions)
one.GetYaxis().SetTitle('#kappa')
one.GetXaxis().SetLabelSize(0.04)

latex2 = ROOT.TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.04)
latex2.SetTextAlign(11)

one.Draw('hist')
kappa_tt.Draw('e1p same')
kappa_W.Draw('e1p same')

leg2.Draw()

latex2.DrawLatex(0.17,0.96,'CMS #bf{#it{simulation}}')
latex2.DrawLatex(0.7,0.96,"L="+printlumi+"fb^{-1} (13TeV)")

can2.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016/sumPlot/'+predictionName+'_Kappa_update.png')
can2.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016/sumPlot/'+predictionName+'_Kappa_update.root')
can2.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016/sumPlot/'+predictionName+'_Kappa_update.pdf')

