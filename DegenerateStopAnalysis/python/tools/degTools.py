import ROOT
import os,sys
import math
import pickle
import numpy as np
import glob
import jinja2
import pprint as pp
import time
import hashlib
from copy import deepcopy

from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.tools.ratioTools import *
from Workspace.DegenerateStopAnalysis.tools.FOM import *

import Workspace.DegenerateStopAnalysis.tools.colors as sample_colors_
sample_colors = sample_colors_.colors

from Workspace.HEPHYPythonTools.u_float import u_float


import multiprocessing 
import itertools

import re
import gc

#execfile('/afs/hephy.at/user/n/nrad/CMSSW/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/python/tools/FOM.py')
#execfile('../../../python/tools/getRatioPlot.py')
#reload(Workspace.DegenerateStopAnalysis.tools.getRatioPlot)

cmsbase = os.getenv("CMSSW_BASE")
def setup_style(cmsbase=cmsbase):
    print "CMSBASE", cmsbase
    ROOT.gROOT.LoadMacro(cmsbase+"/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
    ROOT.setTDRStyle()
    ROOT.gStyle.SetErrorX(0.5)
    maxN = -1
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPalette(1)
    return cmsbase
#ROOT.gStyle.SetCanvasPreferGL(1)

#pp=prettyprint.PrettyPrinter(indent=3, depth=5, width=120)


#############################################################################################################
##########################################                    ###############################################
##########################################    ETC  TOOLS      ###############################################
##########################################                    ###############################################
#############################################################################################################


getAllAlph = lambda str: ''.join(ch for ch in str if ch not in ".!>=|<$&@$%[]{}#()/; '\"")
addSquareSum = lambda x: math.sqrt(sum(( e**2 for e in x   )))
any_in = lambda a, b: any(i in b for i in a)

anyIn = any_in

def whichIn(of_these, this):
    rets = []
    for thing in of_these:
        if thing in this:
            rets.append(thing)
    return rets

canvas_2d_size=(1500,1026)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        #if exc.errno == errno.EEXIST and os.path.isdir(path):
        if os.path.isdir(path):
            pass
        else:
            raise

def set_dict_key_val(d,key, val ):
    try:
        d[key]
    except KeyError:
        d[key]=val

def get_basename (f):
    return os.path.basename(f)
def get_filename (f):
    return os.path.splitext(os.path.basename(f))[0]
def get_ext (f):
    return os.path.splitext(os.path.basename(f))[1]

def makeDir(path):
    if "." in path[-5:]:
        path = path.replace(os.path.basename(path),"")
        print path
    if os.path.isdir(path):
        return
    else:
        mkdir_p(path)

def saveCanvas(canv,dir="./",name="",formats=["png"], extraFormats=["root","C","pdf"] , make_dir=True):
    if not os.path.isdir(dir) and make_dir: 
        makeDir(dir)
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


import collections # requires Python 2.7 -- see note below if you're using an earlier version
def merge_dict(d1, d2):
    """
    Modifies d1 in-place to contain values from d2.  If any value
    in d1 is a dictionary (or dict-like), *and* the corresponding
    value in d2 is also a dictionary, then merge them in-place.
    stolen from: http://stackoverflow.com/questions/10703858/python-merge-multi-level-dictionaries
    """
    for k,v2 in d2.items():
        v1 = d1.get(k) # returns None if v1 has no value for this key
        if ( isinstance(v1, collections.Mapping) and 
             isinstance(v2, collections.Mapping) ):
            merge_dict(v1, v2)
        else:
            d1[k] = v2


def getTerminalSize():
    """
    stolen from the consule module
    http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    """
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])



def uniqueHash():
    return hashlib.md5("%s"%time.time()).hexdigest()    



def get_index(string,by, strict = True):
    if strict:
        sort_indices = [ i1 ==  string for i1 in by ]
    else:
        sort_indices = [ i1 in  string for i1 in by ]
    try:
        return sort_indices.index(True)  
    except ValueError:
        return -1

def sortBy(l,by_l1 , reverse = True):
    return sorted(l , key = lambda x:  get_index(x,by_l1)   , reverse=reverse ) ## ordering first by bin, then by processes 

############################################################################################################

import argparse

def get_args(sys_args):
    """ Setup the command line options. """
    #if 'ipython' in sys_args[0].lower():
    #    sys_args = sys_args[sys_args.index("--")+1:]
    #else: 
    #    if "--" in sys_args: sysarg.remove("--")
    #    sys_args = sys_args[1:]

    print sys_args
                
    description = ''' 
        Basic function to be imported for simple and quick arg 
        '''
    #parser = argparse.ArgumentParser(argument_default=sys_args, description=description)
    parser = argparse.ArgumentParser( description=description)


    parser.add_argument('-s', '--sampleList', nargs='+', 
                                     #default=["s30","w","tt"], help='Input Samples')
                                     default=[],
                                     help='Input Samples')

    parser.add_argument('-c', '--cutInst',  
                                     default="sr1Loose", help='Instance of CutClass To be Used')

    parser.add_argument('-p', '--process', action="store_true", 
                                      help='Do stuff or not')
    parser.add_argument('-ht', '--useHT', action="store_true", 
                                      help='Use HT binned samples')

    #return parser.parse_args(sys_args)
    return parser

class ArgParser(argparse.ArgumentParser):
    def parse(self, sys_args, setdef=True):
        self.sys_args = self._fix_args(sys_args)
        if setdef:
            self.add_argument('-s', '--sampleList', nargs='+',
                                         help='input Samples')
            self.add_argument('-p', '--process', action="store_true",
                                          help='input Samples')
            self.add_argument('-c', '--cutInst',  
                                         default="sr1Loose", help='Instance of CutClass To be Used')
            self.add_argument('-ht', '--useHT', action="store_true", 
                                          help='Use HT binned samples')

        parsed = self.parse_known_args(self.sys_args)
        if parsed[1]:
            print "Some Options were not recognized:", parsed
        return parsed[0]

    def _fix_args(self, sys_args):
        if 'ipython' in sys_args[0].lower() and "--" in sys_args:
            sys_args = sys_args[sys_args.index("--")+1:]
        else: 
            if "--" in sys_args: sys_args.remove("--")
            sys_args = sys_args[1:]
        return sys_args


#############################################################################################################
##########################################                    ###############################################
##########################################   UNCERTAINTIES    ###############################################
##########################################                    ###############################################
#############################################################################################################


import itertools
def addInQuad(l):
    s = 0
    for v in l:
        s += v**2
    return math.sqrt(s) 
def addInQuad100PerctCorr(l):
    s = 0
    for v in l:
        s += v**2
    chi = 0
    for e1,e2 in itertools.combinations(l,2):
        print e1,e2
        chi += e1*e2
    chi = 2*chi
    print 'math.sqrt(%s+%s)'%(s,chi)
    return math.sqrt(s+chi) 








#############################################################################################################
##########################################                    ###############################################
##########################################    EVENT LISTS     ###############################################
##########################################                    ###############################################
#############################################################################################################


def setMVASampleEventList(samples, sample, killTrain = False):
        if not ( hasattr( samples[sample], 'cut' ) and samples[sample]['cut'] ) :
                return
        cuts = [ samples[sample].cut ]
        if killTrain:
                cuts.append("!trainingEvent")
        cutStr = "&&".join("(%s)"%cut for cut in cuts )
        cutInst = CutClass( samples[sample].name, [[ samples[sample].name, cutStr ]] , baseCut = None )
        setEventListToChains( samples, [sample], cutInst , verbose=False)
        return

def getEventListFromFile(eListName,tmpDir=None,opt="read"):
    if opt.lower() in ["read","r"]:
        eListPath="%s/%s.root"%(tmpDir,eListName)
        f=ROOT.TFile(eListPath,"open") 
        eList = f.Get(eListName)
        eList.SetDirectory(0) 
    return eList

def getEventListFromChain(sample,cut,eListName="",tmpDir="./",opt="write", verbose=True):
    if not eListName or eListName.lower()=="elist" : 
        print "WARNING: Using Default eList Name, this could be dangerous! eList name should be customized by the sample name and cut" 
        eListName="eList" 
    sample.SetEventList(0) 
    sample.Draw(">>%s"%eListName,cut) 
    eList=ROOT.gDirectory.Get(eListName)
    if opt.lower() in ["write", "w", "save", "s" ]:
        eListPath="%s/%s.root"%(tmpDir,eListName)
        if verbose: print "EventList saved in: %s"%eListPath
        f = ROOT.TFile(eListPath,"recreate")
        eList.Write()
        f.Close()
    return eList

def setEventListToChain(sample,cut,eListName="",verbose=True,tmpDir=None,opt="read"): 
    if not tmpDir:
        tmpDir = os.getenv("CMSSW_BASE")+"/src/Workspace/DegenerateStopAnalysis/tmp/"
    eListPath="%s/%s.root"%(tmpDir,eListName)
    if opt.lower() in ["read","r"]: 
        if os.path.isfile(eListPath):
            eList = getEventListFromFile(eListName=eListName,tmpDir=tmpDir,opt=opt)
        else:
            if verbose: print "eList was not found in:%s "%eListPath
            opt="write"
    if opt.lower() in ["make","m","write", "w","s","save"] : 
        if verbose: print " "*12, "Creating EList", eListName 
        eList = getEventListFromChain(sample,cut,eListName,tmpDir=tmpDir,opt=opt)
    if verbose: print " "*12, "Setting EventList to Chain: ", sample, "Reducing the raw nEvents from ", sample.GetEntries(), " to ", 
    sample.SetEventList(eList) 
    assert eList.GetN() == sample.GetEventList().GetN() 
    return eList

def setEventListToChains(samples,sampleList,cutInst,verbose=True,opt="read"):
    if cutInst:
        if isinstance(cutInst,CutClass) or hasattr(cutInst,"combined"):
            cutName     = cutInst.fullName
        else:
            cutName, cutString = cutInst
        if verbose:
            #print "Setting Eventlists Using cut: %s        :"%cutName
            #print cutString
            pp.pprint( "Applying EventLists to samples in: %s"%sampleList)
        for sample in sampleList:
            if not sample in samples.keys(): 
                print "Sample %s not in samples.keys()"%sample
                continue
            cutString = decide_cut( samples[sample], cutInst, plot=None, nMinus1=None    )
            if verbose:
                pp.pprint( "     applying cut %s: "%cutString)
            eListName="eList_%s_%s"%(sample,cutName)
            stringsToBeHashed = [] 
            if samples[sample].has_key("dir"):
                stringsToBeHashed =    [samples[sample]['dir']]    
            if samples[sample].get("sample"): # and samples[sample]['sample'] :
                stringsToBeHashed.extend( sorted( samples[sample]['sample']['bins'] )    )
            stringsToBeHashed.append( cutString    )
            #print stringsToBeHashed

            stringToBeHashed = "/".join(stringsToBeHashed)
            sampleHash = hashlib.sha1(stringToBeHashed).hexdigest()
            eListName +="_%s"%sampleHash
            setEventListToChain(samples[sample]['tree'],cutString,eListName=eListName,verbose=False,opt=opt)
            if verbose:
                if samples[sample]['tree'].GetEventList():
                    if verbose: print " "*6 ,"Sample:", sample,     "Reducing the raw nEvents from ", samples[sample]['tree'].GetEntries(), " to ", samples[sample]['tree'].GetEventList().GetN()
                else:
                    print "FAILED Setting EventList to Sample", sample, samples[sample]['tree'].GetEventList() 
                if verbose: print " "*12, "eListName:" , eListName
    else:
        for sample in sampleList:
                if not sample in samples.keys(): 
                    print "Sample %s not in samples.keys()"%sample
                    continue
                samples[sample]['tree'].SetEventList(0)
        print "no cut... EventList set to 0" 
        #print "no cut... no EventList was set to samples" 

#############################################################################################################
##########################################                    ###############################################
##########################################    DECORATOION     ###############################################
##########################################                    ###############################################
#############################################################################################################

def decorHist(samp,cut,hist,decorDict):
    dd=decorDict
    if dd.has_key("title"):
        title = dd['title']
        title = title.format(CUT=cut.fullName, SAMP=samp.name )
        hist.SetName(getAllAlph(samp.name+"_"+cut.fullName+"_"+dd["title"]))
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
    if dd.has_key("style") and dd['style']:
        hist.SetLineStyle( dd['style'] )
        hist.SetMarkerStyle(0)
    elif samp.isData:
        pass
    else:
        #print "default color used for:", samp.name # , cut, hist, decorDict
        pass
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

def getStackFromHists(histList,sName=None,scale=None, normalize=False, transparency=False):
  print "::::::::::::::::::::::::::::::::::::::::::: GETTIN STACKS" , sName
  if not sName:
    sName = "stack_%s"%uniqueHash()
  stk=ROOT.THStack(sName,sName)

  if transparency:
    alphaBase=0.80
    alphaDiff=0.70
    alphas=[alphaBase-i*alphaDiff/len(histList) for i in range(len(histList)) ]
    print alphas
    print histList

  for i, hist in enumerate(histList):
    #h = hist.Clone()
    h = hist

    #  h.ClearUnderflowAndOverflow()  remove for efficiecy plots
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

