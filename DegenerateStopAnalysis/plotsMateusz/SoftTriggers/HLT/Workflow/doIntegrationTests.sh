hltIntegrationTests /users/mzarucki/SoftMuHardJetMET/V5 \
-i root://cms-xrd-global.cern.ch//store/mc/RunIIWinter17DR/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_94X_upgrade2018_realistic_v8-v2/410000/501E3205-3A0E-E811-A48B-0CC47A7C3428.root \
-s /dev/CMSSW_10_0_0/GRun/V33 \
-n 5000 \
-x "--globaltag 100X_upgrade2018_realistic_TSG_2018_01_24_13_08_07" \
-x "--offline --unprescale" \
-x "--l1Xml L1Menu_Collisions2018_v0_2_0.xml" \
-x "--l1-emulator uGT" \
-x "--customise HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2017DtUnpacking" -j 8 \
> hltIntegrationTestResults.log
