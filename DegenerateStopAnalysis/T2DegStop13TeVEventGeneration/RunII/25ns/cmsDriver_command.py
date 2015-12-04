

#  RUN II 
##  GENSIM 7116
#cmsDriver.py  Configuration/GenProduction/python/genfragment_cff.py --filein file:/afs/cern.ch/work/n/nrad/private/T2DegStop/13TeVGeneration/LHE/T2DegStop2j_300_270_merged.lhe  --fileout file:GENSIM.root                  --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --conditions MCRUN2_71_V1::All --beamspot NominalCollision2015 --step GEN,SIM --magField 38T_PostLS1 --no_exec -n 147 --python_filename step0_GENSIM_cfg.py

## DIGI 741_patch1
#cmsDriver.py step1  --mc  --conditions MCRUN2_74_V9A --pileup_input das:/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIIWinter15GS-MCRUN2_71_V1-v1/GEN-SIM  --filein das:/T2DegStop_300_270_GEN-SIM/nrad-T2DegStop_300_270_GEN-SIM-59531333944c2793ca6c056c8055e782/USER  --pileup 2015_25ns_Startup_PoissonOOTPU  -s DIGI,L1,DIGI2RAW,HLT:@frozen25ns --datatier GEN-SIM-RAW --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --eventcontent RAWSIM --magField 38T_PostLS1 --no_exec --python_filename step1_DIGI.py

## RECO
#with DQM
#cmsDriver.py step2 --mc --filein file:step1_DIGI_L1_DIGI2RAW_HLT_PU.root --conditions MCRUN2_74_V9 -s RAW2DIGI,L1Reco,RECO,EI,DQM:DQMOfflinePOGMC --datatier AODSIM,DQMIO --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --eventcontent AODSIM,DQM --magField 38T_PostLS1 --no_exec
#without DQM
#cmsDriver.py step2 --mc --filein file:step1_DIGI_L1_DIGI2RAW_HLT_PU.root --conditions MCRUN2_74_V9 -s RAW2DIGI,L1Reco,RECO,EI --datatier AODSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --eventcontent AODSIM --magField 38T_PostLS1 --no_exec

## miniAOD
#old miniaod# cmsDriver.py step3  --mc --filein file:step2_RAW2DIGI_L1Reco_RECO_EI.root --conditions MCRUN2_74_V9 --eventcontent MINIAODSIM --runUnscheduled -s PAT --datatier MINIAODSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --python_filename step3_miniAOD_cfg.py --no_exec
#miniaodv2
#cmsDriver.py step3 --filein dbs:/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIiM --fileout file:TOP-RunIISpring15MiniAODv2-00001.root --mc --eventcontent MINIAODSIM --runUnscheduled --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --conditions 74X_mcRun2_asymptotic_v2 --step PAT --python_filename /afs/cern.ch/cms/PPD/PdmV/work/McM/submit/TOP-RunIISpring15MiniAODv2-00001/TOP-RunIISpring15MiniAODv2-00001_1_cfg.py --no_exec -n 1920

cmsDriver.py step3 --filein file:step2_RAW2DIGI_L1Reco_RECO_EI.root --mc --eventcontent MINIAODSIM --runUnscheduled --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --conditions 74X_mcRun2_asymptotic_v2 --step PAT --python_filename step3_miniAOD_cfg.py --no_exec -n 1920


##HLT  #minBias sample is fishy
#cmsDriver.py step1 --filein dbs:/T2DegStop2j_300_270_GENSIM/nrad-T2DegStop2j_300_270_GENSIM-edbe023d17b99f8a8fbdf4e576e17580/USER --fileout file:T2DegStop2j_300_270_GENSIMHLT_step1.root --pileup_input dbs:/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIIFall14GS-MCRUN2_71_V1-v3/GEN-SIM --mc --eventcontent RAWSIM --pileup Flat_20_50_50ns --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --conditions MCRUN2_73_V9 --step DIGI,L1,DIGI2RAW,HLT:GRun --magField 38T_PostLS1 --python_filename step1_HLT_cfg.py --no_exec

