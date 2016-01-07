#eleIdEff_loop.py
import ROOT
import os, sys
from Workspace.HEPHYPythonTools.helpers import getChunks, getChain, getObjDict, deltaPhi#, getPlotFromChain, getYieldFromChain
from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_7412pass2 import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from array import array
from math import pi, sqrt #cos, sin, sinh, log

def deltaR(l1, l2):
  return sqrt(deltaPhi(l1['phi'], l2['phi'])**2 + (l1['eta'] - l2['eta'])**2)

#Input options
inputSample = "WJets" # "Signal" "TTJets" "WJets"
zoom = 1
save = 1
presel = 1
nEles = 1 # 1,2,1or2

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
#ROOT.gStyle->SetTitleX(0.1)
#ROOT.gStyle->SetTitleW(0.8)

ROOT.gStyle.SetStatX(0.75)
ROOT.gStyle.SetStatY(0.65)
ROOT.gStyle.SetStatW(0.1)
ROOT.gStyle.SetStatH(0.15)

#CMG Tuples
#data_path = "/data/nrad/cmgTuples/RunII/7412pass2/RunIISpring15xminiAODv2"
#data_path = "/afs/hephy.at/data/mzarucki01/cmgTuples"

print makeLine()
print "Signal Samples:"
newLine()
for s in allSignals: print s['name']
print makeLine()
print "Background Samples:"
newLine()
for s in samples: print s['name']
#print makeLine()

print makeLine()
print "Using", inputSample, "samples."
print makeLine()

Events = ROOT.TChain("tree")

#for s in allSamples_Spring15_25ns:
#   if sample in s['name']:
#      print s['name']
#      for f in getChunks(s)[0]: Events.Add(f['file'])

#Bin size 
#nbins = 100
xmin = 0
xmax = 1000
sampleName = allSignals[0]

if inputSample == "Signal": 
   sampleName = allSignals[0]
   xmax = 150
elif inputSample == "TTJets": 
   sampleName = TTJets_LO
   xmax = 500
elif inputSample == "WJets": 
   sampleName = WJetsToLNu
   xmax = 500
else:
   print "Sample unavailable (check name)."
   sys.exit(0)

for f in getChunks(sampleName)[0]: Events.Add(f['file'])

bins = array('d', range(xmin,50,2) + range(50,100,5) + range(100,xmax+10,10)) #Variable bin size

#Zoom
z = ""
if zoom == 1:
   #nbins = 10
   xmax = 50
   bins = array('d',range(xmin,xmax+2,2))
   z = "_lowPt"

#Geometric divisions
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap
etaAcc = 2.5 #eta acceptance

#Selection criteria
deltaRcut = 0.3

#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)
cutSel = "LepGood_SPRING15_25ns_v1 >="

#MVA IDs
WPs = {'WP90':\
         {'EB1_lowPt':-0.083313, 'EB2_lowPt':-0.235222, 'EE_lowPt':-0.67099, 'EB1':0.913286, 'EB2':0.805013, 'EE':0.358969},\
       'WP80':\
         {'EB1_lowPt':0.287435, 'EB2_lowPt':0.221846, 'EE_lowPt':-0.303263, 'EB1':0.967083, 'EB2':0.929117, 'EE':0.726311},\
}

ptSplit = 10 #we have above and below 10 GeV categories

#Generated electrons
hist_total = emptyHistVarBins("genEle", bins)
hists_passed = []

for i in range(1,7):
   hists_passed.append(emptyHistVarBins("eleID" + str(i), bins))

#Selection criteria
intLum = 10.0 #fb-1
N0 = getChunks(sampleName)[1]

#Preselection
preSel1 = "(met_pt > 200)" #MET
preSel2 = "(Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 4.5 && Jet_id)) > 200)" #HT = Sum of Jets > 30GeV
preSel3 = "(Max$(Jet_pt*(abs(Jet_eta) < " + str(etaAcc) + ") > 100))" #ISR

if presel == 1: preSel = preSel1 + "&&" + preSel2 + "&&" + preSel3
elif presel == 0: preSel = "1"

Events.Draw(">>eList", preSel)
elist = ROOT.gDirectory.Get("eList")
nEvents = elist.GetN()

