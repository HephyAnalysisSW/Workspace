import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("MULT")
options = VarParsing.VarParsing ('standard')
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
options.register ('mode','mc',
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "Switch between MC and data")

infiles = ['file:/data/schoef/local/TTJets-53X-syncfile-AODSIM.root']
options.files=infiles

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(3000) )
if not 'ipython' in VarParsing.sys.argv[0]:
  options.parseArguments()
else:
  print "No parsing of arguments!"

process.source = cms.Source(
    'PoolSource',
#    fileNames = cms.untracked.vstring('root://xrootd.unl.edu//store/relval/CMSSW_7_0_5/RelValTTbar_13/GEN-SIM-RECO/POSTLS170_V6-v3/00000/0423767B-B5DD-E311-A1E0-02163E00E5B5.root')
#    fileNames = cms.untracked.vstring('root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_5/RelValTTbar_13/GEN-SIM-RECO/POSTLS170_V6-v3/00000/0423767B-B5DD-E311-A1E0-02163E00E5B5.root')
#/store/relval/CMSSW_7_0_5/RelValTTbar_13/GEN-SIM-RECO/POSTLS170_V7-v3/00000/F6768EBC-98DD-E311-B7DB-02163E00E7E8.root
    fileNames = cms.untracked.vstring(options.files)
    )
#-- Message Logger ------------------------------------------------------------
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.TFileService = cms.Service("TFileService", fileName = cms.string("histo.root") ,
      closeFileFast = cms.untracked.bool(True))

process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
## Geometry and Detector Conditions (needed for a few patTuple production steps)
#process.load("Configuration.StandardSequences.MagneticField_cff")

#process.GlobalTag.globaltag = 'POSTLS170_V6::All'
process.GlobalTag.globaltag = options.GT



import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
process.hltFilter = hlt.hltHighLevel.clone(
             HLTPaths = cms.vstring(options.triggers),
             TriggerResultsTag = cms.InputTag("TriggerResults","",options.hltName),
             throw = False
         )

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
process.filterSequence = cms.Sequence(
      process.hltFilter *
      process.scrapingVeto *
      process.primaryVertexFilter)
process.filterSequence+= process.goodVertices
process.filterSequence+= process.HBHENoiseFilter
process.filterSequence+= process.trackingFailureFilter
process.filterSequence+= process.hcalLaserEventFilter
process.filterSequence+= process.CSCTightHaloFilter
process.filterSequence+= process.eeBadScFilter
process.filterSequence+= process.EcalDeadCellTriggerPrimitiveFilter

if options.mode.lower()=='sms':
  print "\nFilter List:", "HLT, scraping, PV, EcalTP\n"
if options.mode.lower()=='mc':
  print "\nFilter List:", "HLT, scraping, PV, HBHE, trackingFailureFilter, hcalLaser, CSCTightHalo, eeBadSC, EcalTP\n"

if options.mode.lower()=='data':
  process.load("EventFilter.HcalRawToDigi.hcallasereventfilter2012_cfi")
  process.filterSequence+=process.hcallasereventfilter2012
  process.load('RecoMET.METFilters.ecalLaserCorrFilter_cfi')
  process.filterSequence+= process.ecalLaserCorrFilter

  print "\nFilter List:", "HLT, scraping, PV, HBHE, trackingFailureFilter, hcalLaser, CSCTightHalo, eeBadSC, EcalTP, hcalLaser2012, ecalLaserCorr\n"


process.load('Workspace.HEPHYCommonTools.multPhiCorr_multMETCorrInfoWriter_cff')


#
# RUN!
#
process.run = cms.Path(
  process.filterSequence*
  process.pfMEtMultCorrInfoWriterSequence
)


