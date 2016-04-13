#degTools.py

import ROOT
import os,sys
import math
import pickle
import numpy as np
import glob
import jinja2
import argparse
import array as ar
import pprint as pp

from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.navidTools.getRatioPlot import *
from Workspace.DegenerateStopAnalysis.navidTools.FOM import *

cmsbase = os.getenv("CMSSW_BASE")
print "CMSSW Release: ", cmsbase
#ROOT.gROOT.LoadMacro(cmsbase+"/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
##ROOT.setTDRStyle()
#ROOT.gStyle.SetErrorX(0.5)
#maxN = -1
#ROOT.gStyle.SetOptStat(0)
#ROOT.gStyle.SetPalette(1)
##ROOT.gStyle.SetCanvasPreferGL(1)

#############################################################################################################
##########################################                    ###############################################
##########################################    ETC  TOOLS      ###############################################
##########################################                    ###############################################
#############################################################################################################

getAllAlph = lambda str: ''.join(ch for ch in str if ch not in "!>=|<$&@$%[]{}#()/; '\"")
addSquareSum = lambda x: math.sqrt(sum(( e**2 for e in x   )))

def makeDir(path):
    if os.path.isdir(path):
        return
    else:
        mkdir_p(path)

def saveCanvas(canv,dir="./",name="",formats=["png"], extraFormats=["root","C","pdf"],overwrite=False, makeDir=True):
    if not os.path.isdir(dir): 
        mkdir_p(dir)
    if type(formats)!=type([]):
        formats = [formats]
    for form in formats:
        canv.SaveAs(dir+"/%s.%s"%(name,form) )
    if extraFormats:
        extraDir = dir+"/extras/"
        if not os.path.isdir(extraDir): mkdir_p(extraDir)
        for form in extraFormats:
            canv.SaveAs(extraDir+"/%s.%s"%(name,form) )

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

def get_args(sysargs):
    """ Setup the command line options. """
    #if 'ipython' in sysargs[0].lower():
    #    sysargs = sysargs[sysargs.index("--")+1:]
    #else: 
    #    if "--" in sysargs: sysarg.remove("--")
    #    sysargs = sysargs[1:]

    print sysargs
                
    description = ''' 
        Basic function to be imported for simple and quick arg 
        '''
    #parser = argparse.ArgumentParser(argument_default=sysargs, description=description)
    parser = argparse.ArgumentParser( description=description)


    parser.add_argument('-s', '--sampleList', nargs='+', 
                                     default=["s30","wtau","w"], help='Input Samples')

    parser.add_argument('-c', '--cutInst',  
                                     default="sr1Loose", help='Instance of CutClass To be Used')

    parser.add_argument('-p', '--process', action="store_true", 
                                      help='Do stuff or not')
    parser.add_argument('-ht', '--useHT', action="store_true", 
                                      help='Use HT binned samples')

    #return parser.parse_args(sysargs)
    return parser

class ArgParser(argparse.ArgumentParser):
    def parse(self, sysargs):
        self.sysargs = self._fix_args( sysargs)

        self.add_argument('-s', '--sampleList', nargs='+',
                                     default=["s30","w"], help='input Samples')
        self.add_argument('-p', '--process', action="store_true",
                                      help='input Samples')
        self.add_argument('-c', '--cutInst',  
                                     default="sr1Loose", help='Instance of CutClass To be Used')
        self.add_argument('-ht', '--useHT', action="store_true", 
                                      help='Use HT binned samples')

        parsed = self.parse_known_args(self.sysargs)
        if parsed[1]:
            print "Some Options were not recognized:", parsed
        return parsed[0]

    def _fix_args(self, sysargs):
        if 'ipython' in sysargs[0].lower():
            sysargs = sysargs[sysargs.index("--")+1:]
        else: 
            if "--" in sysargs: sysarg.remove("--")
            sysargs = sysargs[1:]
        return sysargs

#############################################################################################################
##########################################                    ###############################################
##########################################    GET AND DRAW    ###############################################
##########################################  Chains and Plots  ###############################################
##########################################                    ###############################################
#############################################################################################################

def getPlot(sample,plot,cut,weight="(weight)", nMinus1="",cutStr="",addOverFlowBin=''):
    c     = sample.tree
    var = plot.var
    if nMinus1:
        cutString = cut.nMinus1(nMinus1)
    else:
        cutString = cut.combined
    if cutStr:
        cutString += "&&(%s)"%cutStr
    warn=False
    if hasattr(sample,"triggers") and sample['triggers']:
        cutString += "&&(%s)"%sample['triggers']
        warn = True
    if hasattr(sample,"filters") and sample['filters']:
        cutString += "&&(%s)"%sample['filters']
        warn = True
    if warn:
        print "-----"*10 , sample.name
        print "-----"*20
        print "Applying Triggers: %s"%sample['triggers']
        print "Applying Filters: %s"%sample['filters']

        print "-----"*20
        print "-----"*20

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

def getPlots(samples,plots,cut,sampleList=[],plotList=[],weight="(weight)",nMinus1="", addOverFlowBin='',verbose=True):
    if verbose:print "Getting Plots: "

    sigList, bkgList, dataList = getSigBkgDataLists(samples, sampleList=sampleList)
    isDataPlot = bool(len(dataList))
    if isDataPlot:
 
        if "Blind" in samples[dataList[0]].name and "sr" in cut.name:
            raise Exception("NO DATA IN SIGNAL REGION: %s"%[dataList, cut.name])
        weight = samples[dataList[0]].name+"_weight"

    if len(dataList) > 1:
        raise Exception("More than one Data Set in the sampleList... This could be dangerous: %s"%dataList)

    for sample in samples.iterkeys():
        #if sample in sampleList or not sampleList:
        if not sample in sampleList:
            continue
        if verbose: print "  Sample:" , samples[sample].name, 
        weight_str = decide_weight(samples[sample], weight)
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
                nMinus1String = nMinus1
                #nMinus1String = plots[plot]["nMinus1"] if plots[plot].has_key("nMinus1") else nMinus1
            else: nMinus1String=""
            getPlot(samples[sample],plots[plot],cut,weight=weight_str,nMinus1=nMinus1String,cutStr=cutStr,addOverFlowBin=addOverFlowBin)

def getStackFromHists(histList,sName=None,scale=None, normalize=False, transparency=False):
  if sName:
    stk=ROOT.THStack(sName,sName)
  else:
    stk=ROOT.THStack()

  if transparency:
    alphaBase=0.80
    alphaDiff=0.70
    alphas=[alphaBase-i*alphaDiff/len(histList) for i in range(len(histList)) ]
    print alphas
    print histList

  for i, hist in enumerate(histList):
    #h = hist.Clone()
    h = hist
    h.ClearUnderflowAndOverflow()
    if scale:
      print "    Scaling: ", sName if sName else [ hist.GetName(), hist.GetTitle() ]
      h.Scale(scale)
    if normalize:
      if h.Integral():
        h.Scale(1/h.Integral())
      else:
        print "Histogram Integral is zero, can't normalize",  sName if sName else [ hist.GetName(), hist.GetTitle()]
    if transparency:
      h.SetFillColorAlpha(h.GetFillColor(), alphas[i])
    stk.Add(h)
  return stk