def getSamplePlots(samples,plots,cut,sampleList=[],plotList=[],plots_first = False):
    cut_name = cut if type(cut) == type("") else cut.fullName
    if not sampleList: sampleList= samples.keys()
    bkgList=[samp for samp in sampleList if not samples[samp]['isSignal'] and not samples[samp]['isData'] ]
    dataList = [samp for samp in sampleList if samples[samp]['isData'] ]
    sigList=[samp for samp in sampleList if samples[samp]['isSignal'] ]
    if not plotList: plotList=plots.keys()
    hists={}

    if plots_first:
        for p in plotList:
            hists[p]={}
            for samp in sampleList:
                hists[p][samp]= samples[samp]['cuts'][cut_name][p]
    else:
        for samp in sampleList:
            hists[samp]={}
            for p in plotList:
                hists[samp][p]= samples[samp]['cuts'][cut_name][p]
    return hists

def getSamplePlotsInfo(samples,plots,cut,sampleList=[],plotList=[],plots_first = False):
    cut_name = cut if type(cut) == type("") else cut.fullName
    if not sampleList: sampleList= samples.keys()
    bkgList=[samp for samp in sampleList if not samples[samp]['isSignal'] and not samples[samp]['isData'] ]
    dataList = [samp for samp in sampleList if samples[samp]['isData'] ]
    sigList=[samp for samp in sampleList if samples[samp]['isSignal'] ]
    if not plotList: plotList=plots.keys()
    hists={}
    if plots_first:
        for p in plotList:
            hists[p]={}
            for samp in sampleList:
                hists[p][samp]= getattr( samples[samp]['cuts'][cut_name][p], "plot_info", {} )
    else:
        for samp in sampleList:
            hists[samp]={}
            for p in plotList:
                hists[samp][p]= getattr( samples[samp]['cuts'][cut_name][p], "plot_info", {})
    return hists



def getBkgSigStacks(samples, plots, cut, sampleList=[],plotList=[], normalize=False, transparency=None, sName=None):
    """Get stacks for signal and backgrounds. make vars in varlist are available in samples. no stacks for 2d histograms.     """
    cut_name = cut if type(cut) == type("") else cut.fullName

    sampleList    = matchListToDictKeys(sampleList,samples)
    plotList     = matchListToDictKeys(plotList,plots)
    #sampleList=samples.keys()
    #plotList=plots.keys()
    #samples=samples
    bkgStackDict={}
    sigStackDict={}
    dataStackDict={}
    for v in plotList:
        sName_plot = sName + "_%s"%v if sName else None
        if len(plots[v]['bins'])!=6:
            bkgStackDict[v]= getStackFromHists([ samples[samp]['cuts'][cut_name][v] for samp in sampleList if not samples[samp]['isSignal'] and not samples[samp]['isData']], normalize=normalize, transparency=transparency, sName= "stack_bkg_" + sName_plot)
            sigStackDict[v]= getStackFromHists([ samples[samp]['cuts'][cut_name][v] for samp in sampleList if samples[samp]['isSignal']], normalize=normalize, transparency=False, sName= "stack_sig_" + sName_plot)
            dataStackDict[v]=getStackFromHists([ samples[samp]['cuts'][cut_name][v] for samp in sampleList if samples[samp]['isData']], normalize=normalize, transparency=False, sName= "stack_data_" + sName_plot)
    return {'bkg': bkgStackDict,'sig': sigStackDict, 'data': dataStackDict}
  
def getPlot(sample,plot,cut,weight="", nMinus1="",cutStr="",addOverFlowBin='', lumi='target_lumi', verbose= False):
    plot_info = {}
    c     = sample.tree
    var = plot.var
    cut_str, weight_str = decide_cut_weight( sample, cutInst = cut , weight=weight,  lumi=lumi, plot=plot, nMinus1=nMinus1 ,  )
    plot_info = {'cut':cut_str, 'weight':weight_str}

    if verbose: 
        print "\n  Using Weight:            %s "%(weight_str)
        print "\n  And Cut:                 %s"%cut_str

    binningIsExplicit= False
    if not len(plot.bins) in [3,6]:
        if hasattr(plot, "binningIsExplicit"):
            binningIsExplicit = plot.binningIsExplicit
    if type(var) == type(""):
        hist = getPlotFromChain(sample.tree,plot.var,plot.bins,cut_str,weight=weight_str, addOverFlowBin=addOverFlowBin, binningIsExplicit=binningIsExplicit)
    elif hasattr(var, "__call__"):
        hist = var( sample , bins = plot.bins, cutString=cut_str, weight=weight_str, addOverFlowBin=addOverFlowBin, binningIsExplicit=binningIsExplicit)
    else:
        raise Exception("I'm not sure what this variable is! %s"%var)
    #plot.decorHistFunc(p)
    decorHist(sample,cut,hist,plot.decor) 
    plotName=plot.name + "_"+ cut.fullName
    sample.plots[plotName]=hist
    if not sample.has_key("cuts"):
        sample.cuts=Dict()
    if not sample.cuts.has_key(cut.fullName):
        sample.cuts[cut.fullName]=Dict()
    sample.cuts[cut.fullName][plot.name]=hist
    hist.plot_info = plot_info
    return { "%s_%s"%(sample.name,plotName) : plot_info }

def getPlotsSimple(samples,plots,cut):
  for sample in samples.itervalues():
    for plot in plots.itervalues():
      getPlot(sample,plot,cut)


def getPlots(samples,plots,cut,sampleList=[],plotList=[],weight="",nMinus1="", addOverFlowBin='',verbose=True):
    if verbose:print "Getting Plots: "

    sigList, bkgList, dataList = getSigBkgDataLists(samples, sampleList=sampleList)
    isDataPlot = bool(len(dataList))
    print "CUT NAME: ", cut.fullName
    if isDataPlot:
       #if "Blind" in samples[dataList[0]].name and "sr" in cut.fullName.lower():
       #    raise Exception("NO DATA IN SIGNAL REGION: %s"%[dataList, cut.fullName])

       if "DataBlind" in samples[dataList[0]].name: lumi_weight = "DataBlind_lumi"
       elif "DataUnblind" in samples[dataList[0]].name: lumi_weight = "DataUnblind_lumi"
       else: assert False
       print "Reweighting MC histograms to", lumi_weight, ":", round(samples[dataList[0]].lumi/1000.,2), "fb-1"
    else:
       lumi_weight = "target_lumi"
       print "Reweighting MC histograms to", lumi_weight, ":", round(samples[bkgList[0]].weights.weight_dict['lumis']['target_lumi']/1000.,2), "fb-1"

    if len(dataList) > 1:
        raise Exception("More than one Data Set in the sampleList... This could be dangerous: %s"%dataList)
 
    if verbose: print " "*15, "Getting Plots: ", plotList
    for sample in samples.iterkeys():
        #if sample in sampleList or not sampleList:
        if not sample in sampleList:
            continue
        if verbose: print "========= Sample:" , samples[sample].name, 
        #weight_str = decide_weight2(samples[sample] , cut=cut.combined, lumi=lumi_weight)
        #cut_str , weight_str = decide_cut_weight(samples[sample] , cut=cut.combined, lumi=lumi_weight)
        plotList = plotList if plotList else plots.keys()
        for plot in plotList:
            if plot not in plots.keys():
                print "Ignoring %s .... not in the Plot Dictionary"%plot
                continue    
            getPlot(samples[sample],plots[plot],cut  , weight = weight , nMinus1=nMinus1,addOverFlowBin=addOverFlowBin, lumi=lumi_weight, verbose = verbose)

          
def getSigBkgDataLists ( samples, sampleList):
    sigList=[samp for samp in sampleList if samples[samp]['isSignal'] ]
    bkgList=[samp for samp in sampleList if not samples[samp]['isSignal']  and not samples[samp]['isData'] ]
    dataList = [samp for samp in sampleList if samples[samp]['isData'] ]
    return sigList, bkgList, dataList

def makeLegend(samples, hists, sampleList, plot, name="Legend",loc=[0.6,0.6,0.9,0.9],borderSize=0,legOpt="f"):
    leg = ROOT.TLegend(*loc)
    leg.SetName(name)
    leg.SetFillColorAlpha(0,0.001)
    leg.SetBorderSize(borderSize)


    for samp in sampleList:
        samp_name = samples[samp]['name']
        if samp_name in fixDict:
            samp_name = fixDict[samp_name]
        legOpt_ = "lep" if samples[samp]['isData'] else legOpt
        if plot:
            leg.AddEntry(hists[samp][plot], samp_name , legOpt_)    
        else:
            leg.AddEntry(hists[samp], samp_name , legOpt_)    
    return leg

def getPlotFromYields(name, yields, keys=[]):
    if not keys:
        keys = sorted(yields.keys())
    hist_name   = name
    hist        = ROOT.TH1F( name, name, len(keys), 0, len(keys)   )
    graph       = ROOT.TGraph()
    graph_err   = ROOT.TGraphErrors()

    for i, k in enumerate(keys,1):
        v = get_float( yields[k] )
        v_err = get_float( yields[k], sigma=True)
        #hist.SetBinContent(i,v)
        #hist.Fill(k,v)
        hist.SetBinContent(i,v)
        hist.SetBinError(i,v_err)
        hist.GetXaxis().SetBinLabel(i,k)
    hist.GetXaxis().LabelsOption("v")
    return hist  

