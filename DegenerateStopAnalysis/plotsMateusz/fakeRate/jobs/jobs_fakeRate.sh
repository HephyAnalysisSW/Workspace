python ../fakeRate.py --region $1 --lep el --sample st
python ../fakeRate.py --region $1 --lep el --sample vv
python ../fakeRate.py --region $1 --lep el --sample dy
python ../fakeRate.py --region $1 --lep el --sample z
python ../fakeRate.py --region $1 --lep el --sample qcd
python ../fakeRate.py --region $1 --lep el --sample tt
python ../fakeRate.py --region $1 --lep el --sample w

python ../fakeRate.py --region $1 --lep mu --sample st
python ../fakeRate.py --region $1 --lep mu --sample vv
python ../fakeRate.py --region $1 --lep mu --sample dy
python ../fakeRate.py --region $1 --lep mu --sample z
python ../fakeRate.py --region $1 --lep mu --sample qcd
python ../fakeRate.py --region $1 --lep mu --sample tt
python ../fakeRate.py --region $1 --lep mu --sample w

python ../fakeRate.py --region $1 --lep el --sample st                   --varBins 0 --do2D 
python ../fakeRate.py --region $1 --lep el --sample vv                   --varBins 0 --do2D
python ../fakeRate.py --region $1 --lep el --sample dy                   --varBins 0 --do2D
python ../fakeRate.py --region $1 --lep el --sample z                    --varBins 0 --do2D
python ../fakeRate.py --region $1 --lep el --sample qcd                  --varBins 0 --do2D
python ../fakeRate.py --region $1 --lep el --sample tt                   --varBins 0 --do2D
python ../fakeRate.py --region $1 --lep el --sample w                    --varBins 0 --do2D

python ../fakeRate.py --region $1 --lep mu --sample st                   --varBins 0 --do2D
python ../fakeRate.py --region $1 --lep mu --sample vv                   --varBins 0 --do2D
python ../fakeRate.py --region $1 --lep mu --sample dy                   --varBins 0 --do2D
python ../fakeRate.py --region $1 --lep mu --sample z                    --varBins 0 --do2D
python ../fakeRate.py --region $1 --lep mu --sample qcd                  --varBins 0 --do2D
python ../fakeRate.py --region $1 --lep mu --sample tt                   --varBins 0 --do2D
python ../fakeRate.py --region $1 --lep mu --sample w                    --varBins 0 --do2D
