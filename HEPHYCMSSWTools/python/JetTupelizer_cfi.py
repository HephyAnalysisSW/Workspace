import FWCore.ParameterSet.Config as cms

JetTupelizer = cms.EDProducer ( "JetTupelizer",
    verbose           = cms.untracked.bool(False),
    input             = cms.untracked.InputTag("patJetsAK5PF"),
    ptThreshold       = cms.untracked.double(10.0),
    btag              = cms.untracked.string("combinedSecondaryVertexBJetTags"),
    puJetIdCutBased   = cms.untracked.InputTag("puJetMvapatJetsAK5PF", "cutbasedId"),
    puJetIdFull53X    = cms.untracked.InputTag("puJetMvapatJetsAK5PF", "full53xId"),
    puJetIdMET53X     = cms.untracked.InputTag("puJetMvapatJetsAK5PF", "met53xId"),
    useForDefaultAlias = cms.untracked.bool(False)

) 
