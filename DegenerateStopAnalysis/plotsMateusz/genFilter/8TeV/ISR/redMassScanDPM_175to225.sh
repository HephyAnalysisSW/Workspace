DIR=//dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_240614/T2DegenerateStop_2J_mStop-175to225-4/
MASSES="175to225"

python redMassScanDPM.py --job=19 --first=1 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=20 --first=60 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=21 --first=120 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=22 --first=180 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=23 --first=240 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=24 --first=300 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=25 --first=360 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=26 --first=420 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=27 --first=480 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=28 --first=540 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=29 --first=600 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=30 --first=660 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=31 --first=720 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanDPM.py --job=32 --first=780 --maxFiles=31 --masses=$MASSES -b $DIR & 
