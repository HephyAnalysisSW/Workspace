# fakesClosure.py
# Application of fake rate to estimate fake background contribution and closure 
# Mateusz Zarucki 2017

import os
from fakeInfo import *

script = os.path.basename(__file__) #sys.argv[0]

#Arguments
args = fakeParser(script)

lep = args.lep
region = args.region
measurementRegion = args.measurementRegion
measurementType = args.measurementType
closureDef = args.closureDef
looseNotTight = args.looseNotTight
doPlots = args.doPlots
doYields = args.doYields
doControlPlots = args.doControlPlots
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

regDefs = selection['regDefs']

if doPlots:
   
   if save: 
      saveTag = fakeInfo['saveTag']
      etaBin =  fakeInfo['etaBin']
      binDir =  fakeInfo['binDir']
   
      if not varBins: binDir += "/fixedBins"
      else:           binDir += "/varBins"
    
   # Root file with fake rate
   fakeRateDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate"
   fakeRateDir += "/" + saveTag 
   fakeRateDir += "/" + measurementRegion
   fakeRateDir += binDir
   fakeRateDir += "/" + etaBin
   
   fakeRateFile = "FakeRate_TightToLoose_lepPt_%s_%s_%s.root"%(lep, measurementRegion, measurementType)
 
   if verbose:
      print makeLine()
      print "Using tight-to-loose ratio from ", fakeRateDir + "/" + fakeRateFile
      print makeLine()
   
   f1 = ROOT.TFile(fakeRateDir + "/" + fakeRateFile)
   
   TLratio = {}
  
   for var in ['pt']:#, 'eta']: 
      TLratio[var] = f1.Get("canv_%s"%var).GetPrimitive("canv_%s_2"%var).GetPrimitive("ratio_%s_%s"%(var, measurementType))

#Save
if save:
   savedir = fakeInfo['savedir']
   suffix =  fakeInfo['suffix']
   
index = {}
pt = {}
eta = {}
mt = {}
hybIso = {}
regionSel = {}

for WP in ['loose', 'tight']:
   index[WP] = selection[WP]['lepIndex1']
   pt[WP] = "LepGood_pt[%s]"%index[WP]
   mt[WP] = "LepGood_mt[%s]"%index[WP]
   eta[WP] = "abs(LepGood_eta[%s])"%index[WP]
   hybIso[WP] = "(LepGood_relIso03[{ind}]*min(LepGood_pt[{ind}], 25))".format(ind = index[WP])
   regionSel[WP] = selection[WP][region][samplesList[0]][0] #NOTE: application region only

# Signal region
regions = {'SR':{}, 'looseCR':{}}

regions['SR']['total'] =  [selection['tight']['cuts'], regDefs['regDef']] 
regions['SR']['prompt'] = [selection['tight']['cuts'], regDefs['regDef'] + '_plus_prompt'] 
regions['SR']['fake'] =   [selection['tight']['cuts'], regDefs['regDef'] + '_plus_fake'] 

# Loose (not-Tight) CR
if looseNotTight:
   notTight = "_notTight"
else:
   notTight = ""

regions['looseCR']['total'] =  [selection['loose']['cuts'], regDefs['regDef' + notTight]] 
regions['looseCR']['prompt'] = [selection['loose']['cuts'], regDefs['regDef' + notTight] + '_plus_prompt'] 
regions['looseCR']['fake'] =   [selection['loose']['cuts'], regDefs['regDef' + notTight] + '_plus_fake'] 

