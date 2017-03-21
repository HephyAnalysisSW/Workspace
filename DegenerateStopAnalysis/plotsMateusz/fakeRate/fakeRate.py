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
mva = args.mva
getData = args.getData
sample = args.sample
noWeights = args.noWeights
fakeTauVeto = args.fakeTauVeto
fakeRateMeasurement = args.fakeRateMeasurement
varBins = args.varBins
do2D = args.do2D
doYields = args.doYields
logy = args.logy
save = args.save
verbose = args.verbose

if varBins: do2D = False #NOTE: still under development

fakeInfo = fakeInfo(script, vars(args))

lepton =      fakeInfo['lepton']
samplesList = fakeInfo['samplesList']
samples =     fakeInfo['samples']
selection =   fakeInfo['selection']
bins =        fakeInfo['bins']

if save:
   savedir = fakeInfo['savedir']
   suffix =  fakeInfo['suffix']

   if fakeRateMeasurement:
      resultsDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate"
      
      resultsDir += "/%s/TL_%s"%(region, fakeRateMeasurement)
      
      if not varBins: resultsDir += "/fixedBins"
      else:           resultsDir += "/varBins"
      
      makeDir(resultsDir)

index = selection['MC']['loose']['lepIndex'] #loose index

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
   'total':{'loose':{'pt':{}, 'eta':{}, '2D':{}}, 'tight':{'pt':{}, 'eta':{}, '2D':{}}},
    'prompt':{'loose':{'pt':{}, 'eta':{}, '2D':{}}, 'tight':{'pt':{}, 'eta':{}, '2D':{}}},
    'fake':{'loose':{'pt':{}, 'eta':{}, '2D':{}}, 'tight':{'pt':{}, 'eta':{}, '2D':{}}}
   }

finalHists = {'loose':{'pt':{}, 'eta':{}, '2D':{}}, 'tight':{'pt':{}, 'eta':{}, '2D':{}}}

# Selection and weights 

WPs = ['loose', 'tight']
 
for samp in samplesList:
   if samples[samp].isData: 
      sampType = 'data'
   else:
      sampType = 'MC'

   weight = selection[sampType]['loose'][region][samp][1] #NOTE: Fake rate should be the same indepdendent of the weight! (at least the central value)

   #Selection
   selList = {}
   regionSel = {}

   for WP in WPs:
      selList[WP] = {}
      regionSel[WP] = selection[sampType][WP][region][samp][0] 
 
      selList[WP]['total'] = ["1", regionSel[WP]] 
      
      if sampType == 'data': 
         selList[WP]['total'].append(selection[sampType]['trigger'])
       
      selList[WP]['prompt'] = selList[WP]['total'][:]
      selList[WP]['fake'] =   selList[WP]['total'][:]

      selList[WP]['prompt'].append(selection[sampType][WP]['cuts_weights'].cuts.cuts_dict['prompt']['cut']) 
      selList[WP]['fake'].append(selection[sampType][WP]['cuts_weights'].cuts.cuts_dict['fake']['cut']) 
   
   # Lepton matching done by requiring indices to be equal 
   selection[sampType]['match'] = "(%s == %s)"%(selection[sampType]['loose']['lepIndex'], selection[sampType]['tight']['lepIndex'])
   
   #tight definition
   for x in ['total', 'prompt', 'fake']:
      selList['tight'][x].extend(selList['loose'][x][:])
      selList['tight'][x].append(selection[sampType]['match']) 
 
   # Final cut strings
   cutStr = {'loose':{}, 'tight':{}}
   for x in ['total', 'prompt', 'fake']:
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

   # Histograms
   histList = ['fake']
   if "EWK" in fakeRateMeasurement:
      histList.extend(['total', 'prompt'])
   elif not fakeRateMeasurement and sampType == "data":
      histList.append('total')
   
   for hist in histList: 
      if sampType == "data" and hist in ['prompt', 'fake']: continue
      
      for WP in WPs: 
         for plot in plots:
            if not varBins:
               hists[hist][WP][plot][samp] = makeHist(samples[samp].tree, variables[plot], cutStr[WP][hist], bins[plot][0], bins[plot][1], bins[plot][2])
            else: 
               hists[hist][WP][plot][samp] = makeHistVarBins(samples[samp].tree, variables[plot],  cutStr[WP][hist], bins[plot],  variableBinning = (varBins, bins[plot][1]-bins[plot][0]))
            hists[hist][WP][plot][samp].SetName("%s_%s_%s"%(WP, plot, samp))
              
         if do2D:
            if not varBins:
               hists[hist][WP]['2D'][samp] = make2DHist(samples[samp].tree, variables['pt'], variables['eta'], cutStr[WP][hist], bins['pt'][0], bins['pt'][1], bins['pt'][2], bins['eta'][0], bins['eta'][1], bins['eta'][2])
            #else:
               #hists[hist][WP]['2D'][samp] = make2DHistVarBins(samples[samp].tree, variables['pt'], variables['eta'], "%s*%s*(%s)"%(normFactor['pt'], normFactor['eta'], cutString[WP][hist]), bins['pt'], bins['eta'])
               #hists[hist][WP]['2D'][samp].GetYaxis().SetTitle("Events / 5 GeV")
               #hists[hist][WP]['2D'][samp].GetYaxis().SetTitle("Events / 0.1 rad")
               
               hists[hist][WP]['2D'][samp].SetName("%s_2D_%s"%(WP,samp))
      
