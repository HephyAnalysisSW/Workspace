## use this file to define all necessary samples, variables etc needed for the entire prediction process

import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.helpers import getChain

from Workspace.RA4Analysis.cmgTuples_Data25ns_Moriond2017_reminiaod_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Summer16_Moriond2017_MiniAODv2_postProcessed import *

from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *

testRun = False

## b-tagging and other variables
dPhiStr = 'deltaPhi_Wl'
bjreg = (0,0)

nBTagVar              = 'nBJetMediumCSV30'
#nBTagVar              = "Sum$(Jet_pt>30&&abs(Jet_eta)<2.5&&(Jet_DFbb+Jet_DFb)>0.6324)"
useBTagWeights        = True
btagWeightSuffix      = '_SF'
templateWeights       = False
templateWeightSuffix  = '_SF'
useDLCorr = False
useDLCorr_constantUp = False
useDLCorr_slopeUp = False
correct_kappaTT = True #for dilep

QCDup       = False
QCDdown     = False
nameSuffix  = ''
if QCDup: nameSuffix += '_QCDup'
if QCDdown: nameSuffix += '_QCDdown'

## samples
isData              = True
unblinded           = True
unblid5fb           = False
validation          = False
aggrigated          = False 
isCentralPrediction = True
if isData:
  isCentralPrediction = False #should be false for data, otherwise kappa is measured in data!

loadTemplate = True

wjetsSB = (3,4)
ttjetsSB = (1,-1)
if validation: wjetsSB = (3,3)

cWJets      = getChain([WJetsHTToLNu,diBoson_1L1Nu2Q],histname='') #FIXME: For now add this to WJets
cTTJets     = getChain(TTJets_Comb,histname='')
cDY         = getChain(DY_HT,histname='')
csingleTop  = getChain(singleTop_lep,histname='')
cTTV        = getChain(TTV,histname='')
cDiBoson    = getChain(diBoson, histname='')
cDiBoson_rest = getChain(diBoson_rest,histname='')
cDiBoson_1l = getChain(diBoson_1L1Nu2Q,histname='')
cRest       = getChain([singleTop_lep, DY_HT, TTV,diBoson_rest],histname='')#no QCD
cBkg        = getChain([WJetsHTToLNu, TTJets_Comb, singleTop_lep, DY_HT, TTV,diBoson], histname='')#no QCD
cQCD        = getChain(QCDHT,histname='')

if correct_kappaTT:
  dilepCorr_dict_dir = '/afs/hephy.at/data/easilar01/Results2017/Prediction_Spring16_templates_SR_Moriond2017_Summer16_DLcorrected_lep_MC_SF_36p5/singleLeptonic_Spring16_iso_Veto_ISRforttJets_NEWttJetsSB_addDiBoson_withSystematics_pkl' 
  dilepCorr_dict = pickle.load(file(dilepCorr_dict_dir)) 

## QCD estimation
useQCDestimation = False
if not isData and useQCDestimation:
  QCDpickle = '/data/dspitzbart/Results2016/QCDEstimation/20160714_QCDestimation_2016SR_MC7p62fb_pkl'
if isData:
  QCDpickle  = '/afs/hephy.at/data/dspitzbart01/RA4/Moriond2017/QCDEstimation/20161220_QCDestimation_Moriond17SR_v7_data36p5fb_orig'
if isData and validation:
  QCDestimate=False
  #QCDpickle  = '/data/dspitzbart/Results2016/QCDEstimation/20160725_QCDestimation_2016val_v2_data12p9fb_100p'

if isData or useQCDestimation: 
  QCDestimate = pickle.load(file(QCDpickle))
  #QCDestimate=False
else: QCDestimate=False

if validation or aggrigated :
  useQCDestimation = False
  QCDestimate=False

if isData:
  if unblid5fb :
    cData = getChain([single_mu_unblind, single_ele_unblind, met_unblind], histname='')
  else: 
    print "will use data"
    cData = getChain([single_mu, single_ele, met], histname='')
elif not isData and useQCDestimation:
  cData = getChain([WJetsHTToLNu, TTJets_Comb, singleTop_lep, DY_HT, TTV, QCDHT], histname='')
else:
  cData = getChain([WJetsHTToLNu, TTJets_Comb, singleTop_lep, DY_HT, TTV], histname='')


## signal region definition
if validation:
  #signalRegions = validation2016
  regStr = 'validation_4j_Moriond2017'
if aggrigated:
  regStr = 'Aggr_Moriond2017' 
else:
  regStr = 'SR_Moriond2017_Summer16'

if useDLCorr : regStr = regStr+'_DLcorrected'
if useDLCorr_constantUp : regStr = regStr+'_DLconstantUp'
if useDLCorr_slopeUp : regStr = regStr+'_DLslopeUp'

signalRegion_dict =  {"Moriond":signalRegions_Moriond2017_onebyone,\
                      "ICHEP":signalRegions2016_onebyone,\
                      "Validation":validationRegion_Moriond_onebyone,\
                      "Aggr":aggregateRegions_Moriond2017_Test2_onebyone,\
                     }

## weight calculations
lumi = 36.
templateLumi = 36. # lumi that was used when template was created - if defined wrong, fixed rest backgrounds will be wrong
sampleLumi = 3.
printlumi = '36'
#lumi = 5.2
#templateLumi = 5.2 # lumi that was used when template was created - if defined wrong, fixed rest backgrounds will be wrong
#sampleLumi = 3.
#printlumi = '5'
debugReweighting = False

year = '2017'

if year=='2017':
  lumistr = str(lumi).replace('.','p')
  templateLumistr = str(templateLumi).replace('.','p')
else:
  lumistr = str(lumi)#.replace('.','p')
  templateLumistr = str(templateLumi)#.replace('.','p')

