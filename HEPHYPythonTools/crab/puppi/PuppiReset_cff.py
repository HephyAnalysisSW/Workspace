import FWCore.ParameterSet.Config as cms

puppiCentral = cms.VPSet(
                 cms.PSet(
                  algoId           = cms.untracked.int32(5),  #0 is default Puppi
                  useCharged       = cms.untracked.bool(False), #Step 6a (True)
                  applyLowPUCorr   = cms.untracked.bool(True),
                  combOpt          = cms.untracked.int32(0),
                  cone             = cms.untracked.double(0.3),
                  rmsPtMin         = cms.untracked.double(0.1),
                  rmsScaleFactor   = cms.untracked.double(0.01) #Step 5a (1.0)
                 )
                )

puppiForward = cms.VPSet(
                cms.PSet(
                 algoId         = cms.untracked.int32(5),  #0 is default Puppi
                 useCharged     = cms.untracked.bool(False), #Step 6b (False)
                 applyLowPUCorr = cms.untracked.bool(True),
                 combOpt        = cms.untracked.int32(0),
                 cone           = cms.untracked.double(0.3),
                 rmsPtMin       = cms.untracked.double(0.5),
                 rmsScaleFactor = cms.untracked.double(0.01) #Step 5a (1.0)
                 )
                )

puppi =  puppi = cms.EDProducer("PuppiProducer",#cms.PSet(#"PuppiProducer",
                       PuppiName      = cms.untracked.string("Puppi"),
                       UseDeltaZCut   = cms.untracked.bool  (False),
                       DeltaZCut      = cms.untracked.double(0.3),
                       candName       = cms.untracked.string('particleFlow'),
                       vertexName     = cms.untracked.string('offlinePrimaryVertices'),
                       #candName      = cms.untracked.string('packedPFCandidates'),
                       #vertexName     = cms.untracked.string('offlineSlimmedPrimaryVertices'),
                       applyCHS       = cms.untracked.bool  (False),#Step 1
                       useExp         = cms.untracked.bool  (False),
                       #MinNeutralPt   = cms.untracked.double(0),#Was not here
                       #MinNeutralPtSlope   = cms.untracked.double(0),#Was not here
                       MinPuppiWeight = cms.untracked.double(0.001),#Step 2 (0.01)
                       algos          = cms.VPSet( 
                        cms.PSet( 
                         etaMin = cms.untracked.double(-2.5), #neg eta was missing (0.0)
                         etaMax = cms.untracked.double( 2.5),
                         ptMin  = cms.untracked.double(0.0), #Step 4a (0.)
                         MinNeutralPt   = cms.untracked.double(0),#Step 3a (0.2)
                         MinNeutralPtSlope   = cms.untracked.double(0),#Step 3a (0.02)
                         puppiAlgos = puppiCentral
                        ),
                        cms.PSet( 
                         etaMin = cms.untracked.double(2.5),
                         etaMax = cms.untracked.double(3.0),
                         ptMin  = cms.untracked.double(0.0), #Step 4b (0.)
                         MinNeutralPt        = cms.untracked.double(0),#Step 3b (1.0)
                         MinNeutralPtSlope   = cms.untracked.double(0), #Step3b (0.005)
                         puppiAlgos = puppiForward
                        ),
                        cms.PSet( 
                         etaMin = cms.untracked.double(3.0),
                         etaMax = cms.untracked.double(10.0),
                         ptMin  = cms.untracked.double(0.0),
                         MinNeutralPt        = cms.untracked.double(0), #Step 4c (1.5)
                         MinNeutralPtSlope   = cms.untracked.double(0), #Step 4c (0.005)
                         puppiAlgos = puppiForward
                       ),
                        cms.PSet(
                         etaMin = cms.untracked.double(-3.0),
                         etaMax = cms.untracked.double(-2.5),
                         ptMin  = cms.untracked.double(0.0), #Step 4b (0.)
                         MinNeutralPt        = cms.untracked.double(0),#Step 3b (1.0)
                         MinNeutralPtSlope   = cms.untracked.double(0), #Step3b (0.005)
                         puppiAlgos = puppiForward
                       ),
                        cms.PSet(
                         etaMin = cms.untracked.double(-10.0),
                         etaMax = cms.untracked.double(-3.0),
                         ptMin  = cms.untracked.double(0.0),
                         MinNeutralPt        = cms.untracked.double(0), #Step 4c (1.5)
                         MinNeutralPtSlope   = cms.untracked.double(0), #Step 4c (0.005)
                         puppiAlgos = puppiForward
                       )
                      )
)

