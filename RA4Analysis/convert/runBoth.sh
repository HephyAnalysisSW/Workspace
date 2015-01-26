#!/bin/sh
python cmgPostProcessing.py --leptonSelection=soft --samples=$1 &
python cmgPostProcessing.py --leptonSelection=hard --samples=$1 &
