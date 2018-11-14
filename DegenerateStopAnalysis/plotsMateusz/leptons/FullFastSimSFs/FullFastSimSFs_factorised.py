# FullFastSimSFs_factored.py
# Determination of factored out HI & IP FullSim-FastSim SFs (using the Sum$ method) 
# Mateusz Zarucki 2017

import os
from FullFastSimSFs_info import *

#ROOT.gStyle.SetOptStat(0)

script = os.path.basename(__file__) #sys.argv[0]

#Arguments
args = getParser(script)

#Arguments
lep = args.lep
base = args.base
sample = args.sample
variable = args.variable
standardBins = args.standardBins
varBins = args.varBins
applyWeights = args.applyWeights
logy = args.logy
save = args.save
verbose = args.verbose

info = getInfo(script, vars(args))

lepton =        info['lepton']
samples =       info['samples']
bins =          info['bins']
#genFilterEffs = info['genFilterEffs'] #NOTE: should not make any difference in efficiencies
#genFilterEff = str(genFilterEffs[sample])

if 'allFullSim' in sample:
   trees = {'FullSim':samples['allFullSim'].tree, 'FastSim': info['allFastSim']}
else:
   trees = {'FullSim':samples[sample].tree, 'FastSim':samples['t2tt' + samples[sample].name.replace('S','')].tree}

if verbose:
   print makeLine()
   print "Using samples:", trees
   print makeLine()


if save:
   saveResults = True
   
   savedir = info['savedir']
   suffix =  info['suffix']

   if saveResults:
      resultsDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/FullFastSFs"
      makeDir(resultsDir)

# Cuts and Weights
cuts_weights = CutsWeights(samples, cutWeightOptions)

lepTag = cuts_weights.cuts.settings['lepTag'] #cutWeightOptions['settings']['lepTag']

presel = cuts_weights.cuts_weights['presel'][sample][0]
weight = cuts_weights.cuts_weights['presel'][sample][1]

# Leptons
if lep == "el":
   lepton = "Electron"
   pdgId = "11"
elif lep == "mu":
   pdgId = "13"
   lepton = "Muon"

# Geometric divisions
if lep == 'el':   etaAcc = 2.5 # eta acceptance
elif lep == 'mu': etaAcc = 2.4

variables = {\
   'pt':"LepGood_pt",
   'eta':"abs(LepGood_eta)",
}

# Lepton IDs
if lep == "mu":   ID = "looseMuonId"
elif lep == "el": ID = "SPRING15_25ns_v1" # >= 1 = Veto ID
IDcut = "LepGood_%s >= 1"%ID

dzCut = "abs(LepGood_dz) < 0.1"
dxyCut = "abs(LepGood_dxy) < 0.02"
hybIsoCut = "(LepGood_relIso03*min(LepGood_pt, 25)) < 5" 

if base == "ID":
   baseString = "(abs(LepGood_pdgId) == {pdgId} && abs(LepGood_pt) > 3.5 && abs(LepGood_eta) < {etaAcc} && {IDcut} && LepGood_mcMatchId != 0 && LepGood_mcMatchId != -99 && LepGood_mcMatchId != 100)".format(pdgId = pdgId, etaAcc = etaAcc, IDcut = IDcut)
   
   if variable == "HI":      selString = combineCuts(baseString, hybIsoCut)
   elif variable == "IP":    selString = combineCuts(baseString, dxyCut, dzCut)
   elif variable == "HI+IP": selString = combineCutsList([baseString, hybIsoCut, dxyCut, dzCut])
   else:
      print "Wrong base + variable combination."
      sys.exit(0)

