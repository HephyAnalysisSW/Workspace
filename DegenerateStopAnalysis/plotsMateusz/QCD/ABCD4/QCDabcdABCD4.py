#QCDabcdABCD4.py
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

ROOT.setTDRStyle(1)
ROOT.gStyle.SetOptStat(0) #1111 #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

#Input options
parser = argparse.ArgumentParser(description = "Input options")
#parser.add_argument("--isolation", dest = "isolation",  help = "Isolation (hybIso03/hybIso04)", type = str, default = "hybIso03")
parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "300")
parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "300")
#parser.add_argument("--METloose", dest = "METloose",  help = "Loose MET Cut", type = str, default = "300")
parser.add_argument("--eleWP", dest = "eleWP",  help = "Electron WP", type = str, default = "Veto")
#parser.add_argument("--removedCut", dest = "removedCut",  help = "Variable removed from electron ID", type = str, default = "None") #"sigmaEtaEta" "hOverE" "ooEmooP" "dEta" "dPhi" "d0" "dz" "MissingHits" "convVeto"
parser.add_argument("--enriched", dest = "enriched",  help = "EM enriched QCD?", type = bool, default = False)
parser.add_argument("--getData", dest = "getData",  help = "Use data", type = bool, default = False)
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
#METloose = args.METloose
HTcut = args.HT
eleWP = args.eleWP
#removedCut = args.removedCut
enriched = args.enriched
getData = args.getData
logy = args.logy
save = args.save

#print makeLine()
#print "HT | MET | Loose MET: ", HTcut, " | ", METcut, " | ", METloose
#print makeLine()

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD4/plots"
   if getData: savedir += "/data"
   savedir += "/" + eleWP + "/HT" + HTcut + "MET" + METcut #+ "_looseMET" + METloose
   if enriched == True: savedir += "_EMenriched"
   if not os.path.exists(savedir): os.makedirs(savedir)


#Samples
if enriched == True: qcd = "qcdem"
else: qcd = "qcd"

privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
backgrounds = ["w","tt", "z", "qcd"]

cmgPP = cmgTuplesPostProcessed()#mc_path, signal_path, data_path)

samplesList = backgrounds # + privateSignals
if getData: samplesList.append("dblind")

samples = getSamples(cmgPP = cmgPP, skim = 'presel', sampleList = samplesList, scan = False, useHT = True, getData = getData)

officialSignals = ["s300_290", "s300_270", "s300_250"] #FIXME: crosscheck if these are in allOfficialSignals

allOfficialSignals = samples.massScanList()
#allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
allSignals = privateSignals + allOfficialSignals
allSamples = allSignals + backgrounds

#selectedSamples = privateSignals + officialSignals + backgrounds
selectedSamples = ["qcd", "z", "tt", "w"]#, "s300_270"]

if getData: selectedSamples.append("dblind")

print makeLine()
print "Using samples:"
newLine()
for s in selectedSamples:
   if s: print samples[s].name,":",s
   else:
      print "!!! Sample " + sample + " unavailable."
      sys.exit(0)

suffix = "_HT" + HTcut + "_MET" + METcut #+ "_METloose" + METloose
if enriched == True: suffix += "_EMenriched"

QCDcuts = {}

print makeLine()
print "Using LepAll collection."
print makeLine()

#Gets all cuts (electron, SR, CR) for given electron ID
eleIDsel = electronIDs(ID = "nMinus1", removedCut = "sigmaEtaEta", iso = False, collection = "LepAll")
#eleIDsel = electronIDs(ID = "manual", removedCut = "None", iso = False, collection = "LepAll")
#eleIDsel = electronIDs(ID = "nMinus1", removedCut = "d0", iso = False, collection = "LepAll")

##for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
#for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

#Geometrical cuts
etaAcc = 2.1
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap

eleSel = "abs(LepAll_pdgId) == 11 && abs(LepAll_eta) < " + str(etaAcc) + " && " + eleIDsel[eleWP]

geoSel= {\
   'EB':"(abs(LepAll_eta) <= " + str(ebeeSplit) + ")",
   'EE':"(abs(LepAll_eta) > " + str(ebeeSplit) + " && abs(LepAll_eta) < " + str(etaAcc) + ")"}

sigmaEtaEtaCuts = {\
   'Veto':{'EB':0.0114, 'EE':0.0352},
   'Loose':{'EB':0.0103, 'EE':0.0301},
   'Medium':{'EB':0.0101, 'EE':0.0283},
   'Tight':{'EB':0.0101, 'EE':0.0279}}

sigmaEtaEtaCut = "((" + geoSel['EB'] + " && LepAll_sigmaIEtaIEta <" + str(sigmaEtaEtaCuts[eleWP]['EB']) + ") || (" + geoSel['EE'] + "&& LepAll_sigmaIEtaIEta <" + str(sigmaEtaEtaCuts[eleWP]['EE']) + "))"
antiSigmaEtaEtaCut = "((" + geoSel['EB'] + " && LepAll_sigmaIEtaIEta >" + str(sigmaEtaEtaCuts[eleWP]['EB']) + ") || (" + geoSel['EE'] + "&& LepAll_sigmaIEtaIEta >" + str(sigmaEtaEtaCuts[eleWP]['EE']) + "))"

hybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) < 5"
antiHybIsoCut = "(LepAll_relIso03*min(LepAll_pt, 25)) > 5"
#hybIsoCut = "((LepAll_absIso03 < 5) || LepAll_relIso03 < 0.2))"
#antiHybIsoCut = "((LepAll_absIso03 > 5) && (LepAll_relIso03 > 0.2))"

#Redefining electron pT in terms of selection
elePt = {}
elePt['SR'] = "Max$(LepAll_pt*(" + combineCutsList([eleSel, hybIsoCut, sigmaEtaEtaCut]) + "))"
elePt['IS'] = "Max$(LepAll_pt*(" + combineCutsList([eleSel, antiHybIsoCut, antiSigmaEtaEtaCut]) + "))"
elePt['I_S'] = "Max$(LepAll_pt*(" + combineCutsList([eleSel, antiHybIsoCut, sigmaEtaEtaCut]) + "))"
elePt['S_I'] = "Max$(LepAll_pt*(" + combineCutsList([eleSel, hybIsoCut, antiSigmaEtaEtaCut]) + "))"

#Redefining mT in terms of selection
eleMt = {}
eleMt['SR'] = "Max$(LepAll_mt*(" + combineCutsList([eleSel, hybIsoCut, sigmaEtaEtaCut]) + "))"
eleMt['IS'] = "Max$(LepAll_mt*(" + combineCutsList([eleSel, antiHybIsoCut, antiSigmaEtaEtaCut]) + "))"
eleMt['I_S'] = "Max$(LepAll_mt*(" + combineCutsList([eleSel, antiHybIsoCut, sigmaEtaEtaCut]) + "))"
eleMt['S_I'] = "Max$(LepAll_mt*(" + combineCutsList([eleSel, hybIsoCut, antiSigmaEtaEtaCut]) + "))"

#Redefining HI in terms of selection
absIso = {} 
absIso['SR'] = "Max$(LepAll_absIso03*(" + combineCutsList([eleSel, hybIsoCut, sigmaEtaEtaCut]) + "))"
absIso['IS'] = "Max$(LepAll_absIso03*(" + combineCutsList([eleSel, antiHybIsoCut, antiSigmaEtaEtaCut]) + "))"
absIso['I_S'] = "Max$(LepAll_absIso03*(" + combineCutsList([eleSel, antiHybIsoCut, sigmaEtaEtaCut]) + "))"
absIso['S_I'] = "Max$(LepAll_absIso03*(" + combineCutsList([eleSel, hybIsoCut, antiSigmaEtaEtaCut]) + "))"

relIso = {} 
relIso['SR'] = "Max$(LepAll_relIso03*(" + combineCutsList([eleSel, hybIsoCut, sigmaEtaEtaCut]) + "))"
relIso['IS'] = "Max$(LepAll_relIso03*(" + combineCutsList([eleSel, antiHybIsoCut, antiSigmaEtaEtaCut]) + "))"
relIso['I_S'] = "Max$(LepAll_relIso03*(" + combineCutsList([eleSel, antiHybIsoCut, sigmaEtaEtaCut]) + "))"
relIso['S_I'] = "Max$(LepAll_relIso03*(" + combineCutsList([eleSel, hybIsoCut, antiSigmaEtaEtaCut]) + "))"

hybIso = {} 
hybIso['SR'] = "Max$((LepAll_relIso03*min(LepAll_pt, 25))*(" + combineCutsList([eleSel, hybIsoCut, sigmaEtaEtaCut]) + "))"
hybIso['IS'] = "Max$((LepAll_relIso03*min(LepAll_pt, 25))*(" + combineCutsList([eleSel, antiHybIsoCut, antiSigmaEtaEtaCut]) + "))"
hybIso['I_S'] = "Max$((LepAll_relIso03*min(LepAll_pt, 25))*(" + combineCutsList([eleSel, antiHybIsoCut, sigmaEtaEtaCut]) + "))"
hybIso['S_I'] = "Max$((LepAll_relIso03*min(LepAll_pt, 25))*(" + combineCutsList([eleSel, hybIsoCut, antiSigmaEtaEtaCut]) + "))"

#Redefining IP in terms of selection
absDxy = {}
absDxy['SR'] = "Max$(abs(LepAll_dxy*(" + combineCutsList([eleSel, hybIsoCut, sigmaEtaEtaCut]) + ")))"
absDxy['IS'] = "Max$(abs(LepAll_dxy*(" + combineCutsList([eleSel, antiHybIsoCut, antiSigmaEtaEtaCut]) + ")))"
absDxy['I_S'] = "Max$(abs(LepAll_dxy*(" + combineCutsList([eleSel, antiHybIsoCut, sigmaEtaEtaCut]) + ")))"
absDxy['S_I'] = "Max$(abs(LepAll_dxy*(" + combineCutsList([eleSel, hybIsoCut, antiSigmaEtaEtaCut]) + ")))"

