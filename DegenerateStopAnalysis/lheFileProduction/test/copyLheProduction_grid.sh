#!/bin/sh

# copy the decayed LHE files from the HEPHY-Vienna storage element to another location
# via grid tools
#
# under the working directory, it creates the directory
#     /T2tt/stop_stop"/output/${dataLheSet}_mergedFiles
# where it copies the files

if [[ $1 == "-help" || $1 == "--help" || $# -eq 0 || $# -gt 2 ]]; then

    echo
    echo "Copy the decayed LHE files from the HEPHY-Vienna storage element to another location"
    echo "via grid tools"

    echo
    echo "Under the working directory, it creates the directory"
    echo "    {pwd}/T2tt/stop_stop/output/{dataLheSet}_mergedFiles"
    echo "where it copies the files (see {dataLheSet} variable below)"
    echo
    echo "It requires the list of directories from SE, given in the file dirLheFiles.txt"
    echo "in the same directory as the shell script"

    echo
    echo "Usage: "
    echo "   source copyLheProduction_grid.sh 200 | tee copyLheProduction_grid_stopMass_200.log"
    echo "   copy all the files for stop mass 200 GeV for all deltaMassStopLsp values"    
    echo
    echo "   source copyLheProduction_grid.sh 200 10 | tee copyLheProduction_grid_stopMass_200_dMStopLsp_10.log"
    echo "   copy all the files for stop mass 200 GeV and deltaMassStopLsp 10 GeV"    
    echo 
    echo
    return
    
fi


# variable definitions

stopMass=$1
deltaMassStopLsp=$2

#     set of undecayed LHE files
dataLheSet="T2tt_stopMass_0_500"

# data directory for merged LHE files: dataDirRead  - source on SE, dataDirWrite  - destination
#
dataDirRead="gsiftp://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/ghete/DegenerateLightStop/LheProduction/T2tt/stop_stop/output/"${dataLheSet}_mergedFiles   
dataDirWrite=`pwd`"/T2tt/stop_stop"/output/${dataLheSet}_mergedFiles

# end of variable definitions

# copy the output data 
if [ -d ${dataDirWrite} ]
then
    echo "Directory ${dataDirWrite} already exists"
    echo
else
    echo "Trying to create directory ${dataDirWrite}"
    echo
    mkdir -p ${dataDirWrite}
fi

for lheDir in `cat dirLheFiles.txt`; do

    case "${lheDir}" in
        *stopMass_${stopMass}_* ) stopMassTransfer=1;;
        * ) stopMassTransfer=0;;
    esac
    
    case "${lheDir}" in
        *dMStopLsp_${deltaMassStopLsp}* ) dMTransfer=1;;
        * ) dMTransfer=0;;
    esac
    
    
    if [[ ${stopMassTransfer} == 1  &&  ${dMTransfer} == 1 ]]
    then
        echo "globus-url-copy -r -cd ${dataDirRead}/${lheDir}/ file://${dataDirWrite}/ "
        echo
        globus-url-copy -r -cd ${dataDirRead}/${lheDir}/ file://${dataDirWrite}/ 
        
    fi
         
done

echo 
echo "Transfer finished"


