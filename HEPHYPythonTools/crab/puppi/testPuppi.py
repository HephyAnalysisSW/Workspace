import FWCore.ParameterSet.Config as cms
import os
import pickle
import FWCore.ParameterSet.VarParsing as VarParsing


options = VarParsing.VarParsing ('standard')
options.register ('file','defaultinput.root',
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "Input File")

options.register ('outfile','testPuppi.root',
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "Output File")

options.register ('AOD',1,
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "Output File")


options.parseArguments()

AOD=options.AOD


print "INPUT FILE ___________________________________"
print options.file
print "OUTPUT FILE ___________________________________"
print options.outfile


process = cms.Process('TestPuppi')
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.GlobalTag.globaltag = 'START53_V7G::All'
'''
process.load('Dummy/Puppi/Puppi_cff')   
process.puppi.candName = cms.untracked.string('particleFlow')                 #for AOD
process.puppi.vertexName = cms.untracked.string('offlinePrimaryVertices')     #for AOD
process.puppi.algos[0].ptMin = cms.untracked.double(-1)
process.puppi.algos[1].ptMin = cms.untracked.double(-1)
process.puppi.algos[2].ptMin = cms.untracked.double(-1)
process.puppi.algos[3].ptMin = cms.untracked.double(-1)
process.puppi.algos[4].ptMin = cms.untracked.double(-1)
process.puppi.MinNeutralPt = cms.untracked.double(0.05)

process.puppi.algos[0].algoId = cms.untracked.int32(0)
#process.puppi.algos[0].cone  = cms.untracked.double(0.3),
#process.puppi.algos[0].rmsPtMin.  = cms.untracked.double(0.1),
'''
'''
process.load('PuppiUpgrade_cff')   
process.puppi.MinNeutralPtSlope = cms.untracked.double(-1)
'''

#process.load('Dummy/Puppi/Puppi_cff')   
process.load('PuppiReset_cff')

if AOD==1:
  print 'Running On AOD'
  process.puppi.candName = cms.untracked.string('particleFlow')                 #for AOD
  process.puppi.vertexName = cms.untracked.string('offlinePrimaryVertices')  
else:
  print 'Running on miniAOD'
  process.puppi.candName   = cms.untracked.string('packedPFCandidates')
  process.puppi.vertexName = cms.untracked.string('offlineSlimmedPrimaryVertices')

steps = ['Old','Step1','Step2','Step3','Step4','Step5','Step6']

puppiStep = os.environ.get('PUPPISTEP')
puppiStepIndex = steps.index(puppiStep)


if puppiStepIndex == 0:
  print 'we are in default mode'


if puppiStepIndex >= 1:
  print 'Step1: Puppi Parameters Turned OFF'
  #Puppi as is, just the algo with a step function and no Pt cut
if puppiStepIndex >= 2:
  print 'Step2: Turning Vertexing On'
  process.puppi.applyCHS       = cms.untracked.bool  (True)
  process.puppi.UseDeltaZCut   = cms.untracked.bool  (True)
  process.puppi.algos[0].puppiAlgos[0].useCharged     = cms.untracked.bool(True)
  #process.puppiForward.useCharged     = cms.untracked.bool(True) #keep off, no tracking in HF
if puppiStepIndex >= 3:
  print 'Step3: rmsScaleFactor = 1'
  process.puppi.algos[0].puppiAlgos[0].rmsScaleFactor   = cms.untracked.double(1.0)
  process.puppi.algos[1].puppiAlgos[0].rmsScaleFactor   = cms.untracked.double(1.0)
  process.puppi.algos[2].puppiAlgos[0].rmsScaleFactor   = cms.untracked.double(1.0)
  process.puppi.algos[3].puppiAlgos[0].rmsScaleFactor   = cms.untracked.double(1.0)
  process.puppi.algos[4].puppiAlgos[0].rmsScaleFactor   = cms.untracked.double(1.0)
  #process.puppiCentral.rmsScaleFactor   = cms.untracked.double(1.0)
  #process.puppiForward.rmsScaleFactor   = cms.untracked.double(1.0)
