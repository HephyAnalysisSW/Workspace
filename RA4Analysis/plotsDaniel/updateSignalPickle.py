import ROOT
import os, sys, copy
import pickle, operator

from math import *
from array import array
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *


sig = pickle.load(file('/afs/hephy.at/data/easilar01/Ra40b/pickleDir/allSignals_12p88_ultimate_2016Syst_pkl'))
pickleDir = '/afs/hephy.at/data/easilar01/Ra40b/pickleDir/T5qqqqWW_mass_nEvents_xsec_pkl'
mass_dict = pickle.load(file(pickleDir))

signalRegions = signalRegions2016

for srNJet in sorted(signalRegions):
  for stb in sorted(signalRegions[srNJet]):
    for htb in sorted(signalRegions[srNJet][stb]):
      for mgl in mass_dict:
        for mLSP in mass_dict[mgl]:
          y = sig[srNJet][stb][htb]['signals'][mgl][mLSP]['mod_yield_MB_SR']
          syst_rel = sig[srNJet][stb][htb]['signals'][mgl][mLSP]['tot_syst_err']
          stat_abs = sig[srNJet][stb][htb]['signals'][mgl][mLSP]['err_MB_SR']
          if y>0: stat_rel = stat_abs/y
          else: stat_rel = stat_abs
          sig[srNJet][stb][htb]['signals'][mgl][mLSP]['tot_err'] = sqrt(stat_rel**2 + syst_rel**2)*y

pickle.dump(sig, file('/afs/hephy.at/data/dspitzbart01/Results2016/signals_with_unc_pkl','w'))

