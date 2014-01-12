#!/bin/sh -x

jobParameters=$1
deltaMassStopLspSelected=$2
jobIdentifier=$3

madgraphDir="/data/DegenerateLightStop/LheProduction/MadGraph"
dataDir="/data/DegenerateLightStop/LheProduction/T2tt/stop_stop"
workspaceDir="/data/DegenerateLightStop/LheProduction/WorkspaceTar"

tmpDir="/data/DegenerateLightStop/LheProduction/LheProduction.$$"
mkdir $tmpDir
cd $tmpDir

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
cp  ${madgraphDir}/MG5v1.5.11_CERN_23082013_patched19092013.tar.gz MG5v1.5.11_CERN_23082013_patched19092013.tar.gz
tar -xzf MG5v1.5.11_CERN_23082013_patched19092013.tar.gz

# create data directory - files must be already staged
ln -s ${dataDir}/T2tt_undecayedFiles T2tt_undecayedFiles

# install the Workspace code
cp  ${workspaceDir}/Workspace.tar.gz Workspace.tar.gz
tar -xzf Workspace.tar.gz

# replace the value of deltaMassStopLspSelected 
perl -p -i -e "s/DMASSSTOPLSP/$2/" Workspace/MonoJetAnalysis/lheFileProduction/python/jobParameters/$1.py

# run python 

python -u Workspace/MonoJetAnalysis/lheFileProduction/python/runLheProduction.py ${jobParameters} > ${jobParameters}.log

# copy the output data

cp ${jobParameters}.log ${dataDir}/${jobParameters}.${jobIdentifier}.log

# for interactive jobs, one needs to create the directory

if [ ! -d ${dataDir}/T2tt_mergedFiles.${jobIdentifier} ]
then
    mkdir ${dataDir}/T2tt_mergedFiles.${jobIdentifier}
fi

for lheFile in T2tt_mergedFiles/*; do
    [ -e "${lheFile}" ] || continue
    lheFileName="$(basename "${lheFile}")"
    cp T2tt_mergedFiles/${lheFileName} ${dataDir}/T2tt_mergedFiles.${jobIdentifier}/${lheFileName}  
done

exit 0