def drawYields( name , yieldInst, sampleList=[], keys=[], ratios=True, plotMin = 0.01, plotMax= None, logs = [0,1], save="", normalize = False, ratioLimits=[0,1.8]):

    ret=[]
    yld = yieldInst
    if type(yld)==type(""):
        yld = pickle.load( open(yld))

    if hasattr(yld, "yieldDict"):
        if not sampleList:
            sampleList = yld.bkgList
        if not keys:
            keys = yld.cutNames
        bkgList =  [x for x in sampleList if x in yld.bkgList]
        sigList =  [x for x in sampleList if x in yld.sigList]
        dataList = [x for x in sampleList if x in yld.dataList ] 
        yieldDict = yld.yieldDictFull 
    else:
        if not sampleList:
            raise NotImplementedError()
        if not keys:
            raise NotImplementedError()
        bkgList = [x for x in sampleList if x in [ 'Diboson', 'TTJets', 'ST', 'WJets', 'QCD', 'DYJetsM50', 'ZJetsInv' ] + ['dy', 'qcd', 'st', 'tt', 'vv', 'w', 'z'] ]
        sigList = [x for x in sampleList if 'T2tt' in x]
        dataList = [x for x in sampleList if 'data' in x.lower()] 
        yieldDict = yld

    yldplt = {}
    draw = True
    if draw:
        padRatios = [2,1] if ratios else [1,0]
        canvs = makeCanvasMultiPads(c1Name="%s_%s"%("Yields",name),c1ww=800,c1wh=800, joinPads=True, padRatios=padRatios, pads=[]  )
        cSave, cMain = [0,1] if ratios else [0,0]
        canvs[cMain].cd()
        dOpt = "hist"
        canvs[cMain].SetGrid(1,0)
    for sample in sampleList:
        yldplt[sample] = getPlotFromYields(sample+"_"+name, yieldDict[sample], keys=keys)
        if sample in bkgList:
            yldplt[sample].SetFillColor(  sample_colors.get(sample,1)  )
            
        if sample in sigList:
            yldplt[sample].SetLineColor(  sample_colors.get(sample,1)  )
            yldplt[sample].SetMarkerSize(0)
            yldplt[sample].SetMarkerSize(0)

    stacks  = getStackFromHists([yldplt[bkg] for bkg in bkgList])
    bkg_tot = yldplt[bkg].Clone("bkg_tot_%s"%name)
    bkg_tot.Reset()
    bkg_tot.Merge(stacks.GetHists())
    bkg_tot.SetFillStyle(3001)
    bkg_tot.SetFillColor(1)
    bkg_tot.SetMarkerSize(0)

    drawError = True
    if normalize:
        drawError = False
        for bkg in bkgList:
            #yldplt[bkg] = yldplt[bkg].Clone() 
            yldplt[bkg].Divide(bkg_tot)
            #plotMin = 0.001 
            #logs = [ 0 , 1 ] 
    
    if draw:
        stacks.Draw("hist")
        stacks.SetMinimum(plotMin)
        maxval = plotMax if plotMax else stacks.GetMaximum()* ( 1.35 + logs[1]*10  )
        stacks.SetMaximum( maxval)
        if drawError:
            bkg_tot.Draw("same E2")
        
    for sig in sigList:
        yldplt[sig].Draw("same")
    stacks.Draw("same AXIG")

    if dataList and not normalize:
        yldplt[dataList[0]].SetMarkerSize(1)
        yldplt[dataList[0]].Sumw2()
        yldplt[dataList[0]].Draw("same EP0")


    #
    #   Making Legend
    #

    samples = {} # to make make legend happy!
    for samp in bkgList + sigList:
        samples[samp] = {'name':samp, 'isData':False}
    for samp in dataList:
        samples[samp] = {'name':samp, 'isData':True}
        
    bkgLegList = bkgList[:] 
    sigLegList = sigList[:] 
    
    bkgLegList.reverse()
    sigLegList.reverse()
    bkgLegList += dataList
    #bkgLeg = makeLegend(samples, hists, bkgLegList, p, loc=[0.7,0.7,0.87,0.87], name="Legend_bkgs_%s_%s"%(cut.name, p), legOpt="f")
    #bkgLeg.Draw()
    #ret['legs'].append(bkgLeg)
    legy = [0.7, 0.87 ]
    legx = [0.75, 0.95 ]  
    nBkgInLeg = 4
    if any_in(sampleList, bkgLegList):
        subBkgLists = [ bkgLegList[x:x+nBkgInLeg] for x in range(0,len(bkgLegList),nBkgInLeg) ]
        nBkgLegs = len(subBkgLists)
        for i , subBkgList in enumerate( subBkgLists ):
            newLegY0 = legy[0] + (legy[1]-legy[0])* (1-1.*len(subBkgList)/nBkgInLeg)
            bkgLeg = makeLegend(samples, yldplt , subBkgList, None, loc=[legx[0], newLegY0 ,legx[1],legy[1]], name="Legend_bkgs%s_%s_%s"%(i, name, "LEG"), legOpt="f")
            print "==========================================================================="
            print bkgLeg, subBkgList, legx 
            print "==========================================================================="
            ret.append(bkgLeg)
            ret[-1].Draw()
            legx = [ 2*legx[0] -legx[1] , legx[0]  ] 
            #del bkgLeg

    if any_in(sampleList, sigLegList):
       sigLeg = makeLegend(samples, yldplt, sigLegList, None, loc=[legx[0],legy[0],legx[1],legy[1]], name="Legend_sigs_%s_%s"%(name, "LEG"), legOpt="l")
       sigLeg.Draw()
       ret.append(sigLeg)
       ret[-1].Draw()




    canvs[cMain].SetLogx(logs[0])
    canvs[cMain].SetLogy(logs[1])
    canvs[cMain].Update()

    if ratios:
        canvs[cMain+1].cd()
        canvs[cMain+1].SetGrid()
        ratio_ref = bkg_tot.Clone("ratio_ref_%s"%name)
        #ratio_ref.SetError(ar.array( "d",[0]* ratio_ref.GetNbinsX() ) )
        #ratio_ref.Divide(ratio_ref)
        ratio_ref.Reset()
        #if True: ## draw data/MC
        if dataList: ## draw data/MC
            print 'data is here!'
            ratio_ref.Draw("hist")
            ratio_ref.GetYaxis().SetTitle("DATA/MC")
            ratio_ref.GetYaxis().SetLabelSize(0.01)
            ratio_ref.SetMinimum(ratioLimits[0])
            ratio_ref.SetMaximum(ratioLimits[1])    
   
            MCE = bkg_tot.Clone("MCError_%s"%name)
            bkg_tot_noe =  bkg_tot.Clone("bkg_tot_noe_%s"%name)
            bkg_tot_noe.SetError(ar.array( "d",[0]* bkg_tot_noe.GetNbinsX() ) )
            MCE.Divide( bkg_tot_noe  )
            MCE.SetFillStyle(3001)
            MCE.SetFillColor(1)
            MCE.SetMarkerSize(0)
            MCE.Draw("e2same")
        
            data_ratio = yldplt[dataList[0]].Clone()
            data_ratio.Divide(bkg_tot_noe)
            data_ratio.Draw("e0same")

            ret.extend([bkg_tot_noe, MCE, data_ratio])
            #    bkg_tot = hists['bkg'][plot].Clone("bkg_tot")
            #    bkg_tot.SetError(ar.array( "d",[0]*nBins ) )    # bkg_tot with no error
            #    data_ratio = hists[dataList[0]][plot].Clone("data")
            #    #data_ratio.Divide(bkg_tot)
            #    #data_ratio.Draw("e")

            #    MCE = hists['bkg'][plot].Clone("MCError_%s"%( hists['bkg'][plot].GetName() )  ) ## bkg_tot with error
            #    MCE.Divide( bkg_tot)
            #    MCE.SetFillStyle(3001)
            #    MCE.SetFillColor(1)
            #    MCE.SetMarkerSize(0)
            #    MCE.Draw("e2same")
            #    ret['junk'].append(MCE)

            pass

        elif sigList: ## draw Sig/BKG fom
            fomtype = "AMSSYS"            
            ratio_ref.GetYaxis().SetTitle(fomtype+"     ")
            ratio_ref.Divide(ratio_ref)
            ratio_ref.Draw("hist")
            ratio_ref.SetMaximum(2.9)    
            ratio_ref.SetMinimum(0)    
            for sig in sigList:
                fomplt = "FOM_%s"%sig
                yldplt[fomplt] = getFOMFromTH1FIntegral( yldplt[sig], bkg_tot , fom =fomtype, integral=False )
                yldplt[fomplt].Draw("same")

        ratio_ref.SetNdivisions(505, "y")
        

        ratio_ref.GetXaxis().SetLabelSize(0.08)
        ratio_ref.GetYaxis().SetLabelSize(0.12)
        ratio_ref.GetYaxis().SetTitleOffset(0.75)
        #canvs[0].SetTopMargin(0.05)
        #canvs[1].SetTopMargin(0.05)
        #canvs[2].SetTopMargin(0.05)
        #canvs[0].SetBottomMargin(0.5)
        #canvs[1].SetBottomMargin(0.5)
        canvs[2].SetBottomMargin(0.5)
        canvs[cMain+1].Update()
    else:
        ratio_ref = None

    if save:
        saveCanvas(canvs[cSave], dir = save, name = name ) 
        canvs[cSave]
    #gc.collect()
    return canvs, yldplt, stacks, bkg_tot, ratio_ref, ret 

#                bkg_tot = hists['bkg'][plot].Clone("bkg_tot")
#                bkg_tot.SetError(ar.array( "d",[0]*nBins ) )    # bkg_tot with no error
#                data_ratio = hists[dataList[0]][plot].Clone("data")
#                #data_ratio.Divide(bkg_tot)
#                #data_ratio.Draw("e")
#
#                MCE = hists['bkg'][plot].Clone("MCError_%s"%( hists['bkg'][plot].GetName() )  ) ## bkg_tot with error
#                MCE.Divide( bkg_tot)
#                MCE.SetFillStyle(3001)
#                MCE.SetFillColor(1)
#                MCE.SetMarkerSize(0)
#                MCE.Draw("e2same")
#                ret['junk'].append(MCE)

def drawPlots(samples, plots, cut, sampleList=['s','w'], plotList=[], plotMin=False, plotLimits=[], save=True,
                                            fom=False , normalize=False, 
                                            pairList=None, fomTitles=False, 
                                            denoms=None, noms=None, ratioNorm=False, fomLimits=[],
                                            leg=True, unity=True, verbose=False, dOpt="hist"):
    if normalize and fom and fom.lower() != "ratio":
        raise Exception("Using FOM on area  normalized histograms... This can't be right!")
    
    #tfile = ROOT.TFile("test.root","new")

    cut_name = cut if type(cut) == type("") else cut.fullName

    dOpt_ = dOpt
    ret = {}
    canvs={}
    hists   = getSamplePlots(samples,plots,cut,sampleList=sampleList, plotList=plotList)
    stacks  = getBkgSigStacks(samples,plots,cut, sampleList=sampleList, plotList=plotList, normalize=normalize, transparency=normalize, sName=cut_name )
    sigList, bkgList, dataList = getSigBkgDataLists(samples, sampleList=sampleList)





    ret.update({
                'canvs':canvs       , 
                'stacks':stacks     ,
                'hists':hists       ,
                'fomHists':{}       ,
                'sigBkgDataList': [sigList,bkgList,dataList],
                'legs':[]           ,
                'hist_info' : {}    ,
                })
    isDataPlot = bool(len(dataList))

    if len(dataList) > 1:
        raise Exception("More than one Data Set in the sampleList... This could be dangerous. %"%dataList)       
    for p in plots.iterkeys():
        dOpt = dOpt_ 
        if plotList and p not in plotList:
            continue
        if plots[p]['is2d']:
            print "2D plots not supported:" , p
            continue
        if fom:
            denoms = denoms if type(denoms)==type([]) else [denoms]
            if pairList:
                padRatios=[2]+ [1]*(len(pairList))   
            elif not denoms or len(denoms)==1:
                padRatios=[2,1]
            else:
                padRatios=[2]+[1]*(len(denoms))
            #print "            padRatios:  ", padRatios

            canvs[p]=makeCanvasMultiPads(c1Name="canv_%s_%s"%(cut_name,p),c1ww=800,c1wh=800, joinPads=True, padRatios=padRatios, pads=[])
            cSave , cMain=0,1   # index of the main canvas and the canvas to be saved
        else: 
            canvs[p] = ROOT.TCanvas("canv_%s_%s"%(cut_name,p),"canv_%s_%s"%(cut_name,p),800,800), None, None
            cSave , cMain=0,0
        canvs[p][cMain].cd()
        #dOpt="hist"
        if normalize: 
            #stacks['bkg'][p].SetFillStyle(3001)
            #stacks['bkg'][p].SetFillColorAlpha(kBlue, 0.35)
            dOpt+="nostack"
        if len(bkgList):
            refStack=stacks['bkg'][p]
            refStack.Draw(dOpt)
            #if logy: canvs[p][cMain].SetLogy(logy)
            dOpt="same"
        else:
            refStack = stacks['sig'][p]
        if isDataPlot:
            dataHist=hists[dataList[0]][p]            
            dataHist.SetMarkerSize(0.9)
            dataHist.SetMarkerStyle(20)
            dataHist.Draw("E0Psame")
            dOpt+=""
        stacks['sig'][p].Draw("%s nostack"%dOpt.replace("hist",""))
        #print "!!!!!!!!!!!!!!!!!!!!" , refStack, getattr(refStack,"Get%saxis"%"y".upper() )()
        #if True: return refStack, ret
        if plots[p].has_key("decor"):
            if plots[p]['decor'].has_key("y"): decorAxis(refStack, 'y', plots[p]['decor']['y'], tOffset=1.6, tSize = 0.04)
            if plots[p]['decor'].has_key("x") and not isDataPlot: decorAxis(refStack, 'x', plots[p]['decor']['x'], tOffset=1.3, tSize = 0.04)
            if plots[p]['decor'].has_key("title") :refStack.SetTitle(plots[p]['decor']['title']) 
            if plots[p]['decor'].has_key("log"):
                logx, logy, logz = plots[p]['decor']['log']
                if logx : canvs[p][cMain].SetLogx(1)
                if logy : canvs[p][cMain].SetLogy(1)
        if plotMin: refStack.SetMinimum( plotMin )
        if plotLimits: 
            refStack.SetMinimum(plotLimits[0])
        if logy: 
            refStack.SetMaximum(20*refStack.GetMaximum())
        else:
            refStack.SetMaximum(1.5*refStack.GetMaximum())
                
        if leg:
            bkgLegList = bkgList[:] 
            sigLegList = sigList[:] 
            
            bkgLegList.reverse()
            sigLegList.reverse()
            bkgLegList += dataList
            #bkgLeg = makeLegend(samples, hists, bkgLegList, p, loc=[0.7,0.7,0.87,0.87], name="Legend_bkgs_%s_%s"%(cut.name, p), legOpt="f")
            #bkgLeg.Draw()
            #ret['legs'].append(bkgLeg)
            legy = [0.7, 0.87 ]
            legx = [0.75, 0.95 ]  
            nBkgInLeg = 4
            if any_in(sampleList, bkgLegList):
                subBkgLists = [ bkgLegList[x:x+nBkgInLeg] for x in range(0,len(bkgLegList),nBkgInLeg) ]
                nBkgLegs = len(subBkgLists)
                for i , subBkgList in enumerate( subBkgLists ):
                    newLegY0 = legy[0] + (legy[1]-legy[0])* (1-1.*len(subBkgList)/nBkgInLeg)
                    bkgLeg = makeLegend(samples, hists, subBkgList, p, loc=[legx[0], newLegY0 ,legx[1],legy[1]], name="Legend_bkgs%s_%s_%s"%(i, cut.name, p), legOpt="f")
                    print "==========================================================================="
                    print bkgLeg, subBkgList, legx 
                    print "==========================================================================="
                    ret['legs'].append(bkgLeg)
                    ret['legs'][-1].Draw()
                    legx = [ 2*legx[0] -legx[1] , legx[0]  ] 
                    del bkgLeg

            if any_in(sampleList, sigLegList):
               sigLeg = makeLegend(samples, hists, sigLegList, p, loc=[legx[0],legy[0],legx[1],legy[1]], name="Legend_sigs_%s_%s"%(cut.name, p), legOpt="l")
               sigLeg.Draw()
               ret['legs'].append(sigLeg)

        if fom:
           if plots[p]['decor'].has_key('fom_reverse'):
               fom_reverse= plots[p]['decor']['fom_reverse']
           else: fom_reverse = True

           if pairList:
               getFOMPlotFromStacksPair(ret, p, sampleList, fom=fom, normalize=normalize,
                                             denoms=denoms, noms=noms, ratioNorm=ratioNorm, fomLimits=fomLimits, pairList=pairList, fomTitles=fomTitles,
                                             leg=leg, unity=unity, verbose=verbose)
           else:
               getFOMPlotFromStacks(ret, p, sampleList, fom=fom, fom_reverse=fom_reverse, normalize=normalize,
                                             denoms=denoms, noms=noms, ratioNorm=ratioNorm, fomLimits=fomLimits,
                                             leg=leg, unity=unity, verbose=verbose)
           if bkgList:
               canvs[p][cMain].cd()
               ret['hists']['bkg'][p].SetFillColor(1)
               ret['hists']['bkg'][p].SetFillStyle(3001)
               ret['hists']['bkg'][p].SetMarkerSize(0)
               ret['hists']['bkg'][p].Draw("e2same")
           for c in canvs[p]:
               c.RedrawAxis()
            
        canvs[p][cMain].cd()
        canvs[p][cMain].RedrawAxis()
        canvs[p][cMain].Update()
        if not isDataPlot and not fom: canvs[p][cMain].SetRightMargin(10)
        #canvs[p][cMain].SetLeftMargin(15) 
        
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.04)
        #latex.SetTextAlign(11)
 
        if isDataPlot:
            latex.DrawLatex(0.16,0.92,"#font[22]{CMS Preliminary}")
            latex.DrawLatex(0.7,0.92,"\\mathscr{L} = \\mathrm{%0.1f\, fb^{-1} (13\, TeV)}"%( round(samples[dataList[0]].lumi/1000.,2)) )
        elif fom:
            latex.DrawLatex(0.16,0.92,"#font[22]{CMS Simulation}")
            latex.DrawLatex(0.65,0.92,"\\mathscr{L} = \\mathrm{%0.1f\, fb^{-1} (13\, TeV)}"%(round(samples[bkgList[0]].weights.weight_dict['lumis']['target_lumi']/1000.,2))) # assumes all samples in the sampleList have the same target_lumi
        else:
            latex.DrawLatex(0.16,0.96,"#font[22]{CMS Simulation}")
            latex.DrawLatex(0.6,0.96,"\\mathscr{L} = \\mathrm{%0.1f\, fb^{-1} (13\, TeV)}"%(round(samples[bkgList[0]].weights.weight_dict['lumis']['target_lumi']/1000.,2))) # assumes all samples in the sampleList have the same target_lumi
        
        ret['latex'] = latex

        canvs[p][cSave].Update()

        #cut_saveDir = cut if type(cut) == type("") else cut.saveDir
        #if explicitSaveDir:
        #    cut_saveDir=""
        
        sample_hist_info = getSamplePlotsInfo(samples,plots,cut,sampleList=sampleList,plotList=plotList, plots_first = True)
        if verbose:
            #canvs[p][cSave].plot_info =
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    HIST INFO"
            print sample_hist_info 
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

        if save:
            saveDir = save  if type(save)==type('') else "./"
            #saveDir = save + "/%s/"%cut_saveDir if type(save)==type('') else "./"
            saveCanvas(canvs[p][cSave],saveDir, p, formats=["png"], extraFormats=["root","C","pdf"])
            pp.pprint(   sample_hist_info[p], 
                         open( saveDir+"/extras/%s.txt"%p ,"w") ) 
    #gc.collect()
    return ret

