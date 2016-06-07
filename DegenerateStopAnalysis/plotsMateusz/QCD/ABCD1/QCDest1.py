#QCDest1.py
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

#Input options
parser = argparse.ArgumentParser(description = "Input options")
#parser.add_argument("--isolation", dest = "isolation",  help = "Isolation (hybIso03/hybIso04)", type = str, default = "hybIso03")
#parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "300")
#parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "300")
#parser.add_argument("--METloose", dest = "METloose",  help = "Loose MET Cut", type = str, default = "100")
#parser.add_argument("--eleWP", dest = "eleWP",  help = "Electron WP", type = str, default = "Veto")
#parser.add_argument("--enriched", dest = "enriched",  help = "EM enriched QCD?", type = bool, default = False)
parser.add_argument("--plot", dest = "plot",  help = "Toggle plot", type = int, default = 1)
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
#METcut = args.MET
#METloose = args.METloose
#HTcut = args.HT
#eleWP = args.eleWP
#enriched = args.enriched
plot = args.plot
save = args.save

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD1/estimation/QCDest1"
   if not os.path.exists(savedir): os.makedirs(savedir)

#Samples
#if enriched == True: qcd = "qcdem"
#else: qcd = "qcd"

privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
backgrounds = ["w","tt", "z", "qcd"]

cmgPP = cmgTuplesPostProcessed()#mc_path, signal_path, data_path)

samplesList = backgrounds # + privateSignals
samples = getSamples(cmgPP = cmgPP, skim = 'presel', sampleList = samplesList, scan = False, useHT = True, getData = False)

officialSignals = ["s300_290", "s300_270", "s300_250"] #FIXME: crosscheck if these are in allOfficialSignals

allOfficialSignals = samples.massScanList()
#allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
allSignals = privateSignals + allOfficialSignals
allSamples = allSignals + backgrounds

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

#suffix = "_HT" + HTcut + "_MET" + METcut + "_METloose" + METloose
#if enriched == True: suffix += "_EMenriched"

