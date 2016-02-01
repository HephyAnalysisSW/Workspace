#deltaR_ratioPt_Scan.sh
SAMPLES="S300_240FS
S300_270FS
S300_290FS
S300_270
T2tt300_270FS
TTJets
WJets"
#ZJets"

#PRESEL = 0
#MVAWPS = 1

for s in $SAMPLES
   do
      python -b deltaR_ratioPt.py --sample=$s &
   done
