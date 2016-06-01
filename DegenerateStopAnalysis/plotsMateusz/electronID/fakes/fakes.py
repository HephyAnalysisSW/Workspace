#eleIdFOM.py
import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.degTools import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.cutsEle import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_PP_mAODv2_7412pass2_scan import getSamples

from array import array
from math import pi, sqrt #cos, sin, sinh, log

ROOT.setTDRStyle(1)
ROOT.gStyle.SetOptStat(0) #1111 #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

#Samples
privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
backgrounds = ["w","tt", "z","qcd"]

samplesList = backgrounds # + privateSignals
samples = getSamples(sampleList = samplesList, scan = True, useHT = True, getData = False)#, cmgPP = cmgPP) 

officialSignals = ["s300_290", "s300_270", "s300_240"] #FIXME: crosscheck if these are in allOfficialSignals

allOfficialSignals = samples.massScanList()
#allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
allSignals = privateSignals + allOfficialSignals
allSamples = allSignals + backgrounds

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
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/fakes"

#Gets all cuts (electron, SR, CR) for given electron ID
eleIDsel = electronIDs(ID = "standard", removedCut = "None", iso = False)
allCuts = cutClasses(eleIDsel, ID = "standard")

##for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
#for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

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

#print makeLine()
#print "ID type: ", ID, " | Selection Region: ", selection, " | Electron ID WP: ", WP, " | Electron ID Cut Removed: ", removedCut, " | Isolation applied: ", iso
#print makeLine()
   
#sel = allCuts[WP][selection]

#elePt = "Max$(LepGood_pt*eleSel)"
#eleMt = "Max$(LepGood_mt*eleSel)"
#eleMt = "Max$(sqrt(2*met*{pt}*(1 - cos(met_phi - LepGood_phi)))*(LepGood_pt == {pt}))".format(pt=elePt)  #%(elePt[iWP], elePhi[iWP], elePt[iWP])#

#medMuId = "Sum$(abs(LepGood_pdgId) == 13 && abs(LepGood_eta) < 2.4 && 
#           abs(LepGood_dz) < 0.2  && abs(LepGood_dxy)<0.05 && 
#           (LepGood_relIso04 < 0.2 || LepGood_relIso04 < 5) && 
#           LepGood_mediumMuonId == 1) == 1"

etaAcc = 1.4442

fakeEleSel = "abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && " + eleIDsel['Veto'] + " && LepGood_relIso03 < 0.2 && LepGood_miniRelIso < 0.1 && LepGood_mcMatchId == 0"
#fakeEleSel = "abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + "&& LepGood_mcMatchId == 0"
#fakeEleSel = "abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_relIso03 < 0.2 && LepGood_miniRelIso < 0.1 && LepGood_mcMatchId == 0"
#fakeEleSel = "abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && " + eleIDsel['Loose'] + " && LepGood_mcMatchId == 0"
#fakeEleSel2 = "abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && " + eleIDsel['Veto'] + " && LepGood_miniRelIso < 0.5 && LepGood_mcMatchId == 0"

fakeMt = "Max$(LepGood_mt*(" + fakeEleSel + "))"
fakePt = "Max$(LepGood_pt*(" + fakeEleSel + "))"

fakes = CutClass("fakes", [
   ["MET200","met > 200"],
   ["HT200","htJet30j > 200"],
   ["dPhi(j1234, MET)>0.3", "Min$(acos(cos(Jet_phi - met_phi)) > 0.3)"],
   #["dPhi(j1234, MET)>0.3", "Min$(" + minAngle("Jet_phi", "met_phi") + " > 0.3)"],
   ["Jets>=1","nJet30 >= 1"], #nJet60
   ["fake", "Sum$(" + fakeEleSel + ") >= 1"],
   ["Mt>20", fakeMt + " > 20"],
   ["Pt<20", fakePt + " < 20"],
   #["anti-QCD2", "abs(mhtJet40 - met_pt)/met < 0.5"] #mhtJet40 not a vector
   #["BJets>=0","nSoftBJetsCSV >= 0 && nHardBJetsCSV >= 0"],
   ], baseCut = None) #allCuts['None']['presel'])
   
   #["AntiQCD", " (deltaPhi_j12 < 2.5)"], # monojet
   #["ISR110","nJet110 >= 1" ],
   #["TauElVeto","(Sum$(TauGood_idMVA) == 0) && (Sum$(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + "&& LepGood_SPRING15_25ns_v1 == 1) == 0)"],
   #["1Mu-2ndMu20Veto", "(nlep==1 || (nlep ==2 && LepGood_pt[looseMuonIndex2] < 20) )"],
   #["No3rdJet60","nJet60 <= 2"],

plotDict = {\
   "fakePt":{'var':fakePt, "bins":[25,0,25], "decor":{"title": "Electron Fakes pT Plot" ,"x":"Electron p_{T} / GeV" , "y":"Events"}},
#   "fakeMt":{'var':fakeMt, "bins":[30,1,150], "decor":{"title": "Electron Fakes mT Plot" ,"x":"m_{T} / GeV" , "y":"Events"}},
#   "MET":{'var':"met", "bins":[20,150,900], "decor":{"title": "Electron Fakes MET Plot" ,"x":"Missing E_{T} / GeV" , "y":"Events"}},
   #"HT":{'var':"ht", "bins":[100,0,100], "decor":{"title": "Electron ID FoM Plot: %s_%s_%s"%(ID, selection, WP) ,"x":"H_{T} / GeV" , "y":"Events" ,'log':[0,1,0]}}\
}

plotsDict = Plots(**plotDict)
plotsList = ["fakePt"]#, "fakeMt", "MET"]#, "HT"]

plots = getPlots(samples, plotsDict, fakes, selectedSamples, plotList = plotsList)# addOverFlowBin='both')
fakePlots1 = drawPlots(plots, fom=False, save=False, plotLimits = [0,20], leg = True)#, plotMin=0.001), logy = 1 
#fakePlots2 = drawPlots(samples, plots, fakes, sampleList = selectedSamples, plotList = ['MET'], fom=False, save=False, plotLimits = [0,900], leg = True)#, plotMin=0.001), logy = 1 

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
   
#   for canv2 in fakePlots2['canvs']:
#      fakePlots2['canvs'][canv2][0].SaveAs("%s/%s.png"%(savedir, canv2))
#      fakePlots2['canvs'][canv2][0].SaveAs("%s/root/%s.root"%(savedir, canv2))
#      fakePlots2['canvs'][canv2][0].SaveAs("%s/pdf/%s.pdf"%(savedir, canv2))
