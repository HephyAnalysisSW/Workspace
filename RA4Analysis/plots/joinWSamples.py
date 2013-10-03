import copy
import ROOT
from simplePlotsCommon import *
from math import *
import os, copy, array, xsec, sys
small = False
outputDir = "/data/schoef/convertedTuples_v6/"

mode = "Ele"
#mode = "Mu"
#mode = "HT"
#chmode = "copy"

overwrite = False
npVMean = 7 
#chmode = "higherPU" # + 5% weight per (ngoodpV-npVMean)
#chmode = "lowerPU" # - 5% weight per (ngoodpV-npVMean)

lower_lep_threshold = 20
higher_lep_threshold = 40
#chmode = "higherLowPtLepEff" #increase lep-efficiency linearly starting from 0.8 at lower_lep_threshold to 1 at higher_lep_threshold 
#chmode = "lowerLowPtLepEff" #decrease lep-efficiency linearly starting from 1.2 at lower_lep_threshold to 1 at higher_lep_threshold 

lower_eta_threshold = 1.5
changeWeightBy = 0.05
#chmode = "higherHighEtaLepEff" #increase lep-efficiency by changeWeightBy for |lep_eta|>lower_eta_threshold
#chmode = "lowerHighEtaLepEff" #decrease lep-efficiency by changeWeightBy 

#Bkgs other than Top/W
#chmode = "otherBkgs_1.20"
#chmode = "otherBkgs_1.40"
#chmode = "otherBkgs_0.8"
#chmode = "otherBkgs_0.6"

#B-tag efficiency
#chmode = "btagEff_100_0.8" #increase/decrease weight for bjets above 100 by 0.8 FOR 1ST AND 2ND b-JET!
#chmode = "btagEff_100_1.2"
chmodes = [\
#         "chmode = 'copy3j'", 
         "chmode = 'copyInc'",
#         "chmode = 'copyTotal'",
#         "chmode = 'JES_pfRA4TupelizerJESPlus'",
#         "chmode = 'JES_pfRA4TupelizerJESMinus'", 
#    
#         "chmode = 'otherBkgs_1.50'",
#         "chmode = 'otherBkgs_0.5'",
##         "chmode = 'otherBkgs_1.40'",
##        "chmode = 'otherBkgs_0.6'",
#         "chmode = 'higherPU'",
#         "chmode = 'lowerPU'",
#         "chmode = 'higherHighEtaLepEff'",
#         "chmode = 'lowerHighEtaLepEff'",
#         "chmode = 'higherLowPtLepEff'",
#         "chmode = 'lowerLowPtLepEff'",
#         "chmode = 'btagEff_100_0.9'",
#         "chmode = 'btagEff_100_1.1'",
#         "chmode = 'scaleW_1.32'",
#         "chmode = 'scaleW_0.68'",
#         "chmode = 'scaleT_1.32'",
#         "chmode = 'scaleT_0.68'",
#         "chmode = 'copy10'",
      ]


if len(sys.argv)>1:
  mode = sys.argv[1]
if len(sys.argv)>2:
  chmodes = [chmodes[int(sys.argv[2])]]

print "Going through: ",mode, chmodes

commoncf = "(-1)"
chainstring = "empty"
reweightingHistoFile = "reweightingHisto_Summer2012Private.root"
if mode == "Mu":
  from defaultMu2012Samples import *
  for s in ["WJetsToLNu", "DYtoEE-M20", "DYtoMuMu-M20", "DYtoTauTau-M20"]:    #Adding extra samples
    if mc["bins"].count(s) ==0:
      mc["bins"].append(s)
if mode == "Ele":
  from defaultEle2012Samples import *
  for s in ["WJetsToLNu", "DYtoEE-M20", "DYtoMuMu-M20", "DYtoTauTau-M20"]:    #Adding extra samples
    if mc["bins"].count(s) ==0:
      mc["bins"].append(s)
if mode == "HT":
  from defaultHadSamples import *
  allSamples = [HTdata]
  reweightingHistoFile = ""

#mc["bins"] = ["WJetsToLNu"]
#allSamples = [mc]

for var in allVars:
  var.logy=True
  var.lines = [[0.17,0.963,'#sqrt{s} = 7TeV'], [0.36,0.963,"#font[22]{CMS simulation}"], [0.69, 0.963, str(int(round(targetLumi)))+" pb^{-1}"]]

sample = mc
mc["dirname"] = "/data/trauner/pf_120613/"+mode.replace("Ele", "EG")+"/"
mc["bins"] = ["WJetsToLNu-Summer12", "WJets-HT400-Summer12"]
allSamples = [sample]
sample["filenames"]={}
sample["weight"]={}
if not sample.has_key("bins"):
  sample["bins"]=[""]
for bin in sample["bins"]:
  subdirname = sample["dirname"]+"/"+bin+"/"
  if sample["bins"]==[""]:
    subdirname = sample["dirname"]+"/"
  c = ROOT.TChain("Events")
  d = ROOT.TChain("Runs")
  sample["filenames"][bin]=[]
  if small:
    filelist=os.listdir(subdirname)
    counter = 1   #Joining n files
    maxN = None
    if small:
      maxN = 10
    for file in filelist[:maxN]:
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
    d.Add(file)
