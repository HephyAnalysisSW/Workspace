#!/bin/sh

# shell script to run CMSSW post-processing
# on heplx run it with
#       krenew -t -K 10 -- bash -c ./cmgPostProcessing_v1.sh $1 $2 $3 $4


# set parameters
CMSSW_ACTION="R"
CMG_SAMPLE=$1
CMG_PROCESSING_TAG=$2
CMG_POST_PROCESSING_TAG=$3
PARAMETER_SET=$4

if [[ ${CMSSW_ACTION} == "CB" || ${CMSSW_ACTION} == "R" ]]; then

    export SCRAM_ARCH=slc6_amd64_gcc491

    scram project CMSSW CMSSW_7_4_12_patch4 
    cd CMSSW_7_4_12_patch4/src
    eval `scram runtime -sh`
fi

if [[ ${CMSSW_ACTION} == "R" ]]; then
    
    cd ${CMSSW_BASE}/src/Workspace/DegenerateStopAnalysis/python/cmgPostProcessing
            
    python cmgPostProcessing_v1.py --logLevel=INFO \
        --processSample=${CMG_SAMPLE}  --skim='' --skimLepton='inc' \
        --cmgProcessingTag=${CMG_PROCESSING_TAG} --cmgPostProcessingTag=${CMG_POST_PROCESSING_TAG} \
        --parameterSet=${PARAMETER_SET}  
fi

exit 0


