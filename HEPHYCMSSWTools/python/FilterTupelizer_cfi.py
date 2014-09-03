import FWCore.ParameterSet.Config as cms

FilterTupelizer = cms.EDProducer ( "TriggerTupelizer",
    verbose           = cms.untracked.bool(False),
    triggerCollection = cms.untracked.InputTag("TriggerResults","", "PAT"),
    triggersToMonitor = cms.untracked.vstring(["Flag_trackingFailureFilter", "Flag_goodVertices", "Flag_CSCTightHaloFilter", "Flag_trkPOGFilters", "Flag_trkPOG_logErrorTooManyClusters", "Flag_EcalDeadCellTriggerPrimitiveFilter", "Flag_ecalLaserCorrFilter", "Flag_trkPOG_manystripclus53X", "Flag_eeBadScFilter", "Flag_METFilters", "Flag_HBHENoiseFilter", "Flag_trkPOG_toomanystripclus53X", "Flag_hcalLaserEventFilter"]),

    addL1Prescales = cms.untracked.bool(False),

    useForDefaultAlias = cms.untracked.bool(False)
) 
