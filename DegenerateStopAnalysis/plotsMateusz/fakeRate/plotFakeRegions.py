# plotFakeRegions.py
# Plots of regions for fake rate estimation 
# Mateusz Zarucki 2017

import os
from fakeInfo import *

script = os.path.basename(__file__) #sys.argv[0]

#Arguments
args = fakeParser(script)

lep = args.lep
region = args.region
mva = args.mva
WP = args.WP
looseNotTight = args.looseNotTight
doPlots = args.doPlots
doYields = args.doYields
doControlPlots = args.doControlPlots
varBins = args.varBins
logy = args.logy
save = args.save
verbose = args.verbose

fakeInfo = fakeInfo(script, vars(args))

lepton =      fakeInfo['lepton']
samplesList = fakeInfo['samplesList']
samples =     fakeInfo['samples']
dataset =     fakeInfo['dataset']
selection =   fakeInfo['selection']
bins =        fakeInfo['bins']

if save:
   savedir =  fakeInfo['savedir']
   suffix =   fakeInfo['suffix']
   if doYields: 
      yieldDir = fakeInfo['yieldDir']

if dataset: fom = "RATIO"
else:       fom = False

regDef = selection['regDef']

index = {'probe': selection[WP]['lepIndex1']}

variables = {}

if "measurement2" in region or "measurement3" in region:
   index['tag1'] = selection[WP]['tagIndex1']

   if "measurement3" in region:
      index['tag2'] = selection[WP]['tagIndex2']

      variables['dilepton_mass'] = "sqrt(2*(LepAll_pt[{tag1}] * LepAll_pt[{tag2}]*(cosh(LepAll_eta[{tag1}] - LepAll_eta[{tag2}]) - cos(LepAll_phi[{tag1}] - LepAll_phi[{tag2}]))))".format(tag1 = index['tag1'], tag2 = index['tag2'])
      
      variables['dilepton_pt'] = "sqrt(LepAll_pt[{tag1}]*LepAll_pt[{tag2}] + LepAll_pt[{tag1}]*LepAll_pt[{tag2}] + 2*LepAll_pt[{tag1}]*LepAll_pt[{tag2}]*cos(LepAll_phi[{tag1}] - LepAll_phi[{tag2}]))".format(tag1 = index['tag1'], tag2 = index['tag2'])
      
      variables['dilepton_phi'] = "atan2(\
      ((LepAll_pt[{tag1}]*sin(LepAll_phi[{tag1}])) + (LepAll_pt[{tag2}]*sin(LepAll_phi[{tag2}]))),\
      ((LepAll_pt[{tag1}]*cos(LepAll_phi[{tag1}])) + (LepAll_pt[{tag2}]*cos(LepAll_phi[{tag2}]))))".format(tag1 = index['tag1'], tag2 = index['tag2'])


for x in index:
   variables[x] = {\
      'pt':"LepGood_pt[%s]"%index[x],
      'eta':"abs(LepGood_eta[%s])"%index[x],
      'mt':"LepGood_mt[%s]"%index[x],
      'lepDxy':"abs(LepGood_dxy[%s])"%index[x],
      'lepDz':"abs(LepGood_dz[%s])"%index[x],
      'absIso':"LepGood_absIso03[%s]"%index[x],
      'relIso':"LepGood_relIso03[%s]"%index[x],
      'hybIso':"(LepGood_relIso03[{ind}]*min(LepGood_pt[{ind}], 25))".format(ind = index[x]),
      'mcMatchId':"LepGood_mcMatchId[%s]"%index[x],
      'mcMatchAny':"LepGood_mcMatchAny[%s]"%index[x],
   }
 
   variables[x]['hybIso2'] = "(log(1 + " + variables[x]['hybIso'] + ")/log(1+5))"

# Loose (not-Tight) CR
if WP == "loose" and looseNotTight:
   notTight = "_notTight"
else:
   notTight = ""

# Plots
bins = fakeBinning(lep, varBins = varBins)

