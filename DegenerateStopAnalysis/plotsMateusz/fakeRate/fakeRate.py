# fakeRate.py
# Determination of the fake rate (tight-to-loose ratio)
# Mateusz Zarucki 2017

import os
from fakeInfo import *

#ROOT.gStyle.SetOptStat(1111) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptStat(0)

script = os.path.basename(__file__) #sys.argv[0]

#Arguments
args = fakeParser(script)

lep = args.lep
region = args.region
sample = args.sample
getData = args.getData
measurementType = args.measurementType
noWttWeights = args.noWttWeights
varBins = args.varBins
do2D = args.do2D
doYields = args.doYields
logy = args.logy
save = args.save
verbose = args.verbose

do2D = False # FIXME: still under development

fakeInfo = fakeInfo(script, vars(args))

lepton =      fakeInfo['lepton']
samplesList = fakeInfo['samplesList']
samples =     fakeInfo['samples']
dataset =     fakeInfo['dataset']
selection =   fakeInfo['selection']
bins =        fakeInfo['bins']

if save:
   savedir = fakeInfo['savedir']
   saveTag = fakeInfo['saveTag']
   etaBin =  fakeInfo['etaBin']
   suffix =  fakeInfo['suffix']
   
   if doYields: yieldDir = fakeInfo['yieldDir']

   if measurementType:
      resultsDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate"
      resultsDir += "/" + saveTag
      resultsDir += "/%s/TL_%s"%(region, measurementType)
      
      if not varBins: resultsDir += "/fixedBins"
      else:           resultsDir += "/varBins"

      resultsDir += "/" + etaBin   
      
      if noWttWeights: resultsDir += "/noWttWeights"
   
      makeDir(resultsDir)

plotMin = 1
if logy: plotMax = 500000
else:    plotMax = None

if dataset: lumi = selection['lumis'][samples[dataset].name+'_lumi']
else:       lumi = selection['lumis']['target_lumi']

index = selection['loose']['lepIndex1'] #loose index

variables = {\
   'pt':"LepGood_pt[%s]"%index,
   'eta':"abs(LepGood_eta[%s])"%index,
}

#normFactor = {} #NOTE: update later with TH1:Scale("width")
#normFactor['pt'] =  "((nLepGood_{lep}_loose > 0)*(({var} < 5) + ({var} >= 5 && {var} < 12)*0.714 + ({var} >= 12 && {var} < 20)*0.625 + ({var} >= 20 && {var} < 30)*0.5 + ({var} >= 30 && {var} < 200)*0.0294))".format(lep = lep, var = pt)
#normFactor['eta'] = "((nLepGood_{lep}_loose > 0)*(({var} < 0.9)*0.111 + ({var} >= 0.9 && {var} < 1.2)*0.333 + ({var} >= 1.2 && {var} < 2.1)*0.111 + ({var} >= 2.1 && {var} < 2.4)*0.333))".format(lep = lep, var = eta)

#bins = {'pt': array('d', range(0,30,5) + range(30,60,10) + range(60,100,20) + range(100,200+50,50))} #old binning
#normFactor = {'pt': "(({var} < 30) + ({var} >= 30 && {var} < 60)*0.5 + ({var} >= 60 && {var} < 100)*0.25 + ({var} >= 100 && {var} < 200)*0.1)".format(var = pt)} #old binning

##################################################################################################################################################################################

# Creation of histograms

plots = ['pt', 'eta']
ratios = {'pt':{}, 'eta':{}, '2D':{}}

hists = {
   'total':{ 'loose':{'pt':{}, 'eta':{}, '2D':{}}, 'tight':{'pt':{}, 'eta':{}, '2D':{}}},
   'prompt':{'loose':{'pt':{}, 'eta':{}, '2D':{}}, 'tight':{'pt':{}, 'eta':{}, '2D':{}}},
   'fakes':{  'loose':{'pt':{}, 'eta':{}, '2D':{}}, 'tight':{'pt':{}, 'eta':{}, '2D':{}}}
   }

histCont_samps = {
   'total':{ 'loose':{'pt':{}, 'eta':{}}, 'tight':{'pt':{}, 'eta':{}}},
   'prompt':{'loose':{'pt':{}, 'eta':{}}, 'tight':{'pt':{}, 'eta':{}}},
   'fakes':{  'loose':{'pt':{}, 'eta':{}}, 'tight':{'pt':{}, 'eta':{}}}
   }

