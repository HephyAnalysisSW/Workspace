#QCDabcdABCD2.py
import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.degTools import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.cutsEle import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_mAODv2_analysisHephy13TeV import getSamples
from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2_analysisHephy13TeV import cmgTuplesPostProcessed
#from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2 import cmgTuplesPostProcessed
#from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_analysisHephy_13TeV import getSamples
#from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_PP_mAODv2_7412pass2_scan import getSamples

from array import array
from math import pi, sqrt #cos, sin, sinh, log

ROOT.setTDRStyle(1)
ROOT.gStyle.SetOptStat(0) #1111 #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

#Input options
parser = argparse.ArgumentParser(description = "Input options")
#parser.add_argument("--isolation", dest = "isolation",  help = "Isolation (hybIso03/hybIso04)", type = str, default = "hybIso03")
parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "200")
parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "200")
parser.add_argument("--eleWP", dest = "eleWP",  help = "Electron WP", type = str, default = "Veto")
#parser.add_argument("--enriched", dest = "enriched",  help = "EM enriched QCD?", type = bool, default = False)
parser.add_argument("--save", dest = "save",  help = "Toggle save", type = int, default = 1)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
#isolation = args.isolation
METcut = args.MET
HTcut = args.HT
eleWP = args.eleWP
#enriched = args.enriched
save = args.save

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD2/plots/ABCD"
   if not os.path.exists(savedir): os.makedirs(savedir)

#for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
#for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

#Samples
#if enriched == True: qcd = "qcdem"
#else: qcd = "qcd"

privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
backgrounds = ["w","tt", "z", "qcd"]

cmgPP = cmgTuplesPostProcessed()#mc_path, signal_path, data_path)

samplesList = backgrounds # + privateSignals
samples = getSamples(cmgPP = cmgPP, skim = 'presel', sampleList = samplesList, scan = False, useHT = True, getData = False)

officialSignals = ["s300_290", "s300_270", "s300_250"] #FIXME: crosscheck if these are in allOfficialSignals

allOfficialSignals = samples.massScanList()
#allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
allSignals = privateSignals + allOfficialSignals
allSamples = allSignals + backgrounds

#selectedSamples = privateSignals + officialSignals + backgrounds
selectedSamples = ["qcd", "z", "tt", "w"]#, "s300_270"]

print makeLine()
print "Using samples:"
newLine()
for s in selectedSamples:
   if s: print samples[s].name,":",s
   else:
      print "!!! Sample " + sample + " unavailable."
      sys.exit(0)

suffix = "_HT" + HTcut + "_MET" + METcut
#if enriched == True: suffix += "_EMenriched"

suffix += "_" + eleWP +"_manual"
#if removedCut == "None": suffix += "_" + eleWP +"_manual"
#else: suffix += "_" + eleWP +"_no_" + removedCut

print makeLine()
print "UsingLepAll collection."
print makeLine()

#Gets all cuts (electron, SR, CR) for given electron ID
eleIDsel = electronIDs(ID = "nMinus1", removedCut = "d0", iso = False, collection = collection)
eleIDsel_other = electronIDs(ID = "nMinus1", removedCut = "d0", iso = False, collection = otherCollection)

etaAcc = 2.1
eleSel = "abs(LepAll_pdgId) == 11 && abs(LepAll_eta) < " + str(etaAcc) + " && " + eleIDsel[eleWP]

#Cuts
dxyCut = "abs(LepAll_dxy) < 0.02"
looseDxyCut = "abs(LepAll_dxy) < 0.05"
 
hybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) < 5" #hybIsoCut = "((LepAll_absIso03 < 5) || LepAll_relIso03 < 0.2))"
antiHybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) > 5" #antiHybIsoCut = "((LepAll_absIso03 > 5) && (LepAll_relIso03 > 0.2))"

#Redefining electron pT in terms of selection
elePt = {} 
#elePt = "Max$(LepAll_pt*(" + eleSel + "))"
#elePt_I = "Max$(LepAll_pt*(" + eleSel + "&&" + antiHybIsoCut + "))"
#elePt_D = "Max$(LepAll_pt*(" + eleSel + "&&" + looseDxyCut + "))"
elePt['SR'] = "Max$(LepAll_pt*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
elePt['ID'] = "Max$(LepAll_pt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + looseDxyCut + "))"
#elePt['I_D'] = "Max$(LepAll_pt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
#elePt['D_I'] = "Max$(LepAll_pt*(" + eleSel + "&&" + hybIsoCut + "&&" + looseDxyCut + "))"

