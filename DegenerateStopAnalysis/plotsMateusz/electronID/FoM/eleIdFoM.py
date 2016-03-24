#eleIdFOM.py
import ROOT
import os, sys
import argparse
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.degTools import *
#from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import *
#from Workspace.DegenerateStopAnalysis.navidTools.FOM import *
from Workspace.DegenerateStopAnalysis.cutsEle import *
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_mAODv2 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_mAODv2_7412pass2_scan import getSamples
from array import array
from math import pi, sqrt #cos, sin, sinh, log

ROOT.gStyle.SetOptStat(0) #1111 #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

mc_path     = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v3/RunIISpring15DR74_25ns"
signal_path = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v3/RunIISpring15DR74_25ns"
data_path   = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v3/Data_25ns"

cmgPP = cmgTuplesPostProcessed(mc_path, signal_path, data_path)

#Samples
privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
backgrounds=["w","tt", "z","qcd"]

samplesList = privateSignals + backgrounds
samples = getSamples(sampleList=samplesList, scan=True, useHT=False, cmgPP=cmgPP, getData=False)
allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
allSignals = privateSignals + allOfficialSignals

officialSignals = ["s300_290", "s300_270", "s300_240"] #FIXME: crosscheck if these are in allOfficialSignals
#selectedSamples = privateSignals + officialSignals + backgrounds
selectedSamples = ["qcd", "z", "tt", "w", "s30FS"]

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--ID", dest="ID",  help="Electron ID type", type=str, default="standard") # "standard" "manual" "nMinus1"
parser.add_argument("--WP", dest="WP",  help="Electron ID Working Point", type=str, default="None")
parser.add_argument("--selection", dest="selection",  help="Region selection", type=str, default="NoSel")
parser.add_argument("--removedCut", dest="removedCut",  help="Variable removed from electron ID", type=str, default="None") #"sigmaEtaEta" "dEta" "dPhi" "hOverE" "ooEmooP" "d0" "dz" "MissingHits" "convVeto"
#parser.add_argument("--presel", dest="presel",  help="Add preselection", type=int, default=1) # applies preselection
#parser.add_argument("--lowPt", dest="lowPt",  help="Low electron pt selection", type=int, default=0)
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
ID = args.ID 
WP = args.WP
selection = args.selection
removedCut = args.removedCut 
#presel = args.presel
#lowPt = args.lowPt 
zoom = args.zoom
save = args.save
#if ID == "iso": isolation = args.iso
#nEles = "01" # 01,01tau,1,2 #Number of electrons in event

print makeLine()
print "Using samples:"
newLine()
for s in selectedSamples:
   if s: print samples[s].name,":",s
   else: 
      print "!!! Sample " + sample + " unavailable."
      sys.exit(0)
print makeLine()

#Geometric divisions
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap
etaAcc = 2.5 #eta acceptance

#Pt division for MVA ID
ptSplit = 10 #we have above and below 10 GeV categories 

#Selection criteria
#intLum = 10.0 #fb-1
#weight = "(xsec*" + str(intLum) + "*(10^3)/" + str(getChunks(sample)[1]) + ")" #xsec in pb
#weight = samples[sample].weight

##Preselection
#preSel1 = "(met_pt > 200)" #MET
#preSel2 = "(Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 4.5 && Jet_id)) > 200)" #HT = Sum of Jets > 30GeV
#preSel3 = "(Max$(Jet_pt*(abs(Jet_eta) < " + str(etaAcc) + ") > 100))" #ISR
#preSelList = [preSel1, preSel2, preSel3]
#
#if presel: preSel = combineSelList(preSelList) 
#else: preSel = "1"

#Number of Leptons (hadronic, semileptonic, dileptonic)
nSel = ["(nLepGood == 0)", "(nLepGood == 1)", "(nLepGood == 2)"]
acceptance = "(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + ")"

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
   else: savedir += "/no_" + removedCut

   #if lowPt: savedir += "/lowPt"
   
   if not os.path.exists(savedir + "/root/histograms"): os.makedirs(savedir + "/root/histograms")
   if not os.path.exists(savedir + "/pdf"): os.makedirs(savedir + "/pdf")
   #if not os.path.exists(savedir + "/histogramCounts"): os.makedirs(savedir + "/histogramCounts")
   
   #Histograms save file 
   if removedCut == "None":
      #if ID == "iso": histos = ROOT.TFile(savedir + "/root/histograms/histos_" + plot + "_" + isolation + "_" + samples[sample].name + z + ".root", "recreate")
      histos = ROOT.TFile(savedir + "/root/histograms/histos_FoM" + ".root", "recreate")
   else: histos = ROOT.TFile(savedir + "/root/histograms/histos_FoM_no_" + removedCut + ".root", "recreate")
   
##################################################################################Canvas 1#############################################################################################
#c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
#c1.Divide(1,2)

#c1.cd(1)

#Electron Cut IDs

#cutSel['None'] = "1"

#selList = [preSel, acceptance, cutSel[WP]] 
#sel = combineSelList(selList)
#selection = CutClass("selection", [["eleIDsel",cutSel[WP]]], baseCut=preselEle)

allRegions = cutClasses_eleID(ID) #standard manual nMinus1

sel = allRegions[WP][selection]