plotDict = {\
   "ht":{     'var':"ht_basJet_def",         'bins':[75,0,1500],  'decor':{'title':"H_{{T}} Plot", "y":"Events", "x":"H_{T} / GeV", "log":[0,logy,0]}},
   "met":{    'var':"met",                   'bins':[100,0,1000], 'decor':{'title':"MET Plot",     "y":"Events", "x":"MET / GeV",   "log":[0,logy,0]}},
   "nJets": {'var':"nJet_basJet_def",        'bins':[10,0,10], "nMinus1":None, "decor":{"title":"Number of Jets",      "x":"Number of Jets",      'y':"Events", 'log':[0,logy,0]}},
   "nSoftJets": {'var':"nJet_softJet_def",   'bins':[10,0,10], "nMinus1":None, "decor":{"title":"Number of Soft Jets", "x":"Number of Soft Jets", 'y':"Events", 'log':[0,logy,0]}},
   "nHardJets": {'var':"nJet_hardJet_def",   'bins':[10,0,10], "nMinus1":None, "decor":{"title":"Number of Hard Jets", "x":"Number of Hard Jets", 'y':"Events", 'log':[0,logy,0]}},
   "nBJets": {'var':"nJet_bJet_def",         'bins':[10,0,10], "nMinus1":None, "decor":{"title":"Number of B Jets",    "x":"Number of B Jets",    'y':"Events", 'log':[0,logy,0]}},
   "delPhi":{ 'var':"dPhi_j1j2_vetoJet_def", 'bins':[8, 0, 3.14], 'decor':{'title':"deltaPhi(j1,j2) Plot", 'x':"#Delta#phi(j1,j2)", 'y':"Events", 'log':[0,logy,0]}},
}

plotDict_lep = {}

