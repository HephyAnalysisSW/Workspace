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
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from array import array

from predictionConfig import *

ROOT.gStyle.SetOptTitle(0);
ROOT.gStyle.SetOptStat('')


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

wfile = ROOT.TFile('/data/easilar/uncRoot/WJets_xsec_Unc.root')
a = wfile.Get('cb')
w_h1b = a.GetPrimitive('h1b')
w_h2b = a.GetPrimitive('h2b')

ttfile = ROOT.TFile('/data/easilar/uncRoot/ttJets_xsec_Unc.root')
b = ttfile.Get('cb')
tt_h1b = b.GetPrimitive('h1b')
tt_h2b = b.GetPrimitive('h2b')

pufile = ROOT.TFile('/data/easilar/uncRoot/PU_Unc.root')
c = pufile.Get('cb')
pu_h1b = c.GetPrimitive('h1b')
pu_h2b = c.GetPrimitive('h2b')

lepSFfile = ROOT.TFile('/data/easilar/uncRoot/leptonScale_Unc.root')
d = lepSFfile.Get('cb')
lepSF_h1b = d.GetPrimitive('h1b')
lepSF_h2b = d.GetPrimitive('h2b')


#pickleDir = '/data/dspitzbart/Results2016/Prediction_SFtemplates_validation_lep_data_2p25/'
#pickleDir =  '/data/easilar/Results2016/Prediction_SFtemplates_fullSR_lep_data_2p25/'

pickleDir =  '/data/dspitzbart/Results2016/Prediction_SFtemplates_fullSR_lep_data_2p25/'
#pickleDir =  '/data/dspitzbart/Results2016/Prediction_SFtemplates_validation_4j_lep_data_2p25/'
saveDir = pickleDir
#saveDir = '/data/dspitzbart/Results2016/Prediction_SFtemplates_fullSR_lep_data_2p25/'

wxsec   = pickle.load(file('/data/easilar/Spring15/25ns/WJetsxsec_syst_SRAll_pkl'))
ttxsec  = pickle.load(file('/data/easilar/Spring15/25ns/TTJetsxsec_syst_SRAll_pkl'))
ttvxsec = pickle.load(file('/data/easilar/Spring15/25ns/TTVxsec_syst_SRAll_pkl'))
wpol    = pickle.load(file('/data/dhandl/results2015/WPolarizationEstimation/20151218_wjetsPolSys_pkl'))
b_err   = pickle.load(file('/data/dspitzbart/Results2016/btagErr_pkl_update'))
l_err   = pickle.load(file('/data/dspitzbart/Results2016/mistagErr_pkl_update'))
qcd_err = pickle.load(file('/data/dspitzbart/Results2016/qcdErr_pkl_update'))
rcs     = pickle.load(file(pickleDir+'singleLeptonic_Spring15__estimationResults_pkl_kappa_corrected'))
if validation:
  dilep   = pickle.load(file('/data/dspitzbart/Results2016/dilep_val_pkl'))
else:
  dilep   = pickle.load(file('/data/dspitzbart/Results2016/dilep_pkl'))

#topPt_Err = pickle.load(file("/data/easilar/Spring15/25ns/extended_with_truth_counts_topPt_pkl"))
topPt_Err = pickle.load(file("/data/dspitzbart/Results2016/topErr_pkl_update"))
pu_Unc    = pickle.load(file("/data/easilar/Spring15/25ns/extended_with_truth_counts_PU_pkl"))
lep_Eff   = pickle.load(file("/data/easilar/Spring15/25ns/extended_with_truth_counts_LS_pkl"))
jec       = pickle.load(file('/data/easilar/Spring15/25ns/Jec_syst_SRAll_pkl'))

dataResult = rcs

colors = [ROOT.kBlue+2, ROOT.kBlue-4, ROOT.kBlue-7, ROOT.kBlue-9, ROOT.kCyan-9, ROOT.kCyan-6, ROOT.kCyan-2,ROOT.kGreen+3,ROOT.kGreen-2,ROOT.kGreen-6,ROOT.kGreen-7, ROOT.kOrange-4, ROOT.kOrange+1, ROOT.kOrange+8, ROOT.kRed, ROOT.kRed+1]
colors = [ROOT.kBlue-7, ROOT.kCyan-9, ROOT.kCyan-2, ROOT.kGreen-6, ROOT.kOrange+6, ROOT.kRed+1, ROOT.kRed-6, ROOT.kYellow+2, ROOT.kGreen, ROOT.kGreen+3, ROOT.kBlue-2]