if do2D: plots.append('2D')

if fakeRateMeasurement:
      
   sample = fakeRateMeasurement  

   for plot in plots: 
      for WP in WPs: 
         if fakeRateMeasurement == "data-EWK":
            finalHists[WP][plot][sample] = hists['total'][WP][plot][dataSample].Clone()
         elif fakeRateMeasurement == "MC-EWK":
            finalHists[WP][plot][sample] = hists['total'][WP][plot]['qcd'].Clone()
         elif fakeRateMeasurement == "MC":
            finalHists[WP][plot][sample] = hists['fake'][WP][plot]['qcd'].Clone()
         
         finalHists[WP][plot][sample].SetName("%s_%s_%s"%(WP,plot,sample))
         
         if fakeRateMeasurement == "data-EWK":
            for samp in samplesList:
               if samp != dataSample and samp != 'qcd':
                  finalHists[WP][plot][sample].Add(hists['prompt'][WP][plot][samp], -1) #NOTE: Subtract prompt 
   
            if plot == "2D": 
               finalHists['loose'][plot][sample].SetTitle("%ss: %s p_{T} vs |#eta| Distribution in Data Sample (Prompt Subtracted)"%(lepton, WP))
            else:   
               finalHists['loose'][plot][sample].SetTitle("%ss: Loose vs Tight comparison for Data Sample (Prompt Subtracted)"%lepton)

         elif fakeRateMeasurement == "MC-EWK":
            for samp in samplesList:
               if samp != 'qcd':
                  finalHists[WP][plot][sample].Add(hists['total'][WP][plot][samp]) # NOTE: Add total 
                  finalHists[WP][plot][sample].Add(hists['prompt'][WP][plot][samp], -1) #NOTE: Subtract prompt 
            
            if plot == "2D":
               finalHists['loose'][plot][sample].SetTitle("%ss: %s p_{T} vs |#eta| Distribution in MC Samples (Prompt Subtracted)"%(lepton, WP))
            else:   
               finalHists['loose'][plot][sample].SetTitle("%ss: Loose vs Tight comparison for MC Samples (Prompt Subtracted)"%lepton)
   
         elif fakeRateMeasurement == "MC":
            for samp in samplesList:
                  if samp != 'qcd':
                     finalHists[WP][plot][sample].Add(hists['fake'][WP][plot][samp]) # NOTE: Add fakes only
            if plot == "2D":
               finalHists['loose'][plot][sample].SetTitle("%ss: %s p_{T} vs |#eta| Distribution in MC Samples (Fakes)"%(lepton, WP))
            else:   
               finalHists['loose'][plot][sample].SetTitle("%ss: Loose vs Tight comparison for MC Samples (Fakes)"%lepton)
           
