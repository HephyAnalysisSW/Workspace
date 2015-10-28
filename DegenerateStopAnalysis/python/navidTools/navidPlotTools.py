import ROOT
import os
import math
import pickle



from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.navidTools.CutTools import *


def saveCanvas(canv,name,plotDir="./",format=".gif"):
  canv.SaveAs(plotDir+"/"+name+format)

def decorate(hist,color='',width='',histTitle='',fillColor=''):
  if color: hist.SetLineColor(color)
  if width: hist.SetLineWidth(width)
  if histTitle: hist.SetTitle(histTitle)
  if fillColor: hist.SetFillColor(fillColor)
  return

def decorateAxis(hist,xAxisTitle='x title',yAxisTitle='y title',title=''):
  axis = hist.GetXaxis()
  axis.SetTitle(xAxisTitle)
#  axis.SetTitleOffSet(1)
  axis = hist.GetYaxis()
  axis.SetTitle(yAxisTitle)
#  axis.SetTitleOffSet(1)
#  axis.SetTitleFont(62) 
  if title:  hist.SetTitle(title)
  return 


def addToLeg(legend,hist,RMS=1,Mean=1,RMSError=0,MeanError=0,pName=''):
  if RMS:
    rmsString='  RMS={RMS:.2f}'.format(RMS=hist.GetRMS())
    if RMSError: rmsString += ' #pm {0:.2f}'.format(hist.GetRMSError())
  else: rmsString=''
  if Mean:
    meanString='  Mean={MEAN:.2f}'.format(MEAN=hist.GetMean())
    if MeanError: meanString += ' #pm {0:.2f}'.format(hist.GetMeanError())
  else: meanString=''
  if pName: nameString=pName

  else: nameString=hist.GetName()
  legString= nameString + rmsString + meanString
  legend.AddEntry(hist,legString)
  return legend



def getChainFromChunks( samples, treeName):
  c = ROOT.TChain("tree")
  if type(samples)!=type([]):
    sampleList=[0]
    sampleList[0]=samples
  else:
    sampleList=samples
  nTot=0
  for sample in sampleList:
    fList, niTot = getChunks(sample,treeName)
    for f in fList:
      c.Add(f['file'])
    #print fList
    nTot += niTot
    print c.GetEntries(), nTot, niTot
  return c, nTot 

def getChainFromDir( dir, treeName='tree'):
  c=ROOT.TChain(treeName)
  c.Add(dir+"/*.root")
  return c


getAllAlph = lambda str: ''.join(ch for ch in str if ch not in "!>=|<$&@$%[]{}#();'\"")


#getAllAlph = lambda str: ''.join(ch for ch in str if ch not in "Kl13@$%[]{}();'\"")

def getGoodPlotFromChain(c, var, binning,varName='', cutString='(1)', weight='weight', color='', lineWidth='',fillColor='',histTitle='',  binningIsExplicit=False, addOverFlowBin=''): 
  ret=  getPlotFromChain(c, var, binning, cutString=cutString, weight=weight, binningIsExplicit=binningIsExplicit, addOverFlowBin=addOverFlowBin) 
  if not varName:
    varName=getAllAlph(var)
    print varName
  if not histTitle:
    histTitle = varName
  ret.SetTitle(histTitle)
  ret.SetName(varName)
  if color:
    #ret.SetLineColor(color)
    ret.SetLineColor(color)
  if lineWidth:
    ret.SetLineWidth(lineWidth)
  if fillColor:
    ret.SetFillColor(fillColor)
    ret.SetLineColor(ROOT.kBlack)
  return ret

def getStackFromHists(histList):
  stk=ROOT.THStack()
  for h in histList:
    stk.Add(h)
  return stk



def matchListToDictKeys(List,Dict):
  rej=[]
  if not List:
    List=Dict.keys()
  else:
    if type(List)==type([]) or  type(List)==type(()):
      pass
    else:
      List=List.rsplit()
    for l in List:
      if l not in Dict.keys():
        print "WARNING: Item \' %s \' will be ignored because it is not found in the dictionary keys:"%(l) , Dict.keys()
        rej.append(l)
        List.pop(List.index(l))
  return List