#    nevents = c.GetEntries("bool_EventCounter_passed_PAT.obj")
  nevents = 0
  nruns = d.GetEntries()
  for i in range(0, nruns):
    d.GetEntry(i)
    nevents += getValue(d,"uint_EventCounter_runCounts_PAT.obj")

  weight = 1.
  if xsec.xsec.has_key(bin):
    if nevents>0:
      weight = xsec.xsec[bin]*targetLumi/nevents
    else:
      weight = 0.
  print sample["name"], bin, nevents,"weight",weight
  sample["weight"][bin]=weight
  del c
  del d

variables = []
if mode=="Ele" or mode=="Mu":
  variables = ["weight", "isFromHT400", "met", "mT", "barepfmet" ,"ht", "btag0", "btag1", "genmet", "genmetpx","genmetpy","metpxUncorr", "metpyUncorr", "m3", "singleMuonic", "singleElectronic", \
  "leptonPt", "leptonEta", "leptonPhi", "leptonPdg", "njets", "jet0pt", "jet1pt", "jet2pt", "jet3pt", "nvetoMuons", "nvetoElectrons", "ngoodMuons", "ngoodElectrons", "ngoodVertices",
  "antinuMu", "antinuE", "antinuTau", "nuMu", "nuE", "nuTau", "nuMuFromTausFromWs", "nuEFromTausFromWs", "nuTauFromTausFromWs"]

def getVarValue(c, var, sample):
  varNameHisto = var
  leaf = c.GetAlias(varNameHisto)
  if leaf!='':
    return c.GetLeaf(leaf).GetValue()
  else:
    return float('nan')

structString = "struct MyStruct{"
for var in variables:
  structString +="Float_t "+var+";"

structString   +="};"
ROOT.gROOT.ProcessLine(structString)

from ROOT import MyStruct

s = MyStruct()

rwHisto = ""
if globals().has_key("reweightingHistoFile"):
  if reweightingHistoFile!="":
    rf = ROOT.TFile(reweightingHistoFile)
    htmp = rf.Get("ngoodVertices_Data")
    ROOT.gDirectory.cd("PyROOT:/")
    rwHisto = htmp.Clone()
    rf.Close()
    print "Using reweightingHisto", reweightingHistoFile, rwHisto

for m in chmodes:
  commoncf = "-1"
  exec(m)
  print "Mode:", chmode, "for", mode
  presel = "None"
  prefixString = ""
  hadronicCut = "jet2pt>40&&ht>400"
  if chmode[-3:]=="Inc":
    hadronicCut="(1)"
  if chmode[-2:] == "3j":
    hadronicCut = "(jet2pt>40)"
  if mode=="Mu":
    presel = "pf-3j40"
    commoncf = hadronicCut+"&&ngoodMuons>0" 
    if chmode[:3] == "JES" or chmode[:4] == "TCHE":
      prefixString = chmode.split("_")[1]
      commoncf= prefixString+"_jet2pt>40&&"+prefixString+"_ht>400&&"+prefixString+"_ngoodMuons>0"
  if mode=="Ele":
    presel = "pf-3j40"
    commoncf = hadronicCut+"&&ngoodElectrons>0"
    if chmode[:3] == "JES" or chmode[:4] == "TCHE":
      prefixString = chmode.split("_")[1]
      commoncf= prefixString+"_jet2pt>40&&"+prefixString+"_ht>400&&"+prefixString+"_ngoodElectrons>0"
  if mode=="HT":
    presel = "pf-3j40"
    commoncf = "jet2pt>40&&ht>400&&nvetoMuons==0&&nvetoElectrons==0"
    if chmode[:3] == "JES":
      prefixString = chmode[4:]
      commoncf= prefixString+"_jet2pt>40&&"+prefixString+"_ht>300&&"+prefixString+"_nvetoMuons==0&&"+prefixString+"_nvetoElectrons==0"

  if not os.path.isdir(outputDir+"/"+chmode):
    os.system("mkdir "+outputDir+"/"+chmode)
#  os.system("rm -rf "+outputDir+"/"+chmode+"/"+mode)
  if not os.path.isdir("mkdir "+outputDir+"/"+chmode+"/"+mode):
    os.system("mkdir "+outputDir+"/"+chmode+"/"+mode)
  else:
    print "Directory", outputDir+"/"+chmode+"/"+mode, "already found"
  if not os.path.isdir("mkdir "+outputDir+"/"+chmode+"/"+mode+"/WJetsCombined-Summer12"):
    os.system("mkdir "+outputDir+"/"+chmode+"/"+mode+"/WJetsCombined-Summer12")
  else:
    print "Directory", outputDir+"/"+chmode+"/"+mode+"/WJetsCombined-Summer12", "already found"
  ofile = outputDir+"/"+chmode+"/"+mode+"/WJetsCombined-Summer12/histo_WJetsCombined-Summer12_"+presel+".root"
  t = ROOT.TTree( "Events", "Events", 1 )
  for var in variables:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')
  for sample in allSamples:
    for bin in sample["bins"]:
      isFromHT400 = (bin=="WJets-HT300")
