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
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from array import array
from Workspace.HEPHYPythonTools.xsecSMS import *

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


path = "/data/easilar/Spring15/25ns/allSignals_2p25_all_syst_pkl"
res = pickle.load(file(path))

expand_pickle = "/data/easilar/Spring15/25ns/allSignals_2p25_Jetpt_cut_pkl"
expand_dict = pickle.load(file(expand_pickle))

colors = [ROOT.kBlue+2, ROOT.kBlue-4, ROOT.kBlue-7, ROOT.kBlue-9, ROOT.kCyan-9, ROOT.kCyan-6, ROOT.kCyan-2,ROOT.kGreen+3,ROOT.kGreen-2,ROOT.kGreen-6,ROOT.kGreen-7, ROOT.kOrange-4, ROOT.kOrange+1, ROOT.kOrange+8, ROOT.kRed, ROOT.kRed+1]
colors = [ROOT.kBlue-7, ROOT.kCyan-9, ROOT.kCyan-2, ROOT.kGreen-6, ROOT.kOrange+6, ROOT.kRed+1, ROOT.kRed-6, ROOT.kYellow+2, ROOT.kGreen, ROOT.kGreen+3, ROOT.kBlue-2]

colors = range(28,100,2)

isrErrH       = ROOT.TH1F('isrErrH','ISR',bins,0,bins)
Q2ErrH        = ROOT.TH1F('Q2ErrH','Q2',bins,0,bins)
jecErrH       = ROOT.TH1F('jecErrH','jec',bins,0,bins)
bErrH         = ROOT.TH1F('bErrH','b-jet SFs',bins,0,bins)
lightErrH     = ROOT.TH1F('lightErrH','light q. SFs',bins,0,bins)
lepSFErrH     = ROOT.TH1F('lepSFErrH','lepton SFs',bins,0,bins)
triggerH      = ROOT.TH1F('triggerH','trigger',bins,0,bins)
PUH           = ROOT.TH1F('PUH','PU',bins,0,bins)
lumiH         = ROOT.TH1F('lumiH','luminosity',bins,0,bins)
xsecH         = ROOT.TH1F('xsecH','xsec',bins,0,bins)

dummy = ROOT.TH1F('dummy','',bins,0,bins)
dummy.SetLineColor(ROOT.kWhite)
dummy.SetFillColor(ROOT.kWhite)

ratio = ROOT.TH1F('ratio','ratio',bins,0,bins)

hists = [lepSFErrH, lumiH, triggerH, Q2ErrH, PUH, lightErrH, bErrH, isrErrH,jecErrH]
for i_h,h in enumerate(hists):
  h.SetFillColorAlpha(colors[i_h], 0.8)
  #h.SetFillColor(colors[i_h])
  h.SetLineColor(colors[i_h])
  h.SetLineWidth(1)
  