elePt = "Max$(LepGood_pt*(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && " + standardIDsel[WP] + "))"
plotDict = {\
   "elePt":{'var':elePt, "bins":[100,0,100], "decor":{"title": "Electron ID FoM Plot: %s_%s_%s"%(ID, selection, WP) ,"x":"Electron p_{T} / GeV" , "y":"Events" ,'log':[0,1,0]}},\
   "MT":{'var':"mt", "bins":[30,0,150], "decor":{"title": "Electron ID FoM Plot: %s_%s_%s"%(ID, selection, WP) ,"x":"M_{T} / GeV" , "y":"Events" ,'log':[0,1,0]}},\
   "MET":{'var':"met", "bins":[20,150,900], "decor":{"title": "Electron ID FoM Plot: %s_%s_%s"%(ID, selection, WP) ,"x":"Missing E_{T} / GeV" , "y":"Events" ,'log':[0,1,0]}},\
   #"HT":{'var':"ht", "bins":[100,0,100], "decor":{"title": "Electron ID FoM Plot: %s_%s_%s"%(ID, selection, WP) ,"x":"H_{T} / GeV" , "y":"Events" ,'log':[0,1,0]}}\
}

plots = Plots(**plotDict)
plotsList = ["elePt","MT", "MET"]#, "HT"]

getPlots(samples, plots, sel, selectedSamples, plotList = plotsList)# addOverFlowBin='both')
fomPlots = drawPlots(samples, plots, sel, sampleList=selectedSamples, plotList = plotsList, fom="AMSSYS", denoms=["bkg"], noms=["s30FS"], fomLimits=[0,2], save=False)#, plotMin=0.001)

#c1 = fomPlots['canvs']['elePt'][0]
#c2 = fomPlots['canvs']['mt'][0]
#c3 = fomPlots['canvs']['met'][0]
#c4 = fomPlots['canvs']['ht'][0]
#print "INFO: ", ID, " ", selection, " ", WP
 
#fomPlots['stacks']['bkg']['LepPt'].SetTitle("Electron ID FoM Plot:" + selection + " (" + WP + " ID)")
#fomPlots['stacks']['bkg']['LepPt'].GetHistogram().CenterTitle()
#fomPlots['fomHists']['LepPt']['bkg']['denom'].GetXaxis().SetTitle("Electron p_{T} / GeV")
#fomPlots['fomHists']['LepPt']['bkg']['denom'].SetStats(0)

#ROOT.gStyle.SetTitleAlign(13)
#ROOT.gStyle.SetTitleX(0.1)
#ROOT.gStyle.SetTitleW(0.8)
#hists['None'].Write()

#ROOT.gPad.SetLogy()
#ROOT.gPad.Modified()
#ROOT.gPad.Update()
#   if plot == "efficiency":
#      l1.AddEntry("eleID_WP90", "MVA ID (WP90)", "F")
#      l1.AddEntry("eleID_WP80", "MVA ID (WP80)", "F")
#
#ROOT.gPad.Modified()
#ROOT.gPad.Update()
#
#l1.Draw()

#if not os.path.isfile(savedir  + "/histogramCounts/histogramCounts_" + plot + "_" + samples[sample].name + ".txt"):
#   outfile = open(savedir + "/histogramCounts/histogramCounts_" + plot + "_" + samples[sample].name + ".txt", "w")
#   outfile.write(\
#   plot +": Histogram Counts (" + samples[sample].name + ")\n")
#   if plot == "efficiency" or plot == "misID2":
#      outfile.write(\
#      "Variable     Total     Veto     Loose     Medium     Tight\n")

#if plot == "efficiency" or plot == "misID2":
#   with open(savedir + "/histogramCounts/histogramCounts_" + plot + "_" + samples[sample].name + ".txt", "a") as outfile:
#      outfile.write(removedCut + "      " + str(hists['None'].GetEntries()) + "      " + \
#      str(hists['Veto'].GetEntries()) + "     " + str(hists_passed['Loose'].GetEntries()) + "     " + str(hists_passed['Medium'].GetEntries()) + "      " + str(hists_passed['Tight'].GetEntries()) + "\n")

#c1.Modified()
#c1.Update()

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   for canv in fomPlots['canvs']:
      if not os.path.exists("%s/%s/root"%(savedir, canv)): os.makedirs("%s/%s/root"%(savedir, canv))
      if not os.path.exists("%s/%s/pdf"%(savedir, canv)): os.makedirs("%s/%s/pdf"%(savedir, canv))

      if removedCut == "None":
         #if ID == "iso":
         #   fomPlots['canvs'][canv][0].SaveAs(savedir + "/" + plot + "_" + isolation + "_" + samples[sample].name + z + ".png")
         #   fomPlots['canvs'][canv][0].SaveAs(savedir + "/root/" + plot + "_" + isolation + "_" + samples[sample].name + z + ".root")
         #   fomPlots['canvs'][canv][0].SaveAs(savedir + "/pdf/" + plot + "_" + isolation + "_" + samples[sample].name + z + ".pdf")
         #else: 
         fomPlots['canvs'][canv][0].SaveAs("%s/%s/eleID_FoM_%s_%s.png"%(savedir, canv, sel.name, canv))
         fomPlots['canvs'][canv][0].SaveAs("%s/%s/root/eleID_FoM_%s_%s.root"%(savedir, canv, sel.name, canv))
         fomPlots['canvs'][canv][0].SaveAs("%s/%s/pdf/eleID_FoM_%s_%s.pdf"%(savedir, canv, sel.name, canv))
      else:
         fomPlots['canvs'][canv][0].SaveAs("%s/%s/eleID_FoM_no_%s_%s_%s.png"%(savedir, canv, removedCut, sel.name, canv))
         fomPlots['canvs'][canv][0].SaveAs("%s/%s/root/eleID_FoM_no_%s_%s_%s.root"%(savedir, canv, removedCut, sel.name, canv))
         fomPlots['canvs'][canv][0].SaveAs("%s/%s/pdf/eleID_FoM_no_%s_%s_%s.pdf"%(savedir, canv, sel.name, canv)) 
