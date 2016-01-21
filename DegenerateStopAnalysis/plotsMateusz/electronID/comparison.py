#isoCutEffs.py
import ROOT
import os, sys
from Workspace.HEPHYPythonTools.helpers import getChunks, getChain#, getPlotFromChain, getYieldFromChain
from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_7412pass2 import * #data_path = "/data/nrad/cmgTuples/RunII/7412pass2_v4/RunIISpring15xminiAODv2"
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from array import array
from math import pi, sqrt #cos, sin, sinh, log

filedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronReconstruction/electronID"

#Input options
inputSample = "Signal" # "Signal" "TTJets" "WJets"
zoom = 1
save = 1
presel = 1
nEles = "01" # 01,01tau,1,2
isolation = "relIso03" #miniRelIso, relIso03, relIso04, relIsoAn04

num = "iso" # "iso" | "noIso"
den = "noIso" # "noIso" | "standard"

#ROOT Options
ROOT.gROOT.Reset() #re-initialises ROOT
#ROOT.gROOT.SetStyle("Plain")

ROOT.gStyle.SetOptStat(1111) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptFit(1111) #1111 prints fits results on plot
#ROOT.gStyle.SetOptTitle(0) #suppresses title box
#ROOT.gStyle.SetFuncWidth(1)
#ROOT.gStyle.SetFuncColor(9)
#ROOT.gStyle.SetLineWidth(2)

ROOT.gStyle.SetPaintTextFormat("4.2f")
#ROOT.gStyle.SetTitleX(0.5) 
#ROOT.gStyle.SetTitleAlign(23)
#ROOT.gStyle.SetTitleW(0.8)

ROOT.gStyle.SetStatX(0.75)
ROOT.gStyle.SetStatY(0.65)
ROOT.gStyle.SetStatW(0.1)
ROOT.gStyle.SetStatH(0.15)

print makeLine()
print "Signal Samples:"
newLine()
for s in allSignals: print s['name']
print makeLine()
print "Background Samples:"
newLine()
for s in samples: print s['name']

print makeLine()
print "Using", inputSample, "samples."
print makeLine()

#Events = ROOT.TChain("tree")

#Bin size 
#nbins = 100
xmin = 0
xmax = 1000
#sampleName = allSignals[0]

if inputSample == "Signal":
   #sampleName = allSignals[0]
   xmax = 150
elif inputSample == "TTJets":
   #sampleName = TTJets_LO
   xmax = 500
elif inputSample == "WJets":
   #sampleName = WJetsToLNu
   xmax = 500
else:
   print "Sample unavailable (check name)."
   sys.exit(0)


##Selection criteria
#intLum = 10.0 #fb-1
#weight = "(xsec*" + str(intLum) + "*(10^3)/" + str(getChunks(sampleName)[1]) + ")" #xsec in pb
#if zoom == 1: normFactor = "(0.5)"
#elif zoom == 0: normFactor = "((genLep_pt < 50)*0.5 + (genLep_pt >= 50 && genLep_pt < 100)*0.2 + (genLep_pt >= 100)*0.1)"

#Geometric divisions
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap
etaAcc = 2.5 #eta acceptance

ptSplit = 10 #we have above and below 10 GeV categories

#Preselection
preSel1 = "(met_pt > 200)" #MET
preSel2 = "(Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 4.5 && Jet_id)) > 200)" #HT = Sum of Jets > 30GeV
preSel3 = "(Max$(Jet_pt*(abs(Jet_eta) < " + str(etaAcc) + ") > 100))" #ISR

if presel == 1: preSel = preSel1 + "&&" + preSel2 + "&&" + preSel3
elif presel == 0: preSel = "1"

var = "genLep_pt"
deltaRcut = 0.3

