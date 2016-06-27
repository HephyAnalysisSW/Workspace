import os
from array import array
import ROOT
import pickle
from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import *

#def get_basename (f):
#    return os.path.basename(f)
#def get_filename (f):
#    return os.path.splitext(os.path.basename(f))[0]
#def get_ext (f):
#    return os.path.splitext(os.path.basename(f))[1]
#
#def getMasses(string):
#    import re
#    masses = []    
#    string = get_filename(string)
#    splitted = re.split("_|-", string)
#    #splitted = string.rsplit("_"):
#    for s in splitted: 
#        if s.startswith("s8tev"):
#            s = s[5:]
#        if s.startswith("s"):
#            s = s[1:]
#        if not s.isdigit(): 
#            continue
#        masses.append(s)
#    if len(masses)!=2 or int(masses[0]) < int(masses[1]):
#        raise Exception("Failed to Extract masses from string: %s , only got %s "%(string, masses))        
#    return [int(m) for m in masses]





def getValueFromDict(x, val="0.500", default=999):
    try:
        ret = x[val]
    except KeyError:
        ret = default
    #else:
    #    raise Exception("cannot find value %s in  %s"%(val, x))
    return float(ret)

def drawExpectedLimit( limitDict, plotDir, bins=None, key=None , title="", csize=(1500,1026) ):
    saveDir = plotDir
    
    if type(limitDict)==type({}):
        limits = limitDict
    elif type(limitDict)==type("") and limitDict.endswith(".pkl"):
        limits = pickle.load(open(limitDict, "r"))
    else:
        raise Exception("limitDict should either be a dictionary or path to a picke file")

    if not bins:
        bins = [13,87.5,412.5, 75, 17.5, 392.5 ]
        #bins = [23,87.5,662.5, 127 , 17.5, 642.5]
    
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

def calcLimit(card, options=""):
    import uuid, os 
    card = os.path.abspath(card)

    uniqueDirname="."
    uniqueDirname = "tmp_"+str(uuid.uuid4())
    os.system('mkdir '+uniqueDirname)
    os.system("cd "+uniqueDirname+";combine --saveWorkspace -M Asymptotic "+card)
    try:
        res= readResFile(uniqueDirname+"/higgsCombineTest.Asymptotic.mH120.root")
    except:
        res=None
        print "Did not succeed."
    os.system("rm -rf roostats-*")
    os.system("rm -rf "+uniqueDirname)
    return res


def calcSignif(card, options=""):
    import uuid, os 
    uniqueDirname=""
    unique=False
    fname = card
    if fname=="":
        uniqueDirname = str(uuid.uuid4())
        unique=True
        os.system('mkdir '+uniqueDirname)
        fname = str(uuid.uuid4())+".txt"
        #self.writeToFile(uniqueDirname+"/"+fname)
    else:
        pass
        #self.writeToFile(fname)
    os.system("cd "+uniqueDirname+";combine --saveWorkspace    -M ProfileLikelihood --significance "+fname+" -t -1 --expectSignal=1 ")
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


