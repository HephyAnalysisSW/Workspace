# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step3 --filein file:step2_RAW2DIGI_L1Reco_RECO_EI.root --mc --eventcontent MINIAODSIM --runUnscheduled --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --conditions 74X_mcRun2_asymptotic_v2 --step PAT --python_filename step3_miniAOD_cfg.py --no_exec -n 1920
import FWCore.ParameterSet.Config as cms


samples={
          '300_270': {'outputFiles':['T2DegStop_300_270_RunII_25ns_miniAOD.root'] ,  "outputDatasetTag": 'T2DegStop_300_270',
                       'inputDataset': '/T2DegStop_300_270_GEN-SIM/nrad-T2DegStop_300_270_RECO-RunIISpring15-MCRUN2_74_V9-25ns-cdcc155817963320a88c2dd6cf768461/USER',
                        'testfile': 'root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/nrad/T2DegStop_300_270_GEN-SIM/T2DegStop_300_270_RECO-RunIISpring15-MCRUN2_74_V9-25ns/cdcc155817963320a88c2dd6cf768461/step2_RAW2DIGI_L1Reco_RECO_EI_100_1_iG9.root',
                        },
          '300_270FS': {'outputFiles':['T2DegStop_300_270_RunII_FastSim_miniAOD.root'] ,  "outputDatasetTag": 'T2DegStop_300_270',
                       'inputDataset': '/T2DegStop_300_270_FastSim_v3/mzarucki-T2DegStop_300_270_FastSim_v3-420683af1bb5170fe0b35a3c8f09b1ec/USER',
                        'testfile': 'root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/mzarucki/T2DegStop_300_270_FastSim_v3/T2DegStop_300_270_FastSim_v3/151123_113332/0000/T2DegStop_300_270_FastSim_v3_415.root',
                        },
          '300_290FS': {'outputFiles':['T2DegStop_300_290_RunII_FastSim_miniAOD.root'] ,  "outputDatasetTag": 'T2DegStop_300_290FS',
                       'inputDataset':   '/T2DegStop_300_290_FastSim_v3/mzarucki-T2DegStop_300_290_FastSim_v3-420683af1bb5170fe0b35a3c8f09b1ec/USER' },
          '300_240FS': {'outputFiles':['T2DegStop_300_240_RunII_FastSim_miniAOD.root'] ,  "outputDatasetTag": 'T2DegStop_300_240FS',
                       'inputDataset': '/T2DegStop_300_240_FastSim_v3/mzarucki-T2DegStop_300_240_FastSim_v3-420683af1bb5170fe0b35a3c8f09b1ec/USER' }
        }


sample=samples['300_240FS']

if 'fastsim' in sample['inputDataset'].lower():
  print "Processing MiniAODv2 for FastSim"
  isFastSim=True
else:
  isFastSim=False


process = cms.Process('PAT')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
if isFastSim:
  process.load('FastSimulation.Configuration.EventContent_cff')
  process.load('FastSimulation.Configuration.Geometries_MC_cff')
else:
  process.load('Configuration.EventContent.EventContent_cff')
  process.load('Configuration.StandardSequences.GeometryRecoDB_cff')




process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(20)
)

# Input source
process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring('root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/nrad/T2DegStop_300_270_GEN-SIM/T2DegStop_300_270_RECO-RunIISpring15-MCRUN2_74_V9-25ns/cdcc155817963320a88c2dd6cf768461/step2_RAW2DIGI_L1Reco_RECO_EI_100_1_iG9.root'),
    #fileNames = cms.untracked.vstring(sample['testfile']),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step3 nevts:1920'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.MINIAODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('MINIAODSIM'),
        filterName = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fastCloning = cms.untracked.bool(False),
    fileName = cms.untracked.string(sample['outputFiles'][0]),
    outputCommands = process.MINIAODSIMEventContent.outputCommands,
    overrideInputFileSplitLevels = cms.untracked.bool(True)
)
# Additional output definition
process.MINIAODSIMoutput.outputCommands += cms.untracked.vstring("keep *_genParticles_*_*")

