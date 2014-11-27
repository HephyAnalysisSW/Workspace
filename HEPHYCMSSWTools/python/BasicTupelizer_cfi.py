import FWCore.ParameterSet.Config as cms

BasicTupelizer = cms.EDProducer ( "BasicTupelizer",
    verbose           = cms.untracked.bool(False),
    vertices = cms.untracked.InputTag("offlinePrimaryVertices"),

    addMSugraOSETInfo = cms.untracked.bool(False),
    addPDFWeights = cms.untracked.bool(False),
    metsToMonitor = cms.untracked.vstring([]),
    genMetContainer = cms.untracked.InputTag(""),
    storeGenMet = cms.untracked.bool(False),
    useForDefaultAlias = cms.untracked.bool(False)

) 
