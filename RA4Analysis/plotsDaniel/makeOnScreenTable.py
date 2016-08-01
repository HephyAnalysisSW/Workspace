import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from rCShelpers import *
import math
from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--mn", dest="neutralinoMass", default=100, action="store", help="Set neutralino mass")
parser.add_option("--mgl", dest="gluinoMass", default=1200, action="store", help="Set gluino mass")

(options, args) = parser.parse_args()



fmt = '{0:20}{1:<16}{2:<16}{3:<16}{4:<16}'

def getValErrString(val,err, precision=3):
  return str(round(val,precision))+' +/- '+str(round(err,precision))



pickleDir = '/afs/hephy.at/data/easilar01/Ra40b/pickleDir/T5qqqqWW_mass_nEvents_xsec_pkl'
mass_dict = pickle.load(file(pickleDir))

mGl = int(options.gluinoMass)
mN = int(options.neutralinoMass)



resPickle = '/afs/hephy.at/data/dspitzbart01/Results2016/signal_uncertainties/'
resISR = pickle.load(file(resPickle+'gen_met_study_ISR_mgl'+str(mGl)+'_pkl'))
res    = pickle.load(file(resPickle+'gen_met_study_mgl'+str(mGl)+'_pkl'))

print
print 'Change with using ISR reweighting for masspoint (mGl,mN) ('+str(mGl)+','+str(mN)+')'
print
print fmt.format('Signal Region','with ISR','without ISR', 'ratio', 'unmodified')
line = ''
for x in range(81): line+='-'
print line

signalRegions = signalRegions2016

valKeyToPrint = 'mod_yield_MB_SR'
errKeyToPrint = 'mod_err_MB_SR'
valUnmodKeyToPrint = 'yield_MB_SR'
errUnmodKeyToPrint = 'err_MB_SR'

for srNJet in sorted(signalRegions):
  for stb in sorted(signalRegions[srNJet]):
    for htb in sorted(signalRegions[srNJet][stb]):
      valISR = resISR[srNJet][stb][htb]['signals'][mGl][mN][valKeyToPrint]
      valISRerr = resISR[srNJet][stb][htb]['signals'][mGl][mN][errKeyToPrint]

      val = res[srNJet][stb][htb]['signals'][mGl][mN][valKeyToPrint]
      valerr = res[srNJet][stb][htb]['signals'][mGl][mN][errKeyToPrint]
      
      valUnmod = res[srNJet][stb][htb]['signals'][mGl][mN][valUnmodKeyToPrint]
      valerrUnmod = res[srNJet][stb][htb]['signals'][mGl][mN][errUnmodKeyToPrint]
      
      ratio, ratio_err = getPropagatedError(valISR, valISRerr, val, valerr, returnCalcResult=True)
      
      srString = str(srNJet)+' '+signalRegions[srNJet][stb][htb]['LT']+' '+signalRegions[srNJet][stb][htb]['HT']
      print fmt.format(srString, getValErrString(valISR,valISRerr,2), getValErrString(val,valerr,2), getValErrString(ratio,ratio_err,2), getValErrString(valUnmod,valerrUnmod,2))

print
