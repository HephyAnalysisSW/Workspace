python ../plotFakeRegions.py --lep el  --WP tight --region $1 --doControlPlots --doYields
python ../plotFakeRegions.py --lep el  --WP loose --region $1 --doControlPlots --doYields
python ../plotFakeRegions.py --lep mu  --WP tight --region $1 --doControlPlots --doYields
python ../plotFakeRegions.py --lep mu  --WP loose --region $1 --doControlPlots --doYields

python ../plotFakeRegions.py --lep el  --WP tight --region $1 --doControlPlots             --logy 0
python ../plotFakeRegions.py --lep el  --WP loose --region $1 --doControlPlots             --logy 0
python ../plotFakeRegions.py --lep mu  --WP tight --region $1 --doControlPlots             --logy 0
python ../plotFakeRegions.py --lep mu  --WP loose --region $1 --doControlPlots             --logy 0

python ../plotFakeRegions.py --lep mu  --WP tight --region $1 --doControlPlots --varBins 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region $1 --doControlPlots --varBins 0
python ../plotFakeRegions.py --lep el  --WP tight --region $1 --doControlPlots --varBins 0
python ../plotFakeRegions.py --lep el  --WP loose --region $1 --doControlPlots --varBins 0

python ../plotFakeRegions.py --lep mu  --WP tight --region $1 --doControlPlots --varBins 0 --logy 0
python ../plotFakeRegions.py --lep mu  --WP loose --region $1 --doControlPlots --varBins 0 --logy 0
python ../plotFakeRegions.py --lep el  --WP tight --region $1 --doControlPlots --varBins 0 --logy 0
python ../plotFakeRegions.py --lep el  --WP loose --region $1 --doControlPlots --varBins 0 --logy 0
