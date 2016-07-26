## use this file to define all necessary samples, variables etc needed for the entire prediction process

import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.helpers import getChain

from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Data25ns_Promtv2_postprocessed import *

from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *

testRun = False

## b-tagging and other variables
dPhiStr = 'deltaPhi_Wl'
bjreg = (0,0)

nBTagVar              = 'nBJetMediumCSV30'
useBTagWeights        = True
btagWeightSuffix      = '_SF'
templateWeights       = True
templateWeightSuffix  = '_SF'

QCDup       = False
QCDdown     = False
nameSuffix  = ''
if QCDup: nameSuffix += '_QCDup'
if QCDdown: nameSuffix += '_QCDdown'

## samples
isData              = False
unblinded           = True
validation          = True
isCentralPrediction = True
if isData:
  isCentralPrediction = False #should be false for data, otherwise kappa is measured in data!

loadTemplate = True

wjetsSB = (3,4)
if validation: wjetsSB = (3,3)

cWJets      = getChain(WJetsHTToLNu,histname='')
cTTJets     = getChain(TTJets_Comb,histname='')
cDY         = getChain(DY_HT,histname='')
csingleTop  = getChain(singleTop_lep,histname='')
cTTV        = getChain(TTV,histname='')
cRest       = getChain([singleTop_lep, DY_HT, TTV],histname='')#no QCD
cBkg        = getChain([WJetsHTToLNu, TTJets_Comb, singleTop_lep, DY_HT, TTV], histname='')#no QCD
cQCD        = getChain(QCDHT,histname='')


## QCD estimation
useQCDestimation = False
if not isData and useQCDestimation:
  QCDpickle = '/data/dspitzbart/Results2016/QCDEstimation/20160714_QCDestimation_2016SR_MC7p62fb_pkl'
if isData:
  QCDpickle  = '/data/dspitzbart/Results2016/QCDEstimation/20160714_QCDestimation_2016SR_data7p62fb_pkl'
if isData and validation:
  QCDpickle  = '/data/dspitzbart/Results2016/QCDEstimation/20160718_QCDestimation_2016val_v2_data7p62fb_pkl'

if isData or useQCDestimation: QCDestimate = pickle.load(file(QCDpickle))
else: QCDestimate=False

if isData:
  cData = getChain([single_mu_Run2016B, single_ele_Run2016B, single_mu_Run2016C, single_ele_Run2016C], histname='')
elif not isData and useQCDestimation:
  cData = getChain([WJetsHTToLNu, TTJets_Comb, singleTop_lep, DY_HT, TTV, QCDHT], histname='')
else:
  cData = getChain([WJetsHTToLNu, TTJets_Comb, singleTop_lep, DY_HT, TTV], histname='')


## signal region definition
if validation:
  signalRegions = validation2016
  regStr = 'validation_4j_altWSB'
else:
  signalRegions = signalRegions2016
  regStr = 'SR2016_v2'

## weight calculations
lumi = 12.9
templateLumi = 12.9 # lumi that was used when template was created - if defined wrong, fixed rest backgrounds will be wrong
sampleLumi = 3.
printlumi = '12.9'
debugReweighting = False

year = '2016'

if year=='2016':
  lumistr = str(lumi).replace('.','p')
  templateLumistr = str(templateLumi).replace('.','p')
else:
  lumistr = str(lumi)#.replace('.','p')
  templateLumistr = str(templateLumi)#.replace('.','p')

## Template Bootstrap error dictionary
templateBootstrap = True
if validation:
  templateBootstrap = False
templateBootstrapDir = '/data/dspitzbart/bootstrap2016/bootstrap_unc_pkl'
if templateBootstrap: templateBootstrap = pickle.load(file(templateBootstrapDir))

## Directories for plots, results and templates
if isData:
  templateName   = 'Spring16_templates_'+regStr+'_lep_data'
  predictionName = templateName + nameSuffix
else:
  templateName   = 'Spring16_templates_'+regStr+'_lep_MC'
  predictionName = templateName+btagWeightSuffix + nameSuffix
