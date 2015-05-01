#!/bin/sh
eval `scramv1 runtime -sh`






##### MAKE SURE SAMPLE NAME IN SOURCE AND TARGET MATCH!!!! ####
#export SOURCE1="/babies/CMGTools-from-CMSSW_7_2_3_LocalDevelopments/test1_REST_vienna_crab/TBar_tWch/150425_200808/0000"
#export TARGET1='cmgTuples/crab_cmg_v1/test2/TBar_tWch/'
#export SOURCE1="/babies/CMGTools-from-CMSSW_7_2_3_LocalDevelopments/test1_REST_vienna_crab/TTH/150425_200614/0000"
#export TARGET1='cmgTuples/crab_cmg_v1/test2/TTH/'
#export SOURCE1="/babies/CMGTools-from-CMSSW_7_2_3_LocalDevelopments/test1_REST_vienna_crab/TTWJets/150425_200526/0000"
#export TARGET1='cmgTuples/crab_cmg_v1/test2/TTWJets/'
#export SOURCE1="/babies/CMGTools-from-CMSSW_7_2_3_LocalDevelopments/test1_REST_vienna_crab/TTZJets/150425_200549/0000"
#export TARGET1='cmgTuples/crab_cmg_v1/test2/TTZJets/'
#export SOURCE1="/babies/CMGTools-from-CMSSW_7_2_3_LocalDevelopments/test1_REST_vienna_crab/TToLeptons_sch/150425_200659/0000"
#export TARGET1='cmgTuples/crab_cmg_v1/test2/TToLeptons_sch/'
#export SOURCE1="/babies/CMGTools-from-CMSSW_7_2_3_LocalDevelopments/test1_REST_vienna_crab/TToLeptons_tch/150425_200637/0000"
#export TARGET1='cmgTuples/crab_cmg_v1/test2/TToLeptons_tch/'
#export SOURCE1="/babies/CMGTools-from-CMSSW_7_2_3_LocalDevelopments/test1_REST_vienna_crab/T_tWch/150425_200832/0000"
#export TARGET1='cmgTuples/crab_cmg_v1/test2/T_tWch/'
#export SOURCE1="/babies/CMGTools-from-CMSSW_7_2_3_LocalDevelopments/test1_REST_vienna_crab/DYJetsToLL_M50_HT200to400/150425_200918/0000"
#export TARGET1='cmgTuples/crab_cmg_v1/test2/DYJetsToLL_M50_HT200to400/'
#export SOURCE1="/babies/CMGTools-from-CMSSW_7_2_3_LocalDevelopments/test1_REST_vienna_crab/DYJetsToLL_M50_HT400to600/150425_200940/0000"
#export TARGET1='cmgTuples/crab_cmg_v1/test2/DYJetsToLL_M50_HT400to600/'
#export SOURCE1="/babies/CMGTools-from-CMSSW_7_2_3_LocalDevelopments/test1_REST_vienna_crab/QCD_HT_100To250/150425_200346/0000"
#export TARGET1='cmgTuples/crab_cmg_v1/test2/QCD_HT_100To250/'
export SOURCE1="/babies/CMGTools-from-CMSSW_7_2_3_LocalDevelopments/test1_REST_vienna_crab/QCD_HT_500To1000/150425_200437/0000"
export TARGET1='cmgTuples/crab_cmg_v1/test2/QCD_HT_500To1000/'
export userNameDPM='easilar'
export userNameNFS='easilar'
#echo $userNameDPM
getCMGCrabOutput.py     --userNameDPM=$userNameDPM --userNameNFS=$userNameNFS --source=$SOURCE1 --target=$TARGET1 --fileName='' --suffix=".root .tgz" 
unpackCMGCrabOutput.py  --userNameNFS=$userNameNFS  --dir=$TARGET1 --suffix=".tgz"



##python /afs/hephy.at/scratch/n/nrad/CMSSW/CMSSW_7_2_3/src/Workspace/HEPHYPythonTools/scripts/getCrabOutput.py --userNameDPM=$userNameDPM --userNameNFS=$userNameNFS --source=$SOURCE --target=$TARGET --fileName='' --suffix=".tgz" 

#unpackCMGCrabOutput.py --userNameNFS=nrad  --dir='cmgTuples/crab_ece_v1/test2/SMS_T1tttt_2J_mGl1200_mLSP800/' --suffix=".tgz"
