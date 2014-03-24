import FWCore.ParameterSet.Config as cms

CaloTowersTupelizer = cms.EDProducer ( "CaloTowersTupelizer",
    verbose      = cms.untracked.bool(False),
    hfCaloTowers      = cms.untracked.InputTag("hfreco"),
    useForDefaultAlias = cms.untracked.bool(True)

) 
