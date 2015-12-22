## use this file to define all necessary samples, variables etc needed for the entire prediction process

import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.helpers import getChain

#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT500ST250_postProcessed_btagWeight import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT500ST250_postProcessed_fromArthur import *
from Workspace.RA4Analysis.cmgTuples_Data25ns_miniAODv2_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed_btag import *

from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *

testRun = False

## b-tagging and other variables
dPhiStr = 'deltaPhi_Wl'
bjreg = (0,0)
wjetsSB = (3,4)

nBTagVar = 'nBJetMediumCSV30'
useBTagWeights = False #True for weighted fake data, false for data
btagWeightSuffix = '_SF'
templateWeights = True
templateWeightSuffix = '_SF'

QCDup = False
QCDdown = False
nameSuffix = ''
if QCDup: nameSuffix += '_QCDup'
if QCDdown: nameSuffix += '_QCDdown'

## samples
isData = True
unblinded = False
validation = False

cWJets      = getChain(WJetsHTToLNu_25ns,histname='')
cTTJets     = getChain(TTJets_combined,histname='')
cDY         = getChain(DY_25ns,histname='')
csingleTop  = getChain(singleTop_25ns,histname='')
cTTV        = getChain(TTV_25ns,histname='')
cRest       = getChain([singleTop_25ns, DY_25ns, TTV_25ns],histname='')#no QCD
cBkg        = getChain([WJetsHTToLNu_25ns, TTJets_combined, singleTop_25ns, DY_25ns, TTV_25ns], histname='')#no QCD

if isData:
  cData = getChain([single_mu_Run2015D, single_ele_Run2015D], histname='')
else:
  cData = getChain([WJetsHTToLNu_25ns, TTJets_combined, singleTop_25ns, DY_25ns, TTV_25ns], histname='')


## signal region definition
#signalRegions = validationRegionAll
signalRegions = signalRegion3fb


## weight calculations
lumi = 2.1
templateLumi = 2.1 # lumi that was used when template was created - if defined wrong, fixed rest backgrounds will be wrong
sampleLumi = 3.
debugReweighting = False

## QCD estimation
useQCDestimation = True
#QCDpickle = '/data/dhandl/results2015/QCDEstimation/20151216_QCDestimation_extendedClosureTest3to4j_2p1fb_pkl'
#QCDpickle = '/data/dhandl/results2015/QCDEstimation/20151216_QCDestimation_closureTest4to5j_2p1fb_pkl'
QCDpickle = '/data/dhandl/results2015/QCDEstimation/20151216_QCDestimation_MC2p1fb_pkl'
if isData or useQCDestimation: QCDestimate = pickle.load(file(QCDpickle))
else: QCDestimate=False


## Directories for plots, results and templates
if isData:
  templateName   = 'SFtemplates_fullSR_lep_data'
  predictionName = templateName
else:
  templateName   = 'SFtemplates_fullSR_lep_MC' + nameSuffix
  predictionName = templateName+btagWeightSuffix + nameSuffix
printDir    = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Spring15/25ns/templateFit_'+predictionName+'_'+str(lumi)+'/'
pickleDir   = '/data/'+username+'/Results2015/Prediction_'+predictionName+'_'+str(lumi)+'/'
templateDir = '/data/'+username+'/Results2015/btagTemplates_'+templateName+'_'+str(templateLumi)+'/'
prefix = 'singleLeptonic_Spring15_'


## Preselection cut
triggers = "(HLT_EleHT350||HLT_MuHT350)"
filters = "Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_CSCTightHaloFilter && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter"
presel = "((!isData&&singleLeptonic)||(isData&&"+triggers+"&&((muonDataSet&&singleMuonic)||(eleDataSet&&singleElectronic))&&"+filters+"))"
presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>2 && htJet30j>500"

singleMu_presel = "((!isData&&singleMuonic)||(isData&&"+triggers+"&&(muonDataSet&&singleMuonic)&&"+filters+"))"
singleMu_presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>2 && htJet30j>500"

#presel = singleMu_presel

## corrections
createFits = True
fitDir = '/data/'+username+'/Results2015/correctionFit_validationAll_data/'


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