elif base == "full":
   baseString = "(abs(LepGood_pdgId) == {pdgId} && abs(LepGood_pt) > 3.5 && abs(LepGood_eta) < {etaAcc} && LepGood_mcMatchId != 0 && LepGood_mcMatchId != -99 && LepGood_mcMatchId != 100)".format(pdgId = pdgId, etaAcc = etaAcc)
   
   if   variable == "ID":       selString = combineCuts(baseString, IDcut)
   elif variable == "HI":       selString = combineCuts(baseString, hybIsoCut)
   elif variable == "IP":       selString = combineCuts(baseString, dxyCut, dzCut)
   elif variable == "ID+HI":    selString = combineCutsList([baseString, IDcut, hybIsoCut])
   elif variable == "ID+IP":    selString = combineCutsList([baseString, IDcut, dxyCut, dzCut])
   elif variable == "ID+HI+IP": selString = combineCutsList([baseString, IDcut, hybIsoCut, dxyCut, dzCut])
   else:
      print "Wrong base + variable combination."
      sys.exit(0)

selection = "Sum$(%s) > 0"%selString
baseSel = "Sum$(%s) > 0"%baseString

plotVars = {'pt':{}, 'eta':{}}
plotVars['pt']['baseString'] =  varSel(variables['pt'], baseString)
plotVars['eta']['baseString'] = varSel(variables['eta'], baseString)
plotVars['pt']['selString'] =   varSel(variables['pt'], selString)
plotVars['eta']['selString'] =  varSel(variables['eta'], selString)

print makeLine()
print "Base selection:", baseSel
print "Final selection:", selection
print makeLine()

baseSelList = [filters, presel, baseSel] 
selList = [filters, presel, selection] 
   
print makeLine()
print "Cut string 1: (" + combineCutsList(baseSelList) + ")"
print "Cut string 2: (" + combineCutsList(selList) + ")"
print makeLine()

hists = {'FullSim':{'pt':{}, 'eta':{}, '2D':{}}, 'FastSim':{'pt':{}, 'eta':{}, '2D':{}}}
ratios = {'ID':{}, 'FullSim':{}, 'FastSim':{}, 'Full-Fast':{}}

