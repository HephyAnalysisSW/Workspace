import ROOT
import pickle
import copy, os, sys
import time, datetime
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.TH1F().SetDefaultSumw2()
ROOT.setTDRStyle()
#ROOT.gStyle.SetMarkerStyle(1)
ROOT.gStyle.SetOptTitle(0)

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.HEPHYPythonTools.asym_float import *

from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *

from Workspace.RA4Analysis.cmgTuples_Spring16_Moriond2017_MiniAODv2_antiSel_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Data25ns_Moriond2017_antiSel_postprocessed import *

from array import array

lumi = 36.5
sampleLumi = 1.0
MCweight = '(1)'
#weight_str, weight_err_str = makeWeight(lumi, sampleLumi, reWeight=MCweight) #only use electron trigger efficiency (0.931), pureweight not yet implemented

presel        = 'nLep==1&&nVeto==0&&leptonPt>25&&nEl==1&&Jet2_pt>80&& iso_Veto'
antiSelStr    = presel + '&&Selected==(-1)'
SelStr        = presel + '&&Selected==1'

cQCD  = getChain(QCDHT_antiSel,histname='')

HTbinsMultiB = [(500,1000), (1000,1500), (500,1500), (1500,-1)]
HTbinsMultiB_names = ['HT0i'] + ['HT01','HT23','HT03','HT4i']*4

HTbinsZeroB  = [(500,-1),(500,750), (500,1000), (500,1250), (750,1250), (750,-1), (1000,-1), (1250,-1)]
HTbinsZeroB_names = ['HT0i','HT0i','HT0','HT01','HT02','HT12','HT1i','HT2i','HT3i']

nJbinsMultiB = [(4,5),(6,8),(9,-1)]
nBJbinsMultiB = [(0,0),(1,1),(2,2),(3,-1)]
multiBNames = ['n_{b} = 0', 'n_{b} = 1', 'n_{b} = 2', 'n_{b} #geq 3']

#nJbinsZeroB = [(4,5),(4,4),(5,5),(6,6)]
nJbinsZeroB = [(4,5),(5,5),(6,7),(8,-1)]
#zeroBNames = ['n_{b} = 0, n_{j} #in [4,5]', 'n_{b} = 0,  n_{j} = 4', 'n_{b} = 0,  n_{j} = 5', 'n_{b} = 0,  n_{j} = 6']
zeroBNames = ['n_{b} #geq 1,  n_{j} #in [4,5]', 'n_{b} = 0,  n_{j} = 5', 'n_{b} = 0,  n_{j} #in [6,7]', 'n_{b} = 0,  n_{j} #geq 8']


colors = [ROOT.kOrange+8, ROOT.kGreen+2, ROOT.kCyan+2, ROOT.kBlue+2]

multiB_hists = []
for i in range(4):
  multiB_hists.append(ROOT.TH1F('mulitb'+str(i), multiBNames[i], 4*13, 0, 13))
  multiB_hists[-1].SetLineColor(colors[i])
  multiB_hists[-1].SetMarkerColor(colors[i])
  multiB_hists[-1].SetLineWidth(2)

multiB_h = ROOT.TH1F('multib','multib',13,0,13)
multiB_h.SetLineWidth(2)
multiB_h.SetMinimum(0)
multiB_h.SetMaximum(0.4)
multiB_h.GetYaxis().SetTitle('F-ratio')
multiB_h.GetXaxis().SetLabelSize(0.06)

for i in range(1,14):
  multiB_h.GetXaxis().SetBinLabel(i, HTbinsMultiB_names[i-1])

zeroB_hists = []
for i in range(4):
  zeroB_hists.append(ROOT.TH1F('zerob'+str(i), zeroBNames[i], 4*9, 0, 9))
  zeroB_hists[-1].SetLineColor(colors[i])
  zeroB_hists[-1].SetMarkerColor(colors[i])
  zeroB_hists[-1].SetLineWidth(2)

zeroB_h = ROOT.TH1F('zerob','zerob',9,0,9)
zeroB_h.SetLineWidth(2)
zeroB_h.SetMinimum(0)
zeroB_h.SetMaximum(0.4)
zeroB_h.GetYaxis().SetTitle('F-ratio')
zeroB_h.GetXaxis().SetLabelSize(0.06)

