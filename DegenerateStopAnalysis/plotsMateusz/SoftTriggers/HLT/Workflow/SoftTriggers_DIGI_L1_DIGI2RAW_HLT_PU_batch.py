# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: SoftTriggers --filein root://hephyse.oeaw.ac.at//store/user/mzarucki/T2tt_dM-10to80_mStop-500_mLSP-460_privGridpack_GEN-SIM/T2tt_dM-10to80_mStop-500_mLSP-460_privGridpack_GEN-SIM/180122_170545/0000/T2tt_dM-10to80_mStop-500_mLSP-460_privGridpack_GEN-SIM_1.root --fileout file:T2tt_dM-10to80_mStop-500_mLSP-460_SoftTriggers-V31_HLT_PU.root --step=DIGI,L1,DIGI2RAW,HLT:SoftTriggers_92X --processName=SoftTriggers --datatier GEN-SIM-RAW --eventcontent RAWSIM --conditions 92X_upgrade2017_realistic_v12 --era Run2_2017 --geometry DB:Extended --beamspot Realistic25ns13TeVEarly2017Collision --mc --pileup 2016_25ns_Moriond17MC_PoissonOOTPU --pileup_input dbs:/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIISummer17GS-92X_upgrade2017_realistic_v2-v1/GEN-SIM --customise_commands process.mix.input.nbPileupEvents.probFunctionVariable = cms.vint32(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62) \n process.mix.input.nbPileupEvents.probValue = cms.vdouble(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571)\n process.simHcalDigis.markAndPass = cms.bool(True) --nThreads 8 -n 100 --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('standard')
options.register('infile',    'none',   VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "infile")
options.register('outfile',   'none',   VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "outfile")

if not 'ipython' in VarParsing.sys.argv[0]:
  options.parseArguments()
else:
  print "No parsing of arguments!"

process = cms.Process('SoftTriggers',eras.Run2_2017)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mix_2016_25ns_Moriond17MC_PoissonOOTPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('HLTrigger.Configuration.HLT_SoftTriggers_92X_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    fileNames = cms.untracked.vstring(options.infile),
    inputCommands = cms.untracked.vstring('keep *', 
        'drop *_genParticles_*_*', 
        'drop *_genParticlesForJets_*_*', 
        'drop *_kt4GenJets_*_*', 
        'drop *_kt6GenJets_*_*', 
        'drop *_iterativeCone5GenJets_*_*', 
        'drop *_ak4GenJets_*_*', 
        'drop *_ak7GenJets_*_*', 
        'drop *_ak8GenJets_*_*', 
        'drop *_ak4GenJetsNoNu_*_*', 
        'drop *_ak8GenJetsNoNu_*_*', 
        'drop *_genCandidatesForMET_*_*', 
        'drop *_genParticlesForMETAllVisible_*_*', 
        'drop *_genMetCalo_*_*', 
        'drop *_genMetCaloAndNonPrompt_*_*', 
        'drop *_genMetTrue_*_*', 
        'drop *_genMetIC5GenJs_*_*'),
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

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-RAW'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(20971520),
    fileName = cms.untracked.string(options.outfile),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
process.mix.input.fileNames = cms.untracked.vstring(['/store/mc/RunIISummer17GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/92X_upgrade2017_realistic_v2-v1/110000/0011034F-EF64-E711-B578-549F358EB7B0.root', '/store/mc/RunIISummer17GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/92X_upgrade2017_realistic_v2-v1/110000/002BE35D-FF64-E711-A47F-001E67A42A71.root', '/store/mc/RunIISummer17GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/92X_upgrade2017_realistic_v2-v1/110000/00317390-FF64-E711-83A9-0242AC130002.root', '/store/mc/RunIISummer17GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/92X_upgrade2017_realistic_v2-v1/110000/003FA495-1565-E711-8231-008CFAF28E5C.root', '/store/mc/RunIISummer17GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/92X_upgrade2017_realistic_v2-v1/110000/004B8009-0A65-E711-8ACF-A0369F7F8E80.root', '/store/mc/RunIISummer17GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/92X_upgrade2017_realistic_v2-v1/110000/00592ECC-0365-E711-948C-0242AC130002.root', '/store/mc/RunIISummer17GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/92X_upgrade2017_realistic_v2-v1/110000/008F0204-1765-E711-972E-001E67DDC119.root', '/store/mc/RunIISummer17GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/92X_upgrade2017_realistic_v2-v1/110000/00F6FA7E-1965-E711-8FE8-02163E014B89.root', '/store/mc/RunIISummer17GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/92X_upgrade2017_realistic_v2-v1/110000/0232888F-1065-E711-876B-B499BAAC0694.root', '/store/mc/RunIISummer17GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/92X_upgrade2017_realistic_v2-v1/110000/0288B8B7-0265-E711-94F7-001E67DFF519.root'])
from HLTrigger.Configuration.CustomConfigs import ProcessName
process = ProcessName(process)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '92X_upgrade2017_realistic_v12', '')

# Path and EndPath definitions
process.digitisation_step = cms.Path(process.pdigi)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.digitisation_step,process.L1simulation_step,process.digi2raw_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.endjob_step,process.RAWSIMoutput_step])
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
process.options.numberOfThreads=cms.untracked.uint32(8)
process.options.numberOfStreams=cms.untracked.uint32(8)

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

# End of customisation functions

# Customisation from command line

process.mix.input.nbPileupEvents.probFunctionVariable = cms.vint32(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62) 
process.mix.input.nbPileupEvents.probValue = cms.vdouble(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571)
process.simHcalDigis.markAndPass = cms.bool(True)
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
