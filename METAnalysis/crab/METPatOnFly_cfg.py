import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

#process = cms.Process("PAT")
options = VarParsing.VarParsing ('standard')

options.register ('mode','mc',
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "Switch between MC and data")

options.register ('leptonSelection','None',
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "lepton selection")

options.register ('hltName','HLT',
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "HLT Trigger collection")

options.register ('GT','START53_V7F::All',#GR_R_52_V9::All
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "Global Tag")

options.register ('outfile','histo.root',
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "outfile")

options.register ('triggers','*',
          VarParsing.VarParsing.multiplicity.list,
          VarParsing.VarParsing.varType.string,
          "Trigger requirement")

options.register ('triggersToMonitor','',
          VarParsing.VarParsing.multiplicity.list,
          VarParsing.VarParsing.varType.string,
          "Trigger list to monitor")

options.register ('verbose',False,
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.bool,
          "verbosity")

options.register ('addRA4Info',False,
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.bool,
          "whether or not to add RA4 specific Info")

infiles = ['file:/data/schoef/local/TTJets-53X-syncfile-AODSIM.root']
#  infiles = ['file:/data/jkancsar/pickevent/event4874249.root']
#  infiles = ['file:/data/schoef/monoJetSignals/FastSim/stop200lsp170g100/from_0_to_10000_decayed_stop200lsp170g100.root']
#  infiles = ['root://eoscms//eos/cms/store/data/Run2012C/DoubleMu/AOD/PromptReco-v1/000/198/487/5E5FB822-C8CA-E111-82EE-001D09F2915A.root']

options.files=infiles

options.mode = 'mc'
options.maxEvents=10
if 'ipython' not in VarParsing.sys.argv[0].lower():
  options.parseArguments()
else:
  print "No parsing of arguments!"

from PhysicsTools.PatAlgos.patTemplate_cfg import *

#process = cms.Process("PAT")
### MessageLogger
#process.load("FWCore.MessageLogger.MessageLogger_cfi")
### Options and Output Report
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )
### Source
#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring()
#)
### Geometry and Detector Conditions (needed for a few patTuple production steps)
#process.load("Configuration.Geometry.GeometryIdeal_cff")
#process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:startup')
#process.load("Configuration.StandardSequences.MagneticField_cff")
### Output Module Configuration (expects a path 'p')
#from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning

###from MM. FIXME. for trackJets?
### to roughly estimate the recHit position from the information
### saved on disk (avoid track refitting)
#process.load("RecoTracker.TransientTrackingRecHit.TTRHBuilders_cff")
#process.TTRHBuilderAngleAndTemplate.ComputeCoarseLocalPositionFromDisk = True


isMC = (options.mode.lower()=='mc')
isData = not isMC
jec = []
if isMC:
  jec = ['L1FastJet', 'L2Relative', 'L3Absolute']
else:
  jec = ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']

print "mode",options.mode,"isMC?",isMC, 'leptonSelection',options.leptonSelection, ", verbose?",options.verbose,", add RA4 Info?",options.addRA4Info, ", JEC:",jec,", GT",options.GT, ", triggers", options.triggers


#-- Source information ------------------------------------------------------
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.files)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents ) )
#process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange(
#  '190645:10-190645:110',
#)
### Standard PAT Configuration File
#process.load("PhysicsTools.PatAlgos.patSequences_cff")

##Need this for L1 triggers with CMSSW >= 381
#process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
#process.patTrigger.addL1Algos = cms.bool( False )

process.out = cms.OutputModule("PoolOutputModule",
     #verbose = cms.untracked.bool(True),
     SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
     fileName = cms.untracked.string(options.outfile),
     outputCommands = cms.untracked.vstring() 
#     outputCommands = cms.untracked.vstring('keep *') 
)

#
# to roughly estimate the recHit position from the information
# saved on disk (avoid track refitting)
#
#process.load("RecoTracker.TransientTrackingRecHit.TTRHBuilders_cff")
#process.TTRHBuilderAngleAndTemplate.ComputeCoarseLocalPositionFromDisk = True

from PhysicsTools.PatAlgos.tools.coreTools import *
from PhysicsTools.PatAlgos.tools.pfTools import *
usePFIso( process )

#process.patElectrons.pfElectronSource = 'particleFlow'

