from Workspace.DegenerateStopAnalysis.tools.degTools import *
from Workspace.DegenerateStopAnalysis.tools.cardFileWriter import cardFileWriter
from Workspace.DegenerateStopAnalysis.tools.FOM import get_float
from array import array
from copy import deepcopy
from os.path import basename, splitext
import ROOT
import pickle
import yaml
import glob
import os
import ROOT
import re
import Workspace.HEPHYPythonTools.user as user


combineLocation = getattr(user, "combineLocation")
if not combineLocation:
    raise Exception("Many of the functions in this script only work within the Higgs combine limits tools framework \n\
                     Please add the location for your combine limit setup in HEPHYPythonTools/python/user.py \n\
                    ")






def makeSystTemplate( syst_bins, sample_names, def_val = 0.0, syst_type ='lnN' ,syst_n = ''):
    syst = {}
    for b in syst_bins:
        syst[b]={}
        for s in sample_names:
            syst[b][s] = def_val
    ret = {'bins': syst , 'type':syst_type}
    return ret


def collect_results( limit_pkl_pattern   , scale_rule = None):
    '''
        scale_rule can be used to rescale r-value in case the x-sec was scaled
        make sure this is consistent with how you rescaled it
        scale_rule = lambda mstop, mlsp: 1000.0 if mstop <=250 else False)

    '''
    limit_pkls = glob.glob( limit_pkl_pattern )
    res  = {}
    for limit_pkl in limit_pkls:
        mstop, mlsp = getMasses(limit_pkl)
        print mstop, mlsp
        if not res.has_key(mstop):
            print 'make key', mstop
            res[mstop]={}
        scale = scale_rule( mstop, mlsp)
        limit = pickle.load(file(limit_pkl))
        print limit 
        if not limit:
            print "!!! WARNING !!! pkl seems empty" , limit_pkl
            continue
        if scale:
            limit = dict_function( limit, lambda x: x*scale )
        res[mstop][mlsp] = limit
    return res





#
# Uncert Tools
#


def make_bin_proc_dict(bins,processes,def_val=0):
    return { b:{p:def_val for p in processes} for b in bins}

def make_bin_proc_dict_from_systs(bins,processes,syst,new_bins_map):
    new_syst = make_bin_proc_dict(bins,processes)
    for b in bins:
        if b in syst['bins']:
            bin_name = b
        elif b in new_bins_map:
            bin_name = new_bins_map[b]
        else:
            raise Exception("bin not recognized %s"%b)
        for p in processes:
            #print p, b, bin_name, syst['bins'][bin_name], syst
            new_syst[b][p] = syst['bins'][bin_name][p]
    return new_syst 


def assign_syst_to_cfw(cfw, sname, syst, sample_list=[], bin_list=[]):
    stype = syst['type']
    sbins = syst['bins']
    if stype=="gmN":
        sn = syst['n']
        #c.addUncertainty(sname,stype, sn )
        cfw.addUncertainty(sname,stype, sn )
    else:
        cfw.addUncertainty(sname,stype)
    # each systematics contains entries for bins ...
    for b in sbins:
        if bin_list and b not in bin_list:
            continue
        elif not b in cfw.bins:
            continue
        # ... and processes
        othersAdded=False
        for p in sbins[b]:
            #print "~~~~~~~~~~~~~~",sname, p
            #if not p in cfw.processes[cfw.processes.keys()[0]]:
            #    continue
            #print p
            if sample_list and p not in sample_list:
                continue
            if type(sample_list) == dict:
                pname = sample_list[p]
            else: 
                pname = p
            if p in cfw.other_bkgs:     ## combine values for "other" bkg. For this cfw needs to have yieldDict attribute.
                if othersAdded:
                    continue
                else:
                    #print p,pname, b, sname,  [sbins[b][o] for o in cfw.other_bkgs ]           
                    #print [ cfw.yieldDict[o][b] for o in cfw.other_bkgs ]
                    #print 'sum before:',  sum([ cfw.yieldDict[o][b] for o in cfw.other_bkgs ]) 
                    aft = [ (u_float(cfw.yieldDict[o][b].val, (cfw.yieldDict[o][b].val*(abs(1.0-get_float(sbins[b][o]))) ) ))  for o in cfw.other_bkgs ]
                    v = 1 + sum([x.sigma for x in aft]) /  sum([x.val for x in aft])
                    #print v
                    othersAdded = True
            else:
                v = sbins[b][p]
            print ',,,,,', othersAdded, sname, b, p, v, cfw.yieldDict[p][b].val
            #print ',,,,,,,', p,pname
            # extract value and add it, if non-zero
            if v>1.e-6:
                if abs(1-v) < 9.e-5:
                    v=1.0
                cfw.specifyUncertainty(sname,b,pname,v)

