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

ROOT.gStyle.SetOptTitle(0);
ROOT.gStyle.SetOptStat('')


latextitle = 'Simulation'

weight_str, weight_err_str = makeWeight(lumi, sampleLumi, reWeight=MCweight)

#pickleDir = '/data/dspitzbart/Results2016/QCDEstimation/20160623_v3_QCDestimation_2015SR_MC2p57fb_pkl'
#pickleDir = '/data/dspitzbart/Results2016/QCDEstimation/20160628_QCDestimation_2016SR_preapp_MC10fb_pkl_update'
#pickleDir = '/data/dspitzbart/Results2016/QCDEstimation/20160714_QCDestimation_2016SR_MC7p62fb_pkl'+'update'
#pickleDir = '/data/dspitzbart/Results2016/QCDEstimation/20160628_QCDestimation_2016SR_preapp_100p_MC10fb_pkl'
#pickleDir = '/data/dspitzbart/Results2016/QCDEstimation/20160707_QCDestimation_2016SR_selTemplate_Ltbinned_MC4fb_pkl'
#pickleDir = '/data/dspitzbart/Results2016/QCDEstimation/20160212_QCDestimation_MC2p25fb_pkl'

pickleDir = '/afs/hephy.at/data/dspitzbart01/RA4/Moriond2017/QCDEstimation/20161220_QCDestimation_Moriond17SR_v3_MC36p5fb_orig'

#signalRegions = signalRegion3fb
printlumi = '36.5'

QCD_pred = pickle.load(file(pickleDir))

def getValErrString(val,err, precision=3):
  return str(round(val,precision))+' +/- '+str(round(err,precision))

signalRegions = signalRegions_Moriond2017

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


QCD_H = ROOT.TH1F('rest_H','QCD', bins,0,bins)
QCD_H.SetLineColor(color('QCD'))
QCD_H.SetFillColorAlpha(color('QCD'), 0.8)
QCD_H.SetLineWidth(2)

truth_H  = ROOT.TH1F('truth_H','QCD MC truth', bins,0,bins)
truth_H.SetBarWidth(0.4)
truth_H.SetBarOffset(0.1)


one = ROOT.TH1F('one','one', bins,0,bins)
one.SetLineStyle(2)
one.SetLineWidth(2)

drawOption = 'hist ][ e0'
drawOptionSame = drawOption + 'same'

predXErr = []
predYErr = []
predX = []
predY = []

predRelYErr = []
predRelY = []

ratioXErr = []
ratioYUp = []
ratioYDown = []
ratioX = []
ratioY = []

dataPXErr = []
dataPX = []
dataPY = []
dataPYUp = []
dataPYDown = []



fmt = '{0:30} {1:>6}'
fmt2 = '{0:10}{1:>20}'

ratioWithE = []

lumi = 2.57
sampleLumi = 3.0 #post processed sample already produced with 2.25fb-1
weight_str, weight_err_str = makeWeight(lumi, sampleLumi, reWeight='(1)')

i=1
for srNJet in sorted(signalRegions):
  for stb in sorted(signalRegions[srNJet]):
    for htb in sorted(signalRegions[srNJet][stb]):
      print
      print 'SR'+str(i)
      dPhi = signalRegions[srNJet][stb][htb]['deltaPhi']
      
      n,c = nameAndCut(stb,htb,srNJet,(0,0),presel_MC)
      njb = srNJet
      btb = (0,0)
      #njb = srNJet
      yQCD_pred       = QCD_pred[njb][stb][htb][btb][dPhi]['NQCDpred']
      yQCD_pred_err   = QCD_pred[njb][stb][htb][btb][dPhi]['NQCDpred_err']
      yQCD_truth      = QCD_pred[njb][stb][htb][btb][dPhi]['NQCDSelMC']
      yQCD_truth_err  = QCD_pred[njb][stb][htb][btb][dPhi]['NQCDSelMC_err']
      #yQCD_truth, yQCD_truth_err = getYieldFromChain(cQCD, cutString=c, weight=weight_str, returnError=True)

      QCD_H.SetBinContent(i, yQCD_pred)
      truth_H.SetBinContent(i, yQCD_truth)

      predYErr.append(yQCD_pred_err)
      predRelYErr.append(yQCD_pred_err/yQCD_pred)
      predXErr.append(0.5)
      predY.append(yQCD_pred)
      predX.append(i-0.5)
      predRelY.append(1)
      
      ratio, ratio_err = getPropagatedError(yQCD_truth, yQCD_truth_err, yQCD_pred, yQCD_pred_err, returnCalcResult=True)
      ratio_err = yQCD_truth_err/yQCD_truth
        
      ratioX.append(i-0.5)
      ratioY.append(ratio)
      ratioXErr.append(0)
      ratioYUp.append(ratio_err)
      ratioYDown.append(ratio_err)
      
      dataPX.append(i-0.5)
      dataPY.append(yQCD_truth)
      dataPXErr.append(0)
      dataPYUp.append(yQCD_truth_err)
      dataPYDown.append(yQCD_truth_err)

      #QCD_H.GetXaxis().SetBinLabel(i,'#splitline{'+signalRegions[srNJet][stb][htb]['njet']+'}{#splitline{'+signalRegions[srNJet][stb][htb]['LT']+'}{'+signalRegions[srNJet][stb][htb]['HT']+'}}')
      i+=1