from PhysicsTools.PatAlgos.tools.electronTools import *
addElectronUserIsolation(process)
process.load("RecoEgamma.EgammaIsolationAlgos.egammaIsolationSequence_cff")
process.patElectronIsolation = cms.Sequence(process.egammaIsolationSequence)

process.patElectrons.isolationValues = cms.PSet(
        pfChargedHadrons = cms.InputTag("elPFIsoValueCharged03PFIdPFIso"),
            pfChargedAll = cms.InputTag("elPFIsoValueChargedAll03PFIdPFIso"),
            pfPUChargedHadrons = cms.InputTag("elPFIsoValuePU03PFIdPFIso"),
            pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral03PFIdPFIso"),
            pfPhotons = cms.InputTag("elPFIsoValueGamma03PFIdPFIso")
        )

process.patElectrons.isolationValuesNoPFId = cms.PSet(
        pfChargedHadrons = cms.InputTag("elPFIsoValueCharged03NoPFIdPFIso"),
            pfChargedAll = cms.InputTag("elPFIsoValueChargedAll03NoPFIdPFIso"),
            pfPUChargedHadrons = cms.InputTag("elPFIsoValuePU03NoPFIdPFIso"),
            pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral03NoPFIdPFIso"),
            pfPhotons = cms.InputTag("elPFIsoValueGamma03NoPFIdPFIso")
        )
process.patMETs.addGenMET = cms.bool(isMC)


if options.leptonSelection.lower()=='doublemu':
  print "\nRequiring 2 Muons!"
  process.leptonCounter = cms.EDFilter("PATCandViewCountFilter",
     src = cms.InputTag("selectedPatMuons"),
     maxNumber = cms.uint32(2000),
     minNumber = cms.uint32(2),
     filter = cms.bool(True)
  )
  process.patDefaultSequence += process.leptonCounter
if options.leptonSelection.lower()=='doubleele':
  print "\nRequiring 2 Electrons!"
  process.leptonCounter = cms.EDFilter("PATCandViewCountFilter",
     src = cms.InputTag("selectedPatElectrons"),
     maxNumber = cms.uint32(2000),
     minNumber = cms.uint32(2),
     filter = cms.bool(True)
  )
  process.patDefaultSequence += process.leptonCounter
 
process.load("RecoLocalCalo.EcalRecAlgos.EcalSeverityLevelESProducer_cfi");

from PhysicsTools.PatAlgos.tools.jetTools import *

if isData:
    switchJetCollection(process, cms.InputTag('ak5PFJets'),
                        doJTA            = True,
                        doBTagging       = True,
                        jetCorrLabel     =  ('AK5PF',['L1FastJet','L2Relative', 'L3Absolute','L2L3Residual'] ),#,'Uncertainty'
                        doType1MET       = False,
                        genJetCollection = cms.InputTag("ak5GenJets"),
                        doJetID      = True,
                        jetIdLabel   = "ak5"
                        )
else :
    switchJetCollection(process, cms.InputTag('ak5PFJets'),
                        doJTA            = True,
                        doBTagging       = True,
                        jetCorrLabel     =  ('AK5PF',['L1FastJet','L2Relative', 'L3Absolute'] ), #,'Uncertainty'
                        doType1MET       = False,
                        genJetCollection = cms.InputTag("ak5GenJets"),
                        doJetID      = True,
                        jetIdLabel   = "ak5"
                        )

################### Add Type-I PFMET (for default RECO-PF jets) ########################
#RS:
#process.load("JetMETCorrections.Type1MET.pfMETCorrections_cff")
#if isMC:
#  process.pfJetMETcorr.jetCorrLabel = "ak5PFL1FastL2L3"
#else:
#  process.pfJetMETcorr.jetCorrLabel = "ak5PFL1FastL2L3Residual"

#MM:
process.load("PhysicsTools.PatUtils.patPFMETCorrections_cff")
if isData:
    process.pfJetMETcorr.jetCorrLabel = cms.string("ak5PFL1FastL2L3Residual")
    process.patPFJetMETtype1p2Corr.jetCorrLabel = cms.string("L2L3Residual")
else :
    process.pfJetMETcorr.jetCorrLabel = cms.string("ak5PFL1FastL2L3")
    process.patPFJetMETtype1p2Corr.jetCorrLabel = cms.string("L3Absolute")

# turn off MC matching for the process
if isData:
    removeMCMatching(process, ['All'])