totalH = ROOT.TH1F('totalH','total',bins,0,bins)
totalH.SetLineColor(ROOT.kBlack)
totalH.SetLineWidth(2)
totalH.SetMarkerStyle(21)
totalH.SetMarkerSize(1)
stat_totalYErr = []
totalXErr = []
totalYErr = []
totalX = []
totalY = []
for sig in [allSignals[7]]:
  #for mglu in sig.keys() :
  for mglu in [1500] :
    #for mlsp in sig[mglu].keys() :
    for mlsp in [100] :
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

            isrErr = res[srNJet][stb][htb][mglu][mlsp]['delta_ISR']
            expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['syst_ISR'] = isrErr 
            isrErrH.SetBinContent(i, isrErr) 

            Q2Err = res[srNJet][stb][htb][mglu][mlsp]['delta_Q2']
            Q2ErrH.SetBinContent(i, Q2Err) 
            expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['syst_Q2'] = Q2Err

            jecErr = res[srNJet][stb][htb][mglu][mlsp]['delta_jec']
            jecErrH.SetBinContent(i, jecErr) 
            expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['syst_JEC'] = jecErr

            bErr = res[srNJet][stb][htb][mglu][mlsp]['var_b_MB_SR']
            bErrH.SetBinContent(i, bErr) 
            expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['syst_B'] = bErr

            lightErr = res[srNJet][stb][htb][mglu][mlsp]['var_light_MB_SR']
            lightErrH.SetBinContent(i, lightErr) 
            expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['syst_light'] = lightErr

            ##constant systematics##

            #leptonErr = res[srNJet][stb][htb][mglu][mlsp]['var_lepton_MB_SR']
            leptonErr = 0.05
            lepSFErrH.SetBinContent(i, leptonErr) 
            expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['syst_lepton'] = leptonErr

            triggerErr = 0.01
            triggerH.SetBinContent(i, triggerErr )
            expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['syst_trigger'] = triggerErr

            PUErr      = 0.05
            PUH.SetBinContent(i, PUErr )
            expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['syst_PU'] = PUErr

            lumiErr    = 0.045
            lumiH.SetBinContent(i, lumiErr )
            expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['syst_lumi'] = lumiErr
            
            xsecErr    = (gluino13TeV_NLONLL_Up[mglu]/gluino13TeV_NLONLL[mglu])-1
            #xsecH.SetBinContent(i, xsecErr )
            expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['syst_xsec'] = xsecErr

            totalSyst = isrErr**2 + Q2Err**2 + jecErr**2 +bErr**2 + lightErr**2 + leptonErr**2 + triggerErr**2 + PUErr**2 + lumiErr**2
            totalSyst = sqrt(totalSyst)
            totalH.SetBinContent(i, totalSyst)
            print mglu , mlsp
            print res[srNJet][stb][htb][mglu][mlsp]['err_MB_SR'] , res[srNJet][stb][htb][mglu][mlsp]['yield_MB_SR']
            print expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['stat_err_MB_SR'] , expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['yield_MB_SR']
            #totalH.SetBinError(i,0)
            #if not res[srNJet][stb][htb][mglu][mlsp]['yield_MB_SR']==0 : totalH.SetBinError(i, (res[srNJet][stb][htb][mglu][mlsp]['err_MB_SR']/res[srNJet][stb][htb][mglu][mlsp]['yield_MB_SR']))
            totalErr = totalSyst*expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['yield_MB_SR'] + expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['stat_err_MB_SR']
            ratio.SetBinContent(i,expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['yield_MB_SR'])
            totalYErr.append(totalErr)
            totalXErr.append(0.5)
            totalY.append(expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['yield_MB_SR'])
            totalX.append(i-0.5)

            stat_totalYErr.append(expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]['stat_err_MB_SR'])

            i+=1

      ax =   array('d',totalX)
      ay =   array('d',totalY)
      aexh = array('d',totalXErr)
      aexl = array('d',totalXErr)
      aeyh = array('d',totalYErr)
      aeyl = array('d',totalYErr)

      stat_aeyh = array('d',stat_totalYErr)

      can = ROOT.TCanvas('can','can',700,700)
      pad1=ROOT.TPad("pad1","MyTitle",0.,0.3,1.,1.)
      pad1.SetLeftMargin(0.15)
      pad1.SetBottomMargin(0.02)
      pad1.Draw()
      pad1.cd()
      #can.cd()
      h_Stack = ROOT.THStack('h_Stack','Stack')

      for i_h,h in enumerate(hists):
        #setNiceBinLabel(h, signalRegions)
        h_Stack.Add(h)

      h_Stack.SetMaximum(1.0)
      h_Stack.SetMinimum(0.0)

      leg = ROOT.TLegend(0.7,0.75,0.98,0.95)
      leg.SetFillColor(ROOT.kWhite)
      leg.SetShadowColor(ROOT.kWhite)
      leg.SetBorderSize(1)
      leg.SetTextSize(0.04)
      leg.AddEntry(totalH)
      for i in range(3):
        leg.AddEntry(hists[i], '', 'f')

      leg2 = ROOT.TLegend(0.43,0.75,0.7,0.95)
      leg2.SetFillColor(ROOT.kWhite)
      leg2.SetShadowColor(ROOT.kWhite)
      leg2.SetBorderSize(1)
      leg2.SetTextSize(0.04)
      for i in range(3,6):
        leg2.AddEntry(hists[i], '', 'f')

      leg3 = ROOT.TLegend(0.16,0.75,0.42,0.95)
      leg3.SetFillColor(ROOT.kWhite)
      leg3.SetShadowColor(ROOT.kWhite)
      leg3.SetBorderSize(1)
      leg3.SetTextSize(0.04)
      for i in range(6,len(hists)):
        leg3.AddEntry(hists[i], '', 'f')

      #setNiceBinLabel(totalH, signalRegions)
      totalH.SetLineWidth(2)
      totalH.SetMarkerStyle(34)
      totalH.SetMarkerSize(2)
      #totalH.GetXaxis().SetTitleSize(0.13)
      totalH.GetXaxis().SetLabelSize(0.0)
      #totalH.GetXaxis().SetNdivisions(508) 
      #totalH.GetXAxis().SetLabelOffset(0.05)
      h_Stack.Draw('hist')
      #totalH.Draw('hist same')
      totalH.Draw('p same')

      #h_Stack.GetXaxis().SetLabelSize(0.)
      #h_Stack.GetXaxis().SetLabelOffset(10)
      h_Stack.GetYaxis().SetTitle('Relative Uncertainty')
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

      h_Stack.GetXaxis().SetLabelSize(0.0)
      h_Stack.GetXaxis().SetTitleSize(0.13)
      h_Stack.GetXaxis().SetNdivisions(508)
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
      ratio.GetYaxis().SetTitle('Events')
      ratio.GetYaxis().SetTitleSize(0.13)
      ratio.GetYaxis().SetLabelSize(0.13)
      ratio.GetYaxis().SetTitleOffset(0.4)
      ratio.GetYaxis().SetNdivisions(508)
      ratio.SetMinimum(0.0)
      ratio.SetMaximum(2.2)
      ratio.Draw('p')
      total_err = ROOT.TGraphAsymmErrors(bins, ax, ay, aexl, aexh, aeyl, aeyh)
      total_err.SetFillColor(ROOT.kBlue)
      total_err.SetFillStyle(3244)
      total_err.Draw('2 same')
      stat_err = ROOT.TGraphAsymmErrors(bins, ax, ay, aexl, aexh, aeyl, stat_aeyh)
      stat_err.Draw('p0 same')
      #ratio.Draw('p0 same')
      can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016/signal_syst_approval/syst_errors_signal_'+str(mglu)+'_'+str(mlsp)+'.png')
      can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016/signal_syst_approval/syst_errors_signal_'+str(mglu)+'_'+str(mlsp)+'.root')
      can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016/signal_syst_approval/syst_errors_signal_'+str(mglu)+'_'+str(mlsp)+'.pdf')

#pickle.dump(expand_dict,file('/data/easilar/Spring15/25ns/allSignals_2p25_allSyst_approval_pkl','w'))
