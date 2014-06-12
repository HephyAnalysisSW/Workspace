import ROOT
import os,sys,string
from fnmatch import fnmatch
from Sample import *
#from drawWithFOM import *
#from drawSoB import *
from optparse import OptionParser
from SampleFilters import *

parser = OptionParser()
parser.add_option("--preselection", "-p", dest="preselection",  help="preselection", default=None)
parser.add_option("--draw", "-d", dest="drawClass",  help="draw class", default="DrawWithFOM.py")
parser.add_option("--elist", "-e", dest="elist",  help="event list mode", choices=[ "w", "r", "a" ], default=None )
parser.add_option("--fom", dest="fom",  help="fom to be used", choices=[ "sob", "sosqrtb", "dataovermc", "None" ], default="sosqrtb" )
parser.add_option("--elistBase", dest="elistBase",  help="base directory for event lists", default="./elists")
parser.add_option("-s", dest="save",  help="directory for saved plots", default=None)
parser.add_option("-b", dest="batch",  help="batch mode", action="store_true", default=False)
parser.add_option("--fomByBin", dest="fomByBin",  help="calculate fom by bin", action="store_true", default=False)
parser.add_option("--rebin", dest="rebin",  help="rebin factor", type=int, default=1)
parser.add_option("--dset", dest="dset", help="dataset", choices=[ "met", "singleMu", "diMu" ], default="met" )
parser.add_option("--data", dest="data", help="show data", action="store_true", default=False)
parser.add_option("--canvasNames",dest="canvasNames",help="(comma-separated list) of canvases to show",default=None)
(options, args) = parser.parse_args()
assert len(args)>0
if options.fom=="None":
    options.fom = None
assert options.rebin>0
selectedCanvasNames = [ ]
if options.canvasNames!=None:
    for cnvname in  options.canvasNames.split(","):
        selectedCanvasNames.append(cnvname)
    print selectedCanvasNames

plotGlobals = {}
execfile(args[0],plotGlobals)
plotClassName = os.path.splitext(os.path.basename(args[0]))[0]
plotClass = plotGlobals[plotClassName]

drawGlobals = {}
execfile(options.drawClass,drawGlobals)
drawClassName = os.path.splitext(os.path.basename(options.drawClass))[0]
drawClass = drawGlobals[drawClassName](options)

presel = None
if options.preselection!=None:
    preselGlobals = {}
    execfile(options.preselection,preselGlobals)
    preselClassName = os.path.splitext(os.path.basename(options.preselection))[0]
    preselClass = preselGlobals[preselClassName]
    presel = preselClass()
    setattr(presel,"sourcefile",options.preselection)

sampleBase = "/home/adamwo/data/monoJetTuples_v7/"
if options.dset=="singleMu":
    sampleBase += "copyMu/"
elif options.dset=="diMu":
    sampleBase += "copyMu/"
else:
    sampleBase += "copy/"


samples = []
if options.dset=="singleMu":
    samples.append(Sample("QCD",sampleBase,type="B",color=7,fill=True, \
                              namelist=[ "QCD20to600", "QCD600to1000", "QCD1000" ]))
    samples.append(Sample("WW",sampleBase,type="B",color=6,fill=True))
    samples.append(Sample("DY",sampleBase,type="B",color=3,fill=True))
    samples.append(Sample("singleTop",sampleBase,type="B",color=4,fill=True))
    samples.append(Sample("TTJets-powheg-v2",sampleBase,type="B",color=2,fill=True))
    samples.append(Sample("WJetsHT150v2",sampleBase,type="B",color=5,fill=True))
    samples.append(Sample("stop300lsp270FastSim",sampleBase,type="S",color=4,fill=False))
    samples.append(Sample("stop300lsp240g150FastSim",sampleBase,type="S",color=2,fill=False))
    samples.append(Sample("data",sampleBase,type="D",color=1,fill=False, \
                              namelist=[ 'data_singleMu_Run2012AB', 'data_singleMu_Run2012C', 'data_singleMu_Run2012D' ]))
elif options.dset=="diMu":
    samples.append(Sample("WW",sampleBase,type="B",color=6,fill=True))
    samples.append(Sample("DY",sampleBase,type="B",color=3,fill=True))
    samples.append(Sample("singleTop",sampleBase,type="B",color=4,fill=True))
    samples.append(Sample("TTJetsPowHeg",sampleBase,type="B",color=2,fill=True))
    samples.append(Sample("WJetsHT150v2",sampleBase,type="B",color=5,fill=True))
    samples.append(Sample("stop300lsp270FastSim",sampleBase,type="S",color=4,fill=False))
    samples.append(Sample("stop300lsp240g150FastSim",sampleBase,type="S",color=2,fill=False))
    samples.append(Sample("data","/home/adamwo/data/monoJetTuples_v5/copyDiMu/",type="D",color=1,fill=False, \
                              namelist=[ 'data_singleMu_Run2012AB', 'data_singleMu_Run2012C', 'data_singleMu_Run2012D' ]))
