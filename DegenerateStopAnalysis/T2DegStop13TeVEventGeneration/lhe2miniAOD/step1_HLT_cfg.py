# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step1 --filein dbs:/T2DegStop2j_300_270_GENSIM/nrad-T2DegStop2j_300_270_GENSIM-edbe023d17b99f8a8fbdf4e576e17580/USER --fileout file:T2DegStop2j_300_270_GENSIMHLT_step1.root --pileup_input dbs:/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIIFall14GS-MCRUN2_71_V1-v3/GEN-SIM --mc --eventcontent RAWSIM --pileup Flat_20_50_50ns --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --conditions MCRUN2_73_V9 --step DIGI,L1,DIGI2RAW,HLT:GRun --magField 38T_PostLS1 --python_filename step1_HLT_cfg.py --no_exec

#To be used in CMSSW 7_3_0_patch1

import FWCore.ParameterSet.Config as cms

process = cms.Process('HLT')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mix_Flat_20_50_50ns_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('HLTrigger.Configuration.HLT_GRun_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(500)
)

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
    fileNames = cms.untracked.vstring(['root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/nrad/T2DegStop2j_300_270_GENSIM/T2DegStop2j_300_270_GENSIM/edbe023d17b99f8a8fbdf4e576e17580/T2DegStop2j_300_270_GENSIM_1_1_cYt.root'])
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.19 $'),
    annotation = cms.untracked.string('step1 nevts:1'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    fileName = cms.untracked.string('file:T2DegStop2j_300_270_GEN-SIM-HLT_step1.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-RAW')
    )
)

# Additional output definition

# Other statements
process.mix.input.fileNames = cms.untracked.vstring([\
                                    'root://xrootd.unl.edu//store/mc/RunIIFall14GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v3/00000/001A2454-4871-E411-96DE-001CC416C686.root', 
                                    'root://xrootd.unl.edu//store/mc/RunIIFall14GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v3/00000/008CF00C-4271-E411-8466-001F296544A8.root', 
                                    'root://xrootd.unl.edu//store/mc/RunIIFall14GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v3/00000/0098B0C6-4D71-E411-A1FF-0025905A60D2.root', 
                                    'root://xrootd.unl.edu//store/mc/RunIIFall14GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v3/00000/00C5DD2C-4771-E411-AC2F-0025905A60BE.root', 
                                    'root://xrootd.unl.edu//store/mc/RunIIFall14GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v3/00000/00C6A3EC-3D71-E411-8804-549F35AD8B95.root', 
                                    'root://xrootd.unl.edu//store/mc/RunIIFall14GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v3/00000/00DC78A7-4271-E411-BD0B-001EC9B080CD.root', 
                                    'root://xrootd.unl.edu//store/mc/RunIIFall14GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v3/00000/00E0A2FF-2A71-E411-AB78-BCAEC5567FD2.root', 
                                    'root://xrootd.unl.edu//store/mc/RunIIFall14GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v3/00000/0219E11C-4471-E411-9E90-0025905A612A.root', 
                                    'root://xrootd.unl.edu//store/mc/RunIIFall14GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v3/00000/02517B21-4571-E411-975F-9CB65404FBA0.root', 
                                    'root://xrootd.unl.edu//store/mc/RunIIFall14GS/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v3/00000/0259A65C-4A71-E411-9469-0025905B860E.root'
                                    ])
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_73_V9', '')

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

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.postLS1Customs
from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 

#call to customisation function customisePostLS1 imported from SLHCUpgradeSimulations.Configuration.postLS1Customs
process = customisePostLS1(process)

# End of customisation functions

