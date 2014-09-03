import FWCore.ParameterSet.Config as cms

TriggerTupelizer = cms.EDProducer ( "TriggerTupelizer",
    verbose           = cms.untracked.bool(False),
    triggerCollection = cms.untracked.InputTag("TriggerResults","", "HLT"),
    triggersToMonitor = cms.untracked.vstring(["HLT_IsoMu24_eta2p1"]),
    addL1Prescales = cms.untracked.bool(False),

    useForDefaultAlias = cms.untracked.bool(False)
) 
