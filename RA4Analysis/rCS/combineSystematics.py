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
from array import array

from math import isnan

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

pickleDir =  '/data/dspitzbart/Results2016/Prediction_Spring16_templates_SR2016_postApp_v2_lep_data_12p9/'

saveDir = pickleDir
#saveDir = '/data/dspitzbart/Results2016/Prediction_SFtemplates_fullSR_lep_data_2p25/'
path_syst1 = '/data/easilar/Results2016/ICHEP/SYS/V1/'
wxsec   = pickle.load(file(path_syst1+'Unc_on_WJets__syst_SRAll_pkl'))
ttvxsec = pickle.load(file(path_syst1+'Unc_on_TTV__syst_SRAll_pkl'))
ttxsec  = pickle.load(file('/data/dspitzbart/Results2016/systematics2016/ttxsec_dummy_pkl'))
wpol    = pickle.load(file('/data/dspitzbart/Results2016/systematics2016/Wpol_pkl'))
b_err   = pickle.load(file('/data/dspitzbart/Results2016/systematics2016/btagErr_approval_pkl'))
l_err   = pickle.load(file('/data/dspitzbart/Results2016/systematics2016/mistagErr_approval_pkl'))
qcd_err = pickle.load(file('/data/dspitzbart/Results2016/systematics2016/qcdErr_pkl'))
#rcs     = pickle.load(file(pickleDir+'singleLeptonic_Spring15__estimationResults_pkl_kappa_corrected'))
rcs     = pickle.load(file(pickleDir+'singleLeptonic_Spring16__estimationResults_pkl_kappa_corrected'))
if validation:
  dilep   = pickle.load(file('/data/dspitzbart/Results2016/dilep_val_pkl'))
else:
  #dilep   = pickle.load(file(path_syst1+'unc_on_diLep_with_SRAll_V4_pkl'))
  dilep   = pickle.load(file('/data/dspitzbart/Results2016/systematics2016/dilep_envelope_approval_pkl'))


validation = False

#topPt_Err = pickle.load(file("/data/easilar/Spring15/25ns/extended_with_truth_counts_topPt_pkl"))
#topPt_Err = pickle.load(file("/data/dspitzbart/Results2016/topErr_pkl_update"))
topPt_Err = pickle.load(file(path_syst1+"unc_on_topPt_SRAll_pkl"))
pu_Unc    = pickle.load(file(path_syst1+"unc_on_PU_SRAll_pkl"))
lep_Eff   = pickle.load(file("/data/dspitzbart/Results2016/systematics2016/lepEff_dummy_pkl"))
jec       = pickle.load(file(path_syst1+'/unc_on_JEC_SRAll_v1_pkl'))
#jec       = pickle.load(file('/data/dspitzbart/Results2016/systematics2016/JEC_dummy_pkl'))

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
kappaH    = ROOT.TH1F('kappaH', 'global kappa', bins, 0, bins)

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

kappa_global_list = []
rcsW_list = []
rcstt_list = []
rcsW_diff_list = []
rcsTot_list = []

