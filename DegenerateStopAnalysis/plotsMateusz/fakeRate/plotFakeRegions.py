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
getData = args.getData
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

regDefs = selection['regDefs']

index = {'probe': selection[WP]['lepIndex1']}

variables = {}

if "measurement2" in region or "measurement3" in region:
   index['tag1'] = selection[WP]['tagIndex1']

   if "measurement3" in region:
      index['tag2'] = selection[WP]['tagIndex2']

      variables['dilepton_mass'] = "sqrt(2*(LepGood_pt[{tag1}] * LepGood_pt[{tag2}]*(cosh(LepGood_eta[{tag1}] - LepGood_eta[{tag2}]) - cos(LepGood_phi[{tag1}] - LepGood_phi[{tag2}]))))".format(tag1 = index['tag1'], tag2 = index['tag2'])
      
      variables['dilepton_pt'] = "sqrt(LepGood_pt[{tag1}]*LepGood_pt[{tag2}] + LepGood_pt[{tag1}]*LepGood_pt[{tag2}] + 2*LepGood_pt[{tag1}]*LepGood_pt[{tag2}]*cos(LepGood_phi[{tag1}] - LepGood_phi[{tag2}]))".format(tag1 = index['tag1'], tag2 = index['tag2'])
      
      variables['dilepton_phi'] = "atan2(\
      ((LepGood_pt[{tag1}]*sin(LepGood_phi[{tag1}])) + (LepGood_pt[{tag2}]*sin(LepGood_phi[{tag2}]))),\
      ((LepGood_pt[{tag1}]*cos(LepGood_phi[{tag1}])) + (LepGood_pt[{tag2}]*cos(LepGood_phi[{tag2}]))))".format(tag1 = index['tag1'], tag2 = index['tag2'])

if mva:
   variables['mvaResponse'] = "mva_response[{mvaIdIndex}]".format(mvaIdIndex = selection['mvaIdIndex'])

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
      'eleID':"LepGood_SPRING15_25ns_v1[%s]"%index[x],
      'muID':"LepGood_mediumMuonId[%s]"%index[x],
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
   "weight":{ 'var':"weight", 'bins':[50, 0, 50], 'decor':{'title':"Weight plot", 'x':"weight", 'y':"Events", 'log':[0,logy,0]}},
}

plotDict_lep = {}

