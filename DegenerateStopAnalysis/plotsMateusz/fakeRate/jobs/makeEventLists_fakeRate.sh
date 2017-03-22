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

python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr1         --VR CT200
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr2         --VR CT200
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_srBDT --mva --VR CT200
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_crBDT --mva --VR CT200

python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr1         --invAntiQCD --VR CT200
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr2         --invAntiQCD --VR CT200
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_srBDT --mva --invAntiQCD --VR CT200
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_crBDT --mva --invAntiQCD --VR CT200

python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr1         --VR EVR1
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr2         --VR EVR1
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_srBDT --mva --VR EVR1
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_crBDT --mva --VR EVR1

python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr1         --invAntiQCD --VR EVR1
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr2         --invAntiQCD --VR EVR1
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_srBDT --mva --invAntiQCD --VR EVR1
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_crBDT --mva --invAntiQCD --VR EVR1

python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr1         --VR EVR2
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr2         --VR EVR2
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_srBDT --mva --VR EVR2
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_crBDT --mva --VR EVR2

python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr1         --invAntiQCD --VR EVR2
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_sr2         --invAntiQCD --VR EVR2
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_srBDT --mva --invAntiQCD --VR EVR2
python -b ../fakesEstimation.py --save 0 --doPlots 0 --region application_crBDT --mva --invAntiQCD --VR EVR2
