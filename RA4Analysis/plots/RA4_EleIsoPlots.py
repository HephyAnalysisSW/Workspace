import ROOT
from array import array
from math import *
import os, copy, random
from simpleStatTools import *
from simplePlotsCommon import *
import xsec
small = False
frac = 0.05

if not globals().has_key("dataLoaded"):
  global dataLoaded
  dataLoaded=False
#if loadData:

from defaultEleSamples import *

var1 = "kinMetSig"
var2 = "ht"

presel = "pf-4j30"
subdir = "tmp/"

chainstring = "isopfRA4Analyzer/Events"
commoncf = "jet3pt>30&&singleMuonic&&lepton_pt>15&&ht>200"

for sample in allSamples:
  sample["Chain"] = chainstring

usedSamples = [mc]
prefix = "Ele_ewk+qcd_"

#usedSamples = [qcd]
#prefix = "Ele_qcd_"

for sample in usedSamples:
  sample["Chain"] = chainstring
 
if dataLoaded:
  print "Data already loaded"
if not dataLoaded:
  dataLoaded=True
  Events = {}
  for sample in usedSamples:
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
  for sample in usedSamples:
    Events[sample["name"]] = {}
    for bin in sample["bins"]:
      Events[sample["name"]][bin] = []
      c = ROOT.TChain(sample["Chain"])
      for thisfile in sample["filenames"][bin]:
        c.Add(thisfile)
      c.GetEntries()
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
#          Event["var1"] = var1val
#          Event["var2"] = var2val
#          for nj in range(4):
#            jname = "jet"+str(nj)
#            Event[jname] = {}
#            Event[jname]["phi"] = c.GetLeaf( jname+"phi" ).GetValue()
#            Event[jname]["eta"] = c.GetLeaf( jname+"eta" ).GetValue()
#            Event[jname]["pt"] = c.GetLeaf( jname+"pt" ).GetValue()
##            print jname,"pt",Event[jname]["pt"] , "eta", Event[jname]["eta"], "phi" , Event[jname]["phi"]
          Event["relIso"]   = c.GetLeaf( "lepton_relIso" ).GetValue()
          Event["met"]    = c.GetLeaf( "met" ).GetValue()
          Event["kinMetSig"]    = c.GetLeaf( "kinMetSig" ).GetValue()
          Events[sample["name"]][bin].append(Event)
      del elist
      del c

relIsoEffMu_met0  = variable("relIsoEff:ht2;Muon relative Iso cut; Number of Events",[50,0,1] )
relIsoEffMu_met20 = variable("relIsoEff:ht2;Muon relative Iso cut; Number of Events",[50,0,1] )
relIsoEffMu_met30 = variable("relIsoEff:ht2;Muon relative Iso cut; Number of Events",[50,0,1] )

relIsoEffMu_kinMetSig0   = variable("relIsoEff:ht2;Muon relative Iso cut; Number of Events",[50,0,1])
relIsoEffMu_kinMetSig05  = variable("relIsoEff:ht2;Muon relative Iso cut; Number of Events",[50,0,1])
relIsoEffMu_kinMetSig10  = variable("relIsoEff:ht2;Muon relative Iso cut; Number of Events",[50,0,1])

relIsoEffMu_skinMetSig05   = variable("relIsoEff:ht2;Muon relative Iso cut; Number of Events",[50,0,1])
relIsoEffMu_skinMetSig15  = variable("relIsoEff:ht2;Muon relative Iso cut; Number of Events",[50,0,1])
relIsoEffMu_skinMetSig25  = variable("relIsoEff:ht2;Muon relative Iso cut; Number of Events",[50,0,1])

kinMetSig_Mu_relIso05 = variable("kMs:ht2;kinMetSig; Number of Events",[20,0,5])
kinMetSig_Mu_relIso10 = variable("kMs:ht2;kinMetSig; Number of Events",[20,0,5])
kinMetSig_Mu_relIso15 = variable("kMs:ht2;kinMetSig; Number of Events",[20,0,5])

#kinMetSig_Mu_0relIso05 = variable("kMs:ht2;kinMetSig; Number of Events",[20,0,5])
kinMetSig_Mu_0relIso10 = variable("kMs:ht2;kinMetSig; Number of Events",[20,0,5])
kinMetSig_Mu_10relIso15 = variable("kMs:ht2;kinMetSig; Number of Events",[20,0,5])
kinMetSig_Mu_15relIso   = variable("kMs:ht2;kinMetSig; Number of Events",[20,0,5])

