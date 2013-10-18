import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("PAT")
options = VarParsing.VarParsing ('standard')

options.register ('isMC','True',
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.bool,
          "Switch between MC and Data")

options.register ('hltName','HLT',
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "HLT Trigger collection")

options.register ('GT','START53_V7F::All',#GR_R_52_V9::All
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "Global Tag")

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

options.register ('addRA4Info',True,
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.bool,
          "whether or not to add RA4 specific Info")

infiles = ['file:/data/schoef/local/TTJets-53X-syncfile-AODSIM.root']
#infiles = ['/store/caf/user/imikulec/lstop/Hadronizer_SMS_Scans_2jets_Qcut44_TuneZ2star_8TeV_madgraph_tauola_cff_py_GEN_FASTSIM_HLT_PU.root']
#infiles = ['file:/data/jkancsar/pickevent/event4874249.root']
#infiles = ['file:/afs/hephy.at/scratch/s/schoefbeck/CMS/CMSSW_5_3_3_patch2/src/Workspace/HEPHYCommonTools/crab/pickEvents/pickevents.root']
options.files=infiles

#options.isMC = False
options.isMC = True
options.maxEvents=10

if not 'ipython' in VarParsing.sys.argv[0]:
  options.parseArguments()
else:
  print "No parsing of arguments!"

jec = []
if options.isMC:
  jec = ['L1FastJet', 'L2Relative', 'L3Absolute']
else:
  jec = ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']
#  if options.mode=="Mu":
#    triggers =  ['HLT_PFHT350_Mu15_PFMET45_v*','HLT_PFHT350_Mu15_PFMET50_v*','HLT_PFHT400_Mu5_PFMET45_v*','HLT_PFHT400_Mu5_PFMET50_v*']
#  if options.mode=="Ele":
#    triggers = ['HLT_CleanPFHT350_Ele5_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_PFMET45_v*','HLT_CleanPFHT350_Ele5_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_PFMET50_v*','HLT_CleanPFHT300_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_PFMET45_v*','HLT_CleanPFHT300_Ele15_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_PFMET50_v*']

print "isMC?",options.isMC,", verbose?",options.verbose,", add RA4 Info?",options.addRA4Info, ", JEC:",jec,", GT",options.GT, ", triggers", options.triggers



#-- Message Logger ------------------------------------------------------------
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.categories.append('PATSummaryTables')
process.MessageLogger.cerr.PATSummaryTables = cms.untracked.PSet(
    limit = cms.untracked.int32(-1),
    reportEvery = cms.untracked.int32(100)
)

#-- Source information ------------------------------------------------------
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.files)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents ) )
#process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange(
#  '190645:10-190645:110',
#)

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

## Standard PAT Configuration File
process.load("PhysicsTools.PatAlgos.patSequences_cff")

#Need this for L1 triggers with CMSSW >= 381
process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
process.patTrigger.addL1Algos = cms.bool( True )

process.out = cms.OutputModule("PoolOutputModule",
     #verbose = cms.untracked.bool(True),
     SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
     fileName = cms.untracked.string('histo.root'),
     outputCommands = cms.untracked.vstring() 
#     outputCommands = cms.untracked.vstring('keep *') 
)

#-- SUSYPAT and GlobalTag Settings -----------------------------------------------------------
from PhysicsTools.Configuration.SUSY_pattuple_cff import addDefaultSUSYPAT, getSUSY_pattuple_outputCommands

process.GlobalTag.globaltag = options.GT 
addDefaultSUSYPAT(process,options.isMC,options.hltName,jec,'',['AK5PF'])

process.patJetsAK5PF.addTagInfos = cms.bool(True)
process.pfNoTauPF.enable = cms.bool(False)
#SUSY_pattuple_outputCommands = getSUSY_pattuple_outputCommands( process )

############################## END SUSYPAT specifics ####################################

################### Add Type-I PFMET (for default RECO-PF jets) ########################
#process.load('RecoMET.METFilters.EcalDeadCellBoundaryEnergyFilter_cfi')
process.load("JetMETCorrections.Type1MET.pfMETCorrections_cff")

if options.isMC:
  process.pfJetMETcorr.jetCorrLabel = "ak5PFL1FastL2L3"
else:
  process.pfJetMETcorr.jetCorrLabel = "ak5PFL1FastL2L3Residual"

process.patPFMETs = process.patMETs.clone(
             metSource = cms.InputTag('pfMet'),
             addMuonCorrections = cms.bool(False),
             #genMETSource = cms.InputTag('genMetTrue'),
             #addGenMET = cms.bool(True)
             )

