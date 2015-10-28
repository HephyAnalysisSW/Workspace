import Workspace.DegenerateStopAnalysis.cuts as cuts
from Workspace.HEPHYPythonTools.helpers import getYieldFromChain
from Workspace.DegenerateStopAnalysis.navidTools.CutTools import  CutClass
from Workspace.DegenerateStopAnalysis.navidTools.FOM import calcFOMs
import imp
import pickle
import numpy as np





def getYieldsFromCutFlow(tree,cut_class,weight="(weight)",opt="flow"):
  #if not isinstance(cut_class,cutClass):
  #  raise Exception("use an instance of cutClass")
  if opt.lower()=="flow": flowOpt="flow"
  if opt.lower()=="inclflow": flowOpt="inclFlow"
  yields=[]
  cutflow = getattr(cut_class,flowOpt)
  for cut in cutflow:
    yields.append ( (cut[0], getYieldFromChain(tree,cut[1],weight)) )
  return yields



def getYieldsFromCutFlow(trees,cut_class,weight="(weight)",opt="flow"):
  if opt.lower()=="flow": flowOpt="flow"
  if opt.lower()=="inclflow": flowOpt="inclFlow"

  yields=[ ("CUT",[tree for tree in trees]) ]
  cutflow = getattr(cut_class,flowOpt)
  for iCut, cut in enumerate(cutflow):
    yields.append( (cut[0],[] ))
    for tree in trees:
      yields[iCut+1][1].append ( getYieldFromChain(tree,cut[1],weight) )
  return yields




#class Yields():
#  def __init__(self,sampleDict,treeList,cutInst,tableName='{cut}',cutOpt="flow",weight="(weight)",pklOpt=False,pklDir="./pkl/",nDigits=2):
#    if not isinstance(cutInst,CutClass):
#      raise Exception("use an instance of cutClass")
#    self.nDigits    = nDigits
#    self.sampleDict = sampleDict
#    self.treeList   = treeList
#    self.treeList.sort(key = lambda x: sampleDict[x]['isSignal'])
#    self.cutInst    = cutInst
#    self.weight     = weight
#    self.tableName  = tableName.format(cut=self.cutInst.name)
#    self.cutList    = getattr(cutInst,cutOpt)
#    self.sampleLegend     = [ [" "] + [sampleDict[tree]['name'] for tree in treeList ]]
#    self.sampleLegendTot  = [ [" "] + [sampleDict[tree]['name'] for tree in treeList ]]
#    for iTree, tree in enumerate(self.treeList):
#      if sampleDict[tree]['isSignal']: 
#        self.iBkg = iTree+1
#        self.sampleLegendTot[0].insert(iTree+1,"Total")
#        break
#    self.getYields()
#    self.pklOpt = pklOpt
#    if self.pklOpt:
#      self.pickle(pklOpt,pklDir)
#  def getYields(self):
#    self.rawYields     = [ [cut[0]   ] for cut in self.cutList  ]
#    self.bkgTot     = [ [cut[0],0   ] for cut in self.cutList  ]
#    self.sigTot     = [ [cut[0]   ] for cut in self.cutList  ]
#    for ic, cut in enumerate(self.cutList):
#      for tree in self.treeList:
#        yld = round(getYieldFromChain(self.sampleDict[tree]['tree'], cut[1],self.weight),self.nDigits) 
#        self.rawYields[ic].append( yld )
#        if not self.sampleDict[tree]['isSignal']:
#          self.bkgTot[ic][1]+=yld
#    self.yields= [x for x in self.rawYields]
#    for ic, cut in enumerate(self.cutList):
#       self.yields[ic][self.iBkg]=self.bkgTot[ic][1]
#       pass 
#    self.table= np.array(self.sampleLegendTot+self.yields)
#    self.yields = np.array(self.yields)
#    self.rawTable = tuple(self.sampleLegend+ self.rawYields)
#    self.npYields = np.array(self.rawYields)
#    self.npTable  = np.array(self.rawTable)
#  def pickle(self,pklOpt,pklDir):
#    if self.pklOpt==1:
#      pickle.dump(self,open("YieldInstance_%s.pkl"%self.tableName,"wb"))
#    if self.pklOpt==2:
#      pickle.dump(self.rawTable,open("YieldTable_%s.pkl"%self.tableName,"wb"))
#    if self.pklOpt==3:
#      pickle.dump(self.rawTable,open("YieldTable_%s.pkl"%self.tableName,"wb"))
#      pickle.dump(self,open("YieldInstance_%s.pkl"%self.tableName,"wb"))