for i in range(1,10):
  zeroB_h.GetXaxis().SetBinLabel(i, HTbinsZeroB_names[i-1])


antiSelname, antiSelCut = nameAndCut((250,-1), (500,-1), (3,4), btb=(0,0), presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30', stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean')
Selname, SelCut         = nameAndCut((250,-1), (500,-1), (3,4), btb=(0,0), presel=SelStr, charge="", btagVar = 'nBJetMediumCSV30', stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean')

FselIncl = asym_float(getYieldFromChain(cQCD, SelCut, 'weight', returnError=True))/asym_float(getYieldFromChain(cQCD, antiSelCut, 'weight', returnError=True))
multiB_h.SetBinContent(1, FselIncl.central)
multiB_h.SetBinError(1, FselIncl.up)
zeroB_h.SetBinContent(1, FselIncl.central)
zeroB_h.SetBinError(1, FselIncl.up)


f_sel = ROOT.TF1("f_sel","[0]",0,15)
f_sel.SetParameter(0,FselIncl)
f_sel.SetLineColor(ROOT.kBlack)
f_sel.SetLineWidth(2)

multiB_syst_yErr   = [0, 0.15*FselIncl, 0.3*FselIncl, 0.5*FselIncl]
multiB_syst_y      = [FselIncl]*4
multiB_syst_xErr   = [0.5,2,2,2]
multiB_syst_x      = [0.5,3,7,11]
multiB_ax    = array('d',multiB_syst_x)
multiB_ay    = array('d',multiB_syst_y)
multiB_aexh  = array('d',multiB_syst_xErr)
multiB_aexl  = array('d',multiB_syst_xErr)
multiB_aeyh  = array('d',multiB_syst_yErr)
multiB_aeyl  = array('d',multiB_syst_yErr)
multiB_syst_err = ROOT.TGraphAsymmErrors(4, multiB_ax,  multiB_ay,  multiB_aexl,  multiB_aexh,  multiB_aeyl,  multiB_aeyh)
multiB_syst_err.SetFillColor(ROOT.kGray+1)
multiB_syst_err.SetFillStyle(3444)
multiB_syst_err.SetLineWidth(2)
multiB_syst_err.SetLineColor(ROOT.kBlack)
multiB_syst_err.SetMarkerColor(ROOT.kGray+1)
multiB_syst_err.SetMarkerStyle(0)
multiB_syst_err.SetMarkerSize(0)



zeroB_syst_yErr   = [0,0.25*FselIncl]
zeroB_syst_y      = [FselIncl,FselIncl]
zeroB_syst_xErr   = [0,4]
zeroB_syst_x      = [0.5,5]
zeroB_ax    = array('d',zeroB_syst_x)
zeroB_ay    = array('d',zeroB_syst_y)
zeroB_aexh  = array('d',zeroB_syst_xErr)
zeroB_aexl  = array('d',zeroB_syst_xErr)
zeroB_aeyh  = array('d',zeroB_syst_yErr)
zeroB_aeyl  = array('d',zeroB_syst_yErr)
zeroB_syst_err = ROOT.TGraphAsymmErrors(2, zeroB_ax, zeroB_ay, zeroB_aexl, zeroB_aexh, zeroB_aeyl, zeroB_aeyh)
zeroB_syst_err.SetFillColor(ROOT.kGray+1)
zeroB_syst_err.SetFillStyle(3444)
zeroB_syst_err.SetLineWidth(2)
zeroB_syst_err.SetLineColor(ROOT.kBlack)
zeroB_syst_err.SetMarkerColor(ROOT.kGray+1)
zeroB_syst_err.SetMarkerStyle(0)
zeroB_syst_err.SetMarkerSize(0)


for inb, nb in enumerate(nBJbinsMultiB):
  print
  print nb
  i = 1
  for nj in nJbinsMultiB:
    for ht in HTbinsMultiB:
      print nj, ht
      antiSelname, antiSelCut = nameAndCut((250,-1), ht, nj, btb=nb, presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30', stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean')
      Selname, SelCut         = nameAndCut((250,-1), ht, nj, btb=nb, presel=SelStr, charge="", btagVar = 'nBJetMediumCSV30', stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean')
      Fsel = asym_float(getYieldFromChain(cQCD, SelCut, 'weight', returnError=True))/asym_float(getYieldFromChain(cQCD, antiSelCut, 'weight', returnError=True))
      multiB_hists[inb].SetBinContent(1+inb+4*i, Fsel.central)
      multiB_hists[inb].SetBinError(1+inb+4*i, Fsel.up)
      #if nj == (4,5):     multiB_syst.append ( 0.25 )
      #elif nj == (6,8):   multiB_syst.append ( 0.5 )
      #elif nj == (9,-1):  multiB_syst.append ( 0.5 )
      print Fsel
      i += 1

for inj, nj in enumerate(nJbinsZeroB):
  print
  print nj
  i = 1
  for ht in HTbinsZeroB:
    nb = (0,0)
    if nj == (4,5): nb = (1,-1)
    else: nb = (0,0)
    print nb, ht
    antiSelname, antiSelCut = nameAndCut((250,-1), ht, nj, btb=nb, presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30', stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean')
    Selname, SelCut         = nameAndCut((250,-1), ht, nj, btb=nb, presel=SelStr, charge="", btagVar = 'nBJetMediumCSV30', stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean')
    Fsel = asym_float(getYieldFromChain(cQCD, SelCut, 'weight', returnError=True))/asym_float(getYieldFromChain(cQCD, antiSelCut, 'weight', returnError=True))
    zeroB_hists[inj].SetBinContent(1+inj+4*i, Fsel.central)
    zeroB_hists[inj].SetBinError(1+inj+4*i, Fsel.up)
    #zeroB_syst.append ( 0.25 )
    print Fsel
    i += 1

line1 = ROOT.TLine(1,0,1,0.4)
line1.SetLineColor(ROOT.kBlack)
line1.SetLineStyle(ROOT.kDashed)
line5 = ROOT.TLine(5,0,5,0.4)
line5.SetLineColor(ROOT.kBlack)
line5.SetLineStyle(ROOT.kDashed)
line9 = ROOT.TLine(9,0,9,0.4)
line9.SetLineColor(ROOT.kBlack)
line9.SetLineStyle(ROOT.kDashed)

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)

latextitle = 'Simulation'

canMulti = ROOT.TCanvas('canMulti','Multi b', 1000,500)

leg = ROOT.TLegend(0.2,0.7,0.4,0.9)
leg.SetBorderSize(1)
leg.SetFillColor(0)
leg.SetLineColor(0)
leg.SetTextSize(0.035)

multiB_h.Draw()
line1.Draw('same')
line5.Draw('same')
line9.Draw('same')
multiB_syst_err.Draw('2 same')
for h in multiB_hists:
  h.Draw('e1p same')
  leg.AddEntry(h)
leg.AddEntry(multiB_syst_err,'F-ratio with syst. unc.')
f_sel.Draw('same')
leg.Draw()

latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{'+latextitle+'}}')
latex1.DrawLatex(0.88,0.96,'#bf{MC (13 TeV)}')
latex1.DrawLatex(0.355,0.88,'n_{j} #in [4,5]')
latex1.DrawLatex(0.61,0.88,'n_{j} #in [6,8]')
latex1.DrawLatex(0.86,0.88,'n_{j} #geq 9')

#canMulti.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016B/QCD/Moriond17/systematics_multiB.png')
#canMulti.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016B/QCD/Moriond17/systematics_multiB.pdf')
#canMulti.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016B/QCD/Moriond17/systematics_multiB.root')


canZero = ROOT.TCanvas('canZero','Zero b', 1000,500)

leg2 = ROOT.TLegend(0.2,0.7,0.4,0.9)
leg2.SetBorderSize(1)
leg2.SetFillColor(0)
leg2.SetLineColor(0)

zeroB_h.Draw()
zeroB_syst_err.Draw('2 same')
for h in zeroB_hists:
  h.Draw('e1p same')
  leg2.AddEntry(h)
leg2.AddEntry(zeroB_syst_err,'F-ratio with syst. unc.')
f_sel.Draw('same')
leg2.Draw()

latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{'+latextitle+'}}')
latex1.DrawLatex(0.88,0.96,'#bf{MC (13 TeV)}')

canZero.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016B/QCD/Moriond17/systematics_zeroB_alt.png')
canZero.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016B/QCD/Moriond17/systematics_zeroB_alt.pdf')
canZero.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016B/QCD/Moriond17/systematics_zeroB_alt.root')

