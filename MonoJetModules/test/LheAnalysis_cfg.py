#
# cfg file to run the LheAnalysis analyzer
#

import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
import sys

process = cms.Process('LheAnalysis')

#
# parsing of command line parameters & default values for parameters
#   all these arguments can be overwritten on command line
# https://twiki.cern.ch/twiki/bin/view/CMS/CommandLineOptions
# 
options = VarParsing.VarParsing ('standard')

# event sample: data, FullSim, FastSim (default)
options.register ('eventSample',
                  'FastSim',
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                  "Type of event sample to run on: data, FullSim, FastSim (default)")

# event tier: AOD (default), RECO
options.register ('eventTier',
                  'AOD',
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                  "Tier of event sample to run on: AOD (default), RECO")

# global tag to be used
options.register ('GTag',
                  'auto:startup',
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                  "Global Tag")
    
# number of events 
options.maxEvents = 10

options.output = 'LheAnalysis.root'

# end of options

#
if options.GTag.count('auto') :
    from Configuration.AlCa.autoCond import autoCond
    useGlobalTag = autoCond[options.GTag.replace('auto:', '')]
else :
    useGlobalTag = options.GTag+'::All'
    
print "\n Using global tag ", useGlobalTag, "\n"

# parse arguments from command line (it might overwrite the default values)
if not 'ipython' in VarParsing.sys.argv[0]:
  options.parseArguments()
else:
  print "No parsing of arguments!"


#
# input and output 
#
# for parameters, see
#   https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideEDMParametersForModules

# input source
#

options.files = [  
            'file:/data/DegenerateLightStop/LocalFiles/cms/store/mc/Summer12/SMS-T2DegenerateStop_2J_mStop-175to225_mLSP-95to215_TuneZ2star_8TeV-madgraph-tauolapp/AODSIM/START53_V19_FSIM_PU_S12-v1/00000/FE6DF0C6-05A1-E311-93CA-7845C4FC39AA.root'                     
        ]
secFiles = cms.untracked.vstring() 
selectedEvents = cms.untracked.VEventRange()
selectedLumis= cms.untracked.VLuminosityBlockRange()

process.source = cms.Source ('PoolSource', 
                    fileNames = cms.untracked.vstring(options.files), 
                    secondaryFileNames = secFiles,
                    lumisToProcess = selectedLumis,
                    eventsToProcess = selectedEvents,
                    duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
                    )


# number of events to be processed and source file
process.maxEvents = cms.untracked.PSet(
    input=cms.untracked.int32(options.maxEvents)
)

#
# output module
#
# some parameters will be overwritten at the end of the file
# patSequences_cff needs the module defined before it can be included

process.output = cms.OutputModule('PoolOutputModule',
        fileName = cms.untracked.string(options.output),
        dropMetaData = cms.untracked.string('ALL'),
        outputCommands = cms.untracked.vstring('drop *')
        )

# exception configuration
process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound', )
)


#
# load and configure modules via Global Tag
# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions
#
# add also the geometry and the magnetic field configuration
#
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = useGlobalTag

#
# processes to be run
#

process.schedule = cms.Schedule()

# LheAnalysis analyzer
process.load('Workspace.MonoJetModules.lheAnalysis_cfi')

process.lheAnalysisPath = cms.Path(process.lheAnalysis)
process.output.outputCommands.extend(cms.untracked.vstring('keep *_lheAnalysis_*_' + process.name_()))
#
process.schedule.extend([process.lheAnalysisPath])

# output final parameters 
print "\n  outputCommands used for ", options.eventSample, " sample:\n ", process.output.outputCommands

process.outpath = cms.EndPath(process.output)
#
process.schedule.extend([process.outpath])
print "\n  schedule for ", options.eventSample, " sample:\n ", process.schedule




# Message Logger
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.debugModules = ['lheAnalysis']
process.MessageLogger.categories.append('LheAnalysis')
process.MessageLogger.categories.append('ParserLheModelString')
process.MessageLogger.destinations = ['LheAnalysis_error', 
                                      'LheAnalysis_warning', 
                                      'LheAnalysis_info', 
                                      'LheAnalysis_debug'
                                      ]

process.MessageLogger.cerr.default.limit = 0
process.MessageLogger.cerr.FwkJob.limit = 0
process.MessageLogger.cerr.FwkReport.limit = 0
process.MessageLogger.cerr.FwkSummary.limit = 0

process.MessageLogger.LheAnalysis_debug = cms.untracked.PSet( 
        threshold = cms.untracked.string('DEBUG'),
        DEBUG = cms.untracked.PSet( limit = cms.untracked.int32(0) ),
        INFO = cms.untracked.PSet( limit = cms.untracked.int32(0) ),
        WARNING = cms.untracked.PSet( limit = cms.untracked.int32(0) ),
        ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) ),
        ParserLheModelString = cms.untracked.PSet( limit = cms.untracked.int32(-1) ),
        LheAnalysis = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
        )

process.MessageLogger.LheAnalysis_info = cms.untracked.PSet( 
        threshold = cms.untracked.string('INFO'),
        INFO = cms.untracked.PSet( limit = cms.untracked.int32(0) ),
        WARNING = cms.untracked.PSet( limit = cms.untracked.int32(0) ),
        ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) ),
        LheAnalysis = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
        )

process.MessageLogger.LheAnalysis_warning = cms.untracked.PSet( 
        threshold = cms.untracked.string('WARNING'),
        WARNING = cms.untracked.PSet( limit = cms.untracked.int32(0) ),
        ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) ),
        ParserLheModelString = cms.untracked.PSet( limit = cms.untracked.int32(-1) ),
        LheAnalysis = cms.untracked.PSet( limit = cms.untracked.int32(-1) ) 
        )

process.MessageLogger.LheAnalysis_error = cms.untracked.PSet( 
        threshold = cms.untracked.string('ERROR'),
        ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) ),
        ParserLheModelString = cms.untracked.PSet( limit = cms.untracked.int32(-1) ),
        LheAnalysis = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
        )


# dump python configuration
file = open('LheAnalysisCfgDump_cfg.py','w')
file.write(str(process.dumpPython()))
file.close()


