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
regions = ['sr1', 'sr1a', 'sr1b', 'sr1ab', 'sr1c', 'sr2']

# Open results pickle
yields = {}
for lep in leps:
   yields[lep] = {}
   for etaBin in ['eta_lt_1p5', 'eta_gt_1p5']:
      yields[lep][etaBin] = {}
   for reg in regions:
      if 'sr1' in reg:   etaBins = ['eta_lt_1p5']
      elif 'sr2' in reg: etaBins = ['eta_lt_1p5', 'eta_gt_1p5']
      for etaBin in etaBins:
         yields[lep][etaBin][reg] = {}
         yields[lep][etaBin][reg]['WttWeights'] =   pickle.load(open("%s/applicationRegions/application_%s/estimation/finalEstimate/SR/allBins/fakeTausConsidered/%s/LnotT/varBins/%s/fakesEstimationFinal_yields_%s_application_%s_%s.pkl"%(baseDir, reg, leptons[lep], etaBin, lep, reg, measurementType), "r"))
         yields[lep][etaBin][reg]['noWttWeights'] = pickle.load(open("%s/applicationRegions/application_%s/estimation/finalEstimate/SR/allBins/fakeTausConsidered/%s/LnotT/varBins/%s/noWttWeights/fakesEstimationFinal_yields_%s_application_%s_%s.pkl"%(baseDir, reg, leptons[lep], etaBin, lep, reg, measurementType), "r"))

TLratios =     pickle.load(open("%s/tightToLooseRatios_%s_%s_stat.pkl"%(resultsDir, finalTag, measurementType), "r"))
TLratios_sys = pickle.load(open("%s/tightToLooseRatios_%s_%s_sys.pkl"%(resultsDir, finalTag, measurementType), "r"))

WPs = ['loose', 'tight']

# Estimate
LnT = {'el':{'sr1':{}, 'sr1a':{}, 'sr1b':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}}, 
       'mu':{'sr1':{}, 'sr1a':{}, 'sr1b':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}}}

fakesEstimate = {'el':{'sr1':{}, 'sr1a':{}, 'sr1b':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}}, 
                 'mu':{'sr1':{}, 'sr1a':{}, 'sr1b':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}}}

# Systematics

relErrEstimate = {'el':{'sr1':{}, 'sr1a':{}, 'sr1b':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}}, 
                  'mu':{'sr1':{}, 'sr1a':{}, 'sr1b':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}}}
promptYldRelUnc = {'el':{'sr1':{}, 'sr1a':{}, 'sr1b':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}}, 
                   'mu':{'sr1':{}, 'sr1a':{}, 'sr1b':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}}}
#promptYldRelUnc = 0.3 # systematic uncertainty on prompt yield

# Prompt contamination
percPrompt = {'el':{'sr1':{}, 'sr1a':{}, 'sr1b':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}},
              'mu':{'sr1':{}, 'sr1a':{}, 'sr1b':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}}}
   