#Event Loop
for i in range(nEvents):
   #if i > 1000: break
   Events.GetEntry(elist.GetEntry(i))
   
   xsec = Events.GetLeaf("xsec").GetValue()
   weight = xsec*pow(10,3)*intLum/N0
   
   #Number of generated and reconstructed leptons
   ngenLep = Events.GetLeaf("ngenLep").GetValue()
   nLep = Events.GetLeaf("nLepGood").GetValue()
   
   if ngenLep == 0: continue
 
   #Generated 
   genLeps = [getObjDict(Events, "genLep_", ["pdgId","pt","eta","phi"],i) for i in range(int(ngenLep))]
   genEles = [genEle for genEle in genLeps if abs(genEle['pdgId']) == 11 and abs(genEle['eta']) < etaAcc] 
   
   #Reconstructed
   recoLeps = [getObjDict(Events, "LepGood_", ["pdgId","pt", "eta", "phi", "mcMatchId", "SPRING15_25ns_v1", "mvaIdSpring15"],i) for i in range(int(nLep))]
   recoEles = [recoEle for recoEle in recoLeps if abs(recoEle['pdgId']) == 11 and abs(recoEle['eta']) < etaAcc] 
  
   if ngenLep != 1: continue
   #if len(genEles) != nEles: continue # > if nEles = 1, allowing dileptonic | if nEles = 2 allowing 1 or 2 evts
   
   for recoEle in recoEles: recoEle['deltaR'] = [] #empty deltaR list   
  
   #Calculating dR between gen and reco electrons
   for recoEle in recoEles:
      for genEle in genEles:
         recoEle['deltaR'].append(deltaR(genEle,recoEle))
      
      #Matching
      if recoEle['mcMatchId'] != 0 and len(recoEle['deltaR']) != 0:
         recoEle['deltaRmin'] = min(recoEle['deltaR'])
         matchIndex = recoEle['deltaR'].index(recoEle['deltaRmin']) #finds index of gen electron with lowest dR
      else: matchIndex = -1
      recoEle['matchIndex'] = matchIndex
      recoEle['matchIndexTau'] = -1
 
   #Histogram filling
   #Reconstructed electron pt fill (numerators) 
   for recoEle in recoEles:
      if abs(recoEle['pdgId']) == 11 and abs(recoEle['eta']) < etaAcc and recoEle['mcMatchId'] != 0 and recoEle['matchIndex'] != -1 and recoEle['deltaRmin'] < deltaRcut: #or recoEle['matchIndexTau'] != -1
         
         #Determination of MVA ID cut value (dependent on electron pt and detector region)
         if recoEle['pt'] <= ptSplit:
            if abs(recoEle['eta']) < ebSplit:
               MVA_min1 = WPs['WP80']['EB1_lowPt']
               MVA_min2 = WPs['WP90']['EB1_lowPt']
            elif abs(recoEle['eta']) >= ebSplit and abs(recoEle['eta']) < ebeeSplit:
               MVA_min1 = WPs['WP80']['EB2_lowPt']
               MVA_min2 = WPs['WP90']['EB2_lowPt']
            elif abs(recoEle['eta']) >= ebeeSplit:
               MVA_min1 = WPs['WP80']['EE_lowPt']
               MVA_min2 = WPs['WP90']['EE_lowPt']
         elif recoEle['pt'] > ptSplit:
            if abs(recoEle['eta']) < ebSplit:
               MVA_min1 = WPs['WP80']['EB1']
               MVA_min2 = WPs['WP90']['EB1']
            elif abs(recoEle['eta']) >= ebSplit and abs(recoEle['eta']) < ebeeSplit:
               MVA_min1 = WPs['WP80']['EB2']
               MVA_min2 = WPs['WP90']['EB2']
            elif abs(recoEle['eta']) >= ebeeSplit:
               MVA_min1 = WPs['WP80']['EE']
               MVA_min2 = WPs['WP90']['EE']
   
         #Cut ID Fill
         for i in range(1,5):
            if recoEle['SPRING15_25ns_v1'] >= i: 
               if zoom == 0: 
                  if genEles[recoEle['matchIndex']]['pt'] >= xmin and genEles[recoEle['matchIndex']]['pt'] < 50: hists_passed[i-1].Fill(genEles[recoEle['matchIndex']]['pt'], weight/2)
                  if genEles[recoEle['matchIndex']]['pt'] >= 50 and genEles[recoEle['matchIndex']]['pt'] < 100: hists_passed[i-1].Fill(genEles[recoEle['matchIndex']]['pt'], weight/5)
                  if genEles[recoEle['matchIndex']]['pt'] >= 100 and genEles[recoEle['matchIndex']]['pt'] < xmax + 10: hists_passed[i-1].Fill(genEles[recoEle['matchIndex']]['pt'], weight/10)
               elif zoom == 1: hists_passed[i-1].Fill(genEles[recoEle['matchIndex']]['pt'], weight/2) 
         
         #MVA ID Fill
         if recoEle['mvaIdSpring15'] >= MVA_min1: 
            if zoom == 0:
               if genEles[recoEle['matchIndex']]['pt'] >= xmin and genEles[recoEle['matchIndex']]['pt'] < 50: hists_passed[4].Fill(genEles[recoEle['matchIndex']]['pt'], weight/2)
               if genEles[recoEle['matchIndex']]['pt'] >= 50 and genEles[recoEle['matchIndex']]['pt'] < 100: hists_passed[4].Fill(genEles[recoEle['matchIndex']]['pt'], weight/5)
               if genEles[recoEle['matchIndex']]['pt'] >= 100 and genEles[recoEle['matchIndex']]['pt'] < xmax + 10: hists_passed[4].Fill(genEles[recoEle['matchIndex']]['pt'], weight/10)
            elif zoom == 1: hists_passed[4].Fill(genEles[recoEle['matchIndex']]['pt'], weight/2) 
         
         if recoEle['mvaIdSpring15'] >= MVA_min2:
            if zoom == 0:
               if genEles[recoEle['matchIndex']]['pt'] >= xmin and genEles[recoEle['matchIndex']]['pt'] < 50: hists_passed[5].Fill(genEles[recoEle['matchIndex']]['pt'], weight/2)
               if genEles[recoEle['matchIndex']]['pt'] >= 50 and genEles[recoEle['matchIndex']]['pt'] < 100: hists_passed[5].Fill(genEles[recoEle['matchIndex']]['pt'], weight/5)
               if genEles[recoEle['matchIndex']]['pt'] >= 100 and genEles[recoEle['matchIndex']]['pt'] < xmax + 10: hists_passed[5].Fill(genEles[recoEle['matchIndex']]['pt'], weight/10)
            elif zoom == 1: hists_passed[5].Fill(genEles[recoEle['matchIndex']]['pt'], weight/2) 
   
   #Generated electron pt fill (denominator) 
   for genEle in genEles:
   #if ngenLep == 1 and ngenLepFromTau == 0:
      if abs(genEle['pdgId']) == 11 and abs(genEle['eta']) < etaAcc and len(genEles) == nEles:
         if zoom == 0:
            if genEle['pt'] < 50: hist_total.Fill(genEle['pt'], weight/2)
            if genEle['pt'] >= 50 and genEle['pt'] < 100: hist_total.Fill(genEle['pt'], weight/5)
            if genEle['pt'] >= 100: hist_total.Fill(genEle['pt'], weight/10)
         elif zoom == 1: hist_total.Fill(genEle['pt'], weight/2) 
 