colors = range(28,100,2)

rcsErrH   = ROOT.TH1F('rcsErrH','R_{CS} n_{jet} depend.',bins,0,bins)
dilepErrH = ROOT.TH1F('dilepErrH','dilep. events',bins,0,bins)
qcdErrH   = ROOT.TH1F('qcdErrH','QCD fit',bins,0,bins)
bErrH     = ROOT.TH1F('bErrH','b-jet SFs',bins,0,bins)
topErrH   = ROOT.TH1F('topErrH','top p_{T}',bins,0,bins)
jecErrH   = ROOT.TH1F('jecErrH','JEC',bins,0,bins)
wXErrH    = ROOT.TH1F('WXErrH','W+jets x-sec',bins,0,bins)
ttXErrH   = ROOT.TH1F('ttXErrH','t#bar{t}+jets x-sec',bins,0,bins)
TTVXErrH  = ROOT.TH1F('TTVXErrH','TTV x-sec',bins,0,bins)
wPErrH    = ROOT.TH1F('wPErrH','W polarization',bins,0,bins)
puErrH    = ROOT.TH1F('puErrH','pile-up',bins,0,bins)
lepSFErrH = ROOT.TH1F('lepSFErrH','lepton SFs',bins,0,bins)

XsecErrH  = ROOT.TH1F('XsecErrH','x-sections',bins,0,bins)


dilepC   = ROOT.TH1F('dilepC','2l constant',bins,0,bins)
dilepS   = ROOT.TH1F('dilepS','2l slope',bins,0,bins)

dummy = ROOT.TH1F('dummy','',bins,0,bins)
dummy.SetLineColor(ROOT.kWhite)
dummy.SetFillColor(ROOT.kWhite)

ratio = ROOT.TH1F('ratio','ratio',bins,0,bins)

#hists = [dilepC,dilepS,bErrH,wXErrH,ttXErrH,wPErrH,qcdErrH, puErrH, lepSFErrH, topErrH]
hists = [XsecErrH, wPErrH, puErrH, jecErrH, bErrH, topErrH, dilepErrH, rcsErrH, qcdErrH, lepSFErrH]
#hists = [rcsErrH,dilepErrH,bErrH,wXErrH,ttXErrH,wPErrH,qcdErrH, puErrH, lepSFErrH, topErrH, jecErrH]
for i_h,h in enumerate(hists):
  h.SetFillColorAlpha(colors[i_h], 0.8)
  h.SetLineColor(colors[i_h])
  h.SetLineWidth(2)
  

totalH = ROOT.TH1F('totalH','total',bins,0,bins)
totalH.SetLineColor(ROOT.kBlack)
totalH.SetLineWidth(2)
totalH.SetMarkerStyle(34)
totalH.SetMarkerSize(2)

totalXErr = []
totalYErr = []
totalX = []
totalY = []

