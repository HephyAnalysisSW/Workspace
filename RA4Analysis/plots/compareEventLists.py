from analysisHelpers import *
cData = getRefChain(mode = "Data", dir='/data/schoef/convertedTuples_v18/copyMET/')

mode="Ele"

if mode=="Mu":
  cut = "singleMuonic&&nbtags>=2&&njets>=6&&type1phiMet>150&&ht>500&&((singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)||(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0))"
if mode=="Ele":
  cut = "singleElectronic&&nbtags>=2&&njets>=6&&type1phiMet>150&&ht>500&&((singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)||(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0))"

cData.Draw(">>eList", cut)
eList = ROOT.gDirectory.Get("eList")

myEventList = []
for i in range(eList.GetN()):
  cData.GetEntry(eList.GetEntry(i))
  run = cData.GetLeaf("run").GetValue()
  event = cData.GetLeaf("event").GetValue()
  lumi = cData.GetLeaf("lumi").GetValue()
  myEventList.append([int(run),int(lumi), int(event)])


theirEventList = []
if mode=="Mu":
  fileIN = open("muonlist_noelecs.txt", "r")
if mode=="Ele":
  fileIN = open("eleclist_nomuons.txt", "r")
line = fileIN.readline()
while line:
  ls = line.split(" ")
  theirEventList.append([int(ls[1]), int(ls[2]), int(ls[3])])
  line = fileIN.readline()

for e in theirEventList:
  if not myEventList.count(e):
    print "Not in my list (but in theirs)", e
for e in myEventList:
  if not theirEventList.count(e):
    print "Not in their list (but in mine)", e