for sim in ['FullSim', 'FastSim']:

   #Efficiency of variable 
   
   c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
   c1.Divide(1,2)
   
   c1.cd(1)
   
   #Efficiency
   if not varBins: 
      hists[sim]['pt']['den'] = makeHist(trees[sim], plotVars['pt']['baseString'], "weight*(" + combineCutsList(baseSelList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2])
      hists[sim]['pt']['den'].GetYaxis().SetTitle("Events")
   else: 
      hists[sim]['pt']['den'] = makeHistVarBins(trees[sim], plotVars['pt']['baseString'], "weight*(" + combineCutsList(baseSelList) + ")", bins['pt'], variableBinning = (varBins, bins['pt'][1]-bins['pt'][0]), addOverFlowBin = 'upper')
      if standardBins: hists[sim]['pt']['den'].GetYaxis().SetTitle("Events / 10 GeV")
      else: hists[sim]['pt']['den'].GetYaxis().SetTitle("Events / 5 GeV")

   hists[sim]['pt']['den'].SetName("%s_pt_den"%(sim))
   hists[sim]['pt']['den'].SetTitle("%ss: %s Efficiency for %s Signal Sample"%(lepton, variable, sim))
   hists[sim]['pt']['den'].GetXaxis().SetTitle("%s p_{T} / GeV"%lepton)
   hists[sim]['pt']['den'].SetFillColor(ROOT.kViolet+10)
   hists[sim]['pt']['den'].SetMinimum(1)
   hists[sim]['pt']['den'].SetMaximum(10000)
   hists[sim]['pt']['den'].Draw("hist")
   
   #alignStats(hists[sim]['pt']['den'])
   
   if not varBins: hists[sim]['pt']['num'] = makeHist(trees[sim], plotVars['pt']['baseString'], "weight*(" + combineCutsList(selList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2])
   else: hists[sim]['pt']['num'] = makeHistVarBins(trees[sim], plotVars['pt']['baseString'], "weight*(" + combineCutsList(selList) + ")", bins['pt'],variableBinning = (varBins, bins['pt'][1]-bins['pt'][0]), addOverFlowBin = 'upper')
   hists[sim]['pt']['num'].SetName("%s_pt_num"%sim)
   hists[sim]['pt']['num'].SetFillColor(ROOT.kRed+1)
   hists[sim]['pt']['num'].SetFillColorAlpha(hists[sim]['pt']['num'].GetFillColor(), 0.8)
   hists[sim]['pt']['num'].Draw("histsame")
    
   if logy: ROOT.gPad.SetLogy()
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   l1 = makeLegend2()
   l1 = ROOT.TLegend()
   l1.AddEntry("%s_pt_den"%(sim), "%s"%sim, "F")
   l1.AddEntry("%s_pt_num"%(sim), "%s (%s)"%(sim, variable), "F")
   l1.Draw()
   
   alignLegend(l1, y1=0.5, y2=0.65)
   
   ############################################################################################
   #Efficiency curves
   c1.cd(2)
   
   #Efficiency
   ratios[sim]['pt'] = makeEffPlot(hists[sim]['pt']['num'], hists[sim]['pt']['den'])
   ratios[sim]['pt'].SetName("%s_ratio_pt"%sim)
   #ratios[sim]['pt'].Draw("P")
   ratios[sim]['pt'].Draw("AP")
   ratios[sim]['pt'].SetTitle("%ss: %s Efficiency for %s Signal Sample"%(lepton, variable, sim))
   #ratios[sim]['pt'].GetXaxis().SetTitle("%s p_{T} / GeV"%lepton)
   #setupEffPlot2(ratios['pt'])
   
   #ratios[sim]['pt'].SetMinimum(0.5)
   #ratios[sim]['pt'].SetMaximum(1.1)
   
   #Colours
   ratios[sim]['pt'].SetMarkerColor(ROOT.kGreen+3)
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   ratios[sim]['pt'].GetPaintedGraph().GetXaxis().SetTitle("%s p_{T} / GeV"%lepton)
   ratios[sim]['pt'].GetPaintedGraph().GetXaxis().SetRangeUser(bins['pt'][0], bins['pt'][-1])
   ratios[sim]['pt'].GetPaintedGraph().SetMinimum(0.5)
   ratios[sim]['pt'].GetPaintedGraph().SetMaximum(1.1)
   #ratios[sim]['pt'].GetPaintedGraph().GetYaxis().SetLimits(0, 1.1)
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   #l2 = makeLegend2()
   #l2.AddEntry("ratio_pt", "Veto", "P")
   #l2.Draw()
   
   c1.Modified()
   c1.Update()
   
   ##################################################################################Canvas 1#############################################################################################
   
   #%s Efficiency of variable 
   
   c2 = ROOT.TCanvas("c2", "Canvas 2", 1800, 1500)
   c2.Divide(1,2)
   
   c2.cd(1)
   
   #Efficiency
   if not varBins: 
      hists[sim]['eta']['den'] = makeHist(trees[sim], plotVars['eta']['baseString'], "weight*(" + combineCutsList(baseSelList) + ")", bins['eta'][0], bins['eta'][1], bins['eta'][2])
      hists[sim]['eta']['den'].GetYaxis().SetTitle("Events")
   else: 
      hists[sim]['eta']['den'] = makeHistVarBins(trees[sim], plotVars['eta']['baseString'], "weight*(" + combineCutsList(baseSelList) + ")", bins['eta'])
      hists[sim]['eta']['den'].GetYaxis().SetTitle("Events / 0.1 rad")
   hists[sim]['eta']['den'].SetName("%s_eta_den"%sim)
   hists[sim]['eta']['den'].SetTitle("%ss: %s Efficiency for %s Signal Sample"%(lepton, variable, sim))
   hists[sim]['eta']['den'].GetXaxis().SetTitle("%s |#eta|"%lepton)
   hists[sim]['eta']['den'].SetFillColor(ROOT.kViolet+10)
   hists[sim]['eta']['den'].SetMinimum(1)
   hists[sim]['eta']['den'].SetMaximum(10000)
   hists[sim]['eta']['den'].Draw("hist")
   
   #alignStats(hists[sim]['eta']['den'])
   
   if not varBins: hists[sim]['eta']['num'] = makeHist(trees[sim], plotVars['eta']['baseString'], "weight*(" + combineCutsList(selList) + ")", bins['eta'][0], bins['eta'][1], bins['eta'][2])
   else: hists[sim]['eta']['num'] = makeHistVarBins(trees[sim], plotVars['eta']['baseString'], "weight*(" + combineCutsList(selList) + ")", bins['eta'])
   hists[sim]['eta']['num'].SetName("%s_eta_num"%sim)
   hists[sim]['eta']['num'].SetFillColor(ROOT.kRed+1)
   hists[sim]['eta']['num'].SetFillColorAlpha(hists[sim]['eta']['num'].GetFillColor(), 0.8)
   hists[sim]['eta']['num'].Draw("histsame")
    
   if logy: ROOT.gPad.SetLogy()
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   l2 = makeLegend2()
   l2 = ROOT.TLegend()
   l2.AddEntry("%s_eta_den"%sim, "%s"%sim, "F")
   l2.AddEntry("%s_eta_num"%sim, "%s (%s)"%(sim, variable), "F")
   l2.Draw()
   
   alignLegend(l2, y1=0.5, y2=0.65)
   
   ############################################################################################
   #Efficiency curves
   c2.cd(2)
   
   #Efficiency
   ratios[sim]['eta'] = makeEffPlot(hists[sim]['eta']['num'], hists[sim]['eta']['den'])
   ratios[sim]['eta'].SetName("%s_ratio_eta"%sim)
   ratios[sim]['eta'].Draw("AP")
   #ratios[sim]['eta'].Draw("P")
   ratios[sim]['eta'].SetTitle("%ss: %s Efficiency for %s Signal Sample"%(lepton, variable, sim))
   #ratios[sim]['eta'].GetXaxis().SetTitle("%s |#eta|"%lepton)
   #setupEffPlot2(ratios['eta'])
   
   #ratios[sim]['eta'].SetMinimum(0.5)
   #ratios[sim]['eta'].SetMaximum(1.1)
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   ratios[sim]['eta'].GetPaintedGraph().GetXaxis().SetTitle("%s |#eta|"%lepton)
   ratios[sim]['eta'].GetPaintedGraph().GetXaxis().SetRangeUser(bins['eta'][0], bins['eta'][-1])
   ratios[sim]['eta'].GetPaintedGraph().SetMinimum(0.5)
   ratios[sim]['eta'].GetPaintedGraph().SetMaximum(1.1)
   #ratios[sim]['eta'].GetPaintedGraph().GetYaxis().SetLimits(0, 1.1)
   
   #Colours
   ratios[sim]['eta'].SetMarkerColor(ROOT.kGreen+3)
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   #l2 = makeLegend2()
   #l2.AddEntry("ratio_eta", "Veto", "P")
   #l2.Draw()
   
   c2.Modified()
   c2.Update()
  
   #2D Histograms (wrt. pT)
   if not varBins:
      hists[sim]['2D']['den'] = make2DHist(trees[sim], plotVars['pt']['baseString'], plotVars['eta']['baseString'], "weight*(" + combineCutsList(baseSelList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2], bins['eta'][0], bins['eta'][1], bins['eta'][2])
   else: 
      hists[sim]['2D']['den'] = make2DHistVarBins(trees[sim], plotVars['pt']['baseString'], plotVars['eta']['baseString'], "weight*(" + combineCutsList(baseSelList) + ")", bins['pt'], bins['eta'])
   hists[sim]['2D']['den'].SetName("%s_2D_den"%sim)
   hists[sim]['2D']['den'].SetTitle("%s p_{T} vs |#eta| Distribution in %s Signal Sample"%(lepton, sim))
   hists[sim]['2D']['den'].GetXaxis().SetTitle("%s p_{T}"%lepton)
   hists[sim]['2D']['den'].GetYaxis().SetTitle("%s |#eta|"%lepton)
   #hist.GetZaxis().SetRangeUser(0, 4)
   #alignStats(hist)
   
   #2D Histograms (wrt. pT)
   if not varBins: hists[sim]['2D']['num'] = make2DHist(trees[sim], plotVars['pt']['baseString'], plotVars['eta']['baseString'], "weight*(" + combineCutsList(selList) + ")", bins['pt'][0], bins['pt'][1], bins['pt'][2], bins['eta'][0], bins['eta'][1], bins['eta'][2])
   else: hists[sim]['2D']['num'] = make2DHistVarBins(trees[sim], plotVars['pt']['baseString'], plotVars['eta']['baseString'], "weight*(" + combineCutsList(selList) + ")", bins['pt'], bins['eta'])
   hists[sim]['2D']['num'].SetName("%s_2D_num"%sim)
   hists[sim]['2D']['num'].SetTitle("%s p_{T} vs |#eta| Distribution in %s Signal Sample"%(lepton, sim))
   hists[sim]['2D']['num'].GetXaxis().SetTitle("%s p_{T}"%lepton)
   hists[sim]['2D']['num'].GetYaxis().SetTitle("%s |#eta|"%lepton)
   
   ratios[sim]['2D'] = makeEffPlot(hists[sim]['2D']['num'], hists[sim]['2D']['den'])
   ratios[sim]['2D'].SetName("%s_ratios_2D"%sim)
   ratios[sim]['2D'].SetTitle("%s Efficiency for %s Signal Sample"%(variable, sim))
   #ratios[sim]['2D'].GetXaxis().SetTitle("%s p_{T}"%lepton)
   #ratios[sim]['2D'].GetYaxis().SetTitle("%s |#eta|"%lepton)
   ratios[sim]['2D'].SetMarkerSize(0.8)
   #ratios[sim]['2D'].SetMinimum(0.5)
   #ratios[sim]['2D'].SetMaximum(5)
   #ratios[sim]['2D'].GetZaxis().SetRangeUser(0.5, 5)
   
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      c1.SaveAs("%s/%s_lepPt%s.png"%(savedir, sim, suffix))
      c1.SaveAs("%s/pdf/%s_lepPt%s.pdf"%(savedir, sim, suffix))
      c1.SaveAs("%s/root/%s_lepPt%s.root"%(savedir, sim, suffix))
      
      c2.SaveAs("%s/%s_lepEta%s.png"%(savedir, sim, suffix))
      c2.SaveAs("%s/pdf/%s_lepEta%s.pdf"%(savedir, sim, suffix))
      c2.SaveAs("%s/root/%s_lepEta%s.root"%(savedir, sim, suffix))
   
