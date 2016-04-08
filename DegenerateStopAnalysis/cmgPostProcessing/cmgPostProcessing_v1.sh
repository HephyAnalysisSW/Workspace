#!/bin/sh

# shell script to run CMSSW post-processing
# on heplx run it with
#       krenew -t -K 10 -- bash -c ./cmgPostProcessing_v1.sh $1


# set parameters
CMSSW_ACTION="R"
CMG_SAMPLE=$1

if [[ ${CMSSW_ACTION} == "CB" || ${CMSSW_ACTION} == "R" ]]; then

    export SCRAM_ARCH=slc6_amd64_gcc491

    scram project CMSSW CMSSW_7_4_12_patch4 
    cd CMSSW_7_4_12_patch4/src
    eval `scram runtime -sh`
fi

if [[ ${CMSSW_ACTION} == "R" ]]; then
    
    cd ${CMSSW_BASE}/src/Workspace/DegenerateStopAnalysis/cmgPostProcessing
            
    python cmgPostProcessing_v1.py --logLevel=INFO --processSample=${CMG_SAMPLE} --processingTag='final' \
        --skim='' --skimLepton='inc' --parameterSet='syncLip'  
fi

exit 0