def getSamplePlots(samples,plots,cut,sampleList=[],plotList=[]):
    if not sampleList: sampleList= samples.keys()
    bkgList=[samp for samp in sampleList if not samples[samp]['isSignal'] and not samples[samp]['isData'] ]
    dataList = [samp for samp in sampleList if samples[samp]['isData'] ]
    sigList=[samp for samp in sampleList if samples[samp]['isSignal'] ]
    if not plotList: plotList=plots.keys()
    hists={}
    for samp in sampleList:
        hists[samp]={}
        for p in plotList:
            v = p
            hists[samp][v]= samples[samp]['cuts'][cut.name][v]
    return hists
        
def getBkgSigStacks(samples, plots, cut, sampleList=[],plotList=[], normalize=False, transparency=None):
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
            bkgStackDict[v]= getStackFromHists([ samples[samp]['cuts'][cut.name][v] for samp in sampleList if not samples[samp]['isSignal'] and not samples[samp]['isData']], normalize=normalize, transparency=transparency)
            sigStackDict[v]= getStackFromHists([ samples[samp]['cuts'][cut.name][v] for samp in sampleList if samples[samp]['isSignal']], normalize=normalize, transparency=False)
            dataStackDict[v]=getStackFromHists([ samples[samp]['cuts'][cut.name][v] for samp in sampleList if samples[samp]['isData']], normalize=normalize, transparency=False)
    return {'bkg': bkgStackDict,'sig': sigStackDict, 'data': dataStackDict}
 
def getSigBkgDataLists ( samples, sampleList):
    sigList=[samp for samp in sampleList if samples[samp]['isSignal'] ]
    bkgList=[samp for samp in sampleList if not samples[samp]['isSignal']  and not samples[samp]['isData'] ]
    dataList = [samp for samp in sampleList if samples[samp]['isData'] ]
    return sigList, bkgList, dataList

def drawPlots(samples,plots,cut,sampleList=['s','w'],plotList=[],plotMin=False, plotLimits=[],logy=0,save=False,
                                            fom=True, normalize=False, 
                                            denoms=None,noms=None, ratioNorm=False,  fomLimits=[],
                                            leg=True,unity=True, verbose=False):
    if normalize and fom and fom.lower() != "ratio":
        raise Exception("Using FOM on area  normalized histograms... This can't be right!")
    
    #tfile = ROOT.TFile("test.root","new")

    ret = {}
    canvs={}
    hists   = getSamplePlots(samples,plots,cut,sampleList=sampleList, plotList=plotList)
    stacks  = getBkgSigStacks(samples,plots,cut, sampleList=sampleList, plotList=plotList, normalize=normalize, transparency=normalize )
    sigList, bkgList, dataList = getSigBkgDataLists(samples, sampleList=sampleList)
    ret.update({
                'canvs':canvs       , 
                'stacks':stacks     ,
                'hists':hists       ,
                'fomHists':{}       ,
                'sigBkgDataList': [sigList,bkgList,dataList],
                })
    
    isDataPlot = bool(len(dataList))
    if isDataPlot:
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.05)
        latex.SetTextAlign(11)
        ret['latex']=latex

    if len(dataList) > 1:
        raise Exception("More than one Data Set in the sampleList... This could be dangerous. %"%dataList)       
    for p in plots.iterkeys():
        if plotList and p not in plotList:
            continue
        if plots[p]['is2d']:
            print "2D plots not supported:" , p
            continue
        if fom:
            denoms = denoms if type(denoms)==type([]) else [denoms]
            if not denoms or len(denoms)==1:
                padRatios=[2,1]
            else:
                padRatios=[2]+[1]*(len(denoms))

            canvs[p]=makeCanvasMultiPads(c1Name="%s_%s"%(cut.name,p),c1ww=800,c1wh=800, joinPads=True, padRatios=padRatios, pads=[])
            cSave , cMain=0,1   # index of the main canvas and the canvas to be saved
        else: 
            canvs[p] = ROOT.TCanvas(p,p,800,800), None, None
            cSave , cMain=0,0
        canvs[p][cMain].cd()
        dOpt="hist"
        if normalize: 
            dOpt+="nostack"
        if len(bkgList):
            refStack=stacks['bkg'][p]
            refStack.Draw(dOpt)
            dOpt="same"
        else:
            refStack = stacks['sig'][p]
        if len(dataList):
            dataHist=hists[dataList[0]][p]            
            dataHist.Draw("E0Psame")
            dataHist.SetMarkerStyle(20)
            dataHist.SetMarkerSize(1.2)
            dOpt+=""
        stacks['sig'][p].Draw("%s nostack"%dOpt.replace("hist",""))
        print "!!!!!!!!!!!!!!!!!!!!" , refStack, getattr(refStack,"Get%saxis"%"y".upper() )()
        if plots[p].has_key("decor"):
            if plots[p]['decor'].has_key("y") : decorAxis( refStack, 'y', plots[p]['decor']['y'], tOffset=1 )
            if plots[p]['decor'].has_key("title") :refStack.SetTitle(plots[p]['decor']['title'] ) 
            if plots[p]['decor'].has_key("log"):
                logx, logy, logz = plots[p]['decor']['log']
                if logx : canvs[p][cMain].SetLogx(1)
                if logy : canvs[p][cMain].SetLogy(1)
        if plotMin: refStack.SetMinimum( plotMin )
        if plotLimits: 
            refStack.SetMinimum( plotLimits[0] )
        refStack.SetMaximum( refStack.GetMaximum() * 10 )

        if leg:    #MAKE A LEGEND FUNCTION
            bkgLeg = makeLegend(samples, hists, bkgList, p, loc= [0.7,0.7,0.9,0.9] , name="Legend_bkgs_%s_%s"%(cut.name, p), legOpt="f" )
            sigLeg = makeLegend(samples, hists, sigList, p, loc= [0.4,0.75,0.7,0.9] , name="Legend_sigs_%s_%s"%(cut.name, p), legOpt="l" )

            bkgLeg.Draw()
            sigLeg.Draw()
            ret.update( {'legs':[sigLeg, bkgLeg]})

        if fom:
            getFOMPlotFromStacks( ret, p, sampleList ,fom=fom, normalize=normalize,
                                              denoms=denoms,noms=noms, ratioNorm=ratioNorm, fomLimits=fomLimits,
                                              leg=leg,unity=unity, verbose=verbose  )
        canvs[p][cMain].RedrawAxis()
        canvs[p][cMain].Update()
        canvs[p][cMain].cd()
        if isDataPlot:
            latex.DrawLatex(0.16,0.91,"#font[22]{CMS Preliminary}")
            latex.DrawLatex(0.7,0.91,"#bf{L=%0.2f fb^{-1} (13 TeV)}"%( round(samples[dataList[0]].lumi/1000.,2)) )
        canvs[p][cSave].Update()

        #if save:
        #    saveDir = save + "/%s/"%cut.saveDir if type(save)==type('') else "./"
        #    #saveDir = save + "/%s/"%cut.name
        #    #canvs[p][cSave].SaveAs(saveDir+"/%s.png"%p)
        #    saveCanvas(canvs[p][cSave],saveDir, p, formats=["png"], extraFormats=["root","C","pdf"])
    return ret

