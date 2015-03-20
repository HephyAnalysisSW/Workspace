# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step3 --filein file:/data/schoef/local/WJetsToLNu_HT-400to600_Tune4C_13TeV-madgraph-tauola_AODSIM_PU20bx25_PHYS14_25_V1-v1.root --fileout file:histo.root --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions PHYS14_ST_V1 --step PAT --python_filename miniAOD_DAS.py --no_exec -n 77
import FWCore.ParameterSet.Config as cms

process = cms.Process('PAT')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
#    fileNames = cms.untracked.vstring('file:/data/schoef/local/CMSSW_7_2_0_pre4_RelValZMM_13_GEN-SIM-RECO_PU25ns_POSTLS172_V3-v3.root')
#    fileNames = cms.untracked.vstring('file:/data/schoef/local/DYJetsToLL_M-50_13TeV-madgraph-pythia8_AODSIM_PU20bx25_PHYS14_25_V1-v1.root')
    fileNames = cms.untracked.vstring('file:/data/schoef/local/DYJetsToLL_M-50_HT-100to200_Tune4C_13TeV-madgraph-tauola_PU20bx25_PHYS14_25_V1-v1_AODSIM_Phys14DR.root')
#    fileNames = cms.untracked.vstring('root://xrootd.unl.edu//store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU30bx50_PHYS14_25_V1-v1/00000/003B6371-8D81-E411-8467-003048F0E826.root')
)

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.19 $'),
    annotation = cms.untracked.string('step3 nevts:77'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.MINIAODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionLevel = cms.untracked.int32(4),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    outputCommands = process.MINIAODSIMEventContent.outputCommands,
    fileName = cms.untracked.string('file:histo.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('MINIAODSIM')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    fastCloning = cms.untracked.bool(False),
    overrideInputFileSplitLevels = cms.untracked.bool(True)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'PHYS14_ST_V1', '')

# Path and EndPath definitions
process.endjob_step = cms.EndPath(process.endOfProcess)
process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)

#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)
process.load('Configuration.StandardSequences.PATMC_cff')

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.PatAlgos.slimming.miniAOD_tools
from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllMC 

#call to customisation function miniAOD_customizeAllMC imported from PhysicsTools.PatAlgos.slimming.miniAOD_tools
process = miniAOD_customizeAllMC(process)

process.load('Workspace.HEPHYCMSSWTools.EventCounter')
#
process.filterSequence = cms.Sequence(
    process.EventCounter
)

process.patRAWMETs=process.patMETs.clone(metSource=cms.InputTag("pfMet"))
process.slimmedRAWMETs = process.slimmedMETs.clone(src=cms.InputTag("patRAWMETs"))#,type1p2Uncertainties=cms.InputTag(""))
process.load('JetMETCorrections.Type1MET.correctionTermsPfMetMult_cff')
process.load('JetMETCorrections.Type1MET.correctedMet_cff')
process.patTxyMETs=process.patMETs.clone(metSource=cms.InputTag("pfMetMultCorr"))
process.slimmedTxyMETs = process.slimmedMETs.clone(src=cms.InputTag("patTxyMETs"))#,type1p2Uncertainties=cms.InputTag(""))
process.pfMetT1Txy = process.pfMetT1.clone(src=cms.InputTag("pfMetMultCorr"))
process.patT1TxyMETs=process.patMETs.clone(metSource=cms.InputTag("pfMetT1Txy"))
process.slimmedT1TxyMETs = process.slimmedMETs.clone(src=cms.InputTag("patT1TxyMETs"))#,type1p2Uncertainties=cms.InputTag(""))

process.metSequence = cms.Sequence(
  process.patRAWMETs*
  process.slimmedRAWMETs*
  process.pfMETMultShiftCorrSequence*
  process.pfMetMultCorr*
  process.patTxyMETs*
  process.slimmedTxyMETs*
  process.pfMetT1Txy*
  process.patT1TxyMETs*
  process.slimmedT1TxyMETs
)

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
                                   src = cms.InputTag("genParticles"),                                                                 
                                   printP4 = cms.untracked.bool(False),
                                   printPtEtaPhi = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(False),
                                   printStatus = cms.untracked.bool(True),
                                   printIndex = cms.untracked.bool(False),
                                   status = cms.untracked.vint32( [1,2,3] )
                                   )

process.miniAODTupelizerSequence = cms.Sequence()
process.load('Workspace.HEPHYCMSSWTools.BasicTupelizer_miniAOD_cfi')
process.BasicTupelizer.useForDefaultAlias = cms.untracked.bool(True)
process.BasicTupelizer.addMSugraOSETInfo = cms.untracked.bool(False)
process.BasicTupelizer.verbose = cms.untracked.bool(False)
process.BasicTupelizer.metsToMonitor =  cms.untracked.vstring('slimmedMETs', 'slimmedTxyMETs','slimmedRAWMETs','slimmedT1TxyMETs')
process.miniAODTupelizerSequence += process.BasicTupelizer
process.load('Workspace.HEPHYCMSSWTools.JetTupelizer_miniAOD_cfi')
process.JetTupelizer.useForDefaultAlias = cms.untracked.bool(True)
process.JetTupelizer.verbose = cms.untracked.bool(False)
process.miniAODTupelizerSequence += process.JetTupelizer
process.load('Workspace.HEPHYCMSSWTools.MuonTupelizer_miniAOD_cfi')
process.MuonTupelizer.useForDefaultAlias = cms.untracked.bool(True)
process.miniAODTupelizerSequence += process.MuonTupelizer
process.MuonTupelizer.verbose = cms.untracked.bool(False)
process.load('Workspace.HEPHYCMSSWTools.ElectronTupelizer_miniAOD_cfi')
process.ElectronTupelizer.useForDefaultAlias = cms.untracked.bool(True)
process.ElectronTupelizer.verbose = cms.untracked.bool(False)
process.miniAODTupelizerSequence += process.ElectronTupelizer
process.load('Workspace.HEPHYCMSSWTools.TauTupelizer_miniAOD_cfi')
process.TauTupelizer.useForDefaultAlias = cms.untracked.bool(True)
process.TauTupelizer.verbose = cms.untracked.bool(False)
process.miniAODTupelizerSequence += process.TauTupelizer
process.load('Workspace.HEPHYCMSSWTools.TriggerTupelizer_cfi')
process.TriggerTupelizer.useForDefaultAlias = cms.untracked.bool(True)
#process.TriggerTupelizer.verbose = cms.untracked.bool(options.verbose)
process.miniAODTupelizerSequence += process.TriggerTupelizer
process.load('Workspace.HEPHYCMSSWTools.FilterTupelizer_cfi')
process.FilterTupelizer.useForDefaultAlias = cms.untracked.bool(True)
#process.FilterTupelizer.verbose = cms.untracked.bool(options.verbose)
process.miniAODTupelizerSequence += process.FilterTupelizer
#process.load('Workspace.HEPHYCMSSWTools.PFCandTupelizer_cff')
#process.miniAODTupelizerSequence += process.PFCandTupelizer
#process.PFCandTupelizer.useForDefaultAlias = cms.untracked.bool(True)
#process.PFCandTupelizer.fillIsolatedChargedHadrons = cms.untracked.bool(True)

process.p = cms.Path(process.filterSequence + process.metSequence + process.miniAODTupelizerSequence)

#process.p+=process.printTree

process.MINIAODSIMoutput.outputCommands =  cms.untracked.vstring('drop *', 'keep *_*Tupelizer*_*_*' , 'keep *_*EventCounter*_*_*')
