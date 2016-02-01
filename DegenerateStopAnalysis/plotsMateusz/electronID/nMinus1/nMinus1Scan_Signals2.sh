#nMinus1Scan_Signals2.sh
SAMPLES="S300_270
T2tt300_270FS"
#S300_240FS
#S300_270FS
#S300_290FS"

CUTS="None
sigmaEtaEta
dEta
dPhi
hOverE
ooEmooP
d0
dz
MissingHits
convVeto"

PLOTS="efficiency
misID
misID2"

#PRESEL = 0
#MVAWPS = 1

for s in $SAMPLES
do
   for cut in $CUTS
   do   
      for p in $PLOTS
      do
         python -b eleIDeffs_nMinus1.py --sample=$s --plot=$p --removedCut=$cut --zoom=1 &
         python -b eleIDeffs_nMinus1.py --sample=$s --plot=$p --removedCut=$cut --zoom=0 &
      done
   done
done
