import os,sys,ROOT, pickle
from math import sqrt, pi
from localConfig import afsUser, nfsUser, wwwPlotDir

#FIXME
from cmgSamples import *
signalModel = stopDeltaM30FastSim 
backgroundModel = wJetsToLNu


overWriteData = True 
addAllTestEventsTree = True

seed = 1
prefix = 'DegenerateStop_'+signalModel['name']+"_BkgMix_seed"+str(seed)

setup={}
setup['dataFile'] = '/data/'+nfsUser+'/DegenerateStop/datasets/'+prefix+'.root'
setup['preselection'] = 'FIXME CMG preselection'

assert overWriteData or not os.path.isfile(setup['dataFile']), "Error: %s exists"%setup['dataFile']

setup['varsFromInput'] = ['type1phiMet', 'isrJetPt', 'isrJetBTBVetoPassed', 'softIsolatedMuPt', 'softIsolatedMuEta','ht', 'nHardElectrons', 'nHardMuons', 'njet60/I','njet/I', 'weight', 'isrJetPt']
#  setup['varsFromInput_Signal'] = [\
#        ['mstop/I', getStopMassFromFilename],\
#        ['mlsp/I', getLSPMassFromFilename]] 
#
setup['varsCalculated'] = [\
                ['softIsolatedMT', softIsolatedMT],
                ['deltaPhi', lambda c:acos(cosDeltaPhiLepW(c))],
                ['softIsolatedMuCharge/I', lambda c:-c.GetLeaf('softIsolatedMuPdg').GetValue()/abs(c.GetLeaf('softIsolatedMuPdg').GetValue())],
                ['htRatio', htRatio]
  ]

#nSigTraining, maxBkgFractionForTraining=0.5, [{'nMax':nBkg1Max,'y':yBkg1},...,{'nMax':nBkgNMax,'y':yBkgN}]]
#finds nbBkg1,...,nBkgN such that nBkg1+...+nBkgN is maximal while respecting
#nBkg1+nBkg2+...+nBkgN<=nSigTraining, nBkg1:nBkg2:...:nBkgN=yBkg1:yBkg2:...:yBkgN
#and nBkg1<=maxBkgFractionForTraining*nBkg1Max, ...., maxBkgFractionForTraining*nBkgNMax<=nBkgNMax
def findTrainingSamples(nSigTraining=nSigTraining, bkgs, maxBkgFractionForTraining=0.5):
  maxBkgForTraining = [int(maxBkgFractionForTraining*b['nMax']) for b in bkgs ]