binCont_samps = {
   'total':{ 'loose':{'pt':{}, 'eta':{}}, 'tight':{'pt':{}, 'eta':{}}},
   'prompt':{'loose':{'pt':{}, 'eta':{}}, 'tight':{'pt':{}, 'eta':{}}},
   'fakes':{  'loose':{'pt':{}, 'eta':{}}, 'tight':{'pt':{}, 'eta':{}}}
   }

stacks = {
   'total':{ 'loose':{}, 'tight':{}},
   'prompt':{'loose':{}, 'tight':{}},
   'fakes':{  'loose':{}, 'tight':{}}
   }

histCont_totalMC = {
   'total':{ 'loose':{}, 'tight':{}},
   'prompt':{'loose':{}, 'tight':{}},
   'fakes':{  'loose':{}, 'tight':{}}
   }

binCont_totalMC = {
   'total':{ 'loose':{}, 'tight':{}},
   'prompt':{'loose':{}, 'tight':{}},
   'fakes':{  'loose':{}, 'tight':{}}
   }

histCont_data = {
   'total':{ 'loose':{}, 'tight':{}},
   }

binCont_data = {
   'total':{ 'loose':{}, 'tight':{}},
   }

finalHists = {'loose':{'pt':{}, 'eta':{}, '2D':{}}, 'tight':{'pt':{}, 'eta':{}, '2D':{}}}

# Selection and weights 

WPs = ['loose', 'tight']
   
# Histograms
if "EWK" in measurementType:
   plotTypes = ['total', 'prompt']
else:
   plotTypes = ['fakes']

