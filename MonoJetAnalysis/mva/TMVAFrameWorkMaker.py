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

prepreprefix = 'MonoJet_Try2_'+signalModel['name']+'_refsel_NormDeco_10000_sigmoid_BP_S03_SE08_'

overWriteData = True 
overWriteTMVAFrameWork = True

setup={}
methodCutOpt={}
methodMLP={}

#setup['TMVAFactoryOptions'] = ["!V","!Silent","Color","DrawProgressBar","Transformations=I;D;G,D","AnalysisType=Classification"]
setup['TMVAFactoryOptions'] = ["!V","!Silent","Color","DrawProgressBar","Transformations=I;D;P;G,D","AnalysisType=Classification"]

VarProp={}
VarProp['deltaPhi']='NotEnforced'
VarProp['softIsolatedMT']='FMin'
VarProp['type1phiMet']='FMin'
CutRangeMin={}
CutRangeMin['deltaPhi']='0.'
CutRangeMin['softIsolatedMT']='0'
CutRangeMin['type1phiMet']='150.'
CutRangeMax={}
CutRangeMax['deltaPhi']='3.1415926'
CutRangeMax['softIsolatedMT']='500'
CutRangeMax['type1phiMet']='500'



def setupMVAForModelPoint(signalModel):
   
  preprefix = prepreprefix

  setup['inputVars'] = ["softIsolatedMT", "type1phiMet", 'deltaPhi']
#  setup['inputVars'] = ["softIsolatedMT", "deltaPhi"]
#  setup['inputVars'] = ["softIsolatedMT"] #FIXME
#  setup['inputVars'] = ["type1phiMet"] #FIXME

  

  prefix = '_'.join(setup['inputVars'])
  prefix = preprefix+prefix

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

  setup['preselection'] = 'isrJetPt>110&&isrJetBTBVetoPassed&&softIsolatedMuPt>5&&nHardElectrons+nHardMuons==0&&njet60<=2&&type1phiMet>150'
  setup['modelVars'] = [] #model parameters to be stored in MVA data file
  setup["sigMVAWeightFac"] = background.GetEntries(setup['preselection'])/float(signal.GetEntries(setup['preselection']))
  setup["bkgMVAWeightFac"] = 1.
  setup['weightForMVA'] = {'weight':1., 'sigFac':1, 'bkgFac':1}
  print "Scaling signal weights by ", setup["sigMVAWeightFac"],'using weight', setup['weightForMVA']

  from monoJetFuncs import cosDeltaPhiLepW, softIsolatedMT
  from math import acos
  setup['additionalVars'] = [\
                  ['softIsolatedMT', softIsolatedMT],
                  ['deltaPhi', lambda c:acos(cosDeltaPhiLepW(c))],
                  ['softIsolatedCharge', lambda c:-c.GetLeaf('softIsolatedMuPdg').GetValue()/abs(c.GetLeaf('softIsolatedMuPdg').GetValue())]
    ]


  setup['fom_plot_vars'] = [['softIsolatedMT', [0,1000] , ROOT.kGreen], ['type1phiMet', [0,1000] , ROOT.kMagenta], ['deltaPhi', [0,1000] , ROOT.kBlue]]
#  setup['fom_plot_vars'] = []

  #If changing between met and type1phiMet the formula for deltaPhi (if used) has to be changed!
  setup['varNames'] = ['type1phiMet', 'isrJetPt', 'isrJetBTBVetoPassed', 'softIsolatedMuPt', 'nHardElectrons', 'nHardMuons', 'njet60/I', 'weight']

  setup['plotDir'] = '/afs/hephy.at/user/'+afsUser[0]+'/'+afsUser+'/www/'+localPlotDir

  methodCutOpt['type']=ROOT.TMVA.Types.kCuts
  methodCutOpt['name']='myCut'
  methodCutOpt['lineColor']=ROOT.kRed
  methodCutOpt['niceName']='cutOptimized'
  methodCutOpt['options'] =('!H','V','VarTransform=None','CreateMVAPdfs=False','FitMethod=SA','EffMethod=EffSel','VarProp=NotEnforced','CutRangeMin[0]=-1','CutRangeMax[0]=-1')
  methodCutOpt['options']+=tuple(["CutRangeMin["+str(i)+"]="+CutRangeMin[v]  for i,v in enumerate(setup['inputVars'])])
  methodCutOpt['options']+=tuple(["CutRangeMax["+str(i)+"]="+CutRangeMax[v]  for i,v in enumerate(setup['inputVars'])])
  methodCutOpt['options']+=tuple(["VarProp["+str(i)+"]="+VarProp[v]  for i,v in enumerate(setup['inputVars'])])
  addNeurons = [2,1]
 
  nn_layers = [len(setup['inputVars'])+ i for i in addNeurons]
  hiddenLayers = ','.join([str(i) for i in nn_layers ])
  methodMLP['type']=ROOT.TMVA.Types.kMLP
  methodMLP['name']='MLP21'
  methodMLP['lineColor']=ROOT.kBlack
  methodMLP['drawStatUncertainty'] = True
  methodMLP['drawInParallelCoord'] = True
  methodMLP['niceName'] = "MLP_{"+",".join([str(i) for i in addNeurons])+"}"

#  methodMLP['options']    = ('!H','!V','VarTransform=Norm,Deco','NeuronType=sigmoid','NCycles=10000','TrainingMethod=BP','LearningRate=0.03', 'DecayRate=0.01','HiddenLayers='+hiddenLayers,'Sampling=0.3','SamplingEpoch=0.8','ConvergenceTests=1','CreateMVAPdfs=True','TestRate=10' )
#  methodMLP['options']    = ('!H','!V','VarTransform=None','NeuronType=sigmoid','NCycles=10000','TrainingMethod=BP','LearningRate=0.03', 'DecayRate=0.01','HiddenLayers='+hiddenLayers,'Sampling=0.3','SamplingEpoch=0.8','ConvergenceTests=1','CreateMVAPdfs=False','TestRate=10' )
  methodMLP['options']    = ('!H','V','VarTransform=Norm,Deco','NeuronType=sigmoid','NCycles=10000','TrainingMethod=BP','LearningRate=0.03', 'DecayRate=0.01','HiddenLayers='+hiddenLayers,'Sampling=0.3','SamplingEpoch=0.8','ConvergenceTests=1','CreateMVAPdfs=True','TestRate=10' )

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