else:
   for WP in WPs:
      for plot in plots: 
         finalHists[WP][plot][sample] =  hists['fake'][WP][plot][sample]
         finalHists[WP][plot][sample].SetTitle("%ss: Loose vs Tight comparison for %s Sample"%(lepton, samples[sample].name))
   
      if do2D: 
         finalHists[WP]['2D'][sample] = hists['fake'][WP]['2D'][sample]
         finalHists[WP]['2D'][sample].SetTitle("%ss: %s p_{T} vs |#eta| Distribution in %s Sample"%(lepton, WP, samples[sample].name))

# Yields
#if doYields:
   #yields = {}

   #for WP in WPs:
   #   yields[WP] = finalHists[WP]['pt'][sample].GetEntries()

   #if not os.path.isfile("%s/fakeRateYields2_%s%s.txt"%(yieldDir, region, suffix)):
   #   outfile = open("%s/fakeRateYields2_%s%s.txt"%(yieldDir, region, suffix), "w")
   #   outfile.write("Fake Rate Yields in %s\n"%region.title())
   #   outfile.write("Sample        Loose                Tight\n")
   #outfile.write(sample.ljust(10) + str(yields['loose']).ljust(15) + str(yields['tight']) + "\n")
   #outfile.close() 

   #n = fakeRate['pt'].GetNbinsX()

   #value =  {'fakeRate':{}, 'looseCR':{}, 'estimate':{}, 'SR':{}, 'closure':{}}
   #error =  {'fakeRate':{}, 'looseCR':{}, 'estimate':{}, 'SR':{}, 'closure':{}}
   #uFloat = {'fakeRate':{}, 'looseCR':{}, 'estimate':{}, 'SR':{}, 'closure':{}}

   #for i in range(n):
   #   a = int(fakeRate['pt'].GetBinLowEdge(i+1))
   #   w = int(fakeRate['pt'].GetBinWidth(i+1))

   #   for x in value:
   #      y = x
   #      # Convert THStack into TH1
   #      if type(fakeHists[x]) == ROOT.THStack:
   #         y = x + '_hist'
   #         fakeHists[y] = fakeHists[x].GetStack().Last().Clone()

   #      value[x][i] = fakeHists[y].GetBinContent(i+1)
   #      error[x][i] = fakeHists[y].GetBinError(i+1)
   #      uFloat[x][i] = u_float.u_float(value[x][i], error[x][i])

   #   if verbose:
   #      print makeLine()
   #      print "Fake rate estimation in bin %s %s-%s GeV"%(str(i), str(a), str(a+w))
   #      print makeLine()
   #      print "T-L Ratio:",          uFloat['fakeRate'][i].round(3)
   #      print "L(!T) CR:",           uFloat['looseCR'][i].round(3)
   #      print "Estimate:",           uFloat['estimate'][i].round(3)
   #      print "Estimate (x-check):", (uFloat['fakeRate'][i]*uFloat['looseCR'][i]).round(3)
   #      print "SR MC:",              uFloat['SR'][i].round(3)
   #      print "Closure:",            uFloat['closure'][i].round(3)
   #      if uFloat['estimate'][i].val:
   #         print "Closure (x-check):", (uFloat['SR'][i]/uFloat['estimate'][i]).round(3)
   #      print makeLine()

   #   if save:
   #      if not os.path.isfile("%s/fakesEstimation_%s.txt"%(savedir, suffix)):
   #         outfile = open("%s/fakesEstimation_%s.txt"%(savedir, suffix), "w")
   #         outfile.write("Estimation of fakes in %s region for the %s channel \n"%(region.title(), lepton))
   #         title = "Bin (GeV)         T-L Ratio               Loose CR             Estimate (Pred.)              SR: Fakes (MC)             Closure (%s)\n"%(closureDef.title())
   #         if looseNotTight: title = title.replace("Loose", "L!T")
   #         outfile.write(title)

   #      with open("%s/fakesEstimation_%s.txt"%(savedir, suffix), "a") as outfile:
   #         outfile.write("{}-{}".format(str(a), str(a+w)).ljust(15) +\
   #         str(uFloat['fakeRate'][i].round(3)).ljust(25) +\
   #         str(uFloat['looseCR'][i].round(3)).ljust(25) +\
   #         str(uFloat['estimate'][i].round(3)).ljust(27) +\
   #         str(uFloat['SR'][i].round(3)).ljust(30) +\
   #         str(uFloat['closure'][i].round(3)) + "\n")


