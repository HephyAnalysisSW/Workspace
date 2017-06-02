# fakesEstimationFinal_etaCobmined.py
# Application of fake rate to estimate fake background contribution 
# Mateusz Zarucki 2017

import os
from fakeInfo import *

script = "fakesEstimationFinal.py" #os.path.basename(__file__) #sys.argv[0]

#Arguments
args = fakeParser(script)

mva = args.mva
lep = args.lep
region = args.region
measurementType = args.measurementType
addMRsys = args.addMRsys
VR = args.VR
doPlots = args.doPlots
doYields = args.doYields
doControlPlots = args.doControlPlots
doClosure = args.doClosure
mergeHighPtBins = args.mergeHighPtBins
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

if 'sr2' not in region and not mva: 
   print "Region must be sr2 or MVA. Exiting."
   sys.exit()

if doPlots:

   if save:
      saveTag = fakeInfo['saveTag']
      #etaBin =  fakeInfo['etaBin']

   # Root file with fake rate
   finalTag = "MR14"
   #fakeRateFile = "tightToLooseRatios_%s_%s_stat.pkl"%(finalTag, measurementType)
   #fakeRateDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/final/%s/%s/%s"%(saveTag, finalTag, fakeRateFile)
   #TLratios = pickle.load(open(fakeRateDir, "r"))

   ## if final estimate from data, adding systematics from MR
   #if addMRsys:
   #   TLratios_sys = pickle.load(open(fakeRateDir.replace('stat', 'sys2'), "r"))
   #   for l in ['el', 'mu']:
   #      for ptBin in TLratios[l][etaBin]:
   #         if ptBin == "0_5" or ptBin == "0_3p5": continue
   #         TLratios[l][etaBin][ptBin].sigma = sqrt(TLratios[l][etaBin][ptBin].sigma**2 + (TLratios_sys[measurementType][etaBin][l][ptBin]*TLratios[l][etaBin][ptBin].val)**2)

   #if verbose:
   #   print makeLine()
   #   print "Using tight-to-loose ratio from ", fakeRateDir
   #   print makeLine()

 
#Save
if save:
   baseDir = fakeInfo['baseDir']
   savedir = fakeInfo['savedir']
   suffix =  fakeInfo['suffix']

   if addMRsys:
      suffix2 = "_withMRsys"
      suffix += suffix2 
   else:
      suffix2 = ""
   
   if mergeHighPtBins:
      suffix3 = "_mergedCRbins"
      suffix += suffix3 
      suffix2 += suffix3 
   else:
      suffix3 = ""

# SR/VR plotting for closure   
if 'data' in measurementType and VR not in ['EVR1', 'EVR2']:
   print makeLine()
   print "Warning - data closure should be in suitable VR. Skipping closure."
   print makeLine()
   doClosure = False
 
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
regions = {'SR':{}}#, 'looseCR':{}}

regions['SR']['total'] =  [selection['tight']['cuts'], regDefs['regDef']]
regions['SR']['prompt'] = [selection['tight']['cuts'], regDefs['regDef'] + '_plus_prompt']
regions['SR']['fake'] =   [selection['tight']['cuts'], regDefs['regDef'] + '_plus_fake']

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
#            str(yields['looseCR']['total'].yieldDictFull[samp][regDefs['regDef' + notTight]].round(2)).ljust(24) + ' | '  +\
#            str(yields['looseCR']['prompt'].yieldDictFull[samp][regDefs['regDef' + notTight] + '_plus_prompt'].round(2)).ljust(24) + ' | ' +\
#            str(yields['looseCR']['fake'].yieldDictFull[samp][regDefs['regDef' + notTight] + '_plus_fake'].round(2)).ljust(24) + ' | ' +\
#            str(yields['SR']['total'].yieldDictFull[samp][regDefs['regDef']].round(2)).ljust(24) + ' | ' +\
#            str(yields['SR']['prompt'].yieldDictFull[samp][regDefs['regDef'] + '_plus_prompt'].round(2)).ljust(24) + ' | ' +\
#            str(yields['SR']['fake'].yieldDictFull[samp][regDefs['regDef'] + '_plus_fake'].round(2)) + "\n")

