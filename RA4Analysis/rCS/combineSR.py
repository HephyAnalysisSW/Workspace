import ROOT
import pickle

from Workspace.RA4Analysis.signalRegions import *

signalRegions = signalRegions_Moriond2017

input_files = '/afs/hephy.at/data/dspitzbart01/RA4/Moriond2017/bootstrap/bootstrap_unc_'
output_file = '/afs/hephy.at/data/dspitzbart01/RA4/Moriond2017/bootstrap/bootstrap_unc.pkl'

bins = {}
i = 0

for srNJet in sorted(signalRegions):
  bins[srNJet] = {}
  for stb in sorted(signalRegions[srNJet]):
    bins[srNJet][stb] ={}
    for htb in sorted(signalRegions[srNJet][stb]):
      print i
      r = pickle.load(file(input_files+'SR'+str(i)+'.pkl'))
      try:
        print r[srNJet]
      except 'KeyError':
        print 'Loaded wrong file'
      
      bins[srNJet][stb][htb] = r
      i += 1

pickle.dump(bins, file(output_file,'w'))