def assign_uncert_to_cfw(cfw, sname, stype, sbins, sn = 0.0):
    assert False
    if stype=="gmN":
        cfw.addUncertainty(sname,stype, sn )
    else:
        cfw.addUncertainty(sname,stype)
    # each systematics contains entries for bins ...
    for b in sbins:
        # ... and processes
        for p in sbins[b]:
            # extract value and add it, if non-zero
            v = sbins[b][p]
            if v>1.e-6:
                cfw.specifyUncertainty(sname,b,p,v)






def get_index(string,by):
    sort_indices = [ i1 in string for i1 in by ]
    try: 
        return sort_indices.index(True)
    except ValueError:
        return 0 


def sortBy(l,by_l1,by_l2):
    return sorted(l , key = lambda x: ( get_index(x,by_l1), get_index(x, by_l2))   ) ## ordering first by bin, then by processes 



def try_int(s):
    "Convert to integer if possible."
    try: return int(s)
    except: return s

def natsort_key(s):
    "Used internally to get a tuple by which s is sorted."
    import re
    return map(try_int, re.findall(r'(\d+|\D+)', s))
 

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





import subprocess

#def calcLimitFromCard(card="./cards/T2DegStop_300_270_cards.txt"): 

def calcLimitFromCard(card="./cards/T2DegStop_300_270_cards.txt", name="", mass=""):
    command = ['combine', '--saveWorkspace', '-M', 'Asymptotic'] 
    if name:
        command.extend(["--name", name])
    if mass:
        command.extend(["--mass, mass"])
    command.append(card)
    out = subprocess.Popen(command, stdout = subprocess.PIPE)
    start = False
    end   = False
    limit = {}
    ret = []
    for line in out.stdout.readlines():
        if "-- Asymptotic --" in line:
            start = True
            continue
        if not start:
            continue
        if line == "\n":
            break
        #print line
        for v in [":","%", "\n", "r <"]:
            line = line.replace(v,"")
        ret.append(line)
        limit_sig, limit_val = line.rsplit()[1:]
        if "limit" in limit_sig.lower(): # this should be the observed limit
            limit_sig = "-1"
        else:
            limit_sig = "%0.3f"%(float ( limit_sig ) / 100.)
        
        limit[limit_sig]=limit_val
    return limit

def calcSigFromCard(card="./cards/T2DegStop_300_270_cards.txt", name="", mass=""):
    command = ['combine', '-M', 'ProfileLikelihood', '--uncapped', '1', '--significance', '--rMin', '-5']
    if name:
        command.extend(["--name", name])
    if mass:
        command.extend(["--mass, mass"])
    command.append(card)
    out = subprocess.Popen(command, stdout = subprocess.PIPE)
    start = False
    end   = False
    limit = {}
    ret = []
    for line in out.stdout.readlines():
        if " -- Profile Likelihood --" in line:
            start = True
            continue
        if not start:
            continue
        if line == "\n":
            break
        #print line
        for v in [":","%", "\n", "r <"]:
            line = line.replace(v,"")
        ret.append(line)
        print line
        sp = line.rsplit()

        print sp
        if len(sp)==2:
            limit_sig, limit_val = sp
        elif len(sp) ==3:
            nl = line.replace("(","").replace(")","").replace("=","")
            print nl
            limit_sig, limit_val = nl.rsplit()
        print limit_sig, limit_val
        if "limit" in limit_sig.lower(): # this should be the observed limit
            limit_sig = "-1"
        else:
            limit_sig = "%s"%(limit_sig)
        
        limit[limit_sig]=limit_val
    return limit