fmt = '{0:15}{1:>8}{2:>8}'
#fmt2 = '{0:10}{1:>20}'

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
        if isnan(bErr): bErr = 0.03
        mistag_SF = l_err['tot_pred'][srNJet][stb][htb]
        b_c_SF    = b_err['tot_pred'][srNJet][stb][htb]
      bErrH.SetBinContent(i, bErr)
      
      ##tt
      #if validation:
      #  bErr_tt = 0.03
      #else:
      #  bErr_tt = sqrt(b_err['TT_kappa'][srNJet][stb][htb]**2 + l_err['TT_kappa'][srNJet][stb][htb]**2) # sum of squares of b/c and mistag
      #
      ##W
      #if validation:
      #  bErr_W = 0.12
      #else:
      #  bErr_W = sqrt(b_err['W_kappa'][srNJet][stb][htb]**2 + l_err['W_kappa'][srNJet][stb][htb]**2) # sum of squares of b/c and mistag
      
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
      TTVXErrH.SetBinContent(i, TTVXErr)
      XsecErr = sqrt(wXErr**2 + ttXErr**2 + TTVXErr**2)
      XsecErrWTT = sqrt(wXErr**2 + ttXErr**2)
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
        puErr = abs(pu_Unc[srNJet][stb][htb]['delta']) 
      puErrH.SetBinContent(i, puErr)
      
      #top pt
      if validation:
        topErr = 0.08
      else:
        topErr = abs(topPt_Err[srNJet][stb][htb]['delta'])  
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
        wPErr = sqrt(wpol[srNJet][stb][htb]['W']**2 + wpol[srNJet][stb][htb]['TT']**2)
        #wPErr = sqrt(((abs(wpol[srNJet][stb][htb]['uWPolMinus10'])+abs(wpol[srNJet][stb][htb]['uWPolPlus10']))/2)**2 + ((abs(wpol[srNJet][stb][htb]['uTTPolMinus5'])+abs(wpol[srNJet][stb][htb]['uTTPolPlus5']))/2)**2) # w pol for w and ttbar
      wPErrH.SetBinContent(i, wPErr)
      
      #JEC
      if validation:
        jecErr = 0.09
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
      if validation:
        dilepErr = 0.075
        if srNJet == (5,5): dilepErr = 0.075
        if srNJet == (6,7): dilepErr = 0.15
        if srNJet == (8,-1): dilepErr = 0.30
      else:
        dilepErr = dilep[srNJet][stb][htb]
      dilepErrH.SetBinContent(i, dilepErr)
      
      # uncertainties on MC rest
      trigger_err = 0.01
      lumi_err = 0.045
      rest_xsec = 0.55
      
      # Rcs uncertainties, also considers the composition of W and ttbar and therefore is sensitive to using MC or data
      if rcs[srNJet][stb][htb]['tot_pred']>0: rcsErr = sqrt(rcs[srNJet][stb][htb]['W_pred_errs']['syst']**2+rcs[srNJet][stb][htb]['TT_rCS_fits_MC']['syst']**2)/rcs[srNJet][stb][htb]['tot_pred']
      else: rcsErr = 0.5
      if rcs[srNJet][stb][htb]['TT_pred']>0: rcsErr_tt = rcs[srNJet][stb][htb]['TT_rCS_fits_MC']['syst']/rcs[srNJet][stb][htb]['TT_pred']
      else: rcsErr_tt = 0
      rcsErr_W  = rcs[srNJet][stb][htb]['W_pred_errs']['const_vs_slope']/rcs[srNJet][stb][htb]['W_pred']
      W_muToLep = rcs[srNJet][stb][htb]['W_pred_errs']['ratio_mu_elemu']/rcs[srNJet][stb][htb]['W_pred']
      
      rcsErrH.SetBinContent(i,rcsErr)
      #print rcsErr
      
      kappa_b_Err   = rcs[srNJet][stb][htb]['TT_rCS_fits_MC']['k_0b/1b_btag_err']/rcs[srNJet][stb][htb]['TT_rCS_fits_MC']['k_0b/1b_btag']
      kappa_TT_Err  = rcs[srNJet][stb][htb]['TT_kappa_err']/rcs[srNJet][stb][htb]['TT_kappa']
      kappa_W_Err   = rcs[srNJet][stb][htb]['W_kappa_err']/rcs[srNJet][stb][htb]['W_kappa']
      
      #calculate Kappa systematic uncertainties on global
      TT_kappa_global = kappa_TT_Err*rcs[srNJet][stb][htb]['TT_pred']
      W_kappa_global  = kappa_W_Err*rcs[srNJet][stb][htb]['W_pred']
      kappa_global    = (W_kappa_global + TT_kappa_global)/rcs[srNJet][stb][htb]['tot_pred']
      kappaH.SetBinContent(i, kappa_global)
      
      # get the yields
      W_pred      = rcs[srNJet][stb][htb]['W_pred_final']
      TT_pred     = rcs[srNJet][stb][htb]['TT_pred_final']
      rest_truth  = rcs[srNJet][stb][htb]['Rest_truth']
      total_pred  = rcs[srNJet][stb][htb]['tot_pred_final']
      
      # calculate sum squared of systematics (including kappas from MC stats) on total, W and ttbar predictions
      
      # calculate the correlated error
      totalU  =  (bErr*total_pred)**2 + (wPErr*total_pred)**2 + (dilepErr*total_pred)**2
      totalU +=  (qcdErr*total_pred)**2 + (topErr*total_pred)**2 + (puErr*total_pred)**2 + (lepSFErr*total_pred)**2
      totalU +=  (jecErr*total_pred)**2 + (wXErr*total_pred)**2 + (ttXErr*total_pred)**2
      totalU +=  (rcsErr_W*W_pred)**2  + (W_muToLep*W_pred)**2 + (kappa_W_Err*W_pred)**2
      totalU +=  (kappa_TT_Err*TT_pred)**2 + (kappa_b_Err*TT_pred)**2 + (rcsErr_tt*TT_pred)**2
      totalU +=  (rest_xsec*rest_truth)**2 + (lumi_err*rest_truth)**2 + (trigger_err*rest_truth)**2
      tot_syst_err_Abs = sqrt(totalU) # total abs systematics
      tot_syst_err_Rel = tot_syst_err_Abs/total_pred
      tot_stat_err_Abs = sqrt(rcs[srNJet][stb][htb]['W_pred_final_err']**2 + rcs[srNJet][stb][htb]['TT_pred_final_err']**2 + rcs[srNJet][stb][htb]['Rest_truth_err']**2)
      print 'Stat tt', rcs[srNJet][stb][htb]['TT_pred_final_err']
      print 'Stat W', rcs[srNJet][stb][htb]['W_pred_final_err']
      print 'Stat rest', rcs[srNJet][stb][htb]['Rest_truth_err']
      tot_stat_err_Rel = tot_stat_err_Abs/total_pred
      totalU +=  rcs[srNJet][stb][htb]['W_pred_final_err']**2 + rcs[srNJet][stb][htb]['TT_pred_final_err']**2 + rcs[srNJet][stb][htb]['Rest_truth_err']**2
      totalU = sqrt(totalU)
      if total_pred<0:
        totalU_rel = 1.
        total_pred = 0.
      else:
        totalU_rel = totalU/total_pred
      
      totalSyst = sqrt(bErr**2 + wXErr**2 + ttXErr**2 + wPErr**2 + dilepErr**2 + qcdErr**2 + topErr**2 + puErr**2 + lepSFErr**2 + jecErr**2 + rcsErr**2                    + kappa_global**2)
      ttSyst    = sqrt(bErr**2 + wXErr**2 + ttXErr**2 + wPErr**2 + dilepErr**2 + qcdErr**2 + topErr**2 + puErr**2 + lepSFErr**2 + jecErr**2 + rcsErr_tt**2                 + kappa_TT_Err**2 + kappa_b_Err**2)
      WSyst     = sqrt(bErr**2 + wXErr**2 + ttXErr**2 + wPErr**2 + dilepErr**2 + qcdErr**2 + topErr**2 + puErr**2 + lepSFErr**2 + jecErr**2 + rcsErr_W**2  + W_muToLep**2  + kappa_W_Err**2)

      errorsForTotal = [bErr, wXErr, ttXErr, wPErr, dilepErr, qcdErr, topErr, puErr, lepSFErr, jecErr, rcsErr]
      totalSyst_noKappa = 0
      for err in errorsForTotal: totalSyst_noKappa += err**2
      totalSyst_noKappa = sqrt(totalSyst_noKappa)
      errorsForTotalRounded = [ round(elem, 2) for elem in errorsForTotal ]
      print errorsForTotalRounded
      #totalSyst_noKappa = sqrt(bErr**2 + wXErr**2 + ttXErr**2 + wPErr**2 + dilepErr**2 + qcdErr**2 + topErr**2 + puErr**2 + lepSFErr**2 + jecErr**2 + rcsErr**2) #for visualization purposes only
       
      restSyst = sqrt(bErr**2 + wXErr**2 + ttXErr**2 + wPErr**2 + dilepErr**2 + qcdErr**2 + topErr**2 + puErr**2 + lepSFErr**2 + jecErr**2 + rest_xsec**2 + lumi_err**2 + trigger_err**2)
      #restSyst = 0.5
      
      totalH.SetBinContent(i, totalSyst_noKappa)
      
      systematics = {'btagSF':bErr, 'b_c_SF':b_c_SF, 'mistag_SF':mistag_SF, 'Wxsec':wXErr, 'TTxsec':ttXErr, 'Wpol':wPErr, 'TTVxsec':TTVXErr, 'xsec':XsecErr, 'TTxsec_kappa':ttXErr_k, 'Wxsec_kappa':wXErr_k}
      systematics.update({'rcs':rcsErr, 'QCD':qcdErr, 'total':totalSyst, 'rcs_tt':rcsErr_tt, 'rcs_W':rcsErr_W, 'total_tt':ttSyst, 'total_W':WSyst, 'total_Rest':restSyst, 'ratio_mu_elemu':W_muToLep})
      systematics.update({'topPt':topErr, 'dilep':dilepErr, 'pileup':puErr, 'lepSF':lepSFErr, 'kappa_b':kappa_b_Err, 'kappa_TT':kappa_TT_Err, 'kappa_W':kappa_W_Err, 'JEC':jecErr})
      systematics.update({'kappa_global':kappa_global})
      
      kappa_global_list.append(kappa_global)
      rcsW_list.append(rcsErr_W)
      rcstt_list.append(rcsErr_tt)
      rcsW_diff_list.append(W_muToLep)
      rcsTot_list.append(rcsErr)


      # apply systemtatics on Rcs - not used anymore
      TT_kappa_err_syst  = rcs[srNJet][stb][htb]['TT_kappa']*ttSyst
      W_kappa_err_syst   = rcs[srNJet][stb][htb]['W_kappa']*WSyst
      TT_kappa_err_total = sqrt(rcs[srNJet][stb][htb]['TT_kappa_err']**2 + (rcs[srNJet][stb][htb]['TT_kappa']*ttSyst)**2)
      W_kappa_err_total  = sqrt(rcs[srNJet][stb][htb]['W_kappa_err']**2 + (rcs[srNJet][stb][htb]['W_kappa']*WSyst)**2)
      rcs[srNJet][stb][htb]['TT_kappa_err_syst']  = TT_kappa_err_syst
      rcs[srNJet][stb][htb]['W_kappa_err_syst']   = W_kappa_err_syst
      rcs[srNJet][stb][htb]['TT_kappa_err_total'] = TT_kappa_err_total
      rcs[srNJet][stb][htb]['W_kappa_err_total']  = W_kappa_err_total
      
      #calculate final errors (yields got already corrected in makeCorrections.py)
  
      # get absolute values from relative systematic uncertainties on the different components
      tt_syst_err_Abs = getPropagatedError([rcs[srNJet][stb][htb]['TT_pred_final'], 1],  [0, ttSyst], 1, 0, returnCalcResult=True)
      W_syst_err_Abs = getPropagatedError([rcs[srNJet][stb][htb]['W_pred_final'], 1],    [0, WSyst], 1, 0, returnCalcResult=True)
      rest_syst_err_Abs = getPropagatedError([rcs[srNJet][stb][htb]['Rest_truth'], 1],   [0, restSyst], 1, 0, returnCalcResult=True)
      
      # Combine the stat unc from prediction with systematics
      TT_tot_err_Abs    = getPropagatedError([rcs[srNJet][stb][htb]['TT_pred_final'], 1], [rcs[srNJet][stb][htb]['TT_pred_final_err'],  ttSyst], 1, 0, returnCalcResult=True)
      W_tot_err_Abs     = getPropagatedError([rcs[srNJet][stb][htb]['W_pred_final'],  1], [rcs[srNJet][stb][htb]['W_pred_final_err'],   WSyst], 1, 0, returnCalcResult=True)
      Rest_tot_err_Abs  = getPropagatedError([rcs[srNJet][stb][htb]['Rest_truth'],    1], [rcs[srNJet][stb][htb]['Rest_truth_err'],     restSyst], 1, 0, returnCalcResult=True)

      # Get the total uncertainty on the prediction
      tot_err_Abs = sqrt(TT_tot_err_Abs[1]**2+W_tot_err_Abs[1]**2+Rest_tot_err_Abs[1]**2)
      
      tot_stat_err_Abs = rcs[srNJet][stb][htb]['tot_pred_final_err']
      rcs[srNJet][stb][htb]['tot_pred_final_tot_err'] = totalU
      rcs[srNJet][stb][htb]['tot_pred_final_syst_err'] = tot_syst_err_Abs
      
      rcs[srNJet][stb][htb]['TT_pred_final_tot_err']    = TT_tot_err_Abs[1]
      rcs[srNJet][stb][htb]['W_pred_final_tot_err']     = W_tot_err_Abs[1]
      rcs[srNJet][stb][htb]['Rest_truth_final_tot_err'] = Rest_tot_err_Abs[1]
      
      print '** Absolute values of uncertainties **'
      print 'Stat. unc.:',round(tot_stat_err_Abs,3)
      print 'Syst. W unc.:',round(W_syst_err_Abs[1],3)
      print 'Syst. tt unc.:',round(tt_syst_err_Abs[1],3)
      print 'Syst. unc.:',round(tot_syst_err_Abs,3)
      print 'Rel. syst. unc.:',round(tot_syst_err_Rel,3)
      print 'Rel. stat. unc.:',round(tot_stat_err_Rel,3)
      print 'Rel. tot. unc.:',round(totalU_rel,3)
      print 'Total unc.:',round(tot_err_Abs,3)
      print 'Total yield:',round(total_pred,2)
      print round(totalU,3)
      print totalU/tot_err_Abs
      
      rcs[srNJet][stb][htb]['systematics'] = systematics
      
      ratio.SetBinContent(i,1)
      #totalYErr.append(tot_err_Abs/total)
      totalYErr.append(totalU_rel)
      totalXErr.append(0.5)
      totalY.append(1)
      totalX.append(i-0.5)
      i+=1

