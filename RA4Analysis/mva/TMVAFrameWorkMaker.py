import os,sys
from math import sqrt, pi
from localConfig import afsUser, nfsUser, localPlotDir

for path in [os.path.abspath(p) for p in ['../../HEPHYCommonTools/mva', '../../HEPHYCommonTools/cardFileWriter/', '../../HEPHYCommonTools/python/']]:
  if not path in sys.path:
      sys.path.insert(1, path)

from nnAnalysisHelpers import getEList, constructDataset, setupMVAFrameWork
from xsec import xsec
from xsecSMS import gluino8TeV_NLONLL, gluino14TeV_NLO
import copy
import sys

#RA4
from smsHelpers import *
model="T1tttt"
mgl = 1300
mN = 850
sigMVAWeightFac = 1000
prepreprefix = 'RA4_EventShapeVars_sigMVAWeightFac'+str(sigMVAWeightFac)+'_'+model+'_4j_bt1_met100_mt2w0_NormDeco_10000_sigmoid_BP_S03_SE08_'

overWriteData = True
overWriteTMVAFrameWork = True

setup={}
methodCutOpt={}
methodMLP={}

setup['TMVAFactoryOptions'] = ["!V","!Silent","Color","DrawProgressBar","Transformations=I;D;P;G,D","AnalysisType=Classification"]
setup['plotTransformations'] = ['Id', 'Deco', 'PCA', 'Gauss_Deco']
setup['makeCorrelationScatterPlots'] = False
setup['plotMVAEffs'] = False #needs active X-forwarding since a QT Object is involved

def setupMVAForModelPoint(mgl, mN):
   
#  block = getBlock(mgl, mN, model)
#  blockStr = getBlockString(mgl, mN, model)
  blockStr = "mgl_"+str(mgl)+"_mN_"+str(mN)
  preprefix = prepreprefix+blockStr+'_'

  setup['mvaInputVars'] = ["mT", "type1phiMet", "mt2w","nbtags","njets",'minDeltaPhi', 'deltaPhi','thrust']

  prefix = ''
  for v in setup['mvaInputVars']:
    prefix+=v+'_'
  prefix = preprefix+prefix[:-1]

  setup['dataFile'] = '/data/'+nfsUser+'/nnAnalysis/datasets/'+prefix+'.root'
  setup['outputFile'] =     '/data/'+nfsUser+'/nnAnalysis/MVA_Analyzer/'+prefix+'.root'
  setup['weightDir'] ='/data/'+nfsUser+'/nnAnalysis/MVA_Analyzer/'+prefix+'/'

  if (not overWriteData and ( os.path.isfile(setup['dataFile']))) and (not overWriteTMVAFrameWork and os.path.isfile(setup['outputFile'])):
    return
  
  allModelsInBlock = [[mgl, mN]]#getAllInBlock(mgl, mN, model)
#  allModelsInBlock = getAllInBlock(mgl, mN, model)
  signal      = ROOT.TChain('Events')
  counter=0
  oldEntries = 0
  for mgl, mN in reversed(allModelsInBlock):
#    fstringMu  = '/data/adamwo/convertedTuples_v16/copyMET/Mu/'+model+'_'+str(mgl)+'_'+str(mN)+'/histo_'+model+'_'+str(mgl)+'_'+str(mN)+'.root'
#    fstringEle = '/data/adamwo/convertedTuples_v16/copyMET/Ele/'+model+'_'+str(mgl)+'_'+str(mN)+'/histo_'+model+'_'+str(mgl)+'_'+str(mN)+'.root'
    fstringMu  = '/data/schoef/convertedTuples_v21/copyMET/Mu/'+model+'_'+str(mgl)+'_'+str(mN)+'/histo_'+model+'_'+str(mgl)+'_'+str(mN)+'.root'
    fstringEle = '/data/schoef/convertedTuples_v21/copyMET/Ele/'+model+'_'+str(mgl)+'_'+str(mN)+'/histo_'+model+'_'+str(mgl)+'_'+str(mN)+'.root'
    if (os.path.isfile(fstringMu) and os.path.isfile(fstringEle)):
      signal.Add(fstringMu)
      signal.Add(fstringEle)
      entries = signal.GetEntries()
      print "Added",counter, model, mgl, mN
      print entries, oldEntries
      if entries-oldEntries>0: 
        counter+=1
      else: print "Files were empty!",mgl, mN
      oldEntries=entries
      print "Ratio to ref xsec",gluino8TeV_NLONLL[900]/gluino8TeV_NLONLL[mgl]
#      if oldEntries>10000:break
  if counter==0:
    print "No signal points found!"
    return 
  
  setup['weightForMVA'] = {'weight':'weightLumi', 'sigFac':gluino14TeV_NLO[mgl]/gluino8TeV_NLONLL[mgl], 'bkgFac':882.29/225.197}