i=1
for injb,srNJet in enumerate(sorted(signalRegions)):
  for stb in sorted(signalRegions[srNJet]):
    for htb in sorted(signalRegions[srNJet][stb]):
      print
      print '#############################################'
      print '## * njet:',srNJet
      print '## * LT:  ',stb
      print '## * HT:  ',htb
      print '#############################################'
      print

      #b-tag SF
      #total
      if validation:
        bErr=0.05
        mistag_SF = 0.05/sqrt(2)
        b_c_SF = 0.05/sqrt(2)
      else:
        bErr = sqrt(b_err['tot_pred'][srNJet][stb][htb]**2 + l_err['tot_pred'][srNJet][stb][htb]**2) # sum of squares of b/c and mistag
        mistag_SF = l_err['tot_pred'][srNJet][stb][htb]
        b_c_SF    = b_err['tot_pred'][srNJet][stb][htb]
      bErrH.SetBinContent(i, bErr)
      
      #tt
      if validation:
        bErr_tt = 0.03
      else:
        bErr_tt = sqrt(b_err['TT_kappa'][srNJet][stb][htb]**2 + l_err['TT_kappa'][srNJet][stb][htb]**2) # sum of squares of b/c and mistag
      
      #W
      if validation:
        bErr_W = 0.12
      else:
        bErr_W = sqrt(b_err['W_kappa'][srNJet][stb][htb]**2 + l_err['W_kappa'][srNJet][stb][htb]**2) # sum of squares of b/c and mistag
      
      #W x-sec
      if validation:
        wXErr = 0.04
      else:
        wXErr = (abs(w_h1b.GetBinContent(i))+abs(w_h2b.GetBinContent(i)))/2 # w x-sec
      wXErrH.SetBinContent(i, wXErr)

      #ttbar x-sec
      if validation:
        ttXErr = 0.04
      else:
        ttXErr = (abs(tt_h1b.GetBinContent(i))+abs(tt_h2b.GetBinContent(i)))/2 # ttbar x-sec
      ttXErrH.SetBinContent(i, ttXErr)
      
      #x-secs
      if validation:
        TTVXErr = 0.03
      else:
        TTVXErr = ttvxsec[srNJet][stb][htb]['delta_avarage']
      XsecErr = sqrt(wXErr**2 + ttXErr**2 + TTVXErr**2)
      if validation:
        ttXErr_k = 0.05
        wXErr_k = 0.05
      else:
        ttXErr_k = ttxsec[srNJet][stb][htb]['delta_avarage']
        wXErr_k = wxsec[srNJet][stb][htb]['delta_avarage']
      #TTVXErr = ttvxsec[srNJet][stb][htb]['delta_avarage']
      XsecErrH.SetBinContent(i, XsecErr)
      
      #pile-up
      if validation:
        puErr = 0.1
      else:
        puErr = abs(pu_Unc[srNJet][stb][htb]['delta_Up']) 
      puErrH.SetBinContent(i, puErr)
      
      #top pt
      if validation:
        topErr = 0.12
      else:
        topErr = abs(topPt_Err[srNJet][stb][htb])#['delta_Up'])  
      topErrH.SetBinContent(i, topErr)
      
      #lepton SF
      if validation:
        lepSFErr = 0.03
      else:
        lepSFErr = abs(lep_Eff[srNJet][stb][htb]['delta_Up'])
      lepSFErrH.SetBinContent(i, lepSFErr)

      #W polarization
      if validation:
        wPErr = 0.04
      else:
        wPErr = sqrt(((abs(wpol[srNJet][stb][htb]['uWPolMinus10'])+abs(wpol[srNJet][stb][htb]['uWPolPlus10']))/2)**2 + ((abs(wpol[srNJet][stb][htb]['uTTPolMinus5'])+abs(wpol[srNJet][stb][htb]['uTTPolPlus5']))/2)**2) # w pol for w and ttbar
      wPErrH.SetBinContent(i, wPErr)
      
      #JEC
      #print jec[srNJet][stb][htb]['delta_Up_central'], jec[srNJet][stb][htb]['delta_Down_central'], jec[srNJet][stb][htb]['delta_Up_central']/jec[srNJet][stb][htb]['delta_Down_central']
      #jecErr = max(map(abs,[jec[srNJet][stb][htb]['delta_Up_central'], jec[srNJet][stb][htb]['delta_Down_central']]))
      if validation:
        jecErr = 0.06
      else:
        jecErr = (abs(jec[srNJet][stb][htb]['delta_Up_central']) + abs(jec[srNJet][stb][htb]['delta_Down_central']))/2
      jecErrH.SetBinContent(i, jecErr)
      
      #QCD fit
      if validation:
        qcdErr = 0.03
      else:
        qcdErr = qcd_err[srNJet][stb][htb]
      qcdErrH.SetBinContent(i, qcdErr)
      
      #2l
      dilepErr = dilep[srNJet][stb][htb]
      dilepErrH.SetBinContent(i, dilepErr)
      #dilepConstant = max(map(abs,[dilep[srNJet][stb][htb]['delta_constant_Down'], dilep[srNJet][stb][htb]['delta_constant_Up']]))
      #dilepSlope    = max(map(abs,[dilep[srNJet][stb][htb]['delta_slope_Down'], dilep[srNJet][stb][htb]['delta_slope_Up']]))
      #dilepC.SetBinContent(i, dilepConstant)
      #dilepS.SetBinContent(i, dilepSlope)
      
      rcsErr    = sqrt(rcs[srNJet][stb][htb]['W_pred_errs']['syst']**2+rcs[srNJet][stb][htb]['TT_rCS_fits_MC']['syst']**2)/rcs[srNJet][stb][htb]['tot_pred']
      rcsErr_tt = rcs[srNJet][stb][htb]['TT_rCS_fits_MC']['syst']/rcs[srNJet][stb][htb]['TT_pred']
      rcsErr_W  = rcs[srNJet][stb][htb]['W_pred_errs']['const_vs_slope']/rcs[srNJet][stb][htb]['W_pred']
      W_muToLep = rcs[srNJet][stb][htb]['W_pred_errs']['ratio_mu_elemu']/rcs[srNJet][stb][htb]['W_pred']
      
      kappa_b_Err   = rcs[srNJet][stb][htb]['TT_rCS_fits_MC']['k_0b/1b_btag_err']/rcs[srNJet][stb][htb]['TT_rCS_fits_MC']['k_0b/1b_btag']
      kappa_TT_Err  = rcs[srNJet][stb][htb]['TT_kappa_err']/rcs[srNJet][stb][htb]['TT_kappa']
      kappa_W_Err   = rcs[srNJet][stb][htb]['W_kappa_err']/rcs[srNJet][stb][htb]['W_kappa']
      
      print rcs[srNJet][stb][htb]['W_pred'], (rcs[srNJet][stb][htb]['rCS_W_crNJet_0b_corr']*rcs[srNJet][stb][htb]['yW_srNJet_0b_lowDPhi'])
      print rcsErr_W
      print W_muToLep
      print rcsErr_tt
      #print 'Rcs unc tt, W',rcsErr_tt, rcsErr_W
      #print rcs[srNJet][stb][htb]['W_pred_errs']['syst'], rcs[srNJet][stb][htb]['TT_rCS_fits_MC']['syst'], rcs[srNJet][stb][htb]['tot_pred']
      rcsErrH.SetBinContent(i,rcsErr)
      
      #totalSyst = bErr**2 + wXErr**2 + ttXErr**2 + wPErr**2 + qcdErr**2 + dilepSlope**2 + dilepConstant**2 + topErr**2 + puErr**2 + lepSFErr**2
      #totalSyst = bErr**2 + wXErr**2 + ttXErr**2 + wPErr**2 + qcdErr**2 + rcsErr**2 + topErr**2 + puErr**2 + lepSFErr**2 + dilepErr**2 + jecErr**2
      totalSyst = bErr**2 + wPErr**2 + XsecErr**2 + qcdErr**2 + rcsErr**2 + topErr**2 + puErr**2 + lepSFErr**2 + dilepErr**2 + jecErr**2
      totalSyst = sqrt(totalSyst)

      #ttSyst  = sqrt(bErr_tt**2 + wXErr**2 + ttXErr**2 + wPErr**2 + dilepErr**2 + qcdErr**2 + topErr**2 + puErr**2 + lepSFErr**2 + jecErr**2 + rcsErr_tt**2)
      #WSyst   = sqrt(bErr_W**2  + wXErr**2 + ttXErr**2 + wPErr**2 + dilepErr**2 + qcdErr**2 + topErr**2 + puErr**2 + lepSFErr**2 + jecErr**2 + rcsErr_W**2)
      ttSyst  = sqrt(bErr_tt**2 + XsecErr**2 + wPErr**2 + dilepErr**2 + qcdErr**2 + topErr**2 + puErr**2 + lepSFErr**2 + jecErr**2 + rcsErr_tt**2)
      WSyst   = sqrt(bErr_W**2  + XsecErr**2 + wPErr**2 + dilepErr**2 + qcdErr**2 + topErr**2 + puErr**2 + lepSFErr**2 + jecErr**2 + rcsErr_W**2)
      restSyst = 0.5
      
      dataStat = dataResult[srNJet][stb][htb]['tot_pred_err']/dataResult[srNJet][stb][htb]['tot_pred']
      totalErr = sqrt(totalSyst**2+dataStat**2)
      totalH.SetBinContent(i, totalSyst)
      
      systematics = {'btagSF':bErr, 'b_c_SF':b_c_SF, 'mistag_SF':mistag_SF, 'Wxsec':wXErr, 'TTxsec':ttXErr, 'Wpol':wPErr, 'TTVxsec':TTVXErr, 'xsec':XsecErr, 'TTxsec_kappa':ttXErr_k, 'Wxsec_kappa':wXErr_k}
      systematics.update({'rcs':rcsErr, 'QCD':qcdErr, 'total':totalSyst, 'rcs_tt':rcsErr_tt, 'rcs_W':rcsErr_W, 'total_tt':ttSyst, 'total_W':WSyst, 'total_Rest':restSyst, 'ratio_mu_elemu':W_muToLep})
      systematics.update({'topPt':topErr, 'dilep':dilepErr, 'pileup':puErr, 'lepSF':lepSFErr, 'kappa_b':kappa_b_Err, 'kappa_TT':kappa_TT_Err, 'kappa_W':kappa_W_Err, 'JEC':jecErr})

      #apply systemtatics on Rcs
      TT_kappa_err_syst  = rcs[srNJet][stb][htb]['TT_kappa']*ttSyst
      W_kappa_err_syst   = rcs[srNJet][stb][htb]['W_kappa']*WSyst
      TT_kappa_err_total = sqrt(rcs[srNJet][stb][htb]['TT_kappa_err']**2 + (rcs[srNJet][stb][htb]['TT_kappa']*ttSyst)**2)
      W_kappa_err_total  = sqrt(rcs[srNJet][stb][htb]['W_kappa_err']**2 + (rcs[srNJet][stb][htb]['W_kappa']*WSyst)**2)
      rcs[srNJet][stb][htb]['TT_kappa_err_syst']  = TT_kappa_err_syst
      rcs[srNJet][stb][htb]['W_kappa_err_syst']   = W_kappa_err_syst
      rcs[srNJet][stb][htb]['TT_kappa_err_total'] = TT_kappa_err_total
      rcs[srNJet][stb][htb]['W_kappa_err_total']  = W_kappa_err_total
      
      #calculate final errors (yields got already corrected in makeCorrections.py)
      tt, tt_err      = getPropagatedError([rcs[srNJet][stb][htb]['TT_pred'],rcs[srNJet][stb][htb]['TT_kappa']], [rcs[srNJet][stb][htb]['TT_pred_err'], TT_kappa_err_total], 1, 0, returnCalcResult=True)
      w, w_err        = getPropagatedError([rcs[srNJet][stb][htb]['W_pred'],rcs[srNJet][stb][htb]['W_kappa']], [rcs[srNJet][stb][htb]['W_pred_err'], W_kappa_err_total], 1, 0, returnCalcResult=True)
      rest, rest_err  = getPropagatedError([rcs[srNJet][stb][htb]['Rest_truth'],1], [rcs[srNJet][stb][htb]['Rest_truth_err'],restSyst], 1, 0, returnCalcResult=True)
      
      rcs[srNJet][stb][htb]['TT_pred_final_err']  = tt_err
      
      rcs[srNJet][stb][htb]['W_pred_final_err']   = w_err
      
      rcs[srNJet][stb][htb]['Rest_truth_final']     = rest
      rcs[srNJet][stb][htb]['Rest_truth_final_err'] = rest_err
      
      total = tt + w + rest
      total_err = sqrt(tt_err**2 + w_err**2 + rest_err**2)
      rcs[srNJet][stb][htb]['tot_pred_final']     = total
      rcs[srNJet][stb][htb]['tot_pred_final_err'] = total_err
      
      rcs[srNJet][stb][htb]['systematics'] = systematics
            
      print 'Stat. unc.:',round(dataStat,3)
      print 'Syst. W unc.:',round(WSyst,3)
      print 'Syst. tt unc.:',round(ttSyst,3)
      print 'Syst. unc.:',round(totalSyst,3)
      print 'Total unc.:',round(totalErr,3)

      ratio.SetBinContent(i,1)
      #totalYErr.append(totalErr)
      totalYErr.append(total_err/total)
      totalXErr.append(0.5)
      totalY.append(1)
      totalX.append(i-0.5)
      i+=1


