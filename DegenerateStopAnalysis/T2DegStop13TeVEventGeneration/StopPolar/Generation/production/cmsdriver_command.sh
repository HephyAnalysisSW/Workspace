#cmsDriver.py ../../../RunII/GEN-SIM-RAW/fragments/T2tt_dM-10to80_genHT-160_genMET-80_fragment_onePoint_privGridpack.py \
#--python_filename T2tt_dM-10to80_fragment_onePoint_privGridpack_py_LHE_GEN_mStop-500_mLSP-460_PU.py \
#--fileout file:T2tt_dM-10to80_privGridpack_GEN_mStop-500_mLSP-460_PU.root \
#--step LHE,GEN,SIM,DIGI,L1,DIGI2RAW --datatier GEN --eventcontent RAWSIM,LHE \
#--conditions 92X_upgrade2017_realistic_v12 --era Run2_2017 --geometry DB:Extended --beamspot Realistic25ns13TeVEarly2017Collision --mc \
#--pileup 2016_25ns_Moriond17MC_PoissonOOTPU --customise_commands "process.mi"
#-n 500000 \
#--no_exec
#
#
#cmsDriver commands to produce cfgs:

### No PU ###
cmsDriver.py Configuration/GenProduction/T2tt_dM-10to80_genHT-160_genMET-80_fragment_onePoint_privGridpack.py \
--python_filename T2tt_dM-10to80_fragment_onePoint_privGridpack_py_LHE_GEN_mStop-500_mLSP-460_noPU.py \
--fileout file:T2tt_dM-10to80_privGridpack_LHE-GEN_mStop-500_mLSP-460_noPU.root \
--step LHE,GEN --datatier GEN,LHE  --eventcontent RAW,LHE \
--conditions 92X_upgrade2017_realistic_v12 --era Run2_2017 --geometry DB:Extended --beamspot Realistic25ns13TeVEarly2017Collision --mc \
-n 100000 \
--no_exec

#### With PU ###
#cmsDriver.py fragments/T2tt_dM-10to80_genHT-160_genMET-80_fragment_onePoint_privGridpack.py \
#--python_filename T2tt_dM-10to80_fragment_onePoint_privGridpack_py_LHE_GEN-SIM-RAW_mStop-500_mLSP-460_PU.py \
#--fileout file:T2tt_dM-10to80_privGridpack_LHE-GEN-SIM-RAW_mStop-500_mLSP-460_PU.root \
#--step LHE,GEN,SIM,DIGI,L1,DIGI2RAW --datatier GEN-SIM-RAW,LHE --eventcontent RAWSIM,LHE \
#--conditions 92X_upgrade2017_realistic_v12 --era Run2_2017 --geometry DB:Extended --beamspot Realistic25ns13TeVEarly2017Collision --mc \
#--pileup 2016_25ns_Moriond17MC_PoissonOOTPU --pileup_input "dbs:/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIISummer17GS-92X_upgrade2017_realistic_v2-v1/GEN-SIM" --customise_commands "process.mix.input.nbPileupEvents.probFunctionVariable = cms.vint32(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62) \n process.mix.input.nbPileupEvents.probValue = cms.vdouble(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571)\n process.simHcalDigis.markAndPass = cms.bool(True)" \
#-n 500000 \
#--no_exec
#
#For crab submission with private gridpacks, the cfg created from the gen-fragments (with hard-coded gridpack paths) needed to be modified to include the gridpack path as an option, which is then set by config.JobType.pyCfgParams in the crab config.

