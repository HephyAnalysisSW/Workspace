import FWCore.ParameterSet.Config as cms

from Workspace.HEPHYCMSSWTools.multPhiCorr_multMETCorrInfoWriter_cfi import multPhiCorr_multMETCorrInfoWriter

##____________________________________________________________________________||

pfMEtMultCorrInfoWriter = cms.EDAnalyzer("multMETCorrInfoWriter",
    srcPFlow = cms.InputTag('particleFlow', ''),
    parameters = multPhiCorr_multMETCorrInfoWriter
)

pfMEtMultCorrInfoWriterSequence = cms.Sequence( pfMEtMultCorrInfoWriter )