##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

c1.cd(1)

hist_total.SetName("genEle")
hist_total.SetTitle("Electron p_{T} Distributions for Various IDs (" + inputSample + " Sample)")
hist_total.GetXaxis().SetTitle("Generated Electron p_{T} / GeV")
hist_total.GetYaxis().SetTitle("Counts / GeV")
hist_total.SetFillColor(ROOT.kBlue-9)
hist_total.SetLineColor(ROOT.kBlack)
hist_total.SetLineWidth(3)
hist_total.Draw("hist")
ROOT.gPad.SetLogy()
ROOT.gPad.Update()
hist_total.GetXaxis().SetTitleOffset(1.2)
hist_total.GetYaxis().SetTitleOffset(1.2)
alignStats(hist_total)

#Veto ID
hists_passed[0].SetName("electrons_veto")
hists_passed[0].SetLineColor(ROOT.kGreen+3)

#Loose ID
hists_passed[1].SetName("electrons_loose")
hists_passed[1].SetLineColor(ROOT.kBlue+1)

#Medium ID
hists_passed[2].SetName("electrons_medium")
hists_passed[2].SetLineColor(ROOT.kOrange-2)

#Tight ID
hists_passed[3].SetName("electrons_tight")
hists_passed[3].SetLineColor(ROOT.kRed+1)

hists_passed[4].SetName("electrons_mva_WP80")
hists_passed[4].SetLineColor(ROOT.kAzure+5)

hists_passed[5].SetName("electrons_mva_WP90")
hists_passed[5].SetLineColor(ROOT.kMagenta+2)

for i in range(0,6): #hists 1-6
   hists_passed[i].SetFillColor(0)
   hists_passed[i].SetLineWidth(3)
   hists_passed[i].Draw("histsame")

