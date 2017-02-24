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

from predictionConfig import *

ROOT.gStyle.SetOptTitle(0);
ROOT.gStyle.SetOptStat('')


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
    rowsSt[srNJet][stb] = {'njet':len(signalRegions[srNJet][stb])}
  rowsNJet[srNJet] = {'LT':len(signalRegions[srNJet]), 'n':rows}
  bins += rows

#print signalRegions

saveDir =  '/data/easilar/Results2016/ICHEP/Prediction_Spring16_templates_lep_data_4fb/'
path_noDL = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_SR_Moriond2017_Summer16_lep_MC_SF_36p5/'
#path_CentralDL = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_SR_Moriond2017_Summer16_DLcorrected_lep_MC_SF_36p5/' 
path_ConstantUp = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_SR_Moriond2017_Summer16_DLconstantUp_lep_MC_SF_36p5/'
path_SlopeUp = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_SR_Moriond2017_Summer16_DLslopeUp_lep_MC_SF_36p5/'
pickleFile = 'singleLeptonic_Spring16_iso_Veto_ISRforttJets_NEWttJetsSB_addDiBoson_withSystematics_pkl'
pickleDl = path_noDL+pickleFile
#pickleDl_CentralDL = path_CentralDL+pickleFile
pickleDl_ConstantUp = path_ConstantUp+pickleFile
pickleDl_SlopeUp = path_SlopeUp+pickleFile
dl = pickle.load(file(pickleDl))
#dl_DL = pickle.load(file(pickleDir_CentralDL))
dl_cUp = pickle.load(file(pickleDl_ConstantUp))
dl_sUp = pickle.load(file(pickleDl_SlopeUp))
bkg_pickle_dir = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_SR_Moriond2017_Summer16_lep_data_36p5//resultsFinal_withSystematics_Filesremoved_pkl'
linJet = pickle.load(file(bkg_pickle_dir)) 

validation = False
#dilep   = pickle.load(file('/data/easilar/Results2016/ICHEP/DiLep_SYS/V1/unc_with_SRAll_pkl'))
#dilep   = pickle.load(file('/data/easilar/Results2016/ICHEP/DiLep_SYS/V1/unc_with_SRAll_V4_pkl'))
#dilep   = pickle.load(file('/data/easilar/Results2016/ICHEP/SYS/V1//unc_on_JEC_SRAll_v1_pkl'))

colors = [ROOT.kBlue-7, ROOT.kCyan-9, ROOT.kCyan-2, ROOT.kGreen-6, ROOT.kOrange+6, ROOT.kRed+1, ROOT.kRed-6, ROOT.kYellow+2, ROOT.kGreen, ROOT.kGreen+3, ROOT.kBlue-2]

colors = range(28,100,2)

dilepErrH = ROOT.TH1F('dilepErrH','dilep. events',bins,0,bins)


dilepC   = ROOT.TH1F('dilepC','2l constant',bins,0,bins)
#dilepC   = ROOT.TH1F('dilepC','JEC',bins,0,bins)
dilepS   = ROOT.TH1F('dilepS','2l slope',bins,0,bins)

hlinJet   = ROOT.TH1F('hlinJet','tt linear Fit',bins,0,bins)
h_xsec_W_on_W     = ROOT.TH1F('h_xsec_W_on_W'    ,'xsec_W_on_W'   ,bins,0,bins)
h_xsec_TTV_on_W   = ROOT.TH1F('h_xsec_TTV_on_W'  ,'xsec_TTV_on_W' ,bins,0,bins)
h_xsec_W_on_TT    = ROOT.TH1F('h_xsec_W_on_TT'   ,'xsec_W_on_TT'  ,bins,0,bins)
h_xsec_TTV_on_TT  = ROOT.TH1F('h_xsec_TTV_on_TT' ,'xsec_TTV_on_TT',bins,0,bins)
h_xsec_TT_on_TT   = ROOT.TH1F('h_xsec_TT_on_TT'  ,'xsec_TT_on_TT' ,bins,0,bins)

h_pu_on_W = ROOT.TH1F('h_pu_on_W', 'pu on W' ,bins,0,bins)
h_pu_on_tt = ROOT.TH1F('h_pu_on_tt', 'pu on TT' ,bins,0,bins)

dummy = ROOT.TH1F('dummy','',bins,0,bins)
dummy.SetLineColor(ROOT.kWhite)
dummy.SetFillColor(ROOT.kWhite)

ratio = ROOT.TH1F('ratio','ratio',bins,0,bins)

#hists = [dilepC,dilepS]
#hists = [h_xsec_W_on_W, h_xsec_TTV_on_W,h_xsec_W_on_TT,h_xsec_TTV_on_TT,h_xsec_TT_on_TT]
hists = [h_pu_on_W,h_pu_on_tt]
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

