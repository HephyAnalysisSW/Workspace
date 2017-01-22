python ../fakeRate.py --region measurement --do2D --lep lep --sample qcd                                
python ../fakeRate.py --region measurement --do2D --lep lep --sample tt       
python ../fakeRate.py --region measurement --do2D --lep lep --sample w        
python ../fakeRate.py --region measurement --do2D --lep lep --sample djetBlind --getData
python ../fakeRate.py --region measurement --do2D --lep lep --fakeRateMeasurement data-EWK 
python ../fakeRate.py --region measurement --do2D --lep lep --fakeRateMeasurement MC 

python ../fakeRate.py --region measurement --do2D --lep el  --sample qcd      
python ../fakeRate.py --region measurement --do2D --lep el  --sample tt       
python ../fakeRate.py --region measurement --do2D --lep el  --sample w        
python ../fakeRate.py --region measurement --do2D --lep el  --sample djetBlind --getData
python ../fakeRate.py --region measurement --do2D --lep el --fakeRateMeasurement data-EWK 
python ../fakeRate.py --region measurement --do2D --lep el --fakeRateMeasurement MC 

python ../fakeRate.py --region measurement --do2D --lep mu  --sample qcd      
python ../fakeRate.py --region measurement --do2D --lep mu  --sample tt       
python ../fakeRate.py --region measurement --do2D --lep mu  --sample w        
python ../fakeRate.py --region measurement --do2D --lep mu  --sample djetBlind --getData
python ../fakeRate.py --region measurement --do2D --lep mu --fakeRateMeasurement data-EWK 
python ../fakeRate.py --region measurement --do2D --lep mu --fakeRateMeasurement MC 
