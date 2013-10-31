import ROOT
from simplePlotsCommon import *
from simpleStatTools import niceNum
from math import *

ROOT.tdrStyle.SetPadRightMargin(0.16)
ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)


small = False
c = {}
c["Mu"] = ROOT.TChain("Events")
if small:
  c["Mu"].Add("/data/schoef/pat_120121/Mu/TTJets/histo_80_*.root")
else:
  c["Mu"].Add("/data/schoef/pat_120121/Mu/TTJets/histo*.root")
c["Ele"] = ROOT.TChain("Events")
if small:
  c["Ele"].Add("/data/schoef/pat_120121/EG/TTJets/histo_8_*.root")
else:
  c["Ele"].Add("/data/schoef/pat_120121/EG/TTJets/histo*.root")
#modes = ["Mu", "Ele"]
modes = ["Mu"]



print "Constructing 2nu->1nu HT and MET maps"
constr_commoncf={}
##def
constr_commoncf["Mu"]  = "jet0pt>40&&nvetoMuons+nvetoElectrons>1&&nuMu+antinuMu+nuE+antinuE==2&&nuMu+antinuMu>=1" #use 2l events whose 1l counterpart fits selection
constr_commoncf["Ele"] = "jet0pt>40&&nvetoElectrons>1&&nuE+antinuE==2"
#constr_commoncf["Mu"]  = "nvetoMuons+nvetoElectrons>1&&nuMu+antinuMu+nuE+antinuE==2&&nuMu+antinuMu>=1" 
#constr_commoncf["Ele"] = "nvetoElectrons>1&&nuE+antinuE==2"

twoToOne = {}
for ht in range(0,2000,100):
  twoToOne[ht] = {}
  for met in range(0,1000,50):
    twoToOne[ht][met] = ROOT.TH2F("twoToOne_"+str(ht)+"_"+str(met), "twoToOne_"+str(ht)+"_"+str(met), 20,0,1000, 20,0,2000)
    twoToOne[ht][met].GetXaxis().SetTitle("#slash{E}_{T} (GeV)")
    twoToOne[ht][met].GetYaxis().SetTitle("H_{T} (GeV)")

for mode in modes:
  print "At",mode
  ntot = c[mode].GetEntries()
  c[mode].Draw(">>eList", constr_commoncf[mode])
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  print "nevents:", number_events
  if small:
    if number_events>200:
      number_events=200
  for i in range(0, number_events):
    if (i%10000 == 0) and i>0 :
      print i
#      # Update all the Tuples
    if elist.GetN()>0 and ntot>0:
      c[mode].GetEntry(elist.GetEntry(i))
      metx = getValue(c[mode],"metpxUncorr")
      mety = getValue(c[mode],"metpyUncorr")
      met = getValue(c[mode],"barepfmet")
      nu0Pt = getValue(c[mode],"nu0Pt")
      nu1Pt = getValue(c[mode],"nu1Pt")
      nu0Phi = getValue(c[mode],"nu0Phi")
      nu1Phi = getValue(c[mode],"nu1Phi")
      oneNuMet0 = sqrt( ( - nu0Pt*cos(nu0Phi) + metx)**2 +\
                        ( - nu0Pt*sin(nu0Phi) + mety)**2)
      oneNuMet1 = sqrt( ( - nu1Pt*cos(nu1Phi) + metx)**2 +\
                        ( - nu1Pt*sin(nu1Phi) + mety)**2)
#      metCalc = sqrt ( ( getValue(c[mode],"nu0Pt")*cos(getValue(c[mode],"nu0Phi")) + getValue(c[mode],"nu1Pt")*cos(getValue(c[mode],"nu1Phi")))**2  + \
#                       ( getValue(c[mode],"nu0Pt")*sin(getValue(c[mode],"nu0Phi")) + getValue(c[mode],"nu1Pt")*sin(getValue(c[mode],"nu1Phi")))**2 )
      ht = getValue(c[mode],"ht")
      htCorr0 = ht + nu0Pt + getValue(c[mode],"l0Pt")
      htCorr1 = ht + nu1Pt + getValue(c[mode],"l1Pt")

      twoToOne[100*int(ht/100)][50*int(met/50)].Fill(oneNuMet0, htCorr0)
      twoToOne[100*int(ht/100)][50*int(met/50)].Fill(oneNuMet1, htCorr1)
