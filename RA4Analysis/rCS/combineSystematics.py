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

signalRegions = signalRegion3fb

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

#ttdifile = ROOT.TFile('/data/easilar/uncRoot/ttJets_diLep_Unc.root')
#c = ttdifile.Get('cb')
#ttdi_h1b = a.GetPrimitive('h1b')
#ttdi_h2b = a.GetPrimitive('h2b')

wpol = pickle.load(file('/data/dhandl/results2015/WPolarizationEstimation/20151218_wjetsPolSys_pkl'))
b_err = pickle.load(file('/data/dspitzbart/Results2015/btagErr_pkl'))
l_err = pickle.load(file('/data/dspitzbart/Results2015/mistagErr_pkl'))
qcd_err = pickle.load(file('/data/dspitzbart/Results2015/qcdErr_pkl'))
rcs = pickle.load(file(pickleDir+'singleLeptonic_Spring15__estimationResults_pkl_kappa_corrected'))

#rcs = pickle.load(file('/data/dspitzbart/Results2015/Prediction_SFtemplates_fullSR_lep_MC_SF_2.1/singleLeptonic_Spring15__estimationResults_pkl_kappa_corrected'))
dataResult = rcs
#dataResult = pickle.load(file('/data/dspitzbart/Results2015/Prediction_SFtemplates_fullSR_lep_data_2.1/singleLeptonic_Spring15__estimationResults_pkl_kappa_corrected'))

colors = [ROOT.kBlue+2, ROOT.kBlue-4, ROOT.kBlue-7, ROOT.kBlue-9, ROOT.kCyan-9, ROOT.kCyan-6, ROOT.kCyan-2,ROOT.kGreen+3,ROOT.kGreen-2,ROOT.kGreen-6,ROOT.kGreen-7, ROOT.kOrange-4, ROOT.kOrange+1, ROOT.kOrange+8, ROOT.kRed, ROOT.kRed+1]
colors = [ROOT.kBlue-7, ROOT.kCyan-9, ROOT.kCyan-2, ROOT.kGreen-6, ROOT.kOrange+6, ROOT.kRed+1, ROOT.kRed-6, ROOT.kYellow+2]

bErrH = ROOT.TH1F('bErrH','b-jet SFs',bins,0,bins)
wXErrH = ROOT.TH1F('WXErrH','W+jets x-sec',bins,0,bins)
ttXErrH = ROOT.TH1F('ttXErrH','t#bar{t}+jets x-sec',bins,0,bins)
wPErrH = ROOT.TH1F('wPErrH','W polarization',bins,0,bins)
rcsErrH = ROOT.TH1F('rcsErrH','R_{CS} systematics',bins,0,bins)
qcdErrH = ROOT.TH1F('qcdErrH','QCD fit',bins,0,bins)
puErrH = ROOT.TH1F('puErrH','pile-up',bins,0,bins)
lepSFErrH = ROOT.TH1F('lepSFErrH','lepton SFs',bins,0,bins)

dummy = ROOT.TH1F('dummy','',bins,0,bins)
dummy.SetLineColor(ROOT.kWhite)
dummy.SetFillColor(ROOT.kWhite)

ratio = ROOT.TH1F('ratio','ratio',bins,0,bins)

hists = [rcsErrH,bErrH,wXErrH,ttXErrH,wPErrH,qcdErrH, puErrH, lepSFErrH]
for i_h,h in enumerate(hists):
  h.SetFillColor(colors[i_h])
  h.SetLineColor(colors[i_h]+1)
  h.SetLineWidth(1)
  

