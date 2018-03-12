import FWCore.ParameterSet.Config as cms

from DQMOffline.Trigger.SusyMonitor_cfi import hltSUSYmonitoring

# HLT_Mu3er1p5_PFJet100er2p5_PFMETX_PFMHTX_IDTight (X = 70, 80, 90)
SoftMuPlusHardJetSUSYmonitoring = hltSUSYmonitoring.clone()
SoftMuPlusHardJetSUSYmonitoring.FolderName = cms.string('HLT/SUSY/SoftMuPlusHardJet/')

SoftMuPlusHardJetSUSYmonitoring.numGenericTriggerEventPSet.hltInputTag = cms.InputTag("TriggerResults","","HLT")
SoftMuPlusHardJetSUSYmonitoring.numGenericTriggerEventPSet.hltPaths = cms.vstring(\
    "HLT_Mu3er1p5_PFJet100er2p5_PFMET70_PFMHT70_IDTight_v*",\
    "HLT_Mu3er1p5_PFJet100er2p5_PFMET80_PFMHT80_IDTight_v*",\
    "HLT_Mu3er1p5_PFJet100er2p5_PFMET90_PFMHT90_IDTight_v*" \
)

SoftMuPlusHardJetSUSYmonitoring.met   = cms.InputTag("pfMetEI") # pfMet
SoftMuPlusHardJetSUSYmonitoring.jets  = cms.InputTag("ak4PFJetsCHS") # ak4PFJets, ak4PFJetsCHS, pfJetsEI
SoftMuPlusHardJetSUSYmonitoring.muons = cms.InputTag("muons") # while pfIsolatedMuonsEI are reco::PFCandidate !

SoftMuPlusHardJetSUSYmonitoring.HTdefinition     = cms.string('pt>30 & abs(eta)<2.5')
SoftMuPlusHardJetSUSYmonitoring.leptJetDeltaRmin = cms.double(0.4)
SoftMuPlusHardJetSUSYmonitoring.MHTdefinition    = cms.string('pt>30 & abs(eta)<2.4')

###############
### Muon pt ###
###############
SoftMuPlusHardJetSUSYmonitoring_muPt            = SoftMuPlusHardJetSUSYmonitoring.clone()
SoftMuPlusHardJetSUSYmonitoring_muPt.FolderName = cms.string('HLT/SUSY/SoftMuPlusHardJet/Muon')

## Selection ##
SoftMuPlusHardJetSUSYmonitoring_muPt.denGenericTriggerEventPSet.hltPaths = cms.vstring('HLT_PFMET140_PFMHT140_v*')
# Muon selection
SoftMuPlusHardJetSUSYmonitoring_muPt.nmuons       = cms.uint32(1)
SoftMuPlusHardJetSUSYmonitoring_muPt.muoSelection = cms.string('abs(eta)<1.5')
# Jet selection
SoftMuPlusHardJetSUSYmonitoring_muPt.njets = cms.uint32(1)
SoftMuPlusHardJetSUSYmonitoring_muPt.jetSelection = cms.string("pt>130 & abs(eta)<2.5")
#SoftMuPlusHardJetSUSYmonitoring_muPt.jetId = cms.string("loose")
# MET selection
SoftMuPlusHardJetSUSYmonitoring_muPt.metSelection = cms.string('pt>150')
SoftMuPlusHardJetSUSYmonitoring_muPt.MHTcut       = cms.double(150)

## Binning ##
SoftMuPlusHardJetSUSYmonitoring_muPt.histoPSet.muPtBinning = cms.vdouble(0,2,5,7,10,12,15,17,20,25,30,50)

##############
### Jet pt ###
##############
SoftMuPlusHardJetSUSYmonitoring_jetPt = SoftMuPlusHardJetSUSYmonitoring.clone()
SoftMuPlusHardJetSUSYmonitoring_jetPt.FolderName = cms.string('HLT/SUSY/SoftMuPlusHardJet/Jet')

## Selection ##
SoftMuPlusHardJetSUSYmonitoring_jetPt.denGenericTriggerEventPSet.hltPaths = cms.vstring('HLT_IsoMu27_v*')
# Muon selection
SoftMuPlusHardJetSUSYmonitoring_jetPt.nmuons       = cms.uint32(1)
SoftMuPlusHardJetSUSYmonitoring_jetPt.muoSelection = cms.string('pt>10 & abs(eta)<1.5')
# Jet selection
SoftMuPlusHardJetSUSYmonitoring_jetPt.njets        = cms.uint32(1)
SoftMuPlusHardJetSUSYmonitoring_jetPt.jetSelection = cms.string("abs(eta)<2.5")
#SoftMuPlusHardJetSUSYmonitoring_jetPt.jetId        = cms.string("loose")
# MET selection
SoftMuPlusHardJetSUSYmonitoring_jetPt.metSelection  = cms.string('pt>150')
SoftMuPlusHardJetSUSYmonitoring_jetPt.MHTcut        = cms.double(150)

##############
### MET pt ###
##############
SoftMuPlusHardJetSUSYmonitoring_metPt = SoftMuPlusHardJetSUSYmonitoring.clone()
SoftMuPlusHardJetSUSYmonitoring_metPt.FolderName = cms.string('HLT/SUSY/SoftMuPlusHardJet/MET')

## Selection ##
SoftMuPlusHardJetSUSYmonitoring_metPt.denGenericTriggerEventPSet.hltPaths = cms.vstring('HLT_IsoMu27_v*')
# Muon selection
SoftMuPlusHardJetSUSYmonitoring_metPt.nmuons       = cms.uint32(1)
SoftMuPlusHardJetSUSYmonitoring_metPt.muoSelection = cms.string('pt>10 & abs(eta)<1.5')
# Jet selection
SoftMuPlusHardJetSUSYmonitoring_metPt.njets        = cms.uint32(1)
SoftMuPlusHardJetSUSYmonitoring_metPt.jetSelection = cms.string("pt>130 & abs(eta)<2.5")
#SoftMuPlusHardJetSUSYmonitoring_metPt.jetId        = cms.string("loose")
# MET selection
#SoftMuPlusHardJetSUSYmonitoring_metPt.MHTcut = cms.double(150)

susyHLTSoftMuPlusHardJetMonitoring = cms.Sequence(
    SoftMuPlusHardJetSUSYmonitoring_muPt
  + SoftMuPlusHardJetSUSYmonitoring_jetPt
  + SoftMuPlusHardJetSUSYmonitoring_metPt
)