else:
    samples.append(Sample("QCD",sampleBase,type="B",color=7,fill=True, \
                              namelist=[ "QCD20to600", "QCD600to1000", "QCD1000" ]))
    samples.append(Sample("WW",sampleBase,type="B",color=6,fill=True))
    samples.append(Sample("DY",sampleBase,type="B",color=3,fill=True))
    samples.append(Sample("singleTop",sampleBase,type="B",color=4,fill=True))
    #samples.append(Sample("TTJets",sampleBase,type="B",color=2,fill=True))
    samples.append(Sample("TTJetsPowHeg",sampleBase,type="B",color=2,fill=True))
##    samples.append(Sample("WJetsToLNu",sampleBase,type="B",color=5,fill=True)
#    samples.append(Sample("WJetsToLNuTau",sampleBase,type="B",color=8,fill=True, \
#                              namelist=["WJetsToLNu"],filter=LeptonFilter(16)))
#    samples.append(Sample("WJetsToLNuNoTau",sampleBase,type="B",color=5,fill=True, \
#                              namelist=["WJetsToLNu"],filter=InvertedSampleFilter(LeptonFilter(16))))
#    samples.append(Sample("WJetsToLNu",sampleBase,type="B",color=5,fill=True))
#    samples.append(Sample("WJetsToLNu",sampleBase,type="B",color=5,fill=True))
#    samples.append(Sample("WJetsHT150v2",sampleBase,type="B",color=5,fill=True))
    samples.append(Sample("WJetsHT150v2Tau",sampleBase,type="B",color=8,fill=True, \
                              namelist=["WJetsHT150v2"],filter=LeptonFilter(16)))
    samples.append(Sample("WJetsHT150v2NoTau",sampleBase,type="B",color=5,fill=True, \
                              namelist=["WJetsHT150v2"],filter=InvertedSampleFilter(LeptonFilter(16))))
    #samples.append(Sample("WJetsHT250",sampleBase,type="B",color=5,fill=True))
    #samples.append(Sample("WNJetsToLNu",sampleBase,type="B",color=5,fill=True,downscale=2, \
    #                          namelist=[ "W1JetsToLNu", "W2JetsToLNu", "W3JetsToLNu", "W4JetsToLNu"  ]))
    #samples.append(Sample("W1JetsToLNu",sampleBase,type="B",color=2,fill=True,hatch=3245))
    #samples.append(Sample("W2JetsToLNu",sampleBase,type="B",color=3,fill=True,hatch=3254))
    #samples.append(Sample("W3JetsToLNu",sampleBase,type="B",color=4,fill=True,hatch=3245))
    #samples.append(Sample("W4JetsToLNu",sampleBase,type="B",color=5,fill=True,hatch=3254))
    #samples.append(Sample("stop200lsp170g100FastSim",sampleBase,type="S",color=2,fill=False))
#    samples.append(Sample("stop300lsp270g175FastSim",sampleBase,type="S",color=1,line=1,fill=False))
    samples.append(Sample("stop300lsp270g200FastSim",sampleBase,type="S",color=1,line=2,fill=False))
    samples.append(Sample("stop300lsp240g150FastSim",sampleBase,type="S",color=1,line=1,fill=False))
##    samples.append(Sample("stop300lsp270FastSim",sampleBase,type="S",color=4,fill=False))
##    samples.append(Sample("T2DegStop_225_145",sampleBase,type="S",color=3,fill=False))
##    samples.append(Sample("T2DegStop_200_170",sampleBase,type="S",color=3,fill=False))
##    samples.append(Sample("T2DegStop_150_120",sampleBase,type="S",color=2,fill=False))
#    samples.append(Sample("T2DegStop_100_20",sampleBase,type="S",color=1,line=1,fill=False))
#    samples.append(Sample("T2DegStop_225_145",sampleBase,type="S",color=1,line=2,fill=False))
#    samples.append(Sample("T2DegStop_200_140",sampleBase,type="S",color=1,line=1,fill=False))
#    samples.append(Sample("T2DegStop_200_170",sampleBase,type="S",color=1,line=2,fill=False))
#    samples.append(Sample("T2DegStop_150_120",sampleBase,type="S",color=1,line=4,fill=False))
    if options.data:
        samples.append(Sample("data",sampleBase,type="D",color=1,fill=False))