# Efficiency plots
for plot in plots:
   ratios[plot][sample] =  divideHists(finalHists['tight'][plot][sample], finalHists['loose'][plot][sample])
   ratios[plot][sample].SetName("ratio_%s_%s"%(plot, sample))

if fakeRateMeasurement == "data-EWK":
   ratios['pt'][sample].SetTitle( "%ss: Tight to Loose Ratio for Data Sample (Prompt Subtracted) ; %s p_{T} / GeV ; Ratio"%(lepton, lepton))
   ratios['eta'][sample].SetTitle("%ss: Tight to Loose Ratio for Data Sample (Prompt Subtracted) ; %s |#eta| ; Ratio"%(lepton, lepton))
   if do2D: ratios['2D'][sample].SetTitle("{lep}s: Tight to Loose Ratio for Data Sample (Prompt Subtracted) ; {lep} p_{{T}}; {lep} |#eta|".format(lep = lepton))
elif fakeRateMeasurement == "MC-EWK":
   ratios['pt'][sample].SetTitle( "%ss: Tight to Loose Ratio for MC Samples (Prompt Subtracted) ; %s p_{T} / GeV ; Ratio"%(lepton, lepton))
   ratios['eta'][sample].SetTitle("%ss: Tight to Loose Ratio for MC Samples (Prompt Subtracted) ; %s |#eta| ; Ratio"%(lepton, lepton))
   if do2D: ratios['2D'][sample].SetTitle("{lep}s: Tight to Loose Ratio for MC Samples (Prompt Subtracted) ; {lep} p_{{T}}; {lep} |#eta|".format(lep = lepton))
elif fakeRateMeasurement == "MC":
   ratios['pt'][sample].SetTitle( "%ss: Tight to Loose Ratio for MC Samples (Fakes) ; %s p_{T} / GeV ; Ratio"%(lepton, lepton))
   ratios['eta'][sample].SetTitle("%ss: Tight to Loose Ratio for MC Samples (Fakes) ; %s |#eta| ; Ratio"%(lepton, lepton))
   if do2D: ratios['2D'][sample].SetTitle("{lep}s: Tight to Loose Ratio for MC Samples (Fakes) ; {lep} p_{{T}}; {lep} |#eta|".format(lep = lepton))
else:
   ratios['pt'][sample].SetTitle( "%ss: Tight to Loose Ratio for %s Sample ; %s p_{T} / GeV ; Ratio"%(lepton, samples[sample].name, lepton))
   ratios['eta'][sample].SetTitle("%ss: Tight to Loose Ratio for %s Sample ; %s |#eta| ; Ratio"%(lepton, samples[sample].name, lepton))
   if do2D: ratios['2D'][sample].SetTitle("{lep}s: Tight to Loose Ratio for {} Sample ; {lep} p_{{T}}; {lep} |#eta|".format(samples[sample].name, lep = lepton))

###############################################################################################################################################################################

#####Canvas 1#####

c1 = ROOT.TCanvas("c1", "Canvas 1", 1200, 1700)
c1.Divide(1,2)

c1.cd(1)
   