#if __name__==False:
if False:

  bkgs=["TTJets", "WJets"]
  sig="T2Deg300_270"
  saveDir     =  "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/dmt_regions/"
  pickleDir   =  "/afs/hephy.at/user/n/nrad/CMSSW/CMSSW_7_4_7/src/Workspace/DegenerateStopAnalysis/plotsNavid/analysis/cutbased/pkl/dmt_regions/r1/"
  pickleFiles = glob.glob(pickleDir+"/*.pkl")

  if len(pickleFiles)==0:
    print "############   WARNING    no pickle files found!  #####"
  else:
    print "############ %s ickle files ound: "%len(pickleFiles),
    print pickleFiles

  limitDict={}
  yields={}

  yieldInstPickleFiles = [x for x in pickleFiles if "YieldInstance" in x]
  for pickleFile in yieldInstPickleFiles:
    filename = splitext(basename(pickleFile))[0].replace("YieldInstance_","")
    print "############ making a limit card for %s"%filename
    yields[filename]=pickle.load(open(pickleFile,"rb") )
    bins = yields[filename].cutLegend[0][1:]
    limitDict[filename] = getLimit(yields[filename])

  import ROOT

  nLimits = len(limitDict)
  limitPlot = ROOT.TH1F("limitPlot","limitPlot",nLimits,0,nLimits)
  for i,fname in enumerate(sorted(limitDict),1):
    limit=limitDict[fname][1]['0.500']
    limitPlot.GetXaxis().SetBinLabel(i,fname)
    limitPlot.SetBinContent(i,limit)

  limitPlot.GetYaxis().SetTitle("r")
  limitPlot.SetTitle("Median Expected Limits")
  limitPlot.Draw()
  #ROOT.c1.SaveAs("/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/dmt_regions/ExpectedLimits.png")
  ROOT.c1.SaveAs(saveDir+"/ExpectedLimits.png")
    




















################


def getValueFromDict(x, val="0.500", default=999):
    try:
        ret = x[val]
    except KeyError:
        ret = default
    #else:
    #    raise Exception("cannot find value %s in  %s"%(val, x))
    return float(ret)

def getValueFromDictFunc(val="0.500"):
    def func(x, val=val, default=999):
        try:
            ret = x[val]
        except KeyError:
            ret = default
        #else:
        #    raise Exception("cannot find value %s in  %s"%(val, x))
        return float(ret)
    return func




def drawExpectedLimit( limitDict, plotDir, bins=[23, 237.5, 812.5, 125, 167.5, 792.5], key=None , title="", csize=(1500,1026) ):
    saveDir = plotDir
    
    if type(limitDict)==type({}):
        limits = limitDict
    elif type(limitDict)==type("") and limitDict.endswith(".pkl"):
        limits = pickle.load(open(limitDict, "r"))
    else:
        raise Exception("limitDict should either be a dictionary or path to a picke file")

    if not bins:
        if 500 in limits.keys() or "500" in limits.keys():
            bins = [23,87.5,662.5, 127 , 17.5, 642.5]
        else:
            bins = [13,87.5,412.5, 75, 17.5, 392.5 ]
    
    if not key:
        key = getValueFromDict
    if type(key)==type(""):
        key = getValueFromDictFunc(key)
    else:               ### then key should be a function
        pass
    
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
    c1 = ROOT.TCanvas("c1","c1",*csize)
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
    #    return c1,plot
    #else:
    return c1,plot


limit_keys = {
               "up1":"0.160"         ,
               "up2":"0.025"         ,
               "exp":"0.500"         ,
               "obs":"-1.000"         ,
               "down1":"0.840"       ,
               "down2":"0.975"       ,
            }


