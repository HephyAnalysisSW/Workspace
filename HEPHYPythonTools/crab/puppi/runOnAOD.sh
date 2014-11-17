#!/bin/sh
#source ./setupEnv.sh


export MAXEVENTS="${1:-"-1"}"
export PUPPISTEP="${2:-"Step5"}"
#export FILENAME="${3:-"file:/data/nrad/local/Spring14_TTJets_MiniAOD/Spring14dr_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_AODSIM_PU_S14_POSTLS170_V6-v1MINIAOD.root"}"

export INDIR="${INDIR:-"./"}"
export OUTDIR="${OUTDIR:-"./"}"



#export MAXEVENTS='-1'
#export  PUPPISTEP='Step1'

#export FILENAME="${FILENAME:-"file:/data/schoef/local/Spring14dr_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_AODSIM_PU_S14_POSTLS170_V6-v1.root"}"
#export FILENAME="file:/data/schoef/local/Spring14dr_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_AODSIM_PU_S14_POSTLS170_V6-v1.root"
export PUPPIOUT=`echo ${FILENAME}  | sed "s/data\/schoef/scratch\/nrad/g" | sed "s/.root/Puppi$PUPPISTEP.root/g"`
#echo $PUPPIOUT

export MINIAODOUT=`echo ${PUPPIOUT} | sed "s/.root/MINIAOD.root/g"`
export TUPELOUT=`echo ${MINIAODOUT} | sed "s/.root/Tupel.root/g"`
export CONVERTOUT=`echo ${TUPELOUT} | sed "s/.root/_converted.root/g"`


echo "Input File: "
echo $FILENAME
echo "maxEvents: "
echo $MAXEVENTS
echo "PuppiStep: "
echo $PUPPISTEP

###############

#MiniAOD -> Puppi -> Tupelizer -> Convert

#export PUPPIOUT `echo ${FILENAME} | sed "s/.root/Puppi{$PUPPISTEP}.root/g" | sed  "s/schoef/nrad/g"`
echo "....................."
echo "..................... RUNNING testPuppi"
echo "Puppi Output:"
echo $PUPPIOUT
echo "....................."
###cmsRun testPuppiOnAOD.py file=$INDIR$FILENAME maxEvents=$MAXEVENTS outfile=$OUTDIR$PUPPIOUT
#### this should work too
cmsRun testPuppi.py file=$INDIR$FILENAME maxEvents=$MAXEVENTS outfile=$OUTDIR$PUPPIOUT

#setenv MINIAODOUT `echo ${PUPPIOUT} | sed "s/.root/MINIAOD.root/g"`
echo "....................."
echo "..................... RUNNING MINAODProd"
echo "MINIAOD Output"
echo $MINIAODOUT
echo "....................."
cmsRun miniAODprod_PAT.py file=$OUTDIR$PUPPIOUT maxEvents=$MAXEVENTS outfile=$OUTDIR$MINIAODOUT

#export TUPELOUT `echo ${MINIAODOUT} | sed "s/.root/Tupel.root/g"`
echo "....................."
echo "..................... RUNNING Tupelizer"
echo "Tupelizer Output"
echo $TUPELOUT
echo "....................."
cmsRun ../defaultMINIAODTupelizer_cfg.py files=$OUTDIR$MINIAODOUT  maxEvents=$MAXEVENTS outfile=$OUTDIR$TUPELOUT  keep="*_genMetTrue_*_*,*_pfMet_*_*,*_packedPFCandidates_*_*,*_prunedGenParticles_*_*,*_packedGenParticles_*_*,*_*uppi*_*_*,*_*_*uppi*_*" 

#export CONVERTOUT `echo ${TUPELOUT} | sed "s/.root/_converted.root/g"`
echo "....................."
echo "....................."
echo "..................... RUNNING Convert"
echo "....................."
python ../../../RA4Analysis/CSA14/convert.py --newGenMet --file=$OUTDIR$TUPELOUT  --chmode=copyInc --puppi 