def getPlots(sampleDict,plotDict,treeList='',varList='',cutList=''):
  """Use: getPlots(sampleDict,plotDict,treeList='',varList='',cutList=''):"""
  treeList  = matchListToDictKeys(treeList,sampleDict)
  varList   = matchListToDictKeys(varList,plotDict)
  
  print treeList
  print varList
  for s in treeList:
    if sampleDict[s].has_key("weight") and sampleDict[s]["weight"]:
      weight = str(sampleDict[s]["weight"])
      print "For sample %s, using weight in sampleDict, weight= %s"%(s,weight) 
    else: weight="weight"
    if not sampleDict[s].has_key('plots'):
      sampleDict[s]['plots']={}
    for p in varList:
      lineWidth=plotDict[p]['lineWidth']
      if plotDict[p]['color'] == type("") and plotDict[p]['color'].lower()=="fill" and not sampleDict[s]['isSignal']:
        #color = ROOT.kBlack
        color = sampleDict[s]['color']
        fcolor = sampleDict[s]['color']
      else:
        color  = sampleDict[s]['color']
        fcolor = 0 
        if sampleDict[s]['isSignal']:
          lineWidth=2
      if cutList:
        if type(cutList)==type(()) or type(cutList)==type([]):
          cutString=cutList[1]
          cutName=cutList[0]
          plotName = "%s_%s"%(p,cutName)
          if not plotDict.has_key(plotName):
            plotDict[plotName]=plotDict[p].copy()
            plotDict[plotName]['cut']=cutString
            plotDict[plotName]['presel']="(1)"
          title = plotDict[p]['title'].replace("{SAMPLE}",s).replace("{CUT}",cutName)
          print "*******************************************"
          print title 
          #plotDict[plotName]['title']= title 
          print "Using cut %s : %s"%(cutName,cutString)
        else:
          cutString=cutList
          cutName=getAllAlph(cutList)
          print "Using cut %s : %s "%(cutName,cutString)
          print "Try using cutList=[cutName,cutString] as an input"
          plotName = "%s_%s"%(p,cutName)
          title = plotName
      else:
        cutString="(%s) && (%s)"%(plotDict[p]['presel'],plotDict[p]['cut'])
        cutName=getAllAlpha(cutString)
        print "Using default cut values for var. cut:  %s"%(cutString)
        plotName=p
        title = plotName
      print "Sample:" , s , "Getting Plot: ", p, "with cut:  " , cutName
      sampleDict[s]['plots'][plotName] = getGoodPlotFromChain(sampleDict[s]['tree'] , plotDict[p]['var'], plotDict[p]['bin'],\
                                                       varName     = p  ,
                                                       histTitle   = title, 
                                                       cutString   = cutString, 
                                                       color       = color,
                                                       fillColor   = fcolor,
                                                       lineWidth   = lineWidth,
                                                       weight      = weight
                                                       #weight      = str(sampleDict[s]['weight'])
                                                       )
  return

def getBkgSigStacks(sampleDict, plotDict, varList='',treeList=''):
  """Get stacks for signal and backgrounds. make vars in varlist are available in sampleDict. no stacks for 2d histograms.   """
  treeList  = matchListToDictKeys(treeList,sampleDict)
  varList   = matchListToDictKeys(varList,plotDict)
  #treeList=sampleDict.keys()
  #varList=plotDict.keys()
  #sampleDict=sampleDict
  bkgStackDict={}
  sigStackDict={}
  for v in varList:
    if len(plotDict[v]['bin'])!=6:
      bkgStackDict[v]=getStackFromHists([ sampleDict[t]['plots'][v] for t in treeList if not sampleDict[t]['isSignal']])
      sigStackDict[v]=getStackFromHists([ sampleDict[t]['plots'][v] for t in treeList if sampleDict[t]['isSignal']])
  return (bkgStackDict,sigStackDict)