class Yields():
  def __init__(self,sampleDict,treeList,cutInst,cutOpt='flow',tableName='{cut}',weight="(weight)",pklOpt=False,pklDir="./pkl/",nDigits=2):
    if not isinstance(cutInst,CutClass):
      raise Exception("use an instance of cutClass")
    self.nDigits    = nDigits
    self.sampleDict = sampleDict
    self.cutInst    = cutInst
    self.weight     = weight
    self.tableName  = tableName.format(cut=self.cutInst.name)
    self.treeList   = treeList
    self.treeList.sort(key = lambda x: sampleDict[x]['isSignal'])
    self.bkgList    = [tree for tree in treeList if not sampleDict[tree]['isSignal']]
    self.sigList    = [tree for tree in treeList if tree not in self.bkgList]

    self.cutList    = getattr(cutInst,cutOpt)

    self.cutLegend =   np.array( [[""]+[cut[0] for cut in self.cutList]])
    self.sampleLegend =np.array( [ [sampleDict[tree]['name'] for tree in self.bkgList] + ["Total"] + 
                                 [sampleDict[tree]['name'] for tree in self.sigList] ] )


    self.yieldDictRaw = { tree:[ ] for tree in treeList}

    self.getYields()
    self.pklOpt = pklOpt
    self.pklDir = pklDir +"/"
    if self.pklOpt:
      self.pickle(self.pklOpt,self.pklDir)

  def getYields(self):
    for ic, cut in enumerate(self.cutList):
      for tree in self.treeList:
        yld = round(getYieldFromChain(self.sampleDict[tree]['tree'], cut[1],self.weight),self.nDigits) 
        self.yieldDictRaw[tree].append(yld)
    self.yieldDictRaw['Total']  = [sum(x) for x in zip(*[self.yieldDictRaw[tree] for tree in self.bkgList])]

    self.yieldDict={}
    for tree in self.treeList:
      self.yieldDict[tree]      = np.array([self.sampleDict[tree]['name']] +self.yieldDictRaw[tree],dtype='|S8')
    self.yieldDict["Total"]     = np.array(["Total"]+ self.yieldDictRaw['Total'],dtype='|S8')
    sig = self.sigList[0] #### need to fix for multiple signals
    self.yieldDict["FOM"]       = np.array(["FOM"]+ [ round(calcFOMs(self.yieldDictRaw[sig][ic] , self.yieldDictRaw["Total"][ic] ,0.2,"AMSSYS" ),2 )
                                                     for ic, cut in enumerate(self.cutList) ] , dtype='|S8')

    self.yields = np.concatenate( [ [self.yieldDict[t]] for t in self.bkgList +['Total'] + self.sigList ] )
    self.table  = np.concatenate( [ self.cutLegend , self.yields ] )
    self.FOM = np.concatenate( [ [self.yieldDict[t]] for t in self.bkgList +['Total'] + self.sigList + ['FOM'] ] )
    self.FOMTable = np.concatenate( [ self.cutLegend , self.FOM ] )
  def pickle(self,pklOpt,pklDir):
    if self.pklOpt==1:
      pickle.dump(self,open(pklDir+"YieldInstance_%s.pkl"%self.tableName,"wb"))
      print "Yield Instance pickled in  %s"%"YieldInstance_%s.pkl"%self.tableName
    if self.pklOpt==2:
      pickle.dump(self.table,open(pklDir+"YieldTable_%s.pkl"%self.tableName,"wb"))
      print "Yield Table pickled in  %s"%"YieldTable_%s.pkl"%self.tableName
    if self.pklOpt==3:
      pickle.dump(self.table,open(pklDir+"YieldTable_%s.pkl"%self.tableName,"wb"))
      pickle.dump(self,open(pklDir+"YieldInstance_%s.pkl"%self.tableName,"wb"))
      print "Yield Instance pickled in  %s"%"YieldInstance_%s.pkl"%self.tableName
      print "Yield Table pickled in  %s"%"YieldTable_%s.pkl"%self.tableName









if __name__=='__main__':
  from Workspace.DegenerateStopAnalysis.navidTools.CutTools import *
  from Workspace.DegenerateStopAnalysis.cuts import *
  from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_Spring15 import *

  y=Yields(sampleDict,['tt', 'w','s'],cuts.presel,tableName='{cut}_test',pklOpt=1);
