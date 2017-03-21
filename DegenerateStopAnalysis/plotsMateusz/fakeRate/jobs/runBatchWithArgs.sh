#!/bin/bash

OPT="BATCH"

JOBS=$1
   
BATCHNAME="--title FakeRate"
OUTPUTDIR="--output /afs/hephy.at/work/m/mzarucki/CMSSW/CMSSW_8_0_7/src/Workspace/DegenerateStopAnalysis/plotsMateusz/fakeRate/jobs/logs"

while read p; do

   COMMAND=${p/'$1'/$2}
   COMMAND=${COMMAND/'$2'/$3}
   COMMAND=${COMMAND/'$3'/$4}
   COMMAND=${COMMAND/'$4'/$5}

   if [[ ${OPT} == "SAVE" ]]; then
      echo "$COMMAND" >> jobs_all.sh
   elif [[ ${OPT} == "BATCH" ]]; then
      submitBatch.py "$COMMAND" $BATCHNAME $OUTPUTDIR
   fi

done <$JOBS