#Redefining mT in terms of selection
eleMt = {} 
eleMt['SR'] = "Max$(LepAll_mt*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
eleMt['ID'] = "Max$(LepAll_mt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + looseDxyCut + "))"
#eleMt['I_D'] = "Max$(LepAll_mt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
#eleMt['D_I'] = "Max$(LepAll_mt*(" + eleSel + "&&" + hybIsoCut + "&&" + looseDxyCut + "))"

#Redefining isolation in terms of selection
#absIso = "Max$(LepAll_absIso03*(" + eleSel + "))"
#relIso = "Max$(LepAll_relIso03*(" + eleSel + "))"

absIso = {}   
absIso['SR'] = "Max$(LepAll_absIso03*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
absIso['ID'] = "Max$(LepAll_absIso03*(" + eleSel + "&&" + antiHybIsoCut + "&&" + looseDxyCut + "))"
#absIso['I_D'] = "Max$(LepAll_absIso03*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
#absIso['D_I'] = "Max$(LepAll_absIso03*(" + eleSel + "&&" + hybIsoCut + "&&" + looseDxyCut + "))"

relIso = {}
relIso['SR'] = "Max$(LepAll_relIso03*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
relIso['ID'] = "Max$(LepAll_relIso03*(" + eleSel + "&&" + antiHybIsoCut + "&&" + looseDxyCut + "))"
#relIso['I_D'] = "Max$(LepAll_relIso03*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
#relIso['D_I'] = "Max$(LepAll_relIso03*(" + eleSel + "&&" + hybIsoCut + "&&" + looseDxyCut + "))"

#hybIso = "Max$((LepAll_relIso03*min(LepAll_pt, 25))*(" + eleSel + "))"
#hybIso_I = "Max$((LepAll_relIso03*min(LepAll_pt, 25))*(" + eleSel + "&&" + antiHybIsoCut + "))"
#hybIso_D = "Max$((LepAll_relIso03*min(LepAll_pt, 25))*(" + eleSel + "&&" + looseDxyCut + "))"
hybIso = {}   
hybIso['SR'] = "Max$((LepAll_relIso03*min(LepAll_pt, 25))*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
hybIso['ID'] = "Max$((LepAll_relIso03*min(LepAll_pt, 25))*(" + eleSel + "&&" + antiHybIsoCut + "&&" + looseDxyCut + "))"
#hybIso['I_D'] = "Max$((LepAll_relIso03*min(LepAll_pt, 25))*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
#hybIso['D_I'] = "Max$((LepAll_relIso03*min(LepAll_pt, 25))*(" + eleSel + "&&" + hybIsoCut + "&&" + looseDxyCut + "))"

#absDxy = "Max$(abs(LepAll_dxy*(" + eleSel + ")))"
absDxy = {}   
absDxy['SR'] = "Max$(LepAll_dxy*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
absDxy['ID'] = "Max$(abs(LepAll_dxy*(" + eleSel + "&&" + antiHybIsoCut + "&&" + looseDxyCut + ")))"
#absDxy['I_D'] = "Max$(abs(LepAll_dxy*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + ")))"
#absDxy['D_I'] = "Max$(abs(LepAll_dxy*(" + eleSel + "&&" + hybIsoCut + "&&" + looseDxyCut + ")))"