def QCDest(collection = "LepGood", samples = samples, plot = plot, save = save, savedir = savedir):
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
   #eleIDsel = electronIDs(ID = "standard", removedCut = "", iso = False)
   #allCuts = cutClasses(eleIDsel, ID = "standard")
   
   ##for s in samples.massScanList(): samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
   #for s in samples: samples[s].tree.SetAlias("eleSel", allCuts[WP]['eleSel'])

   etaAcc = 2.1
   eleSel = "abs(" + collection + "_pdgId) == 11 && abs(" + collection + "_eta) < " + str(etaAcc) + " && " + eleIDsel['Veto']
   eleSel_other = "abs(" + otherCollection + "_pdgId) == 11 && abs(" + otherCollection + "_eta) < " + str(etaAcc) + " && " + eleIDsel_other['Veto']
   
   #Cuts
   dxyCut = "abs(" + collection + "_dxy) < 0.02"
   antiDxyCut = "abs(" + collection + "_dxy) > 0.02"
   
   hybIsoCut = "(" + collection + "_relIso03*min(" + collection + "_pt, 25)) < 5"
   antiHybIsoCut = "(" + collection + "_relIso03*min(" + collection + "_pt, 25)) > 5"
   #hybIsoCut = "((" + collection + "_absIso03 < 5) || " + collection + "_relIso03 < 0.2))"
   #antiHybIsoCut = "((" + collection + "_absIso03 > 5) && (" + collection + "_relIso03 > 0.2))"
      
   elePt = {}
   elePt['SR'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
   elePt['ID'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + "))"
   elePt['I_D'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
   elePt['D_I'] = "Max$(" + collection + "_pt*(" + eleSel + "&&" + hybIsoCut + "&&" + antiDxyCut + "))"
   
   eleMt = {}
   eleMt['SR'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
   eleMt['ID'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + "))"
   eleMt['I_D'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
   eleMt['D_I'] = "Max$(" + collection + "_mt*(" + eleSel + "&&" + hybIsoCut + "&&" + antiDxyCut + "))"
   
   presel = CutClass("presel_SR", [
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
      #["anti-dxy", "Max$(abs(" + lep + "_dxy*(" + eleSel + "&&" + antiHybIsoCut + "))) > 0.02"],
      ], baseCut = None) #allCuts['None']['presel'])
   
   SRs ={}
  
   for reg in ['SR', 'ID', 'I_D', 'D_I']:
      SRs[reg] = {\
         'SR1':["SR1","1"],
         'SR1a':["SR1a", eleMt[reg] + " < 60"],
         'SR1b':["SR1b", btw(eleMt[reg], 60, 88)],
         'SR1c':["SR1c", eleMt[reg] + " > 88"],

         'SRL1a':["SRL1a", joinCutStrings([eleMt[reg] + " < 60", btw(elePt[reg], 5, 12)])],
         'SRH1a':["SRH1a", joinCutStrings([eleMt[reg] + " < 60", btw(elePt[reg], 12, 20)])],
         'SRV1a':["SRV1a", joinCutStrings([eleMt[reg] + " < 60", btw(elePt[reg], 20, 30)])],
         
         'SRL1b':["SRL1b", joinCutStrings([btw(eleMt[reg], 60, 88), btw(elePt[reg], 5, 12)])],
         'SRH1b':["SRH1b", joinCutStrings([btw(eleMt[reg], 60, 88), btw(elePt[reg], 12, 20)])],
         'SRV1b':["SRV1b", joinCutStrings([btw(eleMt[reg], 60, 88), btw(elePt[reg], 20, 30)])],
         
         'SRL1c':["SRL1c", joinCutStrings([eleMt[reg] + " > 88", btw(elePt[reg], 5, 12)])],
         'SRH1c':["SRH1c", joinCutStrings([eleMt[reg] + " > 88", btw(elePt[reg], 12, 20)])],
         'SRV1c':["SRV1c", joinCutStrings([eleMt[reg] + " > 88", btw(elePt[reg], 20, 30)])]
      }
   
   QCD = {}
   QCDylds = {}
   plots = {}
   plots2 = {}
   
   regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']
    
   for reg in regions:
      print "Signal sub-region: ", reg 
      QCD[reg] = {}
     
      #SR 
      QCD[reg]['SR'] = CutClass("QCD_SR_" + reg, [
         #["elePt<30", elePt['ID'] + " < 30"],
         SRs['SR'][reg],
         ["A", "vetoJet_dPhi_j1j2 < 2.5"],
         ["ID", "Sum$(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + ") == 1"],
         ], baseCut = presel)

      #nA
      QCD[reg]['ID_A'] = CutClass("QCD_ID_A", [
         #["elePt<30", elePt['ID'] + " < 30"],
         SRs['ID'][reg], 
         ["A", "vetoJet_dPhi_j1j2 < 2.5"], #applied
         ["anti-ID", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + ") == 1"], #inverted, inverted
         ], baseCut = presel)
      
      #nI
      QCD[reg]['DA_I'] = CutClass("QCD_DA_I", [
         #["elePt<30", elePt['D_I'] + " < 30"],
         SRs['D_I'][reg], 
         ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
         ["I+anti-D", "Sum$(" + eleSel + "&&" + hybIsoCut + "&&" + antiDxyCut + ") == 1"], #applied, inverted
         ], baseCut = presel)
      
      #nD
      QCD[reg]['IA_D'] = CutClass("QCD_IA_D", [
         #["elePt<30", elePt['I_D'] + " < 30"],
         SRs['I_D'][reg], 
         ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
         ["anti-I+D", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + ") == 1"], #inverted, applied
         ], baseCut = presel)
      
      #nIDA
      QCD[reg]['IDA'] = CutClass("QCD_IDA", [
         #["elePt<30", elePt['ID'] + " < 30"],
         SRs['ID'][reg], 
         ["anti-A", "vetoJet_dPhi_j1j2 > 2.5"], #inverted
         ["anti-ID", "Sum$(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + ") == 1"], #inverted, inverted
         ], baseCut = presel) 
   
      if plot:
         hybIso = {}
         hybIso['SR'] = "Max$((" + collection + "_relIso03*min(" + collection + "_pt, 25))*(" + eleSel + "&&" + hybIsoCut + "&&" + dxyCut + "))"
         hybIso['ID'] = "Max$((" + collection + "_relIso03*min(" + collection + "_pt, 25))*(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + "))"
         hybIso['I_D'] = "Max$((" + collection + "_relIso03*min(" + collection + "_pt, 25))*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + "))"
         hybIso['D_I'] = "Max$((" + collection + "_relIso03*min(" + collection + "_pt, 25))*(" + eleSel + "&&" + hybIsoCut + "&&" + antiDxyCut + "))"
         
         #absDxy = "Max$(abs(" + collection + "_dxy*(" + eleSel + ")))"
         #absDxy_ID = "Max$(abs(" + collection + "_dxy*(" + eleSel + "&&" + antiHybIsoCut + "&&" + antiDxyCut + ")))"
         #absDxy_I_D = "Max$(abs(" + collection + "_dxy*(" + eleSel + "&&" + antiHybIsoCut + "&&" + dxyCut + ")))"
         #absDxy_D_I = "Max$(abs(" + collection + "_dxy*(" + eleSel + "&&" + hybIsoCut + "&&" + antiDxyCut + ")))"
         plotDict = {} 
         plotsDict = {} 
         plots[reg] = {}
         plots2[reg] = {}
         
         selections = {'SR':'SR', 'ID_A':'ID', 'DA_I':'D_I', 'IA_D':'I_D', 'IDA':'ID'}
         
         for sel in selections.keys(): 
         
            print sel, " ", selections[sel]
            
            plotDict[sel] = {
               "hybIso2_" + sel:{'var':"(log(1 + " + hybIso[selections[sel]] + ")/log(1+5))", "bins":[6, 0, 3], "decor":{"title": "Electron hybIso Plot" ,"x":"log(1+HI)/log(1+5)" , "y":"Events"}},#"log":[0,1,0]
            }
            
            plotsDict[sel] = Plots(**plotDict[sel])
            plots[reg][sel] = getPlots(samples, plotsDict[sel], QCD[reg][sel], selectedSamples, plotList = ["hybIso2_" + sel], addOverFlowBin='upper')
            plots2[reg][sel] = drawPlots(plots[reg][sel], fom=False, save=False, plotMin = 0.1)
            
         ROOT.gPad.Modified()
         ROOT.gPad.Update()
         
         nSR2 = plots2[reg]['SR']['hists']['qcd']['hybIso2_SR'].Integral(0, 100)
         nA2 = plots2[reg]['ID_A']['hists']['qcd']['hybIso2_ID_A'].Integral(0, 100)
         nI2 = plots2[reg]['DA_I']['hists']['qcd']['hybIso2_DA_I'].Integral(0, 100)
         nD2 = plots2[reg]['IA_D']['hists']['qcd']['hybIso2_IA_D'].Integral(0, 100)
         nIDA2 = plots2[reg]['IDA']['hists']['qcd']['hybIso2_IDA'].Integral(0, 100)
        
         if nA2 and nI2 and nD2 and nIDA2: 
            QCDexp2 = (nA2 * nI2 * nD2)/(nIDA2*nIDA2)
         
            print makeLine()
            print "1. For region ", reg, ": nA, nI, nD, nIDA = ", nA2, nI2, nD2, nIDA2
            print "1. QCD Estimation in ", reg, ": ", QCDexp2
            print "1. QCD MC yield in ", reg, ": ", nSR2
            print makeLine()
         else:
            print "1. !!! WARNING! Yield of ", reg, " is zero."
            #continue
      
         #Save canvas
         if save: #web address: http://www.hephy.at/user/mzarucki/plots/QCD
            if not os.path.exists("%s/%s/root"%(savedir, reg)): os.makedirs("%s/%s/root"%(savedir, reg))
            if not os.path.exists("%s/%s/pdf"%(savedir, reg)): os.makedirs("%s/%s/pdf"%(savedir, reg))
            
            for sel in selections.keys():
               for plot in plots2:
                  for canv in plots2[plot][sel]['canvs']:
                     if plots2[plot][sel]['canvs'][canv][0]:
                        plots2[plot][sel]['canvs'][canv][0].SaveAs("%s/%s/%s.png"%(savedir, reg, canv))
                        plots2[plot][sel]['canvs'][canv][0].SaveAs("%s/%s/root/%s.root"%(savedir, reg, canv))
                        plots2[plot][sel]['canvs'][canv][0].SaveAs("%s/%s/pdf/%s.pdf"%(savedir, reg, canv))
     
      #yields = {}
      #yields['ID_A'] = Yields(samples, ['qcd'], QCD['ID_A'], cutOpt = "combinedList", weight = "weight", pklOpt = False, tableName = "QCD_ID_A", nDigits = 2, err = True, verbose = True, nSpaces = 10)
      #yields['DA_I'] = Yields(samples, ['qcd'], QCD['DA_I'], cutOpt = "combinedList", weight = "weight", pklOpt = False, tableName = "QCD_DA_I", nDigits = 2, err = True, verbose = True, nSpaces = 10)
      #yields['IA_D'] = Yields(samples, ['qcd'], QCD['IA_D'], cutOpt = "combinedList", weight = "weight", pklOpt = False, tableName = "QCD_IA_D", nDigits = 2, err = True, verbose = True, nSpaces = 10)
      #yields['IDA'] = Yields(samples, ['qcd'], QCD['IDA'], cutOpt = "combinedList", weight = "weight", pklOpt = False, tableName = "QCD_IDA", nDigits = 2, err = True, verbose = True, nSpaces = 10)
       
      nSR, nSRerr = getYieldFromChain(samples['qcd']['tree'], QCD[reg]['SR'].combined, weight = samples['qcd']['weight'], returnError=True)
      nA, nAerr = getYieldFromChain(samples['qcd']['tree'], QCD[reg]['ID_A'].combined, weight = samples['qcd']['weight'], returnError=True)
      nI, nIerr = getYieldFromChain(samples['qcd']['tree'], QCD[reg]['DA_I'].combined, weight = samples['qcd']['weight'], returnError=True)
      nD, nDerr = getYieldFromChain(samples['qcd']['tree'], QCD[reg]['IA_D'].combined, weight = samples['qcd']['weight'], returnError=True)
      nIDA, nIDAerr = getYieldFromChain(samples['qcd']['tree'], QCD[reg]['IDA'].combined, weight = samples['qcd']['weight'], returnError=True)
     
      QCDylds[reg] = {'nSR':nSR, 'nSRerr': nSRerr, 'nA':nA, 'nAerr':nAerr, 'nI':nI, 'nIerr':nIerr,'nD':nD, 'nDerr':nDerr, 'nIDA':nIDA, 'nIDAerr':nIDAerr}
    
      if 0 not in QCDylds[reg].values():
         QCDexp = (nA * nI * nD)/(nIDA*nIDA)
         QCDerr = QCDexp * sqrt((nAerr/nA)*(nAerr/nA) + (nIerr/nI)*(nIerr/nI) + (nDerr/nD)*(nDerr/nD) + 2*(nIDAerr/nIDA)*(nIDAerr/nIDA))
   
      else:
         print "2. !!!!! WARNING! Yield of ", reg, " is zero."
         continue
         
      print makeLine()
      print collection, " Collection:"
      print "2. For region ", reg, ": nI = ", nI, "+/-", nIerr, " | nD = ", nD, "+/-", nDerr, " | nA = ", nA, "+/-", nAerr, " | nIDA = ", nIDA, "+/-", nIDAerr
      print "2. QCD Estimation in ", reg, ": ", QCDexp, "+/-", QCDerr
      print "2. QCD MC yield in ", reg, ": ", nSR, "+/-", nSRerr
      print makeLine()
      
      if save:
         if not os.path.isfile(savedir + "/QCDyields_" + collection + ".txt"):
            outfile = open(savedir + "/QCDyields_" + collection + ".txt", "w")
            outfile.write(" SR           DA_I              IA_D               ID_A               IDA               QCD               MC               Ratio\n")
         with open(savedir + "/QCDyields_" + collection + ".txt", "a") as outfile:
            outfile.write(reg + "     " +\
            str("%.3f"%(nI)) + " +/- " + str("%.3f"%(nIerr)) + "     " +\
            str("%.3f"%(nD)) + " +/- " + str("%.3f"%(nDerr)) + "     " +\
            str("%.3f"%(nA)) + " +/- " + str("%.3f"%(nAerr)) + "     " +\
            str("%.3f"%(nIDA)) + " +/- " + str("%.3f"%(nIDAerr)) + "     " +\
            str("%.3f"%(QCDexp)) + " +/- " + str("%.3f"%(QCDerr)) + "     " +\
            str("%.3f"%(nSR)) + " +/- " + str("%.3f"%(nSRerr))  + "\n")
   
   if plot: ret = [plots2, QCDylds] 
   else: ret = [None, QCDylds]

   return ret

#LepGood & LepOther
   
#Save canvas
#if save: #web address: http://www.hephy.at/user/mzarucki/plots/QCD
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/ABCD1/estimation/QCDest1/combined" 
if not os.path.exists(savedir): os.makedirs(savedir)

QCDgood = QCDest("LepGood")
QCDother = QCDest("LepOther")

regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']
      
stackHists = {}
QCDtotal = {}
canvs = {}
plotsTotal = {}

print makeLine()
print "3. Adding results for LepGood and LepOther"
print makeLine()
for reg in regions:
   print "3. Yields for region ", reg , ":"
   print QCDgood[1][reg]
   print QCDother[1][reg]

   totalYlds = {}
   totalErr = {}
   
   for n in ['nSR', 'nA', 'nI', 'nD', 'nIDA']:
      #if n in QCDgood[1][reg] and 
      totalYlds[n] = QCDgood[1][reg][n] + QCDother[1][reg][n] 
      totalErr[n + 'err'] = sqrt(QCDgood[1][reg][n + 'err']*QCDgood[1][reg][n + 'err'] + QCDother[1][reg][n + 'err']*QCDother[1][reg][n + 'err']) 

   print "3. Total yields: ", totalYlds
   print makeLine()
   if 0 not in totalYlds.values(): 
      QCDexp = (totalYlds['nA'] * totalYlds['nI'] * totalYlds['nD'])/(totalYlds['nIDA']*totalYlds['nIDA'])
      QCDerr = QCDexp * sqrt(\
               (totalErr['nAerr']/totalYlds['nA'])*(totalErr['nAerr']/totalYlds['nA']) +\
               (totalErr['nIerr']/totalYlds['nI'])*(totalErr['nIerr']/totalYlds['nI']) +\
               (totalErr['nDerr']/totalYlds['nD'])*(totalErr['nDerr']/totalYlds['nD']) +\
               2*(totalErr['nIDAerr']/totalYlds['nIDA'])*(totalErr['nIDAerr']/totalYlds['nIDA']))
   
      print makeLine()
      print "3. nA = ", totalYlds['nA'], "+/-", totalErr['nAerr'], " | nI = ", totalYlds['nI'], "+/-", totalErr['nIerr'],\
            " | nD = ", totalYlds['nD'], "+/-", totalErr['nDerr'], " | nIDA = ", totalYlds['nIDA'], "+/-", totalErr['nIDAerr']
      print "3. QCD Estimation in ", reg, ": ", QCDexp, " +/- ", QCDerr
      print "3. QCD MC yields in ", reg, ": ", totalYlds['nSR'], " +/- ", totalErr['nSRerr']
      print makeLine()
 
      if not os.path.isfile(savedir + "/QCDyields_combined.txt"):
         outfile = open(savedir + "/QCDyields_combined.txt", "w")
         outfile.write(" SR           DA_I              IA_D               ID_A               IDA               QCD               MC               Ratio\n")
      with open(savedir + "/QCDyields_combined.txt", "a") as outfile:
         outfile.write(reg + "     " +\
         str("%.3f"%(totalYlds['nI'])) + " +/- " + str("%.3f"%(totalErr['nIerr'])) + "     " +\
         str("%.3f"%(totalYlds['nD'])) + " +/- " + str("%.3f"%(totalErr['nDerr'])) + "     " +\
         str("%.3f"%(totalYlds['nA'])) + " +/- " + str("%.3f"%(totalErr['nAerr'])) + "     " +\
         str("%.3f"%(totalYlds['nIDA'])) + " +/- " + str("%.3f"%(totalErr['nIDAerr'])) + "     " +\
         str("%.3f"%(QCDexp)) + " +/- " + str("%.3f"%(QCDerr)) + "     " +\
         str("%.3f"%(totalYlds['nSR'])) + " +/- " + str("%.3f"%(totalErr['nSRerr'])) + "     ")
         if totalYlds['nSR']:
            outfile.write(str(QCDexp/totalYlds['nSR'])  + "\n")
         else:
            outfile.write("\n")
                                            
   if plot:
      #Plots
      plotsGood = QCDgood[0]
      plotsOther = QCDother[0]
      
      selections = {'SR':'SR', 'ID_A':'ID', 'DA_I':'D_I', 'IA_D':'I_D', 'IDA':'ID'}

      stackHists[reg] = {}
      plotsTotal[reg] = {}
      canvs[reg] = {}
      
      for sel in selections: 
         stackHists[reg][sel] = []
      
         for samp in ['qcd', 'z', 'tt', 'w']:
            plotsGood[reg][sel]['hists'][samp]['hybIso2_' + sel].Add(plotsOther[reg][sel]['hists'][samp]['hybIso2_' + sel])
         
            stackHists[reg][sel].append(plotsGood[reg][sel]['hists'][samp]['hybIso2_' + sel])
      
         plotsTotal[reg][sel] = getStackFromHists(stackHists[reg][sel])
         canvs[reg][sel] = ROOT.TCanvas(reg + "_" + sel, reg + "_" + sel, 800, 800)
         plotsTotal[reg][sel].Draw("hist")
     
         decorAxis(plotsTotal[reg][sel], 'y', t = "Events", tOffset = 1.6, tSize = 0.045)
         decorAxis(plotsTotal[reg][sel], 'x', t = "log(1+HI)/log(1+5)", tOffset = 1.3, tSize = 0.04)
   
         canvs[reg][sel].SetRightMargin(10)
         #canvs[reg][sel].SetLeftMargin(15) 

         latex = ROOT.TLatex()
         latex.SetNDC()
         latex.SetTextSize(0.03)
         latex.SetTextAlign(11)

         latex.DrawLatex(0.20,0.89,"#font[22]{CMS Simulation}")
         latex.DrawLatex(0.60,0.89,"#bf{L = 2.3 fb^{-1} (13 TeV)}")
         
         canvs[reg][sel].RedrawAxis()
         canvs[reg][sel].Update()
 
         for sel in selections:
            if not os.path.exists("%s/root"%(savedir)): os.makedirs("%s/root"%(savedir))
            if not os.path.exists("%s/pdf"%(savedir)): os.makedirs("%s/pdf"%(savedir))
            #print canvs
            
            if sel in canvs[reg].keys(): 
               canvs[reg][sel].SaveAs("%s/%s.png"%(savedir, sel))
               canvs[reg][sel].SaveAs("%s/root/%s.root"%(savedir, sel))
               canvs[reg][sel].SaveAs("%s/pdf/%s.pdf"%(savedir, sel))
