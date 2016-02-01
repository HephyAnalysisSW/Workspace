#nMinus1Scan_WJets.sh
SAMPLE="WJets"

CUTS1="None
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

for cut in $CUTS
do   
   for p in $PLOTS
   do
      python -b eleIDeffs_nMinus1.py --sample=$SAMPLE --plot=$p --removedCut=$cut  --zoom=1 & 
      python -b eleIDeffs_nMinus1.py --sample=$SAMPLE --plot=$p --removedCut=$cut  --zoom=0 & 
   done
done
