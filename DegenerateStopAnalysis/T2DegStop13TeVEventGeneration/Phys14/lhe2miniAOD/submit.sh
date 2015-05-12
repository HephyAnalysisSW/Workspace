export jobname="GEN-DIGI-L1-DIGI2RAW-HLT-PU40"

crab -submit 1-500 -c $jobname
crab -submit 501-1000 -c $jobname
crab -submit 1001-1500 -c $jobname
crab -submit 1501-2000 -c $jobname
crab -submit 2001-2500 -c $jobname


