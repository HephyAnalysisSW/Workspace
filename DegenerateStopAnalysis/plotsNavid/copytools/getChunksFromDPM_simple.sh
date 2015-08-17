#!/bin/sh
eval `scramv1 runtime -sh`

export userNameDPM='schoef'
export userNameNFS='nrad'


##### MAKE SURE SAMPLE NAME IN SOURCE AND TARGET MATCH!!!! ####
#export SOURCE="/babies/CMGTools-from-CMSSW_7_2_3_LocalDevelopments/test1_REST_vienna_crab/SMS_T1tttt_2J_mGl1200_mLSP800/150425_201204/0000"
#export TARGET='cmgTuples/crab_cmg_v1/test2_test/SMS_T1tttt_2J_mGl1200_mLSP800/'
#echo $userNameDPM

#export SOURCE="TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_fixgentaus/150720_180859/0000/"
#export SOURCE="WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_fixgentaus/150720_181150/0000/"

#export SOURCE="DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3_MC25ns/150808_200524/0000/"
#export TARGET="cmgTuples/Spring15_v0/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3_MC25ns/"
#export TARGET="cmgTuples/Spring15_v0/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/test1/"

#export TARGET="/cmgTuples/for_daniel/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns_150813",


#export TARGET= "cmgTuples/for_daniel/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns_150813"
export TARGET="cmgTuples/for_daniel/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns_150813"
unpackCMGCrabOutput.py  --userNameNFS=$userNameNFS  --dir=$TARGET --suffix=".tgz"
export TARGET="cmgTuples/for_daniel/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns_150813"
unpackCMGCrabOutput.py  --userNameNFS=$userNameNFS  --dir=$TARGET --suffix=".tgz"
export TARGET="cmgTuples/for_daniel/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns_150813"
unpackCMGCrabOutput.py  --userNameNFS=$userNameNFS  --dir=$TARGET --suffix=".tgz"

#getCMGCrabOutput.py     --userNameDPM=$userNameDPM --userNameNFS=$userNameNFS --source=$SOURCE --target=$TARGET --fileName='' --suffix=".root .tgz" 
unpackCMGCrabOutput.py  --userNameNFS=$userNameNFS  --dir=$TARGET --suffix=".tgz"





##python /afs/hephy.at/scratch/n/nrad/CMSSW/CMSSW_7_2_3/src/Workspace/HEPHYPythonTools/scripts/getCrabOutput.py --userNameDPM=$userNameDPM --userNameNFS=$userNameNFS --source=$SOURCE --target=$TARGET --fileName='' --suffix=".tgz" 

#unpackCMGCrabOutput.py --userNameNFS=nrad  --dir='cmgTuples/crab_ece_v1/test2/SMS_T1tttt_2J_mGl1200_mLSP800/' --suffix=".tgz"
