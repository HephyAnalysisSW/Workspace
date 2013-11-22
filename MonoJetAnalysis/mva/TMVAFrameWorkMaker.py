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
from defaultConvertedTuples import stop300lsp270FastSim, stop200lsp170g100FastSim, stop300lsp240g150FastSim
from defaultConvertedTuples import wJetsToLNu
from monoJetFuncs import softIsolatedMT
from helpers import htRatio 
#RA4

signalModel = stop300lsp270FastSim
backgrounds = [wJetsToLNu]

colors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kOrange, ROOT.kMagenta]

overWriteData = True 
overWriteTMVAFrameWork = True

setup={}
methodCutOpt={}
methodMLP={}
methodBDT={}

#setup['TMVAFactoryOptions'] = ["!V","!Silent","Color","DrawProgressBar","Transformations=I;D;G,D","AnalysisType=Classification"]
setup['TMVAFactoryOptions'] = ["!V","!Silent","Color","DrawProgressBar","Transformations=I;D;P;G,D","AnalysisType=Classification"]
setup['plotTransformations'] = ['Id', 'Deco', 'PCA', 'Gauss_Deco']
setup['makeCorrelationScatterPlots'] = False
setup['plotMVAEffs'] = False #needs active X-forwarding since a QT Object is involved
#setup['datasetFactoryOptions'] = ["nTrain_Signal=0", "nTrain_Background=0","SplitMode=Random","SplitSeed=100","NormMode=None","!V"]
setup['datasetFactoryOptions'] = ["nTrain_Signal=0", "nTrain_Background=0","SplitMode=Random","SplitSeed=100","NormMode=None","!V"]
setup['fomPlotZoomCoordinates'] = [0, 0.95, 0.2, 1.0]
convTest=6

VarProp={}
VarProp['deltaPhi']='NotEnforced'
VarProp['softIsolatedMT']='FMin'
VarProp['type1phiMet']='FMin'
VarProp['isrJetPt']='FMin'
VarProp['htRatio']='NotEnforced'
CutRangeMin={}
CutRangeMin['isrJetPt']='110.'
CutRangeMin['htRatio']='0.'
CutRangeMin['deltaPhi']='0.'
CutRangeMin['softIsolatedMT']='0'
CutRangeMin['type1phiMet']='150.'
CutRangeMax={}
CutRangeMax['deltaPhi']='3.1415926'
CutRangeMax['softIsolatedMT']='500'
CutRangeMax['type1phiMet']='500'
CutRangeMax['isrJetPt']='1000.'
CutRangeMax['htRatio']='1.'

addNeurons = [3,3]
shuffleInput = False
nCycles=500
reversed = False
nCuts = -1
maxDepth = 2
nTrees = 400
sigScale = 100
convTest = 20
convImprove = "1e-7"
#for addNeurons in [[2,1]]:
#  for nCycles in [1000]:
#  for nCycles in [20000]:
#    prepreprefix = 'MonoJet_MLP'+''.join([str(x) for x in addNeurons])+'_'+signalModel['name']+'_refsel_Norm_UseRegulator_ConvergenceTests'+str(convTest)+'_ConvImpr1e-6_'+str(nCycles)+'_sigmoid_BP_S1_SE1_'
#for sigScale in [10, 20, 50, 80, 100, 200]:
#for convImprove in ["1e-5", "1e-6", "1e-7", "1e-8", "1e-9"]:
for onlyBkg in ['W1JetsToLNu', 'W2JetsToLNu', 'W3JetsToLNu', 'W4JetsToLNu']:
  prepreprefix = 'MonoJet_BDTvsMLP_'+signalModel['name']+'_convTest'+str(convTest)+'_convImprove'+convImprove+"_"+onlyBkg+"_shuffleInput_"+str(shuffleInput)+"_"
  if reversed:
    prepreprefix+="reversed_"
#    prepreprefix = 'MonoJet_BDT_nTreeComparison_nCuts'+str(nCuts)+'_maxDepth'+str(maxDepth)+'_'+signalModel['name']+'_refsel_None_'
#    prepreprefix = 'MonoJet_BDT_maxDepthComparison_nCuts'+str(nCuts)+'_nTrees'+str(nTrees)+'_'+signalModel['name']+'_refsel_None_'
#    prepreprefix = 'MonoJet_BDT_nEventsMinComparison_maxDepth'+str(maxDepth)+'_nCuts'+str(nCuts)+'_nTrees'+str(nTrees)+'_'+signalModel['name']+'_refsel_None_'

  def setupMVAForModelPoint(signalModel):
     
    preprefix = prepreprefix

