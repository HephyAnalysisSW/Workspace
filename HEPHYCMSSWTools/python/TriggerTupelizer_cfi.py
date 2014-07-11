import FWCore.ParameterSet.Config as cms

BasicTupelizer = cms.EDProducer ( "BasicTupelizer",
    verbose           = cms.untracked.bool(False),
    triggerCollection = cms.untracked.InputTag("HLT"),

    triggersToMonitor = cms.untracked.vstring(["HLT_IsoMu24_eta2p1"]),
    useForDefaultAlias = cms.untracked.bool(False)

) 
