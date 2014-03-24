import ROOT
from ROOT import RooFit as RF
from ROOT import std
import os, ctypes
from math import *

ROOT.gROOT.ProcessLine(".x load.cc")

met_min = 0 
met_max = 1000
binning = range(0,met_max, 100)+[met_max]
initial_vals = [ exp(-i)  for i in range(len(binning) -1)]

met            = ROOT.RooRealVar("met", "met", 100, 0, met_max) 
met .setMin(met_min)
met .setMax(met_max)
met.setRange("fit_range", met_min, met_max)
met.setRange("test_range", met_min+50, met_max)
         
min_met = ROOT.RooRealVar("min_met", "min_met", 0.)
min_met.setConstant() 

c_bins = ((ctypes.c_double)*(len(binning)))(*binning)

stuff=[]

def makeBinnedPDF(name, binning):
  tot = float(sum(initial_vals))
  inormVals = [x/tot for x in initial_vals]
  subLeadingArgs = ROOT.RooArgList(name+"_subLArgs")
  sstring = "1."
  for i in range(1, len(binning) - 1 ):
    rv = ROOT.RooRealVar(name+"_a"+str(i), name+"_a"+str(i),  inormVals[i] , 0., 1.)
    stuff.append(rv)
  #  rv.Print()
    subLeadingArgs.add(rv)
    sstring+="-@"+str(i-1)
  print sstring
  la = ROOT.RooFormulaVar(name+"_a0", name+"_a0", sstring, subLeadingArgs)
#  la = ROOT.RooFormulaVar(name+"_a0Gr0", name+"_a0Gr0", "(@0>0)*@0", ROOT.RooArgList(lb))
  #  la.setMin(0.)
  #  la.setMax(1.)
  stuff.append(la)
  allArgs=ROOT.RooArgList(name+"_allArgs")
  allArgs.add(la)
  for i in range(subLeadingArgs.getSize()):
    allArgs.add(subLeadingArgs.at(i))
   
  metBinning = ROOT.RooBinning(len(c_bins)-1, c_bins, "met_binning")
  stuff.append(metBinning)
  pdf = ROOT.RooBinnedPDF(name+"_RooBinnedPDF", name+"_RooBinnedPDF", met, allArgs, metBinning)
  return pdf

def snapShotBinnedPDF(name, pdf):
  args = ROOT.RooArgList(name+"_snArgList")
  binning = pdf.binning_
  for i in range(binning.numBins()):
    val = pdf.args_.at(i).getVal()
    a = ROOT.RooRealVar(name+"_a"+str(i), name+"_a"+str(i), val)
    a.setConstant(1)
    args.add(a)
    stuff.append(a)
  ret = ROOT.RooBinnedPDF(name+"_snapshot_RooBinnedPDF", name+"_snapshot_RooBinnedPDF", met, args, binning)
  return ret
  
pdf = makeBinnedPDF("def", binning)
pdf_init = snapShotBinnedPDF("snap", pdf)

data = pdf.generate(ROOT.RooArgSet(met),10000)

nllComponents = ROOT.RooArgSet("nllComponents")
nll = pdf.createNLL( data, RF.Range("fit_range"), RF.SumCoefRange("fit_range"), RF.NumCPU(2) )
nllComponents.add(nll)

sumNLL = ROOT.RooAddition("sumNLL","sumNLL", nllComponents)
allParams = sumNLL.getParameters(data)
minuit = ROOT.RooMinuit(sumNLL)
minuit.setStrategy(1)
minuit.setPrintEvalErrors(-1)
minuit.setPrintLevel(3)
#minuit.optimizeConst(True)

status = minuit.hesse()
print "-> initialize hesse (status = ", status, ")"
initialhesseresult = minuit.save("initialhesseResult","initialhesseResult")
initialhesseresult.Print()

status = minuit.migrad()
print "-> migrad (status = ", status, ")"
migradresult = minuit.save("migradResult","migradResult")
migradresult.Print()
status = minuit.hesse()
print "-> hesse (status = ", status, ")"
hesseresult = minuit.save("hesseResult","hesseResult")
hesseresult.Print()

metFrame = met.frame(RF.Title("Demo of threshold and binning mapping functions"))
data.plotOn(metFrame)
pdf_init.plotOn(metFrame)
pdf.plotOn(metFrame,RF.LineColor(ROOT.kRed))

c1 = ROOT.TCanvas("rf405_realtocatfuncs","rf405_realtocatfuncs",600,600)
c1.SetLogy()
metFrame.SetMinimum(10**-4)
ROOT.gPad.SetLeftMargin(0.15)
metFrame.GetYaxis().SetTitleOffset(1.4)
metFrame.Draw()
