import os,sys,ROOT, pickle
from math import sqrt, pi, cos
from localConfig import afsUser, nfsUser, wwwPlotDir
from Workspace.HEPHYPythonTools.helpers import getChain, getYieldFromChain, getEList
from Workspace.HEPHYMVATools.mvaHelpers import getTrainingSampleSizes, createDatasetForTMVA
overWriteData = True 
addAllTestEventsTree = True

#define samples
from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_v6_Phys14V2 import * 
signal         = SMS_T5qqqqWW_Gl1500_Chi800_LSP100
backgrounds    = [ttJets, \
      #WJetsToLNu_HT100to200, 
#      WJetsToLNu_HT200to400, 
      WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf,
#      TTH, TTWJets, TTZJets
      ] 

for s in backgrounds+[signal]:
  assert len(s['bins'])==1, "Sample %s has more than one bin. Can't mix that."%s['name']

prefix = 'test_DegenerateStop_BkgMix'

setup={}
setup['dataFile'] = '/data/'+nfsUser+'/DegenerateStop/datasets/'+prefix+'.root'
setup['preselection'] = 'met_pt>200&&htJet25>500&&nJet>=4&&singleLeptonic'

weight = 'weight'
randomSeed = 1


#specify all observables that are used by TMVA
setup['obsFromInput'] = [weight, 'met_pt/D', 'nBJetMedium25/I', 'htJet25/D', 'nJet/I', 'leptonPt', 'mt2w', 'singleLeptonic/I']
setup['obsCalculated'] = [\
  ['mT', lambda c:sqrt(c.GetLeaf('met_pt').GetValue()*c.GetLeaf('leptonPt').GetValue()*(1.-cos(c.GetLeaf('met_phi').GetValue()-c.GetLeaf('leptonPhi').GetValue())))],
]
#put here all branches that are needed in obsCalculated and in the cut
transientBranches = ["leptonPhi", "met_phi", "leptonPt", "met_pt", "htJet25", "nJet", "singleLeptonic"]

chains={s['name']:getChain(s,histname='') for s in backgrounds+[signal]}
print "Get eLists..."
eLists={s['name']:getEList(chains[s['name']], setup['preselection']) for s in backgrounds+[signal]}
print "Get yields..."
yields={s['name']:getYieldFromChain(chains[s['name']], '('+weight+')*('+setup['preselection']+')') for s in backgrounds+[signal]}
for s in backgrounds+[signal]:
  print "Have %i events (yield %f) for sample %s and pre-selection %s"%(eLists[s['name']].GetN(), yields[s['name']], s['name'], setup['preselection'] )
  chains[s['name']].SetBranchStatus("*",0)
  for v in [x.split('/')[0] for x in setup['obsFromInput']] + transientBranches:
    chains[s['name']].SetBranchStatus(v,1)

#calculate training sample sizes
trainingSampleSizes = getTrainingSampleSizes(countSignal=eLists[signal['name']].GetN(),\
    bkgs=[{'count':eLists[b['name']].GetN(),'yield':yields[b['name']]} for b in backgrounds], 
    fractionForTraining=0.5)

#determine randomized training events
import random
random.seed(randomSeed)
def getRandList(n):
  l=range(n)
  random.shuffle(l)
  return l
signalEvents = getRandList(eLists[signal['name']].GetN())
signalTrainingEvents      = [eLists[signal['name']].GetEntry(j) for j in signalEvents[:trainingSampleSizes['sig']]]
maxNTestEvents=min(eLists[signal['name']].GetN(), 2*trainingSampleSizes['sig'])
signalTestEvents          = [eLists[signal['name']].GetEntry(j) for j in signalEvents[trainingSampleSizes['sig']:maxNTestEvents]]
backgroundTrainingEvents  = {}
backgroundTestEvents  = {}
for i, b in enumerate(backgrounds):
  backgroundEvents = getRandList(eLists[b['name']].GetN()) 
  backgroundTrainingEvents[b['name']] = [eLists[b['name']].GetEntry(j) for j in backgroundEvents[:trainingSampleSizes['bkgs'][i]]]
  maxNTestEvents=min(eLists[b['name']].GetN(), 2*trainingSampleSizes['bkgs'][i])
  backgroundTestEvents[b['name']]     = [eLists[b['name']].GetEntry(j) for j in backgroundEvents[trainingSampleSizes['bkgs'][i]:maxNTestEvents]]

#construct dataset
createDatasetForTMVA(setup, \
  signal={'chain':chains[signal['name']],  'trainingEvents':signalTrainingEvents,                'testEvents':signalTestEvents}, 
  backgrounds=[{'chain':chains[b['name']], 'trainingEvents':backgroundTrainingEvents[b['name']], 'testEvents':backgroundTestEvents[b['name']] } 
                  for b in backgrounds], 
  overWrite=overWriteData
#    ,maxEvents=10
)
 
