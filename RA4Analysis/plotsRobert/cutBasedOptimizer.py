import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.cmgTuplesPostProcessed import *
cBkg  = getChain([st250Skim_WJetsHTToLNu, st250Skim_ttJetsCSA1450ns])
cSignal1200 = getChain(st250Skim_T5Full_1200_1000_800)
cSignal1500 = getChain(st250Skim_T5Full_1500_800_100)
from Workspace.RA4Analysis.helpers import nameAndCut
from math import pi, sqrt

import numpy as np
from scipy import optimize

cuts = [
  {'var':'st',        'type':'lower', 'startVal': 250, 'minVal':250},\
  {'var':'htJet40ja',        'type':'lower', 'startVal': 500, 'minVal':500},\
  {'var':'acos((leptonPt+met*cos(leptonPhi-metPhi))/sqrt(leptonPt**2+met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))',      'type':'lower', 'startVal': 0.5,   'minVal':0.5,  'maxVal':3.  },\
#  {'var':'njet',      'type':'lower', 'startVal': 4., 'minVal':5., 'maxVal':1500}
  ]
#cuts = [
#  {'var':'met',        'type':'lower', 'startVal': 250, 'minVal':250},\
#  {'var':'htJet40ja',        'type':'lower', 'startVal': 500, 'minVal':500},\
#  {'var':'sqrt(2.0*leptonPt*met*(1.-cos(leptonPhi-metPhi)))',      'type':'lower', 'startVal': 150,   'minVal':150,  'maxVal':450.  },\
##  {'var':'njet',      'type':'lower', 'startVal': 4., 'minVal':5., 'maxVal':1500}
#  ]

prepreprefix = 'cutBasedOptimizer_'
presel = "singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&nBJetMedium25==0&&nJet40a>=6"
prefix = 'met_ht_mT_6j'
prefix = 'st_ht_dphi_6j'
#presel = "isrJetPt>110&&isrJetBTBVetoPassed&&softIsolatedMuPt>5&&nHardElectrons+nHardMuons==0&&njet60<=2&&type1phiMet>150"

#  print "S:",yieldS, "B:",yieldB

def getFom(cutVals, relSysErr=0.20, verbose=False):
  cut = presel
  cutFuncs = [] 
  for i, c in enumerate(cuts):
    if (  c.has_key('minVal') and cutVals[i]<c['minVal']) or (c.has_key('maxVal') and cutVals[i]>c['maxVal']):
      return -999
    if type(c['var'])==type(''):
      if c['type']=='lower':op='>='
      elif c['type']=='upper':op='<'
      else: 
        print "Problem in cut",c,"type not known:",c['type']
        return -999.

      cut+="&&"+c['var']+op+str(cutVals[i])

  cutFunc = None
      
  if verbose: print "Now at cut:",cut
  yieldS = getYieldFromChain(cSignal1200, cut, weight = "weight") 
  yieldB = getYieldFromChain(cBkg,    cut, weight = "weight")
  if yieldB<=0 or yieldS<=0:
    return -999.
  fom = yieldS/sqrt(yieldB + (relSysErr*yieldB)**2)       
  if verbose: 
    sigeff = getYieldFromChain(cSignal1200, cut, weight = "weight")/getYieldFromChain(cSignal1200, presel, weight = "weight")
    bkgeff = getYieldFromChain(cBkg, cut, weight = "weight")/getYieldFromChain(cBkg, presel, weight = "weight")
    print "Values", cutVals,"fom:",fom,'bkgeff',bkgeff,'sigeff',sigeff, 'yieldB',yieldB,'yieldS',yieldS
  return fom


#  {'var':'met',        'type':'lower', 'startVal': 250, 'minVal':250},\
#  {'var':'htJet40ja',        'type':'lower', 'startVal': 500, 'minVal':500},\
#  {'var':'sqrt(2.0*leptonPt*met*(1.-cos(leptonPhi-metPhi))',      'type':'lower', 'startVal': 150,   'minVal':150,  'maxVal':450.  },\

goodRes = []
c=0
#for met in range(250, 500, 50):
for st in range(250, 500, 50):
  for ht in range(500, 1100, 100):
#    for mT in np.linspace(150,350,5):
    for dPhi in np.linspace(0.5,2.5,6):
#      vals = [met, ht, mT]
      vals = [st, ht, dPhi]
      fom = getFom(vals,relSysErr=0.20, verbose=True)
      c+=1
#      if fom>1.5: 
      goodRes.append([fom, vals])
      print c, fom,  vals

goodRes.sort()
goodRes.reverse()
print goodRes
import pickle
pickle.dump(goodRes, file('/data/schoef/T5FullStuff/cutBased/'+prefix+'_results.pkl','w'))
#pickle.dump(goodRes, file('/data/schoef/T5FullStuff/cutBased/st_ht_dPhi_6j_results.pkl','w'))

#
#Optimizing
#x0 = np.array([v['startVal'] for v in cuts])
# Using dMT
#  optThresh = optimize.anneal(lambda x:-getFom(x,relSysErr=0.05, lepCharge=-1,verbose=True), x0, T0=.001, learn_rate=0.7)
## anneal: Values [ 261.06062214   11.94453719  437.81238786] fom: 2.2452353601
#  optThresh = list(optThresh[0])
#  for relSysErr in [0., 0.05, 0.08, 0.15]:
#    print 'relSysErr',relSysErr,"charge:-",getFom(optThresh,relSysErr=relSysErr,lepCharge=-1),"charge:+",getFom(optThresh,relSysErr=relSysErr,lepCharge=+1),'comb',getFom(optThresh,relSysErr=relSysErr)

#  optThresh = optimize.fmin(lambda x:-getFom(x,relSysErr=0.05, lepCharge=-1,verbose=True), x0)
#  print "Found maximum",optThresh
#  for relSysErr in [0., 0.05, 0.08, 0.15]:
#    print 'relSysErr',relSysErr,"charge:-",getFom(optThresh,relSysErr=relSysErr,lepCharge=-1),"charge:+",getFom(optThresh,relSysErr=relSysErr,lepCharge=+1),'comb',getFom(optThresh,relSysErr=relSysErr)
##Optimization terminated successfully.
##         Current function value: -2.715423
##         Iterations: 32
##         Function evaluations: 108
##relSysErr 0.0 charge:- 2.73896828448 charge:+ 0.901746679739 comb 1.82387059297
##relSysErr 0.05 charge:- 2.71542309916 charge:+ 0.852811294992 comb 1.71161387649
##relSysErr 0.08 charge:- 2.67987530103 charge:+ 0.790209387858 comb 1.57159670352
##relSysErr 0.15 charge:- 2.54663488097 charge:+ 0.627896383924 comb 1.22430907069
