import FWCore.ParameterSet.Config as cms
process = cms.Process("test")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(3000) )
process.source = cms.Source(
    'PoolSource',
#    fileNames = cms.untracked.vstring('root://xrootd.unl.edu//store/relval/CMSSW_7_0_5/RelValTTbar_13/GEN-SIM-RECO/POSTLS170_V6-v3/00000/0423767B-B5DD-E311-A1E0-02163E00E5B5.root')
#    fileNames = cms.untracked.vstring('root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_5/RelValTTbar_13/GEN-SIM-RECO/POSTLS170_V6-v3/00000/0423767B-B5DD-E311-A1E0-02163E00E5B5.root')
#/store/relval/CMSSW_7_0_5/RelValTTbar_13/GEN-SIM-RECO/POSTLS170_V7-v3/00000/F6768EBC-98DD-E311-B7DB-02163E00E7E8.root
#    fileNames = cms.untracked.vstring('file:/data/schoef/local/TTJets-53X-syncfile-AODSIM.root')
    fileNames = cms.untracked.vstring('file:/data/schoef/local/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola_PU20bx25_POSTLS170_V5-v1_AODSIM.root')
    )

process.TFileService = cms.Service("TFileService", fileName = cms.string("histo.root") ,
      closeFileFast = cms.untracked.bool(True))

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'POSTLS170_V6::All'
#process.GlobalTag.globaltag = 'START53_V7F::All'
process.load('Workspace.HEPHYCMSSWTools.multPhiCorr_multMETCorrInfoWriter_cff')

#
# RUN!
#
process.run = cms.Path(
  process.pfMEtMultCorrInfoWriterSequence
)


