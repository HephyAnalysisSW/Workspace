# QCDplots.py
# Sequential application of inverted anti-QCD cuts around SR
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

#Samples
privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
backgrounds = ["w","tt", "z","qcd"]

cmgPP = cmgTuplesPostProcessed()#mc_path, signal_path, data_path)

samplesList = backgrounds # + privateSignals
samples = getSamples(cmgPP = cmgPP, skim = 'presel', sampleList = samplesList, scan = False, useHT = True, getData = False)

officialSignals = ["s300_290", "s300_270", "s300_240"] #FIXME: crosscheck if these are in allOfficialSignals

allOfficialSignals = samples.massScanList()
#allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
allSignals = privateSignals + allOfficialSignals
allSamples = allSignals + backgrounds

#Input options
parser = argparse.ArgumentParser(description = "Input options")
#parser.add_argument("--sel", dest = "sel",  help = "Selection", type = str, default = "presel") #presel, SR, QCD_A, QCD_I, QCD_D 
#parser.add_argument("--isolation", dest = "isolation",  help = "Isolation (hybIso03/hybIso04)", type = str, default = "hybIso03")
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
#sel = args.sel
logy = args.logy
save = args.save

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/plots"

#Gets all cuts (electron, SR, CR) for given electron ID
eleIDsel = electronIDs(ID = "nMinus1", removedCut = "d0", iso = False)
#eleIDsel = electronIDs(ID = "standard", removedCut = "", iso = False)
#allCuts = cutClasses(eleIDsel, ID = "standard")

##for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
#for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

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

#print makeLine()
#print "ID type: ", ID, " | Selection Region: ", selection, " | Electron ID WP: ", WP, " | Electron ID Cut Removed: ", removedCut, " | Isolation applied: ", iso
#print makeLine()
   
#elePt = "Max$(LepGood_pt*eleSel)"
#eleMt = "Max$(LepGood_mt*eleSel)"
#eleMt = "Max$(sqrt(2*met*{pt}*(1 - cos(met_phi - LepGood_phi)))*(LepGood_pt == {pt}))".format(pt=elePt)  #%(elePt[iWP], elePhi[iWP], elePt[iWP])#