ax =   array('d',totalX)
ay =   array('d',totalY)
aexh = array('d',totalXErr)
aexl = array('d',totalXErr)
aeyh = array('d',totalYErr)
aeyl = array('d',totalYErr)

can = ROOT.TCanvas('can','can',700,700)

pad1=ROOT.TPad("pad1","MyTitle",0.,0.3,1.,1.)
pad1.SetLeftMargin(0.15)
pad1.SetBottomMargin(0.02)
pad1.Draw()
pad1.cd()

h_Stack = ROOT.THStack('h_Stack','Stack')

for i_h,h in enumerate(hists):
  h_Stack.Add(h)

#h_Stack.Add(dilepS)
#h_Stack.Add(dilepC)
#h_Stack.Add(bErrH)
#h_Stack.Add(qcdErrH)
#h_Stack.Add(wXErrH)
#h_Stack.Add(ttXErrH)
#h_Stack.Add(wPErrH)
#h_Stack.Add(puErrH)
#h_Stack.Add(lepSFErrH)
#h_Stack.Add(jecErrH)

h_Stack.SetMaximum(1.5)
h_Stack.SetMinimum(0.0)

leg = ROOT.TLegend(0.7,0.75,0.98,0.95)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.04)
leg.AddEntry(totalH, 'sum squared', 'p')
for i in range(3):
  leg.AddEntry(hists[i], '', 'f')
