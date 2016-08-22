#!/bin/sh

# shell script to run runPostProcessing_v1.py  
# Steps:
#    Prerequisite:
#      set-up the production release (e.g. via manageRelease.sh from script directory)
#      in the base repository (where the release was checked out)
#        ln -s CMSSW_8_0_11/src/Workspace/DegenerateStopAnalysis/python/cmgPostProcessing/runPostProcessing.sh .
#    Run steps:   
#       From the base repository, where the link was done:
#       nohup krenew -t -K 10 -- bash -c "./runPostProcessing.sh $1 [$2 [$3] [$4] [$5]]" & ; disown
#
#       $1 compulsory; 
#          set sample as defined in runPostProcessing.py
#       $2 must be set to 'MC' for MC samples, and to 'DATA' for data
#          take cmgTuples=${CMG_TUPLES} as defined below in the if block
#       $3 if set to "skimPreselect", run skimPreselect, otherwise do not run skimPreselect
#          set it to "" if there is another non-empty parameter after it
#       $4 if set to "skimLepton", run skimLepton, otherwise do not run skimLepton
#          set it to "" if there is another non-empty parameter after it
#       $5 optional;
#          if 'TEST', add to "_TEST" to CMG_POST_PROCESSING_TAG, e.g. "80X_postProcessing_v2_TEST"
#          with 'TEST', it also add '--verbose'
#
# 
# The parameters to be used are available in 
#   ${CMSSW_BASE}/src/Workspace/DegenerateStopAnalysis/python/cmgPostProcessing/cmgPostProcessing_parser.py
#   ${CMSSW_BASE}/src/Workspace/DegenerateStopAnalysis/python/cmgPostProcessing/runPostProcessing.py
# adapt them below to the desired values. If not set here, the default parameters will be used

# activate debugging
#set -vx

# release and architecture, 
CMSSW_RELEASE="CMSSW_8_0_11"
SCRAM_ARCH_VAL="slc6_amd64_gcc530"
CMSSW_ACTION="RO"

# set parameters 

# cli parameters
SAMPLE_SET=$1

# semi-hard-coded parameters
if [[ ${2} == "DATA" ]]; then 
    CMG_TUPLES="Data2016_v1_2"
    BTAG_WEIGHTS=""
else
    CMG_TUPLES="RunIISpring16MiniAODv2_v1"
    BTAG_WEIGHTS="--processBTagWeights"
fi

if [[ ${3} == "skimPreselect" ]]; then 
    SKIM_PRESELECT="--skimPreselect"
else
    SKIM_PRESELECT=""
fi

if [[ ${4} == "skimLepton" ]]; then 
    SKIM_LEPTON="--skimLepton=oneLep"
else
    SKIM_LEPTON=""
fi

#CMG_POST_PROCESSING_TAG="80X_postProcessing_v6_1"
CMG_POST_PROCESSING_TAG="80X_postProcessing_v9"
VERBOSE="--verbose"
if [[ ${5} == "TEST" ]]; then 
    CMG_POST_PROCESSING_TAG=$CMG_POST_PROCESSING_TAG"_TEST"
    VERBOSE="--verbose"
fi

# hard-coded parameters - modify them according to desired full set
CMG_PROCESSING_TAG="8011_mAODv2_v1"
PARAMETER_SET="analysisHephy_13TeV_2016_v0"

# the rest of the parameters are the default parameters from cmgPostProcessing_parser.py

# 
if [[ ${CMSSW_ACTION} == "CB" || ${CMSSW_ACTION} == "R" ]]; then

    export SCRAM_ARCH=${SCRAM_ARCH_VAL}

    scram project CMSSW ${CMSSW_RELEASE}
    cd ${CMSSW_RELEASE}/src
    eval `scram runtime -sh`
fi

if [[ ${CMSSW_ACTION} == "RO" || ${CMSSW_ACTION} == "R" ]]; then
    
    cd ${CMSSW_BASE}/src/Workspace/DegenerateStopAnalysis/python/cmgPostProcessing
            
    python runPostProcessing.py \
        --logLevel=INFO \
        --sampleSet=${SAMPLE_SET} \
        --cmgTuples=${CMG_TUPLES} \
        --parameterSet=${PARAMETER_SET} \
        --cmgProcessingTag=${CMG_PROCESSING_TAG} \
        --cmgPostProcessingTag=${CMG_POST_PROCESSING_TAG} \
        --processLepAll \
        --skimGeneral='' \
        ${SKIM_PRESELECT} \
        ${SKIM_LEPTON} \
        ${BTAG_WEIGHTS} \
        --run \
        ${VERBOSE}
fi

# deactivate debugging
#set +vx

exit 0
