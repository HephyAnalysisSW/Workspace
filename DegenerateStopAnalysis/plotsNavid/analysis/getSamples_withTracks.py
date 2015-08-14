import ROOT
from Workspace.HEPHYPythonTools.helpers import getChunks
from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_withTracks import *


target_lumi = 10000

T2DegChunks = getChunks(T2DegStop_300_270)
#WJetsChunks = getChunks(WJetsToLNu_50ns)
WJetsChunks = getChunks(WJetsToLNu)


def getChains(chunks,tree="tree"):
  chain = ROOT.TChain(tree)
  sumWeights = chunks[1]
  for chunk in chunks[0]:
    if chunk.has_key('file'):
      #print chunk['file']
      chain.Add(chunk['file'])
    else:
      print "missing file:", chunk
  return (chain, sumWeights)



T2Deg = getChains(T2DegChunks)
WJets = getChains(WJetsChunks)



sampleDict={
          'W':          {'tree':WJets[0] , 'color':424      ,'lineColor':1  ,'sumWeights':WJets[1] , 'isSignal':0 , 'isData':0   ,'xsec':20508.9*3    },
          "s":       {'tree':T2Deg[0] , 'color':ROOT.kRed  ,'lineColor':1  ,'sumWeights':T2Deg[1] ,  'isSignal':1 , 'isData':0  ,'xsec':8.51615    },
          #'TTs': {'tree':getChain(ttJets['soft'],histname=' 'lineColor':1') ,               'color':1    , 'isSignal':0 , 'isData':0       },            
       }

for samp in sampleDict:
  sampleDict[samp]['weight']= "(%s*%s)"%("genWeight",str(target_lumi*sampleDict[samp]['xsec']/sampleDict[samp]['sumWeights'])) 



