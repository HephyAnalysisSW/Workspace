Sequence to produce smoothed limits:

cd MonoJetAnalysis/limits/
python pklToHistos.py
python smoothLimits-v5.py
pushd ../../PlotsSMS-master/
python python/makeSMSplots.py ../MonoJetAnalysis/limits/DegStop2016_singleLepton.cfg XYZ # last parameter is prefix for the output files
