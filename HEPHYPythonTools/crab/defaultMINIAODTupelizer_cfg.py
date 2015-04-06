import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("Tupelizer")
options = VarParsing.VarParsing ('standard')

options.register ('mode','mc',
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "Switch between MC, data and SMS")

options.register ('hltName','HLT',
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "HLT Trigger collection")

options.register ('GT','POSTLS170_V5::All',
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "Global Tag")

options.register ('outfile','histo.root',
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "outfile")

options.register ('triggers','*',
          VarParsing.VarParsing.multiplicity.list,
          VarParsing.VarParsing.varType.string,
          "Trigger requirement")

options.register ('triggersToMonitor','',
          VarParsing.VarParsing.multiplicity.list,
          VarParsing.VarParsing.varType.string,
          "Trigger list to monitor")

options.register ('verbose',False,
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.bool,
          "verbosity")

options.register ('keep','',
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "additional keep statements")
#options.register ('addPDFWeights',False,
#          VarParsing.VarParsing.multiplicity.singleton,
#          VarParsing.VarParsing.varType.bool,
#          "whether or not to add pdfWeights")

#infiles = ['root://xrootd.unl.edu//store/mc/Spring14dr/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola/AODSIM/PU20bx25_POSTLS170_V5-v1/00000/00165B45-82E6-E311-B68D-002590AC4FEC.root']
#infiles = ['file:/data/schoef/local/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_PU20bx25_POSTLS170_V5-v1_MINIAODSIM.root']
#infiles = ['root://eoscms.cern.ch//eos/cms/store/relval/CMSSW_7_0_5/RelValTTbar_13/GEN-SIM-RECO/POSTLS170_V6-v3/00000/0423767B-B5DD-E311-A1E0-02163E00E5B5.root']
#infiles = ['file:/afs/hephy.at/scratch/s/schoefbeck/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_PU20bx25_POSTLS170_V5-v1_MINIAODSIM.root']
#infiles = ['file:/data/nrad/local/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola_PU20bx25_POSTLS170_V5-v1_AODSIMPuppiMiniAOD.root']
infiles=['root://xrootd.unl.edu//store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU30bx50_PHYS14_25_V1-v1/00000/003B6371-8D81-E411-8467-003048F0E826.root']
options.files=infiles

options.mode = 'mc'
options.maxEvents=10

if not 'ipython' in VarParsing.sys.argv[0]:
  options.parseArguments()
else:
  print "No parsing of arguments!"

isMC = (options.mode.lower()=='sms' or options.mode.lower()=='mc')
if options.keep!='':
  toKeep = ['keep '+x for x in options.keep.split(',')]
else:
  toKeep=[]
print "mode",options.mode,"isMC?",isMC, ", verbose?",options.verbose,'keep?', toKeep, "GT",options.GT, ", triggers", options.triggers#, 'addPDFWeights?',options.addPDFWeights

#-- Message Logger ------------------------------------------------------------
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options = cms.untracked.PSet(
  SkipEvent = cms.untracked.vstring('ProductNotFound'),
  wantSummary = cms.untracked.bool(False),
  allowUnscheduled = cms.untracked.bool( True )
)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.categories.append('PATSummaryTables')
process.MessageLogger.cerr.PATSummaryTables = cms.untracked.PSet(
    limit = cms.untracked.int32(-1),
    reportEvery = cms.untracked.int32(100)
)

#-- Source information ------------------------------------------------------
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.files)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents ) )
#process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange(
#  '190645:10-190645:110',
#)

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = options.GT
process.load("Configuration.StandardSequences.MagneticField_cff")

process.out = cms.OutputModule("PoolOutputModule",
     #verbose = cms.untracked.bool(True),
     SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
     fileName = cms.untracked.string(options.outfile),
#     fileName = cms.untracked.string(process.source.fileNames[0][0:-5]+'Tupel.root'),
     outputCommands = cms.untracked.vstring() 
#     outputCommands = cms.untracked.vstring('keep *') 
)

process.load('Workspace.HEPHYCMSSWTools.EventCounter')
#
process.filterSequence = cms.Sequence(
    process.EventCounter
)
from RecoMET.METProducers.PFMET_cfi import pfMet
process.pfMet = pfMet.clone(src = "packedPFCandidates")
process.pfMet.calculateSignificance = False # this can't be easily implemented on packed PF candidates at the moment

process.metSequence = cms.Sequence(process.pfMet)

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
                                   src = cms.InputTag("genParticles"),                                                                 
                                   printP4 = cms.untracked.bool(False),
                                   printPtEtaPhi = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(False),
                                   printStatus = cms.untracked.bool(True),
                                   printIndex = cms.untracked.bool(False),
                                   status = cms.untracked.vint32( [1,2,3] )
                                   )

process.miniAODTupelizerSequence = cms.Sequence()
process.load('Workspace.HEPHYCMSSWTools.BasicTupelizer_miniAOD_cfi')
process.BasicTupelizer.useForDefaultAlias = cms.untracked.bool(True)
process.BasicTupelizer.addMSugraOSETInfo = cms.untracked.bool(options.mode.lower()=='sms')
process.BasicTupelizer.verbose = cms.untracked.bool(options.verbose)
process.miniAODTupelizerSequence += process.BasicTupelizer
process.load('Workspace.HEPHYCMSSWTools.JetTupelizer_miniAOD_cfi')
process.JetTupelizer.useForDefaultAlias = cms.untracked.bool(True)
process.JetTupelizer.verbose = cms.untracked.bool(options.verbose)
process.miniAODTupelizerSequence += process.JetTupelizer
process.load('Workspace.HEPHYCMSSWTools.MuonTupelizer_miniAOD_cfi')
process.MuonTupelizer.useForDefaultAlias = cms.untracked.bool(True)
process.miniAODTupelizerSequence += process.MuonTupelizer
process.MuonTupelizer.verbose = cms.untracked.bool(options.verbose)
process.load('Workspace.HEPHYCMSSWTools.ElectronTupelizer_miniAOD_cfi')
process.ElectronTupelizer.useForDefaultAlias = cms.untracked.bool(True)
process.ElectronTupelizer.verbose = cms.untracked.bool(options.verbose)
process.miniAODTupelizerSequence += process.ElectronTupelizer
process.load('Workspace.HEPHYCMSSWTools.TauTupelizer_miniAOD_cfi')
process.TauTupelizer.useForDefaultAlias = cms.untracked.bool(True)
process.TauTupelizer.verbose = cms.untracked.bool(options.verbose)
process.miniAODTupelizerSequence += process.TauTupelizer
process.load('Workspace.HEPHYCMSSWTools.TriggerTupelizer_cfi')
process.TriggerTupelizer.useForDefaultAlias = cms.untracked.bool(True)
#process.TriggerTupelizer.verbose = cms.untracked.bool(options.verbose)
process.miniAODTupelizerSequence += process.TriggerTupelizer
process.load('Workspace.HEPHYCMSSWTools.FilterTupelizer_cfi')
process.FilterTupelizer.useForDefaultAlias = cms.untracked.bool(True)
#process.FilterTupelizer.verbose = cms.untracked.bool(options.verbose)
process.miniAODTupelizerSequence += process.FilterTupelizer

process.p = cms.Path(process.filterSequence + process.metSequence + process.miniAODTupelizerSequence)

process.out.outputCommands =  cms.untracked.vstring('drop *', 'keep *_*Tupelizer*_*_*' , 'keep *_*EventCounter*_*_*', *(toKeep))

process.outpath = cms.EndPath(process.out)
