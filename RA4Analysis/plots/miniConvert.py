import copy, pickle
import ROOT
from simplePlotsCommon import *
from math import *
import os, copy, array, xsec, sys, random
from xsecSMS import gluino8TeV_NLONLL
from btagEff import getMCEff, getTagWeightDict, getSF

small = False
overwrite = False

refMGL = 1100
sms = "T1tttt-madgraph"

if sms == "T1tttt":
  outDir = "/data/schoef/convertedTuples_v16/sigCont_"+str(refMGL)
  inDir = "/data/adamwo/convertedTuples_v16/copyMET"
if sms == "T1tttt-madgraph":
  outDir = "/data/schoef/convertedTuples_v19/sigCont_"+str(refMGL)
  inDir = "/data/schoef/convertedTuples_v19/copyMET"
if sms == "T5tttt":
  outDir = "/data/schoef/convertedTuples_v19/sigCont_"+str(refMGL)
  inDir = "/data/schoef/convertedTuples_v19/copyMET"

jobs = []
if sms == "T1tttt":
  for m0 in [400, 500, 600, 700,800,900,1000,1100,1200,1300,1400]:
#  for m0 in [800]:
    m1_list = [float(x) for x in range(0,int(m0)-350+1,50)]
    for m1 in m1_list:
      f = "T1tttt_"+str(int(m0))+"_"+str(int(m1))
      jobs.append([inDir+"/Ele/"+f+"/histo_"+f+".root", outDir+"/Ele/"+f+"/histo_"+f+".root"])
      jobs.append([inDir+"/Mu/"+f+"/histo_"+f+".root", outDir+"/Mu/"+f+"/histo_"+f+".root"])

if sms == "T1tttt-madgraph":
#  for m0 in [400, 500, 600, 700,800,925,1025,1100,1200,1300,1400]:
  for m0 in [775, 825]:
    m1_list = [float(x) for x in range(25,int(m0)-175+1,50)]
    for m1 in m1_list:
      f = "T1tttt-madgraph_"+str(int(m0))+"_"+str(int(m1))
      jobs.append([inDir+"/Ele/"+f+"/histo_"+f+".root", outDir+"/Ele/"+f+"/histo_"+f+".root"])
      jobs.append([inDir+"/Mu/"+f+"/histo_"+f+".root", outDir+"/Mu/"+f+"/histo_"+f+".root"])

if sms == "T5tttt":
  for m0 in [800,900,1000,1100,1200,1300,1400]:
    m1_list = [float(x) for x in range(225,int(m0)-175+1,50)]
    for m1 in m1_list:
      f = "T5tttt_"+str(int(m0))+"_"+str(int(m1))
      jobs.append([inDir+"/Ele/"+f+"/histo_"+f+".root", outDir+"/Ele/"+f+"/histo_"+f+".root"])
      jobs.append([inDir+"/Mu/"+f+"/histo_"+f+".root", outDir+"/Mu/"+f+"/histo_"+f+".root"])

#filelist=os.listdir(inDir+"/Mu")
#for f in filelist:
#  jobs.append([inDir+"/Mu/"+f+"/histo_"+f+".root", outDir+"/Mu/"+f+"/histo_"+f+".root"])
#
#filelist=os.listdir(inDir+"/Ele")
#for f in filelist:
#  jobs.append([inDir+"/Ele/"+f+"/histo_"+f+".root", outDir+"/Ele/"+f+"/histo_"+f+".root"])
 

def getVarValue(c, var, n=0):
  return c.GetLeaf(var).GetValue(n)

variables = ["weight",  "xsec", "weightLumi",  "type1phiMet", "ht", "btag0", "btag1", "btag2", "btag3", "singleMuonic", "singleElectronic", \
  "leptonPt", "leptonEta", "leptonPhi", "leptonPdg", "njets", "nbtags", "nbjets", "jet0pt", "jet1pt", "jet2pt", "jet3pt", "nvetoMuons", "nvetoElectrons", "ngoodMuons", "ngoodElectrons", "osetMgl", "osetMN", "genmet"]
#extraVariables = ["sigContWeight"]
extraVariables = []

structString = "struct MyStruct{"
for var in variables:
  structString +="Float_t "+var+";"
for var in extraVariables:
  structString +="Float_t "+var+";"
structString   +="};"
ROOT.gROOT.ProcessLine(structString)
print structString
exec("from ROOT import MyStruct")
exec("s = MyStruct()")

for ifile, ofile in jobs:
  print "Mini-converting",ifile,"to",ofile
  t = ROOT.TTree( "Events", "Events", 1 )
  for var in variables+extraVariables:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')
  os.system('mkdir -p '+ofile.split("histo_")[0])
  if os.path.isfile(ofile) and overwrite:
    print "Warning! will overwrite",ofile
  if os.path.isfile(ofile) and not overwrite:
    print ofile, "already there! Skipping!!!" 
    continue
  mgl=int(ofile.split("histo_")[1].split("_")[1])
#  if mgl<=1100:
  weightScaleFac = gluino8TeV_NLONLL[refMGL]/gluino8TeV_NLONLL[mgl]
#  else:
#    weightScaleFac = 1
  print "Scaling down weight by", weightScaleFac
  c = ROOT.TChain("Events")
  c.Add(ifile)
  ntot = c.GetEntries()
  for i in range(0, ntot):
    if not i%5000:
      print i
    c.GetEntry(i)
    for var in variables:
      exec("s."+var+"="+str(getVarValue(c, var)).replace("nan","float('nan')"))
    s.weight = s.weight*weightScaleFac
    t.Fill()
  del c
  if not small:
    f = ROOT.TFile(ofile, "recreate")
    t.Write()
    f.Close()
    print "Written",ofile
  else:
    print "No saving when small!"
  del t
