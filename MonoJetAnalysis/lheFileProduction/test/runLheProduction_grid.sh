#!/bin/sh -x

jobParameters=$1
deltaMassStopLspSelected=$2
jobIdentifier=$3

madgraphDir="root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/ghete/DegenerateLightStop/LheProduction/MadGraph"
dataDir="root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/ghete/DegenerateLightStop/LheProduction/T2tt/stop_stop"
workspaceDir="root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/ghete/DegenerateLightStop/LheProduction/WorkspaceTar"

# setup CMS Environment

if [ -z $CMS_PATH ]
then
    . /cvmfs/cms.cern.ch/cmsset_default.sh
fi

# create CMSSW area

cmssw="CMSSW_5_3_13"

scram project CMSSW $cmssw
cd $cmssw/src
eval `scramv1 runtime -sh`

# install MadGraph
xrdcp  ${madgraphDir}/MG5v1.5.11_CERN_23082013_patched19092013.tar.gz MG5v1.5.11_CERN_23082013_patched19092013.tar.gz
tar -xzf MG5v1.5.11_CERN_23082013_patched19092013.tar.gz

# create and mount data directory - files must be already staged
mkdir T2tt_undecayedFiles
gfalFS T2tt_undecayedFiles/ ${dataDir}/T2tt_undecayedFiles

# install the Workspace code
xrdcp  ${workspaceDir}/Workspace.tar.gz Workspace.tar.gz
tar xzf Workspace.tar.gz

# replace the value of deltaMassStopLspSelected 
perl -p -i -e "s/DMASSSTOPLSP/$2/" Workspace/MonoJetAnalysis/lheFileProduction/python/jobParameters/$1.py

# run LHE file production

python -u Workspace/MonoJetAnalysis/lheFileProduction/python/runLheProduction.py ${jobParameters} > ${jobParameters}.log

# unmount the data directory
gfalFS_umount T2tt_undecayedFiles

# copy the output data 

xrdcp ${jobParameters}.log ${dataDir}/${jobParameters}.${jobIdentifier}.log

for lheFile in T2tt_mergedFiles/*; do
    [ -e "${lheFile}" ] || continue
    lheFileName="$(basename "${lheFile}")"
    xrdcp T2tt_mergedFiles/${lheFileName} ${dataDir}/T2tt_mergedFiles.${jobIdentifier}/${lheFileName}  
done

exit 0
