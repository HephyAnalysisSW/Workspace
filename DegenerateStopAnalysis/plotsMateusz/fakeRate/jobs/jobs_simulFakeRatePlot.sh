python ../simulFakeRatePlot.py --variable pt --lep el  --region $1
python ../simulFakeRatePlot.py --variable pt --lep mu  --region $1
python ../simulFakeRatePlot.py --variable pt --lep el  --region $1 --varBins 0
python ../simulFakeRatePlot.py --variable pt --lep mu  --region $1 --varBins 0

python ../simulFakeRatePlot.py --variable eta --lep el --region $1
python ../simulFakeRatePlot.py --variable eta --lep mu --region $1
python ../simulFakeRatePlot.py --variable eta --lep el --region $1 --varBins 0
python ../simulFakeRatePlot.py --variable eta --lep mu --region $1 --varBins 0
