
#./calc_cards_limit.py "../cutbased/cards/13TeV/HT/IsrWeight_2300pbm1/T2_4bd_*.txt" ../../data/limits/RunII_HT_SysAdjust_IsrWeight_2300pbm1/limits.pkl
#./calc_cards_limit.py "../cutbased/cards/8TeV/Full/T2DegStop_*.txt" ../../data/limits/8TeV/Full/limits.pkl
#./calc_cards_limit.py "../cutbased/cards/13TeV/IsrWeight_2200pbm1/T2_4bd_*.txt" ../../data/limits/RunII_IsrWeight/limits.pkl
#./calc_cards_limit.py "../cutbased/cards/13TeV/SysAdjust_IsrWeight/T2_4bd_*.txt" ../../data/limits/RunII_SysAdjust_IsrWeight/limits.pkl

cardDir="/afs/hephy.at/user/n/nrad/CMSSW/fork/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/plotsNavid/data/cards/8TeV/Bins"

#./calc_cards_limit.py "$cardDir/SRH1a/T2Deg*.txt"   "$cardDir/SRH1a.pkl" 
#./calc_cards_limit.py "$cardDir/SRH1b/T2Deg*.txt"   "$cardDir/SRH1b.pkl" 
#./calc_cards_limit.py "$cardDir/SRH1c/T2Deg*.txt"   "$cardDir/SRH1c.pkl" 
#./calc_cards_limit.py "$cardDir/SRH2/T2Deg*.txt"    "$cardDir/SRH2.pkl"
#./calc_cards_limit.py "$cardDir/SRL1a/T2Deg*.txt"   "$cardDir/SRL1a.pkl" 
#./calc_cards_limit.py "$cardDir/SRL1b/T2Deg*.txt"   "$cardDir/SRL1b.pkl" 
#./calc_cards_limit.py "$cardDir/SRL1c/T2Deg*.txt"   "$cardDir/SRL1c.pkl" 
#./calc_cards_limit.py "$cardDir/SRL2/T2Deg*.txt"    "$cardDir/SRL2.pkl"
#./calc_cards_limit.py "$cardDir/SRV1a/T2Deg*.txt"   "$cardDir/SRV1a.pkl" 
#./calc_cards_limit.py "$cardDir/SRV1b/T2Deg*.txt"   "$cardDir/SRV1b.pkl" 
#./calc_cards_limit.py "$cardDir/SRV1c/T2Deg*.txt"   "$cardDir/SRV1c.pkl" 
#./calc_cards_limit.py "$cardDir/SRV2/T2Deg*.txt"    "$cardDir/SRV2.pkl"


#./calc_cards_limit.py "$cardDir/SRSL1/T2Deg*.txt"      "$cardDir/SRSL1.pkl"
#./calc_cards_limit.py "$cardDir/SRSL1a/T2Deg*.txt"     "$cardDir/SRSL1a.pkl"
#./calc_cards_limit.py "$cardDir/SRSL1b/T2Deg*.txt"     "$cardDir/SRSL1b.pkl"
#./calc_cards_limit.py "$cardDir/SRSL1c/T2Deg*.txt"     "$cardDir/SRSL1c.pkl"
#./calc_cards_limit.py "$cardDir/SRSL2/T2Deg*.txt"      "$cardDir/SRSL2.pkl"
#./calc_cards_limit.py "$cardDir/SRV1a/T2Deg*.txt"      "$cardDir/SRV1a.pkl"



cardDirs="/afs/hephy.at/user/n/nrad/CMSSW/fork/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/plotsNavid/data/cards/13TeV/Reload_IsrWeight/Bins/"
cardPattern="T2_4bd*.txt"

#for card in `ls $cardDirs/$cardPattern`
for cardDir in `ls -d $cardDirs/*`
    do 
    cardDirBase=`basename $cardDir`
    #echo $cardDir
    #echo $cardDirBase  ${cardDir##*/}

    #echo ./calc_cards_limit.py  "$cardDir/$cardPattern"     "$cardDirs/$cardDirBase.pkl"  
    ./calc_cards_limit.py  "$cardDir/$cardPattern"     "$cardDirs/$cardDirBase.pkl"  &
    done



