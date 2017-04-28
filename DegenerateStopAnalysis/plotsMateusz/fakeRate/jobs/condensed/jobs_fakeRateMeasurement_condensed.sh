python ../../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 lt --measurementType MC
python ../../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 lt --measurementType MC
python ../../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 lt --measurementType MC       --varBins 0 --do2D
python ../../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 lt --measurementType MC       --varBins 0 --do2D

python ../../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 lt --measurementType MC-EWK  
python ../../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 lt --measurementType MC-EWK  
python ../../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 lt --measurementType MC-EWK   --varBins 0 --do2D
python ../../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 lt --measurementType MC-EWK   --varBins 0 --do2D

python ../../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 lt --measurementType data-EWK
python ../../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 lt --measurementType data-EWK
python ../../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 lt --measurementType data-EWK --varBins 0 --do2D
python ../../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 lt --measurementType data-EWK --varBins 0 --do2D

python ../../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 lt --measurementType data-EWK                    --noWttWeights
python ../../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 lt --measurementType data-EWK                    --noWttWeights
python ../../fakeRate.py --region $1 --doYields --logy --lep el --eta1p5 lt --measurementType data-EWK --varBins 0 --do2D --noWttWeights
python ../../fakeRate.py --region $1 --doYields --logy --lep mu --eta1p5 lt --measurementType data-EWK --varBins 0 --do2D --noWttWeights