print
print 'Rcs W systematic range', round(min(rcsW_list),3), round(max(rcsW_list),3)
print 'Rcs tt systematic range', round(min(rcstt_list),3), round(max(rcstt_list),3)
print 'Rcs mu/lep systematic range', round(min(rcsW_diff_list),3), round(max(rcsW_diff_list),3)
print 'Rcs total systematic range', round(min(rcsTot_list),3), round(max(rcsTot_list),3)



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

print
print 'min and max of the different sources'
print
print fmt.format('source','min','max')
line = ''
for x in range(31): line+='-'
print line
for h in hists+[wXErrH, TTVXErrH,totalH,kappaH]:
  print fmt.format(h.GetName(), round(h.GetMinimum(),3), round(h.GetMaximum(),3))
print

#print totalH.GetName(), round(totalH.GetMinimum(),2), round(totalH.GetMaximum(),2)

for i_h,h in enumerate(hists):
  h_Stack.Add(h)

h_Stack.SetMaximum(1.5)
h_Stack.SetMinimum(0.0)

leg = ROOT.TLegend(0.7,0.75,0.98,0.95)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.04)
leg.AddEntry(totalH, 'Total', 'p')
for i in range(3):
  leg.AddEntry(hists[i], '', 'f')

leg2 = ROOT.TLegend(0.43,0.75,0.7,0.95)
leg2.SetFillColor(ROOT.kWhite)
leg2.SetShadowColor(ROOT.kWhite)
leg2.SetBorderSize(1)
leg2.SetTextSize(0.04)
for i in range(3,7):
  leg2.AddEntry(hists[i], '', 'f')