def getFOMPlotFromStacks( ret, plot, sampleList ,fom=True, normalize=False, 
                          denoms=None,noms=None, ratioNorm=False , fomLimits=[0.8,2],
                          unity=True, verbose=False , leg=True):

        hists = ret['hists']
        hists['bkg']={} 
        stacks = ret['stacks']
        canvs = ret['canvs']
        fomHists = ret['fomHists']
        sigList, bkgList, dataList = ret['sigBkgDataList']
    

        fomFunc = fom if type(fom)==type('') else "AMSSYS"
        fomIntegral = False if fomFunc =="RATIO" else True
        fomMax = 0
        fomMin = 999
        fomHists[plot]={}
        #ret.update({'fomHist':fomHists})
        if "ratio" in fomFunc.lower():
            pass
        #denom = denom if type(denom)==type([]) else [denom]
    
        print "isdataplot:",  [ x in dataList for x in noms ]
        if any( [ x in dataList for x in noms ]):       
            isDataPlot=True
            fomPlotTitle = "DATA/MC     " if "bkg" in denoms else "BAAAAAAAAAAAAAA"
        else: 
            isDataPlot = False
            fomPlotTitle = fomFunc
            

        for idenom, denom in enumerate(denoms,2):
            canvs[plot][idenom].cd()
            fomHists[plot][denom]={}  
            ## Getting the total BKG hist
            if bkgList:
                hists['bkg'][plot]=stacks['bkg'][plot].GetHists()[0].Clone( "stack_%s"%plot)
                hists['bkg'][plot].Reset()
                hists['bkg'][plot].SetTitle("stack_%s"%plot)
                hists['bkg'][plot].Merge( stacks['bkg'][plot].GetHists() )
            if denom:
                fomHists[plot][denom]['denom']=hists[denom][plot]
                if not isDataPlot: fomPlotTitle += " (%s)"%denom
            else:
                fomHists[plot][denom]['denom']=hists[plot]['bkg'] if bkgList else False

            #refStack.SetMaximum(getHistMax(fomHists[plot][denom]['denom'])[1]*1.3)
            nBins  = fomHists[plot][denom]['denom'].GetNbinsX()
            lowBin = fomHists[plot][denom]['denom'].GetBinLowEdge(1)
            hiBin  = fomHists[plot][denom]['denom'].GetBinLowEdge(fomHists[plot][denom]['denom'].GetNbinsX()+1)

            #dOpt="" if not isDataPlot else "E1P"
            dOpt="" if not isDataPlot else "E0P"

            if not noms:
                nomeratorList = sigList
            else:
                nomeratorList = [x for x in noms]
            if denom in nomeratorList: nomeratorList.remove(denom)
            for nom in nomeratorList:
                #sigHist= samples[sig]['cuts'][cut.name][plot]
                sigHist= hists[nom][plot]
                fomHists[plot][denom][nom] = getFOMFromTH1FIntegral(sigHist, fomHists[plot][denom]['denom'] ,fom=fomFunc, verbose =False, integral = fomIntegral)
                #print "---------------------------------------------------"
                #sigHist.Print("all")
                #fomHists[plot][denom]['denom'].Print("all")
                #fomHists[plot][denom][nom].Print("all")

                #print "---------------------------------------------------"
                if ratioNorm:
                    fomHists[plot][denom][nom].Scale(1./fomHists[plot][denom][nom].Integral() ) 
                fomHists[plot][denom][nom].SetLineWidth(2)
                fomHists[plot][denom][nom].Draw(dOpt)
                fomMax = max(getHistMax(fomHists[plot][denom][nom])[1] ,fomMax)
                newMin = getHistMin(fomHists[plot][denom][nom],onlyPos=True)[1]
                fomMin = min( newMin ,fomMin)
                #print newMin, fomMin
                if dOpt!="same":
                    #print p, nom , fomHists[plot][denom][nom].GetYaxis().GetTitleSize()
                    first_nom = nom
                    decorAxis( fomHists[plot][denom][nom], 'x', tSize=0.1   ,  lSize=0.1)
                    #decorAxis( fomHists[plot][denom][nom], 'y', t='%s  '%fomPlotTitle   , tOffset=0.5 ,  tSize=1./len(fomPlotTitle), lSize=0.1, func= lambda axis: axis.SetNdivisions(506) )
                    decorAxis( fomHists[plot][denom][nom], 'y', t='%s  '%fomPlotTitle   , tOffset=0.8 ,  tSize=0.07, lSize=0.1, func= lambda axis: axis.SetNdivisions(506) )
                    fomHists[plot][denom][nom].SetTitle("")
                    dOpt="same"
            if unity:
                Func = ROOT.TF1('Func',"[0]",lowBin,hiBin)
                Func.SetParameter(0,1)
                #Func.SetLineStyle(3)
                Func.SetLineColor(1)
                Func.SetLineWidth(1)
                Func.Draw("same")
                fomHists[plot][denom].update({'func':Func})
            print 'fom min max', fomMin, fomMax
            print "first fom hist", first_nom
            if fomLimits:
                fomHists[plot][denom][first_nom].SetMinimum(fomLimits[0] )
                fomHists[plot][denom][first_nom].SetMaximum(fomLimits[1] )
            else:
                fomHists[plot][denom][first_nom].SetMaximum(fomMax*(1.2) )
                fomHists[plot][denom][first_nom].SetMinimum(fomMin*(0.8) )
            fomHists[plot][denom][first_nom].Draw("same")
            print "idenom", idenom
            canvs[plot][idenom].RedrawAxis()
            canvs[plot][idenom].Update()

        #for canv in canvs[plot]:
        #    canv.cd()
        return ret

def makeLegend(samples, hists, sampleList, plot, name="Legend",loc=[0.6,0.6,0.9,0.9],borderSize=0,legOpt="f"):

    leg = ROOT.TLegend(*loc)
    leg.SetFillColorAlpha(0,0.001)
    leg.SetBorderSize(borderSize)

    for samp in sampleList:
        leg.AddEntry(hists[samp][plot], samples[samp].name , legOpt)    
    return leg

def getPieChart(samples, sampleList, cut):
    ylds = []
    colors = []
    for samp in sampleList:
        weightStr = "weight" if not samples[samp].has_key("weight") else samples[samp]["weight"]
        ylds.append(  getYieldFromChain(samples[samp]['tree'], cut.combined, weightStr) )
        colors.append( samples[samp]['color'] )

    ylds = ar.array("f",ylds)
    colors = ar.array("i",colors)
    pie = ROOT.TPie( cut.name, cut.name , len(ylds), ylds, colors)

    return pie

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
                leg.SetFillColorAlpha(0,0.001)
                leg.SetBorderSize(0)
                ret.update({'leg':leg})
                for bkg in bkgList:
                    leg.AddEntry(hists[bkg][p], samples[bkg].name , "f")    
                for sig in sigList:
                    leg.AddEntry(hists[sig][p], samples[sig].name , "l")    
                leg.Draw()
            if save:
                saveDir = save + "/%s/"%cut.saveDir if type(save)==type('') else "./"
                if not os.path.isdir(saveDir): os.mkdir(saveDir) 
                canvs[plotName].SaveAs(saveDir+"/%s.png"%plotTitle)
    return ret

