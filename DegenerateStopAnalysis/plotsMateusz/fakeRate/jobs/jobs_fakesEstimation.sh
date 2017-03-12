python ../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --fakeRateMeasurement MC --lep el --doYields 
python ../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --fakeRateMeasurement MC --lep el --logy 
python ../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --fakeRateMeasurement MC --lep el --doYields --varBins 0 
python ../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --fakeRateMeasurement MC --lep el --logy     --varBins 0 

python ../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --fakeRateMeasurement MC --lep mu --doYields 
python ../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --fakeRateMeasurement MC --lep mu --logy 
python ../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --fakeRateMeasurement MC --lep mu --doYields --varBins 0 
python ../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --fakeRateMeasurement MC --lep mu --logy     --varBins 0 

python ../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --fakeRateMeasurement MC --lep el --doYields 
python ../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --fakeRateMeasurement MC --lep el --logy 
python ../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --fakeRateMeasurement MC --lep el --doYields --varBins 0 
python ../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --fakeRateMeasurement MC --lep el --logy     --varBins 0 

python ../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --fakeRateMeasurement MC --lep mu --doYields 
python ../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --fakeRateMeasurement MC --lep mu --logy 
python ../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --fakeRateMeasurement MC --lep mu --doYields --varBins 0 
python ../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --fakeRateMeasurement MC --lep mu --logy     --varBins 0 
