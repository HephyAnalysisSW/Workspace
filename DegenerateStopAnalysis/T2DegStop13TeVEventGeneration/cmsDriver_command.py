
##GENSIM
##cmsDriver.py  Configuration/GenProduction/python/genfragment_cff.py --filein file:input.lhe  --fileout file:FSQ-RunIIFall14GS-00001.root --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --conditions MCRUN2_71_V1::All --beamspot NominalCollision2015 --step GEN,SIM --magField 38T_PostLS1 --no_exec --python_filename step0_GENSIM_cfg.py -n 147
##HLT
cmsDriver.py step1 --filein dbs:/T2DegStop2j_300_270_GENSIM/nrad-T2DegStop2j_300_270_GENSIM-edbe023d17b99f8a8fbdf4e576e17580/USER --fileout file:T2DegStop2j_300_270_GENSIMHLT_step1.root --pileup_input dbs:/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIIFall14GS-MCRUN2_71_V1-v3/GEN-SIM --mc --eventcontent RAWSIM --pileup Flat_20_50_50ns --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --conditions MCRUN2_73_V9 --step DIGI,L1,DIGI2RAW,HLT:GRun --magField 38T_PostLS1 --python_filename step1_HLT_cfg.py --no_exec

