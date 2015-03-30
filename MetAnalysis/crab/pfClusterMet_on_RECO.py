import FWCore.ParameterSet.Config as cms
##____________________________________________________________________________||
process = cms.Process("TEST")
##____________________________________________________________________________||
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("RecoJets.JetProducers.PFClustersForJets_cff")
process.load("RecoMET/METProducers/PFClusterMET_cfi")
##____________________________________________________________________________||
process.source = cms.Source(
"PoolSource",
#RelValTTbar 50ns, CMSSW_7_0_6_patch1_RelValTTbar_13_PU50ns_PLS170_V6AN1-v1
#fileNames = cms.untracked.vstring([
#  'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_6_patch1/RelValTTbar_13/GEN-SIM-RECO/PU50ns_PLS170_V6AN1-v1/00000/5837198B-7502-E411-8625-0025905A60B4.root',
#  'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_6_patch1/RelValTTbar_13/GEN-SIM-RECO/PU50ns_PLS170_V6AN1-v1/00000/72592496-8202-E411-8FF9-002590593920.root',
#  'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_6_patch1/RelValTTbar_13/GEN-SIM-RECO/PU50ns_PLS170_V6AN1-v1/00000/A2D11BEF-7A02-E411-AF7B-0025905A6076.root',
#  'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_6_patch1/RelValTTbar_13/GEN-SIM-RECO/PU50ns_PLS170_V6AN1-v1/00000/D6DC951D-8902-E411-8BB8-002618943951.root',
#  'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_6_patch1/RelValTTbar_13/GEN-SIM-RECO/PU50ns_PLS170_V6AN1-v1/00000/DC1D7A36-7C02-E411-BB4B-0025905A60D0.root',
#  'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_6_patch1/RelValTTbar_13/GEN-SIM-RECO/PU50ns_PLS170_V6AN1-v1/00000/DCA39610-7802-E411-9C3B-00261894396E.root',
#  'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_6_patch1/RelValTTbar_13/GEN-SIM-RECO/PU50ns_PLS170_V6AN1-v1/00000/EA9E7EAF-7902-E411-8133-0025905A60D2.root',
#])
##RelValTTbar 25ns, CMSSW_7_0_6_patch1_RelValTTbar_13_PU25ns_PLS170_V7AN1-v1
#fileNames = cms.untracked.vstring([
#  'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_6_patch1/RelValTTbar_13/GEN-SIM-RECO/PU25ns_PLS170_V7AN1-v1/00000/08E71464-8702-E411-86E9-002590596490.root',
#  'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_6_patch1/RelValTTbar_13/GEN-SIM-RECO/PU25ns_PLS170_V7AN1-v1/00000/84E76E47-7D02-E411-ACCF-0025905A6118.root',
#  'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_6_patch1/RelValTTbar_13/GEN-SIM-RECO/PU25ns_PLS170_V7AN1-v1/00000/A26542C4-7202-E411-AD3B-002618943901.root',
#  'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_6_patch1/RelValTTbar_13/GEN-SIM-RECO/PU25ns_PLS170_V7AN1-v1/00000/C696B887-7502-E411-A806-0026189438B0.root',
#  'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_6_patch1/RelValTTbar_13/GEN-SIM-RECO/PU25ns_PLS170_V7AN1-v1/00000/E6C67B67-7302-E411-AE53-0026189438AC.root'
#])

#CMSSW_7_0_6_patch1_RelValZMM_13_GEN-SIM-RECO_PLS170_V7AN1-v1
fileNames = cms.untracked.vstring([
'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_6_patch1/RelValZMM_13/GEN-SIM-RECO/PLS170_V7AN1-v1/00000/862FBA61-8702-E411-8EE8-003048D25BA6.root',
'root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_6_patch1/RelValZMM_13/GEN-SIM-RECO/PLS170_V7AN1-v1/00000/A84981D0-8302-E411-97DF-00261894386C.root'
])

)
##____________________________________________________________________________||
process.out = cms.OutputModule(
"PoolOutputModule",
#fileName = cms.untracked.string('file:CMSSW_7_0_6_patch1_RelValTTbar_13_PU50ns_PLS170_V6AN1-v1.root'),
#fileName = cms.untracked.string('file:CMSSW_7_0_6_patch1_RelValTTbar_13_PU25ns_PLS170_V7AN1-v1.root'),
fileName = cms.untracked.string('file:CMSSW_7_0_6_patch1_RelValZMM_13_GEN-SIM-RECO_PLS170_V7AN1-v1.root'),
SelectEvents = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
outputCommands = cms.untracked.vstring(
'drop *',
'keep *_corMetGlobalMuons_*_*',
'keep *_met_*_*',
'keep *_pfMet_*_*',
'keep *_*_*_TEST'
)
)
##____________________________________________________________________________||
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.MessageLogger.cerr.FwkReport.reportEvery = 50
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
##____________________________________________________________________________||
process.p = cms.Path(
process.pfClusterRefsForJetsHCAL*
process.pfClusterRefsForJetsECAL*
process.pfClusterRefsForJets *
process.pfClusterMet
)
process.e1 = cms.EndPath(
process.out
)
