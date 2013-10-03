import copy
import ROOT
from simplePlotsCommon import *
from ConvertTupels_fcn import *
from math import *
import os, copy, array, xsec, sys, random
small = False
outputDir = "/data/schoef/convertedTuples_v6/"
import pickle
#from msugraCount import msugraCount
targetLumi = 4700.
#mode = "Ele"
mode = "Mu"

xsecLODict =  pickle.load(file('goodModelNames_10_0_1.pkl'))

def xsecLO(m0, m12):
  if xsecLODict.has_key((m0, m12, 10,0,1)):
    return xsecLODict[(m0, m12, 10, 0, 1)]
  else:
    return float('nan')


from processStatistics import productionCode

overwrite = False
npVMean = 7 

lower_lep_threshold = 20
higher_lep_threshold = 40

lower_eta_threshold = 1.5
changeWeightBy = 0.05

rep_max = 30

chmodes = [\
       "chmode = 'copy'",
      ]

if len(sys.argv)>1:
  mode = sys.argv[1]
if len(sys.argv)>2:
  chmodes = [chmodes[int(sys.argv[2])]]

print "Going through: ",mode, chmodes

commoncf = "(-1)"
chainstring = "empty"
reweightingHistoFile = "reweightingHisto_Summer2011.root"

msugra={} 
msugra["name"]     = "mc";
msugra["dirname"] = "/data/schoef/pat_120121/"+mode.replace("Ele","EG")+"/msugra/"
msugra["specialCuts"] = []
msugra["Chain"] = "Events"

btags=["btag0", "btag1", "btag2", "btag3"]

variables = []
if mode=="Ele" or mode=="Mu":
  variables = ["weight", "met", "mT", "barepfmet" ,"ht", "btag0", "btag1", "btag2", "btag3", "genmet", "genmetpx","genmetpy","metpxUncorr", "metpyUncorr", "m3", "singleMuonic", "singleElectronic", \
  "leptonPt", "leptonEta", "leptonPhi", "leptonPdg", "njets","nbtags", "jet0pt", "jet1pt", "jet2pt", "jet3pt", "nvetoMuons", "nvetoElectrons", "ngoodMuons", "ngoodElectrons", "ngoodVertices",
  "btag0pt", "btag1pt", "btag2pt", "btag3pt", "btag0eta", "btag1eta", "btag2eta", "btag3eta",
  "btag0parton", "btag1parton", "btag2parton", "btag3parton",
  "antinuMu", "antinuE", "antinuTau", "nuMu", "nuE", "nuTau", "nuMuFromTausFromWs", "nuEFromTausFromWs", "nuTauFromTausFromWs", "msugraM0", "msugraM12"]

def getVarValue(c, var):
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
  hadronicCut = "jet2pt>40&&ht>300"
  if chmode[-3:]=="Inc":
    hadronicCut="(1)"
  if chmode[-2:] == "3j":
    hadronicCut = "(jet2pt>40)"
  if mode=="Mu":
    presel = "pf-3j40"
    commoncf = hadronicCut+"&&ngoodMuons>0"
  if mode=="Ele":
    presel = "pf-3j40"
    commoncf = hadronicCut+"&&ngoodElectrons>0"
  if chmode[-5:] == "Total":
    commoncf = "(1)"
  if not os.path.isdir(outputDir+"/"+chmode):
    os.system("mkdir "+outputDir+"/"+chmode)
  if chmode.split("_")[0]=="JER":
    from nsz_formula import *
#  os.system("rm -rf "+outputDir+"/"+chmode+"/"+mode)
  if not os.path.isdir("mkdir "+outputDir+"/"+chmode+"/"+mode):
    os.system("mkdir "+outputDir+"/"+chmode+"/"+mode)
  else:
    print "Directory", outputDir+"/"+chmode+"/"+mode, "already found"
  os.system("mkdir "+outputDir+"/"+chmode+"/"+mode+"/msugra")

  c = ROOT.TChain(msugra["Chain"])
  if small:
    c.Add(msugra["dirname"]+"/histo_100_*.root")
  else:
    c.Add(msugra["dirname"]+"/histo_*.root")
  ntot = c.GetEntries()
  m0Range = (20,1920,20)
  m12Range = (100,780,20)
  if small:
    m0Range = (1080,1100,20)
    m12Range = (500,520,20)
  for m0 in range(*m0Range):
    for m12 in range(*m12Range):

      sstring = getMSUGRAShortString(m0, m12, 10, 0, 1)
      ofile = outputDir+"/"+chmode+"/"+mode+"/msugra/histo_"+sstring+".root"
      if os.path.isfile(ofile) and overwrite:
        print "Warning! will overwrite",ofile
      if os.path.isfile(ofile) and not overwrite:
        print ofile, "already there! Skipping!!!" 
        continue
      t = ROOT.TTree( "Events", "Events", 1 )
      for var in variables:
        t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')
      if ntot>0:
        c.Draw(">>eList", commoncf+"&&msugraM0=="+str(m0)+"&&msugraM12=="+str(m12))
        elist = ROOT.gDirectory.Get("eList")
        number_events = elist.GetN()
        print "Reading: ",number_events,"events for m12",m12,"and m0", m0, " and using cut", commoncf
        if small:
          if number_events>10:
            number_events=10
        for i in range(0, number_events):
          if (i%10000 == 0) and i>0 :
            print i
    #      # Update all the Tuples
          if elist.GetN()>0 and ntot>0:
            c.GetEntry(elist.GetEntry(i))
#            ileaf = c.GetLeaf("ints_pfRA4Tupelizer_sparticles_PAT.obj")
#            pcode = productionCode([int(ileaf.GetValue(0)), int(ileaf.GetValue(1))])
            nvtxWeight = 1.
    #        if rwHisto!="":
    #          nvtxWeight = rwHisto.GetBinContent(rwHisto.FindBin(getVarValue(c, "ngoodVertices")))
    #          print "nvtx:", c.GetLeaf( "ngoodVertices" ).GetValue(), "bin", rwHisto.FindBin(c.GetLeaf( "ngoodVertices" ).GetValue()),"weight",nvtxWeight
            for var in variables[1:]:
              getVar = var
              if prefixString!="":
                getVar = prefixString+"_"+var
              exec("s."+var+"="+str(getVarValue(c, getVar)).replace("nan","float('nan')"))
            s.weight  = nvtxWeight*targetLumi*xsecLO(m0, m12)/float(10000.)
#            print sstring, "M0",s.msugraM0,"M12",s.msugraM12,"weight",s.weight
            t.Fill() 
        del elist
      if not small:
        f = ROOT.TFile(ofile, "recreate")
        t.Write()
        f.Close()
        print "Written",ofile
      else:
        print "No saving when small!"
      del t
#  else:
#    print "Zero entries found." 
#  del c
#  if not small:
#    f = ROOT.TFile(ofile, "recreate")
#    t.Write()
#    f.Close()
#    print "Written",ofile
#  else:
#    print "No saving when small!"
#  del t
