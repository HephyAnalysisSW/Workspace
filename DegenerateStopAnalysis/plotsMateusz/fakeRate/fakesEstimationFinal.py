# fakesEstimationFinal.py
# Application of fake rate to estimate fake background contribution 
# Mateusz Zarucki 2017

import os
from fakeInfo import *

script = os.path.basename(__file__) #sys.argv[0]

#Arguments
args = fakeParser(script)

lep = args.lep
region = args.region
measurementType = args.measurementType
VR = args.VR
addMRsys = args.addMRsys
doClosure = args.doClosure
mergeHighPtBins = args.mergeHighPtBins
doPlots = args.doPlots
doYields = args.doYields
getData = args.getData
varBins = args.varBins
logy = args.logy
save = args.save
verbose = args.verbose

fakeInfo = fakeInfo(script, vars(args))

lepton =      fakeInfo['lepton']
samplesList = fakeInfo['samplesList']
samples =     fakeInfo['samples']
selection =   fakeInfo['selection']
bins =        fakeInfo['bins']
dataset =     fakeInfo['dataset']

regDefs = selection['regDefs']
   
looseNotTight = True

if doPlots:
   
   if save: 
      saveTag = fakeInfo['saveTag']
      etaBin =  fakeInfo['etaBin']
    
   # Root file with fake rate
   finalTag = "MR14"
   fakeRateFile = "tightToLooseRatios_%s_%s_stat.pkl"%(finalTag, measurementType)
   fakeRateDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/final/%s/%s/%s"%(saveTag, finalTag, fakeRateFile)
   TLratios = pickle.load(open(fakeRateDir, "r"))

   # if final estimate from data, adding systematics from MR
   if addMRsys:
      TLratios_sys = pickle.load(open(fakeRateDir.replace('stat', 'sys2'), "r"))
      for l in ['el', 'mu']:
         for ptBin in TLratios[l][etaBin]:
            if ptBin == "0_5" or ptBin == "0_3p5": continue
            if l == 'el' and ptBin == "ptVL": continue
            TLratios[l][etaBin][ptBin].sigma = sqrt(TLratios[l][etaBin][ptBin].sigma**2 + (TLratios_sys[etaBin][l]['proposed'][ptBin]*TLratios[l][etaBin][ptBin].val)**2) 

   if verbose:
      print makeLine()
      print "Using tight-to-loose ratio from", fakeRateDir
      print makeLine()

#Save
if save:
   baseDir = fakeInfo['baseDir']
   savedir = fakeInfo['savedir']
   suffix =  fakeInfo['suffix']

   if addMRsys:
      suffix += "_withMRsys"
   
   if mergeHighPtBins:
      suffix += "_mergedCRbins"
      
# SR/VR plotting for closure   
if 'data' in measurementType and VR not in ['EVR1', 'EVR2']:
   print makeLine()
   print "Warning - data closure should be in suitable VR. Skipping closure." 
   print makeLine()
   doClosure = False
 
index = {}
pt = {}
eta = {}
regionSel = {}

for WP in ['loose', 'tight']:
   index[WP] = selection[WP]['lepIndex1']
   pt[WP] = "LepGood_pt[%s]"%index[WP]
   eta[WP] = "abs(LepGood_eta[%s])"%index[WP]
   regionSel[WP] = selection[WP][region][samplesList[0]][0] #NOTE: application region only

# Signal region
regions = {'SR':{}, 'looseCR':{}}

if doClosure:
   regions['SR']['total'] =  [selection['tight']['cuts'], regDefs['regDef']] 
   regions['SR']['prompt'] = [selection['tight']['cuts'], regDefs['regDef'] + '_plus_prompt'] 
   regions['SR']['fake'] =   [selection['tight']['cuts'], regDefs['regDef'] + '_plus_fake'] 

regions['looseCR']['total'] =  [selection['loose']['cuts'], regDefs['regDef_notTight']] 
regions['looseCR']['prompt'] = [selection['loose']['cuts'], regDefs['regDef_notTight'] + '_plus_prompt']
regions['looseCR']['fake'] =   [selection['loose']['cuts'], regDefs['regDef_notTight'] + '_plus_fake']

