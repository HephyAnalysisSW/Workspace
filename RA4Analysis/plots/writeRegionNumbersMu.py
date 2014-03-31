import ROOT
from array import array
from math import *
import os, copy

from Workspace.RA4Analysis.simplePlotsCommon import *
import xsec
small = False

regions = ["A","B","C","D", "All", "LB"]

from defaultMuSamples import *

if not globals().has_key("dataLoaded"):
  global dataLoaded
  dataLoaded=False
dataLoaded = False

#presel = "2j80+1j50"
#presel = "2j80+2j50"
#presel = "120_80_50"
presel = "pf-4j30-l15"

mode = "ht"
var1 = "kinMetSig"
var2 = mode
subdir = "/Mu-"+mode+"-kMs/"+presel+"/"
#preprefix = "WJLNu_" 
preprefix = "" 

chainstring = "empty"
commoncf = "(0)"
var1_cut1 = -1.
var1_cut2 = -1.
var1_cut3 = -1.
var2_cut1 = -1.
var2_cut2 = -1.
var2_cut3 = -1.

if presel == "2j80+1j50":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet1pt>80&&jet2pt>50&&lepton_pt>20&&singleMuonic"
if presel == "2j80+2j50":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet1pt>80&&jet3pt>50&&lepton_pt>20&&singleMuonic"
if presel == "120_80_50":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet0pt>120&&jet1pt>80&&jet2pt>50&&lepton_pt>20&&singleMuonic"
if presel == "pf-4j30":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet3pt>30&&lepton_pt>20&&singleMuonic"
if presel == "pf-4j30-l15":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet3pt>30&&lepton_pt>15&&singleMuonic"

prefix = preprefix+presel+"_2011_"

for sample in allSamples:
  sample["Chain"] = chainstring

def cutDict(var1, var2, var1_cut1, var1_cut2, var1_cut3, var2_cut1, var2_cut2,var2_cut3):
  dict={}
  dict[var1]=[[var1_cut1,var1_cut2],[var1_cut3, -1]]
  dict[var2]=[[var2_cut1,var2_cut2],[var2_cut3, -1]]
  return dict

if dataLoaded:
  print "Loading file",prefix+"allSamples.txt"
  allSamples = eval(file(prefix+"allSamples.txt","r").read())
if not dataLoaded:
  dataLoaded=True
  for sample in allSamples:
    sample["filenames"]={}
    sample["weight"]={}
    if not sample.has_key("bins"):
      sample["bins"]=[""]
    for bin in sample["bins"]:
      subdirname = sample["dirname"]+"/"+bin+"/"
      if sample["bins"]==[""]:
        subdirname = sample["dirname"]+"/"
      c = ROOT.TChain("countingHLTFilter/CountTree")
      sample["filenames"][bin]=[]
      if small:
        filelist=os.listdir(subdirname)
        counter = 1   #Joining n files
        for thisfile in filelist:
          if os.path.isfile(subdirname+thisfile) and thisfile[-5:]==".root" and thisfile.count("histo")==1:
            sample["filenames"][bin].append(subdirname+thisfile)
  #          c.Add(sample["dirname"]+thisfile)
            if counter==0:
              break
            counter=counter-1
      else:
        sample["filenames"][bin] = [subdirname+"/h*.root"]
      for thisfile in sample["filenames"][bin]:
        c.Add(thisfile)
      nevents = c.GetEntries()
      weight = 1.
      lumi = 1.
      if globals().has_key("targetLumi"):
        lumi = targetLumi
      if xsec.xsec.has_key(bin):
        if nevents>0:
          weight = xsec.xsec[bin]*lumi/float(nevents)
        else:
          weight = 0.
      print sample["name"], bin, nevents,"weight",weight
      sample["weight"][bin]=weight
      del c
  for sample in allSamples:
    sample["Events"]={}
    for bin in sample["bins"]:
      sample["Events"][bin] = []
      c = ROOT.TChain(sample["Chain"])
      for thisfile in sample["filenames"][bin]:
        c.Add(thisfile)
      ntot = c.GetEntries()
      if ntot>0:
        c.Draw(">>eList",commoncf)
        elist = ROOT.gDirectory.Get("eList")
        number_events = elist.GetN()
        print "Reading: ", sample["name"], bin, "with",number_events,"Events"
        if small:
          if number_events>20000:
            number_events=20000
        for i in range(0, number_events):
          if (i%10000 == 0) and i>0 :
            print i
    #      # Update all the Tuples
          if elist.GetN()>0 and c.GetEntries()>0:
            c.GetEntry(elist.GetEntry(i))
            var1val = 0.
            for varstring in var1.split("+"):
              var1val += c.GetLeaf( varstring ).GetValue()
            var2val = 0.
            for varstring in var2.split("+"):
              var2val += c.GetLeaf( varstring ).GetValue()
            Event = {}
            Event["var1"] = var1val
            Event["var2"] = var2val
            sample["Events"][bin].append(Event)
        del elist
        del c
      else:
        print "Zero entries in", bin, sample["name"]
  print "Writing file",prefix+"allSamples.txt"
  file(prefix+"allSamples.txt","w").write(repr(allSamples))