for samp in samplesList:
   if samples[samp].isData: 
      sampType = 'data'
   else:
      sampType = 'MC'

   weight = selection['loose'][region][samp][1] #NOTE: Fake rate should be the same indepdendent of the weight! (at least the central value)

   #Selection
   selList = {}
   regionSel = {}

   for WP in ['loose']: #WPs:
      selList[WP] = {}
      regionSel[WP] = selection[WP][region][samp][0] 
 
      selList[WP]['total'] = ["1", regionSel[WP]] 
      
      selList[WP]['total'].append(selection['trigger']) # trigger applied both to data and MC
       
      selList[WP]['prompt'] = selList[WP]['total'][:]
      selList[WP]['fakes'] =  selList[WP]['total'][:]

      selList[WP]['prompt'].append(selection[WP]['cuts'].cuts_dict['prompt']['cut']) 
      selList[WP]['fakes'].append( selection[WP]['cuts'].cuts_dict['fake']['cut']) 

   # Lepton matching done by requiring indices to be equal 
   selection['match'] = "(%s == %s)"%(selection['loose']['lepIndex1'], selection['tight']['lepIndex1'])
 
   selList['tight'] = {}
 
   # tight definition
   for x in ['total', 'prompt', 'fakes']:
      selList['tight'][x] = selList['loose'][x][:] # loose as baseline
      if "measurement1" in region or "measurement4" in region:
         selList['tight'][x].append(selection['tight']['cuts'].cuts_dict['1Lep']['cut']) # one tight lepton
      elif "measurement2" in region:
         selList['tight'][x].append(selection['tight']['cuts'].cuts_dict['1Tag1Probe']['cut']) # two tight leptons
         selList['tight'][x].append(selection['tight']['cuts'].cuts_dict['min1Probe']['cut']) # min one tight lepton of specific flavour 
         selList['tight'][x].append(selection['tight']['cuts'].cuts_dict['ProbeFlav']['cut']) # the probe (2nd lepton) should have this flavour 
      else:
         selList['tight'][x].append(selection['match']) 
 
   # Final cut strings
   cutStr = {'loose':{}, 'tight':{}}
   for x in ['total', 'prompt', 'fakes']:
      cutStr['loose'][x] = weight + "*(" + combineCutsList(selList['loose'][x]) + ")"
      cutStr['tight'][x] = weight + "*(" + combineCutsList(selList['tight'][x]) + ")"
      
   if verbose:
      print makeLine() 
      print "Sample:", samp
      print makeLine() 
      print "Weight:", weight 
      print makeLine() 
      print "Loose selection:",    selList['loose'] 
      print makeLine() 
      #print "Cut string (loose):", cutStr['loose'] 
      #print makeLine() 
      print "Tight selection:",    selList['tight'] 
      print makeLine() 
      #print "Cut string (tight):", cutStr['tight'] 
      #print makeLine() 

   for plotType in plotTypes:
      if sampType == "data": plotType = "total"
      for plot in plots:
         for WP in WPs: 
            if not varBins:
               hists[plotType][WP][plot][samp] = makeHist(samples[samp].tree, variables[plot], cutStr[WP][plotType], bins[plot][0], bins[plot][1], bins[plot][2], addOverFlowBin = 'upper')
            else: 
               hists[plotType][WP][plot][samp] = makeHistVarBins(samples[samp].tree, variables[plot],  cutStr[WP][plotType], bins[plot],  variableBinning = (varBins, bins[plot][1]-bins[plot][0]), addOverFlowBin = 'upper')

            hists[plotType][WP][plot][samp].SetName("%s_%s_%s"%(WP, plot, samp))
            hists[plotType][WP][plot][samp].SetLineWidth(1)
            if plotMax: hists[plotType][WP][plot][samp].SetMaximum(plotMax)

            if sampType != "data": 
               hists[plotType][WP][plot][samp].SetFillColor(colors[samp])
           
         if do2D:
            if not varBins:
               hists[plotType][WP]['2D'][samp] = make2DHist(samples[samp].tree, variables['pt'], variables['eta'], cutStr[WP][plotType], bins['pt'][0], bins['pt'][1], bins['pt'][2], bins['eta'][0], bins['eta'][1], bins['eta'][2])
            #else:
               #hists[plotType][WP]['2D'][samp] = make2DHistVarBins(samples[samp].tree, variables['pt'], variables['eta'], "%s*%s*(%s)"%(normFactor['pt'], normFactor['eta'], cutString[WP][plotType]), bins['pt'], bins['eta'])
               #hists[plotType][WP]['2D'][samp].GetYaxis().SetTitle("Events / 5 GeV")
               #hists[plotType][WP]['2D'][samp].GetYaxis().SetTitle("Events / 0.1 rad")
               
               hists[plotType][WP]['2D'][samp].SetName("%s_2D_%s"%(WP,samp))
   
   if doYields:
      plot = 'pt' 
      for plotType in plotTypes:
         if sampType == "data": plotType = "total"
         for WP in WPs: 
            histCont_samps[plotType][WP][plot][samp] = getHistContents(hists[plotType][WP][plot][samp], varBinsYield = varBins)
            binCont_samps[plotType][WP][plot][samp] = histCont_samps[plotType][WP][plot][samp][0] 
          
         a = histCont_samps[plotType]['loose'][plot][samp][1]
         w = histCont_samps[plotType]['loose'][plot][samp][2]
         
         if save:
            for i in binCont_samps[plotType]['loose'][plot][samp]:
               if not os.path.isfile("%s/composition/mcYields_%s_%s%s.txt"%(yieldDir, samp, plotType, suffix)):
                  outfile = open("%s/composition/mcYields_%s_%s%s.txt"%(yieldDir, samp, plotType, suffix), "w")
                  outfile.write("Bin yields in %s region for the %s channel (%s sample)\n"%(region.title(), lepton, samp))
                  title = "Bin (GeV)      |        Loose           |         Tight\n"
                  outfile.write(title)

               with open("%s/composition/mcYields_%s_%s%s.txt"%(yieldDir, samp, plotType, suffix), "a") as outfile:
                  outfile.write("{}-{}".format(str(int(a[i])), str(int(a[i]+w[i]))).ljust(15) + ' | ' +\
                  str(binCont_samps[plotType]['loose'][plot][samp][i].round(3)).ljust(25) + ' | ' +\
                  str(binCont_samps[plotType]['tight'][plot][samp][i].round(3)) + "\n")
      
if do2D: plots.append('2D')

# Measurement of tight-to-loose ratio