#      print  "Mu:", getValue(c[mode],"nuMu")  + getValue(c[mode],"antinuMu"), "E", getValue(c[mode],"nuE") + getValue(c[mode],"antinuE"), "genmetCalc", genmetCalc, "genmet",niceNum(getValue(c[mode],"genmet")), "met", niceNum(getValue(c[mode],"barepfmet"))
#      print  "Mu:", getValue(c[mode],"nuMu")  + getValue(c[mode],"antinuMu"), "E", getValue(c[mode],"nuE") + getValue(c[mode],"antinuE"), "met", niceNum(met), sqrt(metx**2 + mety**2), "nu0Pt", niceNum(getValue(c[mode],"nu0Pt")), "oneNuMet0", niceNum(oneNuMet0), "nu1Pt", niceNum(getValue(c[mode],"nu1Pt")), "oneNuMet1", niceNum(oneNuMet1), "genmet",niceNum(getValue(c[mode],"genmet")), "met", niceNum(getValue(c[mode],"barepfmet"))

  del elist

# Normalize prediction templates
for ht in range(0,2000,100):
  for met in range(0,1000,50):
    integr = twoToOne[ht][met].Integral()
    if integr>0:
      twoToOne[ht][met].Scale(1./integr)

#get the 1l ht and met shape
print "Get the 1nu met-ht shape"
commoncf={}
commoncf["Mu"]  = "ht>300&&jet2pt>40&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0" 
commoncf["Ele"] = "ht>300&&jet2pt>40&&singleElectronic&&nvetoElectrons==1&&nvetoMuons==0"

oneLepMETHT =  ROOT.TH2F("oneLepMETHT",  "oneLepMETHT",  20,0,1000, 20,0,2000) 
oneLepMETHT.GetXaxis().SetTitle("#slash{E}_{T} (GeV)")
oneLepMETHT.GetYaxis().SetTitle("H_{T} (GeV)")
for mode in modes:
  print "At",mode
  ntot = c[mode].GetEntries()
  c[mode].Draw(">>eList", commoncf[mode])
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  print "nevents:", number_events
  if small:
    if number_events>200:
      number_events=200
  for i in range(0, number_events):
    if (i%10000 == 0) and i>0 :
      print i
#      # Update all the Tuples
    if elist.GetN()>0 and ntot>0:
      c[mode].GetEntry(elist.GetEntry(i))
      ht =  getValue(c[mode],"ht")
      met =  getValue(c[mode],"barepfmet")
      oneLepMETHT.Fill(met, ht)
  del elist

#Constructing the HT and MET shapes which the 2l Events would have, had they been 1l Events
closure_commoncf={}
closure_commoncf["Mu"]  = "jet0pt>40&&nvetoMuons+nvetoElectrons>1" 
closure_commoncf["Ele"] = "jet0pt>40&&nvetoElectrons>1"

print "Get the  1l MET-HT prediction"
oneLepMETHTPrediction = ROOT.TH2F("oneLepMETHTPrediction", "oneLepMETHTPrediction", 20,0,1000, 20,0,2000) 
oneLepMETHTPrediction.GetXaxis().SetTitle("#slash{E}_{T} (GeV)")
oneLepMETHTPrediction.GetYaxis().SetTitle("H_{T} (GeV)")
for mode in modes:
  print "At",mode
  ntot = c[mode].GetEntries()
  c[mode].Draw(">>eList", closure_commoncf[mode])
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  print "nevents:", number_events
  if small:
    if number_events>200:
      number_events=200
  for i in range(0, number_events):
    if (i%10000 == 0) and i>0 :
      print i
#      # Update all the Tuples
    if elist.GetN()>0 and ntot>0:
      c[mode].GetEntry(elist.GetEntry(i))
      ht =  getValue(c[mode],"ht")
      met =  getValue(c[mode],"barepfmet")
      oneLepMETHTPrediction.Add(twoToOne[100*int(ht/100.)][100*int(met/100.)])
#      print  "Mu:", getValue(c[mode],"nuMu")  + getValue(c[mode],"antinuMu"), "E", getValue(c[mode],"nuE") + getValue(c[mode],"antinuE"), "genmetCalc", genmetCalc, "genmet",niceNum(getValue(c[mode],"genmet")), "met", niceNum(getValue(c[mode],"barepfmet"))
  del elist

for nmet in range(0,22):
  for nht in range(0,22):
    oneLepMETHT.GetBin(nmet,nht)
    if nmet<=3 or nht<=3 or nmet==21 or nht==21:
      oneLepMETHT.SetBinContent(nmet, nht, 0.) 
      oneLepMETHTPrediction.SetBinContent(nmet, nht, 0.) 

