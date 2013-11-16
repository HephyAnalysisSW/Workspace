import ROOT
import pickle
from localConfig import afsUser, nfsUser, localPlotDir
from array import array
import os, sys

for path in [os.path.abspath(p) for p in ['../../HEPHYCommonTools/mva', 'HEPHYCommonTools/cardFileWriter/', '../python', '../../HEPHYCommonTools/cardFileWriter']]:
  if not path in sys.path:
      sys.path.insert(1, path)

from nnAnalysisHelpers import getEList, constructDataset, getYield, fillNNHisto
from xsec import xsec
from xsecSMS import gluino8TeV_NLONLL, gluino14TeV_NLO
import copy, sys
from defaultConvertedTuples import stop300lsp270, stop200lsp170g100, stop300lsp240g150
from defaultConvertedTuples import wJetsToLNu
from monoJetFuncs import softIsolatedMT
from cardFileWriter import cardFileWriter
#RA4

signalModel = stop300lsp270
backgrounds = [wJetsToLNu]

#preprefix = 'MonoJet_Try2_'+signalModel['name']+'_refsel_NormDeco_10000_sigmoid_BP_S03_SE08_'
#prefix = "MonoJet_MLP21_"+signalModel['name']+"_refsel_Norm_ConvergenceTests15_ConvImpr1e-6_1000_sigmoid_BP_S1_SE1_softIsolatedMT_type1phiMet_deltaPhi"
prefix = "MonoJet_BDTvsMLP_"+signalModel['name']+"_refsel_None_softIsolatedMT_type1phiMet_deltaPhi_isrJetPt_htRatio"
#targetSigEff=0.2
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

