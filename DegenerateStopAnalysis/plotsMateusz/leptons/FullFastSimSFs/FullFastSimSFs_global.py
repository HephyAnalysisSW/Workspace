# FullFastSimSFs_global.py
# Determination of global FullSim-FastSim SFs using indicies
# Mateusz Zarucki 2017

import os
from FullFastSimSFs_info import * 

#ROOT.gStyle.SetOptStat(0)

script = os.path.basename(__file__) #sys.argv[0]

#Arguments
args = getParser(script)

#Arguments
lep = args.lep
sample = args.sample
standardBins = args.standardBins
varBins = args.varBins
logy = args.logy
save = args.save
verbose = args.verbose

info = getInfo(script, vars(args))

lepton =        info['lepton']
samples =       info['samples']
bins =          info['bins']
genFilterEffs = info['genFilterEffs']

genFilterEff = str(genFilterEffs[sample])

if 'allFullSim' in sample:
   trees = {'FullSim':samples['allFullSim'].tree, 'FastSim': info['allFastSim']}
else:
   trees = {'FullSim':samples[sample].tree, 'FastSim':samples['t2tt' + samples[sample].name.replace('S','')].tree}

if verbose:
   print makeLine()
   print "Using samples:", trees 
   print makeLine()

if save:
   savedir = info['savedir']
   suffix =  info['suffix']

# Cuts and Weights
cuts_weights = CutsWeights(samples, cutWeightOptions)

lepTag = cuts_weights.cuts.settings['lepTag'] # cutWeightOptions['settings']['lepTag']

presel = cuts_weights.cuts_weights['presel'][sample][0]
weight = cuts_weights.cuts_weights['presel'][sample][1]

#Variable to plot
index = cuts_weights.cuts.vars_dict_format['lepIndex1']

variables = {\
   'pt':"LepGood_pt[%s]"%index,
   'eta':"abs(LepGood_eta[%s])"%index,
}

selection = "(nLepGood_{}_{lt} >= 1 && (LepGood_mcMatchId[{ind}] != 0 && LepGood_mcMatchId[{ind}] != -99 && LepGood_mcMatchId[{ind}] != 100))".format(lep, lt = lepTag, ind = index)

hists = {'FullSim':{}, 'FastSim':{}}
ratios = {}

##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

c1.cd(1)

#Efficiency
selList = [presel, selection] 
if not varBins: 
   hists['FullSim']['pt'] = makeHist(trees['FullSim'], variables['pt'], genFilterEff + "*weight*(" + combineCutsList(selList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2], addOverFlowBin = 'upper')
   hists['FullSim']['pt'].GetYaxis().SetTitle("Events")
else: 
   hists['FullSim']['pt'] = makeHistVarBins(trees['FullSim'], variables['pt'], genFilterEff + "*weight*(" + combineCutsList(selList) + ")", bins['pt'],  variableBinning = (varBins, bins['pt'][1]-bins['pt'][0]), addOverFlowBin = 'upper')
   if standardBins: hists['FullSim']['pt'].GetYaxis().SetTitle("Events / 10 GeV")
   else: hists['FullSim']['pt'].GetYaxis().SetTitle("Events / 5 GeV")
hists['FullSim']['pt'].SetName("FullSim_pt")
hists['FullSim']['pt'].SetTitle("%ss: FullSim vs FastSim comparison for Signal Sample"%lepton)
hists['FullSim']['pt'].GetXaxis().SetTitle("%s p_{T} / GeV"%(lepton))
hists['FullSim']['pt'].SetFillColor(ROOT.kViolet+10)
hists['FullSim']['pt'].SetMinimum(1)
hists['FullSim']['pt'].SetMaximum(1000)
hists['FullSim']['pt'].Draw("hist")

alignStats(hists['FullSim']['pt'])

if not varBins: 
   hists['FastSim']['pt'] = makeHist(trees['FastSim'], variables['pt'], "weight*(" + combineCutsList(selList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2], addOverFlowBin = 'upper')
else: 
   hists['FastSim']['pt'] = makeHistVarBins(trees['FastSim'], variables['pt'], "weight*(" + combineCutsList(selList) + ")", bins['pt'],  variableBinning = (varBins, bins['pt'][1]-bins['pt'][0]), addOverFlowBin = 'upper')
hists['FastSim']['pt'].SetName("FastSim_pt")
hists['FastSim']['pt'].SetFillColor(ROOT.kRed+1)
hists['FastSim']['pt'].SetFillColorAlpha(hists['FastSim']['pt'].GetFillColor(), 0.8)
hists['FastSim']['pt'].Draw("histsame")
 
if logy: ROOT.gPad.SetLogy()

ROOT.gPad.Modified()
ROOT.gPad.Update()

l1 = makeLegend2()
l1 = ROOT.TLegend()
l1.AddEntry("FullSim_pt", "FullSim", "F")
l1.AddEntry("FastSim_pt", "FastSim", "F")
l1.Draw()

