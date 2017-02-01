python ../plotFakeRegions.py --lep el  --WP tight --region measurement --doControlPlots --doYields 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement --doControlPlots --doYields 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement --doControlPlots --doYields 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement --doControlPlots --doYields 

python ../plotFakeRegions.py --lep el  --WP tight --region measurement --doControlPlots --varBins 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement --doControlPlots --varBins 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement --doControlPlots --varBins 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement --doControlPlots --varBins

python ../plotFakeRegions.py --lep el  --WP tight --region measurement --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement --doControlPlots --varBins --logy 0 

python ../plotFakeRegions.py --lep el  --WP tight --region measurement --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement --doControlPlots           --logy 0 
