#! /bin/sh
#SBATCH -J eleIDlimits_Mateusz
#SBATCH -a 1-20 
#SBATCH -D /afs/hephy.at/work/m/mzarucki/CMSSW/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/plotsMateusz/electronID
#SBATCH -o /afs/hephy.at/work/m/mzarucki/CMSSW/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/plotsMateusz/electronID/jobs/logs/job%j_eleIDlimits.out
eval `scram runtime -sh`
echo  CMSBASE: $CMSSW_BASE
python -b eleIDlimits.py --ID standard --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP None
python -b eleIDlimits.py --ID standard --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP Veto
python -b eleIDlimits.py --ID standard --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP Loose
python -b eleIDlimits.py --ID standard --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP Medium
python -b eleIDlimits.py --ID standard --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP Tight
python -b eleIDlimits.py --ID standard --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP None   --iso hybIso03
python -b eleIDlimits.py --ID standard --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP Veto   --iso hybIso03
python -b eleIDlimits.py --ID standard --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP Loose  --iso hybIso03
python -b eleIDlimits.py --ID standard --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP Medium --iso hybIso03
python -b eleIDlimits.py --ID standard --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP Tight  --iso hybIso03
python -b eleIDlimits.py --ID nMinus1  --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP None                  --removedCut sigmaEtaEta 
python -b eleIDlimits.py --ID nMinus1  --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP Veto                  --removedCut sigmaEtaEta 
python -b eleIDlimits.py --ID nMinus1  --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP Loose                 --removedCut sigmaEtaEta 
python -b eleIDlimits.py --ID nMinus1  --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP Medium                --removedCut sigmaEtaEta 
python -b eleIDlimits.py --ID nMinus1  --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP Tight                 --removedCut sigmaEtaEta 
python -b eleIDlimits.py --ID nMinus1  --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP None   --iso hybIso03 --removedCut sigmaEtaEta 
python -b eleIDlimits.py --ID nMinus1  --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP Veto   --iso hybIso03 --removedCut sigmaEtaEta 
python -b eleIDlimits.py --ID nMinus1  --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP Loose  --iso hybIso03 --removedCut sigmaEtaEta 
python -b eleIDlimits.py --ID nMinus1  --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP Medium --iso hybIso03 --removedCut sigmaEtaEta 
python -b eleIDlimits.py --ID nMinus1  --doPlots 1 --doCutFlow 1 --doYields 1 --doLimits 1  --WP Tight  --iso hybIso03 --removedCut sigmaEtaEta 