alignLegend(l1, y1=0.5, y2=0.65)

##################################################################################################################################################################################
#Efficiency curves
c1.cd(2)

#Efficiency
ratios['pt'] = divideHists(hists['FullSim']['pt'], hists['FastSim']['pt'])
ratios['pt'].SetName("ratio_pt")
ratios['pt'].Draw("P")
ratios['pt'].SetTitle("%ss: FullSim vs FastSim SFs for Signal Sample ; %s p_{T} / GeV ; Ratio"%(lepton, lepton))
#setupEffPlot2(ratios['pt'])

ratios['pt'].SetMinimum(0.5)
ratios['pt'].SetMaximum(1.1)

#ratios['pt'].GetPaintedGraph().GetXaxis().SetLimits(xmin,xmax)

#Colours
ratios['pt'].SetMarkerColor(ROOT.kGreen+3)

ROOT.gPad.Modified()
ROOT.gPad.Update()

#l2 = makeLegend2()
#l2.AddEntry("ratio_pt", "Veto", "P")
#l2.Draw()

c1.Modified()
c1.Update()

##################################################################################Canvas 1#############################################################################################
c2 = ROOT.TCanvas("c2", "Canvas 2", 1800, 1500)
c2.Divide(1,2)

c2.cd(1)

if not varBins: 
   hists['FullSim']['eta'] = makeHist(trees['FullSim'], variables['eta'], genFilterEff + "*weight*(" + combineCutsList(selList) + ")", bins['eta'][0], bins['eta'][1], bins['eta'][2])
   hists['FullSim']['eta'].GetYaxis().SetTitle("Events")
else: 
   hists['FullSim']['eta'] = makeHistVarBins(trees['FullSim'], variables['eta'], genFilterEff + "*weight*(" + combineCutsList(selList) + ")", bins['eta'],  variableBinning = (varBins, bins['eta'][1]-bins['eta'][0]), addOverFlowBin = 'upper')
   hists['FullSim']['eta'].GetYaxis().SetTitle("Events / 0.1 rad")
hists['FullSim']['eta'].SetName("FullSim_eta")
hists['FullSim']['eta'].SetTitle("%ss: FullSim vs FastSim comparison for Signal Sample"%lepton)
hists['FullSim']['eta'].GetXaxis().SetTitle("%s |#eta| "%(lepton))
hists['FullSim']['eta'].SetFillColor(ROOT.kViolet+10)
hists['FullSim']['eta'].SetMinimum(1)
hists['FullSim']['eta'].SetMaximum(1000)
hists['FullSim']['eta'].Draw("hist")

alignStats(hists['FullSim']['eta'])#, y1=0.4, y2=0.6)

if not varBins: 
   hists['FastSim']['eta'] = makeHist(trees['FastSim'], variables['eta'], "weight*(" + combineCutsList(selList) + ")", bins['eta'][0], bins['eta'][1], bins['eta'][2])
else: 
   hists['FastSim']['eta'] = makeHistVarBins(trees['FastSim'], variables['eta'], "weight*(" + combineCutsList(selList) + ")", bins['eta'],  variableBinning = (varBins, bins['eta'][1]-bins['eta'][0]), addOverFlowBin = 'upper')
hists['FastSim']['eta'].SetName("FastSim_eta")
hists['FastSim']['eta'].SetFillColor(ROOT.kRed+1)
hists['FastSim']['eta'].SetFillColorAlpha(hists['FastSim']['eta'].GetFillColor(), 0.8)
hists['FastSim']['eta'].Draw("histsame")
   
if logy: ROOT.gPad.SetLogy()

ROOT.gPad.Modified()
ROOT.gPad.Update()

l2 = ROOT.TLegend()
l2.AddEntry("FullSim_eta", "FullSim", "F")
l2.AddEntry("FastSim_eta", "FastSim", "F")
l2.Draw()

alignLegend(l2, y1=0.5, y2=0.65)

##################################################################################################################################################################################
#Efficiency curves
c2.cd(2)

#Efficiency
ratios['eta'] = divideHists(hists['FullSim']['eta'], hists['FastSim']['eta'])
ratios['eta'].SetName("ratio_eta")
ratios['eta'].Draw("P")
ratios['eta'].SetTitle("%ss: FullSim vs FastSim SFs for Signal Sample ; %s |#eta| ; Ratio"%(lepton, lepton))
#setupEffPlot2(ratios['eta'])

ratios['eta'].SetMinimum(0.5)
ratios['eta'].SetMaximum(1.1)

#Colours
ratios['eta'].SetMarkerColor(ROOT.kGreen+3)

ROOT.gPad.Modified()
ROOT.gPad.Update()

#l2 = makeLegend2()
#l2.AddEntry("ratio_eta", "Veto", "P")
#l2.Draw()
c2.Modified()
c2.Update()

#      #hists[plotType][WP]['2D'][samp].GetYaxis().SetTitle("Events / 0.1 rad")
#      
#      hists[plotType][WP]['2D'][samp].SetName("%s_2D_%s"%(WP,samp))

