python ../plotFakeRegions.py --lep el  --WP tight --region application --mva --doYields --doControlPlots 
python ../plotFakeRegions.py --lep el  --WP loose --region application --mva --doYields --doControlPlots 
python ../plotFakeRegions.py --lep mu  --WP tight --region application --mva --doYields --doControlPlots 
python ../plotFakeRegions.py --lep mu  --WP loose --region application --mva --doYields --doControlPlots 

python ../plotFakeRegions.py --lep mu  --WP tight --region application --mva --doControlPlots --varBins 
python ../plotFakeRegions.py --lep mu  --WP loose --region application --mva --doControlPlots --varBins 
python ../plotFakeRegions.py --lep el  --WP tight --region application --mva --doControlPlots --varBins 
python ../plotFakeRegions.py --lep el  --WP loose --region application --mva --doControlPlots --varBins 

python ../plotFakeRegions.py --lep mu  --WP tight --region application --mva --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region application --mva --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep el  --WP tight --region application --mva --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep el  --WP loose --region application --mva --doControlPlots --varBins --logy 0 

python ../plotFakeRegions.py --lep el  --WP tight --region application --mva --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep el  --WP loose --region application --mva --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep mu  --WP tight --region application --mva --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region application --mva --doControlPlots           --logy 0 
