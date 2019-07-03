import ROOT
import os, sys
import re
import gc
import uuid 
import math
import random
import pickle
import numpy as np
import pprint as pp
import glob
import jinja2
import time
import hashlib
import base64
import itertools
import multiprocessing 
import argparse

from array import array
from copy import deepcopy
from collections import OrderedDict, Mapping

import Workspace.HEPHYPythonTools.tdrstyle as tdrstyle
import Workspace.HEPHYPythonTools.CMS_lumi as CMS_lumi
import Workspace.DegenerateStopAnalysis.samples.samplesInfo as samplesInfo 

from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.u_float import u_float
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.tools.ratioTools import *
from Workspace.DegenerateStopAnalysis.tools.FOM import *
from Workspace.DegenerateStopAnalysis.tools.degCuts import CutClass
from Workspace.DegenerateStopAnalysis.tools.degWeights import decide_cut_weight, decide_weight2
from Workspace.DegenerateStopAnalysis.tools.colors import colors as sample_colors


ROOT.TH1.SetDefaultSumw2(1)
#ROOT.gStyle.SetCanvasPreferGL(1)

cmsbase = os.getenv("CMSSW_BASE")

def setup_style(tdrstyle = tdrstyle):
    tdrstyle.setTDRStyle()
    return

#############################################################################################################
##########################################                    ###############################################
##########################################    ETC  TOOLS      ###############################################
##########################################                    ###############################################
#############################################################################################################


def setHistErrorToZero(hist):
    h = hist.Clone()
    h.SetError(array( "d",[0]* (h.GetNbinsX()+1) ) )
    return h

def ceilTo(x,v=1):
    return (int(x/v)+1)*v 

def intOrFloat(v):
    v=float(v)
    if int(v) == float(v):
        ret =  int(v)
    else:
        ret = float(v)
    return ret

def u_intOrFloat_str(uf):
    if not hasattr(uf,'sigma'):
        return intOrFloat(uf)
    else:
        return "%s+-%s"%( intOrFloat(uf.val), intOrFloat(uf.sigma) )
        #return intOrFloat(uf.val), intOrFloat(uf.sigma) )


def safe_round( x, n):
    try:
        ret = x.round(n)
    except AttributeError:
        ret = round(x,n)
    return ret


def round_figures(x, n , func = None):
    
    """Returns x rounded to n significant figures.
       https://mail.python.org/pipermail/tutor/2009-September/071393.html
    """
    if hasattr(x,'sigma'):
        sig = round_figures(x.sigma, n)
        val = x.val
        if not sig or not val:
            return x

        sig_c = math.ceil(math.log10( abs(sig) ))       
        val_c = math.ceil(math.log10( abs(val) ))

        #n2 = max( math.ceil(math.log10( abs(sig) )),n) +max( math.ceil(math.log10( abs(x.val) )), n ) -n
        n2 = n-sig_c 
        print  val_c, sig_c, n2
        #ret=u_float( round_figures(x.val, n2), sig )
        ret=u_float( round(val,int(n2)), sig )
        
    else:
        if not x:
            return x
        ret = round(x, int(n - math.ceil(math.log10(abs(x)))))
    if func:
        ret = func(ret)
    return ret 


class AsymFloatProxy( u_float ):
    def __init__( self, central, up, down):
        self.central = central
        self.up  = up
        self.down = down
        self.sigma = max([up,down])
        self.val = central
    def __str__(self):
        return str(self.central)+'+'+str(abs(self.up))+'-'+str(abs(self.down))



getAllAlph  = lambda str: ''.join(ch for ch in str if ch not in ".!>=|<$&@$%[]{}#()/; '\"")
getOnlyAlph = lambda str: ''.join(ch for ch in str if ch.isalpha() )
addSquareSum = lambda x: math.sqrt(sum(( e**2 for e in x   )))

anyIn = lambda a, b: any(i in b for i in a)

def whichIn(of_these, this):
    rets = []
    for thing in of_these:
        if thing in this:
            rets.append(thing)
    return rets

def whichOneIn(of_these, in_this):
    this = whichIn( of_these, in_this)
    if len(this)>1: 
        raise Exception("Found more than one of these (%s) in this (%s)"%(of_these, in_this))
    elif len(this)==1:
        return this[0] 
    else:
        return None

def whichOfTheseHaveAnyOfThose( these, those, default = []):
    ret = []
    for this in these:
        if anyIn( those, this):
            ret.append(this)
    ret = ret if ret else default
    return ret



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
    if os.path.isdir(path):
        return
    else:
        mkdir_p(path)

def saveCanvas(canv, dir="./", name="", formats=["png"], extraFormats=["root","C","pdf"], make_dir=True):
    if "$" in dir: 
        dir = os.path.expandvars(dir)
        if "$" in dir:
            raise Exception("Unresolved environmental variables! %s"%dir)
    if not os.path.isdir(dir) and make_dir: 
        makeDir(dir)
    if type(formats)!=type([]):
        formats = [formats]
    for form in formats:
        canv.SaveAs(dir + "/%s.%s"%(name,form))
    if extraFormats:
        extraDir = dir + "/extras"
        if not os.path.isdir(extraDir): mkdir_p(extraDir)
        for form in extraFormats:
            canv.SaveAs(extraDir+"/%s.%s"%(name,form))

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


def makeFuncStar(func):
    def funcStar(a_b):
        """Convert `f([1,2])` to `f(1,2)` call."""
        return func(*a_b)
    return funcStar

def merge_dict(d1, d2):
    """
    Modifies d1 in-place to contain values from d2.  If any value
    in d1 is a dictionary (or dict-like), *and* the corresponding
    value in d2 is also a dictionary, then merge them in-place.
    stolen from: http://stackoverflow.com/questions/10703858/python-merge-multi-level-dictionaries
    """
    for k,v2 in d2.items():
        v1 = d1.get(k) # returns None if v1 has no value for this key
        if ( isinstance(v1, Mapping) and 
             isinstance(v2, Mapping) ):
            merge_dict(v1, v2)
        else:
            d1[k] = v2


def natural_sort(list, key=lambda s:s):
    """
    Sort the list into natural alphanumeric order.
    http://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort
    """
    def get_alphanum_key_func(key):
        convert = lambda text: int(text) if text.isdigit() else text 
        return lambda s: [convert(c) for c in re.split('([0-9]+)', key(s))]
    sort_key = get_alphanum_key_func(key)

    lc = sorted(list, key=sort_key)
    return lc


def sortkeypicker(keynames):
    """
        can be used as the key for sort function, to sort a list of dictionaries based on the given keys
        
    """
    negate = set()
    #for i, k in enumerate(keynames):
    #    if k[:1] == '-':
    #        keynames[i] = k[1:]
    #        negate.add(k[1:])
    def getit(adict):
       composite = [adict.get(k) for k in keynames if adict.get(k) ]
       #for i, (k, v) in enumerate(zip(keynames, composite)):
       #    if k in negate:
       #        composite[i] = -v
       return composite
    return getit


def drawLatex( txt = '', x=0.4, y=0.9,  font=22, size=0.04 ):
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(size)
    latex.SetTextFont(font)
    if txt: latex.DrawLatex(x,y,  txt)
    return latex


    

def getTerminalSize():
    """
    stolen from the consule module
    http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    """
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct
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
    #return hashlib.md5("%s"%time.time()).hexdigest()    
    return "uqhsh" + str( uuid.uuid4() ).replace("-","")

def hashString( string ):
    s = base64.b64encode( hashlib.md5( string ).digest() )
    return s

def getHostName():
    hostname = os.path.expandvars("$HOSTNAME")
    return hostname


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

def compareEventLists( elist1, elist2 ):
    el1 = elist1.Clone()
    el2 = elist2.Clone()
    el1.Intersect(el2)    
    el1.Subtract(el2)    
    el2.Subtract(el1)
    el1.Subtract(el2)



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
        eList = f.Get(eListName).Clone()
        eList.SetDirectory(0) 
        f.Close()
    return eList

def getEventListFromChain(sample,cut,eListName="",tmpDir="./",opt="write", verbose=True, attempt = 0 ):
    if not eListName or eListName.lower()=="elist" : 
        print "WARNING: Using Default eList Name, this could be dangerous! eList name should be customized by the sample name and cut" 
        eListName="eList" 
    sample.SetEventList(0) 
    sample.Draw(">>%s"%eListName, cut ) 
    eList=ROOT.gDirectory.Get(eListName)
    if opt.lower() in ["write", "w", "save", "s" ]:
        eListPath="%s/%s.root"%(tmpDir,eListName)
        if verbose: print "EventList saved in: %s"%eListPath
        f = ROOT.TFile(eListPath,"recreate")
        eList.Write()
        f.Close()
        if not os.path.isfile(eListPath):
            print '****'*20
            time.sleep(3)
            if not os.path.isfile( eListPath ):
                print 'Attempt %s: Event List File not Found \n %s \n '%(attempt, eListPath)
                if attempt > 3:
                    print "Tried 3 times but this keeps failing!!!"
                    assert False
                else:
                    getEventListFromChain(sample,cut,eListName="",tmpDir="./",opt="write", verbose=True, attempt = attempt+1 )
                    
    return eList

def getFileSize( f ):
    try:
        size = os.path.getsize( f )
    except:
        size = None
    return size
        
def isGoodEList( f , min_size = 800):
    #print "Testing %s"%f
    if not os.path.isfile( f ):
        return False
    if getFileSize( f ) < 800:
        return False
    el_name = get_filename(f)
    tf = ROOT.TFile( f )
    try:
        elist = tf.Get(el_name)
        if not elist:
            return False
        if not hasattr(elist, "GetN"):
            return False
    except:
        return False
    return True
        

def setEventListToChain(sample,cut,eListName="",verbose=True,tmpDir=None,opt="read"): 
    sample.SetEventList(0) 
    if not tmpDir:
        tmpDir = os.getenv("CMSSW_BASE") + "/src/Workspace/DegenerateStopAnalysis/eLists"
    makeDir(tmpDir)
    eListPath="%s/%s.root"%(tmpDir,eListName)
    if opt.lower() in ["read","r", 'check']:
        #fsize = getFileSize( eListPath )
        #if fsize and fsize > 800:
        if isGoodEList( eListPath , 800):
            if opt == 'check':
                if verbose: 
                    print " "*12, "Found EList", eListName 
                return 
            else:
                eList = getEventListFromFile(eListName=eListName,tmpDir=tmpDir,opt=opt)
        else:
            if verbose: print "eList was not found in:%s "%eListPath
            opt="write"
    if opt.lower() in ["make","m","write", "w","s","save"] : 
        if verbose: print " "*12, "Creating EList", eListName 
        eList = getEventListFromChain(sample,cut,eListName,tmpDir=tmpDir,opt=opt)
    if verbose: print " "*12, "Setting EventList to Chain: ", sample, "Reducing the raw nEvents from ", sample.GetEntries(), " to " 
    sample.SetEventList(eList) 
    #assert eList.GetN() == sample.GetEventList().GetN() 
    return eList


