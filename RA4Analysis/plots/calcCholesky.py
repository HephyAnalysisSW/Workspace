from analysisHelpers import *
import pickle
inDir = "/data/kwolf/RA4Fit2012_6j/output/Res_copyMET_separateBTagWeights_constrPareto_fitData_MuonElectron_jet5pt40__bt1_150.0-met-1500.0__bt2_150.0-met-400.0__bt1_400.0-ht-2500.0__bt2_400.0-ht-750.0_intLumi-20p0_130411_1104/"

regions = [\
  {'btb':'2',"htb":[750,2500], "metb":[250,350]},
  {'btb':'2',"htb":[750,2500], "metb":[350,450]},
  {'btb':'2',"htb":[750,2500], "metb":[450,2500]},
  {'btb':'2',"htb":[400,750], "metb":[250,2500]},
#  {'btb':'2',"htb":[400,750], "metb":[350,450]},  
#  {'btb':'2',"htb":[400,750], "metb":[450,2500]},  
  ]

res = getSamplingCovrianceMatrix(inDir, regions, n=100, sumUpSingleBins = True )
res2 = getSamplingCovrianceMatrix(inDir, regions, n=100, sumUpSingleBins = False )
pickle.dump(res['ratioCovM'], file('/data/schoef/results2012/Cholesky_3b_unifiedLowHT.pkl', "w"))

