#needs to run in a supported CMSSW release

import ROOT
import pickle
from cardFileWriter import cardFileWriter

yieldTable = pickle.load(file('/afs/hephy.at/user/d/dspitzbart/www/softLepYields/yieldsmymt2w_mymt2w200.pkl'))

plotDir='/afs/hephy.at/user/d/dspitzbart/www/softLepYields/'


c = cardFileWriter()
c.defWidth=12
c.precision=6
c.addUncertainty('Lumi', 'lnN')
c.specifyFlatUncertainty('Lumi', 1.20)
c.addUncertainty('JES', 'lnN')

median = '0.500'
signif = '-1.000'

for yields in yieldTable:
  c = cardFileWriter()
  c.defWidth=12
  c.precision=6
  c.addUncertainty('Lumi', 'lnN')
  c.specifyFlatUncertainty('Lumi', 1.20)
  c.addUncertainty('JES', 'lnN')
  
  bY = yields['bkgYield']
  sig = []
  limit = []
  # for significance calculations
  for sY in yields['signalYields']:
      
    c.addBin('1', ['bkg'], '1')
    c.specifyObservation('1', int(bY+sY))
    if bY > 0.:
      c.specifyExpectation('1', 'bkg', bY)
    else:
      c.specifyExpectation('1', 'bkg', 0.001)
    if sY > 0.:
      c.specifyExpectation('1', 'signal', sY)
    else:
      c.specifyExpectation('1', 'signal', 0.001)
    c.specifyUncertainty('JES', '1', 'bkg', 1.3)
    c.writeToFile('significance.txt')
    
    sigAll = c.calcSignif()
    if signif in sigAll:
      sigMed = sigAll[signif]
      sig.append(sigMed)
      print 'Significance:',sigMed
    else:
      sig.append(-1.)
  # for limit calculations
  for sY in yields['signalYields']:

    c.addBin('1', ['bkg'], '1')
    c.specifyObservation('1', int(bY))
    if bY > 0.:
      c.specifyExpectation('1', 'bkg', bY)
    else:
      c.specifyExpectation('1', 'bkg', 0.001)
    if sY > 0.:
      c.specifyExpectation('1', 'signal', sY)
    else:
      c.specifyExpectation('1', 'signal', 0.001)
    c.specifyUncertainty('JES', '1', 'bkg', 1.3)
    c.writeToFile('limit.txt')
    
    limitAll = c.calcLimit()
    if median in limitAll:
      limitMed = limitAll[median]
      limit.append(limitMed)
      print 'Limit:', limitMed
    else:
      limit.append(-1.)
  
  yields.update({'Significances': sig, 'Limits': limit})


yieldFile = open(plotDir+"yields_withLimitAndSig.pkl","w")
pickle.dump(yieldTable,yieldFile)
yieldFile.close()



