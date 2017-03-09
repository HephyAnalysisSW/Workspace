# fakesEstimation.py
# Application of fake rate to estimate fake background contribution 
# Mateusz Zarucki 2017

import ROOT
import os, sys
import argparse
import copy
import pickle
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeDir
from Workspace.DegenerateStopAnalysis.tools.mvaTools import getMVATrees
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from Workspace.HEPHYPythonTools import u_float
from pprint import pprint
from array import array
from math import pi, sqrt #cos, sin, sinh, log
from fakeRegions import fakeRegions, fakeBinning

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--lep", dest = "lep", help = "Lepton", type = str, default = "el")
parser.add_argument("--region", dest = "reg", help = "Measurement or application region", type = str, default = "application_sr1")
parser.add_argument("--CT200", help = "Loosen CT cut to 200", action = "store_true")
parser.add_argument("--invAntiQCD", help = "Invert anti-QCD cut", action = "store_true")
parser.add_argument("--mva", help = "MVA", action = "store_true")
parser.add_argument("--measurementRegion", dest = "measurementRegion", help = "Measurement region", type = str, default = "measurement1")
parser.add_argument("--fakeRateMeasurement", dest = "fakeRateMeasurement", help = "Source of fake rate measurement", type = str, default = "MC")
parser.add_argument("--closureDef", dest="closureDef", help="Closure definition", type=str, default="standard")
parser.add_argument("--looseNotTight", help = "Loose-not-tight CR", action = "store_true")
parser.add_argument("--highPtBin", help = "High pt bin", action = "store_true")
parser.add_argument("--doPlots", dest="doPlots", help="Create plots", type=int, default=1)
parser.add_argument("--doYields", help = "Calculate yields", action = "store_true")
parser.add_argument("--doControlPlots", help = "Additional plots of regions", action = "store_true")
parser.add_argument("--getData", dest = "getData", help = "Get data", type = bool, default = True)
parser.add_argument("--varBins", help = "Variable bin size", action = "store_true")
parser.add_argument("--logy", action = "store_true", help = "Log scale")
parser.add_argument("--save", dest="save", help="Toggle save", type=int, default=1)
parser.add_argument("--verbose", help = "Verbosity switch", action = "store_true")
parser.add_argument("-b", dest="batch", help="Batch mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
lep = args.lep
reg = args.reg
CT200 = args.CT200
invAntiQCD = args.invAntiQCD
mva = args.mva
measurementRegion = args.measurementRegion
fakeRateMeasurement = args.fakeRateMeasurement
closureDef = args.closureDef
looseNotTight = args.looseNotTight
highPtBin = args.highPtBin
doPlots = args.doPlots
doYields = args.doYields
doControlPlots = args.doControlPlots
getData = args.getData
varBins = args.varBins
logy = args.logy
save = args.save
verbose = args.verbose

#Sets TDR style
setup_style()

#Samples
cmgPP = cmgTuplesPostProcessed()

# Application region
samplesList = ["st", "vv", "qcd", "z", "dy", "tt", "w"]
skim = "preIncLep"
getData = False #NOTE: For now, do not plot data near SR

if not "application" in reg:
   print "Region should be an application region."
   sys.exit()

samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = False, useHT = True, getData = getData, def_weights = [])

# Gets MVA friend trees
if mva:
   getMVATrees(samples, mvaIdIndex = 'Sum$((mva_methodId=={mvaId}) * Iteration$)'.format(mvaId = '30'))

if verbose:
   print makeLine()
   print "Using samples:"
   newLine()
   for s in samplesList:
      if s: print samples[s].name,":",s
      else:
         print "!!! Sample " + sample + " unavailable."
         sys.exit()

if lep == "el":    lepton = "Electron" #pdgId = "11"
elif lep == "mu":  lepton = "Muon" #pdgId = "13" 
elif lep == "lep": lepton = "Lepton"

