# PUsys.py
# Mateusz Zarucki 2016

import ROOT
import os, sys
import math
import argparse
import pickle
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, makeSimpleLatexTable, makeDir, setup_style
from Workspace.DegenerateStopAnalysis.tools.degCuts2 import Cuts, CutsWeights
from Workspace.DegenerateStopAnalysis.cmgPostProcessing import cmgObjectSelection
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions, triggers, filters
from Workspace.HEPHYPythonTools import u_float
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
#setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--sample", dest = "sample", help = "Sample", type = str, default = "t2tt300_270")
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
sample = args.sample
save = args.save
verbose = args.verbose

##Samples
cmgPP = cmgTuplesPostProcessed()

#samplesList = [sample]
samplesList = ["t2tt300_270"]#, "t2tt300_220", "t2tt300_290", "t2bw300_220", "t2bw300_270", "t2bw300_290"]

samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = True, useHT = True, getData = 0, def_weights = [])
#
#if 'all' in sample:
#   allFastSim = ROOT.TChain("Events", "Events")
#   for s in samples.sigList():
#      if 't2tt' in s and not 't2ttold' in s:
#         if 'global' in scriptTag and s not in ['t2tt275_205', 't2tt350_330', 't2tt400_350']: continue
#         allFastSim.Add(samples[s].tree)
#
#if verbose:
#   print makeLine()
#   print "Using samples:"
#   newLine()
#   for s in samplesList:
#      if s: print samples[s].name,":",s
#      else:
#         print "!!! Sample " + sample + " unavailable."
#         sys.exit(0)

saveResults = 1

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/PU"%tag

   if saveResults:
      resultsDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/PU"
      makeDir(resultsDir)

   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

pkl = "/afs/hephy.at/user/n/nrad/public/share/PUHistsRatios.pkl"
ratiosPkl = pickle.load(open(pkl, "r"))

effs = {'diff':{}}
effs['pu_lt_20'] = ratiosPkl['hists']['lt20']
effs['pu_gt_20'] = ratiosPkl['hists']['gt20']
ratios = ratiosPkl['ratios']

deltaMhists = {'T2tt':{'lt20':{10:[], 20:[], 30:[], 40:[], 50:[], 60:[], 70:[], 80:[]},
                       'gt20':{10:[], 20:[], 30:[], 40:[], 50:[], 60:[], 70:[], 80:[]}},
               'T2bW':{'lt20':{10:[], 20:[], 30:[], 40:[], 50:[], 60:[], 70:[], 80:[]},
                       'gt20':{10:[], 20:[], 30:[], 40:[], 50:[], 60:[], 70:[], 80:[]}}}

deltaMdict = {'T2tt':{'lt20':{}, 'gt20':{}}, 'T2bW':{'lt20':{}, 'gt20':{}}}

resultsDict = {'T2tt':{}, 'T2bW':{}, 'avg':{}}

for x in ratiosPkl['hists']:
   for y in ratiosPkl['hists'][x]:
      deltaMhists[y.split('-')[0]][x][int(y.split('-')[1])-int(y.split('-')[2])].append(ratiosPkl['hists'][x][y])

for T2 in ['T2tt', 'T2bW']:
   for x in ['lt20', 'gt20']:
      for y in deltaMhists[T2][x]:
         deltaMdict[T2][x][y] = effs['pu_gt_20']['%s-300-270'%T2].Clone()
         deltaMdict[T2][x][y].SetName("%s_%s_deltaM%s"%(T2,x,y))

for T2 in ['T2tt', 'T2bW']:
   for x in ['lt20', 'gt20']:
      for y in deltaMhists[T2][x]:
         for hist in deltaMhists[T2][x][y]:
            deltaMdict[T2][x][y].Add(hist)

###

rDists = {'all':  ROOT.TH1F("rDist_all",  "rDist_all",  100, 0, 2),
          'T2tt': ROOT.TH1F("rDist_T2tt", "rDist_T2tt", 100, 0, 2),
          'T2bW': ROOT.TH1F("rDist_T2bW", "rDist_T2bW", 100, 0, 2),
          'all_avg':  ROOT.TH1F("rDist_all_avg",  "rDist_all_avg",  50, 0, 2),
          'T2tt_avg': ROOT.TH1F("rDist_T2tt_avg", "rDist_T2tt_avg", 50, 0, 2),
          'T2bW_avg': ROOT.TH1F("rDist_T2bW_avg", "rDist_T2bW_avg", 50, 0, 2)}