#for etaBin in ['eta_lt_1p5', 'eta_gt_1p5']:
for lep in leps:
   for reg in regions:
      if 'sr1' in reg:   etaBins = ['eta_lt_1p5']
      elif 'sr2' in reg: etaBins = ['eta_lt_1p5', 'eta_gt_1p5']

      for etaBin in etaBins:
         LnT[lep][reg][etaBin] = {}
         relErrEstimate[lep][reg][etaBin] = {}
         fakesEstimate[lep][reg][etaBin] = {}
         promptYldRelUnc[lep][reg][etaBin] = {}
         percPrompt[lep][reg][etaBin] = {}
         for ptBin in yields[lep][etaBin][reg]['WttWeights']['looseCR']['prompt']:
            if ptBin == 1: continue

            LnT[lep][reg][etaBin][ptBin] = {'data' : yields[lep][etaBin][reg]['WttWeights']['looseCR']['total'][ptBin],
                                          'prompt' : yields[lep][etaBin][reg]['WttWeights']['looseCR']['prompt'][ptBin]}

            LnT[lep][reg][etaBin][ptBin]['data-prompt'] = (LnT[lep][reg][etaBin][ptBin]['data'] - LnT[lep][reg][etaBin][ptBin]['prompt'])

            relErrEstimate[lep][reg][etaBin][ptBin] = {'stat':{}, 'sys':{}} 
            
            if TLratios[lep][etaBin][binMaps[lep][str(ptBin)]].val: 
               relErrEstimate[lep][reg][etaBin][ptBin]['stat']['TLratio'] = TLratios[lep][etaBin][binMaps[lep][str(ptBin)]].sigma/TLratios[lep][etaBin][binMaps[lep][str(ptBin)]].val
            else:
               relErrEstimate[lep][reg][etaBin][ptBin]['stat']['TLratio'] = 0. 
   
            if TLratios_sys[lep][etaBin][binMaps[lep][str(ptBin)]].val: 
               relErrEstimate[lep][reg][etaBin][ptBin]['sys']['TLratio'] =  TLratios_sys[lep][etaBin][binMaps[lep][str(ptBin)]].sigma/TLratios[lep][etaBin][binMaps[lep][str(ptBin)]].val
            else:
               relErrEstimate[lep][reg][etaBin][ptBin]['sys']['TLratio'] = 0. 
          
            # Estimate 
            TF = TLratios[lep][etaBin][binMaps[lep][str(ptBin)]]/(1-TLratios[lep][etaBin][binMaps[lep][str(ptBin)]].val)
            fakesEstimate[lep][reg][etaBin][ptBin] = TF*LnT[lep][reg][etaBin][ptBin]['data-prompt'] 
 
            # Systematic related to prompt contamination in L!T region
            if yields[lep][etaBin][reg]['WttWeights']['looseCR']['prompt'][ptBin].val:
               promptYldRelUnc[lep][reg][etaBin][ptBin] = abs(yields[lep][etaBin][reg]['WttWeights']['looseCR']['prompt'][ptBin].val - yields[lep][etaBin][reg]['noWttWeights']['looseCR']['prompt'][ptBin].val)/yields[lep][etaBin][reg]['WttWeights']['looseCR']['prompt'][ptBin].val
            else:                               
               promptYldRelUnc[lep][reg][etaBin][ptBin] = 0.
            
            if LnT[lep][reg][etaBin][ptBin]['data-prompt'].val: 
               relErrEstimate[lep][reg][etaBin][ptBin]['sys']['promptCont'] = (promptYldRelUnc[lep][reg][etaBin][ptBin]*LnT[lep][reg][etaBin][ptBin]['prompt'].val)/LnT[lep][reg][etaBin][ptBin]['data-prompt'].val
            
               # Systematic related to statistical uncertainty of data and prompts
               relErrEstimate[lep][reg][etaBin][ptBin]['stat'].update({
                  'data':(LnT[lep][reg][etaBin][ptBin]['data'].sigma)/LnT[lep][reg][etaBin][ptBin]['data-prompt'].val,
                  'prompt':(LnT[lep][reg][etaBin][ptBin]['prompt'].sigma)/LnT[lep][reg][etaBin][ptBin]['data-prompt'].val,
                  'data-prompt':sqrt(LnT[lep][reg][etaBin][ptBin]['data'].sigma**2 + LnT[lep][reg][etaBin][ptBin]['prompt'].sigma**2)/LnT[lep][reg][etaBin][ptBin]['data-prompt'].val
                  }) 
              
               # Total Stat. Unc. 
               relErrEstimate[lep][reg][etaBin][ptBin]['stat']['total'] = fakesEstimate[lep][reg][etaBin][ptBin].sigma/fakesEstimate[lep][reg][etaBin][ptBin].val
               # Total Sys. Unc. 
               relErrEstimate[lep][reg][etaBin][ptBin]['sys']['total'] = sqrt(relErrEstimate[lep][reg][etaBin][ptBin]['sys']['TLratio']**2 + relErrEstimate[lep][reg][etaBin][ptBin]['sys']['promptCont']**2) 
               # Total Unc.
               relErrEstimate[lep][reg][etaBin][ptBin]['total'] = sqrt(relErrEstimate[lep][reg][etaBin][ptBin]['sys']['total']**2 + relErrEstimate[lep][reg][etaBin][ptBin]['stat']['total']**2) 

