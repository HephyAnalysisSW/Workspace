python ../plotFakeRegions.py --lep el  --WP tight --region measurement1 --doControlPlots --doYields 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement1 --doControlPlots --doYields 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement1 --doControlPlots --doYields 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement1 --doControlPlots --doYields 

python ../plotFakeRegions.py --lep el  --WP tight --region measurement1 --doControlPlots --varBins 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement1 --doControlPlots --varBins 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement1 --doControlPlots --varBins 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement1 --doControlPlots --varBins

python ../plotFakeRegions.py --lep el  --WP tight --region measurement1 --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement1 --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement1 --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement1 --doControlPlots --varBins --logy 0 

python ../plotFakeRegions.py --lep el  --WP tight --region measurement1 --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep el  --WP loose --region measurement1 --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep mu  --WP tight --region measurement1 --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region measurement1 --doControlPlots           --logy 0 