if measurementType:
   for plot in plots: 
      for WP in WPs: 
         for plotType in plotTypes:
            stackName = '%s_%s_%s_%s'%(plotType, measurementType, WP, plot)
            stacks[plotType][WP][plot] = ROOT.THStack(stackName, stackName)
         
            for samp in samplesList:
               if not samples[samp].isData: # MC only 
                  stacks[plotType][WP][plot].Add(hists[plotType][WP][plot][samp])
         
         if measurementType == "MC":
            basePlot = 'fakes'
            finalHists[WP][plot][measurementType] = stacks[basePlot][WP][plot].GetStack().Last().Clone() # Fakes only
         
            if plot == "2D":
               finalHists['loose'][plot][measurementType].SetTitle("%ss: %s p_{T} vs |#eta| Distribution in MC Samples (Fakes)"%(lepton, WP))
            else:   
               finalHists['loose'][plot][measurementType].SetTitle("%ss: Loose vs Tight comparison for MC Samples (Fakes)"%lepton)
                     
         elif measurementType == "MC-EWK": # emulation of prompt subtraction from data using MC yields
            basePlot = 'total'
            finalHists[WP][plot][measurementType] = stacks[basePlot][WP][plot].GetStack().Last().Clone() # Total MC 
            setErrSqrtN(finalHists[WP][plot][measurementType]) # setting error as sqrt N
            finalHists[WP][plot][measurementType].Add(stacks['prompt'][WP][plot].GetStack().Last().Clone(), -1) # Subtract prompt 
            
            if plot == "2D":
               finalHists['loose'][plot][measurementType].SetTitle("%ss: %s p_{T} vs |#eta| Distribution in MC Samples (Prompt Subtracted)"%(lepton, WP))
            else:   
               finalHists['loose'][plot][measurementType].SetTitle("%ss: Loose vs Tight comparison for MC Samples (Prompt Subtracted)"%lepton)
         
         elif measurementType == "data-EWK":
            basePlot = 'total'
            finalHists[WP][plot][measurementType] = hists[basePlot][WP][plot][dataset].Clone() # Data 
            finalHists[WP][plot][measurementType].Add(stacks['prompt'][WP][plot].GetStack().Last().Clone(), -1) # Subtract prompt 
   
            if plot == "2D": 
               finalHists['loose'][plot][measurementType].SetTitle("%ss: %s p_{T} vs |#eta| Distribution in Data Sample (Prompt Subtracted)"%(lepton, WP))
            else:   
               finalHists['loose'][plot][measurementType].SetTitle("%ss: Loose vs Tight comparison for Data Sample (Prompt Subtracted)"%lepton)
   
         finalHists[WP][plot][measurementType].SetName("%s_%s_%s"%(WP,plot,measurementType))

   sample = measurementType
         
else: # One sample
   for plot in plots: 
      for WP in WPs:
         finalHists[WP][plot][sample] = hists['fakes'][WP][plot][sample]
         finalHists[WP][plot][sample].SetTitle("%ss: Loose vs Tight comparison for %s Sample"%(lepton, samples[sample].name))
   
      if do2D: 
         finalHists[WP]['2D'][sample] = hists['fakes'][WP]['2D'][sample]
         finalHists[WP]['2D'][sample].SetTitle("%ss: %s p_{T} vs |#eta| Distribution in %s Sample"%(lepton, WP, samples[sample].name))