## Template Bootstrap error dictionary
templateBootstrap = True  ###FIXME
if validation:
  templateBootstrap = False
templateBootstrapDir = '/afs/hephy.at/data/dspitzbart01/RA4/Moriond2017/bootstrap/bootstrap_unc.pkl'
if templateBootstrap: templateBootstrap = pickle.load(file(templateBootstrapDir))

## Directories for plots, results and templates
if isData:
  templateName   = 'Spring16_templates_'+regStr+'_lep_data'
  predictionName = templateName + nameSuffix
  getKappaSuffix = '_lep_MC'
else:
  templateName   = 'Spring16_templates_'+regStr+'_lep_MC'
  predictionName = templateName+btagWeightSuffix + nameSuffix
printDir    = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results'+year+'/templateFit_'+predictionName+'_'+lumistr+'/'
pickleDir   = '/afs/hephy.at/data/'+username+'01/Results'+year+'/Prediction_'+predictionName+'_'+lumistr+'/'
templateDir = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results'+year+'/btagTemplates_'+templateName+'_'+templateLumistr+'/'
prefix = 'singleLeptonic_Spring16_iso_Veto_ISRforttJets_NEWttJetsSB_addDiBoson'

if validation:
  kappa_dict_dir = '/afs/hephy.at/data/'+username+'01/Results'+year+'/Prediction_Spring16_templates_'+regStr+'_lep_MC'+btagWeightSuffix+nameSuffix+'_'+lumistr+'/'
else:
  kappa_dict_dir = '/afs/hephy.at/data/'+username+'01/Results'+year+'/Prediction_Spring16_templates_'+regStr+'_lep_MC'+btagWeightSuffix+nameSuffix+'_'+lumistr+'/'

## Preselection cut
trigger_or_ele = "(HLT_Ele105||HLT_Ele115||HLT_Ele50PFJet165||HLT_IsoEle27T||HLT_EleHT400||HLT_EleHT350)"
trigger_or_mu = "(HLT_Mu50||HLT_IsoMu24||HLT_MuHT400||HLT_MuHT350)"
trigger_or_lep = "%s||%s"%(trigger_or_ele,trigger_or_mu)
trigger_or_met = "(HLT_MET100MHT100||HLT_MET110MHT110||HLT_MET120MHT120)"
trigger = "((%s||%s||%s))"%(trigger_or_ele,trigger_or_mu,trigger_or_met)
trigger = "(!isData||(isData&&%s))"%(trigger)
trigger_xor_ele = "((eleDataSet&&%s))"%(trigger_or_ele)
trigger_xor_mu = "((muonDataSet&&%s&&!(%s)))"%(trigger_or_mu,trigger_or_ele)
trigger_xor_met = "((METDataSet&&%s&&!(%s)&&!(%s)) )"%(trigger_or_met,trigger_or_ele,trigger_or_mu)
trigger_xor = "(%s||%s||%s)"%(trigger_xor_ele,trigger_xor_mu,trigger_xor_met)
trigger_xor = "(!isData||(isData&&%s))"%(trigger_xor)
triggers = "((%s)&&(%s))"%(trigger,trigger_xor)

filters = "(!isData&&(Flag_badChargedHadronFilter && Flag_badMuonFilter)||isData&&(Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_goodVertices && Flag_eeBadScFilter &&  Flag_globalTightHalo2016Filter && Flag_badChargedHadronFilter && Flag_badMuonFilter && Flag_badMuons && Flag_duplicateMuons ))"

presel = "((!isData&&singleLeptonic)||(isData&&singleLeptonic&&"+triggers+"&&"+filters+"))"
presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>1 && htJet30j>500"
presel += "&& iso_Veto"
#presel += "&& ((!isData)||(isData&&(run<=279931)))"
singleMu_presel = "((!isData&&singleMuonic)||(isData&&"+triggers+"&&"+filters+"))"
singleMu_presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>1 && htJet30j>500"

singleEle_presel = "((!isData&&singleElectronic)||(isData&&"+triggers+"&&"+filters+"))"
singleEle_presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>1 && htJet30j>500"

presel_MC = "singleLeptonic" + "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>1 && htJet30j>500 && Flag_badChargedHadronFilter && Flag_badMuonFilter"
presel_MC += "&& iso_Veto" 

if not isData: presel = presel_MC

#presel = singleMu_presel

## weights for MC
muTriggerEff = '0.926'
eleTriggerErr = '0.963'
ttJetsweight = '(1.071)'  ### this is temperary change this 
MCweight = '(weight_ISR_new)'
if useDLCorr : MCweight = '(%s*DilepNJetCorr)'%(MCweight)
if useDLCorr_constantUp : MCweight = '(%s*DilepNJetWeightConstUp)'%(MCweight)
if useDLCorr_slopeUp : MCweight = '(%s*DilepNJetWeightSlopeUp)'%(MCweight)

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
  pickleDir   = '/afs/hephy.at/data/'+username+'01/Results'+year+'/Prediction_'+predictionName+'_'+lumistr+'/'
  templateDir = '/afs/hephy.at/data/'+username+'01/Results'+year+'/btagTemplates_'+predictionName+'_'+templateLumistr+'/'



## create directories that are defined but do not yet exist
print "Fit Dir :" , fitDir
if not os.path.exists(fitDir):
  os.makedirs(fitDir)
print "pickle Dir :" , pickleDir
if not os.path.exists(pickleDir):
  os.makedirs(pickleDir)
print "print Dir :" , printDir
if not os.path.exists(printDir):
  os.makedirs(printDir)
print "template Dir :" , templateDir
if not os.path.exists(templateDir):
  os.makedirs(templateDir)
if not os.path.exists(fitPrintDir):
  os.makedirs(fitPrintDir)
