import ROOT
import pickle 
import copy, os, sys
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.TH1F().SetDefaultSumw2()
ROOT.setTDRStyle()
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *
from draw_helpers import *
from math import *
from Workspace.HEPHYPythonTools.user import username

preprefix = 'QCDestimation/ratioPlots'
wwwDir = '/afs/hephy.at/user/d/dhandl/www/RunII/Spring15_25ns/'+preprefix+'/'
presel = 'QCDratio_singleElectronic_'

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

path = '/data/'+username+'/results2015/QCDEstimation/'
pickleFile = '20151028_QCDestimation_pkl'
bins = pickle.load(file(path+pickleFile))

targetLumi = 1.26

def getFraction(Bkg, Bkg_err, QCD, QCD_err):
  try: res = QCD/Bkg
  except ZeroDivisionError: res = float('nan')
  try: res_err = res*sqrt(Bkg_err**2/Bkg**2 + QCD_err**2/QCD**2)
  except ZeroDivisionError: res_err = float('nan')
  return res, res_err

#define SR
signalRegion = {(3, 4): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}, #3-4jets QCD and W+jets control region
                                      (500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (350, 450): {(500, -1):   {'deltaPhi': 1.0},
                                      (500, -1):   {'deltaPhi': 0.75},
                                      (500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (450, -1):  {(500, -1):   {'deltaPhi': 1.0},
                                      (500, -1):   {'deltaPhi': 0.75},
                                      (500, 1000): {'deltaPhi': 0.75},
                                      (1000, -1):  {'deltaPhi': 0.75}}},
                (4, 5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}, #4-5jets TTbar control region
                                      (500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (350, 450): {(500, -1):   {'deltaPhi': 1.0},
                                      (500, -1):   {'deltaPhi': 0.75},
                                      (500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (450, -1):  {(500, -1):   {'deltaPhi': 1.0},
                                      (500, -1):   {'deltaPhi': 0.75},
                                      (500, 1000): {'deltaPhi': 0.75},
                                      (1000, -1):  {'deltaPhi': 0.75}}},
                (5, 5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}},  #signal regions
                         (350, 450): {(500, -1):   {'deltaPhi': 1.0}},
                         (450, -1):  {(500, -1):   {'deltaPhi': 1.0}}},
                (6, 7): {(250, 350): {(500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (350, 450): {(500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                          (450, -1): {(500, 1000): {'deltaPhi': 0.75},
                                      (1000, -1):  {'deltaPhi': 0.75}}},
                (8, -1): {(250, 350):{(500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                          (350, 450):{(500, -1):   {'deltaPhi': 0.75}},
                          (450, -1): {(500, -1):   {'deltaPhi': 0.75}}}
}

btreg = [(0,0), (1,1), (2,2)] #1b and 2b estimates are needed for the btag fit

ROOT_colors = [ROOT.kBlack, ROOT.kRed-4, ROOT.kBlue, ROOT.kGreen+2, ROOT.kOrange+1, ROOT.kAzure+6, ROOT.kCyan+3, ROOT.kOrange , ROOT.kRed-10]
text = ROOT.TLatex()
text.SetNDC()
text.SetTextSize(0.04)
text.SetTextAlign(11)

#plot F_sel-to-antisel vs. [LT,HT] in 3-4j QCD CR
canv = ROOT.TCanvas('canv','canv',600,600)

Fhist=ROOT.TH1F('Fhist','Fhist',9,0,9)
Fhist.SetLineWidth(2)
j=0
for i_CR, ltb in enumerate(sorted(signalRegion[(3,4)])):
  for i_htb,htb in enumerate(sorted(signalRegion[(3,4)][ltb])):
    j+=1
    Fhist.SetBinContent(j,bins[(3,4)][ltb][htb][(0,0)]['F_seltoantisel'])
    Fhist.SetBinError(j,bins[(3,4)][ltb][htb][(0,0)]['F_seltoantisel_err'])
    Fhist.GetXaxis().SetBinLabel(j,'LT'+str(i_CR+1)+'_HT'+str(i_htb+1))
    Fhist.GetYaxis().SetTitle('F_{sel-to-antisel}')

Fhist.Draw('L')
Fhist.SetMinimum(0.)
Fhist.SetMaximum(1.)
text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
text.DrawLatex(0.6,0.96,"#bf{L="+str(targetLumi)+" fb^{-1} (13 TeV)}")

canv.Print(wwwDir+presel+'Fsa_inCR.png')
canv.Print(wwwDir+presel+'Fsa_inCR.pdf')
canv.Print(wwwDir+presel+'Fsa_inCR.root')

canv2 = ROOT.TCanvas('canv2','canv2',600,600)

ClosureHist=ROOT.TH1F('ClosureHist','ClosureHist',9,0,9)
ClosureHist.SetLineWidth(2)
k=0
for i_CR, ltb in enumerate(sorted(signalRegion[(3,4)])):
  for i_htb,htb in enumerate(sorted(signalRegion[(3,4)][ltb])):
    k+=1
    res, res_err = getFraction(bins[(3,4)][ltb][htb][(0,0)]['NQCDSelMC'],bins[(3,4)][ltb][htb][(0,0)]['NQCDSelMC_err'],bins[(3,4)][ltb][htb][(0,0)]['NQCDpred'],bins[(3,4)][ltb][htb][(0,0)]['NQCDpred_err'])
    ClosureHist.SetBinContent(k,res)
    ClosureHist.SetBinError(k,res_err)
    ClosureHist.GetXaxis().SetBinLabel(k,'LT'+str(i_CR+1)+'_HT'+str(i_htb+1))
    ClosureHist.GetYaxis().SetTitle('#frac{N^{pred}_{QCD}}{N^{MC}_{QCD}}')

ClosureHist.Draw('L')
ClosureHist.SetMinimum(0.)
ClosureHist.SetMaximum(2.)
text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
text.DrawLatex(0.6,0.96,"#bf{L="+str(targetLumi)+" fb^{-1} (13 TeV)}")

line = ROOT.TLine()
line.SetY1(1.0)
line.SetX2(9)
line.SetHorizontal()
line.SetLineColor(ROOT.kBlack)
line.SetLineStyle(ROOT.kDashed)
line.Draw()

canv2.Print(wwwDir+presel+'FitClosure_inCR.png')
canv2.Print(wwwDir+presel+'FitClosure_inCR.pdf')
canv2.Print(wwwDir+presel+'FitClosure_inCR.root')

#plot F_sel-to-antisel binned in HT for all Njets
#ratio_ht={}
#for stb in streg:
#  ratio_ht[stb]={}
#  first = True
#  canv = ROOT.TCanvas('canv','canv',600,600)
#  #canv.SetLogy()
#  l = ROOT.TLegend(0.65,0.85,0.95,0.95)
#  l.SetFillColor(0)
#  l.SetBorderSize(1)
#  l.SetShadowColor(ROOT.kWhite)
#  
#  t=ROOT.TLatex()
#  t.SetNDC()
#  t.SetTextSize(0.04)
#  t.SetTextAlign(11)
#  for i_njb, njb in enumerate(njreg):
#    ratio_ht[stb][njb]={}
#    for btb in btreg:
#      ratio_ht[stb][njb][btb]=ROOT.TH1F('ratio_htHist','ratio_htHist',len(htreg),0,len(htreg))
#      ratio_ht[stb][njb][btb].SetLineColor(ROOT_colors[i_njb])
#      ratio_ht[stb][njb][btb].SetLineWidth(2)
#      for i_htb, htb in enumerate(htreg):
#        nQCDsel = bins[njb][stb][htb][btb]['nQCDSelected'] 
#        nQCDselVar = bins[njb][stb][htb][btb]['nQCDSelectedVar'] 
#        nQCDantisel = bins[njb][stb][htb][btb]['nAntiSelected'] 
#        nQCDantiselVar = bins[njb][stb][htb][btb]['nAntiSelectedVar'] 
##          print nQCDsel, nQCDantisel
#        if nQCDantisel>0:
#          F=nQCDsel/nQCDantisel
#          print 'F_sel-to-anti-sel('+str(stb)+','+str(njb)+','+str(htb)+'):',F
#          if F>0:
#            F_err= F*sqrt(nQCDselVar/nQCDsel**2+nQCDantiselVar/nQCDantisel**2)
#            ratio_ht[stb][njb][btb].SetBinContent(i_htb+1,F)
#            ratio_ht[stb][njb][btb].SetBinError(i_htb+1,F_err)
#            print 'F_sel-to-anti-sel Error('+str(stb)+','+str(njb)+','+str(htb)+'):',F_err
#            bins[njb][stb][htb][btb].update({'F_seltoantiselMC':F, 'F_err':F_err})
#        ratio_ht[stb][njb][btb].GetXaxis().SetBinLabel(i_htb+1, varBinName(htb,'H_{T}'))
#        ratio_ht[stb][njb][btb].GetYaxis().SetTitle('F_{sel-to-antisel}')
#        ratio_ht[stb][njb][btb].GetYaxis().SetRangeUser(0.0,1.0)
##        ratio_ht[stb][njb].GetXaxis().SetTitle('F_{sel-to-antisel}')
#      l.AddEntry(ratio_ht[stb][njb][btb], nJetBinName(njb))
#      if first:
#        ratio_ht[stb][njb][btb].Draw()
#        first = False
#      else:
#        ratio_ht[stb][njb][btb].Draw('same') 
#      l.Draw()
#      t.DrawLatex(0.175,0.85,varBinName(stb,'S_{T}'))
#      text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
#      text.DrawLatex(0.6,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")
#      canv.Print(wwwDir+presel+'Fsa_ht_'+nameAndCut(stb, None, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
#      canv.Print(wwwDir+presel+'Fsa_ht_'+nameAndCut(stb, None, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
#      canv.Print(wwwDir+presel+'Fsa_ht_'+nameAndCut(stb, None, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')
#
#
##plot F_sel-to-antisel binned in ST for all Njets
#ratio_st={}
#for htb in htreg:
#  ratio_st[htb]={}
#  first = True
#  canv2= ROOT.TCanvas('canv2','canv2',600,600)
#  #canv.SetLogy()
#  l2 = ROOT.TLegend(0.65,0.85,0.95,0.95)
#  l2.SetFillColor(0)
#  l2.SetBorderSize(1)
#  l2.SetShadowColor(ROOT.kWhite)
#  
#  t=ROOT.TLatex()
#  t.SetNDC()
#  t.SetTextSize(0.04)
#  t.SetTextAlign(11)
#  for i_njb, njb in enumerate(njreg):
#    ratio_st[htb][njb]={}
#    for btb in btreg:
#      ratio_st[htb][njb][btb]=ROOT.TH1F('ratio_stHist','ratio_stHist',len(streg),0,len(streg))
#      ratio_st[htb][njb][btb].SetLineColor(ROOT_colors[i_njb])
#      ratio_st[htb][njb][btb].SetLineWidth(2)
#      for i_stb, stb in enumerate(streg):
#        nQCDsel = bins[njb][stb][htb][btb]['nQCDSelected'] 
#        nQCDselVar = bins[njb][stb][htb][btb]['nQCDSelectedVar'] 
#        nQCDantisel = bins[njb][stb][htb][btb]['nAntiSelected'] 
#        nQCDantiselVar = bins[njb][stb][htb][btb]['nAntiSelectedVar'] 
##          print nQCDsel, nQCDantisel
#        if nQCDantisel>0:
#          F=nQCDsel/nQCDantisel
#          print 'F_sel-to-anti-sel('+str(stb)+','+str(njb)+','+str(htb)+'):',F
#          if F>0:
#            F_err= F*sqrt(nQCDselVar/nQCDsel**2+nQCDantiselVar/nQCDantisel**2)
#            ratio_st[htb][njb][btb].SetBinContent(i_stb+1,F)
#            ratio_st[htb][njb][btb].SetBinError(i_stb+1,F_err)
#            print 'F_sel-to-anti-sel Error('+str(stb)+','+str(njb)+','+str(htb)+'):',F_err
#        ratio_st[htb][njb][btb].GetXaxis().SetBinLabel(i_stb+1, varBinName(stb,'S_{T}'))
#        ratio_st[htb][njb][btb].GetYaxis().SetTitle('F_{sel-to-antisel}')
#        ratio_st[htb][njb][btb].GetYaxis().SetRangeUser(0.0,1.0)
##        ratio_st[htb][njb].GetXaxis().SetTitle('F_{sel-to-antisel}')
#      l2.AddEntry(ratio_st[htb][njb][btb], nJetBinName(njb))
#      if first:
#        ratio_st[htb][njb][btb].Draw()
#        first = False
#      else:
#        ratio_st[htb][njb][btb].Draw('same') 
#      l2.Draw()
#      t.DrawLatex(0.175,0.85,varBinName(htb,'H_{T}'))
#      text.DrawLatex(0.15,.96,"CMS Simulation")
#      text.DrawLatex(0.65,0.96,"L="+str(targetLumi/1000)+" fb^{-1} (13 TeV)")
#      canv2.Print(wwwDir+presel+'Fsa_st_'+nameAndCut(None, htb, njetb=None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
#      canv2.Print(wwwDir+presel+'Fsa_st_'+nameAndCut(None, htb, njetb=None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
#      canv2.Print(wwwDir+presel+'Fsa_st_'+nameAndCut(None, htb, njetb=None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')
#
##plot F_sel-to-antisel binned in ST vs HT
#ratio_2d={}
#for njb in njreg:
#  ratio_2d[njb]={}
#  canv3= ROOT.TCanvas('canv3','canv3',600,600)
#  #canv.SetLogy()
##  l3 = ROOT.TLegend(0.65,0.75,0.95,0.95)
##  l3.SetFillColor(0)
##  l3.SetBorderSize(1)
##  l3.SetShadowColor(ROOT.kWhite)
#  
#  t=ROOT.TLatex()
#  t.SetNDC()
#  t.SetTextSize(0.04)
#  t.SetTextAlign(11)
#  for btb in btreg:
#    ratio_2d[njb][btb]={}
#    ratio_2d[njb][btb]=ROOT.TH2F('ratio_2dHist','ratio_2dHist',len(htreg),0,len(htreg),len(streg),0,len(streg))
#    for i_htb, htb in enumerate(htreg):
#      ratio_2d[njb][btb].GetXaxis().SetBinLabel(i_htb+1,varBinName(htb,'H_{T}'))
#    for i_stb, stb in enumerate(streg):
#      ratio_2d[njb][btb].GetYaxis().SetBinLabel(i_stb+1,varBinName(stb,'S_{T}'))
#
#    for i_htb, htb in enumerate(htreg):
#      for i_stb, stb in enumerate(streg):
#        nQCDsel = bins[njb][stb][htb][btb]['nQCDSelected'] 
#        nQCDselVar = bins[njb][stb][htb][btb]['nQCDSelectedVar'] 
#        nQCDantisel = bins[njb][stb][htb][btb]['nAntiSelected'] 
#        nQCDantiselVar = bins[njb][stb][htb][btb]['nAntiSelectedVar'] 
##          print nQCDsel, nQCDantisel
#        if nQCDantisel>0:
#          F=nQCDsel/nQCDantisel
#          print 'F_sel-to-anti-sel('+str(stb)+','+str(njb)+','+str(htb)+'):',F
#          if F>0:
#            F_err= F*sqrt(nQCDselVar/nQCDsel**2+nQCDantiselVar/nQCDantisel**2)
#            ratio_2d[njb][btb].SetBinContent(i_htb+1,i_stb+1,F)
#            ratio_2d[njb][btb].SetBinError(i_htb+1,i_stb+1,F_err)
#            print 'F_sel-to-anti-sel Error('+str(stb)+','+str(njb)+','+str(htb)+'):',F_err
##      l.AddEntry(ratio_2d[htb][njb][btb], nJetBinName(njb))
#        ratio_2d[njb][btb].Draw('COLZ TEXTE')
#      t.DrawLatex(0.175,0.85,nJetBinName(njb))
#      text.DrawLatex(0.15,.96,"CMS Simulation")
#      text.DrawLatex(0.65,0.96,"L="+str(targetLumi/1000)+" fb^{-1} (13 TeV)") 
#      canv3.Print(wwwDir+presel+'st_vs_ht_'+nameAndCut(None, None, njetb=njb, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
#      canv3.Print(wwwDir+presel+'st_vs_ht_'+nameAndCut(None, None, njetb=njb, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
#      canv3.Print(wwwDir+presel+'st_vs_ht_'+nameAndCut(None, None, njetb=njb, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')
#
##plot F_sel-to-antisel binned in nJets for all ST bins
#ratio_nj={}
#for htb in htreg:
#  ratio_nj[htb]={}
#  first = True
#  canv4 = ROOT.TCanvas('canv','canv',600,600)
#  #canv.SetLogy()
#  l3 = ROOT.TLegend(0.65,0.80,0.95,0.95)
#  l3.SetFillColor(0)
#  l3.SetBorderSize(1)
#  l3.SetShadowColor(ROOT.kWhite)
#  text = ROOT.TLatex()
#  text.SetNDC()
#  text.SetTextSize(0.04)
#  text.SetTextAlign(11)
#  t3=ROOT.TLatex()
#  t3.SetNDC()
#  t3.SetTextSize(0.04)
#  t3.SetTextAlign(11)
#  for i_stb, stb in enumerate(streg):
#    ratio_nj[htb][stb]={}
#    for btb in btreg:
#      ratio_nj[htb][stb][btb]=ROOT.TH1F('ratio_njHist','ratio_njHist',len(njreg),0,len(njreg))
#      ratio_nj[htb][stb][btb].SetLineColor(ROOT_colors[i_stb])
#      ratio_nj[htb][stb][btb].SetLineWidth(2)
#      for i_njb, njb in enumerate(njreg):
#        nQCDsel = bins[njb][stb][htb][btb]['nQCDSelected'] 
#        nQCDselVar = bins[njb][stb][htb][btb]['nQCDSelectedVar'] 
#        nQCDantisel = bins[njb][stb][htb][btb]['nAntiSelected'] 
#        nQCDantiselVar = bins[njb][stb][htb][btb]['nAntiSelectedVar'] 
##          print nQCDsel, nQCDantisel
#        if nQCDantisel>0:
#          F=nQCDsel/nQCDantisel
#          print 'F_sel-to-anti-sel('+str(stb)+','+str(njb)+','+str(htb)+'):',F
#          if F>0:
#            F_err= F*sqrt(nQCDselVar/nQCDsel**2+nQCDantiselVar/nQCDantisel**2)
#            ratio_nj[htb][stb][btb].SetBinContent(i_njb+1,F)
#            ratio_nj[htb][stb][btb].SetBinError(i_njb+1,F_err)
#            print 'F_sel-to-anti-sel Error('+str(stb)+','+str(njb)+','+str(htb)+'):',F_err
#        ratio_nj[htb][stb][btb].GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb))
#        ratio_nj[htb][stb][btb].GetYaxis().SetTitle('F_{sel-to-antisel}')
#        ratio_nj[htb][stb][btb].GetYaxis().SetRangeUser(0.0,1.0)
##        ratio_ht[stb][njb].GetXaxis().SetTitle('F_{sel-to-antisel}')
#      l3.AddEntry(ratio_nj[htb][stb][btb], varBinName(stb,'S_{T}'))
#      if first:
#        ratio_nj[htb][stb][btb].Draw()
#        first = False
#      else:
#        ratio_nj[htb][stb][btb].Draw('same') 
#      l3.Draw()
#      t3.DrawLatex(0.2,0.85,varBinName(htb,'H_{T}'))
#      text.DrawLatex(0.15,.96,"CMS Simulation")
#      text.DrawLatex(0.65,0.96,"L="+str(targetLumi/1000)+" fb^{-1} (13 TeV)")
#      canv4.Print(wwwDir+presel+'Fsa_nj_'+nameAndCut(None, htb, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
#      canv4.Print(wwwDir+presel+'Fsa_nj_'+nameAndCut(None, htb, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
#      canv4.Print(wwwDir+presel+'Fsa_nj_'+nameAndCut(None, htb, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')