def writeCutRegions(var1_start,var1_diff1,var1_diff2,var2_val1,var2_val2,var2_val3):
  var1_cut1 = var1_start
  var1_cut2 = var1_start + var1_diff1
  var1_cut3 = var1_start + var1_diff1 + var1_diff2
  var2_cut1 = var2_val1 
  var2_cut2 = var2_val2
  var2_cut3 = var2_val3
  def lowerBound(var1val, var2val):
    return var1val>=var1_cut1 and var2val>=var2_cut1
  def lowerVar1(var1val):
    return var1val>=var1_cut1 and var1val<var1_cut2
  def upperVar1(var1val):
    return var1val>=var1_cut3
  def lowerVar2(var2val):
    return var2val>=var2_cut1 and var2val<var2_cut2
  def upperVar2(var2val):
    return var2val>=var2_cut3
  numbers={}
  for sample in allSamples:
    for bin in sample["bins"]:
      numbers[bin]={}
      numbers[bin]["Entries"] = {}
      numbers[bin]["Events"] = {}
      numbers[bin]["weight"] = sample["weight"][bin]
      for r in regions:
        numbers[bin]["Entries"][r] = 0
      for event in sample["Events"][bin]:
        lv1 = lowerVar1(event["var1"])
        lv2 = lowerVar2(event["var2"])
        uv1 = upperVar1(event["var1"])
        uv2 = upperVar2(event["var2"])
        lb  = lowerBound(event["var1"], event["var2"])
        numbers[bin]["Entries"]["All"]+=1
        if lv1 and lv2:
          numbers[bin]["Entries"]["A"]+=1
        if lv1 and uv2:
          numbers[bin]["Entries"]["B"]+=1
        if uv1 and lv2:
          numbers[bin]["Entries"]["C"]+=1
        if uv1 and uv2:
          numbers[bin]["Entries"]["D"]+=1
        if lb:
          numbers[bin]["Entries"]["LB"]+=1
      for r in regions:
        numbers[bin]["Events"][r] = sample["weight"][bin]*numbers[bin]["Entries"][r]
  filename = "/afs/hephy.at/scratch/s/schoefbeck/ABCDData_2011/"+subdir+"/"+prefix+getABCDDataFileName(var1, var2, var1_cut1, var1_cut2, var1_cut3, var2_cut1, var2_cut2, var2_cut3)
  outfile = file(filename,"w")
  outfile.write("targetLumi="+str(targetLumi)+"\n")
  outfile.write("data_bins="+repr(data["bins"])+"\n")
  outfile.write("WJets_Bins="+repr(wjets["bins"])+"\n")
  outfile.write("ZJets_Bins="+repr(zjets["bins"])+"\n")
  outfile.write("QCD_Bins="+repr(qcd["bins"])+"\n")
  outfile.write("singleTop_Bins="+repr(stop["bins"])+"\n")
  outfile.write("cuts="+repr(cutDict(var1, var2, var1_cut1, var1_cut2, var1_cut3, var2_cut1, var2_cut2,var2_cut3))+"\n")
  outfile.write("preSelectionROOTCut = "+repr(commoncf)+"\n")
  outfile.write("numbers="+repr(numbers))
  outfile.close()
  print "Written", filename, "mode", mode


writeCutRegions(2.5, 3.0, 0, 300, 650, 650)
for var1_start in frange(2.5,3.51,.5):
  for var1_diff1 in frange(1.,7.01,.5):
    for var1_diff2 in frange(0,1.01,1):
      for var2_val1 in [300,350,400,450,500,550,600,650,700,750,800,850]:
        for var2_val2 in [300,350,400,450,500,550,600,650,700,750,800,850,900]:
#        for var2_val2 in [320,330,350,360,370,380,400,430, 440, 450,470, 500]:
#          for var2_val3 in [300,320,330,350,380,400]:
            for var2_val3 in [var2_val2, var2_val2 + 50, var2_val2 + 100]:
#              if var1_start + var1_diff1 + var1_diff2 < 6.5 and var2_val1<=var2_val2 and var2_val2<=var2_val3 and ((var2_val3-var2_val2==0) or (var2_val3-var2_val2>=50)): 
              if var2_val1<=var2_val2 and var2_val2<=var2_val3 and ((var2_val3-var2_val2==0) or (var2_val3-var2_val2>=50)):                                               
                writeCutRegions(var1_start, var1_diff1, var1_diff2, var2_val1, var2_val2, var2_val3)