if puppiStepIndex >= 4:
  print 'Step4: Turn on MinNeutralPtCut'
  process.puppi.algos[0].MinNeutralPt   = cms.untracked.double(0.2) #Barrel
  process.puppi.algos[1].MinNeutralPt   = cms.untracked.double(1)   #Endcap
  process.puppi.algos[2].MinNeutralPt   = cms.untracked.double(1.5) #HF
  process.puppi.algos[3].MinNeutralPt   = cms.untracked.double(1)   #Endcap
  process.puppi.algos[4].MinNeutralPt   = cms.untracked.double(1.5) #HF
if puppiStepIndex >= 5:
  print 'Step5: Turn on MinNeutralPtSlope'
  process.puppi.algos[0].MinNeutralPtSlope   = cms.untracked.double(0.02)
  process.puppi.algos[1].MinNeutralPtSlope   = cms.untracked.double(0.005)
  process.puppi.algos[2].MinNeutralPtSlope   = cms.untracked.double(0.005)
  process.puppi.algos[3].MinNeutralPtSlope   = cms.untracked.double(0.005)
  process.puppi.algos[4].MinNeutralPtSlope   = cms.untracked.double(0.005)
if puppiStepIndex >= 6:
  print 'Step6: HFPtCut '
  process.puppi.algos[2].MinNeutralPt   = cms.untracked.double(3.5) #HF
  process.puppi.algos[4].MinNeutralPt   = cms.untracked.double(3.5) #HF



#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(int(os.environ.get('MAXEVENTS'))) )
print 'Real PUPPI MAXEVENTS='
print options.maxEvents

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

process.source = cms.Source("PoolSource",
  #fileNames  = cms.untracked.vstring('/store/cmst3/user/gpetrucc/miniAOD/v1/TT_Tune4C_13TeV-pythia8-tauola_PU_S14_PAT.root')
  #fileNames  = cms.untracked.vstring('/store/relval/CMSSW_7_1_0_pre5/RelValTTbar_13/GEN-SIM-RECO/PU50ns_POSTLS171_V2-v2/00000/4CCC03AC-BDBC-E311-8597-02163E00EA7F.root')
 # fileNames  = cms.untracked.vstring('file:/data/nrad/local/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola_PU20bx25_POSTLS170_V5-v1_AODSIM.root')

  #fileNames = cms.untracked.vstring('file:/data/schoef/local/Spring14dr_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_AODSIM_PU_S14_POSTLS170_V6-v1.root')
  #fileNames = cms.untracked.vstring(os.environ.get('filename'))
  #fileNames = cms.untracked.vstring(os.environ.get('FILENAME')) 
  fileNames = cms.untracked.vstring(options.file)
)
process.source.inputCommands = cms.untracked.vstring("keep *",
                                                     "drop *_MEtoEDMConverter_*_*")

process.options = cms.untracked.PSet(
  wantSummary = cms.untracked.bool(True),
  Rethrow     = cms.untracked.vstring('ProductNotFound'),
  fileMode    = cms.untracked.string('NOMERGE')
)


process.puppiSequence = cms.Sequence(process.puppi)
process.p = cms.Path(process.puppiSequence)
process.output = cms.OutputModule("PoolOutputModule",                                                                                                                                                     
                                  #outputCommands = cms.untracked.vstring('drop *','keep *_*_*_RECO','drop *_*_Cleaned_*','keep *_puppi_*_*'),
                                  outputCommands = cms.untracked.vstring('keep *'),
                                  #fileName       = cms.untracked.string ("Output.root")                                                                                                                   
                                  #fileName       = cms.untracked.string(process.source.fileNames[0][0:-5]+'Puppi.root')
                                  #fileName       = cms.untracked.string(process.source.fileNames[0].replace('schoef','nrad').replace('local','local').replace('.root','Puppi{0}.root'.format(os.environ.get('PUPPISTEP'))))
                                  #fileName        = cms.untracked.string('file:/data/nrad/local/50TTAODPuppi.root')
                                  #fileName        = cms.untracked.string(os.environ.get('PUPPIOUT'))
                                  fileName        = cms.untracked.string(options.outfile)
)
# schedule definition                                                                                                       

pickle.dump(process, file(options.outfile.replace('file:','').replace('.root','.pkl'),'w'))
process.outpath  = cms.EndPath(process.output) 
