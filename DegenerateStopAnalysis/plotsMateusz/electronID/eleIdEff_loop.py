#eleIdEff_loop.py
import ROOT
import os, sys
from Workspace.HEPHYPythonTools.helpers import getChunks, getChain, getObjDict, deltaPhi#, getPlotFromChain, getYieldFromChain
from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_7412pass2 import * #data_path = "/data/nrad/cmgTuples/RunII/7412pass2_v4/RunIISpring15xminiAODv2"
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from array import array
from math import pi, sqrt #cos, sin, sinh, log

def deltaR(l1, l2):
  return sqrt(deltaPhi(l1['phi'], l2['phi'])**2 + (l1['eta'] - l2['eta'])**2)

#Input options
inputSample = "Signal" # "Signal" "TTJets" "WJets"
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

Events = ROOT.TChain("tree")

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
WPs_cut = ['Veto', 'Loose', 'Medium', 'Tight']
#MVA IDs
WPs_mva = {'WP90':\
         {'EB1_lowPt':-0.083313, 'EB2_lowPt':-0.235222, 'EE_lowPt':-0.67099, 'EB1':0.913286, 'EB2':0.805013, 'EE':0.358969},\
       'WP80':\
         {'EB1_lowPt':0.287435, 'EB2_lowPt':0.221846, 'EE_lowPt':-0.303263, 'EB1':0.967083, 'EB2':0.929117, 'EE':0.726311},\
}

WPs = WPs_cut + WPs_mva.keys()

ptSplit = 10 #we have above and below 10 GeV categories

#Generated electrons
hist_total = emptyHistVarBins("eleID", bins)
hists_passed = {}

for i,WP in enumerate(WPs):
   hists_passed[WP] = emptyHistVarBins("eleID_" + WP, bins)
   hists_passed[WP].SetName("eleID_" + WP)

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
               MVA_min1 = WPs_mva['WP90']['EB1_lowPt']
               MVA_min2 = WPs_mva['WP80']['EB1_lowPt']
            elif abs(recoEle['eta']) >= ebSplit and abs(recoEle['eta']) < ebeeSplit:
               MVA_min1 = WPs_mva['WP90']['EB2_lowPt']
               MVA_min2 = WPs_mva['WP80']['EB2_lowPt']
            elif abs(recoEle['eta']) >= ebeeSplit:
               MVA_min1 = WPs_mva['WP90']['EE_lowPt']
               MVA_min2 = WPs_mva['WP80']['EE_lowPt']
         elif recoEle['pt'] > ptSplit:
            if abs(recoEle['eta']) < ebSplit:
               MVA_min1 = WPs_mva['WP90']['EB1']
               MVA_min2 = WPs_mva['WP80']['EB1']
            elif abs(recoEle['eta']) >= ebSplit and abs(recoEle['eta']) < ebeeSplit:
               MVA_min1 = WPs_mva['WP90']['EB2']
               MVA_min2 = WPs_mva['WP80']['EB2']
            elif abs(recoEle['eta']) >= ebeeSplit:
               MVA_min1 = WPs_mva['WP90']['EE']
               MVA_min2 = WPs_mva['WP80']['EE']
   
         #Cut ID Fill
         for i,WP in enumerate(WPs_cut):
            if recoEle['SPRING15_25ns_v1'] >= i+1: 
               if zoom == 0: 
                  if genEles[recoEle['matchIndex']]['pt'] >= xmin and genEles[recoEle['matchIndex']]['pt'] < 50: hists_passed[WP].Fill(genEles[recoEle['matchIndex']]['pt'], weight/2)
                  if genEles[recoEle['matchIndex']]['pt'] >= 50 and genEles[recoEle['matchIndex']]['pt'] < 100: hists_passed[WP].Fill(genEles[recoEle['matchIndex']]['pt'], weight/5)
                  if genEles[recoEle['matchIndex']]['pt'] >= 100 and genEles[recoEle['matchIndex']]['pt'] < xmax + 10: hists_passed[WP].Fill(genEles[recoEle['matchIndex']]['pt'], weight/10)
               elif zoom == 1: hists_passed[WP].Fill(genEles[recoEle['matchIndex']]['pt'], weight/2) 
         
         #MVA ID Fill
         if recoEle['mvaIdSpring15'] >= MVA_min1:
            if zoom == 0:
               if genEles[recoEle['matchIndex']]['pt'] >= xmin and genEles[recoEle['matchIndex']]['pt'] < 50: hists_passed['WP90'].Fill(genEles[recoEle['matchIndex']]['pt'], weight/2)
               if genEles[recoEle['matchIndex']]['pt'] >= 50 and genEles[recoEle['matchIndex']]['pt'] < 100: hists_passed['WP90'].Fill(genEles[recoEle['matchIndex']]['pt'], weight/5)
               if genEles[recoEle['matchIndex']]['pt'] >= 100 and genEles[recoEle['matchIndex']]['pt'] < xmax + 10: hists_passed['WP90'].Fill(genEles[recoEle['matchIndex']]['pt'], weight/10)
            elif zoom == 1: hists_passed['WP90'].Fill(genEles[recoEle['matchIndex']]['pt'], weight/2) 
   
         if recoEle['mvaIdSpring15'] >= MVA_min2: 
            if zoom == 0:
               if genEles[recoEle['matchIndex']]['pt'] >= xmin and genEles[recoEle['matchIndex']]['pt'] < 50: hists_passed['WP80'].Fill(genEles[recoEle['matchIndex']]['pt'], weight/2)
               if genEles[recoEle['matchIndex']]['pt'] >= 50 and genEles[recoEle['matchIndex']]['pt'] < 100: hists_passed['WP80'].Fill(genEles[recoEle['matchIndex']]['pt'], weight/5)
               if genEles[recoEle['matchIndex']]['pt'] >= 100 and genEles[recoEle['matchIndex']]['pt'] < xmax + 10: hists_passed['WP80'].Fill(genEles[recoEle['matchIndex']]['pt'], weight/10)
            elif zoom == 1: hists_passed['WP80'].Fill(genEles[recoEle['matchIndex']]['pt'], weight/2) 
         
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