for sig in ratios:
   n = ratios[sig].GetNbinsX()

   for i in range(n):
      i += 1
      
      rDists['all'].Fill(ratios[sig].GetBinContent(i))
      if 'T2tt' in sig:
         rDists['T2tt'].Fill(ratios[sig].GetBinContent(i))
      elif 'T2bW' in sig:
         rDists['T2bW'].Fill(ratios[sig].GetBinContent(i))

canvs = {}

###

doPlots = 0

if doPlots:
   plotDict = {
      "nTrueInt" : {'var':"nTrueInt", "bins":[40,0,40], "nMinus1":"", "decor":{"title":"nTrueInt", "x":"nTrueInt", "y":"Events", 'log':[0,0,0]}},
      }
   plotsDict = Plots(**plotDict)
   
   cuts_weights = CutsWeights(samples, cutWeightOptions)
   
   presel = 0
   
   if presel:
      cut = 'presel'
   else:
      cut = 'none'
   
   cuts_weights.cuts.addCut(cut, 'pu_gt_20')
   cuts_weights.cuts.addCut(cut, 'pu_lt_20')
   
   doExtraPlots = 1
   if doExtraPlots:
      plots_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, cut], samplesList, plotList = ['nTrueInt'], addOverFlowBin='both')
      plots =  drawPlots(samples, plotsDict, [cuts_weights.cuts, cut], samplesList, plotList = ['nTrueInt'], plotLimits = [1, 100], fom = None, fomLimits = [0,8], plotMin = 1, normalize = True, save = False)
   
   plots1_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, cut + '_plus_pu_lt_20'], samplesList, plotList = ['nTrueInt'], addOverFlowBin='both')
   plots1 =  drawPlots(samples, plotsDict, [cuts_weights.cuts, cut + '_plus_pu_lt_20'], samplesList, plotList = ['nTrueInt'], plotLimits = [1, 100], fom = None, fomLimits = [0,8], plotMin = 1, normalize = True, save = False)
   
   plots2_ =  getPlots(samples, plotsDict, [cuts_weights.cuts, cut + '_plus_pu_gt_20'], samplesList, plotList = ['nTrueInt'], addOverFlowBin='both')
   plots2 =  drawPlots(samples, plotsDict, [cuts_weights.cuts, cut + '_plus_pu_gt_20'], samplesList, plotList = ['nTrueInt'], plotLimits = [1, 100], fom = None, fomLimits = [0,8], plotMin = 1, normalize = True, save = False)
   
   hists = {'puIncl':{}, 'pu_lt_20':{}, 'pu_gt_20':{}}
   
   for samp in samplesList:
      if doExtraPlots:
         hists['puIncl'][samp] =   plots['hists'][samp]['nTrueInt']
      hists['pu_lt_20'][samp] = plots1['hists'][samp]['nTrueInt']
      hists['pu_gt_20'][samp] = plots2['hists'][samp]['nTrueInt']
   
   for pu in ['puIncl', 'pu_lt_20', 'pu_gt_20']:
      canvs[pu] = ROOT.TCanvas("c_"+pu, "Canvas "+pu, 1500, 1500)
   
      for i, samp in enumerate(samplesList):
         hists[pu][samp].SetLineColor(2+i)
         hists[pu][samp].Draw('histsame') 
   
   N1 = hists['pu_lt_20']['t2tt300_270'].GetMean()
   N2 = hists['pu_gt_20']['t2tt300_270'].GetMean()
   
   print "N1:", N1
   print "N2:", N2

N1 = 14.7442697019
N2 = 24.7434792224

###

plotEffs = 1
denominator = "r" #N2-N1" #e1_N2-N1" #"e1" # "diff" #"N2-N1"

