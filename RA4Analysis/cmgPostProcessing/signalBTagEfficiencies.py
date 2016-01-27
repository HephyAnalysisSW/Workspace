import ROOT
import pickle

from btagEfficiency import *
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *

effs = {}

for signal in allSignalStrings:
  print
  print 'processing',signal
  s = getSignalSample(signal)
  c = getSignalChain(s)
  effs[signal] = getBTagMCTruthEfficiencies(c, cut="(1)", overwrite=False)

effs['none'] = getDummyEfficiencies()

