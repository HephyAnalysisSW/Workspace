#!/bin/sh 

nohup krenew -t -K 10 -- bash -c "./all_postProcessing_Spring15_25ns_1.sh >& all_postProcessing_Spring15_25ns_1.log" &
nohup krenew -t -K 10 -- bash -c "./all_postProcessing_Spring15_25ns_2.sh >& all_postProcessing_Spring15_25ns_2.log" &
nohup krenew -t -K 10 -- bash -c "./all_postProcessing_Spring15_25ns_3.sh >& all_postProcessing_Spring15_25ns_3.log" &
nohup krenew -t -K 10 -- bash -c "./all_postProcessing_Spring15_25ns_4.sh >& all_postProcessing_Spring15_25ns_4.log" &
nohup krenew -t -K 10 -- bash -c "./all_postProcessing_Spring15_25ns_5.sh >& all_postProcessing_Spring15_25ns_5.log" &
nohup krenew -t -K 10 -- bash -c "./all_postProcessing_Spring15_25ns_6.sh >& all_postProcessing_Spring15_25ns_6.log" &

