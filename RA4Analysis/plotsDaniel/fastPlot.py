import ROOT
import os, sys, copy

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import getVarValue, getChain, deltaPhi
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2 import *
from Workspace.RA4Analysis.helpers import *

binning=[16,0,3.2]

prepresel = 'singleLeptonic==1&&'#&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&'
presel = prepresel + 'Jet_pt[1]>80&&nJet30>=2&&nBJetMediumCMVA30==0&&st>=150&&st<=250'#&&htJet30j>500&&htJet30j<750'#&&htJet30j>=500&&st>=200&&deltaPhi_Wl>1&&mt2w>350'

varstring="deltaPhi_Wl"
plotDir='/afs/hephy.at/user/d/dspitzbart/www/plots/'

#BKG Samples
WJETS = getChain(WJetsHTToLNu['hard'],histname='')
TTJETS = getChain(ttJets['hard'],histname='')
TTVH = getChain(TTVH['hard'],histname='')
SINGLETOP = getChain(singleTop['hard'],histname='')
DY = getChain(DY['hard'],histname='')
QCD = getChain(QCD['hard'],histname='')


#SIG Samples
SIG1 = getChain(SMS_T5qqqqWW_Gl1200_Chi1000_LSP800['hard'],histname='')
SIG2 = getChain(SMS_T5qqqqWW_Gl1500_Chi800_LSP100['hard'],histname='')

wjets = {
  "name":"W + Jets", "chain":WJETS, "weight":"weight", "color":color('wjets')}
ttjets = {
  "name":"t#bar{t} + Jets", "chain":TTJETS, "weight":"weight", "color":color('ttjets')}
ttvh = {
  "name":"TTVH", "chain":TTVH, "weight":"weight", "color":color('ttvh')}
singletop = {
  "name":"single top", "chain":SINGLETOP, "weight":"weight", "color":color('singletop')}
dy = {
  "name":"Drell Yan", "chain":DY, "weight":"weight", "color":color('dy')}
qcd = {
  "name":"QCD", "chain":QCD, "weight":"weight", "color":color('qcd')}



#signal1 = {'name':'SMS_T5qqqqWW_Gl1200_Chi1000_LSP800', 'chain':SIG1, 'weight':'weight', 'color':ROOT.kBlack, "histo":ROOT.TH1F("Signal 1", "sqrt(s)", *binning)}
#signal2 = {'name':'SMS_T5qqqqWW_Gl1500_Chi800_LSP100', 'chain':SIG2, 'weight':'weight', 'color':ROOT.kBlue+2, "histo":ROOT.TH1F("Signal 2", "sqrt(s)", *binning)}

sigSamples=[]
#sigSamples.append(signal1)
#sigSamples.append(signal2)

bkgSamples=[]
bkgSamples.append(qcd)
bkgSamples.append(ttvh)
bkgSamples.append(dy)
bkgSamples.append(singletop)
bkgSamples.append(wjets)
bkgSamples.append(ttjets)

h_Stack = ROOT.THStack('h_Stack',varstring)
h_Stack_S = ROOT.THStack('h_Stack_S',varstring)

can1 = ROOT.TCanvas(varstring,varstring,1200,1000)

h1=ROOT.TH1F("MCDataCombined","MCDataCombined", *binning)
h3=ROOT.TH1F("MCDataCombined","MCDataCombined", *binning)

l = ROOT.TLegend(0.65,0.65,0.9,0.9)
l.SetFillColor(0)
l.SetShadowColor(ROOT.kWhite)
l.SetBorderSize(1)

