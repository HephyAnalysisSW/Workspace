DIR=//dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_240614/T2DegenerateStop_2J_mStop-325to375-4/
MASSES="325to375"

python redMassScanDPM.py --job=44 --first=1 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=45 --first=60 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=46 --first=120 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=47 --first=180 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=48 --first=240 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=49 --first=300 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=50 --first=360 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=51 --first=420 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=52 --first=480 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=53 --first=540 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=54 --first=600 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=55 --first=660 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=56 --first=720 --maxFiles=25 --masses=$MASSES -b $DIR &
