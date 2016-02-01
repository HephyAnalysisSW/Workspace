DIR=//dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_240614/T2DegenerateStop_2J_mStop-100to150-4/
MASSES="100to150"

python redMassScanMETonly.py --job=1 --first=1 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanMETonly.py --job=2 --first=60 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanMETonly.py --job=3 --first=120 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanMETonly.py --job=4 --first=180 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanMETonly.py --job=5 --first=240 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanMETonly.py --job=6 --first=300 --maxFiles=60 --masses=$MASSES -b $DIR & 
python redMassScanMETonly.py --job=7 --first=360 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanMETonly.py --job=8 --first=420 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanMETonly.py --job=9 --first=480 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanMETonly.py --job=10 --first=540 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanMETonly.py --job=11 --first=600 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanMETonly.py --job=12 --first=660 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanMETonly.py --job=13 --first=720 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanMETonly.py --job=14 --first=780 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanMETonly.py --job=15 --first=840 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanMETonly.py --job=16 --first=900 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanMETonly.py --job=17 --first=960 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanMETonly.py --job=18 --first=1020 --maxFiles=23 --masses=$MASSES -b $DIR &
