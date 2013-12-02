import os,sys,ROOT, pickle
from math import sqrt, pi
from localConfig import afsUser, nfsUser, localPlotDir
import random
from array import array
for path in [os.path.abspath(p) for p in ['../../HEPHYCommonTools/mva', '../../HEPHYCommonTools/cardFileWriter/', '../../HEPHYCommonTools/python/', '../python/']]:
  if not path in sys.path:
      sys.path.insert(1, path)

from nnAnalysisHelpers import getEList, constructDataset, setupMVAFrameWork
from xsec import xsec
from xsecSMS import gluino8TeV_NLONLL, gluino14TeV_NLO
import copy, sys
from defaultConvertedTuples import stop300lsp270FastSim, stop200lsp170g100FastSim, stop300lsp240g150FastSim
from defaultConvertedTuples import wJetsToLNu
from monoJetFuncs import softIsolatedMT
from helpers import htRatio, KolmogorovDistance 
#RA4

signalModel = stop300lsp270FastSim
backgroundModel = wJetsToLNu

colors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kOrange, ROOT.kMagenta]

overWriteData = True 

setup={}

#setup['TMVAFactoryOptions'] = ["!V","!Silent","Color","DrawProgressBar","Transformations=I;D;G,D","AnalysisType=Classification"]

ksres = {}
for seed in range(50):
  prepreprefix = 'MonoJet_'+signalModel['name']+"_BkgMix_"+str(seed)