data = constructDataset(setup, None, None, False)
nev = data['simu'].GetEntries()
limits={}
resFile = "/data/schoef/nnAnalysis/MVA_Analyzer/limits/"+prefix+postfix+"_"+'limits.pkl'
if overWrite or not os.path.isfile(resFile):
  for methodName in [ 'MLP21_nCyc1000']:#, 'myCut']:
    import numpy as np
    from scipy import optimize
  #      def getBkgDev(thresh):
  #        res= getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0", thresh, 'weightLumi') 
  #        print "Optimizing MVA cut for bkg estimation of ",targetBkg,". Testing threshold",thresh,"found bkg exp.:",res
  #        return abs(res-targetBkg)
  #      x0 = np.array([0.9])
  #      optThresh = optimize.fmin(getBkgDev, x0)
    sigInc = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1", -1, weight)
    def getSigEffDev(thresh):
      sig = getYield(data['simu'],  setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1", thresh, weight)
      res= sig/float(sigInc) 
      print "Optimizing MVA cut for targetSigEff of ",targetSigEff,". Testing threshold",thresh,"found sig eff.:", res
      return abs(res-targetSigEff)

  #    x0 = np.array([0.9])
  #    optThresh = optimize.fmin(getSigEffDev, x0)

  #  if (model=="T1tttt" or model=="T1tttt-madgraph") and mgl<=950 and mN<=400:
  #    opt = "--rMax 10.0"
  #  else:
    opt = ""

    def getExpExcl(thresh, retType=None): 
      bkgPlus = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0&&softIsolatedMuCharge==1", thresh, weight)
      sigPlus = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&softIsolatedMuCharge==1", thresh, weight)
      bkgMinus = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0&&softIsolatedMuCharge==-1", thresh, weight)
      sigMinus = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&softIsolatedMuCharge==-1", thresh, weight)

      c = cardFileWriter()
      c.addBin('BinPlus', ['bkg'], 'BinPlus')
      c.specifyObservation('BinPlus', int(bkgPlus))
      c.specifyExpectation('BinPlus', 'bkg', bkgPlus)
      c.specifyExpectation('BinPlus', 'signal', sigPlus)
      c.addBin('BinMinus', ['bkg'], 'BinMinus')
      c.specifyObservation('BinMinus', int(bkgMinus))
      c.specifyExpectation('BinMinus', 'bkg', bkgMinus)
      c.specifyExpectation('BinMinus', 'signal', sigMinus)
      c.addUncertainty('globalUnc', 'lnN')
      c.specifyUncertainty('globalUnc', 'BinPlus', 'bkg', 1.09)
      c.specifyUncertainty('globalUnc', 'BinMinus', 'bkg', 1.09)
      c.addUncertainty('globalUncPlus', 'lnN')
      c.specifyUncertainty('globalUncPlus', 'BinPlus', 'bkg', 1.09)
      c.addUncertainty('globalUncMinus', 'lnN')
      c.specifyUncertainty('globalUncMinus', 'BinMinus', 'bkg', 1.09)
      if bkgPlus==0. or sigPlus==0. or bkgMinus==0. or sigMinus==0.:
        res={'0.500':float('nan')}
      else:
        res=  c.calcLimit('opt.txt',options=opt)
      print "#########################", methodName, "##################################"
      print "Now at thresh",thresh, "bkg+/sig+", bkgPlus,"/", sigPlus, "bkg-/sig-", bkgMinus,"/", sigMinus
      print "Results",res
      print "################################################################"
      if not retType:
        return res['0.500']
      else:
        return res

    x0 = np.array([0.9])
    optThresh = optimize.fmin(getExpExcl, x0)

    limits[methodName]={}
    limits[methodName]['result']=getExpExcl(optThresh[0], retType=1)
    if limits[methodName]['result']['0.500']<float('inf'):
      limits[methodName]['cutVal']=optThresh[0]
      sigPlusInc = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&softIsolatedMuCharge==1", -1, weight)
      sigPlus = getYield(data['simu'],    setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&softIsolatedMuCharge==1", optThresh[0], weight)
      bkgPlusInc = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0&&softIsolatedMuCharge==1", -1, weight)
      bkgPlus = getYield(data['simu'],    setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0&&softIsolatedMuCharge==1", optThresh[0], weight)
      sigMinusInc = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&softIsolatedMuCharge==-1", -1, weight)
      sigMinus = getYield(data['simu'],    setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&softIsolatedMuCharge==-1", optThresh[0], weight)
      bkgMinusInc = getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0&&softIsolatedMuCharge==-1", -1, weight)
      bkgMinus = getYield(data['simu'],    setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0&&softIsolatedMuCharge==-1", optThresh[0], weight)
      limits[methodName]['sigPlusEff']=sigPlus/float(sigPlusInc)
      limits[methodName]['bkgPlusEff']=bkgPlus/float(bkgPlusInc)
      limits[methodName]['sigMinusEff']=sigMinus/float(sigMinusInc)
      limits[methodName]['bkgMinusEff']=bkgMinus/float(bkgMinusInc)

  pickle.dump(limits, file(resFile, 'w')) 
else:
  limits = pickle.load(file(resFile))

#methodName = 'MLP21_nCyc1000'
#hSigPlus = fillNNHisto(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&softIsolatedMuCharge==1", ROOT.TH1F("h", "h", 50,0,1.5), weight)
#hBkgPlus = fillNNHisto(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0&&softIsolatedMuCharge==1", ROOT.TH1F("h", "h", 50,0,1.5), weight)
#
#hSigMinus = fillNNHisto(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&softIsolatedMuCharge==-1", ROOT.TH1F("h", "h", 50,0,1.5), weight)
#hBkgMinus = fillNNHisto(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0&&softIsolatedMuCharge==-1", ROOT.TH1F("h", "h", 50,0,1.5), weight)
#
##cutMin = ROOT.std.vector('float')()
##cutMax = ROOT.std.vector('float')()
#
##import ctypes
##p_c_double_8 = ctypes.c_double * 8
##cutMin = p_c_double_8()
##cutMax = p_c_double_8()
##
##
##cutMin = array('f', [0. for x in range(8)])
##cutMax = array('f', [0. for x in range(8)])
