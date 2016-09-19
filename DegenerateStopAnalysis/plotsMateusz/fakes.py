# fakes.py
# Script for plotting MC fakes in SR
# Mateusz Zarucki 2016

import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import Plots, getPlots, drawPlots, setup_style
from Workspace.DegenerateStopAnalysis.toolsMateusz.eleWPs import *
from Workspace.DegenerateStopAnalysis.tools.getSamples_8012 import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#TDR style
setup_style()

#Samples
privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
backgrounds = ["w","tt", "z", "qcd"]

cmgPP = cmgTuplesPostProcessed()#mc_path, signal_path, data_path)

samplesList = backgrounds # + privateSignals
samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = False, useHT = True, getData = False)

officialSignals = ["s300_290", "s300_270", "s300_250"] #FIXME: crosscheck if these are in allOfficialSignals

allOfficialSignals = samples.massScanList()
allSignals = privateSignals + allOfficialSignals
allSamples = allSignals + backgrounds

#selectedSamples = privateSignals + officialSignals + backgrounds
selectedSamples = ["qcd", "z", "tt", "w"]

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--save", dest = "save",  help = "Toggle save", type = int, default = 1)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
save = args.save

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakes"%tag

#Gets all cuts (electron, SR, CR) for given electron ID
eleIDsel = electronIDs(ID = "standard", removedCut = "None", iso = "hybIso03")

#selectedSamples = privateSignals + officialSignals + backgrounds
selectedSamples = ["qcd", "z", "tt", "w"]#, "s300_270"]"qcd", 

print makeLine()
print "Using samples:"
newLine()
for s in selectedSamples:
   if s: print samples[s].name,":",s
   else: 
      print "!!! Sample " + sample + " unavailable."
      sys.exit(0)

etaAcc = 2.1
fakeEleSel = "abs(LepAll_pdgId) == 11 && abs(LepAll_eta) < " + str(etaAcc) + " && " + eleIDsel['Veto'] + " && LepAll_mcMatchId == 0" #(LepAll_relIso03*min(LepAll_pt, 25)) < 5 

fakePt = "Max$(LepAll_pt*(" + fakeEleSel + "))"
fakeMt = "Max$(LepAll_mt*(" + fakeEleSel + "))"

fakes = CutClass("fakes", [
   ["MET300","met > 300"],
   ["HT300","ht_basJet > 300"],
   ["ISR110", "nIsrJet >= 1"],
   ["No3rdJet60","nVetoJet <= 2"],
   ["anti-QCD", "vetoJet_dPhi_j1j2 < 2.5"],
   ["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
   ["fake", "Sum$(" + fakeEleSel + ") == 1"],
   ["Pt<30", fakePt + " < 30"],
   #["anti-QCD2", "abs(mhtJet40 - met_pt)/met < 0.5"] #mhtJet40 not a vector
   #["BJets>=0","nSoftBJetsCSV >= 0 && nHardBJetsCSV >= 0"],
   ], baseCut = None) #allCuts['None']['presel'])
   
   #["AntiQCD", " (deltaPhi_j12 < 2.5)"], # monojet
   #["ISR110","nJet110 >= 1" ],
   #["TauElVeto","(Sum$(TauGood_idMVA) == 0) && (Sum$(abs(LepAll_pdgId) == 11 && abs(LepAll_eta) < " + str(etaAcc) + "&& LepAll_SPRING15_25ns_v1 == 1) == 0)"],
   #["1Mu-2ndMu20Veto", "(nlep==1 || (nlep ==2 && LepAll_pt[looseMuonIndex2] < 20) )"],
   #["No3rdJet60","nJet60 <= 2"],

plotDict = {\
   "fakePt":{'var':fakePt, "bins":[25,0,25], "decor":{"title": "Electron Fakes pT Plot" ,"x":"Electron p_{T} / GeV" , "y":"Events","log":[0,1,0]}},
   "fakeMt":{'var':fakeMt, "bins":[30,1,150], "decor":{"title": "Electron Fakes mT Plot" ,"x":"m_{T} / GeV" , "y":"Events"}},
   "MET":{'var':"met", "bins":[20,150,900], "decor":{"title": "Electron Fakes MET Plot" ,"x":"Missing E_{T} / GeV" , "y":"Events"}},
   #"HT":{'var':"ht", "bins":[100,0,100], "decor":{"title": "Electron ID FoM Plot: %s_%s_%s"%(ID, selection, WP) ,"x":"H_{T} / GeV" , "y":"Events" ,'log':[0,1,0]}}\
}

plotsDict = Plots(**plotDict)
plotsList = ["fakePt", "fakeMt", "MET"]#, "HT"]

plots = getPlots(samples, plotsDict, fakes, selectedSamples, plotList = plotsList)# addOverFlowBin='both')
fakePlots1 = drawPlots(samples, plotsDict, fakes, selectedSamples, plotList = plotsList, plotLimits = [0.1, 5000], denoms = ["bkg"], noms = ["bkg"], fom = "RATIO", fomLimits = [0,2.8], plotMin = 0.1, normalize = False, save = False)

#for leg in fakePlots1['legs']:
#   leg.Draw()

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   if not os.path.exists("%s/root"%(savedir)): os.makedirs("%s/root"%(savedir))
   if not os.path.exists("%s/pdf"%(savedir)): os.makedirs("%s/pdf"%(savedir))
   
   for canv1 in fakePlots1['canvs']:
      if canv1 == 'MET': continue
      fakePlots1['canvs'][canv1][0].SaveAs("%s/%s.png"%(savedir, canv1))
      fakePlots1['canvs'][canv1][0].SaveAs("%s/root/%s.root"%(savedir, canv1))
      fakePlots1['canvs'][canv1][0].SaveAs("%s/pdf/%s.pdf"%(savedir, canv1))