if doPlots:
   # Tight-to-loose ratio
   
   if fakeRateMeasurement == "data-EWK": subtractPrompt = True #if using FR from data, subtract prompt 
   
   #Bin dir 
   binDir = "/TL_" + fakeRateMeasurement
   
   if not varBins: binDir += "/fixedBins"
   else:           binDir += "/varBins"
    
   # Root file with fake rate
   fakeRateDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate"
   
   fakeRateDir += "/" + measurementRegion
   
   fakeRateDir += binDir
   
   fakeRateFile = "FakeRate_TightToLoose_lepPt_%s_%s.root"%(lep, fakeRateMeasurement)
   
   if verbose:
      print makeLine()
      print "Using tight-to-loose ratio from ", fakeRateDir + "/" + fakeRateFile
      print makeLine()
   
   f1 = ROOT.TFile(fakeRateDir + "/" + fakeRateFile)
   
   TLratio = {}
   
   TLratio['pt'] = f1.Get("c1").GetPrimitive("c1_2").GetPrimitive("ratio_pt_%s"%fakeRateMeasurement)
   TLratio['eta'] = f1.Get("c1").GetPrimitive("c1_2").GetPrimitive("ratio_eta_%s"%fakeRateMeasurement)

#####

WPs = ['loose', 'tight']
selection = {}
for WP in WPs:
   selection.update(fakeRegions(samples, reg, lep, WP, highPtBin = highPtBin, mva = mva, CT200 = CT200, invAntiQCD = invAntiQCD))

setEventListToChains(samples, samplesList, selection['kinematic'][reg])

if verbose:
   print makeLine()
   print "Using the following selection: \n",
   pprint(selection)
   print "\n",
   print makeLine()

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakesEstimation"%tag

   if mva: savedir += "/%s_id%s_bdt%s"%(reg, selection['mvaId'], selection['bdtcut'])
   else:   savedir += "/%s"%reg
   
   if CT200 and invAntiQCD: savedir += "/CT200_invAntiQCD"
   elif CT200:              savedir += "/CT200"
   elif invAntiQCD:         savedir += "/invAntiQCD"
  
   savedir += "/" + measurementRegion
    
   if highPtBin: savedir += "/highPtBin"
   else:         savedir += "/allBins"

   savedir += "/estimation/%s"%lepton

   if looseNotTight: savedir += "/L!T"
   else:             savedir += "/Loose"
   
   savedir += binDir
   
   if logy: savedir += "/log"

   suffix = "%s_%s"%(reg, lep)
  
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

index = {}
pt = {}
eta = {}
mt = {}
hybIso = {}
regionSel = {}

for WP in ['loose', 'tight']:
   index[WP] = selection[WP]['lepIndex']
   pt[WP] = "LepGood_pt[%s]"%index[WP]
   mt[WP] = "LepGood_mt[%s]"%index[WP]
   eta[WP] = "abs(LepGood_eta[%s])"%index[WP]
   hybIso[WP] = "(LepGood_relIso03[{ind}]*min(LepGood_pt[{ind}], 25))".format(ind = index[WP])
   regionSel[WP] = selection[WP][reg][samplesList[0]][0] #NOTE: application region only

# Signal region
region = {'SR':{}, 'looseCR':{}}

region['SR']['total'] =  [selection['tight']['cuts'], selection['regDef']] 
region['SR']['prompt'] = [selection['tight']['cuts'], selection['regDef'] + '_prompt'] 
region['SR']['fake'] =   [selection['tight']['cuts'], selection['regDef'] + '_fake'] 

# Loose (not-Tight) CR
if looseNotTight:
   notTight = "_notTight"
else:
   notTight = ""

region['looseCR']['total'] =  [selection['loose']['cuts'], selection['regDef'] + notTight] 
region['looseCR']['prompt'] = [selection['loose']['cuts'], selection['regDef'] + notTight + '_prompt'] 
region['looseCR']['fake'] =   [selection['loose']['cuts'], selection['regDef'] + notTight + '_fake' ] 