c5 = ROOT.TCanvas("c5", "Canvas 5", 1800, 1500)

a = ratios['FullSim']['2D'].GetPassedHistogram().Clone()
b = ratios['FullSim']['2D'].GetTotalHistogram().Clone()
c = ratios['FastSim']['2D'].GetPassedHistogram().Clone()
d = ratios['FastSim']['2D'].GetTotalHistogram().Clone()

a.Sumw2()
b.Sumw2()
c.Sumw2()
d.Sumw2()

a.Divide(b)
c.Divide(d)

ratios['Full-Fast']['2D'] = divideHists(a,c)
ratios['Full-Fast']['2D'].SetName("Full-Fast_ratios_2D")
ratios['Full-Fast']['2D'].SetTitle("%ss: Factorised HI & IP FullSim-FastSim SFs for Signal Sample"%lepton)
ratios['Full-Fast']['2D'].GetXaxis().SetTitle("%s p_{T}"%lepton)
ratios['Full-Fast']['2D'].GetYaxis().SetTitle("%s |#eta|"%lepton)
ratios['Full-Fast']['2D'].SetMarkerSize(0.8)
#ratios['Full-Fast']['2D'].SetMinimum(0.8)
#ratios['Full-Fast']['2D'].SetMaximum(5)
ratios['Full-Fast']['2D'].GetZaxis().SetRangeUser(0.8,1.2)

