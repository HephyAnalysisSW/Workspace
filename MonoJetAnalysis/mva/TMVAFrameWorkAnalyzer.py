import ROOT
import pickle
from localConfig import afsUser, nfsUser, localPlotDir
from array import array
import os, sys
from math import sqrt

for path in [os.path.abspath(p) for p in ['../../HEPHYCommonTools/mva', 'HEPHYCommonTools/cardFileWriter/', '../python', '../../HEPHYCommonTools/cardFileWriter']]:
  if not path in sys.path:
      sys.path.insert(1, path)

from Workspace.HEPHYCommonTools.nnAnalysisHelpers import getEList, constructDataset, getYield, fillNNHisto
from xsec import xsec
from xsecSMS import gluino8TeV_NLONLL, gluino14TeV_NLO
import copy, sys
from defaultConvertedTuples import *  
from defaultConvertedTuples import wJetsToLNu
from monoJetFuncs import softIsolatedMT
from cardFileWriter import cardFileWriter
#RA4

signalModel = stop300lsp270FastSim
backgrounds = [wJetsToLNu]

#preprefix = 'MonoJet_Try2_'+signalModel['name']+'_refsel_NormDeco_10000_sigmoid_BP_S03_SE08_'
#prefix = "MonoJet_MLP21_"+signalModel['name']+"_refsel_Norm_ConvergenceTests15_ConvImpr1e-6_1000_sigmoid_BP_S1_SE1_softIsolatedMT_type1phiMet_deltaPhi"
#prefix = "MonoJet_BDTvsMLP_"+signalModel['name']+"_refsel_None_softIsolatedMT_type1phiMet_deltaPhi_isrJetPt_htRatio"

#1st try, 9v: prefix = 'MonoJet_stopDeltaM30FastSim_BkgMix_0_nTrees400_nCuts_-1_maxDepth_1_maxDepthComparison_softIsolatedMT_type1phiMet_deltaPhi_isrJetPt_softIsolatedMuPt_softIsolatedMuEta_softIsolatedMuCharge_ht_njet'
#2nd try, 8v (njet removed): 

#prefix = 'MonoJet_stopDeltaM30FastSim_BkgMix_0_nTrees400_nCuts_-1_maxDepth_1_maxDepthComparison_softIsolatedMT_type1phiMet_deltaPhi_isrJetPt_softIsolatedMuPt_softIsolatedMuEta_softIsolatedMuCharge_ht'