def getHTreweightedMETPrediction(oneLepMETHT, oneLepMETHTPrediction):
  projectionMETTrue             = oneLepMETHT.ProjectionX("met_proj_true", 0)
  projectionMETPredUnreweighted = oneLepMETHTPrediction.ProjectionX("met_proj_pred_unrew", 0)
  projectionHTTrue = oneLepMETHT           .ProjectionY("ht_proj_true", 0)
  projectionHTPred = oneLepMETHTPrediction .ProjectionY("ht_proj_pred", 0)
  projectionHTPred.SetLineColor(ROOT.kRed)
  projectionHTPred.SetMarkerColor(ROOT.kRed)
  #div = projectionHTPred.Integral(projectionHTPred.FindBin(150), projectionHTPred.FindBin(1000))
  #projectionHTPred.Scale( projectionHTTrue.Integral(projectionHTTrue.FindBin(150), projectionHTTrue.FindBin(1000)) / div)
  projectionMETPred = {}
  predicitedMETReweighted = ROOT.TH1F("met_prediction_rw", "met_prediction_rw", 20, 0, 1000) 
  for p in range(1,21):
    projectionMETPred[p] = oneLepMETHTPrediction.ProjectionX("proj_true"+str(p), p, p).Clone()
    if projectionHTPred.GetBinContent(p)>0:
      projectionMETPred[p].Scale(projectionHTTrue.GetBinContent(p)/projectionHTPred.GetBinContent(p)) 
    print projectionHTPred.GetBinContent(p), projectionMETPred[p].Integral()
    predicitedMETReweighted.Add(projectionMETPred[p])
#  projectionMETTrue.Draw("e")
  predicitedMETReweighted.SetLineColor(ROOT.kRed)
  predicitedMETReweighted.SetMarkerColor(ROOT.kRed)
#  predicitedMETReweighted.Draw("esame")
  projectionMETPredUnreweighted.SetLineColor(ROOT.kBlue)
  projectionMETPredUnreweighted.Scale(predicitedMETReweighted.Integral()/projectionMETPredUnreweighted.Integral())
  projectionMETPredUnreweighted.SetMarkerColor(ROOT.kBlue)
#  projectionMETPredUnreweighted.Draw("esame")
  return [projectionMETTrue, predicitedMETReweighted, projectionMETPredUnreweighted]

[projectionMETTrue, predicitedMETReweighted, projectionMETPredUnreweighted] = getHTreweightedMETPrediction(oneLepMETHT, oneLepMETHTPrediction)

#projectionMETTrue.Draw("e")
#predicitedMETReweighted.Draw("esame")


##make prediction from data

doubleMu = ROOT.TChain("Events")
doubleMu.Add("/data/schoef/pat_120125/DoubleMu/Run2011A-Aug5ReReco-v1/*.root")
doubleMu.Add("/data/schoef/pat_120125/DoubleMu/Run2011A-May10ReReco/*.root")
doubleMu.Add("/data/schoef/pat_120125/DoubleMu/Run2011A-Prompt-v4/*.root")
doubleMu.Add("/data/schoef/pat_120125/DoubleMu/Run2011A-Prompt-v6/*.root")
doubleMu.Add("/data/schoef/pat_120125/DoubleMu/Run2011B-Prompt-v1/*.root")
doubleMu_commoncf  = "jet0pt>40&&nvetoMuons>1" 


oneLepFromDataMETHT =  ROOT.TH2F("oneLepFromDataMETHT",  "oneLepFromDataMETHT",  20,0,1000, 20,0,2000) 
oneLepFromDataMETHT.GetXaxis().SetTitle("#slash{E}_{T} (GeV)")
oneLepFromDataMETHT.GetYaxis().SetTitle("H_{T} (GeV)")
print "At DoubleMu Data: Get the 1l MET prediction"
ntot = doubleMu.GetEntries()
doubleMu.Draw(">>eList", doubleMu_commoncf)
elist = ROOT.gDirectory.Get("eList")
number_events = elist.GetN()
print "nevents:", number_events
if small:
  if number_events>200:
    number_events=200
for i in range(0, number_events):
  if (i%10000 == 0) and i>0 :
    print i
#      # Update all the Tuples
  if elist.GetN()>0 and ntot>0:
    doubleMu.GetEntry(elist.GetEntry(i))
    ht =  getValue(doubleMu,"ht")
    met =  getValue(doubleMu,"barepfmet")
    oneLepFromDataMETHT.Add(twoToOne[100*int(ht/100.)][100*int(met/100.)])
#      print  "Mu:", getValue(c[mode],"nuMu")  + getValue(c[mode],"antinuMu"), "E", getValue(c[mode],"nuE") + getValue(c[mode],"antinuE"), "genmetCalc", genmetCalc, "genmet",niceNum(getValue(c[mode],"genmet")), "met", niceNum(getValue(c[mode],"barepfmet"))
del elist

for nmet in range(0,22):
  for nht in range(0,22):
    oneLepFromDataMETHT.GetBin(nmet,nht)
    if nmet<=3 or nht<=3 or nmet==21 or nht==21:
      oneLepFromDataMETHT.SetBinContent(nmet, nht, 0.)

[projectionMETTrue, predicitedFromDataMETReweighted, projectionMETPredFromDataUnreweighted] = getHTreweightedMETPrediction(oneLepMETHT, oneLepFromDataMETHT)

projectionMETTrue.Draw("e")
predicitedFromDataMETReweighted.Draw("esame")