#single-lepton (semileptonic) events
if nEles == "01":
   var = "genLep_pt[0]"
   if zoom == 0: normFactor = "((genLep_pt[0] < 50)*0.5 + (genLep_pt[0] >= 50 && genLep_pt[0] < 100)*0.2 + (genLep_pt[0] >= 100)*0.1)"
   
   #Generated electron selection
   nSel = "ngenLep == 1" #removes dileptonic events
   genSel1 = "(abs(genLep_pdgId[0]) == 11 && abs(genLep_eta[0]) < " + str(etaAcc) + ")" #electron selection #index [0] ok since (only element)
   genSel = nSel + "&&" + genSel1

   #Reconstructed electron selection
   deltaR = "sqrt((genLep_eta[0] - LepGood_eta)^2 + (genLep_phi[0] - LepGood_phi)^2)"
   matchSel = "(" + deltaR +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0) <" + str(deltaRcut) +\
   "&& (" + deltaR +"*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mcMatchId != 0)) != 0)"

#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)

cuts = {\
'Veto':{'sigmaEtaEta':{'Barrel':0.0114, 'Endcap':0.0352}, 'dEta':{'Barrel':0.0152, 'Endcap':0.0113}, 'dPhi':{'Barrel':0.216, 'Endcap':0.237}, 'hOverE':{'Barrel':0.181, 'Endcap':0.116}, 'ooEmooP':{'Barrel':0.207, 'Endcap':0.174},\
'd0':{'Barrel':0.0564, 'Endcap':0.222}, 'dz':{'Barrel':0.472, 'Endcap':0.921}, 'MissingHits':{'Barrel':2, 'Endcap':3}, 'convVeto':{'Barrel':1, 'Endcap':1}, 'relIso' : {'Barrel':0.126, 'Endcap':0.144}},
'Loose':{'sigmaEtaEta':{'Barrel':0.0103, 'Endcap':0.0301}, 'dEta':{'Barrel':0.0105, 'Endcap':0.00814}, 'dPhi':{'Barrel':0.115, 'Endcap':0.182}, 'hOverE':{'Barrel':0.104, 'Endcap':0.0897}, 'ooEmooP':{'Barrel':0.102, 'Endcap':0.126},\
'd0':{'Barrel':0.0261, 'Endcap':0.118}, 'dz':{'Barrel':0.41, 'Endcap':0.822}, 'MissingHits':{'Barrel':2, 'Endcap':1}, 'convVeto':{'Barrel':1, 'Endcap':1}, 'relIso' : {'Barrel':0.0893, 'Endcap':0.121}},
'Medium':{'sigmaEtaEta':{'Barrel':0.0101, 'Endcap':0.0283}, 'dEta':{'Barrel':0.0103, 'Endcap':0.00733}, 'dPhi':{'Barrel':0.0336, 'Endcap':0.114}, 'hOverE':{'Barrel':0.0876, 'Endcap':0.0678}, 'ooEmooP':{'Barrel':0.0174, 'Endcap':0.0898},\
'd0':{'Barrel':0.0118, 'Endcap':0.0739}, 'dz':{'Barrel':0.373, 'Endcap':0.602}, 'MissingHits':{'Barrel':2, 'Endcap':1}, 'convVeto':{'Barrel':1, 'Endcap':1}, 'relIso' : {'Barrel':0.0766, 'Endcap':0.0678}},
'Tight':{'sigmaEtaEta':{'Barrel':0.0101, 'Endcap':0.0279}, 'dEta':{'Barrel':0.00926, 'Endcap':0.00724}, 'dPhi':{'Barrel':0.0336, 'Endcap':0.0918}, 'hOverE':{'Barrel':0.0597, 'Endcap':0.0615}, 'ooEmooP':{'Barrel':0.012, 'Endcap':0.00999},\
'd0':{'Barrel':0.0111, 'Endcap':0.0351}, 'dz':{'Barrel':0.0466, 'Endcap':0.417}, 'MissingHits':{'Barrel':2, 'Endcap':1}, 'convVeto':{'Barrel':1, 'Endcap':1}, 'relIso' : {'Barrel':0.0354, 'Endcap':0.0646}}}

#cutSel = "LepGood_SPRING15_25ns_v1 >="

bins = array('d', range(xmin,50,2) + range(50,100,5) + range(100,xmax+10,10)) #Variable bin size

#Zoom
z = ""
if zoom == 1:
   #nbins = 10
   xmax = 50
   bins = array('d',range(xmin,xmax+2,2))
   z = "_lowPt"
   
WPs = ['Veto','Loose','Medium','Tight']

