python ../../fakeRate.py --region measurement --lep el --fakeRateMeasurement data-EWK --varBins
python ../../fakeRate.py --region measurement --lep el --fakeRateMeasurement MC       --varBins
python ../../fakeRate.py --region measurement --lep mu --fakeRateMeasurement data-EWK --varBins
python ../../fakeRate.py --region measurement --lep mu --fakeRateMeasurement MC       --varBins

python ../../fakeRate.py --region measurement --lep el --sample qcd                 --varBins 
python ../../fakeRate.py --region measurement --lep el --sample tt                  --varBins
python ../../fakeRate.py --region measurement --lep el --sample w                   --varBins 
python ../../fakeRate.py --region measurement --lep el --sample djetBlind --getData --varBins

python ../../fakeRate.py --region measurement --lep mu --sample qcd                 --varBins 
python ../../fakeRate.py --region measurement --lep mu --sample tt                  --varBins
python ../../fakeRate.py --region measurement --lep mu --sample w                   --varBins
python ../../fakeRate.py --region measurement --lep mu --sample djetBlind --getData --varBins