ratios['Full-Fast']['2D'].Draw("COLZ TEXT89") #CONT1-5 #plots the graph with axes and points
   
#alignStats(ratios['Full-Fast']['2D'])

c5.Modified()
c5.Update()

if save:
   c5.SaveAs("%s/Full-FastSimSFs_2D%s.png"%(savedir, suffix))
   c5.SaveAs("%s/pdf/Full-FastSimSFs_2D%s.pdf"%(savedir, suffix))
   c5.SaveAs("%s/root/Full-FastSimSFs_2D%s.root"%(savedir, suffix))

   if saveResults:
      if base == "ID" and variable == "HI+IP": 
         c5.SaveAs("%s/root/Full-FastSimSFs_factorised_%s.root"%(resultsDir, lep))
      
      #fileName = "%s/Full-FastSimSFs_factorised_%s"%(resultsDir, lep)
      #f = ROOT.TFile('%s.root'%fileName, 'recreate', fileName)
      ##ratios['Full-Fast']['2D'].Write()
      #f.Write() 
      ##f.Print() 
      #f.Close()     

c6 = ROOT.TCanvas("c6", "Canvas 6", 1800, 1500)

ratios['Full-Fast']['pt'] = divideEff(ratios['FullSim']['pt'], ratios['FastSim']['pt'])
ratios['Full-Fast']['pt'].SetName("Full-Fast_ratios_pt")
ratios['Full-Fast']['pt'].SetTitle("%ss: Factorised HI & IP FullSim-FastSim SFs for Signal Sample"%lepton)
ratios['Full-Fast']['pt'].GetXaxis().SetTitle("%s p_{T}"%lepton)
ratios['Full-Fast']['pt'].GetYaxis().SetTitle("FullSim-FastSim SF")
ratios['Full-Fast']['pt'].GetXaxis().CenterTitle()
ratios['Full-Fast']['pt'].GetYaxis().CenterTitle()
ratios['Full-Fast']['pt'].GetXaxis().SetTitleOffset(1.3)
ratios['Full-Fast']['pt'].GetYaxis().SetTitleOffset(1.3)
ratios['Full-Fast']['pt'].SetMarkerSize(0.8)
ratios['Full-Fast']['pt'].SetMinimum(0.8)
ratios['Full-Fast']['pt'].SetMaximum(1.1)
ratios['Full-Fast']['pt'].GetXaxis().SetLimits(0,200)
ratios['Full-Fast']['pt'].Draw("AP") #CONT1-5 #plots the graph with axes and points
   