#def drawExclusionLimit( limitDict, plotDir, bins=[23, 237.5, 812.5, 125, 167.5, 792.5], csize=(1500,950)  , text = None):
def drawExclusionLimit( limitDict, plotDir, bins=[23, 237.5, 812.5, 63, 165.0, 795.0], csize=(1500,950)  , text = None):
    filename = os.path.basename(plotDir)
    basename, ext = os.path.splitext(filename)
    saveDir    =  plotDir.replace(filename,"")

    #setup_style()
    
    #print filename
    #print basename, ext
    #print saveDir   
 
    if type(limitDict)==type({}):
        limits = limitDict
    elif type(limitDict)==type("") and limitDict.endswith(".pkl"):
        limits = pickle.load(open(limitDict, "r"))
    else:
        raise Exception("limitDict should either be a dictionary or path to a picke file")

    if not bins:
        if 500 in limits.keys() or "500" in limits.keys():
            bins = [23,87.5,662.5, 127 , 17.5, 642.5]
        else:
            bins = [13,87.5,412.5, 75, 17.5, 392.5 ]

    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPaintTextFormat("0.2f")
    plots = {}
    canvs = {}
    makeDir(saveDir)
    rootfile = saveDir + basename +".root"
    tfile = ROOT.TFile( rootfile, "RECREATE" )
    for limit_var, k in limit_keys.iteritems():

        plots[limit_var] = makeStopLSPPlot(limit_var, limits, bins=bins, key= getValueFromDictFunc(k)  )

        plots[limit_var].SetContour(2 )
        plots[limit_var].SetContourLevel(0,0 )
        plots[limit_var].SetContourLevel(1,1 )
        plots[limit_var].SetContourLevel(2,10 )

        canvs[limit_var] = ROOT.TCanvas("c_%s"%limit_var,"c_%s"%limit_var,*csize)    
        plots[limit_var].Draw("COL TEXT")    

        ltitle = ROOT.TLatex()
        ltitle.SetNDC()
        ltitle.SetTextAlign(12)   
        #ytop = 1.05- canv.GetTopMargin()
        #ltitle_info = [0.1, ytop]
        ltitle.DrawLatex(0.2, 0.8, limit_var  )

        if text:
            ltitle.DrawLatex(0.2,0.9, text)

        canvs[limit_var].Update()
        canvs[limit_var].Modify()


        plots[limit_var].Write()
        canvs[limit_var].Write()        

        savePlotDir= saveDir + basename + "_" + limit_var
        saveCanvas( canvs[limit_var], saveDir, basename + "_" + limit_var ) 

        #if plotDir:
        #    canvs[limit_var].SaveAs(plotDir.replace(ext,"_"+limit_var + ext))
    #    return c1,plot
    #else:
    
    tfile.Close()

    return plots, canvs , tfile




##### From CardFileWriter



def readResFile(fname):
    f = ROOT.TFile.Open(fname)
    t = f.Get("limit")
    l = t.GetLeaf("limit")
    qE = t.GetLeaf("quantileExpected")
    limit = {}
    preFac = 1.
    for i in range(t.GetEntries()):
            t.GetEntry(i)
            limit["{0:.3f}".format(round(qE.GetValue(),3))] = preFac*l.GetValue()
            limit["{0:.3f}".format(round(qE.GetValue(),3))] = preFac*l.GetValue()
    f.Close()
    return limit

    #os.system("pushd "+self.releaseLocation+";eval `scramv1 runtime -sh`;popd;cd "+uniqueDirname+";"+self.combineStr+" --saveWorkspace  -M ProfileLikelihood --significance "+fname+" -t -1 --expectSignal=1 ")

def calcLimit(card, options="", combineLocation="./", signif=False):
    import uuid, os 
    card = os.path.abspath(card)
    uniqueDirname="."
    uniqueDirname = "tmp_"+str(uuid.uuid4())
    os.system('mkdir '+uniqueDirname)
    #os.system("cd "+uniqueDirname+";combine --saveWorkspace -M Asymptotic "+card)
    #combine_command = "cd "+uniqueDirname+";eval `scramv1 runtime -sh`;combine --saveWorkspace -M Asymptotic "+filename
    if signif:
        combine_method = " -M ProfileLikelihood  --uncapped 1 --significance --rMin -5  "
        resfilename    = "higgsCombineTest.ProfileLikelihood.mH120.root" 
    else:
        combine_method = "--saveWorkspace -M Asymptotic "
        resfilename    = "higgsCombineTest.Asymptotic.mH120.root"

                       #combine --saveWorkspace -M Asymptotic {card}

    combine_command = """
                       pushd {combineLocation}; 
                       eval `scramv1 runtime -sh` ; 
                       popd; 
                       cd {uniqueDirname};
                       combine {method}  {card}
                       """\
                       .format( 
                                combineLocation = combineLocation , 
                                method          = combine_method  ,
                                uniqueDirname   = uniqueDirname   ,  
                                card            = card 
                              )
    print combine_command
    os.system( combine_command )
    try:
        res= readResFile(uniqueDirname + "/" + resfilename ) #higgsCombineTest.Asymptotic.mH120.root")
    except:
        res=None
        print "Did not succeed."
    os.system("rm -rf roostats-*")
    os.system("rm -rf "+uniqueDirname)
    return res


