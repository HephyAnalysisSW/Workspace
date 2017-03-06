# fakesEstimation.py
# Application of fake rate to estimate fake background contribution 
# Mateusz Zarucki 2017

import ROOT
import os, sys
import argparse
import copy
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
parser.add_argument("--subtractPrompt", dest="subtractPrompt", help="Subtract prompt", type=int, default=1)
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
subtractPrompt = args.subtractPrompt
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
   binDir = "/FR_" + fakeRateMeasurement
   
   if not varBins: binDir += "/fixedBins"
   else:           binDir += "/varBins"
    
   # Root file with fake rate
   fakeRateDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate"
   
   fakeRateDir += "/" + measurementRegion
   
   fakeRateDir += binDir
   
   fakeRateFile = "FakeRate_TightToLoose_lepPt_%s_%s.root"%(lep, fakeRateMeasurement)
   
   if verbose:
      print makeLine()
      print "Using fake rate from ", fakeRateDir + "/" + fakeRateFile
      print makeLine()
   
   f1 = ROOT.TFile(fakeRateDir + "/" + fakeRateFile)
   
   fakeRate = {}
   
   fakeRate['pt'] = f1.Get("c1").GetPrimitive("c1_2").GetPrimitive("ratio_pt_%s"%fakeRateMeasurement)
   fakeRate['eta'] = f1.Get("c1").GetPrimitive("c1_2").GetPrimitive("ratio_eta_%s"%fakeRateMeasurement)

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
   
   if subtractPrompt: savedir += "/promptSubtraction"
   else:              savedir += "/noPromptSubtraction"
   
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
   
   if logy: plotMin = 1
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
   
   plots =                           getPlots(samples, plotsDict, region['looseCR']['fake'],   samplesList, plotList = plotList['loose'])
   fakePlots['looseCR']['fakes'] =  drawPlots(samples, plotsDict, region['looseCR']['fake'],   samplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
   
   if subtractPrompt or doControlPlots:
      plots =                           getPlots(samples, plotsDict, region['SR']['total'],       samplesList, plotList = plotList['tight'])# addOverFlowBin='both')
      fakePlots['SR']['total'] =       drawPlots(samples, plotsDict, region['SR']['total'],       samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
      
      plots =                           getPlots(samples, plotsDict, region['looseCR']['total'],  samplesList, plotList = plotList['loose'])
      fakePlots['looseCR']['total'] =  drawPlots(samples, plotsDict, region['looseCR']['total'],  samplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
   
      plots =                           getPlots(samples, plotsDict, region['SR']['prompt'],      samplesList, plotList = plotList['tight'])
      fakePlots['SR']['prompt'] =      drawPlots(samples, plotsDict, region['SR']['prompt'],      samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
      
      plots =                           getPlots(samples, plotsDict, region['looseCR']['prompt'], samplesList, plotList = plotList['loose'])
      fakePlots['looseCR']['prompt'] = drawPlots(samples, plotsDict, region['looseCR']['prompt'], samplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
   
   # Estimation
   
   fakeHists = {}
   fakeHists['fakeRate'] = fakeRate['pt'] #NOTE: currently only using pT inclusive tight-to-loose ratio
   #fakeRate['pt'] = ROOT.TH1D()
   #fakeRate['2D'].ProjectionX().Copy(fakeRate['pt'])#ProfileX()
   #fakeRate['pt'].Sumw2()
   #fakeRate['pt'].Scale(1./Nbins)
   
   # Legend
   leg = copy.deepcopy(fakePlots['looseCR'][fakePlots['looseCR'].keys()[0]]['legs'])
   latex = copy.deepcopy(fakePlots['looseCR'][fakePlots['looseCR'].keys()[0]]['latexText'])
   
   if subtractPrompt:
      fakeHists['looseCR_tot'] =    copy.deepcopy(fakePlots['looseCR']['total'])#['stacks']['bkg']['lepPt_loose'].Clone()
      fakeHists['looseCR_prompt'] = copy.deepcopy(fakePlots['looseCR']['prompt'])#['stacks']['bkg']['lepPt_loose'].Clone()
      fakeHists['looseCR_tot-prompt'] = {}
      fakeHists['looseCR'] = ROOT.THStack('looseCR', 'looseCR') 
      for samp in fakeHists['looseCR_tot']['hists']:
         fakeHists['looseCR_tot-prompt'][samp] = fakeHists['looseCR_tot']['hists'][samp]['lepPt_loose'] - fakeHists['looseCR_prompt']['hists'][samp]['lepPt_loose']
         fakeHists['looseCR'].Add(fakeHists['looseCR_tot-prompt'][samp]) 
   else:   
      fakeHists['looseCR'] = fakePlots['looseCR']['fakes']['stacks']['bkg']['lepPt_loose'].Clone()
   
   # Multiplying L(!T) CR fakes with transfer factor 
   if looseNotTight:
      unity1 = unity(fakeRate['pt'])
      unity2 = unity(fakeRate['pt'])
      unity3 = unity(fakeRate['pt'])
   
      unity1.Divide(fakeHists['fakeRate'].Clone())   
      diff = unity1 - unity2
      unity3.Divide(diff) #NOTE: evaluates to (TL/1-TL) with correct errors
   
      TF = unity3
    
      ratioTitle1 = "#frac{#epsilon_{TL}}{(1 - #epsilon_{TL})}"
   else:
      TF = fakeHists['fakeRate'].Clone() # TF = T-L ratio
      ratioTitle1 = "#epsilon_{TL}"
      
   #fakeHists['estimate'] = multiplyHists(TF, fakeHists['looseCR'].GetStack().Last().Clone())
   fakeHists['estimate'] = TF*fakeHists['looseCR'].GetStack().Last().Clone() #NOTE: last stack in GetStack() array is the sum of all stacks
      
   fakeHists['estimate'].SetName("fakesEstimate")
   fakeHists['estimate'].SetMarkerStyle(20)
   fakeHists['estimate'].SetMarkerColor(1)
   fakeHists['estimate'].SetMarkerSize(0.9)
   fakeHists['estimate'].SetLineWidth(2)
   
   leg[-1].AddEntry(fakeHists['estimate'], "Prediction", "LP")
   canvas = drawPlot(fakeHists['looseCR'], legend = leg, decor = plotsDict['lepPt_loose']['decor'], latexText = latex, ratio = (fakeHists['estimate'], fakeHists['looseCR']), ratioLimits = [0,0.7], ratioTitle = ratioTitle1)
   fakeHists['estimate'].Draw("same")
   
   # Closure
   
   #if subtractPrompt: #NOTE: Do not subtract prompt from SR MC. Just take the fakes via mcMatch.
   #   fakeHists['SR_tot'] =    copy.deepcopy(fakePlots['SR']['total'])#['stacks']['bkg']['lepPt_loose'].Clone()
   #   fakeHists['SR_prompt'] = copy.deepcopy(fakePlots['SR']['prompt'])#['stacks']['bkg']['lepPt_loose'].Clone()
   #   fakeHists['SR_tot-prompt'] = {}
   #   fakeHists['SR'] = ROOT.THStack('SR', 'SR')
   #   for samp in fakeHists['looseCR_tot']['hists']:
   #      fakeHists['SR_tot-prompt'][samp] = fakeHists['SR_tot']['hists'][samp]['lepPt_tight'] - fakeHists['SR_prompt']['hists'][samp]['lepPt_tight']
   #      fakeHists['SR'].Add(fakeHists['SR_tot-prompt'][samp])
   #else:
   fakeHists['SR'] = fakePlots['SR']['fakes']['stacks']['bkg']['lepPt_tight'].Clone()
   
   ratioTitle2 = "#frac{Obs.}{Pred.}"
   
   if closureDef == "ratio":
      ratioLimits2 = [0, 4] 
      unityLine = True
      closure = (fakeHists['SR'], fakeHists['estimate'])
   
   elif closureDef == "standard":
      ratioTitle2 = "1 - " + ratioTitle2
      ratioLimits2 = [-2, 2] 
      unityLine = False
      
      unity4 = unity(fakeRate['pt'])
      closure = fakeHists['SR'].GetStack().Last().Clone()
      closure.Divide(fakeHists['estimate'])
      closure = unity4 - closure
   
   if fakeRateMeasurement == "MC": 
      ratioTitle2 = ratioTitle2.replace('Obs.', 'MC')
   
   canvas2 = drawPlot(fakeHists['SR'], legend = leg, decor = plotsDict['lepPt_tight']['decor'], latexText = latex, ratio = closure, ratioLimits = ratioLimits2, ratioTitle = ratioTitle2, unity = unityLine)
   fakeHists['estimate'].Draw("same")
   
   fakeHists['closure'] = canvas2['ratio']
   
   if doYields:
     
      n = fakeRate['pt'].GetNbinsX()
   
      value =  {'fakeRate':{}, 'looseCR':{}, 'estimate':{}, 'SR':{}, 'closure':{}}
      error =  {'fakeRate':{}, 'looseCR':{}, 'estimate':{}, 'SR':{}, 'closure':{}}
      uFloat = {'fakeRate':{}, 'looseCR':{}, 'estimate':{}, 'SR':{}, 'closure':{}}
   
      for i in range(n):
         a = int(fakeRate['pt'].GetBinLowEdge(i+1))
         w = int(fakeRate['pt'].GetBinWidth(i+1))
        
         for x in value:
            y = x
            # Convert THStack into TH1
            if type(fakeHists[x]) == ROOT.THStack:
               y = x + '_hist'
               fakeHists[y] = fakeHists[x].GetStack().Last().Clone()
   
            value[x][i] = fakeHists[y].GetBinContent(i+1)
            error[x][i] = fakeHists[y].GetBinError(i+1)
            uFloat[x][i] = u_float.u_float(value[x][i], error[x][i]) 
   
         if verbose:
            print makeLine()
            print "Fake rate estimation in bin %s %s-%s GeV"%(str(i), str(a), str(a+w)) 
            print makeLine()
            print "T-L Ratio:",          uFloat['fakeRate'][i].round(3) 
            print "L(!T) CR:",           uFloat['looseCR'][i].round(3) 
            print "Estimate:",           uFloat['estimate'][i].round(3) 
            print "Estimate (x-check):", (uFloat['fakeRate'][i]*uFloat['looseCR'][i]).round(3) 
            print "SR MC:",              uFloat['SR'][i].round(3)
            print "Closure:",            uFloat['closure'][i].round(3) 
            if uFloat['estimate'][i].val:
               print "Closure (x-check):", (uFloat['SR'][i]/uFloat['estimate'][i]).round(3) 
            print makeLine()
   
         if save:
            if not os.path.isfile("%s/fakesEstimation_%s.txt"%(savedir, suffix)):
               outfile = open("%s/fakesEstimation_%s.txt"%(savedir, suffix), "w")
               outfile.write("Estimation of fakes in %s region for the %s channel \n"%(reg.title(), lepton))
               title = "Bin (GeV)         T-L Ratio               Loose CR             Estimate (Pred.)              SR: Fakes (MC)             Closure (%s)\n"%(closureDef.title())
               if looseNotTight: title = title.replace("Loose", "L!T") 
               outfile.write(title)
   
            with open("%s/fakesEstimation_%s.txt"%(savedir, suffix), "a") as outfile:
               outfile.write("{}-{}".format(str(a), str(a+w)).ljust(15) +\
               str(uFloat['fakeRate'][i].round(3)).ljust(25) +\
               str(uFloat['looseCR'][i].round(3)).ljust(25) +\
               str(uFloat['estimate'][i].round(3)).ljust(27) +\
               str(uFloat['SR'][i].round(3)).ljust(30) +\
               str(uFloat['closure'][i].round(3)) + "\n")
   
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