def makeStopLSPPlot(name, massDict, title="", bins = [22,100,650, 65,0,650 ], key=None, func=None,setbin=False ):
    """
    massDict should be of the form {    
                                    stopmass1: { lsp_mass_1: a, lsp_mass_2: b ... },
                                    stopmass2: { lsp_mass_1: c, lsp_mass_2: d ...},
                                    ...
                                    }
    with a, b, c,d ... the bin content TH2D
    if key available then key(a) will be evaluated
    if func available then func(mstop,mlsp) will be evaluted. (func will override key)
    """
    plot = ROOT.TH2F(name,title, *bins )
    if setbin:
        print "USE setbin=TRUE WITH CAUTION"
        for x in range(1, plot.GetNbinsX()+1):
            xbin = int(plot.GetXaxis().GetBinLowEdge(x))
            for y in range(1, plot.GetNbinsY()+1):
                ybin = int(plot.GetYaxis().GetBinLowEdge(y))
                try:
                    plot.SetBinContent(x,y,massDict[xbin][ybin])
                except KeyError:
                    pass
    else:
        for stop_mass in massDict:
            for lsp_mass in massDict[stop_mass]:
                if func:
                    val = func(stop_mass, lsp_mass)
                elif key:
                    val = key(massDict[stop_mass][lsp_mass])
                else:
                    val = massDict[stop_mass][lsp_mass]
                plot.Fill(int(stop_mass), int(lsp_mass) , val )
    plot.SetTitle(title)
    plot.GetXaxis().SetTitle("m(#tilde{t})[GeV]")
    plot.GetYaxis().SetTitle("m(#tilde{#chi}^{0})[GeV]")
    return plot


#############################################################################################################
##########################################                    ###############################################
##########################################    PLOT CLASS      ###############################################
##########################################                    ###############################################
#############################################################################################################

def decorHist(samp,cut,hist,decorDict):
    dd=decorDict
    if dd.has_key("title"):
        title = dd['title']
        title = title.format(CUT=cut.name, SAMP=samp.name )
        hist.SetName(getAllAlph(samp.name+dd["title"]))
        hist.SetTitle(title)
    if dd.has_key("color") and dd['color']:
        hist.SetLineColor(dd['color'])
    elif not samp.isData and not samp.isSignal:
        hist.SetFillColor(samp['color'])
        hist.SetLineColor(ROOT.kBlack)
    elif samp.isSignal:
        hist.SetLineWidth(2)
        hist.SetLineColor(samp['color'])
        hist.SetMarkerStyle(0)
    elif samp.isData:
        pass
    else:
        print "default color used for:", samp.name # , cut, hist, decorDict
    if dd.has_key("x") and dd['x']:
        hist.GetXaxis().SetTitle(dd['x'])
    if dd.has_key("y") and dd['y']:
        hist.GetYaxis().SetTitle(dd['y'])

def decorAxis(hist, axis,t="",tSize="",tFont="",tOffset="",lFont="",lSize="",func=""):
    if not hist:    return
    if not axis:    return
    if axis.lower() not in ['x','y','z']: assert False
    axis = getattr(hist,"Get%saxis"%axis.upper() )()
    if t: axis.SetTitle(t)
    if tSize  : axis.SetTitleSize(tSize)
    if tFont  : axis.SetTitleFont(tFont)
    if tOffset: axis.SetTitleOffset(tOffset)
    if lFont  : axis.SetLabelFont(lFont)
    if lSize  : axis.SetLabelSize(lSize)
    if func   : func(axis)

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
    return "(%s)"%" ".join(["%s"%x for x in [var,greaterOpp,minVal, "&&", var, lessOpp, maxVal ]])

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
        self.inclCombinedList    = (self.name ,self._combine(self.inclList) )
        self.baseCut = baseCut

        self.saveDir = self.baseCut.saveDir +"/" + self.name if self.baseCut else self.name
        self.fullName = self.baseCut.name + "_" + self.name if self.baseCut else self.name

        if baseCut:
            if isinstance(baseCut,CutClass) or hasattr(baseCut,"combined"):
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
        self.list2        = self.list[1:]
        self.flow         = self._makeFlow(self.inclList,self.baseCutString)
        self.combined     = self._combine(self.inclList,self.baseCutString)
        self.combinedList = [[self.name, self.combined]]
    
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
    #def nMinus1(self,minusList, cutList=True ) :
    #    if self.baseCut:
    #        cutList = self.fullList
    #    else:
    #        cutList = self.inclList
    #    if not self.baseCut and cutList:
    #        cutList = cutList
    #    if type(minusList)==type("str"):
    #        minusList = [minusList]
    #    self.cutsToThrow = []
    #    self.minusCutList = [ c for c in cutList]
    #    for cut in cutList:
    #        for minusCut in minusList:
    #            #print minusCut, cut[0] 
    #            if minusCut.lower() in cut[0].lower():
    #                self.cutsToThrow.append(self.minusCutList.pop( self.minusCutList.index(cut)) )
    #    print "ignoring cuts," , self.cutsToThrow
    #    return combineCutList(self.minusCutList)
    
    def add(self, cutInst, cutOpt="inclList", baseCutString="" ):
        if baseCutString:
            cutList = addBaseCutString(getattr(cutInst,cutOpt), baseCutString )
        else: 
            cutList = getattr(cutInst,cutOpt)
        self.__init__(self.name,self.inclList + cutList , baseCut = self.baseCut)  

def splitCutInPt(cutInst ):
    ptRange=[
                ["pt1", btw("lepPt",5,12) ],
                ["pt2", btw("lepPt",12,20) ],
                ["pt3", btw("lepPt",20,30) ],
             ]
    return CutClass( cutInst.name +"_PtBin",
                        [ [cut[0] +"_"+pt[0], "(%s && %s)"%(cut[1],pt[1]) ]  for cut in cutInst.inclList for pt in ptRange],
                    baseCut = cutInst.baseCut
            )

def addBaseCutString(cutList, baseCutString ):
    return     [ [cut[0], joinCutStrings( [ baseCutString, cut[1] ] ) ] for cut in cutList  ]

#############################################################################################################
##########################################                    ###############################################
##########################################    YIELDS CLASS    ###############################################
##########################################                    ###############################################
#############################################################################################################

