# fakesUncertainties.py 
# Mateusz Zarucki 2017

import os
import numpy as np
from fakeInfo import *

script = "fakeRate.py" #os.path.basename(__file__) #sys.argv[0]

#Arguments
args = fakeParser(script)

lep = args.lep
region = args.region
doPlots = args.doPlots
#makeTables = args.makeTables
varBins = args.varBins
save = args.save
verbose = args.verbose

fakeInfo = fakeInfo(script, vars(args))

measurementType = 'data-EWK'
finalTag = "MR14"

lepton =      fakeInfo['lepton']
dataset =     fakeInfo['dataset']
samplesList = fakeInfo['samplesList']
samples =     fakeInfo['samples']
selection =   fakeInfo['selection']
bins =        fakeInfo['bins']

if save:
   baseDir =  fakeInfo['baseDir']
   saveTag =  fakeInfo['saveTag']

   tabledir = baseDir + "/applicationRegions/tables/%s"%finalTag
   makeDir(tabledir)

   resultsDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/final"
   resultsDir += "/%s/%s"%(saveTag, finalTag)

leptons = {'el':'Electron', 'mu':'Muon'}

leps = ['el', 'mu']
regions = ['sr1', 'sr1ab', 'sr1c']
etaBin = 'eta_lt_1p5'

# Open results pickle
yields = {}
for lep in leps:
   yields[lep] = {}
   for reg in regions:
      yields[lep][reg] = {}
      yields[lep][reg]['WttWeights'] =   pickle.load(open("%s/applicationRegions/application_%s/estimation/finalEstimate/SR/allBins/fakeTausConsidered/%s/LnotT/varBins/%s/fakesEstimationFinal_yields_%s_application_%s_%s.pkl"%(baseDir, reg, leptons[lep], etaBin, lep, reg, measurementType), "r"))
      yields[lep][reg]['noWttWeights'] = pickle.load(open("%s/applicationRegions/application_%s/estimation/finalEstimate/SR/allBins/fakeTausConsidered/%s/LnotT/varBins/%s/noWttWeights/fakesEstimationFinal_yields_%s_application_%s_%s.pkl"%(baseDir, reg, leptons[lep], etaBin, lep, reg, measurementType), "r"))

TLratios = pickle.load(open("%s/tightToLooseRatios_%s_%s_stat.pkl"%(resultsDir, finalTag, measurementType), "r"))

WPs = ['loose', 'tight']

# Systematics

sys = {'el':{'sr1':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}}, 'mu':{'sr1':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}}}
promptYldUnc = {'el':{'sr1':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}}, 'mu':{'sr1':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}}}
#promptYldUnc = 0.3 # systematic uncertainty on prompt yield

#for etaBin in ['eta_lt_1p5', 'eta_gt_1p5']:
for lep in leps:
   for reg in regions:
      for ptBin in yields[lep][reg]['WttWeights']['looseCR']['prompt']:
         if yields[lep][reg]['WttWeights']['looseCR']['prompt'][ptBin].val:
            promptYldUnc[lep][reg][ptBin] = abs(yields[lep][reg]['WttWeights']['looseCR']['prompt'][ptBin].val - yields[lep][reg]['noWttWeights']['looseCR']['prompt'][ptBin].val)/yields[lep][reg]['WttWeights']['looseCR']['prompt'][ptBin].val
         else:
            promptYldUnc[lep][reg][ptBin] = 0.
         
         #if yields[lep][reg]['WttWeights'][ptBin]['data']['tight'].val:
         #   TLsys_perc[lep][etaBin][ptBin] = promptSubUnc*sqrt(\
         #else:
         #   TLsys_perc[lep][etaBin][ptBin] = 0.
      
         sys[lep][reg][ptBin] = TLratios[lep][etaBin][binMaps[lep][str(ptBin)]].val*promptYldUnc[lep][reg][ptBin]
         #TLratios_sys[lep][etaBin][ptBin].sigma = TLsys[lep][etaBin][ptBin]
         #TLxcheck[lep][etaBin][ptBin] = (yields[lep][etaBin][ptBin]['data']['tight'].val-yields[lep][etaBin][ptBin]['prompt']['tight'].val)/(yields[lep][etaBin][ptBin]['data']['loose'].val-yields[lep][etaBin][ptBin]['prompt']['loose'].val) 

#overwrite = False
#Pickle results 
#pickleFileName = "%s/tightToLooseRatios_%s_%s_sys.pkl"%(resultsDir, finalTag, measurementType)
#if os.path.isfile(pickleFileName) and not overwrite:
#   print "%s file exists. Set overwrite to True to overwrite."%pickleFileName
#else:
#   pickleFile = open(pickleFileName, "w")
#   pickle.dump(TLratios_sys, pickleFile)
#   pickleFile.close()

# Prompt contamination
percPrompt = {'el':{'sr1':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}},'mu':{'sr1':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}}}
   
doPlots = 0 
doPromptCont = 1
makeTables = 1

