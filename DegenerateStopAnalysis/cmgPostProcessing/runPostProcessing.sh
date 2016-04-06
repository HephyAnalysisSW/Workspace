#PROC_TAG=mAODv2_v4_SMSScan_v1
#PROC_TAG=7412pass2_SMSScan_v3
PROC_TAG=7412pass2_SMSScan_PUTTHISINV3
skimPreselect=true
overwrite=true





signals=false
sigscan=false
sigscan1=false
sigscan2=false
sigscan3=false
sigscan4=false
sigscan5=false
data=false
wjets=false
ttjets=false
qcd=false
zjets=false
dyjets=false

for i in "$@"
do 
case $i in 
    signals)
    signals=true
    echo Will Process Signals:  $signals 
    shift
    ;;

    data)
    data=true
    echo Will Process Data:  $data 
    shift
    ;;
    wjets)
    wjets=true
    echo Will Process WJets:  $wjets
    shift
    ;;
    ttjets)
    ttjets=true
    echo Will Process TTJets:  $ttjets
    shift
    ;;

    qcd)
    qcd=true
    echo Will Process QCD:  $qcd
    shift
    ;;

    zjets)
    zjets=true
    echo Will Process ZJets:  $zjets
    shift
    ;;

    dyjets)
    dyjets=true
    echo Will Process DYJets:  $dyjets
    shift
    ;;

    sigscan)
    sigscan=true
    echo Will Process Sig Mass Scan:  $sigscan
    shift
    ;;

    sigscan1)
    sigscan1=true
    echo Will Process Sig Mass Scan1:  $sigscan1
    shift
    ;;


    sigscan2)
    sigscan2=true
    echo Will Process Sig Mass Scan2:  $sigscan2
    shift
    ;;

    sigscan3)
    sigscan3=true
    echo Will Process Sig Mass Scan3:  $sigscan3
    shift
    ;;


    sigscan4)
    sigscan4=true
    echo Will Process Sig Mass Scan4:  $sigscan4
    shift
    ;;


    sigscan5)
    sigscan5=true
    echo Will Process Sig Mass Scan5:  $sigscan5
    shift
    ;;

esac
done


echo ------------------------------------------------------------------

echo Processing TAG: $PROC_TAG
echo Preselect: $skimPreselect
echo
echo



echo ------------------------------------------------------------------

if $skimPreselect
then
    PRESEL="--skimPreselect"
fi

if $overwrite
then
    OVERWRITE="--overwriteOutputFiles"
fi





#signals=false
#sigscan=false
#data=false
#wjets=false
#ttjets=false
#qcd=false
#zjets=false




if $signals
then
    echo -----------------------------  PROCESSING SIGNAL --------------------------------
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=T2tt_300_270_FastSim        &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=T2DegStop_300_270           &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=T2DegStop_300_290_FastSim   &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=T2DegStop_300_240_FastSim   &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=T2DegStop_300_270_FastSim   &
fi

if $wjets
then
    echo -----------------------------  PROCESSING WJets --------------------------------
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=WJetsToLNu              &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=WJetsToLNu_HT100to200   &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=WJetsToLNu_HT200to400   &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=WJetsToLNu_HT400to600   &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=WJetsToLNu_HT600toInf   &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=WJetsToLNu_HT600to800   &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=WJetsToLNu_HT800to1200  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=WJetsToLNu_HT1200to2500 &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=WJetsToLNu_HT2500toInf  &
fi

if $ttjets
then
    echo -----------------------------  PROCESSING TTJets --------------------------------
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=TTJets_LO              &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --skim=lheHTlow    --processSample=TTJets_LO              &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --skim=lheHThigh    --processSample=TTJets_LO_HT600to800   &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=TTJets_LO_HT800to1200  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=TTJets_LO_HT1200to2500 &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=TTJets_LO_HT2500toInf  &
fi


if $zjets
then
    echo -----------------------------  PROCESSING ZtoInv --------------------------------
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=ZJetsToNuNu_HT100to200 &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=ZJetsToNuNu_HT200to400 &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=ZJetsToNuNu_HT400to600 &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=ZJetsToNuNu_HT600toInf &
fi
#



if $dyjets
then
    echo -----------------------------  PROCESSING DY --------------------------------
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=DYJetsToLL_M5to50_LO &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=DYJetsToNuNu_M50 &

    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=ZJetsToNuNu_HT100to200 &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=ZJetsToNuNu_HT200to400 &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=ZJetsToNuNu_HT400to600 &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=ZJetsToNuNu_HT600toInf &
fi
#


