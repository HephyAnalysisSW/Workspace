import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v3 import *

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--signals", dest="allSignals", default='', type="string", action="store", help="signals:Which signals.")
parser.add_option("--mode", dest="mode", default="", type="string", action="store", help="soft or hard?")
(options, args) = parser.parse_args()
exec('allSignals=['+options.allSignals+']')

def loop_rec(sel, remainingCuts, appliedCuts=[]):
  if len(remainingCuts)==0:
    fom = getFom(sel, relSysErr=0.50)
    print fom, sel
    results.append( [fom, appliedCuts])
  else:
    cut=remainingCuts[0]
    for c in range(cut['min'], cut['max']+cut['step'],cut['step']): 
      s=sel+"&&"+cut['var']+">="+str(c)
      loop_rec(s, remainingCuts[1:], appliedCuts+[[cut['var'], c]])

def getFom(cut, relSysErr=0.20, verbose=False):
  if verbose: print "Now at cut:",cut
  yieldS = getYieldFromChain(cSignal, cut, weight = "weight") 
  yieldB = getYieldFromChain(cBkg,    cut, weight = "weight")
  if yieldB<=0 or yieldS<=0:
    return -999.
  fom = yieldS/sqrt(yieldB + (relSysErr*yieldB)**2)       
  if verbose: 
    sigeff = getYieldFromChain(cSignal1200, cut, weight = "weight")/getYieldFromChain(cSignal1200, presel, weight = "weight")
    bkgeff = getYieldFromChain(cBkg, cut, weight = "weight")/getYieldFromChain(cBkg, presel, weight = "weight")
    print "Values", cutVals,"fom:",fom,'bkgeff',bkgeff,'sigeff',sigeff, 'yieldB',yieldB,'yieldS',yieldS
  return fom

if options.mode=="soft":
#    signals = [soft_T5qqqqWW_Gl_1400_LSP_100_Chi_325, soft_T6qqWW_Sq_950_LSP_300_Chi_350]
  cBkg  = getChain([soft_WJetsHTToLNu, soft_ttJetsCSA1450ns])
  presel = "singleMuonic&&nLooseSoftLeptons==1&&nTightSoftLeptons==1&&nTightHardLeptons==0&&nBJetMedium25==0"
if options.mode=="hard":
#    signals = [hard_T5WW_2J_mGo1200_mCh1000_mChi800, hard_T5WW_2J_mGo1500_mCh800_mChi100, hard_T6qqWW_Sq_950_LSP_300_Chi_350]
  cBkg  = getChain([hard_WJetsHTToLNu, hard_ttJetsCSA1450ns])
  presel= "singleMuonic&&nLooseSoftLeptons==0&&nTightHardLeptons==1&&nLooseHardLeptons==1&&nBJetMedium25==0"
for signal in allSignals:
  cSignal = getChain(signal)
  
  from math import pi, sqrt

  #import numpy as np
  #from scipy import optimize

  cuts = [
    {'name':'jet1pt',   'var':'Jet_pt[1]',  'min': 80, 'max':320, 'step':80},\
    {'name':'njet',     'var':'nJet40a',    'min': 3, 'max':6, 'step':1},\
    {'name':'ht',       'var':'htJet40ja',  'min': 500, 'max':1200, 'step':100},\
    {'name':'met',      'var':'met',        'min':200, 'max':700, 'step':100  },\
    ]

  dPhi = "acos((leptonPt+met_pt*cos(leptonPhi-met_phi))/sqrt(leptonPt**2+met**2+2*met*leptonPt*cos(leptonPhi-met_phi)))"
  presel+= "&&"+dPhi+">1"
  prefix = '_'.join(['cutBasedOptimizer', options.mode, signal['name']])

  results=[]

  loop_rec(presel, cuts) 

  results.sort()
  results.reverse()
  for r in results[:30]:
    print r

  pickle.dump(results, file("/data/schoef/results2014/cutBasedOptimizer/"+prefix+".pkl", "w"))

#goodRes = []
#c=0
##for met in range(250, 500, 50):
#for st in range(250, 500, 50):
#  for ht in range(500, 1100, 100):
##    for mT in np.linspace(150,350,5):
#    for dPhi in np.linspace(0.5,2.5,6):
##      vals = [met, ht, mT]
#      vals = [st, ht, dPhi]
#      fom = getFom(vals,relSysErr=0.20, verbose=True)
#      c+=1
##      if fom>1.5: 
#      goodRes.append([fom, vals])
#      print c, fom,  vals
#
#goodRes.sort()
#goodRes.reverse()
#print goodRes
#import pickle
#pickle.dump(goodRes, file('/data/schoef/T5FullStuff/cutBased/'+prefix+'_results.pkl','w'))
##pickle.dump(goodRes, file('/data/schoef/T5FullStuff/cutBased/st_ht_dPhi_6j_results.pkl','w'))
#
##
##Optimizing
##x0 = np.array([v['startVal'] for v in cuts])
## Using dMT
##  optThresh = optimize.anneal(lambda x:-getFom(x,relSysErr=0.05, lepCharge=-1,verbose=True), x0, T0=.001, learn_rate=0.7)
### anneal: Values [ 261.06062214   11.94453719  437.81238786] fom: 2.2452353601
##  optThresh = list(optThresh[0])
##  for relSysErr in [0., 0.05, 0.08, 0.15]:
##    print 'relSysErr',relSysErr,"charge:-",getFom(optThresh,relSysErr=relSysErr,lepCharge=-1),"charge:+",getFom(optThresh,relSysErr=relSysErr,lepCharge=+1),'comb',getFom(optThresh,relSysErr=relSysErr)
#
##  optThresh = optimize.fmin(lambda x:-getFom(x,relSysErr=0.05, lepCharge=-1,verbose=True), x0)
##  print "Found maximum",optThresh
##  for relSysErr in [0., 0.05, 0.08, 0.15]:
##    print 'relSysErr',relSysErr,"charge:-",getFom(optThresh,relSysErr=relSysErr,lepCharge=-1),"charge:+",getFom(optThresh,relSysErr=relSysErr,lepCharge=+1),'comb',getFom(optThresh,relSysErr=relSysErr)
###Optimization terminated successfully.
###         Current function value: -2.715423
###         Iterations: 32
###         Function evaluations: 108
###relSysErr 0.0 charge:- 2.73896828448 charge:+ 0.901746679739 comb 1.82387059297
###relSysErr 0.05 charge:- 2.71542309916 charge:+ 0.852811294992 comb 1.71161387649
###relSysErr 0.08 charge:- 2.67987530103 charge:+ 0.790209387858 comb 1.57159670352
###relSysErr 0.15 charge:- 2.54663488097 charge:+ 0.627896383924 comb 1.22430907069