#alignStats(ratios['Full-Fast']['pt'])

c6.Modified()
c6.Update()

if save:
   c6.SaveAs("%s/Full-FastSimSFs_pt%s.png"%(savedir, suffix))
   c6.SaveAs("%s/pdf/Full-FastSimSFs_pt%s.pdf"%(savedir, suffix))
   c6.SaveAs("%s/root/Full-FastSimSFs_pt%s.root"%(savedir, suffix))

c7 = ROOT.TCanvas("c7", "Canvas 7", 1800, 1500)

ratios['Full-Fast']['eta'] = divideEff(ratios['FullSim']['eta'], ratios['FastSim']['eta'])
ratios['Full-Fast']['eta'].SetName("Full-Fast_ratios_eta")
ratios['Full-Fast']['eta'].SetTitle("%ss: Factorised HI & IP FullSim-FastSim SFs for Signal Sample"%lepton)
ratios['Full-Fast']['eta'].GetXaxis().SetTitle("%s |#eta|"%lepton)
ratios['Full-Fast']['eta'].GetYaxis().SetTitle("FullSim-FastSim SF")
ratios['Full-Fast']['eta'].GetXaxis().CenterTitle()
ratios['Full-Fast']['eta'].GetYaxis().CenterTitle()
ratios['Full-Fast']['eta'].GetXaxis().SetTitleOffset(1.3)
ratios['Full-Fast']['eta'].GetYaxis().SetTitleOffset(1.3)
ratios['Full-Fast']['eta'].SetMarkerSize(0.8)
ratios['Full-Fast']['eta'].SetMinimum(0.8)
ratios['Full-Fast']['eta'].SetMaximum(1.1)
#ratios['Full-Fast']['eta'].GetXaxis().SetLimits(0,200)
ratios['Full-Fast']['eta'].Draw("AP") #CONT1-5 #plots the graph with axes and points
   