#  def createDatasetForModelPoint(signalModel):
  if True:    
    preprefix = prepreprefix
    prefix = preprefix

    setup['dataFile'] = '/data/'+nfsUser+'/MonoJetNNAnalysis/datasets/'+prefix+'.root'

    if (not overWriteData and ( os.path.isfile(setup['dataFile']))) :
      print "File",setup['dataFile'],"found->do load!"
      data = constructDataset(setup, None, None, overWriteData)
    else: 
      setup['preselection'] = 'isrJetPt>110&&isrJetBTBVetoPassed&&softIsolatedMuPt>5&&nHardElectrons+nHardMuons==0&&njet60<=2&&type1phiMet>150'
      setup["sigMVAWeightFac"] = 1.#background.GetEntries(setup['preselection'])/float(signal.GetEntries(setup['preselection']))
      setup["bkgMVAWeightFac"] = 1.
  #    setup['weightForMVA'] = {'weight':1., 'sigFac':float(sigScale)/100., 'bkgFac':1}
      setup['weightForMVA'] = {'weight':1., 'sigFac':1., 'bkgFac':1}
      #If changing between met and type1phiMet the formula for deltaPhi (if used) has to be changed!
      setup['varsFromInputData'] = ['type1phiMet', 'isrJetPt', 'isrJetBTBVetoPassed', 'softIsolatedMuPt', 'nHardElectrons', 'nHardMuons', 'njet60/I', 'weight', 'isrJetPt']
      setup['varsFromInputSignal'] = [] #model parameters to be stored in MVA data file

      from monoJetFuncs import cosDeltaPhiLepW, softIsolatedMT
      from math import acos
      setup['varsCalculated'] = [\
                      ['softIsolatedMT', softIsolatedMT],
                      ['deltaPhi', lambda c:acos(cosDeltaPhiLepW(c))],
                      ['softIsolatedMuCharge/I', lambda c:-c.GetLeaf('softIsolatedMuPdg').GetValue()/abs(c.GetLeaf('softIsolatedMuPdg').GetValue())],
                      ['htRatio', htRatio]
        ]
      print "Scaling signal weights by ", setup["sigMVAWeightFac"],'using weight', setup['weightForMVA']

      weightForSampleComposition = "weight"
      signal      = ROOT.TChain('Events')
      for b in signalModel['bins']:
        fstring  = signalModel['dirname']+'/'+b+'/*.root'
        signal.Add(fstring)
        signalSampleSize = signal.GetEntries(setup['preselection'])
        signal.Draw(">>eList", setup['preselection'])
        signalModel['eListPreselection'] = ROOT.gDirectory.Get("eList").Clone('eListPreselectionSignal')
        print "Added bin ",b,"to signal, now",signal.GetEntries()," after preselection:",signalSampleSize,signalModel['eListPreselection'].GetN()

      background      = ROOT.TChain('Events')
      counter=0
      backgroundModel['rangeInChain'] = {}
      backgroundModel['sumOfWeightsAfterPreselection'] = {}
      backgroundModel['countAfterPreselection'] = {}
      for bin in backgroundModel['bins']:
        lL = background.GetEntries()
        fstring  = backgroundModel['dirname']+'/'+bin+'/*.root'
        background.Add(fstring)
        uL = background.GetEntries()
        backgroundModel['rangeInChain'][bin] = [lL, uL]
        print "Added bin ",bin,"to background, now,",uL,"entries"
        backgroundModel['sumOfWeightsAfterPreselection'][bin] = 0.
        backgroundModel['countAfterPreselection'][bin] = 0
      print "Calculating Sum(weights) for sample composition"
      background.Draw(">>eList", setup['preselection'])
      backgroundModel['eListPreselection'] = ROOT.gDirectory.Get("eList").Clone('eListPreselectionBackground')
      for i in range(backgroundModel['eListPreselection'].GetN()):
        ev = backgroundModel['eListPreselection'].GetEntry(i)
        background.GetEntry(ev)
        for bin in backgroundModel['bins']: 
          if ev>=backgroundModel['rangeInChain'][bin][0] and ev<backgroundModel['rangeInChain'][bin][1]:
            backgroundModel['sumOfWeightsAfterPreselection'][bin]+=background.GetLeaf(weightForSampleComposition).GetValue()
            backgroundModel['countAfterPreselection'][bin] += 1
      
      maxSumW=max(backgroundModel['sumOfWeightsAfterPreselection'].values())
      backgroundModel['reductionFactor'] = {}
      for bin in backgroundModel['bins']:
        print "bin",bin,":",backgroundModel['countAfterPreselection'][bin]," events after preselection"
        backgroundModel['reductionFactor'][bin] = backgroundModel['sumOfWeightsAfterPreselection'][bin]/maxSumW
      maxBkgSampleSize = sum([backgroundModel['reductionFactor'][bin]*backgroundModel['countAfterPreselection'][bin] for bin in backgroundModel['bins']])
       
      if signalSampleSize>maxBkgSampleSize:
        print "Higher signal stat.!"
        totalFinalBkgSampleSize = sum([int(round(backgroundModel['reductionFactor'][bin]*backgroundModel['countAfterPreselection'][bin])) for bin in backgroundModel['bins']])
        totalFinalSignalSampleSize = finalBkgSampleSize
        signalModel['optimalSize'] = totalFinalSignalSampleSize
        backgroundModel['optimalSize'] = {}
        for b in backgroundModel['bins']:
          backgroundModel['optimalSize'][b] = int(round(backgroundModel['reductionFactor'][bin]*backgroundModel['countAfterPreselection'][bin]))
      else:
        print "Higher background stat.!"
        redFac = signalSampleSize/float(maxBkgSampleSize)
        for k in backgroundModel['reductionFactor'].keys():
          backgroundModel['reductionFactor'][k]*=redFac
        totalFinalBkgSampleSize = sum([int(round(backgroundModel['reductionFactor'][bin]*backgroundModel['countAfterPreselection'][bin])) for bin in backgroundModel['bins']])
        totalFinalSignalSampleSize = signalSampleSize
        signalModel['optimalSize'] = totalFinalSignalSampleSize
        backgroundModel['optimalSize'] = {}
        for b in backgroundModel['bins']:
          backgroundModel['optimalSize'][b] = int(round(backgroundModel['reductionFactor'][b]*backgroundModel['countAfterPreselection'][b]))
      print "Solution: Signal:",totalFinalSignalSampleSize, "Background:",totalFinalBkgSampleSize 
      print " ".join([ k+":"+str(int(round(backgroundModel['reductionFactor'][k]*backgroundModel['countAfterPreselection'][k]))) for k in backgroundModel['reductionFactor'].keys()])

      #Constructing randomized samples
      random.seed(seed)

      signalEvents = range(signalModel['eListPreselection'].GetN())
      random.shuffle(signalEvents)
      nTrainEvents = signalModel['optimalSize']/2
      setup["signalTrainEvents"] = []
      setup["signalTestEvents"] = []
      for i in signalEvents[:nTrainEvents]:
        setup["signalTrainEvents"].append(signalModel['eListPreselection'].GetEntry(i)) 
      for i in signalEvents[nTrainEvents:signalModel['optimalSize']]:
        setup["signalTestEvents"].append(signalModel['eListPreselection'].GetEntry(i)) 

      setup["backgroundTrainEvents"] = []
      setup["backgroundTestEvents"] = []

      eventsPassingPreselection = {}
      for bin in backgroundModel['bins']:
        eventsPassingPreselection[bin]=[]
      for i in range(backgroundModel['eListPreselection'].GetN()):
        ev = backgroundModel['eListPreselection'].GetEntry(i)
        for bin in backgroundModel['bins']:
          if ev>=backgroundModel['rangeInChain'][bin][0] and ev<backgroundModel['rangeInChain'][bin][1]:
            eventsPassingPreselection[bin].append(ev)

      for bin in backgroundModel['bins']:
        nTrainEvents = backgroundModel['optimalSize'][bin]/2
        random.shuffle(eventsPassingPreselection[bin])
        for ev in eventsPassingPreselection[bin][:nTrainEvents]:
          setup["backgroundTrainEvents"].append(ev) 
        for ev in eventsPassingPreselection[bin][nTrainEvents:backgroundModel['optimalSize'][bin]]:
          setup["backgroundTestEvents"].append(ev) 

      data = constructDataset(setup, signal, background, overWriteData)
      

    evList={}
    testVars=['type1phiMet', 'softIsolatedMT', 'deltaPhi', 'rand']
    n = data['simu'].GetEntries()
    for i in range(n):
      data['simu'].GetEntry(i)
      type=data['simu'].GetLeaf('type').GetValue()
      isTraining=data['simu'].GetLeaf('isTraining').GetValue()
      for v in testVars:
        if v=='rand':
          val = random.random()
        else:
          val = data['simu'].GetLeaf(v).GetValue()
        if not evList.has_key(v):
          evList[v] = {}
        if not evList[v].has_key(type):
          evList[v][type] = {}
        if not evList[v][type].has_key(isTraining):
          evList[v][type][isTraining] = []
        evList[v][type][isTraining].append(val)
    print prefix
    ksres[prefix] = {}
    for v in testVars:
      s0 = evList[v][1][0]
      s1 = evList[v][1][1]
      TMathKSTest = ROOT.TMath.KolmogorovTest(len(s0), array('d', s0), len(s1), array('d',s1), '') 
      print "ROOT.TMath.KolmogorovTest: ",v,":", TMathKSTest
      ksDist = float(KolmogorovDistance(s0, s1))
      print "my KS-Dist",v,":", ksDist 
      ksProb = ROOT.TMath.KolmogorovProb(ksDist*sqrt(len(s0)*len(s1)/float(len(s0)+len(s1))))
      print "ROOT.TMath.KolmogorovProb using my dist:", ksProb
      ksres[prefix][v] = {'ksDist':ksDist, 'ksProb':ksProb, 'TMathKSTest':  TMathKSTest}
      
    for o in data.values():
     if o:
       o.IsA().Destructor(o)
    del data

for v in ['type1phiMet', 'softIsolatedMT', 'deltaPhi', 'rand']:
  c1 = ROOT.TCanvas()
  h = ROOT.TH1F('ksres','ksres', 100,0,1)
  for prefix in ksres.keys():
    h.Fill(ksres[prefix][v]['ksProb'])
  h.Draw()
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMJ/inputKSTest_'+prefix+"_"+v+".png")



