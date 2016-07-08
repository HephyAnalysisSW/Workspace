#QCDabcdABCD3.py
import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.degTools import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.cutsEle import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2_analysisHephy13TeV import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_mAODv2_analysisHephy13TeV import getSamples
#from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2 import cmgTuplesPostProcessed
#from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_analysisHephy_13TeV import getSamples
#from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_PP_mAODv2_7412pass2_scan import getSamples

from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Set TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
#parser.add_argument("--isolation", dest = "isolation",  help = "Isolation (hybIso03/hybIso04)", type = str, default = "hybIso03")
parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "300")
parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "300")
parser.add_argument("--METloose", dest = "METloose",  help = "Loose MET Cut", type = str, default = "300")
parser.add_argument("--eleWP", dest = "eleWP",  help = "Electron WP", type = str, default = "Veto")
parser.add_argument("--removedCut", dest = "removedCut",  help = "Variable removed from electron ID", type = str, default = "None") #"sigmaEtaEta" "hOverE" "ooEmooP" "dEta" "dPhi" "d0" "dz" "MissingHits" "convVeto"
parser.add_argument("--enriched", dest = "enriched",  help = "EM enriched QCD?", type = bool, default = False)
parser.add_argument("--useData", dest = "useData",  help = "Use data", type = bool, default = True)
parser.add_argument("--logy", dest = "logy",  help = "Toggle logy", type = int, default = 0)
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
METloose = args.METloose
HTcut = args.HT
eleWP = args.eleWP
removedCut = args.removedCut
enriched = args.enriched
useData = args.useData
logy = args.logy
save = args.save

print makeLine()
print "HT | MET | Loose MET: ", HTcut, " | ", METcut, " | ", METloose
print makeLine()

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD3/plots" 
   if useData: savedir += "/data"
   if removedCut == "None": savedir += "/" + eleWP + "/HT" + HTcut + "MET" + METcut + "_looseMET" + METloose
   else: savedir += "/" + eleWP + "_no_" + removedCut + "/HT" + HTcut + "MET" + METcut + "_looseMET" + METloose
   if enriched == True: savedir += "_EMenriched"
   if not os.path.exists(savedir): os.makedirs(savedir)

#Samples
if enriched == True: qcd = "qcdem"
else: qcd = "qcd"

privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
backgrounds = ["w","tt", "z", "qcd"]

cmgPP = cmgTuplesPostProcessed()#mc_path, signal_path, data_path)

samplesList = backgrounds # + privateSignals
if useData: samplesList.append("dblind")

samples = getSamples(cmgPP = cmgPP, skim = 'presel', sampleList = samplesList, scan = False, useHT = True, getData = useData, blinded = True)

officialSignals = ["s300_290", "s300_270", "s300_250"] #FIXME: crosscheck if these are in allOfficialSignals

allOfficialSignals = samples.massScanList()
#allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
allSignals = privateSignals + allOfficialSignals
allSamples = allSignals + backgrounds

#selectedSamples = privateSignals + officialSignals + backgrounds
selectedSamples = ["qcd", "z", "tt", "w"]#, "s300_270"]

if useData: selectedSamples.append("dblind")

print makeLine()
print "Using samples:"
newLine()
for s in selectedSamples:
   if s: print samples[s].name,":",s
   else:
      print "!!! Sample " + sample + " unavailable."
      sys.exit(0)

suffix = "_HT" + HTcut + "_MET" + METcut + "_METloose" + METloose
if enriched == True: suffix += "_EMenriched"

if removedCut == "None": suffix += "_" + eleWP +"_manual"
else: suffix += "_" + eleWP +"_no_" + removedCut

QCDcuts = {}

#if collection == "LepGood": otherCollection = "LepOther"
#elif collection == "LepOther": otherCollection = "LepGood"

print makeLine()
print "Using LepAll collection."
print makeLine()

#Gets all cuts (electron, SR, CR) for given electron ID
if removedCut == "None": eleIDsel = electronIDs(ID = "standard", removedCut = "None", iso = False, collection = "LepAll")
else: eleIDsel = electronIDs(ID = "nMinus1", removedCut = removedCut, iso = False, collection = "LepAll")
#eleIDsel = electronIDs(ID = "nMinus1", removedCut = removedCut, iso = False, collection = "LepAll")
#eleIDsel = electronIDs(ID = "manual", removedCut = "None", iso = False, collection = "LepAll")
#eleIDsel = electronIDs(ID = "nMinus1", removedCut = "d0", iso = False, collection = "LepAll")

##for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
#for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

etaAcc = 2.1
eleSel = "abs(LepAll_pdgId) == 11 && abs(LepAll_eta) < " + str(etaAcc) + " && " + eleIDsel[eleWP]

hybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) < 5"
antiHybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) > 5"
#hybIsoCut = "((LepAll_absIso03 < 5) || LepAll_relIso03 < 0.2))"
#antiHybIsoCut = "((LepAll_absIso03 > 5) && (LepAll_relIso03 > 0.2))"

#Redefining electron pT in terms of selection
elePt = {}
elePt['I'] = "Max$(LepAll_pt*(" + eleSel + "&&" + hybIsoCut + "))"
elePt['anti-I'] = "Max$(LepAll_pt*(" + eleSel + "&&" + antiHybIsoCut + "))"

#Redefining mT in terms of selection
eleMt = {}
eleMt['I'] = "Max$(LepAll_mt*(" + eleSel + "&&" + hybIsoCut + "))"
eleMt['anti-I'] = "Max$(LepAll_mt*(" + eleSel + "&&" + antiHybIsoCut + "))"

#Redefining HI in terms of selection
absIso = {} 
absIso['I'] = "Max$(LepAll_absIso03*(" + eleSel + "&&" + hybIsoCut + "))"
absIso['anti-I'] = "Max$(LepAll_absIso03*(" + eleSel + "&&" + antiHybIsoCut + "))"

relIso = {} 
relIso['I'] = "Max$(LepAll_relIso03*(" + eleSel + "&&" + hybIsoCut + "))"
relIso['anti-I'] = "Max$(LepAll_relIso03*(" + eleSel + "&&" + antiHybIsoCut + "))"

hybIso = {} 
hybIso['I'] = "Max$((LepAll_relIso03*min(LepAll_pt, 25))*(" + eleSel + "&&" + hybIsoCut + "))"
hybIso['anti-I'] = "Max$((LepAll_relIso03*min(LepAll_pt, 25))*(" + eleSel + "&&" + antiHybIsoCut + "))"

#Redefining IP in terms of selection
absDxy = {}
absDxy['I'] = "Max$(abs(LepAll_dxy*(" + eleSel + "&&" + hybIsoCut + ")))"
absDxy['anti-I'] = "Max$(abs(LepAll_dxy*(" + eleSel + "&&" + antiHybIsoCut + ")))"

#Redefining sigmaEtaEta in terms of selection
sigmaEtaEta = {}
sigmaEtaEta['I'] = "Max$(abs(LepAll_sigmaIEtaIEta*(" + eleSel + "&&" + hybIsoCut + ")))"
sigmaEtaEta['anti-I'] = "Max$(abs(LepAll_sigmaIEtaIEta*(" + eleSel + "&&" + antiHybIsoCut + ")))"

QCD = {}

