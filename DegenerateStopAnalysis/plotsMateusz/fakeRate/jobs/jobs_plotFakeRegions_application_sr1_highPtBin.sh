python ../plotFakeRegions.py --lep el  --WP tight --region application_sr1 --highPtBin --doYields --doControlPlots 
python ../plotFakeRegions.py --lep el  --WP loose --region application_sr1 --highPtBin --doYields --doControlPlots 
python ../plotFakeRegions.py --lep mu  --WP tight --region application_sr1 --highPtBin --doYields --doControlPlots 
python ../plotFakeRegions.py --lep mu  --WP loose --region application_sr1 --highPtBin --doYields --doControlPlots 

python ../plotFakeRegions.py --lep mu  --WP tight --region application_sr1 --highPtBin --doControlPlots --varBins 
python ../plotFakeRegions.py --lep mu  --WP loose --region application_sr1 --highPtBin --doControlPlots --varBins 
python ../plotFakeRegions.py --lep el  --WP tight --region application_sr1 --highPtBin --doControlPlots --varBins 
python ../plotFakeRegions.py --lep el  --WP loose --region application_sr1 --highPtBin --doControlPlots --varBins 

python ../plotFakeRegions.py --lep el  --WP tight --region application_sr1 --highPtBin --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep el  --WP loose --region application_sr1 --highPtBin --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep mu  --WP tight --region application_sr1 --highPtBin --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region application_sr1 --highPtBin --doControlPlots           --logy 0 

python ../plotFakeRegions.py --lep mu  --WP tight --region application_sr1 --highPtBin --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region application_sr1 --highPtBin --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep el  --WP tight --region application_sr1 --highPtBin --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep el  --WP loose --region application_sr1 --highPtBin --doControlPlots --varBins --logy 0 
