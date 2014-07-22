#!/bin/sh
python convert.py --chmode=$1 $2 --smsMsqRange=300-325 --samples=sms --keepPDFWeights & 
python convert.py --chmode=$1 $2 --smsMsqRange=325-350 --samples=sms --keepPDFWeights & 
python convert.py --chmode=$1 $2 --smsMsqRange=350-375 --samples=sms --keepPDFWeights & 
python convert.py --chmode=$1 $2 --smsMsqRange=375-400 --samples=sms --keepPDFWeights & 
python convert.py --chmode=$1 $2 --smsMsqRange=400-425 --samples=sms --keepPDFWeights & 
python convert.py --chmode=$1 $2 --smsMsqRange=425-450 --samples=sms --keepPDFWeights & 
python convert.py --chmode=$1 $2 --smsMsqRange=450-475 --samples=sms --keepPDFWeights & 
python convert.py --chmode=$1 $2 --smsMsqRange=475-500 --samples=sms --keepPDFWeights & 
python convert.py --chmode=$1 $2 --smsMsqRange=500-525 --samples=sms --keepPDFWeights & 
