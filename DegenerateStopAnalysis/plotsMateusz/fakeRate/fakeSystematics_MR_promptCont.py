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
   tabledir = baseDir + "/measurementRegions/systematics/%s"%finalTag
   makeDir(tabledir)

   resultsDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/final"
   resultsDir += "/%s/%s"%(saveTag, finalTag)

leps = ['el', 'mu']

# Open results pickle
yields = {}
yields['WttWeights'] = pickle.load(open("%s/yields_%s_%s.pkl"%(resultsDir, finalTag, measurementType), "r"))
yields['noWttWeights'] = pickle.load(open("%s/noWttWeights/yields_%s_%s.pkl"%(resultsDir, finalTag, measurementType), "r"))
TLratios = pickle.load(open("%s/tightToLooseRatios_%s_%s_stat.pkl"%(resultsDir, finalTag, measurementType), "r"))

WPs = ['loose', 'tight']

# Systematics on TL ratio

promptYldUnc = {'el':{}, 'mu':{}} # systematic uncertainty on prompt yield
#promptYldUnc = 0.3 # systematic uncertainty on prompt yield

TLratios_sys = copy.deepcopy(TLratios) 
TLsys = {'el':{}, 'mu':{}}
TLsys_perc = {'el':{}, 'mu':{}}
#TLxcheck = {'el':{}, 'mu':{}}

for lep in leps:
   for etaBin in ['eta_lt_1p5', 'eta_gt_1p5']:
      promptYldUnc[lep][etaBin] = {'loose':{}, 'tight':{}}
      TLsys[lep][etaBin] = {}
      TLsys_perc[lep][etaBin] = {}
      #TLxcheck[lep][etaBin] = {}
      for ptBin in yields['WttWeights'][lep][etaBin].keys():
         
         for WP in WPs:
            if yields['WttWeights'][lep][etaBin][ptBin]['prompt'][WP].val:
               promptYldUnc[lep][etaBin][WP][ptBin] = abs(yields['WttWeights'][lep][etaBin][ptBin]['prompt'][WP].val - yields['noWttWeights'][lep][etaBin][ptBin]['prompt'][WP].val)/yields['WttWeights'][lep][etaBin][ptBin]['prompt'][WP].val
            else:
               promptYldUnc[lep][etaBin][WP][ptBin] = 0.

         if yields['WttWeights'][lep][etaBin][ptBin]['data']['tight'].val:
            TLsys_perc[lep][etaBin][ptBin] = sqrt(\
               pow(((promptYldUnc[lep][etaBin]['tight'][ptBin]*yields['WttWeights'][lep][etaBin][ptBin]['prompt']['tight'].val)/(yields['WttWeights'][lep][etaBin][ptBin]['data']['tight'].val-yields['WttWeights'][lep][etaBin][ptBin]['prompt']['tight'].val)), 2) +\
               pow(((promptYldUnc[lep][etaBin]['loose'][ptBin]*yields['WttWeights'][lep][etaBin][ptBin]['prompt']['loose'].val)/(yields['WttWeights'][lep][etaBin][ptBin]['data']['loose'].val-yields['WttWeights'][lep][etaBin][ptBin]['prompt']['loose'].val)), 2))
         else:
            TLsys_perc[lep][etaBin][ptBin] = 0.

         TLsys[lep][etaBin][ptBin] = TLratios[lep][etaBin][ptBin].val*TLsys_perc[lep][etaBin][ptBin]
         TLratios_sys[lep][etaBin][ptBin].sigma = TLsys[lep][etaBin][ptBin]
         #TLxcheck[lep][etaBin][ptBin] = (yields[lep][etaBin][ptBin]['data']['tight'].val-yields[lep][etaBin][ptBin]['prompt']['tight'].val)/(yields[lep][etaBin][ptBin]['data']['loose'].val-yields[lep][etaBin][ptBin]['prompt']['loose'].val) 

overwrite = False
#Pickle results 
pickleFileName = "%s/tightToLooseRatios_%s_%s_sys.pkl"%(resultsDir, finalTag, measurementType)
if os.path.isfile(pickleFileName) and not overwrite:
   print "%s file exists. Set overwrite to True to overwrite."%pickleFileName
else:
   pickleFile = open(pickleFileName, "w")
   pickle.dump(TLratios_sys, pickleFile)
   pickleFile.close()

# Prompt contamination
percPrompt = {'el':{'loose':{}, 'tight':{}},'mu':{'loose':{}, 'tight':{}},}
   
doPlots = 0 
doTable = 1
makeTables = 1

if doTable:
   binNames = {}
   for lep in leps:
      binNames[lep] = [binMaps[lep][i] for i in binMaps[lep]]
      for etaBin in ['eta_lt_1p5', 'eta_gt_1p5']:
         if makeTables:
            rows = []
            listTitle = ['Bin', 'Data Yield (Loose)', 'Prompt Yield (Loose)', '\% Prompt Cont. (Loose)', 'Data Yield (Tight)', 'Prompt Yield (Tight)', '\% Prompt Cont. (Tight)', 'T-L Ratio (stat.)', 'Sys. unc. (\%)', 'Sys. unc.']
            rows.append(listTitle)
         for ptBin in binNames[lep]:
            if ptBin == "0_5" or ptBin == "0_3p5": continue
            for WP in WPs:
               if yields['WttWeights'][lep][etaBin][ptBin]['data'][WP].val:
                  percPrompt[lep][WP][ptBin] = yields['WttWeights'][lep][etaBin][ptBin]['prompt'][WP].val/yields['WttWeights'][lep][etaBin][ptBin]['data'][WP].val*100
               else:
                  percPrompt[lep][WP][ptBin] = 0.
            
            if makeTables:
               row = [ptBin, 
               yields['WttWeights'][lep][etaBin][ptBin]['data']['loose'].round(4), 
               yields['WttWeights'][lep][etaBin][ptBin]['prompt']['loose'].round(4), 
               "%.1f"%percPrompt[lep]['loose'][ptBin],
               yields['WttWeights'][lep][etaBin][ptBin]['data']['tight'].round(4), 
               yields['WttWeights'][lep][etaBin][ptBin]['prompt']['tight'].round(4), 
               "%.1f"%percPrompt[lep]['tight'][ptBin],
               TLratios[lep][etaBin][ptBin].round(4),
               "%.2f"%(TLsys_perc[lep][etaBin][ptBin]*100),
               "%.4f"%TLsys[lep][etaBin][ptBin]]
               rows.append(row)
               
         makeSimpleLatexTable(rows, "TLpromptSubSysTable_%s_%s_%s"%(finalTag, lep, etaBin), tabledir)

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
