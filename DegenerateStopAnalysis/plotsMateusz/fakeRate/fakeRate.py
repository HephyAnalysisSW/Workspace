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

if lep == "mu":
   lepTag = "lowpt"
else:
   lepTag = "def"

if varBins: do2D = False #NOTE: still under development

fakeInfo = fakeInfo(script, vars(args))

lepton =      fakeInfo['lepton']
samplesList = fakeInfo['samplesList']
samples =     fakeInfo['samples']
dataSample =  fakeInfo['dataSample']
selection =   fakeInfo['selection']
bins =        fakeInfo['bins']

if save:
   savedir = fakeInfo['savedir']
   saveTag = fakeInfo['saveTag']
   suffix =  fakeInfo['suffix']

   if fakeRateMeasurement:
      resultsDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate"
      resultsDir += "/" + saveTag
      resultsDir += "/%s/TL_%s"%(region, fakeRateMeasurement)
      
      if not varBins: resultsDir += "/fixedBins"
      else:           resultsDir += "/varBins"
      
      makeDir(resultsDir)

index = selection['MC']['loose']['lepIndex1'] #loose index

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
   selection[sampType]['match'] = "(%s == %s)"%(selection[sampType]['loose']['lepIndex1'], selection[sampType]['tight']['lepIndex1'])
  
   # tight definition
   for x in ['total', 'prompt', 'fake']:
      if "measurement2" in region: 
         selList['tight'][x].append(selection[sampType]['match']) 
      elif "measurement1" in region:
         selList['tight'][x] = ["nLepGood_{lep}_{lt} > 0".format(lep = lep, lt = lepTag)] 
      
      selList['tight'][x].extend(selList['loose'][x][:])
 
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
               hists[hist][WP][plot][samp] = makeHist(samples[samp].tree, variables[plot], cutStr[WP][hist], bins[plot][0], bins[plot][1], bins[plot][2], addOverFlowBin = 'upper')
            else: 
               hists[hist][WP][plot][samp] = makeHistVarBins(samples[samp].tree, variables[plot],  cutStr[WP][hist], bins[plot],  variableBinning = (varBins, bins[plot][1]-bins[plot][0]), addOverFlowBin = 'upper')
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

         elif fakeRateMeasurement == "MC-EWK": # emulation of prompt subtraction from data using MC yields
            for samp in samplesList:
               if samp != 'qcd':
                  finalHists[WP][plot][sample].Add(hists['total'][WP][plot][samp]) # NOTE: Add total 
                  setErrSqrtN(finalHists[WP][plot][sample]) # setting error as sqrt N
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
         finalHists[WP][plot][sample] = hists['fake'][WP][plot][sample]
         finalHists[WP][plot][sample].SetTitle("%ss: Loose vs Tight comparison for %s Sample"%(lepton, samples[sample].name))
   
      if do2D: 
         finalHists[WP]['2D'][sample] = hists['fake'][WP]['2D'][sample]
         finalHists[WP]['2D'][sample].SetTitle("%ss: %s p_{T} vs |#eta| Distribution in %s Sample"%(lepton, WP, samples[sample].name))

