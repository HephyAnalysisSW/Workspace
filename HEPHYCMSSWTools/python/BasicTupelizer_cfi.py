import FWCore.ParameterSet.Config as cms

BasicTupelizer = cms.EDProducer ( "BasicTupelizer",
    verbose           = cms.untracked.bool(False),
    triggerCollection = cms.untracked.InputTag("HLT"),
    vertices = cms.untracked.InputTag("goodVertices"),

    addTriggerInfo = cms.untracked.bool(True),
    triggersToMonitor = cms.untracked.vstring(["HLT_IsoMu24_eta2p1"]),
    addMSugraOSETInfo = cms.untracked.bool(False),
    addPDFWeights = cms.untracked.bool(False),
    addMetUncertaintyInfo = cms.untracked.bool(False),
    metsToMonitor = cms.untracked.vstring([]),
    useForDefaultAlias = cms.untracked.bool(False)

) 
