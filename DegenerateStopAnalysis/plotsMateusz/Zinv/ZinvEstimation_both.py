# ZinvEstimation.py
import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setup_style
from Workspace.DegenerateStopAnalysis.tools.getSamples_8011 import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed

from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--SR", dest = "SR",  help = "SR", type = str, default = "SR1") # 'SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1', 'SRH1', 'SRV1', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c'
parser.add_argument("--CT2", dest = "CT2",  help = "CT2 Cut", type = str, default = "75")
#parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "200")
#parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "200")
parser.add_argument("--Zpeak", dest = "Zpeak",  help = "Zpeak plot", type = int, default = 0)
parser.add_argument("--emulated", dest = "emulated",  help = "Emulated plot", type = int, default = 1)
parser.add_argument("--peak", dest = "peak",  help = "Z-peak selection", type = int, default = 0)
parser.add_argument("--leptons", dest = "leptons",  help = "Extra lepton distributions", type = int, default = 0)
parser.add_argument("--doYields", dest = "doYields",  help = "Calulate yields", type = int, default = 1)
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 1)
parser.add_argument("--dataset", dest = "dataset",  help = "Dataset", type = str, default = "SingleMu")
parser.add_argument("--plot", dest = "plot",  help = "Toggle plot", type = int, default = 0)
parser.add_argument("--logy", dest = "logy",  help = "Toggle logy", type = int, default = 1)
parser.add_argument("--save", dest = "save",  help = "Toggle save", type = int, default = 1)
parser.add_argument("--verbose", dest = "verbose",  help = "Verbosity switch", type = int, default = 0)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
SR = args.SR
CT2cut = args.CT2
Zpeak = args.Zpeak
emulated = args.emulated
peak = args.peak
leptons = args.leptons
#METcut = args.MET
#HTcut = args.HT
doYields = args.doYields
getData = args.getData
dataset = args.dataset
plot = args.plot
logy = args.logy
save = args.save
verbose = args.verbose

print makeDoubleLine()
print "Performing Zinv estimation."
print makeDoubleLine()

#Samples
cmgPP = cmgTuplesPostProcessed()#mc_path, signal_path, data_path)
samplesList = ["vv", "tt", "dy"] #"qcd", "w", "z", 
if getData: 
   if dataset == "SingleMu": 
      dataKey = "d1muBlind"
      samplesList.append(dataKey)
      
      dileptonic = "mu" #dileptonic system Z->ll
      lepton = "el"
   elif dataset == "SingleEl": 
      dataKey = "d1elBlind"
      samplesList.append(dataKey)
      
      dileptonic = "el"
      lepton = "mu"

samples = getSamples(cmgPP = cmgPP, skim = 'oneLep', sampleList = samplesList, scan = False, useHT = True, getData = getData) 

if verbose:
   print makeLine()
   print "Using samples:"
   newLine()
   for s in samplesList:
      if s: print samples[s].name,":",s
      else: 
         print "!!! Sample " + sample + " unavailable."
         sys.exit(0)
   
   collection = "LepAll" 
   print makeLine()
   print "Using " + collection + " collection."
   print makeLine()

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/Zinv"
   if getData: savedir += "/" + dataset
   savedir += "/" + SR
   
   savedir1 = savedir + "/beforeEmul"
   savedir2 = savedir + "/afterEmul/" + CT2cut
   
   suffix = "_" + SR

   if peak: 
      suffix = "_peak"
      savedir1 += "/peak"
      savedir2 += "/peak"

   if not os.path.exists("%s/root"%(savedir1)): os.makedirs("%s/root"%(savedir1))
   if not os.path.exists("%s/pdf"%(savedir1)): os.makedirs("%s/pdf"%(savedir1))
   if not os.path.exists("%s/root"%(savedir2)): os.makedirs("%s/root"%(savedir2))
   if not os.path.exists("%s/pdf"%(savedir2)): os.makedirs("%s/pdf"%(savedir2))

#Geometric cuts
#etaAcc = 2.1
#ebSplit = 0.8 #barrel is split into two regions
#ebeeSplit = 1.479 #division between barrel and endcap

