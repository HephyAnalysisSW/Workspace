#!/bin/sh -x


# variable definitions

jobParameters=$1
stopMassLowLimit=$2
stopMassHighLimit=$3
generatedLspMassLowLimit=$4
generatedLspMassHighLimit=$5
deltaMassStopLspSelected=$6

# data directory: undecayed and merged LHE files - grid: xrootd for read, rfcp for write; interactive: cp for both read and write
dataDirRead="/data/DegenerateLightStop/LheProduction/T2tt/stop_stop"
dataDirWrite="/data/DegenerateLightStop/LheProduction/T2tt/stop_stop"
#     set of undecayed LHE files
dataLheSet="T2tt_stopMass_0_500"
dataUndecayedLheDir=${dataDirRead}/${dataLheSet}_undecayedFiles
#     directory to copy the log files and the directories with merged files
dataMergedLheDir=${dataDirWrite}/output/${dataLheSet}_mergedFiles

# MadGraph reference directory - it contains a soft link with the version of the MadGraph5 
# (namely ${jobDirMadGraph} defined below) the the tar.gz file
madGraphRefDir="/data/DegenerateLightStop/LheProduction/MadGraph"

# Workspace reference directory
workspaceRefDir="/data/DegenerateLightStop/LheProduction/WorkspaceTar"

# local job directories - perl replaced in job parameters
jobDirMadGraph="MG5v1.5.11"
jobDirUndecayedLhe="T2tt_undecayedFiles"
jobDirMergedLhe="T2tt_mergedFiles"

# for interactive jobs, create a job directory
tmpDir="/data/DegenerateLightStop/LheProduction/LheProduction.$$"
mkdir $tmpDir
cd $tmpDir

# end of variable definitions


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
cp  ${madGraphRefDir}/${jobDirMadGraph}.tar.gz ${jobDirMadGraph}.tar.gz
tar -xzf ${jobDirMadGraph}.tar.gz

# install the Workspace code
cp  ${workspaceRefDir}/Workspace.tar.gz Workspace.tar.gz
tar -xzf Workspace.tar.gz

# create job data directory for undecayed LHE files and copy the list of files
mkdir ${jobDirUndecayedLhe}
cp ${dataUndecayedLheDir}.txt ${jobDirUndecayedLhe}.txt

# set the final list of job parameters
#
#     replace the value of stopMassLowLimit 
perl -p -i -e "s/REPLACE_stopMassLowLimit/${stopMassLowLimit}/" Workspace/MonoJetAnalysis/lheFileProduction/python/jobParameters/runLheProduction_parameters_replace.py
#
#     replace the value of stopMassHighLimit 
perl -p -i -e "s/REPLACE_stopMassHighLimit/${stopMassHighLimit}/" Workspace/MonoJetAnalysis/lheFileProduction/python/jobParameters/runLheProduction_parameters_replace.py
#
#     replace the value of generatedLspMassLowLimit 
perl -p -i -e "s/REPLACE_generatedLspMassLowLimit/${generatedLspMassLowLimit}/" Workspace/MonoJetAnalysis/lheFileProduction/python/jobParameters/runLheProduction_parameters_replace.py
#
#     replace the value of generatedLspMassHighLimit 
perl -p -i -e "s/REPLACE_generatedLspMassHighLimit/${generatedLspMassHighLimit}/" Workspace/MonoJetAnalysis/lheFileProduction/python/jobParameters/runLheProduction_parameters_replace.py
#
#     replace the value of deltaMassStopLspSelected 
perl -p -i -e "s/REPLACE_deltaMassStopLspSelected/${deltaMassStopLspSelected}/" Workspace/MonoJetAnalysis/lheFileProduction/python/jobParameters/runLheProduction_parameters_replace.py
#
#     replace the value of job Madgraph directory
perl -p -i -e "s'REPLACE_madGraphDirectory'${jobDirMadGraph}'" Workspace/MonoJetAnalysis/lheFileProduction/python/jobParameters/runLheProduction_parameters_replace.py
#
#     replace the value of job undecayed LHE directory
perl -p -i -e "s'REPLACE_undecayedFilesDirectory'${jobDirUndecayedLhe}'" Workspace/MonoJetAnalysis/lheFileProduction/python/jobParameters/runLheProduction_parameters_replace.py
#
#     replace the value of job merged LHE directory
perl -p -i -e "s'REPLACE_mergedFilesDirectory'${jobDirMergedLhe}'" Workspace/MonoJetAnalysis/lheFileProduction/python/jobParameters/runLheProduction_parameters_replace.py
#
#     replace the value of undecayedFilesStageDirectory 
perl -p -i -e "s'REPLACE_undecayedFilesStageDirectory'${dataUndecayedLheDir}'" Workspace/MonoJetAnalysis/lheFileProduction/python/jobParameters/runLheProduction_parameters_replace.py



# run LHE file production

if [ ${stopMassLowLimit} ==  ${stopMassHighLimit} ]
then
    stopMassValues=${stopMassLowLimit}
else
    stopMassValues=${stopMassLowLimit}_${stopMassHighLimit}
fi

if [ ${generatedLspMassLowLimit} ==  ${generatedLspMassHighLimit} ]
then
    generatedLspMassValues=${generatedLspMassLowLimit}
else
    generatedLspMassValues=${generatedLspMassLowLimit}_${generatedLspMassHighLimit}
fi

jobIdentifier=${jobParameters}_stopMass_${stopMassValues}_genLsp_${generatedLspMassValues}_dMStopLsp_${deltaMassStopLspSelected}
logFile=${jobIdentifier}.log
dataFinalDir=${dataMergedLheDir}/${jobDirMergedLhe}.${jobIdentifier}

python -u Workspace/MonoJetAnalysis/lheFileProduction/python/runLheProduction.py ${jobParameters} > ${logFile}

# copy the output data 

# for interactive jobs and rfcp protocol, one needs to create the directory
if [ -d ${dataFinalDir} ]
then
    echo "Directory ${dataFinalDir} already exists"
else
    echo "Trying to create directory ${dataFinalDir}"
    mkdir -p ${dataFinalDir}
fi

cp ${logFile} ${dataMergedLheDir}/${logFile}

for lheFile in ${jobDirMergedLhe}/*; do
    [ -e "${lheFile}" ] || continue
    lheFileName="$(basename "${lheFile}")"
    cp ${jobDirMergedLhe}/${lheFileName} ${dataFinalDir}/${lheFileName}  
done

exit 0