class Yields():
    '''
        Usage:
        y=Yields(samples,['tt', 'w','s'],cuts.presel,tableName='{cut}_test',pklOpt=1);
    '''
    def __init__(self,samples,sampleList,cutInst,cutOpt='flow',tableName='{cut}',weight="(weight)",pklOpt=False,pklDir="./pkl/",nDigits=2, err=True, verbose=False, nSpaces=None):
        if not (isinstance(cutInst,CutClass) or hasattr(cutInst,cutOpt)):
            raise Exception("use an instance of cutClass")
        self.nDigits        = nDigits
        samples = samples
        self.cutInst        = cutInst
        self.weight         = weight
        self.tableName      = tableName.format(cut=self.cutInst.name)
        self.sampleList     = [s for s in sampleList]
        self.sampleList.sort(key = lambda x: samples[x]['isSignal'])
        self.npsize="|S20"
        self.err = err

        self.fomNames={}

        self.updateSampleLists(samples,self.sampleList)

        self.cutList        = getattr(cutInst,cutOpt)
        self.cutLegend =     np.array( [[""]+[cut[0] for cut in self.cutList]])
        self.cutNames        = list( self.cutLegend[0][1:] )

        if not nSpaces:
            terminal_size = getTerminalSize()
            nSpaces = (terminal_size[0] -  10 - len(self.cutLegend[0]) )/len(self.cutLegend[0])
        self.nSpaces =  nSpaces 

        self.yieldDictRaw = { sample:[ ] for sample in sampleList}
        self.yieldDictFull = { sample:{} for sample in sampleList}
        self.pklOpt = pklOpt
        self.pklDir = pklDir +"/"
        self.verbose = verbose
        if self.verbose:
           print "Weights:"
           pp.pprint(self.weights)

        self.getYieldDictFull( samples, self.cutList )

        #self.getYields(samples, self.cutList,err)
        if self.pklOpt:
            self.pickle(self.pklOpt,self.pklDir)

    def updateSampleLists(self, samples, sampleList):
        self.bkgList        = [samp for samp in   samples.bkgList()  if samp in sampleList]
        self.sigList        = [samp for samp in   samples.sigList()  if samp in sampleList]
        self.dataList       = [samp for samp in   samples.dataList()  if samp in sampleList]
        self.sampleNames    = { samp:fixForLatex(samples[samp]['name']) for samp in sampleList}


        self.LatexTitles    = {}
        self.LatexTitles.update({ samp:self.sampleNames[samp] for samp in self.sampleNames})
        self.LatexTitles.update({ fomName:self.fomNames[fomName] for fomName in self.fomNames }) 
        self.LatexTitles.update({ "Total":"Total" })


        #self.sampleLegend   = np.array( [ [samples[sample]['name'] for sample in self.bkgList] + ["Total"] + 
        #                                                         [samples[sample]['name'] for sample in self.sigList] ] )

        self.weights        = { samp:decide_weight(samples[samp] , self.weight    ) for samp in self.sampleList }
        #self.weights        = { samp:decide_weight2(samples[samp] , cut=self.cutInst.name, lumi="target_lumi"    ) for samp in self.sampleList } # need to fix lumi for comparison with data
            

        if hasattr(self,"LatexTitles"):
            #self.sampleLegend   =   [self.LatexTitles[sample] for sample in self.bkgList] +\
            #                        ["Total"] +  \
            #                        [self.LatexTitles[sample] for sample in self.sigList] +  \
            #                        [self.LatexTitles[sample] for sample in getattr(self,"fomList",[]) ]
            self.sampleLegend   =   [self.LatexTitles[sample] for sample in self.bkgList] +\
                                    ["Total"]
            if self.fomNames:
                for sample in self.sigList:
                    self.sampleLegend.extend( [self.LatexTitles[sample], self.LatexTitles["FOM_%s"%sample] ] ) 
                                    #[self.LatexTitles[sample] for sample in getattr(self,"fomList",[]) ]
                                   


    def addYieldDict(self,samples,yieldDict):
        """
        Updating the current Yield Dictionary with a new one. 
        yieldDict should be of the format yd = { 'samp1': {'cut1':u_float(val,sigma), ...}, ... }
        """
        new_samples = yieldDict.keys()
        for samp in new_samples:
            if samp in samples.keys():
                self.sampleList.append(samp)
            else:
                raise Exception("%s not currently in the samples dictionary. could this be a problem?"%s)
                self.sampleList = self.sampleList + new_samples
        self.updateSampleLists(samples,self.sampleList)
        for samp in new_samples:
            cuts = yieldDict[samp].keys()
            if not sorted(cuts) ==  sorted( list( self.cutLegend[0][1:] ) ) :
                raise Exception("The new yield dictionary seems to have different cuts than the current one  %s \n vs. %s"%(cuts, sorted( list(self.cutLegend[0][1:]) ) ))
        self.yieldDict.update(yieldDict)
        self.yieldDictFull.update(yieldDict)  ### FIX ME, should also combine Totals, FOMs, etc

    def makeNumpyFromDict(self, yieldDict=None,rowList=[]):
        """
        """
        exps = []
        if not yieldDict:
            yieldDict = self.yieldDictFull        
        if not rowList:
            rowList = self.sampleList
        first = True
        for samp in rowList: 
            if first:
                #exps.append( np.array([samp]+[ yieldDict[samp][cut] for cut in self.cutNames] , self.npsize) )
                exps.append( np.array([ self.sampleNames[samp] ]+[ yieldDict[samp][cut] for cut in self.cutNames] , self.npsize) )
            else:
                exps.append( np.array([samp]+[ yieldDict[samp][cut] for cut in self.cutNames] , self.npsize) )
        return np.concatenate(  [ self.cutLegend, np.array(exps)] )                                            
            

    def getBySample(self, samples, yieldDict):
        pass

    def getByBin(self, bin,  yieldDict=None):
        return { samp: yieldDict[samp][bin]  for samp in yieldDict.keys() }

    def getByBins(self, yieldDict=None):
        if not yieldDict: yieldDict = self.yieldDictFull
        return { bin: { samp:yieldDict[samp][bin] for samp in yieldDict.keys() } for bin in self.cutNames}  

    def round(self, val, nDigits):
        try: 
            return val.round(nDigits)
        except AttributeError:
            return round(val, nDigits)

    def getBkgTotal(self, yieldDict):
        yieldDictTotal={}
        for cut in self.cutNames:
            summed = sum( [ yieldDict[samp][cut] for samp in self.bkgList  ] )
            yieldDictTotal[cut] =   self.round( summed ,self.nDigits ) 
        #return {'Total':yieldDictTotal}
        return yieldDictTotal

    def getSigFOM(self, yieldDict=None, yieldDictTotal = None, fom="AMSSYS", uncert=0.2, nDigits = 3):
        fomDict={}
        self.fomNames = {}
        self.fomList  = []
        if not yieldDict: yieldDict = self.yieldDict
        if not yieldDictTotal:
            yieldDictTotal = self.getBkgTotal(yieldDict)
        for sig in self.sigList:
            fom_name = "FOM_%s"%sig
            fom_title = "FOM_%s"%self.sampleNames[sig]
            self.fomList.append(fom_name)
            self.fomNames[fom_name]=fixForLatex(fom_title)
            fomDict[fom_name]={}
            for cut in self.cutNames:
                fom_val = calcFOMs( yieldDict[sig][cut] , yieldDictTotal[cut] , uncert , fom) 
                fomDict[fom_name][cut]  = round( fom_val , nDigits ) 
        return fomDict

    def getNiceYieldDict(self, yieldDict=None):
        yld  = {}
        if not yieldDict: yieldDict = self.yieldDictFull
        for samp in yieldDict:
            yld[ self.LatexTitles[samp] ]  = yieldDict[samp]
        return yld                        

    def getYieldsForSample(self,samples,sample, cutList ):
        yieldDictSample={}
        for ic, cut in enumerate(cutList):
            yld = getYieldFromChain( samples[sample]['tree'], cut[1],self.weights[sample], returnError=self.err) #,self.nDigits) 
            #print cut[0], "     ", "getYieldFromChain( %s, '%s', '%s',%s )"%( "samples."+sample+".tree", cut[1], self.weights[sample], True) + "==(%s,%s)"%yld 
            if self.err:
                    rounded = [ round(x,self.nDigits) for x in yld ] 
                    yld = u_float(*rounded)
            else:
                    yld = u_float(yld)
            yieldDictSample[cut[0]] = yld
            self.yieldDictFull[sample][cut[0]] = yld
            #self.yieldDictRaw[sample].append(yld)
        if self.verbose:  
            
            self.pprint( [np.array([self.sampleNames[sample]]+[ yieldDictSample[cut] for cut in self.cutNames] , self.npsize)] , nSpaces=self.nSpaces   )     
            #self.pprint( yieldDictSample, nSpaces=14) 
            #print sample, yieldDictSample
        return yieldDictSample

    

    def getYields2(self,samples,cutList):
        yieldDict={}
        if self.verbose: self.pprint(  self.cutLegend  , nSpaces=self.nSpaces )
        for samp in self.sampleList:
            yieldDict[samp] = self.getYieldsForSample(samples,samp, cutList )
        self.yieldDict = yieldDict
        #print yieldDict
        return yieldDict
        
    def getYieldDictFull(self, samples, cutList, yieldDict=None, yieldDictTotal=None, yieldDictFOMs=None,  fom="AMSSYS", uncert=0.2, nDigits = 3 ):
        yieldDictFull = {}
        if not yieldDict:
            yieldDict       =   self.getYields2(samples, cutList )
            yieldDictFull.update(yieldDict)
        if not yieldDictTotal:
            yieldDictTotal  =   self.getBkgTotal(yieldDict)
            yieldDictFull.update({'Total':yieldDictTotal})
        if not yieldDictFOMs:
            yieldDictFOMs   =   self.getSigFOM(yieldDict, yieldDictTotal, fom=fom, uncert=uncert, nDigits=nDigits )
            yieldDictFull.update(yieldDictFOMs)
        self.yieldDict = yieldDict
        self.yieldDictTotal = yieldDictTotal
        self.yieldDictFOMs  = yieldDictFOMs
        self.yieldDictFull  = yieldDictFull

        self.FOMTable       =   self.makeNumpyFromDict(self.yieldDict)
        self.table          =   self.makeNumpyFromDict(self.yieldDictFull)


        self.updateSampleLists(samples,self.sampleList)
        return yieldDictFull


    #   ########################
    #   ##### Old Function #####
    #   ########################

    #   def getYields(self,samples, cutList ):
    #       for sample in self.sampleList:
    #           for ic, cut in enumerate(cutList):
    #               yld = getYieldFromChain(samples[sample]['tree'], cut[1],self.weights[sample], returnError=self.err) #,self.nDigits) 
    #               if self.err:
    #                       rounded = [ round(x,self.nDigits) for x in yld ] 
    #                       yld = u_float(*rounded)
    #               else:
    #                       yld = u_float(yld)
    #               self.yieldDictFull[sample][cut[0]] = yld
    #               self.yieldDictRaw[sample].append(yld)
    #           if self.verbose:  print sample, self.yieldDictRaw[sample]
    #       self.yieldDictRaw['Total']    = [ sum(x).round(self.nDigits) for x in zip(*[self.yieldDictRaw[sample] for sample in self.bkgList])    ]
    #       #self.yieldDictRaw['Total']    = [ round(x,self.nDigits) for x in self.yieldDictRaw['Total'] ]
    #       self.yieldDict={}
    #       for sample in self.sampleList:
    #           self.yieldDict[sample]            = np.array( [samples[sample]['name']] +self.yieldDictRaw[sample],dtype='|S20' ) 
    #       self.yieldDict["Total"]         = np.array(["Total"]+ self.yieldDictRaw['Total'],dtype='|S20')
    #       self.yields = np.concatenate( [ [self.yieldDict[t]] for t in self.bkgList +['Total'] + self.sigList ] )
    #       self.table    = np.concatenate( [ self.cutLegend , self.yields ] )
    #       if self.sigList and self.bkgList:
    #           for sig in self.sigList:
    #                   #sig = self.sigList[0] #### need to fix for multiple signals
    #                   #self.yieldDict["FOM"]             = np.array(["FOM"]+ [ round(calcFOMs(self.yieldDictRaw[sig][ic] , self.yieldDictRaw["Total"][ic] ,0.2,"AMSSYS" ),2 )
    #                   #                                    for ic, cut in enumerate(self.cutList) ] , dtype='|S8')
    #                   self.yieldDict["FOM_%s"%sig]             = np.array(["FOM_%s"%samples[sig]['name'] ]+ [ round(calcFOMs( self.yieldDictRaw[sig][ic] , self.yieldDictRaw["Total"][ic] , 0.2, "AMSSYS"), 3 )
    #                                                                for ic, cut in enumerate(cutList) ] , dtype='|S20')
    #           self.FOM = np.concatenate( [ [self.yieldDict[t]] for t in self.bkgList +['Total'] + self.sigList + ['FOM_%s'%x for x in self.sigList] ] )
    #           self.FOMTable = np.concatenate( [ self.cutLegend , self.FOM ] )


    def pickle(self,pklOpt,pklDir):
        if self.pklOpt==1:
            pickle.dump(self,open(pklDir+"YieldInstance_%s.pkl"%self.tableName,"wb"))
            print "Yield Instance pickled in    %s"%"YieldInstance_%s.pkl"%self.tableName
        if self.pklOpt==2:
            pickle.dump(self.table,open(pklDir+"YieldTable_%s.pkl"%self.tableName,"wb"))
            print "Yield Table pickled in    %s"%"YieldTable_%s.pkl"%self.tableName
        if self.pklOpt==3:
            pickle.dump(self.table,open(pklDir+"YieldTable_%s.pkl"%self.tableName,"wb"))
            pickle.dump(self,open(pklDir+"YieldInstance_%s.pkl"%self.tableName,"wb"))
            print "Yield Instance pickled in    %s"%"YieldInstance_%s.pkl"%self.tableName
            print "Yield Table pickled in    %s"%"YieldTable_%s.pkl"%self.tableName
    def __sizeof__(self):
        return object.__sizeof__(self) + \
            sum(sys.getsizeof(v) for v in self.__dict__.values())

    def makeLatexTable(self,table=None):
        if table is None:
            table = self.FOMTable
        ret = " \\\\\n".join([" & ".join(map(str,line)) for line in table])
        print ret
        return ret

    def pprint(self, table=None,transpose=True, nSpaces=17, align="<", ret=None):
        if table is None:
            table = self.FOMTable.T
        block = "| {:%s%s}"%(align,nSpaces)
        #ret = [( block*len(line) ).format(*map(lambda x: "%s"%x,line)) for line in a.T]
        ret = [( block*len(line) ).format(*line) for line in table]
        print ret
        if ret:
            return ret

