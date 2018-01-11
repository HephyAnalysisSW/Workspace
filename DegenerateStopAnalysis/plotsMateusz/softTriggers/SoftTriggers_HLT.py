# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: SoftTriggers --filein file:/afs/hephy.at/data/mzarucki02/TriggerStudies/CMSSW_9_2_12/GEN-SIM-RAW/T2tt_dM-10to80_privGridpack_LHE-GEN-SIM-RAW_mStop-500_mLSP-460_noPU/T2tt_dM-10to80_privGridpack_LHE-GEN-SIM-RAW_mStop-500_mLSP-460_noPU_1.root --fileout file:/afs/hephy.at/data/mzarucki02/TriggerStudies/CMSSW_9_2_12/HLT/T2tt_dM-10to80_mStop-500_mLSP-460_noPU_SoftTriggers_HLT.root --step=HLT:SoftTriggers_92X --processName=SoftTriggers --datatier GEN-SIM-RAW --eventcontent RAWSIM --conditions 92X_upgrade2017_realistic_v12 --era Run2_2017 --geometry DB:Extended --beamspot Realistic25ns13TeVEarly2017Collision --mc -n 100 --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('SoftTriggers',eras.Run2_2017)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('HLTrigger.Configuration.HLT_SoftTriggers_92X_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/afs/hephy.at/data/mzarucki02/TriggerStudies/CMSSW_9_2_12/GEN-SIM-RAW/T2tt_dM-10to80_privGridpack_LHE-GEN-SIM-RAW_mStop-500_mLSP-460_noPU/T2tt_dM-10to80_privGridpack_LHE-GEN-SIM-RAW_mStop-500_mLSP-460_noPU_1.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('SoftTriggers nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition
process.RAWSIMEventContent.outputCommands.append('keep bool_*_HLT*_*')
process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-RAW'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(20971520),
    fileName = cms.untracked.string('file:/afs/hephy.at/data/mzarucki02/TriggerStudies/CMSSW_9_2_12/HLT/T2tt_dM-10to80_mStop-500_mLSP-460_noPU_SoftTriggers_HLT.root'),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition
process.trigDec = cms.EDProducer('TriggerDecisionAnalyzer')
process.trigDec_step = cms.EndPath(process.trigDec)

# Other statements
from HLTrigger.Configuration.CustomConfigs import ProcessName
process = ProcessName(process)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '92X_upgrade2017_realistic_v12', '')

# Path and EndPath definitions
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

# Schedule definition
process.schedule = cms.Schedule()
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.endjob_step, process.trigDec_step, process.RAWSIMoutput_step])

from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