class Draw():
    """
    Not really functional
    FIXME:
        needs these:
            getStacks ( with bkg_tot, sig, data ) 
            set pads
            set legend
            set limit
            draw

    """

    def __init__(samples,plots,cut,sampleList=['s','w'],plot="lepPt",plotMin=False, plotLimits=[],logy=0,save=True,
                                            fom=True, normalize=False,
                                            denoms=None,noms=None, ratioNorm=False,  fomLimits=[],
                                            leg=True,unity=True, verbose=False):

            self.npads = 0

    def setup_pads():
        self.pad_ratios = [2] + [1]*(self.nPads-1)
        self.canv_save, self.canv_main = (0,1)

    def draw_main_plot():
        self.canvs[self.canv_main].cd()
        if self.dataList:
            self.ref_hist = data_hist
        elif self.bkgList:
            self.ref_hist = self.stacks['bkg']
        elif self.sigList:
            self.ref_hist = self.stacks['sig']

    def add_new_pad(pad_rel_size, what_to_plot ):
            self.nPads +=1

    def draw():
            #get_pad_ratios
            #makeMultiCanv
            pass

    def get_hists():
        self.hists   = getSamplePlots(samples,plots,cut,sampleList=sampleList, plotList=[plotList])[plot]
        self.stacks  = getBkgSigStacks(samples,plots,cut, sampleList=sampleList, plotList=plotList, normalize=normalize, transparency=normalize )
        self.sigList, self.bkgList, self.dataList = getSigBkgDataLists(samples, sampleList=sampleList)

    def get_weights():
        pass

