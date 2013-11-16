#!/bin/sh

#cmsRun defaultPatOnFly_cfg.py maxEvents=-1 mode=sms files=load:$1 outfile=/data/schoef/monoJetSignals/SUSYTupelizer/FastSim/8TeV-$1_0_1.root    startFileNumber=0   stopFileNumber=1  &

cmsRun defaultPatOnFly_cfg.py maxEvents=-1 mode=sms files=load:$1 outfile=/data/schoef/monoJetSignals/SUSYTupelizer/FullSim/8TeV-$1_0_50.root    startFileNumber=0   stopFileNumber=50  &
cmsRun defaultPatOnFly_cfg.py maxEvents=-1 mode=sms files=load:$1 outfile=/data/schoef/monoJetSignals/SUSYTupelizer/FullSim/8TeV-$1_50_100.root  startFileNumber=50  stopFileNumber=100 &
cmsRun defaultPatOnFly_cfg.py maxEvents=-1 mode=sms files=load:$1 outfile=/data/schoef/monoJetSignals/SUSYTupelizer/FullSim/8TeV-$1_100_150.root startFileNumber=100 stopFileNumber=150 &
cmsRun defaultPatOnFly_cfg.py maxEvents=-1 mode=sms files=load:$1 outfile=/data/schoef/monoJetSignals/SUSYTupelizer/FullSim/8TeV-$1_150_200.root startFileNumber=150 stopFileNumber=200 &
cmsRun defaultPatOnFly_cfg.py maxEvents=-1 mode=sms files=load:$1 outfile=/data/schoef/monoJetSignals/SUSYTupelizer/FullSim/8TeV-$1_200_250.root startFileNumber=200 stopFileNumber=250 &
cmsRun defaultPatOnFly_cfg.py maxEvents=-1 mode=sms files=load:$1 outfile=/data/schoef/monoJetSignals/SUSYTupelizer/FullSim/8TeV-$1_250_300.root startFileNumber=250 stopFileNumber=300 & 
cmsRun defaultPatOnFly_cfg.py maxEvents=-1 mode=sms files=load:$1 outfile=/data/schoef/monoJetSignals/SUSYTupelizer/FullSim/8TeV-$1_300_350.root startFileNumber=300 stopFileNumber=350 &
cmsRun defaultPatOnFly_cfg.py maxEvents=-1 mode=sms files=load:$1 outfile=/data/schoef/monoJetSignals/SUSYTupelizer/FullSim/8TeV-$1_350_400.root startFileNumber=350 stopFileNumber=400 &
cmsRun defaultPatOnFly_cfg.py maxEvents=-1 mode=sms files=load:$1 outfile=/data/schoef/monoJetSignals/SUSYTupelizer/FullSim/8TeV-$1_400_450.root startFileNumber=400 stopFileNumber=450 &

#cmsRun defaultPatOnFly_cfg.py maxEvents=-1 mode=sms files=load:$1 outfile=/data/schoef/monoJetSignals/SUSYTupelizer/FullSim/8TeV-$1_450_500.root startFileNumber=450 stopFileNumber=500 &

