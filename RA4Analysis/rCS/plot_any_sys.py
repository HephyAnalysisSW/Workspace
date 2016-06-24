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


signalRegions = signalRegion3fb

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

saveDir =  '/data/easilar/Results2016/ICHEP/Prediction_Spring16_templates_lep_data_2p57/'
validation = False
dilep   = pickle.load(file('/data/easilar/Results2016/ICHEP/DiLep_SYS/V1/unc_with_SRAll_pkl'))

colors = [ROOT.kBlue-7, ROOT.kCyan-9, ROOT.kCyan-2, ROOT.kGreen-6, ROOT.kOrange+6, ROOT.kRed+1, ROOT.kRed-6, ROOT.kYellow+2, ROOT.kGreen, ROOT.kGreen+3, ROOT.kBlue-2]

colors = range(28,100,2)

dilepErrH = ROOT.TH1F('dilepErrH','dilep. events',bins,0,bins)


dilepC   = ROOT.TH1F('dilepC','2l constant',bins,0,bins)
dilepS   = ROOT.TH1F('dilepS','2l slope',bins,0,bins)

dummy = ROOT.TH1F('dummy','',bins,0,bins)
dummy.SetLineColor(ROOT.kWhite)
dummy.SetFillColor(ROOT.kWhite)

ratio = ROOT.TH1F('ratio','ratio',bins,0,bins)

hists = [dilepC,dilepS]
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

      #dilepErr = abs(dilep[srNJet][stb][htb]["delta_constant_Up"])*100
      #dilepErrH
      constant_err = (abs(dilep[srNJet][stb][htb]["delta_constant_Up"])+abs(dilep[srNJet][stb][htb]["delta_constant_Down"]))/2
      slope_err = (abs(dilep[srNJet][stb][htb]["delta_slope_Up"])+abs(dilep[srNJet][stb][htb]["delta_slope_Down"]))/2
      dilepC.SetBinContent(i, constant_err)
      dilepS.SetBinContent(i, slope_err)
      print constant_err , slope_err
      
      i+=1


can = ROOT.TCanvas('can','can',700,700)


h_Stack = ROOT.THStack('h_Stack','Stack')

print 'min and max of the different sources'
for h in hists:
  print h.GetName(), round(h.GetMinimum(),2), round(h.GetMaximum(),2)

for i_h,h in enumerate(hists):
  h_Stack.Add(h)

h_Stack.SetMaximum(1.0)
h_Stack.SetMinimum(0.0)

leg = ROOT.TLegend(0.7,0.75,0.98,0.95)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.04)
for i in range(2):
  leg.AddEntry(hists[i], '', 'f')


h_Stack.Draw('hist')
setNiceBinLabel(h_Stack, signalRegions)

h_Stack.GetYaxis().SetTitle('Relative uncertainty')
h_Stack.GetYaxis().SetTitleOffset(0.8)
h_Stack.GetYaxis().SetNdivisions(508)
h_Stack.GetXaxis().SetLabelSize(0.04)
h_Stack.GetXaxis().SetTitleSize(0.06)
h_Stack.GetXaxis().SetTitleOffset(2)
h_Stack.GetXaxis().SetLabelSize(0.04)
h_Stack.GetXaxis().SetNdivisions(508)
leg.Draw()

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.15,0.96,'CMS #bf{#it{Preliminary}}')
latex1.DrawLatex(0.85,0.96,"#bf{(13TeV)}")

can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/data/Run2016B/2571pb/syst_uncertainties/diLepSys_ICHEP_v4.png')
can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/data/Run2016B/2571pb/syst_uncertainties/diLepSys_ICHEP_v4.root')
can.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/data/Run2016B/2571pb/syst_uncertainties/diLepSys_ICHEP_v4.pdf')
