# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: Configuration/GenProduction/python/SUS-RunIISpring15FSPremix-00002-fragment.py --filein root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/nrad/lhe/merged/T2DegStop2j_300_270_merged.lhe --pileup_input dbs:/Neutrino_E-10_gun/RunIISpring15PrePremix-MCRUN2_74_V9-v1/GEN-SIM-DIGI-RAW --mc --eventcontent AODSIM --fast --customise SLHCUpgradeSimulations/Configuration/postLS1CustomsPreMixing.customisePostLS1 --datatier AODSIM --conditions MCRUN2_74_V9 --beamspot NominalCollision2015 --step GEN,SIM,RECOBEFMIX,DIGIPREMIX_S2:pdigi_valid,DATAMIX,L1,L1Reco,RECO,HLT:@frozen25ns --magField 38T_PostLS1 --datamix PreMix --no_exec --python_filename fastSim_filtered_cfg.py -n 1500000 --fileout T2DegStop_300_270_FastSim.root
import FWCore.ParameterSet.Config as cms

process = cms.Process('HLT')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('FastSimulation.Configuration.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('FastSimulation.Configuration.Geometries_MC_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedNominalCollision2015_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('FastSimulation.Configuration.SimIdeal_cff')
process.load('FastSimulation.Configuration.Reconstruction_BefMix_cff')
process.load('FastSimulation.Configuration.DigiDMPreMix_cff')
process.load('SimGeneral.MixingModule.digi_MixPreMix_cfi')
process.load('FastSimulation.Configuration.DataMixerPreMix_cff')
process.load('FastSimulation.Configuration.SimL1Emulator_cff')
process.load('FastSimulation.Configuration.L1Reco_cff')
process.load('FastSimulation.Configuration.Reconstruction_AftMix_cff')
process.load('HLTrigger.Configuration.HLT_25ns14e33_v1_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('GeneratorInterface.GenFilters.genHTFilter_cfi')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("LHESource",
    fileNames = cms.untracked.vstring('root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/nrad/lhe/merged/T2DegStop2j_300_270_merged.lhe')
)

process.options = cms.untracked.PSet(
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('Configuration/GenProduction/python/SUS-RunIISpring15FSPremix-00002-fragment.py nevts:1500000'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition
process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('AODSIM'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fileName = cms.untracked.string('T2DegStop_300_270_FastSim.root'),
    outputCommands = process.AODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
process.mix.digitizers = cms.PSet(process.theDigitizersMixPreMixValid)
process.mixData.input.fileNames = cms.untracked.vstring(['/store/mc/RunIISpring15PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MCRUN2_74_V9-v1/20000/0021F46D-ED25-E511-9376-0025905B8576.root', '/store/mc/RunIISpring15PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MCRUN2_74_V9-v1/20000/0040E519-2226-E511-A1C9-002618FDA277.root', '/store/mc/RunIISpring15PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MCRUN2_74_V9-v1/20000/00458809-B226-E511-952B-002354EF3BE0.root', '/store/mc/RunIISpring15PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MCRUN2_74_V9-v1/20000/00946A66-4726-E511-BA1E-0025905A60F2.root', '/store/mc/RunIISpring15PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MCRUN2_74_V9-v1/20000/009FA86E-5F26-E511-A542-003048FFD732.root', '/store/mc/RunIISpring15PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MCRUN2_74_V9-v1/20000/00AE3880-B826-E511-9B01-00261894394F.root', '/store/mc/RunIISpring15PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MCRUN2_74_V9-v1/20000/00AF43F2-2B26-E511-BC56-0025905A6088.root', '/store/mc/RunIISpring15PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MCRUN2_74_V9-v1/20000/00B5E935-3C26-E511-A7DF-0025905B85D6.root', '/store/mc/RunIISpring15PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MCRUN2_74_V9-v1/20000/00CC8235-3C26-E511-8D60-0025905A60F4.root', '/store/mc/RunIISpring15PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/MCRUN2_74_V9-v1/20000/00D70232-4126-E511-B79A-0025905938A4.root'])
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_74_V9', '')

process.generator = cms.EDFilter("Pythia8HadronizerFilter",
    PythiaParameters = cms.PSet(
        JetMatchingParameters = cms.vstring('JetMatching:setMad = off', 
            'JetMatching:scheme = 1', 
            'JetMatching:merge = on', 
            'JetMatching:jetAlgorithm = 2', 
            'JetMatching:etaJetMax = 5.', 
            'JetMatching:coneRadius = 1.', 
            'JetMatching:slowJetPower = 1', 
            'JetMatching:qCut = 50.', # 116 previously 
            'JetMatching:nQmatch = 5', 
            'JetMatching:nJetMax = 2', 
            'JetMatching:doShowerKt = off'),
        parameterSets = cms.vstring('pythia8CommonSettings', 
            'pythia8CUEP8M1Settings', 
            'JetMatchingParameters'),
        pythia8CUEP8M1Settings = cms.vstring('Tune:pp 14', 
            'Tune:ee 7', 
            'MultipartonInteractions:pT0Ref=2.4024', 
            'MultipartonInteractions:ecmPow=0.25208', 
            'MultipartonInteractions:expPow=1.6'),
        pythia8CommonSettings = cms.vstring('Tune:preferLHAPDF = 2', 
            'Main:timesAllowErrors = 10000', 
            'Check:epTolErr = 0.01', 
            'Beams:setProductionScalesFromLHEF = off', 
            'SLHA:keepSM = on', 
            'SLHA:minMassSM = 1000.', 
            'ParticleDecays:limitTau0 = on', 
            'ParticleDecays:tau0Max = 10', 
            'ParticleDecays:allowPhotonRadiation = on')
    ),
    comEnergy = cms.double(13000.0),
    filterEfficiency = cms.untracked.double(1.0),
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(1)
)

#genMET filter
process.genMETfilter1 = cms.EDFilter("CandViewSelector",
   src = cms.InputTag("genMetTrue"),
   cut = cms.string("pt > 60")
)

process.genMETfilter2 = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("genMETfilter1"),
    minNumber = cms.uint32(1),
    )

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.reconstruction_befmix_step = cms.Path(process.reconstruction_befmix)
process.digitisation_step = cms.Path(process.pdigi_valid)
process.datamixing_step = cms.Path(process.pdatamix)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

process.filter_step = cms.Sequence(process.genHTFilter + process.genMETfilter1 * process.genMETfilter2)
process.ProductionFilterSequence = cms.Sequence(process.generator + process.pgen + process.filter_step)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.simulation_step,process.reconstruction_befmix_step,process.digitisation_step,process.datamixing_step,process.L1simulation_step,process.L1Reco_step,process.reconstruction_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.endjob_step,process.AODSIMoutput_step])

# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq 

# customisation of the process.

# Automatic addition of the customisation function from FastSimulation.Configuration.MixingModule_Full2Fast
from FastSimulation.Configuration.MixingModule_Full2Fast import prepareDigiRecoMixing 

#call to customisation function prepareDigiRecoMixing imported from FastSimulation.Configuration.MixingModule_Full2Fast
process = prepareDigiRecoMixing(process)

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.postLS1CustomsPreMixing
from SLHCUpgradeSimulations.Configuration.postLS1CustomsPreMixing import customisePostLS1 

#call to customisation function customisePostLS1 imported from SLHCUpgradeSimulations.Configuration.postLS1CustomsPreMixing
process = customisePostLS1(process)

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforFastSim 

#call to customisation function customizeHLTforFastSim imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforFastSim(process)

# End of customisation functions
