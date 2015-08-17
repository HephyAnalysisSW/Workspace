#!/bin/sh
eval `scramv1 runtime -sh`

export userNameDPM='easilar'
#export userNameNFS='nrad2'

export userNameNFS='easilar'


#export SOURCE='ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_plzworkheplx/150808_092028/0000'
#export SOURCE='/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_plzworkheplx/150808_095925/0000/'
####export SOURCE='/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_plzworkheplx/150808_091926/0000/'
####export TARGET='/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_plzworkheplx/'



declare -a array=(
"/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_plzworkheplx/150808_091956/0000/" 
"/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx/150808_071117/0000/" 
"/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx/150808_071117/0001/"
"/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx/150808_071144/0000/"
"/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx/150808_071216/0000/"
"/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx/150808_071244/0000/"
"/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx/150808_071313/0000/"
"/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx/150808_071344/0000/"
"/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx/150808_071414/0000/"
"/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx/150808_071443/0000/"
)
# get length of an array
arraylength=${#array[@]}

# use for loop to read all values and indexes
for (( i=1; i<${arraylength}+1; i++ ));
do
  export SOURCE=${array[$i-1]}
  array2=(${SOURCE//\// })
  export TARGET="/TEST/${array2[0]}/${array2[1]}"
  #echo $i " / " ${arraylength} " : " ${array[$i-1]}
  echo $i " / " ${arraylength} " : " $SOURCE 
  echo $TARGET 
  cp_CMGoutput_fromDPM.py --userNameDPM=$userNameDPM --userNameNFS=$userNameNFS --source=$SOURCE --target=$TARGET --fileName='' --suffix=".root .tgz" 
  unpackCMGCrabOutput.py    --userNameNFS=$userNameNFS  --dir=$TARGET --suffix=".tgz"
done


####getCMGCrabOutput.py     --userNameDPM=$userNameDPM --userNameNFS=$userNameNFS --source=$SOURCE --target=$TARGET --fileName='' --suffix=".root .tgz" 
####unpackCMGCrabOutput.py  --userNameNFS=$userNameNFS  --dir=$TARGET --suffix=".tgz"


##python /afs/hephy.at/scratch/n/nrad/CMSSW/CMSSW_7_2_3/src/Workspace/HEPHYPythonTools/scripts/getCrabOutput.py --userNameDPM=$userNameDPM --userNameNFS=$userNameNFS --source=$SOURCE --target=$TARGET --fileName='' --suffix=".tgz" 

#unpackCMGCrabOutput.py --userNameNFS=nrad  --dir='cmgTuples/crab_ece_v1/test2/SMS_T1tttt_2J_mGl1200_mLSP800/' --suffix=".tgz"
