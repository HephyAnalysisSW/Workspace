DIR=//dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_240614/T2DegenerateStop_2J_mStop-250to300-4/
MASSES="250to300"

python redMassScanHT.py --job=33 --first=1 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanHT.py --job=34 --first=60 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanHT.py --job=35 --first=120 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanHT.py --job=36 --first=180 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanHT.py --job=37 --first=240 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanHT.py --job=38 --first=300 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanHT.py --job=39 --first=360 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanHT.py --job=40 --first=420 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanHT.py --job=41 --first=480 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanHT.py --job=42 --first=540 --maxFiles=60 --masses=$MASSES -b $DIR &
python redMassScanHT.py --job=43 --first=600 --maxFiles=62 --masses=$MASSES -b $DIR & 
