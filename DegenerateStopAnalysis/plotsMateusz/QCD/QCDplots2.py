# QCDplots2.py
# Additional ABCD plots 
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
#parser.add_argument("--sel", dest = "sel",  help = "Selection", type = str, default = "presel") #presel, SR, QCD_A, QCD_I, QCD_D 
#parser.add_argument("--isolation", dest = "isolation",  help = "Isolation (hybIso03/hybIso04)", type = str, default = "hybIso03")
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
save = args.save

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/plots/extra"

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

def QCDplots(collection = "LepGood", samples = samples, logy = 1, save = save, savedir = savedir):

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
   
   #Isolation
   hybIsoCut = "(" + collection + "_relIso03*min(" + collection + "_pt, 25)) < 5"
   antiHybIsoCut = "(" + collection + "_relIso03*min(" + collection + "_pt, 25)) > 5"
   #antiHybIsoCut = "((absIso03 > 5) && (relIso03 > 0.2))"
   
   dxyCut = "abs(" + collection + "_dxy) < 0.02"
   antiDxyCut = "abs(" + collection + "_dxy) > 0.02"
   
   #Redefining electron pT in terms of selection
   elePt = {}
   elePt['I_D'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
   elePt['I_A'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + hybIsoCut + "))"
   elePt['A_D'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + dxyCut + "))"
   elePt['A_I'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + hybIsoCut + "))"
   elePt['D_I'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + hybIsoCut + "&&" + antiDxyCut + "))"
   elePt['D_A'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + antiDxyCut + "))"
 
   #Redefining mT in terms of selection
   eleMt = {}
   eleMt['I_D'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
   eleMt['I_A'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + hybIsoCut + "))"
   eleMt['A_D'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + dxyCut + "))"
   eleMt['A_I'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + hybIsoCut + "))"
   eleMt['D_I'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + hybIsoCut + "&&" + antiDxyCut + "))"
   eleMt['D_A'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + antiDxyCut + "))"
   
   #Redefining HI in terms of selection
   absIso = {} 
   absIso['I_D'] = "Max$(" + collection + "_absIso03*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
   absIso['I_A'] = "Max$(" + collection + "_absIso03*(" + eleSel + "&&" + hybIsoCut + "))"
   absIso['A_D'] = "Max$(" + collection + "_absIso03*(" + eleSel + "&&" + dxyCut + "))"
   absIso['A_I'] = "Max$(" + collection + "_absIso03*(" + eleSel + "&&" + hybIsoCut + "))"
   absIso['D_I'] = "Max$(" + collection + "_absIso03*(" + eleSel + "&&" + hybIsoCut + "&&" + antiDxyCut + "))"
   absIso['D_A'] = "Max$(" + collection + "_absIso03*(" + eleSel + "&&" + antiDxyCut + "))"
   
   relIso = {} 
   relIso['I_D'] = "Max$(" + collection + "_relIso03*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
   relIso['I_A'] = "Max$(" + collection + "_relIso03*(" + eleSel + "&&" + hybIsoCut + "))"
   relIso['A_D'] = "Max$(" + collection + "_relIso03*(" + eleSel + "&&" + dxyCut + "))"
   relIso['A_I'] = "Max$(" + collection + "_relIso03*(" + eleSel + "&&" + hybIsoCut + "))"
   relIso['D_I'] = "Max$(" + collection + "_relIso03*(" + eleSel + "&&" + hybIsoCut + "&&" + antiDxyCut + "))"
   relIso['D_A'] = "Max$(" + collection + "_relIso03*(" + eleSel + "&&" + antiDxyCut + "))"
   
   hybIso = {} 
   hybIso['I_D'] = "Max$((" + collection + "_relIso03*min( " + collection + "_pt, 25))*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
   hybIso['I_A'] = "Max$((" + collection + "_relIso03*min( " + collection + "_pt, 25))*(" + eleSel + "&&" + hybIsoCut + "))"
   hybIso['A_D'] = "Max$((" + collection + "_relIso03*min( " + collection + "_pt, 25))*(" + eleSel + "&&" + dxyCut + "))"
   hybIso['A_I'] = "Max$((" + collection + "_relIso03*min( " + collection + "_pt, 25))*(" + eleSel + "&&" + hybIsoCut + "))"
   hybIso['D_I'] = "Max$((" + collection + "_relIso03*min( " + collection + "_pt, 25))*(" + eleSel + "&&" + hybIsoCut + "&&" + antiDxyCut + "))"
   hybIso['D_A'] = "Max$((" + collection + "_relIso03*min( " + collection + "_pt, 25))*(" + eleSel + "&&" + antiDxyCut + "))"

   #Redefining IP in terms of selection
   absDxy = {}
   absDxy['I_D'] = "Max$(abs(" + collection + "_dxy*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + ")))"
   absDxy['I_A'] = "Max$(abs(" + collection + "_dxy*(" + eleSel + "&&" + hybIsoCut + ")))"
   absDxy['A_D'] = "Max$(abs(" + collection + "_dxy*(" + eleSel + "&&" + dxyCut + ")))"
   absDxy['A_I'] = "Max$(abs(" + collection + "_dxy*(" + eleSel + "&&" + hybIsoCut + ")))"
   absDxy['D_I'] = "Max$(abs(" + collection + "_dxy*(" + eleSel + "&&" + hybIsoCut + "&&" + antiDxyCut + ")))"
   absDxy['D_A'] = "Max$(abs(" + collection + "_dxy*(" + eleSel + "&&" + antiDxyCut + ")))"
   
   QCD = {}
   
   presel = CutClass("presel_loose", [
      ["MET200","met > 200"],
      ["HT200","htJet30j > 200"],
      ["eleSel", "Sum$(" + eleSel + ") == 1"],
      ["No3rdJet60","nJet60 <= 2"],
      #["BVeto","(nSoftBJetsCSV == 0 && nHardBJetsCSV == 0)"],
      ["otherCollection", "Sum$(" + eleSel_other + ") == 0"],
      #["elePt<30", elePt + " < 30"],
      #["anti-AntiQCD", "deltaPhi_j12 > 2.5"],
      #["anti-HybIso", "Sum$(" + eleSel + "&&" + antiHybIsoCut + ") == 1"],
      #["anti-dxy", "Max$(abs(" + collection + "_dxy*(" + eleSel + "&&" + antiHybIsoCut + "))) > 0.02"], #TODO:check
      ], baseCut = None) #allCuts['None']['presel'])
   
   #extra plots 
   QCD['I_D'] = CutClass("QCD_I_D", [
      ["elePt<30", elePt['I_D'] + " < 30"],
      ["anti-I+D", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + ") == 1"], #inverted, applied
      ], baseCut = presel)

   QCD['I_A'] = CutClass("QCD_I_A", [
      ["elePt<30", elePt['I_A'] + " < 30"],
      ["A", "deltaPhi_j12 < 2.5"], #applied
      ["anti-I", "Sum$(" + eleSel + "&&" + antiHybIsoCut + ") == 1"], #inverted
      ], baseCut = presel)

   QCD['A_I'] = CutClass("QCD_A_I", [
      ["elePt<30", elePt['A_I'] + " < 30"],
      ["anti-A", "deltaPhi_j12 > 2.5"], #inverted
      ["I", "Sum$(" + eleSel + "&&" + hybIsoCut + ") == 1"], #applied
      ], baseCut = presel)
   
   QCD['A_D'] = CutClass("QCD_A_D", [
      ["elePt<30", elePt['A_D'] + " < 30"],
      ["anti-A", "deltaPhi_j12 > 2.5"], #inverted
      ["D", "Sum$(" + eleSel + "&&" + dxyCut + ") == 1"], #applied
      ], baseCut = presel)
   
   QCD['D_A'] = CutClass("QCD_D_A", [
      ["elePt<30", elePt['D_A'] + " < 30"],
      ["A", "deltaPhi_j12 < 2.5"], #applied
      ["anti-D", "Sum$(" + eleSel + "&&" + antiDxyCut + ") == 1"], #inverted
      ], baseCut = presel)

   QCD['D_I'] = CutClass("QCD_D_I", [
      ["elePt<30", elePt['D_I'] + " < 30"],
      ["anti-D+I", "Sum$(" + eleSel + "&&" + hybIsoCut + "&&" + antiDxyCut + ") == 1"], #applied, inverted
      ], baseCut = presel)

   plotsList = {}
   plotDict = {}
   plotsDict = {}
   plots = {}
   plots2 = {}
  
   selections = ['A_D', 'A_I', 'I_D', 'I_A', 'A_D', 'A_I', 'D_A', 'D_I']
   
   for sel in selections:
      plotDict[sel] = {\
         "elePt_" + sel:{'var':elePt[sel], "bins":[10, 0, 50], "decor":{"title": "Electron pT Plot" ,"x":"Electron p_{T} / GeV" , "y":"Events", 'log':[0, logy,0]}}, 
         "absIso_" + sel:{'var':absIso[sel], "bins":[4, 0, 20], "decor":{"title": "Electron absIso Plot" ,"x":"I_{abs} / GeV" , "y":"Events", 'log':[0,logy,0]}}, 
         "relIso_" + sel:{'var':relIso[sel], "bins":[8, 0, 2], "decor":{"title": "Electron relIso Plot" ,"x":"I_{rel}" , "y":"Events", 'log':[0,logy,0]}}, 
         "hybIso_" + sel:{'var':hybIso[sel], "bins":[10, 0, 25], "decor":{"title": "Electron hybIso Plot" ,"x":"HI = I_{rel}*min(p_{T}, 25 GeV)" , "y":"Events", 'log':[0,logy,0]}},
         "hybIso2_" + sel:{'var':"(log(1 + " + hybIso[sel] + ")/log(1+5))", "bins":[6, 0, 3], "decor":{"title": "Electron hybIso Plot" ,"x":"log(1+HI)/log(1+5)" , "y":"Events", 'log':[0,logy,0]}},
         "absDxy_" + sel:{'var':absDxy[sel], "bins":[6, 0, 0.06], "decor":{"title": "Electron |dxy| Plot" ,"x":"|dxy|" , "y":"Events", "log":[0,logy,0]}},
         "delPhi_" + sel:{'var':"deltaPhi_j12", "bins":[4, 2, 4], "decor":{"title": "deltaPhi(j1,j2) Plot" ,"x":"#Delta#phi(j1,j2)" , "y":"Events", 'log':[0,logy,0]}},
         "eleMt_" + sel:{'var':eleMt[sel], "bins":[10,0,100], "decor":{"title": "mT Plot" ,"x":"m_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "MET_" + sel:{'var':"met", "bins":[20,100,500], "decor":{"title": "MET Plot" ,"x":"Missing E_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "HT_" + sel:{'var':"htJet30j", "bins":[20,100,500], "decor":{"title": "HT Plot","x":"H_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}}
      }
  
      plotsList[sel] = ["elePt_" + sel, "absIso_" + sel, "relIso_" + sel,"hybIso_" + sel, "hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel, "eleMt_" + sel, "MET_" + sel, "HT_" + sel]
      #plotsList[sel] = ["hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel]
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

selections = ['A_D', 'A_I', 'I_D', 'I_A', 'A_D', 'A_I', 'D_A', 'D_I']

for sel in selections:
   if not os.path.exists("%s/%s/root"%(savedir, sel)): os.makedirs("%s/%s/root"%(savedir, sel))
   if not os.path.exists("%s/%s/pdf"%(savedir, sel)): os.makedirs("%s/%s/pdf"%(savedir, sel))

   stackHists[sel] = {}
   plotsTotal[sel] = {}
   canvs[sel] = {}
   plotsList[sel] = ["elePt_" + sel, "absIso_" + sel, "relIso_" + sel,"hybIso_" + sel, "hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel, "eleMt_" + sel, "MET_" + sel, "HT_" + sel]
   #plotsList[sel] = ["hybIso2_" + sel, "absDxy_" + sel, "delPhi_" + sel]

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
      canvs[sel][plot].SetLogy()

      if sel in canvs.keys():
         canvs[sel][plot].SaveAs("%s/%s/%s.png"%(savedir, sel, plot))
         canvs[sel][plot].SaveAs("%s/%s/root/%s.root"%(savedir, sel, plot))
         canvs[sel][plot].SaveAs("%s/%s/pdf/%s.pdf"%(savedir, sel, plot))
