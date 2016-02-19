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

####################################################################################################33
# top pt weight removed in MCweight!!


## b-tagging and other variables
dPhiStr = 'deltaPhi_Wl'
bjreg = (0,0)
wjetsSB = (3,4)

nBTagVar              = 'nBJetMediumCSV30'
useBTagWeights        = True
btagWeightSuffix      = '_SF'
templateWeights       = True
templateWeightSuffix  = '_SF'

QCDup       = False
QCDdown     = False
nameSuffix  = '_noTopPTweights2'
if QCDup: nameSuffix += '_QCDup'
if QCDdown: nameSuffix += '_QCDdown'

## samples
isData              = False
unblinded           = True
validation          = False
isCentralPrediction = True
if isData:
  isCentralPrediction = False #should be false for data, otherwise kappa is measured in data!

cWJets      = getChain(WJetsHTToLNu_25ns,histname='')
cTTJets     = getChain(TTJets_combined,histname='')
cDY         = getChain(DY_25ns,histname='')
csingleTop  = getChain(singleTop_25ns,histname='')
cTTV        = getChain(TTV_25ns,histname='')
cRest       = getChain([singleTop_25ns, DY_25ns, TTV_25ns],histname='')#no QCD
cBkg        = getChain([WJetsHTToLNu_25ns, TTJets_combined, singleTop_25ns, DY_25ns, TTV_25ns], histname='')#no QCD
cQCD        = getChain(QCDHT_25ns,histname='')


## QCD estimation
useQCDestimation = False
if not isData and useQCDestimation: QCDpickle = '/data/dspitzbart/Results2016/QCDEstimation/20160212_QCDestimation_MC2p25fb_pkl'
if isData:
  #QCDpickle  = '/data/dspitzbart/Results2016/QCDEstimation/20160212_QCDestimation_data2p25fb_pkl'
  QCDpickle  = '/data/dspitzbart/Results2016/QCDEstimation/20160218_QCDestimation_validation_data2p25fb_pkl'
  #QCDpickle  = '/data/dhandl/results2015/QCDEstimation/20151216_QCDestimation_2p1fb_pkl'
  #QCDpickle = '/data/dhandl/results2015/QCDEstimation/20151216_QCDestimation_extendedClosureTest3to4j_2p1fb_pkl'
  #QCDpickle = '/data/dhandl/results2015/QCDEstimation/20151216_QCDestimation_closureTest4to5j_2p1fb_pkl'

if isData or useQCDestimation: QCDestimate = pickle.load(file(QCDpickle))
else: QCDestimate=False

if isData:
  cData = getChain([single_mu_Run2015D, single_ele_Run2015D], histname='')
elif not isData and useQCDestimation:
  cData = getChain([WJetsHTToLNu_25ns, TTJets_combined, singleTop_25ns, DY_25ns, TTV_25ns, QCDHT_25ns], histname='')
else:
  cData = getChain([WJetsHTToLNu_25ns, TTJets_combined, singleTop_25ns, DY_25ns, TTV_25ns], histname='')


## signal region definition
if validation:
  signalRegions = validationRegionAll
  regStr = 'validation_4j'
else:
  signalRegions = signalRegion3fb
  regStr = 'fullSR'
#signalRegions = signalRegion3fbMerge

## weight calculations
lumi = 2.25
templateLumi = 2.25 # lumi that was used when template was created - if defined wrong, fixed rest backgrounds will be wrong
sampleLumi = 3.
printlumi = '2.2'
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
templateBootstrapDir = '/data/dspitzbart/bootstrap/combined_errs_pkl'
if templateBootstrap: templateBootstrap = pickle.load(file(templateBootstrapDir))

## Directories for plots, results and templates
if isData:
  templateName   = 'SFtemplates_'+regStr+'_lep_data'
  predictionName = templateName
else:
  templateName   = 'SFtemplates_'+regStr+'_lep_MC'
  predictionName = templateName+btagWeightSuffix + nameSuffix
printDir    = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Spring15/25ns/templateFit_'+predictionName+'_'+lumistr+'/'
pickleDir   = '/data/'+username+'/Results'+year+'/Prediction_'+predictionName+'_'+lumistr+'/'
templateDir = '/data/'+username+'/Results'+year+'/btagTemplates_'+templateName+'_'+templateLumistr+'/'
prefix = 'singleLeptonic_Spring15_'

if validation:
  kappa_dict_dir = '/data/dspitzbart/Results'+year+'/Prediction_SFtemplates_validation_4j_lep_MC_SFnoPUreweight_2p25/singleLeptonic_Spring15__estimationResults_pkl_kappa_corrected'
else:
  kappa_dict_dir = '/data/dspitzbart/Results'+year+'/Prediction_SFtemplates_fullSR_lep_MC_SFnoPUreweight_2p25/singleLeptonic_Spring15__estimationResults_pkl_kappa_corrected'

## Preselection cut
triggers = "(HLT_EleHT350||HLT_MuHT350)"
#filters = "Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_CSCTightHaloFilter && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter"
filters = "Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter && veto_evt_list"
presel = "((!isData&&singleLeptonic)||(isData&&"+triggers+"&&((muonDataSet&&singleMuonic)||(eleDataSet&&singleElectronic))&&"+filters+"))"
presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>2 && htJet30j>500"

singleMu_presel = "((!isData&&singleMuonic)||(isData&&"+triggers+"&&(muonDataSet&&singleMuonic)&&"+filters+"))"
singleMu_presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>2 && htJet30j>500"

#presel = singleMu_presel

## weights for MC
MCweight = 'lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*0.94'
#MCweight = 'lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*TopPtWeight*0.94'

## corrections
createFits = False # turn off if you already did one
if not isCentralPrediction:
  createFits = False
fitDir = '/data/'+username+'/Results'+year+'/correctionFit_'+regStr+'_MC/'
fitPrintDir = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results'+year+'/25ns/RcsFit_'+predictionName+'_'+lumistr+'/'

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