if mergeHighPtBins:
   varBins2 = False
else:
   varBins2 = varBins

if doPlots:
   # Plots
   
   plotDict = {\
      "lepPt_loose":{'var':pt['loose'],   "bins":bins['pt'],  'decor':{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins2, bins['pt'][1]-bins['pt'][0])},
      "lepPt_tight":{'var':pt['tight'],   "bins":bins['pt'],  'decor':{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins2, bins['pt'][1]-bins['pt'][0])},
   }
    
   plotsDict = Plots(**plotDict)
   
   if logy: plotMin = 0.1
   else:    plotMin = 0
   
   plotList = {}
   plotList['loose'] = ['lepPt_loose']
   plotList['tight'] = ['lepPt_tight']
   
   fakePlots = {'SR':{}, 'looseCR':{}}
  
   if measurementType == "MC":
      plots =                           getPlots(samples, plotsDict, regions['looseCR']['fake'],   samplesList, plotList = plotList['loose'], addOverFlowBin='upper')
      fakePlots['looseCR']['fakes'] =  drawPlots(samples, plotsDict, regions['looseCR']['fake'],   samplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
   elif measurementType == "data-EWK": 
      plots =                           getPlots(samples, plotsDict, regions['looseCR']['total'],  samplesList, plotList = plotList['loose'], addOverFlowBin='upper')
      fakePlots['looseCR']['total'] =  drawPlots(samples, plotsDict, regions['looseCR']['total'],  samplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["dblind"], fom = "RATIO", fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
      
      MCsamplesList = samplesList[:]
      MCsamplesList.remove(dataset)   
      plots =                           getPlots(samples, plotsDict, regions['looseCR']['prompt'], MCsamplesList, plotList = plotList['loose'], addOverFlowBin='upper')
      fakePlots['looseCR']['prompt'] = drawPlots(samples, plotsDict, regions['looseCR']['prompt'], MCsamplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
   
   if doClosure: 
      if measurementType == "MC":
         plots =                           getPlots(samples, plotsDict, regions['SR']['fake'],   samplesList, plotList = plotList['tight'], addOverFlowBin='upper')
         fakePlots['SR']['fakes'] =       drawPlots(samples, plotsDict, regions['SR']['fake'],   samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
      elif measurementType == "data-EWK": 
         plots =                           getPlots(samples, plotsDict, regions['SR']['total'],  samplesList, plotList = plotList['tight'], addOverFlowBin='upper')
         fakePlots['SR']['total'] =       drawPlots(samples, plotsDict, regions['SR']['total'],  samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["dblind"], fom = "RATIO", fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
      
         plots =                           getPlots(samples, plotsDict, regions['SR']['prompt'], MCsamplesList, plotList = plotList['tight'], addOverFlowBin='upper')
         fakePlots['SR']['prompt'] =      drawPlots(samples, plotsDict, regions['SR']['prompt'], MCsamplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
   
   # Legend
   leg = copy.deepcopy(fakePlots['looseCR'][fakePlots['looseCR'].keys()[-1]]['legs'])
   latex = copy.deepcopy(fakePlots['looseCR'][fakePlots['looseCR'].keys()[-1]]['latexText'])

   if len(leg) > 2:
      leg = [leg[0], leg[1]]

   finalHists = {'looseCR':{}, 'SR':{}}

   # L(!T) CR
   if measurementType == "MC": # Fakes
      basePlot = 'fakes'
      finalHists['looseCR'][basePlot] = fakePlots['looseCR']['fakes']['stacks']['bkg']['lepPt_loose'].Clone()
      #finalHists['looseCR']['total'] =  looseCR_tot['stacks']['total']['lepPt_loose'].Clone()
      #finalHists['looseCR']['prompt'] = looseCR_prompt['stacks']['bkg']['lepPt_loose'].Clone()

      if doClosure:
         finalHists['SR'][basePlot] = fakePlots['SR']['fakes']['stacks']['bkg']['lepPt_tight'].Clone()
   
   elif measurementType == "data-EWK": # Data and prompt 
      basePlot = 'data-prompt'
      looseCR_tot =    copy.deepcopy(fakePlots['looseCR']['total'])
      looseCR_prompt = copy.deepcopy(fakePlots['looseCR']['prompt'])

      finalHists['looseCR'][basePlot] = looseCR_tot['hists'][dataset]['lepPt_loose'].Clone() # data-prompt
      finalHists['looseCR']['total'] =  looseCR_tot['hists'][dataset]['lepPt_loose'].Clone() # data
      finalHists['looseCR']['prompt'] = looseCR_prompt['stacks']['bkg']['lepPt_loose'].Clone() # prompt
      
      for samp in looseCR_prompt['hists']:
         finalHists['looseCR'][basePlot].Add(looseCR_prompt['hists'][samp]['lepPt_loose'], -1) # subtract prompt
      
      if doClosure:
         VR_tot =    copy.deepcopy(fakePlots['SR']['total'])
         VR_prompt = copy.deepcopy(fakePlots['SR']['prompt'])
         
         finalHists['SR'][basePlot] = VR_tot['hists'][dataset]['lepPt_tight'].Clone() # add data
         for samp in VR_prompt['hists']:
            finalHists['SR'][basePlot].Add(VR_prompt['hists'][samp]['lepPt_tight'], -1) # subtract prompt
    
   for plot in finalHists['looseCR'].keys(): 
      if type(finalHists['looseCR'][plot]) == ROOT.THStack: # Convert THStack into TH1
         finalHists['looseCR'][plot] = finalHists['looseCR'][plot].GetStack().Last().Clone() #NOTE: last stack in GetStack() array is the sum of all stacks
   
   # Multiplying L(!T) CR fakes with transfer factor
   finalHists['estimate'] = finalHists['looseCR'][basePlot].Clone() # start with L!T CR 
   
   n = finalHists['estimate'].GetNbinsX()
   
   #w1 = finalHists['estimate'][basePlot].GetBinWidth(1)

   TF = {}
   est = {}
   est_err = {}

   for i in range(n):
      i += 1
      a = finalHists['estimate'].GetBinLowEdge(i)
      w = finalHists['estimate'].GetBinWidth(i)
    
      TF = TLratios[lep][etaBin][binMaps[lep][str(i)]].val/(1-TLratios[lep][etaBin][binMaps[lep][str(i)]].val) #NOTE: evaluates to (TLratio/1-TLratio)
      TF_err = TLratios[lep][etaBin][binMaps[lep][str(i)]].sigma
 
      est[str(i)] = finalHists['estimate'].GetBinContent(i)*TF
      if TF and finalHists['estimate'].GetBinContent(i):
         est_err[str(i)] = est[str(i)]*sqrt(pow(finalHists['estimate'].GetBinError(i)/finalHists['estimate'].GetBinContent(i),2)+pow(TF_err/TF,2)) # adding TL ratio errors + loose CR stat. error 
      else:
         est_err[str(i)] = 0. 
 
      finalHists['estimate'].SetBinContent(i, est[str(i)])
      finalHists['estimate'].SetBinError(i, est_err[str(i)])
  
   finalHists['estimate'].SetName("fakesEstimate")
   finalHists['estimate'].SetMarkerStyle(20)
   finalHists['estimate'].SetMarkerColor(1)
   finalHists['estimate'].SetMarkerSize(0.9)
   finalHists['estimate'].SetLineWidth(2)
   
   ratioTitle1 = "#frac{#epsilon_{TL}}{(1 - #epsilon_{TL})}"
   
   #leg[-1].AddEntry(finalHists['estimate'], "Prediction", "LP")
   
   canvas = drawPlot(finalHists['looseCR'][basePlot], legend = leg, decor = plotsDict['lepPt_loose']['decor'], latexText = latex, ratio = (finalHists['estimate'], finalHists['looseCR'][basePlot]), ratioLimits = [0,0.7], ratioTitle = ratioTitle1, plotMin = plotMin)
   finalHists['estimate'].Draw("same")

   estKey = 'estimate'

   # Closure
   if doClosure:
      ratioTitle2 = "#frac{Pred. - Obs.}{Pred.}"
      if lep == "mu" and ('ab' in region or 'sr1c' in region):
         ratioLimits2 = [-4, 4]
      else: 
         ratioLimits2 = [-2, 2] 
      unityLine = False
      
      if mergeHighPtBins:

         estKey = 'estimate2'
   
         bins2 = fakeBinning(lep, varBins = varBins, mergeHighPtBins = mergeHighPtBins)
         binsCond = array('d', bins2['pt'])

         if type(finalHists['SR'][basePlot]) == ROOT.THStack:
            SR_rebinned = ROOT.THStack('SR_rebinned', 'SR_rebinned')
            SR_rebinned_hists = {}
            
            for samp in fakePlots['SR'][basePlot]['hists']:
               SR_rebinned_hists[samp] = fakePlots['SR'][basePlot]['hists'][samp]['lepPt_tight'].Clone()
               SR_rebinned_hists[samp] = SR_rebinned_hists[samp].Rebin(len(bins2['pt'])-1, "SR_rebinned_"+samp, binsCond)
               #SR_rebinned_hists[samp].Sumw2()
               SR_rebinned_hists[samp].Scale(SR_rebinned_hists[samp].GetBinWidth(1),"width")
               SR_rebinned.Add(SR_rebinned_hists[samp])

            finalHists['SR'][basePlot] = SR_rebinned 

         finalHists[estKey] = finalHists['estimate'].Clone()
         #finalHists[estKey].Sumw2()
         finalHists[estKey] = finalHists[estKey].Rebin(len(bins2['pt'])-1, "fakesEstimate_rebinned", binsCond)
         finalHists[estKey].Scale(finalHists[estKey].GetBinWidth(1),"width")
 
      if type(finalHists['SR'][basePlot]) == ROOT.THStack:
         closure = finalHists[estKey].Clone() - finalHists['SR'][basePlot].GetStack().Last().Clone() # Convert THStack into TH1
      else:
         closure = finalHists[estKey].Clone() - finalHists['SR'][basePlot]

      estimate_zeroErr = finalHists[estKey].Clone()
      setErrZero(estimate_zeroErr)
      closure.Divide(estimate_zeroErr)
      
      if measurementType == "MC": 
         ratioTitle2 = ratioTitle2.replace('Obs.', 'MC')

      canvas2 = drawPlot(finalHists['SR'][basePlot], legend = leg, decor = plotsDict['lepPt_tight']['decor'], latexText = latex, ratio = closure, ratioLimits = ratioLimits2, ratioTitle = ratioTitle2, unity = unityLine, plotMin = plotMin)
      finalHists[estKey].Draw("same")
      
      finalHists['closure'] = canvas2['ratio']

   if doYields:
   
      hists =  ['looseCR', estKey]
   
      if doClosure:
         hists.extend(['SR', 'closure'])
 
      value =    {'TLratio':{}, 'looseCR':{'total':{}, 'prompt':{}, basePlot:{}}, estKey:{}, 'SR':{'total':{}, 'prompt':{}, basePlot:{}}, 'closure':{}}
      error =    {'TLratio':{}, 'looseCR':{'total':{}, 'prompt':{}, basePlot:{}}, estKey:{}, 'SR':{'total':{}, 'prompt':{}, basePlot:{}}, 'closure':{}}
      uFloat =   {'TLratio':{}, 'looseCR':{'total':{}, 'prompt':{}, basePlot:{}}, estKey:{}, 'SR':{'total':{}, 'prompt':{}, basePlot:{}}, 'closure':{}}
      histCont = {'TLratio':{}, 'looseCR':{'total':{}, 'prompt':{}, basePlot:{}}, estKey:{}, 'SR':{'total':{}, 'prompt':{}, basePlot:{}}, 'closure':{}}
      histYlds = {'TLratio':{}, 'looseCR':{'total':{}, 'prompt':{}, basePlot:{}}, estKey:{}, 'SR':{'total':{}, 'prompt':{}, basePlot:{}}, 'closure':{}}
      uFloat_ylds =            {'looseCR':{'total':{}, 'prompt':{}, basePlot:{}}, estKey:{}, 'SR':{'total':{}, 'prompt':{}, basePlot:{}}}
   
      n = finalHists[estKey].GetNbinsX()
      w1 = finalHists[estKey].GetBinWidth(1)

      for i in range(n):
         i += 1
        
         for x in hists:
            if x in ['looseCR', 'SR']: # sub-hists
               for z in finalHists[x].keys():
                  plot = z
                  if type(finalHists[x][plot]) == ROOT.THStack:
                     plot += "_hist"
                     finalHists[x][plot] = finalHists[x][z].GetStack().Last().Clone() 

                  histCont[x][z] = getHistContents(finalHists[x][plot], varBinsYield = False)
                  if z == basePlot:
                     histYlds[x][z] = getHistContents(finalHists[x][plot], varBinsYield = varBins)
                  else:
                     histYlds[x][z] = getHistContents(finalHists[x][plot], varBinsYield = varBins2)

                  uFloat[x][z] =      histCont[x][z][0]
                  uFloat_ylds[x][z] = histYlds[x][z][0]

                  a = histCont[x][z][1]
                  w = histCont[x][z][2]

            else: 
               plot = x
               if type(finalHists[x]) == ROOT.THStack:
                  plot += "_hist"
                  finalHists[plot] = finalHists[x].GetStack().Last().Clone() 

               histCont[x] = getHistContents(finalHists[plot], varBinsYield = False)
               uFloat[x] = histCont[x][0]

               a = histCont[x][1]
               w = histCont[x][2]

               if x != 'closure':
                  if x == estKey:
                     histYlds[x] = getHistContents(finalHists[x], varBinsYield = varBins)
                  else: 
                     histYlds[x] = getHistContents(finalHists[x], varBinsYield = varBins2)
                  uFloat_ylds[x] = histYlds[x][0]

         if verbose:
            print makeLine()
            print "Fake rate estimation numbers in bin %s %s-%s GeV"%(str(i), str(a[i]), str(a[i]+w[i])) 
            print makeLine()
            print "T-L Ratio:",           TLratios[lep][etaBin][binMaps[lep][str(i)]].round(3)
            
            for plot in uFloat['looseCR'].keys(): 
               print "L(!T) CR (%s):"%plot,  uFloat['looseCR'][plot][i].round(3) 
            print "Estimate:",               uFloat[estKey][i].round(3) 
            print "Estimate (x-check):",    (TLratios[lep][etaBin][binMaps[lep][str(i)]]/(u_float.u_float(1,0) - TLratios[lep][etaBin][binMaps[lep][str(i)]])*uFloat['looseCR'][basePlot][i]).round(3).val
            print makeLine()
         
            print makeLine()
            print "Fake rate estimation yields in bin %s %s-%s GeV"%(str(i), str(a), str(a+w)) 
            print makeLine()
            for plot in uFloat['looseCR'].keys(): 
               print "L(!T) CR (%s):"%plot,  uFloat_ylds['looseCR'][plot][i].round(3) 
            print "Estimate:",               uFloat_ylds[estKey][i].round(3) 
            print "Estimate (x-check):",    (TLratios[lep][etaBin][binMaps[lep][str(i)]]/(u_float.u_float(1,0) - TLratios[lep][etaBin][binMaps[lep][str(i)]])*uFloat_ylds['looseCR'][basePlot][i]).round(3)
            
            if doClosure:
               print "SR (%s):"%basePlot,       uFloat_ylds['SR'][basePlot][i].round(3)
               print "SR (%s):"%basePlot,       uFloat['SR'][basePlot][i].round(3)
               
               print "Closure:", uFloat['closure'][i].round(3) 
               if uFloat[estKey][i].val:
                  print "Closure (x-check):", ((uFloat[estKey][i] - uFloat['SR'][basePlot][i])/uFloat[estKey][i]).round(3).val 
               print makeLine()
         
         if save:
            title1 = "Estimation of fakes in %s region for the %s channel (Yields) using %s FR\n"%(region.title(), lepton, measurementType)
            if 'prompt' in uFloat_ylds['looseCR'].keys() and uFloat_ylds['looseCR']['prompt']:
               title2 = "Bin (GeV)       |   T-L Ratio         |        Loose CR (total)      |     Loose CR (prompt)      |         Loose CR (%s)      |       Estimate    "%basePlot
            else:
               title2 = "Bin (GeV)       |   T-L Ratio         |        Loose CR (%s)      |       Estimate    "%basePlot
            if doClosure: 
               title2 += "       |      SR (%s)         |        Closure (Standard)\n"%basePlot
            else:   
               title2 += "\n"
               
            if looseNotTight: title2 = title2.replace("Loose", "L!T")
 
            #if not os.path.isfile("%s/fakesEstimationFinal%s.txt"%(savedir, suffix)):
            #   outfile = open("%s/fakesEstimationFinal%s.txt"%(savedir, suffix), "w")
            #   outfile.write(title1.replace('Yields', 'Bin Content'))
            #   outfile.write(title2)
   
            #with open("%s/fakesEstimationFinal%s.txt"%(savedir, suffix), "a") as outfile:
            #   outfile.write("{}-{}".format(str(a), str(a+w)).ljust(15) + ' | ' +\
            #   str(TLratios[lep][etaBin][binMaps[lep][str(i)]].round(3)).ljust(22) + ' | ' +\
            #   str(uFloat['looseCR']['total'][i].round(3)).ljust(22)  + ' | ' +\
            #   str(uFloat['looseCR']['prompt'][i].round(3)).ljust(22)  + ' | ' +\
            #   str(uFloat['looseCR'][basePlot][i].round(3)).ljust(22)  + ' | ' +\
            #   str(uFloat[estKey][i].round(3)).ljust(25))
            #   if doClosure:
            #      outfile.write(' | ' +\
            #         str(uFloat['SR'][basePlot][i].round(3)).ljust(25) + ' | ' +\
            #         str(uFloat['closure'][i].round(3)).ljust(25) + '\n')
            #   else:
            #      outfile.write('\n')
            
            if not os.path.isfile("%s/fakesEstimationFinal_yields%s.txt"%(savedir, suffix)):
               outfile = open("%s/fakesEstimationFinal_yields%s.txt"%(savedir, suffix), "w")
               outfile.write(title1)
               outfile.write(title2)
  
            with open("%s/fakesEstimationFinal_yields%s.txt"%(savedir, suffix), "a") as outfile:
               outfile.write("{}-{}".format(str(a[i]), str(a[i]+w[i])).ljust(15) + ' | ' +\
               str(TLratios[lep][etaBin][binMaps[lep][str(i)]].round(3)).ljust(22) + ' | ')
               if uFloat_ylds['looseCR']['prompt']:
                  outfile.write(str(uFloat_ylds['looseCR']['total'][i].round(3)).ljust(22)  + ' | ')
                  outfile.write(str(uFloat_ylds['looseCR']['prompt'][i].round(3)).ljust(22)  + ' | ')
               outfile.write(str(uFloat_ylds['looseCR'][basePlot][i].round(3)).ljust(22)  + ' | ')
               outfile.write(str(uFloat_ylds[estKey][i].round(3)).ljust(25))
               if doClosure:
                  outfile.write(' | ' +\
                     str(uFloat_ylds['SR'][basePlot][i].round(3)).ljust(25) + ' | ' +\
                     str(uFloat['closure'][i].round(3)).ljust(25) + '\n')
               else:
                  outfile.write('\n')
  
            #Pickle results 
            #pickleFile1 = open("%s/fakesEstimationFinal%s.pkl"%(savedir,suffix), "w")
            #pickle.dump(uFloat, pickleFile1)
            #pickleFile1.close()
            
            pickleFile2 = open("%s/fakesEstimationFinal_yields%s.pkl"%(savedir,suffix), "w")
            pickle.dump(uFloat_ylds, pickleFile2)
            pickleFile2.close()

   if save:
      # Loose CR
      for p in fakePlots['looseCR']: 
         for canv in fakePlots['looseCR'][p]['canvs']:
            fakePlots['looseCR'][p]['canvs'][canv][0].SaveAs("%s/looseCR%s_%s_%s.png"%(savedir, suffix, p, canv))
            fakePlots['looseCR'][p]['canvs'][canv][0].SaveAs("%s/root/looseCR%s_%s_%s.root"%(savedir, suffix, p, canv))
            fakePlots['looseCR'][p]['canvs'][canv][0].SaveAs("%s/pdf/looseCR%s_%s_%s.pdf"%(savedir, suffix, p, canv))
     
      # SR/VR 
      if VR: tightPlotTitle = VR
      else:  tightPlotTitle = 'SR'

      for p in fakePlots['SR']: 
         for canv in fakePlots['SR'][p]['canvs']:
            fakePlots['SR'][p]['canvs'][canv][0].SaveAs("%s/%s%s_%s_%s.png"%(savedir, tightPlotTitle, suffix, p, canv))
            fakePlots['SR'][p]['canvs'][canv][0].SaveAs("%s/root/%s%s_%s_%s.root"%(savedir, tightPlotTitle, suffix, p, canv))
            fakePlots['SR'][p]['canvs'][canv][0].SaveAs("%s/pdf/%s%s_%s_%s.pdf"%(savedir, tightPlotTitle, suffix, p, canv))
      
      canvas['canvs'][0].SaveAs("%s/fakesEstimate%s.png"%(savedir, suffix))
      canvas['canvs'][0].SaveAs("%s/root/fakesEstimate%s.root"%(savedir, suffix))
      canvas['canvs'][0].SaveAs("%s/pdf/fakesEstimate%s.pdf"%(savedir, suffix))
  
      if doClosure:
         canvas2['canvs'][0].SaveAs("%s/closure%s.png"%(savedir, suffix))
         canvas2['canvs'][0].SaveAs("%s/root/closure%s.root"%(savedir, suffix))
         canvas2['canvs'][0].SaveAs("%s/pdf/closure%s.pdf"%(savedir, suffix))

## Yields 
#if doYields:
#   yields = {'SR':{}, 'looseCR':{}}
#
#   for x in yields: 
#      yields[x]['total'] =  Yields(samples, samplesList, cutInst = None, cuts = regions[x]['total'],  cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
#      yields[x]['prompt'] = Yields(samples, samplesList, cutInst = None, cuts = regions[x]['prompt'], cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
#      yields[x]['fake'] =   Yields(samples, samplesList, cutInst = None, cuts = regions[x]['fake'],   cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
#
#   if save:
#      if not os.path.isfile("%s/fakeYields%s.txt"%(savedir, suffix)):
#         outfile = open("%s/fakeYields%s.txt"%(savedir, suffix), "w")
#         outfile.write("Estimation of fakes in %s region for the %s channel \n"%(region.title(), lepton))
#         title = "Sample     |   Loose CR: Total      |    Loose CR: Prompt         |    Loose CR: Fakes         |    SR: Total          |     SR: Prompt           |     SR: Fakes\n"
#         if looseNotTight: title = title.replace("Loose", "L!T") 
#         outfile.write(title)
#
#      yieldsList = samplesList[:]
#      yieldsList.append('Total')
#
#      with open("%s/fakeYields%s.txt"%(savedir, suffix), "a") as outfile:
#        for samp in yieldsList:
#            outfile.write(samp.ljust(12) + ' | ' +\
#            str(yields['looseCR']['total'].yieldDictFull[samp][regDefs['regDef'] + '_notTight'].round(2)).ljust(24) + ' | '  +\
#            str(yields['looseCR']['prompt'].yieldDictFull[samp][regDefs['regDef' + '_notTight] + _prompt'].round(2)).ljust(24) + ' | ' +\
#            str(yields['looseCR']['fake'].yieldDictFull[samp][regDefs['regDef' + '_notTight] + _fake'].round(2)).ljust(24) + ' | ' +\
#            str(yields['SR']['total'].yieldDictFull[samp][regDefs['regDef']].round(2)).ljust(24) + ' | ' +\
#            str(yields['SR']['prompt'].yieldDictFull[samp][regDefs['regDef'] + '_prompt'].round(2)).ljust(24) + ' | ' +\
#            str(yields['SR']['fake'].yieldDictFull[samp][regDefs['regDef'] + '_fake'].round(2)) + "\n")

