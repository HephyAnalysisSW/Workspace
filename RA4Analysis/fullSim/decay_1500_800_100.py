import FWCore.ParameterSet.Config as cms

process = cms.Process("PROD")

process.load("Configuration.StandardSequences.SimulationRandomNumberGeneratorSeeds_cff")
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.maxEvents = cms.untracked.PSet(
	    input = cms.untracked.int32(-1)
)

# The following three lines reduce the clutter of repeated printouts
# of the same exception message.
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.destinations = ['cerr']
process.MessageLogger.statistics = []
process.MessageLogger.fwkJobReports = []
process.MessageLogger.cerr.FwkReport.reportEvery = 10000


process.source = cms.Source("LHESource",
fileNames = cms.untracked.vstring(
'root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/schoef/lhe/13TeV_GoGo_run1_1500_800_100.lhe',
)
)

#from Configuration.Generator.PythiaUEZ2Settings_cfi import *
from Configuration.Generator.PythiaUED6TSettings_cfi import *

process.generator = cms.EDFilter("Pythia6HadronizerFilter",
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(10),
    pythiaPylistVerbosity = cms.untracked.int32(20),
    comEnergy = cms.double(13000.0),
    pythiaToLHE = cms.bool(True),
    PythiaParameters = cms.PSet(
        pythiaUESettingsBlock,
        processParameters = cms.vstring(
'MSEL=0',
'IMSS(1)=11',
#'IMSS(22)=33',##FIXME
'MSTJ(1)=1       ! Fragmentation/hadronization on or off',
'MSTP(161)=67',
'MSTP(162)=68',
'MSTP(163)=69',
),
        SLHAParameters = cms.vstring(
		'SLHAFILE = Workspace/RA4Analysis/data/test_param_card_T5lnu_1500_800_100_AllDecays.dat'
#    'SLHAFILE = Workspace/RA4Analysis/data/param_card_T5lnu_template.dat'
#		'SLHAFILE = Configuration/Generator/data/CSA07SUSYBSM_LM9p_sftsdkpyt_slha.out'
#    'SLHAFILE = Workspace/RA4Analysis/data/lesya.dat'
        ),
        parameterSets = cms.vstring('pythiaUESettings', 
            'processParameters','SLHAParameters')
    ),
   jetMatching = cms.untracked.PSet(
        MEMAIN_nqmatch = cms.int32(5),
        MEMAIN_showerkt = cms.double(0),
        MEMAIN_minjets = cms.int32(0),
        MEMAIN_qcut = cms.double(50),
        MEMAIN_excres = cms.string(''),
        MEMAIN_etaclmax = cms.double(5),
        outTree_flag = cms.int32(0),
        scheme = cms.string('Madgraph'),
        MEMAIN_maxjets = cms.int32(2),
        mode = cms.string('auto')
    )

)

#from IOMC.RandomEngine.RandomServiceHelper import  RandomNumberServiceHelper
#randHelper =  RandomNumberServiceHelper(process.RandomNumberGeneratorService)
#randHelper.populate()

#process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
#    moduleSeeds = cms.PSet(
#        generator = cms.untracked.uint32(123456789),
#        g4SimHits = cms.untracked.uint32(123456788),
#        VtxSmeared = cms.untracked.uint32(123456789)
#    ),
#)


process.RandomNumberGeneratorService = cms.Service(

     "RandomNumberGeneratorService",

     # This is to initialize the random engine of the source
     generator = cms.PSet(
         initialSeed = cms.untracked.uint32(123456789),
         engineName = cms.untracked.string('TRandom3')
     ),

     # This is to initialize the random engines used for  Famos
     VtxSmeared = cms.PSet(
         initialSeed = cms.untracked.uint32(123456789),
         engineName = cms.untracked.string('TRandom3')
     ),
     g4SimHits = cms.PSet(
         initialSeed = cms.untracked.uint32(123456789),
         engineName = cms.untracked.string('TRandom3')
     ))


process.printGenParticles = cms.EDAnalyzer("ParticleListDrawer",
     src = cms.InputTag("genParticles"),
     maxEventsToPrint = cms.untracked.int32(10)
)


process.out = cms.OutputModule("PoolOutputModule",
     #verbose = cms.untracked.bool(True),
     SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('pp') ),
     fileName = cms.untracked.string('histo.root'),
#     outputCommands = cms.untracked.vstring()
     outputCommands = cms.untracked.vstring('keep *') 
)

process.outpath = cms.EndPath(process.out)


process.pp = cms.Path(process.generator*process.genParticles*process.printGenParticles)

process.schedule = cms.Schedule(process.pp, process.outpath)

