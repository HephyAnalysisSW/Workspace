python ../../fakeRate.py --region measurement1 --lep el --fakeRateMeasurement data-EWK --varBins
python ../../fakeRate.py --region measurement1 --lep el --fakeRateMeasurement MC       --varBins
python ../../fakeRate.py --region measurement1 --lep mu --fakeRateMeasurement data-EWK --varBins
python ../../fakeRate.py --region measurement1 --lep mu --fakeRateMeasurement MC       --varBins

python ../../fakeRate.py --region measurement1 --lep el --sample qcd                 --varBins 
python ../../fakeRate.py --region measurement1 --lep el --sample tt                  --varBins
python ../../fakeRate.py --region measurement1 --lep el --sample w                   --varBins 
python ../../fakeRate.py --region measurement1 --lep el --sample djetBlind --getData --varBins

python ../../fakeRate.py --region measurement1 --lep mu --sample qcd                 --varBins 
python ../../fakeRate.py --region measurement1 --lep mu --sample tt                  --varBins
python ../../fakeRate.py --region measurement1 --lep mu --sample w                   --varBins
python ../../fakeRate.py --region measurement1 --lep mu --sample djetBlind --getData --varBins
