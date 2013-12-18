import os,sys,ROOT,pickle
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

colors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kOrange, ROOT.kMagenta]

overWriteTMVAFrameWork = True

#methodCutOpt={}
methodMLP={}
methodBDT={}

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
nCycles=500
nCuts = -1
maxDepth = 1
nTrees = 400

convTest = 20
convImprove = "1e-7"

#comparison = "nTree"
#comparison = "maxDepth"
#comparison = "nEventsMin"
allVars = ["softIsolatedMT", "type1phiMet",'deltaPhi', 'isrJetPt', 'softIsolatedMuPt', 'softIsolatedMuEta', 'softIsolatedMuCharge', 'ht', 'njet' ]
#for omit in range(len(allVars)):
#  selectedVars = allVars[0:omit] + allVars[omit+1:] 
if True:
  selectedVars = allVars
  for comparison in ['nTree', 'maxDepth', 'nEventsMin']:
    for seed in range(1):
    #  datasetName =   'MonoJet_stop300lsp270FastSim_BkgMix_'+str(seed)
      datasetName =   'MonoJet_stopDeltaM30FastSim_BkgMix_'+str(seed)
      datasetFile =   '/data/'+nfsUser+'/MonoJetNNAnalysis/datasets/'+datasetName
    #  prepreprefix = datasetName+'_nTrees'+str(nTrees)+"_nCuts_"+str(nCuts)+"_maxDepth"+str(maxDepth)+"_nEventsMinComparison_"
      prepreprefix = datasetName+'_nTrees'+str(nTrees)+"_nCuts_"+str(nCuts)+"_maxDepth_"+str(maxDepth)+"_"+comparison+"Comparison_"

      preprefix = prepreprefix
      setup = pickle.load(file(datasetFile+'.pkl'))

      setup['datasetFactoryOptions'] = ["NormMode=None","V"]
      setup['TMVAFactoryOptions'] = ["!V","!Silent","Color","DrawProgressBar","Transformations=I;D;P;G,D","AnalysisType=Classification"]
      setup['plotTransformations'] = ['Id', 'Deco', 'PCA', 'Gauss_Deco']
      setup['makeCorrelationScatterPlots'] = False
      setup['plotMVAEffs'] = False #needs active X-forwarding since a QT Object is involved
      setup['fomPlotZoomCoordinates'] = [0, 0.95, 0.2, 1.0]

    #      setup['mvaInputVars'] = ["softIsolatedMT", "type1phiMet", 'deltaPhi', 'isrJetPt', 'htRatio']
    #  setup['mvaInputVars'] = ["softIsolatedMT", "type1phiMet", 'deltaPhi']
      setup['mvaInputVars'] = selectedVars 
      prefix = '_'.join(setup['mvaInputVars'])
      prefix = preprefix+prefix

      setup['TMVAOutputFile'] =     '/data/'+nfsUser+'/MonoJetNNAnalysis/MVA_Analyzer/'+prefix+'.root'
      setup['weightDir'] ='/data/'+nfsUser+'/MonoJetNNAnalysis/MVA_Analyzer/'+prefix+'/'

      data = constructDataset(setup, None, None, False)
      if not data:
        print "Could not load dataset -> do nothing"
      if data and (overWriteTMVAFrameWork or not os.path.isfile(setup['TMVAOutputFile'])):
      #      setup['fom_plot_vars'] = [['softIsolatedMT', [0,1000] , ROOT.kGreen], ['type1phiMet', [0,1000] , ROOT.kMagenta], ['deltaPhi', [0,1000] , ROOT.kBlue]]
        setup['fom_plot_vars'] = []

        setup['plotDir']    = '/afs/hephy.at/user/'+afsUser[0]+'/'+afsUser+'/www/'+localPlotDir
        setup['plotSubDir'] = prefix
      #    data = constructDataset(setup, signal, background, overWriteData, maxEvents = min([background.GetEntries(setup['preselection']), signal.GetEntries(setup['preselection'])]), shuffleInput = shuffleInput )

    #    methodCutOpt['type']=ROOT.TMVA.Types.kCuts
    #    methodCutOpt['name']='myCut'
    #    methodCutOpt['lineColor']=ROOT.kRed
    #    methodCutOpt['niceName']='cutOptimized'
    #    methodCutOpt['options'] =('!H','V','VarTransform=None','CreateMVAPdfs=False','FitMethod=SA','EffMethod=EffSel','VarProp=NotEnforced','CutRangeMin[0]=-1','CutRangeMax[0]=-1')
    #    methodCutOpt['options']+=tuple(["CutRangeMin["+str(i)+"]="+CutRangeMin[v]  for i,v in enumerate(setup['mvaInputVars'])])
    #    methodCutOpt['options']+=tuple(["CutRangeMax["+str(i)+"]="+CutRangeMax[v]  for i,v in enumerate(setup['mvaInputVars'])])
    #    methodCutOpt['options']+=tuple(["VarProp["+str(i)+"]="+VarProp[v]  for i,v in enumerate(setup['mvaInputVars'])])
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

    #    methodBDT['type']=ROOT.TMVA.Types.kBDT
    #    methodBDT['name']='BDT_nTrees'+str(nTrees)
    #    methodBDT['lineColor']=colors[i]
    #    methodBDT['niceName']=methodBDT['name']
    #    methodBDT['options'] =('!H','V','VarTransform=None', 'CreateMVAPdfs=True', 'BoostType=AdaBoost',\
    #                           'NTrees='+str(nTrees), 
    #  #                             'nEventsMin=400', 
    #  #                               'MinNodeSize='+str(mNS),
    #  #                               'nEventsMin='+str(mNS),
    #                           'MaxDepth='+str(maxDepth),
    #                           'SeparationType=GiniIndex',
    #                           'nCuts='+str(nCuts),
    #                           'PruneMethod=NoPruning',
    #                           'AdaBoostBeta=0.5',
    #                           'UseRandomisedTrees=False'
    #    )

    #    allMethods = [methodMLP, methodBDT]

      #     NN_book_options_list.append("!H:!V:NTrees=400:nEventsMin=400:MaxDepth=3:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:PruneMethod=NoPruning")
      #     https://svnweb.cern.ch/cern/wsvn/UGentSUSY/trunk/User/Sigamani/babyReaderSTOPS/runBDT/makeconfigs.py

        if comparison=="nTree":
          allMethods = [methodMLP]
          for i, nT in enumerate([ 100, 200, 400, 800, 1000]):
           methodBDT['type']=ROOT.TMVA.Types.kBDT
           methodBDT['name']='BDT_nTrees'+str(nT)
           methodBDT['lineColor']=colors[i]
           methodBDT['niceName']=methodBDT['name']
           methodBDT['options'] =('!H','V','VarTransform=None', 'CreateMVAPdfs=True', 'BoostType=AdaBoost',\
                                  'NTrees='+str(nT), 
      #                            'nEventsMin='+str(mNS),
                                  'MaxDepth='+str(maxDepth),
                                  'SeparationType=GiniIndex',
                                  'nCuts='+str(nCuts),
                                  'PruneMethod=NoPruning',
                                  'AdaBoostBeta=0.5',
                                  'UseRandomisedTrees=False'
           )
           allMethods.append(copy.deepcopy(methodBDT))

        if comparison=="nEventsMin":
          allMethods = [methodMLP]
          defNEventsMin = int(max(40, data['simu'].GetEntries('isTraining==1')/(float(len(setup['mvaInputVars']))**2)/10.))
          nEventsMinVals = list(set([10,30,40,100,300]+[defNEventsMin]))
          nEventsMinVals.sort()
          for i, nEventsMin in enumerate(nEventsMinVals):
            methodBDT['type']=ROOT.TMVA.Types.kBDT
            methodBDT['name']='BDT_nEventsMin'+str(nEventsMin)
            methodBDT['lineColor']=colors[i]
            methodBDT['niceName']='BDT_nEventsMin'+str(nEventsMin)
            methodBDT['options'] =('!H','V','VarTransform=None', 'CreateMVAPdfs=True', 'BoostType=AdaBoost',\
                                   'NTrees='+str(nTrees),
                                   'nEventsMin='+str(nEventsMin), 
                                   'MaxDepth='+str(maxDepth),
                                   'SeparationType=GiniIndex',
                                   'nCuts='+str(nCuts),
                                   'PruneMethod=NoPruning'
            )
            allMethods.append(copy.deepcopy(methodBDT))
        if comparison=="maxDepth":
          allMethods = [methodMLP]
          for i, mD in enumerate([1,2,3,4,10]):
            methodBDT['type']=ROOT.TMVA.Types.kBDT
            methodBDT['name']='BDT_maxDepth'+str(mD)
            methodBDT['lineColor']=colors[i]
            methodBDT['niceName']='BDT_maxDepth'+str(mD)
            methodBDT['options'] =('!H','V','VarTransform=None', 'CreateMVAPdfs=True', 'BoostType=AdaBoost',\
                                   'NTrees='+str(nTrees),
      #                              'nEventsMin=400', 
                                   'MaxDepth='+str(mD),
                                   'SeparationType=GiniIndex',
                                   'nCuts='+str(nCuts),
                                   'PruneMethod=NoPruning'
            )
            allMethods.append(copy.deepcopy(methodBDT))
      

        setup["methodConfigs"] = copy.deepcopy(allMethods)
        if not os.path.isdir(setup['weightDir']) or overWriteTMVAFrameWork:
          setupMVAFrameWork(setup, data, allMethods, prefix)

        for o in data.values():
         if o:
           o.IsA().Destructor(o)
        del data
