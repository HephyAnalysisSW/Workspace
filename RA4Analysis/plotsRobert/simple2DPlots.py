import ROOT
from array import array
from math import *
import os, copy, sys

ROOT.TH1F().SetDefaultSumw2()
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/useNiceColorPalette.C+")
ROOT.useNiceColorPalette(255)
ROOT.gStyle.SetPadLeftMargin(0.18)
ROOT.gStyle.SetPadRightMargin(0.15)

from Workspace.HEPHYPythonTools.helpers import getObjFromFile
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2 import *
mode = 'hard'

subdir = "/pngCMG2/"+mode+'/'

prefix = mode+'_mu_ht600-6j-1b-diLepVeto-met200'
presel="met>200&&singleMuonic&&nLooseSoftLeptons==0&&nTightHardLeptons==1&&nLooseHardLeptons==1"\
      +"&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCMVA>0.732)>=1"\
      +"&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=6"\
      +"&&Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>=600"

#      +"&&Sum$(Jet_pt>80&&abs(Jet_eta)<2.4&&Jet_id)>=2"\
#      +"&&Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))<1000"\

from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks
#from Workspace.RA4Analysis.helpers import *

samples=[ttJets, SMS_T1tttt_2J_mGl1500_mLSP100]#, SMS_T1tttt_2J_mGl1200_mLSP800, SMS_T5qqqqWW_Gl1200_Chi1000_LSP800, SMS_T5qqqqWW_Gl1500_Chi800_LSP100, WJetsHTToLNu]
samples = [s['hard'] for s in samples]
for s in samples:
  s['chain']=getChain(s,histname='')

var = {'dPhi':'acos((leptonPt + met*cos(leptonPhi - metPhi))/sqrt(leptonPt**2 + met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))',\
       'mT':  'sqrt(2.*leptonPt*met*(1.-cos(metPhi-leptonPhi)))',
       'mT2W': 'mt2w'}

aName = {'dPhi':'#Delta#Phi(W,l)', 'mT':"m_{T} [GeV]", "mT2W":"m_{T2}^{W} [GeV]"}
binning = {'dPhi':[50,0,pi], 'mT':[55,0,550], 'mT2W':[49,0,490]}

c1=ROOT.TCanvas()
stuff=[]
for s in samples:
  for varx,vary in [['mT', 'mT2W']]:#, ['mT', 'dPhi'], ['dPhi', 'mT2W']]:
    h=ROOT.TH2F('h','',*(binning[varx]+binning[vary]))
    s['chain'].Draw(var[vary]+":"+var[varx]+">>h","weight*("+presel+")",'goff')
    c1.SetLogz()
    h.Draw('COLZ')
    h.GetXaxis().SetTitle(aName[varx])
    h.GetYaxis().SetTitle(aName[vary])
    h.GetXaxis().SetLabelSize(0.038)
    h.GetYaxis().SetLabelSize(0.038)
    h.GetXaxis().SetRangeUser(0,550)
    h.GetYaxis().SetRangeUser(80,490)
    l1_1 = ROOT.TLine(120,200-1, 550,200-1) #H
    l2_1 = ROOT.TLine(120,80,120, 200-1) #V bottom right 
    l1_2 = ROOT.TLine(120,200+1,120,490) #top right
    l2_2 = ROOT.TLine(120,200+1,550, 200+1) 
    l3_2 = ROOT.TLine(120-3,80,120-3, 490) 
    l1_1.SetLineWidth(3)
    l2_1.SetLineWidth(3)
    l1_2.SetLineWidth(3)
    l2_2.SetLineWidth(3)
    l3_2.SetLineWidth(3)
    l1_1.SetLineColor(ROOT.kGreen)
    l2_1.SetLineColor(ROOT.kGreen)
    l1_2.SetLineColor(ROOT.kRed)
    l2_2.SetLineColor(ROOT.kRed)
    l3_2.SetLineColor(ROOT.kBlue)
    l1_1.Draw()
    l2_1.Draw()
    l1_2.Draw()
    l2_2.Draw()
    l3_2.Draw()
    tl = ROOT.TLatex()
    tl.SetTextSize(0.033)
    l1 = ROOT.TLine(200,360,260,360) #H
    l2 = ROOT.TLine(200,380,260,380) #V bottom right 
    l3 = ROOT.TLine(200,400,260,400) #V bottom right 
    l1.SetLineColor(ROOT.kRed)
    l2.SetLineColor(ROOT.kGreen)
    l3.SetLineColor(ROOT.kBlue)
    l1.SetLineWidth(3)
    l2.SetLineWidth(3)
    l3.SetLineWidth(3)
    tb=ROOT.TBox(195,350,510,430)
    tb.SetFillColor(ROOT.kWhite)
    tb.Draw()
    stuff.append(tb)
    l1.Draw()
    l2.Draw()
    l3.Draw()
    stuff.append(l1)
    stuff.append(l2)
    stuff.append(l3)
    if s['name'].count("T1tttt"):
      tl.DrawLatex(200, 420-5, "relative fractions (13 TeV)") 
      tl.DrawLatex(270, 400-5, "24.7%")
      tl.DrawLatex(270, 380-5, "30.0%") 
      tl.DrawLatex(270, 360-5, "45.3%") 
    else:
      tl.DrawLatex(200, 420-5, "relative fractions (13 TeV)") 
      tl.DrawLatex(270, 400-5, "71.9%")
      tl.DrawLatex(270, 380-5, "21.8%") 
      tl.DrawLatex(270, 360-5, "6.1%") 

    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/'+subdir+'/'+prefix+'_'+'_vs_'.join([varx,vary])+'_'+s['name']+'.png')
    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/'+subdir+'/'+prefix+'_'+'_vs_'.join([varx,vary])+'_'+s['name']+'.root')
    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/'+subdir+'/'+prefix+'_'+'_vs_'.join([varx,vary])+'_'+s['name']+'.pdf')
    del h