#      setup['mvaInputVars'] = ["softIsolatedMT", "type1phiMet", 'deltaPhi', 'isrJetPt', 'htRatio']
    setup['mvaInputVars'] = ["softIsolatedMT", "type1phiMet", 'deltaPhi']
    prefix = '_'.join(setup['mvaInputVars'])
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
#    for bkg in backgrounds:
#      for b in bkg['bins']:
    background.Add(wJetsToLNu['dirname']+'/'+onlyBkg+'/*.root')

    if reversed:
      background, signal = signal, background

    setup['preselection'] = 'isrJetPt>110&&isrJetBTBVetoPassed&&softIsolatedMuPt>5&&nHardElectrons+nHardMuons==0&&njet60<=2&&type1phiMet>150'
    setup['varsFromInputSignal'] = [] #model parameters to be stored in MVA data file
    setup["sigMVAWeightFac"] = 1.#background.GetEntries(setup['preselection'])/float(signal.GetEntries(setup['preselection']))
    setup["bkgMVAWeightFac"] = 1.
#    setup['weightForMVA'] = {'weight':1., 'sigFac':float(sigScale)/100., 'bkgFac':1}
    setup['weightForMVA'] = {'weight':1., 'sigFac':1., 'bkgFac':1}
    #If changing between met and type1phiMet the formula for deltaPhi (if used) has to be changed!
    setup['varsFromInputData'] = ['type1phiMet', 'isrJetPt', 'isrJetBTBVetoPassed', 'softIsolatedMuPt', 'nHardElectrons', 'nHardMuons', 'njet60/I', 'weight', 'isrJetPt']
    from monoJetFuncs import cosDeltaPhiLepW, softIsolatedMT
    from math import acos
    setup['varsCalculated'] = [\
                    ['softIsolatedMT', softIsolatedMT],
                    ['deltaPhi', lambda c:acos(cosDeltaPhiLepW(c))],
                    ['softIsolatedMuCharge/I', lambda c:-c.GetLeaf('softIsolatedMuPdg').GetValue()/abs(c.GetLeaf('softIsolatedMuPdg').GetValue())],
                    ['htRatio', htRatio]
      ]
    print "Scaling signal weights by ", setup["sigMVAWeightFac"],'using weight', setup['weightForMVA']


#      setup['fom_plot_vars'] = [['softIsolatedMT', [0,1000] , ROOT.kGreen], ['type1phiMet', [0,1000] , ROOT.kMagenta], ['deltaPhi', [0,1000] , ROOT.kBlue]]
    setup['fom_plot_vars'] = []

    setup['plotDir']    = '/afs/hephy.at/user/'+afsUser[0]+'/'+afsUser+'/www/'+localPlotDir
    setup['plotSubDir'] = prefix
#    data = constructDataset(setup, signal, background, overWriteData, maxEvents = min([background.GetEntries(setup['preselection']), signal.GetEntries(setup['preselection'])]), shuffleInput = shuffleInput )
    data = constructDataset(setup, signal, background, overWriteData, maxEvents = -1, shuffleInput = shuffleInput )

    methodCutOpt['type']=ROOT.TMVA.Types.kCuts
    methodCutOpt['name']='myCut'
    methodCutOpt['lineColor']=ROOT.kRed
    methodCutOpt['niceName']='cutOptimized'
    methodCutOpt['options'] =('!H','V','VarTransform=None','CreateMVAPdfs=False','FitMethod=SA','EffMethod=EffSel','VarProp=NotEnforced','CutRangeMin[0]=-1','CutRangeMax[0]=-1')
    methodCutOpt['options']+=tuple(["CutRangeMin["+str(i)+"]="+CutRangeMin[v]  for i,v in enumerate(setup['mvaInputVars'])])
    methodCutOpt['options']+=tuple(["CutRangeMax["+str(i)+"]="+CutRangeMax[v]  for i,v in enumerate(setup['mvaInputVars'])])
    methodCutOpt['options']+=tuple(["VarProp["+str(i)+"]="+VarProp[v]  for i,v in enumerate(setup['mvaInputVars'])])

    nn_layers = [len(setup['mvaInputVars'])+ i for i in addNeurons]
    hiddenLayers = ','.join([str(i) for i in nn_layers ])
    methodMLP['type']=ROOT.TMVA.Types.kMLP
    methodMLP['name']='MLP'+"".join([str(x) for x in addNeurons])+"_nCyc"+str(nCycles)
    methodMLP['lineColor']=ROOT.kBlack
    methodMLP['drawStatUncertainty'] = True
    methodMLP['drawInParallelCoord'] = True
    methodMLP['niceName'] = "MLP_{"+",".join([str(i) for i in addNeurons])+"}"

    methodMLP['options']    = ('!H','V','VarTransform=Norm','NeuronType=sigmoid', 'HiddenLayers='+hiddenLayers, 'NCycles='+str(nCycles), 'CreateMVAPdfs=True', 'EpochMonitoring=True', \
                                'TrainingMethod=BP', 'BPMode=sequential', 'LearningRate=0.02', 'DecayRate=0.01', 
#                                  'Sampling=0.3','SamplingEpoch=0.8', 
                                'Sampling=1.','SamplingEpoch=1.', 
                                'ConvergenceTests='+str(convTest),'ConvergenceImprove='+convImprove, 'TestRate=1',
                                'UseRegulator=False' )

    methodBDT['type']=ROOT.TMVA.Types.kBDT
    methodBDT['name']='BDT_nTrees'+str(nTrees)
    methodBDT['lineColor']=colors[i]
    methodBDT['niceName']=methodBDT['name']
    methodBDT['options'] =('!H','V','VarTransform=None', 'CreateMVAPdfs=True', 'BoostType=AdaBoost',\
                           'NTrees='+str(nTrees), 
#                             'nEventsMin=400', 
#                               'MinNodeSize='+str(mNS),
#                               'nEventsMin='+str(mNS),
                           'MaxDepth='+str(maxDepth),
                           'SeparationType=GiniIndex',
                           'nCuts='+str(nCuts),
                           'PruneMethod=NoPruning',
                           'AdaBoostBeta=0.5',
                           'UseRandomisedTrees=False'
    )

    allMethods = [methodMLP, methodBDT]

