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

prefix = mode+'_mu_ht750-st200-6j-2j80-2b-diLepVeto'
presel="singleMuonic&&nLooseSoftLeptons==0&&nTightHardLeptons==1&&nLooseHardLeptons==1&&st>200"\
      +"&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCMVA>0.732)>=2"\
      +"&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=6"\
      +"&&Sum$(Jet_pt>80&&abs(Jet_eta)<2.4&&Jet_id)>=2"\
      +"&&Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>=750"\
#      +"&&Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))<1000"\

from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks
#from Workspace.RA4Analysis.helpers import *

samples=[ttJets, WJetsHTToLNu, 
         SMS_T1tttt_2J_mGl1200_mLSP800, SMS_T1tttt_2J_mGl1500_mLSP100, SMS_T5qqqqWW_Gl1200_Chi1000_LSP800, SMS_T5qqqqWW_Gl1500_Chi800_LSP100]
samples = [s['hard'] for s in samples]
for s in samples:
  s['chain']=getChain(s,histname='')

var = {'dPhi':'acos((leptonPt + met*cos(leptonPhi - metPhi))/sqrt(leptonPt**2 + met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))',\
       'mT':  'sqrt(2.*leptonPt*met*(1.-cos(metPhi-leptonPhi)))',
       'mT2W': 'mt2w'}

aName = {'dPhi':'#Delta#Phi(W,l)', 'mT':"m_{T} (GeV)", "mT2W":"m_{T2}^{W} (GeV)"}
binning = {'dPhi':[100,0,pi], 'mT':[100,0,500], 'mT2W':[100,0,500]}

c1=ROOT.TCanvas()
for s in samples:
  for varx,vary in [['mT', 'mT2W'], ['mT', 'dPhi'], ['dPhi', 'mT2W']]:
    h=ROOT.TH2F('h','',*(binning[varx]+binning[vary]))
    s['chain'].Draw(var[vary]+":"+var[varx]+">>h",presel,'goff')
    c1.SetLogz()
    h.Draw('COLZ')
    h.GetXaxis().SetTitle(aName[varx])
    h.GetYaxis().SetTitle(aName[vary])
    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/'+subdir+'/'+prefix+'_'+'_vs_'.join([varx,vary])+'_'+s['name']+'.png')
    del h



