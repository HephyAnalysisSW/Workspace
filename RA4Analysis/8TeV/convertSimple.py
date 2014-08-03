import copy
import ROOT
from Workspace.RA4Analysis.simplePlotsCommon import *
from math import *
import os, copy, array, xsec, sys


small = True                             #FIXME: True for debugging, False for the full thing
presel = "pf-3j40"                       #pre-selection
outputDir = "/data/adriana/isoTuples/"   #output directory

#mode = "Mu"      #Ele or Mu?
mode = "Ele"

#chmode = "copy" # For "copying". 
chmode = "Iso"   # For using the isopfRA4Tupelizer

commoncf = "(-1)"
chainstring = "empty"
reweightingHistoFile = "reweightingHisto_Summer2011.root"   #for PU reweighting
isoString = "isopfRA4Tupelizer"
if mode == "Mu":
  from defaultMuSamples import *
if mode == "Ele":
  from defaultEleSamples import *

if mode=="Mu":
  if presel == "pf-3j40":
    commoncf = "jet2pt>40&&ht>300&&ngoodMuons>0"      #Enter your desired cuts here...
    if chmode=="Iso":
      commoncf= isoString+"_jet2pt>40&&"+isoString+"_ht>300&&"+isoString+"_ngoodMuons>0" #...here...
if mode=="Ele":
  if presel == "pf-3j40":
    commoncf = "jet2pt>40&&ht>300&&ngoodElectrons>0" #...here...
    if chmode=="Iso":
      commoncf= isoString+"_jet2pt>40&&"+isoString+"_ht>300&&"+isoString+"_ngoodElectrons>0" #...and here!

#calculate weights (no changes needed probably)
for sample in allSamples:
  sample["filenames"]={}
  sample["weight"]={}
  if not sample.has_key("bins"):
    sample["bins"]=[""]
  for bin in sample["bins"]:
    subdirname = sample["dirname"]+"/"+bin+"/"
    if sample["bins"]==[""]:
      subdirname = sample["dirname"]+"/"
    c = ROOT.TChain("Events")
    sample["filenames"][bin]=[]
    if small:
      filelist=os.listdir(subdirname)
      counter = 1   #Joining n files
      for file in filelist:
        if os.path.isfile(subdirname+file) and file[-5:]==".root" and file.count("histo")==1:
          sample["filenames"][bin].append(subdirname+file)
#          c.Add(sample["dirname"]+file)
          if counter==0:
            break
          counter=counter-1
    else:
      sample["filenames"][bin] = [subdirname+"/h*.root"]
    for file in sample["filenames"][bin]:
      c.Add(file)
    nevents = c.GetEntries("bool_EventCounter_passed_PAT.obj")
    weight = 1.
    if xsec.xsec.has_key(bin):
      if nevents>0:
        weight = xsec.xsec[bin]*targetLumi/nevents
      else:
        weight = 0.
    print sample["name"], bin, nevents,"weight",weight
    sample["weight"][bin]=weight
    del c

#define your variables here. Add anything in the standard alias (i.e. "met" not "isopfRA4Tupelizer_met")
variables = ["weight", "met", "mT", "barepfmet" ,"ht", "btag0", "btag1", "genmet", "metpxUncorr", "metpyUncorr", "m3", "singleMuonic", "singleElectronic", \
  "leptonPt", "leptonEta", "leptonPhi", "leptonPdg", "njets", "jet0pt", "jet1pt", "jet2pt", "jet3pt", "nvetoMuons", "nvetoElectrons", "ngoodMuons", "ngoodElectrons", "ngoodVertices"]
variables.append("antinuMu")
variables.append("antinuE")
variables.append("antinuTau")
variables.append("nuMu")
variables.append("nuE")
variables.append("nuTau")
variables.append("nuMuFromTausFromWs")
variables.append("nuEFromTausFromWs")
variables.append("nuTauFromTausFromWs")

#The method to access the chain
def getVarValue(c, var):
  varNameHisto = var
  leaf = c.GetAlias(varNameHisto)
  if leaf!='':
    return c.GetLeaf(leaf).GetValue()
  else:
    return float('nan')