for x in index:
   if "tag" in x:
      lepName = "Lepton " + x.replace('tag','')
   else:
      lepName = lepton

   plotDict_lep.update({\
      "lepPt_"+x:{     'var':variables[x]['pt'],         'bins':bins['pt'],      'decor':{'title':" Lepton p_{{T}} Plot",   'y':"Events", 'x':"%s %s %s p_{T} / GeV"%(x.title(), WP.title(),lepName), "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])},
      "lepEta_"+x:{    'var':variables[x]['eta'],        'bins':bins['eta'],     'decor':{'title':" Lepton |#eta| Plot",    'y':"Events", 'x':"%s %s %s |#eta|"%(x.title(), WP.title(),lepName),      "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['eta'][1]-bins['eta'][0])}, 
      "lepMt_"+x:{     'var':variables[x]['mt'],         'bins':bins['mt'],      'decor':{'title':" Lepton m_{{T}} Plot",   'y':"Events", 'x':"%s %s %s m_{T} / GeV"%(x.title(), WP.title(),lepName), "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['mt'][1]-bins['mt'][0])}, 
      "lepDxy_"+x:{    'var':variables[x]['lepDxy'],     'bins':[10, 0, 0.1],    'decor':{'title':" Lepton |dxy| Plot",     'y':"Events", 'x':"%s %s %s|dxy|"%(x.title(), WP.title(),lepName),                            'log':[0,logy,0]}},
      "lepDz_"+x:{     'var':variables[x]['lepDz'],      'bins':[10, 0, 0.5],    'decor':{'title':" Lepton |dz| Plot",      'y':"Events", 'x':"%s %s %s|dz|"%(x.title(), WP.title(),lepName),                             'log':[0,logy,0]}},
      "absIso_"+x:{    'var':variables[x]['absIso'],     'bins':[4, 0, 20],      'decor':{'title':" Lepton absIso Plot",    'y':"Events", 'x':"%s %s %s I_{abs} / GeV"%(x.title(), WP.title(),lepName),                   'log':[0,logy,0]}},
      "relIso_"+x:{    'var':variables[x]['relIso'],     'bins':[20, 0, 5],      'decor':{'title':" Lepton relIso Plot",    'y':"Events", 'x':"%s %s %s I_{rel}"%(x.title(), WP.title(),lepName),                         'log':[0,logy,0]}},
      "hybIso_"+x:{    'var':variables[x]['hybIso'],     'bins':[10, 0, 25],     'decor':{'title':" Lepton hybIso Plot",    'y':"Events", 'x':"%s %s %s HI = I_{rel}*min(p_{T}, 25 GeV)"%(x.title(), WP.title(),lepName), 'log':[0,logy,0]}},
      "hybIso2_"+x:{   'var':variables[x]['hybIso2'],    'bins':[8, 0, 4],       'decor':{'title':" Lepton hybIso Plot",    'y':"Events", 'x':"%s %s %s log(1+HI)/log(1+5)"%(x.title(), WP.title(),lepName),              'log':[0,logy,0]}},
      "mcMatchId_"+x:{ 'var':variables[x]['mcMatchId'],  'bins':[140, -30, 110], 'decor':{'title':" Lepton mcMatchId Plot", 'y':"Events", 'x':"%s %s %s mcMatchId"%(x.title(), WP.title(),lepName),           'log':[0,logy,0]}},
      "mcMatchAny_"+x:{'var':variables[x]['mcMatchAny'], 'bins':[14, -4, 10],    'decor':{'title':" Lepton mcMatchAny Plot",'y':"Events", 'x':"%s %s %s mcMatchAny"%(x.title(), WP.title(),lepName),          'log':[0,logy,0]}},
   })
      
plotDict_lep.update({\
   "nLep":{'var':selection[WP]['cuts'].vars.nLep.string, 'bins':[10,0,10], 'decor':{'title':"Number of %s %ss"%(WP.title(), lepName), "y":"Events", "x":"nLep (%s %ss)"%(WP.title(), lepton), "log":[0,logy,0]}},
   })

plotDict.update(plotDict_lep)

if region == "measurement3":
   plotDict_MR3 = {\
      "dilepton_mass":{'var':variables["dilepton_mass"], 'bins':[50,5,255],      'decor':{'title':"Di-lepton System Invariant Mass Distribution",      'x':"M_{ll} / GeV",              'y':"Events", 'log':[0,logy,0]}},
      "dilepton_pt":{  'var':variables["dilepton_pt"],   'bins':[50,0,250],      'decor':{'title':"Di-lepton System Transverse Momentum Distribution", 'x':"p_{T_{ll}} / GeV",          'y':"Events", 'log':[0,logy,0]}},
      "dilepton_phi":{ 'var':variables["dilepton_phi"],  'bins':[20,-3.15,3.15], 'decor':{'title':"Di-lepton System Phi Distribution",                 'x':"Dilepton System Phi / GeV", 'y':"Events", 'log':[0,logy,0]}},
   }

   plotDict.update(plotDict_MR3)

if "application" in region:
   if not varBins: plotDict['met']['bins'] = [100, 0, 1000]
   
if logy: plotMin = 10
else: plotMin = 0

plotsDict = Plots(**plotDict)
plotsList = ["lepPt_probe", "lepMt_probe", "lepEta_probe"]
if "measurement2" in region or "measurement3" in region: 
   plotsList.extend(["lepPt_tag1", "lepMt_tag1", "lepEta_tag1"])

   if "measurement3" in region: 
      plotsList.extend(["lepPt_tag2", "lepMt_tag2", "lepEta_tag2"])
      plotsList.extend(["dilepton_mass", "dilepton_pt", "dilepton_phi"])

if not varBins: 
   plotsList.extend(["met", "ht", "nLep"])
   plotsList.extend(["hybIso_probe", "hybIso2_probe"])
   plotsList.extend(["nJets", "nSoftJets", "nHardJets", "nBJets"])
   plotsList.extend(["lepDxy_probe", "lepDz_probe", "absIso_probe", "relIso_probe", "delPhi"]) 
#if not getData: plotsList.extend(["mcMatchId_probe", "mcMatchAny_probe"])

if doPlots:
   for plot in plotsList:
      plots =       getPlots(samples, plotsDict, [selection[WP]['cuts'], regDef + notTight], samplesList, plotList = [plot], addOverFlowBin='both')
      fakePlots =  drawPlots(samples, plotsDict, [selection[WP]['cuts'], regDef + notTight], samplesList, plotList = [plot], plotLimits = [plotMin, 100], denoms = ["bkg"], noms = [dataset], fom = fom, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)

      if doControlPlots:
         MCsamplesList = samplesList[:]
         if dataset in MCsamplesList: samplesList.remove(dataset)
         plots =       getPlots(samples, plotsDict, [selection[WP]['cuts'], regDef + notTight + '_prompt'], MCsamplesList, plotList = [plot], addOverFlowBin='both')
         fakePlots2 = drawPlots(samples, plotsDict, [selection[WP]['cuts'], regDef + notTight + '_prompt'], MCsamplesList, plotList = [plot], plotLimits = [plotMin, 100], fom = None, plotMin = plotMin, normalize = False, save = False)
         
         plots =       getPlots(samples, plotsDict, [selection[WP]['cuts'], regDef + notTight + '_fake'],  MCsamplesList, plotList = [plot], addOverFlowBin='both')
         fakePlots3 = drawPlots(samples, plotsDict, [selection[WP]['cuts'], regDef + notTight + '_fake'],  MCsamplesList, plotList = [plot], plotLimits = [plotMin, 100], fom = None, plotMin = plotMin, normalize = False, save = False)
      
      if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
         for canv in fakePlots['canvs']:
            fakePlots['canvs'][canv][0].SaveAs("%s/%s%s.png"%(savedir, canv, suffix))
            fakePlots['canvs'][canv][0].SaveAs("%s/root/%s%s.root"%(savedir, canv, suffix))
            fakePlots['canvs'][canv][0].SaveAs("%s/pdf/%s%s.pdf"%(savedir, canv, suffix))
         if doControlPlots:
            for canv in fakePlots2['canvs']:
               fakePlots2['canvs'][canv][0].SaveAs("%s/%s%s_prompt.png"%(savedir, canv, suffix))
               fakePlots2['canvs'][canv][0].SaveAs("%s/root/%s%s_prompt.root"%(savedir, canv, suffix))
               fakePlots2['canvs'][canv][0].SaveAs("%s/pdf/%s%s_prompt.pdf"%(savedir, canv, suffix))
            for canv in fakePlots3['canvs']:
               fakePlots3['canvs'][canv][0].SaveAs("%s/%s%s_fake.png"%(savedir, canv, suffix))
               fakePlots3['canvs'][canv][0].SaveAs("%s/root/%s%s_fake.root"%(savedir, canv, suffix))
               fakePlots3['canvs'][canv][0].SaveAs("%s/pdf/%s%s_fake.pdf"%(savedir, canv, suffix))

# Yields
if doYields:
   yields = {}

   yields['total'] =     Yields(samples, samplesList, cutInst = None, cuts = [selection[WP]['cuts'], regDef + notTight],             cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
   if doControlPlots:
      yields['prompt'] = Yields(samples, samplesList, cutInst = None, cuts = [selection[WP]['cuts'], regDef + notTight + '_prompt'], cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
      yields['fake'] =   Yields(samples, samplesList, cutInst = None, cuts = [selection[WP]['cuts'], regDef + notTight + '_fake'],   cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
 
   if not os.path.isfile("%s/fakeYields_%s%s.txt"%(yieldDir, region, suffix)):
      outfile = open("%s/fakeYields_%s%s.txt"%(yieldDir, region, suffix), "w")
      outfile.write("Fake Estimation Yields in %s %s\n"%(WP, region.title()))
      outfile.write("Sample        Total                Prompt                Fakes\n")

   yieldsList = samplesList[:]
   yieldsList.append('Total')

   with open("%s/fakeYields_%s%s.txt"%(yieldDir, region, suffix), "a") as outfile:
     for samp in yieldsList:
         outfile.write(samp.ljust(10) +\
         str(yields['total'].yieldDictFull[samp][regDef  + notTight].round(2)).ljust(25))
         if doControlPlots:
            outfile.write(\
            str(yields['prompt'].yieldDictFull[samp][regDef + notTight + '_prompt'].round(2)).ljust(25) +\
            str(yields['fake'].yieldDictFull[samp][regDef  + notTight + '_fake'].round(2)) + "\n")
         else:   
            outfile.write("\n")

   outfile.close()
