# finalTL.py
# Mateusz Zarucki 2017

import os, sys
import ROOT
import pickle
from Workspace.DegenerateStopAnalysis.tools.degTools import makeDir
#from Workspace.DegenerateStopAnalysis.tools.degVars import VarsCutsWeightsRegions
#from Workspace.HEPHYPythonTools import u_float
#from fakeInfo import binMaps, invBinMaps

#varsCuts = VarsCutsWeightsRegions()
#allRegions = varsCuts.regions['bins_sum'] #bins_cr, bins_mainsr
#print allRegions

save = True

if save:
   saveTag = "8025_mAODv2_v7/80X_postProcessing_v0"
   finalTag = "MR14"
   
   resultsDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate"
   finalResultsDir = "%s/final/%s/%s/systematics"%(resultsDir, saveTag, finalTag)

   savedir = finalResultsDir
   makeDir(savedir) 

systs = {}

systs['NonUniv'] = {'ptVL':20., 'ptL':20., 'ptM':30., 'ptH':30., 'ptCR':50.}
systs['NonClosure'] = {
   'sr1vla':20., 'sr1la':30., 'sr1ma':80., 'sr1ha':100., 'sr1vlb':20., 'sr1lb':30., 'sr1mb':80., 'sr1hb':100., 'sr1vlc':25., 'sr1lc':0.,  'sr1mc':0.,  'sr1hc':0., # SR1 
   'sr2vla':0.,  'sr2la':0., 'sr2ma':0.,   'sr2ha':30.,  'sr2vlb':0.,  'sr2lb':0., 'sr2mb':0.,   'sr2hb':30.,  'sr2vlc':30., 'sr2lc':30., 'sr2mc':30., 'sr2hc':30., # SR2 
   'cr1a':150., 'cr1b':150., 'cr1c':100., 'cr2a':200., 'cr2b':200., 'cr2c':30.} # CRs

SR1s = ['sr1vla', 'sr1la', 'sr1ma', 'sr1ha', 'sr1vlb', 'sr1lb', 'sr1mb', 'sr1hb', 'sr1vlc', 'sr1lc', 'sr1mc', 'sr1hc'] 
SR2s = ['sr2vla', 'sr2la', 'sr2ma', 'sr2ha', 'sr2vlb', 'sr2lb', 'sr2mb', 'sr2hb', 'sr2vlc', 'sr2lc', 'sr2mc', 'sr2hc'] 
CRs = ['cr1a', 'cr1b', 'cr1c', 'cr2a', 'cr2b', 'cr2c']

allRegions = SR1s + SR2s + CRs

finalSys = {'NonUniv':{}, 'NonClosure':{}, 'together':{'NonUniv':{}, 'NonClosure':{}}}

for reg in allRegions:
  finalSys['NonUniv'][reg] = {}   
  finalSys['NonClosure'][reg] = {}   
  finalSys['together']['NonUniv'][reg] = {}   
  finalSys['together']['NonClosure'][reg] = {}   

for reg in allRegions:

   if 'vl' in reg:
      ptTag = 'ptVL'
   elif 'l' in reg:
      ptTag = 'ptL'
   elif 'm' in reg:
      ptTag = 'ptM'
   elif 'h' in reg:
      ptTag = 'ptH'
   else:
      ptTag = 'ptCR'

   finalSys['NonUniv'][reg]['Fakes'] =                systs['NonUniv'][ptTag]
   finalSys['NonClosure'][reg]['Fakes'] =             systs['NonClosure'][reg]
   finalSys['together']['NonUniv'][reg]['Fakes'] =    systs['NonUniv'][ptTag]
   finalSys['together']['NonClosure'][reg]['Fakes'] = systs['NonClosure'][reg]

#Pickle results
overwrite = False
if save: 
   # together
   pickleFileName1 = "%s/fakeSystematics_%s.pkl"%(savedir, finalTag) 
   if os.path.isfile(pickleFileName1) and not overwrite:
      print "%s file exists. Set overwrite to True to overwrite."%pickleFileName1
   else:
      pickleFile1 = open(pickleFileName1, "w")
      pickle.dump(finalSys['together'], pickleFile1)
      pickleFile1.close()
   
   # NonUniv
   pickleFileName2 = "%s/fakeSystematics_%s_NonUniv.pkl"%(savedir, finalTag) 
   if os.path.isfile(pickleFileName2) and not overwrite:
      print "%s file exists. Set overwrite to True to overwrite."%pickleFileName2
   else:
      pickleFile2 = open(pickleFileName2, "w")
      pickle.dump(finalSys['NonUniv'], pickleFile2)
      pickleFile2.close()
   
   # NonClosure
   pickleFileName3 = "%s/fakeSystematics_%s_NonClosure.pkl"%(savedir, finalTag) 
   if os.path.isfile(pickleFileName3) and not overwrite:
      print "%s file exists. Set overwrite to True to overwrite."%pickleFileName3
   else:
      pickleFile3 = open(pickleFileName3, "w")
      pickle.dump(finalSys['NonClosure'], pickleFile3)
      pickleFile3.close()