##Turn on trigger info
#from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
#switchOnTrigger(process, triggerProducer='patTrigger', triggerEventProducer='patTriggerEvent', sequence='patDefaultSequence', hltProcess="HLT")

import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
process.hltFilter = hlt.hltHighLevel.clone(
             HLTPaths = cms.vstring(options.triggers),
             TriggerResultsTag = cms.InputTag("TriggerResults","",options.hltName),
             throw = False
         )

process.scrapingVeto = cms.EDFilter("FilterOutScraping",
                                             applyfilter = cms.untracked.bool(True),
                                             debugOn = cms.untracked.bool(False),
                                             numtrack = cms.untracked.uint32(10),
                                             thresh = cms.untracked.double(0.25)
                                             )

process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
                      vertexCollection = cms.InputTag('offlinePrimaryVertices'),
                      minimumNDOF = cms.uint32(4) ,
                      maxAbsZ = cms.double(24),
                      maxd0 = cms.double(2))

process.load('CommonTools/RecoAlgos/HBHENoiseFilter_cfi')


process.goodVertices = cms.EDFilter(
            "VertexSelector",
            filter = cms.bool(False),
            src = cms.InputTag("offlinePrimaryVertices"),
            cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2")
          )

process.load("RecoMET.METFilters.hcalLaserEventFilter_cfi")
process.hcalLaserEventFilter.vetoByRunEventNumber=cms.untracked.bool(False)
process.hcalLaserEventFilter.vetoByHBHEOccupancy=cms.untracked.bool(True)
process.load('RecoMET.METFilters.eeBadScFilter_cfi')
process.load('RecoMET.METAnalyzers.CSCHaloFilter_cfi')
process.load('RecoMET.METFilters.EcalDeadCellTriggerPrimitiveFilter_cfi')
process.load('RecoMET.METFilters.trackingFailureFilter_cfi')
process.trackingFailureFilter.JetSource = cms.InputTag('ak5PFJets')
process.load('Workspace.HEPHYCommonTools.EventCounter')

process.EventCounterAfterHLT = process.EventCounter.clone()
process.EventCounterAfterScraping = process.EventCounter.clone()
process.EventCounterAfterPV = process.EventCounter.clone()
process.EventCounterAfterHBHE = process.EventCounter.clone()
process.EventCounterAfterTrackingFailure = process.EventCounter.clone()
process.EventCounterAfterLaser = process.EventCounter.clone()
process.EventCounterAfterCSC = process.EventCounter.clone()
process.EventCounterAfterEEBadSC = process.EventCounter.clone()
process.EventCounterAfterECALTP = process.EventCounter.clone()

process.filterSequence = cms.Sequence(
    process.EventCounter*
      process.hltFilter *
    process.EventCounterAfterHLT*
      process.scrapingVeto *
    process.EventCounterAfterScraping*
      process.primaryVertexFilter*
    process.EventCounterAfterPV*
      process.HBHENoiseFilter*
    process.EventCounterAfterHBHE*
      process.goodVertices*
    process.trackingFailureFilter*
      process.EventCounterAfterTrackingFailure*
    process.hcalLaserEventFilter*
      process.EventCounterAfterLaser*
    process.CSCTightHaloFilter*
      process.EventCounterAfterCSC*
    process.eeBadScFilter*
      process.EventCounterAfterEEBadSC*
      process.EcalDeadCellTriggerPrimitiveFilter*
    process.EventCounterAfterECALTP
  )

if options.mode.lower()=='mc':
  print "\nFilter List:", "HLT, scraping, PV, HBHE, trackingFailureFilter, hcalLaser, CSCTightHalo, eeBadSC, EcalTP\n"

if options.mode.lower()=='data':
  process.load("EventFilter.HcalRawToDigi.hcallasereventfilter2012_cfi")
  process.filterSequence+=process.hcallasereventfilter2012
  process.EventCounterAfterHCALLaser2012 = process.EventCounter.clone()
  process.filterSequence+=process.EventCounterAfterHCALLaser2012
  process.load('RecoMET.METFilters.ecalLaserCorrFilter_cfi')
  process.filterSequence+= process.ecalLaserCorrFilter
  process.EventCounterafterECalLaserCorrectionFilter = process.EventCounter.clone()
  process.filterSequence+=process.EventCounterafterECalLaserCorrectionFilter

  print "\nFilter List:", "HLT, scraping, PV, HBHE, trackingFailureFilter, hcalLaser, CSCTightHalo, eeBadSC, EcalTP, hcalLaser2012, ecalLaserCorr\n"