# Yields
if doYields and measurementType:
   # pickle MC yields 
   plot = 'pt' 
   for plotType in plotTypes:
      for WP in WPs:
         histCont_totalMC[plotType][WP][plot] = getHistContents(stacks[plotType][WP][plot].GetStack().Last().Clone(), varBinsYield = varBins)
         binCont_totalMC[plotType][WP][plot] = histCont_totalMC[plotType][WP][plot][0] 
       
      a = histCont_totalMC[plotType]['loose'][plot][1]
      w = histCont_totalMC[plotType]['loose'][plot][2]
      
      if save:
         for i in binCont_totalMC[plotType]['loose'][plot]:
            if not os.path.isfile("%s/mcYields_%s%s.txt"%(yieldDir, plotType, suffix)):
               outfile = open("%s/mcYields_%s%s.txt"%(yieldDir, plotType, suffix), "w")
               outfile.write("%s yields in %s region for the %s channel\n"%(plotType.title(), region.title(), lepton))
               title = "Bin (GeV)      |        Loose           |         Tight\n"
               outfile.write(title)
   
            with open("%s/mcYields_%s%s.txt"%(yieldDir, plotType, suffix), "a") as outfile:
               outfile.write("{}-{}".format(str(int(a[i])), str(int(a[i]+w[i]))).ljust(15) + ' | ' +\
               str(binCont_totalMC[plotType]['loose'][plot][i].round(3)).ljust(25) + ' | ' +\
               str(binCont_totalMC[plotType]['tight'][plot][i].round(3)) + "\n")
      
         pickleFile1 = open("%s/mcYields_%s%s.pkl"%(yieldDir, plotType, suffix), "w")
         pickle.dump(binCont_totalMC, pickleFile1)
         pickleFile1.close()

   # pickle data yields
   if 'data' in measurementType:
      plotType = 'total' 
      for WP in WPs:
         histCont_data[plotType][WP][plot] = getHistContents(hists[basePlot][WP][plot][dataset].Clone(), varBinsYield = varBins)
         binCont_data[plotType][WP][plot] = histCont_data[plotType][WP][plot][0] 
      
      if save:
         pickleFile2 = open("%s/dataYields_%s%s.pkl"%(yieldDir, plotType, suffix), "w")
         pickle.dump(binCont_data, pickleFile2)
         pickleFile2.close()
   
   # numbers from final hists
   histCont = {}
   histCont_ylds = {}
   binCont =      {'ratio':{}}
   binCont_ylds = {'ratio':{}}

   for WP in WPs:
      histCont[WP] =      getHistContents(finalHists[WP]['pt'][measurementType])
      histCont_ylds[WP] = getHistContents(finalHists[WP]['pt'][measurementType], varBinsYield = varBins)
      binCont[WP] =       histCont[WP][0]
      binCont_ylds[WP] =  histCont_ylds[WP][0]
   
   a = histCont['loose'][1]
   w = histCont['loose'][2]

   for i in binCont['loose']:
      if binCont['loose'][i].val: 
         binCont['ratio'][i] =      binCont['tight'][i]/binCont['loose'][i]
         binCont_ylds['ratio'][i] = binCont['tight'][i]/binCont['loose'][i]
      else:
         binCont['ratio'][i] =      u_float.u_float(0.,0.)
         binCont_ylds['ratio'][i] = u_float.u_float(0.,0.)

      if verbose:
         print makeLine()
         print "T-L ratio in bin %s (%s-%s) GeV"%(str(i), str(int(a[i])), str(int(a[i]+w[i])))
         print makeLine()
         print "Loose:",     binCont['loose'][i].round(3)
         print "Tight:",     binCont['tight'][i].round(3)
         print "T-L Ratio:", binCont['ratio'][i].round(3)
         print makeLine()
   
      if save:
         if not os.path.isfile("%s/tightToLooseRatios%s.txt"%(yieldDir, suffix)):
            outfile = open("%s/tightToLooseRatios%s.txt"%(yieldDir, suffix), "w")
            outfile.write("T-L Ratio yields in %s region for the %s channel (%s)\n"%(region.title(), lepton, measurementType))
            title = "Bin (GeV)      |        Loose           |         Tight        |        T-L Ratio\n"
            outfile.write(title)

         with open("%s/tightToLooseRatios%s.txt"%(yieldDir, suffix), "a") as outfile:
            outfile.write("{}-{}".format(str(int(a[i])), str(int(a[i]+w[i]))).ljust(15) + ' | ' +\
            str(binCont['loose'][i].round(3)).ljust(25) + ' | ' +\
            str(binCont['tight'][i].round(3)).ljust(25) + ' | ' +\
            str(binCont['ratio'][i].round(3)) + "\n")
         
         if not os.path.isfile("%s/tightToLooseRatios_yields%s.txt"%(yieldDir, suffix)):
            outfile = open("%s/tightToLooseRatios_yields%s.txt"%(yieldDir, suffix), "w")
            outfile.write("T-L Ratio yields in %s region for the %s channel (%s)\n"%(region.title(), lepton, measurementType))
            title = "Bin (GeV)      |        Loose           |         Tight        |        T-L Ratio\n"
            outfile.write(title)

         with open("%s/tightToLooseRatios_yields%s.txt"%(yieldDir, suffix), "a") as outfile:
            outfile.write("{}-{}".format(str(int(a[i])), str(int(a[i]+w[i]))).ljust(15) + ' | ' +\
            str(binCont_ylds['loose'][i].round(3)).ljust(25) + ' | ' +\
            str(binCont_ylds['tight'][i].round(3)).ljust(25) + ' | ' +\
            str(binCont_ylds['ratio'][i].round(3)) + "\n")

      #Pickle results 
      pickleFile3 = open("%s/tightToLooseRatios%s.pkl"%(yieldDir,suffix), "w")
      pickle.dump(binCont_ylds, pickleFile3)
      pickleFile3.close()
      
      pickleFile4 = open("%s/tightToLooseRatios%s.pkl"%(resultsDir,suffix), "w")
      pickle.dump(binCont_ylds, pickleFile4)
      pickleFile4.close()

