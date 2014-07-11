import FWCore.ParameterSet.Config as cms

MuonTupelizer = cms.EDProducer ( "MuonTupelizer",
    verbose        = cms.untracked.bool(False),
    input          = cms.untracked.InputTag("cleanPatMuons"),
    ptThreshold = cms.untracked.double(5.),

    vertices = cms.untracked.InputTag("goodVertices"),
    muonPFRelIsoDeltaBeta = cms.untracked.bool(True),

    useForDefaultAlias = cms.untracked.bool(False)

) 