# Yields 
if doYields:
   yields = {'SR':{}, 'looseCR':{}}

   for x in yields: 
      yields[x]['total'] =  Yields(samples, samplesList, cutInst = None, cuts = region[x]['total'],  cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
      yields[x]['prompt'] = Yields(samples, samplesList, cutInst = None, cuts = region[x]['prompt'], cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
      yields[x]['fake'] =   Yields(samples, samplesList, cutInst = None, cuts = region[x]['fake'],   cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)

   if save:
      if not os.path.isfile("%s/fakeYields_%s.txt"%(savedir, suffix)):
         outfile = open("%s/fakeYields_%s.txt"%(savedir, suffix), "w")
         outfile.write("Estimation of fakes in %s region for the %s channel \n"%(reg.title(), lepton))
         title = "Sample        Loose CR: Total            Loose CR: Prompt            Loose CR: Fakes              SR: Total               SR: Prompt                SR: Fakes\n"
         if looseNotTight: title = title.replace("Loose", "L!T") 
         outfile.write(title)

      yieldsList = samplesList[:]
      yieldsList.append('Total')

      with open("%s/fakeYields_%s.txt"%(savedir, suffix), "a") as outfile:
        for samp in yieldsList:
            outfile.write(samp.ljust(15) +\
            str(yields['looseCR']['total'].yieldDictFull[samp][selection['regDef'] + notTight].round(2)).ljust(25) +\
            str(yields['looseCR']['prompt'].yieldDictFull[samp][selection['regDef'] + notTight + '_prompt'].round(2)).ljust(25) +\
            str(yields['looseCR']['fake'].yieldDictFull[samp][selection['regDef'] + notTight + '_fake'].round(2)).ljust(25) +\
            str(yields['SR']['total'].yieldDictFull[samp][selection['regDef']].round(2)).ljust(25) +\
            str(yields['SR']['prompt'].yieldDictFull[samp][selection['regDef'] + '_prompt'].round(2)).ljust(25) +\
            str(yields['SR']['fake'].yieldDictFull[samp][selection['regDef'] + '_fake'].round(2)) + "\n")# .ljust(18) +\

if doPlots:
   # Plots
   bins = fakeBinning(lep, varBins = varBins)
   
   plotDict = {\
      "lepPt_loose":{'var':pt['loose'], "bins":bins['pt'], "decor":{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])},
      "lepPt_tight":{'var':pt['tight'], "bins":bins['pt'], "decor":{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])},
      "hybIso_loose":{ 'var':hybIso['loose'],  'bins':[10, 0, 25], 'decor':{'title':"Lepton hybIso Plot", 'x':"%s HI = I_{rel}*min(p_{T}, 25 GeV)"%lepton, 'y':"Events", 'log':[0,logy,0]}},
      "hybIso_tight":{ 'var':hybIso['tight'],  'bins':[10, 0, 25], 'decor':{'title':"Lepton hybIso Plot", 'x':"%s HI = I_{rel}*min(p_{T}, 25 GeV)"%lepton, 'y':"Events", 'log':[0,logy,0]}},
   }
    
   plotsDict = Plots(**plotDict)
   
   if logy: plotMin = 0.1
   else: plotMin = 0
   
   plotList = {}
   plotList['loose'] = ['lepPt_loose']
   plotList['tight'] = ['lepPt_tight']
   if not varBins: 
      plotList['loose'].append('hybIso_loose')
      plotList['tight'].append('hybIso_tight')
   
   fakePlots = {'SR':{}, 'looseCR':{}}
   
   plots =                           getPlots(samples, plotsDict, region['SR']['fake'],        samplesList, plotList = plotList['tight'])
   fakePlots['SR']['fakes'] =       drawPlots(samples, plotsDict, region['SR']['fake'],        samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
      
   plots =                           getPlots(samples, plotsDict, region['looseCR']['total'],  samplesList, plotList = plotList['loose'])
   fakePlots['looseCR']['total'] =  drawPlots(samples, plotsDict, region['looseCR']['total'],  samplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
   
   plots =                           getPlots(samples, plotsDict, region['looseCR']['fake'],   samplesList, plotList = plotList['loose'])
   fakePlots['looseCR']['fakes'] =  drawPlots(samples, plotsDict, region['looseCR']['fake'],   samplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
      
   plots =                           getPlots(samples, plotsDict, region['looseCR']['prompt'], samplesList, plotList = plotList['loose'])
   fakePlots['looseCR']['prompt'] = drawPlots(samples, plotsDict, region['looseCR']['prompt'], samplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
   
   if doControlPlots:
      plots =                        getPlots(samples, plotsDict, region['SR']['total'],       samplesList, plotList = plotList['tight'])# addOverFlowBin='both')
      fakePlots['SR']['total'] =    drawPlots(samples, plotsDict, region['SR']['total'],       samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
      
      plots =                        getPlots(samples, plotsDict, region['SR']['prompt'],      samplesList, plotList = plotList['tight'])
      fakePlots['SR']['prompt'] =   drawPlots(samples, plotsDict, region['SR']['prompt'],      samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
      
   # Legend
   leg = copy.deepcopy(fakePlots['looseCR'][fakePlots['looseCR'].keys()[0]]['legs'])
   latex = copy.deepcopy(fakePlots['looseCR'][fakePlots['looseCR'].keys()[0]]['latexText'])

   ### Estimation ###
   
   fakeHists = {}
   fakeHists['TLratio'] = TLratio['pt'].Clone() #NOTE: currently only using pT inclusive tight-to-loose ratio
   #TLratio['pt'] = ROOT.TH1D()
   #TLratio['2D'].ProjectionX().Copy(TLratio['pt'])#ProfileX()
   #TLratio['pt'].Sumw2()
   #TLratio['pt'].Scale(1./Nbins)
   
   # L(!T) CR   
   fakeHists['looseCR'] = {} # 2 options for loose CR

   # Fakes
   fakeHists['looseCR']['fakes'] = fakePlots['looseCR']['fakes']['stacks']['bkg']['lepPt_loose'].Clone()
  
   # Total and prompt 
   looseCR_tot =    copy.deepcopy(fakePlots['looseCR']['total'])#['stacks']['bkg']['lepPt_loose'].Clone()
   looseCR_prompt = copy.deepcopy(fakePlots['looseCR']['prompt'])#['stacks']['bkg']['lepPt_loose'].Clone()
   looseCR_tot_prompt = {}

   fakeHists['looseCR']['tot-prompt'] = ROOT.THStack('looseCR_tot-prompt', 'looseCR_tot-prompt') 
   for samp in looseCR_tot['hists']:
      
      looseCR_tot_prompt[samp] = looseCR_tot['hists'][samp]['lepPt_loose']
      setErrSqrtN(looseCR_tot_prompt[samp]) 
      looseCR_tot_prompt[samp].Add(looseCR_prompt['hists'][samp]['lepPt_loose'], -1)
      
      #common
      fakeHists['looseCR']['tot-prompt'].Add(looseCR_tot_prompt[samp]) 
      
   # Multiplying L(!T) CR fakes with transfer factor 
   if looseNotTight:
      unity1 = unity(fakeHists['TLratio'])
      unity2 = unity(fakeHists['TLratio'])
      unity3 = unity(fakeHists['TLratio'])
   
      unity1.Divide(fakeHists['TLratio'].Clone())   
      diff = unity1 - unity2
      unity3.Divide(diff) #NOTE: evaluates to (TLratio/1-TLratio) with correct errors
   
      TF = unity3
    
      ratioTitle1 = "#frac{#epsilon_{TL}}{(1 - #epsilon_{TL})}"
   else:
      TF = fakeHists['TLratio'].Clone() # TF = T-L ratio
      ratioTitle1 = "#epsilon_{TL}"
      
   #fakeHists['estimate'] = multiplyHists(TF, fakeHists['looseCR'].GetStack().Last().Clone())
   
   fakeHists['estimate'] = {} 
 
   for x in ['fakes', 'tot-prompt']: 
      fakeHists['estimate'][x] = TF*fakeHists['looseCR'][x].GetStack().Last().Clone() #NOTE: last stack in GetStack() array is the sum of all stacks
      fakeHists['estimate'][x].SetName("fakesEstimate_"+x)
   
   fakeHists['estimate']['fakes'].SetMarkerStyle(20)
   fakeHists['estimate']['fakes'].SetMarkerColor(1)
   fakeHists['estimate']['fakes'].SetMarkerSize(0.9)
   fakeHists['estimate']['fakes'].SetLineWidth(2)
   
   leg[-1].AddEntry(fakeHists['estimate']['fakes'], "Prediction", "LP")
   canvas = drawPlot(fakeHists['looseCR']['fakes'], legend = leg, decor = plotsDict['lepPt_loose']['decor'], latexText = latex, ratio = (fakeHists['estimate']['fakes'], fakeHists['looseCR']['fakes']), ratioLimits = [0,0.7], ratioTitle = ratioTitle1)
   fakeHists['estimate']['fakes'].Draw("same")
  
   # Closure
   
   fakeHists['SR'] = fakePlots['SR']['fakes']['stacks']['bkg']['lepPt_tight'].Clone()
   
   if closureDef == "ratio":
      ratioTitle2 = "#frac{Obs.}{Pred.}"
      ratioLimits2 = [0, 4] 
      unityLine = True
      closure = (fakeHists['SR'], fakeHists['estimate'])
   
   elif closureDef == "standard":
      ratioTitle2 = "#frac{Pred. - Obs.}{Pred.}"
      ratioLimits2 = [-2, 2] 
      unityLine = False
      
      closure = fakeHists['estimate']['fakes'].Clone() - fakeHists['SR'].GetStack().Last().Clone()
      estimate_zeroErr = fakeHists['estimate']['fakes'].Clone()
      setErrZero(estimate_zeroErr)
      closure.Divide(estimate_zeroErr)
   
   if fakeRateMeasurement == "MC": 
      ratioTitle2 = ratioTitle2.replace('Obs.', 'MC')
   
   canvas2 = drawPlot(fakeHists['SR'], legend = leg, decor = plotsDict['lepPt_tight']['decor'], latexText = latex, ratio = closure, ratioLimits = ratioLimits2, ratioTitle = ratioTitle2, unity = unityLine)
   fakeHists['estimate']['fakes'].Draw("same")
   
   fakeHists['closure'] = canvas2['ratio']

   if doYields:
   
      n = fakeHists['TLratio'].GetNbinsX()
   
      fakeHists['looseCR_hist'] = {} 
     
      numbers =  ['TLratio', 'looseCR', 'estimate', 'SR', 'closure']
 
      value =  {'TLratio':{}, 'looseCR':{'fakes':{}, 'tot-prompt':{}}, 'looseCR_hist':{'fakes':{}, 'tot-prompt':{}}, 'estimate':{'fakes':{}, 'tot-prompt':{}}, 'SR':{}, 'closure':{}}
      error =  {'TLratio':{}, 'looseCR':{'fakes':{}, 'tot-prompt':{}}, 'looseCR_hist':{'fakes':{}, 'tot-prompt':{}}, 'estimate':{'fakes':{}, 'tot-prompt':{}}, 'SR':{}, 'closure':{}}
      uFloat = {'TLratio':{}, 'looseCR':{'fakes':{}, 'tot-prompt':{}}, 'looseCR_hist':{'fakes':{}, 'tot-prompt':{}}, 'estimate':{'fakes':{}, 'tot-prompt':{}}, 'SR':{}, 'closure':{}}
   
      for i in range(n):
         a = int(fakeHists['TLratio'].GetBinLowEdge(i+1))
         w = int(fakeHists['TLratio'].GetBinWidth(i+1))
        
         for x in numbers:
            if 'fakes' in value[x].keys():
               for y in value[x]:
                  z = x
                  if type(fakeHists[x][y]) == ROOT.THStack: # Convert THStack into TH1
                     z += '_hist'
                     fakeHists[z][y] = fakeHists[x][y].GetStack().Last().Clone()
   
                  value[x][y][i] = fakeHists[z][y].GetBinContent(i+1)
                  error[x][y][i] = fakeHists[z][y].GetBinError(i+1)
                  uFloat[x][y][i] = u_float.u_float(value[x][y][i], error[x][y][i]) 
            else: 
               z = x
               if type(fakeHists[x]) == ROOT.THStack: # Convert THStack into TH1
                  z += '_hist'
                  fakeHists[z] = fakeHists[x].GetStack().Last().Clone()
   
               value[x][i] = fakeHists[z].GetBinContent(i+1)
               error[x][i] = fakeHists[z].GetBinError(i+1)
               uFloat[x][i] = u_float.u_float(value[x][i], error[x][i]) 
   
         if verbose:
            print makeLine()
            print "Fake rate estimation in bin %s %s-%s GeV"%(str(i), str(a), str(a+w)) 
            print makeLine()
            print "T-L Ratio:",           uFloat['TLratio'][i].round(3) 
            
            print "L(!T) CR:",            uFloat['looseCR'][i].round(3) 
            print "Estimate:",            uFloat['estimate']['fakes'][i].round(3) 
            print "Estimate (x-check):", (uFloat['TLratio'][i]*uFloat['looseCR']['fakes'][i]).round(3) 
            print "SR MC:",               uFloat['SR'][i].round(3)
            print "Closure:",             uFloat['closure'][i].round(3) 
            if uFloat['estimate']['fakes'][i].val:
               print "Closure (x-check):", (uFloat['SR'][i]/uFloat['estimate']['fakes'][i]).round(3) 
            
            print makeLine()
            print "L(!T) CR (prompt sub.)",  uFloat['looseCR']['tot-prompt'][i].round(3) 
            print "Estimate (prompt sub.):", uFloat['estimate']['tot-prompt'][i].round(3) 
            print makeLine()
   
         if save:
            if not os.path.isfile("%s/fakesEstimation_%s.txt"%(savedir, suffix)):
               outfile = open("%s/fakesEstimation_%s.txt"%(savedir, suffix), "w")
               outfile.write("Estimation of fakes in %s region for the %s channel \n"%(reg.title(), lepton))
               title = "Bin (GeV)         T-L Ratio               Loose CR (MC)             Estimate (MC)              SR: Fakes (MC)             MC Closure (%s)     |     Loose CR (Prompt Sub.)             Estimate (Prompt Sub.)\n"%(closureDef.title())
               if looseNotTight: title = title.replace("Loose", "L!T") 
               outfile.write(title)
   
            with open("%s/fakesEstimation_%s.txt"%(savedir, suffix), "a") as outfile:
               outfile.write("{}-{}".format(str(a), str(a+w)).ljust(15) +\
               str(uFloat['TLratio'][i].round(3)).ljust(25) +\
               str(uFloat['looseCR']['fakes'][i].round(3)).ljust(25) +\
               str(uFloat['estimate']['fakes'][i].round(3)).ljust(27) +\
               str(uFloat['SR'][i].round(3)).ljust(30) +\
               str(uFloat['closure'][i].round(3)).ljust(30) +\
               str(uFloat['looseCR']['tot-prompt'][i].round(3)).ljust(30) +\
               str(uFloat['estimate']['tot-prompt'][i].round(3))  + "\n")
  
            #Pickle results 
            pickleFile = open("%s/fakesEstimation_%s.pkl"%(savedir,suffix), "w")
            pickle.dump(uFloat, pickleFile)
            pickleFile.close()
 
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      if doControlPlots:
         for canv in fakePlots['SR']['total']['canvs']:
            fakePlots['SR']['total']['canvs'][canv][0].SaveAs("%s/SR_%s_%s.png"%(savedir, suffix, canv))
            fakePlots['SR']['total']['canvs'][canv][0].SaveAs("%s/root/SR_%s_%s.root"%(savedir, suffix, canv))
            fakePlots['SR']['total']['canvs'][canv][0].SaveAs("%s/pdf/SR_%s_%s.pdf"%(savedir, suffix, canv))
         for canv in fakePlots['SR']['fakes']['canvs']:
            fakePlots['SR']['fakes']['canvs'][canv][0].SaveAs("%s/SR_%s_%s_fake.png"%(savedir, suffix, canv))
            fakePlots['SR']['fakes']['canvs'][canv][0].SaveAs("%s/root/SR_%s_%s_fake.root"%(savedir, suffix, canv))
            fakePlots['SR']['fakes']['canvs'][canv][0].SaveAs("%s/pdf/SR_%s_%s_fake.pdf"%(savedir, suffix, canv))
         for canv in fakePlots['SR']['prompt']['canvs']:
            fakePlots['SR']['prompt']['canvs'][canv][0].SaveAs("%s/SR_%s_%s_prompt.png"%(savedir, suffix, canv))
            fakePlots['SR']['prompt']['canvs'][canv][0].SaveAs("%s/root/SR_%s_%s_prompt.root"%(savedir, suffix, canv))
            fakePlots['SR']['prompt']['canvs'][canv][0].SaveAs("%s/pdf/SR_%s_%s_prompt.pdf"%(savedir, suffix, canv))
         
         for canv in fakePlots['looseCR']['total']['canvs']:
            fakePlots['looseCR']['total']['canvs'][canv][0].SaveAs("%s/looseCR_%s_%s.png"%(savedir, suffix, canv))
            fakePlots['looseCR']['total']['canvs'][canv][0].SaveAs("%s/root/looseCR_%s_%s.root"%(savedir, suffix, canv))
            fakePlots['looseCR']['total']['canvs'][canv][0].SaveAs("%s/pdf/looseCR_%s_%s.pdf"%(savedir, suffix, canv))
         for canv in fakePlots['looseCR']['fakes']['canvs']:
            fakePlots['looseCR']['fakes']['canvs'][canv][0].SaveAs("%s/looseCR_%s_%s_fake.png"%(savedir, suffix, canv))
            fakePlots['looseCR']['fakes']['canvs'][canv][0].SaveAs("%s/root/looseCR_%s_%s_fake.root"%(savedir, suffix, canv))
            fakePlots['looseCR']['fakes']['canvs'][canv][0].SaveAs("%s/pdf/looseCR_%s_%s_fake.pdf"%(savedir, suffix, canv))
         for canv in fakePlots['looseCR']['prompt']['canvs']:
            fakePlots['looseCR']['prompt']['canvs'][canv][0].SaveAs("%s/looseCR_%s_%s_prompt.png"%(savedir, suffix, canv))
            fakePlots['looseCR']['prompt']['canvs'][canv][0].SaveAs("%s/root/looseCR_%s_%s_prompt.root"%(savedir, suffix, canv))
            fakePlots['looseCR']['prompt']['canvs'][canv][0].SaveAs("%s/pdf/looseCR_%s_%s_prompt.pdf"%(savedir, suffix, canv))
      
      canvas['canvs'][0].SaveAs("%s/fakesEstimate_%s.png"%(savedir, suffix))
      canvas['canvs'][0].SaveAs("%s/root/fakesEstimate_%s.root"%(savedir, suffix))
      canvas['canvs'][0].SaveAs("%s/pdf/fakesEstimate_%s.pdf"%(savedir, suffix))
   
      canvas2['canvs'][0].SaveAs("%s/closureMC_%s.png"%(savedir, suffix))
      canvas2['canvs'][0].SaveAs("%s/root/closureMC_%s.root"%(savedir, suffix))
      canvas2['canvs'][0].SaveAs("%s/pdf/closureMC_%s.pdf"%(savedir, suffix))