def maxLikelihoodFit(shapecard, output_name = None , combineLocation=combineLocation, bins_to_mask= None, nToys=2000):
    import uuid, os 
    card = os.path.abspath(shapecard)
    uniqueDirname="."
    uniqueTag = str(uuid.uuid4())
    uniqueDirname = "tmp_mlf_"+uniqueTag
    os.system('mkdir '+uniqueDirname)

    #combine ${prefix}_fakeshapecard_chmask.root -M MaxLikelihoodFit  --numToysForShape 2000  --saveShapes  --saveNormalizations  --saveWithUncertainties --setPhysicsModelParameters mask_ch1_sr1vla=1,mask_ch1_sr1la=1,mask_ch1_sr1ma=1,mask_ch1_sr1ha=1,mask_ch1_sr1vlb=1,mask_ch1_sr1lb=1,mask_ch1_sr1mb=1,mask_ch1_sr1hb=1,mask_ch1_sr1vlc=1,mask_ch1_sr1lc=1,mask_ch1_sr1mc=1,mask_ch1_sr1hc=1,mask_ch1_sr2vl=1,mask_ch1_sr2l=1,mask_ch1_sr2m=1,mask_ch1_sr2h=1
    if bins_to_mask:
        mask_opt = '--setPhysicsModelParameters  '
        mask_opt += ','.join(['mask_ch1_%s=1'%b for b in bins_to_mask])
    else:   
        mask_opt = ''

    combine_command = """
                       pushd {combineLocation}; 
                       eval `scramv1 runtime -sh` ; 
                       popd; 
                       cd {uniqueDirname};
                       combine {card} -M MaxLikelihoodFit --numToysForShape {nToys} --saveShapes --saveNormalizations --saveOverall --saveWithUncertainties {mask_opt}"""\
                       .format( 
                                combineLocation = combineLocation, 
                                uniqueDirname   = uniqueDirname  , 
                                card            = card          ,
                                mask_opt        = mask_opt      ,
                                nToys           = nToys         ,
                              )
    print combine_command
    os.system( combine_command )
    #output_name = output_name if output_name else "mlfit_%s.root"%uniqueTag
    if not output_name: output_name = shapecard.replace(".txt", "_mlfit.root") 
    def_output = "%s/mlfit.root"%uniqueDirname
    
    if os.path.isfile(def_output):
        os.system( 'mv %s %s'%(def_output, output_name) )
        print "mlf output: " , output_name
        ret = True
    else:
        print "ERROR:  !!!!!!!!!!!!!  MLF FAILED  !!!!!!!!!!!!"
        ret = False
    os.system("rm -rf "+uniqueDirname)
    return ret



def GoodnessOfFit( card, algo='saturated' , nToys = 500, seed = None, output_dir="./" , only_plot = False):

    output_dir +"/%s"%algo
    makeDir( output_dir ) 
    
    dataOptions = "-M GoodnessOfFit --algo={algo}".format(algo=algo) 
    toyOptions  = "-M GoodnessOfFit --algo={algo} -t {nToys} {seedOpt}".format(algo=algo, nToys = nToys, seedOpt = '-s %s'%seed if seed else '')

    dataFile  = output_dir + "/higgsCombineTest.GoodnessOfFit.mH120.root"
    toysFile  = output_dir + "/higgsCombineTest.GoodnessOfFit.mH120.%s.root"%(seed if seed else 123456)

    print "combine %s"%dataOptions
    if not only_plot:
        runCombineCommand( card, dataOptions , output_dir = output_dir ) 
        runCombineCommand( card, toyOptions  , output_dir = output_dir ) 


    dataGoF = readResFile(dataFile).get("-1.000")

    
    toyHist = ROOT.TH1F("toyHist","expected (toys)", 100,int(1.1*dataGoF),int(0.9*dataGoF))
    dataHist = ROOT.TH1F("dataHist","observed", 100,int(1.1*dataGoF),int(0.9*dataGoF))
    dataHist.Fill(dataGoF, 0.001)


    toysTF = ROOT.TFile( toysFile ) 
    toyTree = toysTF.limit

    
    for i in range(toyTree.GetEntries()):
        toyTree.GetEntry(i)
        toyHist.Fill(toyTree.limit)
    toyHist.SetBinContent(100,toyHist.GetBinContent(100)+toyHist.GetBinContent(101))
    toyHist.Scale(1/toyHist.Integral()) 
   

    toyHist.GetXaxis().SetTitle("q_{GoF}")
    toyHist.SetTitle(algo.title())
    toyHist.GetYaxis().SetTitle("a.u.")
    toyHist.Draw("hist")
    toyHist.SetLineWidth(2)
    toyHist.SetMarkerSize(0)
    dataHist.SetMarkerStyle(23)
    dataHist.SetMarkerSize(2)
    dataHist.SetLineWidth(0)
    dataHist.SetMarkerColor(ROOT.kBlue)
    dataHist.Draw("same")
   
    print toyHist.Integral()
    pvalue = toyHist.Integral(dataHist.GetXaxis().FindBin(dataHist.GetMean()),100)

    ltitle = ROOT.TLatex()
    ltitle.SetNDC()
    ltitle.SetTextAlign(12)
    ltitle.DrawLatex(0.1, 0.8, "p_value = %s"%(round(pvalue, 4))  )


 
    ROOT.gPad.SaveAs(output_dir+"/GOF_%s.png"%algo) 

    print toyHist, dataHist 
    return toyHist, dataHist 