# Efficiency plots
for plot in plots:
   ratios[plot][sample] =  divideHists(finalHists['tight'][plot][sample], finalHists['loose'][plot][sample])
   ratios[plot][sample].SetName("ratio_%s_%s"%(plot, sample))

if measurementType == "data-EWK":
   ratios['pt'][sample].SetTitle( "%ss: Tight to Loose Ratio for Data Sample (Prompt Subtracted) ; %s p_{T} / GeV ; Ratio"%(lepton, lepton))
   ratios['eta'][sample].SetTitle("%ss: Tight to Loose Ratio for Data Sample (Prompt Subtracted) ; %s |#eta| ; Ratio"%(lepton, lepton))
   if do2D: ratios['2D'][sample].SetTitle("{lep}s: Tight to Loose Ratio for Data Sample (Prompt Subtracted) ; {lep} p_{{T}}; {lep} |#eta|".format(lep = lepton))
elif measurementType == "MC-EWK":
   ratios['pt'][sample].SetTitle( "%ss: Tight to Loose Ratio for MC Samples (Prompt Subtracted) ; %s p_{T} / GeV ; Ratio"%(lepton, lepton))
   ratios['eta'][sample].SetTitle("%ss: Tight to Loose Ratio for MC Samples (Prompt Subtracted) ; %s |#eta| ; Ratio"%(lepton, lepton))
   if do2D: ratios['2D'][sample].SetTitle("{lep}s: Tight to Loose Ratio for MC Samples (Prompt Subtracted) ; {lep} p_{{T}}; {lep} |#eta|".format(lep = lepton))
elif measurementType == "MC":
   ratios['pt'][sample].SetTitle( "%ss: Tight to Loose Ratio for MC Samples (Fakes) ; %s p_{T} / GeV ; Ratio"%(lepton, lepton))
   ratios['eta'][sample].SetTitle("%ss: Tight to Loose Ratio for MC Samples (Fakes) ; %s |#eta| ; Ratio"%(lepton, lepton))
   if do2D: ratios['2D'][sample].SetTitle("{lep}s: Tight to Loose Ratio for MC Samples (Fakes) ; {lep} p_{{T}}; {lep} |#eta|".format(lep = lepton))
else:
   ratios['pt'][sample].SetTitle( "%ss: Tight to Loose Ratio for %s Sample ; %s p_{T} / GeV ; Ratio"%(lepton, samples[sample].name, lepton))
   ratios['eta'][sample].SetTitle("%ss: Tight to Loose Ratio for %s Sample ; %s |#eta| ; Ratio"%(lepton, samples[sample].name, lepton))
   if do2D: ratios['2D'][sample].SetTitle("{lep}s: Tight to Loose Ratio for {} Sample ; {lep} p_{{T}}; {lep} |#eta|".format(samples[sample].name, lep = lepton))

###############################################################################################################################################################################

canvs = {}

for x in ['pt', 'eta']:

   canvs[x] = ROOT.TCanvas("canv_" + x, "Canvas " + x, 1200, 1700)
   canvs[x].Divide(1,2)
   
   canvs[x].cd(1)
      
   if x == "pt":
      finalHists['loose'][x][sample].GetXaxis().SetTitle("%s p_{T} / GeV"%lepton)
   elif x == "eta":
      finalHists['loose'][x][sample].GetXaxis().SetTitle("%s |#eta| "%lepton)
   
   finalHists['loose'][x][sample].SetFillColor(ROOT.kViolet+10)
   #finalHists['loose'][x][sample].SetMinimum(1)
   if plotMax: finalHists['loose'][x][sample].SetMaximum(plotMax)
   finalHists['loose'][x][sample].Draw("hist")
   
   #alignStats(finalHists['loose'][x][sample])
   
   finalHists['tight'][x][sample].SetFillColor(ROOT.kRed+1)
   finalHists['tight'][x][sample].SetFillColorAlpha(finalHists['tight'][x][sample].GetFillColor(), 0.8)
   finalHists['tight'][x][sample].Draw("histsame")
    
   if logy: ROOT.gPad.SetLogy()
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   l1 = makeLegend2()
   l1 = ROOT.TLegend()
   l1.AddEntry("loose_%s_%s"%(x, sample), "Loose", "F")
   l1.AddEntry("tight_%s_%s"%(x, sample), "Tight", "F")
   l1.Draw()
   
   alignLegend(l1, y1=0.5, y2=0.65)
   
   # Ratio 
   canvs[x].cd(2)
   
   ratios[x][sample].GetYaxis().SetTitle("#epsilon_{TL}")
   ratios[x][sample].SetLineWidth(2) 
   ratios[x][sample].Draw("P")
   
   #setupEffPlot(ratios[x][sample])
   ratios[x][sample].SetMinimum(0)
   ratios[x][sample].SetMaximum(1.0)
   
   #ratios[x][sample].GetPaintedGraph().SetMinimum(0)
   #ratios[x][sample].GetPaintedGraph().SetMaximum(0.6)
   #ratios[x][sample].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)
   
   #Colours
   ratios[x][sample].SetMarkerColor(ROOT.kGreen+3)
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   canvs[x].Modified()
   canvs[x].Update()

