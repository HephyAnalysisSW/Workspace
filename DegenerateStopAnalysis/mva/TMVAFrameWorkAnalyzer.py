import ROOT
import pickle
from localConfig import afsUser, nfsUser, wwwPlotDir
from array import array
import os, sys, pickle
import ROOT

from Workspace.HEPHYMVATools.mvaHelpers import loadDatasetForTMVA, getYield
prefix = "test_DegenerateStop_BkgMix_met_pt_nBJetMedium25_htJet25_nJet_leptonPt_mT"
setup = pickle.load(file('/data/'+nfsUser+'/DegenerateStop/TMVAAnalyzers/'+prefix+'.pkl'))

readerInstance = ROOT.TMVA.Reader()  
for var in setup['mvaInputObs']:
  var_i  = array('f',[0])
#  vars[var] = var_i
  readerInstance.AddVariable(var,var_i)

data = loadDatasetForTMVA(setup['dataFile'])
assert data, "Could not load dataset from %s"%setup['dataFile']
for m in setup['methodConfigs']:
  readerInstance.BookMVA(m['name'],setup['weightDir']+'/TMVAClassification_'+m['name']+'.weights.xml')

print "\nSome numbers:"
print "Signal yield", getYield(tree=data['tree'], setup=setup,readerInstance=readerInstance,  method=setup['methodConfigs'][0],  cut=setup["preselection"]+"&&type==1&&isTraining==0", nnCutVal=-1, weight="weight")
print "Signal yield disc>0.5:", getYield(tree=data['tree'], setup=setup,readerInstance=readerInstance,  method=setup['methodConfigs'][0],  cut=setup["preselection"]+"&&type==1&&isTraining==0", nnCutVal=0.5, weight="weight")
print "Bkg yield", getYield(tree=data['tree'], setup=setup,readerInstance=readerInstance,  method=setup['methodConfigs'][0],  cut=setup["preselection"]+"&&type==0&&isTraining==0", nnCutVal=-1, weight="weight")
print "Bkg yield disc>0.5:", getYield(tree=data['tree'], setup=setup,readerInstance=readerInstance,  method=setup['methodConfigs'][0],  cut=setup["preselection"]+"&&type==0&&isTraining==0", nnCutVal=0.5, weight="weight")

#    sigInc = lumiFac*getYield(data['simu'], setup, reader, allMethods[methodName]['config'], setup["preselection"]+"&&type==1&&osetMgl=="+str(mgl)+"&&osetMN=="+str(mN), -1, weight)
