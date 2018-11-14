# promptContamination.py 
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

lepton =      fakeInfo['lepton']
dataset =     fakeInfo['dataset']
samplesList = fakeInfo['samplesList']
samples =     fakeInfo['samples']
selection =   fakeInfo['selection']
bins =        fakeInfo['bins']

if save:
   baseDir =  fakeInfo['baseDir']
   savedir =  fakeInfo['savedir']
   yieldDir = fakeInfo['yieldDir']
   suffix =   fakeInfo['suffix']

# Open results pickle
pklPath = {}
pklPath['total'] = "%s/MCyields_total%s.pkl"%(yieldDir,suffix)
pklPath['prompt'] = "%s/MCyields_prompt%s.pkl"%(yieldDir,suffix)

binYields = {'data':{'loose':{'pt':{}}, 'tight':{'pt':{}}}}
#binYields['MC'] =  pickle.load(open(pklPath['MC'], "r"))
binYields.update(pickle.load(open(pklPath['prompt'], "r")))

txtPath = "%s/binContents_%s_total%s.txt"%(yieldDir, dataset, suffix)

with open(txtPath) as f:
   #next(f)
   lines = f.readlines()[2:]
   for i, line in enumerate(lines):
      #print i, line
      line = line.split('|')
      binYields['data']['loose']['pt'][i+1] = float(line[1].split('+-')[0])
      binYields['data']['tight']['pt'][i+1] = float(line[2].split('+-')[0])
      if line[0] in ['0-5', '0-3'] and i > 0: break

percPrompt = {'MC':{'loose':{}, 'tight':{}}, 'data':{'loose':{}, 'tight':{}}}
   
WPs = ['loose', 'tight']

for WP in WPs:
   for bin in binYields['prompt'][WP]['pt']:
      if binYields['total'][WP]['pt'][bin].val:
         percPrompt['MC'][WP][bin] = binYields['prompt'][WP]['pt'][bin].val/binYields['total'][WP]['pt'][bin].val*100 
      if binYields['data'][WP]['pt'][bin]:
         percPrompt['data'][WP][bin] = binYields['prompt'][WP]['pt'][bin].val/binYields['data'][WP]['pt'][bin]*100

#print makeLine()
#print binYields
#print percPrompt
#print makeLine()

if lep == "mu":
   binNames = ["0-3.5", "3.5-5", "5-12", "12-20", "20-30", "30-50", "50-80","80-200", ">200"]
else:
   binNames = ["0-5", "5-12", "12-20", "20-30", "30-50", "50-80","80-200", ">200"]
 
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
         for bin in bins:
            percPrompt_arr[plot][WP].append(percPrompt[plot][WP][bin])
            percPrompt_err_arr.append(0)#percPromptEstimate[bin].sigma)
      
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
      
      for i, binName in enumerate(binNames):
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

#if makeTables:
#
#   #Ratios
#   for channel in corr:
#      ZinvRows = []
#      listTitle = ['CT', 'Zpeak_data', 'Zpeak_dy', 'Zpeak_tt', 'Zpeak_vv', 'Nel_data', 'Nel_dy', 'Nel_tt', 'Nel_vv', 'Nmu_data', 'Nmu_dy', 'Nmu_tt', 'Nmu_vv']
#      ZinvRows.append(listTitle)
#      for CT2 in CTs:
#         ZinvRow = [CT2, 
#         ZinvYields[channel]['CT' + CT2]['Zpeak']['data'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Zpeak']['dy'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Zpeak']['tt'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Zpeak']['vv'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Nel']['data'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Nel']['dy'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Nel']['tt'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Nel']['vv'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Nmu']['data'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Nmu']['dy'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Nmu']['tt'].round(4), 
#         ZinvYields[channel]['CT' + CT2]['Nmu']['vv'].round(4)] 
#         ZinvRows.append(ZinvRow)
#      
#      makeSimpleLatexTable(ZinvRows, "ZinvYields_" + channel, tabledir)
#
#      ZinvRows = []
#      listTitle = ['CT', 'Zpeak_dataMC', 'prob_el_data', 'prob_el_MC', 'prob_el_dataMC', 'prob_mu_data', 'prob_mu_MC', 'prob_mu_dataMC']
#      #listTitle.extend(ZinvRatios[channel]['CT' + CT2].keys())
#      ZinvRows.append(listTitle)
#      for CT2 in CTs:
#         ZinvRow = [CT2, ZinvRatios[channel]['CT' + CT2]['Zpeak_dataMC'].round(4), 
#                         ZinvRatios[channel]['CT' + CT2]['prob_el_data'].round(4), ZinvRatios[channel]['CT' + CT2]['prob_el_MC'].round(4), ZinvRatios[channel]['CT' + CT2]['prob_el_dataMC'].round(4),   
#                         ZinvRatios[channel]['CT' + CT2]['prob_mu_data'].round(4), ZinvRatios[channel]['CT' + CT2]['prob_mu_MC'].round(4), ZinvRatios[channel]['CT' + CT2]['prob_mu_dataMC'].round(4)]
#         #ZinvRow.extend([x.round(4) for x in ZinvRatios[channel]['CT' + CT2].values()])
#         ZinvRows.append(ZinvRow)
#      
#      makeSimpleLatexTable(ZinvRows, "ZinvRatios_" + channel, tabledir)
#      
#      ZinvRows = []
#      listTitle = ['CT', 'Correction electrons', 'Correction muons']
#      ZinvRows.append(listTitle)
#      for CT2 in CTs:
#         ZinvRow = [CT2, corr[channel]['CT' + CT2]['electrons'].round(3), corr[channel]['CT' + CT2]['muons'].round(3)]
#         #ZinvRow.extend([x.round(4) for x in ZinvRatios[channel]['CT' + CT2].values()])
#         ZinvRows.append(ZinvRow)
#      
#      makeSimpleLatexTable(ZinvRows, "ZinvCorrections_" + channel, tabledir)