# Yields
if doYields and fakeRateMeasurement:

   refHist = finalHists['loose']['pt'][fakeRateMeasurement]   

   n = refHist.GetNbinsX()

   value =  {'loose':{}, 'tight':{}}
   error =  {'loose':{}, 'tight':{}}
   uFloat = {'loose':{}, 'tight':{}, 'ratio':{}}
   uFloat_ylds = {'loose':{}, 'tight':{}, 'ratio':{}}

   w1 = refHist.GetBinWidth(1)

   for i in range(n):
      i += 1
      a = int(refHist.GetBinLowEdge(i))
      w = int(refHist.GetBinWidth(i))

      for x in value.keys():
         value[x][i] = finalHists[x]['pt'][fakeRateMeasurement].GetBinContent(i)
         error[x][i] = finalHists[x]['pt'][fakeRateMeasurement].GetBinError(i)
         uFloat[x][i] = u_float.u_float(value[x][i], error[x][i])

         uFloat_ylds[x][i] = uFloat[x][i]*w/w1

      if uFloat['loose'][i].val: 
         uFloat['ratio'][i] = uFloat['tight'][i]/uFloat['loose'][i]
         uFloat_ylds['ratio'][i] = uFloat['tight'][i]/uFloat['loose'][i]
      else:
         uFloat['ratio'][i] = u_float.u_float(0.,0.)
         uFloat_ylds['ratio'][i] = u_float.u_float(0.,0.)

      if verbose:
         print makeLine()
         print "T-L ratio in bin %s %s-%s GeV"%(str(i), str(a), str(a+w))
         print makeLine()
         print "Loose:",     uFloat['loose'][i].round(3)
         print "Tight:",     uFloat['tight'][i].round(3)
         print "T-L Ratio:", uFloat['ratio'][i].round(3)
         print makeLine()

      if save:
         if not os.path.isfile("%s/tightToLooseRatios%s.txt"%(savedir, suffix)):
            outfile = open("%s/tightToLooseRatios%s.txt"%(savedir, suffix), "w")
            outfile.write("T-L Ratio yields in %s region for the %s channel (%s)\n"%(region.title(), lepton, fakeRateMeasurement))
            title = "Bin (GeV)      |        Loose           |         Tight        |        T-L Ratio\n"
            outfile.write(title)

         with open("%s/tightToLooseRatios%s.txt"%(savedir, suffix), "a") as outfile:
            outfile.write("{}-{}".format(str(a), str(a+w)).ljust(15) + '|' +\
            str(uFloat['loose'][i].round(3)).ljust(25) + ' | ' +\
            str(uFloat['tight'][i].round(3)).ljust(25) + ' | ' +\
            str(uFloat['ratio'][i].round(3)) + "\n")
         
         if not os.path.isfile("%s/tightToLooseRatios_yields%s.txt"%(savedir, suffix)):
            outfile = open("%s/tightToLooseRatios_yields%s.txt"%(savedir, suffix), "w")
            outfile.write("T-L Ratio yields in %s region for the %s channel (%s)\n"%(region.title(), lepton, fakeRateMeasurement))
            title = "Bin (GeV)      |        Loose           |         Tight        |        T-L Ratio\n"
            outfile.write(title)

         with open("%s/tightToLooseRatios_yields%s.txt"%(savedir, suffix), "a") as outfile:
            outfile.write("{}-{}".format(str(a), str(a+w)).ljust(15) + '|' +\
            str(uFloat_ylds['loose'][i].round(3)).ljust(25) + ' | ' +\
            str(uFloat_ylds['tight'][i].round(3)).ljust(25) + ' | ' +\
            str(uFloat_ylds['ratio'][i].round(3)) + "\n")

         #Pickle results 
         pickleFile1 = open("%s/tightToLooseRatios%s.pkl"%(savedir,suffix), "w")
         pickle.dump(uFloat_ylds, pickleFile1)
         pickleFile1.close()
         
         pickleFile2 = open("%s/tightToLooseRatios%s.pkl"%(resultsDir,suffix), "w")
         pickle.dump(uFloat_ylds, pickleFile2)
         pickleFile2.close()

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
   #finalHists['loose'][x][sample].SetMaximum(1000)
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

#Save canvas
if save:
   canvs['pt'].SaveAs("%s/FakeRate_TightToLoose_lepPt%s.png"%(savedir, suffix))
   canvs['pt'].SaveAs("%s/pdf/FakeRate_TightToLoose_lepPt%s.pdf"%(savedir, suffix))
   canvs['pt'].SaveAs("%s/root/FakeRate_TightToLoose_lepPt%s.root"%(savedir, suffix))
   
   canvs['eta'].SaveAs("%s/FakeRate_TightToLoose_lepEta%s.png"%(savedir, suffix))
   canvs['eta'].SaveAs("%s/pdf/FakeRate_TightToLoose_lepEta%s.pdf"%(savedir, suffix))
   canvs['eta'].SaveAs("%s/root/FakeRate_TightToLoose_lepEta%s.root"%(savedir, suffix))

   if do2D:   
      canvs['2D'].SaveAs("%s/FakeRate_TightToLoose_2D_Ratio%s.png"%(savedir, suffix))
      canvs['2D'].SaveAs("%s/pdf/FakeRate_TightToLoose_2D_Ratio%s.pdf"%(savedir, suffix))
      canvs['2D'].SaveAs("%s/root/FakeRate_TightToLoose_2D_Ratio%s.root"%(savedir, suffix))
      
      canvs['2D_dist'].SaveAs("%s/FakeRate_TightToLoose_2D_distributions%s.png"%(savedir, suffix))
      canvs['2D_dist'].SaveAs("%s/pdf/FakeRate_TightToLoose_2D_distributions%s.pdf"%(savedir, suffix))
      canvs['2D_dist'].SaveAs("%s/root/FakeRate_TightToLoose_2D_distributions%s.root"%(savedir, suffix))

   if fakeRateMeasurement and "measurement" in region:
      canvs['pt'].SaveAs("%s/FakeRate_TightToLoose_lepPt%s.root"%(resultsDir, suffix))
      canvs['eta'].SaveAs("%s/FakeRate_TightToLoose_lepEta%s.root"%(resultsDir, suffix))
      if do2D: canvs['2D'].SaveAs("%s/FakeRate_TightToLoose_2D_Ratio%s.root"%(resultsDir, suffix))