#Gets root files
total = {"eleID":{}, "misID":{}, "misID2":{}}
passed = {"eleID":{}, "misID":{}, "misID2":{}}

plot = "eleID"
if den == "standard": denFile = ROOT.TFile(filedir + "/" + den + "/efficiency/root/eleIDeff_" + inputSample + z + ".root", "read")
else: denFile = ROOT.TFile(filedir + "/" + den + "/efficiency/root/eleIDeff_" + den + "_" + inputSample + z + ".root", "read")
if num == "iso": numFile = ROOT.TFile(filedir + "/" + num + "/" + isolation + "/efficiency/root/eleIDeff_" + num + "_" + inputSample + z + ".root", "read")
else: numFile = ROOT.TFile(filedir + "/" + num + "/efficiency/root/eleIDeff_" + num + "_" + inputSample + z + ".root", "read")
for WP in WPs:
   total[plot][WP] = denFile.Get("c1").GetPrimitive("c1_1").GetPrimitive(plot + "_" + WP) 
   passed[plot][WP] = numFile.Get("c1").GetPrimitive("c1_1").GetPrimitive(plot + "_" + WP) 

plot = "misID"
if den == "standard": denFile = ROOT.TFile(filedir + "/" + den + "/misID/root/eleMisID_" + inputSample + z + ".root", "read")
else: denFile = ROOT.TFile(filedir + "/" + den + "/misID/root/eleMisID_" + den + "_" + inputSample + z + ".root", "read")
if num == "iso": numFile = ROOT.TFile(filedir + "/" + num + "/" + isolation + "/misID/root/eleMisID_" + num + "_" + inputSample + z + ".root", "read")
else: numFile = ROOT.TFile(filedir + "/" + num + "/misID/root/eleMisID_" + num + "_" + inputSample + z + ".root", "read")

for WP in WPs:
   total[plot][WP] = denFile.Get("c1").GetPrimitive("c1_1").GetPrimitive(plot + "_" + WP) 
   passed[plot][WP] = numFile.Get("c1").GetPrimitive("c1_1").GetPrimitive(plot + "_" + WP) 

plot = "misID2"
if den == "standard": denFile = ROOT.TFile(filedir + "/" + den + "/misID2/root/eleMisID2_" + inputSample + z + ".root", "read")
else: denFile = ROOT.TFile(filedir + "/" + den + "/misID2/root/eleMisID2_" + den + "_" + inputSample + z + ".root", "read")
if num == "iso": numFile = ROOT.TFile(filedir + "/" + num + "/" + isolation + "/misID2/root/eleMisID2_" + num + "_" + inputSample + z + ".root", "read")
else: numFile = ROOT.TFile(filedir + "/" + num + "/misID2/root/eleMisID2_" + num + "_" + inputSample + z + ".root", "read")
for WP in WPs:
   total[plot][WP] = denFile.Get("c1").GetPrimitive("c1_1").GetPrimitive(plot + "_" + WP) 
   passed[plot][WP] = numFile.Get("c1").GetPrimitive("c1_1").GetPrimitive(plot + "_" + WP) 

##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,3)

effs = {"eleID":{}, "misID": {}, "misID2": {}}

#Efficiency
for plot in sorted(total.keys()):
   for WP in WPs: 
      effs[plot][WP] = passed[plot][WP]
      effs[plot][WP].Divide(total[plot][WP])
      effs[plot][WP].SetName("eff_" + plot + "_" + WP) 
      effs[plot][WP].SetMarkerStyle(33) 
      effs[plot][WP].SetMarkerSize(1.5) 
      effs[plot][WP].SetLineWidth(2) 

