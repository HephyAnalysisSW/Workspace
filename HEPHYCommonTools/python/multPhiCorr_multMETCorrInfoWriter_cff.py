import FWCore.ParameterSet.Config as cms

from Workspace.HEPHYCommonTools.multPhiCorr_multMETCorrInfoWriter_53X_cfi import multPhiCorr_multMETCorrInfoWriter_53X

##____________________________________________________________________________||

pfMEtMultCorrInfoWriter = cms.EDAnalyzer("multMETCorrInfoWriter",
    srcPFlow = cms.InputTag('particleFlow', ''),
    parameters = multPhiCorr_multMETCorrInfoWriter_53X
)

pfMEtMultCorrInfoWriterSequence = cms.Sequence( pfMEtMultCorrInfoWriter )