l1 = makeLegend()
l1.AddEntry("genEle", "Generated Electron p_{T}", "F")
l1.AddEntry("electrons_veto", "Veto ID", "F")
l1.AddEntry("electrons_loose", "Loose ID", "F")
l1.AddEntry("electrons_medium", "Medium ID", "F")
l1.AddEntry("electrons_tight", "Tight ID", "F")
l1.AddEntry("electrons_mva_WP80", "MVA ID (WP80)", "F")
l1.AddEntry("electrons_mva_WP90", "MVA ID (WP90)", "F")
l1.Draw()

################################################################################################################################################################################
#Efficiency curves
c1.cd(2)
l2 = makeLegend()

effs = []

#Efficiency Veto
for i in range (0, 6):
   effs.append(ROOT.TEfficiency(hists_passed[i], hist_total)) #(passed, total)
   effs[i].SetMarkerStyle(33)
   effs[i].SetMarkerSize(1.5)
   effs[i].SetLineWidth(2)

effs[0].SetTitle("Electron ID Efficiencies (" + inputSample + " Sample) ; Generated Electron p_{T} / GeV ; Efficiency")
effs[0].SetName("eff1")
effs[0].SetMarkerColor(ROOT.kGreen+3)
effs[0].SetLineColor(ROOT.kGreen+3)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
effs[0].Draw("AP") 
ROOT.gPad.Update()
effs[0].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)
effs[0].GetPaintedGraph().SetMinimum(0)
effs[0].GetPaintedGraph().SetMaximum(1)
#effs[0].GetPaintedGraph().GetXaxis().SetNdivisions(510, 1)
effs[0].GetPaintedGraph().GetXaxis().CenterTitle()
effs[0].GetPaintedGraph().GetYaxis().CenterTitle()

#Efficiency Loose
effs[1].SetName("eff2")
effs[1].SetMarkerColor(ROOT.kBlue+1)
effs[1].SetLineColor(ROOT.kBlue+1)
effs[1].Draw("sameP") 

#Efficiency Medium
effs[2].SetName("eff3")
effs[2].SetMarkerColor(ROOT.kOrange-2)
effs[2].SetLineColor(ROOT.kOrange-2)
effs[2].Draw("sameP") 

#Efficiency Tight
effs[3].SetName("eff4")
effs[3].SetMarkerColor(ROOT.kRed+1)
effs[3].SetLineColor(ROOT.kRed+1)
effs[3].Draw("sameP") 

#Efficiency WP80
effs[4].SetName("eff5")
effs[4].SetMarkerColor(ROOT.kAzure+5)
effs[4].SetMarkerStyle(22)
effs[4].SetMarkerSize(1)
effs[4].Draw("sameP")
effs[4].SetLineColor(ROOT.kAzure+5)

#Efficiency WP90
effs[5].SetName("eff6")
effs[5].SetMarkerColor(ROOT.kMagenta+2)
effs[5].SetMarkerStyle(22)
effs[5].SetMarkerSize(1)
effs[5].Draw("sameP")
effs[5].SetLineColor(ROOT.kMagenta+2)

ROOT.gPad.Update()

l2.AddEntry("eff1", "Veto ID", "P")
l2.AddEntry("eff2", "Loose ID", "P")
l2.AddEntry("eff3", "Medium ID", "P")
l2.AddEntry("eff4", "Tight ID", "P")
l2.AddEntry("eff5", "MVA ID (WP80)", "P")
l2.AddEntry("eff6", "MVA ID (WP90)", "P")
l2.Draw()

ROOT.gPad.Update()
c1.Modified()
c1.Update()

if save == 1:
   #Write to file
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronReconstruction/electronID/efficiency/loop" #web address: http://www.hephy.at/user/mzarucki/plots/electronReconstruction/electronIdEfficiency
   
   if not os.path.exists(savedir):
      os.makedirs(savedir)
   if not os.path.exists(savedir + "/root"):
      os.makedirs(savedir + "/root")
   if not os.path.exists(savedir + "/pdf"):
      os.makedirs(savedir + "/pdf")
 
   #Save to Web
   c1.SaveAs(savedir + "/eleIDeff_loop_" + inputSample + z + ".png")
   c1.SaveAs(savedir + "/root/eleIDeff_loop_" + inputSample + z + ".root")
   c1.SaveAs(savedir + "/pdf/eleIDeff_loop_" + inputSample + z + ".pdf")
