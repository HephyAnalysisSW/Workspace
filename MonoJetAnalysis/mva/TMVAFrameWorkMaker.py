import os,sys,ROOT
from math import sqrt, pi
from localConfig import afsUser, nfsUser, localPlotDir

for path in [os.path.abspath(p) for p in ['../../HEPHYCommonTools/mva', '../../HEPHYCommonTools/cardFileWriter/', '../../HEPHYCommonTools/python/', '../python/']]:
  if not path in sys.path:
      sys.path.insert(1, path)

from nnAnalysisHelpers import getEList, constructDataset, setupMVAFrameWork
from xsec import xsec
from xsecSMS import gluino8TeV_NLONLL, gluino14TeV_NLO
import copy, sys
from defaultConvertedTuples import stop300lsp270, stop200lsp170g100, stop300lsp240g150
from defaultConvertedTuples import wJetsToLNu
from monoJetFuncs import softIsolatedMT 
#RA4

signalModel = stop300lsp270
backgrounds = [wJetsToLNu]

prepreprefix = 'MonoJet_'+signalModel['name']+'_refsel_NormDeco_10000_sigmoid_BP_S03_SE08_'

overWriteData = False 
overWriteTMVAFrameWork = True

setup={}
methodCutOpt={}
methodMLP={}

setup['TMVAFactoryOptions'] = ["!V","!Silent","Color","DrawProgressBar","Transformations=I;D;G,D","AnalysisType=Classification"]

def setupMVAForModelPoint(signalModel):
   
  preprefix = prepreprefix

#  setup['inputVars'] = ["softIsolatedMT", "type1phiMet", 'deltaPhi']
  setup['inputVars'] = ["softIsolatedMT", "type1phiMet"]
#  setup['inputVars'] = ["softIsolatedMT"] #FIXME

  prefix = ''
  for v in setup['inputVars']:
    prefix+=v+'_'
  prefix = preprefix+prefix[:-1]

  setup['dataFile'] = '/data/'+nfsUser+'/MonoJetNNAnalysis/datasets/'+prefix+'.root'
  setup['outputFile'] =     '/data/'+nfsUser+'/MonoJetNNAnalysis/MVA_Analyzer/'+prefix+'.root'
  setup['weightDir'] ='/data/'+nfsUser+'/MonoJetNNAnalysis/MVA_Analyzer/'+prefix+'/'

  if (not overWriteData and ( os.path.isfile(setup['dataFile']))) and (not overWriteTMVAFrameWork and os.path.isfile(setup['outputFile'])):
    return
  
  signal      = ROOT.TChain('Events')
  for b in signalModel['bins']:
    fstring  = signalModel['dirname']+'/'+b+'/*.root'
    signal.Add(fstring)
    entries = signal.GetEntries()
    print "Added bin ",b,"to signal, now,",entries,"entries"
  background  = ROOT.TChain('Events')
  for bkg in backgrounds:
    for b in bkg['bins']:
      background.Add(bkg['dirname']+'/'+b+'/*.root')

  setup['modelVars'] = [] #model parameters to be stored in MVA data file
  setup["sigMVAWeightFac"] = 1. 
  setup["bkgMVAWeightFac"] = 1.
  setup['weightForMVA'] = {'weight':'weight', 'sigFac':1, 'bkgFac':1}
  print "Scaling signal weights by ", setup["sigMVAWeightFac"],'using weight', setup['weightForMVA']

  setup['preselection'] = 'isrJetPt>110&&isrJetBTBVetoPassed&&softIsolatedMuPt>5&&nHardElectrons+nHardMuons==0&&njet60<=2'
  from monoJetFuncs import cosDeltaPhiLepW, softIsolatedMT
  from math import acos
  setup['additionalVars'] = [\
                  ['softIsolatedMT', softIsolatedMT],
                  ['deltaPhi', lambda c:acos(cosDeltaPhiLepW(c))]
    ]


#  setup['fom_plot_vars'] = [['softIsolatedMT', [0,1000] , ROOT.kGreen], ['type1phiMet', [0,1000] , ROOT.kMagenta], ['deltaPhi', [0,1000] , ROOT.kBlue]]
  setup['fom_plot_vars'] = []

  #If changing between met and type1phiMet the formula for deltaPhi (if used) has to be changed!
  setup['varNames'] = ['type1phiMet', 'isrJetPt', 'isrJetBTBVetoPassed', 'softIsolatedMuPt', 'nHardElectrons', 'nHardMuons', 'njet60/I']

  setup['plotDir'] = '/afs/hephy.at/user/'+afsUser[0]+'/'+afsUser+'/www/'+localPlotDir

  methodCutOpt['type']=ROOT.TMVA.Types.kCuts
  methodCutOpt['name']='myCut'
  methodCutOpt['lineColor']=ROOT.kRed
  methodCutOpt['niceName']='cutOptimized'
  methodCutOpt['options'] =('!H','!V','VarTransform=Norm','CreateMVAPdfs=True','FitMethod=GA','EffMethod=EffSel','VarProp=NotEnforced','CutRangeMin=-1','CutRangeMax=-1')

#  addNeurons = [2,1] #FIXME
  addNeurons = [0]
  nn_layers = [len(setup['inputVars'])+ i for i in addNeurons]
  hiddenLayers = ','.join([str(i) for i in nn_layers ])
  methodMLP['type']=ROOT.TMVA.Types.kMLP
  methodMLP['name']='MLP21'
  methodMLP['lineColor']=ROOT.kBlack
  methodMLP['drawStatUncertainty'] = True
  methodMLP['drawInParallelCoord'] = True
  methodMLP['niceName'] = "MLP_{2,1}"

#  methodMLP['options']    = ('!H','!V','VarTransform=Norm,Deco','NeuronType=sigmoid','NCycles=10000','TrainingMethod=BP','LearningRate=0.03', 'DecayRate=0.01','HiddenLayers='+hiddenLayers,'Sampling=0.3','SamplingEpoch=0.8','ConvergenceTests=1','CreateMVAPdfs=True','TestRate=10' )
#  methodMLP['options']    = ('!H','!V','VarTransform=None','NeuronType=sigmoid','NCycles=10000','TrainingMethod=BP','LearningRate=0.03', 'DecayRate=0.01','HiddenLayers='+hiddenLayers,'Sampling=0.3','SamplingEpoch=0.8','ConvergenceTests=1','CreateMVAPdfs=False','TestRate=10' )
  methodMLP['options']    = ('!H','!V','VarTransform=None','NeuronType=sigmoid','NCycles=10','TrainingMethod=BP','LearningRate=0.03', 'DecayRate=0.01','HiddenLayers='+hiddenLayers,'Sampling=0.3','SamplingEpoch=0.8','ConvergenceTests=1','CreateMVAPdfs=False','TestRate=10' )

  data = constructDataset(setup, signal, background, overWriteData)
#  allMethods = [methodMLP, methodCutOpt]
#  allMethods = [methodCutOpt]
  allMethods = [methodMLP]
  setup["methodConfigs"] = copy.deepcopy(allMethods)

  if not os.path.isdir(setup['weightDir']) or overWriteTMVAFrameWork:
    setupMVAFrameWork(setup, data, allMethods, prefix)

  for o in data.values():
   if o:
     o.IsA().Destructor(o)
  del data


setupMVAForModelPoint(signalModel)

