###
### HLT integration tests ### 
###

hltIntegrationTests /users/mzarucki/SoftTriggers/SoftTriggers/V9 \
-i file:/afs/hephy.at/data/mzarucki02/TriggerStudies/CMSSW_9_2_12/GEN-SIM-RAW/T2tt_dM-10to80_privGridpack_LHE-GEN-SIM-RAW_mStop-500_mLSP-460_noPU/T2tt_dM-10to80_privGridpack_LHE-GEN-SIM-RAW_mStop-500_mLSP-460_noPU_1.root \
-s /dev/CMSSW_9_2_0/GRun/V145 \
-x "--globaltag 92X_upgrade2017_realistic_v12" \
-x "--offline --unprescale" \
-j 8 \
> hltIntegrationTestResults.txt

Official files:
root://eoscms.cern.ch//eos/cms/store/mc/RunIISummer17DRStdmix/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50000/8CAC0136-BFA0-E711-82A8-0025904B2C4C.root  \
root://xrootd-cms.infn.it//store/
root://cms-xrd-global.cern.ch//store/


###
### HLT configuration with customised menu: ###
###

hltGetConfiguration /users/mzarucki/SoftTriggers/SoftTriggers/V9 \
--setup /dev/CMSSW_9_2_0/GRun/V145 \
--globaltag 92X_upgrade2017_realistic_v12 \
--mc --offline --unprescale --cff \
> HLT_SoftTriggers_92X_cff.py

Additional option to use only subset of menu:
--paths HLTriggerFirstPath,HLTriggerFinalPath,HLT_Mu3_PFMET50_PFHT50_L1_ETM30_v1,HLT_Mu3_PFMET50_L1_ETM30_v1,HLT_Mu3_PFMET50_L1_ETM30_v1,HLT_Mu3_PFMET50_L1_SingleMuOpen_v1,HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v12,HLT_PFMET120_PFMHT120_IDTight_v17\

In the cfg fix the setup fragment path: fragment.load("HLTrigger.Configuration.setup_dev_CMSSW_9_2_0_GRun_V145_cff")

Copy the cfg and the setup cffs to the python dir: $CMSSW_BASE/src/HLTrigger/Configuration/python


###
### Configuration for HLT step with customised menu ###
###

cmsDriver.py SoftTriggers \
--filein file:/afs/hephy.at/data/mzarucki02/TriggerStudies/CMSSW_9_2_12/GEN-SIM-RAW/T2tt_dM-10to80_privGridpack_LHE-GEN-SIM-RAW_mStop-500_mLSP-460_noPU/T2tt_dM-10to80_privGridpack_LHE-GEN-SIM-RAW_mStop-500_mLSP-460_noPU_1.root \
--fileout file:/afs/hephy.at/data/mzarucki02/TriggerStudies/CMSSW_9_2_12/HLT/T2tt_dM-10to80_mStop-500_mLSP-460_noPU_SoftTriggers_HLT.root \
--step=HLT:SoftTriggers_92X --processName=SoftTriggers --datatier GEN-SIM-RAW --eventcontent RAWSIM \
--conditions 92X_upgrade2017_realistic_v12 --era Run2_2017 --geometry DB:Extended --beamspot Realistic25ns13TeVEarly2017Collision --mc \
-n 100 \
--no_exec

Add TriggerDecisionAnalyzer EDProducer to extract custom trigger decision from trigger results #NOTE: can be done in HLT step or in AODSIM step

# Output definition
process.RAWSIMEventContent.outputCommands.append('keep bool_*_HLT*_*')

# Additional output definition
process.trigDec = cms.EDProducer('TriggerDecisionAnalyzer')
process.trigDec_step = cms.EndPath(process.trigDec)

# Schedule definition
process.schedule.extend([process.endjob_step, process.trigDec_step, process.RAWSIMoutput_step])


###
### Configuration for AODSIM step over output of HLT step ###
###

cmsDriver.py SoftTriggers \
--filein file:/afs/hephy.at/data/mzarucki02/TriggerStudies/CMSSW_9_2_12/HLT/T2tt_dM-10to80_mStop-500_mLSP-460_noPU_SoftTriggers_HLT.root \
--fileout file:/afs/hephy.at/data/mzarucki02/TriggerStudies/CMSSW_9_2_12/AOD/T2tt_dM-10to80_mStop-500_mLSP-460_noPU_SoftTriggers_HLT_AODSIM.root \
--step RAW2DIGI,L1Reco,RECO --datatier AODSIM --eventcontent AODSIM \
--conditions 92X_upgrade2017_realistic_v12 --era Run2_2017 --geometry DB:Extended --beamspot Realistic25ns13TeVEarly2017Collision --mc \
-n 100 \
--no_exec

Add:
# Output definition
process.AODSIMEventContent.outputCommands.append('keep bool_*_HLT*_*')