# Yields 
if doYields:
   yields = {'SR':{}, 'looseCR':{}}

   for x in yields: 
      yields[x]['total'] =  Yields(samples, samplesList, cutInst = None, cuts = regions[x]['total'],  cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
      yields[x]['prompt'] = Yields(samples, samplesList, cutInst = None, cuts = regions[x]['prompt'], cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
      yields[x]['fake'] =   Yields(samples, samplesList, cutInst = None, cuts = regions[x]['fake'],   cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)

   if save:
      if not os.path.isfile("%s/fakeYields%s.txt"%(savedir, suffix)):
         outfile = open("%s/fakeYields%s.txt"%(savedir, suffix), "w")
         outfile.write("Estimation of fakes in %s region for the %s channel \n"%(region.title(), lepton))
         title = "Sample     |   Loose CR: Total      |    Loose CR: Prompt         |    Loose CR: Fakes         |    SR: Total          |     SR: Prompt           |     SR: Fakes\n"
         if looseNotTight: title = title.replace("Loose", "L!T") 
         outfile.write(title)

      yieldsList = samplesList[:]
      yieldsList.append('Total')

      with open("%s/fakeYields%s.txt"%(savedir, suffix), "a") as outfile:
        for samp in yieldsList:
            outfile.write(samp.ljust(12) + ' | ' +\
            str(yields['looseCR']['total'].yieldDictFull[samp][regDefs['regDef' + notTight]].round(2)).ljust(24) + ' | '  +\
            str(yields['looseCR']['prompt'].yieldDictFull[samp][regDefs['regDef' + notTight] + '_plus_prompt'].round(2)).ljust(24) + ' | ' +\
            str(yields['looseCR']['fake'].yieldDictFull[samp][regDefs['regDef' + notTight] + '_plus_fake'].round(2)).ljust(24) + ' | ' +\
            str(yields['SR']['total'].yieldDictFull[samp][regDefs['regDef']].round(2)).ljust(24) + ' | ' +\
            str(yields['SR']['prompt'].yieldDictFull[samp][regDefs['regDef'] + '_plus_prompt'].round(2)).ljust(24) + ' | ' +\
            str(yields['SR']['fake'].yieldDictFull[samp][regDefs['regDef'] + '_plus_fake'].round(2)) + "\n")

if doPlots:
   # Plots
   bins = fakeBinning(lep, varBins = varBins)
   
   plotDict = {\
      "lepPt_loose":{'var':pt['loose'],   "bins":bins['pt'],  'decor':{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])},
      "lepPt_tight":{'var':pt['tight'],   "bins":bins['pt'],  'decor':{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])},
      "lepEta_loose":{'var':eta['loose'], "bins":bins['eta'], 'decor':{"title": "Lepton |#eta| Plot", "y":"Events", "x":"%s |#eta|"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['eta'][1]-bins['eta'][0])},
      "lepEta_tight":{'var':eta['tight'], "bins":bins['eta'], 'decor':{"title": "Lepton |#eta| Plot", "y":"Events", "x":"%s |#eta|"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['eta'][1]-bins['eta'][0])},
      "hybIso_loose":{ 'var':hybIso['loose'],  'bins':[10, 0, 25], 'decor':{'title':"Lepton hybIso Plot", 'x':"%s HI = I_{rel}*min(p_{T}, 25 GeV)"%lepton, 'y':"Events", 'log':[0,logy,0]}},
      "hybIso_tight":{ 'var':hybIso['tight'],  'bins':[10, 0, 25], 'decor':{'title':"Lepton hybIso Plot", 'x':"%s HI = I_{rel}*min(p_{T}, 25 GeV)"%lepton, 'y':"Events", 'log':[0,logy,0]}},
   }
    
   plotsDict = Plots(**plotDict)
   
   if logy: plotMin = 0.1
   else: plotMin = 0
   
   plotList = {}
   plotList['loose'] = ['lepPt_loose']
   plotList['tight'] = ['lepPt_tight']
   plotList['loose'].append('lepEta_loose')
   plotList['tight'].append('lepEta_tight')
   if not varBins: 
      plotList['loose'].append('hybIso_loose')
      plotList['tight'].append('hybIso_tight')
   
   fakePlots = {'SR':{}, 'looseCR':{}}
   
   plots =                           getPlots(samples, plotsDict, regions['SR']['fake'],        samplesList, plotList = plotList['tight'], addOverFlowBin='upper')
   fakePlots['SR']['fakes'] =       drawPlots(samples, plotsDict, regions['SR']['fake'],        samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
      
   plots =                           getPlots(samples, plotsDict, regions['looseCR']['fake'],   samplesList, plotList = plotList['loose'], addOverFlowBin='upper')
   fakePlots['looseCR']['fakes'] =  drawPlots(samples, plotsDict, regions['looseCR']['fake'],   samplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
      
   plots =                           getPlots(samples, plotsDict, regions['looseCR']['total'],  samplesList, plotList = plotList['loose'], addOverFlowBin='upper')
   fakePlots['looseCR']['total'] =  drawPlots(samples, plotsDict, regions['looseCR']['total'],  samplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
      
   plots =                           getPlots(samples, plotsDict, regions['looseCR']['prompt'], samplesList, plotList = plotList['loose'], addOverFlowBin='upper')
   fakePlots['looseCR']['prompt'] = drawPlots(samples, plotsDict, regions['looseCR']['prompt'], samplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
   
   if doControlPlots:
      plots =                        getPlots(samples, plotsDict, regions['SR']['total'],       samplesList, plotList = plotList['tight'], addOverFlowBin='upper')
      fakePlots['SR']['total'] =    drawPlots(samples, plotsDict, regions['SR']['total'],       samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
      
      plots =                        getPlots(samples, plotsDict, regions['SR']['prompt'],      samplesList, plotList = plotList['tight'], addOverFlowBin='upper')
      fakePlots['SR']['prompt'] =   drawPlots(samples, plotsDict, regions['SR']['prompt'],      samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
  
   # Legend
   leg = copy.deepcopy(fakePlots['looseCR']['fakes']['legs'])
   latex = copy.deepcopy(fakePlots['looseCR']['fakes']['latexText'])

   if len(leg) > 2:
      leg = [leg[0], leg[1]]

   ### Estimation ###
   
   finalHists = {}
   finalHists['TLratio'] = TLratio['pt'].Clone() #NOTE: currently only using pT inclusive tight-to-loose ratio
   #TLratio['pt'] = ROOT.TH1D()
   #TLratio['2D'].ProjectionX().Copy(TLratio['pt'])#ProfileX()
   #TLratio['pt'].Sumw2()
   #TLratio['pt'].Scale(1./Nbins)
   
   # L(!T) CR   
   finalHists['looseCR'] = {} # 2 options for loose CR

   # Fakes
   finalHists['looseCR']['fakes'] = fakePlots['looseCR']['fakes']['stacks']['bkg']['lepPt_loose'].Clone()
  
   # Total and prompt 
   looseCR_tot =    copy.deepcopy(fakePlots['looseCR']['total'])
   looseCR_prompt = copy.deepcopy(fakePlots['looseCR']['prompt'])
   looseCR_tot_prompt = {}

   finalHists['looseCR']['total'] =  looseCR_tot['stacks']['bkg']['lepPt_loose'].Clone()
   finalHists['looseCR']['prompt'] = looseCR_prompt['stacks']['bkg']['lepPt_loose'].Clone()
   finalHists['looseCR']['tot-prompt'] = ROOT.THStack('looseCR_tot-prompt', 'looseCR_tot-prompt') 
   
   # emulation of prompt subtraction from data using MC yields 
   for samp in looseCR_tot['hists']:
      looseCR_tot_prompt[samp] = looseCR_tot['hists'][samp]['lepPt_loose']
      setErrSqrtN(looseCR_tot_prompt[samp], varBins = varBins) # setting error as sqrt N
      looseCR_tot_prompt[samp].Add(looseCR_prompt['hists'][samp]['lepPt_loose'], -1)
      
      finalHists['looseCR']['tot-prompt'].Add(looseCR_tot_prompt[samp]) 
      
   # Multiplying L(!T) CR fakes with transfer factor 
   if looseNotTight:
      unity1 = unity(finalHists['TLratio'])
      unity2 = unity(finalHists['TLratio'])
      unity3 = unity(finalHists['TLratio'])
   
      unity1.Divide(finalHists['TLratio'].Clone())   
      diff = unity1 - unity2
      unity3.Divide(diff) #NOTE: evaluates to (TLratio/1-TLratio) with correct errors
   
      TF = unity3
    
      ratioTitle1 = "#frac{#epsilon_{TL}}{(1 - #epsilon_{TL})}"
   else:
      TF = finalHists['TLratio'].Clone() # TF = T-L ratio
      ratioTitle1 = "#epsilon_{TL}"
      
   #finalHists['estimate'] = multiplyHists(TF, finalHists['looseCR'].GetStack().Last().Clone())
   
   finalHists['estimate'] = {} 
 
   for x in ['fakes', 'tot-prompt']: 
      finalHists['estimate'][x] = TF*finalHists['looseCR'][x].GetStack().Last().Clone() #NOTE: last stack in GetStack() array is the sum of all stacks
      finalHists['estimate'][x].SetName("fakesEstimate_"+x)
   
   finalHists['estimate']['fakes'].SetMarkerStyle(20)
   finalHists['estimate']['fakes'].SetMarkerColor(1)
   finalHists['estimate']['fakes'].SetMarkerSize(0.9)
   finalHists['estimate']['fakes'].SetLineWidth(2)
   
   leg[-1].AddEntry(finalHists['estimate']['fakes'], "Prediction", "LP")
   canvas = drawPlot(finalHists['looseCR']['fakes'], legend = leg, decor = plotsDict['lepPt_loose']['decor'], latexText = latex, ratio = (finalHists['estimate']['fakes'], finalHists['looseCR']['fakes']), ratioLimits = [0,0.7], ratioTitle = ratioTitle1)
   #finalHists['estimate']['fakes'].SetName("fakesEstimate_final")
   finalHists['estimate']['fakes'].Draw("same")
 
   # Closure
   finalHists['SR'] = fakePlots['SR']['fakes']['stacks']['bkg']['lepPt_tight'].Clone()
   
   if closureDef == "ratio":
      ratioTitle2 = "#frac{Obs.}{Pred.}"
      ratioLimits2 = [0, 4] 
      unityLine = True
      closure = (finalHists['SR'], finalHists['estimate'])
   
   elif closureDef == "standard":
      ratioTitle2 = "#frac{Pred. - Obs.}{Pred.}"
      ratioLimits2 = [-2, 2] 
      unityLine = False
      
      closure = finalHists['estimate']['fakes'].Clone() - finalHists['SR'].GetStack().Last().Clone()
      estimate_zeroErr = finalHists['estimate']['fakes'].Clone()
      setErrZero(estimate_zeroErr)
      closure.Divide(estimate_zeroErr)
   
   if measurementType == "MC": 
      ratioTitle2 = ratioTitle2.replace('Obs.', 'MC')
   
   canvas2 = drawPlot(finalHists['SR'], legend = leg, decor = plotsDict['lepPt_tight']['decor'], latexText = latex, ratio = closure, ratioLimits = ratioLimits2, ratioTitle = ratioTitle2, unity = unityLine)
   finalHists['estimate']['fakes'].Draw("same")
   
   finalHists['closure'] = canvas2['ratio']

   if doYields:
   
      n = finalHists['TLratio'].GetNbinsX()
   
      finalHists['looseCR_hist'] = {} 
     
      hists =  ['TLratio', 'looseCR', 'estimate', 'SR', 'closure']
 
      value =     {'TLratio':{}, 'looseCR':{'total':{}, 'fakes':{}, 'prompt':{}, 'tot-prompt':{}}, 'looseCR_hist':{'total':{}, 'prompt':{}, 'fakes':{}, 'tot-prompt':{}}, 'estimate':{'fakes':{}, 'tot-prompt':{}}, 'SR':{}, 'closure':{}}
      error =     {'TLratio':{}, 'looseCR':{'total':{}, 'fakes':{}, 'prompt':{}, 'tot-prompt':{}}, 'looseCR_hist':{'total':{}, 'prompt':{}, 'fakes':{}, 'tot-prompt':{}}, 'estimate':{'fakes':{}, 'tot-prompt':{}}, 'SR':{}, 'closure':{}}
      histCont =  {'TLratio':{}, 'looseCR':{'total':{}, 'fakes':{}, 'prompt':{}, 'tot-prompt':{}}, 'looseCR_hist':{'total':{}, 'prompt':{}, 'fakes':{}, 'tot-prompt':{}}, 'estimate':{'fakes':{}, 'tot-prompt':{}}, 'SR':{}, 'closure':{}}
      histYlds =  {'TLratio':{}, 'looseCR':{'total':{}, 'fakes':{}, 'prompt':{}, 'tot-prompt':{}}, 'looseCR_hist':{'total':{}, 'prompt':{}, 'fakes':{}, 'tot-prompt':{}}, 'estimate':{'fakes':{}, 'tot-prompt':{}}, 'SR':{}, 'closure':{}}
      uFloat =    {'TLratio':{}, 'looseCR':{'total':{}, 'fakes':{}, 'prompt':{}, 'tot-prompt':{}}, 'looseCR_hist':{'total':{}, 'prompt':{}, 'fakes':{}, 'tot-prompt':{}}, 'estimate':{'fakes':{}, 'tot-prompt':{}}, 'SR':{}, 'closure':{}}
      uFloat_ylds =             {'looseCR':{'total':{}, 'fakes':{}, 'prompt':{}, 'tot-prompt':{}}, 'looseCR_hist':{'total':{}, 'prompt':{}, 'fakes':{}, 'tot-prompt':{}}, 'estimate':{'fakes':{}, 'tot-prompt':{}}, 'SR':{}}
   
      for i in range(n):
         i += 1
        
         for x in hists:
            if 'fakes' in value[x].keys(): # sub-hists
               for y in value[x]:
                  z = x
                  if type(finalHists[x][y]) == ROOT.THStack: # Convert THStack into TH1
                     z += '_hist'
                     finalHists[z][y] = finalHists[x][y].GetStack().Last().Clone()
  
                  histCont[x][y] = getHistContents(finalHists[z][y], varBinsYield = False)
                  uFloat[x][y] = histCont[x][y][0]

                  a = histCont[x][y][1]
                  w = histCont[x][y][2]

                  if x not in ['TLratio', 'closure']:
                     histYlds[x][y] = getHistContents(finalHists[z][y], varBinsYield = varBins)
                     uFloat_ylds[x][y] = histYlds[x][y][0]
            else: 
               z = x
               if type(finalHists[x]) == ROOT.THStack: # Convert THStack into TH1
                  z += '_hist'
                  finalHists[z] = finalHists[x].GetStack().Last().Clone()
                   
               histCont[x] = getHistContents(finalHists[z], varBinsYield = False)
               uFloat[x] = histCont[x][0]
                   
               a = histCont[x][1]
               w = histCont[x][2]
   
               if x not in ['TLratio', 'closure']:
                  histYlds[x] = getHistContents(finalHists[z], varBinsYield = varBins)
                  uFloat_ylds[x] = histYlds[x][0]
  
         if verbose:
            print makeLine()
            print "Fake rate estimation hists in bin %s %s-%s GeV"%(str(i), str(a[i]), str(a[i]+w[i])) 
            print makeLine()
            print "T-L Ratio:",           uFloat['TLratio'][i].round(3) 
            
            print "L(!T) CR (total):",    uFloat['looseCR']['total'][i].round(3) 
            print "L(!T) CR (prompt):",   uFloat['looseCR']['prompt'][i].round(3) 
            print "L(!T) CR (fakes):",    uFloat['looseCR']['fakes'][i].round(3) 
            print "Estimate:",            uFloat['estimate']['fakes'][i].round(3) 
            if looseNotTight: 
               print "Estimate (x-check):", (uFloat['TLratio'][i]/(u_float.u_float(1,0) - uFloat['TLratio'][i])*uFloat['looseCR']['fakes'][i]).round(3).val
            else: 
               print "Estimate (x-check):", (uFloat['TLratio'][i]*uFloat['looseCR']['fakes'][i]).round(3).val 
            print "SR MC:",               uFloat['SR'][i].round(3)
            print makeLine()
            print "L(!T) CR (prompt sub.)",  uFloat['looseCR']['tot-prompt'][i].round(3) 
            print "Estimate (prompt sub.):", uFloat['estimate']['tot-prompt'][i].round(3) 
            print makeLine()
         
            print makeLine()
            print "Fake rate estimation yields in bin %s %s-%s GeV"%(str(i), str(a[i]), str(a[i]+w[i])) 
            print makeLine()
            print "L(!T) CR (total):",    uFloat_ylds['looseCR']['total'][i].round(3) 
            print "L(!T) CR (prompt):",   uFloat_ylds['looseCR']['prompt'][i].round(3) 
            print "L(!T) CR (fakes):",    uFloat_ylds['looseCR']['fakes'][i].round(3) 
            print "Estimate:",            uFloat_ylds['estimate']['fakes'][i].round(3) 
            if looseNotTight: 
               print "Estimate (x-check):", (uFloat['TLratio'][i]/(u_float.u_float(1,0) - uFloat['TLratio'][i])*uFloat_ylds['looseCR']['fakes'][i]).round(3)
            else: 
               print "Estimate (x-check):", (uFloat['TLratio'][i]*uFloat_ylds['looseCR']['fakes'][i]).round(3) 
            print "SR MC:",               uFloat_ylds['SR'][i].round(3)
            print makeLine()
            print "L(!T) CR (prompt sub.)",  uFloat_ylds['looseCR']['tot-prompt'][i].round(3) 
            print "Estimate (prompt sub.):", uFloat_ylds['estimate']['tot-prompt'][i].round(3) 
            print makeLine()
            
            print "Closure:",             uFloat['closure'][i].round(3) 
            if uFloat['estimate']['fakes'][i].val:
               if closureDef == "ratio":
                  print "Closure (x-check):", (uFloat['SR'][i]/uFloat['estimate']['fakes'][i]).round(3) 
               elif closureDef == "standard":
                  print "Closure (x-check):", ((uFloat['estimate']['fakes'][i] - uFloat['SR'][i])/uFloat['estimate']['fakes'][i]).round(3).val 
            print makeLine()
            
         if save:
            if not os.path.isfile("%s/fakesClosure%s.txt"%(savedir, suffix)):
               outfile = open("%s/fakesClosure%s.txt"%(savedir, suffix), "w")
               outfile.write("Estimation of fakes in %s region for the %s channel (Bin Content)\n"%(region.title(), lepton))
               title = "Bin (GeV)       |   T-L Ratio      |        Loose CR (Total)       |       Loose CR (Prompt)       |       Loose CR (Fakes)     |     Estimate (MC)       |      SR: Fakes (MC)       |      MC Closure (%s)     |     Loose CR (Prompt Sub.)      |      Estimate (Prompt Sub.)\n"%(closureDef.title())
               if looseNotTight: title = title.replace("Loose", "L!T") 
               outfile.write(title)
   
            with open("%s/fakesClosure%s.txt"%(savedir, suffix), "a") as outfile:
               outfile.write("{}-{}".format(str(a[i]), str(a[i]+w[i])).ljust(15) + ' | ' +\
               str(uFloat['TLratio'][i].round(3)).ljust(22) + ' | ' +\
               str(uFloat['looseCR']['total'][i].round(3)).ljust(22)  + ' | ' +\
               str(uFloat['looseCR']['prompt'][i].round(3)).ljust(22) + ' | ' +\
               str(uFloat['looseCR']['fakes'][i].round(3)).ljust(22)  + ' | ' +\
               str(uFloat['estimate']['fakes'][i].round(3)).ljust(25) + ' | ' +\
               str(uFloat['SR'][i].round(3)).ljust(30) + ' | ' +\
               str(uFloat['closure'][i].round(3)).ljust(30) + ' | ' +\
               str(uFloat['looseCR']['tot-prompt'][i].round(3)).ljust(30) + ' | ' +\
               str(uFloat['estimate']['tot-prompt'][i].round(3))  + "\n")
            
            if not os.path.isfile("%s/fakesClosure_yields%s.txt"%(savedir, suffix)):
               outfile = open("%s/fakesClosure_yields%s.txt"%(savedir, suffix), "w")
               outfile.write("Estimation of fakes in %s region for the %s channel (Yields)\n"%(region.title(), lepton))
               title = "Bin (GeV)       |   T-L Ratio      |        Loose CR (Total)       |       Loose CR (Prompt)       |       Loose CR (Fakes)     |     Estimate (MC)       |      SR: Fakes (MC)       |      MC Closure (%s)     |     Loose CR (Prompt Sub.)      |      Estimate (Prompt Sub.)\n"%(closureDef.title())
               if looseNotTight: title = title.replace("Loose", "L!T") 
               outfile.write(title)
  
            with open("%s/fakesClosure_yields%s.txt"%(savedir, suffix), "a") as outfile:
               outfile.write("{}-{}".format(str(a[i]), str(a[i]+w[i])).ljust(15) + ' | ' +\
               str(uFloat['TLratio'][i].round(3)).ljust(22) + ' | ' +\
               str(uFloat_ylds['looseCR']['total'][i].round(3)).ljust(22)  + ' | ' +\
               str(uFloat_ylds['looseCR']['prompt'][i].round(3)).ljust(22) + ' | ' +\
               str(uFloat_ylds['looseCR']['fakes'][i].round(3)).ljust(22)  + ' | ' +\
               str(uFloat_ylds['estimate']['fakes'][i].round(3)).ljust(25) + ' | ' +\
               str(uFloat_ylds['SR'][i].round(3)).ljust(30) + ' | ' +\
               str(uFloat['closure'][i].round(3)).ljust(30) + ' | ' +\
               str(uFloat_ylds['looseCR']['tot-prompt'][i].round(3)).ljust(30) + ' | ' +\
               str(uFloat_ylds['estimate']['tot-prompt'][i].round(3))  + "\n")
  
            #Pickle results 
            pickleFile1 = open("%s/fakesClosure%s.pkl"%(savedir,suffix), "w")
            pickle.dump(uFloat, pickleFile1)
            pickleFile1.close()
            
            pickleFile2 = open("%s/fakesClosure_yields%s.pkl"%(savedir,suffix), "w")
            pickle.dump(uFloat_ylds, pickleFile2)
            pickleFile2.close()
 
   if save:
      if doControlPlots:
         for canv in fakePlots['SR']['total']['canvs']:
            fakePlots['SR']['total']['canvs'][canv][0].SaveAs("%s/SR%s_%s.png"%(savedir, suffix, canv))
            fakePlots['SR']['total']['canvs'][canv][0].SaveAs("%s/root/SR%s_%s.root"%(savedir, suffix, canv))
            fakePlots['SR']['total']['canvs'][canv][0].SaveAs("%s/pdf/SR%s_%s.pdf"%(savedir, suffix, canv))
         for canv in fakePlots['SR']['fakes']['canvs']:
            fakePlots['SR']['fakes']['canvs'][canv][0].SaveAs("%s/SR%s_%s_fake.png"%(savedir, suffix, canv))
            fakePlots['SR']['fakes']['canvs'][canv][0].SaveAs("%s/root/SR%s_%s_fake.root"%(savedir, suffix, canv))
            fakePlots['SR']['fakes']['canvs'][canv][0].SaveAs("%s/pdf/SR%s_%s_fake.pdf"%(savedir, suffix, canv))
         for canv in fakePlots['SR']['prompt']['canvs']:
            fakePlots['SR']['prompt']['canvs'][canv][0].SaveAs("%s/SR%s_%s_prompt.png"%(savedir, suffix, canv))
            fakePlots['SR']['prompt']['canvs'][canv][0].SaveAs("%s/root/SR%s_%s_prompt.root"%(savedir, suffix, canv))
            fakePlots['SR']['prompt']['canvs'][canv][0].SaveAs("%s/pdf/SR%s_%s_prompt.pdf"%(savedir, suffix, canv))
         
         for canv in fakePlots['looseCR']['total']['canvs']:
            fakePlots['looseCR']['total']['canvs'][canv][0].SaveAs("%s/looseCR%s_%s.png"%(savedir, suffix, canv))
            fakePlots['looseCR']['total']['canvs'][canv][0].SaveAs("%s/root/looseCR%s_%s.root"%(savedir, suffix, canv))
            fakePlots['looseCR']['total']['canvs'][canv][0].SaveAs("%s/pdf/looseCR%s_%s.pdf"%(savedir, suffix, canv))
         for canv in fakePlots['looseCR']['fakes']['canvs']:
            fakePlots['looseCR']['fakes']['canvs'][canv][0].SaveAs("%s/looseCR%s_%s_fake.png"%(savedir, suffix, canv))
            fakePlots['looseCR']['fakes']['canvs'][canv][0].SaveAs("%s/root/looseCR%s_%s_fake.root"%(savedir, suffix, canv))
            fakePlots['looseCR']['fakes']['canvs'][canv][0].SaveAs("%s/pdf/looseCR%s_%s_fake.pdf"%(savedir, suffix, canv))
         for canv in fakePlots['looseCR']['prompt']['canvs']:
            fakePlots['looseCR']['prompt']['canvs'][canv][0].SaveAs("%s/looseCR%s_%s_prompt.png"%(savedir, suffix, canv))
            fakePlots['looseCR']['prompt']['canvs'][canv][0].SaveAs("%s/root/looseCR%s_%s_prompt.root"%(savedir, suffix, canv))
            fakePlots['looseCR']['prompt']['canvs'][canv][0].SaveAs("%s/pdf/looseCR%s_%s_prompt.pdf"%(savedir, suffix, canv))
      
      canvas['canvs'][0].SaveAs("%s/fakesEstimate%s.png"%(savedir, suffix))
      canvas['canvs'][0].SaveAs("%s/root/fakesEstimate%s.root"%(savedir, suffix))
      canvas['canvs'][0].SaveAs("%s/pdf/fakesEstimate%s.pdf"%(savedir, suffix))
   
      canvas2['canvs'][0].SaveAs("%s/closureMC%s.png"%(savedir, suffix))
      canvas2['canvs'][0].SaveAs("%s/root/closureMC%s.root"%(savedir, suffix))
      canvas2['canvs'][0].SaveAs("%s/pdf/closureMC%s.pdf"%(savedir, suffix))