def setEventListToChainWrapper( args ):
    sample, name, cutName, cutString, verbose, opt = args
    if verbose and opt not in ['check']:
        pp.pprint("Sample %s applying cut %s: %s "%(sample['name'], cutName, cutString))
    eListName = "eList_%s_%s"%(name, cutName)
    stringsToBeHashed = []
    sample_file_list  = [x.GetTitle()+"_size_%s"%os.path.getsize(x.GetTitle() ) for x in sample['tree'].GetListOfFiles() ]
    stringsToBeHashed.extend( sorted( sample_file_list ) )
    stringsToBeHashed.append( cutString    )
    stringToBeHashed = "/".join(stringsToBeHashed)
    sampleHash = hashlib.sha1(stringToBeHashed).hexdigest()
    eListName +="_%s"%sampleHash
    tmpDir = os.path.expandvars("$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/eLists/%s/%s"%(name, cutName))
    
    setEventListToChain(sample['tree'],cutString,eListName=eListName,verbose=False, tmpDir=tmpDir, opt=opt)
    if verbose:
        if sample['tree'].GetEventList():
            if verbose: 
                print " "*6 ,"Sample:", sample.name,   'Cut:', cutName,  "Reducing the raw nEvents from ", sample['tree'].GetEntries(), " to ", sample['tree'].GetEventList().GetN()
        elif opt in ['check']:
            pass
        else:
            print "FAILED Setting EventList to Sample", sample.name, sample['tree'].GetEventList() , opt

def setEventListsFromCutWeights(samples, sampleList, cut_weights, cutNames=None, nProc = 15, redo = False, keep_chain_elist = False):
    opt = 'write' if redo else ('read' if keep_chain_elist else 'check')
    if not cutNames:
        cutNames = cut_weights.keys()
    args = [[samples[samp], samp, cutName, cut_weights[cutName][samp][0], True, opt] for samp in sampleList for cutName in cutNames]
    if "worker" in getHostName() or keep_chain_elist: # multiprocesses kills the worker! also to keep the elist, multiprocess doesn't work
        nProc = 1
    res = runFuncInParal(setEventListToChainWrapper, args, nProc= nProc)
    if not keep_chain_elist or len(cutNames)>1:
        print "Setting EventLists to 0 for all samples"
        for samp in sampleList:
            samples[samp]['tree'].SetEventList(0)
    return 
    

def setEventListToChains(samples,sampleList,cutInst,verbose=True,opt="read"):
    if cutInst:
        if isinstance(cutInst,CutClass) or hasattr(cutInst,"combined"):
            cutName     = cutInst.fullName
        else:
            cutName, cutString = cutInst
        if verbose:
            pp.pprint("Applying EventLists to samples in: %s"%sampleList)
        for sample in sampleList:
            if not sample in samples.keys(): 
                print "Sample %s not in samples.keys()"%sample
                continue
            cutString = decide_cut( samples[sample], cutInst, plot=None, nMinus1=None    )
            if verbose:
                pp.pprint("Applying cut %s: "%cutString)

            eListName="eList_%s_%s"%(sample,cutName)
            #   stringsToBeHashed = [] 
            #   #sample_file_list = [x.GetTitle() for x in samples[sample]['tree'].GetListOfFiles]
            #   #stringsToBeHashed.extend( sorted( sample_file_list ) )
            #   if samples[sample].has_key("dir"):
            #       stringsToBeHashed =    [samples[sample]['dir']]    
            #   if samples[sample].get("sample"): # and samples[sample]['sample'] :
            #       stringsToBeHashed.extend( sorted( samples[sample]['sample']['bins'] )    )
            #   stringsToBeHashed.append( cutString    )
            #   #print stringsToBeHashed
            #   stringToBeHashed = "/".join(stringsToBeHashed)
            #   sampleHash = hashlib.sha1(stringToBeHashed).hexdigest()
            #   eListName +="_%s"%sampleHash

            ## hash the rootfiles with their sizes and the full cutstring
            stringsToBeHashed = []
            sample_file_list  = [x.GetTitle()+"_size_%s"%os.path.getsize(x.GetTitle() ) for x in samples[sample]['tree'].GetListOfFiles() ]
            stringsToBeHashed.extend( sorted( sample_file_list ) )
            stringsToBeHashed.append( cutString    )
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
        print "No cut... EventList set to 0" 

#############################################################################################################
##########################################                    ###############################################
##########################################    DECORATOION     ###############################################
##########################################                    ###############################################
#############################################################################################################

def drawCMSHeader( preliminary = "Preliminary", lumi = 35.9, lxy = [0.16,0.915], rxy=[0.77,0.915], textR="%0.1f fb^{-1} (13 TeV)", cmsinside=True):
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    font=52
    latex.SetTextFont(font)
    #latexTextL = "#font[%s]{CMS %s}"%(font, preliminary)
    #latexTextL = "CMS %s"%(preliminary)
    cmstext = "#font[61]{CMS}"
    if not cmsinside:
        latexTextL = cmstext
        if preliminary:
            latexTextL += "  #font[%s]{%s}"%(font,preliminary)
        latex.DrawLatex(lxy[0],lxy[1],  latexTextL)
    else:
        textCMSlarge = ROOT.TLatex()
        textCMSlarge.SetNDC()
        textCMSlarge.SetTextSize(0.06)
        textCMSlarge.SetTextAlign(13)   
        textCMSlarge.SetTextFont(42)
        textCMSlarge.DrawLatex(0.21,0.85, cmstext)

        if preliminary:
            prelim = "#font[%s]{%s}"%(font,preliminary)
            textPrelimlarge = ROOT.TLatex()
            textPrelimlarge.SetNDC()
            textPrelimlarge.SetTextSize(0.06*0.6)
            textPrelimlarge.SetTextAlign(13)   
            textPrelimlarge.SetTextFont(42)
            textPrelimlarge.DrawLatex(0.21,0.78, prelim)

       
    if "%" in textR:
        textR      = textR%lumi
    latexTextR = "#font[%s]{%s}"%(font,textR)
    #latexTextR = "#font[%s]{%0.1f fb^{-1} (13 TeV)}"%(lumi)
    latex.DrawLatex(rxy[0],rxy[1],  latexTextR)

def sampleName(name, sample_names = samplesInfo.sample_names, name_opt = "niceName", isSignal = False, verbose = False):
    """
    name_opt should be one of ['niceName', 'latexName', 'shortName']
    """

    orig_name = name[:]
    if isSignal:
        model, m1, m2 = getMasses(name, returnModel = True)
        name = model

    possibleNames = {}
    for n, ndict in sample_names.iteritems():
        possibleNames[n] = ndict.values()
    foundIt = False
    for n, pNames in possibleNames.iteritems():
        if name in pNames:
            if foundIt:
                raise Exception("found multiple matches to the name %s"%name)
            foundIt = n
    if not foundIt:
        raise Exception("Did not find a sample corresponding to: %s"%name)
    wantedName = sample_names[foundIt][name_opt]
    if isSignal:
        wantedName = "%s%s_%s"%( wantedName, m1, m2 )
        wantedName = wantedName.replace(".","p")
    if verbose:
        print "choose", wantedName, " for ", orig_name
    return wantedName

def makeLumiTag(lumi, latex=False):
    """ lumi given in pb """
    if latex:
        tag = "%0.1f fb^{-1}"%(round(lumi/1000.,2))
    else:
        tag = "%0.1f fbm1"%(round(lumi/1000.,2))
    return tag

def getDataLumi(lumi_dict, eras):
    lumi = sum([lumi_dict[era]['lumi'] for era in eras])
    return round(lumi,1)

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
        hist.SetLineWidth(3)
        #hist.SetLineStyle(5)
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
    if dd.has_key('bin_labels'):
        bin_labels = dd['bin_labels']
        nBins = hist.GetNbinsX()
        assert nBins == len(bin_labels), "Number of bins and bin labels dont match!: %s, %s"%( nBins,  bin_labels)
        xaxis = hist.GetXaxis()
        for ib , bin_label in enumerate(bin_labels, 1) :
            xaxis.SetBinLabel( ib, str(bin_label))

def decorate(hist,color='',width='',histTitle='',fillColor=''):
  if color: hist.SetLineColor(color)
  if width: hist.SetLineWidth(width)
  if histTitle: hist.SetTitle(histTitle)
  if fillColor: hist.SetFillColor(fillColor)
  return

def decorAxis(hist, axis,t="",tSize="",tFont="",tOffset="",lFont="",lSize="",func="", center = False):
    if not hist:    return
    if not axis:    return
    if axis.lower() not in ['x','y','z']: assert False
    axis = getattr(hist,"Get%saxis"%axis.upper() )()
    if t:       axis.SetTitle(t)
    if tSize  : axis.SetTitleSize(tSize)
    if tFont  : axis.SetTitleFont(tFont)
    if tOffset: axis.SetTitleOffset(tOffset)
    if lFont  : axis.SetLabelFont(lFont)
    if lSize  : axis.SetLabelSize(lSize)
    if center : axis.CenterTitle()
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

def getGoodPlotFromChain(c, var, binning, varName='', cutString='(1)', weight = 'weight_lumi', color = '', lineWidth = '', fillColor = '', histTitle = '', binningIsExplicit = False, addOverFlowBin = False): 
  ret = getPlotFromChain(c, var, binning, cutString = cutString, weight = weight, binningIsExplicit = binningIsExplicit, addOverFlowBin = addOverFlowBin) 
  if not varName:
    varName = getAllAlph(var)
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
  #print "::::::::::::::::::::::::::::::::::::::::::: Getting stack" , sName
  if not sName:
    sName = "stack_%s"%uniqueHash()
  stk=ROOT.THStack(sName,sName)

  if transparency:
    alphaBase=0.80
    alphaDiff=0.70
    alphas=[alphaBase-i*alphaDiff/len(histList) for i in range(len(histList)) ]
    #print alphas
    #print histList

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


def normalizeStack( stack, norm_to= None):
    if not norm_to:
        norm_to = getTotalFromStack( stack)
    hists = [x.Clone() for x in stack.GetHists() ]
    for h in  hists:
        h.Divide( norm_to)
    normalized_stack = getStackFromHists( hists ) 
    normalized_stack.SetMinimum(0)
    normalized_stack.SetMaximum(1.1)
    return normalized_stack 

def getTotalFromStack(stack):
    hists = stack.GetHists()
    tot   = hists.Last().Clone("total_"+stack.GetName())
    tot.Reset()
    tot.Merge(hists)
    return tot

def getSamplePlots(samples,plots,cut,sampleList=[],plotList=[],plots_first = False):
    cut_name = cut if type(cut) == type("") else cut.fullName
    if not sampleList: sampleList = samples.keys()
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
    if not sampleList: sampleList = samples.keys()
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


def getTotHistFromStack(stack):
    mc_hist = stack.GetHists().Last().Clone(stack.GetName()+"_tot_" + uniqueHash() )
    mc_hist.Reset()
    mc_hist.Merge( stack.GetHists() )
    return mc_hist

def getDataMCNormFactor(mcstack,datahist):
    mctot = getTotHistFromStack(mcstack)
    datainteg = datahist.Integral()
    mcinteg   = mctot.Integral()
    normfact  = datainteg/mcinteg
    return normfact


