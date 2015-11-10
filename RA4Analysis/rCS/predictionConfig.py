## use this file to define all necessary samples, variables etc needed for the entire prediction process

import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.helpers import getChain

from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT500ST250_postProcessed_btagWeight import *
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT500ST250_postProcessed_fromArthur import *

from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *

testRun = True

## b-tagging and other variables
dPhiStr = 'deltaPhi_Wl'
bjreg = (0,0)
nBTagVar = 'nBJetMediumCSV30'
useBTagWeights = False #True for weighted fake data, false for data
btagWeightSuffix = ''
templateWeights = True
templateWeightSuffix = '_SF'


## samples
isData = False

cWJets      = getChain(WJetsHT_25ns_btagweight,histname='')
cTTJets     = getChain(TTJets_HTLO_25ns_btagweight,histname='')
cDY         = getChain(DY_25ns,histname='')
csingleTop  = getChain(singleTop_25ns,histname='')
cTTV        = getChain(TTV_25ns,histname='')
cRest       = getChain([singleTop_25ns, DY_25ns, TTV_25ns],histname='')#no QCD
cBkg        = getChain([WJetsHT_25ns_btagweight, TTJets_HTLO_25ns_btagweight, singleTop_25ns, DY_25ns, TTV_25ns], histname='')#no QCD

if isData:
  cData = getChain([SingleMuon_Run2015D, SingleElectron_Run2015D], histname='')
else:
  cData = getChain([WJetsHT_25ns_btagweight, TTJets_HTLO_25ns_btagweight, singleTop_25ns, DY_25ns, TTV_25ns], histname='')


## signal region definition
signalRegions = signalRegion3fb


## weight calculations
lumi = 1.26
templateLumi = 1.26 # lumi that was used when template was created - if defined wrong, fixed rest backgrounds will be wrong
sampleLumi = 3.
debugReweighting = False

## QCD estimation
QCDpickle = '/data/dhandl/results2015/QCDEstimation/20151106_QCDestimation_pkl'
QCDestimate = pickle.load(file(QCDpickle))
QCDestimate=False


## Directories for plots, results and templates
predictionName = 'data_newSR_lep_SFtemplates'
templateName   = 'SFtemplates_for_data_newSR_lep'
printDir    = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Spring15/25ns/templateFit_'+predictionName+'_'+str(lumi)+'/'
pickleDir   = '/data/'+username+'/Results2015/Prediction_'+predictionName+'_'+str(lumi)+'/'
templateDir = '/data/'+username+'/Results2015/btagTemplates_'+templateName+'_'+str(templateLumi)+'/'
prefix = 'singleLeptonic_Spring15_'


## Preselection cut
triggers = "(HLT_EleHT350||HLT_MuHT350)"
filters = "Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_CSCTightHaloFilter && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter"
presel = "((!isData&&singleLeptonic)||(isData&&"+triggers+"&&((muonDataSet&&singleMuonic)||(eleDataSet&&singleElectronic))&&"+filters+"))"
presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>2 && htJet30j>500"


## corrections
createFits = True
fitDir = '/data/'+username+'/Results2015/correctionFit_btagKappa_data_fullSR/'


## do stuff for test runs
if testRun:
  signalRegions = smallRegion
  predictionName = 'testRun'
  printDir    = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Spring15/25ns/templateFit_'+predictionName+'_'+str(lumi)+'/'
  pickleDir   = '/data/'+username+'/Results2015/Prediction_'+predictionName+'_'+str(lumi)+'/'
  templateDir = '/data/'+username+'/Results2015/btagTemplates_'+predictionName+'_'+str(templateLumi)+'/'


## create directories that are defined but do not yet exist
if not os.path.exists(fitDir):
  os.makedirs(fitDir)
if not os.path.exists(pickleDir):
  os.makedirs(pickleDir)
if not os.path.exists(printDir):
  os.makedirs(printDir)
if not os.path.exists(templateDir):
  os.makedirs(templateDir)
