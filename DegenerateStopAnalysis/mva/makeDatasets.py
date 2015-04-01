import os,sys,ROOT, pickle
from math import sqrt, pi
from localConfig import afsUser, nfsUser, wwwPlotDir
from Workspace.HEPHYPythonTools.helpers import getChain, getYieldFromChain, getEList
from Workspace.HEPHYMVATools.mvaHelpers import getTrainingSampleSizes
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

weight = 'weight'
prefix = 'test_DegenerateStop_'+signal['name']+"_BkgMix"

setup={}
setup['dataFile'] = '/data/'+nfsUser+'/DegenerateStop/datasets/'+prefix+'.root'
setup['preselection'] = 'met_pt>200&&htJet25>500&&nJet>=4&&singleLeptonic'

#specify all observables that are used by TMVA
setup['obsFromInput'] = [weight, 'met_pt', 'nBJetMedium25/I', 'htJet25', 'nJet/I', 'leptonPt', 'mt2w']
setup['obsCalculated'] = [\
  ['mT', lambda c:sqrt(c.GetLeaf('met_pt').GetValue()*c.GetLeaf('leptonPt').GetValue()*(1.-cos(c.GetLeaf('met_phi').GetValue()-c.GetLeaf('leptonPhi').GetValue())))],
]

if overWriteData or not os.path.isfile(setup['dataFile']):

  chains={s['name']:getChain(s,histname='') for s in backgrounds+[signal]}
  print "Get eLists..."
  eLists={s['name']:getEList(chains[s['name']], setup['preselection']) for s in backgrounds+[signal]}
  print "Get yields..."
  yields={s['name']:getYieldFromChain(chains[s['name']], '('+weight+')*('+setup['preselection']+')') for s in backgrounds+[signal]}
  for s in backgrounds+[signal]:
    print "Have %i events (yield %f) for sample %s and pre-selection %s"%(eLists[s['name']].GetN(), yields[s['name']], s['name'], setup['preselection'] )

  #calculate training sample sizes
  trainingSampleSizes = getTrainingSampleSizes(countSignal=eLists[signal['name']].GetN(),\
      bkgs=[{'count':eLists[b['name']].GetN(),'yield':yields[b['name']]} for b in backgrounds], 
      fractionForTraining=0.5)

  #determine randomized training events
  import random
  random.seed(seed)
  def getRandList(n):
    l=range(n)
    random.shuffle(l)
    return l
  signalEvents = getRandList(eLists[signal['name']].GetN())
  signalTrainingEvents      = [eLists[signal['name']].GetEntry(i) for i in signalEvents[:trainingSampleSizes['sig']]]
  signalTestEvents          = [eLists[signal['name']].GetEntry(i) for i in signalEvents[trainingSampleSizes['sig']:]]
  backgroundTrainingEvents  = {}
  backgroundTestEvents  = {}
  for i, b in enumerate(backgrounds):
    backgroundEvents = getRandList(eLists[b['name']].GetN()) 
    backgroundTrainingEvents[b['name']] = [eLists[b['name']].GetEntry(i) for i in backgroundEvents[:trainingSampleSizes['bkgs']]]
    backgroundTestEvents[b['name']]     = [eLists[b['name']].GetEntry(i) for i in backgroundEvents[trainingSampleSizes['bkgs']:]]
  #construct dataset
  constructDataset(setup, \
    signal={'chain':chains[signal['name'],   'trainingEvents':signalTrainingEvents,                'testEvents':signalTestEvents}, 
    backgrounds=[{'chain':chains[b['name']], 'trainingEvents':backgroundTrainingEvents[b['name']], 'testEvents':backgroundTestEvents[b['name']] } 
                    for b in backgrounds], 
    overWrite=overWriteData
  )
 
#  setup["backgroundTrainEvents"] = []
#  setup["backgroundTestEvents"] = []
#  if addAllTestEventsTree:
#    setup["backgroundAllTestEvents"] = []
#  eventsPassingPreselection = {}
#  for bin in backgroundModel['bins']:
#    eventsPassingPreselection[bin]=[]
#  for i in range(backgroundModel['eListPreselection'].GetN()):
#    ev = backgroundModel['eListPreselection'].GetEntry(i)
#    for bin in backgroundModel['bins']:
#      if ev>=backgroundModel['rangeInChain'][bin][0] and ev<backgroundModel['rangeInChain'][bin][1]:
#        eventsPassingPreselection[bin].append(ev)
#
#  for bin in backgroundModel['bins']:
#    nTrainEvents = backgroundModel['optimalSize'][bin]/2
#    random.shuffle(eventsPassingPreselection[bin])
#    for ev in eventsPassingPreselection[bin][:nTrainEvents]:
#      setup["backgroundTrainEvents"].append(ev) 
#    for ev in eventsPassingPreselection[bin][nTrainEvents:backgroundModel['optimalSize'][bin]]:
#      setup["backgroundTestEvents"].append(ev) 
#    if addAllTestEventsTree:
#      scaleToNominal =  len(eventsPassingPreselection[bin])/float(len(eventsPassingPreselection[bin]) - nTrainEvents) 
#      for ev in eventsPassingPreselection[bin][nTrainEvents:]:
#        setup["backgroundAllTestEvents"].append([ev, scaleToNominal]) 
#
#  data = constructDataset(setup, signal, background, overWriteData, addAllTestEventsTree = addAllTestEventsTree)
#    
#  evList={}
#  testObs=['type1phiMet', 'softIsolatedMT', 'deltaPhi', 'rand']
#  n = data['simu'].GetEntries()
#  for i in range(n):
#    data['simu'].GetEntry(i)
#    type=data['simu'].GetLeaf('type').GetValue()
#    isTraining=data['simu'].GetLeaf('isTraining').GetValue()
#    for v in testObs:
#      if v=='rand':
#        val = random.random()
#      else:
#        val = data['simu'].GetLeaf(v).GetValue()
#      if not evList.has_key(v):
#        evList[v] = {}
#      if not evList[v].has_key(type):
#        evList[v][type] = {}
#      if not evList[v][type].has_key(isTraining):
#        evList[v][type][isTraining] = []
#      evList[v][type][isTraining].append(val)
#  print prefix
#  ksres = {}
#  ksres[prefix] = {}
#  for v in testObs:
#    s0 = evList[v][1][0]
#    s1 = evList[v][1][1]
#    TMathKSTest = ROOT.TMath.KolmogorovTest(len(s0), array('d', s0), len(s1), array('d',s1), '') 
#    print "ROOT.TMath.KolmogorovTest: ",v,":", TMathKSTest
#    ksDist = float(KolmogorovDistance(s0, s1))
#    print "my KS-Dist",v,":", ksDist 
#    ksProb = ROOT.TMath.KolmogorovProb(ksDist*sqrt(len(s0)*len(s1)/float(len(s0)+len(s1))))
#    print "ROOT.TMath.KolmogorovProb using my dist:", ksProb
#    ksres[prefix][v] = {'ksDist':ksDist, 'ksProb':ksProb, 'TMathKSTest':  TMathKSTest}
#    
#  for o in data.values():
#   if o:
#     o.IsA().Destructor(o)
#  del data
#
##for v in ['type1phiMet', 'softIsolatedMT', 'deltaPhi', 'rand']:
##  c1 = ROOT.TCanvas()
##  h = ROOT.TH1F('ksres','ksres', 100,0,1)
##  for prefix in ksres.keys():
##    h.Fill(ksres[prefix][v]['ksProb'])
##  h.Draw()
##  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMJ/inputKSTest_'+prefix+"_"+v+".png")



