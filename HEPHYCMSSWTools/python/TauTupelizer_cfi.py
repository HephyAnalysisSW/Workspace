import FWCore.ParameterSet.Config as cms

TauTupelizer = cms.EDProducer ( "TauTupelizer",
    verbose      = cms.untracked.bool(False),
    input        = cms.untracked.InputTag("patTaus"),
    ptThreshold = cms.untracked.double(5.),
    useForDefaultAlias = cms.untracked.bool(False)

) 