# Other statements
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '74X_mcRun2_asymptotic_v2', '')

# Path and EndPath definitions
process.Flag_trkPOG_toomanystripclus53X = cms.Path(~process.toomanystripclus53X)
process.Flag_EcalDeadCellBoundaryEnergyFilter = cms.Path(process.EcalDeadCellBoundaryEnergyFilter)
process.Flag_HBHENoiseIsoFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseIsoFilter)
process.Flag_trackingFailureFilter = cms.Path(process.goodVertices+process.trackingFailureFilter)
process.Flag_goodVertices = cms.Path(process.primaryVertexFilter)
process.Flag_hcalLaserEventFilter = cms.Path(process.hcalLaserEventFilter)
process.Flag_CSCTightHaloFilter = cms.Path(process.CSCTightHaloFilter)
process.Flag_trkPOGFilters = cms.Path(process.trkPOGFilters)
process.Flag_eeBadScFilter = cms.Path(process.eeBadScFilter)
process.Flag_trkPOG_manystripclus53X = cms.Path(~process.manystripclus53X)
process.Flag_METFilters = cms.Path(process.metFilters)
process.Flag_trkPOG_logErrorTooManyClusters = cms.Path(~process.logErrorTooManyClusters)
process.Flag_HBHENoiseFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseFilter)
process.Flag_EcalDeadCellTriggerPrimitiveFilter = cms.Path(process.EcalDeadCellTriggerPrimitiveFilter)
process.Flag_ecalLaserCorrFilter = cms.Path(process.ecalLaserCorrFilter)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.Flag_HBHENoiseFilter,process.Flag_HBHENoiseIsoFilter,process.Flag_CSCTightHaloFilter,process.Flag_hcalLaserEventFilter,process.Flag_EcalDeadCellTriggerPrimitiveFilter,process.Flag_EcalDeadCellBoundaryEnergyFilter,process.Flag_goodVertices,process.Flag_eeBadScFilter,process.Flag_ecalLaserCorrFilter,process.Flag_trkPOGFilters,process.Flag_trkPOG_manystripclus53X,process.Flag_trkPOG_toomanystripclus53X,process.Flag_trkPOG_logErrorTooManyClusters,process.Flag_METFilters,process.endjob_step,process.MINIAODSIMoutput_step)

# customisation of the process.

if isFastSim:
  # Automatic addition of the customisation function from FastSimulation.Configuration.MixingModule_Full2Fast
  from FastSimulation.Configuration.MixingModule_Full2Fast import prepareDigiRecoMixing
  #call to customisation function prepareDigiRecoMixing imported from FastSimulation.Configuration.MixingModule_Full2Fast
  process = prepareDigiRecoMixing(process)



# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.postLS1Customs
from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 

#call to customisation function customisePostLS1 imported from SLHCUpgradeSimulations.Configuration.postLS1Customs
process = customisePostLS1(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions
#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)
process.load('Configuration.StandardSequences.PATMC_cff')
from FWCore.ParameterSet.Utilities import cleanUnscheduled
process=cleanUnscheduled(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.PatAlgos.slimming.miniAOD_tools
from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllMC 

#call to customisation function miniAOD_customizeAllMC imported from PhysicsTools.PatAlgos.slimming.miniAOD_tools
process = miniAOD_customizeAllMC(process)


if isFastSim:
  # Automatic addition of the customisation function from PhysicsTools.PatAlgos.slimming.metFilterPaths_cff
  from PhysicsTools.PatAlgos.slimming.metFilterPaths_cff import miniAOD_customizeMETFiltersFastSim

  #call to customisation function miniAOD_customizeMETFiltersFastSim imported from PhysicsTools.PatAlgos.slimming.metFilterPaths_cff
  process = miniAOD_customizeMETFiltersFastSim(process)
  

# End of customisation functions