printDir    = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Spring15/25ns/templateFit_'+predictionName+'_'+lumistr+'/'
pickleDir   = '/data/'+username+'/Results'+year+'/Prediction_'+predictionName+'_'+lumistr+'/'
templateDir = '/data/'+username+'/Results'+year+'/btagTemplates_'+templateName+'_'+templateLumistr+'/'
prefix = 'singleLeptonic_Spring16_'

if validation:
  kappa_dict_dir = '/data/dspitzbart/Results'+year+'/Prediction_Spring16_templates_validation_4j_lep_MC_SF_7p7/singleLeptonic_Spring16__estimationResults_pkl_kappa_corrected'
else:
  kappa_dict_dir = '/data/dspitzbart/Results'+year+'/Prediction_Spring16_templates_SR2016_v2_lep_MC_SF_7p7/singleLeptonic_Spring16__estimationResults_pkl_kappa_corrected'

## Preselection cut
triggers = "((HLT_EleHT350||HLT_EleHT400||HLT_Ele105)||(HLT_MuHT350||HLT_MuHT400))"
filters = "(Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_goodVertices && Flag_eeBadScFilter &&  Flag_globalTightHalo2016Filter && Flag_badChargedHadronFilter && Flag_badMuonFilter)"
presel = "((!isData&&singleLeptonic)||(isData&&"+triggers+"&&((muonDataSet&&singleMuonic)||(eleDataSet&&singleElectronic))&&"+filters+"))"
presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>1 && htJet30j>500"

singleMu_presel = "((!isData&&singleMuonic)||(isData&&"+triggers+"&&(muonDataSet&&singleMuonic)&&"+filters+"))"
singleMu_presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>1 && htJet30j>500"

singleEle_presel = "((!isData&&singleElectronic)||(isData&&"+triggers+"&&(eleDataSet&&singleElectronic)&&"+filters+"))"
singleEle_presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>1 && htJet30j>500"

presel_MC = "singleLeptonic" + "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>1 && htJet30j>500 && Flag_badChargedHadronFilter && Flag_badMuonFilter"

if not isData: presel = presel_MC

#presel = singleMu_presel

## weights for MC
muTriggerEff = '0.926'
eleTriggerErr = '0.963'
MCweight = 'TopPtWeight*puReweight_true_max4*(singleMuonic*'+muTriggerEff+' + singleElectronic*'+eleTriggerErr+')*lepton_muSF_HIP*lepton_muSF_mediumID*lepton_muSF_miniIso02*lepton_muSF_sip3d*lepton_eleSF_cutbasedID*lepton_eleSF_miniIso01*lepton_eleSF_gsf'

## corrections
createFits = True # turn off if you already did one
if not isCentralPrediction:
  createFits = False
fitDir = '/data/'+username+'/Results'+year+'/correctionFit_'+regStr+'_MC_'+lumistr+nameSuffix+'/'
#fitDir = '/data/'+username+'/Results'+year+'/correctionFit_SR2016_v1_MC_test/'
fitPrintDir = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results'+year+'/25ns/RcsFit_'+predictionName+'_'+lumistr+'_test/'

## do stuff for test runs
if testRun:
  signalRegions = oneRegion
  predictionName = 'testRun'
  printDir    = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results'+year+'/25ns/templateFit_'+predictionName+'_'+lumistr+'/'
  pickleDir   = '/data/'+username+'/Results'+year+'/Prediction_'+predictionName+'_'+lumistr+'/'
  templateDir = '/data/'+username+'/Results'+year+'/btagTemplates_'+predictionName+'_'+templateLumistr+'/'



## create directories that are defined but do not yet exist
if not os.path.exists(fitDir):
  os.makedirs(fitDir)
if not os.path.exists(pickleDir):
  os.makedirs(pickleDir)
if not os.path.exists(printDir):
  os.makedirs(printDir)
if not os.path.exists(templateDir):
  os.makedirs(templateDir)
if not os.path.exists(fitPrintDir):
  os.makedirs(fitPrintDir)