#2D Histograms (wrt. pT)
if not varBins:
   hists['FullSim']['2D'] = make2DHist(trees['FullSim'], variables['pt'], variables['eta'], genFilterEff + "*weight*(" + combineCutsList(selList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2], bins['eta'][0], bins['eta'][1], bins['eta'][2])
else:
   hists['FullSim']['2D'] = make2DHistVarBins(trees['FullSim'], variables['pt'], variables['eta'], genFilterEff + "*weight*(" + combineCutsList(selList) + ")", bins['pt'], bins['eta'])
    #hists[plotType][WP]['2D'][samp].GetYaxis().SetTitle("Events / 5 GeV")
hists['FullSim']['2D'].SetName("FullSim_2D")
hists['FullSim']['2D'].SetTitle("%s p_{T} vs |#eta| Distribution in FullSim Signal Sample"%(lepton))
hists['FullSim']['2D'].GetXaxis().SetTitle("%s p_{T}"%lepton)
hists['FullSim']['2D'].GetYaxis().SetTitle("%s |#eta|"%lepton)
#hist.GetZaxis().SetRangeUser(0, 4)
#alignStats(hist)

#2D Histograms (wrt. pT)
if not varBins:
   hists['FastSim']['2D'] = make2DHist(trees['FastSim'], variables['pt'], variables['eta'], "weight*(" + combineCutsList(selList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2], bins['eta'][0], bins['eta'][1], bins['eta'][2])
else:
   hists['FastSim']['2D'] = make2DHistVarBins(trees['FastSim'], variables['pt'], variables['eta'], "weight*(" + combineCutsList(selList) + ")", bins['pt'], bins['eta'])
hists['FastSim']['2D'].SetName("FastSim_2D")
hists['FastSim']['2D'].SetTitle("%s p_{T} vs |#eta| Distribution in FastSim Signal Sample"%(lepton))
hists['FastSim']['2D'].GetXaxis().SetTitle("%s p_{T}"%lepton)
hists['FastSim']['2D'].GetYaxis().SetTitle("%s |#eta|"%lepton)

ratios['2D'] = divideHists(hists['FullSim']['2D'], hists['FastSim']['2D'])
ratios['2D'].SetName("ratios_2D")
ratios['2D'].SetTitle("%ss: FullSim vs FastSim SFs for Signal Sample"%lepton)
ratios['2D'].GetXaxis().SetTitle("%s p_{T}"%lepton)
ratios['2D'].GetYaxis().SetTitle("%s |#eta|"%lepton)
ratios['2D'].SetMarkerSize(0.8)
#ratios['2D'].SetMinimum(0.8)
#ratios['2D'].SetMaximum(5)
ratios['2D'].GetZaxis().SetRangeUser(0.8,1.2)

c4 = ROOT.TCanvas("c4", "Canvas 4", 1800, 1500)
ratios['2D'].Draw("COLZ TEXT89") #CONT1-5 #plots the graph with axes and points

alignStats(ratios['2D'])

#if logy: ROOT.gPad.SetLogz()
c4.Modified()
c4.Update()

c3 = ROOT.TCanvas("c3", "Canvas 3", 1800, 1500)
c3.Divide(1,2)

c3.cd(1)
hists['FastSim']['2D'].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
if logy: ROOT.gPad.SetLogz()

c3.cd(2)
hists['FullSim']['2D'].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
if logy: ROOT.gPad.SetLogz()
c3.Modified()
c3.Update()

#Save canvas
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   c1.SaveAs("%s/FastVsFullSim_lepPt%s.png"%(savedir, suffix))
   c1.SaveAs("%s/pdf/FastVsFullSim_lepPt%s.pdf"%(savedir, suffix))
   c1.SaveAs("%s/root/FastVsFullSim_lepPt%s.root"%(savedir, suffix))
   
   c2.SaveAs("%s/FastVsFullSim_lepEta%s.png"%(savedir, suffix))
   c2.SaveAs("%s/pdf/FastVsFullSim_lepEta%s.pdf"%(savedir, suffix))
   c2.SaveAs("%s/root/FastVsFullSim_lepEta%s.root"%(savedir, suffix))
   
   c3.SaveAs("%s/FastVsFullSim_2D_distributions%s.png"%(savedir, suffix))
   c3.SaveAs("%s/pdf/FastVsFullSim_2D_distributions%s.pdf"%(savedir, suffix))
   c3.SaveAs("%s/root/FastVsFullSim_2D_distributions%s.root"%(savedir, suffix))
   
   c4.SaveAs("%s/FastVsFullSim_2D_SFs%s.png"%(savedir, suffix))
   c4.SaveAs("%s/pdf/FastVsFullSim_2D_SFs%s.pdf"%(savedir, suffix))
   c4.SaveAs("%s/root/FastVsFullSim_2D_SFs%s.root"%(savedir, suffix))
