import FWCore.ParameterSet.Config as cms

PFCandTupelizer = cms.EDProducer ( "PFCandTupelizer",
    srcPFlow = cms.InputTag('particleFlow', ''),
    useForDefaultAlias = cms.untracked.bool(True)
) 