def runCombineCommand(card, combine_option = "-M Asymptotic", output_dir = "./",  combineLocation=combineLocation, verbose = True):
    """
        Simple function to run to get HiggsCombine Env. and then run the given combine command.
        The output must be handeled externally.
    """
    combine_command = """
                       pushd {combineLocation}; 
                       eval `scramv1 runtime -sh` ; 
                       popd; 
                       pushd {output_dir};
                       combine {card} {combine_option} ; 
                       popd; 
                       """\
                       .format( 
                                combineLocation = combineLocation, 
                                output_dir      = output_dir, 
                                combine_option  = combine_option,
                                card            = card          ,
                              )
    if verbose:
        print combine_command
    os.system( combine_command )
    return 


def makeFakeShapeCard(card, output_card  , combineLocation=combineLocation):
    card = os.path.abspath(card)
    combine_command = """
                       pushd {combineLocation}; 
                       eval `scramv1 runtime -sh` ; 
                       popd; 
                       combineCards.py {card} -S > {output_card} """\
                       .format( 
                                combineLocation = combineLocation, 
                                card            = card          ,
                               output_card      = output_card
                              )
    print combine_command
    os.system( combine_command )
    return 


def makeWorkspace( card, output_file = None , combineLocation=combineLocation , opts = '--channel-masks'):
    card = os.path.abspath(card)
    if not output_file:
        output_file = card.replace(".txt",".root")
    combine_command = """
                       pushd {combineLocation}; 
                       eval `scramv1 runtime -sh` ; 
                       popd; 
                       text2workspace.py {card}   {opts}  ; 
                       mv {def_output}   {output_file}  
                       """\
                       .format( 
                                combineLocation = combineLocation, 
                                card            = card          ,
                                def_output      = card.replace(".txt", ".root"),
                                output_file      = output_file,
                                opts             = opts 
                              )
    print combine_command
    os.system( combine_command )
    return 



def runMLF(card, output, bins = None,  combineLocation=combineLocation , nToys = 2000) :
    shapecard = card.replace(".txt","_fakeshape.txt")
    if not os.path.isfile(card):
        raise Exception("Card Not Found!! %s"%card)
    print '\n --- Creating a fake shape card: %s'%shapecard
    makeFakeShapeCard( card, shapecard , combineLocation)
    workspace_file = shapecard.replace('_fakeshape.txt','_fakeshape_chmask.root')
    print '\n --- Creating RooWorkspace: %s'%workspace_file
    makeWorkspace( shapecard , output_file = workspace_file, combineLocation = combineLocation , opts = '--channel-masks' )
    if not output.endswith('.root'): output +='.root'

    rets = {}
    if False:
        output_nosrmask = output.replace('.root', '_NoSRMasked.root' )
        maxLikelihoodFit( workspace_file, output_name = output_nosrmask , combineLocation=combineLocation , bins_to_mask = None, nToys = nToys)
        rets['nosrmask']=output_nosrmask 
    if bins:
        output_srmask = output.replace('.root', '_SRMasked.root' )
        
        rets['srmask']= output_srmask
        maxLikelihoodFit( workspace_file, output_name = output_srmask , combineLocation=combineLocation, bins_to_mask= bins, nToys = nToys)
    return rets




