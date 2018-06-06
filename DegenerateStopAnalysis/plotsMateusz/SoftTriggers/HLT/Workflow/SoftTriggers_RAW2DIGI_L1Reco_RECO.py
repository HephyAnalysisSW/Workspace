# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: SoftTriggers --filein root://hephyse.oeaw.ac.at//store/user/mzarucki/T2tt_dM-10to80_mStop-500_mLSP-460_privGridpack_GEN-SIM/T2tt_dM-10to80_mStop-500_mLSP-460_HLT_SoftTriggers-V17/180124_005336/0000/T2tt_dM-10to80_mStop-500_mLSP-460_HLT_SoftTriggers-V17_1.root --fileout file:T2tt_dM-10to80_mStop-500_mLSP-460_SoftTriggers-V17_AODSIM.root --step RAW2DIGI,L1Reco,RECO --datatier AODSIM --eventcontent AODSIM --conditions 92X_upgrade2017_realistic_v12 --era Run2_2017 --geometry DB:Extended --beamspot Realistic25ns13TeVEarly2017Collision --mc --nThreads 4 -n 100 --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('standard')
options.register('outputName',    'none',   VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "outputName")

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
    fileNames = cms.untracked.vstring('file:file.root'),
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
hltFilterBranches = [\
    'keep triggerTriggerEventWithRefs_*_*_*',
    'keep triggerTriggerEvent_*_*_*',
    'keep triggerTriggerFilterObjectWithRefs_*_*_*',
]

hltProductBranches = [\
    'keep *_hltAK4CaloJets_*_*',
    'keep *_hltAK4PFJetsCorrected_*_*',
    'keep *_hltAK4PFJets_*_*',
    'keep *_hltL2Muons_*_*',
    'keep *_hltL3Muons_*_*',
    'keep *_hltMet_*_*',
]

process.AODSIMEventContent.outputCommands.remove('drop *_hlt*_*_*')
process.AODSIMEventContent.outputCommands.extend(hltFilterBranches)
process.AODSIMEventContent.outputCommands.extend(hltProductBranches)

process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('AODSIM'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fileName = cms.untracked.string('file:%s.root'%options.outputName),
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
process.options.numberOfThreads=cms.untracked.uint32(8)
process.options.numberOfStreams=cms.untracked.uint32(8)


# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