#Define and compile C struct; do not recompile when changes have been made in a single py session because the import statement will not update the struct
structString = "struct MyStruct{"
for var in variables:
  structString +="Float_t "+var+";"
structString   +="};"
ROOT.gROOT.ProcessLine(structString)
from ROOT import MyStruct
s = MyStruct()

#Did you specify a PU reweighting hist file?
rwHisto = ""
if globals().has_key("reweightingHistoFile"):
  if reweightingHistoFile!="":
    rf = ROOT.TFile(reweightingHistoFile)
    htmp = rf.Get("ngoodVertices_Data")
    ROOT.gDirectory.cd("PyROOT:/")
    rwHisto = htmp.Clone()
    rf.Close()
    print "Using reweightingHisto", reweightingHistoFile, rwHisto

if not os.path.isdir(outputDir):
  os.system("mkdir "+outputDir)
if not os.path.isdir(outputDir+"/"+chmode+"/"):
  os.system("mkdir "+outputDir+"/"+chmode+"/")
if not os.path.isdir("mkdir "+outputDir+"/"+chmode+"/"+mode):
  os.system("mkdir "+outputDir+"/"+chmode+"/"+mode)
else:
  print "Directory", outputDir+"/"+chmode+"/"+mode, "already found"
for sample in allSamples:
  for bin in sample["bins"]:
    os.system("mkdir "+outputDir+"/"+chmode+"/"+mode+"/"+bin)
    #pyROOT copy 
    t = ROOT.TTree( "Events", "Events", 1 ) #Construct the Events TTreefor the target file
    for var in variables:
      t.Branch(var,   ROOT.AddressOf(s,var),var+'/F')
    c = ROOT.TChain(sample["Chain"])
    for thisfile in sample["filenames"][bin]:
      c.Add(thisfile)
    ofile = outputDir+"/"+chmode+"/"+mode+"/"+bin+"/histo_"+bin+"_"+presel+".root"
    if os.path.isfile(ofile):
      print ofile, "already there! Skipping!!!" 
      continue        #Don't overwrite if file is already there but skip! (You might want to remove this line)
    ntot = c.GetEntries()
    if ntot>0:
      usedcommoncf = commoncf
      c.Draw(">>eList", commoncf)
      elist = ROOT.gDirectory.Get("eList")
      number_events = elist.GetN()
      print "Reading: ", sample["name"], bin, "with",number_events,"Events using cut", usedcommoncf
      if small:
        if number_events>200:
          number_events=200
      for i in range(0, number_events):
        if (i%10000 == 0) and i>0 :
          print i
  #      # Update all the Tuples
        if elist.GetN()>0 and ntot>0:
          c.GetEntry(elist.GetEntry(i))
          nvtxWeight = 1.
          if rwHisto!="" and xsec.xsec.has_key(bin):
            nvtxWeight = rwHisto.GetBinContent(rwHisto.FindBin(getVarValue(c, "ngoodVertices")))
          for var in variables[1:]: #exclude "weight" from the list of variables; it is filled below and not from the original chain
            myvar = var
            if chmode=="Iso":   #Here I prepend "isopfRA4Tupelizer_" in case isoMode was set. You can change the logic, of course
              myvar = isoString+"_"+var
            exec("s."+var+"="+str(getVarValue(c, myvar)).replace("nan","float('nan')"))  #Here it happens: We "getVarValue" the variable from the chain, 
                                                                                         #construct a string whose execution writes into the MyStruct instance s. Change only after marvling for 5min.
          s.weight  = sample["weight"][bin]*nvtxWeight  # here we store the weight

          t.Fill() #Fill output ttree 
      del elist
    else:
      print "Zero entries in", bin, sample["name"]
    del c
#    if not small:
    f = ROOT.TFile(ofile, "recreate")   #Write to ofile
    t.Write()
    f.Close()
    print "Written",ofile
#    else:
#      print "No saving when small!"
    del t