if plotEffs:
   legs = {}
   #massPoints = {}
   #massPoints['low'] =  ['300-220', '300-270', '300-290']
   #massPoints['high'] = ['800-720', '800-770', '800-790']
   
   #ROOT.gStyle.SetOptStat(0)
      
   canvs['c_combined_'+denominator] = ROOT.TCanvas("c_combined", "Canvas c_combined", 1500, 1500)
   legs['l_combined'] = makeLegend2()
   
   for col,T2 in enumerate(['T2tt', 'T2bW']):
 
      effs['diff'][T2] = effs['pu_gt_20']['%s-300-270'%T2].Clone()
      effs['diff'][T2].Reset()
      
      ###effs['pu_gt_20'][T2] = effs['pu_gt_20']['%s-300-270'%T2].Clone()
      ###effs['pu_lt_20'][T2] = effs['pu_lt_20']['%s-300-270'%T2].Clone()
      ###effs['pu_gt_20'][T2].Reset()
      ###effs['pu_lt_20'][T2].Reset()
      
      counter = 0
      for dm in deltaMdict[T2]['gt20']:
         counter += 1
         #print counter, T2, dm
      
         effs['diff'][dm] = deltaMdict[T2]['gt20'][dm].Clone() - deltaMdict[T2]['lt20'][dm].Clone()
      
         if denominator == "e1":
            den = deltaMdict[T2]['lt20'][dm].Clone()
            setErrZero(den)
            effs['diff'][dm].Divide(den)
         elif denominator == "N2-N1":
            effs['diff'][dm].Scale(1./(N2-N1)) 
         elif denominator == "e1_N2-N1":
            den = effs['pu_lt_20'][dm].Clone()
            setErrZero(den)
            effs['diff'][dm].Divide(den)
            effs['diff'][dm].Scale(1./(N2-N1)) 
         elif denominator == "r": #NOTE: Not denominator but e2-e1/e1 + 1 = r
            unity1 = unity(effs['pu_gt_20']['%s-300-270'%T2].Clone())
            den = deltaMdict[T2]['lt20'][dm].Clone()
            setErrZero(den)
            effs['diff'][dm].Divide(den)
            
            N = effs['diff'][dm].GetNbinsX()
            
            for i in range(N):
               i += 1
               if effs['diff'][dm].GetBinContent(i):
                  effs['diff'][dm].SetBinContent(i, effs['diff'][dm].GetBinContent(i)+1.)

         elif denominator == "r2": #NOTE: Not denominator but ratio 
            effs['diff'][dm] = ratios[dm] 
         
         effs['diff'][T2].Add(effs['diff'][dm])
   
      ##NOTE: average over all signal points 
      ##counter = 0
      ##for massPoint in effs['pu_gt_20']: #'T2tt-300-270', 'T2tt-300-220', 'T2tt-300-290']: ##['T2tt-300-270', 'T2tt-300-220']: 
      ##   if T2+'-' not in massPoint: continue
      ##   counter += 1
      ##   #print counter, T2, massPoint
      ##
      ##   effs['diff'][massPoint] = effs['pu_gt_20'][massPoint].Clone() - effs['pu_lt_20'][massPoint].Clone()
      ##   ###effs['pu_lt_20'][T2].Add(effs['pu_lt_20'][massPoint])
      ##   ###effs['pu_gt_20'][T2].Add(effs['pu_gt_20'][massPoint])
      ##
      ##   if denominator == "e1":
      ##      den = effs['pu_lt_20'][massPoint].Clone()
      ##      setErrZero(den)
      ##      effs['diff'][massPoint].Divide(den)
      ##   elif denominator == "N2-N1":
      ##      effs['diff'][massPoint].Scale(1./(N2-N1)) 
      ##   elif denominator == "e1_N2-N1":
      ##      den = effs['pu_lt_20'][massPoint].Clone()
      ##      setErrZero(den)
      ##      effs['diff'][massPoint].Divide(den)
      ##      effs['diff'][massPoint].Scale(1./(N2-N1)) 
      ##   elif denominator == "r": #NOTE: Not denominator but e2-e1/e1 + 1 = r
      ##      unity1 = unity(effs['pu_gt_20']['%s-300-270'%T2].Clone())
      ##      den = effs['pu_lt_20'][massPoint].Clone()
      ##      setErrZero(den)
      ##      effs['diff'][massPoint].Divide(den)
      ##      
      ##      N = effs['diff'][massPoint].GetNbinsX()
      ##      
      ##      for i in range(N):
      ##         i += 1
      ##         if effs['diff'][massPoint].GetBinContent(i):
      ##            effs['diff'][massPoint].SetBinContent(i, effs['diff'][massPoint].GetBinContent(i)+1.)

      ##   elif denominator == "r2": #NOTE: Not denominator but ratio 
      ##      effs['diff'][massPoint] = ratios[massPoint] 
      ##   
      ##   effs['diff'][T2].Add(effs['diff'][massPoint])
            
      ###effs['diff'][T2] = effs['pu_gt_20'][T2].Clone() - effs['pu_lt_20'][T2].Clone()
            
      ###if denominator == "e1":
      ###   den = effs['pu_lt_20'][T2].Clone()
      ###   setErrZero(den)
      ###   effs['diff'][T2].Divide(den)
      ###elif denominator == "N2-N1":
      ###   effs['diff'][T2].Scale(1./(N2-N1)) 
            
      #effs['pu_lt_20'][T2].Scale(1./counter)
      #effs['pu_gt_20'][T2].Scale(1./counter)
      effs['diff'][T2].Scale(1./counter)

      #effs['diff']['%s-%s'%(T2,mp)] = effs['pu_gt_20']['%s-%s'%(T2,mp)].Clone() - effs['pu_lt_20']['%s-%s'%(T2,mp)].Clone()
      #den = effs['pu_lt_20']['%s-%s'%(T2,mp)].Clone()
      #setErrZero(den)
      #effs['diff']['%s-%s'%(T2,mp)].Divide(den)
      diffName = "%s-diff"%T2
      if denominator != "diff":
         diffName += "_" + denominator

      effs['diff'][T2].SetName(diffName)
      effs['diff'][T2].SetLineColor(2+col)
      effs['diff'][T2].Draw("same")

      if denominator == "e1":
         ymax = 0.5
         #ymax = 1.5
         ymin = -0.2
      elif "r" in denominator:
         ymax = 1.5
         #ymax = 2.5
         ymin = 0.8
      elif denominator == "diff":
         ymax = 0.02
         ymin = -0.02
         #ymax = 0.001
         #ymin = -0.001
      elif denominator == "N2-N1":
         ymax = 0.002
         ymin = -0.002
         #ymax = 0.0001
         #ymin = -0.0001
      else:
         ymax = 0.2
         ymin = -0.05

      effs['diff'][T2].SetMinimum(ymin) #-0.2
      effs['diff'][T2].SetMaximum(ymax) #0.3
      
      #effs['pu_lt_20'][T2].SetName("%s-lt20"%T2)
      #effs['pu_gt_20'][T2].SetName("%s-gt20"%T2)
      #effs['pu_lt_20'][T2].SetLineColor(4+col)
      #effs['pu_gt_20'][T2].SetLineColor(6+col)
      #effs['pu_lt_20'][T2].Draw("same")
      #effs['pu_gt_20'][T2].Draw("same")

      #ratios['%s-300-270'%T2].Draw("same")
      
      legs['l_combined'].AddEntry(diffName, diffName, "L")
      #legs['l_combined'].AddEntry("%s-gt20"%T2, "%s-gt20"%T2, "L")
      #legs['l_combined'].AddEntry("%s-lt20"%T2, "%s-lt20"%T2, "L")
     
   legs['l_combined'].Draw()
   alignLegend(legs['l_combined'], y1=0.65, y2=0.85) 

