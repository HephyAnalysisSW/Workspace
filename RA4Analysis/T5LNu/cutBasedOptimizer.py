import os,sys,ROOT,pickle
from math import sqrt, pi
from localConfig import afsUser, nfsUser, localPlotDir
import operator

from Workspace.HEPHYPythonTools.nnAnalysisHelpers import getEList, getYieldFromChain
from Workspace.HEPHYPythonTools.xsec import xsec
import copy, sys
from defaultConvertedTuples import * 

colors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kOrange, ROOT.kMagenta]

cSignal = ROOT.TChain("Events")
cSignal.Add("/data/schoef/convertedTuples_v22/copy/T5LNu_1000_100/histo_T5LNu_1000_100.root")

cBkg    = ROOT.TChain("Events")
cBkg.Add("/data/schoef/convertedTuples_v22/copy/WJetsHT150v2/histo_WJetsHT150v2_from*.root")

import numpy as np
from scipy import optimize

cuts = [
  {'var':'type1phiMet',   'type':'lower', 'startVal': 200, 'minVal':200},\
  {'var': 'mT',      'type':'lower', 'startVal': 70,   'minVal':70.,  'maxVal':200.  },\
  {'var':'ht',      'type':'lower', 'startVal': 400., 'minVal':400., 'maxVal':1000}
  ]

prepreprefix = 'cutBasedOptimizer_'
presel = "njets>=4&&ht>400&&nTightMuons+nTightElectrons==1&&nbtags==0&&type1phiMet>150."
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
  yieldS = getYieldFromChain(cSignal, cut, weight = "weight") 
  yieldB = getYieldFromChain(cBkg,    cut, weight = "weight")
  if yieldB<=0 or yieldS<=0:
    return -999.
  fom = yieldS/sqrt(yieldB + (relSysErr*yieldB)**2)       
  if verbose: 
    sigeff = getYieldFromChain(cSignal, cut, weight = "weight")/getYieldFromChain(cSignal, presel, weight = "weight")
    bkgeff = getYieldFromChain(cBkg, cut, weight = "weight")/getYieldFromChain(cBkg, presel, weight = "weight")
    print "Values", cutVals,"fom:",fom,'bkgeff',bkgeff,'sigeff',sigeff, 'yieldB',yieldB,'yieldS',yieldS
  return fom

goodRes = []
c=0
for met in range(250, 450, 25):
  for mT in range(70, 200, 10):
    for ht in range(500,900,100):
      vals = [met, mT, ht]
      fom = getFom(vals,relSysErr=0.20, verbose=True)
      c+=1
#      if fom>1.5: 
      goodRes.append([fom, vals])
      print c, fom,  vals

goodRes.sort()
goodRes.reverse()
print goodRes
pickle.dump(goodRes, file('/data/schoef/T5LNuStuff/cutBased/met_mT_ht_results.pkl','w'))

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