allVars = ["softIsolatedMT", "type1phiMet",'deltaPhi', 'isrJetPt', 'softIsolatedMuPt', 'softIsolatedMuEta', 'softIsolatedMuCharge', 'ht', 'njet' ]
#for omit in range(len(allVars)+1):
#  selectedVars = allVars[0:omit] + allVars[omit+1:] 
if True:
  selectedVars = allVars
  prefix = 'MonoJet_stopDeltaM30FastSim_BkgMix_0_nTrees400_nCuts_-1_maxDepth_1_maxDepthComparison_'
  prefix+="_".join(selectedVars)
  postfix = ""
  weight = 'weight'

  overWrite = True

  setup=pickle.load(file('/data/'+nfsUser+'/MonoJetNNAnalysis/MVA_Analyzer/'+prefix+'.pkl'))

  reader = ROOT.TMVA.Reader()  
  for var in setup['mvaInputVars']:
    var_i  = array('f',[0])
  #  vars[var] = var_i
    reader.AddVariable(var,var_i)

  allMethods = {}
  for m in setup['methodConfigs']:
    if m['type']!=ROOT.TMVA.Types.kCuts: 
      allMethods[m['name']] = {'reader':reader.BookMVA(m['name'],setup['weightDir']+'/TMVAClassification_'+m['name']+'.weights.xml'), 'config':m}
    else:
      allMethods[m['name']] = {'reader':reader.BookMVA(m['name'],setup['weightDir']+'/TMVAClassification_'+m['name']+'.weights.xml'), 'config':m}

  #cSignal = ROOT.TChain("Events")
  #cSignal.Add("/data/schoef/monoJetTuples_v3/copy/stop300lsp270FastSim/histo_stop300lsp270FastSim.root")
  #
  #cBkg    = ROOT.TChain("Events")
  #cBkg.Add("/data/schoef/monoJetTuples_v3/copy/W1JetsToLNu/histo_W1JetsToLNu.root")
  #cBkg.Add("/data/schoef/monoJetTuples_v3/copy/W2JetsToLNu/histo_W2JetsToLNu.root")
  #cBkg.Add("/data/schoef/monoJetTuples_v3/copy/W3JetsToLNu/histo_W3JetsToLNu.root")
  #cBkg.Add("/data/schoef/monoJetTuples_v3/copy/W4JetsToLNu/histo_W4JetsToLNu.root")

  def getScaledWeight(c):
    return  c.GetLeaf('weight').GetValue()*c.GetLeaf('testSampleScaleFac').GetValue()

  data = constructDataset(setup, None, None, False)
  #limits={}
  #resFile = "/data/schoef/nnAnalysis/MVA_Analyzer/limits/"+prefix+postfix+"_"+'limits.pkl'
  if overWrite or not os.path.isfile(resFile):
    import numpy as np
    from scipy import optimize
    classifier = 'BDT_maxDepth1'
    def getFom(thresh, classifier, relSysErr=0.05, lepCharge=0, verbose=False, resType="fom"):
      cut = setup['preselection']
      if lepCharge==-1:
        cut += "&&softIsolatedMuCharge==-1"
      if lepCharge==1:
        cut += "&&softIsolatedMuCharge==+1"
      yieldStot = getYield(data['allTestEvents'], setup, reader, allMethods[classifier]['config'], cut+'&&type==1&&mstop==300&&mlsp==270', -999, weightFunc = getScaledWeight)
      yieldS    = getYield(data['allTestEvents'], setup, reader, allMethods[classifier]['config'], cut+'&&type==1&&mstop==300&&mlsp==270', thresh, weightFunc = getScaledWeight)
      yieldB = getYield(data['allTestEvents'], setup, reader, allMethods[classifier]['config'], cut+'&&type==0', thresh, weightFunc = getScaledWeight )
  #      yieldS = getYieldFromChain(cSignal, cut, weight = "weight")
  #      yieldB = getYieldFromChain(cBkg,    cut, weight = "weight")
      if yieldS<=0. or yieldB<=0.:return -999.
      fom = yieldS/sqrt(yieldB + (relSysErr*yieldB)**2)
      
      if verbose: print "thresh", thresh,"fom:",fom,'cut',cut,'sigEff:',yieldS/yieldStot
      if resType=="fom":
        return fom
      else:
        return {'fom':fom,'yieldS':yieldS,"yieldB":yieldB,'sigEff':yieldS/yieldStot}

    print "Find start value"
    xstart = 0.5 
    while 1:
      v = getFom(xstart, classifier, relSysErr=0.05, lepCharge=-1)
      if v>0:break
      xstart-=0.05
    print "Starting at", xstart

    x0 = np.array([xstart])
    optThresh = optimize.fmin(lambda x:-getFom(x,classifier,relSysErr=0.05, lepCharge=-1,verbose=True), x0)

    for relSysErr in [0., 0.05, 0.08, 0.15]:
      print 'relSysErr',relSysErr
      print "charge:-",getFom(optThresh,classifier, relSysErr=relSysErr,lepCharge=-1,resType="")
      print "charge:+",getFom(optThresh,classifier, relSysErr=relSysErr,lepCharge=+1,resType="")
      print 'comb',getFom(optThresh,classifier,relSysErr=relSysErr,resType="")

#    sigInc = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1", -1, weight)
#    def getSigEffDev(thresh):
#      sig = getYield(data['simu'],  setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1", thresh, weight)
#      res= sig/float(sigInc) 
#      print "Optimizing MVA cut for targetSigEff of ",targetSigEff,". Testing threshold",thresh,"found sig eff.:", res
#      return abs(res-targetSigEff)

