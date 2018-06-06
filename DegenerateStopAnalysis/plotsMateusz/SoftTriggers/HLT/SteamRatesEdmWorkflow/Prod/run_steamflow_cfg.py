# Import HLT configuration #
import os,sys
import importlib
from hlt_config import *

# STEAM Customization #

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('standard')
options.register('sampName',    'none',   VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "sampName")
options.register('fileSize',    'none',   VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "fileSize")

if not 'ipython' in VarParsing.sys.argv[0]:
  options.parseArguments()
else:
  print "No parsing of arguments!"

# Options

sampName = options.sampName
fileSize = options.fileSize

menuVersion = 'V26'
hackConditions = False
nEvents = -1                    # number of events to process
switchL1PS = False              # apply L1 PS ratios to switch to tighter column
columnL1PS = 1                  # choose the tighter column ( 0 <=> tightest )
outputName = "hlt_SoftTriggers-%s_%s"%(menuVersion,sampName)  # output file name

savedir = "outputSamples/SoftTriggers-%s/%s"%(menuVersion,sampName)

if not os.path.isdir(savedir): os.makedirs(savedir)

if hackConditions:
    outputName += "_hackedL1PS"
else:
    outputName += "_originalL1PS"

if switchL1PS:
    outputName += "_switchL1PSTrue"
else:
    outputName += "_switchL1PSFalse"

inputFilesFile = 'Workspace.DegenerateStopAnalysis.inputFiles.inputFiles_%s'%sampName
inputFiles = importlib.import_module(inputFilesFile)
inputFileNames = inputFiles.inputFileNames

if fileSize == "vsmall":
    numInputFiles = 5
elif fileSize == "small":
    numInputFiles = 20
elif fileSize == "medium":
    numInputFiles = 50
elif fileSize == "large":
    numInputFiles = 100
elif fileSize == "vlarge":
    numInputFiles = 500
else:
    numInputFiles = len(inputFileNames)
    fileSize = 'full'
    print "Processing full sample list."

outputName += "_" + fileSize

if numInputFiles > len(inputFileNames):
    print "Number of files smaller than requested. Exiting."
    sys.exit()
else: 
    inputFileNames = inputFileNames[:numInputFiles]

# Input
#from list_cff import inputFileNames
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(inputFileNames),
    inputCommands = cms.untracked.vstring('keep *')
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( nEvents )
)
# Hack conditions
if hackConditions:
    process.load('L1Trigger.L1TGlobal.hackConditions_cff')
    process.L1TGlobalPrescalesVetos.PrescaleXMLFile = cms.string('prescale-slim.xml') #NOTE: located in $CMSSW_BASE/src/L1Trigger/L1TGlobal/data/Luminosity/startup
    process.L1TGlobalPrescalesVetos.FinOrMaskXMLFile = cms.string('mask-slim.xml')    #NOTE: located in $CMSSW_BASE/src/L1Trigger/L1TGlobal/data/Luminosity/startup
    process.simGtStage2Digis.AlgorithmTriggersUnmasked = cms.bool(False)
    process.simGtStage2Digis.AlgorithmTriggersUnprescaled = cms.bool(False)
    process.simGtStage2Digis.PrescaleSet = cms.uint32(4)

# L1 customizations
from HLTrigger.Configuration.common import *
import itertools

def insert_modules_after(process, target, *modules):
    "Add the `modules` after the `target` in any Sequence, Paths or EndPath that contains the latter."                                                      
    for sequence in itertools.chain(
        process._Process__sequences.itervalues(),
        process._Process__paths.itervalues(),
        process._Process__endpaths.itervalues()
    ):                                                                                                                                                      
        try:
            position = sequence.index ( target )
        except ValueError:
            continue
        else:
            for module in reversed(modules):
                sequence.insert(position+1, module)

process.l1tGlobalPrescaler = cms.EDFilter('L1TGlobalPrescaler',
  l1tResults = cms.InputTag('hltGtStage2Digis'),
  mode = cms.string('applyColumnRatios'),
  l1tPrescaleColumn = cms.uint32(columnL1PS)
)                                                                                                                                                           

if switchL1PS:
    insert_modules_after(process, process.hltGtStage2Digis, process.l1tGlobalPrescaler )
                                                                                                                                                            
    for module in filters_by_type(process, 'HLTL1TSeed'):
        module.L1GlobalInputTag = 'l1tGlobalPrescaler'

    for module in filters_by_type(process, 'HLTPrescaler'):
        module.L1GtReadoutRecordTag = 'l1tGlobalPrescaler'

#Setup FWK for multithreaded
process.options.numberOfThreads=cms.untracked.uint32(8)
process.options.numberOfStreams=cms.untracked.uint32(8)

# Output
process.DQMOutput.remove(process.dqmOutput)

process.hltOutput = cms.OutputModule( "PoolOutputModule",
     fileName = cms.untracked.string( "%s/%s.root"%(savedir,outputName)),
     fastCloning = cms.untracked.bool( False ),
     dataset = cms.untracked.PSet(
     filterName = cms.untracked.string( "" ),
     dataTier = cms.untracked.string( "RAW" )
                        ),
     outputCommands = cms.untracked.vstring( 'drop *',
         'keep edmTriggerResults_*_*_MYHLT',
         )
     )

process.HLTOutput = cms.EndPath( process.hltOutput )
