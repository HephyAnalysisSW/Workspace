python ../fakeRate.py --region measurement1 --lep el --fakeRateMeasurement MC       --do2D 
python ../fakeRate.py --region measurement1 --lep mu --fakeRateMeasurement MC       --do2D 

python ../fakeRate.py --region measurement1 --lep el --fakeRateMeasurement MC       --varBins
python ../fakeRate.py --region measurement1 --lep mu --fakeRateMeasurement MC       --varBins

python ../fakeRate.py --region measurement1 --lep el --sample qcd                 --do2D  
python ../fakeRate.py --region measurement1 --lep el --sample tt                  --do2D 
python ../fakeRate.py --region measurement1 --lep el --sample w                   --do2D 
python ../fakeRate.py --region measurement1 --lep el --sample djetBlind --getData --do2D 

python ../fakeRate.py --region measurement1 --lep mu --sample qcd                 --do2D 
python ../fakeRate.py --region measurement1 --lep mu --sample tt                  --do2D 
python ../fakeRate.py --region measurement1 --lep mu --sample w                   --do2D 
python ../fakeRate.py --region measurement1 --lep mu --sample djetBlind --getData --do2D 

python ../fakeRate.py --region measurement1 --lep el --sample qcd                 --varBins 
python ../fakeRate.py --region measurement1 --lep el --sample tt                  --varBins
python ../fakeRate.py --region measurement1 --lep el --sample w                   --varBins 
python ../fakeRate.py --region measurement1 --lep el --sample djetBlind --getData --varBins

python ../fakeRate.py --region measurement1 --lep mu --sample qcd                 --varBins 
python ../fakeRate.py --region measurement1 --lep mu --sample tt                  --varBins
python ../fakeRate.py --region measurement1 --lep mu --sample w                   --varBins
python ../fakeRate.py --region measurement1 --lep mu --sample djetBlind --getData --varBins
