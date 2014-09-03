import FWCore.ParameterSet.Config as cms

BasicTupelizer = cms.EDProducer ( "BasicTupelizer",
    verbose           = cms.untracked.bool(False),
    vertices = cms.untracked.InputTag("offlineSlimmedPrimaryVertices"),

    addMSugraOSETInfo = cms.untracked.bool(False),
    addPDFWeights = cms.untracked.bool(False),
    metsToMonitor = cms.untracked.vstring(["slimmedMETs"]),
    genMetContainer = cms.untracked.InputTag("slimmedMETs"),
    useForDefaultAlias = cms.untracked.bool(False)

) 
