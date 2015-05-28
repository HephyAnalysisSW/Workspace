import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_v3_Phys14V1 import *


TTSample    = getChain(ttJets['none'],histname='') 
T2DegSample = getChain(T2DegStop_300_270['none'],histname='')
#WSample     = getChain(WJetsHTToLNu['none'],histname='')
sampleDict={
          'TTJets':             {'tree':TTSample    , 'color':31          ,'lineColor':1   , 'isSignal':0 , 'isData':0       },
          #'WJets':              {'tree': WSample    , 'color':424         ,'lineColor':1   , 'isSignal':0 , 'isData':0       },
          "T2Deg300_270":       {'tree':T2DegSample , 'color':ROOT.kRed  , 'lineColor':1   , 'isSignal':1 , 'isData':0 },
          #'TTs': {'tree':getChain(ttJets['soft'],histname='') ,               'color':1    , 'isSignal':0 , 'isData':0       },            
       }




