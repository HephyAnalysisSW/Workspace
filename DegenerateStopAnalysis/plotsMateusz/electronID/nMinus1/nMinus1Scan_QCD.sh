#nMinus1Scan_ZJets.sh
SAMPLE="QCD"

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

PLOTS="misID
misID2"
#efficiency"

#PRESEL = 0
#MVAWPS = 1

for cut in $CUTS
do   
   for p in $PLOTS
   do
      python -b eleIDeffs_nMinus1.py --sample=$SAMPLE --removedCut=$cut --plot=$p --zoom=1 &
      python -b eleIDeffs_nMinus1.py --sample=$SAMPLE --removedCut=$cut --plot=$p --zoom=0 &
   done
done
