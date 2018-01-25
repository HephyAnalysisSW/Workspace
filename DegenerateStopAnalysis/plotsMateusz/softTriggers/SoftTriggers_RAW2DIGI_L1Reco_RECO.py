# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: SoftTriggers --filein root://hephyse.oeaw.ac.at//store/user/mzarucki/T2tt_dM-10to80_mStop-500_mLSP-460_privGridpack_GEN-SIM/T2tt_dM-10to80_mStop-500_mLSP-460_HLT_SoftTriggers-V15/180124_005336/0000/T2tt_dM-10to80_mStop-500_mLSP-460_HLT_SoftTriggers-V15_1.root --fileout file:T2tt_dM-10to80_mStop-500_mLSP-460_SoftTriggers-V15_AODSIM.root --step RAW2DIGI,L1Reco,RECO --datatier AODSIM --eventcontent AODSIM --conditions 92X_upgrade2017_realistic_v12 --era Run2_2017 --geometry DB:Extended --beamspot Realistic25ns13TeVEarly2017Collision --mc --nThreads 4 -n 100 --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('standard')
options.register('mStop',    'none',   VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "stop mass")
options.register('mLSP',     'none',   VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "LSP mass")

if not 'ipython' in VarParsing.sys.argv[0]:
  options.parseArguments()
else:
  print "No parsing of arguments!"

process = cms.Process('RECO',eras.Run2_2017)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('root://hephyse.oeaw.ac.at//store/user/mzarucki/T2tt_dM-10to80_mStop-500_mLSP-460_privGridpack_GEN-SIM/T2tt_dM-10to80_mStop-500_mLSP-460_HLT_SoftTriggers-V15/180124_005336/0000/T2tt_dM-10to80_mStop-500_mLSP-460_HLT_SoftTriggers-V15_1.root'),
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

process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('AODSIM'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fileName = cms.untracked.string('file:T2tt_dM-10to80_mStop-%s_mLSP-%s_SoftTriggers-V15_AODSIM.root'%(options.mStop,options.mLSP)),
    outputCommands = process.AODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '92X_upgrade2017_realistic_v12', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.AODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
process.options.numberOfThreads=cms.untracked.uint32(4)
process.options.numberOfStreams=cms.untracked.uint32(0)


# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
