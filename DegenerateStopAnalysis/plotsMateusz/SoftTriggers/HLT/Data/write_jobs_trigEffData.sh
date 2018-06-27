#!/bin/sh
PD="SingleMuon"
joblist=`cat jobs_trigEffData.sh`
filelist=`cat inputFiles/inputFiles_2018A_${PD}_MINIAOD_315974-316723.txt`

while read j; 
do
    for f in $filelist; 
    do
        echo "$j "--PD ${PD} --infiles" $f" >> "jobs_trigEffData_${PD}.sh"
    done
done <jobs_trigEffData.sh