if $qcd
then
    echo -----------------------------  PROCESSING QCD --------------------------------
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=QCD_HT200to300   &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=QCD_HT300to500   &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=QCD_HT500to700   &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=QCD_HT700to1000  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=QCD_HT1000to1500 &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=QCD_HT1500to2000 &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --processSample=QCD_HT2000toInf  &
fi



if $data
then

    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=Data_25ns --processSample=MET_Run2015D_05Oct            &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=Data_25ns --processSample=MET_Run2015D_v4               &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=Data_25ns --processSample=SingleElectron_Run2015D_05Oct &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=Data_25ns --processSample=SingleElectron_Run2015D_v4    &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=Data_25ns --processSample=SingleMuon_Run2015D_05Oct     &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=Data_25ns --processSample=SingleMuon_Run2015D_v4        &


fi





if $sigscan1
then

    echo -----------------------------  PROCESSING SIGNAL SCAN 1--------------------------------
    
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_100_mLSP_20to90 --processSignalScan 100 20  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_100_mLSP_20to90 --processSignalScan 100 30  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_100_mLSP_20to90 --processSignalScan 100 40  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_100_mLSP_20to90 --processSignalScan 100 50  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_100_mLSP_20to90 --processSignalScan 100 60  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_100_mLSP_20to90 --processSignalScan 100 70  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_100_mLSP_20to90 --processSignalScan 100 80  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_100_mLSP_20to90 --processSignalScan 100 90  &
    
    
        
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_125_mLSP_45to115                             --processSignalScan 125 45  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_125_mLSP_45to115                             --processSignalScan 125 55  &  
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_125_mLSP_45to115                             --processSignalScan 125 65  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_125_mLSP_45to115                             --processSignalScan 125 75  &

    wait

    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_125_mLSP_45to115                             --processSignalScan 125 85  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_125_mLSP_45to115                             --processSignalScan 125 95  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_125_mLSP_45to115                             --processSignalScan 125 105 &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_125_mLSP_45to115                             --processSignalScan 125 115 &
    
   

    
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_200_mLSP_120to190                             --processSignalScan 200 120  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_200_mLSP_120to190                             --processSignalScan 200 130  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_200_mLSP_120to190                             --processSignalScan 200 140  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_200_mLSP_120to190                             --processSignalScan 200 150  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_200_mLSP_120to190                             --processSignalScan 200 160  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_200_mLSP_120to190                             --processSignalScan 200 170  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_200_mLSP_120to190                             --processSignalScan 200 180  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_200_mLSP_120to190                             --processSignalScan 200 190  &
fi

if $sigscan2
then

    echo -----------------------------  PROCESSING SIGNAL SCAN 2--------------------------------
    
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_225_mLSP_145to225                             --processSignalScan 225 145  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_225_mLSP_145to225                             --processSignalScan 225 155  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_225_mLSP_145to225                             --processSignalScan 225 165  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_225_mLSP_145to225                             --processSignalScan 225 175  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_225_mLSP_145to225                             --processSignalScan 225 185  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_225_mLSP_145to225                             --processSignalScan 225 195  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_225_mLSP_145to225                             --processSignalScan 225 205  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_225_mLSP_145to225                             --processSignalScan 225 215  &
   

 
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_275_mLSP_195to265                             --processSignalScan 275 195  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_275_mLSP_195to265                             --processSignalScan 275 205  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_275_mLSP_195to265                             --processSignalScan 275 215  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_275_mLSP_195to265                             --processSignalScan 275 225  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_275_mLSP_195to265                             --processSignalScan 275 235  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_275_mLSP_195to265                             --processSignalScan 275 245  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_275_mLSP_195to265                             --processSignalScan 275 255  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_275_mLSP_195to265                             --processSignalScan 275 265  &
    #
    #wait
   
    
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_300_mLSP_220to290                             --processSignalScan 300 220  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_300_mLSP_220to290                             --processSignalScan 300 230  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_300_mLSP_220to290                             --processSignalScan 300 240  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_300_mLSP_220to290                             --processSignalScan 300 250  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_300_mLSP_220to290                             --processSignalScan 300 260  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_300_mLSP_220to290                             --processSignalScan 300 270  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_300_mLSP_220to290                             --processSignalScan 300 280  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_300_mLSP_220to290                             --processSignalScan 300 290  &
fi


