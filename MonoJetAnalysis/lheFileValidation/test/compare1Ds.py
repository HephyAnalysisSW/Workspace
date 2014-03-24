#
# compare 1D LHE validation histograms for several mass combinations
#
import ROOT
import os,sys
from fnmatch import fnmatch
from operator import itemgetter
from optparse import OptionParser
#
# color / linestyle from index
#
def applyStyle(index,object):
    colors = [ 1, 2, 4, 3, 5 ]
    styles = [ 1, 2, 3 ]
    istyle = (index/len(colors))%len(styles)
    icolor = index%len(colors)
    object.SetLineStyle(styles[istyle])
    object.SetLineColor(colors[icolor])
    return
#
# extract stop and LSP masses from filename
#
def decodeFileName(fname):
    result = ( None, None )
    if not fnmatch(fname,'T2tt*.*.root'):
        return result
    fields = file.split(".")
    if len(fields)!=3:
        return result
    fields = fields[1].split("_")
    if len(fields)!=9:
        return result
    return ( int(fields[3]), int(fields[8]) )
#
parser = OptionParser()
parser.add_option("--dir", dest="dir",  help="input directory", action="store", \
                  default="/data/adamwo/DegenerateLightStop/LheProduction/T2tt/stop_stop/validationGridFilesModifiedHeaders/")
parser.add_option("--masses", "-m",  dest="masses",  help="mass pair (mstop,dm)", action="append", \
                  default=None)
parser.add_option("--label", dest="label",  help="axis label", action="store", \
                  default=None)
parser.add_option("--unique", "-u",  dest="unique",  help="select only one file per mass point", action="store_true", default=False)
parser.add_option("-b",  dest="batch",  help="batch mode", action="store_true", default=False)
(options, args) = parser.parse_args()
assert len(args)==1
histograms = { }
for n in args[0].split(","):
    histograms[n] = [ ]
masses = [ ]
for s in options.masses:
    mpair = s.split(",")
    assert len(mpair)==2 and mpair[0].isdigit() and mpair[1].isdigit()
    masses.append( ( int(mpair[0]), int(mpair[1]) ) )
assert len(masses)>0
#
# ROOT options
#
ROOT.gStyle.SetOptStat(0)
#ROOT.gStyle.SetPadRightMargin(0.15)
#
# create list of files according to required mass combinations
#   and define binning
#
filteredFiles = [ ]
filteredMasses = [ ]
for file in os.listdir(options.dir):
    mstop,dm = decodeFileName(file)
    if mstop==None or dm==None:
        continue
    if (mstop,dm) in masses:
        if not options.unique or not (mstop,dm) in filteredMasses:
            filteredFiles.append( ( file, mstop, dm ) )
            filteredMasses.append( ( mstop, dm ) )
filteredFiles.sort(key=itemgetter(1,2))
print filteredFiles
#
# loop over accepted files
#
for file,mstop,dm in filteredFiles:
    #
    # open ROOT file and get all 1D histograms
    #
    tfile = ROOT.TFile(options.dir+"/"+file)
    ROOT.gROOT.cd()
    for n in histograms:
        h = tfile.Get(n)
        if h and h.InheritsFrom(ROOT.TH1.Class()) and not h.InheritsFrom(ROOT.TH2.Class()):
            histograms[n].append(h.Clone())
        else:
            histograms[n].append(None)
    tfile.Close()

canvases = [ ]
legends = [ ]
for i,n in enumerate(histograms):
    hmax = 0
    for j,h in enumerate(histograms[n]):
        if h:
            applyStyle(j,h)
            h.SetLineWidth(2)
            v = h.GetMaximum()
            if v>hmax:
                hmax = v
    hmax /= 0.85
    cnv = ROOT.TCanvas("c_"+n,"c_"+n)
    leg = ROOT.TLegend(0.65,0.7,0.9,0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetHeader("m(stop) / #delta m(stop-LSP)")
    opt = "hist"
    for j,h in enumerate(histograms[n]):
        if h:
            h.SetMaximum(hmax)
            h.Draw(opt)
            leg.AddEntry(h,str(filteredFiles[j][1])+" GeV / "+str(filteredFiles[j][2])+" GeV","l")
            opt = "hist same"
    leg.Draw()
    cnv.SaveAs(n+".png")
    canvases.append(cnv)
    legends.append(leg)

if not options.batch:
    raw_input("Press enter")