def getFOMPlotFromStacks( ret, plot, sampleList ,fom=True, fom_reverse = False,  normalize=False, 
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
        ret['junk']=[]
        if "ratio" in fomFunc.lower():
            pass
        #print "isdataplot:",  [ x in dataList for x in noms ]
        if any( [ x in dataList for x in noms ]):       
            isDataPlot=True
            fomPlotTitle_ = "DATA/MC     " if "bkg" in denoms else "AAAAAAAAAAAAAA"
        else: 
            isDataPlot = False
            fomPlotTitle_ = fomFunc
        for idenom, denom in enumerate(denoms,2):
            fomPlotTitle = "%s"%fomPlotTitle_
            canvs[plot][idenom].cd()
            canvs[plot][idenom].SetGridx(1)
            canvs[plot][idenom].SetGridy(1)

            fomHists[plot][denom]={}  
            ## Getting the total BKG hist
            if bkgList:
                hists['bkg'][plot]=stacks['bkg'][plot].GetHists()[0].Clone()
                hists['bkg'][plot].Reset()
                stack_name = "stack_%s"%stacks['bkg'][plot].GetHists()[0].GetName()
                hists['bkg'][plot].SetName(  stack_name  )
                hists['bkg'][plot].SetTitle( stack_name   )
                hists['bkg'][plot].Merge( stacks['bkg'][plot].GetHists() )
            if denom:
                fomHists[plot][denom]['denom']=hists[denom][plot]
                if not isDataPlot: fomPlotTitle += " (%s)"%denom
            else:
                fomHists[plot][denom]['denom']=hists[plot]['bkg'] if bkgList else False
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

            fomMin, fomMax = (100,-100)
            for nom in nomeratorList:
                #sigHist= samples[sig]['cuts'][cut.name][plot]
                sigHist= hists[nom][plot]
                fomHists[plot][denom][nom] = getFOMFromTH1FIntegral(sigHist, fomHists[plot][denom]['denom'] ,fom=fomFunc, verbose = verbose, integral = fomIntegral, reverse=fom_reverse)
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

            if isDataPlot:
                bkg_tot = hists['bkg'][plot].Clone("bkg_tot")
                bkg_tot.SetError(ar.array( "d",[0]*nBins ) )    # bkg_tot with no error
                data_ratio = hists[dataList[0]][plot].Clone("data")
                #data_ratio.Divide(bkg_tot)
                #data_ratio.Draw("e")

                MCE = hists['bkg'][plot].Clone("MCError_%s"%( hists['bkg'][plot].GetName() )  ) ## bkg_tot with error
                MCE.Divide( bkg_tot)
                MCE.SetFillStyle(3001)
                MCE.SetFillColor(1)
                MCE.SetMarkerSize(0)
                MCE.Draw("e2same")
                ret['junk'].extend([MCE, data_ratio, bkg_tot])
                #ll = TLine(Hr.GetXaxis().GetXmin(),1,Hr.GetXaxis().GetXma),1)
                 
            if unity:
                Func = ROOT.TF1('Func_%s'%uniqueHash(),"[0]",lowBin,hiBin)
                Func.SetParameter(0,1)
                #Func.SetLineStyle(3)
                Func.SetLineColor(1)
                Func.SetLineWidth(1)
                Func.Draw("same")
                ret['junk'].append(Func)
                fomHists[plot][denom].update({'func':Func})
            #print 'fom min max', fomMin, fomMax
            #print "first fom hist", first_nom
            if fomLimits:
                fomHists[plot][denom][first_nom].SetMinimum(fomLimits[0] )
                fomHists[plot][denom][first_nom].SetMaximum(fomLimits[1] )
            else:
                fomHists[plot][denom][first_nom].SetMaximum(fomMax*(1.2) )
                fomHists[plot][denom][first_nom].SetMinimum(fomMin*(0.8) )
            #print denom, first_nom, fomLimits, fomMin, fomMax
            fomHists[plot][denom][first_nom].Draw("same")
            #print "idenom", idenom
            if hasattr(canvs[plot][idenom], "RedrawAxis"):
                canvs[plot][idenom].RedrawAxis()
                canvs[plot][idenom].Update()
            else:
                print 
                print "!!!!!!!!!!!!!!!!!!!!!!!!! SOMETHING WRONG WITH THE CANVAS!!!!!"
                print 
                print plot, idenom, canvs
                print 
                print "!!!!!!!!!!!!!!!!!!!!!!!!!" 
                print 

        #for canv in canvs[plot]:
        #    canv.cd()
        return ret

def getFOMPlotFromStacksPair( ret, plot, sampleList ,fom=True, normalize=False, 
                          denoms=None,noms=None, 
                          pairList = False, 
                          ratioNorm=False , fomLimits=[0.8,2], fomTitles=False,
                          unity=True, verbose=False , leg=True):
        """
            pairList [  
                        [ [samp1, samp2] , [samp3, samp4] ]    , 
                        [ [samp4,samp5] , [samp5,samp6]   ]    , ....
                     ]
            should produce two ratio pads with
            pad1 : samp1/samp2 and samp3/samp4
            pad2 : ....

        """
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
        if "ratio" in fomFunc.lower():
            pass
        for ipad, pairs in enumerate(pairList,2):
            canvs[ plot ][ ipad ].cd()                

            if any( [x in dataList for x in pairs ] ):
                isDataPlot=True
                fomPlotTitle = "DATA/MC     " if "bkg" in denoms else "BAAAAAAAAAAAAAA"
            else: 
                isDataPlot = False
                fomPlotTitle = fomFunc if not fomTitles else fomTitles[ipad-2]
            if fomTitles:
                fomPlotTitle=fomTitles[ipad-2]
            dOpt="" if not isDataPlot else "E0P"
            for pair in pairs:
                pair = tuple(pair)
                print "   pairs:   ",ipad, pair, dOpt
                nom, denom = pair

                fomHists[plot][pair]={}
                denomHist = hists[denom][plot]
                nomHist= hists[nom][plot]
                #if not isDataPlot: fomPlotTitle += " (%s)"%denom

                nBins  = denomHist.GetNbinsX()
                lowBin = denomHist.GetBinLowEdge(1)
                hiBin  = denomHist.GetBinLowEdge(denomHist.GetNbinsX()+1)
                #dOpt="" if not isDataPlot else "E1P"

                #fomHists[plot][denom][nom] = getFOMFromTH1FIntegral(nomHist, denomHist ,fom=fomFunc, verbose =False, integral = fomIntegral)
                fomHists[plot][pair] = getFOMFromTH1FIntegral(nomHist, denomHist ,fom=fomFunc, verbose =False, integral = fomIntegral)
                if ratioNorm:
                    fomHists[plot][pair].Scale(1./fomHists[plot][pair].Integral() ) 

                fomHists[plot][pair].SetLineWidth(2)
                fomHists[plot][pair].Draw(dOpt)

                fomMax = max(getHistMax(fomHists[plot][pair])[1] ,fomMax)
                newMin = getHistMin(fomHists[plot][pair],onlyPos=True)[1]
                fomMin = min( newMin ,fomMin)

                if dOpt!="same":
                    #print p, nom , fomHists[plot][denom][nom].GetYaxis().GetTitleSize()
                    first_nom = nom
                    decorAxis( fomHists[plot][pair], 'x', tSize=0.1   ,  lSize=0.1)
                    #decorAxis( fomHists[plot][pair], 'y', t='%s  '%fomPlotTitle   , tOffset=0.5 ,  tSize=1./len(fomPlotTitle), lSize=0.1, func= lambda axis: axis.SetNdivisions(506) )
                    decorAxis( fomHists[plot][pair], 'y', t='%s  '%fomPlotTitle   , tOffset=0.8 ,  tSize=0.07, lSize=0.1, func= lambda axis: axis.SetNdivisions(506) )
                    fomHists[plot][pair].SetTitle("")
                    dOpt="same"
                if unity:
                    Func = ROOT.TF1('unity_%s'%plot,"[0]",lowBin,hiBin)
                    Func.SetParameter(0,1)
                    #Func.SetLineStyle(3)
                    Func.SetLineColor(1)
                    Func.SetLineWidth(1)
                    Func.Draw("same")
                    fomHists[plot].update({'unity_func':Func})
                #print 'fom min max', fomMin, fomMax
                #print "first fom hist", first_nom
                #print fomHists[plot]
                if fomLimits:
                    fomHists[plot][pair].SetMinimum(fomLimits[0] )
                    fomHists[plot][pair].SetMaximum(fomLimits[1] )
                else:
                    fomHists[plot][pair].SetMaximum(fomMax*(1.2) )
                    fomHists[plot][pair].SetMinimum(fomMin*(0.8) )
            fomHists[plot][pair].Draw("same")
            print "idenom", ipad
            canvs[plot][ipad].RedrawAxis()
            canvs[plot][ipad].Update()
        return ret

fomDefaultSet =   { 
                    "fom":"AMSSYS", 
                    "normalize":False, 
                    "denom":None,  #None will use the stack as the BKG for the FOM and denom for ratio
                    "noms":None, 
                    "ratioNorm":False, 
                    "leg":True,
                    "unity":True, 
                    "verbose":False, 
                    "limits":[0.8,1.2]
                   }

import array as ar

def getPieChart(samples, sampleList, cut):
    ylds = []
    colors = []
    for samp in sampleList:
        weightStr = "weight" if not samples[samp].has_key("weight") else samples[samp]["weight"]
        ylds.append(  getYieldFromChain(samples[samp]['tree'], cut.combined, weightStr) )
        colors.append( samples[samp]['color'] )

    ylds = ar.array("f",ylds)
    colors = ar.array("i",colors)
    pie = ROOT.TPie( cut.fullName, cut.fullName , len(ylds), ylds, colors)

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
                leg.SetFillColorAlpha(0,0.01)
                leg.SetBorderSize(1)
                ret.update({'leg':leg})
                for bkg in bkgList:
                    leg.AddEntry(hists[bkg][p], samples[bkg].name , "f")    
                for sig in sigList:
                    leg.AddEntry(hists[sig][p], samples[sig].name , "l")    
                leg.Draw()
            if save:
                saveDir = save + "/%s/"%cut.saveDir if type(save)==type('') else "./"
                if not os.path.isdir(saveDir): os.mkdir(saveDir) 
                canvs[plotName].SaveAs(saveDir+"/%s.png"%plotTitle.replace("#",""))
    return ret

def saveDrawOutputToFile( drawOut, fileOut):
    canvs = drawOut['canvs']
    fileOut.cd()
    for canv in canvs:
        canvs[canv][0].Write()
    return fileOut 

def getAndDrawQuickPlots(samples,var,bins=[],varName='',cut="(1)",weight="weight", sampleList=['s','w'],min=False,logy=0,save=True,fom=True, leg=True,unity=True):
    ret = {}
    canv = ROOT.TCanvas(varName,varName,800,800)
    ####### Getting Plots
    ret['hists']={}
    ret.update({'canv':canv })

    bkgList = [ samp for samp in sampleList if samp in samples.bkgList()]
    sigList = [ samp for samp in sampleList if samp in samples.sigList()]

    print bkgList, sigList
    if not (sigList or bkgList):
        raise Exception("No Signal or Background... what to draw? sampleList = %s"%sampleList)

    if leg:
        leg = ROOT.TLegend(0.6,0.7,0.9,0.9)
        ret.update({'leg':leg})
    for sampKey in samples:
        if sampKey not in sampleList:
            continue
        samp = samples[sampKey]
        weightStr = decide_weight2(samp, weight)
        if sampKey in sigList:
            ret['hists'][sampKey]=getGoodPlotFromChain(samp.tree, var, binning = bins, varName=varName, cutString=cut, weight=weightStr, color = samp.color, lineWidth=2 )
        if sampKey in bkgList:
            ret['hists'][sampKey]=getGoodPlotFromChain(samp.tree, var, binning = bins, varName=varName, cutString=cut, weight=weightStr, color = 1, fillColor = samp.color )
        
    dopt ="hist"
    first_stack = None
    stacks={}
    if bkgList:
        bkgStack  = getStackFromHists([ ret['hists'][x] for x in bkgList ],sName="stack_bkg",scale=None)
        bkgStack.Draw(dopt)
        dopt += " same"
        first_stack = bkgStack
        stacks['bkg']=bkgStack
    if sigList:
        sigStack  = getStackFromHists([ ret['hists'][x] for x in sigList ],sName="stack_sig",scale=None)
        if not first_stack: first_stack = sigStack
        sigStack.Draw(dopt+" nostack")
        stacks['sig']=sigStack
    first_stack.SetTitle(varName)
    ret.update({'stacks':stacks})
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

def getTH2FbinContent(hist):
    nbinsx = hist.GetNbinsX()
    nbinsy = hist.GetNbinsY()
    cont = {}
    for x in range(1,nbinsx+1):
        xbin = int( hist.GetXaxis().GetBinCenter(x) )
        cont[xbin]={}
        for y in range(1,nbinsy+1):
            ybin = int( hist.GetYaxis().GetBinCenter(y) )
            bincontent = hist.GetBinContent(x,y)
            if bincontent:
                cont[xbin][ybin]=hist.GetBinContent(x,y)
    return cont

def getEfficiency(samples,samp, plot, cutInst_pass, cutInst_tot ,ret = False ):

    str_pass = cutInst_pass.fullName
    str_tot  = cutInst_tot.fullName

    try:
        h_pass = samples[samp]['cuts'][str_pass][plot]
        h_tot  = samples[samp]['cuts'][str_tot][plot]
    except KeyError:
        print "!!!!!!!!!!!!!!!!!!!!!"
        print "Plot key not for pass or tot not found."
        print "pass: samples[{samp}]['cuts'][{str_pass}][{plot}]".format(samp=samp, str_pass = str_pass, plot=plot)
        print "tot:  samples[{samp}]['cuts'][{str_tot}][{plot}]".format(samp=samp, str_tot = str_tot, plot=plot)
        return False    

    #g_efficiency    =   ROOT.TGraphAsymmErrors()
    #g_efficiency.Divide(h_pass,h_tot,"cl=0.683 b(1,1) mode")

    h_eff = ROOT.TEfficiency(h_pass, h_tot)

    eff_name = 'EFF_%s_WRT_%s'%(str_pass,str_tot)
    eff_plot_name = plot + "_" + eff_name     

    #decorHist( samples[samp], cutInst_pass, h_eff, plots[plot]['decor'] ) 
    #decorHist( samples[samp], cutInst_pass, h_eff, {} ) 
    h_eff.SetName(samples[samp].name+"_"+eff_plot_name)
    h_eff.SetMarkerStyle(0)
    #h_eff.SetLineColor( samples[samp]['tree'].GetLineColor() )
    h_eff.SetLineColor( sample_colors[samp] ) 
    
    if samp in samples.bkgList():
        h_eff.SetLineWidth(2)
        h_eff.SetLineStyle(3)

    h_eff.SetTitle("{TITLE};{X};{Y}".format(TITLE=samples[samp].name+"_"+eff_plot_name,  X= h_pass.GetXaxis().GetTitle()  , Y= "#frac{%s}{%s}"%(str_pass, str_tot)  ))
    
    if not samples[samp]['cuts'].has_key(eff_name):
        samples[samp]['cuts'][eff_name] = {}
    samples[samp]['cuts'][eff_name][plot] = h_eff

    samples[samp]['plots'][eff_plot_name] = h_eff
    
    if ret:
        return h_eff

 
#[ len(mstops), min(mstops) - 0.5*dstops , max(mstops) + 0.5*dstops, (max(mstops) + min(dms) - ( min(stops)-max(dms))) /5.  ,min(stops)-max(dms)-5 , max(mstops) + min(dms)+5 ) ]
# [ len(mstops), min(mstops) - 0.5*dstops , max(mstops) + 0.5*dstops, (max(mstops) + min(dms) - ( min(mstops)-max(dms))) /5  ,min(mstops)-max(dms)-5 , max(mstops) + min(dms)+5 ] 
def makeStopLSPPlot(name, massDict, title="", bins = [23,87.5,662.5, 127 , 17.5, 642.5] , key=None, func=None,setbin=False, massFunc = None ):
    """
    massDict should be of the form {    
                                    stopmass1: { lsp_mass_1: a, lsp_mass_2: b ... },
                                    stopmass2: { lsp_mass_1: c, lsp_mass_2: d ...},
                                    ...
                                    }
    with a, b, c,d ... the bin content TH2D
    if key available then key(a) will be evaluated
    if func available then func(mstop,mlsp) will be evaluted. (func will override key)
    if massFunc:  stop_mass, lsp_mass  = massFunc(key)
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
    elif massFunc:
        for k,val in massDict.iteritems():
            masses  = massFunc(k)
            if not masses: 
                continue
            stop_mass, lsp_mass = masses
            val = val if not key else key(val) 
            plot.Fill(int(stop_mass), int(lsp_mass), val)


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
    plot.SetNdivisions(0,"z")
    plot.SetNdivisions(410,"x")
    plot.GetXaxis().SetTitle("m(#tilde{t})[GeV]")
    plot.GetYaxis().SetTitle("m(#tilde{#chi}^{0})[GeV]")
    return plot

def makeStopLSPRatioPlot(name, massDictNom, massDictDenom, title="", bins=[22,100,650, 65,0,650], key=None ):
    """
    massDict should be of the form {    
                                    stopmass1: { lsp_mass_1: a, lsp_mass_2: b ... },
                                    stopmass2: { lsp_mass_1: c, lsp_mass_2: d ...},
                                    ...
                                    }
    with a, b, c,d ... the bin content TH2D
    if key available then key(a) will be evaluated
    """
    ratio_dict = {}
    for mstop in massDictDenom:
        ratio_dict[mstop]={}
        for mlsp in massDictDenom[mstop]:
            if massDictDenom[mstop][mlsp]:
                try: 
                    massDictNom[mstop][mlsp]
                except KeyError:
                    print "Nomerator Dict missing value for %s, %s"%(mstop, mlsp)
                    continue
                if key:
                    val = key( massDictNom[mstop][mlsp] ) / key( massDictDenom[mstop][mlsp]  )
                else:
                    val = massDictNom[mstop][mlsp] / massDictDenom[mstop][mlsp]
                ratio_dict[mstop][mlsp] = val 
    ratio_pl = makeStopLSPPlot( name, ratio_dict, title=title , bins=bins )
    return ratio_pl, ratio_dict

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

#less = lambda var,val: "(%s < %s)"%(var,val)
#more = lambda var,val: "(%s > %s)"%(var,val)
#btw = lambda var,minVal,maxVal: "(%s > %s && %s < %s)"%(var, min(minVal,maxVal), var, max(minVal,maxVal))

deltaPhiStr = lambda x,y : "abs( atan2(sin({x}-{y}), cos({x}-{y}) ) )".format(x=x,y=y)

deltaRStr = lambda eta1,eta2,phi1,phi2: "sqrt( ({eta1}-{eta2})**2 - ({dphi})**2  )".format(eta1=eta1,eta2=eta2, dphi=deltaPhiStr(phi1,phi2) ) 

def more(var,val, eq= True):
    op = ">"
    if eq: op = op +"="
    return "%s %s %s"%(var, op, val)

def less(var,val, eq= False):
    op = "<"
    if eq: op = op +"="
    return "%s %s %s"%(var, op, val)

def btw(var,minVal,maxVal, rangeLimit=[0,1] ):
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

def joinWeightList(weightStringList):
    return "(" + " * ".join([ "("+c +")" for c in weightStringList])    +")"

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
        self.inclCombinedList    = [ [self.name , self._combine(self.inclList) ], ] 
        self.baseCut = baseCut

        self.saveDir = self.baseCut.saveDir +"/" + self.name if self.baseCut else self.name
        self.fullName = self.baseCut.fullName + "_" + self.name if self.baseCut else self.name

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
        self.list2         = self.list[1:] if self.baseCut else self.list
        self.flow2         = self._makeFlow(self.inclList,self.baseCutString)
        if baseCut:
            self.flow        = self._makeFlow([[self.baseCutName, self.baseCutString]]+self.inclList)
        else:
            self.flow = self.flow2
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
        if self.cutsToThrow:
            return combineCutList(self.minusCutList)
        else: 
            return self.combined

    def add(self, cutInst, cutOpt="inclList", baseCutString="" ):
        if baseCutString:
            cutList = addBaseCutString(getattr(cutInst,cutOpt), baseCutString )
        else: 
            cutList = getattr(cutInst,cutOpt)
        self.__init__(self.name,self.inclList + cutList , baseCut = self.baseCut)  

    def __str__(self):
        #return "%s Instance %s : %s"%(self.__class__.__name__ , self.name,   object.__str__(self) )
        return "<%s Instance: %s>"%(self.__class__ , self.name )
    def __repr__(self):
        return "<%s Instance: %s>"%(self.__class__ , self.name  )

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
##########################################    Weight CLASS    ###############################################
##########################################                    ###############################################
#############################################################################################################

#def decide_weight( sample, weight, cutInst=None, weightDict = None):
#    """
#    chooses the weight for the sample.
#    if an instance of CutClass is given as cutInst, the weightDict is also required.
#    in this case, the weight is chosen from the weightDict, based the sample, cutInst, and the origianl weight string.
#    otherwise, the weight is chosen based on weight keys in the sample
#
#    """
#
#    if sample.isData:
#        weight_str = "(1)"
#        return weight_str
#    if "weight" in weight.lower():
#        if sample.has_key("weight"):
#            weight_str = sample['weight']
#        if weight.endswith("_weight"):
#            if sample.has_key(weight):
#                weight_str = sample[weight]
#                #print sample, weight_str, samples[sample]
#    else:
#        weight_str=weight
#    if not cutInst:
#        return weight_str
#    elif weightDict:
#        sample_name =  sample['name']
#        if weightDict.has_key(sample_name):
#            if weightDict[sample_name]
#        extra_weight = 
#    else:
#        raise Exception("When an instance of CutClass is given, a weight Dictionary is also required.")
#

def makeDefaultDict(d, default_dict):
        for key in default_dict:
            d.setdefault(key,deepcopy(default_dict[key]))
            if type( default_dict[key] ) == type({}):
                if not type(d[key]) == type({}):
                    raise Exception("There is inconsistancy between input dict and the default dict for key %s, dict:%s \n def_dict:%s \n"%(key,d, default_dict))
                else:
                    makeDefaultDict(d[key], default_dict[key])
            else:
                pass

class Weight(object):
    """

    """
    def __init__(self, weight_dict={}, def_weights={}):
        self.weight_dict = deepcopy(weight_dict)
        makeDefaultDict(self.weight_dict, def_weights)
    
    def getWeightList(self, weight_dict, cut="", lumi="target_lumi"):
        weight_list=[]
        for weight_key in weight_dict:
            #print weight_key
            new_weight = ""
            if weight_key == "cuts":
                found_a_match = False
                for cut_category in weight_dict['cuts']:
                    cut_weight , cut_finder_funct = weight_dict['cuts'][cut_category]
                    #print "looking for a match for", cut_category
                    #if cut_category in cut:
                    #    weight_list.append(cut_weight)
                    if True:
                        #### Should be careful of the weight_dict['cuts'] ...regex expresions confusing!
                        #print cut_category
                        if cut_finder_funct( cut ):
                            print "found a match to the cut string!", cut_category    
                            weight_list.append(  cut_weight )
                            #assert not found_a_match, "WARNING! Multiple matches to the cutstring... using all matches! (could be dangerous!)"            
                            if found_a_match : print  "WARNING! Multiple matches to the cutstring... using all matches! (could be dangerous!)"            
                            found_a_match = True
            elif weight_key == "lumis":
                weight_list.append(  "%s/%s"%(weight_dict['lumis'][lumi], weight_dict['lumis']["mc_lumi"]) )
            else:
                weight_list.append(  weight_dict[weight_key] )
            #if new_weight:
            #    weight_list.append(new_weight)
        return weight_list

    def combine(self, weight_dict=None, cut="default", lumi="target_lumi"):
        weights = self.weight_dict
        #if not weight_dict:
        #    weight_dict = self.weight_dict
        if weight_dict:
            weights.update(weight_dict) 
        self.weight_list = self.getWeightList(weights, cut, lumi)
        return joinWeightList(self.weight_list) 

def decide_weight2( sample, weight=None, cut="default" , lumi="target_lumi"):
    #print "Deciding weight:", sample.name, lumi, cut
    if sample.isData:
        weight_str = "(1)"
        return weight_str
    if not weight:
        weight = sample.weights

    #if isinstance(weight,Weight):
    if hasattr(weight,"combine"):
        weight_str = weight.combine(cut=cut, lumi=lumi)
    else:
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



#from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import btag_to_sf , sf_to_btag
from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import BTagSFMap



def decide_cut( sample, cut, plot=None, nMinus1=None):
    cuts = []



    if hasattr(cut, "nMinus1"):
        if nMinus1:
            main_cut_str = cut.nMinus1(nMinus1)
        else:          
            main_cut_str = cut.combined
    else:
        main_cut_str = cut
    cuts.append(main_cut_str)
    if getattr(sample, "cut", None):
        cuts.append(   sample.cut  )
    if plot and getattr(plot, "cut", None):
        cuts.append(   plot.cut   )
    warn=False
    if getattr(sample,"triggers", None):
        cuts.append( "(%s)"%sample['triggers'] )
        #warn = True
    if getattr(sample,"filters" , None):
        cuts.append( "(%s)"%sample['filters']   )
        #warn = True
    if warn:
        print "-----"*10 , sample.name
        print "-----"*20
        print "Applying Triggers: %s"%sample['triggers']
        print "Applying Filters: %s"%sample['filters']
        print "-----"*20
        print "-----"*20
    cut_str =  " && ".join(["( %s )"% c for c in cuts]) 

    sf_list = ["SF","SF_b_Down", "SF_b_Up", "SF_l_Down", "SF_l_Up" ] 

    modified = False
    new_cut = cut_str[:]
    for sfOpt in sf_list:
        btag_sf_map = BTagSFMap(sfOpt)
        btag_to_sf  = btag_sf_map.btag_to_sf
        sf_to_btag  = btag_sf_map.sf_to_btag
        sfs = sf_to_btag.keys()
        #print '----------------------'
        #print cut_str
        #print '----------------------'
        for sf in sfs:
            if sf in new_cut:
                #print ' found sf: %s in cut_str, \n%s'%(sf,new_cut)
                if sample.isData:
                    new_cut = new_cut.replace(sf, sf_to_btag[sf])
                    #print 'replacing sf: %s , with %s'%(sf, sf_to_btag[sf])
                else:
                    new_cut = new_cut.replace(sf, "(1)")
                    #print 'replacing sf: %s , with %s'%(sf, "(1)") 
                modified = True 
    if "met_genPt" in new_cut and not sample.isSignal:
        print "-------------------- Detected non-signal with genmet cut!"
        print "BEFORE:", new_cut
        new_cut = new_cut.replace("met_genPt","met_pt").replace("met_genPhi","met_phi")
        print "AFTER:" , new_cut
        print "--------------------"

    return new_cut




def decide_cut_weight( sample, cutInst, weight=None,  lumi="target_lumi" , plot=None, nMinus1=None,  ):
    #print "     ", sample 
    #print "     ", cutInst 
    #print "     ", weight 
    #print "     ", lumi 
    #print "     ", plot
    #print "     ", nMinus1
    cutStr = getattr( cutInst, "combined", cutInst )
    weight_str = decide_weight2(sample, weight, cutStr , lumi)
    cut_str    = decide_cut(sample, cutInst, plot = plot, nMinus1 = nMinus1)
    return cut_str, weight_str    




def decide_weight( sample, weight ):
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

#############################################################################################################
##########################################                    ###############################################
##########################################    YIELDS CLASS    ###############################################
##########################################                    ###############################################
#############################################################################################################

def getYieldsTEST(samp):
    print samp
    return samp

def getYieldsForSampleFunc(samples,cutList, weights, err, nDigits, yieldDictFull, verbose, pprint, sampleNames, cutNames, npsize, nSpaces): ## This is to make a picklable function for the multiprocessing. Better solution? 
    def func(sample):
        yieldDictSample={}
        for ic, cut in enumerate(cutList):
            yld = getYieldFromChain( samples[sample]['tree'], cut[1],weights[cut[0]][sample], returnError=err) #,nDigits) 
            #print cut[0], "     ", "getYieldFromChain( %s, '%s', '%s',%s )"%( "samples."+sample+".tree", cut[1], weights[sample], True) + "==(%s,%s)"%yld 
            if err:
                    rounded = [ round(x,nDigits) for x in yld ]
                    yld = u_float(*rounded)
            else:
                    yld = u_float(yld)
            yieldDictSample[cut[0]] = yld
            yieldDictFull[sample][cut[0]] = yld
            #yieldDictRaw[sample].append(yld)
        if verbose:
            pprint( [np.array([sampleNames[sample]]+[ yieldDictSample[cut] for cut in cutNames] , npsize)] , nSpaces=nSpaces   )
            #pprint( yieldDictSample, nSpaces=14) 
            #print sample, yieldDictSample
        return yieldDictSample
    return func

class Yields():
    '''
        Usage:
        y=Yields(samples,['tt', 'w','s'],cuts.presel,tableName='{cut}_test',pklOpt=1);
    '''
    def __init__(self,   samples,    sampleList, cutInst,    cutOpt='flow',  tableName='{cut}',  weight="",
                 pklOpt=False,   pklDir="./pkl/",    nDigits=2, err=True, nProc = None, lumi = 'target_lumi',
                 isMVASample = None, 
                 verbose=False, nSpaces=None):
        if not (isinstance(cutInst,CutClass) or hasattr(cutInst,cutOpt)):
            raise Exception("use an instance of cutClass")
        
        if pklOpt: makeDir(pklDir)
        
        self.nDigits        = nDigits
        samples = samples
        self.cutInst        = cutInst
        self.weight         = weight
        self.tableName    = tableName.format(cut=self.cutInst.fullName)
        self.sampleList     = [s for s in sampleList if s in samples.keys()]
        self.sampleList.sort(key = lambda x: samples[x]['isSignal'])
        self.npsize="|S20"
        self.err = err
        self.nProc = nProc
        self.isMVASample = isMVASample
        self.cutOpt = cutOpt

        self.lumi_string    =  lumi 
        #self.lumi           =  samples.get_lumis( self.lumi_string ) 
        
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
           #pp.pprint(self.weights)
           pp.pprint(self.cut_weights)

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
        
        isDataPlot = bool(len(self.dataList))
        if isDataPlot:
           if "DataBlind" in samples[self.dataList[0]].name: self.lumi_weight = "DataBlind_lumi"
           elif "DataUnblind" in samples[self.dataList[0]].name: self.lumi_weight = "DataUnblind_lumi"
           else: raise Exception("Data sample not recognized! %s"%dataList)
           print "Reweighting MC yields to", self.lumi_weight, ":", round(samples[self.dataList[0]].lumi/1000.,2), "fb-1" 
        else:
           self.lumi_weight = "target_lumi" 
           print "Reweighting MC yields to", self.lumi_weight, ":", round(samples[self.bkgList[0]].weights.weight_dict['lumis']['target_lumi']/1000.,2), "fb-1" 
        
        #self.sampleLegend   = np.array( [ [samples[sample]['name'] for sample in self.bkgList] + ["Total"] + 
        #                                                         [samples[sample]['name'] for sample in self.sigList] ] )

        #self.weights        = { samp:decide_weight(samples[samp] , self.weight    ) for samp in self.sampleList }
        
        #self.cut_weights_ = {}
        #for cutName, cutStr in getattr(self.cutInst, self.cutOpt):
        #    self.cut_weights_[cutName] = {samp:decide_weight2(samples[samp], cut=cutStr, lumi=self.lumi_weight) for samp in self.sampleList}     

        self.cut_weights = {}
        for cutName, cutStr in getattr(self.cutInst, self.cutOpt):  
            self.cut_weights[cutName] = {}
            for samp in self.sampleList:
                self.cut_weights[cutName][samp] =  decide_cut_weight( samples[samp] , cutInst = cutStr  ,  weight=self.weight,  lumi=self.lumi_weight, plot=None, nMinus1= None  )

        #print "CUT AND WEIGHT SUMMARY:"
        

        if hasattr(self,"LatexTitles"):
            #self.sampleLegend   =   [self.LatexTitles[sample] for sample in self.bkgList] +\
            #                        ["Total"] +  \
            #                        [self.LatexTitles[sample] for sample in self.sigList] +  \
            #                        [self.LatexTitles[sample] for sample in getattr(self,"fomList",[]) ]
            self.sampleLegend   =   [self.LatexTitles[sample] for sample in self.bkgList] +\
                                    ["Total"] +\
                                    [self.LatexTitles[d] for d in self.dataList ] 
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
            if samp in yieldDict.keys():
                continue
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
        #self.yieldDictFull.update(yieldDict)  ### FIX ME, should also combine Totals, FOMs, etc
        self.getYieldDictFull(samples, yieldDict = self.yieldDict )

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
                exps.append( np.array([ self.sampleNames.get(samp,samp) ]+[ yieldDict[samp][cut] for cut in self.cutNames] , self.npsize) )
            else:
                exps.append( np.array([samp]+[ yieldDict[samp][cut] for cut in self.cutNames] , self.npsize) )
        return np.concatenate(  [ self.cutLegend, np.array(exps)] )                                            
            
    def getBySample(self, samples, yieldDict):
        pass

    def getByBin(self, bin,  yieldDict=None):
        if not yieldDict:
            yieldDict = self.yieldDictFull
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

    def getYieldsForSample(self,samples, sample, cutList ):
        yieldDictSample={}
        #if cfg and hasattr(cfg, "isMVASample") and cfg.isMVASample and not samples[sample]['tree'].GetEventList():
        setSampleEventList = False
        if self.isMVASample and not samples[sample]['tree'].GetEventList():
            setSampleEventList = True
            setMVASampleEventList(samples, sample)

        for ic, cut in enumerate(cutList):
            cutName = cut[0]
            #cut_strings = [cut[1]]
            #warn = False
            #if hasattr(samples[sample], 'cut'):
            #    cut_strings.append(samples[sample].cut) 
            #if hasattr(samples[sample],"triggers") and samples[sample]['triggers']:
            #    cut_strings.append( samples[sample]['triggers'] )
            #    warn = True
            #if hasattr(samples[sample],"filters") and samples[sample]['filters']:
            #    cut_strings.append(  samples[sample]['filters'] )
            #    warn = True
            #if warn:
            #    print "-----"*10 , samples[sample].name
            #    print "-----"*20
            #    print "Applying Triggers: %s"%samples[sample]['triggers']
            #    print "Applying Filters: %s"%samples[sample]['filters']
            #    print "-----"*20
            #    print "-----"*20
            #cutStr = "&&".join([ "(%s)"%x for x in cut_strings])
            #print "CUT: ", cutName
            #print "OLD ONE: "
            #print cutStr
            #print "New ONE: "
            #print cutStr
            #yld = getYieldFromChain(samples[sample]['tree'], cutStr,self.cut_weights[cutName][sample], returnError=self.err) #,self.nDigits) 
            cutStr , weightStr = self.cut_weights[cutName][sample]
            yld = getYieldFromChain(samples[sample]['tree'], cutStr, weightStr, returnError=self.err) #,self.nDigits) 
            #print cut[0], "     ", "getYieldFromChain( %s, '%s', '%s',%s )"%( "samples."+sample+".tree", cut[1], self.weights[sample], True) + "==(%s,%s)"%yld 
            if self.err:
                    rounded = [ round(x,self.nDigits) for x in yld ] 
                    yld = u_float(*rounded)
            else:
                    yld = u_float(yld)
            yieldDictSample[cutName] = yld
            self.yieldDictFull[sample][cut[0]] = yld
            #self.yieldDictRaw[sample].append(yld)
        if setSampleEventList:
            samples[sample]['tree'].SetEventList(0)
            #setSampleEventList = False
        
        if self.verbose:  
            self.pprint( [np.array([self.sampleNames[sample]]+[ yieldDictSample[cut] for cut in self.cutNames] , self.npsize)] , nSpaces=self.nSpaces   )     
            #self.pprint( yieldDictSample, nSpaces=14) 
            #print sample, yieldDictSample
        return yieldDictSample

    def getYields2(self,samples,cutList):
        yieldDict={}
        if self.verbose: self.pprint(  self.cutLegend  , nSpaces=self.nSpaces )

        if self.nProc:
            #getYieldsFunc = getYieldsForSampleFunc( samples, cutList, self.weights, self.err, self.nDigits, self.yieldDictFull, self.verbose, self.pprint, self.sampleNames, self.cutNames, self.npsize, self.nSpaces)
            getYieldsFunc = getYieldsForSampleFunc(samples, cutList, self.cut_weights, self.err, self.nDigits, self.yieldDictFull, self.verbose, self.pprint, self.sampleNames, self.cutNames, self.npsize, self.nSpaces)
            pickle.dump(getYieldsFunc, file("delme.pkl","w"))
            test = getYieldsFunc( self.sampleList[0])
        
            print "--------------------", test
            pool    = multiprocessing.Pool( processes = self.nProc       )
            results = pool.map( getYieldsFunc, self.sampleList     )# [ [samples, samp, cutList] for samp in self.sampleList] )
            pool.close()
            pool.join()
            for isamp, samp in enumerate( self.sampleList ):
                yieldDict[samp] = results[isamp]
            #print yieldDict
            del results, pool             

        else:
            for samp in self.sampleList:
                yieldDict[samp] = self.getYieldsForSample(samples,samp, cutList )

        self.yieldDict = yieldDict
        #print yieldDict
        return yieldDict
        
    def getYieldDictFull(self, samples, cutList=None, yieldDict=None, yieldDictTotal=None, yieldDictFOMs=None,  fom="AMSSYS", uncert=0.2, nDigits = 3 ):
        yieldDictFull = {}
        if not yieldDict:
            if cutList:
                yieldDict       =   self.getYields2(samples, cutList )
            else:
                raise Exception("Either a cutList or yieldDict should be given!")
        yieldDictFull.update(yieldDict)
        if not yieldDictTotal:
            yieldDictTotal  =   self.getBkgTotal(yieldDict)
            print 'bkg total' ,  yieldDictTotal
            yieldDictFull.update({'Total': yieldDictTotal})
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
        lines = []
        first = True
        for line in table:
            new_line = " & ".join(map(str,line)) 
            fixed_line = fixForLatex( new_line)
            fixed_line = fixRowCol( fixed_line)
            fixed_line += " \\\ "
            lines.append( fixed_line )
        
        if first:
            lines[0] += "  \hline"
        ret = " \n".join(lines)
        #if self.verbose: print ret
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

    ####################################################
    ################## Fancy Stuff #####################
    ####################################################

    def getSignalYieldMap(self):
        """
        Getting the Yield per each bin on the stop lsp plane

        """
        yld_mass_map = {}
        for cut_name in self.cutNames:
            yieldDict = self.getByBin(cut_name)
            yld_mass_map[cut_name] = {}
            for sig in self.sigList:
                yld_value = yieldDict[sig]
                mstop, mlsp = getMasses(sig)
                set_dict_key_val( yld_mass_map[cut_name], mstop, {} )
                set_dict_key_val( yld_mass_map[cut_name][mstop] , mlsp, yld_value)
        return yld_mass_map

    def getBkgYieldMap(self, nice_names = False):
        """
        Getting the Yield per each bin for each background

        """
        name = lambda x: self.sampleNames[x] if nice_names else lambda x: x
        yld_bkg_map  = self.getByBins( { name(bkg):self.yieldDict[bkg] for bkg in self.bkgList} )
        #nom_ylds.getByBins( { nom_ylds.sampleNames[bkg]:nom_ylds.yieldDict[bkg] for bkg in nom_ylds.bkgList} )

        return yld_bkg_map

    def getSignalEffMap(self, xsecs,lumi=None):
        """
        calculating the signal efficiencies given the cross sections and luminosity        

        """
        if not lumi:
            lumi = self.lumi
        yld_mass_map = self.getSignalYieldMap()
        eff_mass_map = deepcopy( yld_mass_map)
        for cutName in self.cutNames:
            for mstop in eff_mass_map[cutName]:
                try:
                    xsec = xsecs[mstop]
                except KeyError:
                    xsec = xsecs[int(mstop)]
                for mlsp in eff_mass_map[cutName][mstop]:
                    yld_val =  yld_mass_map[cutName][mstop][mlsp] 
                    eff_mass_map[cutName][mstop][mlsp]  = yld_val/(xsec*lumi)
        return eff_mass_map, yld_mass_map

combine_bins =  {
                    'SR1a':'SR.*1a', 
                    'SR1b':'SR.*1b', 
                    'SR1c':'SR.*1c', 
                    'SR1':'SR.*1' , 
                    'SR2':'SR.*2'
                }

def getSignalEffMapFromYields(name, title, yld, xsecs, lumi = None  , combine_bins = None, saveDirBase = None,
    
                                 saveDirs={'main': "Regions/", 
                                           'comb': "CombinedRegions/"     ,
                                           'ratios': "Ratios/"     ,
                                          }
                                ):
    eff_map, yld_map = yld.getSignalEffMap(xsecs=xsecs, lumi = lumi )
    eff_plots = {}
    yld_plots = {}
    eff_canvs = {}
    yld_canvs = {}
    key = lambda x: x.val
    yld_bkg_map = yld.getBkgYieldMap(nice_names = True)
    def get_text_list(d):
        text_list = []
        mx = len ( max( d ) ) 
        for k,v in d.iteritems():
            text_list.append( "{k}:{spaces}{v}".format(k=k, v=v, spaces =" "*(3-len(k)+mx)  )  )
        return text_list
    if saveDirBase:
        if saveDirs:
            saveDir_main = saveDirBase  + "/" + saveDirs['main']
            saveDir_comb = saveDirBase + "/" + saveDirs['comb']
    dOpt = "gOff"

    cut_names = deepcopy( yld.cutNames ) 
    if combine_bins:
        combine_bins = deepcopy(combine_bins)
        for new_bin, bins_to_combine in combine_bins.iteritems():
            if not type(bins_to_combine)==type([]):
                bins_to_combine = [ bins_to_combine ]  
            #for b in cut_names: # Finding bins that match the given patterns
            #     to_be_combined = re.match("|".join(bins_to_combine),b )
            explicit_combine_list = [bin for bin in cut_names if re.match("|".join(bins_to_combine) ,bin)]
            combine_bins[new_bin] = explicit_combine_list
                 
    #print combine_bins
    #if True:
    #    return 

    cut_names.extend(combine_bins.keys())

    print cut_names
    print combine_bins
    for cut_name in cut_names:
        #if cut_name in combine_bins:
        print "------------", cut_name
        eff_plt_name = "EffAccpMap_" + ( name + "_" if name else "")+ cut_name
        yld_plt_name = "Yields_"     + ( name + "_" if name else "")+ cut_name
        print eff_plt_name

        if cut_name in combine_bins:  ## adding the  yields for signal and bkg based on the combined bins
            yld_map[cut_name] = sig_yield_adder( [ yld_map[b] for b in combine_bins[cut_name] ] )
            yld_bkg_map[cut_name] = dict_manipulator( [yld_bkg_map[b] for b in combine_bins[cut_name]]  , lambda *bins: sum(bins).round(4) )
            eff_map[cut_name] = sig_yield_adder( [ eff_map[b] for b in combine_bins[cut_name] ] )
            saveDir = saveDir_comb
        else:
            saveDir = saveDir_main

        eff_plots[cut_name] = makeStopLSPPlot(  eff_plt_name  , eff_map[cut_name] , key = key)
        eff_canvs[cut_name] = ROOT.TCanvas( "Canvas_%s"%eff_plt_name, "Canvas_%s"%eff_plt_name, *canvas_2d_size )  
        ROOT.gStyle.SetPaintTextFormat("0.1e")
        eff_plots[cut_name].Draw("COLZ TEXT" + dOpt)
        saveCanvas( eff_canvs[cut_name], saveDir , eff_plt_name )
        print yld_plt_name
        yld_plots[cut_name] = makeStopLSPPlot( yld_plt_name, yld_map[cut_name] , key = key )
        yld_canvs[cut_name] = ROOT.TCanvas( "Canvas_%s"%yld_plt_name, "Canvas_%s"%yld_plt_name, *canvas_2d_size )  
        ROOT.gStyle.SetPaintTextFormat("0.2f")
        yld_plots[cut_name].Draw("COLZ TEXT" + dOpt)
        text_list = get_text_list( yld_bkg_map[cut_name]  )
        ptext = make_ptext( 0.6,0.2,0.9,0.4, text_list=text_list  )
        ptext.Draw()
        saveCanvas( yld_canvs[cut_name], saveDir , yld_plt_name )
        yld_canvs[cut_name].Update()

    ret  = { 
                'eff_plots':eff_plots, 
                'yld_plots':yld_plots , 
                'eff_dict':eff_map, 
                'yld_dict':yld_map , 
                'bkg_yld_dict': yld_bkg_map, 
                'yld_canvs':yld_canvs, 
                'eff_canvs': eff_canvs 
           } 

    return ret 

def make_ptext( x1, y1, x2, y2, text_list = [] , option = "brNDC"):
    ptext = ROOT.TPaveText(x1,y1,x2,y2, option)
    ptext.SetBorderSize(0)
    ptext.SetFillColor(0)
    ptext.SetShadowColor(0)
    ptext.SetTextAlign(11)
    for text in text_list:
        ptext.AddText(text)
    return ptext

def dict_manipulator( ds = [],  func= lambda a,b: a+b, def_val = u_float(0) ):
    """
    ds is a list of dictionaries with the same keys... not implemented for the case with different keys
    func will be applied on elements of the dictionaries for the given key
    (order of the dicts in the ds has to much the order of the inputs for the function)
    """
    ## to implement: def_Val for each dict in ds (how?)
    #print func.__code__.co_name
    res = {}
    keys = list( set( itertools.chain( *[d.keys() for d in ds ] )))
    #print keys
    for k in keys:
        #res[k] = itertools.starmap( func , [d.get(k,def_val) for d in ds] )
        res[k] = func(* [d.get(k,def_val) for d in ds] )
    return res

def make_dict_manipulator( func ):
    """
    examples:

    given the structure for sr1a and sr1b as:
        sr1a = { mstop_1: {mlsp_1: yld1, mlsp_2:yld2, ..} , mstop_2: {...} ...}
    dm = dict_manipulator( [sr1b,sr1a], func = make_dict_manipulator( lambda a,b: a+b) )
    gives the sum of ylds for each stop lsp mass in sr1b and sr1a

    dm = dict_manipulator( [sr1a,sr1b,sr1a], func = make_dict_manipulator( lambda *a: sum(a) ) )
    same as above, but can have arbitrary number of bins

    bkg_tot =  yield_adder_func( *[ yld.getNiceYieldDict()[b] for b in ['WJets', 'QCD', 'DYJetsM50', 'TTJets', 'ZJetsInv'] ] )


    """
    def func_wrapper(*ds):
        return dict_manipulator( list(ds) , func)
    return func_wrapper

yield_adder_func = make_dict_manipulator( lambda *bins: sum(bins)) 
yield_adder_func2 = make_dict_manipulator( lambda *bins:  sum(bins).round(2) )

def sig_yield_adder( bins = [ ] ):
    return dict_manipulator( bins, func = yield_adder_func )


def dict_operator ( ylds , keys = [] , func =  lambda *x: sum(x) ):
    """
    use like this dict_operator( ylds.getByBins() , keys = ['DataBlind', 'Total'] , func = lambda a,b: a/b)

    or for fancier use:
    dict_operator( ylds.yieldDictFul, keys=['tt','w','d'] , func = yield_dict_adder )


    """
    args = [ ylds[x] for x in keys]
    return func(*args)



###########################################################################################################################
###########################################################################################################################
#########################################        TABLES         ###########################################################
###########################################################################################################################
###########################################################################################################################

texDir="./tex/"
#pdfDir="/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/dmt_regions/tables/"
pdfDir="/afs/hephy.at/user/n/%s/www/T2Deg13TeV/Test/"%username
pklDir="./pkl/dmt_regions/*.pkl"

def fix(x):
    ret = str(x).replace("+-","$\pm$").replace("-+","$\mp$").replace(">","$>$").replace("/","/").replace("","")
    if "_{" in ret:
        pass
    else:
        ret = ret.replace("_","-")
    return ret 

def fixForLatex(x):
  if type(x)==type(""):
    return fix(x)
  if type(x) in [ type([]), type(()) ] : 
    return [fix(ix) for ix in x]
  if type(x) in [ type(np.array([])) ]:
    return np.array( [ fix(ix) for ix in x ] )

def uround(x,n=2):
    if hasattr(x,"round"):
        return x.round(n)
    elif type(x) == float:
        return round(x,n)
    elif type(x) == int:
        return x


from collections import OrderedDict
fixDict = OrderedDict()

#print fixDict

#fixDict["MET200_ISR100_HT300"]  =  "$E_{T}^{miss}$ $>$ $200GeV$ , $H_{T}$ $>$ $300GeV$, $P_{T}$(Leading$ $Jet) $>$ $100GeV$ " 
#fixDict["MET200_ISR110_HT300"]  =  "$E_{T}^{miss}$ $>$ $200GeV$ , $H_{T}$ $>$ $300GeV$, $P_{T}$(Leading$ $Jet) $>$ $110GeV$ "  
fixDict["MET200-ISR100-HT300"]  =  "$C_{T1}$ $>$ $200GeV$ ,$P_{T}(IsrJet)$ $>$ $100GeV$ " 
fixDict["MET200-ISR110-HT300"]  =  "$C_{T1}$ $>$ $200GeV$ ,$P_{T}(IsrJet)$ $>$ $110GeV$ "  
fixDict["MET200"]  =  "$E_{T}^{miss}$ $>$ $200GeV$" 
fixDict["HT300"]  =  "$H_{T}$ $>$ $300GeV$"  
fixDict["CT300"]  =  "$C_{T1}$ $>$ $300GeV$"  
fixDict["ISR110"]  =  " $P_{T}(IsrJet)$  $>$ $110GeV$"  
fixDict["ISR100"]  =  " $P_{T}(IsrJet)$  $>$ $100GeV$"  
#fixDict["ISR325"]  =  " $P_{T}(IsrJet)$  $>$ $325GeV$"  
fixDict["ISR325"]  =  " $C_{T2}(IsrJet)$  $>$ $300GeV$"  
fixDict["Met300"]  =  "$E_{T}^{miss}$ $>$ $300$"  
fixDict["No3rdJet60"]  =  "$Hard$ $3rd$ $Jet$ $Veto$"  
fixDict["1Lep-2ndLep20Veto"]  =  "$Single$ $Lep$" 
fixDict["AntiQCD"]  =  "$\Delta\phi(j1,j2)<2.5$ (if 2 hard jets)"
fixDict["negLep"]  =  "$Charge(l)$ $<$ $0$"  
fixDict["BVeto"]  =  "$BJet$ $Veto$"  
fixDict["TauVeto"]  =  "$Tau$ $Veto$"  
fixDict["SoftBJet"]  =  "$Soft$ $BJet$"  
fixDict["LepPt30" ]  =  "$ P_{T}(l)$ $<$ $30GeV$"  
fixDict["LepPt_lt_30" ]  =  "$ P_{T}(l)$ $<$ $30GeV$"  
fixDict["LepPt-lt-30" ]  =  "$ P_{T}(l)$ $<$ $30GeV$"  
fixDict["LepEta1.5"]  =  "$ |\eta(l)|  $ $<$ $1.5$"  
fixDict["-pos"]  =  "-Q+"  
fixDict["-neg"]  =  "-Q-"  



fixDict["Other"]  =  "Other" 
fixDict["T2-4bd-"]  =  "Signal" 
fixDict["T2_4bd_"]  =  "Signal" 
fixDict["DYJetsM50"]  =  "DYJets" 
fixDict["WJets"]  =  "WJets" 
fixDict["ZJetsInv"]  =  "ZJetsInv" 
fixDict["TTJets"]  =  "TTJets" 
fixDict["Total"]  =  "Total S.M."
fixDict["DataBlind"]  =  "Data(12.9fb-1)"
fixDict["DataUnblind"]  =  "Data(4.0fb-1)"
#fixDict["Total"]  =  "Total S.M."

def fixRowCol(x):
    ret = x[:]
    fixed = False
    #print "-----------------------------------------", x,ret , x==ret, fixed
    for this,that in fixDict.iteritems():
        if this in ret:
            ret = ret.replace(this,that)
            fixed = True
            break 
    #if not fixed:
    #    if not "$" in ret:
    #        ret = "$%s$"%ret

    return ret

import os

#templateDir = "/afs/hephy.at/user/n/nrad/CMSSW/fork/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/python/tools/LaTexJinjaTemplates/"
templateDir = cmsbase + "/src/Workspace/DegenerateStopAnalysis/python/tools/LaTexJinjaTemplates/"

class JinjaTexTable():
    def __init__(self,yieldInstance, yieldOpt=None, texDir="./tex/", pdfDir=pdfDir, outputName="",\
                 searchpath=templateDir, template_file= "", removeJunk=True, tableNum=1, caption="", title="", transpose=False, noFOM =False, 
                 combineBkgs = [] , seperators=[] ):
        """
            combineBkgs = [ ["DYJetsM50", "ZJetsInv", "QCD"] , "Other" ] 

        """ 
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

        self.isDataTable = True if self.yields.dataList else False
            

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
        self.templateEnv.filters['fixRowCol']= fixRowCol
        self.templateEnv.filters['uround']= uround

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

        sampleLegend = ylds.sampleLegend[:]
        cutNames     = ylds.cutNames[:]

        if not yieldOpt:
            yieldDict = ylds.getNiceYieldDict()
        elif hasattr(yieldOpt,"__call__") :
            yieldDict = yieldOpt(ylds)
        else:
            yieldDict = getattr(ylds, yieldOpt)
        yieldDict = deepcopy(yieldDict)

        for d in ylds.dataList:
            dataName = ylds.sampleNames[d] if ylds.sampleNames[d] in yieldDict.keys() else d
            print yieldDict[dataName]
            for dataBin in yieldDict[dataName].keys():
                #print "before" , yieldDict[dataName][dataBin]
                yieldDict[dataName][dataBin] = int( getattr(yieldDict[dataName][dataBin],"val", yieldDict[dataName][dataBin] ) )
                #print "after" , yieldDict[dataName][dataBin]


        if noFOM:
            yieldDict = { k:v for k,v in yieldDict.iteritems() if "FOM" not in k}
            sampleLegend = [samp for samp in sampleLegend if "FOM" not in samp]
        
        #combine_bkgs = [ ] 
        if combineBkgs:
            bkgs_to_combine = combineBkgs[0]
            combined_bkgs_name = combineBkgs[1]
            combined_yields = yield_adder_func2( *[ yieldDict[bkg] for bkg in combineBkgs[0] ] )
            yieldDict[ combined_bkgs_name ] = combined_yields
            sampleLegend.insert( sampleLegend.index("Total"), combined_bkgs_name)
            for bkg in bkgs_to_combine:
                print "```", bkg
                yieldDict.pop(bkg)
                sampleLegend.remove(bkg)
        sampleLegend = sortBy( sampleLegend , [ "TTJets","WJets" ]  , reverse=True)

        if transpose:
            self.info.update( {
                             "yieldDict"      :     yieldDict,  
                             "rowList"        :     sampleLegend,
                             "colList"        :     cutNames ,
                             "title"          :     self.title,
                             "caption"        :     self.caption,
                                })
        else:
            self.info.update( {
                             "yieldDict"      :     ylds.getByBins( yieldDict ) ,
                             "rowList"        :     cutNames ,
                             "colList"        :     sampleLegend,
                             "title"          :     self.title,
                             "caption"        :     self.caption,
                            })
        self.info.update( {"seperators":seperators} )

        self.makeTable(self.yields,self.outputName, self.info) 

        #if transpose == "both":
        #    self.makeTable(self.yields,self.outputName self.info) 
        #    self.makeTable(self.yields,self.outputName self.info) 

    def makeTable(self,yields, outputName, info ):
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
        # print(self.out)
        self.fout.write( self.out)
        self.fout.close()
        self.fout2 = open( self.pdfDir + "/" + outputName ,'w')
        self.fout2.write( self.out)
        self.fout2.close()
        print "LaTex File:", self.texDir+outputName
        print "LaTex output:", self.outputTex
        print "pdf output:", self.pdfDir
        os.system("pdflatex -output-directory=%s %s"%(self.pdfDir,self.outputTex))

        removeJunk=True 
        if removeJunk:
            out = self.pdfDir+"/"+outputName
            os.system("rm %s"%out.replace(".tex",".aux"))            
            os.system("rm %s"%out.replace(".tex",".log"))            

def pdfLatex(texFile, pdfDir, removeJunk = True):
    os.system("pdflatex -output-directory=%s %s"%( pdfDir, texFile))
    if removeJunk:
        out = pdfDir+"/"+os.path.basename( texFile ) 
        os.system("rm %s"%out.replace(".tex",".aux"))
        os.system("rm %s"%out.replace(".tex",".log"))




def makeSimpleLatexTable( table_list , texName, outDir, caption="" , align_char = 'c|', align_func= lambda align_char, table: (align_char *len(table[1])).rstrip("|")   ):
    #\\begin{document}
    #\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}
    #{\\begin{tabular}{%s}
    #\hline
    """
    align func takes align_char and table_list as arguments
    default: align_func = lambda ac, table : ( ac * len(table[1]) ).strip("|")

    """
    #alignment = align_char *len(table_list[1]).rstrip("|")
    alignment = align_func( align_char , table_list)
    
    header = \
    """
\documentclass[12pt]{paper}
\usepackage{a4}
%%\usepackage[usenames,dvipnames]{color}
\usepackage{amssymb,amsmath}
\usepackage{amsfonts}
\usepackage{epsfig,graphics,graphicx,graphpap,color}
\usepackage{slashed,xspace,setspace}
\usepackage{caption}
\usepackage{rotating}
\usepackage{fullpage}
\usepackage[top=0.83in]{geometry}
\usepackage{longtable}
\usepackage{multirow}
\usepackage{hhline}
\\begin{document}
\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}
{\\begin{tabular}{%s}
    """%( alignment )

    body = ""
    first_line = True
    for row in table_list:
        if "hline" in row[0] or "hline" in row:
            body +="\hline \n"
            continue
        body += " & ".join([ "%s"%fixForLatex( str(x)) for x in row]) #+ "\\\ \n"
        if len(row)>1:
            body += "\\\ "

        body += "\n"

        if first_line and len(row)>1:
            body+= "\hline\n"
            first_line = False

    footer = \
    """
\end{tabular}}
\end{center}\caption*{%s}\end{table}\end{document}
    """%caption
    
    table = header + body + footer

    texFile = outDir+"/"+texName + ".tex"
    f = open( texFile, 'w')
    f.write( table)
    f.close()

    #os.system("pdflatex -output-directory=%s %s"%(pdfDir, texDir))
    pdfLatex(texFile , outDir ) 

    return header + body + footer





############################## Stop LSP Stuff

def getMasses(string):
    masses = []
    string = get_filename(string)
    splitted = re.split("_|-", string)
    #splitted = string.rsplit("_"):
    for s in splitted:
        if s.startswith("s8tev"):
            s = s[5:]
        if s.startswith("s"):
            s = s[1:]
        if not s.isdigit():
            continue
        masses.append(s)
    if len(masses)!=2 or int(masses[0]) < int(masses[1]):
        raise Exception("Failed to Extract masses from string: %s , only got %s "%(string, masses))
    return [int(m) for m in masses]

def getMasses2(string):
    masses = []
    string = get_filename(string)
    splitted = re.split("_|-", string)
    #splitted = string.rsplit("_"):
    for s in splitted:
        if s.startswith("s8tev"):
            s = s[5:]
        if s.startswith("s"):
            s = s[1:]
        if not s.isdigit():
            continue
        masses.append(s)
    if len(masses)!=2 or int(masses[0]) < int(masses[1]):
        return False
    return [int(m) for m in masses]

def getValueFromDict(x, val="0.500", default=999):  ##  can use dict.get()?
    try:
        ret = x[val]
    except KeyError:
        ret = default
    #else:
    #    raise Exception("cannot find value %s in  %s"%(val, x))
    return float(ret)
