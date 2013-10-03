#!/bin/sh

python convert.py $1 0 25    T1tttt &
python convert.py $1 25 50    T1tttt &
python convert.py $1 50 75    T1tttt &
python convert.py $1 75 100    T1tttt &
python convert.py $1 100 125    T1tttt &
python convert.py $1 125 150    T1tttt &
python convert.py $1 150 175    T1tttt &
python convert.py $1 175 200    T1tttt &