def decide_weight( sample, weight):
    if sample.isData:
        weight_str = "(1)"
        return weight_str
    if "weight" in weight.lower():
        if sample.has_key("weight"):
            weight_str = sample['weight']
        if weight.endswith("_weight"):
            if sample.has_key(weight):
                weight_str = sample[weight]
                #print sample, weight_str, samples[sample]
    else:
        weight_str=weight
    return weight_str

###########################################################################################################################
###########################################################################################################################
#########################################        TABLES         ###########################################################
###########################################################################################################################
###########################################################################################################################

def fix(x):
    return str(x).replace("_","-").replace("+-","$\pm$").replace("-+","$\mp$").replace(">","$>$")

def fixForLatex(x):
  if type(x)==type(""):
    return fix(x)
  if type(x) in [ type([]), type(()) ] : 
    return [fix(ix) for ix in x]
  if type(x) in [ type(np.array([])) ]:
    return np.array([ fix(ix) for ix in x ])

class JinjaTexTable():
    def __init__(self,yieldInstance, yieldOpt=None, texDir="./tex/", pdfDir="./tex/", outputName="",\
                 searchpath=cmsbase+"/src/Workspace/DegenerateStopAnalysis/python/navidTools/LaTexJinjaTemplates", template_file= "", tableNum=1, caption="", title="", transpose=False):
        if not template_file:
            template_file = "LaTexTemplateWithFOM_v2.j2.tex"
        self.tableNum       = tableNum
        self.caption        = caption
        self.title          = title
        self.template_file  = template_file 
        self.searchpath     = searchpath
        self.pdfDir         = pdfDir
        self.texDir         = texDir
        self.yields         = yieldInstance
        if not outputName:
            self.outputName = self.yields.tableName+".tex"
        else: 
            self.outputName = outputName

        templateLoader = jinja2.FileSystemLoader( searchpath=self.searchpath )

        #yieldDict ={
        #            "y": self.yields,
        #            "table":self.yields.table.T,
        #            "yields":self.yields.yields.T,
        #            "colLegend" : [ x[0] for x in yields.table[1:] ],
        #            "rowLegend" : [x for x in yields.table[0][1:]],
        #            }

        self.templateEnv = jinja2.Environment( 
                      #"%<", ">%",
                      #"<<", ">>",
                      #"<#", "",
                      block_start_string = '\BLOCK{',
                      block_end_string = '}',
                      variable_start_string = '\VAR{',
                      variable_end_string = '}',
                      comment_start_string = '\#{',
                      comment_end_string = '}',
                      #line_statement_prefix = '%-',
                      #line_comment_prefix = '%#',
                      trim_blocks = False,
                      #autoescape = True,
                      loader=templateLoader )
        self.templateEnv.filters['fixForLatex']=fixForLatex
        self.templateEnv.filters['fix']= fix

        ylds = self.yields
        self.info     = {
                             "LatexTitles"  :     {},
                             "T":transpose,
                             "":"",
                        }
                           # "yieldDict" : yields.yieldDictFull, 
                           # "bkgList"   :yields.bkgList, 
                           # "sigList"   : yields.sigList, 
                           # "fomList"   : yields.fomList , 
                           # "cutNames"  : yields.cutNames, 
                           # "transpose" :False, 
                           # "TAB"       :self.tableNum, 
                           #  "CAPTION"  :self.caption,

        if not yieldOpt:
            yieldDict = ylds.getNiceYieldDict()
        elif hasattr(yieldOpt,"__call__") :
            yieldDict = yieldOpt(ylds)
        else:
            yieldDict = getattr(ylds, yieldOpt)

        if transpose:
            self.info.update( {
                             "yieldDict"      :     yieldDict,  
                             "rowList"        :     ylds.sampleLegend,
                             "colList"        :     ylds.cutNames ,
                             "title"          :     self.title,
                             "caption"        :     self.caption,
                             #"fomList"   : yields.fomList , 
                                })
        else:
            self.info.update( {
                             "yieldDict"      :     ylds.getByBins(yieldDict) ,
                             "rowList"        :     ylds.cutNames ,
                             "colList"        :     ylds.sampleLegend,
                             "title"          :     self.title,
                             "caption"        :     self.caption,
                            })

        self.makeTable(self.yields,self.outputName, self.info) 

        #if transpose == "both":
        #    self.makeTable(self.yields,self.outputName self.info) 
        #    self.makeTable(self.yields,self.outputName self.info) 

    def makeTable(self,yields, outputName, info, removeJunk = True):
        texTemplate = self.templateEnv.get_template( self.template_file )
        makeDir(self.texDir)  
        self.outputTex = self.texDir + outputName
        self.fout=open(self.outputTex,"w")
        #self.out = texTemplate.render( yields=self.yields, yieldTable=self.yields.FOMTable.T, TAB=self.tableNum, CAPTION=self.caption)
        self.out = texTemplate.render( 
                                        ##yieldDict= yields.yieldDictFull, 
                                        #yieldDict= yields.getByBins( yields.makeYieldDictNice( yields.yieldDictFull  ) ), 
                                        #bkgList=yields.bkgList, 
                                        #sigList = yields.sigList, 
                                        #fomList = yields.fomList , 
                                        #cutNames = yields.cutNames,
                                        #LatexTitles = yields.LatexTitles,
                                        #transpose=False,
                                        #TAB=self.tableNum, 
                                        #CAPTION=self.caption
                                        **info
                                    )
        print(self.out)
        self.fout.write( self.out)
        self.fout.close()
        print "LaTex File:", self.texDir+outputName
        os.system("pdflatex -output-directory=%s %s"%(self.pdfDir,self.outputTex))

        if removeJunk:
            out = self.pdfDir+"/"+outputName
            print "output:", self.outputTex
            os.system("rm %s"%out.replace(".tex",".aux"))            
            os.system("rm %s"%out.replace(".tex",".log"))     