for sample in bkgSamples:
  chain = sample["chain"]
  print chain
  histo = 'h_'+sample["name"]
  histoname = histo
  print histoname
  histo = ROOT.TH1F(str(histo) ,str(histo),*binning)
  print histo
  color = sample["color"]
  print color
  chain.Draw(varstring+'>>'+str(histoname),'weight*('+presel+')')
  histo.SetLineColor(ROOT.kBlack)
  histo.SetLineWidth(1)
  histo.SetMarkerSize(0)
  histo.SetMarkerStyle(0)
  histo.SetTitleSize(20)
  histo.GetXaxis().SetTitle(varstring)
  histo.GetYaxis().SetTitle("Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV")
  histo.GetXaxis().SetLabelSize(0.04)
  histo.GetYaxis().SetLabelSize(0.04)
  histo.GetYaxis().SetTitleOffset(0.8)
  histo.GetYaxis().SetTitleSize(0.05)
  histo.SetFillColor(sample["color"])
  histo.SetFillStyle(1001)
  histo.SetMinimum(.0008)
  h_Stack.Add(histo)
  h1.Add(histo)
  l.AddEntry(histo, sample["name"])

signalString=''

for sample in sigSamples:
  chain = sample["chain"]
  print chain
  histo = 'h_'+sample["name"]
  histoname = histo
  print histoname
  histo = ROOT.TH1F(str(histo) ,str(histo),*binning)
  print histo
  color = sample["color"]
  print color
  chain.Draw(varstring+'>>'+str(histoname),'weight*('+presel+')')
  histo.SetLineColor(color)
  histo.SetLineWidth(2)
  histo.SetMarkerSize(0)
  histo.SetMarkerStyle(0)
  histo.SetTitleSize(20)
  histo.GetXaxis().SetTitle(varstring)
  histo.GetYaxis().SetTitle("Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV")
  histo.GetXaxis().SetLabelSize(0.04)
  histo.GetYaxis().SetLabelSize(0.04)
  histo.GetYaxis().SetTitleOffset(0.8)
  histo.GetYaxis().SetTitleSize(0.05)
  histo.SetFillColor(0)
  histo.SetMinimum(.0008)
  h_Stack_S.Add(histo)
  h3.Add(histo)
  l.AddEntry(histo, sample["name"])
  signalString+=sample["name"]

pad1=ROOT.TPad("pad1","MyTitle",0,0.3,1,1.0)
pad1.SetBottomMargin(0)
pad1.SetLeftMargin(0.1)
pad1.SetGrid()
pad1.SetLogy()
pad1.Draw()
pad1.cd()

histo.GetXaxis().SetTitle(varstring)
histo.GetYaxis().SetTitle("Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV")
histo.GetXaxis().SetLabelSize(0.04)
histo.GetYaxis().SetLabelSize(0.04)
histo.GetYaxis().SetTitleOffset(0.8)
histo.GetYaxis().SetTitleSize(0.05)


h_Stack.Draw()
h_Stack.SetMinimum(0.0008)
h_Stack_S.Draw('noStacksame')
l.Draw()

#Draw ratio MC/Data
can1.cd()
pad2=ROOT.TPad("pad2","pad2",0,0.05,1.,0.3)
pad2.SetGrid()
pad2.Draw()
pad2.cd()
pad2.SetTopMargin(0)
pad2.SetBottomMargin(0.3)
pad2.SetLeftMargin(0.1)

h3.Divide(h1)
h3.SetMaximum(1.35)
h3.SetMinimum(0.)
h3.GetXaxis().SetLabelSize(0.10)
h3.GetXaxis().SetTitle(varstring)
h3.GetXaxis().SetTitleSize(0.15)

h3.GetYaxis().SetLabelSize(0.10)
h3.GetYaxis().SetTitle("Signal / BG")
h3.GetYaxis().SetNdivisions(505)
h3.GetYaxis().SetTitleSize(0.15)
h3.GetYaxis().SetTitleOffset(0.3)
h3.SetLineColor(ROOT.kBlack)
h3.Draw("E1P")

#Draw Title
can1.cd()
pad1.cd()
t1=ROOT.TLatex()
t1.SetTextFont(22)
t1.DrawLatex(150,600,"CMS preliminary")
t1.DrawLatex(150,300,"L=19.4 fb^{-1}, #sqrt{s}=8TeV")

can1.Print(plotDir+varstring+'_'+presel+signalString+'.png')
can1.Print(plotDir+varstring+'_'+presel+signalString+'.pdf')
can1.Print(plotDir+varstring+'_'+presel+signalString+'.root')



#can1.SetLogy()

