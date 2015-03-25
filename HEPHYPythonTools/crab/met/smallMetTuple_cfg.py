import FWCore.ParameterSet.Config as cms

##____________________________________________________________________________||
process = cms.Process("TEST")

##____________________________________________________________________________||
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

##____________________________________________________________________________||
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

##____________________________________________________________________________||
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType1Type2_cff")
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType0PFCandidate_cff")
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType0RecoTrack_cff")
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetShiftXY_cff")

# process.corrPfMetShiftXY.parameter = process.pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_data
process.corrPfMetShiftXY.parameter = process.pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_mc

##____________________________________________________________________________||
process.load('JetMETCorrections.Type1MET.correctionTermsPfMetMult_cff')
process.load('JetMETCorrections.Type1MET.correctedMet_cff')

##____________________________________________________________________________||
from JetMETCorrections.Type1MET.testInputFiles_cff import corrMETtestInputFiles
process.source = cms.Source(
    "PoolSource",
#    fileNames = cms.untracked.vstring(corrMETtestInputFiles)
    fileNames = cms.untracked.vstring('file:/data/schoef/local/CMSSW_7_2_0_pre4_RelValZMM_13_GEN-SIM-RECO_PU25ns_POSTLS172_V3-v3.root')
#    fileNames = cms.untracked.vstring('root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_2_2_patch1/RelValTTbar_13/GEN-SIM-RECO/PU25ns_MCRUN2_72_V1-v1/00000/0EB681C0-8173-E411-BBB0-0025905A6094.root')
    )

##____________________________________________________________________________||
process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('histo.root'),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring(
        'keep *',
        'keep recoPFMETs_*_*_*',
#        'keep *_*_*_TEST',
        'keep recoMuons_muons_*_*'  

        )
    )

##____________________________________________________________________________||
process.options   = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.MessageLogger.cerr.FwkReport.reportEvery = 50
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))

##____________________________________________________________________________||
process.p = cms.Path(
  process.pfMETMultShiftCorrSequence*
  process.pfMetMultCorr
    )

process.e1 = cms.EndPath(
    process.out
    )

##____________________________________________________________________________||
