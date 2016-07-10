#eleIdLimits.py
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
#from Workspace.DegenerateStopAnalysis.toolsMateusz.getSamples_PP_mAODv2_7412pass2_scan import getSamples

from array import array
from math import pi, sqrt #cos, sin, sinh, log

ROOT.gStyle.SetOptStat(0) #1111 #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--doLimits", dest = "doLimits",  help = "Draw exclusion limit plot", type = int, default = 1)
parser.add_argument("--doYields", dest = "doYields",  help = "Make yields table", type = int, default = 1)
parser.add_argument("--doPlots", dest = "doPlots",  help = "Draw plots", type = int, default = 1)
parser.add_argument("--doCutFlow", dest = "doCutFlow",  help = "Make cut flow table", type = int, default = 1)
parser.add_argument("--ID", dest = "ID",  help = "Electron ID type", type = str, default = "standard") # "standard" "manual" "nMinus1"
parser.add_argument("--removedCut", dest = "removedCut",  help = "Variable removed from electron ID", type = str, default = "None") #"sigmaEtaEta" "hOverE" "ooEmooP" "dEta" "dPhi" "d0" "dz" "MissingHits" "convVeto"
parser.add_argument("--iso", dest = "iso",  help = "Apply isolation", type = str, default = "")
parser.add_argument("--WP", dest = "WP",  help = "Electron ID Working Point", type = str, default = "None")
parser.add_argument("--selection", dest = "selection",  help = "Region selection", type = str, default = "nosel")
parser.add_argument("--save", dest = "save",  help = "Toggle save", type = int, default = 1)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
doLimits = args.doLimits 
doYields = args.doYields 
doPlots = args.doPlots 
doCutFlow = args.doCutFlow
ID = args.ID 
removedCut = args.removedCut 
iso = args.iso
WP = args.WP
selection = args.selection
save = args.save

if ID == "nMinus1":
   string1 = "no_" + removedCut
   string2 = "_no_" + removedCut
else: 
   string1 = ""
   string2 = ""

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID"
   savedir1 = savedir2 = savedir3 = savedir
   
   savedir1 += "/limits"
   savedir2 += "/yields"    
   savedir3 += "/plots/" + selection

   savedir += "/" + ID

   if iso == "hybIso03" or iso == "hybIso04":
      savedir += "/" + iso
      isoString = "_" + iso
   elif not iso:
      savedir += "/noIso"
      isoString = ""
   
   if not os.path.exists("%s/cards/%s/%s%s"%(savedir1, string1, WP, string2)): os.makedirs("%s/cards/%s/%s%s"%(savedir1, string1, WP, string2))
   if not os.path.exists("%s/tex/%s/%s%s"%(savedir1, string1, WP, string2)): os.makedirs("%s/tex/%s/%s%s"%(savedir1, string1, WP, string2))
   if not os.path.exists("%s/tex/%s/%s%s"%(savedir2, string1, WP, string2)): os.makedirs("%s/tex/%s/%s%s"%(savedir2, string1, WP, string2))
   
   #if os.path.isfile(limitPkl):
   #      limits = pickle.load(file(limitPkl))

#Samples
privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
backgrounds = ["w","tt", "z","qcd"]

cmgPP = cmgTuplesPostProcessed()

samplesList = backgrounds # + privateSignals
samples = getSamples(cmgPP = cmgPP, sampleList = samplesList, scan = True, useHT = True, getData = False)

officialSignals = ["s300_290", "s300_270", "s300_240"] #FIXME: crosscheck if these are in allOfficialSignals

allOfficialSignals = samples.massScanList()
#allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
lessOfficialSignals = [s for s in allOfficialSignals if int(s.split("s")[1].split("_")[0]) < 425]
allSignals = privateSignals + allOfficialSignals
allSamples = allSignals + backgrounds
   
#Gets all cuts (electron, SR, CR) for given electron ID
eleIDsel = electronIDs(ID, removedCut, iso)
allCuts = cutClasses(eleIDsel, ID)
#selectedSamples = privateSignals + officialSignals + backgrounds

if doLimits or doYields:
   print makeLine()
   print "ID type: ", ID, " | Electron ID WP: ", WP, " | Electron ID Cut Removed: ", removedCut, " | Isolation applied: ", iso
   print makeLine()

   if doLimits:
      selectedSamples = lessOfficialSignals + backgrounds 
      
      limits={}
      
      setEventListToChains(samples, selectedSamples, allCuts['None']['presel'])
   
      allYields = Yields(samples, selectedSamples, allCuts[WP]['runI'], cutOpt = "list2", pklOpt = False, tableName = "RunI_" + WP + string2 + isoString, nDigits = 2, err = True, verbose = True, nSpaces = 10)#weight = "weight"
      JinjaTexTable(allYields, pdfDir = savedir1, texDir = "%s/tex/%s/%s%s%s/"%(savedir1, string1, WP, string2, isoString), caption = "Yields: RunI Reload Electrons (" + WP + string2 + " WP)", transpose = True)
      
      for sig in allOfficialSignals:
         mstop, mlsp = [int(x) for x in sig[1:].rsplit("_")]
         print makeLine()
         print "signal, mstop, mlsp: ", sig, " ", mstop, " ", mlsp
         print makeLine()
         
         try: limits[mstop]
         except KeyError: limits[mstop]={}
         
         limits[mstop][mlsp] = getLimit(allYields, sig = sig, outDir = "%s/cards/%s"%(savedir1, string1), calc_limit = True) #, postfix = WP + string2 + isoString
   
      #pickle.dump(limits, open(savedir + "/cards/limits.pkl",'w'))
      exclCanv, exclPlot = drawExpectedLimit(limits, plotDir = "%s/%s/ExpectedLimit_eleID_%s%s%s.png"%(savedir1, string1, WP, string2, isoString), bins = None, key = None, title = "Expected Limits (%s %s %s Electron ID)"%(WP, string1, iso))
      #exclCanv.SetName("ExpectedLimit_eleID_%s.pkl"%(WP))
   
   if doYields:
      selectedSamples = officialSignals + backgrounds 
      setEventListToChains(samples, selectedSamples, allCuts['None']['presel'])
      fewSignalYields = Yields(samples, selectedSamples, allCuts[WP]['runI'], cutOpt = "list2", pklOpt = False, tableName = "RunI_" + WP + string2 + isoString, nDigits = 2, err = True, verbose = True, nSpaces = 10)#weight = "weight" 
      JinjaTexTable(fewSignalYields, pdfDir = savedir2, texDir = "%s/%s/tex/%s%s%s/"%(savedir2, string1, WP, string2, isoString), caption = "Cut Flow Table: RunI Reload Electrons (" + WP + string2 + " WP)", transpose = False)