def getBkgSigStacks(samples, plots, cut, sampleList = [], plotList = [], normalize = False, transparency = None, scale = None, sName = None):
    """Get stacks for signal and backgrounds. make vars in varlist are available in samples. no stacks for 2d histograms.     """
    cut_name = cut if type(cut) == type("") else cut.fullName

    sampleList = matchListToDictKeys(sampleList, samples)
    plotList   = matchListToDictKeys(plotList, plots)

    bkgStackDict = {}
    sigStackDict = {}
    dataStackDict = {}

    for v in plotList:
        sName_plot = sName + "_%s"%v if sName else None
        if len(plots[v]['bins'])!=6 or getattr(plots[v],"binningIsExplicit",False):
            bkgStackDict[v]  = getStackFromHists([samples[samp]['cuts'][cut_name][v] for samp in sampleList if not samples[samp]['isSignal'] and not samples[samp]['isData']], normalize = normalize, transparency = transparency, sName= "stack_bkg_" + sName_plot, scale = scale)
            sigStackDict[v]  = getStackFromHists([samples[samp]['cuts'][cut_name][v] for samp in sampleList if     samples[samp]['isSignal']],                                 normalize = normalize, transparency = False, sName= "stack_sig_" + sName_plot)
            dataStackDict[v] = getStackFromHists([samples[samp]['cuts'][cut_name][v] for samp in sampleList if     samples[samp]['isData']],                                   normalize = normalize, transparency = False, sName= "stack_data_" + sName_plot)
    return {'bkg': bkgStackDict,'sig': sigStackDict, 'data': dataStackDict}
  
def getPlot(sample, plot, cut, nMinus1 = "", addOverFlowBin = False, lumi_weight = 'target_lumi', useEList = False, verbose = False):
    plot_info = {}
    c = sample.tree
    var = plot.var

    if type(cut) == type([]) and len(cut) == 2:
        cuts_weights, cutInstName = cut
        cuts = cuts_weights.cuts 
        cut  = getattr(cuts, cutInstName)
        cut_str, weight_str = cuts.getSampleFullCutWeights(sample, [cutInstName], nMinus1 = nMinus1)
        
        cutWeightOptions = cuts_weights.cutWeightOptions
        lumis = cutWeightOptions['settings']['lumis']
    else:
        cut_str, weight_str = decide_cut_weight(sample, cutInst = cut, lumi_weight = lumi_weight, plot = plot, nMinus1 = nMinus1)
        lumis = samplesInfo.lumis

    lumi = lumis[lumi_weight]

    plot_info = {'cut':cut_str, 'weight':weight_str, 'lumi':lumi}
    
    if useEList:
        setEventListToChainWrapper([sample, sampleName(sample.name, name_opt = "shortName", isSignal = sample.isSignal), cutInstName, cut_str, False, 'read'])

    if verbose: 
        print "=== Cut ===\n"
        print cut_str, "\n"
        print "=== Weight ===\n"
        print weight_str

    binningIsExplicit = False
    variableBinning = (False, 1)

    if hasattr(plot, "binningIsExplicit"):
        binningIsExplicit = plot.binningIsExplicit
    if hasattr(plot, "variableBinning"):
        variableBinning = plot.variableBinning
    if type(var) == type(""):
        hist = getPlotFromChain(sample.tree, plot.var, plot.bins, cut_str, weight = weight_str, addOverFlowBin = addOverFlowBin, binningIsExplicit = binningIsExplicit, variableBinning = variableBinning, uniqueName = False)
    elif hasattr(var, "__call__"):
        hist = var(sample, bins = plot.bins, cutString = cut_str, weight = weight_str, addOverFlowBin = addOverFlowBin, binningIsExplicit = binningIsExplicit, variableBinning = variableBinning, uniqueName = False)
    else:
        raise Exception("I'm not sure what this variable is! %s"%var)

    #plot.decorHistFunc(p)
    decorHist(sample, cut, hist, plot.decor) 
    plotName = plot.name + "_" + cut.fullName
    sample.plots[plotName] = hist

    if not sample.has_key("cuts"):
        sample.cuts = Dict()
    if not sample.cuts.has_key(cut.fullName):
        sample.cuts[cut.fullName] = Dict()
    sample.cuts[cut.fullName][plot.name] = hist
    hist.plot_info = plot_info
    
    plot_info_full = plot_info.copy()
    plot_info_full['hist'] = hist
    ret = {"%s_%s"%(sample.name, plotName):plot_info_full}

    return #ret 

def getPlotsSimple(samples,plots,cut):
  for sample in samples.itervalues():
    for plot in plots.itervalues():
      getPlot(sample,plot,cut)


def getPlots(samples, plotsDict, cut, sampleList = [], plotList = [], nMinus1 = "", addOverFlowBin = False, lumi_weight = "target_lumi", verbose = True):

    if verbose: 
        print "\n==========================================\n"
        print "Getting Plots:", plotList

    for sample in samples.iterkeys():
        if not sample in sampleList:
            continue
        if verbose:
            print "\n=====================\n"
            print "Plotting Sample:", samples[sample].name, "\n"

        ret = {}
        plotList = plotList if plotList else plotsDict.keys()
        for plot in plotList:
            if plot not in plotsDict.keys():
                print "Ignoring %s .... not in the Plot Dictionary"%plot
                continue
 
            ret[plot] = getPlot(samples[sample], plotsDict[plot], cut, nMinus1 = nMinus1, addOverFlowBin = addOverFlowBin, lumi_weight = lumi_weight, verbose = verbose)
    
    return #ret

          
def getSigBkgDataLists(samples, sampleList):
    sigList =  [samp for samp in sampleList if samples[samp]['isSignal']]
    bkgList =  [samp for samp in sampleList if not samples[samp]['isSignal'] and not samples[samp]['isData']]
    dataList = [samp for samp in sampleList if samples[samp]['isData']]
    return sigList, bkgList, dataList

def makeLegend(samples, hists, sampleList, plot, name="Legend",loc=[0.6,0.6,0.9,0.9],borderSize=0,legOpt="f"):
    leg = ROOT.TLegend(*loc)
    leg.SetName(name)
    leg.SetFillColorAlpha(0,0.001)
    leg.SetBorderSize(borderSize)

    for samp in sampleList:
        isSignal = samples[samp]['isSignal']
        samp_name = sampleName(samp, name_opt = 'latexName', isSignal = isSignal)
        if isSignal:
            model_masses = getSigModelMasses( samp_name) 
            samp_name = "%s(%s,%s)"%tuple(model_masses) 
        #samp_name = samples[samp]['name']
        legOpt_ = "lep" if samples[samp]['isData'] else legOpt
        if plot:
            leg.AddEntry(hists[samp][plot], samp_name , legOpt_)    
        else:
            leg.AddEntry(hists[samp], samp_name , legOpt_)    
    return leg

def addHistsToLeg( leg, hists_info):
    """
        hists_info = [ {'hist':<TH1F> , 'name':<hist_name> ,'opt':'f'}, {... }]
    """
    for hist_info in hists_info:
        h    = hist_info['hist']
        name = hist_info['name']
        opt  = hist_info.get("opt","f")
        leg.AddEntry( h, name, opt)
    return leg

def getPlotFromYields(name, yields, keys=[], labelOpt = "v", labelSize = None, labelFormatFunc = None):
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
        if labelFormatFunc:
            k =  labelFormatFunc(k)
        hist.GetXaxis().SetBinLabel(i,k)
    hist.GetXaxis().LabelsOption( labelOpt)
    if labelSize:
        hist.GetXaxis().SetLabelSize( labelSize )
    return hist  

def drawYields( name , yieldInst, sampleList=[], keys=[], ratios=True, plotMin = 0.01, plotMax= None, logs = [0,1], 
                save="", normalize = False, ratioLimits=[0,1.8], labelOpt = "v", labelSize=None , labelFormatFunc = None):

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

    if dataList:
        data = dataList [0]
        dataTag = sampleName(data, name_opt = "latexName")

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
        yldplt[sample] = getPlotFromYields(sample+"_"+name, yieldDict[sample], keys=keys, labelOpt = labelOpt, labelSize = labelSize , labelFormatFunc = labelFormatFunc)
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
        stacks.GetYaxis().SetTitle("Events")
        stacks.SetMinimum(plotMin)
        maxval = plotMax if plotMax else stacks.GetMaximum()* ( 1.35 + logs[1]*10  )
        stacks.SetMaximum( maxval)
        if drawError:
            bkg_tot.Draw("same E2")
        
    for sig in sigList:
        yldplt[sig].SetLineWidth(2)
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
    for samp in bkgList:
        samples[samp] = {'name':sampleName(samp, name_opt = "latexName"), 'isData':False, 'isSignal':False}
    for samp in sigList:
        samples[samp] = {'name':sampleName(samp, name_opt = "latexName", isSignal = True), 'isData':False, 'isSignal':True}
    for samp in dataList:
        samples[samp] = {'name':sampleName(samp, name_opt = "latexName"), 'isData':True, 'isSignal':False}
        
    bkgLegList = bkgList[:] 
    sigLegList = sigList[:] 
    
    bkgLegList.reverse()
    sigLegList.reverse()
    sigLegList += dataList

    legy = [0.7, 0.87]
    legx = [0.75, 0.95] 
 
    nBkgInLeg = 4
    if anyIn(sampleList, bkgLegList):
        subBkgLists = [ bkgLegList[x:x+nBkgInLeg] for x in range(0,len(bkgLegList),nBkgInLeg) ]
        nBkgLegs = len(subBkgLists)
        for i , subBkgList in enumerate( subBkgLists ):
            newLegY0 = legy[0] + (legy[1]-legy[0])* (1-1.*len(subBkgList)/nBkgInLeg)
            bkgLeg = makeLegend(samples, yldplt , subBkgList, None, loc=[legx[0], newLegY0 ,legx[1],legy[1]], name="Legend_bkgs%s_%s_%s"%(i, name, "LEG"), legOpt="f")
            ret.append(bkgLeg)
            ret[-1].Draw()
            legx = [ 2*legx[0] -legx[1] , legx[0]  ] 
            #del bkgLeg

    if anyIn(sampleList, sigLegList):
       sigLeg = makeLegend(samples, yldplt, sigLegList, None, loc=[legx[0],legy[0],legx[1],legy[1]], name="Legend_sigs_%s_%s"%(name, "LEG"), legOpt="l")
       sigLeg.Draw()
       ret.append(sigLeg)
       ret[-1].Draw()

    if len(dataList):
       year = "2016" # FIXME
       latex = ROOT.TLatex()
       latex.SetNDC()
       latex.SetTextSize(0.04)
       lumiTag = makeLumiTag(samplesInfo.lumis[year][sampleName(dataList[0], name_opt = 'niceName')], latex=True)
       latex.DrawLatex(0.165,0.92,"#font[22]{CMS Preliminary}")
       latex.DrawLatex(0.76,0.92,"\\mathrm{ %s (13\, TeV)}"%lumiTag)
       ret.append(latex)    

    canvs[cMain].SetLogx(logs[0])
    canvs[cMain].SetLogy(logs[1])
    canvs[cMain].Update()

    if ratios:
        canvs[cMain+1].cd()
        canvs[cMain+1].SetGrid()
        ratio_ref = bkg_tot.Clone("ratio_ref_%s"%name)
        #ratio_ref.SetError(array( "d",[0]* ratio_ref.GetNbinsX() ) )
        #ratio_ref.Divide(ratio_ref)
        ratio_ref.Reset()
        #if True: ## draw data/MC
        if dataList: ## draw data/MC
            print 'data is here!'
            #ratio_ref.SetLabelSize(0.04,"Y")
        
            ratio_ref.Draw("hist")
            ratio_ref.GetYaxis().SetTitle("DATA/MC")
            ratio_ref.SetMinimum(ratioLimits[0])
            ratio_ref.SetMaximum(ratioLimits[1])    
   
            MCE = bkg_tot.Clone("MCError_%s"%name)
            bkg_tot_noe =  bkg_tot.Clone("bkg_tot_noe_%s"%name)
            bkg_tot_noe.SetError(array( "d",[0]* (bkg_tot_noe.GetNbinsX()+1) ) )
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
            #    bkg_tot.SetError(array( "d",[0]*nBins ) )    # bkg_tot with no error
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
        

        #ratio_ref.GetXaxis().SetLabelSize(0.10)
        ratio_ref.GetYaxis().SetLabelSize(0.09)
        ratio_ref.GetYaxis().SetTitleOffset(0.85)
        ratio_ref.GetYaxis().SetTitleSize(0.09)
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
#                bkg_tot.SetError(array( "d",[0]*nBins ) )    # bkg_tot with no error
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

