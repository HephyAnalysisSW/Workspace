import FWCore.ParameterSet.Config as cms

#from Workspace.HEPHYCMSSWTools.multPhiCorr_multMETCorrInfoWriter_CSA14_cfi import multPhiCorr_multMETCorrInfoWriter
from Workspace.HEPHYCMSSWTools.multPhiCorr_multMETCorrInfoWriter_PHYS14_cfi import multPhiCorr_multMETCorrInfoWriter_PHYS14 as multPhiCorr_multMETCorrInfoWriter

##____________________________________________________________________________||

pfMEtMultCorrInfoWriter = cms.EDAnalyzer("multMETCorrInfoWriter",
    vertexCollection = cms.untracked.InputTag('offlinePrimaryVertices'),
    srcPFlow = cms.InputTag('particleFlow', ''),
    parameters = multPhiCorr_multMETCorrInfoWriter
)
pfMEtMultCorrInfoWriterSequence = cms.Sequence( pfMEtMultCorrInfoWriter )
