#!/bin/sh 

python cmgPostProcessing.py --leptonSelection=$1 --samples=T2DegStop_test  $2   &  #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=$1 --samples=SMS_T5qqqqWW_Gl1500_Chi800_LSP100  $2   &  #--skim=HT400ST150 


