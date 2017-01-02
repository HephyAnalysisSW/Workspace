## use this file to define all necessary samples, variables etc needed for the entire prediction process

import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.helpers import getChain

from Workspace.RA4Analysis.cmgTuples_Data25ns_Moriond2017_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Spring16_Moriond2017_MiniAODv2_postProcessed import *

from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *

testRun = False

## b-tagging and other variables
dPhiStr = 'deltaPhi_Wl'
bjreg = (0,0)

nBTagVar              = 'nBJetMediumCSV30'
useBTagWeights        = False
btagWeightSuffix      = '_SF'
templateWeights       = False
templateWeightSuffix  = '_SF'

QCDup       = False
QCDdown     = False
nameSuffix  = ''
if QCDup: nameSuffix += '_QCDup'
if QCDdown: nameSuffix += '_QCDdown'

## samples
isData              = True
unblinded           = False
validation          = False
isCentralPrediction = True
if isData:
  isCentralPrediction = False #should be false for data, otherwise kappa is measured in data!

loadTemplate = True

wjetsSB = (3,4)
if validation: wjetsSB = (3,3)

cWJets      = getChain([WJetsHTToLNu,diBoson_1L1Nu2Q],histname='') #FIXME: For now add this to WJets
cTTJets     = getChain(TTJets_Comb,histname='')
cDY         = getChain(DY_HT,histname='')
csingleTop  = getChain(singleTop_lep,histname='')
cTTV        = getChain(TTV,histname='')
cDiBoson    = getChain(diBoson, histname='')
cDiboson_rest = getChain(diBoson_rest,histname='')
cDiboson_1l = getChain(diBoson_1L1Nu2Q,histname='')
cRest       = getChain([singleTop_lep, DY_HT, TTV,diBoson_rest],histname='')#no QCD
cBkg        = getChain([WJetsHTToLNu, TTJets_Comb, singleTop_lep, DY_HT, TTV], histname='')#no QCD
cQCD        = getChain(QCDHT,histname='')


## QCD estimation
useQCDestimation = False
if not isData and useQCDestimation:
  QCDpickle = '/data/dspitzbart/Results2016/QCDEstimation/20160714_QCDestimation_2016SR_MC7p62fb_pkl'
if isData:
  QCDpickle  = '/afs/hephy.at/data/dspitzbart01/RA4/Moriond2017/QCDEstimation/20161220_QCDestimation_Moriond17SR_v7_data36p5fb_orig'
if isData and validation:
  QCDpickle  = '/data/dspitzbart/Results2016/QCDEstimation/20160725_QCDestimation_2016val_v2_data12p9fb_100p'

if isData or useQCDestimation: QCDestimate = pickle.load(file(QCDpickle))
else: QCDestimate=False

if isData:
  cData = getChain([single_mu, single_ele, met], histname='')
elif not isData and useQCDestimation:
  cData = getChain([WJetsHTToLNu, TTJets_Comb, singleTop_lep, DY_HT, TTV, QCDHT], histname='')
else:
  cData = getChain([WJetsHTToLNu, TTJets_Comb, singleTop_lep, DY_HT, TTV], histname='')


## signal region definition
if validation:
  signalRegions = validation2016
  regStr = 'validation_4j_altWSB'
else:
  #signalRegions = signalRegions2016
  ##signalRegions = signalRegions_Moriond2017
  regStr = 'SR_Moriond2017_v3'
  #regStr = 'SR2016_v2'

## weight calculations
lumi = 36.5
templateLumi = 36.5 # lumi that was used when template was created - if defined wrong, fixed rest backgrounds will be wrong
sampleLumi = 3.
printlumi = '36'
debugReweighting = False

year = '2017'

if year=='2017':
  lumistr = str(lumi).replace('.','p')
  templateLumistr = str(templateLumi).replace('.','p')
else:
  lumistr = str(lumi)#.replace('.','p')
  templateLumistr = str(templateLumi)#.replace('.','p')

## Template Bootstrap error dictionary
templateBootstrap = False   ###FIXME
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
pickleDir   = '/afs/hephy.at/data/'+username+'01/Results'+year+'/Prediction_'+predictionName+'_'+lumistr+'/'
templateDir = '/afs/hephy.at/data/'+username+'01/Results'+year+'/btagTemplates_'+templateName+'_'+templateLumistr+'/'
prefix = 'singleLeptonic_Spring16_'

if validation:
  kappa_dict_dir = '/data/dspitzbart/Results'+year+'/Prediction_Spring16_templates_validation_4j_altWSB_lep_MC_SF_12p9/singleLeptonic_Spring16__estimationResults_pkl_kappa_corrected'
else:
  kappa_dict_dir = '/afs/hephy.at/data/'+username+'01/Results'+year+'/Prediction_Spring16_templates_SR2016_postApp_v2_lep_MC_SF_12p9/singleLeptonic_Spring16__estimationResults_pkl_kappa_corrected'

## Preselection cut
trigger_or_ele = "(HLT_Ele105||HLT_Ele115||HLT_Ele50PFJet165||HLT_IsoEle27T||HLT_EleHT400||HLT_EleHT350)"
trigger_or_mu = "(HLT_Mu50||HLT_IsoMu24||HLT_MuHT400||HLT_MuHT350)"
trigger_or_met = "(HLT_MET100MHT100||HLT_MET110MHT110||HLT_MET120MHT120)"
trigger_xor_ele = "((eleDataSet&&%s))"%(trigger_or_ele)
trigger_xor_mu = "((muonDataSet&&%s&&!(%s)))"%(trigger_or_mu,trigger_or_ele)
trigger_xor_met = "((METDataSet&&%s&&!(%s)&&!(%s)) )"%(trigger_or_met,trigger_or_ele,trigger_or_mu)
trigger_xor = "(%s||%s||%s)"%(trigger_xor_ele,trigger_xor_mu,trigger_xor_met)
triggers = trigger_xor
filters = "(Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_goodVertices && Flag_eeBadScFilter &&  Flag_globalTightHalo2016Filter && Flag_badChargedHadronFilter && Flag_badMuonFilter)"
presel = "((!isData&&singleLeptonic)||(isData&&"+triggers+"&&"+filters+"))"
presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>1 && htJet30j>500"

singleMu_presel = "((!isData&&singleMuonic)||(isData&&"+triggers+"&&"+filters+"))"
singleMu_presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>1 && htJet30j>500"

singleEle_presel = "((!isData&&singleElectronic)||(isData&&"+triggers+"&&"+filters+"))"
singleEle_presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>1 && htJet30j>500"

presel_MC = "singleLeptonic" + "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>1 && htJet30j>500 && Flag_badChargedHadronFilter && Flag_badMuonFilter"

if not isData: presel = presel_MC

#presel = singleMu_presel

## weights for MC
muTriggerEff = '0.926'
eleTriggerErr = '0.963'
ttJetsweight = '(weight_ISR_new*1.071)'  ### this is temperary change this 
MCweight = '(1)'

## corrections
createFits = True # turn off if you already did one
if not isCentralPrediction:
  createFits = False
fitDir = '/afs/hephy.at/data/'+username+'01'+'/Results'+year+'/correctionFit_'+regStr+'_MC_'+lumistr+nameSuffix+'/'
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
