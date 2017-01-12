# only works with x-forwarding turned off

import ROOT
import pickle, os
import UserString
import copy


from os import listdir
from os.path import isfile, join

from Workspace.RA4Analysis.helpers import *

ROOT.gROOT.Reset()

path = '/afs/hephy.at/user/d/dspitzbart/www/Results2016B/QCDestimation/Moriond17SR_v8_36p5fb/data/templateFit/'

files = [f for f in listdir(path) if isfile(join(path, f))]

rootfiles = [f for f in files if 'root' in f]


#rootfiles = [rootfiles[0]]

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
  
  kinematics = name.split('_')
  lt = kinematics[2].split('t')[1].split('-')
  ht = kinematics[3].split('t')[1].split('-')
  njet = kinematics[4].split('t')[1].split('-')
  
  c.Draw()
  
  
  curve1 = c.GetPrimitive('model_Norm[Lp]')
  curve2 = c.GetPrimitive('model_Norm[Lp]_Comp[model_QCD]')
  curve3 = c.GetPrimitive('model_Norm[Lp]_Comp[model_EWK]')
  h_d    = c.GetPrimitive('h_data')
  
  
  #curve1 = ROOT.RooCurve('total','total',curve1_1)
  #curve2 = ROOT.RooCurve('QCD','QCD',curve2_1)
  #curve3 = ROOT.RooCurve('EWK','EWK',curve3_1)
  #h_d = ROOT.RooHist(h_d_1)
  
  histMax = h_d.GetHistogram().GetMaximum()
  histMax = histMax*1.3
  
  curve1.SetLineStyle(1)
  curve2.SetLineColor(color('QCD'))
  curve3.SetLineColor(color('ttjets')-2)
  
  h_d.SetLineWidth(5)
  h_d.SetMarkerSize(1)
  curve1.SetLineWidth(3)
  curve2.SetLineWidth(3)
  curve3.SetLineWidth(3)
  
  ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
  ROOT.setTDRStyle()
  
  can2 = ROOT.TCanvas('can2','',650,650)
  
  h_t = ROOT.TH1F('h_t','h_t',32,-0.6,2.6)
  
  h_t.SetMaximum(histMax)
  
  h_t.GetXaxis().SetTitle('L_{p}')
  h_t.GetXaxis().SetTitleSize(0.065)
  #h_t.GetXaxis().SetBinLabel(1,'0')
  #h_t.GetXaxis().SetBinLabel(2,'1')
  #h_t.GetXaxis().SetBinLabel(3,'#geq2')
  #h_t.GetXaxis().SetLabelSize(0.08)
  
  h_t.GetYaxis().SetTitle('Events')
  h_t.GetYaxis().SetTitleOffset(1.4)
  h_t.GetYaxis().SetNdivisions(508)
  
  h_d.SetLineColor(ROOT.kBlack)
  h_d.SetLineWidth(2)
  
  
  h_t.Draw()
  
  curve1.Draw('same')
  curve2.Draw('same')
  curve3.Draw('same')
  h_d.Draw('E1P same')
  
  latex1 = ROOT.TLatex()
  latex1.SetNDC()
  latex1.SetTextSize(0.04)
  latex1.SetTextAlign(11)
  
  latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{Preliminary}}')
  latex1.DrawLatex(0.71,0.96,"#bf{36.5 fb^{-1} (13 TeV)}")
  
  latex2 = ROOT.TLatex()
  latex2.SetNDC()
  latex2.SetTextSize(0.04)
  latex2.SetTextAlign(11)
  
  if len(lt)>1: lt_str = lt[0]+' #leq L_{T} < '+lt[1] + ' GeV'
  else: lt_str = 'L_{T} #geq ' + lt[0]+' GeV'
  if len(ht)>1: ht_str = ht[0]+' #leq H_{T} < '+ht[1] + ' GeV'
  else: ht_str = 'H_{T} #geq ' + ht[0] + ' GeV'
  if len(njet)>1: njet_str = njet[0]+' #leq n_{jet} #leq '+njet[1]
  else:
    if njet[0] == 'Eq5': njet_str = 'n_{jet} = 5'
    else: njet_str = 'n_{jet} #geq ' + njet[0]
  
  print lt_str

  latex2.DrawLatex(0.20,0.89,lt_str)
  latex2.DrawLatex(0.20,0.85,ht_str)
  latex2.DrawLatex(0.20,0.81,njet_str)
  
  lowerBound = 0.79
  leg = ROOT.TLegend(0.65,lowerBound,0.98,0.95)
  leg.SetFillColor(ROOT.kWhite)
  leg.SetShadowColor(ROOT.kWhite)
  leg.SetBorderSize(1)
  leg.SetTextSize(0.035)
  leg.AddEntry(h_d, 'Data', 'lp')
  leg.AddEntry(curve1, 'Full fit', 'l')
  leg.AddEntry(curve2, 'QCD fit (Data)', 'l')
  leg.AddEntry(curve3, 'EWK fit (MC)', 'l')
  leg.Draw()
  
  
  printPath = '/afs/hephy.at/user/d/dspitzbart/www/Results2016/QCD_fit_v8/'
  
  if not os.path.exists(printPath):
    os.makedirs(printPath)
  
  can2.Print(printPath+name+'.png')
  can2.Print(printPath+name+'.pdf')
  can2.Print(printPath+name+'.root')
  
  del c
  #del can1, can2, can3, h_t, histMax


