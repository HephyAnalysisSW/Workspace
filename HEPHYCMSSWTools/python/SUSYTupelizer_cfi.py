import FWCore.ParameterSet.Config as cms

SUSYTupelizer = cms.EDProducer ( "SUSYTupelizer",
    verbose           = cms.untracked.bool(False),
    triggerCollection = cms.untracked.InputTag("HLT"),
    patJets           = cms.untracked.InputTag("patJetsAK5PF"),

    patMuons     = cms.untracked.InputTag("cleanPatMuons"),
    patElectrons = cms.untracked.InputTag("cleanPatElectrons"),
    patTaus = cms.untracked.InputTag("patTaus"),
    vertices = cms.untracked.InputTag("goodVertices"),

    lowLeptonPtThreshold = cms.untracked.double(5.),
    muonPFRelIsoDeltaBeta = cms.untracked.bool(True),

    elePFRelIsoAreaCorrected = cms.untracked.bool(True) ,
    eleRho = cms.untracked.InputTag('kt6PFJetsForIsolation2011','rho'),

    softJetPtThreshold= cms.untracked.double(10.0),
    btag              = cms.untracked.string("combinedSecondaryVertexBJetTags"),
    btagWP            = cms.untracked.double(0.679),
    btagPure          = cms.untracked.string("combinedSecondaryVertexBJetTags"),
    btagPureWP        = cms.untracked.double(0.244),
    hasL1Trigger      = cms.untracked.bool(True),
    puJetIdCutBased   = cms.untracked.InputTag("puJetMvapatJetsAK5PF", "cutbasedId"),
    puJetIdFull53X    = cms.untracked.InputTag("puJetMvapatJetsAK5PF", "full53xId"),
    puJetIdMET53X     = cms.untracked.InputTag("puJetMvapatJetsAK5PF", "met53xId"),

#    addRA4AnalysisInfo = cms.untracked.bool(True),
#    addTriggerInfo = cms.untracked.bool(False),
    triggersToMonitor = cms.untracked.vstring(["HLT_IsoMu24_eta2p1"]),
#    addFullBTagInfo = cms.untracked.bool(False),
    addJetVector = cms.untracked.bool(False),
#    addFullLeptonInfo = cms.untracked.bool(False),
    addFullTauInfo = cms.untracked.bool(False),
    addMuonVector = cms.untracked.bool(False),
    addEleVector = cms.untracked.bool(False),
#    addGeneratorInfo = cms.untracked.bool(False),
    addMSugraOSETInfo = cms.untracked.bool(False),
    addPDFWeights = cms.untracked.bool(False),
    addMetUncertaintyInfo = cms.untracked.bool(False),
    metsToMonitor = cms.untracked.vstring(["patType1CorrectedPFMet","patType1CorrectedPFMetElectronEnDown","patType1CorrectedPFMetElectronEnUp","patType1CorrectedPFMetJetEnDown","patType1CorrectedPFMetJetEnUp","patType1CorrectedPFMetJetResDown","patType1CorrectedPFMetJetResUp","patType1CorrectedPFMetMuonEnDown","patType1CorrectedPFMetMuonEnUp","patType1CorrectedPFMetTauEnDown","patType1CorrectedPFMetTauEnUp","patType1CorrectedPFMetUnclusteredEnDown","patType1CorrectedPFMetUnclusteredEnUp"]),
    useForDefaultAlias = cms.untracked.bool(False)

) 
