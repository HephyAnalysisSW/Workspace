#!/bin/sh

# shell script to build and compile a CMSSW release, including 
# contributions from:
#   https://github.com/HephySusySW/Workspace
#   https://github.com/CERN-PH-CMG/cmg-cmssw.git
#   https://github.com/HephySusySW/cmg-cmssw.git
#
# Usage: in sh shell execute
#   source ./manageRelease.sh

# set parameters
CMSSW_ACTION="CB"

# activate debuging
set -vx

if [[ ${CMSSW_ACTION} == "CB" || ${CMSSW_ACTION} == "R" ]]; then

    export SCRAM_ARCH=slc6_amd64_gcc491

    scram project CMSSW CMSSW_7_4_12_patch4 
    cd CMSSW_7_4_12_patch4/src
    eval `scram runtime -sh`
fi

if [[ ${CMSSW_ACTION} == "CB" ]]; then

    # create empty repository (with the cmssw trick to keep the repository small)
    git cms-init
    
    # clone Vienna Workspace repository
    git clone https://github.com/HephySusySW/Workspace 
    cd Workspace
    git checkout 74X-master
    
    # 
    cd ${CMSSW_BASE}/src
    eval `scram runtime -sh`

    # add the central CMG repository, and fetch it
    # limit the fetch to the 7_4_12-related branches, to avoid loading all the past history of CMGTools
    git remote add cmg-central https://github.com/CERN-PH-CMG/cmg-cmssw.git -f \
        -t CMGTools-from-CMSSW_7_4_12 -t heppy_74X
    git fetch cmg-central

    # add your mirror
    git remote add cmg-hephy https://github.com/HephySusySW/cmg-cmssw.git -f \
        -t CMGTools-from-CMSSW_7_4_12_LocalDevelopmentsPass2_DegStop
    git fetch cmg-hephy

    # configure the sparse checkout
    git config core.sparsecheckout true
    /bin/cp /afs/cern.ch/user/c/cmgtools/public/sparse-checkout_7412_heppy .git/info/sparse-checkout
    
    echo
    echo "\n sparse-checkout file: \n"
    cat .git/info/sparse-checkout
    echo 
        
    # add some additional packages (optional)
    echo "/CMGTools/ObjectStudies/" >> .git/info/sparse-checkout
    echo "/JetMETCorrections/Type1MET/" >> .git/info/sparse-checkout
    echo "/PhysicsTools/PatAlgos/" >> .git/info/sparse-checkout
    echo "/PhysicsTools/PatUtils/" >> .git/info/sparse-checkout
    echo "/DataFormats/FWLite/" >> .git/info/sparse-checkout

    
    # checkout the CMGTools branch of the release
    git checkout -b CMGTools-from-CMSSW_7_4_12_LocalDevelopmentsPass2_DegStop \
        cmg-hephy/CMGTools-from-CMSSW_7_4_12_LocalDevelopmentsPass2_DegStop
   
    # create also the heppy branch
    git branch heppy_74X cmg-central/heppy_74X
    
    #
    git gc --prune=now
    git read-tree -mu HEAD
    
    #compile
    cd $CMSSW_BASE/src
    scram b -j 8

fi

# deactivate debuging
set +vx
