import ROOT
import os,sys,pickle,copy
from math import sqrt, pi
from localConfig import afsUser, nfsUser, wwwPlotDir

from Workspace.HEPHYMVATools.mvaHelpers import loadDatasetForTMVA, setupMVAFrameWork

#RA4
#from smsHelpers import *

overWriteTMVAFrameWork = True

setup={}
methodCutOpt={}
methodMLP={}

prefix = 'test_DegenerateStop_BkgMix'
setup = pickle.load(file('/data/schoef/DegenerateStop/datasets/'+prefix+'.pkl'))

setup['TMVAFactoryOptions'] = ["!V","!Silent","Color","DrawProgressBar","Transformations=I;D;P;G,D","AnalysisType=Classification"]
setup['plotTransformations'] = ['Id', 'Deco', 'PCA', 'Gauss_Deco']
setup['makeCorrelationScatterPlots'] = False
setup['plotMVAEffs'] = False #needs active X-forwarding since a QT Object is involved

setup['fomPlotZoomCoordinates'] = [0, 0.95, 0.2, 1.0]
setup['mvaInputObs'] = ['met_pt', 'nBJetMedium25', 'htJet25', 'nJet', 'leptonPt']

obsPrefix = '_'.join(setup['mvaInputObs'])

setup['TMVAOutputFile'] = '/data/'+nfsUser+'/DegenerateStop/TMVAAnalyzers/'+prefix+'.root'
setup['weightDir'] = '/data/'+nfsUser+'/DegenerateStop/TMVAAnalyzers/'+prefix+'/'+obsPrefix+'/'

data = loadDatasetForTMVA(setup['dataFile'])
assert data, "Could not load dataset from %s"%setup['dataFile']

if data and (overWriteTMVAFrameWork or not os.path.isfile(setup['TMVAOutputFile'])):
  setup['fom_plot_vars'] = []#[['mT', [0,1000] , ROOT.kGreen], ['type1phiMet', [0,1000] , ROOT.kMagenta], ['mt2w',[0,1000],ROOT.kGreen+4],['nbtags',[0,1000],ROOT.kYellow]]

  setup['plotDir'] = '/afs/hephy.at/user/'+afsUser[0]+'/'+afsUser+'/www/'+wwwPlotDir
  setup['plotSubDir'] = prefix

  methodCutOpt['type']=ROOT.TMVA.Types.kCuts
  methodCutOpt['name']='myCut'
  methodCutOpt['lineColor']=ROOT.kRed
  methodCutOpt['niceName']='cutOptimized'
  methodCutOpt['options'] =('!H','!V','VarTransform=None','CreateMVAPdfs=True','FitMethod=GA','EffMethod=EffSel','VarProp=NotEnforced','CutRangeMin=-1','CutRangeMax=-1')

  addNeurons = [2,1]
  nn_layers = [len(setup['mvaInputObs'])+ i for i in addNeurons]
  hiddenLayers = ','.join([str(i) for i in nn_layers ])
  methodMLP['type']=ROOT.TMVA.Types.kMLP
  methodMLP['name']='MLP21'
  methodMLP['lineColor']=ROOT.kBlack
  methodMLP['drawStatUncertainty'] = True
  methodMLP['drawInParallelCoord'] = True
  methodMLP['niceName'] = "MLP_{2,1}"
  #methodMLP['options']    = ('!H','!V','VarTransform=Deco','NeuronType=sigmoid','NCycles=5000','TrainingMethod=BP','LearningRate=0.03','DecayRate=0.01','HiddenLayers='+hiddenLayers,'Sampling=0.3','SamplingEpoch=5000','SamplingTraining=True','SamplingTesting=False','ConvergenceTests=0','CreateMVAPdfs=True','TestRate=10')
#  methodMLP['options']    = ('!H','!V','VarTransform=Norm,Deco','NeuronType=sigmoid','NCycles=5000','TrainingMethod=BFGS','LearningRate=0.02', 'DecayRate=0.01','HiddenLayers='+hiddenLayers,'Sampling=1','SamplingEpoch=1','ConvergenceTests=1','CreateMVAPdfs=True','TestRate=10' )
  methodMLP['options']    = ('!H','!V','VarTransform=Norm,Deco','NeuronType=sigmoid','NCycles=10000','TrainingMethod=BP','LearningRate=0.03', 'DecayRate=0.01','HiddenLayers='+hiddenLayers,'Sampling=0.3','SamplingEpoch=0.8','ConvergenceTests=1','CreateMVAPdfs=True','TestRate=10' )

#  allMethods = [methodMLP, methodCutOpt]
  allMethods = [methodMLP]
  setup["methodConfigs"] = copy.deepcopy(allMethods)

  if not os.path.isdir(setup['weightDir']) or overWriteTMVAFrameWork:
    setupMVAFrameWork(setup, data, allMethods, prefix)

  for o in data.values():
   if o:
     o.IsA().Destructor(o)
  del data