process.load('RecoJets.JetProducers.PileupJetID_cfi')
process.pileupJetIdProducer.jets = cms.InputTag('selectedPatJets')

#electron
Ele_acceptance = '(pt >= 19 && abs(eta)<2.5)'
Ele_Id = 'abs(deltaPhiSuperClusterTrackAtVtx)<0.06 && abs(deltaEtaSuperClusterTrackAtVtx)<0.007 && scSigmaIEtaIEta<0.03 && hadronicOverEm<0.12'
Ele_Iso = '(chargedHadronIso + max(neutralHadronIso + photonIso - 0.5*puChargedHadronIso, 0.))/pt < 0.3'
Mu_acceptance = '(abs(eta)<2.4 && pt>=15)'
Mu_Id = 'isPFMuon && isGlobalMuon && isTrackerMuon && globalTrack.normalizedChi2 < 10 && globalTrack.hitPattern.numberOfValidMuonHits > 0'
Mu_Iso = '(chargedHadronIso + max(neutralHadronIso + photonIso - 0.5*puChargedHadronIso, 0.))/pt < 0.2'
process.selectedPatMuons.cut = Mu_acceptance+'&&'+Mu_Id+'&&'+Mu_Iso
process.selectedPatElectrons.cut = Ele_acceptance+"&&"+Ele_Id+"&&"+Ele_Iso


### No Pu MET
process.load('JetMETCorrections.METPUSubtraction.noPileUpPFMET_cff')
process.calibratedAK5PFJetsForNoPileUpPFMEt.correctors = cms.vstring('ak5PFL1FastL2L3')
process.noPileUpPFMEt.srcLeptons = cms.VInputTag(["selectedPatMuons"])
### MVA MET
process.load('JetMETCorrections.METPUSubtraction.mvaPFMET_cff')
process.calibratedAK5PFJetsForPFMEtMVA.correctors = cms.vstring('ak5PFL1FastL2L3')
process.pfMEtMVA.srcLeptons = cms.VInputTag( ["selectedPatMuons"]) #selectedPatMuons
### ==================   NoPU and MVA MET ==================##

#process.minEleFilter = cms.EDFilter("PATCandViewCountFilter",
#    minNumber = cms.uint32(2),
#    maxNumber = cms.uint32(999999),
#    src = cms.InputTag("selectedPatElectrons")
#    )
#process.minMuFilter = cms.EDFilter("PATCandViewCountFilter",
#    minNumber = cms.uint32(2),
#    maxNumber = cms.uint32(999999),
#    src = cms.InputTag("selectedPatMuons")
#    )

##
## PAT processes 
##

# apply type I/type I + II PFMEt corrections to pat::MET object
# and estimate systematic uncertainties on MET
from PhysicsTools.PatUtils.tools.runType1PFMEtUncertainties import runType1PFMEtUncertainties
from PhysicsTools.PatUtils.tools.runType1CaloMEtUncertainties import runType1CaloMEtUncertainties
from PhysicsTools.PatUtils.tools.runMVAMEtUncertainties import runMVAMEtUncertainties
from PhysicsTools.PatUtils.tools.runNoPileUpMEtUncertainties import runNoPileUpMEtUncertainties


sfNoPUjetOffsetEnCorr = None
if isData:
    sfNoPUjetOffsetEnCorr = 0.2
else:
    sfNoPUjetOffsetEnCorr = 0.2

doApplyUnclEnergyResidualCorr=False

runType1PFMEtUncertainties(
  process,
  electronCollection = '',#cms.InputTag('selectedPatElectrons'),
  photonCollection = '',
  muonCollection = cms.InputTag('selectedPatMuons'),
  tauCollection = '',
  jetCollection = cms.InputTag('patJets'),
  makeType1corrPFMEt = True,
  makeType1p2corrPFMEt = True,
  doApplyType0corr = True,
  doSmearJets =isMC,
  postfix = ''
)

runMVAMEtUncertainties(
  process,
  electronCollection = '',
  photonCollection = '',
  muonCollection = cms.InputTag('selectedPatMuons'),
  tauCollection = '',
  jetCollection = cms.InputTag('patJets'),
  doSmearJets =isMC,
  addToPatDefaultSequence = False,
  postfix = ''
  )

