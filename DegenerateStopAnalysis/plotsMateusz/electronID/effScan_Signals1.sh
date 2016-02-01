#effScan_Signals1.sh
SAMPLES="S300_240FS
S300_270FS
S300_290FS"
#S300_270
#T2tt300_270FS"

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

for s in $SAMPLES
do
   for id in $IDS
   do
      for p in $PLOTS
      do
         if [ $id = "iso" ]
         then
            for iso in $ISOLATIONS 
            do   
               python -b eleIDeffs.py --sample=$s --id=$id --plot=$p --iso=$iso --zoom=1 &
               python -b eleIDeffs.py --sample=$s --id=$id --plot=$p --iso=$iso --zoom=0 &
            done
         else
               python -b eleIDeffs.py --sample=$s --id=$id --plot=$p --zoom=1 &
               python -b eleIDeffs.py --sample=$s --id=$id --plot=$p --zoom=0 &
         fi
      done
   done
done