totalH = ROOT.TH1F('totalH','total',bins,0,bins)
totalH.SetLineColor(ROOT.kBlack)
totalH.SetLineWidth(2)
totalH.SetMarkerStyle(21)
totalH.SetMarkerSize(1)

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
      bErr = sqrt(b_err[srNJet][stb][htb]**2 + l_err[srNJet][stb][htb]**2) # sum of squares of b/c and mistag
      bErrH.SetBinContent(i, bErr)\

      #W x-sec
      wXErr = (abs(w_h1b.GetBinContent(i))+abs(w_h2b.GetBinContent(i)))/2 # w x-sec
      wXErrH.SetBinContent(i, wXErr)

      #ttbar x-sec
      ttXErr = (abs(tt_h1b.GetBinContent(i))+abs(tt_h2b.GetBinContent(i)))/2 # ttbar x-sec
      ttXErrH.SetBinContent(i, ttXErr)
      
      #pile-up
      puErr = (abs(pu_h1b.GetBinContent(i))+abs(pu_h2b.GetBinContent(i)))/2 # w x-sec
      puErrH.SetBinContent(i, puErr)
      
      #lepton SF
      lepSFErr = (abs(lepSF_h1b.GetBinContent(i))+abs(lepSF_h2b.GetBinContent(i)))/2 # w x-sec
      lepSFErrH.SetBinContent(i, lepSFErr)

      #W polarization      
      wPErr = sqrt(((abs(wpol[srNJet][stb][htb]['uWPolMinus10'])+abs(wpol[srNJet][stb][htb]['uWPolPlus10']))/2)**2 + ((abs(wpol[srNJet][stb][htb]['uTTPolMinus5'])+abs(wpol[srNJet][stb][htb]['uTTPolPlus5']))/2)**2) # w pol for w and ttbar
      wPErrH.SetBinContent(i, wPErr)
      
      #QCD fit
      qcdErr = qcd_err[srNJet][stb][htb]
      qcdErrH.SetBinContent(i, qcdErr)
      
      rcsErr = sqrt(rcs[srNJet][stb][htb]['W_pred_errs']['syst']**2+rcs[srNJet][stb][htb]['TT_rCS_fits_MC']['syst']**2)/rcs[srNJet][stb][htb]['tot_pred']
      print rcs[srNJet][stb][htb]['W_pred_errs']['syst'], rcs[srNJet][stb][htb]['TT_rCS_fits_MC']['syst'], rcs[srNJet][stb][htb]['tot_pred']
      rcsErrH.SetBinContent(i,rcsErr)
      
      totalSyst = bErr**2 + wXErr**2 + ttXErr**2 + wPErr**2 + rcsErr**2 + qcdErr**2
      totalSyst = sqrt(totalSyst)
      
      dataStat = dataResult[srNJet][stb][htb]['tot_pred_err']/dataResult[srNJet][stb][htb]['tot_pred']
      total = sqrt(totalSyst**2+dataStat**2)
      totalH.SetBinContent(i, totalSyst)
      
      systematics = {'btagSF':bErr, 'Wxsec':wXErr, 'TTxsec':ttXErr, 'Wpol':wPErr, 'rcs':rcsErr, 'QCD':qcdErr, 'total':totalSyst}
      
      rcs[srNJet][stb][htb]['systematics'] = systematics
            
      print 'Stat. unc.:',round(dataStat,3)
      print 'Syst. unc.:',round(totalSyst,3)
      print 'Total unc.:',round(total,3)

      ratio.SetBinContent(i,1)
      totalYErr.append(total)
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

h_Stack.Add(rcsErrH)
h_Stack.Add(bErrH)
h_Stack.Add(qcdErrH)
h_Stack.Add(wXErrH)
h_Stack.Add(ttXErrH)
h_Stack.Add(wPErrH)
h_Stack.Add(puErrH)
h_Stack.Add(lepSFErrH)

h_Stack.SetMaximum(0.6)
h_Stack.SetMinimum(0)

leg = ROOT.TLegend(0.7,0.75,0.98,0.95)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.04)
leg.AddEntry(totalH)
leg.AddEntry(rcsErrH,'','f')
leg.AddEntry(bErrH,'','f')
leg.AddEntry(wXErrH,'','f')

leg2 = ROOT.TLegend(0.43,0.75,0.7,0.95)
leg2.SetFillColor(ROOT.kWhite)
leg2.SetShadowColor(ROOT.kWhite)
leg2.SetBorderSize(1)
leg2.SetTextSize(0.04)
leg2.AddEntry(qcdErrH,'','f')
leg2.AddEntry(ttXErrH,'','f')
leg2.AddEntry(wPErrH,'','f')
leg2.AddEntry(puErrH,'','f')

leg3 = ROOT.TLegend(0.15,0.75,0.43,0.95)
leg3.SetFillColor(ROOT.kWhite)
leg3.SetShadowColor(ROOT.kWhite)
leg3.SetBorderSize(1)
leg3.SetTextSize(0.04)
leg3.AddEntry(lepSFErrH,'','f')
leg3.AddEntry(dummy,'','f')
leg3.AddEntry(dummy,'','f')
leg3.AddEntry(dummy,'','f')



h_Stack.Draw('hist')
totalH.Draw('hist same')
totalH.Draw('p same')

h_Stack.GetXaxis().SetLabelSize(0.)
h_Stack.GetXaxis().SetLabelOffset(10)
h_Stack.GetYaxis().SetTitle('syst. unc.')
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

setNiceBinLabel(ratio, signalRegion3fb)
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
total_err.SetFillColor(ROOT.kGray+1)
total_err.SetFillStyle(3244)
total_err.Draw('2 same')

can.cd()

can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2015/syst_errors_6.png')
can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2015/syst_errors_6.root')
can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2015/syst_errors_6.pdf')

pickle.dump(rcs, file(pickleDir+'resultsFinal_withSystematics_pkl','w'))

