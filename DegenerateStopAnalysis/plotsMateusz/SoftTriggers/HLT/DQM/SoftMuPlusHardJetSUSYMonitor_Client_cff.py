import FWCore.ParameterSet.Config as cms
from DQMServices.Core.DQMEDHarvester import DQMEDHarvester

SoftMuPlusHardJetEfficiency_muPt = DQMEDHarvester("DQMGenericClient",
    subDirs        = cms.untracked.vstring("HLT/SUSY/SoftMuPlusHardJet/Muon/*"),
    verbose        = cms.untracked.uint32(0), # Set to 2 for all messages
    resolution     = cms.vstring(),
    efficiency     = cms.vstring(\
        "effic_muPt  'Efficiency vs Muon pt;  Muon p_{T} [GeV]; efficiency' muPt_1_numerator                  muPt_1_variableBinning_denominator",
        "effic_muEta 'Efficiency vs Muon eta; Muon #eta ;       efficiency' muEta_1_variableBinning_numerator muEta_1_variableBinning_denominator",
        "effic_muPhi 'Efficiency vs Muon phi; Muon #phi ;       efficiency' muPhi_1_numerator                 muPhi_1_denominator",
    ),
)

SoftMuPlusHardJetEfficiency_jetPt = DQMEDHarvester("DQMGenericClient",
    subDirs        = cms.untracked.vstring("HLT/SUSY/SoftMuPlusHardJet/Jet/*"),
    verbose        = cms.untracked.uint32(0), # Set to 2 for all messages
    resolution     = cms.vstring(),
    efficiency     = cms.vstring(\
        "effic_jetPt   'Jet p_{T} turnON; PFJet p_{T} [GeV]; efficiency' jetPt_1_numerator  jetPt_1_denominator",
        "effic_jetEta  'Jet #eta turnON;  Jet #eta;          efficiency' jetEta_1_numerator jetEta_1_denominator",
        
    ),
)

SoftMuPlusHardJetEfficiency_metPt = DQMEDHarvester("DQMGenericClient",
    subDirs        = cms.untracked.vstring("HLT/SUSY/SoftMuPlusHardJet/MET/*"),
    verbose        = cms.untracked.uint32(0), # Set to 2 for all messages
    resolution     = cms.vstring(),
    efficiency     = cms.vstring(\
        "effic_metPt   'MET turnON; PF MET [GeV]; efficiency' met_numerator met_denominator",
        
    ),
)

susyHLTSoftMuPlusHardJetClient = cms.Sequence(
    SoftMuPlusHardJetEfficiency_muPt
  + SoftMuPlusHardJetEfficiency_jetPt
  + SoftMuPlusHardJetEfficiency_metPt 
)