presel = CutClass("presel_SR", [
   ["METloose","met >" + METloose], #looser MET for B & D regions
   ["HT","ht_basJet >" + HTcut],
   ["ISR110", "nIsrJet >= 1"],
   ["No3rdJet60","nVetoJet <= 2"],
   ["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
   #["anti-AntiQCD", "vetoJet_dPhi_j1j2 > 2.5"],
   #["anti-HybIso", "Sum$(" + eleSel + "&&" + antiHybIsoCut + ") == 1"],
   #["anti-dxy", "Max$(abs(" + lep + "_dxy*(" + eleSel + "&&" + antiHybIsoCut + "))) > 0.02"],
   ], baseCut = None) #allCuts['None']['presel'])

#SR 
if not useData:
   QCD['SR'] = CutClass("QCD_SR", [
      ["elePt<30", elePt['I'] + " < 30"],
      ["MET", "met >" + METcut], #applied
      ["I", "Sum$(" + eleSel + "&&" + hybIsoCut + ") == 1"],
      ["A", "vetoJet_dPhi_j1j2 < 2.5"],
      ], baseCut = presel)

#nA
QCD['MI_A'] = CutClass("QCD_MI_A", [
   ["elePt<30", elePt['anti-I'] + " < 30"],
   ["anti-I", "Sum$(" + eleSel + "&&" + antiHybIsoCut + ") == 1"], #inverted
   ["A", "vetoJet_dPhi_j1j2 < 2.5"], #applied
   ], baseCut = presel)

#nI
QCD['A_MI'] = CutClass("QCD_A_MI", [
   ["elePt<30", elePt['I'] + " < 30"],
   ["MET", "met >" + METcut], #applied
   ["I", "Sum$(" + eleSel + "&&" + hybIsoCut + ") == 1"], #applied
   ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
   ], baseCut = presel)

#nIDA
QCD['MIA'] = CutClass("QCD_MIA", [
   ["elePt<30", elePt['anti-I'] + " < 30"],
   ["anti-I", "Sum$(" + eleSel + "&&" + antiHybIsoCut + ") == 1"], #inverted
   ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
   ], baseCut = presel)

plotsList = {}
plotDict = {}
plotsDict = {}
plots = {}
plots2 = {}

abcd = {'SR':'I', 'MI_A':'anti-I', 'A_MI':'I', 'MIA':'anti-I'}
plotSamples = [qcd, "z", "tt", "w"]

if useData: 
   del abcd['SR']
   plotSamples.append("dblind")

for sel in abcd:
   plotDict[sel] = {\
      "elePt_" + sel:{'var':elePt[abcd[sel]], "bins":[10, 0, 50], "decor":{"title": "Electron pT Plot" ,"x":"Electron p_{T} / GeV" , "y":"Events", 'log':[0, logy,0]}}, 
      "absIso_" + sel:{'var':absIso[abcd[sel]], "bins":[4, 0, 20], "decor":{"title": "Electron absIso Plot" ,"x":"I_{abs} / GeV" , "y":"Events", 'log':[0,logy,0]}}, 
      "relIso_" + sel:{'var':relIso[abcd[sel]], "bins":[20, 0, 5], "decor":{"title": "Electron relIso Plot" ,"x":"I_{rel}" , "y":"Events", 'log':[0,logy,0]}}, 
      "hybIso_" + sel:{'var':hybIso[abcd[sel]], "bins":[10, 0, 25], "decor":{"title": "Electron hybIso Plot" ,"x":"HI = I_{rel}*min(p_{T}, 25 GeV)" , "y":"Events", 'log':[0,logy,0]}},
      "hybIso2_" + sel:{'var':"(log(1 + " + hybIso[abcd[sel]] + ")/log(1+5))", "bins":[8, 0, 4], "decor":{"title": "Electron hybIso Plot" ,"x":"log(1+HI)/log(1+5)" , "y":"Events", 'log':[0,logy,0]}},
      "absDxy_" + sel:{'var':absDxy[abcd[sel]], "bins":[20, 0, 0.1], "decor":{"title": "Electron |dxy| Plot" ,"x":"|dxy|" , "y":"Events", "log":[0,logy,0]}},
      "delPhi_" + sel:{'var':"vetoJet_dPhi_j1j2", "bins":[8, 0, 3.14], "decor":{"title": "deltaPhi(j1,j2) Plot" ,"x":"#Delta#phi(j1,j2)" , "y":"Events", 'log':[0,logy,0]}},
      "eleMt_" + sel:{'var':eleMt[abcd[sel]], "bins":[10,0,100], "decor":{"title": "mT Plot" ,"x":"m_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
      "MET_" + sel:{'var':"met", "bins":[50,0,500], "decor":{"title": "MET Plot" ,"x":"Missing E_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
      "HT_" + sel:{'var':"ht_basJet", "bins":[50,0,500], "decor":{"title": "HT Plot","x":"H_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
      "sigmaEtaEta_" + sel:{'var':sigmaEtaEta[abcd[sel]], "bins":[40,0,0.04], "decor":{"title": "#sigma#eta#eta Plot","x":"#sigma#eta#eta" , "y":"Events", 'log':[0,logy,0]}},
      "weight_" + sel:{'var':"weight", "bins":[20,0,500], "decor":{"title": "Weight Plot","x":"Event Weight" , "y":"Events", 'log':[0,1,0]}}
   }

   plotsList[sel] = ["elePt_" + sel, "absIso_" + sel, "relIso_" + sel,"hybIso_" + sel, "hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel, "eleMt_" + sel, "MET_" + sel, "HT_" + sel, "sigmaEtaEta_" + sel, "weight_" + sel]
   #plotsList[sel] = ["elePt_" + sel, "hybIso2_" + sel, "delPhi_" + sel, "eleMt_" + sel, "MET_" + sel, "HT_" + sel, "sigmaEtaEta_" + sel, "weight_" + sel]
   #plotsList[sel] = ["hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel]
   plotsDict[sel] = Plots(**plotDict[sel])
   plots[sel] = getPlots(samples, plotsDict[sel], QCD[sel], plotSamples, plotList = plotsList[sel], addOverFlowBin='upper')
   plots2[sel] = drawPlots(plots[sel], fom=False, save=False, plotMin = 0.1)
   
   #Save canvas
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      if not os.path.exists("%s/%s/root"%(savedir, sel)): os.makedirs("%s/%s/root"%(savedir, sel))
      if not os.path.exists("%s/%s/pdf"%(savedir, sel)): os.makedirs("%s/%s/pdf"%(savedir, sel))
   
      for canv in plots2[sel]['canvs']:
         #if plot['canvs'][canv][0]:
         plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/%s%s.png"%(savedir, sel, canv, suffix))
         plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/root/%s%s.root"%(savedir, sel, canv, suffix))
         plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/pdf/%s%s.pdf"%(savedir, sel, canv, suffix))
