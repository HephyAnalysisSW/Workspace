#!/bin/sh
python convert.py --chmode=$1 --smsMsqRange=100-125 --samples=sms --keepPDFWeights & 
python convert.py --chmode=$1 --smsMsqRange=125-150 --samples=sms --keepPDFWeights & 
python convert.py --chmode=$1 --smsMsqRange=150-175 --samples=sms --keepPDFWeights & 
python convert.py --chmode=$1 --smsMsqRange=175-200 --samples=sms --keepPDFWeights & 
python convert.py --chmode=$1 --smsMsqRange=200-225 --samples=sms --keepPDFWeights & 
python convert.py --chmode=$1 --smsMsqRange=225-250 --samples=sms --keepPDFWeights & 
python convert.py --chmode=$1 --smsMsqRange=250-275 --samples=sms --keepPDFWeights & 
python convert.py --chmode=$1 --smsMsqRange=275-300 --samples=sms --keepPDFWeights & 
