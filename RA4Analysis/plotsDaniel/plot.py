import ROOT
import os, sys, copy
import pickle, operator

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_Spring15_hard import *

lepSel = 'hard'

WJETS = {'name':'WJets', 'chain':getChain(WJetsHTToLNu[lepSel],histname=''), 'color':color('WJets'),'weight':'weight', 'niceName':'W Jets'}
TTJETS = {'name':'TTJets', 'chain':getChain(ttJets[lepSel],histname=''), 'color':color('TTJets'),'weight':'weight', 'niceName':'t#bar{t} Jets'}
DY = {}
QCD = {}
samples = [WJETS, TTJETS]#, DY, QCD]

st = {'name':'st', 'binning':[30,0,1500], 'titleX':'L_{T}', 'titleY':'Events'}
variables = [st]

presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80"
name, cut = nameAndCut((250,-1),(500,-1),(3,-1),btb=(0,0),presel=presel)
cuts = [cut]

def plot(samples, variable, cuts, data=False, maximum=False, minimum=0., stacking=False, filling=True, setLogY=False, setLogX=False, titleText='CMS', lumi='?', legend=True):
  can = ROOT.TCanvas('c','c',700,600)
  colorList = [ROOT.kBlue+2, ROOT.kCyan-9, ROOT.kGreen+3, ROOT.kOrange-4, ROOT.kRed+1]
  h = []
  nsamples = len(samples)
  ncuts = len(cuts)
  for isample, sample in enumerate(samples):
    for icut, cut in enumerate(cuts):
      i = isample*ncuts+icut
      h.append({'hist':ROOT.TH1F('h'+str(isample)+'_'+str(icut),sample['niceName'],*variable['binning']),'yield':0.})
      if sample['weight']=='weight':weight='weight'
      else: weight=str(sample['weight'])
      sample['chain'].Draw(variable['name']+'>>h'+str(isample)+'_'+str(icut),weight+'*('+cut+')','goff')
      h[i]['yield'] = h[i]['hist'].GetSumOfWeights()
      if minimum: h[i]['hist'].SetMinimum(minimum)
      if maximum: h[i]['hist'].SetMaximum(maximum)
      if filling:
        h[i]['hist'].SetLineColor(ROOT.kBlack)
        if len(samples)>1 or len(cuts)<2: h[i]['hist'].SetFillColor(sample['color'])
        else: h[i]['hist'].SetFillColor(colorList[icut])
      else:
        if len(samples)>1 or len(cuts)<2: h[i]['hist'].SetLineColor(sample['color'])
        else: h[i]['hist'].SetLineColor(colorList[icut])
      h[i]['hist'].SetLineWidth(2)
      h[i]['hist'].GetXaxis().SetTitle(variable['titleX'])
      #h[i]['hist'].GetXaxis().SetTitleSize(0.04)
      h[i]['hist'].GetYaxis().SetTitle(variable['titleY'])
      #h[i]['hist'].GetYaxis().SetTitleSize(0.04)
  h.sort(key=operator.itemgetter('yield'))
  if legend:
    height = 0.07*len(h)
    leg = ROOT.TLegend(0.7,0.95-height,0.98,0.95)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetShadowColor(ROOT.kWhite)
    leg.SetBorderSize(1)
    leg.SetTextSize(0.04)
    for item in reversed(h):
      leg.AddEntry(item['hist'])
  if setLogY: can.SetLogy()
  if setLogX: can.SetLogx()
  if stacking:
    h_Stack = ROOT.THStack('h_Stack','Stack')
    for item in h:
      h_Stack.Add(item['hist'])
    if minimum: h_Stack.SetMinimum(minimum)
    if maximum: h_Stack.SetMaximum(maximum)
    h_Stack.Draw('hist')
    h_Stack.GetXaxis().SetTitle(variable['titleX'])
    h_Stack.GetYaxis().SetTitle(variable['titleY'])
  else:
    first = True
    for item in reversed(h):
      if first:
        item['hist'].Draw('hist')
        first = False
      else:
        item['hist'].Draw('hist same')
  if data:
    dataHist = ROOT.TH1F('data','Data',*variable['binning'])
    data.Draw(variable['name']+'>>data',cut)
    data.Draw('e1p same')
    h['data'] = dataHist
    leg.AddEntry(dataHist)
  if titleText:
    latex1 = ROOT.TLatex()
    latex1.SetNDC()
    latex1.SetTextSize(0.04)
    latex1.SetTextAlign(11) # align right
    latex1.DrawLatex(0.17,0.96,titleText)
  if lumi:
    latex2 = ROOT.TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.04)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.75,0.96,"L="+str(lumi)+"fb^{-1} (13TeV)")
  if legend: leg.Draw()
  can.Update()
  return [h, can, leg]

#plot(samples,st,cuts)

