#!/bin/sh
python makePDFYieldHistos.py --sms $1  --htl 0 --hth 2500 --metl 0 --meth 2500  --btb none &

python makePDFYieldHistos.py --sms $1  --htl 750 --hth 2500 --metl 250 --meth 350  --btb 2 &
python makePDFYieldHistos.py --sms $1  --htl 750 --hth 2500 --metl 350 --meth 450  --btb 2 &
python makePDFYieldHistos.py --sms $1  --htl 750 --hth 2500 --metl 450 --meth 2500 --btb 2 &

python makePDFYieldHistos.py --sms $1  --htl 750 --hth 2500 --metl 150 --meth 250  --btb 3p &
python makePDFYieldHistos.py --sms $1  --htl 750 --hth 2500 --metl 250 --meth 350  --btb 3p &
python makePDFYieldHistos.py --sms $1  --htl 750 --hth 2500 --metl 350 --meth 450  --btb 3p &

python makePDFYieldHistos.py --sms $1  --htl 750 --hth 2500 --metl 450 --meth 2500 --btb 3p &
python makePDFYieldHistos.py --sms $1  --htl 400 --hth 750 --metl 150 --meth 250  --btb 3p &
python makePDFYieldHistos.py --sms $1  --htl 400 --hth 750 --metl 250 --meth 2500 --btb 3p &
