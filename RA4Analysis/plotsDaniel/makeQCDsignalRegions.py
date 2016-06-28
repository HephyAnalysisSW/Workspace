import ROOT

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.HEPHYPythonTools.xsec import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *
from helpers import addKey
from copy import deepcopy

signalRegions2016_QCD = signalRegions2016

signalRegions2016_QCD = addKey(signalRegions2016_QCD, newDict='deltaPhi')

def makeQCDsignalRegions(d2, QCDSB = (3,4), ttSB = (4,5)):
  d = deepcopy(d2)
  #del d2
  dQCD = addKey(d, newDict='deltaPhi')
  
  for njet in sorted(d):
    for lt in sorted(d[njet]):
      for ht in sorted(d[njet][lt]):
        dPhi = d2[njet][lt][ht]['deltaPhi']
        try: dQCD[njet][lt][ht][dPhi]['sys']
        except KeyError:
          sys = 0.025
          if ht[1]<0 and ht[0]>700: sys = 0.05
          if njet[0]>5: sys = 0.05
          if njet[0]>7: sys = 0.1
          dQCD[njet][lt][ht][dPhi] = {'deltaPhi':dPhi,'sys': sys}
        try: dQCD[QCDSB][lt][ht][dPhi]
        #  print 'QCD SB with LT',lt,', HT',ht, ' and dPhi', dPhi, ' already exists'
        except KeyError:
          sys = 0.025
          if ht[1]<0 and ht[0]>700: sys = 0.05
          #if njet[0]>7: sys = 0.1
          try: dQCD[QCDSB]
          except KeyError: dQCD[QCDSB] = {}
          try: dQCD[QCDSB][lt]
          except KeyError: dQCD[QCDSB][lt] = {}
          try: dQCD[QCDSB][lt][ht]
          except KeyError: dQCD[QCDSB][lt][ht] = {}
          try: dQCD[QCDSB][lt][ht][dPhi]
          except KeyError: dQCD[QCDSB][lt][ht][dPhi] = {'deltaPhi':dPhi, 'sys':sys}
          #dQCD[(3,4)][lt][ht][dPhi] = {'deltaPhi':dPhi, 'sys':sys}}}}
        try: dQCD[ttSB][lt][ht][dPhi]
        except KeyError:
          sys = 0.025
          if ht[1]<0 and ht[0]>700: sys = 0.05
          #if njet[0]>7: sys = 0.1
          try: dQCD[ttSB]
          except KeyError: dQCD[ttSB] = {}
          try: dQCD[ttSB][lt]
          except KeyError: dQCD[ttSB][lt] = {}
          try: dQCD[ttSB][lt][ht]
          except KeyError: dQCD[ttSB][lt][ht] = {}
          try: dQCD[ttSB][lt][ht][dPhi]
          except KeyError: dQCD[ttSB][lt][ht][dPhi] = {'deltaPhi':dPhi, 'sys':sys}
          #dQCD[(4,5)] = {lt:{ht:{dPhi:{'deltaPhi':dPhi, 'sys':sys}}}}
  return dQCD


