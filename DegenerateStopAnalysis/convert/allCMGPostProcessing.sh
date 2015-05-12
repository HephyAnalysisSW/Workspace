#!/bin/sh 

#python cmgPostProcessing.py --leptonSelection=hard --samples=T2DegStop_300_270  $2  &   #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=soft --samples=T2DegStop_300_270  $2     #--skim=HT400ST150 

#python cmgPostProcessing.py --leptonSelection=none --samples=TTJets_PU20bx25                 --dontClean=True          $2    
#python cmgPostProcessing.py --leptonSelection=none --samples=T2DegStop_300_270                --dontClean=True         $2     #--skim=HT400ST150 
#python cmgPostProcessing.py --leptonSelection=none --samples=WJetsToLNu_HT100to200_PU20bx25  --dontClean=True          $2  
#python cmgPostProcessing.py --leptonSelection=none --samples=WJetsToLNu_HT200to400_PU20bx25  --dontClean=True          $2   
python cmgPostProcessing.py --leptonSelection=none --samples=WJetsToLNu_HT400to600_PU20bx25  --dontClean=True          $2 &   
python cmgPostProcessing.py --leptonSelection=none --samples=WJetsToLNu_HT600toInf_PU20bx25  --dontClean=True          $2    






#python cmgPostProcessing.py --leptonSelection=soft --samples=WJetsToLNu_HT100to200_PU20bx25  $2   &       
#python cmgPostProcessing.py --leptonSelection=soft --samples=WJetsToLNu_HT200to400_PU20bx25  $2   &      
#python cmgPostProcessing.py --leptonSelection=soft --samples=WJetsToLNu_HT400to600_PU20bx25  $2   &      
#python cmgPostProcessing.py --leptonSelection=soft --samples=WJetsToLNu_HT600toInf_PU20bx25  $2


#python cmgPostProcessing.py --leptonSelection=hard --samples=WJetsToLNu_HT100to200_PU20bx25  $2   &       
#python cmgPostProcessing.py --leptonSelection=hard --samples=WJetsToLNu_HT200to400_PU20bx25  $2   &      
#python cmgPostProcessing.py --leptonSelection=hard --samples=WJetsToLNu_HT400to600_PU20bx25  $2   &      
#python cmgPostProcessing.py --leptonSelection=hard --samples=WJetsToLNu_HT600toInf_PU20bx25  $2
