#  weightForSampleComposition = "weight"
#  signal      = ROOT.TChain('Events')
#  for b in signalModel['bins']:
#    fstring  = signalModel['dirname']+'/'+b+'/*.root'
#    signal.Add(fstring)
#    signalSampleSize = signal.GetEntries(setup['preselection'])
#    signal.Draw(">>eList", setup['preselection'])
#    signalModel['eListPreselection'] = ROOT.gDirectory.Get("eList").Clone('eListPreselectionSignal')
#    print "Added bin ",b,"to signal, now",signal.GetEntries()," after preselection:",signalSampleSize,signalModel['eListPreselection'].GetN()
#
#  background      = ROOT.TChain('Events')
#  counter=0
#  backgroundModel['rangeInChain'] = {}
#  backgroundModel['sumOfWeightsAfterPreselection'] = {}
#  backgroundModel['countAfterPreselection'] = {}
#  for bin in backgroundModel['bins']:
#    lL = background.GetEntries()
#    fstring  = backgroundModel['dirname']+'/'+bin+'/*.root'
#    background.Add(fstring)
#    uL = background.GetEntries()
#    backgroundModel['rangeInChain'][bin] = [lL, uL]
#    print "Added bin ",bin,"to background, now,",uL,"entries"
#    backgroundModel['sumOfWeightsAfterPreselection'][bin] = 0.
#    backgroundModel['countAfterPreselection'][bin] = 0
#  print "Calculating Sum(weights) for sample composition"
#  background.Draw(">>eList", setup['preselection'])
#  backgroundModel['eListPreselection'] = ROOT.gDirectory.Get("eList").Clone('eListPreselectionBackground')
#  for i in range(backgroundModel['eListPreselection'].GetN()):
#    ev = backgroundModel['eListPreselection'].GetEntry(i)
#    background.GetEntry(ev)
#    for bin in backgroundModel['bins']: 
#      if ev>=backgroundModel['rangeInChain'][bin][0] and ev<backgroundModel['rangeInChain'][bin][1]:
#        backgroundModel['sumOfWeightsAfterPreselection'][bin]+=background.GetLeaf(weightForSampleComposition).GetValue()
#        backgroundModel['countAfterPreselection'][bin] += 1
#  
#  maxSumW=max(backgroundModel['sumOfWeightsAfterPreselection'].values())
#  backgroundModel['reductionFactor'] = {}
#  for bin in backgroundModel['bins']:
#    print "bin",bin,":",backgroundModel['countAfterPreselection'][bin]," events after preselection"
#    backgroundModel['reductionFactor'][bin] = backgroundModel['sumOfWeightsAfterPreselection'][bin]/maxSumW
#  maxBkgSampleSize = sum([backgroundModel['reductionFactor'][bin]*backgroundModel['countAfterPreselection'][bin] for bin in backgroundModel['bins']])
#   
#  if signalSampleSize>maxBkgSampleSize:
#    print "Higher signal stat.!"
#    totalFinalBkgSampleSize = sum([int(round(backgroundModel['reductionFactor'][bin]*backgroundModel['countAfterPreselection'][bin])) for bin in backgroundModel['bins']])
#    totalFinalSignalSampleSize = finalBkgSampleSize
#    signalModel['optimalSize'] = totalFinalSignalSampleSize
#    backgroundModel['optimalSize'] = {}
#    for b in backgroundModel['bins']:
#      backgroundModel['optimalSize'][b] = int(round(backgroundModel['reductionFactor'][bin]*backgroundModel['countAfterPreselection'][bin]))
#  else:
#    print "Higher background stat.!"
#    redFac = signalSampleSize/float(maxBkgSampleSize)
#    for k in backgroundModel['reductionFactor'].keys():
#      backgroundModel['reductionFactor'][k]*=redFac
#    totalFinalBkgSampleSize = sum([int(round(backgroundModel['reductionFactor'][bin]*backgroundModel['countAfterPreselection'][bin])) for bin in backgroundModel['bins']])
#    totalFinalSignalSampleSize = signalSampleSize
#    signalModel['optimalSize'] = totalFinalSignalSampleSize
#    backgroundModel['optimalSize'] = {}
#    for b in backgroundModel['bins']:
#      backgroundModel['optimalSize'][b] = int(round(backgroundModel['reductionFactor'][b]*backgroundModel['countAfterPreselection'][b]))
#  print "Solution: Signal:",totalFinalSignalSampleSize, "Background:",totalFinalBkgSampleSize 
#  print " ".join([ k+":"+str(int(round(backgroundModel['reductionFactor'][k]*backgroundModel['countAfterPreselection'][k]))) for k in backgroundModel['reductionFactor'].keys()])
#
#  #Constructing randomized samples
#  random.seed(seed)
#
#  signalEvents = range(signalModel['eListPreselection'].GetN())
#  random.shuffle(signalEvents)
#  nTrainEvents = signalModel['optimalSize']/2
#  setup["signalTrainEvents"] = []
#  setup["signalTestEvents"] = []
#  if addAllTestEventsTree:
#    setup["signalAllTestEvents"] = []
#  for i in signalEvents[:nTrainEvents]:
#    setup["signalTrainEvents"].append(signalModel['eListPreselection'].GetEntry(i)) 
#  for i in signalEvents[nTrainEvents:signalModel['optimalSize']]:
#    setup["signalTestEvents"].append(signalModel['eListPreselection'].GetEntry(i))
#  if addAllTestEventsTree:
#    scaleToNominal = signalModel['eListPreselection'].GetN() / float(signalModel['eListPreselection'].GetN() - nTrainEvents) 
#    for i in signalEvents[nTrainEvents:]:
#      setup["signalAllTestEvents"].append([signalModel['eListPreselection'].GetEntry(i), scaleToNominal]) 
#
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
#  testVars=['type1phiMet', 'softIsolatedMT', 'deltaPhi', 'rand']
#  n = data['simu'].GetEntries()
#  for i in range(n):
#    data['simu'].GetEntry(i)
#    type=data['simu'].GetLeaf('type').GetValue()
#    isTraining=data['simu'].GetLeaf('isTraining').GetValue()
#    for v in testVars:
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
#  for v in testVars:
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



