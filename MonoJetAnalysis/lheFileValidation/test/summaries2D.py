#
# create 2D (deltaM vs. Mstop) summaries of LHE validation histograms
#
import ROOT
import os,sys
import fnmatch
#
# extract stop and LSP masses from filename
#
def decodeFileName(fname):
    result = ( None, None )
    if not fnmatch.fnmatch(fname,'T2tt*.*.root'):
        return result
    fields = file.split(".")
    if len(fields)!=3:
        return result
    fields = fields[1].split("_")
    if len(fields)!=9:
        return result
    return ( int(fields[3]), int(fields[8]) )
#
# find (nbins,xmin,xmax) from list of values
#   (assumes regularily-spaced values - missing values
#    are accepted if at least one pair with the minimum
#    distance exists)
def findBinning(values):
    vmin = None
    vmax = None
    dmin = None
    vlast = None
    # find minimum, maximum and minimum distance
    for v in sorted(values):
        if vmin==None or v<vmin:
            vmin = v
        if vmax==None or v>vmax:
            vmax = v
        if vlast!=None and v!=vlast:
            d = v - vlast
            if dmin==None or d<dmin:
                dmin = d
        vlast = v
    # check
    vlast = None
    for v in sorted(values):
        if vlast!=None and v!=vlast:
            d = v - vlast
            assert (d%dmin)==0
        vlast = v
    nb = (vmax-vmin)/dmin + 1
    return (nb,vmin-dmin/2.,vmax+dmin/2.)
#
# ROOT options
#
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadRightMargin(0.15)
ROOT.gROOT.ProcessLine(".L ../../../HEPHYCommonTools/scripts/root/useNiceColorPalette.C")
ROOT.useNiceColorPalette()
#
summaryHistograms = { }
mstopBins = None
dmBins = None
#
# create a histogram with standard mstop and dm binning
#
def createHistogram(name):
    h = ROOT.TH2F(name,name,
                  mstopBins[0],mstopBins[1],mstopBins[2],
                  dmBins[0],dmBins[1],dmBins[2])
    h.GetXaxis().SetTitle("m(stop) [GeV]")
    h.GetYaxis().SetTitle("#deltam(stop-lsp) [GeV]")
    h.SetDirectory(ROOT.gROOT)
    return h
#
# create histograms for mean and RMS
#
def createHistograms(name):
    hMean = createHistogram(name+"_mean")
    hRms = createHistogram(name+"_rms")
    return (hMean,hRms)
#
# create histograms for polarization parameters
#
def createPolHistograms(name):
    hPlus = createHistogram(name+"_fplus")
    hMinus = createHistogram(name+"_fminus")
    h0 = createHistogram(name+"_f0")
    return (hPlus,hMinus,h0)
#
# get list of 1D histograms from file
#
def getHistograms(tfile):
    result = [ ]
    for key in tfile.GetListOfKeys():
        obj = key.ReadObj()
        if obj.InheritsFrom(ROOT.TH1.Class()) and \
           not obj.InheritsFrom(ROOT.TH2.Class()):
            result.append(obj)
    return result
#
# input directory
#
dir = "/data/adamwo/DegenerateLightStop/LheProduction/T2tt/stop_stop/validationGridFilesModifiedHeaders/"
#
# create list of files and masses
#   and define binning
#
filteredFiles = [ ]
mstops = set()
dms = set()
for file in os.listdir(dir):
    mstop,dm = decodeFileName(file)
    if mstop==None or dm==None:
        continue
    mstops.add(mstop)
    dms.add(dm)
    filteredFiles.append( ( file,mstop,dm ) )
mstopBins = findBinning(mstops)
dmBins = findBinning(dms)
#
# loop over accepted files
#
for file,mstop,dm in filteredFiles:
    #
    # open ROOT file and get all 1D histograms
    #
    tfile = ROOT.TFile(dir+"/"+file)
    inhistos = getHistograms(tfile)
    #
    # loop over histograms
    #
    for h in inhistos:
        n = h.GetName()
        #
        # create summary histograms, if not yet done
        #
        if not n in summaryHistograms:
            # special case "polarization" histograms: one histogram / parameter
            if n.endswith("costh"):
                summaryHistograms[n] = createPolHistograms(n)
            # all others: one histogram each for mean and RMS
            else:
                summaryHistograms[n] = createHistograms(n)
        # get histograms
        shs = summaryHistograms[n]
        if shs[0]==None or shs[1]==None:
            print n in summaryHistograms
            print file,n,shs
        # fill polarization parameters (after normalization)
        if n.endswith("costh"):
            fp = h.GetListOfFunctions()[0].GetParameter(0)
            fm = h.GetListOfFunctions()[0].GetParameter(1)
            f0 = h.GetListOfFunctions()[0].GetParameter(2)
            sumf = fp+fm+f0
            shs[0].Fill(mstop,dm,fp/sumf)
            shs[1].Fill(mstop,dm,fm/sumf)
            shs[2].Fill(mstop,dm,f0/sumf)
        # fill mean and RMS
        else:
            shs[0].Fill(mstop,dm,h.GetMean())
            shs[1].Fill(mstop,dm,h.GetRMS())
    tfile.Close()
#
# create output histograms (root file and individual canvases)
#
tf = ROOT.TFile("summary.root","recreate")
for n,hs in summaryHistograms.iteritems():
    for h in hs:
        h.SetDirectory(tf)
        h.Write()
        h.Draw("zcol")
        ROOT.gPad.SaveAs(h.GetName()+"_summary.png")
tf.Close()