runNoPileUpMEtUncertainties(
  process,
  electronCollection = '',
  photonCollection = '',
  muonCollection = cms.InputTag('selectedPatMuons'),
  tauCollection = '',
  jetCollection = cms.InputTag('patJets'),
  addToPatDefaultSequence = False,
  doApplyChargedHadronSubtraction = False,
  doApplyUnclEnergyCalibration = (doApplyUnclEnergyResidualCorr and not isData),
  sfNoPUjetOffsetEnCorr = sfNoPUjetOffsetEnCorr,
  doSmearJets =isMC,
  postfix = ''
  )


runMVAMEtUncertainties(
  process,
  electronCollection = cms.InputTag(''),
  photonCollection = '',
  muonCollection = cms.InputTag('selectedPatMuons'),
  tauCollection = '',
  jetCollection = cms.InputTag('patJets'),
  addToPatDefaultSequence = False,
  doSmearJets =isMC,
  postfix = "Unity"
  )

process.pfMEtMVAUnity.inputFileNames = cms.PSet(
       U     = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmet_53_Sep2013_type1_UnityResponse_v3.root'),
       DPhi  = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmetphi_53_June2013_type1.root'),
       CovU1 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru1cov_53_Dec2012.root'),
       CovU2 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru2cov_53_Dec2012.root')
)

process.pfMEtMVAUnclusteredEnUpUnity.inputFileNames = cms.PSet(
       U     = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmet_53_Sep2013_type1_UnityResponse_v3.root'),
       DPhi  = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmetphi_53_June2013_type1.root'),
       CovU1 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru1cov_53_Dec2012.root'),
       CovU2 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru2cov_53_Dec2012.root')
)
process.pfMEtMVAUnclusteredEnDownUnity.inputFileNames = cms.PSet(
       U     = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmet_53_Sep2013_type1_UnityResponse_v3.root'),
       DPhi  = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmetphi_53_June2013_type1.root'),
       CovU1 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru1cov_53_Dec2012.root'),
       CovU2 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru2cov_53_Dec2012.root')
)
process.pfMEtMVAJetEnUpUnity.inputFileNames = cms.PSet(
       U     = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmet_53_Sep2013_type1_UnityResponse_v3.root'),
       DPhi  = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmetphi_53_June2013_type1.root'),
       CovU1 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru1cov_53_Dec2012.root'),
       CovU2 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru2cov_53_Dec2012.root')
)
process.pfMEtMVAJetEnDownUnity.inputFileNames = cms.PSet(
       U     = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmet_53_Sep2013_type1_UnityResponse_v3.root'),
       DPhi  = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmetphi_53_June2013_type1.root'),
       CovU1 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru1cov_53_Dec2012.root'),
       CovU2 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru2cov_53_Dec2012.root')
)
if isMC:
  process.pfMEtMVAJetResUpUnity.inputFileNames = cms.PSet(
         U     = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmet_53_Sep2013_type1_UnityResponse_v3.root'),
         DPhi  = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmetphi_53_June2013_type1.root'),
         CovU1 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru1cov_53_Dec2012.root'),
         CovU2 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru2cov_53_Dec2012.root')
  )
  process.pfMEtMVAJetResDownUnity.inputFileNames = cms.PSet(
         U     = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmet_53_Sep2013_type1_UnityResponse_v3.root'),
         DPhi  = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmetphi_53_June2013_type1.root'),
         CovU1 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru1cov_53_Dec2012.root'),
         CovU2 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru2cov_53_Dec2012.root')
  )
process.pfMEtMVAMuonEnUpUnity.inputFileNames = cms.PSet(
       U     = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmet_53_Sep2013_type1_UnityResponse_v3.root'),
       DPhi  = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmetphi_53_June2013_type1.root'),
       CovU1 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru1cov_53_Dec2012.root'),
       CovU2 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru2cov_53_Dec2012.root')
)
process.pfMEtMVAMuonEnDownUnity.inputFileNames = cms.PSet(
       U     = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmet_53_Sep2013_type1_UnityResponse_v3.root'),
       DPhi  = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbrmetphi_53_June2013_type1.root'),
       CovU1 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru1cov_53_Dec2012.root'),
       CovU2 = cms.FileInPath('JetMETCorrections/METPUSubtraction/data/gbru2cov_53_Dec2012.root')
)

##-------------------- Turn-on the FastJet density calculation -----------------------
process.load('RecoJets.JetProducers.kt4PFJets_cfi')
process.kt6PFJets = process.kt4PFJets.clone( rParam = 0.6, doRhoFastjet = True )