presel = CutClass("presel_SR", [
   ["MET","met > " + METcut],
   ["HT","ht_basJet > " + HTcut],
   ["ISR110", "nIsrJet >= 1"],
   ["No3rdJet60","nVetoJet <= 2"],
   ["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
   #["elePt<30", elePt + " < 30"],
   #["anti-AntiQCD", "vetoJet_dPhi_j1j2 > 2.5"],
   #["anti-HybIso", "Sum$(" + eleSel + "&&" + antiHybIsoCut + ") == 1"],
   #["anti-dxy", "Max$(abs(LepAll_dxy*(" + eleSel + "&&" + antiHybIsoCut + "))) > 0.02"],
   ], baseCut = None) #allCuts['None']['presel'])

QCD = {} 

#SR 
QCD['SR'] = CutClass("QCD_SR", [
   ["elePt<30", elePt['SR'] + " < 30"],
   ["A", "vetoJet_dPhi_j1j2 < 2.5"],
   ["ID", "Sum$(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + ") == 1"],
   ], baseCut = presel)

#nA
QCD['ID_A'] = CutClass("QCD_ID_A", [
   ["elePt<30", elePt['ID'] + " < 30"],
   ["A", "vetoJet_dPhi_j1j2 < 2.5"], #applied
   ["anti-I+D", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + looseDxyCut + ") == 1"], #inverted, loose
   ], baseCut = presel)

#nI
QCD['A_ID'] = CutClass("QCD_A_ID", [
   ["elePt<30", elePt['SR'] + " < 30"],
   ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
   ["I+loose-D", "Sum$(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + ") == 1"], #applied, applied
   ], baseCut = presel)

#nIDA
QCD['IDA'] = CutClass("QCD_IDA", [
   ["elePt<30", elePt['ID'] + " < 30"],
   ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
   ["anti-I+loose-D", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + looseDxyCut + ") == 1"], #inverted, loose
   ], baseCut = presel)

plotDict = {}
plotsList = {} 
plotsDict = {} 
plots = {} 
plots2 = {} 

selections = {'SR':'SR', 'ID_A':'ID', 'A_ID':'SR', 'IDA':'ID'}

for sel in selections:
   plotDict[sel] = {\
      "elePt_" + sel:{'var':elePt[selections[sel]], "bins":[10, 0, 50], "decor":{"title": "Electron pT Plot" ,"x":"Electron p_{T} / GeV" , "y":"Events", 'log':[0, logy,0]}},
      "absIso_" + sel:{'var':absIso[selections[sel]], "bins":[4, 0, 20], "decor":{"title": "Electron absIso Plot" ,"x":"I_{abs} / GeV" , "y":"Events", 'log':[0,logy,0]}},
      "relIso_" + sel:{'var':relIso[selections[sel]], "bins":[20, 0, 5], "decor":{"title": "Electron relIso Plot" ,"x":"I_{rel}" , "y":"Events", 'log':[0,logy,0]}}, 
      "hybIso_" + sel:{'var':hybIso[selections[sel]], "bins":[10, 0, 25], "decor":{"title": "Electron hybIso Plot" ,"x":"HI = I_{rel}*min(p_{T}, 25 GeV)" , "y":"Events", 'log':[0,logy,0]}},
      "hybIso2_" + sel:{'var':"(log(1 + " + hybIso[selections[sel]] + ")/log(1+5))", "bins":[8, 0, 4], "decor":{"title": "Electron hybIso Plot" ,"x":"log(1+HI)/log(1+5)" , "y":"Events", 'log':[0,logy,0]}},
      "absDxy_" + sel:{'var':absDxy[selections[sel]], "bins":[6, 0, 0.06], "decor":{"title": "Electron |dxy| Plot" ,"x":"|dxy|" , "y":"Events", "log":[0,logy,0]}},
      "delPhi_" + sel:{'var':"vetoJet_dPhi_j1j2", "bins":[0, 0, 3.14], "decor":{"title": "deltaPhi(j1,j2) Plot" ,"x":"#Delta#phi(j1,j2)" , "y":"Events", 'log':[0,logy,0]}},
      "eleMt_" + sel:{'var':eleMt[selections[sel]], "bins":[10,0,100], "decor":{"title": "mT Plot" ,"x":"m_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
      "MET_" + sel:{'var':"met", "bins":[20,100,500], "decor":{"title": "MET Plot" ,"x":"Missing E_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
      "HT_" + sel:{'var':"ht_basJet", "bins":[20,100,500], "decor":{"title": "HT Plot","x":"H_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}}
   }

   plotsList[sel] = ["elePt_" + sel, "absIso_" + sel, "relIso_" + sel,"hybIso_" + sel, "hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel, "eleMt_" + sel, "MET_" + sel, "HT_" + sel]
   plotsDict[sel] = Plots(**plotDict[sel])

   plots[sel] = getPlots(samples, plotsDict[sel], QCD[sel], selectedSamples, plotList = plotsList[sel], addOverFlowBin='upper')
   plots2[sel] = drawPlots(plots[sel], fom=False, save=False, plotMin = 0.1)

ROOT.gPad.Modified()
ROOT.gPad.Update()

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   for sel in selections:
      if not os.path.exists("%s/%s/root"%(savedir, sel)): os.makedirs("%s/%s/root"%(savedir, sel))
      if not os.path.exists("%s/%s/pdf"%(savedir, sel)): os.makedirs("%s/%s/pdf"%(savedir, sel))
      for canv in plots2[sel]['canvs']:
         if plots2[sel]['canvs'][canv][0]:
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/%s.png"%(savedir, sel, canv))
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/root/%s.root"%(savedir, sel, canv))
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/pdf/%s.pdf"%(savedir, sel, canv))