def drawPlots(samples, plotsDict, cut, sampleList = [], plotList = [], lumi_weight = "target_lumi", 
              plotMin = False, plotLimits = [], save = True,
              fom = False , fomIntegral = True, normalize = False, pairList = None, fomTitles = False, 
              denoms = None, noms = None, ratioNorm = False, fomLimits = [], mc_scale = None,
              leg = True, unity = True, verbose = False, dOpt = "hist", postfix = ""):
    
    if normalize and fom and fom.lower() != "ratio":
        raise Exception("Using FOM on area  normalized histograms... This can't be right!")
    
    if type(cut) == type([]) and len(cut) == 2:
        cuts_weights, cutInstName = cut
        cuts = cuts_weights.cuts 
        cut = getattr(cuts, cutInstName)
        
        cutWeightOptions = cuts_weights.cutWeightOptions
        lumis = cutWeightOptions['settings']['lumis']
    else:
        lumis = samplesInfo.lumis

    lumi = lumis[lumi_weight]

    cut_name = cut if type(cut) == type("") else cut.fullName

    dOpt_ = dOpt
    ret = {}
    canvs = {}

    hists  = getSamplePlots( samples, plotsDict, cut, sampleList = sampleList, plotList = plotList)
    stacks = getBkgSigStacks(samples, plotsDict, cut, sampleList = sampleList, plotList = plotList, normalize = normalize, transparency = normalize, scale = mc_scale, sName = cut_name)
    sigList, bkgList, dataList = getSigBkgDataLists(samples, sampleList = sampleList)

    if mc_scale:
        postfix +="_MCSCALE%s"%(str(mc_scale).replace(".","p")) 

    ret.update({
                'canvs':canvs       , 
                'stacks':stacks     ,
                'hists':hists       ,
                'fomHists':{}       ,
                'sigBkgDataList': [sigList,bkgList,dataList],
                'legs':[]           ,
                'hist_info' : {}    ,
                'junk' : []    ,
                })
    
    isDataPlot = bool(len(dataList))
    
    if len(dataList) > 1:
        raise Exception("More than one Data Set in the sampleList... This could be dangerous. %"%dataList)       
    for p in plotsDict.iterkeys():
        dOpt = dOpt_ 
        if plotList and p not in plotList:
            continue
        if plotsDict[p]['is2d']:
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

            canvs[p] = makeCanvasMultiPads(c1Name = "canv_%s_%s"%(cut_name,p), c1ww = 800, c1wh = 800, joinPads = True, padRatios = padRatios, pads = [])
            cSave, cMain, cFom = 0, 1, 2 # index of the main canvas and the canvas to be saved
        else: 
            canvs[p] = ROOT.TCanvas("canv_%s_%s"%(cut_name,p), "canv_%s_%s"%(cut_name, p), 800, 800), None, None
            cSave, cMain = 0, 0
        
        canvs[p][cMain].cd()
        
        if isDataPlot:
            dataHist = hists[dataList[0]][p]            
            dataHist.SetMarkerSize(0.9)
            dataHist.SetMarkerStyle(20)
            dataHist.Draw("E0P")
        
        if normalize: 
            #stacks['bkg'][p].SetFillStyle(3001)
            #stacks['bkg'][p].SetFillColorAlpha(kBlue, 0.35)
            dOpt+="nostack"
        if len(bkgList):
            refStack=stacks['bkg'][p]
            refStack.Draw(dOpt + "same")
            #if logy: canvs[p][cMain].SetLogy(logy)
            dOpt="same"

            errBarHist = refStack.GetStack().Last().Clone(p+"errBarHist")
            errBarHist.SetFillColor(ROOT.kBlue-5)
            errBarHist.SetFillStyle(3001)
            errBarHist.SetMarkerSize(0)
            errBarHist.Draw("E2same")
            ret['junk'].append(errBarHist)
        elif len(sigList):
            refStack = stacks['sig'][p]
        elif len(dataList):
            refStack = dataHist  

        if len(sigList):
            stacks['sig'][p].Draw("%s nostack"%dOpt.replace("hist",""))
        
        if plotsDict[p].has_key("decor"):
            if plotsDict[p]['decor'].has_key("y"):             decorAxis(refStack, 'y', plotsDict[p]['decor']['y'], tOffset=1.2, tSize = 0.05)
            if plotsDict[p]['decor'].has_key("x") and not fom: decorAxis(refStack, 'x', plotsDict[p]['decor']['x'], tOffset=1.4, tSize = 0.04)
            if plotsDict[p]['decor'].has_key("title"): refStack.SetTitle(plotsDict[p]['decor']['title']) 
            if plotsDict[p]['decor'].has_key("log"):
                logx, logy, logz = plotsDict[p]['decor']['log']
                if logx: canvs[p][cMain].SetLogx(1)
                if logy: canvs[p][cMain].SetLogy(1)
        
        if plotMin: refStack.SetMinimum(plotMin)
        
        if plotLimits: 
            refStack.SetMinimum(plotLimits[0])
        if logy: 
            refStack.SetMaximum(25*refStack.GetMaximum())
        else:
            refStack.SetMaximum(1.2*refStack.GetMaximum())
                
        if leg:
            bkgLegList = bkgList[:] 
            sigLegList = sigList[:] 
            
            bkgLegList.reverse()
            sigLegList.reverse()
            sigLegList += dataList

            legy  = [0.66, 0.87]
            legy2 = [0.73, 0.87]
            
            if fom:
               legx = [0.78, 0.98]
            else:
               legx = [0.7, 0.85]

            nBkgInLeg = len(bkgLegList)/2 + 1
            if anyIn(sampleList, bkgLegList):
                print "!!!!!!!!!!", bkgLegList, nBkgInLeg
                subBkgLists = [ bkgLegList[x:x+nBkgInLeg] for x in range(0,len(bkgLegList),nBkgInLeg) ]
                nBkgLegs = len(subBkgLists)
                for i, subBkgList in enumerate(subBkgLists):
                    newLegY0 = legy[0] + (legy[1] - legy[0])*(1-1.*len(subBkgList)/nBkgInLeg)
                    bkgLeg = makeLegend(samples, hists, subBkgList, p, loc = [legx[0], newLegY0, legx[1], legy[1]], name = "Legend_bkgs%s_%s_%s"%(i, cut.name, p), legOpt = "f")
                    ret['legs'].append(bkgLeg)
                    ret['legs'][-1].Draw()
                    legx = [2*legx[0] - legx[1], legx[0]] 
                    del bkgLeg

            if anyIn(sampleList, sigLegList):
               sigLeg = makeLegend(samples, hists, sigLegList, p, loc = [legx[0]*0.90, legy2[0], legx[1], legy2[1]], name = "Legend_sigs_%s_%s"%(cut.name, p), legOpt = "l")
               sigLeg.Draw()
               ret['legs'].append(sigLeg)

        if fom:
           if plotsDict[p]['decor'].has_key('fom_reverse'):
               fom_reverse = plotsDict[p]['decor']['fom_reverse']
           else: fom_reverse = True

           if pairList:
               getFOMPlotFromStacksPair(ret, p, sampleList, fom=fom, fomIntegral=fomIntegral, normalize=normalize,
                                             denoms=denoms, noms=noms, ratioNorm=ratioNorm, fomLimits=fomLimits, pairList=pairList, fomTitles=fomTitles,
                                             leg=leg, unity=unity, verbose=verbose)
           else:
               getFOMPlotFromStacks(ret, p, sampleList, fom=fom, fomIntegral=fomIntegral, fom_reverse=fom_reverse, normalize=normalize,
                                             denoms=denoms, noms=noms, ratioNorm=ratioNorm, fomLimits=fomLimits,
                                             leg=leg, unity=unity, verbose=verbose)
           if bkgList:
               canvs[p][cMain].cd()
               ret['hists']['bkg'][p].SetFillColor(1)
               ret['hists']['bkg'][p].SetFillStyle(3001)
               ret['hists']['bkg'][p].SetMarkerSize(0)
               ret['hists']['bkg'][p].Draw("E2same")
           for c in canvs[p]:
              if c: c.RedrawAxis()
        
        if not fom:
           canvs[p][cMain].SetRightMargin(10)
        else:
           canvs[p][cMain].SetRightMargin(0.03)
           canvs[p][cSave].SetRightMargin(0.03)
           canvs[p][cFom].SetRightMargin(0.03)

           for c in canvs[p]:
              if c: c.RedrawAxis()

        canvs[p][cMain].cd()
        canvs[p][cMain].RedrawAxis()
        canvs[p][cMain].Update()
        #canvs[p][cMain].SetLeftMargin(15) 
        
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.04)
        #latex.SetTextAlign(11)

        lumiTag = makeLumiTag(lumi)
        print "Reweighting %s MC histograms to lumi %s"%(plotsDict[p].name, lumiTag)

        if isDataPlot:
            drawCMSHeader(lumi)
        else:
            latexTextL = "#font[22]{CMS Simulation}"
            latexTextR = lumiTag

            if fom:
                latex.DrawLatex(0.16,0.92, latexTextL)
                latex.DrawLatex(0.75,0.92, latexTextR)
            else:
                latex.DrawLatex(0.16,0.96, latexTextL)
                latex.DrawLatex(0.6,0.96,  latexTextR)

        if mc_scale:
            latex.DrawLatex( 0.35, 0.7, "MC SF:%s"%mc_scale)

        ret['latex'] = latex
        if not isDataPlot:
            ret['latexText'] = {'L': latexTextL, 'R':latexTextR}

        canvs[p][cSave].Update()

        sample_hist_info = getSamplePlotsInfo(samples, plotsDict, cut, sampleList = sampleList, plotList = plotList, plots_first = True)

        if verbose:
            #canvs[p][cSave].plot_info =
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    HIST INFO"
            print sample_hist_info 
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

        if save:
            saveDir = save if type(save)==type('') else "./"
            saveCanvas(canvs[p][cSave], saveDir, p + postfix, formats = ["png"], extraFormats = ["root","C","pdf"])
            pp.pprint(sample_hist_info[p], open(saveDir + "/extras/%s.txt"%p ,"w"))

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