finalHists['loose']['pt'][sample].GetXaxis().SetTitle("%s p_{T} / GeV"%lepton)
finalHists['loose']['pt'][sample].SetFillColor(ROOT.kViolet+10)
#finalHists['loose']['pt'][sample].SetMinimum(1)
#finalHists['loose']['pt'][sample].SetMaximum(1000)
finalHists['loose']['pt'][sample].Draw("hist")

#alignStats(finalHists['loose']['pt'][sample])

finalHists['tight']['pt'][sample].SetFillColor(ROOT.kRed+1)
finalHists['tight']['pt'][sample].SetFillColorAlpha(finalHists['tight']['pt'][sample].GetFillColor(), 0.8)
finalHists['tight']['pt'][sample].Draw("histsame")
 
if logy: ROOT.gPad.SetLogy()

ROOT.gPad.Modified()
ROOT.gPad.Update()

l1 = makeLegend2()
l1 = ROOT.TLegend()
l1.AddEntry("loose_pt_%s"%sample, "Loose", "F")
l1.AddEntry("tight_pt_%s"%sample, "Tight", "F")
l1.Draw()

alignLegend(l1, y1=0.5, y2=0.65)

#####

# Efficiency

c1.cd(2)

ratios['pt'][sample].Draw("P")

#setupEffPlot(ratios['pt'][sample])
ratios['pt'][sample].SetMinimum(0)
ratios['pt'][sample].SetMaximum(1.0)

#ratios['pt'][sample].GetPaintedGraph().SetMinimum(0)
#ratios['pt'][sample].GetPaintedGraph().SetMaximum(0.6)
#ratios['pt'][sample].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)

#Colours
ratios['pt'][sample].SetMarkerColor(ROOT.kGreen+3)

ROOT.gPad.Modified()
ROOT.gPad.Update()

#l2 = makeLegend2()
#l2.AddEntry("ratio_%s_pt"%sample, "Veto", "P")
#l2.Draw()

c1.Modified()
c1.Update()

#####Canvas 2######

c2 = ROOT.TCanvas("c2", "Canvas 2", 1200, 1700)
c2.Divide(1,2)

c2.cd(1)

finalHists['loose']['eta'][sample].GetXaxis().SetTitle("%s |#eta| "%(lepton))
finalHists['loose']['eta'][sample].SetFillColor(ROOT.kViolet+10)
#finalHists['loose']['eta'][sample].SetMinimum(1)
#finalHists['loose']['eta'][sample].SetMaximum(1000)
finalHists['loose']['eta'][sample].Draw("hist")

#alignStats(finalHists['loose']['eta'][sample])#, y1=0.4, y2=0.6)

finalHists['tight']['eta'][sample].SetFillColor(ROOT.kRed+1)
finalHists['tight']['eta'][sample].SetFillColorAlpha(finalHists['tight']['eta'][sample].GetFillColor(), 0.8)
finalHists['tight']['eta'][sample].Draw("histsame")
   
if logy: ROOT.gPad.SetLogy()

ROOT.gPad.Modified()
ROOT.gPad.Update()

l2 = ROOT.TLegend()
l2.AddEntry("loose_eta_%s"%sample, "Loose", "F")
l2.AddEntry("tight_eta_%s"%sample, "Tight", "F")
l2.Draw()

alignLegend(l2, y1=0.5, y2=0.65)

#####

c2.cd(2)

ratios['eta'][sample].Draw("P")

ratios['eta'][sample].SetMinimum(0)
ratios['eta'][sample].SetMaximum(0.6)

#setupEffPlot(ratios['eta'][sample])
#ratios['eta'][sample].GetPaintedGraph().SetMinimum(0)
#ratios['eta'][sample].GetPaintedGraph().SetMaximum(0.6)
#ratios['eta'][sample].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)

#Colours
ratios['eta'][sample].SetMarkerColor(ROOT.kGreen+3)

ROOT.gPad.Modified()
ROOT.gPad.Update()

#l3 = makeLegend2()
#l3.AddEntry("ratio_%s_eta"%sample, "Veto", "P")
#l3.Draw()

c2.Modified()
c2.Update()