ROOT.TH1.SetDefaultSumw2()

allplots = [ ]
variables = { }
for s in samples:
    plots = plotClass(s.name,presel,elist=options.elist,elistBase=options.elistBase,rebin=options.rebin)
    if options.fomByBin:
        for v in plots.getVariables1D():
            v.scut = 'b'
    allplots.append(plots)
    plots.fillall(s)
    if len(variables)==0:
        variableNames = plots.getVariables()
        for varname in variableNames:
            variables[varname] = ( plots.getVariables()[varname] , [ ] )
    for varname in variables:
        variables[varname][1].append(plots.histograms()[varname])
#    print s.name," : ",plots.hdr.GetSumOfWeights()


ROOT.gROOT.cd()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

if options.save:
    savedir = "".join(s for s in options.save if s in string.letters+string.digits+"_-")
    savedir = "plots_"+savedir+"/"
    if not os.path.isdir(savedir):
        os.mkdir(savedir)
    else:
        os.system("rm "+savedir+"*.png")
        os.system("rm "+savedir+"*.root")
canvases = [ ]
pads = [ ]
allobjects = [ ]
definedPalette = False
for varname in variables:

    showCanvas = False if selectedCanvasNames else True
    for cnvname in selectedCanvasNames:
        if fnmatch(varname,cnvname):
            showCanvas = True
            break
    if not showCanvas:
        continue

    variable, histograms = variables[varname]


#    cnv = ROOT.TCanvas(bkgs.GetName(),bkgs.GetName(),700,700)
    cnv = ROOT.TCanvas("cnv","cnv",700,700)

#    drawClass = DrawWithFOM(fom=options.fom)

    data = None
    if variable.is2D():
        cnv.SetRightMargin(0.15)
        if not definedPalette:
            ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/useNiceColorPalette.C")
            ROOT.useNiceColorPalette()
            definedPalette = True
        data, bkgs, sigs, legend = drawClass.drawStack2D(samples,histograms,cnv)
        if variable.uselog:
            cnv.SetLogz(1)

    else:
        if options.fom!=None:
            p1 = ROOT.TPad("p1","", 0, 0.28, 1, 0.95)
            p1.SetTopMargin(1e-7)
            p1.Draw()
            p2 = ROOT.TPad("p2","", 0, 0, 1, 0.3)
            p2.SetTopMargin(1e-7)
            p2.Draw()
            if not options.batch:
                pads.append(p1)
                pads.append(p2)
        else:
            p1 = ROOT.TPad("p1","", 0, 0., 1, 0.95)
            p1.SetTopMargin(1e-7)
            p1.Draw()
            if not options.batch:
                pads.append(p1)

        data, bkgs, sigs, legend = drawClass.drawStack1D(samples,histograms,p1)
        if data==None and bkgs==None and sigs==None and legend==None:
            continue
        if variable.uselog:
            p1.SetLogy(1)

    if not options.batch:
        canvases.append(cnv)

    ROOT.SetOwnership(bkgs,False)
    cnv.SetName(bkgs.GetName())
    cnv.SetTitle(bkgs.GetName())
    if not options.batch:
        if data!=None:
            allobjects.append(data)
        if bkgs!=None:
            allobjects.append(bkgs)
        if legend!=None:
            allobjects.append(legend)
        if len(sigs)>0:
            allobjects.extend(sigs)
    if not variable.is2D() and bkgs!=None and options.fom!=None:
#        drawClass.drawSoB(bkgs,sigs,variable.scut,pad=p2)
        if data!=None and options.fom=="dataovermc":
            drawClass.drawDoMC(data,bkgs,pad=p2)
        elif variable.scut!=None:
            drawClass.drawFom(bkgs,sigs,variable.scut,pad=p2)
    cnv.Update()
    if options.save:
        cnv.SaveAs(savedir+cnv.GetName()+".png")
        cnv.SaveAs(savedir+cnv.GetName()+".root")
    if options.batch:
        del cnv

if not options.batch:
    raw_input("Press enter")
#if options.save:
#    savedir = "".join(s for s in options.save if s in string.letters+string.digits+"_-")
#    savedir = "plots_"+savedir+"/"
#    if not os.path.isdir(savedir):
#        os.mkdir(savedir)
#    else:
#        os.system("rm "+savedir+"*.png")
#        os.system("rm "+savedir+"*.root")
#    for c in canvases:
#        c.SaveAs(savedir+c.GetName()+".png")
#        c.SaveAs(savedir+c.GetName()+".root")
print "continuing"
