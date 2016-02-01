#effScan_WJets.sh
SAMPLE="WJets"

IDS="standard
noIso
iso"

PLOTS="efficiency
misID
misID2"

ISOLATIONS="miniRelIso
relIso03
relIso04" #relIsoAn04

#PRESEL = 0
#MVAWPS = 1

for id in $IDS
do   
   for p in $PLOTS
   do
      if [ $id = "iso" ]
      then
         for iso in $ISOLATIONS
         do   
            python -b eleIDeffs.py --sample=$SAMPLE --id=$id --plot=$p --iso=$iso --zoom=1 &
            python -b eleIDeffs.py --sample=$SAMPLE --id=$id --plot=$p --iso=$iso --zoom=0 &
         done
      else
         python -b eleIDeffs.py --sample=$SAMPLE --id=$id --plot=$p --zoom=1 &
         python -b eleIDeffs.py --sample=$SAMPLE --id=$id --plot=$p --zoom=0 &
      fi
   done
done
