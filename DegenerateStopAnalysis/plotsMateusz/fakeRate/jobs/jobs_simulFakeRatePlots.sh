python ../simulFakeRatePlots.py --variable pt --lep el  --region $1
python ../simulFakeRatePlots.py --variable pt --lep mu  --region $1
python ../simulFakeRatePlots.py --variable pt --lep el  --region $1 --varBins 0
python ../simulFakeRatePlots.py --variable pt --lep mu  --region $1 --varBins 0

python ../simulFakeRatePlots.py --variable eta --lep el --region $1
python ../simulFakeRatePlots.py --variable eta --lep mu --region $1
python ../simulFakeRatePlots.py --variable eta --lep el --region $1 --varBins 0
python ../simulFakeRatePlots.py --variable eta --lep mu --region $1 --varBins 0
