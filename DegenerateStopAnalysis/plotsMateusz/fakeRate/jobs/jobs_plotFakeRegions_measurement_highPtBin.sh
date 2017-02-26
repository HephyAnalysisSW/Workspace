python ../plotFakeRegions.py --lep el  --WP tight --region measurement1 --highPtBin --doControlPlots --doYields 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement1 --highPtBin --doControlPlots --doYields 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement1 --highPtBin --doControlPlots --doYields 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement1 --highPtBin --doControlPlots --doYields 

python ../plotFakeRegions.py --lep el  --WP tight --region measurement1 --highPtBin --doControlPlots --varBins 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement1 --highPtBin --doControlPlots --varBins 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement1 --highPtBin --doControlPlots --varBins 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement1 --highPtBin --doControlPlots --varBins

python ../plotFakeRegions.py --lep el  --WP tight --region measurement1 --highPtBin --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement1 --highPtBin --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement1 --highPtBin --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement1 --highPtBin --doControlPlots           --logy 0 

python ../plotFakeRegions.py --lep el  --WP tight --region measurement1 --highPtBin --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement1 --highPtBin --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement1 --highPtBin --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement1 --highPtBin --doControlPlots --varBins --logy 0 
