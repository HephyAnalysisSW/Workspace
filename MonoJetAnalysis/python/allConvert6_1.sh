#!/bin/sh
python convert.py --chmode=$1 --smsMsqRange=300-325 --samples=sms --keppPDFWeights & 
python convert.py --chmode=$1 --smsMsqRange=325-350 --samples=sms --keppPDFWeights & 
python convert.py --chmode=$1 --smsMsqRange=350-375 --samples=sms --keppPDFWeights & 
python convert.py --chmode=$1 --smsMsqRange=375-400 --samples=sms --keppPDFWeights & 
python convert.py --chmode=$1 --smsMsqRange=400-425 --samples=sms --keppPDFWeights & 
python convert.py --chmode=$1 --smsMsqRange=425-450 --samples=sms --keppPDFWeights & 
python convert.py --chmode=$1 --smsMsqRange=450-475 --samples=sms --keppPDFWeights & 
python convert.py --chmode=$1 --smsMsqRange=475-500 --samples=sms --keppPDFWeights & 
python convert.py --chmode=$1 --smsMsqRange=500-525 --samples=sms --keppPDFWeights & 
