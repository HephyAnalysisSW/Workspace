import ROOT
import pickle
from math import sqrt
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getPropagatedError
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName

from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *

signalRegions = signalRegions2016



uncD = {}
uncDtt = {}
uncDW = {}

for i_njb, njb in enumerate(sorted(signalRegions)):
  uncD[njb] = {}
  uncDtt[njb] = {}
  uncDW[njb] = {}
  for stb in sorted(signalRegions[njb]):
    uncD[njb][stb] ={}
    uncDtt[njb][stb] = {}
    uncDW[njb][stb] = {}
    for htb in sorted(signalRegions[njb][stb]):
      if njb == (5,5): dilepErr = 0.075
      if njb == (6,7): dilepErr = 0.15
      if njb == (8,-1): dilepErr = 0.30
      uncD[njb][stb][htb] = {}
      uncD[njb][stb][htb] = dilepErr
      #uncDtt[njb][stb][htb] = 0.03
      #uncDW[njb][stb][htb] = 0.12

#uncD = {'tot_pred':uncD, 'TT_kappa':uncDtt, 'W_kappa':uncDW}


pickle.dump(uncD, file('/data/dspitzbart/Results2016/systematics2016/dilep_envelope_approval_pkl','w'))

