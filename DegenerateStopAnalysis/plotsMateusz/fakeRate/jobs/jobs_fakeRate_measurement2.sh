python ../fakeRate.py --region measurement --lep lep --sample qcd                               --varBins  
python ../fakeRate.py --region measurement --lep lep --sample tt                                --varBins 
python ../fakeRate.py --region measurement --lep lep --sample w                                 --varBins 
python ../fakeRate.py --region measurement --lep lep --sample djetBlind --getData               --varBins
python ../fakeRate.py --region measurement --lep lep --sample djetBlind --getData --subtractEWK --varBins

python ../fakeRate.py --region measurement --lep el  --sample qcd                               --varBins 
python ../fakeRate.py --region measurement --lep el  --sample tt                                --varBins
python ../fakeRate.py --region measurement --lep el  --sample w                                 --varBins 
python ../fakeRate.py --region measurement --lep el  --sample djetBlind --getData               --varBins
python ../fakeRate.py --region measurement --lep el  --sample djetBlind --getData --subtractEWK --varBins

python ../fakeRate.py --region measurement --lep mu  --sample qcd                               --varBins 
python ../fakeRate.py --region measurement --lep mu  --sample tt                                --varBins
python ../fakeRate.py --region measurement --lep mu  --sample w                                 --varBins
python ../fakeRate.py --region measurement --lep mu  --sample djetBlind --getData               --varBins
python ../fakeRate.py --region measurement --lep mu  --sample djetBlind --getData --subtractEWK --varBins