for sample in usedSamples:
  for bin in sample["bins"]:
    for event in Events[sample["name"]][bin]:
      if event["met"]>0:
        relIsoEffMu_met0. data_histo.Fill(event["relIso"], sample["weight"][bin])
      if event["met"]>20:
        relIsoEffMu_met20.data_histo.Fill(event["relIso"], sample["weight"][bin])
      if event["met"]>30:
        relIsoEffMu_met30.data_histo.Fill(event["relIso"], sample["weight"][bin])

      if event["kinMetSig"]>0:
        relIsoEffMu_kinMetSig0. data_histo.Fill(event["relIso"], sample["weight"][bin])
      if event["kinMetSig"]>0.5:
        relIsoEffMu_kinMetSig05.data_histo.Fill(event["relIso"], sample["weight"][bin])
      if event["kinMetSig"]>1.0:
        relIsoEffMu_kinMetSig10.data_histo.Fill(event["relIso"], sample["weight"][bin])

      if event["kinMetSig"]<0.5:
        relIsoEffMu_skinMetSig05. data_histo.Fill(event["relIso"], sample["weight"][bin])
      if event["kinMetSig"]<1.5:
        relIsoEffMu_skinMetSig15.data_histo.Fill(event["relIso"], sample["weight"][bin])
      if event["kinMetSig"]<2.5:
        relIsoEffMu_skinMetSig25.data_histo.Fill(event["relIso"], sample["weight"][bin])

      if event["relIso"]>0.05:
        kinMetSig_Mu_relIso05.data_histo.Fill(event["kinMetSig"], sample["weight"][bin]) 
      if event["relIso"]>0.10:
        kinMetSig_Mu_relIso10.data_histo.Fill(event["kinMetSig"], sample["weight"][bin])
      if event["relIso"]>0.15:
        kinMetSig_Mu_relIso15.data_histo.Fill(event["kinMetSig"], sample["weight"][bin])

      if 0<event["relIso"] and event["relIso"]<0.10:
        kinMetSig_Mu_0relIso10.data_histo.Fill(event["kinMetSig"], sample["weight"][bin]) 
      if 0.10<event["relIso"] and event["relIso"]<0.15:
        kinMetSig_Mu_10relIso15.data_histo.Fill(event["kinMetSig"],sample["weight"][bin]) 
      if 0.15<event["relIso"]:
        kinMetSig_Mu_15relIso.data_histo.Fill(event["kinMetSig"]  ,sample["weight"][bin]) 

relIsoEffMu_met0.logy=True
relIsoEffMu_met0.color=ROOT.kBlue
relIsoEffMu_met20.color=ROOT.kRed
relIsoEffMu_met30.color=ROOT.kBlack
relIsoEffMu_met0 .legendText = "MET>0"
relIsoEffMu_met20.legendText = "MET>20"
relIsoEffMu_met30.legendText = "MET>30"
relIsoStack_met = [ relIsoEffMu_met0, relIsoEffMu_met20, relIsoEffMu_met30 ]
getLinesForStack(relIsoStack_met)
drawNMStacks(1,1,[relIsoStack_met],             "pngTMP/"+prefix+"iso_met.png", True)

relIsoEffMu_skinMetSig05.logy=True
relIsoEffMu_skinMetSig05.color=ROOT.kBlue
relIsoEffMu_skinMetSig15.color=ROOT.kRed
relIsoEffMu_skinMetSig25.color=ROOT.kBlack
relIsoEffMu_skinMetSig05 .legendText = "kinMetSig<0.5"
relIsoEffMu_skinMetSig15.legendText = "kinMetSig<1.5"
relIsoEffMu_skinMetSig25.legendText = "kinMetSig<2.5"
relIsoStack_skinMetSig = [ relIsoEffMu_skinMetSig05, relIsoEffMu_skinMetSig15, relIsoEffMu_skinMetSig25 ]
getLinesForStack(relIsoStack_skinMetSig)
drawNMStacks(1,1,[relIsoStack_skinMetSig],             "pngTMP/"+prefix+"iso_small-kinMetSig.png", True)

relIsoEffMu_kinMetSig0.logy=True
relIsoEffMu_kinMetSig0.color=ROOT.kBlue
relIsoEffMu_kinMetSig05.color=ROOT.kRed
relIsoEffMu_kinMetSig10.color=ROOT.kBlack
relIsoEffMu_kinMetSig0 .legendText = "kinMetSig>0"
relIsoEffMu_kinMetSig05.legendText = "kinMetSig>0.5"
relIsoEffMu_kinMetSig10.legendText = "kinMetSig>1.0"
relIsoStack_kinMetSig = [ relIsoEffMu_kinMetSig0, relIsoEffMu_kinMetSig05, relIsoEffMu_kinMetSig10 ]
getLinesForStack(relIsoStack_kinMetSig)
drawNMStacks(1,1,[relIsoStack_kinMetSig],             "pngTMP/"+prefix+"iso_kinMetSig.png", True)

kinMetSig_Mu_relIso05.logy=True
kinMetSig_Mu_relIso05.color=ROOT.kBlue
kinMetSig_Mu_relIso10.color=ROOT.kRed
kinMetSig_Mu_relIso15.color=ROOT.kBlack
kinMetSig_Mu_relIso05.legendText = "relIso>0.05"
kinMetSig_Mu_relIso10.legendText = "relIso>0.10"
kinMetSig_Mu_relIso15.legendText = "relIso>0.15"
kinMetSig_Mu_relIso_stack = [ kinMetSig_Mu_relIso05, kinMetSig_Mu_relIso10, kinMetSig_Mu_relIso15 ]
getLinesForStack(kinMetSig_Mu_relIso_stack)
drawNMStacks(1,1,[kinMetSig_Mu_relIso_stack],             "pngTMP/"+prefix+"iso_met_in_relIso.png", True)

