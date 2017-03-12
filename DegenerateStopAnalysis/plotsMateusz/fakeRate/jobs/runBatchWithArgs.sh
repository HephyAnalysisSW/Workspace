#!/bin/bash
JOBS=$1
   
BATCHNAME="--title FakeRate"
OUTPUTDIR="--output /afs/hephy.at/work/m/mzarucki/CMSSW/CMSSW_8_0_7/src/Workspace/DegenerateStopAnalysis/plotsMateusz/fakeRate/jobs/logs"

while read p; do

   COMMAND=${p/'$1'/$2}
   COMMAND=${COMMAND/'$2'/$3}
   COMMAND=${COMMAND/'$3'/$4}
   COMMAND=${COMMAND/'$4'/$5}
   submitBatch.py "$COMMAND" $BATCHNAME $OUTPUTDIR

done <$JOBS
