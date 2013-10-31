from cardFileWriter import cardFileWriter
from math import exp

c = cardFileWriter()
c.defWidth=12
c.precision=6

for i in range(5):
  c.addBin('Bin'+str(i), ['bkg'], 'Bin'+str(i))
  y = 1000*exp(-i/2.)*0.01**(i/4.)
  print "Bin"+str(i), y
  c.specifyObservation('Bin'+str(i), int(y))
  c.specifyExpectation('Bin'+str(i), 'bkg', y)
  c.specifyExpectation('Bin'+str(i), 'signal', 0.00000001)

c.addUncertainty('Lumi', 'lnN')
c.specifyFlatUncertainty('Lumi', 1.044)

#pf=""

##correlated large uncertainty
#pf+="_corr100"
#c.addUncertainty('ratio', 'lnN')
#for i in range(5):
#  c.specifyUncertainty('ratio', 'Bin'+str(i), 'bkg', 2)
#
##uncorrelated large uncertainty
#pf+="_uncorr100"
#for i in range(5):
#  c.addUncertainty('ratio'+str(i), 'lnN')
#  c.specifyUncertainty('ratio'+str(i), 'Bin'+str(i), 'bkg', 2)

c.writeToFile('test.txt')

print c.calcLimit()