kinMetSig_Mu_0relIso10.color=ROOT.kRed
kinMetSig_Mu_10relIso15.color=ROOT.kBlack
kinMetSig_Mu_15relIso.color=ROOT.kGreen
kinMetSig_Mu_0relIso10.legendText = "0<relIso<0.10"
kinMetSig_Mu_10relIso15.legendText = "0.10<relIso<0.15"
kinMetSig_Mu_15relIso.legendText = "0.15<relIso"
kinMetSig_Mu_relIso_stack_binned = [ kinMetSig_Mu_0relIso10, kinMetSig_Mu_10relIso15 , kinMetSig_Mu_15relIso]
getLinesForStack(kinMetSig_Mu_relIso_stack_binned)
drawNMStacks(1,1,[kinMetSig_Mu_relIso_stack_binned],             "pngTMP/"+prefix+"iso_met_in_relIso_binned.png", True)

def getEstimation(vetosamplestrings=[]):
  smallkMs_smallRelIso = 0.
  smallkMs = 0.
  largerelIso_largekMs = 0.
  largerelIso = 0.
  eventsAfterPreselection = 0.
  trueQCDEvents = 0.
  sstring = ""
  vstring = ""
  for sample in usedSamples:
    for bin in sample["bins"]:
      dropthis=False
      for vs in vetosamplestrings:
        if bin.count(vs)>0:
          dropthis = True
      if dropthis:
        vstring+=bin+" " #Skip this sample
        continue
      sstring +=bin+" " 
      for event in Events[sample["name"]][bin]:
        eventsAfterPreselection += sample["weight"][bin]
        if event["kinMetSig"]<0.5:
          if event["relIso"]<0.1:
            smallkMs_smallRelIso += sample["weight"][bin]
          smallkMs += sample["weight"][bin]
        if event["relIso"]>0.15:
          if event["kinMetSig"]>2.5:
            largerelIso_largekMs += sample["weight"][bin]
          largerelIso += sample["weight"][bin]
  print "Considering: ", sstring
  print "Dropping   : ", vstring
  sstring = ""
  for sample in usedSamples:
    for bin in sample["bins"]:
      if bin.count("QCD")>0:
        sstring +=bin+" " 
        for event in Events[sample["name"]][bin]:
          if event["relIso"]<0.1:
            if event["kinMetSig"]>2.5:
              trueQCDEvents += sample["weight"][bin]
  print "Considering true QCD", sstring
  print "smallkMs_smallRelIso/smallkMs",smallkMs_smallRelIso/smallkMs,  "largeRelIso_largekMs/largerelIso", largerelIso_largekMs/largerelIso
  ratio= smallkMs_smallRelIso/smallkMs*largerelIso_largekMs/largerelIso
  print "ratio",ratio, "Events", ratio*eventsAfterPreselection, "true", trueQCDEvents


#def getEstimation(): 
#  smallkMs_smallRelIso = 0.
#  smallkMs = 0.
#  largerelIso_largekMs = 0.
#  largerelIso = 0.
#  eventsAfterPreselection = 0.
#  trueQCDEvents = 0.
#  sstring = ""
#  for sample in usedSamples:
#    for bin in sample["bins"]:
#      sstring +=bin+" " 
#      for event in Events[sample["name"]][bin]:
#        eventsAfterPreselection += sample["weight"][bin]
#        if event["kinMetSig"]<0.5:
#          if event["relIso"]<0.1:
#            smallkMs_smallRelIso += sample["weight"][bin]
#          smallkMs += sample["weight"][bin]
#        if event["relIso"]>0.15:
#          if event["kinMetSig"]>2.5:
#            largerelIso_largekMs += sample["weight"][bin]
#          largerelIso += sample["weight"][bin]
#  print "Considering: ", sstring
#  sstring = ""
#  for sample in usedSamples:
#    for bin in sample["bins"]:
#      if bin.count("QCD")>0:
#        sstring +=bin+" " 
#        for event in Events[sample["name"]][bin]:
#          if event["relIso"]<0.1:
#            if event["kinMetSig"]>2.5:
#              trueQCDEvents += sample["weight"][bin]
#  print "Considering true QCD", sstring
#  print "smallkMs_smallRelIso/smallkMs",smallkMs_smallRelIso/smallkMs,  "largeRelIso_largekMs/largerelIso", largerelIso_largekMs/largerelIso
#  ratio= smallkMs_smallRelIso/smallkMs*largerelIso_largekMs/largerelIso
#  print "ratio",ratio, "Events", ratio*eventsAfterPreselection, "true", trueQCDEvents
#
