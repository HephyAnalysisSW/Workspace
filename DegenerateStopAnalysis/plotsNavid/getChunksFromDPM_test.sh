#!/bin/sh
eval `scramv1 runtime -sh`

export userNameDPM='easilar'
export userNameNFS='easilar'


##### MAKE SURE SAMPLE NAME IN SOURCE AND TARGET MATCH!!!! ####
#export SOURCE="/babies/CMGTools-from-CMSSW_7_2_3_LocalDevelopments/test1_REST_vienna_crab/SMS_T1tttt_2J_mGl1200_mLSP800/150425_201204/0000"
#export TARGET='cmgTuples/crab_cmg_v1/test2_test/SMS_T1tttt_2J_mGl1200_mLSP800/'
#echo $userNameDPM

#export SOURCE="TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_fixgentaus/150720_180859/0000/"
#export SOURCE="WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_fixgentaus/150720_181150/0000/"

export SOURCE="ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_fixgentaus/150720_181025/0000/"
export TARGET="cmgTuples/crab_Spring15/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/"


getCMGCrabOutput.py     --userNameDPM=$userNameDPM --userNameNFS=$userNameNFS --source=$SOURCE --target=$TARGET --fileName='' --suffix=".root .tgz" 
unpackCMGCrabOutput.py  --userNameNFS=$userNameNFS  --dir=$TARGET --suffix=".tgz"





##python /afs/hephy.at/scratch/n/nrad/CMSSW/CMSSW_7_2_3/src/Workspace/HEPHYPythonTools/scripts/getCrabOutput.py --userNameDPM=$userNameDPM --userNameNFS=$userNameNFS --source=$SOURCE --target=$TARGET --fileName='' --suffix=".tgz" 

#unpackCMGCrabOutput.py --userNameNFS=nrad  --dir='cmgTuples/crab_ece_v1/test2/SMS_T1tttt_2J_mGl1200_mLSP800/' --suffix=".tgz"