#    opt = ""
#    def getExpExcl(thresh, retType=None): 
#      bkgPlus = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0&&softIsolatedMuCharge==1", thresh, weight)
#      sigPlus = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&softIsolatedMuCharge==1", thresh, weight)
#      bkgMinus = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0&&softIsolatedMuCharge==-1", thresh, weight)
#      sigMinus = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&softIsolatedMuCharge==-1", thresh, weight)
#      c = cardFileWriter()
#      c.addBin('BinPlus', ['bkg'], 'BinPlus')
#      c.specifyObservation('BinPlus', int(bkgPlus))
#      c.specifyExpectation('BinPlus', 'bkg', bkgPlus)
#      c.specifyExpectation('BinPlus', 'signal', sigPlus)
#      c.addBin('BinMinus', ['bkg'], 'BinMinus')
#      c.specifyObservation('BinMinus', int(bkgMinus))
#      c.specifyExpectation('BinMinus', 'bkg', bkgMinus)
#      c.specifyExpectation('BinMinus', 'signal', sigMinus)
#      c.addUncertainty('globalUnc', 'lnN')
#      c.specifyUncertainty('globalUnc', 'BinPlus', 'bkg', 1.09)
#      c.specifyUncertainty('globalUnc', 'BinMinus', 'bkg', 1.09)
#      c.addUncertainty('globalUncPlus', 'lnN')
#      c.specifyUncertainty('globalUncPlus', 'BinPlus', 'bkg', 1.09)
#      c.addUncertainty('globalUncMinus', 'lnN')
#      c.specifyUncertainty('globalUncMinus', 'BinMinus', 'bkg', 1.09)
#      if bkgPlus==0. or sigPlus==0. or bkgMinus==0. or sigMinus==0.:
#        res={'0.500':float('nan')}
#      else:
#        res=  c.calcLimit('opt.txt',options=opt)
#      print "#########################", methodName, "##################################"
#      print "Now at thresh",thresh, "bkg+/sig+", bkgPlus,"/", sigPlus, "bkg-/sig-", bkgMinus,"/", sigMinus
#      print "Results",res
#      print "################################################################"
#      if not retType:
#        return res['0.500']
#      else:
#        return res
#
#    x0 = np.array([0.9])
#    optThresh = optimize.fmin(getExpExcl, x0)

#    limits[methodName]={}
#    limits[methodName]['result']=getExpExcl(optThresh[0], retType=1)
#    if limits[methodName]['result']['0.500']<float('inf'):
#      limits[methodName]['cutVal']=optThresh[0]
#      sigPlusInc = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&softIsolatedMuCharge==1", -1, weight)
#      sigPlus = getYield(data['simu'],    setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&softIsolatedMuCharge==1", optThresh[0], weight)
#      bkgPlusInc = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0&&softIsolatedMuCharge==1", -1, weight)
#      bkgPlus = getYield(data['simu'],    setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0&&softIsolatedMuCharge==1", optThresh[0], weight)
#      sigMinusInc = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&softIsolatedMuCharge==-1", -1, weight)
#      sigMinus = getYield(data['simu'],    setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&softIsolatedMuCharge==-1", optThresh[0], weight)
#      bkgMinusInc = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0&&softIsolatedMuCharge==-1", -1, weight)
#      bkgMinus = getYield(data['simu'],    setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0&&softIsolatedMuCharge==-1", optThresh[0], weight)
#      limits[methodName]['sigPlusEff']=sigPlus/float(sigPlusInc)
#      limits[methodName]['bkgPlusEff']=bkgPlus/float(bkgPlusInc)
#      limits[methodName]['sigMinusEff']=sigMinus/float(sigMinusInc)
#      limits[methodName]['bkgMinusEff']=bkgMinus/float(bkgMinusInc)
#  pickle.dump(limits, file(resFile, 'w')) 
#else:
#  limits = pickle.load(file(resFile))


