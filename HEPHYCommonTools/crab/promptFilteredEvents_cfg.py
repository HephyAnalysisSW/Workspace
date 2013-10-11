import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("PAT")
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

infiles = ['file:/afs/hephy.at/scratch/s/schoefbeck/CMS/CMSSW_5_3_3_patch2/src/Workspace/HEPHYCommonTools/crab/pickEvents/pickevents.root']


## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

options.files=infiles


options.maxEvents=10

if not 'ipython' in VarParsing.sys.argv[0]:
  options.parseArguments()
else:
  print "No parsing of arguments!"


print "GT",options.GT, "triggers", options.triggers



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


process.GlobalTag.globaltag = options.GT 

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

process.load("EventFilter.HcalRawToDigi.hcallasereventfilter2012_cfi")
process.load('RecoMET.METFilters.ecalLaserCorrFilter_cfi')
process.load('RecoMET.METFilters.trackingPOGFilters_cff')
print "\nFilter List:", "HLT, scraping, PV, HBHE, CSCTightHalo, EcalTP, Laser, eeBadSc, HCALLaser, ecalLaserCorrectionFilter, TrkPOG odd event filter\n"

#-- Execution path ------------------------------------------------------------
# Full path
process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi') #FIXME Added R.S.
process.load('Workspace.HEPHYCommonTools.promptEvent_cfi')

process.goodVertices = process.goodOfflinePrimaryVertices.clone()
process.initialPath = cms.Path(process.goodVertices)
#process.passingFilters = cms.Sequence(
#               ~process.scrapingVeto
#              +~process.HBHENoiseFilter
#              +~process.trackingFailureFilter
#              +~process.hcalLaserEventFilter
#              +~process.CSCTightHaloFilter
#              +~process.eeBadScFilter
#              +~process.EcalDeadCellTriggerPrimitiveFilter
#              +~process.hcallasereventfilter2012
#              +~process.ecalLaserCorrFilter
#              +process.trkPOGFilters
#	    )

process.promptEventScraping = process.promptEvent.clone( promptMsg = 'scraping')
process.scrapingPath = cms.Path(
              process.hltFilter*
              process.primaryVertexFilter*
              ~process.scrapingVeto*
              process.promptEventScraping
          )

process.promptEventHBHE = process.promptEvent.clone( promptMsg = 'HBHE')
process.HBHENoisePath = cms.Path(
              process.hltFilter*
              process.primaryVertexFilter*
#              ~process.HBHENoiseFilter*
              ~process.HBHENoiseFilter*
              process.promptEventHBHE
          )

process.promptEventTrackingFailure = process.promptEvent.clone( promptMsg = 'trackingFailure')
process.trackingFailurePath = cms.Path(
              process.hltFilter*
              process.primaryVertexFilter*
              ~process.trackingFailureFilter*
              process.promptEventTrackingFailure
          )
process.promptEventHCalLaser = process.promptEvent.clone( promptMsg = 'HCalLaser')
process.HCalLaserPath = cms.Path(
              process.hltFilter*
              process.primaryVertexFilter*
              ~process.hcalLaserEventFilter*
              process.promptEventHCalLaser
          )
process.promptEventHCalLaser2012 = process.promptEvent.clone( promptMsg = 'HCalLaser2012')
process.HCalLaser2012Path = cms.Path(
              process.hltFilter*
              process.primaryVertexFilter*
              ~process.hcallasereventfilter2012*
              process.promptEventHCalLaser2012
          )
process.promptEventCSCTightHalo = process.promptEvent.clone( promptMsg = 'CSCTightHalo')
process.CSCTightHaloPath = cms.Path(
              process.hltFilter*
              process.primaryVertexFilter*
              ~process.CSCTightHaloFilter*
              process.promptEventCSCTightHalo
          )
process.promptEventeeBadSc = process.promptEvent.clone( promptMsg = 'eeBadSc')
process.eeBadScPath = cms.Path(
              process.hltFilter*
              process.primaryVertexFilter*
              ~process.eeBadScFilter*
              process.promptEventeeBadSc
          )
process.promptEventEcalDeadCellTriggerPrimitive = process.promptEvent.clone( promptMsg = 'EcalDeadCellTriggerPrimitive')
process.EcalDeadCellTriggerPrimitivePath = cms.Path(
              process.hltFilter*
              process.primaryVertexFilter*
              ~process.EcalDeadCellTriggerPrimitiveFilter*
              process.promptEventEcalDeadCellTriggerPrimitive
          )

process.promptEventecalLaserCorr = process.promptEvent.clone( promptMsg = 'ecalLaserCorr')
process.ecalLaserCorrPath = cms.Path(
              process.hltFilter*
              process.primaryVertexFilter*
              ~process.ecalLaserCorrFilter*
              process.promptEventecalLaserCorr
          )

process.promptEventmanystripclus53X = process.promptEvent.clone( promptMsg = 'manystripclus53X')
process.manystripclus53XPath = cms.Path(
              process.hltFilter*
              process.primaryVertexFilter*
              process.manystripclus53X*
              process.promptEventmanystripclus53X
          )
process.promptEventtoomanystripclus53X = process.promptEvent.clone( promptMsg = 'toomanystripclus53X')
process.toomanystripclus53XPath = cms.Path(
              process.hltFilter*
              process.primaryVertexFilter*
              process.toomanystripclus53X*
              process.promptEventtoomanystripclus53X
          )
process.promptEventlogErrorTooManyClusters = process.promptEvent.clone( promptMsg = 'logErrorTooManyClusters')
process.logErrorTooManyClustersPath = cms.Path(
              process.hltFilter*
              process.primaryVertexFilter*
              process.logErrorTooManyClusters*
              process.promptEventlogErrorTooManyClusters
          )


from RecoJets.JetProducers.kt4PFJets_cfi import *
process.kt6PFJetsForIsolation2011 = kt4PFJets.clone( rParam = 0.6, doRhoFastjet = True )
process.kt6PFJetsForIsolation2011.Rho_EtaMax = cms.double(2.5)
#compute rho for 2012 effective area Egamma isolation corrections
process.kt6PFJetsForIsolation2012 = kt4PFJets.clone( rParam = 0.6, doRhoFastjet = True )
process.kt6PFJetsForIsolation2012.Rho_EtaMax = cms.double(4.4)
process.kt6PFJetsForIsolation2012.voronoiRfact = cms.double(0.9)


process.schedule = cms.Schedule(process.initialPath, process.scrapingPath, process.HBHENoisePath, process.trackingFailurePath, process.HCalLaserPath, process.HCalLaser2012Path, 
                                process.CSCTightHaloPath, process.eeBadScPath, process.EcalDeadCellTriggerPrimitivePath,process.ecalLaserCorrPath, process.manystripclus53XPath, process.toomanystripclus53XPath, process.logErrorTooManyClustersPath )