#leg.AddEntry(rcsErrH,'','f')
#leg.AddEntry(bErrH,'','f')
#leg.AddEntry(wXErrH,'','f')

leg2 = ROOT.TLegend(0.43,0.75,0.7,0.95)
leg2.SetFillColor(ROOT.kWhite)
leg2.SetShadowColor(ROOT.kWhite)
leg2.SetBorderSize(1)
leg2.SetTextSize(0.04)
for i in range(3,7):
  leg2.AddEntry(hists[i], '', 'f')
#leg2.AddEntry(qcdErrH,'','f')
#leg2.AddEntry(ttXErrH,'','f')
#leg2.AddEntry(wPErrH,'','f')
#leg2.AddEntry(puErrH,'','f')

leg3 = ROOT.TLegend(0.15,0.75,0.43,0.95)
leg3.SetFillColor(ROOT.kWhite)
leg3.SetShadowColor(ROOT.kWhite)
leg3.SetBorderSize(1)
leg3.SetTextSize(0.04)
for i in range(7,len(hists)):
  leg3.AddEntry(hists[i],'','f')
#leg3.AddEntry(lepSFErrH,'','f')
#leg3.AddEntry(dummy,'','f')
#leg3.AddEntry(dummy,'','f')
#leg3.AddEntry(dummy,'','f')
for i in range(len(hists),11):
  leg3.AddEntry(dummy,'','f')


