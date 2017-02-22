python ../plotFakeRegions.py --lep el  --WP tight --region measurement --highPtBin --doControlPlots --doYields 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement --highPtBin --doControlPlots --doYields 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement --highPtBin --doControlPlots --doYields 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement --highPtBin --doControlPlots --doYields 

python ../plotFakeRegions.py --lep el  --WP tight --region measurement --highPtBin --doControlPlots --varBins 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement --highPtBin --doControlPlots --varBins 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement --highPtBin --doControlPlots --varBins 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement --highPtBin --doControlPlots --varBins

python ../plotFakeRegions.py --lep el  --WP tight --region measurement --highPtBin --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement --highPtBin --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement --highPtBin --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement --highPtBin --doControlPlots           --logy 0 

python ../plotFakeRegions.py --lep el  --WP tight --region measurement --highPtBin --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement --highPtBin --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement --highPtBin --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement --highPtBin --doControlPlots --varBins --logy 0 