#############################################################################################################
##########################################                    ###############################################
##########################################    EVENT LISTS     ###############################################
##########################################                    ###############################################
#############################################################################################################

import hashlib

def getEventListFromFile(eListName,tmpDir=None,opt="read"):
  if opt.lower() in ["read","r"]:
    eListPath="%s/%s.root"%(tmpDir,eListName)
    f=ROOT.TFile(eListPath,"open") 
    eList = f.Get(eListName)
    eList.SetDirectory(0) 
  return eList

def getEventListFromChain(sample,cut,eListName="",tmpDir=None,opt="write"):
  if not tmpDir:
    tmpDir = os.getenv("CMSSW_BASE")+"/src/Workspace/DegenerateStopAnalysis/plotsMateusz/tmp"
    if not os.path.exists(tmpDir): os.makedirs(tmpDir)

  if not eListName or eListName.lower()=="elist" : 
    print "WARNING: Using Default eList Name, this could be dangerous! eList name should be customized by the sample name and cut" 
    eListName="eList" 
  sample.SetEventList(0) 
  sample.Draw(">>%s"%eListName,cut) 
  eList=ROOT.gDirectory.Get(eListName)
  if opt.lower() in ["write", "w", "save", "s" ]:
    eListPath="%s/%s.root"%(tmpDir,eListName)
    f = ROOT.TFile(eListPath,"recreate")
    eList.Write()
    f.Close()
    print "EventList saved in: %s"%eListPath
  return eList

def setEventListToChain(sample,cut,eListName="",verbose=True,tmpDir=None,opt="read"): 
  if not tmpDir:
    tmpDir = os.getenv("CMSSW_BASE")+"/src/Workspace/DegenerateStopAnalysis/plotsMateusz/tmp"
    if not os.path.exists(tmpDir): os.makedirs(tmpDir)

  eListPath="%s/%s.root"%(tmpDir,eListName)

  if opt.lower() in ["read","r"]: 
    if os.path.isfile(eListPath):
      eList = getEventListFromFile(eListName=eListName,tmpDir=tmpDir,opt=opt)
    else:
      print "eList was not found in:%s "%eListPath
      opt="write"
  if opt.lower() in ["make","m","write", "w","s","save"] : 
    if True: print " "*12, "Creating EList", eListName 
    eList = getEventListFromChain(sample,cut,eListName,tmpDir=tmpDir,opt=opt)
  if verbose: print " "*12, "Setting EventList to Chain: ", sample, "Reducing the raw nEvents from ", sample.GetEntries(), " to ", 
  sample.SetEventList(eList) 
  assert eList.GetN() == sample.GetEventList().GetN() 
  return eList

def setEventListToChains(samples,sampleList,cutInst,verbose=True,opt="read"):
  if cutInst:
    if isinstance(cutInst,CutClass) or hasattr(cutInst,"combined"):
      cutName   = cutInst.name
      cutString = cutInst.combined
    else:
      cutName, cutString = cutInst
    if verbose:
      print "Setting Eventlists Using cut:"
      print cutName, cutString
      print "Applying to samples in: %s"%sampleList
    for sample in sampleList:
      eListName="eList_%s_%s"%(sample,cutName)
      if samples[sample].has_key("dir"):
        stringToBeHashed = "/".join( [samples[sample]['dir']] + sorted(samples[sample]['sample']['bins'])+ [cutString] ) 
        sampleHash = hashlib.sha1(stringToBeHashed).hexdigest()
        eListName +="_%s"%sampleHash
      setEventListToChain(samples[sample]['tree'],cutString,eListName=eListName,verbose=False,opt=opt)
      if verbose:
        if samples[sample]['tree'].GetEventList():
          print " "*6 ,"Sample:", sample,   "Reducing the raw nEvents from ", samples[sample]['tree'].GetEntries(), " to ", samples[sample]['tree'].GetEventList().GetN()
        else:
          print "FAILED Setting EventList to Sample", sample, samples[sample]['tree'].GetEventList() 
        print " "*12, "eListName:" , eListName
  else:
    print "No cut -> No EventList was set to samples" 

