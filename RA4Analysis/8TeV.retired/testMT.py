import ROOT
from analysisHelpers import getCutSignalYield, getSignalChain

sms="T1tttt-madgraph"
cut = "njets>=4&&nbtags>=2&&type1phiMet>200"
mtc = [300,500]
c = getSignalChain(1150, 0, sms,  dir = '/data/schoef/convertedTuples_v19/copyMET/')

res = getCutSignalYield(c, cut, mtc, "weight", correctForFastSim = True)

print res

c.IsA().Destructor(c)
del c
