import ROOT
import pickle, os
import UserString
import copy


from os import listdir
from os.path import isfile, join

from Workspace.RA4Analysis.helpers import *

ROOT.gROOT.Reset()

path = '/afs/hephy.at/user/d/dspitzbart/www/Spring15/25ns/templateFit_SFtemplates_fullSR_lep_data_2p25/'

files = [f for f in listdir(path) if isfile(join(path, f))]

rootfiles = [f for f in files if 'root' in f]

#name = 'st250-350_ht750_njet6-7_nBTagFitRes'


for rfile in rootfiles:
  
  print rfile

  ROOT.gROOT.Reset()
  f = ROOT.TFile(path+rfile,'READ')
  c = f.Get('c1')

  tmp = UserString.MutableString(rfile)

  for i in '.root':
    del(tmp[-1])
  name = copy.deepcopy(tmp)
  name = str(name)
  del f
  
  if '3-4' in name:
    hasQCD = False
  else:
    hasQCD = True
  
  c.Draw()
  
  can1 = ROOT.TCanvas('can1','mycan1')
  p1 = c.GetPrimitive('c1_2')
  #p1.SetPad(0,0,1,1)
  p1 = p1.Clone()
  p1.SetName('myp1')
  p1.Draw()
  
  can3 = ROOT.TCanvas('can3','mycan3')
  p2 = c.GetPrimitive('c1_1')
  #p2.SetPad(0,0,1,1)
  p2.SetName('myp2')
  p2.Draw()
  
  del c
  
  curve1_1 = p1.GetPrimitive('model_NegPdg_Norm[nBJetMediumCSV30]')
  curve2_1 = p1.GetPrimitive('model_NegPdg_Norm[nBJetMediumCSV30]_Comp[model_WJets_NegPdg]')
  curve3_1 = p1.GetPrimitive('model_NegPdg_Norm[nBJetMediumCSV30]_Comp[model_TTJets]')
  curve4_1 = p1.GetPrimitive('model_NegPdg_Norm[nBJetMediumCSV30]_Comp[model_Rest_NegPdg]')
  if hasQCD: curve5_1 = p1.GetPrimitive('model_NegPdg_Norm[nBJetMediumCSV30]_Comp[model_QCD]')
  h_d_1 = p1.GetPrimitive('h_data')
  
  curve1_2 = p2.GetPrimitive('model_PosPdg_Norm[nBJetMediumCSV30]')
  curve2_2 = p2.GetPrimitive('model_PosPdg_Norm[nBJetMediumCSV30]_Comp[model_WJets_PosPdg]')
  curve3_2 = p2.GetPrimitive('model_PosPdg_Norm[nBJetMediumCSV30]_Comp[model_TTJets]')
  curve4_2 = p2.GetPrimitive('model_PosPdg_Norm[nBJetMediumCSV30]_Comp[model_Rest_PosPdg]')
  if hasQCD: curve5_2 = p2.GetPrimitive('model_PosPdg_Norm[nBJetMediumCSV30]_Comp[model_QCD]')
  h_d_2 = p2.GetPrimitive('h_data')
  
  curve1 = ROOT.RooCurve('total','total',curve1_1,curve1_2)
  curve2 = ROOT.RooCurve('wjets','wjets',curve2_1,curve2_2)
  curve3 = ROOT.RooCurve('ttjets','ttjets',curve3_1,curve3_2)
  curve4 = ROOT.RooCurve('rest','rest',curve4_1,curve4_2)
  if hasQCD: curve5 = ROOT.RooCurve('qcd','qcd',curve5_1,curve5_2)
  h_d = ROOT.RooHist(h_d_1, h_d_2)
  
  histMax = h_d.GetHistogram().GetMaximum()
  histMax = histMax*1.3
  
  curve1.SetLineStyle(2)
  curve2.SetLineColor(color('wjets'))
  curve3.SetLineColor(color('ttjets')-2)
  curve4.SetLineColor(color('dy'))
  if hasQCD: curve5.SetLineColor(color('qcd'))
  
  h_d.SetLineWidth(5)
  h_d.SetMarkerSize(1.3)
  curve1.SetLineWidth(5)
  curve2.SetLineWidth(5)
  curve3.SetLineWidth(5)
  curve4.SetLineWidth(5)
  if hasQCD: curve5.SetLineWidth(5)
  
  ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
  ROOT.setTDRStyle()
  
  can2 = ROOT.TCanvas('can2','',650,650)
  
  h_t = ROOT.TH1F('h_t','h_t',3,0,3)
  
  h_t.SetMaximum(histMax)
  
  h_t.GetXaxis().SetTitle('n_{b-tag}')
  h_t.GetXaxis().SetTitleSize(0.065)
  h_t.GetXaxis().SetBinLabel(1,'0')
  h_t.GetXaxis().SetBinLabel(2,'1')
  h_t.GetXaxis().SetBinLabel(3,'#geq2')
  h_t.GetXaxis().SetLabelSize(0.08)
  
  h_t.GetYaxis().SetTitle('Events')
  h_t.GetYaxis().SetNdivisions(508)
  
  h_d.SetLineColor(ROOT.kBlack)
  h_d.SetLineWidth(2)
  
  
  h_t.Draw()
  
  curve1.Draw('same')
  curve2.Draw('same')
  curve3.Draw('same')
  curve4.Draw('same')
  if hasQCD: curve5.Draw('same')
  h_d.Draw('E1P same')
  
  latex1 = ROOT.TLatex()
  latex1.SetNDC()
  latex1.SetTextSize(0.04)
  latex1.SetTextAlign(11)
  
  latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{Preliminary}}')
  latex1.DrawLatex(0.75,0.96,"2.2fb^{-1} (13TeV)")
  
  #if curve5_1:
  #  lowerBound = 0.70
  #else:
  #  lowerBound = 0.75
  leg = ROOT.TLegend(0.72,0.7,0.98,0.95)
  leg.SetFillColor(ROOT.kWhite)
  leg.SetShadowColor(ROOT.kWhite)
  leg.SetBorderSize(1)
  leg.SetTextSize(0.035)
  leg.AddEntry(h_d, 'data', 'lp')
  leg.AddEntry(curve1, 'total', 'l')
  leg.AddEntry(curve2, 'W+jets', 'l')
  leg.AddEntry(curve3, 't#bar{t}+jets', 'l')
  if hasQCD: leg.AddEntry(curve5, 'QCD', 'l')
  leg.AddEntry(curve4, 'other', 'l')
  #if curve5: leg.AddEntry(curve5, 'QCD', 'l')
  leg.Draw()
  
  
  printPath = '/afs/hephy.at/user/d/dspitzbart/www/Results2016/btagFitResults/'
  
  if not os.path.exists(printPath):
    os.makedirs(printPath)
  
  can2.Print(printPath+name+'.png')
  can2.Print(printPath+name+'.pdf')
  can2.Print(printPath+name+'.root')
  
  del p1, p2
  #del can1, can2, can3, h_t, histMax


