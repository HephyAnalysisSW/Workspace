#!/bin/sh

export MAXEVENTS="${1:-"-1"}"
export INDIR="file:/data/schoef/local/"
#export OUTDIR="${2:-"file:/data/nrad/local/"}"
export OUTDIR="${2:-"file:./nuGun/"}"



#export FILENAME='file:/data/schoef/local/Spring14dr_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_AODSIM_PU_S14_POSTLS170_V6-v1.root'
#export FILENAME='Spring14dr_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_AODSIM_PU_S14_POSTLS170_V6-v1.root'

#export INDIR="file:/data/nrad/local/ZToMuMu/"
#export FILENAME='Spring14dr_DYJetsToLL_M-50_13TeV-madgraph-pythia8-tauola_v2_AODSIM_PU_S14_POSTLS170_V6-v1.root'

export INDIR="file:/data/nrad/local/Ngun/"
export FILENAME='Spring14dr_Neutrino_Pt-2to20_gun_AODSIM_PU_S14_POSTLS170_V6-v1.root'



#export  PUPPISTEP="${2:-"Step1"}"
echo $MAXEVENTS
echo "INDIR ="
echo $INDIR
echo $FILENAME
echo "OUTDIR ="
echo $OUTDIR

#export FILENAME='file:/data/nrad/local/Spring14_TTJets_MiniAOD/Spring14dr_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_AODSIM_PU_S14_POSTLS170_V6-v1MINIAOD.root'
#export LOG=`echo ${FILENAME} | sed -r "s/file:|\/Spring14_TTJets_MiniAOD//g"`




export LOG=`echo ${FILENAME} | sed -r "s/file://g"  | sed -r "s/data\/schoef/scratch\/nrad/g"`



#./runOnMiniAOD.sh "1" >>&  `echo blah.txt | sed -r "s/.root|file://g"`
export PUPPISTEP="Step1"
./runOnAOD.sh $MAXEVENTS $PUPPISTEP $FILENAME >& `echo ${OUTDIR}${LOG}  | sed "s/file://g" | sed "s/.root/Puppi$PUPPISTEP.txt/g"` &
export PUPPISTEP="Step2"
./runOnAOD.sh $MAXEVENTS $PUPPISTEP $FILENAME >& `echo ${OUTDIR}${LOG}  | sed "s/file://g" | sed "s/.root/Puppi$PUPPISTEP.txt/g"` &
export PUPPISTEP="Step3"
./runOnAOD.sh $MAXEVENTS $PUPPISTEP $FILENAME >& `echo ${OUTDIR}${LOG}  | sed "s/file://g" | sed "s/.root/Puppi$PUPPISTEP.txt/g"` &
export PUPPISTEP="Step4"
./runOnAOD.sh $MAXEVENTS $PUPPISTEP $FILENAME >& `echo ${OUTDIR}${LOG}  | sed "s/file://g" | sed "s/.root/Puppi$PUPPISTEP.txt/g"` &
export PUPPISTEP="Step5"
./runOnAOD.sh $MAXEVENTS $PUPPISTEP $FILENAME >& `echo ${OUTDIR}${LOG}  | sed "s/file://g" | sed "s/.root/Puppi$PUPPISTEP.txt/g"` & 
export PUPPISTEP="Step6"
./runOnAOD.sh $MAXEVENTS $PUPPISTEP $FILENAME >& `echo ${OUTDIR}${LOG}  | sed "s/file://g" | sed "s/.root/Puppi$PUPPISTEP.txt/g"` & 