#     if bin=="DYtoLL-M50":
      c = ROOT.TChain(sample["Chain"])
      for thisfile in sample["filenames"][bin]:
        c.Add(thisfile)
      if os.path.isfile(ofile) and overwrite:
        print "Warning! will overwrite",ofile
      if os.path.isfile(ofile) and not overwrite:
        print ofile, "already there! Skipping!!!" 
        continue
      ntot = c.GetEntries()
      if ntot>0:
        c.Draw(">>eList", commoncf)
        elist = ROOT.gDirectory.Get("eList")
        number_events = elist.GetN()
        print "Reading: ", sample["name"], bin, "with",number_events,"Events using cut", commoncf
#        if small:
#          if number_events>200:
#            number_events=200
        for i in range(0, number_events):
          if (i%10000 == 0) and i>0 :
            print i
    #      # Update all the Tuples
          if elist.GetN()>0 and ntot>0:
            c.GetEntry(elist.GetEntry(i))
            ht = getVarValue(c, "ht", sample)
            if isFromHT400 and (not ht > 450 ):
#              print isFromHT400, ht ,"-> Continue"
              continue
            if (not isFromHT400) and ht > 450:
              continue
#              print isFromHT400, ht ,"-> Continue"
#            print isFromHT400, ht ,"-> Write!"
            s.isFromHT400 = isFromHT400
            nvtxWeight = 1.
            if rwHisto!="" and xsec.xsec.has_key(bin):
              nvtxWeight = rwHisto.GetBinContent(rwHisto.FindBin(getVarValue(c, "ngoodVertices", sample)))
    #                print "nvtx:", c.GetLeaf( "ngoodVertices" ).GetValue(), "bin", rwHisto.FindBin(c.GetLeaf( "ngoodVertices" ).GetValue()),"weight",nvtxWeight
            for var in variables[1:]:
              getVar = var
              if prefixString!="":
                getVar = prefixString+"_"+var
              exec("s."+var+"="+str(getVarValue(c, getVar, sample)).replace("nan","float('nan')"))
            s.weight  = sample["weight"][bin]*nvtxWeight
            if chmode=="copy10":
              s.weight = s.weight*10
  
            if chmode=="higherPU" or chmode=="lowerPU": #Increase weight by 5% for each good PV
              addW = 0.05* ( s.ngoodVertices - npVMean)
              if chmode=="higherPU":
                s.weight *= 1+addW
              if chmode=="lowerPU":
                s.weight *= max(0., 1-addW)

            if chmode=="lowerLowPtLepEff" or chmode=="higherLowPtLepEff":
              if s.leptonPt>lower_lep_threshold and s.leptonPt<higher_lep_threshold:
                reweight = (higher_lep_threshold - s.leptonPt)/float(higher_lep_threshold - lower_lep_threshold)
                if chmode=="lowerLowPtLepEff":
                  s.weight *= 1. - 0.2*reweight
                if chmode=="higherLowPtLepEff":
                  s.weight *= 1. + 0.2*reweight

            if chmode=="lowerHighEtaLepEff" or chmode=="higherHighEtaLepEff":
              if abs(s.leptonEta)>lower_eta_threshold:
                if chmode=="lowerHighEtaLepEff":
                  s.weight *= 1 - changeWeightBy
                if chmode=="higherHighEtaLepEff":
                  s.weight *= 1 + changeWeightBy

            if chmode[:9] == "otherBkgs":
              if sample["name"] == "MC":
                if bin.count("TTJets")==0 and bin.count("WJets")==0:
                  s.weight *= float(chmode[10:])
            
            if chmode.split("_")[0] == "btagEff":
              if getVarValue(c, "btag0pt", sample)>float(chmode.split("_")[1]):
                s.weight *= float(chmode.split("_")[2])
              if getVarValue(c, "btag1pt", sample)>float(chmode.split("_")[1]):
                s.weight *= float(chmode.split("_")[2])
#            if isFromHT400:
#              s.weight *= 1.13598  #Compensate for lower CS of HT-300 sample (obtained from ratio of HT>450 cut) ## already included!
            if chmode[:5]=="scale":
               fac = float(chmode.split("_")[1])
               if chmode[6]=="W" and sample["name"] == "MC" and bin.count("WJets")==1:
                 s.weight*=fac
#               if chmode[6]=="T" and sample["name"] == "MC" and bin.count("TTJets")==1:
#                 s.weight*=fac

            t.Fill() 
        del elist
      else:
        print "Zero entries in", bin, sample["name"]
      del c
  if not small:
    f = ROOT.TFile(ofile, "recreate")
    t.Write()
    f.Close()
    print "Written",ofile
  else:
    print "No saving when small!"
  del t