if "r" in denominator:
   for T2 in ['T2tt', 'T2bW']:
      N = effs['diff'][T2].GetNbinsX()
      
      for i in range(N):
         i += 1
         rDists['all_avg'].Fill(effs['diff'][T2].GetBinContent(i))
         rDists[T2+'_avg'].Fill(effs['diff'][T2].GetBinContent(i))

      canvs['dist_avg'] = ROOT.TCanvas("c1", "Canvas 1", 1500, 1500)
      
      rDists['all_avg'].SetLineColor(1)
      rDists['T2tt_avg'].SetLineColor(2)
      rDists['T2bW_avg'].SetLineColor(3)

      rDists['all_avg'].SetMaximum(35)

      rDists['all_avg'].Draw("histsame")
      rDists['T2tt_avg'].Draw("histsame")
      rDists['T2bW_avg'].Draw("histsame")

      #alignStats(rDists['all_avg'])
      
      l1 = makeLegend2(y1=0.65, y2=0.85)
      l1.AddEntry("rDist_all_avg", "All", "L")
      l1.AddEntry("rDist_T2tt_avg", "T2tt", "L")
      l1.AddEntry("rDist_T2bW_avg", "T2bW", "L")
      l1.Draw()
   
if saveResults and ("r" in denominator or "e1" in denominator):
   for T2 in ['T2tt', 'T2bW']:
      N = effs['diff'][T2].GetNbinsX()
      
      for i in range(N):
         i += 1
         SR = effs['diff'][T2].GetXaxis().GetBinLabel(i)
         resultsDict[T2][SR] = effs['diff'][T2].GetBinContent(i)
      
   for i in range(N):
      i += 1
      SR = effs['diff']['T2tt'].GetXaxis().GetBinLabel(i)
      resultsDict['avg'][SR] = 0.5*(resultsDict['T2tt'][SR] + resultsDict['T2bW'][SR])
   