elif doPlots or doCutFlow:
   print makeLine()
   print "ID type: ", ID, " | Selection Region: ", selection, " | Electron ID WP: ", WP, " | Electron ID Cut Removed: ", removedCut, " | Isolation applied: ", iso
   print makeLine()
   
   sel = allCuts[WP][selection]
   
   selectedSamples = ["qcd", "z", "tt", "w", "s300_270"]
   
   print "Using samples:"
   newLine()
   for s in selectedSamples:
      if s: print samples[s].name,":",s
      else:
         print "!!! Sample " + sample + " unavailable."
         sys.exit(0)
   print makeLine()
   
   #for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
   for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])
   
   
   #for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
   for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

   if doPlots:
      elePt = "Max$(LepGood_pt*eleSel)"
      eleMt = "Max$(LepGood_mt*eleSel)"
      #eleMt = "Max$(sqrt(2*met*{pt}*(1 - cos(met_phi - LepGood_phi)))*(LepGood_pt == {pt}))".format(pt=elePt)  #%(elePt[iWP], elePhi[iWP], elePt[iWP])#
   
      plotDict = {\
         "elePt":{'var':elePt, "bins":[100,1,101], "decor":{"title": "Electron ID FoM Plot: %s_%s_%s"%(ID, selection, WP) ,"x":"Electron p_{T} / GeV" , "y":"Events" ,'log':[0,1,0]}},\
         "MT":{'var':eleMt, "bins":[30,1,151], "decor":{"title": "Electron ID FoM Plot: %s_%s_%s"%(ID, selection, WP) ,"x":"M_{T} / GeV" , "y":"Events" ,'log':[0,1,0]}},\
         "MET":{'var':"met", "bins":[60,100,700], "decor":{"title": "Electron ID FoM Plot: %s_%s_%s"%(ID, selection, WP) ,"x":"Missing E_{T} / GeV" , "y":"Events" ,'log':[0,1,0]}},\
         "HT":{'var':"ht", "bins":[100,0,100], "decor":{"title": "Electron ID FoM Plot: %s_%s_%s"%(ID, selection, WP) ,"x":"H_{T} / GeV" , "y":"Events" ,'log':[0,1,0]}}\
      }
   
      plotsDict = Plots(**plotDict)
      plotsList = ["elePt", "MT", "MET", "HT"]
   
      plots = getPlots(samples, plotsDict, sel, selectedSamples, plotList = plotsList)# addOverFlowBin='both')
   
      fomPlots = drawPlots(plots, fom="AMSSYS", denoms=["bkg"], noms=["s300_270"], fomLimits=[0,2], save=False)#, plotMin=0.001)
   
   if doCutFlow:
      if sel.baseCut: flow = 'fullFlow'
      else: flow = 'flow'
   
      yields = Yields(samples, selectedSamples, sel, cutOpt = flow, pklOpt = False, verbose = True, nSpaces = 10)
      if save: JinjaTexTable(yields, outputName = "",  pdfDir = savedir + "/cutFlow", texDir = savedir + "/cutFlow/tex/", caption = "Cut Flow Table (" + yields.cutInst.name.replace("_",", ") + " WP " + iso + ")")
   
   #Save canvas
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      if doPlots:
         for canv in fomPlots['canvs']:
            if not os.path.exists("%s/plots/%s/root"%(savedir, canv)): os.makedirs("%s/plots/%s/root"%(savedir, canv))
            if not os.path.exists("%s/plots/%s/pdf"%(savedir, canv)): os.makedirs("%s/plots/%s/pdf"%(savedir, canv))
   
            if ID != "nMinus1":
               fomPlots['canvs'][canv][0].SaveAs("%s/plots/%s/eleID_FoM_%s_%s%s.png"%(savedir, canv, sel.name, canv, isoString))
               fomPlots['canvs'][canv][0].SaveAs("%s/plots/%s/root/eleID_FoM_%s_%s%s.root"%(savedir, canv, sel.name, canv, isoString))
               fomPlots['canvs'][canv][0].SaveAs("%s/plots/%s/pdf/eleID_FoM_%s_%s%s.pdf"%(savedir, canv, sel.name, canv, isoString))
            else:
               fomPlots['canvs'][canv][0].SaveAs("%s/plots/%s/eleID_FoM_no_%s_%s_%s%s.png"%(savedir, canv, removedCut, sel.name, canv, isoString))
               fomPlots['canvs'][canv][0].SaveAs("%s/plots/%s/root/eleID_FoM_no_%s_%s_%s%s.root"%(savedir, canv, removedCut, sel.name, canv, isoString))
               fomPlots['canvs'][canv][0].SaveAs("%s/plots/%s/pdf/eleID_FoM_no_%s_%s_%s%s.pdf"%(savedir, canv, removedCut, sel.name, canv, isoString))