h_Stack.Draw('hist')
#totalH.Draw('hist same')
totalH.Draw('p same')

h_Stack.GetXaxis().SetLabelSize(0.)
h_Stack.GetXaxis().SetLabelOffset(10)
h_Stack.GetYaxis().SetTitle('Relative systematic uncertainty')
h_Stack.GetYaxis().SetTitleOffset(0.8)
h_Stack.GetYaxis().SetNdivisions(508)

leg.Draw()
leg2.Draw()
leg3.Draw()

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.15,0.96,'CMS #bf{#it{simulation}}')
#latex1.DrawLatex(0.78,0.96,"L=2.1fb^{-1} (13TeV)")

h_Stack.GetXaxis().SetLabelSize(0.04)
h_Stack.GetYaxis().SetLabelSize(0.055)
h_Stack.GetYaxis().SetTitleSize(0.055)
h_Stack.GetYaxis().SetTitleOffset(1.0)

can.cd()

pad2=ROOT.TPad("pad2","datavsMC",0.,0.,1.,.3)
pad2.SetLeftMargin(0.15)
pad2.SetBottomMargin(0.3)
pad2.SetTopMargin(0.02)
pad2.Draw()
pad2.cd()

setNiceBinLabel(ratio, signalRegions)
ratio.GetXaxis().SetTitleSize(0.13)
ratio.GetXaxis().SetLabelSize(0.11)
ratio.GetXaxis().SetNdivisions(508)
ratio.GetYaxis().SetTitle('total unc.')
ratio.GetYaxis().SetTitleSize(0.13)
ratio.GetYaxis().SetLabelSize(0.13)
ratio.GetYaxis().SetTitleOffset(0.4)
ratio.GetYaxis().SetNdivisions(508)
ratio.SetMinimum(0.1)
ratio.SetMaximum(2.2)
ratio.Draw('hist')
total_err = ROOT.TGraphAsymmErrors(bins, ax, ay, aexl, aexh, aeyl, aeyh)
total_err.SetFillColor(ROOT.kBlue)
total_err.SetFillStyle(3244)
total_err.Draw('2 same')

can.cd()

can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016/syst_errors_update_data_ARC5.png')
can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016/syst_errors_update_data_ARC5.root')
can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016/syst_errors_update_data_ARC5.pdf')

pickle.dump(rcs, file(saveDir+'resultsFinal_withSystematics_pkl','w'))
print "pickle Written :" , saveDir+'resultsFinal_withSystematics_pkl'
