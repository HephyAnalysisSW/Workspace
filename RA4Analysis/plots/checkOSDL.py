import ROOT

emu = ROOT.TChain("Events")
emu.Add("/data/schoef/convertedTuples_v11/OSDL_eleMu/highMET/eleMuData/histo_eleMuData.root")
emu.SetScanField(1000)

emuFull = ROOT.TChain("Events")
#emuFull.Add("/data/schoef/pat_120905/data8TeV/MuEG-Run2012A-13Jul2012/histo_*.root")
emuFull.Add("/data/schoef/pat_120905/data8TeV/MuEG-Run2012B-13Jul2012/histo_*.root")
#
mumu = ROOT.TChain("Events")
mumu.Add("/data/schoef/convertedTuples_v11/OSDL_doubleMu/highMET/doubleMuData/histo_doubleMuData.root")
mumu.SetScanField(1000)

mumuFull = ROOT.TChain("Events")
mumuFull.Add("/data/schoef/pat_120908/data8TeV/DoubleMu-Run2012B-13Jul2012/histo_136_0_wrs.root")
mumuFull.SetScanField(1000)

mumuRun2012BOSDL = ROOT.TChain("Events")
mumuRun2012BOSDL.Add("../crab/pickEvents/mumu/histo.root")
#mumuRun2012BOSDL.Scan ("event:run:lumi:mLL:njets:ht","njets>=2&&ht>100","@colsize=12")

for i in range(mumuRun2012BOSDL.GetEntries()):
  mumuRun2012BOSDL.GetEntry(i)
  nmuons = getVarValue(mumuRun2012BOSDL, "nmuons")
  allGoodLeptons =  getGoodMuons(mumuRun2012BOSDL, nmuons, "OSDL")
#  if len(allGoodLeptons) >=2 and (allGoodLeptons[1]["pt"]>10.) and abs(allGoodLeptons[0]["pdg"] + allGoodLeptons[1]["pdg"]) <= 2:
#    if (abs(allGoodLeptons[0]["pdg"])==13 and abs(allGoodLeptons[1]["pdg"])==13): 
#      continue
  if not checkLumi(getVarValue(mumuRun2012BOSDL, "run"), getVarValue(mumuRun2012BOSDL, "lumi")):
    print i,getVarValue(mumuRun2012BOSDL, "event"), allGoodLeptons
  

mumuRun2012BOSDLConverted = ROOT.TChain("Events")
mumuRun2012BOSDLConverted.Add("/data/schoef/debugOSDL//OSDL_doubleMu/highMET/doubleMuData/histo_doubleMuData.root")


mumuFull = ROOT.TChain("Events")
mumuFull.Add("/data/schoef/pat_120905/data8TeV/DoubleMu-Run2012A-13Jul2012/h*.root")
mumuFull.Add("/data/schoef/pat_120905/data8TeV/DoubleMu-Run2012B-13Jul2012/h*.root")
mumuFull.SetScanField(1000)

#
#ee = ROOT.TChain("Events")
#ee.Add("/data/schoef/convertedTuples_v11/OSDL_doubleEle/highMET/doubleEleData/histo_doubleEleData.root")
#ee.SetScanField(1000)
#
#n_ee = ee.GetEntries    ("jet1pt>40&&ht>100&&met>150&&mLL>20&&mLL<70&&deltaRLL>0.3&&run<=196531")
#n_mumu = mumu.GetEntries("jet1pt>40&&ht>100&&met>150&&mLL>20&&mLL<70&&deltaRLL>0.3&&run<=196531")
#n_emu = emu.GetEntries  ("jet1pt>40&&ht>100&&met>150&&mLL>20&&mLL<70&&deltaRLL>0.3&&run<=196531")
#
#print "Me:   ",n_ee, n_mumu, n_emu
#print "Them: ",90, 156, 194
##ee.Scan ("event:run:lumi:deltaRLL","ht>100&&jet1pt>40&&met>150&&ptZ>0.&&mLL>20&&mLL<70&&deltaRLL>0.3&&run<=196531","@colsize=12")
##emu.Scan("event:run:lumi:deltaRLL","ht>100&&jet1pt>40&&met>150&&ptZ>0.&&mLL>20&&mLL<70&&deltaRLL>0.3&&run<=196531","@colsize=12")

