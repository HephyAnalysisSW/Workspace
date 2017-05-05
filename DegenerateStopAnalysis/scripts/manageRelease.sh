#!/bin/sh

# shell script to build and compile a CMSSW release, including 
# contributions from:
#   https://github.com/HephySusySW/Workspace
#   https://github.com/CERN-PH-CMG/cmg-cmssw.git
#   https://github.com/HephySusySW/cmgtools-lite
#
# Usage: in sh shell execute
#   source ./manageRelease.sh WORKSPACE_TAG_BRANCH CMGTOOLS_LITE_TAG_BRANCH
#   or
#   source ./manageRelease.sh WORKSPACE_TAG_BRANCH
#   or
#   source ./manageRelease.sh

# in the directory where the realease has to be checkout and built
#
# if no argument or one argument is given, the default branch(es) or tag(s) given below will be used. 
# Note: when using tags (to be given as tags/TAG_NAME), 
#       git checkout tags/TAG_NAME, 
#       the repository goes in "detached head", so you can not commit 
#       your changes. 
#       Use tags only for producing tuples.

# set parameters
CMSSW_ACTION="CB"

if [[ $# -eq 2 ]]; then
    # Workspace and cmgtools-lite tags / branches from cli
    WORKSPACE_TAG_BRANCH=$1
    CMGTOOLS_LITE_TAG_BRANCH=$2
elif [[ $# -eq 1 ]]; then
    # Workspace tag / branch only from cli, fixed tag / branch for cmgtools-lite
    WORKSPACE_TAG_BRANCH=$1
    CMGTOOLS_LITE_TAG_BRANCH="80X_DegStop"
else
    # default tags or branches
    WORKSPACE_TAG_BRANCH="80X-master"
    CMGTOOLS_LITE_TAG_BRANCH="80X_DegStop"
fi

# activate debuging
set -vx

# release and architecture, 
CMSSW_RELEASE="CMSSW_8_0_25"
SCRAM_ARCH_VAL="slc6_amd64_gcc530"

if [[ ${CMSSW_ACTION} == "CB" || ${CMSSW_ACTION} == "R" ]]; then

    export SCRAM_ARCH=${SCRAM_ARCH_VAL}

    scram project CMSSW ${CMSSW_RELEASE}
    cd ${CMSSW_RELEASE}/src
    eval `scram runtime -sh`
    
fi

if [[ ${CMSSW_ACTION} == "CB" ]]; then

    # create empty repository 
    git cms-init
    
    # clone github Vienna Workspace repository
    git clone https://github.com/HephySusySW/Workspace 
    cd Workspace
    git checkout ${WORKSPACE_TAG_BRANCH}
    
    # 
    cd ${CMSSW_BASE}/src
    eval `scram runtime -sh`
            
    # add the central cmg-cmssw repository to get the Heppy 80X branch
    git remote add cmg-central https://github.com/CERN-PH-CMG/cmg-cmssw.git  -f  -t heppy_80X

    # configure the sparse checkout
    git config core.sparsecheckout true
    /bin/cp /afs/cern.ch/user/c/cmgtools/public/sparse-checkout_80X_heppy .git/info/sparse-checkout
    
    echo
    echo "sparse-checkout file:"
    echo
    cat .git/info/sparse-checkout
    echo 
        
    # add some additional packages (optional)
    echo "/JetMETCorrections/Type1MET/" >> .git/info/sparse-checkout
    echo "/PhysicsTools/PatAlgos/" >> .git/info/sparse-checkout
    echo "/PhysicsTools/PatUtils/" >> .git/info/sparse-checkout
    echo "/DataFormats/FWLite/" >> .git/info/sparse-checkout

    
    # checkout the base heppy packages
    git checkout -b heppy_80X cmg-central/heppy_80X
   
    # get the CMGTools subsystem from the cmgtools-lite repository
    git clone -o cmg-central https://github.com/CERN-PH-CMG/cmgtools-lite.git -b 80X CMGTools
    cd CMGTools
    
    # add your fork, fetch the changes, checkout the branch/tag
    git remote add cmg-lite-hephy https://github.com/HephySusySW/cmgtools-lite.git
    git fetch cmg-lite-hephy
    git checkout -b ${CMGTOOLS_LITE_TAG_BRANCH} cmg-lite-hephy/${CMGTOOLS_LITE_TAG_BRANCH}
    
    ADD_CMS_ANALYSIS="ADD"
    CMSANALYSIS_TAG_BRANCH="80X-master"
    
    cd ${CMSSW_BASE}/src
    
    if [[ ${ADD_CMS_ANALYSIS} == "ADD" ]]; then
        # get the CmsAnalysis subsystem from the CERN gitlab cms-analysis repository
        git clone -o cms-analysis https://gitlab.cern.ch/ghete/cms-analysis.git -b ${CMSANALYSIS_TAG_BRANCH} CmsAnalysis
        cd CmsAnalysis
        git checkout -b ${CMSANALYSIS_TAG_BRANCH} cms-analysis/${CMSANALYSIS_TAG_BRANCH}
    fi

    #compile
    cd $CMSSW_BASE/src
    scram b -j 8

fi

# deactivate debuging
set +vx
