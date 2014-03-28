import ROOT
import pickle
from smsHelpers import *
from localConfig import afsUser, nfsUser, localPlotDir
from array import array
import os, sys

for path in [os.path.abspath(p) for p in ['../../HEPHYCommonTools/mva', 'HEPHYCommonTools/cardFileWriter/', '../python', '../../HEPHYCommonTools/cardFileWriter']]:
  if not path in sys.path:
      sys.path.insert(1, path)

from Workspace.HEPHYCommonTools.nnAnalysisHelpers import getEList, constructDataset, getYield

model = "T1tttt"
mgl = 1300
mN = 850
refWeight = 1000
prepreprefix = 'RA4_test_refWeight'+str(refWeight)+'_'+model+'_4j_bt1_met100_mt2w0_NormDeco_10000_sigmoid_BP_S03_SE08_'
targetSigEff=0.2
postfix = "eff02"
weight = 'weightLumi14'
lumiFac = 0.25 
allJobs = [[mgl, mN]]
start=0
stop = len(allJobs)


#for mgl in range(400, 1425, 25):
#  for mN in range(0, mgl-175-1, 25):
overWrite = True
#allJobs = [[1100, 25]]
#start=0
#stop = len(allJobs)
#if len(sys.argv)>=3:
#  from jobs import jobs
#  jobs.sort()
#  start = int(sys.argv[1])
#  stop = int(sys.argv[2])
#  allJobs = jobs


print "allJobs", allJobs[start:stop]
for job in allJobs[start:stop]:
  mgl, mN = job
  limits={}
  blockStr = "mgl_"+str(mgl)+"_mN_"+str(mN)
  preprefix = prepreprefix+blockStr+'_'
#  block = getBlock(mgl, mN, model)
#  blockStr = getBlockString(mgl, mN, model)
  mvaInputVars = ["mT", "type1phiMet", "mt2w","nbtags","njets",'minDeltaPhi', 'htRatio','deltaPhi']
  prefix = ''
  for v in mvaInputVars:
    prefix+=v+'_'
  prefix = preprefix+prefix[:-1]
  
  resFile = "/data/schoef/nnAnalysis/MVA_Analyzer/limits/"+prepreprefix+postfix+"mgl_"+str(mgl)+"_mN_"+str(mN)+"_"+'limits.pkl'
  if os.path.isfile(resFile):
    if overWrite:
      print "Found",resFile,"->overwrite!"
    else:
      print "Found",resFile,"->skip"
      continue

  pklFile = '/data/'+nfsUser+'/nnAnalysis/MVA_Analyzer/'+prefix+'.pkl'
  if not os.path.isfile(pklFile):
    print "Pickle file not found for",mgl, mN, blockStr, pklFile
    continue
  setup=pickle.load(file(pklFile))
  #allModels=getAllInBlock(block, model=model)

  reader = ROOT.TMVA.Reader()  
  #vars={}
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
  nev = data['simu'].GetEntries('osetMgl=='+str(mgl)+'&&osetMN=='+str(mN))
  if nev==0:
    print "No events in dataset for mgl/mN ",mgl, "/",mN
    continue
  from cardFileWriter import cardFileWriter
#  targetBkg=3.
  for methodName in [ 'MLP21']:#, 'myCut']:
    import numpy as np
    from scipy import optimize
#      def getBkgDev(thresh):
#        res= getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0", thresh, 'weightLumi') 
#        print "Optimizing MVA cut for bkg estimation of ",targetBkg,". Testing threshold",thresh,"found bkg exp.:",res
#        return abs(res-targetBkg)
#      x0 = np.array([0.9])
#      optThresh = optimize.fmin(getBkgDev, x0)
    sigInc = lumiFac*getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&osetMgl=="+str(mgl)+"&&osetMN=="+str(mN), -1, weight)
    def getSigEffDev(thresh):
      sig = lumiFac*getYield(data['simu'],  setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&osetMgl=="+str(mgl)+"&&osetMN=="+str(mN), thresh, weight)
      res= sig/float(sigInc) 
      print "Optimizing MVA cut for targetSigEff of ",targetSigEff,". Testing threshold",thresh,"found sig eff.:", res
      return abs(res-targetSigEff)

#    x0 = np.array([0.9])
#    optThresh = optimize.fmin(getSigEffDev, x0)

    if (model=="T1tttt" or model=="T1tttt-madgraph") and mgl<=950 and mN<=400:
      opt = "--rMax 10.0"
    else:
      opt = ""

    def getExpExcl(thresh, retType=None): 
      bkg = lumiFac*getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==0", thresh, weight)
      sig = lumiFac*getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&osetMgl=="+str(mgl)+"&&osetMN=="+str(mN), thresh, weight)

      c = cardFileWriter()
      c.addBin('Bin0', ['bkg'], 'Bin0')
      c.specifyObservation('Bin0', int(bkg))
      c.specifyExpectation('Bin0', 'bkg', bkg)
      c.specifyExpectation('Bin0', 'signal', sig)
      c.addUncertainty('globalUnc', 'lnN')
      c.specifyUncertainty('globalUnc', 'Bin0', 'bkg', 1.2)
      if bkg==0. or sig==0.:
        res={'0.500':float('nan')}
      else:
        res=  c.calcLimit('opt.txt',options=opt)
      print "#########################", methodName, "##################################"
      print "Now at thresh",thresh, "bkg/sig", bkg,"/", sig, 
      print "Results",res
      print "################################################################"
      if not retType:
        return res['0.500']
      else:
        return res

    x0 = np.array([0.9])
    optThresh = optimize.fmin(getExpExcl, x0)

    limits[methodName]={}
    limits["job"] = job
    limits[methodName]['result']=getExpExcl(optThresh[0], retType=1)
    if not limits[methodName]['result']['0.500']<float('inf'):
      limits[methodName]['cutVal']=optThresh[0]
      sigInc = lumiFac*getYield(data['simu'], setup, reader,  allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&osetMgl=="+str(mgl)+"&&osetMN=="+str(mN), -1, weight)
      sig = lumiFac*getYield(data['simu'],    setup, reader,  allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&osetMgl=="+str(mgl)+"&&osetMN=="+str(mN), optThresh[0], weight)
      bkgInc = lumiFac*getYield(data['simu'], setup, reader,  allMethods[methodName]['config'], setup["preselection"]+"&&type==0", -1, weight)
      bkg = lumiFac*getYield(data['simu'],    setup, reader,  allMethods[methodName]['config'], setup["preselection"]+"&&type==0", optThresh[0], weight)
      limits[methodName]['sigEff']=sig/float(sigInc)
      limits[methodName]['bkgEff']=bkg/float(bkgInc)
  pickle.dump(limits, file(resFile, 'w')) 


#cutMin = ROOT.std.vector('float')()
#cutMax = ROOT.std.vector('float')()

#import ctypes
#p_c_double_8 = ctypes.c_double * 8
#cutMin = p_c_double_8()
#cutMax = p_c_double_8()
#
#
#cutMin = array('f', [0. for x in range(8)])
#cutMax = array('f', [0. for x in range(8)])
