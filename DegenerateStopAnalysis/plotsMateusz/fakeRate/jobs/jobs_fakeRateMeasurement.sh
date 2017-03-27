python ../fakeRate.py --region $1 --doYields --logy --lep el --fakeRateMeasurement MC
python ../fakeRate.py --region $1 --doYields --logy --lep mu --fakeRateMeasurement MC
python ../fakeRate.py --region $1 --doYields --logy --lep el --fakeRateMeasurement MC       --varBins 0 --do2D
python ../fakeRate.py --region $1 --doYields --logy --lep mu --fakeRateMeasurement MC       --varBins 0 --do2D

python ../fakeRate.py --region $1 --doYields --logy --lep el --fakeRateMeasurement MC-EWK  
python ../fakeRate.py --region $1 --doYields --logy --lep mu --fakeRateMeasurement MC-EWK  
python ../fakeRate.py --region $1 --doYields --logy --lep el --fakeRateMeasurement MC-EWK   --varBins 0 --do2D
python ../fakeRate.py --region $1 --doYields --logy --lep mu --fakeRateMeasurement MC-EWK   --varBins 0 --do2D

python ../fakeRate.py --region $1 --doYields --logy --lep el --fakeRateMeasurement data-EWK
python ../fakeRate.py --region $1 --doYields --logy --lep mu --fakeRateMeasurement data-EWK
python ../fakeRate.py --region $1 --doYields --logy --lep el --fakeRateMeasurement data-EWK --varBins 0 --do2D
python ../fakeRate.py --region $1 --doYields --logy --lep mu --fakeRateMeasurement data-EWK --varBins 0 --do2D

python ../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 gt --fakeRateMeasurement MC
python ../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 gt --fakeRateMeasurement MC
python ../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 gt --fakeRateMeasurement MC       --varBins 0 --do2D
python ../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 gt --fakeRateMeasurement MC       --varBins 0 --do2D

python ../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 gt --fakeRateMeasurement MC-EWK  
python ../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 gt --fakeRateMeasurement MC-EWK  
python ../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 gt --fakeRateMeasurement MC-EWK   --varBins 0 --do2D
python ../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 gt --fakeRateMeasurement MC-EWK   --varBins 0 --do2D

python ../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 gt --fakeRateMeasurement data-EWK
python ../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 gt --fakeRateMeasurement data-EWK
python ../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 gt --fakeRateMeasurement data-EWK --varBins 0 --do2D
python ../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 gt --fakeRateMeasurement data-EWK --varBins 0 --do2D

python ../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 lt --fakeRateMeasurement MC
python ../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 lt --fakeRateMeasurement MC
python ../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 lt --fakeRateMeasurement MC       --varBins 0 --do2D
python ../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 lt --fakeRateMeasurement MC       --varBins 0 --do2D

python ../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 lt --fakeRateMeasurement MC-EWK  
python ../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 lt --fakeRateMeasurement MC-EWK  
python ../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 lt --fakeRateMeasurement MC-EWK   --varBins 0 --do2D
python ../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 lt --fakeRateMeasurement MC-EWK   --varBins 0 --do2D

python ../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 lt --fakeRateMeasurement data-EWK
python ../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 lt --fakeRateMeasurement data-EWK
python ../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 lt --fakeRateMeasurement data-EWK --varBins 0 --do2D
python ../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 lt --fakeRateMeasurement data-EWK --varBins 0 --do2D

