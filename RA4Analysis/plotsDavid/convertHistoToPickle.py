import ROOT
import pickle
import copy, os, sys

from math import *
from Workspace.HEPHYPythonTools.user import *

ROOT.TH1F().SetDefaultSumw2()

rootFile = ROOT.TFile('/afs/hephy.at/user/d/dhandl/www/RunII/Spring15_50ns/ZtoWclosure_MCstudy/njet2_nbtagEq0_genLevel_1stLepNu_Z-Wclosure_Lp.root')
pickleFileName = 'njet2_nbtagEq0_Z-Wratio_Lp_pkl'
picklePath = '/data/'+username+'/results2015/convertHistToPickle/'

histInformation = []

yes = set(['yes','y'])
no = set(['no','n'])

print '+++ File content: +++'
print rootFile.ls()
can = input("What's the name of the canvas? ")
canvas = rootFile.Get(can)
print '+++ Canvas content: +++'
print canvas.GetListOfPrimitives().ls()
choice = raw_input("Does canvas have multiple pads? (y/n) ").lower()
if choice in yes:
  pad = input("What's the name of the pad? ")
  hist = input("What's the name of the histogram? ")
  histogram = canvas.GetPrimitive(pad).GetPrimitive(hist)
elif choice in no:
  hist = input("What's the name of the histogram? ")
  histogram = canvas.GetPrimitive(hist)
else:
   sys.stdout.write("Please respond with 'yes' or 'no'")

bins = histogram.GetNbinsX()

underFlow = {'BinLowEdge':histogram.GetBinLowEdge(0), 'BinContent':histogram.GetBinContent(0), 'BinError':histogram.GetBinError(0)}
overFlow =  {'BinLowEdge':histogram.GetBinLowEdge(bins+1), 'BinContent':histogram.GetBinContent(bins+1), 'BinError':histogram.GetBinError(bins+1)}

histInformation.append(underFlow)

for i in range(bins):
  histInformation.append({'BinLowEdge':histogram.GetBinLowEdge(i+1), 'BinContent':histogram.GetBinContent(i+1), 'BinError':histogram.GetBinError(i+1)})

histInformation.append(overFlow)

if not os.path.exists(picklePath):
  os.makedirs(picklePath)
pickle.dump(histInformation, file(picklePath+pickleFileName,'w'))