#Indicies of leading muons
ind1 = "IndexLepAll_%s[0]"%(dileptonic)
ind2 = "IndexLepAll_%s[1]"%(dileptonic)

dilepton_mass = "sqrt(2*(LepAll_pt[" + ind1 + "] * LepAll_pt[" + ind2 + "]*(cosh(LepAll_eta[" + ind1 + "] - LepAll_eta[" + ind2 + "]) - cos(LepAll_phi[" + ind1 + "] - LepAll_phi[" + ind2 + "]))))"
dilepton_pt = "sqrt(LepAll_pt[" + ind1 + "]*LepAll_pt[" + ind1 + "] + LepAll_pt[" + ind2 + "]*LepAll_pt[" + ind2 + "] + 2*(LepAll_pt[" + ind1 + "]*LepAll_pt[" + ind2 + "]*cos(LepAll_phi[" + ind1 + "] - LepAll_phi[" + ind2 + "])))"
met2 = "met + dilepton_pt"
#met2_phi = 
#electron_mt2 = "sqrt(2*met2*LepAll_pt[IndexLepAll_el[0]]*(1 - cos(met2_phi - LepAll_phi[IndexLepAll_el[0]])))"
#muon_mt2 = "sqrt(2*met2*LepAll_pt[IndexLepAll_mu[2]]*(1 - cos(met2_phi - LepAll_phi[IndexLepAll_mu[2]])))"

for s in samplesList: 
   samples[s].tree.SetAlias("dilepton_mass", dilepton_mass)
   samples[s].tree.SetAlias("dilepton_pt", dilepton_pt)
   samples[s].tree.SetAlias("met2", met2)
   #samples[s].tree.SetAlias("met2_phi", met2_phi)
   #samples[s].tree.SetAlias("electron_mt2", electron_mt2)
   #samples[s].tree.SetAlias("muon_mt2", muon_mt2)

def regions(ind):
   SRs = {\
      'SR1':["SR1","LepAll_pt[" + ind + "] < 30"],
   
      'SR1a':["SR1a", combineCuts("LepAll_mt[" + ind + "] < 60", "LepAll_pt[" + ind + "] < 30")],
      'SR1b':["SR1b", combineCuts(btw("LepAll_mt[" + ind + "]", 60, 95), "LepAll_pt[" + ind + "] < 30")],
      'SR1c':["SR1c", combineCuts("LepAll_mt[" + ind + "] > 95", "LepAll_pt[" + ind + "] < 30")],
      
      'SRL1':["SRL1", btw("LepAll_pt[" + ind + "]", 5, 12)],
      'SRH1':["SRH1", btw("LepAll_pt[" + ind + "]", 12, 20)],
      'SRV1':["SRV1", btw("LepAll_pt[" + ind + "]", 20, 30)],
   
      'SRL1a':["SRL1a", combineCuts("LepAll_mt[" + ind + "] < 60", btw("LepAll_pt[" + ind + "]", 5, 12))],
      'SRH1a':["SRH1a", combineCuts("LepAll_mt[" + ind + "] < 60", btw("LepAll_pt[" + ind + "]", 12, 20))],
      'SRV1a':["SRV1a", combineCuts("LepAll_mt[" + ind + "] < 60", btw("LepAll_pt[" + ind + "]", 20, 30))],
   
      'SRL1b':["SRL1b", combineCuts(btw("LepAll_mt[" + ind + "]", 60, 95), btw("LepAll_pt[" + ind + "]", 5, 12))],
      'SRH1b':["SRH1b", combineCuts(btw("LepAll_mt[" + ind + "]", 60, 95), btw("LepAll_pt[" + ind + "]", 12, 20))],
      'SRV1b':["SRV1b", combineCuts(btw("LepAll_mt[" + ind + "]", 60, 95), btw("LepAll_pt[" + ind + "]", 20, 30))],
   
      'SRL1c':["SRL1c", combineCuts("LepAll_mt[" + ind + "] > 95", btw("LepAll_pt[" + ind + "]", 5, 12))],
      'SRH1c':["SRH1c", combineCuts("LepAll_mt[" + ind + "] > 95", btw("LepAll_pt[" + ind + "]", 12, 20))],
      'SRV1c':["SRV1c", combineCuts("LepAll_mt[" + ind + "] > 95", btw("LepAll_pt[" + ind + "]", 20, 30))]}
   return SRs

