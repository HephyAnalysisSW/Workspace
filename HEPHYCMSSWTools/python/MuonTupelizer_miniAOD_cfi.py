import FWCore.ParameterSet.Config as cms

MuonTupelizer = cms.EDProducer ( "MuonTupelizer",
    verbose        = cms.untracked.bool(False),
    input          = cms.untracked.InputTag("slimmedMuons"),
    ptThreshold = cms.untracked.double(5.),

    vertices = cms.untracked.InputTag("offlineSlimmedPrimaryVertices"),
    muonPFRelIsoDeltaBeta = cms.untracked.bool(True),

    useForDefaultAlias = cms.untracked.bool(False)

) 