if $sigscan3
then

    echo -----------------------------  PROCESSING SIGNAL SCAN 3--------------------------------
 
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_325_mLSP_245to315   --processSignalScan 325 245  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_325_mLSP_245to315   --processSignalScan 325 255  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_325_mLSP_245to315   --processSignalScan 325 265  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_325_mLSP_245to315   --processSignalScan 325 275  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_325_mLSP_245to315   --processSignalScan 325 285  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_325_mLSP_245to315   --processSignalScan 325 295  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_325_mLSP_245to315   --processSignalScan 325 305  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_325_mLSP_245to315   --processSignalScan 325 315  &
    

    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_350_mLSP_270to340   --processSignalScan 350 270  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_350_mLSP_270to340   --processSignalScan 350 280  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_350_mLSP_270to340   --processSignalScan 350 290  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_350_mLSP_270to340   --processSignalScan 350 300  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_350_mLSP_270to340   --processSignalScan 350 310  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_350_mLSP_270to340   --processSignalScan 350 320  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_350_mLSP_270to340   --processSignalScan 350 330  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_350_mLSP_270to340   --processSignalScan 350 340  &
    
    #wait 
    
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_375_mLSP_295to365   --processSignalScan 375 295  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_375_mLSP_295to365   --processSignalScan 375 305  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_375_mLSP_295to365   --processSignalScan 375 315  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_375_mLSP_295to365   --processSignalScan 375 325  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_375_mLSP_295to365   --processSignalScan 375 335  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_375_mLSP_295to365   --processSignalScan 375 345  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_375_mLSP_295to365   --processSignalScan 375 355  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_375_mLSP_295to365   --processSignalScan 375 365  &

fi
  


if $sigscan4
then

    echo -----------------------------  PROCESSING SIGNAL SCAN 4--------------------------------

  
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_400_mLSP_320to390                             --processSignalScan 400 320  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_400_mLSP_320to390                             --processSignalScan 400 330  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_400_mLSP_320to390                             --processSignalScan 400 340  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_400_mLSP_320to390                             --processSignalScan 400 350  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_400_mLSP_320to390                             --processSignalScan 400 360  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_400_mLSP_320to390                             --processSignalScan 400 370  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_400_mLSP_320to390                             --processSignalScan 400 380  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_400_mLSP_320to390                             --processSignalScan 400 390  &
   
    wait

 
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 550 470  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 550 480  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 550 490  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 550 500  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 550 510  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 550 520  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 550 530  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 550 540  &
     
    
    
fi


if $sigscan5
then

    echo -----------------------------  PROCESSING SIGNAL SCAN 5 --------------------------------


    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 575 495  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 575 505  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 575 515  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 575 525  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 575 535  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 575 545  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 575 555  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 575 565  &


    wait


    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 600 520  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 600 530  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 600 540  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 600 550  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 600 560  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 600 570  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 600 580  &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_550to600_mLSP_470to590                             --processSignalScan 600 590  &

fi



    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --skim=lheHTlow    --processSample=TTJets_LO              &
    python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc $PRESEL --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns --skim=lheHThigh    --processSample=TTJets_LO_HT600to800   &


#if true
#then

    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_325_mLSP_245to315   --processSignalScan 325 245  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_325_mLSP_245to315   --processSignalScan 325 255  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_325_mLSP_245to315   --processSignalScan 325 265  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_325_mLSP_245to315   --processSignalScan 325 275  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_325_mLSP_245to315   --processSignalScan 325 285  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_325_mLSP_245to315   --processSignalScan 325 295  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_325_mLSP_245to315   --processSignalScan 325 305  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_325_mLSP_245to315   --processSignalScan 325 315  &
    

    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_350_mLSP_270to340   --processSignalScan 350 270  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_350_mLSP_270to340   --processSignalScan 350 280  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_350_mLSP_270to340   --processSignalScan 350 290  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_350_mLSP_270to340   --processSignalScan 350 300  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_350_mLSP_270to340   --processSignalScan 350 310  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_350_mLSP_270to340   --processSignalScan 350 320  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_350_mLSP_270to340   --processSignalScan 350 330  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_350_mLSP_270to340   --processSignalScan 350 340  &
    
  
    
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_375_mLSP_295to365   --processSignalScan 375 295  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_375_mLSP_295to365   --processSignalScan 375 305  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_375_mLSP_295to365   --processSignalScan 375 315  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_375_mLSP_295to365   --processSignalScan 375 325  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_375_mLSP_295to365   --processSignalScan 375 335  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_375_mLSP_295to365   --processSignalScan 375 345  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_375_mLSP_295to365   --processSignalScan 375 355  &
    #python cmgPostProcessing_v1.py $OVERWRITE --skimLepton=inc  --logLevel=INFO --processingTag=$PROC_TAG --cmgTuples=RunIISpring15DR74_25ns $PRESEL --processSample=SMS_T2_4bd_mStop_375_mLSP_295to365   --processSignalScan 375 365  &



#fi

wait
echo ------------------------------------------ DONE --------------------------------------------------