hist_total.SetName("eleID")
hist_total.SetTitle("Electron p_{T} Distributions for Various IDs (" + inputSample + " Sample)")
hist_total.GetXaxis().SetTitle("Generated Electron p_{T} / GeV")
hist_total.GetYaxis().SetTitle("Counts / GeV")
hist_total.GetXaxis().SetTitleOffset(1.2)
hist_total.GetYaxis().SetTitleOffset(1.2)
hist_total.SetFillColor(ROOT.kBlue-9)
hist_total.SetLineColor(ROOT.kBlack)
hist_total.SetLineWidth(3)
hist_total.Draw("hist")

ROOT.gPad.SetLogy()
ROOT.gPad.Modified()
ROOT.gPad.Update()

alignStats(hist_total)

#Colours
hists_passed['Veto'].SetLineColor(ROOT.kGreen+3)
hists_passed['Loose'].SetLineColor(ROOT.kBlue+1)
hists_passed['Medium'].SetLineColor(ROOT.kOrange-2)
hists_passed['Tight'].SetLineColor(ROOT.kRed+1)
hists_passed['WP90'].SetLineColor(ROOT.kMagenta+2)
hists_passed['WP80'].SetLineColor(ROOT.kAzure+5)

for WP in WPs: 
   hists_passed[WP].SetFillColor(0)
   hists_passed[WP].SetLineWidth(3)
   hists_passed[WP].Draw("histsame")

ROOT.gPad.Modified()
ROOT.gPad.Update()

l1 = makeLegend()
l1.AddEntry("eleID", "Generated Electron p_{T}", "F")
l1.AddEntry("eleID_Veto", "Veto ID", "F")
l1.AddEntry("eleID_Loose", "Loose ID", "F")
l1.AddEntry("eleID_Medium", "Medium ID", "F")
l1.AddEntry("eleID_Tight", "Tight ID", "F")
l1.AddEntry("eleID_WP80", "MVA ID (WP80)", "F")
l1.AddEntry("eleID_WP90", "MVA ID (WP90)", "F")
l1.Draw()

################################################################################################################################################################################
#Efficiency curves
c1.cd(2)

effs = {}

for WP in sorted(hists_passed.keys()):
   print WP
   effs[WP] = ROOT.TEfficiency(hists_passed[WP], hist_total) #(passed, total)
   effs[WP].SetName("eff_" + WP)
   effs[WP].SetMarkerStyle(33)
   effs[WP].SetMarkerSize(1.5)
   effs[WP].SetLineWidth(2)
   if WP == 'Loose': effs['Loose'].Draw("AP")
   elif WP != 'Loose': effs[WP].Draw("sameP")

effs['Loose'].SetTitle("Electron ID Efficiencies (" + inputSample + " Sample) ; Generated Electron p_{T} / GeV ; Efficiency")
effs['Loose'].SetMarkerColor(ROOT.kBlue+1)
effs['Loose'].SetLineColor(ROOT.kBlue+1)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Modified()
ROOT.gPad.Update()
effs['Loose'].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)
effs['Loose'].GetPaintedGraph().SetMinimum(0)
effs['Loose'].GetPaintedGraph().SetMaximum(1)
effs['Loose'].GetPaintedGraph().GetXaxis().CenterTitle()
effs['Loose'].GetPaintedGraph().GetYaxis().CenterTitle()

#Colours
effs['Veto'].SetMarkerColor(ROOT.kGreen+3)
effs['Veto'].SetLineColor(ROOT.kGreen+3)
effs['Medium'].SetMarkerColor(ROOT.kOrange-2)
effs['Medium'].SetLineColor(ROOT.kOrange-2)
effs['Tight'].SetMarkerColor(ROOT.kRed+1)
effs['Tight'].SetLineColor(ROOT.kRed+1)
effs['WP90'].SetMarkerColor(ROOT.kMagenta+2)
effs['WP90'].SetLineColor(ROOT.kMagenta+2)
effs['WP90'].SetMarkerStyle(22)
effs['WP90'].SetMarkerSize(1)
effs['WP80'].SetMarkerColor(ROOT.kAzure+5)
effs['WP80'].SetLineColor(ROOT.kAzure+5)
effs['WP80'].SetMarkerStyle(22)
effs['WP80'].SetMarkerSize(1)

ROOT.gPad.Modified()
ROOT.gPad.Update()

l2 = makeLegend()
l2.AddEntry("eff_Veto", "Veto ID", "P")
l2.AddEntry("eff_Loose", "Loose ID", "P")
l2.AddEntry("eff_Medium", "Medium ID", "P")
l2.AddEntry("eff_Tight", "Tight ID", "P")
l2.AddEntry("eff_WP90", "MVA ID (WP90)", "P")
l2.AddEntry("eff_WP80", "MVA ID (WP80)", "P")

l2.Draw()

ROOT.gPad.Modified()
ROOT.gPad.Update()
c1.Modified()
c1.Update()

if save == 1:
   #Write to file
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronReconstruction/electronID/standard/efficiency/loop" #web address: http://www.hephy.at/user/mzarucki/plots/electronReconstruction/electronIdEfficiency
   
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