#alignStats(ratios['Full-Fast']['pt'])

c7.Modified()
c7.Update()

if save:
   c7.SaveAs("%s/Full-FastSimSFs_eta%s.png"%(savedir, suffix))
   c7.SaveAs("%s/pdf/Full-FastSimSFs_eta%s.pdf"%(savedir, suffix))
   c7.SaveAs("%s/root/Full-FastSimSFs_eta%s.root"%(savedir, suffix))
  
for sim in ['FullSim', 'FastSim']:
 
   c4 = ROOT.TCanvas("c4", "Canvas 4", 1800, 1500)
   ratios[sim]['2D'].Draw("COLZ TEXT89") #CONT1-5 #plots the graph with axes and points
   #alignStats(ratios[sim]['2D'])
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   #ratios[sim]['2D'].GetPaintedGraph().SetMaximum(5)
   
   #if logy: ROOT.gPad.SetLogz()
   c4.Modified()
   c4.Update()
   
   c3 = ROOT.TCanvas("c3", "Canvas 3", 1800, 1500)
   c3.Divide(1,2)
   
   c3.cd(1)
   hists[sim]['2D']['den'].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
   if logy: ROOT.gPad.SetLogz()
   
   c3.cd(2)
   hists[sim]['2D']['num'].Draw("COLZ") #CONT1-5 #plots the graph with axes and points
   if logy: ROOT.gPad.SetLogz()
   c3.Modified()
   c3.Update()
   
   #Save canvas
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      c3.SaveAs("%s/%s_2D_distributions%s.png"%(savedir, sim, suffix))
      c3.SaveAs("%s/pdf/%s_2D_distributions%s.pdf"%(savedir, sim, suffix))
      c3.SaveAs("%s/root/%s_2D_distributions%s.root"%(savedir, sim, suffix))
      
      c4.SaveAs("%s/%s_2D_eff%s.png"%(savedir, sim, suffix))
      c4.SaveAs("%s/pdf/%s_2D_eff%s.pdf"%(savedir, sim, suffix))
      c4.SaveAs("%s/root/%s_2D_eff%s.root"%(savedir, sim, suffix))

doPickle = 0
if doPickle:
   graph = ratios['Full-Fast']['pt']
   
   nPoints = graph.GetNbinsX()
   print nPoints 
   #for i in range(nPoints):
   #   print i
   i = 1
   points = {'SRL':[5,12], 'SRH':[12,20], 'SRV':[20,30], 'CR':[30-200]}
   bins = {'v':{}, 'u':{}, 'd':{}, 'e':{}}
   
   bins['v']['SRL'] = graph.GetBinContent(2)
   bins['e']['SRL'] = graph.GetBinError(2) 
   bins['v']['SRH'] = graph.GetBinContent(3)
   bins['e']['SRH'] = graph.GetBinError(3) 
   bins['v']['SRV'] = graph.GetBinContent(4)
   bins['e']['SRV'] = graph.GetBinError(4) 
   bins['v']['CR'] = graph.GetBinContent(5)
   bins['e']['CR'] = graph.GetBinError(5) 
   
   SFs = {'SRL': u_float.u_float(bins['v']['SRL'], bins['e']['SRL']),
          'SRH': u_float.u_float(bins['v']['SRH'], bins['e']['SRH']),
          'SRV': u_float.u_float(bins['v']['SRV'], bins['e']['SRV']),
          'CR':  u_float.u_float(bins['v']['CR'],  bins['e']['CR'])}
   
   pickleFile1 = open("%s/FullSim-FastSim_SFs_factored%s.pkl"%(savedir, suffix), "w")
   pickle.dump(SFs, pickleFile1)
   pickleFile1.close()
   
   pickleFile2 = open("%s/FullSim-FastSim_SFs_factored_ratios%s.pkl"%(savedir, suffix), "w")
   pickle.dump(ratios, pickleFile2)
   pickleFile2.close()
