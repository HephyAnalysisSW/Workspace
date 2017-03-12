python ../../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --fakeRateMeasurement MC --lep el --doYields             $3 $4 
python ../../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --fakeRateMeasurement MC --lep el --logy                 $3 $4  
python ../../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --fakeRateMeasurement MC --lep el --doYields --varBins 0 $3 $4
python ../../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --fakeRateMeasurement MC --lep el --logy     --varBins 0 $3 $4
python ../../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --fakeRateMeasurement MC --lep mu --doYields             $3 $4 
python ../../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --fakeRateMeasurement MC --lep mu --logy                 $3 $4 
python ../../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --fakeRateMeasurement MC --lep mu --doYields --varBins 0 $3 $4
python ../../fakesEstimation.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --fakeRateMeasurement MC --lep mu --logy     --varBins 0 $3 $4