#     NN_book_options_list.append("!H:!V:NTrees=400:nEventsMin=400:MaxDepth=3:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:PruneMethod=NoPruning")
#     https://svnweb.cern.ch/cern/wsvn/UGentSUSY/trunk/User/Sigamani/babyReaderSTOPS/runBDT/makeconfigs.py
#      allMethods = [methodMLP]


#      for i, nT in enumerate([ 100, 200, 400, 800]):
#        methodBDT['type']=ROOT.TMVA.Types.kBDT
#        methodBDT['name']='BDT_nTrees'+str(nT)
#        methodBDT['lineColor']=colors[i]
#        methodBDT['niceName']=methodBDT['name']
#        methodBDT['options'] =('!H','V','VarTransform=None', 'CreateMVAPdfs=True', 'BoostType=AdaBoost',\
#                               'NTrees='+str(nT), 
#  #                             'nEventsMin=400', 
##                               'MinNodeSize='+str(mNS),
##                               'nEventsMin='+str(mNS),
#                               'MaxDepth='+str(maxDepth),
#                               'SeparationType=GiniIndex',
#                               'nCuts='+str(nCuts),
#                               'PruneMethod=NoPruning',
#                               'AdaBoostBeta=0.5',
#                               'UseRandomisedTrees=True'
#        )
#        allMethods.append(copy.deepcopy(methodBDT))

#      for i, mNS in enumerate([30,  100, 374, 500]):
#        methodBDT['type']=ROOT.TMVA.Types.kBDT
#        methodBDT['name']='BDT_minNodeSize'+str(mNS)
#        methodBDT['lineColor']=colors[i]
#        methodBDT['niceName']=methodBDT['name']
#        methodBDT['options'] =('!H','V','VarTransform=None', 'CreateMVAPdfs=True', 'BoostType=AdaBoost',\
#                               'NTrees='+str(nTrees), 
#  #                             'nEventsMin=400', 
##                               'MinNodeSize='+str(mNS),
#                               'nEventsMin='+str(mNS),
#                               'MaxDepth='+str(maxDepth),
#                               'SeparationType=GiniIndex',
#                               'nCuts='+str(nCuts),
#                               'PruneMethod=NoPruning'
#        )
#        allMethods.append(copy.deepcopy(methodBDT))

#      for i, mD in enumerate([2,3,4,10]):
#        methodBDT['type']=ROOT.TMVA.Types.kBDT
#        methodBDT['name']='BDT_maxDepth'+str(mD)
#        methodBDT['lineColor']=colors[i]
#        methodBDT['niceName']='BDT_maxDepth'+str(mD)
#        methodBDT['options'] =('!H','V','VarTransform=None', 'CreateMVAPdfs=True', 'BoostType=AdaBoost',\
#                               'NTrees='+str(nTrees),
#  #                             'nEventsMin=400', 
#                               'MaxDepth='+str(mD),
#                               'SeparationType=GiniIndex',
#                               'nCuts='+str(nCuts),
#                               'PruneMethod=NoPruning'
#        )
#        allMethods.append(copy.deepcopy(methodBDT))
#

    setup["methodConfigs"] = copy.deepcopy(allMethods)
    if not os.path.isdir(setup['weightDir']) or overWriteTMVAFrameWork:
      setupMVAFrameWork(setup, data, allMethods, prefix)

    for o in data.values():
     if o:
       o.IsA().Destructor(o)
    del data


  setupMVAForModelPoint(signalModel)

