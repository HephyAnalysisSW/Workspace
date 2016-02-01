DIR=//dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_240614/T2DegenerateStop_2J_mStop-400-4/
MASSES="400"

python redMassScanISR.py --job=57 --first=1 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanISR.py --job=58 --first=60 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanISR.py --job=59 --first=120 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanISR.py --job=60 --first=180 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanISR.py --job=61 --first=240 --maxFiles=26 --masses=$MASSES -b $DIR &