def calcSignif(card, options=""):
    import uuid, os 
    uniqueDirname=""
    unique=False
    fname = card
    uniqueDirname = "tmp_"+str(uuid.uuid4())
    unique=True
    os.system('mkdir '+uniqueDirname)
    if fname=="":
        fname = str(uuid.uuid4())+".txt"
        #self.writeToFile(uniqueDirname+"/"+fname)
    else:
        pass
        #self.writeToFile(fname)
    #os.system("cd "+uniqueDirname+";combine --saveWorkspace    -M ProfileLikelihood --significance "+fname+" -t -1 --expectSignal=1 ")
    print "combine  -M ProfileLikelihood  --uncapped 1 --significance --rMin -5  " +fname
    os.system("cd "+uniqueDirname+";combine  -M ProfileLikelihood  --uncapped 1 --significance --rMin -5  " +fname)
    #os.system("cd "+uniqueDirname+";combine  -M ProfileLikelihood  --uncapped 1 " +fname)
    try:
        res= readResFile(uniqueDirname+"/higgsCombineTest.ProfileLikelihood.mH120.root")
    except:
        res=None
        print "Did not succeed."
    os.system("rm -rf roostats-*")
    if unique:
         os.system("rm -rf "+uniqueDirname)
    else:
        if res:
            print res
            os.system("cp higgsCombineTest.ProfileLikelihood.mH120.root "+fname.replace('.txt','')+'.root')

    return res



########################





def SetupColors():
    num = 5
    bands = 255
    colors = [ ]
    #stops = [0.00, 0.34, 0.61, 0.84, 1.00]
    #red = [0.50, 0.50, 1.00, 1.00, 1.00]
    #green = [0.50, 1.00, 1.00, 0.60, 0.50]
    #blue = [1.00, 1.00, 0.50, 0.40, 0.50]
    red        = [1.,0.,0.,0.,1.,1.]
    green      = [0.,0.,1.,1.,1.,0.]
    blue       = [1.,1.,1.,0.,0.,0.]
    stops      = [0.,0.2,0.4,0.6,0.8,1.]
    arr_stops = array('d', stops)
    arr_red = array('d', red)
    arr_green = array('d', green)
    arr_blue = array('d', blue)
    # num = 6
    # red[num] =   {1.,0.,0.,0.,1.,1.}
    # green[num] = {0.,0.,1.,1.,1.,0.}
    # blue[num] =  {1.,1.,1.,0.,0.,0.}
    # stops[num] = {0.,0.2,0.4,0.6,0.8,1.}*/
    fi = ROOT.TColor.CreateGradientColorTable(num,arr_stops,arr_red,arr_green,arr_blue,bands)
    for i in range(bands):
        colors.append(fi+i)
    arr_colors = array('i', colors)
    ROOT.gStyle.SetNumberContours(bands)
    ROOT.gStyle.SetPalette(bands, arr_colors)


def SetupColorsForExpectedLimit():
    """
    Stolen and Pythonized from: aaduszki; https://root.cern.ch/phpBB3/viewtopic.php?t=14597
    """
    # palette settings - completely independent
    #NRGBs = 6;
    #NCont = 999;
    #stops = array( 'd', [ 0.00, 0.1, 0.34, 0.61, 0.84, 1.00 ])
    #red   = array( 'd', [ 0.99, 0.0, 0.00, 0.87, 1.00, 0.51 ])
    #green = array( 'd', [ 0.00, 0.0, 0.81, 1.00, 0.20, 0.00 ])
    #blue  = array( 'd', [ 0.99, 0.0, 1.00, 0.12, 0.00, 0.00 ])
    #ROOT.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
    #ROOT.gStyle.SetNumberContours(NCont);
    ##here the actually interesting code starts
    min = 0.9;
    max = 1.1;
    nLevels = 999;
    levels=[];
    for i in range(1,nLevels):
      levels.append( min + (max - min) / (nLevels - 1) * (i))
    levels=array("d",levels)
    levels[0] = 0.01;
    #levels[0] = -1; //Interesting, but this also works as I want!
    c=ROOT.TCanvas();
    h  = ROOT.TH2D("h", "", 10, 0, 10, 10, 0, 10);
    h.SetContour((len(levels)/8), levels);
    h.SetBinContent(5, 7, 1.20);
    h.SetBinContent(5, 6, 1.05);
    h.SetBinContent(5, 5, 1.00);
    h.SetBinContent(5, 4, 0.95);
    h.SetBinContent(5, 3, 0.80);
    h.DrawClone("colz text")#;// draw "axes", "contents", "statistics box"
    h.GetZaxis().SetRangeUser(min, max); #// ... set the range ...
    h.Draw("z same")#; // draw the "color palette"
    c.SaveAs("c.png")#;