if doPromptCont:
   binNames = {}
   for lep in leps:
      #binNames[lep] = [binMaps[lep][i] for i in binMaps[lep]]
      #for etaBin in ['eta_lt_1p5', 'eta_gt_1p5']:
      for reg in regions:
         if makeTables:
            rows = []
            listTitle = ['Bin', 'T-L Ratio (stat.)', 'Data Yield (L!T)', 'Prompt Yield (L!T)', '\% Prompt Cont. (L!T)', 'Sys. unc. Prompt', 'Sys. unc. Est.']
            rows.append(listTitle)
         for ptBin in yields[lep][reg]['WttWeights']['looseCR']['total']: #binNames[lep]:
            if binMaps[lep][str(ptBin)] == "0_5" or binMaps[lep][str(ptBin)] == "0_3p5": continue
            if yields[lep][reg]['WttWeights']['looseCR']['total'][ptBin].val:
               percPrompt[lep][reg][ptBin] = yields[lep][reg]['WttWeights']['looseCR']['prompt'][ptBin].val/yields[lep][reg]['WttWeights']['looseCR']['total'][ptBin].val*100
            else:
               percPrompt[lep][reg][ptBin] = 0.
            
            if makeTables:
               row = [binMaps[lep][str(ptBin)], 
               TLratios[lep][etaBin][binMaps[lep][str(ptBin)]].round(3),
               yields[lep][reg]['WttWeights']['looseCR']['total'][ptBin].round(3), 
               yields[lep][reg]['WttWeights']['looseCR']['prompt'][ptBin].round(3), 
               "%.1f"%percPrompt[lep][reg][ptBin],
               "%.2f"%(promptYldUnc[lep][reg][ptBin]*100),
               "%.4f"%(sys[lep][reg][ptBin]*100)]
               rows.append(row)
               
         makeSimpleLatexTable(rows, "FRestTable_%s_%s_%s"%(finalTag, lep, reg), tabledir)

if doPlots:
   for plot in ['data', 'MC']:

      #Sets TDR style
      setup_style()
 
      #arrays for plot
      bins = [int(x) for x in percPrompt['MC']['loose']]

      percPrompt_arr = {plot:{'loose':{}, 'tight':{}}}
      for WP in WPs:
         percPrompt_arr[plot][WP] = []
  
      percPrompt_err_arr = []
 
      for WP in WPs:
         for ptBin in bins:
            percPrompt_arr[plot][WP].append(percPrompt[plot][WP][ptBin])
            percPrompt_err_arr.append(0)#percPromptEstimate[ptBin].sigma)
      
      c1 = ROOT.TCanvas("c1", "percPrompt")
      c1.SetGrid() #adds a grid to the canvas
      #c1.SetFillColor(42)
      c1.GetFrame().SetFillColor(21)
      c1.GetFrame().SetBorderSize(12)
      
      gr1 = ROOT.TGraphErrors(len(bins), np.array(bins, 'float64'), np.array(percPrompt_arr[plot]['loose'], 'float64'), np.array([0]), np.array(percPrompt_err_arr, 'float64')) #graph object with error bars using arrays of data
      gr1.SetTitle("Prompt Contamination in %s for %s"%(region, plot))
      gr1.SetMarkerColor(ROOT.kBlue)
      gr1.SetMarkerStyle(ROOT.kFullCircle)
      gr1.SetMarkerSize(1)
      gr1.GetXaxis().SetTitle("%s p_{T}"%lepton)
      gr1.GetYaxis().SetTitle("Percentage of Prompts")
      gr1.GetXaxis().CenterTitle()
      gr1.GetYaxis().CenterTitle()
      gr1.GetXaxis().SetTitleSize(0.04)
      gr1.GetYaxis().SetTitleSize(0.04)
      gr1.GetYaxis().SetNdivisions(512);
      gr1.GetXaxis().SetTitleOffset(1.4)
      gr1.GetYaxis().SetTitleOffset(1.6)
      gr1.SetMinimum(0)
      gr1.SetMaximum(140)
      
      for i, binName in enumerate(binNames[lep]):
         binIndex = gr1.GetXaxis().FindBin(i+1)
         gr1.GetXaxis().SetBinLabel(binIndex, binName)

      gr1.Draw("AP") #plots the graph with axes and points
      
      gr2 = ROOT.TGraphErrors(len(bins), np.array(bins, 'float64'), np.array(percPrompt_arr[plot]['tight'], 'float64'), np.array([0]), np.array(percPrompt_err_arr, 'float64')) #graph object with error bars using arrays of data
      gr2.SetMarkerColor(ROOT.kRed)
      gr2.SetMarkerStyle(ROOT.kFullCircle)
      gr2.SetMarkerSize(1)
      gr2.Draw("Psame")
      
      leg = ROOT.TLegend(0.20, 0.8, 0.75, 0.925) #x1,y1,x2,y2
      #leg = ROOT.TLegend(0.600, 0.8, 0.95, 0.925) #x1,y1,x2,y2
      leg.AddEntry(gr1, "% Loose Prompt", "P")
      leg.AddEntry(gr2, "% Tight Prompt", "P")
      leg.SetTextSize(0.03)
      leg.Draw()
      
      #Save to Web
      c1.SaveAs("%s/percPrompt%s_%s.png"%(savedir, suffix, plot))
      c1.SaveAs("%s/percPrompt%s_%s.pdf"%(savedir, suffix, plot))
      c1.SaveAs("%s/percPrompt%s_%s.root"%(savedir, suffix, plot))