if mergeHighPtBins:
   varBins2 = False
else:
   varBins2 = varBins

# Plots
if doPlots:
   bins = fakeBinning(lep, varBins = varBins)
   
   plotDict = {\
      "lepPt_loose":{'var':pt['loose'],   "bins":bins['pt'],  'decor':{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins2, bins['pt'][1]-bins['pt'][0])},
      "lepPt_tight":{'var':pt['tight'],   "bins":bins['pt'],  'decor':{"title": "Lepton p_{{T}} Plot", "y":"Events", "x":"%s p_{T} / GeV"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins2, bins['pt'][1]-bins['pt'][0])},
      "lepEta_loose":{'var':eta['loose'], "bins":bins['eta'], 'decor':{"title": "Lepton |#eta| Plot", "y":"Events", "x":"%s |#eta|"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins2, bins['eta'][1]-bins['eta'][0])},
      "lepEta_tight":{'var':eta['tight'], "bins":bins['eta'], 'decor':{"title": "Lepton |#eta| Plot", "y":"Events", "x":"%s |#eta|"%lepton, "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins2, bins['eta'][1]-bins['eta'][0])},
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
 
   estDir = {}
   estFileName = {}
   estFile = {}
   estimate = {}

   if save:
      baseFileDir = savedir.split('/')
      del baseFileDir[-1]
      if logy:  del baseFileDir[-1]
      baseFileDir = '/'.join(baseFileDir)
      #savedir2 = baseFileDir + "/combinedEta"
      #if logy: savedir2 += "/log"
      #makeDir(savedir2 + '/root')
      #makeDir(savedir2 + '/pdf')

   for etaBin in ['eta_lt_1p5', 'eta_gt_1p5']:
      estDir[etaBin] = "%s/%s/log/root/"%(baseFileDir, etaBin)
      #estFileName[etaBin] = "closure_%s_%s_%s%s.root"%(lep, region, measurementType, suffix2)
      estFileName[etaBin] = "fakesEstimate_%s_%s_%s%s.root"%(lep, region, measurementType, suffix2)
      
      if 'lt' in etaBin:   etaName = 'plus_lepEta1p5'
      elif 'gt' in etaBin: etaName = 'plus_lepEta_gt_1p5'

      if mva: a = "presel_mvaTrain_"
      else:   a = ""
         
      canvName = 'Canvas_TTX_%s%s_%s_plus_highWeightVeto_plus_notTight_plus_fake_Leptonp_TPlot'%(a, regDefs['regDef'].replace('_plus_highWeightVeto', ''), etaName)
      print '!!!', canvName 
      if 'data' in measurementType: canvName = canvName.replace('TTX', 'DataBlind')
      plotName = "fakesEstimate"
      
      try:
         estFile[etaBin] = ROOT.TFile(estDir[etaBin] + estFileName[etaBin])
         estimate[etaBin] = estFile[etaBin].Get(canvName).GetPrimitive(canvName + '_p1').GetPrimitive(plotName).Clone()
      except:
         AttributeError
         print "File", estDir[etaBin] + estFileName[etaBin], "not found. Exiting."
         sys.exit()
         #continue

   fakePlots = {'SR':{}}#, 'looseCR':{}}
   
   plots =                           getPlots(samples, plotsDict, regions['SR']['fake'],        samplesList, plotList = plotList['tight'], addOverFlowBin='upper')
   fakePlots['SR']['fakes'] =       drawPlots(samples, plotsDict, regions['SR']['fake'],        samplesList, plotList = plotList['tight'], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
      
   if doControlPlots:
      plots =                        getPlots(samples, plotsDict, regions['SR']['total'],       samplesList, plotList = plotList['tight'], addOverFlowBin='upper')
      fakePlots['SR']['total'] =    drawPlots(samples, plotsDict, regions['SR']['total'],       samplesList, plotList = plotList['tight'], plotLimits = [10, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
      
      plots =                        getPlots(samples, plotsDict, regions['SR']['prompt'],      samplesList, plotList = plotList['tight'], addOverFlowBin='upper')
      fakePlots['SR']['prompt'] =   drawPlots(samples, plotsDict, regions['SR']['prompt'],      samplesList, plotList = plotList['tight'], plotLimits = [10, 100], denoms = ["bkg"], noms = ["qcd"], fom = None, fomLimits = [0,2.8], plotMin = 10, normalize = False, save = False)
   
   # Legend
   leg = copy.deepcopy(fakePlots['SR']['fakes']['legs'])
   latex = copy.deepcopy(fakePlots['SR']['fakes']['latexText'])

   if len(leg) > 2:
      leg = [leg[0], leg[1]]

   ratioTitle1 = "#frac{#epsilon_{TL}}{(1 - #epsilon_{TL})}"
      
   ##finalHists['estimate'] = multiplyHists(TF, finalHists['looseCR'].GetStack().Last().Clone())
   
   finalHists = {}  
 
   finalHists['estimate'] = estimate['eta_lt_1p5'] + estimate['eta_gt_1p5'] # final estimate is sum of estimates from two eta bins 
 
   finalHists['estimate'].SetMarkerStyle(20)
   finalHists['estimate'].SetMarkerColor(1)
   finalHists['estimate'].SetMarkerSize(0.9)
   finalHists['estimate'].SetLineWidth(2)
   
   leg[-1].AddEntry(finalHists['estimate'], "Prediction", "LP")
   canvas = drawPlot(finalHists['estimate'], legend = leg, decor = plotsDict['lepPt_loose']['decor'], latexText = latex, ratio = (finalHists['estimate'], finalHists['estimate']), ratioLimits = [0,0.7], ratioTitle = ratioTitle1, plotMin = plotMin)

   estKey = 'estimate'
   
   # Closure
   if doClosure: 
      finalHists['SR'] = fakePlots['SR']['fakes']['stacks']['bkg']['lepPt_tight'].Clone()
      
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

         if type(finalHists['SR']) == ROOT.THStack:
            SR_rebinned = ROOT.THStack('SR_rebinned', 'SR_rebinned')
            SR_rebinned_hists = {}
            
            for samp in fakePlots['SR']['fakes']['hists']:
               SR_rebinned_hists[samp] = fakePlots['SR']['fakes']['hists'][samp]['lepPt_tight'].Clone() 
               SR_rebinned_hists[samp] = SR_rebinned_hists[samp].Rebin(len(bins2['pt'])-1, "SR_rebinned_"+samp, binsCond)
               #SR_rebinned_hists[samp].Sumw2()
               SR_rebinned_hists[samp].Scale(SR_rebinned_hists[samp].GetBinWidth(1),"width")
               SR_rebinned.Add(SR_rebinned_hists[samp])

            finalHists['SR'] = SR_rebinned

         finalHists[estKey] = finalHists['estimate'].Clone()
         #finalHists[estKey].Sumw2()
         finalHists[estKey] = finalHists[estKey].Rebin(len(bins2['pt'])-1, "fakesEstimate_rebinned", binsCond)
         finalHists[estKey].Scale(finalHists[estKey].GetBinWidth(1),"width")
 
      closure = finalHists[estKey].Clone() - finalHists['SR'].GetStack().Last().Clone()
      estimate_zeroErr = finalHists[estKey].Clone()
      setErrZero(estimate_zeroErr)
      closure.Divide(estimate_zeroErr)
      
      if measurementType == "MC": 
         ratioTitle2 = ratioTitle2.replace('Obs.', 'MC')
      
      canvas2 = drawPlot(finalHists['SR'], legend = leg, decor = plotsDict['lepPt_tight']['decor'], latexText = latex, ratio = closure, ratioLimits = ratioLimits2, ratioTitle = ratioTitle2, unity = unityLine, plotMin = plotMin)
      finalHists[estKey].Draw("same")
      
      finalHists['closure'] = canvas2['ratio']

   #if doYields:
   #
   #   n = finalHists['TLratio'].GetNbinsX()
   #
   #   finalHists['looseCR_hist'] = {} 
   #  
   #   numbers =  ['TLratio', 'looseCR', 'estimate', 'SR', 'closure']
 
   #   value =  {'TLratio':{}, 'looseCR':{'total':{}, 'fakes':{}, 'prompt':{}, 'tot-prompt':{}}, 'looseCR_hist':{'total':{}, 'prompt':{}, 'fakes':{}, 'tot-prompt':{}}, 'estimate':{'fakes':{}, 'tot-prompt':{}}, 'SR':{}, 'closure':{}}
   #   error =  {'TLratio':{}, 'looseCR':{'total':{}, 'fakes':{}, 'prompt':{}, 'tot-prompt':{}}, 'looseCR_hist':{'total':{}, 'prompt':{}, 'fakes':{}, 'tot-prompt':{}}, 'estimate':{'fakes':{}, 'tot-prompt':{}}, 'SR':{}, 'closure':{}}
   #   uFloat = {'TLratio':{}, 'looseCR':{'total':{}, 'fakes':{}, 'prompt':{}, 'tot-prompt':{}}, 'looseCR_hist':{'total':{}, 'prompt':{}, 'fakes':{}, 'tot-prompt':{}}, 'estimate':{'fakes':{}, 'tot-prompt':{}}, 'SR':{}, 'closure':{}}
   #   uFloat_ylds =          {'looseCR':{'total':{}, 'fakes':{}, 'prompt':{}, 'tot-prompt':{}}, 'looseCR_hist':{'total':{}, 'prompt':{}, 'fakes':{}, 'tot-prompt':{}}, 'estimate':{'fakes':{}, 'tot-prompt':{}}, 'SR':{}}
   #
   #   w1 = finalHists['TLratio'].GetBinWidth(1)

   #   for i in range(n):
   #      i += 1
   #      a = finalHists['TLratio'].GetBinLowEdge(i)
   #      w = finalHists['TLratio'].GetBinWidth(i)
   #     
   #      for x in numbers:
   #         if 'fakes' in value[x].keys():
   #            for y in value[x]:
   #               z = x
   #               if type(finalHists[x][y]) == ROOT.THStack: # Convert THStack into TH1
   #                  z += '_hist'
   #                  finalHists[z][y] = finalHists[x][y].GetStack().Last().Clone()
   #
   #               value[x][y][i] = finalHists[z][y].GetBinContent(i)
   #               error[x][y][i] = finalHists[z][y].GetBinError(i)
   #               uFloat[x][y][i] = u_float.u_float(value[x][y][i], error[x][y][i]) 
   #               if x not in ['TLratio', 'closure']:
   #                  uFloat_ylds[x][y][i] = copy.deepcopy(uFloat[x][y][i])
   #                  uFloat_ylds[x][y][i].val =   uFloat_ylds[x][y][i].val*w/w1
   #                  uFloat_ylds[x][y][i].sigma = uFloat_ylds[x][y][i].sigma*sqrt(w/w1)
   #         else: 
   #            z = x
   #            if type(finalHists[x]) == ROOT.THStack: # Convert THStack into TH1
   #               z += '_hist'
   #               finalHists[z] = finalHists[x].GetStack().Last().Clone()
   #
   #            value[x][i] = finalHists[z].GetBinContent(i)
   #            error[x][i] = finalHists[z].GetBinError(i)
   #            uFloat[x][i] = u_float.u_float(value[x][i], error[x][i]) 
   #            if x not in ['TLratio', 'closure']:
   #               uFloat_ylds[x][i] = copy.deepcopy(uFloat[x][i])
   #               uFloat_ylds[x][i].val =   uFloat_ylds[x][i].val*w/w1
   #               uFloat_ylds[x][i].sigma = uFloat_ylds[x][i].sigma*sqrt(w/w1)
   #
   #      if verbose:
   #         print makeLine()
   #         print "Fake rate estimation numbers in bin %s %s-%s GeV"%(str(i), str(a), str(a+w)) 
   #         print makeLine()
   #         print "T-L Ratio:",           uFloat['TLratio'][i].round(3) 
   #         
   #         print "L(!T) CR (total):",    uFloat['looseCR']['total'][i].round(3) 
   #         print "L(!T) CR (prompt):",   uFloat['looseCR']['prompt'][i].round(3) 
   #         print "L(!T) CR (fakes):",    uFloat['looseCR']['fakes'][i].round(3) 
   #         print "Estimate:",            uFloat['estimate']['fakes'][i].round(3) 
   #         if looseNotTight: 
   #            print "Estimate (x-check):", (uFloat['TLratio'][i]/(u_float.u_float(1,0) - uFloat['TLratio'][i])*uFloat['looseCR']['fakes'][i]).round(3).val
   #         else: 
   #            print "Estimate (x-check):", (uFloat['TLratio'][i]*uFloat['looseCR']['fakes'][i]).round(3).val 
   #         print "SR MC:",               uFloat['SR'][i].round(3)
   #         print makeLine()
   #         print "L(!T) CR (prompt sub.)",  uFloat['looseCR']['tot-prompt'][i].round(3) 
   #         print "Estimate (prompt sub.):", uFloat['estimate']['tot-prompt'][i].round(3) 
   #         print makeLine()
   #      
   #         print makeLine()
   #         print "Fake rate estimation yields in bin %s %s-%s GeV"%(str(i), str(a), str(a+w)) 
   #         print makeLine()
   #         print "L(!T) CR (total):",    uFloat_ylds['looseCR']['total'][i].round(3) 
   #         print "L(!T) CR (prompt):",   uFloat_ylds['looseCR']['prompt'][i].round(3) 
   #         print "L(!T) CR (fakes):",    uFloat_ylds['looseCR']['fakes'][i].round(3) 
   #         print "Estimate:",            uFloat_ylds['estimate']['fakes'][i].round(3) 
   #         if looseNotTight: 
   #            print "Estimate (x-check):", (uFloat['TLratio'][i]/(u_float.u_float(1,0) - uFloat['TLratio'][i])*uFloat_ylds['looseCR']['fakes'][i]).round(3)
   #         else: 
   #            print "Estimate (x-check):", (uFloat['TLratio'][i]*uFloat_ylds['looseCR']['fakes'][i]).round(3) 
   #         print "SR MC:",               uFloat_ylds['SR'][i].round(3)
   #         print makeLine()
   #         print "L(!T) CR (prompt sub.)",  uFloat_ylds['looseCR']['tot-prompt'][i].round(3) 
   #         print "Estimate (prompt sub.):", uFloat_ylds['estimate']['tot-prompt'][i].round(3) 
   #         print makeLine()
   #         
   #         print "Closure:",             uFloat['closure'][i].round(3) 
   #         if uFloat['estimate']['fakes'][i].val:
   #            if closureDef == "ratio":
   #               print "Closure (x-check):", (uFloat['SR'][i]/uFloat['estimate']['fakes'][i]).round(3) 
   #            elif closureDef == "standard":
   #               print "Closure (x-check):", ((uFloat['estimate']['fakes'][i] - uFloat['SR'][i])/uFloat['estimate']['fakes'][i]).round(3).val 
   #         print makeLine()
   #         
   #
   #      if save:
   #         if not os.path.isfile("%s/fakesEstimation%s.txt"%(savedir, suffix)):
   #            outfile = open("%s/fakesEstimation%s.txt"%(savedir, suffix), "w")
   #            outfile.write("Estimation of fakes in %s region for the %s channel (Bin Content)\n"%(region.title(), lepton))
   #            title = "Bin (GeV)       |   T-L Ratio      |        Loose CR (Total)       |       Loose CR (Prompt)       |       Loose CR (Fakes)     |     Estimate (MC)       |      SR: Fakes (MC)       |      MC Closure (%s)     |     Loose CR (Prompt Sub.)      |      Estimate (Prompt Sub.)\n"%(closureDef.title())
   #            if looseNotTight: title = title.replace("Loose", "L!T") 
   #            outfile.write(title)
   #
   #         with open("%s/fakesEstimation%s.txt"%(savedir, suffix), "a") as outfile:
   #            outfile.write("{}-{}".format(str(a), str(a+w)).ljust(15) + ' | ' +\
   #            str(uFloat['TLratio'][i].round(3)).ljust(22) + ' | ' +\
   #            str(uFloat['looseCR']['total'][i].round(3)).ljust(22)  + ' | ' +\
   #            str(uFloat['looseCR']['prompt'][i].round(3)).ljust(22) + ' | ' +\
   #            str(uFloat['looseCR']['fakes'][i].round(3)).ljust(22)  + ' | ' +\
   #            str(uFloat['estimate']['fakes'][i].round(3)).ljust(25) + ' | ' +\
   #            str(uFloat['SR'][i].round(3)).ljust(30) + ' | ' +\
   #            str(uFloat['closure'][i].round(3)).ljust(30) + ' | ' +\
   #            str(uFloat['looseCR']['tot-prompt'][i].round(3)).ljust(30) + ' | ' +\
   #            str(uFloat['estimate']['tot-prompt'][i].round(3))  + "\n")
   #         
   #         if not os.path.isfile("%s/fakesEstimation_yields%s.txt"%(savedir, suffix)):
   #            outfile = open("%s/fakesEstimation_yields%s.txt"%(savedir, suffix), "w")
   #            outfile.write("Estimation of fakes in %s region for the %s channel (Yields)\n"%(region.title(), lepton))
   #            title = "Bin (GeV)       |   T-L Ratio      |        Loose CR (Total)       |       Loose CR (Prompt)       |       Loose CR (Fakes)     |     Estimate (MC)       |      SR: Fakes (MC)       |      MC Closure (%s)     |     Loose CR (Prompt Sub.)      |      Estimate (Prompt Sub.)\n"%(closureDef.title())
   #            if looseNotTight: title = title.replace("Loose", "L!T") 
   #            outfile.write(title)
  
   #         with open("%s/fakesEstimation_yields%s.txt"%(savedir, suffix), "a") as outfile:
   #            outfile.write("{}-{}".format(str(a), str(a+w)).ljust(15) + ' | ' +\
   #            str(uFloat['TLratio'][i].round(3)).ljust(22) + ' | ' +\
   #            str(uFloat_ylds['looseCR']['total'][i].round(3)).ljust(22)  + ' | ' +\
   #            str(uFloat_ylds['looseCR']['prompt'][i].round(3)).ljust(22) + ' | ' +\
   #            str(uFloat_ylds['looseCR']['fakes'][i].round(3)).ljust(22)  + ' | ' +\
   #            str(uFloat_ylds['estimate']['fakes'][i].round(3)).ljust(25) + ' | ' +\
   #            str(uFloat_ylds['SR'][i].round(3)).ljust(30) + ' | ' +\
   #            str(uFloat['closure'][i].round(3)).ljust(30) + ' | ' +\
   #            str(uFloat_ylds['looseCR']['tot-prompt'][i].round(3)).ljust(30) + ' | ' +\
   #            str(uFloat_ylds['estimate']['tot-prompt'][i].round(3))  + "\n")
  
   #         #Pickle results 
   #         pickleFile1 = open("%s/fakesEstimation%s.pkl"%(savedir,suffix), "w")
   #         pickle.dump(uFloat, pickleFile1)
   #         pickleFile1.close()
   #         
   #         pickleFile2 = open("%s/fakesEstimation_yields%s.pkl"%(savedir,suffix), "w")
   #         pickle.dump(uFloat_ylds, pickleFile2)
   #         pickleFile2.close()
 
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
         
      canvas['canvs'][0].SaveAs("%s/fakesEstimate%s.png"%(savedir, suffix))
      canvas['canvs'][0].SaveAs("%s/root/fakesEstimate%s.root"%(savedir, suffix))
      canvas['canvs'][0].SaveAs("%s/pdf/fakesEstimate%s.pdf"%(savedir, suffix))

      if doClosure: 
         canvas2['canvs'][0].SaveAs("%s/closure%s.png"%(savedir, suffix))
         canvas2['canvs'][0].SaveAs("%s/root/closure%s.root"%(savedir, suffix))
         canvas2['canvs'][0].SaveAs("%s/pdf/closure%s.pdf"%(savedir, suffix))