leg3 = ROOT.TLegend(0.15,0.75,0.43,0.95)
leg3.SetFillColor(ROOT.kWhite)
leg3.SetShadowColor(ROOT.kWhite)
leg3.SetBorderSize(1)
leg3.SetTextSize(0.04)
for i in range(7,len(hists)):
  leg3.AddEntry(hists[i],'','f')
for i in range(len(hists),11):
  leg3.AddEntry(dummy,'','f')


h_Stack.Draw('hist')
totalH.Draw('p same')

h_Stack.GetXaxis().SetLabelSize(0.)
h_Stack.GetXaxis().SetLabelOffset(10)
h_Stack.GetYaxis().SetTitle('Relative uncertainty')
h_Stack.GetYaxis().SetTitleOffset(0.8)
h_Stack.GetYaxis().SetNdivisions(508)

leg.Draw()
leg2.Draw()
leg3.Draw()

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.15,0.96,'CMS #bf{#it{Preliminary}}')
latex1.DrawLatex(0.80,0.96,"#bf{"+printlumi+"fb^{-1} (13TeV)}")

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
ratio.GetXaxis().SetLabelSize(0.09)
ratio.GetXaxis().SetNdivisions(508)
ratio.GetYaxis().SetTitle('Total unc.')
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

can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016B/syst_uncertainties/sys_'+predictionName+'_postApproval_v2.png')
can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016B/syst_uncertainties/sys_'+predictionName+'_postApproval_v2.root')
can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016B/syst_uncertainties/sys_'+predictionName+'_postApproval_v2.pdf')


savePickle = True
if savePickle:
  pickle.dump(rcs, file(saveDir+'resultsFinal_withSystematics_pkl','w'))
  print "pickle Written :" , saveDir+'resultsFinal_withSystematics_pkl'
else:
  print "Pickle not saved!"