if do2D:
   finalHists['loose']['2D'][sample].GetXaxis().SetTitle("%s p_{T}"%lepton)
   finalHists['loose']['2D'][sample].GetYaxis().SetTitle("%s |#eta|"%lepton)
   #finalHists['loose']['2D'][sample].GetZaxis().SetRangeUser(0, 4)
   #alignStats(finalHists['loose']['2D'][sample])
   
   finalHists['tight']['2D'][sample].GetXaxis().SetTitle("%s p_{T}"%lepton)
   finalHists['tight']['2D'][sample].GetYaxis().SetTitle("%s |#eta|"%lepton)
   
   ratios['2D'][sample].SetMarkerSize(0.8)
   
   #####Canvas 3#####
   
   c3 = ROOT.TCanvas("c3", "Canvas 3", 1800, 1500)
   ratios['2D'][sample].Draw("COLZ TEXTE89") #CONT1-5 #plots the graph with axes and points
   #ratios['2D'][sample].GetPaintedGraph().GetXaxis().SetTitle("%s p_{T}"%lepton)
   #ratios['2D'][sample].GetPaintedGraph().GetYaxis().SetTitle("%s |#eta|"%lepton)
   #ratios['2D'][sample].SetMinimum(0.8)
   #ratios['2D'][sample].SetMaximum(5)
   #ratios['2D'][sample].GetZaxis().SetRangeUser(0.8,1.2)
   
   #alignStats(ratios['2D'][sample])
   
   #if logy: ROOT.gPad.SetLogz()
   c3.Modified()
   c3.Update()
   
   #####Canvas 4#####
   
   c4 = ROOT.TCanvas("c4", "Canvas 4", 1800, 1500)
   c4.Divide(1,2)
   
   c4.cd(1)
   finalHists['tight']['2D'][sample].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
   if logy: ROOT.gPad.SetLogz()
   
   c4.cd(2)
   finalHists['loose']['2D'][sample].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
   if logy: ROOT.gPad.SetLogz()
   c4.Modified()
   c4.Update()

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   c1.SaveAs("%s/FakeRate_TightToLoose_lepPt%s.png"%(savedir, suffix))
   c1.SaveAs("%s/pdf/FakeRate_TightToLoose_lepPt%s.pdf"%(savedir, suffix))
   c1.SaveAs("%s/root/FakeRate_TightToLoose_lepPt%s.root"%(savedir, suffix))
   
   c2.SaveAs("%s/FakeRate_TightToLoose_lepEta%s.png"%(savedir, suffix))
   c2.SaveAs("%s/pdf/FakeRate_TightToLoose_lepEta%s.pdf"%(savedir, suffix))
   c2.SaveAs("%s/root/FakeRate_TightToLoose_lepEta%s.root"%(savedir, suffix))

   if do2D:   
      c3.SaveAs("%s/FakeRate_TightToLoose_2D_Ratio%s.png"%(savedir, suffix))
      c3.SaveAs("%s/pdf/FakeRate_TightToLoose_2D_Ratio%s.pdf"%(savedir, suffix))
      c3.SaveAs("%s/root/FakeRate_TightToLoose_2D_Ratio%s.root"%(savedir, suffix))
      
      c4.SaveAs("%s/FakeRate_TightToLoose_2D_distributions%s.png"%(savedir, suffix))
      c4.SaveAs("%s/pdf/FakeRate_TightToLoose_2D_distributions%s.pdf"%(savedir, suffix))
      c4.SaveAs("%s/root/FakeRate_TightToLoose_2D_distributions%s.root"%(savedir, suffix))

   if fakeRateMeasurement and "measurement" in region:
      c1.SaveAs("%s/FakeRate_TightToLoose_lepPt%s.root"%(resultsDir, suffix))
      c2.SaveAs("%s/FakeRate_TightToLoose_lepEta%s.root"%(resultsDir, suffix))
      if do2D: c3.SaveAs("%s/FakeRate_TightToLoose_2D_Ratio%s.root"%(resultsDir, suffix))