#if unblinded:
#  print
#  print
#  print 'Sum over all SRs:'
#  print fmt.format('- Predicted: ', getValErrString(total_yield, sqrt(total_err**2+total_stat_var)))
#  print fmt.format('- Measured: ', getValErrString(total_meas, sqrt(total_meas)))

print
print
#pred error
ax = array('d',predX)
ay = array('d',predY)
aexh = array('d',predXErr)
aexl = array('d',predXErr)
aeyh = array('d',predYErr)
aeyl = array('d',predYErr)


#pred rel error for ratio plot
a_r_eyh = array('d',predRelYErr)
a_r_eyl = array('d',predRelYErr)
a_r_y = array('d',predRelY)

#ratio errors
rx    = array('d',ratioX)
ry    = array('d',ratioY)
rexh  = array('d',ratioXErr)
rexl  = array('d',ratioXErr)
reyh  = array('d',ratioYUp)
reyl  = array('d',ratioYDown)

#data points
dx    = array('d',dataPX)
dy    = array('d',dataPY)
dexh  = array('d',dataPXErr)
dexl  = array('d',dataPXErr)
deyh  = array('d',dataPYUp)
deyl  = array('d',dataPYDown)

can = ROOT.TCanvas('can','can',700,700)

pad1=ROOT.TPad("pad1","MyTitle",0.,0.3,1.,1.)
pad1.SetLeftMargin(0.15)
pad1.SetBottomMargin(0.02)
pad1.Draw()
pad1.cd()


QCD_H.SetMaximum(8000)
QCD_H.SetMinimum(0.08)
QCD_H.GetXaxis().SetLabelSize(0)

QCD_H.Draw()

data_err = ROOT.TGraphAsymmErrors(bins, dx, dy, dexl, dexh, deyl, deyh)
data_err.SetMarkerStyle(10)
data_err.SetMarkerSize(1)
data_err.SetLineWidth(2)

pred_err = ROOT.TGraphAsymmErrors(bins, ax, ay, aexl, aexh, aeyl, aeyh)
pred_err.SetFillColor(ROOT.kGray+1)
pred_err.SetLineWidth(0)
pred_err.SetFillStyle(3444)


leg = ROOT.TLegend(0.65,0.75,0.98,0.95)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.045)
#leg.AddEntry(None,'bla','')
leg.AddEntry(truth_H,'QCD MC truth','f')
leg.AddEntry(QCD_H,'QCD prediction','f')
leg.AddEntry(pred_err,'Pred. Uncertainty','f')

pred_err.Draw('2 same')
truth_H.SetMarkerStyle(22)
truth_H.Draw('hist e same')

pred_rel_err = ROOT.TGraphAsymmErrors(bins, ax, a_r_y, aexl, aexh, a_r_eyl, a_r_eyh)
pred_rel_err.SetFillColor(ROOT.kGray+1)
pred_rel_err.SetFillStyle(3444)
#pred_err.Draw('2 same')

ratio_err = ROOT.TGraphAsymmErrors(bins, rx, ry, rexl, rexh, reyl, reyh)
ratio_err.SetMarkerStyle(10)
ratio_err.SetMarkerSize(1.1)
ratio_err.SetLineWidth(2)

leg.Draw()


latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.15,0.96,'CMS #bf{#it{'+latextitle+'}}')
latex1.DrawLatex(0.8,0.96,'#bf{'+printlumi+"fb^{-1} (13TeV)}")

pad1.SetLogy()

can.cd()

ratio2 = ROOT.TH1F('ratio_d','ratio pred/data',bins,0,bins)
#ratio2.Sumw2()
ratio2 = truth_H.Clone()
ratio2.Divide(QCD_H)
ratio2.SetLineColor(ROOT.kBlack)
ratio2.SetMarkerStyle(8)
ratio2.SetMarkerSize(0)
ratio2.SetLineWidth(0)
ratio2.SetLineColor(ROOT.kWhite)
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
#ratio2.GetXaxis().SetLabelSize(0.11)
ratio2.GetXaxis().SetLabelSize(0.09)
ratio2.GetXaxis().SetNdivisions(508)
ratio2.GetYaxis().SetTitle('MC/pred.')
ratio2.GetYaxis().SetTitleSize(0.13)
ratio2.GetYaxis().SetLabelSize(0.13)
ratio2.GetYaxis().SetTitleOffset(0.4)
ratio2.GetYaxis().SetNdivisions(304)
ratio2.SetMinimum(0.)
ratio2.SetMaximum(3.2)
ratio2.Draw('p')

pred_rel_err.Draw('2 same')
ratio_err.Draw("P0 same")


can.cd()


can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016B/QCD/Closure_Spring16_Moriond17_v2.png')
can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016B/QCD/Closure_Spring16_Moriond17_v2.root')
can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016B/QCD/Closure_Spring16_Moriond17_v2.pdf')

