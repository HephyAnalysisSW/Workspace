import ROOT
import pickle
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain
from Workspace.RA4Analysis.cmgTuples_Data25ns_miniAODv2 import *


def allUnique(x):
  seen = list()
  return not any(i in seen or seen.append(i) for i in x)

chunks = getChunks(SingleElectron_Run2016B_PromptReco_v2)

chain = getChain(chunks[0],treeName='tree')

nEvents = chain.GetEntries()

ultimate_events = []

for i in range(nEvents):
  chain.GetEntry(i)
  run_branch = chain.GetLeaf('run').GetValue()
  lumi_branch = chain.GetLeaf('lumi').GetValue()
  evt_branch = chain.GetLeaf('evt').GetValue()
  #print run_branch , lumi_branch , evt_branch
  str_evt = "_".join([str(run_branch),str(lumi_branch),str(evt_branch)]) 
  #print str_evt
  ultimate_events.append(list(str_evt)) 
  
if not allUnique(ultimate_events):
  print "HEYY You have double counting in your events!!!!"