#SRs
if dileptonic == "mu":
   ind_mu = "IndexLepAll_mu[2]"
   ind_el = "IndexLepAll_el[0]"
elif dileptonic == "el":
   ind_mu = "IndexLepAll_mu[0]"
   ind_el = "IndexLepAll_el[2]"

SRs_el = regions(ind_el)
SRs_mu = regions(ind_mu)

if peak:
   peak = CutClass("Zpeak", [
      ["dilep", "nLepAll_%s >= 2"%(dileptonic)],
      ["Zpeak","abs(dilepton_mass - 91.1876) < 15"],
      ], baseCut = None)
else:
   peak = CutClass("None", [["None","1"]], baseCut = None)

#Preselection & basic SR cuts
dilepton = CutClass("dilepton", [
   ["ISR100", "nIsrJet >= 1"],
   ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
   ["BVeto","nBSoftJet == 0 && nBHardJet == 0"],
   ["No3rdJet60","nVetoJet <= 2"],
   ["dilep", "nLepAll_%s >= 2"%(dileptonic)], 
   ["dilep-lep30Veto-2Lep20Veto", "((nLepAll_{dilep} == 2 && nLepAll_{lep} == 0) ||\
                                    (nLepAll_{dilep} == 2 && nLepAll_{lep} == 1 && LepAll_pt[IndexLepAll_{lep}[0]] < 30) ||\
                                    (nLepAll_{dilep} == 2 && nLepAll_{lep} == 2 && LepAll_pt[IndexLepAll_{lep}[0]] < 30 && LepAll_pt[IndexLepAll_{lep}[1]] < 20) ||\
                                    (nLepAll_{dilep} == 3 && nLepAll_{lep} == 0 && LepAll_pt[IndexLepAll_{dilep}[2]] < 30) ||\
                                    (nLepAll_{dilep} == 4 && nLepAll_{lep} == 0 && LepAll_pt[IndexLepAll_{dilep}[2]] < 30 && LepAll_pt[IndexLepAll_{dilep}[3]] < 20))".format(dilep = dileptonic, lep = lepton)],
    
   #["muon1", "abs(LepAll_pdgId[" + ind1 + "]) == 13"], #redundant with index sel
   ["relIso", "LepAll_relIso03[" + ind1 + "] < 0.12"],
   ["pt28", "LepAll_pt[" + ind1 + "] > 28"],
   # 
   #["muon2", "abs(LepAll_pdgId[" + ind2 + "]) == 13"], #redundant with index sel
   ["relIso", "LepAll_relIso03[" + ind2 + "] < 0.12"],
   ["pt20", "LepAll_pt[" + ind2 + "] > 20"],
   #
   ["OS", "LepAll_pdgId[" + ind1 + "] == -LepAll_pdgId[" + ind2 + "]"],
   #
   ["dilepton_mass","dilepton_mass > 55"],
   #["dilepton_pt","dilepton_pt > 75"],
   ["met2","met2 > 75"],
   ], baseCut = peak)

emulated = CutClass("emulated", [
   ["CT2","min(met2, ht_basJet - 100) >" + CT2cut],
   ], baseCut = dilepton)

leptons1 = CutClass("leptons1", [
   ["1lep","nLepAll_%s >= 1"%(lepton)],
   SRs_el[SR]
   ], baseCut = emulated)

leptons2 = CutClass("leptons2", [
   ["3lep","nLepAll_%s >= 3"%(dileptonic)],
   SRs_mu[SR]
   ], baseCut = emulated)