def getFOMPlotFromStacks( ret, plot, sampleList ,fom=True, fomIntegral = True, fom_reverse = False,  normalize=False, 
                          denoms=None,noms=None, ratioNorm=False , fomLimits=[0.8,2],
                          unity=True, verbose=False , leg=True):

        hists = ret['hists']
        hists['bkg']={} 
        stacks = ret['stacks']
        canvs = ret['canvs']
        fomHists = ret['fomHists']
        sigList, bkgList, dataList = ret['sigBkgDataList']
        fomFunc = fom if type(fom)==type('') else "AMSSYS"
        fomIntegral = False if fomFunc =="RATIO" else ""
        fomMax = 0
        fomMin = 999
        fomHists[plot]={}
        ret['junk']=[]
        if "ratio" in fomFunc.lower():
            pass
        #print "isdataplot:",  [ x in dataList for x in noms ]
        if not noms:
            noms = sigList
        if not denoms:
            denoms = ['bkg']
        
        if any( [ x in dataList for x in noms ]):       
            isDataPlot=True
            fomPlotTitle_ = "Data/MC     " if "bkg" in denoms else "AAAAAAAAAAAAAA"
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

            if denom in noms: noms.remove(denom)

            fomMin, fomMax = (100,-100)
            for nom in noms:
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
                    decorAxis(fomHists[plot][denom][nom], 'x', tSize=0.1,  lSize=0.1, tOffset = 1.1)
                    decorAxis(fomHists[plot][denom][nom], 'y', t='%s  '%fomPlotTitle, tOffset=0.8,  tSize=0.07, lSize=0.1, center = True, func= lambda axis: axis.SetNdivisions(506))
                    #decorAxis(fomHists[plot][denom][nom], 'y', t='%s  '%fomPlotTitle   , tOffset=0.5 ,  tSize=1./len(fomPlotTitle), lSize=0.1, func= lambda axis: axis.SetNdivisions(506) )
                    fomHists[plot][denom][nom].SetTitle("")
                    dOpt="same"

            if isDataPlot:
                bkg_tot = hists['bkg'][plot].Clone("bkg_tot")
                bkg_tot.SetError(array( "d",[0]*(nBins+1) ) )    # bkg_tot with no error
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

