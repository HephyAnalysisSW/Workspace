#Configuration file fragment used for GenHTFilter module initalisation (GeneratorInterface/GenFilters/GenHTFilter/plugins/GenHTFilter.cc)

import FWCore.ParameterSet.Config as cms

genHTFilter = cms.EDFilter("GenHTFilter",
   src = cms.InputTag("ak4GenJetsNoNu"), #GenJet collection as input
   jetPtCut = cms.double(30.0), #GenJet pT cut for HT
   jetEtaCut = cms.double(4.5), #GenJet eta cut for HT
   genHTcut = cms.double(160.0) #GenHT cut
)