process.pfType1CorrectedMet.applyType0Corrections = cms.bool(False)

process.patPFMETsTypeIcorrected = process.patPFMETs.clone(
             metSource = cms.InputTag('pfType1CorrectedMet'),
             )

process.rawpfMet = process.pfType1CorrectedMet.clone(applyType1Corrections = cms.bool(False))

process.patRAWPFMETs = process.patPFMETs.clone(
    metSource = cms.InputTag('rawpfMet'),
)

process.load("JetMETCorrections.Type1MET.pfMETCorrectionType0_cfi")
process.pfType1Type0PFCandidateCorrectedMet = process.pfType1CorrectedMet.clone(
           applyType0Corrections = cms.bool(False),
           srcType1Corrections = cms.VInputTag(
           cms.InputTag('pfMETcorrType0'),
           cms.InputTag('pfJetMETcorr', 'type1')
           )
             )

process.patPFMETsTypeIType0PFCandcorrected = process.patPFMETs.clone(
             metSource = cms.InputTag('pfType1Type0PFCandidateCorrectedMet'),
            )
process.load("JetMETCorrections.Type1MET.pfMETsysShiftCorrections_cfi")

if options.isMC:
  process.pfMEtSysShiftCorr.parameter = process.pfMEtSysShiftCorrParameters_2012runAvsNvtx_mc
else:
  process.pfMEtSysShiftCorr.parameter = process.pfMEtSysShiftCorrParameters_2012runAvsNvtx_data

process.pfType1PhiCorrectedMet = process.pfType1CorrectedMet.clone(
  srcType1Corrections = cms.VInputTag(
      cms.InputTag('pfJetMETcorr', 'type1') ,
      cms.InputTag('pfMEtSysShiftCorr')  
  )
)
#process.producePFMETCorrections += process.pfType1PhiCorrectedMet
process.patPFMETsTypeIPhicorrected = process.patPFMETs.clone(
             metSource = cms.InputTag('pfType1PhiCorrectedMet'),
             )
#Turn on trigger info
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
switchOnTrigger(process, triggerProducer='patTrigger', triggerEventProducer='patTriggerEvent', sequence='patDefaultSequence', hltProcess="HLT")

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
              #process.EcalDeadCellBoundaryEnergyFilter*
            process.EventCounterAfterECALTP
              #process.totalKinematicsFilter*
            #process.EventCounterAfterTotalKinematicsFilter
          )

if options.isMC:
  print "\nFilter List:", "HLT, scraping, PV, HBHE, CSCTightHalo, EcalTP, Laser, eeBadSc\n"
else:
#  process.load("EventFilter.HcalRawToDigi.hcallasereventfilter2012_cfi")
#  process.filterSequence+=process.hcallasereventfilter2012
#  process.EventCounterAfterHCALLaser2012 = process.EventCounter.clone()
#  process.filterSequence+=process.EventCounterAfterHCALLaser2012
#  process.load('RecoMET.METFilters.ecalLaserCorrFilter_cfi')
#  process.filterSequence+= process.ecalLaserCorrFilter
#  process.EventCounterafterECalLaserCorrectionFilter = process.EventCounter.clone()
#  process.filterSequence+=process.EventCounterafterECalLaserCorrectionFilter
#  process.load('RecoMET.METFilters.trackingPOGFilters_cff')
#  process.filterSequence+=process.trkPOGFilters
#  process.EventCounterAfterTrkPOGFilters = process.EventCounter.clone()
#  process.filterSequence+=process.EventCounterAfterTrkPOGFilters
#  process.load("EventFilter.HcalRawToDigi.hcallasereventfilter2012_cff")

  process.load("EventFilter.HcalRawToDigi.hcallasereventfilter2012_cfi")
  process.filterSequence+=process.hcallasereventfilter2012
  process.EventCounterAfterHCALLaser2012 = process.EventCounter.clone()
  process.filterSequence+=process.EventCounterAfterHCALLaser2012
  process.load('RecoMET.METFilters.ecalLaserCorrFilter_cfi')
  process.filterSequence+= process.ecalLaserCorrFilter
  process.EventCounterafterECalLaserCorrectionFilter = process.EventCounter.clone()
  process.filterSequence+=process.EventCounterafterECalLaserCorrectionFilter