suffix = "_" + denominator

#Pickle results 
if saveResults:
   pickleFile = open("%s/PUsys%s.pkl"%(resultsDir,suffix), "w")
   pickle.dump(resultsDict, pickleFile)
   pickleFile.close()

#plotRatios = 0
#if plotRatios:
#   legs = {}
#   massPoints = {}
#   massPoints['low'] =  ['300-220', '300-270', '300-290']
#   massPoints['high'] = ['800-720', '800-770', '800-790']
#   
#   ROOT.gStyle.SetOptStat(0)
#   
#   for T2 in ['T2tt', 'T2bW']:
#      for mStop in ['low', 'high']:
#         canvs['c_%s_%s'%(T2,mStop)] = ROOT.TCanvas('c_%s_%s'%(T2,mStop), "Canvas c_%s_%s"%(T2,mStop), 1500, 1500)
#         legs['c_%s_%s'%(T2,mStop)] = makeLegend2()
#   
#         for i, mp in enumerate(massPoints[mStop]):
#            ratios['%s-%s'%(T2,mp)].SetLineColor(2+i)
#            ratios['%s-%s'%(T2,mp)].Draw("same")
#            ratios['%s-%s'%(T2,mp)].SetMinimum(0)
#            ratios['%s-%s'%(T2,mp)].SetMaximum(5)
#            #alignStats(ratios['%s-%s'%(T2,mp)])    
#            legs['c_%s_%s'%(T2,mStop)].AddEntry("gt20_%s-%s"%(T2,mp), "%s-%s"%(T2,mp), "L")
#         
#         legs['c_%s_%s'%(T2,mStop)].Draw()

doDist = 0
if doDist:
   canvs['dist'] = ROOT.TCanvas("c1", "Canvas 1", 1500, 1500)
   
   rDists['all'].SetLineColor(1)
   rDists['T2tt'].SetLineColor(2)
   rDists['T2bW'].SetLineColor(3)
  
   rDists['all'].SetMaximum(600)
 
   for rDist in rDists:
      rDists[rDist].Draw("same")

   alignStats(rDists['all'])
   
   l1 = makeLegend2()
   l1.AddEntry("rDist_all", "All", "L")
   l1.AddEntry("rDist_T2tt", "T2tt", "L")
   l1.AddEntry("rDist_T2bW", "T2bW", "L")
   l1.Draw()
 
#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   for canv in canvs:
      #if plot['canvs'][canv][0]:
      canvs[canv].SaveAs("%s/PUsys_%s%s.png"%(savedir, canv, suffix))
      canvs[canv].SaveAs("%s/root/PUsys_%s%s.root"%(savedir, canv, suffix))
      canvs[canv].SaveAs("%s/pdf/PUsys_%s%s.pdf"%(savedir, canv, suffix))

#SR1s = ['sr1a', 'sr1b', 'sr1c', 'sr1vla', 'sr1vlb', 'sr1vlc', 'sr1la', 'sr1lb', 'sr1lc', 'sr1ma', 'sr1mb', 'sr1mc', 'sr1ha', 'sr1hb', 'sr1hc']
#SR2s = ['sr2a', 'sr2b', 'sr2c', 'sr2vla', 'sr2vlb', 'sr2vlc', 'sr2la', 'sr2lb', 'sr2lc', 'sr2ma', 'sr2mb', 'sr2mc', 'sr2ha', 'sr2hb', 'sr2hc']
#CRs =  ['cr1a', 'cr1b', 'cr1c', 'cr2a', 'cr2b', 'cr2c']
#
#regions = SR1s + SR2s + CRs
#allRegions = []
#
#for x in regions:
#   allRegions.append(x+'X')
#   allRegions.append(x+'Y')
#
