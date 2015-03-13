import FWCore.ParameterSet.Config as cms

PFCandTupelizer = cms.EDProducer ( "PFCandTupelizer",
    srcPFlow = cms.InputTag('particleFlow', ''),
    fillIsolatedChargedHadrons = cms.untracked.bool(False),
    useForDefaultAlias = cms.untracked.bool(True),
) 