if do2D:
   finalHists['loose']['2D'][sample].GetXaxis().SetTitle("%s p_{T}"%lepton)
   finalHists['loose']['2D'][sample].GetYaxis().SetTitle("%s |#eta|"%lepton)
   #finalHists['loose']['2D'][sample].GetZaxis().SetRangeUser(0, 4)
   #alignStats(finalHists['loose']['2D'][sample])
   
   finalHists['tight']['2D'][sample].GetXaxis().SetTitle("%s p_{T}"%lepton)
   finalHists['tight']['2D'][sample].GetYaxis().SetTitle("%s |#eta|"%lepton)
   
   ratios['2D'][sample].SetMarkerSize(0.8)
   
   #####Canvas 3#####
   canvs['2D'] = ROOT.TCanvas("canv_2D", "Canvas 2D", 1800, 1500)
   ratios['2D'][sample].Draw("COLZ TEXTE89") #CONT1-5 #plots the graph with axes and points
   #ratios['2D'][sample].GetPaintedGraph().GetXaxis().SetTitle("%s p_{T}"%lepton)
   #ratios['2D'][sample].GetPaintedGraph().GetYaxis().SetTitle("%s |#eta|"%lepton)
   #ratios['2D'][sample].SetMinimum(0.8)
   #ratios['2D'][sample].SetMaximum(5)
   #ratios['2D'][sample].GetZaxis().SetRangeUser(0.8,1.2)
   
   #alignStats(ratios['2D'][sample])
   
   #if logy: ROOT.gPad.SetLogz()
   canvs['2D'].Modified()
   canvs['2D'].Update()
   
   #####Canvas 4#####
   
   canvs['2D_dist'] = ROOT.TCanvas("c_2D_dist", "Canvas 2D Distributions", 1800, 1500)
   canvs['2D_dist'].Divide(1,2)
   
   canvs['2D_dist'].cd(1)
   finalHists['tight']['2D'][sample].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
   if logy: ROOT.gPad.SetLogz()
   
   canvs['2D_dist'].cd(2)
   finalHists['loose']['2D'][sample].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
   if logy: ROOT.gPad.SetLogz()
   canvs['2D_dist'].Modified()
   canvs['2D_dist'].Update()