process.patJetCorrFactors.useRho = cms.bool(True)
process.patJetCorrFactors.rho = cms.InputTag("kt6PFJets:rho:RECO") #PAT
process.patJetCorrFactors.useNPV = cms.bool(False)

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi') #FIXME Added R.S.
process.prepat_sequence = cms.Sequence(
    process.goodOfflinePrimaryVertices *
    #MET filters
    process.filterSequence*
    #HLT Filter
    #process.HLTFilter *
    # Get Rho isolation correction
    process.kt6PFJets#*
#        process.ak5CaloL1FastL2L3
    )

if isData :
    process.prepat_sequence += process.ak5PFJetsL1FastL2L3Residual
else :
    process.prepat_sequence += process.ak5PFJetsL1FastL2L3

process.pat_sequence =  cms.Sequence(
    # PAT
    process.patDefaultSequence
    # jet id for PU reduction
    *process.pileupJetIdProducer
)

process.pat_sequence += process.pfMVAMEtUncertaintySequence
process.pat_sequence += process.pfNoPileUpMEtUncertaintySequence
#process.pat_sequence += process.pfMVAMEtUncertaintySequenceEMu
process.pat_sequence += process.pfMVAMEtUncertaintySequenceUnity
#process.pat_sequence += process.pfNoPileUpMEtUncertaintySequenceEMu
#process.pat_sequence += process.pfNoPileUpMEtUncertaintySequenceEle
#process.pat_sequence += process.pfType1MEtUncertaintySequenceEle
#process.pat_sequence += process.pfType1MEtUncertaintySequenceEMu


process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
                                   src = cms.InputTag("genParticles"),                                                                 
                                   printP4 = cms.untracked.bool(False),
                                   printPtEtaPhi = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(False),
                                   printStatus = cms.untracked.bool(True),
                                   printIndex = cms.untracked.bool(False),
                                   status = cms.untracked.vint32( [1,2,3] )
                                   )
#process.printTree = cms.EDAnalyzer("ParticleListDrawer",
#    printVertex = cms.untracked.bool(False),
#    src = cms.InputTag("genParticles"),
#    maxEventsToPrint = cms.untracked.int32(-1)
#)

#from CMGTools.External.pujetidsequence_cff import loadPujetId#FIXME
#loadPujetId(process,'patJetsAK5PF',mvaOnly=False,isChs=False,release="53X")

#-- Execution path ------------------------------------------------------------

process.p = cms.Path(
  #prepat sequence
  process.prepat_sequence*
  #pat sequence
  process.pat_sequence
  )


process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryProducer_cfi")
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryFilter_cfi")
process.load('Workspace.HEPHYCommonTools.SUSYTupelizer_cfi')
if isMC:
  process.p +=  process.bFlavorHistoryProducer
  process.p +=  process.cFlavorHistoryProducer
  process.p +=  process.flavorHistoryFilter

if options.triggersToMonitor!='':
  options.triggersToMonitor+=options.triggers
else:
  options.triggersToMonitor = options.triggers
for t in options.triggersToMonitor:
  ts = t.replace("_v*","")
  if ts != "*":
    process.SUSYTupelizer.triggersToMonitor.append(ts)
process.SUSYTupelizer.triggersToMonitor = list(set(process.SUSYTupelizer.triggersToMonitor)) #remove duplicates

print "TriggersToMonitor:",process.SUSYTupelizer.triggersToMonitor
process.SUSYTupelizer.eleRho = cms.untracked.InputTag('kt6PFJets:rho:RECO')
process.SUSYTupelizer.patJets = cms.untracked.InputTag('selectedPatJets')
process.SUSYTupelizer.puJetIdCutBased = cms.untracked.InputTag("pileupJetIdProducer", "cutbasedId")
process.SUSYTupelizer.puJetIdFull53X    = cms.untracked.InputTag("pileupJetIdProducer", "fullId")
process.SUSYTupelizer.puJetIdMET53X     = cms.untracked.InputTag("pileupJetIdProducer", "philv1Id")
process.SUSYTupelizer.softJetPtThreshold= cms.untracked.double(30.0)
process.SUSYTupelizer.minJetPt          = cms.untracked.double(30.0)

process.SUSYTupelizer.triggerCollection = cms.untracked.string( options.hltName )

