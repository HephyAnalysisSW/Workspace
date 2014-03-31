import ROOT
from array import array
from math import *
import os, copy

from Workspace.RA4Analysis.simplePlotsCommon import *
#execfile("simplePlotsCommon.py")
import xsec
small = False

from defaultEleSamples import *
mode = "ht"
#jes = "jes103"
jes = ""

var2 = mode

allVars=[]
allStacks=[]

if mode == "ht":
  niceVar2Name = "H_{T}"
if mode == "ht2":
  niceVar2Name = "H_{T2}"

def kinMetSigBin(cutlow, cuthigh = -1):
  if cuthigh>0:
    return "&&(kinMetSig>"+str(cutlow)+")&&(kinMetSig<"+str(cuthigh)+")"
  else:
    return "&&(kinMetSig>"+str(cutlow)+")"

def var2Bin(var2, cutlow, cuthigh = -1):
  if cuthigh>0:
    return "&&("+var2+">"+str(cutlow)+")&&("+var2+"<"+str(cuthigh)+")"
  else:
    return "&&("+var2+">"+str(cutlow)+")"

def getStack(varstring, binning, cutstring):
  MC               = variable(varstring, binning, cutstring)
  MC.sample        = copy.deepcopy(mc)
  bins = ["TTJets"]
  bins.extend(WJets_Bins)
  bins.extend(ZJets_Bins)
  bins.extend(singleTop_Bins)
  MC.sample["bins"] = bins 
  MC.style              = "f"
  res = [MC]
  getLinesForStack(res, targetLumi)
  return res 

#datapath ="/afs/hephy.at/user/s/schoefbeck/www/ABCDData/pf-4j30/"
#filelist = os.listdir(datapath)
#for filename in filelist:
if mode == "ht":
  print "Importing points_ht_Ele"
  from points_ht_Ele import points
if mode == "ht2":
  print "Importing points_ht2_Ele"
  from points_ht2_Ele import points

for point in points:
  exec(file(point,"r").read())
  presel = point.split("/")[-2]
  if jes!="":
    prefix =  "Ele-"+presel+"_"+jes+"_"+point.split("/")[-1][0:-3]+"_"
  else:
    prefix =  "Ele-"+presel+"_"+point.split("/")[-1][0:-3]+"_"

  chainstring = "empty"
  commoncf = "(0)"

  if presel == "pf-4j30":
    chainstring = jes+"pfRA4Analyzer/Events"
  commoncf = preSelectionROOTCut
  print "At",point,"prefix",prefix,chainstring, commoncf
  for sample in allSamples:
    sample["Chain"] = chainstring

  metSigBins  = cuts["kinMetSig"] 
  var2Bins  = cuts[var2] 
  var2_stacks=[]
  for bin in metSigBins:
    var2_stacks.append(getStack(":"+var2+";"+niceVar2Name+" [GeV];Number of Events / 50 GeV",[31,0,1550], commoncf+kinMetSigBin(*bin)+"&&"+var2+">"+str(cuts[var2][0][0])))
  kinMetSig_stacks=[]
  for bin in var2Bins:
    kinMetSig_stacks.append(getStack(":kinMetSig;S_{MET};Number of Events",[17,0,17], commoncf+var2Bin(var2,*bin)+"&&kinMetSig>"+str(cuts["kinMetSig"][0][0])) )
  for stack in var2_stacks:
    allStacks.append(stack)
  for stack in kinMetSig_stacks:
    allStacks.append(stack)
  for stack in allStacks:
    for var in stack:
      var.minimum = 0.45

  execfile("simplePlotsKernel.py")

  ROOT.setTDRStyle()
  ROOT.gStyle.SetOptStat(0)

  def binName(cutlow, cuthigh = -1):
    if cuthigh>0:
      return str(cutlow)+"_"+str(cuthigh)
    else:
      return str(cutlow)

  def legendName(varname, cutlow, cuthigh = -1):
    if cuthigh>0:
      return str(cutlow)+" < "+varname+" < "+str(cuthigh)
    else:
      return str(cutlow)+" < "+varname

  binColors = [ROOT.kBlack, ROOT.kRed + 1, ROOT.kBlue + 2, ROOT.kGreen + 2, ROOT.kOrange + 2, ROOT.kYellow]

  var2_totalBkgStack=[]
  for i in range(len(metSigBins)):
    var2_c = copy.deepcopy(var2_stacks[i][0])
    var2_c.color = binColors[i]
    var2_c.style = "e"
    var2_c.legendText = legendName("S_{MET}", *metSigBins[i]) 
    var2_c.minimum = 0.45
    var2_totalBkgStack.append(var2_c)

  for var in var2_totalBkgStack:
    var.logy=True
  drawNMStacks(1,1,[var2_totalBkgStack],"pngHTBin/Ele/"+mode+"/"+prefix+mode+"_shapes", True)
  for var in var2_totalBkgStack:
    var.logy=False
  drawNMStacks(1,1,[var2_totalBkgStack],"pngHTBin/Ele/"+mode+"/"+prefix+mode+"_shapes_NonLog", True)

  kinMetSig_totalBkgStack=[]
  for i in range(len(var2Bins)):
    kinMetSig_c = copy.deepcopy(kinMetSig_stacks[i][0])
    kinMetSig_c.color = binColors[i]
    kinMetSig_c.style = "e"
    kinMetSig_c.legendText = legendName(niceVar2Name, *var2Bins[i]) 
    kinMetSig_c.minimum = 0.45
    kinMetSig_totalBkgStack.append(kinMetSig_c)
  for var in kinMetSig_totalBkgStack:
    var.logy=True
  drawNMStacks(1,1,[kinMetSig_totalBkgStack],"pngHTBin/Ele/"+mode+"/"+prefix+"kinMetSig_shapes", True)
  for var in kinMetSig_totalBkgStack:
    var.logy=False
  drawNMStacks(1,1,[kinMetSig_totalBkgStack],"pngHTBin/Ele/"+mode+"/"+prefix+"kinMetSig_shapes_NonLog", True)
