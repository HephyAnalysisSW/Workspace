python ../plotFakeRegions.py --lep el  --WP tight --region application_srBDT --mva --doYields --doControlPlots 
python ../plotFakeRegions.py --lep el  --WP loose --region application_srBDT --mva --doYields --doControlPlots 
python ../plotFakeRegions.py --lep mu  --WP tight --region application_srBDT --mva --doYields --doControlPlots 
python ../plotFakeRegions.py --lep mu  --WP loose --region application_srBDT --mva --doYields --doControlPlots 

python ../plotFakeRegions.py --lep mu  --WP tight --region application_srBDT --mva --doControlPlots --varBins 
python ../plotFakeRegions.py --lep mu  --WP loose --region application_srBDT --mva --doControlPlots --varBins 
python ../plotFakeRegions.py --lep el  --WP tight --region application_srBDT --mva --doControlPlots --varBins 
python ../plotFakeRegions.py --lep el  --WP loose --region application_srBDT --mva --doControlPlots --varBins 

python ../plotFakeRegions.py --lep mu  --WP tight --region application_srBDT --mva --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region application_srBDT --mva --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep el  --WP tight --region application_srBDT --mva --doControlPlots --varBins --logy 0 
python ../plotFakeRegions.py --lep el  --WP loose --region application_srBDT --mva --doControlPlots --varBins --logy 0 

python ../plotFakeRegions.py --lep el  --WP tight --region application_srBDT --mva --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep el  --WP loose --region application_srBDT --mva --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep mu  --WP tight --region application_srBDT --mva --doControlPlots           --logy 0 
python ../plotFakeRegions.py --lep mu  --WP loose --region application_srBDT --mva --doControlPlots           --logy 0 
