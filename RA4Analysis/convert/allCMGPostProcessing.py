#!/bin/sh 
 
python cmgPostProcessing.py --samples=WJetsToLNu_HT200to400     --skim=$1 $2  &
python cmgPostProcessing.py --samples=WJetsToLNu_HT400to600     --skim=$1 $2  &
python cmgPostProcessing.py --samples=WJetsToLNu_HT600toInf     --skim=$1 $2  &
python cmgPostProcessing.py --samples=ttJetsCSA1450ns           --skim=$1 $2  &
python cmgPostProcessing.py --samples=T5Full_1200_1000_800      --skim=$1 $2  &
python cmgPostProcessing.py --samples=T5Full_1500_800_100       --skim=$1 $2  &