#############################################################################################################
##########################################                    ###############################################
##########################################      LIMITS        ###############################################
##########################################                    ###############################################
#############################################################################################################

from Workspace.DegenerateStopAnalysis.cardFileWriter import cardFileWriter
from Workspace.DegenerateStopAnalysis.navidTools.FOM import get_float

from os.path import basename, splitext

#pickleFiles = ["/afs/hephy.at/user/n/nrad/CMSSW/CMSSW_7_4_7/src/Workspace/DegenerateStopAnalysis/plotsNavid/analysis/pkl/SR1_r1_a.pkl"]

def getLimit(yld, sig=None , outDir ="./cards/", postfix = "", sys_uncorr=1.2, sys_corr = 1.06, calc_limit=False):
    c = cardFileWriter()
    c.defWidth=40
    c.maxUncNameWidth=40
    c.maxUncStrWidth=40
    c.precision=6
    c.addUncertainty("Sys", 'lnN')

    #bins = yld.cutLegend[0][1:]
    bins = yld.cutNames
    bkgs = yld.bkgList

    if not sig:
        sig  = yld.sigList[0]
    elif sig in yld.sigList:
        pass
    else:
        assert False, "Signal %s not in the yield dictionary signal list:%s" %(sig, yld.sigList)

    #processNames = { bkg:yld.yieldDictFull[bkg][0] for bkg in bkgs}
    processNames = yld.sampleNames
    #processNames.update(  { sig:yld.yieldDictFull[sig][0] } )
    #processNames.update(  { sig:'signal'} )
    processNames.update(  { 'signal':'signal'} )

    for iBin, bin in enumerate(bins,1):
        c.addBin(bin,[processNames[bkg] for bkg in bkgs],bin)
        c.specifyObservation(bin,int( get_float(yld.yieldDictFull["Total"][bin]) ))
        sysName = "Sys_%s"%(bin)
        c.addUncertainty(sysName, 'lnN')
        c.addUncertainty(sysName+"_sig", 'lnN')
        for bkg in bkgs:
          c.specifyExpectation(bin,processNames[bkg],get_float(yld.yieldDictFull[bkg][bin]))
          c.specifyUncertainty('Sys',bin,processNames[bkg],sys_corr)
          #sysName = "Sys_%s"%bkg
          c.specifyUncertainty(sysName,bin,processNames[bkg],sys_uncorr)
        c.specifyExpectation(bin,"signal",get_float(yld.yieldDictFull[sig][bin]))
        c.specifyUncertainty(sysName+"_sig",bin,'signal',sys_uncorr)
        #c.specifyUncertainty('Sys',bin,"signal",sys_corr)
    badBins=[]
    #if True:
    #  return c
    print "--------debug-------------"
    print c.bins
    print c.processes
    print c.expectation
    print "--------debug-------------"

    for bin in c.bins:
        expectations = [c.expectation[( bin, process )] for process in c.processes[bin]]
        bkgExpectations = [ c.expectation[(bin,processNames[process])] for process in bkgs]
        print bin, any(expectations), c.processes[bin], expectations
        if not any(expectations):
          print "############ no processes contributing to the bin %s, to make life easier the bin will be removed from card but make sure everything is ok"%bin
          print bin, c.processes[bin], expectations
          badBins.append(bin)
          #print c.bins
        if not any(bkgExpectations):
          print "############ no background contributing to the bin %s, a small non zero value (0.001) has been assigned to the bin"%bin
          c.expectation[(bin,process[bkgs[0]])]=0.001
          print bin, c.processes[bin], expectations

    for bin in badBins:
        c.bins.remove(bin)

    #sigName  =  yld.yieldDictFull[sig][0]
    sigName  =  yld.sampleNames[sig]
    filename =  sigName + "_" + yld.tableName
    if postfix:
        if not postfix.startswith("_"):
            postfix = "_" + postfix
        filename += postfix

    cardName='%s.txt'%filename
    c.writeToFile('%s/%s'%(outDir,cardName))
    print "Card Written To: %s/%s"%(outDir,cardName)
    #limits=c.calcLimit("./output/%s"%cardName)
    if calc_limit: limits=c.calcLimit()
    #print cardName,   "median:  ", limits['0.500']
    return (c, limits)

def plotLimits(limitDict):
  nLimits = len(limitDict)
  limitPlot = ROOT.TH1F("limitPlot","limitPlot",nLimits,0,nLimits)
  for i,fname in enumerate(sorted(limitDict, key=natsort_key),1):
    limit=limitDict[fname][1]['0.500']
    limitPlot.GetXaxis().SetBinLabel(i,fname)
    limitPlot.SetBinContent(i,limit)

  limitPlot.GetYaxis().SetTitle("r")
  limitPlot.SetTitle("Median Expected Limits")
  return limitPlot

def drawExpectedLimit( limitDict, plotDir, bins=None, key=None , title=""):
    saveDir = plotDir

    if type(limitDict)==type({}):
        limits = limitDict
    elif type(limitDict)==type("") and limitDict.endswith(".pkl"):
        limits = pickle.load(open(limitDict, "r"))
    else:
        raise Exception("limitDict should either be a dictionary or path to a picke file")

    if not bins:
        #bins = [13,87.5,412.5, 75, 17.5, 392.5 ]
        bins = [23,87.5,662.5, 127 , 17.5, 642.5]

    if not key:
        key = getValueFromDict

    plot = makeStopLSPPlot("Exclusion", limits, bins=bins, key=key )

    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPaintTextFormat("0.2f")

    #levels = array("d",[0,1,10])
    #nLevels = len(levels)
    #plot.SetContour(nLevels, levels)

    plot.SetContour(2 )
    plot.SetContourLevel(0,0 )
    plot.SetContourLevel(1,1 )
    plot.SetContourLevel(2,10 )

    #output_name = os.path.splitext(os.path.basename(limit_pickle))[0]+".png"

    #c1 = ROOT.TCanvas("c1","c1",1910,1070)
    c1 = ROOT.TCanvas("c1","c1",1500,1026)
    plot.Draw("COL TEXT")
    if title:
        ltitle = ROOT.TLatex()
        ltitle.SetNDC()
        ltitle.SetTextAlign(12)
        #ytop = 1.05- canv.GetTopMargin()
        #ltitle_info = [0.1, ytop]
        ltitle.DrawLatex(0.2, 0.8, title  )
    c1.Update()
    c1.Modify()
    #c1.SaveAs("/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2/reload_scan_isrweight/%s"%output_name)
    if plotDir:
        c1.SaveAs(plotDir)
        return c1,plot
    else:
        return c1,plot

def getValueFromDict(x, val="0.500", default=999):
    try:
        ret = x[1][val]
    except KeyError:
        ret = default
    #else:
    #    raise Exception("cannot find value %s in  %s"%(val, x))
    return float(ret)

