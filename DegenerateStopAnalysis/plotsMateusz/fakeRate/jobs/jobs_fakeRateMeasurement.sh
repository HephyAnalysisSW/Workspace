python ../fakeRate.py --region $1 --lep el --fakeRateMeasurement MC
python ../fakeRate.py --region $1 --lep mu --fakeRateMeasurement MC
python ../fakeRate.py --region $1 --lep el --fakeRateMeasurement MC       --varBins 0 --do2D
python ../fakeRate.py --region $1 --lep mu --fakeRateMeasurement MC       --varBins 0 --do2D

python ../fakeRate.py --region $1 --lep el --fakeRateMeasurement MC-EWK  
python ../fakeRate.py --region $1 --lep mu --fakeRateMeasurement MC-EWK  
python ../fakeRate.py --region $1 --lep el --fakeRateMeasurement MC-EWK   --varBins 0 --do2D
python ../fakeRate.py --region $1 --lep mu --fakeRateMeasurement MC-EWK   --varBins 0 --do2D

python ../fakeRate.py --region $1 --lep el --fakeRateMeasurement data-EWK
python ../fakeRate.py --region $1 --lep mu --fakeRateMeasurement data-EWK
python ../fakeRate.py --region $1 --lep el --fakeRateMeasurement data-EWK --varBins 0 --do2D
python ../fakeRate.py --region $1 --lep mu --fakeRateMeasurement data-EWK --varBins 0 --do2D