#Redefining sigmaEtaEta in terms of selection
sigmaEtaEta = {}
sigmaEtaEta['SR'] = "Max$(LepAll_sigmaIEtaIEta*(" + combineCutsList([eleSel, hybIsoCut, sigmaEtaEtaCut]) + "))"
sigmaEtaEta['IS'] = "Max$(LepAll_sigmaIEtaIEta*(" + combineCutsList([eleSel, antiHybIsoCut, antiSigmaEtaEtaCut]) + "))"
sigmaEtaEta['I_S'] = "Max$(LepAll_sigmaIEtaIEta*(" + combineCutsList([eleSel, antiHybIsoCut, sigmaEtaEtaCut]) + "))"
sigmaEtaEta['S_I'] = "Max$(LepAll_sigmaIEtaIEta*(" + combineCutsList([eleSel, hybIsoCut, antiSigmaEtaEtaCut]) + "))"

QCD = {}

presel = CutClass("presel_SR", [
   #["METloose","met >" + METloose], #looser MET for B & D regions
   ["MET","met >" + METcut],
   ["HT","ht_basJet >" + HTcut],
   ["ISR110", "nIsrJet >= 1"],
   ["No3rdJet60","nVetoJet <= 2"],
   ["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
   #["eleSel", "Sum$(" + eleSel + ") == 1"],
   #["anti-AntiQCD", "vetoJet_dPhi_j1j2 > 2.5"],
   #["anti-HybIso", "Sum$(" + eleSel + "&&" + antiHybIsoCut + ") == 1"],
   #["anti-dxy", "Max$(abs(" + lep + "_dxy*(" + eleSel + "&&" + antiHybIsoCut + "))) > 0.02"],
   ], baseCut = None) #allCuts['None']['presel'])

if not getData:
   QCD['SR'] = CutClass("QCD_SR", [
      ["elePt<30", elePt['SR'] + " < 30"],
      ["A", "vetoJet_dPhi_j1j2 < 2.5"],
      ["IS", "Sum$(" + eleSel + "&&" + hybIsoCut + "&&" + sigmaEtaEtaCut + ") == 1"],
      ], baseCut = presel)

QCD['IS_A'] = CutClass("QCD_IS_A", [
   ["elePt<30", elePt['IS'] + " < 30"],
   ["A", "vetoJet_dPhi_j1j2 < 2.5"], #applied
   ["anti-IS", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiSigmaEtaEtaCut + ") == 1"], #inverted, inverted
   ], baseCut = presel)

QCD['SA_I'] = CutClass("QCD_SA_I", [
   ["elePt<30", elePt['S_I'] + " < 30"],
   ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
   ["I+anti-S", "Sum$(" + eleSel + "&&" + hybIsoCut + "&&" + antiSigmaEtaEtaCut + ") == 1"], #applied, inverted
   ], baseCut = presel)

QCD['IA_S'] = CutClass("QCD_IA_S", [
   ["elePt<30", elePt['I_S'] + " < 30"],
   ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
   ["anti-I+S", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + sigmaEtaEtaCut + ") == 1"], #inverted, applied
   ], baseCut = presel)

QCD['ISA'] = CutClass("QCD_ISA", [
   ["elePt<30", elePt['IS'] + " < 30"],
   ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
   ["anti-IS", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiSigmaEtaEtaCut + ") == 1"], #inverted, inverted
   ], baseCut = presel)

plotsList = {}
plotDict = {}
plotsDict = {}
plots = {}
plots2 = {}

abcd = {'SR':'SR', 'IS_A':'IS', 'SA_I':'S_I', 'IA_S':'I_S', 'ISA':'IS'}
plotSamples = [qcd, "z", "tt", "w"]

if getData: 
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
      "sigmaEtaEta_" + sel:{'var':sigmaEtaEta[abcd[sel]], "bins":[50,0,0.05], "decor":{"title": "#sigma#eta#eta Plot","x":"#sigma#eta#eta" , "y":"Events", 'log':[0,logy,0]}},
      "weight_" + sel:{'var':"weight", "bins":[20,0,500], "decor":{"title": "Weight Plot","x":"Event Weight" , "y":"Events", 'log':[0,1,0]}}
   }

   plotsList[sel] = ["elePt_" + sel, "absIso_" + sel, "relIso_" + sel,"hybIso_" + sel, "hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel, "eleMt_" + sel, "MET_" + sel, "HT_" + sel, "sigmaEtaEta_" + sel, "weight_" + sel]
   #plotsList[sel] = ["hybIso2_" + sel, "sigmaEtaEta_" + sel, "weight_" + sel]
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
