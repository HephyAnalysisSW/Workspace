python ../fakesClosure.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --measurementType MC --lep el --doYields             $3 $4  
python ../fakesClosure.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --measurementType MC --lep el --logy                 $3 $4 
python ../fakesClosure.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --measurementType MC --lep el --doYields --varBins 0 $3 $4
python ../fakesClosure.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --measurementType MC --lep el --logy     --varBins 0 $3 $4

python ../fakesClosure.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --measurementType MC --lep mu --doYields  $3 $4 
python ../fakesClosure.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --measurementType MC --lep mu --logy      $3 $4 
python ../fakesClosure.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --measurementType MC --lep mu --doYields  $3 $4 --varBins 0 
python ../fakesClosure.py --region $1 --measurementRegion $2 --doControlPlots --looseNotTight --measurementType MC --lep mu --logy      $3 $4 --varBins 0 
