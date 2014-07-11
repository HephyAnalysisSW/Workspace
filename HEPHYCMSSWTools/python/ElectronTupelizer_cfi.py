import FWCore.ParameterSet.Config as cms

ElectronTupelizer = cms.EDProducer ( "ElectronTupelizer",
    verbose           = cms.untracked.bool(False),
    input             = cms.untracked.InputTag("cleanPatElectrons"),
    ptThreshold       = cms.untracked.double(5.),

    elePFRelIsoAreaCorrected = cms.untracked.bool(True) ,
    eleRho = cms.untracked.InputTag('kt6PFJetsForIsolation2011','rho'),

    useForDefaultAlias = cms.untracked.bool(False)

) 