def QCDplots(collection = "LepGood", samples = samples, logy = logy, save = save, savedir = savedir):

   if collection == "LepGood": otherCollection = "LepOther"
   elif collection == "LepOther": otherCollection = "LepGood"

   print makeLine()
   print "Using " + collection + " collection."
   print "Ignoring " + otherCollection + " collection."
   print makeLine()

   savedir += "/" + collection
   if not os.path.exists(savedir): os.makedirs(savedir)

   #Gets all cuts (electron, SR, CR) for given electron ID
   eleIDsel = electronIDs(ID = "nMinus1", removedCut = "d0", iso = False, collection = collection)
   eleIDsel_other = electronIDs(ID = "nMinus1", removedCut = "d0", iso = False, collection = otherCollection)

   etaAcc = 2.1
   eleSel = "abs(" + collection + "_pdgId) == 11 && abs(" + collection + "_eta) < " + str(etaAcc) + " && " + eleIDsel['Veto']
   eleSel_other = "abs(" + otherCollection + "_pdgId) == 11 && abs(" + otherCollection + "_eta) < " + str(etaAcc) + " && " + eleIDsel_other['Veto']
   
   ##Isolation
   #if isolation == "hybIso03": 
   #   aiso = "" + collection + "_" + collection + "_absIso03"
   #   riso = "" + collection + "_" + collection + "_relIso03"
   #elif isolation == "hybIso04": 
   #   aiso = "" + collection + "_absIso"
   #   riso = "" + collection + "_relIso04"
   
   hybIsoCut = "((" + collection + "_absIso03 < 5) || (" + collection + "_relIso03 < 0.2))"
   antiHybIsoCut = "(" + collection + "_relIso03*min(" + collection + "_pt, 25)) > 5"
   #antiHybIsoCut = "((" + collection + "_absIso03 > 5) && (" + collection + "_relIso03 > 0.2))"
   
   dxyCut = "abs(" + collection + "_dxy) < 0.02"
   antiDxyCut = "abs(" + collection + "_dxy) > 0.02"
   
   #Redefining electron pT in terms of selection
   elePt = {}
   elePt['eleSel'] = "Max$(" + collection + "_pt*(" + eleSel + "))"
   elePt['SR'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
   elePt['I'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + antiHybIsoCut + "))"
   elePt['D'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + antiDxyCut + "))"
   elePt['ID'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + "))"
   
   #Redefining mT in terms of selection
   eleMt = {}
   eleMt['eleSel'] = "Max$(" + collection + "_mt*(" + eleSel + "))"
   eleMt['SR'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
   eleMt['I'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + antiHybIsoCut + "))"
   eleMt['D'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + antiDxyCut + "))"
   eleMt['ID'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + "))"
   
   #Redefining HI in terms of selection
   absIso = {} 
   absIso['eleSel'] = "Max$(" + collection + "_absIso03*(" + eleSel + "))"
   absIso['SR'] = "Max$(" + collection + "_absIso03*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
   absIso['I'] = "Max$(" + collection + "_absIso03*(" + eleSel + "&&" + antiHybIsoCut + "))"
   absIso['D'] = "Max$(" + collection + "_absIso03*(" + eleSel + "&&" + antiDxyCut + "))"
   absIso['ID'] = "Max$(" + collection + "_absIso03*(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + "))"
   
   relIso = {} 
   relIso['eleSel'] = "Max$(" + collection + "_relIso03*(" + eleSel + "))"
   relIso['SR'] = "Max$(" + collection + "_relIso03*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
   relIso['I'] = "Max$(" + collection + "_relIso03*(" + eleSel + "&&" + antiHybIsoCut + "))"
   relIso['D'] = "Max$(" + collection + "_relIso03*(" + eleSel + "&&" + antiDxyCut + "))"
   relIso['ID'] = "Max$(" + collection + "_relIso03*(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + "))"
   
   hybIso = {} 
   hybIso['eleSel'] = "Max$((" + collection + "_relIso03*min(" + collection + "_pt, 25))*(" + eleSel + "))"
   hybIso['SR'] = "Max$((" + collection + "_relIso03*min(" + collection + "_pt, 25))*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
   hybIso['I'] = "Max$((" + collection + "_relIso03*min(" + collection + "_pt, 25))*(" + eleSel + "&&" + antiHybIsoCut + "))"
   hybIso['D'] = "Max$((" + collection + "_relIso03*min(" + collection + "_pt, 25))*(" + eleSel + "&&" + antiDxyCut + "))"
   hybIso['ID'] = "Max$((" + collection + "_relIso03*min(" + collection + "_pt, 25))*(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + "))"

   #Redefining IP in terms of selection
   absDxy = {}
   absDxy['eleSel'] = "Max$(abs(" + collection + "_dxy*(" + eleSel + ")))"
   absDxy['SR'] = "Max$(abs(" + collection + "_dxy*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + ")))"
   absDxy['I'] = "Max$(abs(" + collection + "_dxy*(" + eleSel + "&&" + antiHybIsoCut + ")))"
   absDxy['D'] = "Max$(abs(" + collection + "_dxy*(" + eleSel + "&&" + antiDxyCut + ")))"
   absDxy['ID'] = "Max$(abs(" + collection + "_dxy*(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + ")))"

   QCD = {}
   
   QCD['presel'] = CutClass("presel_SR", [
      ["MET300","met > 300"],
      ["HT300","ht_basJet > 300"],
      ["ISR110", "nIsrJet >= 1"],
      ["No3rdJet60","nVetoJet <= 2"],
      ["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
      ["eleSel", "Sum$(" + eleSel + ") == 1"],
      ["otherCollection", "Sum$(" + eleSel_other + ") == 0"],
      #["elePt<30", elePt + " < 30"],
      #["anti-AntiQCD", "vetoJet_dPhi_j1j2 > 2.5"],
      #["anti-HybIso", "Sum$(" + eleSel + "&&" + antiHybIsoCut + ") == 1"],
      #["anti-dxy", "Max$(abs(" + collection + "_dxy*(" + eleSel + "&&" + antiHybIsoCut + "))) > 0.02"], #TODO:check
      ], baseCut = None) #allCuts['None']['presel'])
   
   QCD['elePt30'] = CutClass("elePt30", [
      ["elePt<30", elePt['eleSel'] + " < 30"],
      ], baseCut = QCD['presel']) 
   
   QCD['SR'] = CutClass("QCD_SR", [
      ["elePt<30", elePt['SR'] + " < 30"],
      ["A", "vetoJet_dPhi_j1j2 < 2.5"],
      ["ID", "Sum$(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + ") == 1"],
      ], baseCut = QCD['presel'])
   
   QCD['A'] = CutClass("QCD_A", [ 
      ["elePt<30", elePt['eleSel'] + " < 30"],
      ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"],
      ], baseCut = QCD['presel']) 
   
   QCD['I'] = CutClass("QCD_I", [
      ["elePt<30", elePt['I'] + " < 30"],
      ["anti-I", "Sum$(" + eleSel + "&&" + antiHybIsoCut + ") == 1"],
      ], baseCut = QCD['presel']) 
   
   QCD['D'] = CutClass("QCD_D", [
      ["elePt<30", elePt['D'] + " < 30"],
      ["anti-D", "Sum$(" + eleSel + "&&" + antiDxyCut + ") == 1"],
      ], baseCut = QCD['presel']) 
   
   QCD['IA'] = CutClass("QCD_IA", [
      ["elePt<30", elePt['I'] + " < 30"],
      ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"],
      ["anti-I", "Sum$(" + eleSel + "&&" + antiHybIsoCut + ") == 1"],
      ], baseCut = QCD['presel']) 
   
   QCD['DA'] = CutClass("QCD_DA", [
      ["elePt<30", elePt['D'] + " < 30"],
      ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"],
      ["anti-D", "Sum$(" + eleSel + "&&" + antiDxyCut + ") == 1"],
      ], baseCut = QCD['presel']) 
   
   QCD['ID'] = CutClass("QCD_ID", [
      ["elePt<30", elePt['ID'] + " < 30"],
      ["anti-ID", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + ") == 1"],
      ], baseCut = QCD['presel']) 
   
   QCD['IDA'] = CutClass("QCD_IDA", [
      ["elePt<30", elePt['ID'] + " < 30"],
      ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"],
      ["anti-ID", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + ") == 1"],
      ], baseCut = QCD['presel']) 
  
   plotsList = {}
   plotDict = {}
   plotsDict = {}
   plots = {}
   plots2 = {}
  
   selections = {'presel': 'eleSel', 'elePt30':'eleSel', 'SR':'SR', 'I':'I', 'D':'D', 'A':'eleSel', 'IA':'I', 'DA':'D', 'ID':'ID', 'IDA':'ID'}
   
   for sel in selections.keys():
      plotDict[sel] = {\
         "elePt_" + sel:{'var':elePt[selections[sel]], "bins":[10, 0, 50], "decor":{"title": "Electron pT Plot" ,"x":"Electron p_{T} / GeV" , "y":"Events", 'log':[0, logy,0]}},
         "absIso_" + sel:{'var':absIso[selections[sel]], "bins":[4, 0, 20], "decor":{"title": "Electron absIso Plot" ,"x":"I_{abs} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "relIso_" + sel:{'var':relIso[selections[sel]], "bins":[20, 0, 5], "decor":{"title": "Electron relIso Plot" ,"x":"I_{rel}" , "y":"Events", 'log':[0,logy,0]}}, 
         "hybIso_" + sel:{'var':hybIso[selections[sel]], "bins":[10, 0, 25], "decor":{"title": "Electron hybIso Plot" ,"x":"HI = I_{rel}*min(p_{T}, 25 GeV)" , "y":"Events", 'log':[0,logy,0]}},
         "hybIso2_" + sel:{'var':"(log(1 + " + hybIso[selections[sel]] + ")/log(1+5))", "bins":[8, 0, 4], "decor":{"title": "Electron hybIso Plot" ,"x":"log(1+HI)/log(1+5)" , "y":"Events", 'log':[0,logy,0]}},
         "absDxy_" + sel:{'var':absDxy[selections[sel]], "bins":[6, 0, 0.06], "decor":{"title": "Electron |dxy| Plot" ,"x":"|dxy|" , "y":"Events", "log":[0,logy,0]}},
         "delPhi_" + sel:{'var':"vetoJet_dPhi_j1j2", "bins":[8, 0, 3.14], "decor":{"title": "deltaPhi(j1,j2) Plot" ,"x":"#Delta#phi(j1,j2)" , "y":"Events", 'log':[0,logy,0]}},
         "eleMt_" + sel:{'var':eleMt[selections[sel]], "bins":[10,0,100], "decor":{"title": "mT Plot" ,"x":"m_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "MET_" + sel:{'var':"met", "bins":[20,100,500], "decor":{"title": "MET Plot" ,"x":"Missing E_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "HT_" + sel:{'var':"ht_basJet", "bins":[20,100,500], "decor":{"title": "HT Plot","x":"H_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}}
      }
 
      plotsList[sel] = ["elePt_" + sel, "absIso_" + sel, "relIso_" + sel,"hybIso_" + sel, "hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel, "eleMt_" + sel, "MET_" + sel, "HT_" + sel]
      plotsDict[sel] = Plots(**plotDict[sel])
      plots[sel] = getPlots(samples, plotsDict[sel], QCD[sel], selectedSamples, plotList = plotsList[sel], addOverFlowBin='upper')
      plots2[sel] = drawPlots(plots[sel], fom=False, save=False, plotMin = 0.1)
      
      #Save canvas
      if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
         if not os.path.exists("%s/%s/root"%(savedir, sel)): os.makedirs("%s/%s/root"%(savedir, sel))
         if not os.path.exists("%s/%s/pdf"%(savedir, sel)): os.makedirs("%s/%s/pdf"%(savedir, sel))
      
         for canv in plots2[sel]['canvs']:
            #if plot['canvs'][canv][0]:
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/%s.png"%(savedir, sel, canv))
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/root/%s.root"%(savedir, sel, canv))
            plots2[sel]['canvs'][canv][0].SaveAs("%s/%s/pdf/%s.pdf"%(savedir, sel, canv))
   
   return plots2

print makeLine()
print "Adding results for LepGood and LepOther"
print makeLine()

plotsGood = QCDplots("LepGood")
plotsOther = QCDplots("LepOther")

#regions = ['SRL1a', 'SRH1a', 'SRV1a','SRL1b','SRH1b','SRV1c','SRL1c','SRH1c','SRV1c']

#Plots

stackHists = {}
plotsTotal = {}
plotsList = {}
canvs = {}

#if save: #web address: http://www.hephy.at/user/mzarucki/plots/QCD
savedir += "/combined"
if not os.path.exists(savedir): os.makedirs(savedir)

selections = ['presel', 'elePt30', 'SR', 'I', 'D', 'A', 'IA', 'DA', 'ID', 'IDA']
#plotsList[sel] = ["elePt_" + sel, "absIso_" + sel, "relIso_" + sel,"hybIso_" + sel, "hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel]

for sel in selections:
   if not os.path.exists("%s/%s/root"%(savedir, sel)): os.makedirs("%s/%s/root"%(savedir, sel))
   if not os.path.exists("%s/%s/pdf"%(savedir, sel)): os.makedirs("%s/%s/pdf"%(savedir, sel))

   stackHists[sel] = {}
   plotsTotal[sel] = {}
   canvs[sel] = {}
   plotsList[sel] = ["elePt_" + sel, "absIso_" + sel, "relIso_" + sel,"hybIso_" + sel, "hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel, "eleMt_" + sel, "MET_" + sel, "HT_" + sel]

   for plot in plotsList[sel]:
      stackHists[sel][plot] = []

      for samp in ['qcd', 'z', 'tt', 'w']:
         plotsGood[sel]['hists'][samp][plot].Add(plotsOther[sel]['hists'][samp][plot])
         stackHists[sel][plot].append(plotsGood[sel]['hists'][samp][plot])

      plotsTotal[sel][plot] = getStackFromHists(stackHists[sel][plot])
      canvs[sel][plot] = ROOT.TCanvas(sel + "_" + plot, sel + "_" + plot, 800, 800)

      plotsTotal[sel][plot].Draw("hist")

      decorAxis(plotsTotal[sel][plot], 'y', t = "Events", tOffset = 1.6, tSize = 0.045)
      decorAxis(plotsTotal[sel][plot], 'x', t = plotsGood[sel]['hists']['qcd'][plot].GetXaxis().GetTitle(), tOffset = 1.3, tSize = 0.04)

      canvs[sel][plot].SetRightMargin(10)
      #canvs[sel][plot].SetLeftMargin(15) 
      
      latex = ROOT.TLatex()
      latex.SetNDC()
      latex.SetTextSize(0.03)
      latex.SetTextAlign(11)

      latex.DrawLatex(0.20,0.89,"#font[22]{CMS Simulation}")
      latex.DrawLatex(0.60,0.89,"#bf{L = 2.3 fb^{-1} (13 TeV)}")

      canvs[sel][plot].RedrawAxis()
      canvs[sel][plot].Update()
      if logy: canvs[sel][plot].SetLogy()   
   
      if sel in canvs.keys():
         canvs[sel][plot].SaveAs("%s/%s/%s.png"%(savedir, sel, plot))
         canvs[sel][plot].SaveAs("%s/%s/root/%s.root"%(savedir, sel, plot))
         canvs[sel][plot].SaveAs("%s/%s/pdf/%s.pdf"%(savedir, sel, plot))