# SR2
reg = 'sr2'
for lep in leps:
   fakesEstimate[lep][reg]['etaCombined'] = {} 
   relErrEstimate[lep][reg]['etaCombined'] = {} 
   for ptBin in yields[lep][etaBin][reg]['WttWeights']['looseCR']['prompt']:
      if ptBin == 1: continue
      fakesEstimate[lep][reg]['etaCombined'][ptBin] = {} 
      relErrEstimate[lep][reg]['etaCombined'][ptBin] = {'stat':{}, 'sys':{}} 

      # Estimate
      fakesEstimate[lep][reg]['etaCombined'][ptBin] = fakesEstimate[lep][reg]['eta_lt_1p5'][ptBin] + fakesEstimate[lep][reg]['eta_gt_1p5'][ptBin] 
      
      # Total Stat. Unc. 
      if fakesEstimate[lep][reg]['etaCombined'][ptBin].val: 
         relErrEstimate[lep][reg]['etaCombined'][ptBin]['stat']['total'] = fakesEstimate[lep][reg]['etaCombined'][ptBin].sigma/fakesEstimate[lep][reg]['etaCombined'][ptBin].val
      else:
         relErrEstimate[lep][reg]['etaCombined'][ptBin]['stat']['total'] = 0. 
      #print "sr2 stat. err:", relErrEstimate[lep][reg]['etaCombined'][ptBin]['stat']['total']
      #print "sr2 stat. err x-check:", sqrt((relErrEstimate[lep][reg]['eta_lt_1p5'][ptBin]['stat']['total']*fakesEstimate[lep][reg]['eta_lt_1p5'][ptBin].val)**2 + (relErrEstimate[lep][reg]['eta_gt_1p5'][ptBin]['stat']['total']*fakesEstimate[lep][reg]['eta_gt_1p5'][ptBin].val)**2)/(fakesEstimate[lep][reg]['etaCombined'][ptBin].val)
      
      # Total Sys. Unc. 
      relErrEstimate[lep][reg]['etaCombined'][ptBin]['sys']['total'] = sqrt((relErrEstimate[lep][reg]['eta_lt_1p5'][ptBin]['sys']['total']*fakesEstimate[lep][reg]['eta_lt_1p5'][ptBin].val)**2 + (relErrEstimate[lep][reg]['eta_gt_1p5'][ptBin]['sys']['total']*fakesEstimate[lep][reg]['eta_gt_1p5'][ptBin].val)**2)/(fakesEstimate[lep][reg]['etaCombined'][ptBin].val)
      
      # Total Unc. 
      relErrEstimate[lep][reg]['etaCombined'][ptBin]['total'] = sqrt((relErrEstimate[lep][reg]['eta_lt_1p5'][ptBin]['total']*fakesEstimate[lep][reg]['eta_lt_1p5'][ptBin].val)**2 + (relErrEstimate[lep][reg]['eta_gt_1p5'][ptBin]['total']*fakesEstimate[lep][reg]['eta_gt_1p5'][ptBin].val)**2)/(fakesEstimate[lep][reg]['etaCombined'][ptBin].val)
         
