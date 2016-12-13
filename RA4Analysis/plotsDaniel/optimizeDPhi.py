import ROOT
import os, sys, copy

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import getVarValue, getChain, deltaPhi

from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_postProcessed import *


from Workspace.RA4Analysis.helpers import *
from rCShelpers import *


binning=[30,0,1500]

prepresel = '!isData&&singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&st>250&&nJet30>2&&htJet30j>500'

bVar = 'nBJetMediumCSV30'

varstring='deltaPhi_Wl'
vartex = '#Delta#Phi(W,l)'

nJetReg=[(5,5),(6,7),(8,-1)]
ltReg=[(250,350),(350,450),(450,600),(600,-1)]
htReg=[(500,750),(750,1000),(1000,1250),(1250,-1)]

targetLumi = 40. #fb^-1
sampleLumi = 3. #fb^-1
threshold = 1.


scaleFactor = targetLumi/sampleLumi

cBkg = getChain([TTJets_Comb,WJetsHTToLNu,DY_HT,singleTop_lep,TTV],histname='')

signal1 = getChain(allSignals[0][1400][800], histname='')
signal2 = getChain(allSignals[0][1600][900], histname='')
signal3 = getChain(allSignals[0][1800][100], histname='')

bkgH  = ROOT.TH1F('bkgH','',32,0,3.2)

sig1H = ROOT.TH1F('sig1H','',32,0,3.2)
sig2H = ROOT.TH1F('sig2H','',32,0,3.2)
sig3H = ROOT.TH1F('sig3H','',32,0,3.2)
FOM1H = ROOT.TH1F('FOM1H','(1.4,0.8)',32,0,3.2)
FOM2H = ROOT.TH1F('FOM2H','(1.6,0.9)',32,0,3.2)
FOM3H = ROOT.TH1F('FOM3H','(1.8,0.1)',32,0,3.2)

FOM1H.SetLineColor(ROOT.kOrange)
FOM2H.SetLineColor(ROOT.kBlue)
FOM3H.SetLineColor(ROOT.kGreen+1)

FOMS = [FOM1H,FOM2H,FOM3H]


for f in FOMS:
  f.SetLineWidth(2)
  f.SetMarkerSize(0)
#  leg.AddEntry(f)

muTriggerEff = '0.926'
eleTriggerEff = '0.963'
weight = 'weight*TopPtWeight*puReweight_true_max4*(singleMuonic*'+muTriggerEff+' + singleElectronic*'+eleTriggerEff+')*leptonSF'

signalWeight = 'weight*puReweight_true_max4*(singleMuonic*'+muTriggerEff+'+singleElectronic*'+eleTriggerEff+')*reweightLeptonFastSimSF*lepton_muSF_HIP*lepton_muSF_mediumID*lepton_muSF_miniIso02*lepton_muSF_sip3d*lepton_eleSF_cutbasedID*lepton_eleSF_miniIso01*lepton_eleSF_gsf'

htb = (500,-1)
njb = (5,-1)

for ltb in ltReg:
  can = ROOT.TCanvas('can','can',600,600)
  print
  print ltb
  name, cut = nameAndCut(ltb, htb, njb, btb=(0,0), presel=prepresel, btagVar=bVar)
  cBkg.Draw(varstring+'>>bkgH','('+cut+')*'+weight)
  signal1.Draw(varstring+'>>sig1H','('+cut+')*'+signalWeight)
  signal2.Draw(varstring+'>>sig2H','('+cut+')*'+signalWeight)
  signal3.Draw(varstring+'>>sig3H','('+cut+')*'+signalWeight)
  
  for i in range(1,32):
    bkg = bkgH.Integral(i,32)*scaleFactor
    if bkg>0:
      FOM1 = sig1H.Integral(i,32)*scaleFactor/sqrt(bkg)
      FOM2 = sig2H.Integral(i,32)*scaleFactor/sqrt(bkg)
      FOM3 = sig3H.Integral(i,32)*scaleFactor/sqrt(bkg)
    else:
      FOM1 = FOM2 = FOM3 = 0.
    print round(i/10.,2), round(FOM3,3)
    FOM1H.SetBinContent(i,FOM1)
    FOM2H.SetBinContent(i,FOM2)
    FOM3H.SetBinContent(i,FOM3)

  first = True
  leg = ROOT.TLegend(0.5,0.83,0.98,0.95)
  leg.SetFillColor(ROOT.kWhite)
  leg.SetShadowColor(ROOT.kWhite)
  leg.SetBorderSize(1)
  leg.SetTextSize(0.035)

  for f in FOMS:
    if first:
      opt = 'hist'
      first = False
    else: opt = 'hist same'
    f.Draw(opt)
    leg.AddEntry(f,f.GetTitle()+' max. at: '+str(f.GetMaximumBin()/10.))
  leg.Draw()
  ltb_str = str(ltb)
  ltb_str = ltb_str.replace('(','')
  ltb_str = ltb_str.replace(')','')
  ltb_str = ltb_str.replace(',','to')
  ltb_str = 'lt_'+ltb_str


  can.Print('/afs/hephy.at/user/d/dspitzbart/www/Spring16/deltaPhiOpt/'+ltb_str+'.png')