#  setup["sigMVAWeightFac"] = gluino14TeV_NLO[mgl]/gluino8TeV_NLONLL[mgl]*sigMVAWeightFac #avgRatio/counter 
  setup["sigMVAWeightFac"] = sigMVAWeightFac #avgRatio/counter 
  print "Scaling signal weights by ", setup["sigMVAWeightFac"],'using weight', setup['weightForMVA']

  background  = ROOT.TChain('Events')
  background.Add('/data/schoef/convertedTuples_v21/copyMET/Mu/TTJets-PowHeg/histo_TTJets-PowHeg.root')
  background.Add('/data/schoef/convertedTuples_v21/copyMET/Ele/TTJets-PowHeg/histo_TTJets-PowHeg.root')
  setup["bkgMVAWeightFac"] = 1.

  setup['preselection'] = 'nbtags>=1&&njets>=4 && type1phiMet>=100&&mt2w>0&&ht>=500&&((singleMuonic&&nvetoElectrons==0&&nvetoMuons==1)||(singleElectronic&&nvetoElectrons==1&&nvetoMuons==0))'
  setup['fom_plot_vars'] = [['mT', [0,1000] , ROOT.kGreen], ['type1phiMet', [0,1000] , ROOT.kMagenta], ['mt2w',[0,1000],ROOT.kGreen+4],['nbtags',[0,1000],ROOT.kYellow]]
  #setup['trainingRequ']  = 'Entry$%2'
  #setup['testRequ']      = '(Entry$+1)%2'

  #If changing between met and type1phiMet the formula for deltaPhi (if used) has to be changed!
  setup['varsFromInputData'] = ['type1phiMet', 'mT', 'weightLumi', 'ht', 'singleMuonic', 'singleElectronic', 'nvetoMuons', 'nvetoElectrons', 'mt2w', 'minDeltaPhi', 'thrust']
  setup['varsFromInputSignal'] =  ["osetMN", "osetMgl", "osetMsq"]
  setup['varsFromInputSignal'] =  []
  from mvaFuncs import cosDeltaPhiLepW
  from math import acos
  setup['varsCalculated'] = [\
                ['njets/I', lambda c:int(c.GetLeaf('njets').GetValue())],
                ['nbtags/I', lambda c:int(c.GetLeaf('nbtags').GetValue())],
                ['jet10pt', lambda c:c.GetLeaf('jet0pt').GetValue()/c.GetLeaf('jet1pt').GetValue()],
                ['jet20pt', lambda c:c.GetLeaf('jet0pt').GetValue()/c.GetLeaf('jet2pt').GetValue()],
                ['jet30pt', lambda c:c.GetLeaf('jet0pt').GetValue()/c.GetLeaf('jet3pt').GetValue()],
                ['deltaPhi', lambda c:acos(cosDeltaPhiLepW(c))]
    ]

  setup['plotDir'] = '/afs/hephy.at/user/'+afsUser[0]+'/'+afsUser+'/www/'+localPlotDir
  setup['plotSubDir'] = prefix

  methodCutOpt['type']=ROOT.TMVA.Types.kCuts
  methodCutOpt['name']='myCut'
  methodCutOpt['lineColor']=ROOT.kRed
  methodCutOpt['niceName']='cutOptimized'
  methodCutOpt['options'] =('!H','!V','VarTransform=None','CreateMVAPdfs=True','FitMethod=GA','EffMethod=EffSel','VarProp=NotEnforced','CutRangeMin=-1','CutRangeMax=-1')

  addNeurons = [2,1]
  nn_layers = [len(setup['mvaInputVars'])+ i for i in addNeurons]
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

  data = constructDataset(setup, signal, background, overWriteData)
#  allMethods = [methodMLP, methodCutOpt]
  allMethods = [methodMLP]
  setup["methodConfigs"] = copy.deepcopy(allMethods)

  if not os.path.isdir(setup['weightDir']) or overWriteTMVAFrameWork:
    setupMVAFrameWork(setup, data, allMethods, prefix)

  for o in data.values():
   if o:
     o.IsA().Destructor(o)
  del data

#allBlocks=[{'mD': [mgl-mN, mgl-mN+25], 'mN': [mN, mN+25]}]
#
#start=0
#stop=len(allBlocks)
#
#if len(sys.argv)>=3:
#  allBlocks = getAllBlocks(1600, model=model)
#  allBlocks.sort()
#  allBlocks.reverse()
#  start = int(sys.argv[1])
#  stop = int(sys.argv[2])
#
#print "Looping from ",start,"to",stop, allBlocks[start:stop]

#for b in allBlocks[start:stop] :
#  mgl, mN = getAllInBlock(b)[0]
#  print "Setting up MVA-framework for model ",model, b, mgl, mN

setupMVAForModelPoint(mgl, mN)

