import ROOT
import pickle
import copy, os, sys
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.TH1F().SetDefaultSumw2()
ROOT.setTDRStyle()
ROOT.gStyle.SetMarkerStyle(1)
ROOT.gStyle.SetOptTitle(0)

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *

from btagEfficiency import *

from Workspace.RA4Analysis.cmgTuples_Spring16_Moriond2017_MiniAODv2_postProcessed import *

cTT = getChain(TTJets_Comb, histname='')
cW = getChain(WJetsHTToLNu, histname='')

cSignal = ROOT.TChain("Events")
for mgl in allSignals[0].keys():
    for mneu in allSignals[0][mgl].keys():
        cSignal.Add(allSignals[0][mgl][mneu]['file'])

#presel = '((!isData&&singleLeptonic)||(isData&&((eleDataSet&&singleElectronic)||(muonDataSet&&singleMuonic))))&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&iso_Veto&&nJet30>=5&&(Jet_pt[1]>80)&&htJet30j>500&&st>250&&iso_Veto&&(Jet_pt[1]>80)'

presel = '(1)'

btags = [
        #{'name':'deepFlavour', 'var':'Jet_DFb',      'WP':0.6324},
        #{'name':'deepFlavourBBplusB', 'var':'(Jet_DFbb+Jet_DFb)',      'WP':0.6324},
        #{'name':'CSVv2'      , 'var':'Jet_btagCSV',  'WP':0.8484},
        {'name':'signal_v2_CSVv2'      , 'var':'Jet_btagCSV',  'WP':0.8484}
        ]

dataDir = '/afs/hephy.at/work/d/dspitzbart/gluinos/CMSSW_8_0_21/src/Workspace/RA4Analysis/cmgPostProcessing/data/'

for btag in btags:
  print
  print 'Working on b-tagging type %s with WP %f' %(btag['name'],btag['WP'])
  effs = {}
  bTagEffFile = dataDir+'Moriond17_v1_%s_%s.pkl'%(btag['name'],str(btag['WP']).replace('.','p'))
  #effs['TTJets']  = getBTagMCTruthEfficiencies(cTT, cut=presel, btagVar=btag['var'], btagWP=btag['WP'])
  #effs['WJets']   = getBTagMCTruthEfficiencies(cW, cut=presel, btagVar=btag['var'], btagWP=btag['WP'])
  effs['signal_inclusive'] = getBTagMCTruthEfficiencies(cSignal, cut=presel, btagVar=btag['var'], btagWP=btag['WP'])
  effs['none']    = getDummyEfficiencies()
  
  pickle.dump(effs, file(bTagEffFile,'w'))


