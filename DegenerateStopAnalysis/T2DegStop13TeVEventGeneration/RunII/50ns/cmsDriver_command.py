
##GENSIM
##cmsDriver.py  Configuration/GenProduction/python/genfragment_cff.py --filein file:input.lhe  --fileout file:FSQ-RunIIFall14GS-00001.root --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --conditions MCRUN2_71_V1::All --beamspot NominalCollision2015 --step GEN,SIM --magField 38T_PostLS1 --no_exec --python_filename step0_GENSIM_cfg.py -n 147

## Phys 14 CMSSW_7_2_0_patch1
#cmsDriver.py step1 --filein root://xrootd.unl.edu//store/user/nrad/T2DegStop2j_300_270_GENSIM/T2DegStop2j_300_270_GENSIM/edbe023d17b99f8a8fbdf4e576e17580/  --fileout file:step1.root --pileup_input "dbs:/MinBias_TuneA2MB_13TeV-pythia8/Fall13-POSTLS162_V1-v1/GEN-SIM" --mc --eventcontent RAWSIM --inputEventContent REGEN --pileup AVE_40_BX_25ns --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --datatier GEN-SIM-RAW --conditions PHYS14_25_V1 --step GEN:fixGenInfo,DIGI,L1,DIGI2RAW,HLT:GRun --magField 38T_PostLS1 -n -1 --no_exec


#cmsDriver.py step2 --filein file:step1.root --fileout file:step2.root --mc --eventcontent AODSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --datatier AODSIM  --conditions PHYS14_25_V1 --step RAW2DIGI,L1Reco,RECO,EI --magField 38T_PostLS1 --no_exec 


cmsDriver.py step3 --filein file:step2.root --fileout file:MINIAOD.root --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions PHYS14_25_V1 --step PAT --no_exec




#cmsDriver.py step1 --filein "dbs:/T2DegStop2j_300_270_GENSIM/nrad-T2DegStop2j_300_270_GENSIM-edbe023d17b99f8a8fbdf4e576e17580/USER" --fileout file:step1.root --pileup_input "dbs:/MinBias_TuneA2MB_13TeV-pythia8/Fall13-POSTLS162_V1-v1/GEN-SIM" --mc --eventcontent RAWSIM --inputEventContent REGEN --pileup AVE_40_BX_25ns --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --datatier GEN-SIM-RAW --conditions PHYS14_25_V1 --step GEN:fixGenInfo,DIGI,L1,DIGI2RAW,HLT:GRun --magField 38T_PostLS1 -n -1 --no_exec


#cmsDriver.py step2 --filein file:step1.root --fileout file:step2.root --mc --eventcontent AODSIM,DQM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --datatier AODSIM,DQMIO --conditions PHYS14_25_V1 --step RAW2DIGI,L1Reco,RECO,EI,DQM:DQMOfflinePOGMC --magField 38T_PostLS1 -n -1

#cmsDriver.py step3 --filein file:step2.root --fileout file:out.root --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions PHYS14_25_V1 --step PAT -n -1



###### RUN II

##DIGI 2 RECO
##   https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVMCcampaignRunIISpring15DR74x
cmsDriver.py step1  --mc  --conditions MCRUN2_74_V7A --pileup_input das:/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIIWinter15GS-MCRUN2_71_V1-v1/GEN-SIM  --filein "T2DegStop "  --pileup 2015_50ns_Startup_PoissonOOTPU  -s DIGI,L1,DIGI2RAW,HLT:@frozen50ns --datatier GEN-SIM-RAW --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1_50ns --eventcontent RAWSIM --magField 38T_PostLS1 --no_exec


##HLT  #minBias sample is fishy
#cmsDriver.py step1 --filein dbs:/T2DegStop2j_300_270_GENSIM/nrad-T2DegStop2j_300_270_GENSIM-edbe023d17b99f8a8fbdf4e576e17580/USER --fileout file:T2DegStop2j_300_270_GENSIMHLT_step1.root --pileup_input dbs:/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIIFall14GS-MCRUN2_71_V1-v3/GEN-SIM --mc --eventcontent RAWSIM --pileup Flat_20_50_50ns --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --conditions MCRUN2_73_V9 --step DIGI,L1,DIGI2RAW,HLT:GRun --magField 38T_PostLS1 --python_filename step1_HLT_cfg.py --no_exec

