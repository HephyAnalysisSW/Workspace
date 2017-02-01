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

python ../fakeRate.py --region measurement --lep el  --sample qcd                   --varBins 
python ../fakeRate.py --region measurement --lep el  --sample tt                    --varBins
python ../fakeRate.py --region measurement --lep el  --sample w                     --varBins 
python ../fakeRate.py --region measurement --lep el  --sample djetBlind --getData   --varBins
python ../fakeRate.py --region measurement --lep el  --fakeRateMeasurement data-EWK --varBins
python ../fakeRate.py --region measurement --lep el  --fakeRateMeasurement MC       --varBins

python ../fakeRate.py --region measurement --lep mu  --sample qcd                   --varBins 
python ../fakeRate.py --region measurement --lep mu  --sample tt                    --varBins
python ../fakeRate.py --region measurement --lep mu  --sample w                     --varBins
python ../fakeRate.py --region measurement --lep mu  --sample djetBlind --getData   --varBins
python ../fakeRate.py --region measurement --lep mu  --fakeRateMeasurement data-EWK --varBins
python ../fakeRate.py --region measurement --lep mu  --fakeRateMeasurement MC       --varBins
