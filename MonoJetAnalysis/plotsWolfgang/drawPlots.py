import ROOT
import os,sys,string
from Sample import *
from drawWithFOM import *
#from drawSoB import *
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--preselection", "-p", dest="preselection",  help="preselection", default=None)
parser.add_option("--draw", "-d", dest="drawClass",  help="draw class", default="DrawWithFOM.py")
parser.add_option("--elist", "-e", dest="elist",  help="event list mode", choices=[ "w", "r", "a" ], default=None )
parser.add_option("--fom", dest="fom",  help="fom to be used", choices=[ "sob", "sosqrtb", "dataovermc", "None" ], default="sosqrtb" )
parser.add_option("--elistBase", dest="elistBase",  help="base directory for event lists", default="./elists")
parser.add_option("-s", dest="save",  help="directory for saved plots", default=None)
parser.add_option("-b", dest="batch",  help="batch mode", action="store_true", default=False)
parser.add_option("--rebin", dest="rebin",  help="rebin factor", type=int, default=1)
parser.add_option("--singleMu", dest="singleMu", help="use single mu dataset", action="store_true", default=False)
(options, args) = parser.parse_args()
assert len(args)>0
if options.fom=="None":
    options.fom = None
assert options.rebin>0

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

sampleBase = "/home/adamwo/data/monoJetTuples_v5/"
if options.singleMu:
    sampleBase += "copyMu/"
else:
    sampleBase += "copy/"


samples = []
if options.singleMu:
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
else:
    samples.append(Sample("QCD",sampleBase,type="B",color=7,fill=True, \
                              namelist=[ "QCD20to600", "QCD600to1000", "QCD1000" ]))
    samples.append(Sample("WW",sampleBase,type="B",color=6,fill=True))
    samples.append(Sample("DY",sampleBase,type="B",color=3,fill=True))
    samples.append(Sample("singleTop",sampleBase,type="B",color=4,fill=True))
    #samples.append(Sample("TTJets",sampleBase,type="B",color=2,fill=True))
    samples.append(Sample("TTJets-powheg-v2",sampleBase,type="B",color=2,fill=True))
    #samples.append(Sample("WJetsToLNu",sampleBase,type="B",color=5,fill=True))
    samples.append(Sample("WJetsHT150v2",sampleBase,type="B",color=5,fill=True))
    #samples.append(Sample("WJetsHT250",sampleBase,type="B",color=5,fill=True))
    #samples.append(Sample("WNJetsToLNu",sampleBase,type="B",color=5,fill=True,downscale=2, \
    #                          namelist=[ "W1JetsToLNu", "W2JetsToLNu", "W3JetsToLNu", "W4JetsToLNu"  ]))
    #samples.append(Sample("W1JetsToLNu",sampleBase,type="B",color=2,fill=True,hatch=3245))
    #samples.append(Sample("W2JetsToLNu",sampleBase,type="B",color=3,fill=True,hatch=3254))
    #samples.append(Sample("W3JetsToLNu",sampleBase,type="B",color=4,fill=True,hatch=3245))
    #samples.append(Sample("W4JetsToLNu",sampleBase,type="B",color=5,fill=True,hatch=3254))
    #samples.append(Sample("stop200lsp170g100FastSim",sampleBase,type="S",color=2,fill=False))
    #samples.append(Sample("stop300lsp270g175FastSim",sampleBase,type="S",color=3,fill=False))
    #samples.append(Sample("stop300lsp270g200FastSim",sampleBase,type="S",color=4,fill=False))
    samples.append(Sample("stop300lsp270FastSim",sampleBase,type="S",color=4,fill=False))
    samples.append(Sample("stop300lsp240g150FastSim",sampleBase,type="S",color=2,fill=False))
    samples.append(Sample("data",sampleBase,type="D",color=1,fill=False))

ROOT.TH1.SetDefaultSumw2()

allplots = [ ]
variables = { }
for s in samples:
    plots = plotClass(s.name,presel,elist=options.elist,elistBase=options.elistBase,rebin=options.rebin)
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

canvases = [ ]
pads = [ ]
allstacks = [ ]
definedPalette = False
for varname in variables:
    variable, histograms = variables[varname]


#    cnv = ROOT.TCanvas(bkgs.GetName(),bkgs.GetName(),700,700)
    cnv = ROOT.TCanvas("cnv","cnv",700,700)
    canvases.append(cnv)

#    drawClass = DrawWithFOM(fom=options.fom)

    data = None
    if variable.is2D():
        cnv.SetRightMargin(0.15)
        if not definedPalette:
            ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/useNiceColorPalette.C")
            ROOT.useNiceColorPalette()
            definedPalette = True
        data, bkgs, sigs, legend = drawClass.drawStack2D(samples,histograms,cnv)
        if variable.uselog:
            cnv.SetLogz(1)

    else:
        p1 = ROOT.TPad("p1","", 0, 0.28, 1, 0.95)
        p1.SetTopMargin(1e-7)
        p1.Draw()
        p2 = ROOT.TPad("p2","", 0, 0, 1, 0.3)
        p2.SetTopMargin(1e-7)
        p2.Draw()

        pads.append(p1)
        pads.append(p2)


        data, bkgs, sigs, legend = drawClass.drawStack1D(samples,histograms,p1)
        if variable.uselog:
            p1.SetLogy(1)

    cnv.SetName(bkgs.GetName())
    cnv.SetTitle(bkgs.GetName())
    if data!=None:
        allstacks.append(data)
    if bkgs!=None:
        allstacks.append(bkgs)
    if len(sigs)>0:
        allstacks.extend(sigs)
    if not variable.is2D() and bkgs!=None and options.fom!=None:
#        drawClass.drawSoB(bkgs,sigs,variable.scut,pad=p2)
        if data!=None and options.fom=="dataovermc":
            drawClass.drawDoMC(data,bkgs,pad=p2)
        elif variable.scut!=None:
            drawClass.drawFom(bkgs,sigs,variable.scut,pad=p2)
    cnv.Update()

if not options.batch:
    raw_input("Press enter")
if options.save:
    savedir = "".join(s for s in options.save if s in string.letters+string.digits+"_-")
    savedir = "plots_"+savedir+"/"
    if not os.path.isdir(savedir):
        os.mkdir(savedir)
    else:
        os.system("rm "+savedir+"*.png")
        os.system("rm "+savedir+"*.root")
    for c in canvases:
        c.SaveAs(savedir+c.GetName()+".png")
        c.SaveAs(savedir+c.GetName()+".root")
print "continuing"
