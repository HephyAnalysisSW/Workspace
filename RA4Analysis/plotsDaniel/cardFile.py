from cardFileWriter import cardFileWriter
from math import exp
#import pickle

c = cardFileWriter()
c.defWidth=12
c.precision=6

#yields=pickle.load(file('yields_saved.pkl')



BgYield = 0.165+0.734
SigYield = 1.207+1.781
TotalYield = int(BgYield+SigYield)

c.addBin('Bin0', ['bkg'], 'Bin0')
c.specifyObservation('Bin0', TotalYield)
c.specifyExpectation('Bin0', 'bkg', BgYield)
c.specifyExpectation('Bin0', 'signal', SigYield)

c.addUncertainty('Lumi', 'lnN')
c.specifyFlatUncertainty('Lumi', 1.20)
c.addUncertainty('JES', 'lnN')
c.specifyUncertainty('JES', '1', 'bkg', 1.3)

#c.addUncertainty('signalUn', 'lnN')
#c.specifyUncertainty('signalUn', 'Bin0', 'signal', 0.5)#hoehere uncertainty drueckt limit?!

#c.addUncertainty('bkgUn', 'lnN')
#c.specifyUncertainty('bkgUn', 'Bin0', 'bkg', 0.2)

c.writeToFile('BDTcard.txt')
      
limit = c.calcSignif()
