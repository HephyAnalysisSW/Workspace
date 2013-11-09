from analysisHelpers import *
for path in [os.path.abspath(p) for p in ['../../HEPHYCommonTools/python/']]:
  if not path in sys.path:
      sys.path.insert(1, path)

from xsecSMS import gluino8TeV_NLONLL

htb = (500, 2500)
metvar = "type1phiMet"
minNJet = 6
weight="weight"
indir = '/data/schoef/convertedTuples_v19/copyMET/'
sms="T1tttt-madgraph"
varX=1250
#varY=200
varY=225

#for btb in ['2', '3']:
#  for metb in [(250, 350), (350, 450), (450, 2500)]:
#    print btb, htb, metb, 0.01/gluino8TeV_NLONLL[1200]*getSignalYield(btb, htb, metb, metvar, minNJet, varX, varY, sms,  dir = indir, weight=weight, correctForFastSim = True)
#for weight in ['weightBTag2_SF', 'weightBTag3p_SF']:
#  for metb in [(250, 350), (350, 450), (450, 2500)]:
#    print btb, htb, metb, 0.01/gluino8TeV_NLONLL[1200]*getSignalYield('none', htb, metb, metvar, minNJet, varX, varY, sms,  dir = indir, weight=weight, correctForFastSim = True)
for metb in [(250, 350), (350, 450), (450, 2500)]:
    
    resBT3 =   0.01/gluino8TeV_NLONLL[1200]*getSignalYield('3', htb, metb, metvar, minNJet, varX, varY, sms,  dir = indir, weight='weight', correctForFastSim = True)
    resBT2 =   0.01/gluino8TeV_NLONLL[1200]*getSignalYield('2', htb, metb, metvar, minNJet, varX, varY, sms,  dir = indir, weight='weight', correctForFastSim = True)
#    resComb =   0.01/gluino8TeV_NLONLL[1200]*getSignalYield('none', htb, metb, metvar, minNJet, varX, varY, sms,  dir = indir, weight='weightBTag3p_SF', correctForFastSim = True)
    print metb, "2b", resBT2,"3+",resBT3 #,resComb

#HT>500, Njet>=6
#Nb=2, 250<MET<350: 2.77
#Nb=2, 350<MET<450: 2.69
#Nb=2, MET>450: 4.51
#Nb>=3, 250<MET<350: 3.33
#Nb>=3, 350<MET<450: 3.11
#Nb>=3, MET>450: 5.20