process.SUSYTupelizer.addFullJetInfo = cms.untracked.bool(True)
process.SUSYTupelizer.addMetUncertaintyInfo = cms.untracked.bool(True)
process.SUSYTupelizer.useForDefaultAlias = cms.untracked.bool(True)
process.SUSYTupelizer.addTriggerInfo = cms.untracked.bool(True)
process.SUSYTupelizer.addFullLeptonInfo = cms.untracked.bool(False)
process.SUSYTupelizer.addFullBTagInfo = cms.untracked.bool(False)
process.SUSYTupelizer.addGeneratorInfo = cms.untracked.bool(False)
process.SUSYTupelizer.addMSugraOSETInfo = cms.untracked.bool(False)
process.SUSYTupelizer.addPDFWeights = cms.untracked.bool(False)
process.SUSYTupelizer.verbose = cms.untracked.bool(options.verbose)
process.SUSYTupelizer.addFullMuonInfo = cms.untracked.bool(True)
process.SUSYTupelizer.addFullEleInfo = cms.untracked.bool(True)
process.SUSYTupelizer.addFullTauInfo = cms.untracked.bool(True)
process.SUSYTupelizer.addHEPHYCommonToolsInfo = cms.untracked.bool(False)

metsToMonitor = []
metsToMonitor.extend( [ 
    "patMETs",
    "patPFMet",
    "patPFMetMVA",
    "patPFMetMVAUnity",
    "patPFMetNoPileUp",
    "patType1p2CorrectedPFMet",
    "patPFMetJetEnDown",
    "patPFMetJetEnUp",
    "patPFMetMVAJetEnDown",
    "patPFMetMVAJetEnDownUnity",
    "patPFMetMVAJetEnUp",
    "patPFMetMVAJetEnUpUnity",
    "patPFMetMVAMuonEnDown",
    "patPFMetMVAMuonEnDownUnity",
    "patPFMetMVAMuonEnUp",
    "patPFMetMVAMuonEnUpUnity",
    "patPFMetMVAUnclusteredEnDown",
    "patPFMetMVAUnclusteredEnDownUnity",
    "patPFMetMVAUnclusteredEnUp",
    "patPFMetMVAUnclusteredEnUpUnity",
    "patPFMetMuonEnDown",
    "patPFMetMuonEnUp",
    "patPFMetNoPileUpJetEnDown",
    "patPFMetNoPileUpJetEnUp",
    "patPFMetNoPileUpMuonEnDown",
    "patPFMetNoPileUpMuonEnUp",
    "patPFMetNoPileUpUnclusteredEnDown",
    "patPFMetNoPileUpUnclusteredEnUp",
    "patPFMetUnclusteredEnDown",
    "patPFMetUnclusteredEnUp",
    "patType1CorrectedPFMet",
    "patType1CorrectedPFMetJetEnDown",
    "patType1CorrectedPFMetJetEnUp",
    "patType1CorrectedPFMetMuonEnDown",
    "patType1CorrectedPFMetMuonEnUp",
    "patType1CorrectedPFMetUnclusteredEnDown",
    "patType1CorrectedPFMetUnclusteredEnUp",
    "patType1p2CorrectedPFMetJetEnDown",
    "patType1p2CorrectedPFMetJetEnUp",
    "patType1p2CorrectedPFMetMuonEnDown",
    "patType1p2CorrectedPFMetMuonEnUp",
    "patType1p2CorrectedPFMetUnclusteredEnDown",
    "patType1p2CorrectedPFMetUnclusteredEnUp"
] )

process.SUSYTupelizer.metsToMonitor = cms.untracked.vstring(metsToMonitor)


process.p += process.SUSYTupelizer

#process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
#process.printTree = cms.EDAnalyzer("ParticleListDrawer",
#  maxEventsToPrint = cms.untracked.int32(-1),
#  printVertex = cms.untracked.bool(False),
#  src = cms.InputTag("genParticles")
#)
#process.p+=process.printTree
process.out.outputCommands =  cms.untracked.vstring('drop *', 'keep *_*SUSYTupelizer*_*_*' , 'keep *_*EventCounter*_*_*', 'keep *_genParticles_*_*' ,'keep *_particleFlow__RECO')
process.outpath = cms.EndPath(process.out)
#-- Dump config ------------------------------------------------------------
file = open('vienna_SusyPAT_cfg.py','w')
file.write(str(process.dumpPython()))
file.close()
