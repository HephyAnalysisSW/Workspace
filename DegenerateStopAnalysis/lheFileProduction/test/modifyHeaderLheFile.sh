#!/bin/sh -x

# modify the header of a LHE file such that the <slha> section contains only
# <slha>
# DECAY   1000022   0.0E+00
# </slha>
#
#

# variable definitions

selectedLheFiles=$1

# data directory for merged LHE files: dataDirRead  - source, dataDirWrite  - destination
dataLheSet="T2tt_stopMass_0_500"
dataDirRead=`pwd`"/T2tt/stop_stop/output/"${dataLheSet}_mergedFiles   
dataDirWrite=`pwd`"/T2tt/stop_stop/modifiedHeader/"${dataLheSet}_mergedFiles

# end of variable definitions

# create the destination directory, if it does not exist
if [ -d ${dataDirWrite} ]
then
    echo "Directory ${dataDirWrite} already exists"
else
    echo "Trying to create directory ${dataDirWrite}"
    mkdir -p ${dataDirWrite}
fi

for lheFile in `cat ${selectedLheFiles}`; do

    originalFile=${dataDirRead}/${lheFile}    
    [ -e "${originalFile}" ] || continue
    
    copyFile=${dataDirWrite}/${lheFile}
    newFile=${dataDirWrite}/${lheFile}.new
        
    cp ${originalFile} ${copyFile}  
    
    gunzip  -c ${copyFile} > ${newFile} 
    sed -n -e '/<slha>/ {r slha.txt' -e ':a; n; /<\/slha>/ {b}; ba}; p' ${newFile} > ${copyFile}.mod
    
    rm ${copyFile}
    
    gzip ${copyFile}.mod 
    mv ${copyFile}.mod.gz ${copyFile}
    
    rm ${newFile} 
             
done

echo 
echo "Job finished"


 
           