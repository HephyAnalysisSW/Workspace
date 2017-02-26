python ../plotFakeRegions.py --lep el  --WP tight --region measurement2 --doControlPlots --doYields 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement2 --doControlPlots --doYields 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement2 --doControlPlots --doYields 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement2 --doControlPlots --doYields 

python ../plotFakeRegions.py --lep el  --WP tight --region measurement2 --doControlPlots --varBins 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement2 --doControlPlots --varBins 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement2 --doControlPlots --varBins 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement2 --doControlPlots --varBins

python ../plotFakeRegions.py --lep el  --WP tight --region measurement2 --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement2 --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement2 --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement2 --doControlPlots --varBins --logy 0 

python ../plotFakeRegions.py --lep el  --WP tight --region measurement2 --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement2 --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement2 --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement2 --doControlPlots           --logy 0 