for x in index:
   if "tag" in x:
      lepName = "Lepton "# + x.replace('tag','')
   else:
      lepName = lepton

   plotDict_lep.update({\
      "lepPt_"+x:{     'var':variables[x]['pt'],         'bins':bins['pt'],      'decor':{'title':"Lepton p_{{T}} Plot",   'y':"Events", 'x':"%s %s %s p_{T} / GeV"%(x.title(), WP.title(),lepName), "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['pt'][1]-bins['pt'][0])},
      "lepEta_"+x:{    'var':variables[x]['eta'],        'bins':bins['eta'],     'decor':{'title':"Lepton |#eta| Plot",    'y':"Events", 'x':"%s %s %s |#eta|"%(x.title(), WP.title(),lepName),      "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['eta'][1]-bins['eta'][0])}, 
      "lepMt_"+x:{     'var':variables[x]['mt'],         'bins':bins['mt'],      'decor':{'title':"Lepton m_{{T}} Plot",   'y':"Events", 'x':"%s %s %s m_{T} / GeV"%(x.title(), WP.title(),lepName), "log":[0,logy,0]}, "binningIsExplicit":varBins, "variableBinning":(varBins, bins['mt'][1]-bins['mt'][0])}, 
      "lepDxy_"+x:{    'var':variables[x]['lepDxy'],     'bins':[10, 0, 0.1],    'decor':{'title':"Lepton |dxy| Plot",     'y':"Events", 'x':"%s %s %s|dxy|"%(x.title(), WP.title(),lepName),                            'log':[0,logy,0]}},
      "lepDz_"+x:{     'var':variables[x]['lepDz'],      'bins':[10, 0, 0.5],    'decor':{'title':"Lepton |dz| Plot",      'y':"Events", 'x':"%s %s %s|dz|"%(x.title(), WP.title(),lepName),                             'log':[0,logy,0]}},
      "absIso_"+x:{    'var':variables[x]['absIso'],     'bins':[4, 0, 20],      'decor':{'title':"Lepton absIso Plot",    'y':"Events", 'x':"%s %s %s I_{abs} / GeV"%(x.title(), WP.title(),lepName),                   'log':[0,logy,0]}},
      "relIso_"+x:{    'var':variables[x]['relIso'],     'bins':[20, 0, 5],      'decor':{'title':"Lepton relIso Plot",    'y':"Events", 'x':"%s %s %s I_{rel}"%(x.title(), WP.title(),lepName),                         'log':[0,logy,0]}},
      "hybIso_"+x:{    'var':variables[x]['hybIso'],     'bins':[10, 0, 25],     'decor':{'title':"Lepton hybIso Plot",    'y':"Events", 'x':"%s %s %s HI = I_{rel}*min(p_{T}, 25 GeV)"%(x.title(), WP.title(),lepName), 'log':[0,logy,0]}},
      "hybIso2_"+x:{   'var':variables[x]['hybIso2'],    'bins':[8, 0, 4],       'decor':{'title':"Lepton hybIso Plot",    'y':"Events", 'x':"%s %s %s log(1+HI)/log(1+5)"%(x.title(), WP.title(),lepName),              'log':[0,logy,0]}},
      "eleID_"+x:{     'var':variables[x]['eleID'],      'bins':[5,0,5],         'decor':{"title":"Electron ID",           'y':"Events", 'x':"%s %s %s Electron ID"%(x.title(), WP.title(),lepName), 'log':[0,logy,0]}},
      "muID_"+x:{      'var':variables[x]['muID'],       'bins':[5,0,5],         'decor':{"title":"Muon ID",               'y':"Events", 'x':"%s %s %s Muon ID"%(x.title(), WP.title(),lepName),     'log':[0,logy,0]}},
      "mcMatchId_"+x:{ 'var':variables[x]['mcMatchId'],  'bins':[140, -30, 110], 'decor':{'title':"Lepton mcMatchId Plot", 'y':"Events", 'x':"%s %s %s mcMatchId"%(x.title(), WP.title(),lepName),   'log':[0,logy,0]}},
      "mcMatchAny_"+x:{'var':variables[x]['mcMatchAny'], 'bins':[14, -4, 10],    'decor':{'title':"Lepton mcMatchAny Plot",'y':"Events", 'x':"%s %s %s mcMatchAny"%(x.title(), WP.title(),lepName),  'log':[0,logy,0]}},
   })
      
plotDict_lep.update({\
   "nLep":{'var':selection[WP]['cuts'].vars.nLep.string, 'bins':[10,0,10], 'decor':{'title':"Number of %s %ss"%(WP.title(), lepName), "y":"Events", "x":"nLep (%s %ss)"%(WP.title(), lepton), "log":[0,logy,0]}},
   })
plotDict.update(plotDict_lep)

if mva:
   plotDict_mva = {\
      "mvaResponse":{'var':variables['mvaResponse'], 'bins':[48, -0.6, 0.6],  'decor':{'title':"MVA Response",   'x':"MVA Response", 'y':"Events", 'log':[0,logy,0]}},
   }
   plotDict.update(plotDict_mva)

if "measurement3" in region:
   plotDict_MR3 = {\
      "dilepton_mass":{'var':variables["dilepton_mass"], 'bins':[50,5,255],      'decor':{'title':"Di-lepton System Invariant Mass Distribution",      'x':"M_{ll} / GeV",              'y':"Events", 'log':[0,logy,0]}},
      "dilepton_pt":{  'var':variables["dilepton_pt"],   'bins':[50,0,250],      'decor':{'title':"Di-lepton System Transverse Momentum Distribution", 'x':"p_{T_{ll}} / GeV",          'y':"Events", 'log':[0,logy,0]}},
      "dilepton_phi":{ 'var':variables["dilepton_phi"],  'bins':[20,-3.15,3.15], 'decor':{'title':"Di-lepton System Phi Distribution",                 'x':"Dilepton System Phi / GeV", 'y':"Events", 'log':[0,logy,0]}},
   }

   plotDict.update(plotDict_MR3)

if "application" in region:
   if not varBins: plotDict['met']['bins'] = [100, 0, 1000]
   
if logy: plotMin = 100
else: plotMin = 0

plotsDict = Plots(**plotDict)
plotsList = ["lepPt_probe", "lepMt_probe", "lepEta_probe"]

if "measurement2" in region or "measurement3" in region: 
   plotsList.extend(["lepPt_tag1", "lepMt_tag1", "lepEta_tag1"])
   
   if not varBins: 
      plotsList.extend(['eleID_tag1', 'muID_tag2'])

   if "measurement3" in region: 
      plotsList.extend(["lepPt_tag2", "lepMt_tag2", "lepEta_tag2"])
      plotsList.extend(["dilepton_mass", "dilepton_pt", "dilepton_phi"])
      
      if not varBins: 
         plotsList.extend(['eleID_tag1', 'muID_tag2'])

if not varBins: 
   plotsList.extend(["met", "ht", "nLep"])
   plotsList.extend(["hybIso_probe", "hybIso2_probe"])
   plotsList.extend(["nJets", "nSoftJets", "nHardJets", "nBJets"])
   plotsList.extend(["lepDxy_probe", "lepDz_probe", "absIso_probe", "relIso_probe", "delPhi"])

   if lep == 'el':  plotsList.append('eleID_probe')
   elif lep == 'mu':plotsList.append('muID_probe')
   
   if mva:plotsList.append('mvaResponse')

if not getData: plotsList.extend(["mcMatchId_probe", "mcMatchAny_probe"])
      
MCsamplesList = samplesList[:]
if dataset in MCsamplesList: MCsamplesList.remove(dataset)

if doPlots:
   plots =       getPlots(samples, plotsDict, [selection[WP]['cuts'], regDefs['regDef' + notTight]], samplesList, plotList = plotsList, addOverFlowBin='both')
   fakePlots =  drawPlots(samples, plotsDict, [selection[WP]['cuts'], regDefs['regDef' + notTight]], samplesList, plotList = plotsList, plotLimits = [plotMin, 100], denoms = ["bkg"], noms = [dataset], fom = fom, fomLimits = [0,2.8], plotMin = plotMin, normalize = False, save = False)
   
   if doControlPlots:
      plots =       getPlots(samples, plotsDict, [selection[WP]['cuts'], regDefs['regDef' + notTight] + '_plus_prompt'], MCsamplesList, plotList = plotsList, addOverFlowBin='both')
      fakePlots2 = drawPlots(samples, plotsDict, [selection[WP]['cuts'], regDefs['regDef' + notTight] + '_plus_prompt'], MCsamplesList, plotList = plotsList, plotLimits = [plotMin, 100], fom = None, plotMin = plotMin, normalize = False, save = False)
      
      plots =       getPlots(samples, plotsDict, [selection[WP]['cuts'], regDefs['regDef' + notTight] + '_plus_fake'],  MCsamplesList, plotList = plotsList, addOverFlowBin='both')
      fakePlots3 = drawPlots(samples, plotsDict, [selection[WP]['cuts'], regDefs['regDef' + notTight] + '_plus_fake'],  MCsamplesList, plotList = plotsList, plotLimits = [plotMin, 100], fom = None, plotMin = plotMin, normalize = False, save = False)
   
   if save: #web address: http://www.hephy.at/user/mzarucki/plots
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

   yields['total'] =  Yields(samples, samplesList, cutInst = None, cuts = [selection[WP]['cuts'], regDefs['regDef' + notTight]],                  cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
   yields['prompt'] = Yields(samples, MCsamplesList, cutInst = None, cuts = [selection[WP]['cuts'], regDefs['regDef' + notTight] + '_plus_prompt'], cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
   yields['fake'] =   Yields(samples, MCsamplesList, cutInst = None, cuts = [selection[WP]['cuts'], regDefs['regDef' + notTight] + '_plus_fake'],   cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
 
   if not os.path.isfile("%s/fakeYields_%s%s.txt"%(yieldDir, region, suffix)):
      outfile = open("%s/fakeYields_%s%s.txt"%(yieldDir, region, suffix), "w")
      outfile.write("Fake Estimation Yields in %s %s\n"%(WP, region.title()))
      outfile.write("Sample        Total                Prompt                Fakes\n")

   yieldsList = MCsamplesList[:]
   yieldsList.append('Total')

   with open("%s/fakeYields_%s%s.txt"%(yieldDir, region, suffix), "a") as outfile:
      if dataset in samplesList: 
         outfile.write('data'.ljust(10) + str(yields['total'].yieldDictFull[dataset][regDefs['regDef' + notTight]].round(2)).ljust(25) + "\n")
      for samp in yieldsList:
         outfile.write(samp.ljust(10) +\
         str(yields['total'].yieldDictFull[samp][regDefs['regDef' + notTight]].round(2)).ljust(25) +\
         str(yields['prompt'].yieldDictFull[samp][regDefs['regDef' + notTight] + '_plus_prompt'].round(2)).ljust(25) +\
         str(yields['fake'].yieldDictFull[samp][regDefs['regDef' + notTight] + '_plus_fake'].round(2)) + "\n")

   outfile.close()