decor = {}
decor['pt'] = {"title": "Lepton p_{T} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}
decor['eta'] = {"title": "Lepton |#eta| Plot", "y":"Events", "x":"%s |#eta|"%lepton, "log":[0,logy,0]}

dataHist = {'pt':{}, 'eta':{}}

## Legend
#legy = [0.7, 0.87]
#if getData:
#   legx = [0.75, 0.95]
#else:
#   legx = [0.65, 0.85]
#
#nBkgInLeg = 4
#subBkgLists = [samplesList[x:x+nBkgInLeg] for x in range(0,len(samplesList),nBkgInLeg)]
#nBkgLegs = len(subBkgLists)
#for i, subBkgList in enumerate( subBkgLists ):
#    newLegY0 = legy[0] + (legy[1]-legy[0])* (1-1.*len(subBkgList)/nBkgInLeg)
#    leg = makeLegend(samples, None, subBkgList, None, loc=[legx[0], newLegY0, legx[1],legy[1]], name="Legend", legOpt="f")
#
if measurementType:
   for plot in plots:
      for WP in WPs:
         for plotType in plotTypes: 
            if measurementType == "data-EWK" and plotType == "total":
               dataHist[plot][WP] = hists['total'][WP][plot][dataset]
            else:
               dataHist[plot][WP] = None
            
            canvs['%s2_%s_%s'%(plot, WP, plotType)] = drawPlot(stacks[plotType][WP][plot], dataHist = dataHist[plot][WP], lumi = lumi, legend = None, decor = decor[plot], latexText = None, ratio = None, ratioTitle = None, plotMin = plotMin, plotMax = plotMax)

#Save canvas
if save:
   canvs['pt'].SaveAs("%s/FakeRate_TightToLoose_lepPt%s.png"%(savedir, suffix))
   canvs['pt'].SaveAs("%s/pdf/FakeRate_TightToLoose_lepPt%s.pdf"%(savedir, suffix))
   canvs['pt'].SaveAs("%s/root/FakeRate_TightToLoose_lepPt%s.root"%(savedir, suffix))
   
   canvs['eta'].SaveAs("%s/FakeRate_TightToLoose_lepEta%s.png"%(savedir, suffix))
   canvs['eta'].SaveAs("%s/pdf/FakeRate_TightToLoose_lepEta%s.pdf"%(savedir, suffix))
   canvs['eta'].SaveAs("%s/root/FakeRate_TightToLoose_lepEta%s.root"%(savedir, suffix))
    
   if measurementType: 
      for WP in WPs:
         for plotType in plotTypes: 
            canvs['pt2_%s_%s'%(WP, plotType)]['canvs'][0].SaveAs("%s/FakeRate_TightToLoose_lepPt_stack_%s_%s%s.png"%(savedir, WP, plotType, suffix))
            canvs['pt2_%s_%s'%(WP, plotType)]['canvs'][0].SaveAs("%s/pdf/FakeRate_TightToLoose_lepPt_stack_%s_%s%s.pdf"%(savedir, WP, plotType, suffix))
            canvs['pt2_%s_%s'%(WP, plotType)]['canvs'][0].SaveAs("%s/root/FakeRate_TightToLoose_lepPt_stack_%s_%s%s.root"%(savedir, WP, plotType, suffix))
            
            canvs['eta2_%s_%s'%(WP, plotType)]['canvs'][0].SaveAs("%s/FakeRate_TightToLoose_lepEta_stack_%s_%s%s.png"%(savedir, WP, plotType, suffix))
            canvs['eta2_%s_%s'%(WP, plotType)]['canvs'][0].SaveAs("%s/pdf/FakeRate_TightToLoose_lepEta_stack_%s_%s%s.pdf"%(savedir, WP, plotType, suffix))
            canvs['eta2_%s_%s'%(WP, plotType)]['canvs'][0].SaveAs("%s/root/FakeRate_TightToLoose_lepEta_%s_%s%s.root"%(savedir, WP, plotType, suffix))

   if do2D:   
      canvs['2D'].SaveAs("%s/FakeRate_TightToLoose_2D_Ratio%s.png"%(savedir, suffix))
      canvs['2D'].SaveAs("%s/pdf/FakeRate_TightToLoose_2D_Ratio%s.pdf"%(savedir, suffix))
      canvs['2D'].SaveAs("%s/root/FakeRate_TightToLoose_2D_Ratio%s.root"%(savedir, suffix))
      
      canvs['2D_dist'].SaveAs("%s/FakeRate_TightToLoose_2D_distributions%s.png"%(savedir, suffix))
      canvs['2D_dist'].SaveAs("%s/pdf/FakeRate_TightToLoose_2D_distributions%s.pdf"%(savedir, suffix))
      canvs['2D_dist'].SaveAs("%s/root/FakeRate_TightToLoose_2D_distributions%s.root"%(savedir, suffix))

   if measurementType and "measurement" in region:
      canvs['pt'].SaveAs("%s/FakeRate_TightToLoose_lepPt%s.root"%(resultsDir, suffix))
      canvs['eta'].SaveAs("%s/FakeRate_TightToLoose_lepEta%s.root"%(resultsDir, suffix))
      if do2D: canvs['2D'].SaveAs("%s/FakeRate_TightToLoose_2D_Ratio%s.root"%(resultsDir, suffix))
