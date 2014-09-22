#!/bin/sh
python calcSignalSys2.py $1 $2 250 2500 &
python calcSignalSys2.py $1 $2 150 2500 &
python calcSignalSys2.py $1 $2 250 350 &
python calcSignalSys2.py $1 $2 350 450 &
python calcSignalSys2.py $1 $2 450 2500 &
