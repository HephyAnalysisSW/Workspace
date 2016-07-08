#! /bin/sh
#SBATCH -J QCD_Mateusz
#SBATCH -a 1-20 
#SBATCH -D /afs/hephy.at/work/m/mzarucki/CMSSW/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/plotsMateusz/QCD/jobs
#SBATCH -o /afs/hephy.at/work/m/mzarucki/CMSSW/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/plotsMateusz/QCD/jobs/logs/job%j_QCD.out
eval `scram runtime -sh`
echo  CMSBASE: $CMSSW_BASE
python -b ../QCDestimation.py       --plot 1 --ABCD 4 --highWeightVeto 1 --eleWP Veto --HT 300 --MET 300                
python -b ../QCDestimation.py       --plot 1 --ABCD 4 --highWeightVeto 1 --eleWP Veto --HT 200 --MET 200                
python -b ../QCDestimation.py       --plot 1 --ABCD 3 --highWeightVeto 1 --eleWP Veto --HT 300 --MET 300 --METloose 300 
python -b ../QCDestimation.py       --plot 1 --ABCD 3 --highWeightVeto 1 --eleWP Veto --HT 300 --MET 300 --METloose 250 
python -b ../QCDestimation.py       --plot 1 --ABCD 3 --highWeightVeto 1 --eleWP Veto --HT 200 --MET 200 --METloose 200 
python -b ../QCDestimation.py       --plot 1 --ABCD 3 --highWeightVeto 1 --eleWP Veto --HT 200 --MET 200 --METloose 150 
python -b ../QCDestimation.py       --plot 1 --ABCD 2 --highWeightVeto 1 --eleWP Veto --HT 300 --MET 300 
python -b ../QCDestimation.py       --plot 1 --ABCD 2 --highWeightVeto 1 --eleWP Veto --HT 200 --MET 200 
python -b ../QCDestimation.py       --plot 1 --ABCD 1 --highWeightVeto 1 --eleWP Veto --HT 300 --MET 300 
python -b ../QCDestimation.py       --plot 1 --ABCD 1 --highWeightVeto 1 --eleWP Veto --HT 200 --MET 200 
python -b ../QCDestimation_index.py --plot 1 --ABCD 4 --highWeightVeto 1 --eleWP Veto --HT 300 --MET 300                
python -b ../QCDestimation_index.py --plot 1 --ABCD 4 --highWeightVeto 1 --eleWP Veto --HT 200 --MET 200                
python -b ../QCDestimation_index.py --plot 1 --ABCD 3 --highWeightVeto 1 --eleWP Veto --HT 300 --MET 300 --METloose 300 
python -b ../QCDestimation_index.py --plot 1 --ABCD 3 --highWeightVeto 1 --eleWP Veto --HT 300 --MET 300 --METloose 250 
python -b ../QCDestimation_index.py --plot 1 --ABCD 3 --highWeightVeto 1 --eleWP Veto --HT 200 --MET 200 --METloose 200 
python -b ../QCDestimation_index.py --plot 1 --ABCD 3 --highWeightVeto 1 --eleWP Veto --HT 200 --MET 200 --METloose 150 
python -b ../QCDestimation_index.py --plot 1 --ABCD 2 --highWeightVeto 1 --eleWP Veto --HT 300 --MET 300 
python -b ../QCDestimation_index.py --plot 1 --ABCD 2 --highWeightVeto 1 --eleWP Veto --HT 200 --MET 200 
python -b ../QCDestimation_index.py --plot 1 --ABCD 1 --highWeightVeto 1 --eleWP Veto --HT 300 --MET 300 
python -b ../QCDestimation_index.py --plot 1 --ABCD 1 --highWeightVeto 1 --eleWP Veto --HT 200 --MET 200 

