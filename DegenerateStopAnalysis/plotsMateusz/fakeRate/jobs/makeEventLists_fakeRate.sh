python -b ../plotFakeRegions.py --save 0 --doPlots 0 --region measurement1 
python -b ../plotFakeRegions.py --save 0 --doPlots 0 --region measurement2 --lep el
python -b ../plotFakeRegions.py --save 0 --doPlots 0 --region measurement2 --lep mu
python -b ../plotFakeRegions.py --save 0 --doPlots 0 --region application_sr1
python -b ../plotFakeRegions.py --save 0 --doPlots 0 --region application_sr2
python -b ../plotFakeRegions.py --save 0 --doPlots 0 --region application_srBDT --mva
python -b ../plotFakeRegions.py --save 0 --doPlots 0 --region application_crBDT --mva

python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr1         --invAntiQCD
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr2         --invAntiQCD
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_srBDT --mva --invAntiQCD
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_crBDT --mva --invAntiQCD

python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr1         --CT200
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr2         --CT200
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_srBDT --mva --CT200
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_crBDT --mva --CT200

python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr1         --invAntiQCD --CT200
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr2         --invAntiQCD --CT200
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_srBDT --mva --invAntiQCD --CT200
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_crBDT --mva --invAntiQCD --CT200
