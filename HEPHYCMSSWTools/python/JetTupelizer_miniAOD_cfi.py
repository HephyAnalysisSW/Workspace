import FWCore.ParameterSet.Config as cms

JetTupelizer = cms.EDProducer ( "JetTupelizer",
    verbose           = cms.untracked.bool(False),
    input             = cms.untracked.InputTag("slimmedJets"),
    ptThreshold       = cms.untracked.double(10.0),
    
    userFloats = cms.untracked.VPSet(
        cms.untracked.PSet(accessTag = cms.untracked.string("vtxMass"), 
                           storeTag = cms.untracked.string("VtxMass")),
        cms.untracked.PSet(accessTag = cms.untracked.string("vtxNtracks"), 
                           storeTag = cms.untracked.string("VtxNtracks")),
        cms.untracked.PSet(accessTag = cms.untracked.string("pileupJetId:fullDiscriminant"), 
                 storeTag = cms.untracked.string("PUJetIDFull")),
    ),

    #jetBProbabilityBJetTags, jetProbabilityBJetTags, trackCountingHighPurBJetTags, 
    #trackCountingHighEffBJetTags, simpleSecondaryVertexHighEffBJetTags, simpleSecondaryVertexHighPurBJetTags, 
    #combinedSecondaryVertexBJetTags , combinedInclusiveSecondaryVertexBJetTags
    bTags = cms.untracked.VPSet(
        cms.untracked.PSet(accessTag = cms.untracked.string("combinedSecondaryVertexBJetTags"), 
                           storeTag = cms.untracked.string("BTag")),
        cms.untracked.PSet(accessTag = cms.untracked.string("combinedInclusiveSecondaryVertexBJetTags"), 
                           storeTag = cms.untracked.string("IncBTag"))
    ),


    useForDefaultAlias = cms.untracked.bool(False)

) 
