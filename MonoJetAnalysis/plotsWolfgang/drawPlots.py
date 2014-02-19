import ROOT
import os,sys
from Sample import *
from drawWithFOM import *
#from drawSoB import *
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--preselection", "-p", dest="preselection",  help="preselection", default=None)
parser.add_option("--elist", "-e", dest="elist",  help="event list mode", choices=[ "w", "r" ], default=None )
parser.add_option("--elistBase", dest="elistBase",  help="base directory for event lists", default="./elists")
parser.add_option("-s", dest="save",  help="save plots", action="store_true", default=False)
parser.add_option("-b", dest="batch",  help="batch mode", action="store_true", default=False)
(options, args) = parser.parse_args()
assert len(args)>0

plotGlobals = {}
execfile(args[0],plotGlobals)
plotClassName = os.path.splitext(os.path.basename(args[0]))[0]
plotClass = plotGlobals[plotClassName]

presel = None
if options.preselection!=None:
    preselGlobals = {}
    execfile(options.preselection,preselGlobals)
    preselClassName = os.path.splitext(os.path.basename(options.preselection))[0]
    preselClass = preselGlobals[preselClassName]
    presel = preselClass()

sampleBase = "/home/adamwo/data/monoJetTuples_v4/copy/"


samples = []
samples.append(Sample("QCD",sampleBase,type="B",color=7,fill=True, \
                          namelist=[ "QCD20to600", "QCD600to1000", "QCD1000" ]))
samples.append(Sample("WW",sampleBase,type="B",color=6,fill=True))
samples.append(Sample("DY",sampleBase,type="B",color=3,fill=True))
samples.append(Sample("singleTop",sampleBase,type="B",color=4,fill=True))
samples.append(Sample("TTJets",sampleBase,type="B",color=2,fill=True))
#samples.append(Sample("WJetsToLNu",sampleBase,type="B",color=5,fill=True))
samples.append(Sample("WNJetsToLNu",sampleBase,type="B",color=5,fill=True,downscale=2, \
                          namelist=[ "W1JetsToLNu", "W2JetsToLNu", "W3JetsToLNu", "W4JetsToLNu"  ]))
#samples.append(Sample("stop200lsp170g100FastSim",sampleBase,type="S",color=2,fill=False))
#samples.append(Sample("stop300lsp270g175FastSim",sampleBase,type="S",color=3,fill=False))
#samples.append(Sample("stop300lsp270g200FastSim",sampleBase,type="S",color=4,fill=False))
samples.append(Sample("stop300lsp270FastSim",sampleBase,type="S",color=4,fill=False))
samples.append(Sample("stop300lsp240g150FastSim",sampleBase,type="S",color=2,fill=False))

ROOT.TH1.SetDefaultSumw2()

allplots = [ ]
variables = { }
for s in samples:
    plots = plotClass(s.name,presel,elist=options.elist,elistBase=options.elistBase)
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
allstacks = [ ]
for varname in variables:
    variable, histograms = variables[varname]


#    cnv = ROOT.TCanvas(bkgs.GetName(),bkgs.GetName(),700,700)
    cnv = ROOT.TCanvas("cnv","cnv",700,700)
    canvases.append(cnv)

    p1 = ROOT.TPad("p1","", 0, 0.28, 1, 0.95)
    p1.SetTopMargin(1e-7)
    p1.Draw()
    p2 = ROOT.TPad("p2","", 0, 0, 1, 0.3)
    p2.SetTopMargin(1e-7)
    p2.Draw()

    drawClass = DrawWithFOM()

    bkgs, sigs, legend = drawClass.drawStack(samples,histograms,p1)
    if variable.uselog:
        p1.SetLogy(1)
    cnv.SetName(bkgs.GetName())
    cnv.SetTitle(bkgs.GetName())
    if bkgs!=None:
        allstacks.append(bkgs)
    if len(sigs)>0:
        allstacks.extend(sigs)
    if bkgs!=None and variable.scut!=None:
#        drawClass.drawSoB(bkgs,sigs,variable.scut,pad=p2)
        drawClass.drawSoSqrtB(bkgs,sigs,variable.scut,pad=p2)
    cnv.Update()
#    if bkgs!=None:
#        cnv = drawClass.drawSoSqrtB(bkgs,sigs,'l',pad=p2)
#        canvases.append(cnv)

if not options.batch:
    raw_input("Press enter")
if options.save:
    for c in canvases:
        c.SaveAs(c.GetName()+".png")
print "continuing"