#overwrite = False
#Pickle results 
#pickleFileName = "%s/tightToLooseRatios_%s_%s_sys.pkl"%(resultsDir, finalTag, measurementType)
#if os.path.isfile(pickleFileName) and not overwrite:
#   print "%s file exists. Set overwrite to True to overwrite."%pickleFileName
#else:
#   pickleFile = open(pickleFileName, "w")
#   pickle.dump(TLratios_sys, pickleFile)
#   pickleFile.close()

doPlots = 0 
makeTables = 1

binNames = {}

for lep in leps:
   #binNames[lep] = [binMaps[lep][i] for i in binMaps[lep]]
   for reg in regions:
      if 'sr1' in reg:   etaBins = ['eta_lt_1p5']
      elif 'sr2' in reg: etaBins = ['eta_lt_1p5', 'eta_gt_1p5', 'etaCombined']
      #if 'sr1' in reg:   etaBin = 'eta_lt_1p5'
      #elif 'sr2' in reg: etaBin = 'etaCombined'
      for etaBin in etaBins:
         if makeTables:
            rows = []
            listTitle = ['Bin', 'T-L Ratio (Stat.)', 'Rel. Err. Est. T-L Ratio Stat. (\%)', 'T-L Ratio (Sys.)', 'Rel. Err. Est. T-L Ratio Sys. (\%)', 'L!T Data Yield (Stat.)', 'L!T Prompt Yield (Stat.)', 'L!T \% Prompt Cont.', 'L!T Data-Prompt Yield (Stat.)', 'Rel. Err. Est. Data Stat. (\%)', 'Rel. Err. Est. Prompt Stat. (\%)', 'Rel. Err. Est. Data-Prompt Stat. (\%)', 'Estimate ($\pm$ Stat.)', 'Rel. Err. Est. (Stat.)', 'Sys. Unc. Prompt (\%)', 'Rel. Err. Est. Prompt Sys. (\%)']
            rows.append(listTitle)
         for ptBin in yields[lep]['eta_lt_1p5'][reg]['WttWeights']['looseCR']['total']: #binNames[lep]:
            if binMaps[lep][str(ptBin)] == "0_5" or binMaps[lep][str(ptBin)] == "0_3p5": continue
            if not 'etaCombined' in etaBin:
               if yields[lep][etaBin][reg]['WttWeights']['looseCR']['total'][ptBin].val:
                  percPrompt[lep][reg][etaBin][ptBin] = yields[lep][etaBin][reg]['WttWeights']['looseCR']['prompt'][ptBin].val/yields[lep][etaBin][reg]['WttWeights']['looseCR']['total'][ptBin].val*100
               else:
                  percPrompt[lep][reg][etaBin][ptBin] = 0.
            
            if makeTables and not 'sr2' in reg:
               row = [binMaps[lep][str(ptBin)], 
               TLratios[lep][etaBin][binMaps[lep][str(ptBin)]].round(3),
               "%.1f"%(relErrEstimate[lep][reg][etaBin][ptBin]['stat']['TLratio']*100),
               TLratios_sys[lep][etaBin][binMaps[lep][str(ptBin)]].round(3),
               "%.1f"%(relErrEstimate[lep][reg][etaBin][ptBin]['sys']['TLratio']*100),
               LnT[lep][reg][etaBin][ptBin]['data'].round(3), 
               LnT[lep][reg][etaBin][ptBin]['prompt'].round(3), 
               "%.1f"%percPrompt[lep][reg][etaBin][ptBin],
               LnT[lep][reg][etaBin][ptBin]['data-prompt'].round(3), 
               "%.1f"%(relErrEstimate[lep][reg][etaBin][ptBin]['stat']['data']*100),
               "%.1f"%(relErrEstimate[lep][reg][etaBin][ptBin]['stat']['prompt']*100),
               "%.1f"%(relErrEstimate[lep][reg][etaBin][ptBin]['stat']['data-prompt']*100),
               fakesEstimate[lep][reg][etaBin][ptBin].round(3),
               "%.1f"%(relErrEstimate[lep][reg][etaBin][ptBin]['stat']['total']*100),
               "%.1f"%(promptYldRelUnc[lep][reg][etaBin][ptBin]*100),
               "%.1f"%(relErrEstimate[lep][reg][etaBin][ptBin]['sys']['promptCont']*100)]
               rows.append(row)
               
         if makeTables and not 'sr2' in reg:
            makeSimpleLatexTable(rows, "FRestTable_%s_%s_%s_%s"%(finalTag, lep, reg, etaBin), tabledir)
         
         if makeTables:
            rows = []
            if not 'etaCombined' in etaBin:
               listTitle = ['Bin', 'T-L Ratio ($\pm$ Stat. $\pm$ Sys.)', 'Rel. Err. Est. T-L Ratio Stat. (\%)', 'Rel. Err. Est. L!T Data-Prompt Stat. (\%)', 'Rel. Err. Est. Prompt Sys. (\%)', 'Rel. Err. Est. T-L Ratio Sys. (\%)', 'Rel. Err. Est. (Stat.)', 'Rel. Err. Est. (Sys.)', 'Rel. Err. Est. (Tot.)', 'Estimate ($\pm$ Stat. $\pm$ Sys.)']
            else:
               listTitle = ['Bin', 'Rel. Err. Est. (Stat.)', 'Rel. Err. Est. (Sys.)', 'Rel. Err. Est. (Tot.)', 'Estimate ($\pm$ Stat. $\pm$ Sys.)']
            rows.append(listTitle)
         for ptBin in yields[lep]['eta_lt_1p5'][reg]['WttWeights']['looseCR']['total']: #binNames[lep]:
            if binMaps[lep][str(ptBin)] == "0_5" or binMaps[lep][str(ptBin)] == "0_3p5": continue
            if not 'etaCombined' in etaBin:
               if yields[lep][etaBin][reg]['WttWeights']['looseCR']['total'][ptBin].val:
                  percPrompt[lep][reg][etaBin][ptBin] = yields[lep][etaBin][reg]['WttWeights']['looseCR']['prompt'][ptBin].val/yields[lep][etaBin][reg]['WttWeights']['looseCR']['total'][ptBin].val*100
               else:
                  percPrompt[lep][reg][ptBin] = 0.
            
            if makeTables:
               row = [binMaps[lep][str(ptBin)]]
               if not 'etaCombined' in etaBin:
                  row.extend([str(TLratios[lep][etaBin][binMaps[lep][str(ptBin)]].round(3)) + "$\pm$" + str(TLratios_sys[lep][etaBin][binMaps[lep][str(ptBin)]].round(3).sigma),
                  "%.1f"%(relErrEstimate[lep][reg][etaBin][ptBin]['stat']['TLratio']*100),
                  "%.1f"%(relErrEstimate[lep][reg][etaBin][ptBin]['stat']['data-prompt']*100),
                  "%.1f"%(relErrEstimate[lep][reg][etaBin][ptBin]['sys']['TLratio']*100),
                  "%.1f"%(relErrEstimate[lep][reg][etaBin][ptBin]['sys']['promptCont']*100)])
               row.extend([\
               "%.1f"%(relErrEstimate[lep][reg][etaBin][ptBin]['stat']['total']*100),
               "%.1f"%(relErrEstimate[lep][reg][etaBin][ptBin]['sys']['total']*100),
               "%.1f"%(relErrEstimate[lep][reg][etaBin][ptBin]['total']*100),
               str(fakesEstimate[lep][reg][etaBin][ptBin].round(3)) + "$\pm$" + "%.1f"%(relErrEstimate[lep][reg][etaBin][ptBin]['sys']['total']*fakesEstimate[lep][reg][etaBin][ptBin].val)])
               rows.append(row)
               
         makeSimpleLatexTable(rows, "FRestTable_%s_%s_%s_%s_relErrEstimate"%(finalTag, lep, reg, etaBin), tabledir)
     
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