def makeOfficialLimitPlot( input_pkl , tag = "XYZ", savePlotDir = None, model="T2DegStop", dmplot=False, signif=False):
    from Workspace.DegenerateStopAnalysis.limits.MonoJetAnalysis.limits.pklToHistos import pklToHistos


    baseLimitScriptsDir   = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/python/limits/"
    baseLimitScriptsDir   = os.path.expandvars(baseLimitScriptsDir)

    limitScriptsDir       = baseLimitScriptsDir + "MonoJetAnalysis/limits/"
    smsPlotDir            = baseLimitScriptsDir + "PlotsSMS-master/python/"

    if signif:
        model += "_signif"
    elif dmplot:
         model += "_dm"
    tag+="_"+model

    presmooth_file ="%s_presmooth_file.root"%tag

    print tag
    print presmooth_file
    
    pklToHistos( input_pkl, limitScriptsDir +"/"+ presmooth_file )
    smooth_file ="%s_smooth_file.root"%tag

    dmopt = "--dmplot" if dmplot else ""

    if not signif:
        smoothLimitScript = "smoothLimits-v5.py"
    else:
        smoothLimitScript = "smoothSignifs-v5.py"
    script1 = "cd {dir} ; python {script} --input={inputfile} --output={outputfile} {dmopt}"\
                .format( dir = limitScriptsDir , script = smoothLimitScript , inputfile = presmooth_file , outputfile = smooth_file , dmopt = dmopt) 

    print "running: \n ", script1
    os.system(script1)

    smooth_histo_path = limitScriptsDir + "/"+ smooth_file
    cfg_info = {
                'histo'      : smooth_histo_path ,
                'histo_exp'  : smooth_histo_path ,
                'histo_obs'  : smooth_histo_path ,
                'preliminary':'Preliminary',
                'lumi'       : 35.9        ,
                'energy'     : 13          ,
               }
    cfg = makeSMScfg( ** cfg_info )
    cfg_file = limitScriptsDir + "DegStop2016_singleLepton_%s.cfg"%(tag)
    with open(cfg_file , 'w' ) as f:
        f.write(cfg)
    
    if savePlotDir:
        makeDir(savePlotDir)
    else:
        savePlotDir = smsPlotDir+"../"
    smsPlotScript = "cd {savePlotDir} ; python {smsPlotDir}makeSMSplots.py {cfg_file} {tag} {model}".format(savePlotDir = savePlotDir , smsPlotDir = smsPlotDir, cfg_file = cfg_file, tag = tag, model = model)
    print smsPlotScript
    os.system( smsPlotScript ) 

    #"python python/makeSMSplots.py ../MonoJetAnalysis/limits/DegStop2016_singleLepton.cfg XYZ"
   


def makeSMScfg(histo , histo_exp, histo_obs, preliminary, lumi, energy):
    temp=\
"""
# AVAILABLE COLORS:
# kMagenta
# kBlue
# kOrange
# kRed
#####################################################
#FORMAT: input root histo-name line-color area-color  
#####################################################
HISTOGRAM {histo} OBSOut
EXPECTED {histo_exp} gEXPOut0 gP1SOut0 gM1SOut0 kRed kOrange
OBSERVED {histo_obs} gOBSOut0 gOBSUpOut0 gOBSDownOut0 kBlack kGray
# Preliminary Simulation or leave empty
#PRELIMINARY Preliminary
PRELIMINARY {preliminary}
# Lumi in fb 
LUMI {lumi}
# Beam energy in TeV
ENERGY {energy}
# Analysis name
#ANALYSIS Single-muon analysis
""".format( 
            histo     = histo         ,
            histo_exp = histo_exp  ,
            histo_obs = histo_obs ,
        preliminary   = preliminary,
            lumi      = lumi      ,
            energy    = energy    , 
          )
    return temp