#  process.load('RecoMET.METFilters.trackingPOGFilters_cff')
#  process.filterSequence+=process.trkPOGFilters
#  process.EventCounterAfterTrkPOGFilters = process.EventCounter.clone()
#  process.filterSequence+=process.EventCounterAfterTrkPOGFilters

  print "\nFilter List:", "HLT, scraping, PV, HBHE, CSCTightHalo, EcalTP, Laser, eeBadSc, hcal2012, ecallaser\n"


from RecoJets.JetProducers.kt4PFJets_cfi import *
process.kt6PFJetsForIsolation2011 = kt4PFJets.clone( rParam = 0.6, doRhoFastjet = True )
process.kt6PFJetsForIsolation2011.Rho_EtaMax = cms.double(2.5)
#compute rho for 2012 effective area Egamma isolation corrections
process.kt6PFJetsForIsolation2012 = kt4PFJets.clone( rParam = 0.6, doRhoFastjet = True )
process.kt6PFJetsForIsolation2012.Rho_EtaMax = cms.double(4.4)
process.kt6PFJetsForIsolation2012.voronoiRfact = cms.double(0.9)

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

from CMGTools.External.pujetidsequence_cff import loadPujetId
loadPujetId(process,'patJetsAK5PF',mvaOnly=False,isChs=False,release="53X")

#-- Execution path ------------------------------------------------------------
# Full path
process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi') #FIXME Added R.S.


process.p = cms.Path(process.goodOfflinePrimaryVertices + process.filterSequence + process.susyPatDefaultSequence + process.puJetIdpatJetsAK5PF + process.puJetMvapatJetsAK5PF)
#process.p += process.printTree
process.p += process.kt6PFJetsForIsolation2011
process.p += process.pfMEtSysShiftCorrSequence
process.p += process.producePFMETCorrections
process.p += process.type0PFMEtCorrection
process.p += process.pfType1Type0PFCandidateCorrectedMet
process.p += process.pfType1PhiCorrectedMet
process.p += process.patPFMETsTypeIcorrected
process.p += process.patPFMETsTypeIPhicorrected
process.p += process.patPFMETsTypeIType0PFCandcorrected
process.p += process.rawpfMet
process.p += process.patRAWPFMETs

process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryProducer_cfi")
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryFilter_cfi")
process.load('Workspace.HEPHYCommonTools.SUSYTupelizer_cfi')
if options.isMC:
  process.p +=      process.bFlavorHistoryProducer
  process.p +=      process.cFlavorHistoryProducer
  process.p +=      process.flavorHistoryFilter

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

process.SUSYTupelizer.triggerCollection = cms.untracked.string( options.hltName )

process.SUSYTupelizer.addFullLeptonInfo = cms.untracked.bool(True)
process.SUSYTupelizer.addFullJetInfo = cms.untracked.bool(True)
process.SUSYTupelizer.addFullMETInfo = cms.untracked.bool(True)
process.SUSYTupelizer.useForDefaultAlias = cms.untracked.bool(True)
#process.SUSYTupelizer.addLeptonTriggerInfo = cms.untracked.bool(False)
process.SUSYTupelizer.addTriggerInfo = cms.untracked.bool(True)
process.SUSYTupelizer.addFullLeptonInfo = cms.untracked.bool(True)
process.SUSYTupelizer.addFullBTagInfo = cms.untracked.bool(True)
process.SUSYTupelizer.addGeneratorInfo = cms.untracked.bool(options.isMC)
#process.SUSYTupelizer.addMSugraOSETInfo = cms.untracked.bool(False)
process.SUSYTupelizer.verbose = cms.untracked.bool(options.verbose)
process.SUSYTupelizer.addFullMuonInfo = cms.untracked.bool(True)
process.SUSYTupelizer.addFullEleInfo = cms.untracked.bool(True)
process.SUSYTupelizer.addFullTauInfo = cms.untracked.bool(True)
process.SUSYTupelizer.addHEPHYCommonToolsInfo = cms.untracked.bool(options.addRA4Info)
process.p += process.SUSYTupelizer

#process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
#process.printTree = cms.EDAnalyzer("ParticleListDrawer",
#  maxEventsToPrint = cms.untracked.int32(-1),
#  printVertex = cms.untracked.bool(False),
#  src = cms.InputTag("genParticles")
#)
#process.p+=process.printTree
process.out.outputCommands =  cms.untracked.vstring('drop *', 'keep *_*SUSYTupelizer*_*_*' , 'keep *_*EventCounter*_*_*', 'keep *_genParticles_*_SIM')
process.outpath = cms.EndPath(process.out)
#-- Dump config ------------------------------------------------------------
file = open('vienna_SusyPAT_cfg.py','w')
file.write(str(process.dumpPython()))
file.close()
