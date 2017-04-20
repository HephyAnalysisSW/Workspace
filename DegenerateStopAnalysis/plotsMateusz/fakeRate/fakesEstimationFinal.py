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
measurementRegion = args.measurementRegion
fakeRateMeasurement = args.fakeRateMeasurement
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
dataset =     fakeInfo['dataset']

regDef = selection['regDef']
   
etaBin = 'eta_lt_1p5'

if doPlots:
   
   if save: 
      saveTag = fakeInfo['saveTag']
      etaBin =  fakeInfo['etaBin']
    
   # Root file with fake rate
   finalTag = "MR14"
   fakeRateFile = "tightToLooseRatios_%s_%s_stat.pkl"%(finalTag, fakeRateMeasurement)
   fakeRateDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/final/%s/%s/%s"%(saveTag, finalTag, fakeRateFile)
   TLratios = pickle.load(open(fakeRateDir, "r"))

   # if final estimate, adding systematics from MR
   if 'data' in fakeRateMeasurement:
      TLratios_sys = pickle.load(open(fakeRateDir.replace('stat', 'sys'), "r"))
      for l in ['el', 'mu']:
         for ptBin in TLratios[l][etaBin]:
            TLratios[l][etaBin][ptBin].sigma = sqrt(TLratios[l][etaBin][ptBin].sigma**2 + TLratios_sys[l][etaBin][ptBin].sigma**2) 

   if verbose:
      print makeLine()
      print "Using tight-to-loose ratio from ", fakeRateDir
      print makeLine()

#Save
if save:
   baseDir = fakeInfo['baseDir']
   #savedir = fakeInfo['savedir']
   suffix =  fakeInfo['suffix']
   savedir = baseDir + "/TEST"
   makeDir(savedir)
 
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

if not 'data' in fakeRateMeasurement:
   regions['SR']['total'] =  [selection['tight']['cuts'], regDef] 
   regions['SR']['prompt'] = [selection['tight']['cuts'], regDef + '_prompt'] 
   regions['SR']['fake'] =   [selection['tight']['cuts'], regDef + '_fake'] 

regions['looseCR']['total'] =  [selection['loose']['cuts'], regDef + '_notTight'] 
regions['looseCR']['prompt'] = [selection['loose']['cuts'], regDef + '_notTight_prompt'] 
regions['looseCR']['fake'] =   [selection['loose']['cuts'], regDef + '_notTight_fake'] 

