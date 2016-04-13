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

ROOT.gStyle.SetOptStat(0) #1111 #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

#Samples
privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
backgrounds=["w","tt", "z","qcd"]

samplesList = backgrounds # + privateSignals
samples = getSamples(sampleList=samplesList, scan=True, useHT=False, getData=False)#, cmgPP=cmgPP) 

officialSignals = ["s300_290", "s300_270", "s300_240"] #FIXME: crosscheck if these are in allOfficialSignals

allOfficialSignals = samples.massScanList()
#allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
allSignals = privateSignals + allOfficialSignals
allSamples = allSignals + backgrounds

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--doPlots", dest="doPlots",  help="Draw plots", type=int, default=1)
parser.add_argument("--doYields", dest="doYields",  help="Get yields table", type=int, default=1)
parser.add_argument("--ID", dest="ID",  help="Electron ID type", type=str, default="standard") # "standard" "manual" "nMinus1"
parser.add_argument("--WP", dest="WP",  help="Electron ID Working Point", type=str, default="None")
parser.add_argument("--selection", dest="selection",  help="Region selection", type=str, default="nosel")
parser.add_argument("--removedCut", dest="removedCut",  help="Variable removed from electron ID", type=str, default="None") #"sigmaEtaEta" "dEta" "dPhi" "hOverE" "ooEmooP" "d0" "dz" "MissingHits" "convVeto"
parser.add_argument("--save", dest="save",  help="Toggle save", type=int, default=1)
parser.add_argument("--zoom", dest="zoom",  help="Toggle zoom", type=int, default=1)
parser.add_argument("-b", dest="batch",  help="Batch mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
doPlots = args.doPlots
doYields = args.doYields
ID = args.ID 
WP = args.WP
selection = args.selection
removedCut = args.removedCut 
zoom = args.zoom
save = args.save
#if ID == "iso": isolation = args.iso
#nEles = "01" # 01,01tau,1,2 #Number of electrons in event

#Geometric divisions
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap
etaAcc = 2.5 #eta acceptance

#Pt division for MVA ID
ptSplit = 10 #we have above and below 10 GeV categories 

#Number of Leptons (hadronic, semileptonic, dileptonic)
nSel = ["(nLepGood == 0)", "(nLepGood == 1)", "(nLepGood == 2)"]

#Bin size 
#nbins = 100
xmin = 0
#xmax = 1000

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/electronID/FoM"
 
   #Save path
   if removedCut == "None":
      #if ID == "iso": savedir += "/" + isolation
      savedir += "/" + ID + "/" + selection
   else: savedir += "/no_" + removedCut + "/" + selection

   if doPlots:
      if not os.path.exists(savedir + "/plots/root"): os.makedirs(savedir + "/plots/root")
      if not os.path.exists(savedir + "/plots/pdf"): os.makedirs(savedir + "/plots/pdf")
   if doYields:
      if not os.path.exists(savedir + "/yields/tex"): os.makedirs(savedir + "/yields/tex")

#Gets all cuts (electron, SR, CR) for given electronID
allCuts = cutClasses(ID) #standard manual nMinus1

#for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

#selectedSamples = privateSignals + officialSignals + backgrounds
selectedSamples = ["qcd", "z", "tt", "w", "s300_270"]

print makeLine()
print "Using samples:"
newLine()
for s in selectedSamples:
   if s: print samples[s].name,":",s
   else: 
      print "!!! Sample " + sample + " unavailable."
      sys.exit(0)
print makeLine()

print "ID type: ", ID, " Selection Region: ", selection, " WP: ", WP
   
sel = allCuts[WP][selection]

if doPlots:
   elePt = "Max$(LepGood_pt*eleSel)"
   eleMt = "Max$(LepGood_mt*eleSel)"
   #eleMt = "Max$(sqrt(2*met*{pt}*(1 - cos(met_phi - LepGood_phi)))*(LepGood_pt == {pt}))".format(pt=elePt)  #%(elePt[iWP], elePhi[iWP], elePt[iWP])#
   
   plotDict = {\
      "elePt":{'var':elePt, "bins":[100,1,100], "decor":{"title": "Electron ID FoM Plot: %s_%s_%s"%(ID, selection, WP) ,"x":"Electron p_{T} / GeV" , "y":"Events" ,'log':[0,1,0]}},\
      "MT":{'var':eleMt, "bins":[30,1,150], "decor":{"title": "Electron ID FoM Plot: %s_%s_%s"%(ID, selection, WP) ,"x":"M_{T} / GeV" , "y":"Events" ,'log':[0,1,0]}},\
      "MET":{'var':"met", "bins":[20,150,900], "decor":{"title": "Electron ID FoM Plot: %s_%s_%s"%(ID, selection, WP) ,"x":"Missing E_{T} / GeV" , "y":"Events" ,'log':[0,1,0]}},\
      #"HT":{'var':"ht", "bins":[100,0,100], "decor":{"title": "Electron ID FoM Plot: %s_%s_%s"%(ID, selection, WP) ,"x":"H_{T} / GeV" , "y":"Events" ,'log':[0,1,0]}}\
   }
   
   plots = Plots(**plotDict)
   plotsList = ["elePt", "MT", "MET"]#, "HT"]
   
   getPlots(samples, plots, sel, selectedSamples, plotList = plotsList)# addOverFlowBin='both')
   fomPlots = drawPlots(samples, plots, sel, sampleList=selectedSamples, plotList = plotsList, fom="AMSSYS", denoms=["bkg"], noms=["s300_270"], fomLimits=[0,2], save=False)#, plotMin=0.001)

if doYields:
   if sel.baseCut: flow = 'fullFlow'
   else: flow = 'flow'

   yields = Yields(samples, selectedSamples, sel, cutOpt = flow, pklOpt=False, verbose=True, nSpaces=10)
   if save: JinjaTexTable(yields, outputName="",  pdfDir = savedir + "/yields", texDir = savedir + "/yields/tex/", caption = "Cut Flow Table (" + yields.cutInst.name.replace("_",", ") + " WP)")

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   if doPlots:
      for canv in fomPlots['canvs']:
         if removedCut == "None":
            fomPlots['canvs'][canv][0].SaveAs("%s/plots/eleID_FoM_%s_%s.png"%(savedir, sel.name, canv))
            fomPlots['canvs'][canv][0].SaveAs("%s/plots/root/eleID_FoM_%s_%s.root"%(savedir, sel.name, canv))
            fomPlots['canvs'][canv][0].SaveAs("%s/plots/pdf/eleID_FoM_%s_%s.pdf"%(savedir, sel.name, canv))
         else:
            fomPlots['canvs'][canv][0].SaveAs("%s/plots/eleID_FoM_no_%s_%s_%s.png"%(savedir, removedCut, sel.name, canv))
            fomPlots['canvs'][canv][0].SaveAs("%s/plots/root/eleID_FoM_no_%s_%s_%s.root"%(savedir, removedCut, sel.name, canv))
            fomPlots['canvs'][canv][0].SaveAs("%s/plots/pdf/eleID_FoM_no_%s_%s_%s.pdf"%(savedir, removedCut, sel.name, canv)) 
