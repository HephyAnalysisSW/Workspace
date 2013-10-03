from analysisHelpers import *
import os, pickle, copy

mc_chain = getRefChain(mode = "mc")
data_chain = getRefChain(mode = "data")
minNJet = 6
##For Syncing with UCSB
#for btb in ['2']:
#  for metb in [[150, 250], [250, 350], [350, 450], [450, 2500]]:
#    mc_yield    = getRefYield(btb=btb, htb=[500,2500], metb=metb, metvar='type1phiMet', minNJet = minNJet,chain = mc_chain)
#    data_yield  = getRefYield(btb=btb, htb=[500,2500], metb=metb, metvar='type1phiMet', minNJet = minNJet,chain = data_chain)
#    print "500/",metb,", btb:",btb, data_yield , "(",mc_yield,")"


#def sanityPlot(inDir, btb, htb, n=100):
#  btb = '2'
#  htb = [750,2500]
#
#  c1 = ROOT.TCanvas()
#  c1.SetLogy()
#  #  sampledShapes = getSampledMetShapePrediction(inDir, btb, htb, n)
#  predMetShape = getPredictedMetShapes(inDir, btb, htb)
#  inputMetShape = getInputMetShape(inDir, btb, htb)
#  inputMetShape.Draw()
#  predMetShape["central"].Draw("same")
#  predMetShape["varMedian"].Draw("same")
#  predMetShape["varDown"].Draw("same")
#  predMetShape["varUp"].Draw("same")
#  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/sanityModelPlots/test.png")
#
#  normalizedYield = getNormRegYield(inDir, btb, htb)
#  print "normalizationYield:",normalizedYield,"should be",getRefYield(btb=btb, htb=htb, metb=[150,250], metvar='type1phiMet', minNJet = minNJet, chain = mc_chain)

htlow = 1000
metbins = [[250, 350],[350,450],[450,2500]]
print "MC"
MC_inDir = '/data/kwolf/RA4Fit2012_6j/output/Res_copyMET_constrPareto_fitMC_MuonElectron_jet5pt40__bt1_150.0-met-1500.0__bt2_150.0-met-400.0__bt1_400.0-ht-2500.0__bt2_400.0-ht-750.0_intLumi-20p0_130306_1714/err_sampling_'+str(htlow)+'_ht_2500/'
mcchain = getRefChain(dir = "/data/schoef/convertedTuples_v16/copyMET/", mode = "MC", onlyTT = False)

for metb in metbins:
  res = getSampledMetYieldPrediction(MC_inDir, '2', htb=[htlow, 2500], metb=metb)
  mcTruth = getRefYield('2', [htlow,2500], metb, 'type1phiMet', 6, mcchain, weight = "weight")
  mcTruthErr2 = getRefYield('2', [htlow,2500], metb, 'type1phiMet', 6, mcchain, weight = "weight*weight")
  mcPred = res['results'][tuple(metb)]['central']
  mcPredMinus = res['results'][tuple(metb)]['varDown'] - mcPred
  mcPredPlus = res['results'][tuple(metb)]['varUp'] - mcPred

  print "Pred:",mcPred,"-",-mcPredMinus,"+",mcPredPlus,"Truth:",mcTruth,"+/-",sqrt(mcTruthErr2)

data_inDir = '/data/kwolf/RA4Fit2012_6j/output/Res_copyMET_separateBTagWeights_constrPareto_fitData_MuonElectron_jet5pt40__bt1_150.0-met-1500.0__bt2_150.0-met-400.0__bt1_400.0-ht-2500.0__bt2_400.0-ht-750.0_intLumi-20p0_130306_1714/err_sampling_'+str(htlow)+'_ht_2500/'

print "Data"
datachain = getRefChain(dir = "/data/schoef/convertedTuples_v16/copyMET/", mode = "Data", onlyTT = False)
for metb in metbins:
  res = getSampledMetYieldPrediction(data_inDir, '2', htb=[htlow, 2500], metb=metb)
  dataObserved = getRefYield('2', [htlow,2500], metb, 'type1phiMet', 6, datachain, weight = "weight")
  dataObservedErr2 = getRefYield('2', [htlow,2500], metb, 'type1phiMet', 6, datachain, weight = "weight*weight")
  mcPred = res['results'][tuple(metb)]['central']
  mcPredMinus = res['results'][tuple(metb)]['varDown'] - mcPred
  mcPredPlus = res['results'][tuple(metb)]['varUp'] - mcPred

  print "Pred:",mcPred,"-",-mcPredMinus,"+",mcPredPlus,"Truth:",dataObserved,"+/-",sqrt(dataObservedErr2)