if doPlots:
   # Plots
   bins = fakeBinning(lep, varBins = varBins)
   
   plotDict = {\
      "lepPt_loose":{'var':pt['loose'],   "bins":bins['pt'],  'decor':{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])},
      #"lepPt_tight":{'var':pt['tight'],   "bins":bins['pt'],  'decor':{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])},
   }
    
   plotsDict = Plots(**plotDict)
   
   if logy: plotMin = 0.1
   else: plotMin = 0
   
   plotList = {}
   plotList['loose'] = ['lepPt_loose']
   #plotList['tight'] = ['lepPt_tight']
   
   fakePlots = {'SR':{}, 'looseCR':{}}
   
   #plots =                           getPlots(samples, plotsDict, regions['SR']['fake'],        samplesList, plotList = plotList['tight'], addOverFlowBin='upper')
   #fakePlots['SR']['fakes'] =       drawPlots(samples, plotsDict, regions['SR']['fake'],        samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
   
   if fakeRateMeasurement == "MC":
      plots =                           getPlots(samples, plotsDict, regions['looseCR']['fake'],   samplesList, plotList = plotList['loose'], addOverFlowBin='upper')
      fakePlots['looseCR']['fakes'] =  drawPlots(samples, plotsDict, regions['looseCR']['fake'],   samplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
   elif fakeRateMeasurement == "data-EWK": 
      plots =                           getPlots(samples, plotsDict, regions['looseCR']['total'],  samplesList, plotList = plotList['loose'], addOverFlowBin='upper')
      fakePlots['looseCR']['total'] =   drawPlots(samples, plotsDict, regions['looseCR']['total'],  samplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["dblind"], fom = "RATIO", fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
      
      MCsamplesList = samplesList[:]
      MCsamplesList.remove(dataset)   
      plots =                           getPlots(samples, plotsDict, regions['looseCR']['prompt'], MCsamplesList, plotList = plotList['loose'], addOverFlowBin='upper')
      fakePlots['looseCR']['prompt'] = drawPlots(samples, plotsDict, regions['looseCR']['prompt'], MCsamplesList, plotList = plotList['loose'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
   
   #if doControlPlots:
   #   plots =                        getPlots(samples, plotsDict, regions['SR']['total'],       samplesList, plotList = plotList['tight'], addOverFlowBin='upper')
   #   fakePlots['SR']['total'] =    drawPlots(samples, plotsDict, regions['SR']['total'],       samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
   #   
   #   plots =                        getPlots(samples, plotsDict, regions['SR']['prompt'],      samplesList, plotList = plotList['tight'], addOverFlowBin='upper')
   #   fakePlots['SR']['prompt'] =   drawPlots(samples, plotsDict, regions['SR']['prompt'],      samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
  
   # Legend
   leg = copy.deepcopy(fakePlots['looseCR'][fakePlots['looseCR'].keys()[-1]]['legs'])
   latex = copy.deepcopy(fakePlots['looseCR'][fakePlots['looseCR'].keys()[-1]]['latexText'])

   if len(leg) > 2:
      leg = [leg[0], leg[1]]

   fakeHists = {'looseCR':{}}

   # L(!T) CR
   if fakeRateMeasurement == "MC": # Fakes
      basePlot = 'fakes'
      fakeHists['looseCR'][basePlot] = fakePlots['looseCR']['fakes']['stacks']['bkg']['lepPt_loose'].Clone()
   elif fakeRateMeasurement == "data-EWK": # Data and prompt 
      basePlot = 'data-prompt'
      looseCR_tot =    copy.deepcopy(fakePlots['looseCR']['total'])
      looseCR_prompt = copy.deepcopy(fakePlots['looseCR']['prompt'])
      #looseCR_data_prompt = {}

      #fakeHists['looseCR']['total'] =   looseCR_tot['hists'][dataset]['lepPt_loose'].Clone() # looseCR_tot['stacks']['total']['lepPt_loose'].Clone()
      fakeHists['looseCR']['prompt'] = looseCR_prompt['stacks']['bkg']['lepPt_loose'].Clone()
      #fakeHists['looseCR'][basePlot] = ROOT.THStack('looseCR_%s'%basePlot, 'looseCR_%s'%basePlot) 
      
      fakeHists['looseCR'][basePlot] = looseCR_tot['hists'][dataset]['lepPt_loose'].Clone() # add data
      for samp in looseCR_prompt['hists']:
         fakeHists['looseCR'][basePlot].Add(looseCR_prompt['hists'][samp]['lepPt_loose'], -1) # subtract prompt
         #looseCR_data_prompt[samp] = looseCR_tot['hists'][samp]['lepPt_loose']
         #looseCR_data_prompt[samp].Add(looseCR_prompt['hists'][samp]['lepPt_loose'], -1)
      
   #if type(fakeHists['looseCR'][basePlot]) == ROOT.THStack: # Convert THStack into TH1
   #   fakeHists['looseCR'][basePlot] = fakeHists['looseCR'][basePlot].GetStack().Last().Clone() #NOTE: last stack in GetStack() array is the sum of all stacks
   
   # Multiplying L(!T) CR fakes with transfer factor
   fakeHists['estimate'] = fakeHists['looseCR'][basePlot].Clone() 
   
   n = fakeHists['estimate'].GetNbinsX()
   
   #w1 = fakeHists['estimate'][basePlot].GetBinWidth(1)

   TF = {}
   est = {}
   est_err = {}

   for i in range(n):
      i += 1
      a = fakeHists['estimate'].GetBinLowEdge(i)
      w = fakeHists['estimate'].GetBinWidth(i)
    
      TF = TLratios[lep][etaBin][binMaps[lep][str(i)]].val/(1-TLratios[lep][etaBin][binMaps[lep][str(i)]].val) #NOTE: evaluates to (TLratio/1-TLratio)
      TF_err = TLratios[lep][etaBin][binMaps[lep][str(i)]].sigma
 
      est[str(i)] =  fakeHists['estimate'].GetBinContent(i)*TF
      if TF and fakeHists['estimate'].GetBinContent(i):
         est_err[str(i)] = est[str(i)]*sqrt(pow(fakeHists['estimate'].GetBinError(i)/fakeHists['estimate'].GetBinContent(i),2)+pow(TF_err/TF,2))
      else:
         est_err[str(i)] = 0. 
 
      fakeHists['estimate'].SetBinContent(i, est[str(i)])
      fakeHists['estimate'].SetBinError(i, est_err[str(i)])
      fakeHists['estimate'].SetName("fakesEstimate_"+basePlot)
   
   fakeHists['estimate'].SetMarkerStyle(20)
   fakeHists['estimate'].SetMarkerColor(1)
   fakeHists['estimate'].SetMarkerSize(0.9)
   fakeHists['estimate'].SetLineWidth(2)
   
   ratioTitle1 = "#frac{#epsilon_{TL}}{(1 - #epsilon_{TL})}"
   
   leg[-1].AddEntry(fakeHists['estimate'], "Prediction", "LP")
   
   canvas = drawPlot(fakeHists['looseCR'][basePlot], legend = leg, decor = plotsDict['lepPt_loose']['decor'], latexText = latex, ratio = (fakeHists['estimate'], fakeHists['looseCR'][basePlot]), ratioLimits = [0,0.7], ratioTitle = ratioTitle1)
   #fakeHists['estimate']['fakes'].SetName("fakesEstimate_final")
   fakeHists['estimate'].Draw("same")

   # Closure
   doClosure = False
   #if doClosure: 
   #   fakeHists['SR'] = fakePlots['SR']['fakes']['stacks']['bkg']['lepPt_tight'].Clone()
   #   
   #   ratioTitle2 = "#frac{Pred. - Obs.}{Pred.}"
   #   ratioLimits2 = [-2, 2] 
   #   unityLine = False
   #   
   #   closure = fakeHists['estimate']['fakes'].Clone() - fakeHists['SR'].GetStack().Last().Clone()
   #   estimate_zeroErr = fakeHists['estimate']['fakes'].Clone()
   #   setErrZero(estimate_zeroErr)
   #   closure.Divide(estimate_zeroErr)
   #   
   #   if fakeRateMeasurement == "MC": 
   #      ratioTitle2 = ratioTitle2.replace('Obs.', 'MC')
   #
   #   canvas2 = drawPlot(fakeHists['SR'], legend = leg, decor = plotsDict['lepPt_tight']['decor'], latexText = latex, ratio = closure, ratioLimits = ratioLimits2, ratioTitle = ratioTitle2, unity = unityLine)
   #   fakeHists['estimate'].Draw("same")
   #   
   #   fakeHists['closure'] = canvas2['ratio']

   doYields = 0
   if doYields:
   
      n = fakeHists['estimate'].GetNbinsX()
   
      numbers =  ['TLratio', 'looseCR', 'estimate']
 
      value =  {'TLratio':{}, 'looseCR':{'total':{}, 'fakes':{}, 'prompt':{}, 'data-prompt':{}}, 'looseCR_hist':{'total':{}, 'prompt':{}, 'fakes':{}, 'data-prompt':{}}, 'estimate':{'fakes':{}, 'data-prompt':{}}, 'SR':{}, 'closure':{}}
      error =  {'TLratio':{}, 'looseCR':{'total':{}, 'fakes':{}, 'prompt':{}, 'data-prompt':{}}, 'looseCR_hist':{'total':{}, 'prompt':{}, 'fakes':{}, 'data-prompt':{}}, 'estimate':{'fakes':{}, 'data-prompt':{}}, 'SR':{}, 'closure':{}}
      uFloat = {'TLratio':{}, 'looseCR':{'total':{}, 'fakes':{}, 'prompt':{}, 'data-prompt':{}}, 'looseCR_hist':{'total':{}, 'prompt':{}, 'fakes':{}, 'data-prompt':{}}, 'estimate':{'fakes':{}, 'data-prompt':{}}, 'SR':{}, 'closure':{}}
      uFloat_ylds =          {'looseCR':{'total':{}, 'fakes':{}, 'prompt':{}, 'data-prompt':{}}, 'looseCR_hist':{'total':{}, 'prompt':{}, 'fakes':{}, 'data-prompt':{}}, 'estimate':{'fakes':{}, 'data-prompt':{}}, 'SR':{}}
   
      w1 = fakeHists['TLratio'].GetBinWidth(1)

      for i in range(n):
         i += 1
         a = fakeHists['TLratio'].GetBinLowEdge(i)
         w = fakeHists['TLratio'].GetBinWidth(i)
        
         for x in numbers:
            if 'fakes' in value[x].keys():
               for y in value[x]:
                  z = x
                  if type(fakeHists[x][y]) == ROOT.THStack: # Convert THStack into TH1
                     z += '_hist'
                     fakeHists[z][y] = fakeHists[x][y].GetStack().Last().Clone()
   
                  value[x][y][i] = fakeHists[z][y].GetBinContent(i)
                  error[x][y][i] = fakeHists[z][y].GetBinError(i)
                  uFloat[x][y][i] = u_float.u_float(value[x][y][i], error[x][y][i]) 
                  if x not in ['TLratio', 'closure']:
                     uFloat_ylds[x][y][i] = copy.deepcopy(uFloat[x][y][i])
                     uFloat_ylds[x][y][i].val =   uFloat_ylds[x][y][i].val*w/w1
                     uFloat_ylds[x][y][i].sigma = uFloat_ylds[x][y][i].sigma*sqrt(w/w1)
            else: 
               z = x
               if type(fakeHists[x]) == ROOT.THStack: # Convert THStack into TH1
                  z += '_hist'
                  fakeHists[z] = fakeHists[x].GetStack().Last().Clone()
   
               value[x][i] = fakeHists[z].GetBinContent(i)
               error[x][i] = fakeHists[z].GetBinError(i)
               uFloat[x][i] = u_float.u_float(value[x][i], error[x][i]) 
               if x not in ['TLratio', 'closure']:
                  uFloat_ylds[x][i] = copy.deepcopy(uFloat[x][i])
                  uFloat_ylds[x][i].val =   uFloat_ylds[x][i].val*w/w1
                  uFloat_ylds[x][i].sigma = uFloat_ylds[x][i].sigma*sqrt(w/w1)
   
         if verbose:
            print makeLine()
            print "Fake rate estimation numbers in bin %s %s-%s GeV"%(str(i), str(a), str(a+w)) 
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
            print "L(!T) CR (prompt sub.)",  uFloat['looseCR']['data-prompt'][i].round(3) 
            print "Estimate (prompt sub.):", uFloat['estimate']['data-prompt'][i].round(3) 
            print makeLine()
         
            print makeLine()
            print "Fake rate estimation yields in bin %s %s-%s GeV"%(str(i), str(a), str(a+w)) 
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
            print "L(!T) CR (prompt sub.)",  uFloat_ylds['looseCR']['data-prompt'][i].round(3) 
            print "Estimate (prompt sub.):", uFloat_ylds['estimate']['data-prompt'][i].round(3) 
            print makeLine()
            
            print "Closure:",             uFloat['closure'][i].round(3) 
            if uFloat['estimate']['fakes'][i].val:
               if closureDef == "ratio":
                  print "Closure (x-check):", (uFloat['SR'][i]/uFloat['estimate']['fakes'][i]).round(3) 
               elif closureDef == "standard":
                  print "Closure (x-check):", ((uFloat['estimate']['fakes'][i] - uFloat['SR'][i])/uFloat['estimate']['fakes'][i]).round(3).val 
            print makeLine()
            
         if save:
            if not os.path.isfile("%s/fakesEstimation%s.txt"%(savedir, suffix)):
               outfile = open("%s/fakesEstimation%s.txt"%(savedir, suffix), "w")
               outfile.write("Estimation of fakes in %s region for the %s channel (Bin Content)\n"%(region.title(), lepton))
               title = "Bin (GeV)       |   T-L Ratio      |        Loose CR (Total)       |       Loose CR (Prompt)       |       Loose CR (Fakes)     |     Estimate (MC)       |      SR: Fakes (MC)       |      MC Closure (%s)     |     Loose CR (Prompt Sub.)      |      Estimate (Prompt Sub.)\n"%(closureDef.title())
               if looseNotTight: title = title.replace("Loose", "L!T") 
               outfile.write(title)
   
            with open("%s/fakesEstimation%s.txt"%(savedir, suffix), "a") as outfile:
               outfile.write("{}-{}".format(str(a), str(a+w)).ljust(15) + ' | ' +\
               str(uFloat['TLratio'][i].round(3)).ljust(22) + ' | ' +\
               str(uFloat['looseCR']['total'][i].round(3)).ljust(22)  + ' | ' +\
               str(uFloat['looseCR']['prompt'][i].round(3)).ljust(22) + ' | ' +\
               str(uFloat['looseCR']['fakes'][i].round(3)).ljust(22)  + ' | ' +\
               str(uFloat['estimate']['fakes'][i].round(3)).ljust(25) + ' | ' +\
               str(uFloat['SR'][i].round(3)).ljust(30) + ' | ' +\
               str(uFloat['closure'][i].round(3)).ljust(30) + ' | ' +\
               str(uFloat['looseCR']['data-prompt'][i].round(3)).ljust(30) + ' | ' +\
               str(uFloat['estimate']['data-prompt'][i].round(3))  + "\n")
            
            if not os.path.isfile("%s/fakesEstimation_yields%s.txt"%(savedir, suffix)):
               outfile = open("%s/fakesEstimation_yields%s.txt"%(savedir, suffix), "w")
               outfile.write("Estimation of fakes in %s region for the %s channel (Yields)\n"%(region.title(), lepton))
               title = "Bin (GeV)       |   T-L Ratio      |        Loose CR (Total)       |       Loose CR (Prompt)       |       Loose CR (Fakes)     |     Estimate (MC)       |      SR: Fakes (MC)       |      MC Closure (%s)     |     Loose CR (Prompt Sub.)      |      Estimate (Prompt Sub.)\n"%(closureDef.title())
               if looseNotTight: title = title.replace("Loose", "L!T") 
               outfile.write(title)
  
            with open("%s/fakesEstimation_yields%s.txt"%(savedir, suffix), "a") as outfile:
               outfile.write("{}-{}".format(str(a), str(a+w)).ljust(15) + ' | ' +\
               str(uFloat['TLratio'][i].round(3)).ljust(22) + ' | ' +\
               str(uFloat_ylds['looseCR']['total'][i].round(3)).ljust(22)  + ' | ' +\
               str(uFloat_ylds['looseCR']['prompt'][i].round(3)).ljust(22) + ' | ' +\
               str(uFloat_ylds['looseCR']['fakes'][i].round(3)).ljust(22)  + ' | ' +\
               str(uFloat_ylds['estimate']['fakes'][i].round(3)).ljust(25) + ' | ' +\
               str(uFloat_ylds['SR'][i].round(3)).ljust(30) + ' | ' +\
               str(uFloat['closure'][i].round(3)).ljust(30) + ' | ' +\
               str(uFloat_ylds['looseCR']['data-prompt'][i].round(3)).ljust(30) + ' | ' +\
               str(uFloat_ylds['estimate']['data-prompt'][i].round(3))  + "\n")
  
            #Pickle results 
            pickleFile1 = open("%s/fakesEstimation%s.pkl"%(savedir,suffix), "w")
            pickle.dump(uFloat, pickleFile1)
            pickleFile1.close()
            
            pickleFile2 = open("%s/fakesEstimation_yields%s.pkl"%(savedir,suffix), "w")
            pickle.dump(uFloat_ylds, pickleFile2)
            pickleFile2.close()

   if save:
      #if doControlPlots:
      #   for canv in fakePlots['SR']['total']['canvs']:
      #      fakePlots['SR']['total']['canvs'][canv][0].SaveAs("%s/SR%s_%s.png"%(savedir, suffix, canv))
      #      fakePlots['SR']['total']['canvs'][canv][0].SaveAs("%s/root/SR%s_%s.root"%(savedir, suffix, canv))
      #      fakePlots['SR']['total']['canvs'][canv][0].SaveAs("%s/pdf/SR%s_%s.pdf"%(savedir, suffix, canv))
      #   for canv in fakePlots['SR']['fakes']['canvs']:
      #      fakePlots['SR']['fakes']['canvs'][canv][0].SaveAs("%s/SR%s_%s_fake.png"%(savedir, suffix, canv))
      #      fakePlots['SR']['fakes']['canvs'][canv][0].SaveAs("%s/root/SR%s_%s_fake.root"%(savedir, suffix, canv))
      #      fakePlots['SR']['fakes']['canvs'][canv][0].SaveAs("%s/pdf/SR%s_%s_fake.pdf"%(savedir, suffix, canv))
      #   for canv in fakePlots['SR']['prompt']['canvs']:
      #      fakePlots['SR']['prompt']['canvs'][canv][0].SaveAs("%s/SR%s_%s_prompt.png"%(savedir, suffix, canv))
      #      fakePlots['SR']['prompt']['canvs'][canv][0].SaveAs("%s/root/SR%s_%s_prompt.root"%(savedir, suffix, canv))
      #      fakePlots['SR']['prompt']['canvs'][canv][0].SaveAs("%s/pdf/SR%s_%s_prompt.pdf"%(savedir, suffix, canv))
      #   
      for p in fakePlots['looseCR']: 
         for canv in fakePlots['looseCR'][p]['canvs']:
            fakePlots['looseCR'][p]['canvs'][canv][0].SaveAs("%s/looseCR%s_%s_%s.png"%(savedir, suffix, p, canv))
            fakePlots['looseCR'][p]['canvs'][canv][0].SaveAs("%s/root/looseCR%s_%s_%s.root"%(savedir, suffix, p, canv))
            fakePlots['looseCR'][p]['canvs'][canv][0].SaveAs("%s/pdf/looseCR%s_%s_%s.pdf"%(savedir, suffix, p, canv))
      
      canvas['canvs'][0].SaveAs("%s/fakesEstimate%s.png"%(savedir, suffix))
      canvas['canvs'][0].SaveAs("%s/root/fakesEstimate%s.root"%(savedir, suffix))
      canvas['canvs'][0].SaveAs("%s/pdf/fakesEstimate%s.pdf"%(savedir, suffix))
   
      #canvas2['canvs'][0].SaveAs("%s/closureMC%s.png"%(savedir, suffix))
      #canvas2['canvs'][0].SaveAs("%s/root/closureMC%s.root"%(savedir, suffix))
      #canvas2['canvs'][0].SaveAs("%s/pdf/closureMC%s.pdf"%(savedir, suffix))

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
#            str(yields['looseCR']['total'].yieldDictFull[samp][regDef + '_notTight'].round(2)).ljust(24) + ' | '  +\
#            str(yields['looseCR']['prompt'].yieldDictFull[samp][regDef + '_notTight_prompt'].round(2)).ljust(24) + ' | ' +\
#            str(yields['looseCR']['fake'].yieldDictFull[samp][regDef + '_notTight_fake'].round(2)).ljust(24) + ' | ' +\
#            str(yields['SR']['total'].yieldDictFull[samp][regDef].round(2)).ljust(24) + ' | ' +\
#            str(yields['SR']['prompt'].yieldDictFull[samp][regDef + '_prompt'].round(2)).ljust(24) + ' | ' +\
#            str(yields['SR']['fake'].yieldDictFull[samp][regDef + '_fake'].round(2)) + "\n")

