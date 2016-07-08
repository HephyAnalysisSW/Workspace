#! /bin/sh
#SBATCH -J electronID_Mateusz
#SBATCH -a 1-10 
#SBATCH -D /afs/hephy.at/work/m/mzarucki/CMSSW/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/plotsMateusz/electronID/jobs
#SBATCH -o /afs/hephy.at/work/m/mzarucki/CMSSW/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/plotsMateusz/electronID/jobs/logs/job%j_electronID.out
eval `scram runtime -sh`
echo  CMSBASE: $CMSSW_BASE
python -b scans.py --scan standard
python -b scans.py --scan standard --iso hybIso03
python -b scans.py --scan nMinus1
python -b scans.py --scan nMinus1 --iso hybIso03
python -b scans.py --scan standard --lowPt 1
python -b scans.py --scan standard --iso hybIso03 --lowPt 1
python -b scans.py --scan nMinus1 --lowPt 1
python -b scans.py --scan nMinus1 --iso hybIso03 --lowPt 1
python -b scans.py --scan slices
python -b scans.py --scan deltaR_ratioPt
