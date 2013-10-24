#!/bin/sh

printenv PATH
cd $HOME/private/CMSSW_6_0_0
eval `scramv1 runtime -sh`
cd ../susy/MonoJetAnalysis/python

#if [ ! -d /tmp/imikulec ]; then
#  mkdir /tmp/imikulec
#  chmod 700 /tmp/imikulec
#fi

script="convertv5.py"
logfile="/data/imikulec/logs/convertv5_$1_$2.log"

date >$logfile 2>&1
hostname >>$logfile 2>&1
echo "python -u $script $1 $2 -b" >>$logfile 2>&1
python -u $script $1 $2 -b >>$logfile 2>&1
date >>$logfile 2>&1
echo "done" >>$logfile 2>&1


