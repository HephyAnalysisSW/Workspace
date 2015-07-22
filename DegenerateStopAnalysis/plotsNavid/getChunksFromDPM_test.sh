#!/bin/sh
eval `scramv1 runtime -sh`

export userNameDPM='easilar'
export userNameNFS='nrad2'







##### MAKE SURE SAMPLE NAME IN SOURCE AND TARGET MATCH!!!! ####
export SOURCE="/babies/CMGTools-from-CMSSW_7_2_3_LocalDevelopments/test2_RobertSignals_vienna_crab/SMS_T2tt_2J_mStop425_mLSP325/150511_194125/0000/"
export TARGET='cmgTuples/crab_cmg_v1/SMS_T2tt_2J_mStop425_mLSP325'
export userNameDPM='easilar'
export userNameNFS='nrad2'
#echo $userNameDPM
getCMGCrabOutput.py     --userNameDPM=$userNameDPM --userNameNFS=$userNameNFS --source=$SOURCE --target=$TARGET --fileName='' --suffix=".root .tgz" 
unpackCMGCrabOutput.py  --userNameNFS=$userNameNFS  --dir=$TARGET --suffix=".tgz"



##python /afs/hephy.at/scratch/n/nrad/CMSSW/CMSSW_7_2_3/src/Workspace/HEPHYPythonTools/scripts/getCrabOutput.py --userNameDPM=$userNameDPM --userNameNFS=$userNameNFS --source=$SOURCE --target=$TARGET --fileName='' --suffix=".tgz" 

#unpackCMGCrabOutput.py --userNameNFS=nrad  --dir='cmgTuples/crab_ece_v1/test2/SMS_T1tttt_2J_mGl1200_mLSP800/' --suffix=".tgz"
