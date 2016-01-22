#!/bin/sh 

nohup krenew -t -K 10 -- bash -c "sh all_postProcessing_Spring15_25ns_signals_1.sh>  all_postProcessing_Spring15_25ns_signals_1.log" &
nohup krenew -t -K 10 -- bash -c "sh all_postProcessing_Spring15_25ns_signals_2.sh>  all_postProcessing_Spring15_25ns_signals_2.log" &
nohup krenew -t -K 10 -- bash -c "sh all_postProcessing_Spring15_25ns_signals_3.sh>  all_postProcessing_Spring15_25ns_signals_3.log" &
nohup krenew -t -K 10 -- bash -c "sh all_postProcessing_Spring15_25ns_signals_4.sh>  all_postProcessing_Spring15_25ns_signals_4.log" &
nohup krenew -t -K 10 -- bash -c "sh all_postProcessing_Spring15_25ns_signals_5.sh>  all_postProcessing_Spring15_25ns_signals_5.log" &
nohup krenew -t -K 10 -- bash -c "sh all_postProcessing_Spring15_25ns_signals_6.sh>  all_postProcessing_Spring15_25ns_signals_6.log" &