def getFOMPlotFromStacksPair( ret, plot, sampleList ,fom=True, fomIntegral = True, normalize=False, 
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
        fomIntegral = False if fomFunc =="RATIO" else ""
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


def getPieChart(samples, sampleList, cut):
    ylds = []
    colors = []
    for samp in sampleList:
        weightStr = "weight_lumi" if not samples[samp].has_key("weight") else samples[samp]["weight"]
        ylds.append(  getYieldFromChain(samples[samp]['tree'], cut.combined, weightStr) )
        colors.append( samples[samp]['color'] )

    ylds = array("f",ylds)
    colors = array("i",colors)
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

def getAndDrawQuickPlots(samples,var,bins=[],varName='',cut="(1)",weight="weight_lumi", sampleList=['s','w'],min=False,logy=0,save=True,fom=True, leg=True,unity=True):
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
            ret['hists'][sampKey]=getGoodPlotFromChain(samp.tree, var, binning = bins, varName=varName, cutString=cut, weight=weightStr, color = samp.color, lineWidth=3 )
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
        canv.SaveAs(saveDir+'/%s.png'%varName)
    return ret

def getTH2MaxBinContent(hist):
    bcs = getTH2FbinContent(hist)
    return max( itertools.chain( *[ y.values() for x,y in bcs.items() ] ) )
    
def getTH2DwithVarBins( c, var,  cutString = "(1)", weight = "weight_lumi"  , xbins=[0,2], ybins=[0,3], name = "testhist"):
    htmp = name +"_"+uniqueHash()
    print ( len(xbins)-1, array('d', xbins), len(ybins)-1, array('d', ybins) )
    h = ROOT.TH2D(htmp, htmp, len(xbins)-1, array('d', xbins), len(ybins)-1, array('d', ybins) )
    c.Draw(var+">>%s"%htmp, weight+"*("+cutString+")", 'goff')
    return h






def getHistBins(hist ):
    xbins = [hist.GetXaxis().GetBinLowEdge(ix+1) for ix in range(hist.GetNbinsX() +1 )  ]
    ybins = [hist.GetYaxis().GetBinLowEdge(iy+1) for iy in range(hist.GetNbinsY() +1 )  ]
    return xbins,ybins




def getTH2FbinContent(hist , legFunc= lambda xtitle,ytitle : (xtitle,ytitle)):
    """
       legFunc can be used to change the xtitle and ytitle in the output dictionary 
    """
    nbinsx = hist.GetNbinsX()
    nbinsy = hist.GetNbinsY()
    cont = {}
    for x in range(1,nbinsx+1):
        xbin = int( hist.GetXaxis().GetBinCenter(x) )
        #cont[xbin]={}
        for y in range(1,nbinsy+1):
            ybin = int( hist.GetYaxis().GetBinCenter(y) )
            bincontent = hist.GetBinContent(x,y)
            if bincontent:
                xtitle,ytitle = legFunc(xbin,ybin)
                if not cont.has_key(xtitle):
                    cont[xtitle]={}
                cont[xtitle][ytitle]=hist.GetBinContent(x,y)
    return cont


def getTH1FbinContent(hist, keep_order = False, get_errors = False):
    '''
        returns (Ordered)Dict with binLabels and binValues (not sure if this works for unlabled axis)
    '''
    if type(hist) in [ROOT.THStack]:
        stack = hist.Clone()
        hist  = getTotalFromStack(stack)


    bin_labels = [ hist.GetXaxis().GetBinLabel(ib) for ib in range(1, hist.GetNbinsX() +1 ) ]
    if get_errors:
        #bin_erros  = [ hist.GetBinError(ib) for ib in range(1, hist.GetNbinsX() + 1 ) ]
        bin_values = [ u_float( hist.GetBinContent(ib) , hist.GetBinError(ib) )  for ib in range(1, hist.GetNbinsX() +1 ) ]
    else:
        bin_values = [ hist.GetBinContent(ib)  for ib in range(1, hist.GetNbinsX() +1 ) ]
    
    labels_values =  zip( bin_labels, bin_values) 
    d = OrderedDict if keep_order else dict
    return d( labels_values ) 

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

 

def getBinning( m1_range = (250,801,25) , m2_range = (10,81,10) ):
    min_m1 , max_m1, step_m1 = m1_range
    min_m2 , max_m2, step_m2 = m2_range
    max_m1 -= max_m1%10
    max_m2 -= max_m2%10
    m1s = range(  *m1_range )
    m2s = range(  *m2_range )
    n_m1 = len(m1s)
    n_m2 = len(m2s)
    x=10
    return [    n_m1,     min_m1 - 0.5* step_m1 ,    max_m1 + 0.5*step_m1, 
                int( ( (max_m1 - min_m2)+x/2.   -  (min_m1-max_m2-x/2.) )/x) , (min_m1-max_m2)-x/2. , (max_m1 - min_m2)+x/2. ]




def makeStopLSPPlot(name, massDict, title="", bins = [23, 237.5, 812.5, 125, 167.5, 792.5]  , key=None, func=None,setbin=False, massFunc = None , xtitle="m(#tilde{t})[GeV]", ytitle="m(#tilde{#chi}^{0})[GeV]", merge_bins = False):
    # ("test", bins =[ 23, 237.5, 812.5, 8,10,80] , massFunc = lambda mstop, mlsp : [mstop, mstop-mlsp]
    """
    massDict should be of the form {    
                                    stopmass1: { lsp_mass_1: a, lsp_mass_2: b ... },
                                    stopmass2: { lsp_mass_1: c, lsp_mass_2: d ...},
                                    ...
                                    }
    with a, b, c,d ... the bin content TH2D
    if key available then key(a) will be evaluated
    if func available then func(mstop,mlsp) will be evaluted. (func will override key)
    ## if massFunc:  stop_mass, lsp_mass  = massFunc(key)
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
    #elif massFunc:
    #    for k,val in massDict.iteritems():
    #        masses  = massFunc(k)
    #        if not masses: 
    #            continue
    #        stop_mass, lsp_mass = masses
    #        val = val if not key else key(val)
    #        bin_to_fill = plot.FindBin(int(stop_mass),int(lsp_mass) ) 
    #        if plot.GetBinContent(bin_to_fill):
    #            raise Exception("Seems binning seems to fill dublicate values for %s, %s..... check the binning!"%(stop_mass,lsp_mass))
    #        plot.SetBinContent(bin_to_fill, val)
    #        #plot.Fill(int(stop_mass), int(lsp_mass), val)


    else:
        for stop_mass in massDict:
            for lsp_mass in massDict[stop_mass]:
                hasSigma = False
                if func:
                    val = func(stop_mass, lsp_mass)
                elif key:
                    val = key(massDict[stop_mass][lsp_mass])
                else:
                    val = massDict[stop_mass][lsp_mass]
    
                if hasattr(val, "sigma"):
                    sigma = val. sigma
                    val = val.val
                    hasSigma = True
                stop_mass, lsp_mass = (stop_mass, lsp_mass) if not massFunc else massFunc(stop_mass, lsp_mass)
                #bin_to_fill = plot.FindBin(int(stop_mass),int(lsp_mass) ) 
                bin_to_fill = plot.FindBin(stop_mass,lsp_mass ) 
                #print bin_to_fill , stop_mass, lsp_mass, val
                if plot.GetBinContent(bin_to_fill) and not merge_bins:
                    raise Exception("Seems like same bin (%s) is being filled with more than one value for %s, %s..... check the binning!"%(bin_to_fill, stop_mass,lsp_mass))
                plot.SetBinContent( bin_to_fill, val )
                if hasSigma:
                    plot.SetBinError( bin_to_fill, sigma )
                #plot.Fill(int(stop_mass), int(lsp_mass) , val )
    plot.SetTitle(title)

    plot.SetNdivisions(0,"z")
    plot.SetNdivisions(410,"x")
    plot.GetXaxis().SetTitle(xtitle)
    plot.GetYaxis().SetTitle(ytitle)
    return plot


def makeStopLSPRatioPlot(name, massDictNom, massDictDenom, title="", bins=[23, 237.5, 812.5, 125, 167.5, 792.5], key=None ):
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
                    val = key( massDictNom[mstop][mlsp] ) / key( massDictDenom[mstop][mlsp]  ) if  key( massDictDenom[mstop][mlsp]  ) else 0 
                else:
                    val = massDictNom[mstop][mlsp] / massDictDenom[mstop][mlsp] if massDictDenom[mstop][mlsp] else 0
                ratio_dict[mstop][mlsp] = val 
    ratio_pl = makeStopLSPPlot( name, ratio_dict, title=title , bins=bins )
    return ratio_pl, ratio_dict


limit_keys = {
                 '-1.000': {'label':'obs'    ,  'color':ROOT.kBlack    , 'style':1     }   ,
                  '0.025': {'label':'down2'  ,  'color':0              , 'style':7     }   ,
                  '0.160': {'label':'down1'  ,  'color':0              , 'style':5     }   ,
                  '0.500': {'label':'exp'    ,  'color':ROOT.kRed      , 'style':3     }   ,
                  '0.840': {'label':'up1'    ,  'color':ROOT.kYellow   , 'style':5     }   ,
                  '0.975': {'label':'up2'    ,  'color':ROOT.kGreen    , 'style':7     }   ,
             }


def get1DLimitHists(name, di  , limit_keys = limit_keys):
    hists = {}
    for limit_key, limit_info in limit_keys.items() :
        limit_label = limit_info['label']
        hists[limit_label] = makeHistoFromDict( di, name = name+"_"+limit_label, func = lambda x: x[limit_key] , bin_order = sorted(di) )
        hists[limit_label].SetLineColor(limit_info['color'])
        hists[limit_label].SetFillColor(limit_info['color'])
        hists[limit_label].SetLineStyle(limit_info['style'])
    return hists 

def makeTGraph(name, di, bin_order = None, limit_keys = limit_keys , xtitle="", ytitle="", title="", limits = [] ) :
    if not bin_order:
        bin_order = sorted(di.keys())

    values_raw = {}
    values_rel = {}
    nbins = len(bin_order)
    for limit_key, limit_info in limit_keys.items():
        limit_label = limit_info['label']    
        values_raw[limit_label] = [ di[b][limit_key] for b in bin_order ]
    for limit_label in [l['label'] for l in limit_keys.values() ]: 
        if anyIn(['down', 'up'] , limit_label.lower()):
            values_rel[limit_label] = [ abs( values_raw[limit_label][b] - values_raw['exp'][b] ) for b in range(nbins) ]
        else:
            values_rel[limit_label] = values_raw[limit_label]        

    arrs = dict_function( values_rel, lambda x: array('d', x) )
    arrs['zero'] = array('d', [0]* nbins )
    arrs['x']    = array('d', bin_order)
    sig1 = ROOT.TGraphAsymmErrors( nbins , arrs['x'], arrs['exp'], arrs['zero'],arrs['zero'], arrs['down1'], arrs['up1'])
    sig2 = ROOT.TGraphAsymmErrors( nbins , arrs['x'], arrs['exp'], arrs['zero'],arrs['zero'], arrs['down2'], arrs['up2'])
    exp  = ROOT.TGraph( nbins , arrs['x'], arrs['exp'] )
    obs  = ROOT.TGraph( nbins , arrs['x'], arrs['obs'] )


    for g, color, title, name in ( (sig1, ROOT.kGreen , "Expected #pm 1#sigma" , "Expected1Sigma" ),
                                   (sig2, ROOT.kYellow, "Expected #pm 2#sigma" , "Expected2Sigma" )
                                  ):
        g.SetFillColor(color)
        g.SetTitle(title)
        g.SetName(name)
        g.SetMarkerSize(0)
        g.SetMarkerStyle(21)
        g.GetYaxis().SetTitleSize(0.04)
    exp.SetTitle("Expected")
    obs.SetTitle("Observed")
    
    for g in (exp, sig1, sig2):
        g.SetLineStyle(5)
        g.SetLineColor(ROOT.kRed)

    if limits:
        if limits[0] : sig2.SetMinimum( limits[0] )
        if limits[1] : sig2.SetMaximum( limits[1] )

    sig2.SetTitle(title)
    sig2.GetXaxis().SetTitle(xtitle)
    sig2.GetYaxis().SetTitle(ytitle)
    sig2.Draw("a3")
    sig1.Draw("same 3")
    exp.Draw("same")
    obs.Draw("same")

    return sig2, sig1, exp, obs


def getDiagonalPointsFromMassDict(d, dm):
    masses = sorted(d.keys())
    ret = {}
    for m1 in masses:
        m2 = m1-dm
        if not m2 in d[m1]:
            continue
        ret[m1]=d[m1][m2]
    return ret


def makeStopLSP1DPlot(name, hists):
    stack = ROOT.THStack(name, name)
    hists_list = hists.values() if type(hists)==dict else hists
    for h in hists_list:
        stack.Add(h)
    return stack

#############################################################################################################
##########################################                    ###############################################
##########################################    YIELDS CLASS    ###############################################
##########################################                    ###############################################
#############################################################################################################

def runFuncInParal( func, args , nProc = 15 ):
    #nProc=1
    if nProc >1:
        pool         =   multiprocessing.Pool( processes = nProc )
        results      =   pool.map( func , args)
        pool.close()
        pool.join()
    else:
        results = map(func,args)
    return results

#getYieldFromChainStar =  makeFuncStar(getYieldFromChain)
#funcStar = getYieldFromChainStar

def getYieldFromChainStar(args):
    return getYieldFromChain(*args)
def getYieldFromChainCutWeights(args):
    (chain_dict, cut_weight, samp,b, useELists) = args
    c,w = cut_weight
    if useELists: 
        setEventListToChainWrapper( [chain_dict[samp], samp, b, c, False, 'read'] )
    ret = (b,u_float(* getYieldFromChain(chain_dict[samp]['tree'], c,w , returnError=True) ) )
    #print samp, b, ret
    return ret 

def getYieldsForSampleParal( self, tree_dict, cut_weights, nProc=None ):
    yieldDict = {}
    for samp in self.sampleList:
        print samp, nProc
        bins = cut_weights.keys() 
        useELists = self.useELists
        if not nProc:
            nProc = max(len(bins), 18)
        pool    = multiprocessing.Pool( processes = nProc  )
        start_time = time.time()
        yieldDict_samp = pool.map( getYieldFromChainCutWeights , [ [tree_dict, cut_weights[b][samp], samp, b, useELists  ] for b in bins ]    )
        print samp, time.time() - start_time 
        pool.close()
        pool.join()
        yieldDict[samp]={v[0]:v[1] for v in yieldDict_samp}
        if self.verbose:
            self.pprint( [np.array([self.sampleNames[samp]]+[ uround(yieldDict[samp][cut],3) for cut in self.cutNames] , self.npsize)] , nSpaces=self.nSpaces   )
    #print yieldDict
    return yieldDict        

def getYieldsForSampleFunc(samples, cutList, weights, err, nDigits, yieldDictFull, verbose, pprint, sampleNames, cutNames, npsize, nSpaces): ## This is to make a picklable function for the multiprocessing. Better solution? 
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
        y = Yields(samples, ['tt', 'w','s'], cuts.presel, tableName = '{cut}_test', pklOpt = 1);
    '''
    def __init__(self, samples, sampleList, cutInst, cutOpt = 'flow', tableName = '{cut}', weight = "", pklOpt = False, pklDir = "./pkl/", nDigits = 2, err = True, nProc = None, lumi = 'target_lumi',
                 isMVASample = None, verbose = False, nSpaces = None, cuts = None, useELists = False):

        if not (isinstance(cutInst,CutClass) or hasattr(cutInst,cutOpt)) and not cuts:
            raise Exception("use an instance of cutClass")
        
        if pklOpt: makeDir(pklDir)
       
        self.nDigits = nDigits
        samples = samples
        if cuts:
            cutInst = getattr(cuts[0], cuts[1])
            cuts = cuts[0]
        else: 
            cuts = None
            
        self.cutInst = cutInst
        self.weight = weight
        self.tableName = tableName.format(cut=self.cutInst.fullName)
        self.sampleList = [s for s in sampleList if s in samples.keys()]
        self.sampleList.sort(key = lambda x: samples[x]['isSignal'])
        self.npsize="|S20"
        self.err = err
        self.nProc = nProc
        self.isMVASample = isMVASample
        self.cutOpt = cutOpt
        self.useELists = useELists 
        self.lumi_string = lumi 
        self.fomNames = {}

        self.updateSampleLists(samples,self.sampleList, cuts)
        
        self.cutList   = getattr(cutInst,cutOpt)
        self.cutLegend = np.array([[""] + [cut[0] for cut in self.cutList]])
        self.cutNames  = list(self.cutLegend[0][1:])

        if not nSpaces:
            terminal_size = getTerminalSize()
            nSpaces = (terminal_size[0] - 10 - len(self.cutLegend[0]))/len(self.cutLegend[0])
        
        self.nSpaces = max(nSpaces, 12)
        self.yieldDictFull = {sample:{} for sample in sampleList}
        self.pklOpt = pklOpt
        self.pklDir = pklDir +"/"
        self.verbose = verbose

        if self.verbose:
           print "Weights:"
           pp.pprint({self.cut_weights[c][s] for c in self.cut_weights.keys() for s in self.dataList + self.bkgList + self.sigList[:3]})

        self.getYieldDictFull(samples, self.cutList, cuts = cuts)

        if self.pklOpt:
            self.pickle(self.pklOpt, self.pklDir)

    def updateSampleLists(self, samples, sampleList, cuts = None):
        self.bkgList        = [samp for samp in   samples.bkgList()  if samp in sampleList]
        self.sigList        = [samp for samp in   samples.sigList()  if samp in sampleList]
        self.dataList       = [samp for samp in   samples.dataList()  if samp in sampleList]
        self.sampleNames    = {samp:fixForLatex(samples[samp]['name']) for samp in sampleList}
        self.sigTypes       = list(set([ sig[:-7] for sig in self.sigList]))

        self.LatexTitles = {}
        self.LatexTitles.update({samp:self.sampleNames[samp] for samp in self.sampleNames})
        self.LatexTitles.update({fomName:self.fomNames[fomName] for fomName in self.fomNames}) 
        self.LatexTitles.update({"Total":"Total"})
        
        isDataPlot = bool(len(self.dataList))
        if isDataPlot:
           self.lumi_weight = samples[self.dataList[0]].name
        else:
           self.lumi_weight = "target_lumi" 

        self.cut_weights = {}
        baseCut = self.cutInst.baseCut
        baseCutName = baseCut.name if baseCut else ""
        for cutName, cutStr in getattr(self.cutInst, self.cutOpt):  
            self.cut_weights[cutName] = {}
            for samp in self.sampleList:
                if cuts:
                    c,w = cuts.getSampleFullCutWeights(samples[samp], cutListNames = [baseCutName, cutName], weightListNames = [])

                    self.cut_weights[cutName][samp] = (c,w)
                else: 
                    self.cut_weights[cutName][samp] = decide_cut_weight(samples[samp], cutInst = cutStr, weight = self.weight, lumi = self.lumi_weight, plot = None, nMinus1 = None)

        if hasattr(self, "LatexTitles"):
            self.sampleLegend = [self.LatexTitles[sample] for sample in self.bkgList] +\
                                ["Total"] +\
                                [self.LatexTitles[d] for d in self.dataList] 
            if self.fomNames:
                for sample in self.sigList:
                    self.sampleLegend.extend([self.LatexTitles[sample], self.LatexTitles["FOM_%s"%sample]])

    def addYieldDict(self, samples, yieldDict, cuts = None):
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
                raise Exception("The new yield dictionary seems to have different cuts than the current one  %s \n vs. %s"%(cuts, sorted(list(self.cutLegend[0][1:]))))

        self.yieldDict.update(yieldDict) # FIXME: should also combine Totals, FOMs, etc
        self.getYieldDictFull(samples, yieldDict = self.yieldDict , cuts=cuts)

    def makeNumpyFromDict(self, yieldDict = None, rowList = []):
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
                exps.append(np.array([self.sampleNames.get(samp,samp)] + [yieldDict[samp][cut] for cut in self.cutNames], self.npsize))
            else:
                exps.append(np.array([samp] + [yieldDict[samp][cut] for cut in self.cutNames], self.npsize))
        return np.concatenate([self.cutLegend, np.array(exps)])
            
    def getBySample(self, sampleList, yieldByBin):
        return {samp:{b: yieldByBin[b][samp] for b in yieldByBin.keys()}  for samp in sampleList}

    def getByBin(self, bin, yieldDict = None):
        if not yieldDict:
            yieldDict = self.yieldDictFull
        return {samp: yieldDict[samp][bin] for samp in yieldDict.keys()}

    def getByBins(self, yieldDict = None):
        if not yieldDict: yieldDict = self.yieldDictFull
        return {bin:{samp:yieldDict[samp][bin] for samp in yieldDict.keys()} for bin in self.cutNames}  

    def round(self, val, nDigits):
        try: 
            return val.round(nDigits)
        except AttributeError:
            return round(val, nDigits)

    def getBkgTotal(self, yieldDict):
        yieldDictTotal = {}
        for cut in self.cutNames:
            summed = sum([yieldDict[samp][cut] for samp in self.bkgList])
            yieldDictTotal[cut] = self.round(summed, self.nDigits)
        return yieldDictTotal

    def getSigFOM(self, yieldDict = None, yieldDictTotal = None, fom = "AMSSYS", uncert = 0.2, nDigits = 3):
        fomDict = {}
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
            fomDict[fom_name] = {}
            for cut in self.cutNames:
                fom_val = calcFOMs(yieldDict[sig][cut], yieldDictTotal[cut], uncert, fom) 
                fomDict[fom_name][cut] = round(fom_val, nDigits) 
        return fomDict

    def getNiceYieldDict(self, yieldDict = None):
        yld = {}
        if not yieldDict: yieldDict = self.yieldDictFull
        for samp in yieldDict:
            yld[self.LatexTitles[samp]] = yieldDict[samp]
        return yld                        

    def getYieldsForSample(self, samples, sample, cutList, rerun = True):
        yieldDictSample = {}
        setSampleEventList = False
        if self.isMVASample and not samples[sample]['tree'].GetEventList():
            setSampleEventList = True
            setMVASampleEventList(samples, sample)

        for ic, cut in enumerate(cutList):
            cutName = cut[0]
            cutStr, weightStr = self.cut_weights[cutName][sample]
            if self.useELists: 
                setEventListToChainWrapper([samples[sample], sample, cutName, cutStr, False, 'read'])

            yld = getYieldFromChain(samples[sample]['tree'], cutStr, weightStr, returnError = self.err)

            if self.err:
                rounded = [round(x,self.nDigits) for x in yld]
                yld = u_float(*rounded)
            else:
                yld = u_float(yld)

            yieldDictSample[cutName] = yld
            self.yieldDictFull[sample][cut[0]] = yld

        if setSampleEventList:
            samples[sample]['tree'].SetEventList(0)
        
        if self.verbose:  
            self.pprint([np.array([self.sampleNames[sample]] + [yieldDictSample[cut] for cut in self.cutNames], self.npsize)], nSpaces = self.nSpaces)
        return yieldDictSample

    def getYields2(self, samples, cutList):
        yieldDict={}
        if self.verbose: self.pprint(self.cutLegend, nSpaces = self.nSpaces)

        if self.useELists:
            ret__ = setEventListsFromCutWeights(samples, self.bkgList + self.dataList + self.sigList, self.cut_weights, keep_chain_elist = False, nProc = 20)

        if self.nProc > 1:
            yieldDict = getYieldsForSampleParal(self, {k:samples[k] for k in self.sampleList}, self.cut_weights, self.nProc)
        else:
            for samp in self.sampleList:
                a = time.time()
                yieldDict[samp] = self.getYieldsForSample(samples,samp, cutList)
                t1 = time.time() - a
                if self.verbose:
                    print samp, 'time:', t1

        self.yieldDict = yieldDict
        return yieldDict
        
    def getYieldDictFull(self, samples, cutList = None, yieldDict = None, yieldDictTotal = None, yieldDictFOMs = None, fom = "AMSSYS", uncert = 0.2, nDigits = 3 , cuts = None):
        yieldDictFull = {}
        if not yieldDict:
            if cutList:
                yieldDict = self.getYields2(samples, cutList)
            else:
                raise Exception("Either a cutList or yieldDict should be given!")

        yieldDictFull.update(yieldDict)
        if not yieldDictTotal:
            yieldDictTotal = self.getBkgTotal(yieldDict)
            if self.verbose:
                print 'bkg total',  yieldDictTotal
            yieldDictFull.update({'Total': yieldDictTotal})

        if yieldDictFOMs:
            if not type(yieldDictFOMs) == type({}):
                yieldDictFOMs = self.getSigFOM(yieldDict, yieldDictTotal, fom = fom, uncert = uncert, nDigits = nDigits)
            yieldDictFull.update(yieldDictFOMs)
            self.yieldDictFOMs = yieldDictFOMs
            self.FOMTable = self.makeNumpyFromDict(self.yieldDict)

        self.yieldDictFull  = yieldDictFull
        self.updateSampleLists(samples, self.sampleList, cuts)
        return yieldDictFull

    def pickle(self,pklOpt,pklDir):
        if self.pklOpt == 1:
            pickle.dump(self,open(pklDir + "YieldInstance_%s.pkl"%self.tableName,"wb"))
            print "Yield Instance pickled in %s"%"YieldInstance_%s.pkl"%self.tableName

        if self.pklOpt == 2:
            pickle.dump(self.table,open(pklDir + "YieldTable_%s.pkl"%self.tableName,"wb"))
            print "Yield Table pickled in    %s"%"YieldTable_%s.pkl"%self.tableName

        if self.pklOpt == 3:
            pickle.dump(self.table,open(pklDir + "YieldTable_%s.pkl"%self.tableName,"wb"))
            pickle.dump(self,open(pklDir + "YieldInstance_%s.pkl"%self.tableName,"wb"))
            print "Yield Instance pickled in %s"%"YieldInstance_%s.pkl"%self.tableName
            print "Yield Table pickled in    %s"%"YieldTable_%s.pkl"%self.tableName

    def __sizeof__(self):
        return object.__sizeof__(self) + sum(sys.getsizeof(v) for v in self.__dict__.values())

    def makeLatexTable(self, table = None):
        if table is None:
            table = self.FOMTable
        lines = []
        first = True
        for line in table:
            new_line = " & ".join(map(str,line)) 
            fixed_line = fixForLatex( new_line)
            fixed_line += " \\\ "
            lines.append( fixed_line )
        
        if first:
            lines[0] += "  \hline"
        ret = " \n".join(lines)
        return ret

    def pprint(self, table = None, transpose = True, nSpaces = 17, align = "<", ret = None):
        if table is None:
            table = self.FOMTable.T
        block = "| {:%s%s}"%(align,nSpaces)
        ret = [(block*len(line)).format(*[uround(col) for col in line]) for line in table]
        if ret:
            return ret

    ####################################################
    ################## Fancy Stuff #####################
    ####################################################

    def getYieldMaps(self, sigList):
            yld_mass_map = {}
            ylds = self
            if not sigList:
                sigList = self.sigList 
            for cut_name in ylds.cutNames:
                yieldDict = ylds.getByBin(cut_name)
                yld_mass_map[cut_name] = {}
                for sig in sigList:
                    yld_value = yieldDict[sig]
                    mstop, mlsp = getMasses(sig)
                    set_dict_key_val( yld_mass_map[cut_name], mstop, {} )
                    set_dict_key_val( yld_mass_map[cut_name][mstop] , mlsp, yld_value)
            return yld_mass_map


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
        name = (lambda x: self.sampleNames[x]) if nice_names else ( lambda x: x)
        yld_bkg_map  = self.getByBins( { name(bkg):self.yieldDict[bkg] for bkg in self.bkgList} )

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

def getDictVal(d,keys):
    return reduce(dict.__getitem__, keys, d)

def dict_function ( d,  func ):
    """
    creates a new dictionary with the same structure and depth as the input dictionary
    but the final values are determined by func(val)
    """
    new_dict = {}
    for k in d.keys():
        v = d.get(k)
        if type(v)==dict:
            ret = dict_function( v , func)         
        else:
            ret = func(v)        
        new_dict[k] = ret
    return new_dict


def dict_walk(d):
    ret = []
    for k, v in d.iteritems():
        keys = []
        keys.append( k )
        if type(v)==type({}):
            print k, v
            keys.extend( dict_walk(v) )
        else:
            print k
            #keys.append( k)
        ret.append(keys)
    return ret


def rd():
    #rnd = random.randint(0,5)
    rnd = random.randint(0,2) 
    #print rnd
    ret = {}
    for i in range( rnd):
        ret["%s"%i]=rd()
    print ret
    return ret


###########################################################################################################################
###########################################################################################################################
#########################################        TABLES         ###########################################################
###########################################################################################################################
###########################################################################################################################

def fix(x):
    ret = str(x).replace("+-","$\pm$").replace("-+","$\mp$").replace(">","$>$").replace("/","/").replace("","")
    if ret.startswith("#"):
        ret = "$%s$"%ret.replace("#","")
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
    if hasattr(x,"round") and hasattr(x,'sigma'):
        return x.round(n)
    elif type(x) == float:
        return round(x,n)
    elif type(x) == int or type(x)==type(""):
        return x
    else:
        return x

templateDir = cmsbase + "/src/Workspace/DegenerateStopAnalysis/python/tools/LaTexJinjaTemplates/"

class JinjaTexTable():
    def __init__(self,yieldInstance, yieldOpt=None, texDir="./tex/", pdfDir='./pdf', outputName="",\
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
        self.templateEnv.filters['fixForLatex'] = fixForLatex
        self.templateEnv.filters['fixRowCol'] = lambda x:x # FIXME 
        self.templateEnv.filters['fix'] = fix
        self.templateEnv.filters['uround'] = uround

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




def makeSimpleLatexTable( table_list , texName, outDir, caption="" , align_char = 'c|', align_func= lambda align_char, table: (align_char *len(table[1])).rstrip("|")  , tableOnly=False ):
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
    r"""
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
\begin{document}
\begin{table}[ht]
\begin{center}
\resizebox{\textwidth}{!}
    """
    tableheader = \
    r"""
\begin{tabular}{%s}
    """%( alignment )

    body = r""
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

    tablefooter = \
    r"""
\end{tabular}}
    """
    footer = \
    r"""