yields = {}
if doYields and peak:
   yields['Zpeak'] = Yields(samples, samplesList, emulated, cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
   yields['N1'] = Yields(samples, samplesList, leptons1, cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
   yields['N2'] = Yields(samples, samplesList, leptons2, cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
   
   if not os.path.isfile(savedir + "/ZinvYields" + suffix + ".txt"):
      outfile = open(savedir + "/ZinvYields" + suffix + ".txt", "w")
      outfile.write("Zinv Estimation Yields\n")
      outfile.write("CT        Zpeak_data                  Zpeak_DY                   Zpeak_TT                    N{lep}_data                   N{lep}_DY                   N{lep}_TT                   N{dilep}_data                  N{dilep}_DY                 N{dilep}_TT\n".format(dilep = dileptonic, lep = lepton))
   
   with open(savedir + "/ZinvYields" + suffix + ".txt", "a") as outfile:
      outfile.write(CT2cut + "     " +\
      str(yields['Zpeak'].yieldDictFull[dataKey]['emulated'].round(2)) + "              " +\
      str(yields['Zpeak'].yieldDictFull['dy']['emulated'].round(2)) + "              " +\
      str(yields['Zpeak'].yieldDictFull['tt']['emulated'].round(2)) + "              " +\
      str(yields['N1'].yieldDictFull[dataKey]['leptons1'].round(2)) + "              " +\
      str(yields['N1'].yieldDictFull['dy']['leptons1'].round(2)) + "              " +\
      str(yields['N1'].yieldDictFull['tt']['leptons1'].round(2)) + "              " +\
      str(yields['N2'].yieldDictFull[dataKey]['leptons2'].round(2)) + "              " +\
      str(yields['N2'].yieldDictFull['dy']['leptons2'].round(2)) + "              " +\
      str(yields['N2'].yieldDictFull['tt']['leptons2'].round(2)) + "\n")

   Zpeak_dMC = (yields['Zpeak'].yieldDictFull[dataKey]['emulated']/(yields['Zpeak'].yieldDictFull['dy']['emulated'] + yields['Zpeak'].yieldDictFull['tt']['emulated'])).round(3)
   prob_el_data = (yields['N1'].yieldDictFull[dataKey]['leptons1']/yields['Zpeak'].yieldDictFull[dataKey]['emulated'])
   prob_el_MC = ((yields['N1'].yieldDictFull['dy']['leptons1'] + yields['N1'].yieldDictFull['tt']['leptons1'])/(yields['Zpeak'].yieldDictFull['dy']['emulated'] + yields['Zpeak'].yieldDictFull['tt']['emulated']))
   prob_el_dMC = (prob_el_data/prob_el_MC).round(3)
   prob_mu_data = (yields['N2'].yieldDictFull[dataKey]['leptons2']/yields['Zpeak'].yieldDictFull[dataKey]['emulated'])
   prob_mu_MC = ((yields['N2'].yieldDictFull['dy']['leptons2'] + yields['N2'].yieldDictFull['tt']['leptons2'])/(yields['Zpeak'].yieldDictFull['dy']['emulated'] + yields['Zpeak'].yieldDictFull['tt']['emulated']))
   prob_mu_dMC = (prob_mu_data/prob_mu_MC).round(3)
   ratio_el = (Zpeak_dMC*prob_el_dMC).round(3)
   ratio_mu = (Zpeak_dMC*prob_mu_dMC).round(3)
 
   if not os.path.isfile(savedir + "/ZinvRatios" + suffix + ".txt"):
      outfile = open(savedir + "/ZinvRatios" + suffix + ".txt", "w")
      outfile.write("Zinv Estimation Ratios\n")
      outfile.write("CT       Zpeak_data_MC           prob_{lep}_data           prob_{lep}_MC           prob_{lep}_data_MC           prob_{dilep}_data          prob_{dilep}_MC          prob_{dilep}_data_MC          Ratio_{lep}         Ratio_{dilep}\n".format(dilep = dileptonic, lep = lepton))
   
   with open(savedir + "/ZinvRatios" + suffix + ".txt", "a") as outfile:
      outfile.write(CT2cut + "       " +\
      str(Zpeak_dMC) + "            " +\
      str(prob_el_data.round(3)) + "            " +\
      str(prob_el_MC.round(3)) + "            " +\
      str(prob_el_dMC) + "            " +\
      str(prob_mu_data.round(3)) + "            " +\
      str(prob_mu_MC.round(3)) + "            " +\
      str(prob_mu_dMC) + "            " +\
      str(ratio_el) + "            " +\
      str(ratio_mu)+ "\n")

if plot:
   
   plotDict = {\
      "dilepton_mass":{'var':"dilepton_mass", "bins":[50, 0, 250], "decor":{"title": "Di-lepton System Invariant Mass Distribution" ,"x":"M_{ll} / GeV" , "y":"Events", 'log':[0, logy,0]}},
      "dilepton_pt":{'var':"dilepton_pt", "bins":[50, 0, 250], "decor":{"title": "Di-lepton System Transverse Momentum Distribution" ,"x":"p_{T_{ll}} / GeV" , "y":"Events", 'log':[0, logy,0]}},
      "MET":{'var':"met", "bins":[50,0,500], "decor":{"title": "MET Distribution" ,"x":"Missing E_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
      "HT":{'var':"ht_basJet", "bins":[50,0,500], "decor":{"title": "H_{{T}} Distribution","x":"H_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
      "nJets30":{'var':"nBasJet", "bins":[10,0,10], "decor":{"title":"Number of Jets with p_{{T}} > 30GeV", "x":"Number of Jets with p_{T} > 30GeV", "y":"Events", 'log':[0,1,0]}},      
      "nJets60":{'var':"nVetoJet", "bins":[10,0,10], "decor":{"title":"Number of Jets with p_{{T}} > 60GeV", "x":"Number of Jets with p_{T} > 60GeV", "y":"Events", 'log':[0,1,0]}},
      "ISRpt":{'var':"Jet_pt[IndexJet_basJet[0]]", "bins":[45,100,1000], "decor":{"title":"Leading Jet p_{{T}}","x":"ISR Jet p_{T}","y":"Events", 'log':[0,1,0]}},
   }
      
   plotDict2 = plotDict.copy()
   plotDict2["MET2"] = {'var':"met2", "bins":[50,0,500], "decor":{"title": "Emulated MET Distribution" ,"x":"Emulated Missing E_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}}
   if dileptonic == "mu": 
      plotDict3 = {\
         "elPt":{'var':"LepAll_pt[IndexLepAll_el[0]]", "bins":[10,0,50], "decor":{"title": "Electron pT Distribution" ,"x":"Electron p_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "muPt":{'var':"LepAll_pt[IndexLepAll_mu[2]]", "bins":[10,0,50], "decor":{"title": "Muon pT Distribution" ,"x":"Muon p_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         #"electron_mt2":{'var':"electron_mt2", "bins":[10,0,100], "decor":{"title": "Electron mT Distribution" ,"x":"Electron m_{T2} / GeV" , "y":"Events", 'log':[0,logy,0]}}, 
         #"muon_mt2":{'var':"muon_mt2", "bins":[10,0,100], "decor":{"title": "Muon mT Distribution" ,"x":"Muon m_{T2} / GeV" , "y":"Events", 'log':[0,logy,0]}}, 
      }
   if dileptonic == "el": 
      plotDict3 = {\
         "elPt":{'var':"LepAll_pt[IndexLepAll_el[2]]", "bins":[10,0,50], "decor":{"title": "Electron pT Distribution" ,"x":"Electron p_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         "muPt":{'var':"LepAll_pt[IndexLepAll_mu[0]]", "bins":[10,0,50], "decor":{"title": "Muon pT Distribution" ,"x":"Muon p_{T} / GeV" , "y":"Events", 'log':[0,logy,0]}},
         #"electron_mt2":{'var':"electron_mt2", "bins":[10,0,100], "decor":{"title": "Electron mT Distribution" ,"x":"Electron m_{T2} / GeV" , "y":"Events", 'log':[0,logy,0]}}, 
         #"muon_mt2":{'var':"muon_mt2", "bins":[10,0,100], "decor":{"title": "Muon mT Distribution" ,"x":"Muon m_{T2} / GeV" , "y":"Events", 'log':[0,logy,0]}}, 
      }
   
   plotsList = ["dilepton_mass", "dilepton_pt", "MET", "HT", "nJets30", "nJets60", "ISRpt"]
   plotsList2 = plotsList + ["MET2"]
   
   plotsDict = Plots(**plotDict)
   plotsDict2 = Plots(**plotDict2)
   plotsDict3 = Plots(**plotDict3)
   
   if Zpeak:
      dileptonPlots = getPlots(samples, plotsDict, dilepton, samplesList, plotList = plotsList, addOverFlowBin='upper')
      dileptonPlots2 = drawPlots(samples, plotsDict, dilepton, samplesList, plotList = plotsList, plotLimits = [10, 100], denoms=["bkg"], noms = [dataKey], fom="RATIO", fomLimits=[0,2.8], plotMin = 0.01, normalize = False, save=False)
   
   if emulated:
      emulatedPlots = getPlots(samples, plotsDict2, emulated, samplesList, plotList = plotsList2, addOverFlowBin='upper')
      emulatedPlots2 = drawPlots(samples, plotsDict2, emulated, samplesList, plotList = plotsList2, plotLimits = [10, 100], denoms=["bkg"], noms = [dataKey], fom="RATIO", fomLimits=[0,2.8], plotMin = 0.01, normalize = False, save=False)
   
   if leptons:
      lep1Plots = getPlots(samples, plotsDict3, leptons1, samplesList, plotList = ["%sPt"%(lepton)], addOverFlowBin='upper')
      lep1Plots2 = drawPlots(samples, plotsDict3, leptons1, samplesList, plotList = ["%sPt"%(lepton)], plotLimits = [10, 100], denoms=["bkg"], noms = [dataKey], fom="RATIO", fomLimits=[0,2.8], plotMin = 0.01, normalize = False, save=False)
      
      lep2Plots = getPlots(samples, plotsDict3, leptons2, samplesList, plotList = ["%sPt"%(dileptonic)], addOverFlowBin='upper')
      lep2Plots2 = drawPlots(samples, plotsDict3, leptons2, samplesList, plotList = ["%sPt"%(dileptonic)], plotLimits = [10, 100], denoms=["bkg"], noms = [dataKey], fom="RATIO", fomLimits=[0,2.8], plotMin = 0.01, normalize = False, save=False)
   
   #Save canvas
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      if Zpeak:
         for canv in dileptonPlots2['canvs']:
            #if plot['canvs'][canv][0]:
            dileptonPlots2['canvs'][canv][0].SaveAs("%s/%s%s.png"%(savedir1, canv, suffix))
            dileptonPlots2['canvs'][canv][0].SaveAs("%s/root/%s%s.root"%(savedir1, canv, suffix))
            dileptonPlots2['canvs'][canv][0].SaveAs("%s/pdf/%s%s.pdf"%(savedir1, canv, suffix))
      if emulated:   
         for canv in emulatedPlots2['canvs']:
            #if plot['canvs'][canv][0]:
            emulatedPlots2['canvs'][canv][0].SaveAs("%s/%s%s.png"%(savedir2, canv, suffix))
            emulatedPlots2['canvs'][canv][0].SaveAs("%s/root/%s%s.root"%(savedir2, canv, suffix))
            emulatedPlots2['canvs'][canv][0].SaveAs("%s/pdf/%s%s.pdf"%(savedir2, canv, suffix))
      if leptons:   
         for canv in lep1Plots2['canvs']:
            #if plot['canvs'][canv][0]:
            lep1Plots2['canvs'][canv][0].SaveAs("%s/%s%s.png"%(savedir2, canv, suffix))
            lep1Plots2['canvs'][canv][0].SaveAs("%s/root/%s%s.root"%(savedir2, canv, suffix))
            lep1Plots2['canvs'][canv][0].SaveAs("%s/pdf/%s%s.pdf"%(savedir2, canv, suffix))
         for canv in lep2Plots2['canvs']:
            #if plot['canvs'][canv][0]:
            lep2Plots2['canvs'][canv][0].SaveAs("%s/%s%s.png"%(savedir2, canv, suffix))
            lep2Plots2['canvs'][canv][0].SaveAs("%s/root/%s%s.root"%(savedir2, canv, suffix))
            lep2Plots2['canvs'][canv][0].SaveAs("%s/pdf/%s%s.pdf"%(savedir2, canv, suffix))