def drawPlots(sampleDict,plotDict,varList='',treeList='',plotDir='',dOpt=""):
  treeList  = matchListToDictKeys(treeList,sampleDict)
  varList   = matchListToDictKeys(varList,plotDict)

  bkgStackDict, sigStackDict =  getBkgSigStacks(sampleDict,plotDict, varList=varList,treeList=treeList)
  for v in varList:
    if len(plotDict[v]['bin'])!=6:
      c1=ROOT.TCanvas("c1","c1")
      bkgStackDict[v].Draw()
      bkgStackDict[v].SetMinimum(1)
      sigStackDict[v].Draw("samenostack")
      decorateAxis(bkgStackDict[v],xAxisTitle=plotDict[v]['xLabel'],yAxisTitle=plotDict[v]['yLabel'])
    #plotDict[v]['yAxis']
      c1.SetLogy(plotDict[v]['yLog'])
      c1.SetLogx(plotDict[v]['xLog'])
      c1.Update()
      saveCanvas(c1,v,plotDir=plotDir)
      saveCanvas(c1,v,plotDir=plotDir+"/pdf/",format=".pdf")  
      saveCanvas(c1,v,plotDir=plotDir+"/root/",format=".root")
      
      del c1
    ### 2D plots:
    elif len(plotDict[v]['bin'])==6:
      for t in treeList:
        c1=ROOT.TCanvas("c1","c1")
        #sampleDict[t]['plots'][v].SetTitle(t+"_"+plotDict[v]['title'])
        
        sampleDict[t]['plots'][v].Draw("colz%s"%dOpt)
        decorateAxis(sampleDict[t]['plots'][v],xAxisTitle=plotDict[v]['xLabel'],yAxisTitle=plotDict[v]['yLabel'])
        c1.SetLogx(plotDict[v]['xLog'])
        c1.SetLogy(plotDict[v]['yLog'])
        c1.SetLogz(plotDict[v]['zLog'])
        saveCanvas(c1,v+"_"+t,plotDir=plotDir)
        saveCanvas(c1,v+"_"+t,plotDir=plotDir+"/pdf/",format=".pdf")
        saveCanvas(c1,v+"_"+t,plotDir=plotDir+"/root/",format=".root")
        del c1



###############################################################################
###############################################################################
###############################################################################
###############################################################################


addSquareSum = lambda x: math.sqrt(sum(( e**2 for e in x   )))



def setEventListToChain(tree,cut,eListName="",verbose=True):
  if not eListName:
    print "WARNING: Using Default eList Name, this could be dangerous!"
    eListName="eList"
  if verbose: print "Setting EventList to Chain: ", tree, "Reducing the raw nEvents from ", tree.GetEntries(), " to ",
  tree.SetEventList(0)
  tree.Draw(">>%s"%eListName,cut)
  eList = getattr(ROOT,eListName)
  tree.SetEventList(eList )
  if verbose: print eList.GetN()
  assert eList.GetN() == tree.GetEventList().GetN()
  del eList

def setEventListToChains(sampleDict,treeList,cutInst,verbose=True):
  if cutInst:
    if isinstance(cutInst,CutClass):
      cutName   = cutInst.name
      cutString = cutInst.combined
    else:
      cutName, cutString = cutInst
    if verbose:
      print "Setting eventlists using cut:"
      print cutName, cutString


    for tree in treeList:
      eListName="eList_%s_%s"%(tree,cutName)
      setEventListToChain(sampleDict[tree]['tree'],cutString,eListName=eListName,verbose=False)
      if verbose:
        print "     Sample:", tree,   "Reducing the raw nEvents from ", sampleDict[tree]['tree'].GetEntries(), " to ", sampleDict[tree]['tree'].GetEventList().GetN()

  else:
    print "no cut... no EventList was set to trees"  


def decorHist(title='',x='',y="",color='',width='',fillColor=''):
  def decorateFunc(h):
    if color: h.SetLineColor(color)
    if width: h.SetLineWidth(width)
    if title: h.SetTitle(title)
    if fillColor: h.SetFillColor(fillColor)
    if x : h.GetXaxis().SetTitle(x)
    if y : h.GetYaxis().SetTitle(y)
  return decorateFunc


def decorCanv(xlog=0,ylog=0,zlog=0):
  def decorateFunc(canv):
    if xlog: canv.SetLogx(xlog)
    if ylog: canv.SetLogy(zlog)
    if zlog: canv.SetLogz(ylog)
  return decorateFunc

 