plot_DL = False
plot_xsec = False
plot_PU = True
jec   = pickle.load(file('/afs/hephy.at/user/e/easilar/www/Moriond2017/sys/JEC/unc_on_JEC_SRAll_pkl'))

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
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      if plot_DL:
        kappa_dl = dl[srNJet][stb][htb]['TT_kappa']
        kappa_cUpdl = dl_cUp[srNJet][stb][htb]['TT_kappa']
        kappa_sUpdl = dl_sUp[srNJet][stb][htb]['TT_kappa']
        delta_constant_Up = abs((kappa_cUpdl-kappa_dl)/kappa_dl)
        delta_slope_Up = abs((kappa_sUpdl-kappa_dl)/kappa_dl)
        constant_err = delta_constant_Up
        slope_err = delta_slope_Up
        dilepC.SetBinContent(i, constant_err)
        dilepS.SetBinContent(i, slope_err)
        hlinJet.SetBinContent(i, linJet[srNJet][stb][htb]['TT_rCS_fits_MC']['syst']/linJet[srNJet][stb][htb]['TT_pred'])
        print constant_err , slope_err
        errorsForTotal = [constant_err , slope_err]
      if plot_xsec:
        p_xsectt   = pickle.load(file('/afs/hephy.at/user/e/easilar/www/Moriond2017/sys/XSEC/BKG_kappaTT_SR'+str(i-1)+'_xsecs_pkl')) 
        p_xsecW   = pickle.load(file('/afs/hephy.at/user/e/easilar/www/Moriond2017/sys/XSEC/BKG_kappaW_SR'+str(i-1)+'_xsecs_pkl')) 
        xsec_W_on_W    = p_xsecW[srNJet][stb][htb]["xsecW_delta_Up"] 
        xsec_TTV_on_W  = p_xsecW[srNJet][stb][htb]["xsecTTV_delta_Up"] 
        xsec_W_on_TT   = p_xsectt[srNJet][stb][htb]["xsecwJetsweight_delta_Up"]
        xsec_TTV_on_TT = p_xsectt[srNJet][stb][htb]["xsecttVweight_delta_Up"]
        xsec_TT_on_TT  = p_xsectt[srNJet][stb][htb]["xsecttJetsw_delta_Up"]
        h_xsec_W_on_W.SetBinContent(i, xsec_W_on_W)          
        h_xsec_TTV_on_W.SetBinContent(i, xsec_TTV_on_W)  
        h_xsec_W_on_TT.SetBinContent(i, xsec_W_on_TT) 
        h_xsec_TTV_on_TT.SetBinContent(i, xsec_TTV_on_TT) 
        h_xsec_TT_on_TT.SetBinContent(i, xsec_TT_on_TT) 
        errorsForTotal = [xsec_W_on_W, xsec_TTV_on_W, xsec_W_on_TT,xsec_TTV_on_TT, xsec_TT_on_TT]
      if plot_PU:
        p_putt   = pickle.load(file('/afs/hephy.at/user/e/easilar/www/Moriond2017/sys/PU/BKG_kappaTT_SR'+str(i-1)+'_PU_pkl')) 
        p_puW   = pickle.load(file('/afs/hephy.at/user/e/easilar/www/Moriond2017/sys/PU/BKG_kappaW_SR'+str(i-1)+'_pu_pkl')) 
        pu_on_W    = (p_puW[srNJet][stb][htb]["puReweight_true_Up_delta"] + p_puW[srNJet][stb][htb]["puReweight_true_Down_delta"])/2
        pu_on_tt  = (p_putt[srNJet][stb][htb]["PUpuReweight_true_Up_delta_Up"] + p_putt[srNJet][stb][htb]["PUpuReweight_true_Down_delta_Up"])/2 
        h_pu_on_W.SetBinContent(i, pu_on_W)
        h_pu_on_tt.SetBinContent(i, pu_on_tt)
        errorsForTotal = [pu_on_W,pu_on_tt]

      totalSyst_noKappa = 0
      for err in errorsForTotal: totalSyst_noKappa += err**2
      totalH.SetBinContent(i, sqrt(totalSyst_noKappa))
      
      i+=1


can = ROOT.TCanvas('can','can',1000,500)


h_Stack = ROOT.THStack('h_Stack','Stack')

print 'min and max of the different sources'
for h in hists:
  print h.GetName(), round(h.GetMinimum(),2), round(h.GetMaximum(),2)

for i_h,h in enumerate(hists):
  h_Stack.Add(h)

h_Stack.SetMaximum(0.5)
h_Stack.SetMinimum(0.0)

leg = ROOT.TLegend(0.7,0.75,0.98,0.95)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.04)
leg.AddEntry(totalH, 'Total', 'p')
#leg.AddEntry(dilepC, 'JEC', 'f')
for i in range(2):
  leg.AddEntry(hists[i], '', 'f')


h_Stack.Draw('hist')
totalH.Draw('p same')
hlinJet.Draw("same")
setNiceBinLabel(h_Stack, signalRegions )

h_Stack.GetYaxis().SetTitle('Relative uncertainty')
h_Stack.GetYaxis().SetTitleOffset(0.8)
h_Stack.GetYaxis().SetNdivisions(508)
h_Stack.GetXaxis().SetLabelSize(0.04)
h_Stack.GetXaxis().SetTitleSize(0.06)
h_Stack.GetXaxis().SetTitleOffset(2)
h_Stack.GetXaxis().SetLabelSize(0.02)
h_Stack.GetXaxis().SetNdivisions(508)
leg.Draw()

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.15,0.96,'CMS #bf{#it{Preliminary}}')
latex1.DrawLatex(0.85,0.96,"#bf{(13TeV)}")

can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Moriond2017/plots/syst_uncertainties/PU.png')
can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Moriond2017/plots/syst_uncertainties/PU.root')
can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Moriond2017/plots/syst_uncertainties/PU.pdf')
