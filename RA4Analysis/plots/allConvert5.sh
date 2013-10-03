#!/bin/sh
python convert.py $1 900  925  T1tttt &
python convert.py $1 925  950  T1tttt &
python convert.py $1 950  975  T1tttt &
python convert.py $1 975  1000 T1tttt &
python convert.py $1 1000 1025  T1tttt &
python convert.py $1 1025 1050  T1tttt &
python convert.py $1 1050 1175 T1tttt &

