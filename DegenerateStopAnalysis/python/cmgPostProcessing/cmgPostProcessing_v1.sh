#!/bin/sh

# shell script to run post-processing via CMSSW cmgPostProcessing_v1.py  
# Steps:
#    Prerequisite:
#      set-up the production release (e.g. via manageRelease.sh from script directory)
#      in the base repository (where the release was checked out)
#        ln -s CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/python/cmgPostProcessing/cmgPostProcessing_v1.sh .
#    Run steps:   
#       From the base repository, where the link was done:
#       krenew -t -K 10 -- bash -c "./cmgPostProcessing_v1.sh $1 [$2 [3]]" &
# 
#       $1 compulsory; 
#          set processSample to values defined in sample definition file
#       $2 optional for MC samples, must be set to 'DATA' for data
#          if 'DATA', take cmgTuples="Data25ns_v6", for any other value takes cmgTuples="Spring15_7412pass2_mAODv2_v6"
#       $3 optional;
#          if 'TEST', add to "_TEST" to CMG_POST_PROCESSING_TAG, e.g. "74X_postProcessing_v3_TEST"
#          with 'TEST', it also add '--verbose'
#
# 
# The parameters to be used are available in 
#   ${CMSSW_BASE}/src/Workspace/DegenerateStopAnalysis/python/cmgPostProcessing/cmgPostProcessing_parser.py
#   ${CMSSW_BASE}/src/Workspace/DegenerateStopAnalysis/python/cmgPostProcessing/runPostProcessing.py
# adapt them below to the desired values. If not set here, the default parameters will be used

# activate debugging
set -vx

# release and architecture, 
CMSSW_RELEASE="CMSSW_7_4_12_patch4"
SCRAM_ARCH_VAL="slc6_amd64_gcc491"
CMSSW_ACTION="R"

# set parameters 

# cli parameters
CMG_SAMPLE=$1

# semi-hard-coded parameters
if [[ ${2} == "DATA" ]]; then 
    CMG_TUPLES="Data25ns_v6"
else
    CMG_TUPLES="Spring15_7412pass2_mAODv2_v6"
fi

CMG_POST_PROCESSING_TAG="74X_postProcessing_v3"
VERBOSE=""
if [[ ${3} == "TEST" ]]; then 
    CMG_POST_PROCESSING_TAG="74X_postProcessing_v3_TEST"
    VERBOSE="--verbose"
fi

# hard-coded parameters - modify them according to desired full set
CMG_PROCESSING_TAG="7412pass2_mAODv2_v6"
PARAMETER_SET="analysisHephy_13TeV_v0"

# the rest of the parameters are the default parameters from cmgPostProcessing_parser.py

# 
if [[ ${CMSSW_ACTION} == "CB" || ${CMSSW_ACTION} == "R" ]]; then

    export SCRAM_ARCH=${SCRAM_ARCH_VAL}

    scram project CMSSW ${CMSSW_RELEASE}
    cd ${CMSSW_RELEASE}/src
    eval `scram runtime -sh`
fi

if [[ ${CMSSW_ACTION} == "R" ]]; then
    
    cd ${CMSSW_BASE}/src/Workspace/DegenerateStopAnalysis/python/cmgPostProcessing
            
    python cmgPostProcessing_v1.py \
        --logLevel=INFO \
        --processSample=${CMG_SAMPLE} \
        --cmgTuples=${CMG_TUPLES} \
        --parameterSet=${PARAMETER_SET} \
        --cmgProcessingTag=${CMG_PROCESSING_TAG} \
        --cmgPostProcessingTag=${CMG_POST_PROCESSING_TAG} \
        --processLepAll \
        --skimGeneral='' \
        --skimLepton='inc' \
        --skimPreselect \
        ${VERBOSE}
fi

# deactivate debugging
set +vx

exit 0


