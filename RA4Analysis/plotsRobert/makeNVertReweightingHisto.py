import ROOT
from array import array
from math import *
import os, copy, sys

ROOT.TH1F().SetDefaultSumw2()

from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain
from Workspace.RA4Analysis.cmgTuples_Data50ns_1l_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Spring15_50ns_postProcessed import * 

maxN=1

data = getChain([SingleMuon_Run2015B_PromptReco, SingleElectron_Run2015B_PromptReco],histname='')
mc   = getChain([TTJets_50ns, WJetsToLNu_50ns, DYHT_50ns, singleTop_50ns],histname='',maxN=maxN)

presel=""\
  +"((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0))>=1)"\
  +"&&((Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4)))>400)"\
  +"&&(Sum$(((LepGood_pt[0]+met_pt)>200))>=1)"\

dataCut = ""\
  +"(Flag_HBHENoiseFilterMinZeroPatched&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_eeBadScFilter)"\
  +"&&(HLT_MuHT350MET70 || HLT_Mu50NoIso)"\

data_nVert = getPlotFromChain(data, 'nVert', [50,0,50], cutString=dataCut+"&&"+presel, weight='weight')
mc_nVert = getPlotFromChain(mc, 'nVert', [50,0,50], cutString=dataCut+"&&"+presel, weight='weight')

data_nVert
