import ROOT
import os
import math
import pickle
import numpy as np


from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.navidTools.CutTools import *
from Workspace.DegenerateStopAnalysis.navidTools.getRatioPlot import *
#from Workspace.DegenerateStopAnalysis.navidTools.FOM import *
execfile('../../../python/navidTools/FOM.py')



cmsbase = os.getenv("CMSSW_BASE")
print "CMSBASE", cmsbase
ROOT.gROOT.LoadMacro(cmsbase+"/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
#ROOT.setTDRStyle()
maxN = -1
ROOT.gStyle.SetOptStat(0)




#############################################################################################################
##########################################                    ###############################################
##########################################    ETC  TOOLS      ###############################################
##########################################                    ###############################################
#############################################################################################################


getAllAlph = lambda str: ''.join(ch for ch in str if ch not in "!>=|<$&@$%[]{}#(); '\"")
addSquareSum = lambda x: math.sqrt(sum(( e**2 for e in x   )))


def saveCanvas(canv,name,plotDir="./",format=".gif"):
  canv.SaveAs(plotDir+"/"+name+format)

class Dict(dict):
  def __init__(self,*arg,**kw):
      super(Dict, self).__init__(*arg, **kw)
      self.__dict__ = self

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


#############################################################################################################
##########################################                    ###############################################
##########################################    EVENT LISTS     ###############################################
##########################################                    ###############################################
#############################################################################################################


def getEventListFromFile(eListName,tmpDir=None,opt="read"):
  if opt.lower() in ["read","r"]:
    eListPath="%s/%s.root"%(tmpDir,eListName)
    f=ROOT.TFile(eListPath,"open") 
    eList = f.Get(eListName)
    eList.SetDirectory(0) 
  return eList

def getEventListFromChain(sample,cut,eListName="",tmpDir="./",opt="write"):
  if not eListName or eListName.lower()=="elist" : 
    print "WARNING: Using Default eList Name, this could be dangerous! eList name should be customized by the sample name and cut" 
    eListName="eList" 
  sample.SetEventList(0) 
  sample.Draw(">>%s"%eListName,cut) 
  eList=ROOT.gDirectory.Get(eListName)
  if opt.lower() in ["write", "w", "save", "s" ]:
    eListPath="%s/%s.root"%(tmpDir,eListName)
    print "EventList saved in: %s"%eListPath
    f = ROOT.TFile(eListPath,"recreate")
    eList.Write()
    f.Close()
  return eList

def setEventListToChain(sample,cut,eListName="",verbose=True,tmpDir=None,opt="read"): 
  if not tmpDir:
    tmpDir = os.getenv("CMSSW_BASE")+"/src/Workspace/DegenerateStopAnalysis/plotsNavid/tmp/"
  eListPath="%s/%s.root"%(tmpDir,eListName)
  if opt.lower() in ["read","r"]: 
    if os.path.isfile(eListPath):
      eList = getEventListFromFile(eListName=eListName,tmpDir=tmpDir,opt=opt)
    else:
      print "eList was not found in:%s "%eListPath
      opt="write"
  if opt.lower() in ["make","m","write", "w","s","save"] : 
    if True: print "Creating EList", eListName 
    eList = getEventListFromChain(sample,cut,eListName,tmpDir=tmpDir,opt=opt)
  if verbose: print "Setting EventList to Chain: ", sample, "Reducing the raw nEvents from ", sample.GetEntries(), " to ", 
  sample.SetEventList(eList) 
  assert eList.GetN() == sample.GetEventList().GetN() 
  return eList

def setEventListToChains(sampleDict,sampleList,cutInst,verbose=True,opt="read"):
  if cutInst:
    if isinstance(cutInst,CutClass):
      cutName   = cutInst.name
      cutString = cutInst.combined
    else:
      cutName, cutString = cutInst
    if verbose:
      print "Setting eventlists using cut:"
      print cutName, cutString
    for sample in sampleList:
      eListName="eList_%s_%s"%(sample,cutName)
      setEventListToChain(sampleDict[sample]['tree'],cutString,eListName=eListName,verbose=False,opt=opt)
      if verbose:
        if sampleDict[sample]['tree'].GetEventList():
          print "     Sample:", sample,   "Reducing the raw nEvents from ", sampleDict[sample]['tree'].GetEntries(), " to ", sampleDict[sample]['tree'].GetEventList().GetN()
        else:
          print "FAILED Setting EventList to Sample", sample, sampleDict[sample]['tree'].GetEventList() 
  else:
    print "no cut... no EventList was set to samples" 





#############################################################################################################
##########################################                    ###############################################
##########################################    DECORATOION     ###############################################
##########################################                    ###############################################
#############################################################################################################


def decorHist(samp,cut,hist,decorDict):
    dd=decorDict
    if dd.has_key("title"):
        title = dd['title']
        title = title.format(CUT=cut.name, SAMP=samp.name )
        hist.SetName(getAllAlph(dd["title"]))
        hist.SetTitle(title)
    if dd.has_key("color") and dd['color']:
        hist.SetLineColor(dd['color'])
    elif not samp.isData and not samp.isSignal:
        hist.SetFillColor(samp['color'])
        hist.SetLineColor(ROOT.kBlack)
    elif samp.isSignal:
        hist.SetLineWidth(2)
        hist.SetLineColor(samp['color'])
    else:
        print "default color used for:", samp, cut, hist, decorDict
    if dd.has_key("x") and dd['x']:
        hist.GetXaxis().SetTitle(dd['x'])
    if dd.has_key("y") and dd['y']:
        hist.GetYaxis().SetTitle(dd['y'])


def decorate(hist,color='',width='',histTitle='',fillColor=''):
  if color: hist.SetLineColor(color)
  if width: hist.SetLineWidth(width)
  if histTitle: hist.SetTitle(histTitle)
  if fillColor: hist.SetFillColor(fillColor)
  return

def decorAxis(hist, axis,t="",tSize="",tFont="",tOffset="",lFont="",lSize="",func=""):
    if axis.lower() not in ['x','y','z']: assert False
    axis = getattr(hist,"Get%saxis"%axis.upper() )()
    if t: axis.SetTitle(t)
    if tSize  : axis.SetTitleSize(tSize)
    if tFont  : axis.SetTitleFont(tFont)
    if tOffset: axis.SetTitleOffset(tOffset)
    if lFont  : axis.SetLabelFont(lFont)
    if lSize  : axis.SetLabelSize(lSize)
    if func   : func(axis)




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



#############################################################################################################
##########################################                    ###############################################
##########################################    GET AND DRAW    ###############################################
##########################################  Chains and Plots  ###############################################
##########################################                    ###############################################
#############################################################################################################



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
  return ret

def getStackFromHists(histList,sName=None,scale=None):
  if sName:
    stk=ROOT.THStack(sName,sName)
  else:
    stk=ROOT.THStack()
  for h in histList:
    if scale:
      h.Scale(scale)
    stk.Add(h)
  return stk

def getSamplePlots(samples,plots,cut,sampleList=[],plotList=[]):
    bkgList=[samp for samp in sampleList if not samples[samp]['isSignal'] ]
    sigList=[samp for samp in sampleList if samples[samp]['isSignal'] ]
    if not sampleList: sampleList= samples.keys()
    if not plotList: plotList=plots.keys()
    hists={}
    for samp in sampleList:
        hists[samp]={}
        for p in plotList:
            v = p
            hists[samp][v]= samples[samp]['cuts'][cut.name][v]
    return hists







def getBkgSigStacks(samples, plots, cut, sampleList=[],plotList=[]):
    """Get stacks for signal and backgrounds. make vars in varlist are available in samples. no stacks for 2d histograms.     """
    sampleList    = matchListToDictKeys(sampleList,samples)
    plotList     = matchListToDictKeys(plotList,plots)
    #sampleList=samples.keys()
    #plotList=plots.keys()
    #samples=samples
    bkgStackDict={}
    sigStackDict={}
    dataStackDict={}
    for v in plotList:
        if len(plots[v]['bins'])!=6:
            bkgStackDict[v]=getStackFromHists([ samples[samp]['cuts'][cut.name][v] for samp in sampleList if not samples[samp]['isSignal']])
            sigStackDict[v]=getStackFromHists([ samples[samp]['cuts'][cut.name][v] for samp in sampleList if samples[samp]['isSignal']])
            dataStackDict[v]=getStackFromHists([ samples[samp]['cuts'][cut.name][v] for samp in sampleList if samples[samp]['isData']])
    return {'bkg': bkgStackDict,'sig': sigStackDict, 'data': dataStackDict}



  
def getPlot(sample,plot,cut,weight="(weight)", nMinus1="",cutStr="",addOverFlowBin=''):
  c   = sample.tree
  var = plot.var
  if nMinus1:
    cutString = cut.nMinus1(nMinus1)
  else:
    cutString = cut.combined
  if cutStr:
    cutString += "&&(%s)"%cutStr

  if weight:
    w = weight
  else:
    print "No Weight is being applied"
    w = "(1)"
  hist = getPlotFromChain(sample.tree,plot.var,plot.bins,cutString,weight=w, addOverFlowBin=addOverFlowBin)
  #plot.decorHistFunc(p)
  decorHist(sample,cut,hist,plot.decor) 
  plotName=plot.name + "_"+ cut.name
  sample.plots[plotName]=hist
  if not sample.has_key("cuts"):
    sample.cuts=Dict()
  if not sample.cuts.has_key(cut.name):
    sample.cuts[cut.name]=Dict()
  sample.cuts[cut.name][plot.name]=hist



def getPlotsSimple(samples,plots,cut):
  for sample in samples.itervalues():
    for plot in plots.itervalues():
      getPlot(sample,plot,cut)


def getPlots(samples,plots,cut,sampleList=[],plotList=[],weight="(weight)",nMinus1="", addOverFlowBin='',verbose=True):
    if verbose:print "Getting Plots: "
    for sample in samples.iterkeys():
        #if sample in sampleList or not sampleList:
        if not sample in sampleList:
            continue

        if verbose: print "  Sample:" , samples[sample].name, 



        if samples[sample].has_key("weight"):
            weight_str = samples[sample]['weight']
        elif weight.endswith("_weight"):
            if samples[sample].has_key(weight):
                weight_str = samples[sample][weight]         
                #print sample, weight_str, samples[sample]
            elif samples[sample].isData:
                weight_str = "(1)"
            else:
                print "not sure what weight to use!", sample, weight_str,    samples[sample]
                assert False
                #w = "(weight)"
            #if verbose: print "     Sample: %s, weight: %s"%(sample,weight_str)
        else:
            weight_str = weight
        if verbose: print "  Using Weight: %s"%(weight_str)
        plotList = plotList if plotList else plots.keys()
        for plot in plotList:
            if plot not in plots.keys():
                print "Ignoring %s .... not in the Plot Dictionary"%plot
                continue    
            
            cutStr = plots[plot]['cut']  if plots[plot].has_key("cut") and plots[plot]['cut'] else ''
            if cutStr: print "        ---applying cutString:", cutStr
            
            if verbose: print " "*15, plot
            if nMinus1:
                nMinus1String = plots[p]["nMinus1"] if plots[plot].has_key("nMinus1") else nMinus1
            else: nMinus1String=""
            getPlot(samples[sample],plots[plot],cut,weight=weight_str,nMinus1=nMinus1String,cutStr=cutStr,addOverFlowBin=addOverFlowBin)


def drawPlots_basic(samples,plots):
  canv=ROOT.TCanvas()
  for plot in plots.itervalues():
    drawOpt=""
    for sample in samples.itervalues():
      sample.plots[plot.name].Draw(drawOpt)
      drawOpt="same"
  return canv

          



def drawPlots(samples,plots,cut,sampleList=['s','w'],plotList=[],plotMin=False,logy=0,save=True,fom=True,ratioDenom=None, ratioNorm=True, leg=True,unity=True):
    ret = {}
    canvs={}
    hists   = getSamplePlots(samples,plots,cut,sampleList=sampleList, plotList=plotList)
    stacks  = getBkgSigStacks(samples,plots,cut, sampleList=sampleList, plotList=plotList )
    ret.update({'canv':canvs}   )
    ret.update({'stacks':stacks})
    sigList=[samp for samp in sampleList if samples[samp]['isSignal'] ]
    bkgList=[samp for samp in sampleList if not samples[samp]['isSignal']  and not samples[samp]['isData'] ]
    fomHists={}
    for p in plots.iterkeys():
        if plotList and p not in plotList:
            continue
        if plots[p]['is2d']:
            print "2D plots not supported:" , p
            continue
        if fom:
            canvs[p]=makeCanvasPads(c1Name="c_%s"%p,c1ww=800,c1wh=800, p1Name="p1_%s"%p, p2Name="p2_%s"%p)
            cSave , cMain=0,1   # index of the main canvas and the canvas to be saved
        else: 
            canvs[p] = ROOT.TCanvas(p,p,800,800), None, None
            cSave , cMain=0,0
        canvs[p][cMain].cd()
        dOpt="hist"
        if len(bkgList):
            refStack=stacks['bkg'][p]
            stacks['bkg'][p].Draw(dOpt)
            #if logy: canvs[p][cMain].SetLogy(logy)
            dOpt="same"
        else:
            refStack = stacks['sig'][p]
        stacks['sig'][p].Draw("%s nostack"%dOpt.replace("hist",""))
        if plots[p].has_key("decor"):
            if plots[p]['decor'].has_key("y") : decorAxis( refStack, 'y', plots[p]['decor']['y'], tOffset=1 )
            if plots[p]['decor'].has_key("title") :refStack.SetTitle(plots[p]['decor']['title'] ) 
            if plots[p]['decor'].has_key("log"):
                logx, logy, logz = plots[p]['decor']['log']
                if logx : canvs[p][cMain].SetLogx(1)
                if logy : canvs[p][cMain].SetLogy(1)
        if plotMin: refStack.SetMinimum( plotMin )



        if leg:
            leg = ROOT.TLegend(0.6,0.7,0.9,0.9)
            ret.update({'leg':leg})
            for bkg in bkgList:
                leg.AddEntry(hists[bkg][p], samples[bkg].name , "f")    
            for sig in sigList:
                leg.AddEntry(hists[sig][p], samples[sig].name , "l")    
            leg.Draw()
        if fom:
            fomFunc = fom if type(fom)==type('') else "AMSSYS"
            fomMax = 0
            fomMin = 999
            canvs[p][2].cd()
            fomHists[p]={}
            ret.update({'fomHist':fomHists})
            if "ratio" in fomFunc.lower():
                if ratioDenom:
                    fomHists[p]['denom']=hists[ratioDenom][p]
            else:
                fomHists[p]['denom']=ROOT.TH1F()
                fomHists[p]['denom'].SetTitle("stack_%s"%p)
                fomHists[p]['denom'].SetName("stack_%s"%p)
                fomHists[p]['denom'].Merge( stacks['bkg'][p].GetHists() )
            #refStack.SetMaximum(getHistMax(fomHists[p]['denom'])[1]*1.3)
            nBins  = fomHists[p]['denom'].GetNbinsX()
            lowBin = fomHists[p]['denom'].GetBinLowEdge(1)
            hiBin  = fomHists[p]['denom'].GetBinLowEdge(fomHists[p]['denom'].GetNbinsX()+1)
            dOpt=""
            for sig in sigList:
                sigHist= samples[sig]['cuts'][cut.name][p]
                fomHists[p][sig] = getFOMFromTH1FIntegral(sigHist, fomHists[p]['denom'] ,fom=fomFunc, verbose =False)
                if ratioNorm:
                    fomHists[p][sig].Scale(1./fomHists[p][sig].Integral() ) 
                fomHists[p][sig].SetLineWidth(2)
                fomHists[p][sig].Draw(dOpt)
                fomMax = max(getHistMax(fomHists[p][sig])[1] ,fomMax)
                newMin = getHistMin(fomHists[p][sig],onlyPos=True)[1]
                fomMin = min( newMin ,fomMin)
                print newMin, fomMin

                if dOpt!="same":
                    print p, sig , fomHists[p][sig].GetYaxis().GetTitleSize()
                    first_sig = sig
                    decorAxis( fomHists[p][sig], 'x', tSize=0.1   ,  lSize=0.1)
                    decorAxis( fomHists[p][sig], 'y', t='%s  '%fomFunc   , tOffset=0.5 ,  tSize=0.1,lSize=0.1, func= lambda axis: axis.SetNdivisions(506) )
                    fomHists[p][sig].SetTitle("")
                    if unity:
                        Func = ROOT.TF1('Func',"[0]",lowBin,hiBin)
                        Func.SetParameter(0,1)
                        #Func.SetLineStyle(3)
                        Func.SetLineColor(1)
                        Func.SetLineWidth(1)
                        Func.Draw("same")
                        ret.update({'func':Func})
                    dOpt="same"
            print 'fom min max', fomMin, fomMax
            print "first sig", first_sig
            fomHists[p][first_sig].SetMaximum(fomMax*(1.2) )
            fomHists[p][first_sig].SetMinimum(fomMin*(0.8) )
            fomHists[p][first_sig].Draw("same")
            canvs[p][2].Update()

        if save:
            saveDir = save + "/%s/"%cut.name if type(save)==type('') else "./"
            #saveDir = save + "/%s/"%cut.name
            if not os.path.isdir(saveDir): os.mkdir(saveDir) 
            canvs[p][cSave].SaveAs(saveDir+"/%s.png"%p)
    return ret



def draw2DPlots(samples,plots,cut,sampleList=['s','w'],plotList=[],min=False,logy=0,logx=0,save=True, leg=True, fom=False):
    ret = {}
    canvs={}
    hists   = getSamplePlots(samples,plots,cut,sampleList=sampleList, plotList=plotList)
    stacks  = getBkgSigStacks(samples,plots,cut, sampleList=sampleList, plotList=plotList )
    ret.update({'canv':canvs})
    sigList=[samp for samp in sampleList if samples[samp]['isSignal'] ]
    bkgList=[samp for samp in sampleList if not samples[samp]['isSignal']  and not samples[samp]['isData'] ]
    fomHists={}
    for p in plots.iterkeys():
        if plotList and p not in plotList:
            continue
        if plots[p]['is1d']:
            print "For 1D plot use drawPlots()  :" , p
            continue
        if fom:
            pass
        for samp in sigList + bkgList:
            plotName = p+"_"+samp
            plotTitle = p+"_"+samples[samp]['name']
            print plotName
            canvs[plotName] = ROOT.TCanvas(plotName, plotName,800,800)
            cSave , cMain=0,0  # index of the main canvas and the canvas to be saved
            canvs[plotName].cd()
            hists[samp][p].Draw("COLZ")
            if logy: canvs[plotName].SetLogy(logy)
            if plots[p].has_key("decor"):
                decorHist( samples[samp], cut, hists[samp][p] , plots[p]['decor'] )
                if plots[p]['decor'].has_key("log"):
                    logx, logy, logz = plots[p]['decor']['log']
                    if logx : canvs[plotName].SetLogx(1)    
                    if logy : canvs[plotName].SetLogy(1)    
                    if logz : canvs[plotName].SetLogz(1)    

                #if plots[p]['decor'].has_key("y") : decorAxis( hists[samp][p], 'y', plots[p]['decor']['y'], tOffset=1 )
                #if plots[p]['decor'].has_key("title") : hists[samp][p].SetTitle(plots[p]['decor']['title'] ) 
            if leg:
                leg = ROOT.TLegend(0.6,0.7,0.9,0.9)
                ret.update({'leg':leg})
                for bkg in bkgList:
                    leg.AddEntry(hists[bkg][p], samples[bkg].name , "f")    
                for sig in sigList:
                    leg.AddEntry(hists[sig][p], samples[sig].name , "l")    
                leg.Draw()
            if save:
                saveDir = save + "/%s/"%cut.name if type(save)==type('') else "./"
                if not os.path.isdir(saveDir): os.mkdir(saveDir) 
                canvs[plotName].SaveAs(saveDir+"/%s.png"%plotTitle)
    return ret


def getAndDraw(samples,plots,cut,sampleList=['s','w'],plotList=[],weight="weight", min=False,logy=0,save=True,fom=True, leg=True,unity=True):
    getPlots(samples,plots,cut,sampleList,plotList,weight=weight,nMinus1="",verbose=True)
    plotList2D = [p for p in plots if p['is2d'] ]
    plotList1D = [p for p in plots if p['is1d'] ] 


def getAndDrawPlot(samples,plots, cut, name, sampleList=['s','w'], plotList=[],  weight="weight",nMinus1='',min=False,logy=0,fom="AMSSYS",fomOpt=True,save=False):

    bkgList=sampleList 
    getPlots( samples, plots, cut, sampleList=sampleList, plotList=plotList, weight=weight, nMinus1=nMinus1, verbose=True)
    stacks = getBkgSigStacks( samples, plots, cut, pltoList=plotList)
    bkgHists={}
    for plot in plotList:
        pass
    for bkg in bkgList:
        bkgHists[bkg]={}
        bkgHistName= bkg+"_"+name
        bkgHists[bkg]['name']=bkgHistName
        bkgTree=samples[bkg].tree
        if hasattr(ROOT,bkgHistName) and getattr(ROOT,bkgHistName):
            hist=getattr(ROOT,bkgHistName)
            #print hist, "already exist, will try to delete it!"
            #hist.IsA().Destructor(hist)
            del hist
        bkgTree.Draw(var+">>hTmp%s"%(binning) ,  "(%s)*(%s)"%(weight,cut), "goff")
        bkgHists[bkg]['hist'] = ROOT.hTmp.Clone(bkgHistName)
        del ROOT.hTmp
        bkgHists[bkg]['hist'].SetFillColor(bkgHists[bkg]['hist'].GetLineColor())
        bkgHists[bkg]['hist'].SetLineColor(1)
        bkgHists[bkg]['hist'].SetTitle(name)
    bkgStack = getStackFromHists( [bkgHists[bkg]['hist'] for bkg in bkgList] )
    bkgStack.SetTitle(name)
    
    sigHistName="s_%s"%name
    samples.s.tree.Draw(var+">>hTmp2%s"%(binning), "(%s)*(%s)"%(weight,cut), "goff")
    sigHist = ROOT.hTmp2.Clone(sigHistName)
    del ROOT.hTmp2

    nBins  = sigHist.GetNbinsX()
    lowBin = sigHist.GetBinLowEdge(1)
    hiBin  = sigHist.GetBinLowEdge(sigHist.GetNbinsX()+1)

    stackHist=ROOT.TH1F("stack_hist","stack_hist",nBins,lowBin,hiBin)
    stackHist.Merge(bkgStack.GetHists())

    if min:
        bkgStack.SetMinimum(min)
    ret.update({'sHist':sigHist, 'bkgHists':bkgHists, "bkgStack":bkgStack, "stackHist":stackHist } )

    if fom:
        c1,p1,p2 = makeCanvasPads("%s"%name,800,800)
        p2.cd()

        if str(fom)  == "ratio": 
            ratio = getRatio(sigHist,stackHist,normalize=True, min=0.01,max=2.0)
            for bkg in bkgList:
                bkgHists[bkg]['ratio'] = getRatio(sigHist, bkgHists[bkg]['hist'] ,normalize=True, min=0.01,max=2.0)
                bkgHists[bkg]['ratio'].SetName("%s_%s"%(bkg,fom))
        else:
            ratio=getFOMFromTH1FIntegral(sigHist,stackHist,fom=fom)
            for bkg in bkgList:
                bkgHists[bkg]['ratio'] = getFOMFromTH1FIntegral(sigHist, bkgHists[bkg]['hist'], fom=fom )
                bkgHists[bkg]['ratio'].SetName("%s_%s"%(bkg,fom))
        dOpt=''
        if not fomOpt:
            for bkg in bkgList:
                bkgHists[bkg]['ratio'].SetLineColor( bkgHists[bkg]['hist'].GetFillColor() )
                bkgHists[bkg]['ratio'].SetLineWidth(2)

                if not dOpt:
                    firstHist = bkgHists[bkg]['ratio']
                bkgHists[bkg]['ratio'].Draw(dOpt)
                dOpt="same"
        else:
            firstHist = ratio
            ratio.SetTitle(name)
            ratio.Draw(dOpt)

        firstHist.SetStats(0)
        x = firstHist.GetXaxis()
        x.SetTitleSize(20)
        x.SetTitleFont(43)
        x.SetTitleOffset(4.0)
        x.SetLabelFont(43)
        x.SetLabelSize(15)
        y = firstHist.GetYaxis()
        y.SetTitle(fom)
        y.SetNdivisions(505)
        y.SetTitleSize(20)
        y.SetTitleFont(43)
        y.SetTitleOffset(1)
        y.SetLabelFont(43)
        y.SetLabelSize(15)
               
 
        ratio.SetLineColor(ROOT.kSpring+4)
        ratio.SetMarkerColor(ROOT.kSpring+4)
        ratio.SetLineWidth(2)
        if "ratio" in fom.lower():
          ratio.SetMinimum(0)
          ratio.SetMaximum(2)
        else:
          ratio.SetMinimum(0.5)
          ratio.SetMaximum(2)
        print "getting ratio"
        Func = ROOT.TF1('Func',"[0]",sigHist.GetBinLowEdge(1),sigHist.GetBinLowEdge( sigHist.GetNbinsX()+1) )
        Func.SetParameter(0,1)
        Func.SetLineColor(ROOT.kRed)
        Func.Draw('same')
        c1.Update()
        p1.Update()
        ret.update({'ratio':ratio, 'canv': (c1,p1,p2), 'func':Func } )
    else:
        p1 = ROOT.TCanvas(name,name,600,600)
        ret.update({'canv': (p1) } )
        #bkgHist.Draw("hist")
        #sigHist.Draw("same")
    p1.cd()

    bkgStack.Draw("hist")
    bkgStack.GetYaxis().SetTitle("nEvents")
    sigHist.Draw("same")
    if logy:
        p1.SetLogy(1)
    if save:
        if fom:
            c1.SaveAs(save+"/%s.png"%name)
        else:
            p1.SaveAs(save+"/%s.png"%name)
    return ret 





def getAndDrawQuickPlots(samples,var,bins=[],varName='',cut="(1)",weight="weight", sampleList=['s','w'],min=False,logy=0,save=True,fom=True, leg=True,unity=True):
    ret = {}
    canv = ROOT.TCanvas(varName,varName,800,800)
    ####### Getting Plots
    ret['hists']={}
    ret.update({'canv':canv })
    bkgList = [samp for samp in samples if samp in sampleList and not samples[samp].isSignal and not samples[samp].isData]
    sigList = [samp for samp in samples if samp in sampleList and samples[samp].isSignal and not samples[samp].isData]

    print bkgList, sigList

    if leg:
        leg = ROOT.TLegend(0.6,0.7,0.9,0.9)
        ret.update({'leg':leg})
    for sampKey in samples:
        if sampKey not in sampleList:
            continue
        samp = samples[sampKey]
        if weight:
            if samp.has_key("weight"):
                weightStr=samp['weight']
            else:
                weightStr=weight
        else:
            weightStr = "(1)"
        if sampKey in sigList:
            ret['hists'][sampKey]=getGoodPlotFromChain(samp.tree, var, binning = bins, varName=varName, cutString=cut, weight=weightStr, color = samp.color, lineWidth=2 )
        if sampKey in bkgList:
            ret['hists'][sampKey]=getGoodPlotFromChain(samp.tree, var, binning = bins, varName=varName, cutString=cut, weight=weightStr, color = 1, fillColor = samp.color )


    bkgStack  = getStackFromHists([ ret['hists'][x] for x in bkgList ],sName="stack_bkg",scale=None)
    sigStack  = getStackFromHists([ ret['hists'][x] for x in sigList ],sName="stack_sig",scale=None)
    stacks = {'bkg':bkgStack, 'sig':sigStack}
    ret.update({'stacks':stacks})

    bkgStack.SetTitle(varName)
    bkgStack.Draw("hist")
    sigStack.Draw("noStack same")
    if leg:
        for sampKey in bkgList + sigList:
          if sampKey in bkgList:
              legOpt = "f"
          if sampKey in sigList:
              legOpt = "l"
          leg.AddEntry(ret['hists'][sampKey] , samples[sampKey].name , legOpt)    
        leg.Draw()



    if min: bkgStack.SetMinimum(min) 
    if logy: canv.SetLogy(1)
    if save: 
        saveDir = save if type(save)==type('') else "./"
        print saveDir
        canv.SaveAs(saveDir+'/%s.png'%varName)
    return ret
    

    #fomHists={}
    #for p in plots.iterkeys():
    #    if plotList and p not in plotList:
    #        continue
    #    if fom:
    #        canvs[p]=makeCanvasPads(c1Name="c_%s"%p,c1ww=800,c1wh=800, p1Name="p1_%s"%p, p2Name="p2_%s"%p)
    #        cSave , cMain=0,1   # index of the main canvas and the canvas to be saved
    #    else: 
    #        canvs[p] = ROOT.TCanvas(p,p,800,800), None, None
    #        cSave , cMain=0,0
    #    canvs[p][cMain].cd()
    #    stacks['bkg']
    #    stacks['bkg'][p].Draw("hist")
    #    if min: stacks['bkg'][p].SetMinimum(min)
    #    if logy: canvs[p][cMain].SetLogy(logy)
    #    stacks['sig'][p].Draw("same hist nostack")
    #    if plots[p].has_key("decor"):
    #        if plots[p]['decor'].has_key("y") : decorAxis( stacks['bkg'][p], 'y', plots[p]['decor']['y'], tOffset=1 )
    #        if plots[p]['decor'].has_key("title") :stacks['bkg'][p].SetTitle(plots[p]['decor']['title'] ) 
    #    if leg:
    #        leg = ROOT.TLegend(0.6,0.7,0.9,0.9)
    #        ret.update({'leg':leg})
    #        for bkg in bkgList:
    #            leg.AddEntry(hists[bkg][p], samples[bkg].name , "f")    
    #        for sig in sigList:
    #            leg.AddEntry(hists[sig][p], samples[sig].name , "l")    
    #        leg.Draw()
    #    if fom:
    #        fomMax = 0
    #        canvs[p][2].cd()
    #        fomHists[p]={}
    #        ret.update({'fomHist':fomHists})
    #        nBins  = hists[bkgList[0]][p].GetNbinsX()
    #        lowBin = hists[bkgList[0]][p].GetBinLowEdge(1)
    #        hiBin  = hists[bkgList[0]][p].GetBinLowEdge(hists[bkgList[0]][p].GetNbinsX()+1)
    #        fomHists[p]['denom']=ROOT.TH1F("stack_%s"%p,"stack_%s"%p,nBins,lowBin,hiBin)
    #        fomHists[p]['denom'].Merge( stacks['bkg'][p].GetHists() )
    #        dOpt=""
    #        for sig in sigList:
    #            sigHist= samples[sig]['cuts'][cut.name][p]
    #            fomHists[p][sig] = getFOMFromTH1FIntegral(sigHist, fomHists[p]['denom'] )
    #            fomHists[p][sig].SetLineWidth(2)
    #            fomHists[p][sig].Draw(dOpt)
    #            fomMax = max(getHistMax(fomHists[p][sig])[1] ,fomMax)
    #            if dOpt!="same":
    #                print p, sig , fomHists[p][sig].GetYaxis().GetTitleSize()
    #                first_sig = sig
    #                decorAxis( fomHists[p][sig], 'x', tSize=0.1   ,  lSize=0.1)
    #                decorAxis( fomHists[p][sig], 'y', t='FOM  '   , tOffset=0.5 ,  tSize=0.1,lSize=0.1, func= lambda axis: axis.SetNdivisions(506) )
    #                fomHists[p][sig].SetTitle("")
    #                if unity:
    #                    Func = ROOT.TF1('Func',"[0]",lowBin,hiBin)
    #                    Func.SetParameter(0,1)
    #                    #Func.SetLineStyle(3)
    #                    Func.SetLineColor(1)
    #                    Func.SetLineWidth(1)
    #                    Func.Draw("same")
    #                    fomHists[p][sig].Draw("same")
    #                    ret.update({'func':Func})
    #                dOpt="same"
    #        print 'fom max', fomMax
    #        fomHists[p][first_sig].SetMaximum(fomMax*(1.2))
    #    if save:
    #        saveDir = save + "/%s/"%cut.name
    #        if not os.path.isdir(saveDir): os.mkdir(saveDir) 
    #        canvs[p][cSave].SaveAs(saveDir+"/%s.png"%p)
    #return ret









#############################################################################################################
##########################################                    ###############################################
##########################################    PLOT CLASS      ###############################################
##########################################                    ###############################################
#############################################################################################################


class Plot(dict):
  def __init__(self, name, var, bins, decor={},cut='',**kwargs):
    super(Plot, self).__init__( name=name, var=var, bins=bins,decor=decor,cut=cut,**kwargs)
    self.__dict__ = self 
    #if not all([x in self.__dict__ for x in ['name','tree']]):
    #  assert False,  "Cannot create sample.... Usage:  Sample(name='name', tree=ROOT.TChain, isData=0, isSignal=0, color=ROOT.kBlue)"
    #for attr in defdict:
    #  if attr not in self.__dict__:
    #    self[attr]=defdict[attr]
    if len(self.bins)==3:
      self.is1d = True
    else: self.is1d=  False
    if len(self.bins)==6:
      self.is2d = True
    else: self.is2d = False
    if "hists" not in self.__dict__:
      self.hists=Dict()
  def decorate(hist,decorDict):
    pass


class Plots(dict):
  def __init__(self,  **kwargs):
    plotDict = {}
    for arg in kwargs:
        if not isinstance(arg,Plot):
            #print arg , "Creating Class Plot"
            if not kwargs[arg].has_key('name'): kwargs[arg]['name']=arg
            if not kwargs[arg].has_key('cut'): kwargs[arg]['cut']=''
            plotDict[arg]=Plot(**kwargs[arg])
            #print arg, type(arg)
            #print plotDict
        else:
            #print arg, "already an instance of class Plot"
            plotDict[arg]=kwargs[arg]
    #super(Plots, self).__init__(**kwargs)
    super(Plots, self).__init__(**plotDict)
    self.__dict__=self



#############################################################################################################
##########################################                    ###############################################
##########################################    CUT  CLASS      ###############################################
##########################################                    ###############################################
#############################################################################################################



less = lambda var,val: "(%s < %s)"%(var,val)
more = lambda var,val: "(%s > %s)"%(var,val)
btw = lambda var,minVal,maxVal: "(%s > %s && %s < %s)"%(var, min(minVal,maxVal), var, max(minVal,maxVal))

deltaPhiStr = lambda x,y : "abs( atan2(sin({x}-{y}), cos({x}-{y}) ) )".format(x=x,y=y)

deltaRStr = lambda eta1,eta2,phi1,phi2: "sqrt( ({eta1}-{eta2})**2 - ({dphi})**2  )".format(eta1=eta1,eta2=eta2, dphi=deltaPhiStr(phi1,phi2) ) 

def btw(var,minVal,maxVal, rangeLimit=[0,0] ):
    greaterOpp = ">"
    lessOpp = "<"
    vals = [minVal, maxVal]
    minVal = min(vals)
    maxVal = max(vals)
    if rangeLimit[0]:
        greaterOpp += "="
    if rangeLimit[1]:
        lessOpp += "="
    return "(%s)"%" ".join([var,greaterOpp,minVal, "&&", var, lessOpp, maxVal ])


def makeCutFlowList(cutList,baseCut=''):
  cutFlowList=[]
  for cutName,cutString in cutList:
    cutsToJoin=[] if not baseCut else [baseCut]
    cutsToJoin.extend( [ cutList[i][1] for i in range(0, 1+cutList.index( [cutName,cutString])) ] )
    cutFlowString = joinCutStrings( cutsToJoin   )
    cutFlowList.append( [cutName, cutFlowString ])
  return cutFlowList

def combineCutList(cutList):
  return joinCutStrings([x[1] for x in cutList if x[1]!="(1)"])

def joinCutStrings(cutStringList):
  return "(" + " && ".join([ "("+c +")" for c in cutStringList])    +")"





class CutClass():
  """ CutClass(Name, cutList = [
                                    ["cut1name","cut1string"] ,
                                    ..., 
                                    ["cut2name","cut2string"]] , 
        baseCut=baseCutClass   ) 
  """
  def __init__(self,name,cutList,baseCut=None):
    self.name         = name
    self.inclList     = cutList
    self.inclFlow     = self._makeFlow(self.inclList,baseCut='')
    self.inclCombined = self._combine(self.inclList) 
    self.inclCombinedList  = (self.name ,self._combine(self.inclList) )
    self.baseCut = baseCut
    if baseCut:
      if isinstance(baseCut,CutClass):
        self.baseCutString      = baseCut.combined
        self.baseCutName        = baseCut.name
        self.fullList           = self.baseCut.fullList + self.inclList
        self.fullFlow           = self._makeFlow(self.fullList)
      else:
        self.baseCutName, self.baseCutString = baseCut
    else: 
      self.baseCutName, self.baseCutString = (None,None)
      self.fullList           = self.inclList
    if not self.baseCutString or self.baseCutString == "(1)":
      self.list         = cutList
    else:
      self.list         =[[self.baseCutName, self.baseCutString]]+  [ [cutName,"(%s)"%"&&".join([self.baseCutString,cut])  ] for cutName,cut in self.inclList ]
    self.flow         = self._makeFlow(self.inclList,self.baseCutString)
    self.combined     = self._combine(self.inclList,self.baseCutString)
    self.combinedList = (self.name, self.combined)
  def _makeDict(self,cutList):
    Dict={}
    for cutName, cutString in cutList:
      Dict[cutName]=cutString
    return Dict
  def _makeFlow(self,cutList,baseCut=''):
    flow=makeCutFlowList(cutList,baseCut)
    flowDict= self._makeDict(flow)
    return flow
  def _combine(self,cutList,baseCutString=None) :
    if not baseCutString or baseCutString == "(1)":
      return combineCutList(cutList)
    else:
      return "(%s &&"%baseCutString+ combineCutList(cutList)+ ")"
  def nMinus1(self,minusList, cutList=True ) :
    if self.baseCut:
      cutList = self.fullList
    else:
      cutList = self.inclList
    if not self.baseCut and cutList:
      cutList = cutList
    if type(minusList)==type("str"):
      minusList = [minusList]
    self.cutsToThrow = []
    self.minusCutList = [ c for c in cutList]
    for cut in cutList:
      for minusCut in minusList:
        #print minusCut, cut[0] 
        if minusCut.lower() in cut[0].lower():
          self.cutsToThrow.append(self.minusCutList.pop( self.minusCutList.index(cut)) )
    print "ignoring cuts," , self.cutsToThrow
    return combineCutList(self.minusCutList)



#############################################################################################################
##########################################                    ###############################################
##########################################    YIELDS CLASS    ###############################################
##########################################                    ###############################################
#############################################################################################################



def decide_weight( sample, weight):
    if sample.has_key("weight"):
        weight_str = sample['weight']
    elif weight.endswith("_weight"):
        if sample.has_key(weight):
            weight_str = sample[weight]
            #print sample, weight_str, samples[sample]
        elif sample.isData:
            weight_str = "(1)"
    return weight_str


class Yields():
  '''
    Usage:
    y=Yields(sampleDict,['tt', 'w','s'],cuts.presel,tableName='{cut}_test',pklOpt=1);
  '''
  def __init__(self,sampleDict,sampleList,cutInst,cutOpt='flow',tableName='{cut}',weight="(weight)",pklOpt=False,pklDir="./pkl/",nDigits=2):
    if not isinstance(cutInst,CutClass):
      raise Exception("use an instance of cutClass")
    self.nDigits    = nDigits
    sampleDict = sampleDict
    self.cutInst    = cutInst
    self.weight     = weight
    self.tableName  = tableName.format(cut=self.cutInst.name)
    self.sampleList   = sampleList
    self.sampleList.sort(key = lambda x: sampleDict[x]['isSignal'])
    self.bkgList    = [sample for sample in sampleList if not sampleDict[sample]['isSignal']]
    self.sigList    = [sample for sample in sampleList if sample not in self.bkgList]
    self.cutList    = getattr(cutInst,cutOpt)
    self.cutLegend =   np.array( [[""]+[cut[0] for cut in self.cutList]])
    self.sampleLegend =np.array( [ [sampleDict[sample]['name'] for sample in self.bkgList] + ["Total"] + 
                                 [sampleDict[sample]['name'] for sample in self.sigList] ] )
    self.yieldDictRaw = { sample:[ ] for sample in sampleList}
    self.weights = { samp:decide_weight(sampleDict[samp] , self.weight  ) for samp in sampleList }
    self.getYields(sampleDict)
    self.pklOpt = pklOpt
    self.pklDir = pklDir +"/"
    if self.pklOpt:
      self.pickle(self.pklOpt,self.pklDir)
  def getYields(self,sampleDict):
    for ic, cut in enumerate(self.cutList):
      for sample in self.sampleList:
        yld = round(getYieldFromChain(sampleDict[sample]['tree'], cut[1],self.weights[sample]),self.nDigits) 
        self.yieldDictRaw[sample].append(yld)
    self.yieldDictRaw['Total']  = [sum(x) for x in zip(*[self.yieldDictRaw[sample] for sample in self.bkgList])]
    self.yieldDict={}
    for sample in self.sampleList:
      self.yieldDict[sample]      = np.array([sampleDict[sample]['name']] +self.yieldDictRaw[sample],dtype='|S16')
    self.yieldDict["Total"]     = np.array(["Total"]+ self.yieldDictRaw['Total'],dtype='|S16')
    for sig in self.sigList:
        #sig = self.sigList[0] #### need to fix for multiple signals
        #self.yieldDict["FOM"]       = np.array(["FOM"]+ [ round(calcFOMs(self.yieldDictRaw[sig][ic] , self.yieldDictRaw["Total"][ic] ,0.2,"AMSSYS" ),2 )
        #                                             for ic, cut in enumerate(self.cutList) ] , dtype='|S8')
        self.yieldDict["FOM_%s"%sig]       = np.array(["FOM_%s"%sampleDict[sig]['name'] ]+ [ round(calcFOMs(self.yieldDictRaw[sig][ic] , self.yieldDictRaw["Total"][ic] , 0.2, "AMSSYS"), 3 )
                                                     for ic, cut in enumerate(self.cutList) ] , dtype='|S16')
    self.yields = np.concatenate( [ [self.yieldDict[t]] for t in self.bkgList +['Total'] + self.sigList ] )
    self.table  = np.concatenate( [ self.cutLegend , self.yields ] )
    self.FOM = np.concatenate( [ [self.yieldDict[t]] for t in self.bkgList +['Total'] + self.sigList + ['FOM_%s'%x for x in self.sigList] ] )
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
  def __sizeof__(self):
    return object.__sizeof__(self) + \
      sum(sys.getsizeof(v) for v in self.__dict__.values())










 