fileIN = open("myMuMu.txt", "r")
line = fileIN.readline()
myEvents = []
while line:
  l =  line.replace(" ","").replace("\n","").split("*")
  if len(l)==3:
    myEvents.append([int(l[1]), int(l[2]), int(l[0])])
  line = fileIN.readline()

#fileIN = open("20120914-OSEdgeEvents5fbi/emuHighMETEdge.txt", "r")
fileIN = open("20120914-OSEdgeEvents5fbi/mumuHighMETEdge.txt", "r")
#fileIN = open("20120914-OSEdgeEvents5fbi/eeHighMETEdge.txt", "r")
line = fileIN.readline()
theirEvents = []
while line:
  l =  line.replace(" ","").replace("\n","").split(":")
  if len(l)==3 and int(l[0])>193621:
    theirEvents.append([int(l[0]), int(l[1]), int(l[2])])
  line = fileIN.readline()

mineButNotTheirs = []
theirsButNotMine = []

for i in theirEvents:
  if i not in myEvents:
#    print "Why don't I have", i
    theirsButNotMine.append(i)
for i in myEvents:
  if i not in theirEvents:
#    print "Why don't they have",i
    mineButNotTheirs.append(i)

def getStr(i):
  return "run=="+str(i[0])+"&&lumi=="+str(i[1])+"&&event=="+str(i[2])

#emuRun2012BOSDL = ROOT.TChain("Events")
#emuRun2012BOSDL.Add("../crab/pickEvents/emu/histo_Trigger.root")
#for i in theirsButNotMine:
#  if i[0]>193800:
#    print i, emuRun2012BOSDL.GetEntries(getStr(i))

#tbc =[
#  [193998, 108, 81816276],
#  [194151, 315, 305327569],
#  [194533, 136, 175465801],
#  [194533, 795, 978835608],
#  [194643, 16, 20707405],
#  [194789, 433, 544239341],
#  [195113, 413, 499198531],
#  [195304, 1030, 1124741752],
#  [195915, 45, 83571779],
#  [195398, 1137, 922209276],
#  [195551, 99, 40305441],
#  [195649, 84, 127962190]
#  ]
#
#for i in tbc:
#  print i, getStr(i)
#  emuRun2012BOSDL.Scan("event:run:lumi:njets:met:ht:muonsPt:muonsEta:muonsisPF:muonsisGlobal:muonsPFRelIso:muonsNormChi2:muonsNValMuonHits:muonsNumMatchedStadions:muonsPixelHits:muonsNumtrackerLayerWithMeasurement:muonsDxy:muonsDz", getStr(i))
#  emuRun2012BOSDL.Scan("event:run:lumi:njets:met:ht:elesPt:elesEta:elesOneOverEMinusOneOverP:elesPfRelIso:elesSigmaIEtaIEta:elesHoE:elesDPhi:elesDEta:elesMissingHits:elesDxy:elesDz:elesPassConversionRejection", getStr(i))

#from simplePlotsCommon import *
#from convertDiLep import goodEleID
#c = ROOT.TChain("Events")
#c.Add("../crab/pickEvents/histo_Trigger.root")
#c.Scan("event","event==20707405")
#c.GetEntry(83)

mumuRun2012BOSDL = ROOT.TChain("Events")
mumuRun2012BOSDL.Add("../crab/pickEvents/mumu/histo.root")
#emuRun2012BOSDLConvert = ROOT.TChain("Events")
#emuRun2012BOSDLConvert.Add("/data/schoef/debugOSDL/OSDL_eleMu/highMET/eleMuData/histo_eleMuData.root")
mumuRun2012BOSDLConvert = ROOT.TChain("Events")
mumuRun2012BOSDLConvert.Add("/data/schoef/debugOSDL//OSDL_doubleMu/highMET/doubleMuData/histo_doubleMuData.root")

