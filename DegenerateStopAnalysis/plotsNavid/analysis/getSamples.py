import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_Spring15_soft import *


TTSample    = getChain(TTJets['soft'],histname='') 
T2DegSample = getChain(T2DegStop_300_270['soft'],histname='')
WSample     = getChain(WJets['soft'],histname='')
sampleDict={
          'TTJets':             {'tree':TTSample    , 'color':31          ,'lineColor':1   , 'isSignal':0 , 'isData':0       },
          'WJets':              {'tree': WSample    , 'color':424         ,'lineColor':1   , 'isSignal':0 , 'isData':0       },
          "T2Deg300_270":       {'tree':T2DegSample , 'color':ROOT.kRed  , 'lineColor':1   , 'isSignal':1 , 'isData':0 },
          #'TTs': {'tree':getChain(ttJets['soft'],histname='') ,               'color':1    , 'isSignal':0 , 'isData':0       },            
       }




