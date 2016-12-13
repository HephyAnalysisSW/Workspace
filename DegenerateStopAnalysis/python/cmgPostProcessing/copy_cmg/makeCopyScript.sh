echo $1

getCMGFromDPM.py --usernameDPM=$USER --targetBaseDir=/data/$USER/ --targetSubDir=cmgTuples/ --source=/cmgTuples/$1/ --seperator="/" --suggest --strip=_$1 > copy_$1_auto.sh


echo output: copy_$1_auto.sh
