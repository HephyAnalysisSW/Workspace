python ../plotFakeRegions.py --lep el  --WP tight --region $1 --doControlPlots --getData --doYields
python ../plotFakeRegions.py --lep el  --WP loose --region $1 --doControlPlots --getData --doYields
python ../plotFakeRegions.py --lep mu  --WP tight --region $1 --doControlPlots --getData --doYields
python ../plotFakeRegions.py --lep mu  --WP loose --region $1 --doControlPlots --getData --doYields

python ../plotFakeRegions.py --lep el  --WP tight --region $1 --doControlPlots --getData             --logy
python ../plotFakeRegions.py --lep el  --WP loose --region $1 --doControlPlots --getData             --logy
python ../plotFakeRegions.py --lep mu  --WP tight --region $1 --doControlPlots --getData             --logy
python ../plotFakeRegions.py --lep mu  --WP loose --region $1 --doControlPlots --getData             --logy

python ../plotFakeRegions.py --lep mu  --WP tight --region $1 --doControlPlots --getData --varBins 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region $1 --doControlPlots --getData --varBins 0
python ../plotFakeRegions.py --lep el  --WP tight --region $1 --doControlPlots --getData --varBins 0
python ../plotFakeRegions.py --lep el  --WP loose --region $1 --doControlPlots --getData --varBins 0

python ../plotFakeRegions.py --lep mu  --WP tight --region $1 --doControlPlots --getData --varBins 0 --logy
python ../plotFakeRegions.py --lep mu  --WP loose --region $1 --doControlPlots --getData --varBins 0 --logy
python ../plotFakeRegions.py --lep el  --WP tight --region $1 --doControlPlots --getData --varBins 0 --logy
python ../plotFakeRegions.py --lep el  --WP loose --region $1 --doControlPlots --getData --varBins 0 --logy