\end{center}
\caption*{%s}
\end{table}
\end{document}
    """%caption
    
    table = tableheader + body + tablefooter
    document = header + table + footer

    if tableOnly:
        document = body

    makeDir(outDir)
    texFile = outDir+"/"+texName + ".tex"
    f = open( texFile, 'w')
    f.write( document )
    f.close()

    #os.system("pdflatex -output-directory=%s %s"%(pdfDir, texDir))
    print document
    if not tableOnly:
        pdfLatex(texFile , outDir ) 

    #return header + body + footer
    return document

############################## Stop LSP Stuff
#sig_prefixes = ['s','cwz', 'cww', 't2tt','t2bw','t2ttold']


sigModelTags = ['t2tt', 't2bw', 'c1c1h', 'c1n1h', 'n2n1h', 'hino', 'tchiwz', 'mssm']

default_binning    = [23, 237.5, 812.5, 63, 165.0, 795.0]
default_binning_dm = [23, 237.5, 812.5, 9, 5, 95 ]
sigModelBinnings = {  
                    'T2bW_DM':  default_binning_dm,
                    'T2tt_DM':  default_binning_dm,
                    'T2tt': default_binning,
                    'T2bW': default_binning, 
                    'C1C1H': [10,100,200,20,100,300],
                    'C1N1H': [10,100,200,10,100,200],
                    'N2N1H': [10,100,200,10,100,200], 
                    #'TChiWZ': [10,100,200,10,100,200],
                    'TChiWZ': [9, 87.5, 312.5, 25,0,51],
                    #'Hino': [10,100,500,10,100,1000],
                    'Hino': [ 8, 90, 250, 11, 250, 1250 ],
                    'MSSM': [ 8, 90, 250, 10, 250, 1250 ],
                  }

latex_mlsp    = 'm(#tilde{#chi}^{0}_{1}) [GeV]'
#latex_mstop   = 'm(#tilde{t})[GeV]'
latex_mstop   = 'm_{#tilde{t}} [GeV]'
latex_mchipm1 = 'm(#tilde{#chi}^{\pm}_{1}) [GeV]' 
latex_mchipm2 = 'm(#tilde{#chi}^{\pm}_{2}) [GeV]' 
latex_mn2     = 'm(#tilde{#chi}^{0}_{2}  ) [GeV]' 
latex_dm      = '#Delta m [GeV]'
latex_mn2c1   = 'm(#tilde{#chi}^{#pm}_{1}),m(#tilde{#chi}^{0}_{2})[GeV]'
latex_mu      = '#mu[GEV]'
latex_M1      = 'M_{1}'

modelsInfo      = {
                    'T2tt':  {  'binning' :default_binning,         'binning_dm' :default_binning_dm,           'xtitle':latex_mstop     , 'ytitle': latex_mlsp, 'ytitle_dm': latex_dm }      , 
                    'T2bW':  {  'binning' :default_binning,         'binning_dm' :default_binning_dm,           'xtitle':latex_mstop     , 'ytitle': latex_mlsp, 'ytitle_dm': latex_dm }      ,     
                    'C1C1H': {  'binning' :[10,100,200,20,100,300], 'binning_dm' :[10,100,200,20,100,300],   'xtitle':latex_mchipm1   , 'ytitle': latex_mlsp, 'ytitle_dm': latex_dm }      ,     
                    'C1N1H': {  'binning' :[10,100,200,10,100,200], 'binning_dm' :[10,100,200,10,100,200],   'xtitle':latex_mchipm1   , 'ytitle': latex_mlsp, 'ytitle_dm': latex_dm }      ,     
                    'N2N1H': {  'binning' :[10,100,200,10,100,200], 'binning_dm' :[10,100,200,10,100,200],   'xtitle':latex_mn2       , 'ytitle': latex_mlsp, 'ytitle_dm': latex_dm }      ,         
         #           'Hino': {  'binning' :[10,100,200,10,100,200], 'binning_dm' :[10,100,200,10,100,200],   'xtitle':latex_mn2       , 'ytitle': latex_mlsp, 'ytitle_dm': latex_dm }      ,         
                   'MSSM': {  'binning' : [ 8, 90, 250, 10, 250, 1250 ] , 'binning_dm' :None,  'xtitle':latex_mu       , 'ytitle': latex_M1, 'ytitle_dm': latex_M1}      ,         
                   'TChiWZ': {  'binning' :[10,100,200,10,100,200], 'binning_dm' :[9, 87.5, 312.5, 25,0,51],   'xtitle':latex_mn2c1   , 'ytitle': latex_mlsp, 'ytitle_dm': latex_dm }      ,         
                 }


sig_prefixes = sigModelTags




def getSignalModel( signal_name ):
    #l = [x.isalpha() for x in reversed(signal_name)]
    #if True in l:
    #    last_alpha_indx = l.index(True)
    #    model = signal_name[:-last_alpha_indx]
    #else:
    #    model = None
    return getSigModelMasses( signal_name)[0]
    #return model


def getMasses(string, returnModel = False):
    masses = []
    string = get_filename(string)
    string = string.replace("-","_")
    #splitted = re.split("_|-", string)
    #splitted = string.rsplit("_"):
    
    #s = string[-7:]
    #masses = re.split("_", s)

    search = re.search("(\d\d\d_\d\d\dp\d\d)|(\d\d\d_\d\d\dp\d)|(\d\d\d_\d\d\d\d)|(\d\d\d_\d\d\d)|(\d\d\d_\d\d)", string)
    #search = re.search("(\d\d\d_\d\d\dp\d\d)|(\d\d\d_\d\d\dp\d)|(\d\d\d_\d\d\d\d)|(\d\d\d_\d\d\d)|(\d\d\d\d\d_\d\d\d)", string)
    if search:
        model  = string.replace(search.group(),"")
        masses = search.group().replace("p",".").rsplit("_")
    if len(masses)!=2 : #or intOrFloat(masses[0]) < intOrFloat(masses[1]):
        return False
        #raise Exception("Failed to Extract masses from string: %s , only got %s "%(string, masses))
    if returnModel:
        return [model.replace("_","") ] + [intOrFloat(m) for m in masses] 
    else:
        return [intOrFloat(m) for m in masses]

def getMasses2(string):
    masses = []
    string = get_filename(string)
    splitted = re.split("_|-", string)
    #splitted = string.rsplit("_"):
    for s in splitted:
        for sig_prefix in sig_prefixes:
            if s.startswith(sig_prefix):
                s = s[len(sig_prefix):]
        if not s.isdigit() and s.replace("p","").isdigit():
            s=s.replace("p",".")
        elif not s.isdigit(): 
            continue
        
        masses.append(s)
    if len(masses)!=2 or intOrFloat(masses[0]) < intOrFloat(masses[1]):
        return False
    return [intOrFloat(m) for m in masses]

def getValueFromDict(x, val="0.500", default=999):  ##  can use dict.get()?
    try:
        ret = x[val]
    except KeyError:
        ret = default
    #else:
    #    raise Exception("cannot find value %s in  %s"%(val, x))
    return float(ret)



def getSigModelMasses( s ):
    #model = getSignalModel(s)
    #masses = getMasses2( s)
    #if masses:
    #    return [model] + masses
    #else:
    #    return None
    modelmasses = getMasses(s, returnModel=True)
    return modelmasses


def getModelsAndMasses( processList , d = {}):
    model_masses = map ( getSigModelMasses , processList)

    output = {}
    for proc in processList:
        modelmass = getSigModelMasses(proc)
        if not modelmass:
            continue
        model, m1, m2 = modelmass
        set_dict_key_val( output, model, {} )
        set_dict_key_val( output[model], m1, {} )
        set_dict_key_val( output[model][m1], m2, d.get(proc,None) )
    return output

def getModelsAndSigs( processList ):
    models = list(set( [ getSignalModel(s_) for s_ in processList ] ))
    sigModelLists = { sigModel:[s_ for s_ in processList if sigModel in s_] for sigModel in models}
    return sigModelLists



def getSignalYieldMap(yieldDict, sigList=[], bins=[], make_hists = False, models_info=modelsInfo):
    """
    Getting the Yield per each bin on the m1 m2 plane
    """
    bins = yieldDict.keys() if not bins else bins

    yld_mass_map = {}
    hists  = {} 
    for b in bins:
        sigList_ = sigList if sigList else yieldDict[b].keys()
        res = getModelsAndMasses( sigList_, yieldDict[b] )
        print res , '------'*20
        for model in res.keys():
            set_dict_key_val( yld_mass_map, model, {} )
            set_dict_key_val( yld_mass_map[model], b , res[model] )
            model_info = models_info.get( model, {} ) 
            binning = model_info.get( 'binning_dm')
            makedm  = True
            if not binning:
                makedm  = False
                binning = model_info.get('binning') 
            print binning
            if make_hists:
                #print model
                hist = makeStopLSPPlot("%s_%s"%(model, b) ,  yld_mass_map[model][b] , 
                                        bins     = binning , 
                                        xtitle   = models_info.get(model,{}).get('xtitle'   , 'm(#tilde{t})[GeV]') ,
                                        ytitle   = models_info.get(model,{}).get('ytitle_dm', '#delta m[GeV]') , 
                                        massFunc = lambda m1,m2 : (m1, m1-m2) if makedm else ( m1, m2 ) ,
                                        )
                set_dict_key_val( hists, model, {} )
                set_dict_key_val( hists[model], b , hist )
    return yld_mass_map, hists 





def makeHistoFromList(lst, bins=None,name ="Histo", func=None):
    if not bins:
        bins = [len(lst),0,len(lst)]
    h = ROOT.TH1F(name,name,*bins)
    for ib,l in enumerate(lst,1):
        if func:
            l = func(l)
        if hasattr(l,"sigma"):
            h.SetBinContent(ib,l.val)
            h.SetBinError(ib,l.sigma)        
        else:
            h.SetBinContent(ib,l)
    return h

#def makeAsymGraph(lst, bins=None, name = "AsymGraph", func=None):
#    if not bins:
#        bins = [len(lst),0, len(lst)]
    
def makeAsymTGraphFromDict(name, li, bin_names = None,   xtitle="", ytitle="", title="", limits = [] , func = lambda item, cen_or_sig: item[cen_or_sig]) :
    nBins = len(bin_names)
    if bin_names:
        x = []
        hist = ROOT.TH1F("hist", "HistForAsymTGraphLabels", nBins, 0, nBins)
        for  iB in range(nBins):
            hist.GetXaxis().SetBinLabel(iB+1, bin_names[iB])
            x.append( hist.GetXaxis().GetBinCenter(iB+1) )
            hist.Fill( x[iB], func( li[bin_names[iB]], 'central')  )

    x_cen      = array('d', x )
    zeros      = array('d', [0]*len(x) )
    y_cen      = array('d', [ func(li[y], 'central' )       for y in bin_names])
    y_err_down = array('d', [ abs(func(li[y], 'down'))  for y in bin_names]) 
    y_err_up   = array('d', [ abs(func(li[y], 'up'  ))  for y in bin_names])


    print x_cen
    print y_cen
    print y_err_down
    print y_err_up

    graph = ROOT.TGraphAsymmErrors(nBins,x_cen,y_cen, zeros, zeros, y_err_down, y_err_up)

    return hist, graph


def setAxisLabels( h, axis='X', labels=[]):
    if axis.lower()=='x':
        a = h.GetXaxis()
    elif axis.lower()=='y':
        a = h.GetYaxis()
    nbins = a.GetNbins()
    assert nbins == len(labels)
    for i in range(nbins):
        a.SetBinLabel( i+1, labels[i] )
    return h



def makeHistoFromDict(di , bins=None, name="Histo", bin_order=None,func=None):
    if bin_order:
        #lst   = [ di[x] for x in bin_order if x in di]
        #labels = [ x for x in bin_order if x in di]
        lst   = [ di.get(x,0) for x in bin_order ]
        labels = bin_order #[ x for x in bin_order if x in di]
    else:
        lst    = di.values()
        labels = di.keys()
    #print lst
    #print labels
    print lst
    h = makeHistoFromList(lst, bins, name, func)
    for ib, bin_label in enumerate(labels,1):
        h.GetXaxis().SetBinLabel( ib, str(bin_label))
    return h


def fillHistoFromList( l , name="Histo" , nBins = None, minVal=None, maxVal=None):
    maxVal = maxVal if maxVal else  max(l)
    minVal = minVal if minVal else  min(l)
    if not nBins:
        nBins = len(set(l))
    h = ROOT.TH1F( name, name, nBins, minVal, maxVal)
    for v in l:
        h.Fill(v)
    return h


def makeTH2FromDict( di , name="histo2d", xbins = None , ybins=None , setlabels = True, func = None, labelFunc = None):
    """
        if func is given, the bin contents will be evaluated as func( dictionary, xbin, ybin)
    """
    xbins_ = xbins if xbins else di.keys()
    ybins_ = ybins if ybins else di[xbins_[0]].keys()    
    nx = len(xbins_)
    ny = len(ybins_)
    hist= ROOT.TH2D( name, name, nx, 0, ny, ny, 0, ny)
    for ix, xbin in enumerate( xbins_):
        for iy, ybin in enumerate( ybins_):
            if not func:
                v = di[xbin][ybin]
            else:
                v = func( di, xbin, ybin)
            hist.SetBinContent(ix+1,iy+1, v)
    if setlabels:
        labelFunc = labelFunc if labelFunc else lambda x:x
        for ix, xbin in enumerate( xbins_):
            hist.GetXaxis().SetBinLabel(ix+1, labelFunc(xbin))
        for iy, ybin in enumerate( ybins_):
            hist.GetYaxis().SetBinLabel(iy+1, labelFunc(ybin) )
        hist.GetXaxis().SetLabelSize(0.035)
        hist.GetYaxis().SetLabelSize(0.035)
        hist.LabelsOption("V")
        
    return hist    
