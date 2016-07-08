#! /bin/sh
#SBATCH -J ZinvEstimation_Mateusz
#SBATCH -a 1-10 
#SBATCH -D /afs/hephy.at/work/m/mzarucki/CMSSW/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/plotsMateusz/Zinv
#SBATCH -o /afs/hephy.at/work/m/mzarucki/CMSSW/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/plotsMateusz/Zinv/jobs/logs/job%j_ZinvEstimation.out
eval `scram runtime -sh`
echo  CMSBASE: $CMSSW_BASE
python -b ZinvEstimation.py --plot 1 --Zpeak 1 --emulated 1 --leptons 1 --peak 0 --CT2 75
python -b ZinvEstimation.py --plot 1 --Zpeak 1 --emulated 1 --leptons 1 --peak 1 --CT2 75
python -b ZinvEstimation.py --plot 1 --Zpeak 0 --emulated 1 --leptons 1 --peak 0 --CT2 100
python -b ZinvEstimation.py --plot 1 --Zpeak 0 --emulated 1 --leptons 1 --peak 1 --CT2 100
python -b ZinvEstimation.py --plot 1 --Zpeak 0 --emulated 1 --leptons 1 --peak 0 --CT2 125
python -b ZinvEstimation.py --plot 1 --Zpeak 0 --emulated 1 --leptons 1 --peak 1 --CT2 125
python -b ZinvEstimation.py --plot 1 --Zpeak 0 --emulated 1 --leptons 1 --peak 0 --CT2 150
python -b ZinvEstimation.py --plot 1 --Zpeak 0 --emulated 1 --leptons 1 --peak 1 --CT2 150
python -b ZinvEstimation.py --plot 1 --Zpeak 0 --emulated 1 --leptons 1 --peak 0 --CT2 300
python -b ZinvEstimation.py --plot 1 --Zpeak 0 --emulated 1 --leptons 1 --peak 1 --CT2 300