for i,plot in enumerate(sorted(total.keys())):
   c1.cd(i+1)
  
   if num == "iso":
      if plot == "eleID": effs[plot]['Veto'].SetTitle("Efficiency: Comparison of " + num + " (" + isolation + ") and " + den + " Plots (" + inputSample + " Sample)")
      elif plot == "misID": effs[plot]['Veto'].SetTitle("MisID Efficiency: Comparison of " + num + " (" + isolation + ") and " + den + " Plots (" + inputSample + " Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency")
      elif plot == "misID2": effs[plot]['Veto'].SetTitle("MisID2 Efficiency: Comparison of " + num + " (" + isolation + ") and " + den + " Plots (" + inputSample + " Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency")
   else: 
      if plot == "eleID": effs[plot]['Veto'].SetTitle("Efficiency: Comparison of " + num + " and " + den + " Plots (" + inputSample + " Sample) ; Generated Electron p_{T} / GeV ; Efficiency")
      elif plot == "misID": effs[plot]['Veto'].SetTitle("MisID Efficiency: Comparison of " + num + " and " + den + " Plots (" + inputSample + " Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency")
      elif plot == "misID2": effs[plot]['Veto'].SetTitle("MisID2 Efficiency: Comparison of " + num + " and " + den + " Plots (" + inputSample + " Sample) ; Reconstructed Electron p_{T} / GeV ; Efficiency")
   
   effs[plot]['Veto'].SetMarkerColor(ROOT.kGreen+3) 
   effs[plot]['Veto'].SetLineColor(ROOT.kGreen+3) 
   effs[plot]['Veto'].Draw("P") 
   ROOT.gPad.SetGridx() 
   ROOT.gPad.SetGridy() 
   #ROOT.gPad.RedrawAxis()
   ROOT.gPad.Modified() 
   ROOT.gPad.Update() 
   #effs[plot]['Veto'].GetXaxis().SetLimits(xmin,xmax) 
   effs[plot]['Veto'].GetYaxis().SetTitle("Efficiency")
   effs[plot]['Veto'].GetXaxis().SetTitle("Generated Electron p_{T} / GeV")
   effs[plot]['Veto'].SetMinimum(0) 
   if num == "noIso" and den == "standard": effs[plot]['Veto'].SetMaximum(3) 
   else: effs[plot]['Veto'].SetMaximum(1) 
   
   effs[plot]['Veto'].GetXaxis().CenterTitle() 
   effs[plot]['Veto'].GetYaxis().CenterTitle() 
   
   alignStats(effs[plot]['Veto'])
 
   for WP in WPs:
      if WP != 'Veto': effs[plot][WP].Draw("sameP")  
    
   #Colours 
   effs[plot]['Loose'].SetMarkerColor(ROOT.kBlue+1) 
   effs[plot]['Loose'].SetLineColor(ROOT.kBlue+1) 
   effs[plot]['Medium'].SetMarkerColor(ROOT.kOrange-2) 
   effs[plot]['Medium'].SetLineColor(ROOT.kOrange-2) 
   effs[plot]['Tight'].SetMarkerColor(ROOT.kRed+1) 
   effs[plot]['Tight'].SetLineColor(ROOT.kRed+1) 
   
   ROOT.gPad.Modified() 
   ROOT.gPad.Update() 
   
   if plot == "eleID": 
      l1 = makeLegend() 
      l1.AddEntry("eff_eleID_Veto", "Veto ID", "P") 
      l1.AddEntry("eff_eleID_Loose", "Loose ID", "P") 
      l1.AddEntry("eff_eleID_Medium", "Medium ID", "P") 
      l1.AddEntry("eff_eleID_Tight", "Tight ID", "P") 
   l1.Draw()

ROOT.gPad.Modified()
ROOT.gPad.Update()
c1.Modified()
c1.Update()

#Write to file
if save == 1:
   if num == "iso": num = isolation #naming 
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronReconstruction/electronID/comparisons/" + num + "_" + den #web address: http://www.hephy.at/user/mzarucki/plots/electronReconstruction/electronIdEfficiency
   
   if not os.path.exists(savedir):
      os.makedirs(savedir)
   if not os.path.exists(savedir + "/root"):
      os.makedirs(savedir + "/root")
   if not os.path.exists(savedir + "/pdf"):
      os.makedirs(savedir + "/pdf")
   
   #Save to Web
   c1.SaveAs(savedir + "/comparison_" + num + "_" + den + "_" + inputSample + z + ".png")
   c1.SaveAs(savedir + "/root/comparison_" + num + "_" + den + "_" + inputSample + z + ".root")
   c1.SaveAs(savedir + "/pdf/comparison_" + num + "_" + den + "_" + inputSample + z + ".pdf")
