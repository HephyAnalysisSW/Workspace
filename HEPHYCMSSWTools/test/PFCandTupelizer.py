import FWCore.ParameterSet.Config as cms
process = cms.Process("test")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
process.source = cms.Source(
    'PoolSource',
#    fileNames = cms.untracked.vstring('root://xrootd.unl.edu//store/relval/CMSSW_7_0_5/RelValTTbar_13/GEN-SIM-RECO/POSTLS170_V6-v3/00000/0423767B-B5DD-E311-A1E0-02163E00E5B5.root')
    fileNames = cms.untracked.vstring('root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_5/RelValTTbar_13/GEN-SIM-RECO/POSTLS170_V6-v3/00000/0423767B-B5DD-E311-A1E0-02163E00E5B5.root')
#/store/relval/CMSSW_7_0_5/RelValTTbar_13/GEN-SIM-RECO/POSTLS170_V7-v3/00000/F6768EBC-98DD-E311-B7DB-02163E00E7E8.root
    )


import Workspace.HEPHYCMSSWTools.PFCandTupelizer_cff

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'POSTLS170_V6::All'
process.load('Workspace.HEPHYCMSSWTools.PFCandTupelizer_cff')
#process.load('Workspace.HEPHYCMSSWTools.CaloTowersTupelizer_cff')

process.out = cms.OutputModule("PoolOutputModule",
     #verbose = cms.untracked.bool(True),
     fileName = cms.untracked.string('histo.root'),
     outputCommands = cms.untracked.vstring('drop *', 'keep *_*PFCandTupelizer*_*_*', 'keep *_*CaloTowersTupelizer*_*_*')
)


#
# RUN!
#
process.p = cms.Path(
  process.PFCandTupelizer
#  process.CaloTowersTupelizer
)


process.outpath = cms.EndPath(process.out)
