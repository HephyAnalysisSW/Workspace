from analysisHelpers import *
import ROOT
from simplePlotsCommon import *
from simpleStatTools import niceNum
import os, pickle, copy

SpF = pickle.load(file('/data/schoef/results2012/jackKnifeSpF.pkl'))
SpF_small = pickle.load(file('/data/schoef/results2012/jackKnifeSpF_SFsmall.pkl'))
exclusiveHTBins = [\
  [400,450  ],
  [450,500  ],
  [500,550  ],
  [550,600  ],
  [600,650  ],
  [650,700  ],
  [700,750  ],
  [750,800  ],
  [800,1000 ],
  [1000,1200],
  [1200,1500],
  [1500,2500]
]

inclusiveHTBins = [\
    [400,2500  ],
    [750,2500  ],
    [1000,2500  ],
  ]

mode = "mc"

if mode=="mc":
  inclusiveInDir = "/data/kwolf/RA4Fit2012_6j/output/Res_copyMET_constrPareto_fitMC_MuonElectron_jet5pt40__bt1_150.0-met-1500.0__bt2_150.0-met-400.0__bt1_400.0-ht-2500.0__bt2_400.0-ht-750.0_intLumi-20p0_130416_1815/"
#  exclusiveInDir = "/data/kwolf/RA4Fit2012_6j/output/Res_copyMET_separateBTagWeights_constrPareto_weightBTag_SF_fitMC_MuonElectron_jet5pt40__bt1_150.0-met-1500.0__bt2_150.0-met-400.0__bt1_400.0-ht-2500.0__bt2_400.0-ht-750.0_intLumi-20p0_130329_1556/"
  c = getRefChain(dir = "/data/schoef/convertedTuples_v16/copyMET/", mode = "MC", onlyTT = False)

if mode=="data":
  inclusiveInDir = "/data/kwolf/RA4Fit2012_6j/output/Res_copyMET_separateBTagWeights_constrPareto_fitData_MuonElectron_jet5pt40__bt1_150.0-met-1500.0__bt2_150.0-met-400.0__bt1_400.0-ht-2500.0__bt2_400.0-ht-750.0_intLumi-20p0_130325_2023/"
#  exclusiveInDir = "/data/kwolf/RA4Fit2012_6j/output/Res_copyMET_separateBTagWeights_constrPareto_fitData_MuonElectron_jet5pt40__bt1_150.0-met-1500.0__bt2_150.0-met-400.0__bt1_400.0-ht-2500.0__bt2_400.0-ht-750.0_intLumi-20p0_130328_1108/"
  c = getRefChain(dir = "/data/schoef/convertedTuples_v16/copyMET/", mode = "Data", onlyTT = False)

SpFDataMCSys = pickle.load(file('../results/SpillFactorDataMCSys.pkl'))
sysTable = pickle.load(file('../results/systTable.pkl'))

metbins =[ [150,250], [250, 350], [350, 450], [450, 2500]]
#metbins =[ [450,2500]]
for htb in inclusiveHTBins:
  res = getSampledMetYieldPrediction(inclusiveInDir, '2', htb, metbins)
  for metb in  metbins:
#    print htb, metb, "==2b result", res['results'][tuple(metb)]['central']
    if mode=="data":
      sKey = 'sigmaForData'
      key = 'rForData'
    else:
      sKey = 'rTrueSigma'
      key = 'rTrue'

    spf = SpF[tuple(htb)][tuple(metb)][(6,99)]['SF']['3po2']
    if mode=="mc":
      ref = getRefYield("none", htb, metb, "type1phiMet", 6, c, weight = "weightBTag3p")
      refErr = sqrt(getRefYield("none", htb, metb, "type1phiMet", 6, c, weight = "weightBTag3p*weightBTag3p"))
    if mode=="data":
      ref = getRefYield("3", htb, metb, "type1phiMet", 6, c, weight = "weight")
      refErr = sqrt(getRefYield("3", htb, metb, "type1phiMet", 6, c, weight = "weight*weight"))
    pred =  spf[key]*res['results'][tuple(metb)]['central']
    predSamplingErr = spf[key]*0.5*(res['results'][tuple(metb)]['varUp'] - res['results'][tuple(metb)]['varDown'])
    totVar = predSamplingErr**2 

    predSpillFactorErr = spf[sKey]*res['results'][tuple(metb)]['central']

    totVar+= predSpillFactorErr**2
    
    spf_b_Up = SpF[tuple(htb)][tuple(metb)][(6,99)]['SF_b_Up']['3po2']
    spf_b_Down = SpF[tuple(htb)][tuple(metb)][(6,99)]['SF_b_Down']['3po2']
    predSFbErr = 0.5*(spf_b_Up[key] - spf_b_Down[key])*res['results'][tuple(metb)]['central']
    totVar+= predSFbErr**2

    spf_light_Up = SpF[tuple(htb)][tuple(metb)][(6,99)]['SF_light_Up']['3po2']
    spf_light_Down = SpF[tuple(htb)][tuple(metb)][(6,99)]['SF_light_Down']['3po2']
    predSFlErr = 0.5*(spf_light_Up[key] - spf_light_Down[key])*res['results'][tuple(metb)]['central']
    totVar+= predSFlErr**2

    spf_GluSplit_Up = SpF[tuple(htb)][tuple(metb)][(6,99)]['GluSplitUp']['3po2']
    spf_GluSplit_Down = SpF[tuple(htb)][tuple(metb)][(6,99)]['GluSplitDown']['3po2']
    predGluSplitErr = 0.5*(spf_GluSplit_Up[key] - spf_GluSplit_Down[key])*res['results'][tuple(metb)]['central']
    totVar+= predGluSplitErr**2

    spf_cFrac_Up = SpF_small[tuple(htb)][tuple(metb)][(6,99)]['cFracUp']['3po2']
    spf_cFrac_Down = SpF_small[tuple(htb)][tuple(metb)][(6,99)]['cFracDown']['3po2']
    predcFracErr = abs(0.5*(spf_cFrac_Up[key] - spf_cFrac_Down[key])*res['results'][tuple(metb)]['central'])
    totVar+= predcFracErr**2

#    print metb, htb, "mcTruth", round(mcTruth,2),"+/-",round(mcTruthErr,2),"pred",round(pred,2),"+/-",round(predSamplingErr,2),"(Sampling) +/-",round(predSpillFactorErr,2),\
#          "(spillfactorStat) +/-", round(predSFbErr,2), "(SF b) +/-", round(predSFlErr,2), "(SF light)", round(predGluSplitErr,2), "(gluSplit)", round(predcFracErr,2), "(cFrac)"
    predSpFNonClosureErr = SpFDataMCSys[tuple(htb)][tuple(metb)]*spf[key]*res['results'][tuple(metb)]['central']
    totVar+= predSpFNonClosureErr**2

    if not metb == [150, 250]:
      for sys in sysTable['systematics'].keys():
        totVar+= (sysTable['systematics'][sys][tuple(htb)][tuple(metb)]*spf[key]*res['results'][tuple(metb)]['central'])**2

    #Control region Poissonian
    if mode=="data":
      ref2b = getRefYield("2", htb,[150, 250] , "type1phiMet", 6, c, weight = "weight")
    if mode=="mc":
      ref2b = getRefYield("none", htb, [150, 250], "type1phiMet", 6, c, weight = "weightBTag2")

    controlRegionPoissonianErr = pred/sqrt(ref2b)
#    print totVar, controlRegionPoissonianErr
    totVarPlusCRP = totVar + controlRegionPoissonianErr**2

    if mode=="data":
      print "Result  :", metb, htb, "observed", round(ref,2),"+/-",round(refErr,2),"pred",round(pred,2),"+/-",round(sqrt(totVarPlusCRP),2)
    else:
      print "Closure :", metb, htb, "mcTruth",  round(ref,2),"+/-",round(refErr,2),"pred",round(pred,2),"+/-",round(sqrt(totVar),2),"(",round(sqrt(totVarPlusCRP),2),")"


#doExclusiveBins = False
#if doExclusiveBins:
#  print "\n\nNow from exclusive bins:\n"
#
#  for metb in  metbins:
#    for ihtb in inclusiveHTBins:
#      if mode=="data":
#        sKey = 'sigmaForData'
#        key = 'rForData'
#      else:
#        sKey = 'rTrueSigma'
#        key = 'rTrue'
#      totVar  = 0.
#      ref = 0.
#      refVar = 0. 
#      pred = 0.
#      predSFbErr = 0.
#      predSFlErr = 0.
#      predGluSplitErr = 0.
#      predcFracErr = 0.
#
#      controlRegionPoissonianVar = 0. 
#
#      for htb in exclusiveHTBins:
#        if not (htb[0]>=ihtb[0] and htb[1]<=ihtb[1]) : 
#  #        print "Disregarding", htb, "for",ihtb 
#          continue
#        print "Adding",htb, "to",ihtb
#        res = getSampledMetYieldPrediction(exclusiveInDir, '2', htb, [metb])
#      #    print htb, metb, "==2b result", res['results'][tuple(metb)]['central']
#
#        spf = SpF[tuple(htb)][tuple(metb)][(6,99)]['SF']['3po2']
#        if mode=="mc":
#          ref += getRefYield("none", htb, metb, "type1phiMet", 6, c, weight = "weightBTag3p")
#          refVar += getRefYield("none", htb, metb, "type1phiMet", 6, c, weight = "weightBTag3p*weightBTag3p")
#        if mode=="data":
#          ref += getRefYield("3", htb, metb, "type1phiMet", 6, c, weight = "weight")
#          refVar += getRefYield("3", htb, metb, "type1phiMet", 6, c, weight = "weight*weight")
#
#        pred +=  spf[key]*res['results'][tuple(metb)]['central']
#
#        predSpillFactorErr = spf[sKey]*res['results'][tuple(metb)]['central']
#        totVar+= predSpillFactorErr**2
#        
#        spf_b_Up = SpF[tuple(htb)][tuple(metb)][(6,99)]['SF_b_Up']['3po2']
#        spf_b_Down = SpF[tuple(htb)][tuple(metb)][(6,99)]['SF_b_Down']['3po2']
#        predSFbErr += 0.5*(spf_b_Up[key] - spf_b_Down[key])*res['results'][tuple(metb)]['central']
#
#        spf_light_Up = SpF[tuple(htb)][tuple(metb)][(6,99)]['SF_light_Up']['3po2']
#        spf_light_Down = SpF[tuple(htb)][tuple(metb)][(6,99)]['SF_light_Down']['3po2']
#        predSFlErr += 0.5*(spf_light_Up['rTrue'] - spf_light_Down['rTrue'])*res['results'][tuple(metb)]['central']
#
#        spf_GluSplit_Up = SpF[tuple(htb)][tuple(metb)][(6,99)]['GluSplitUp']['3po2']
#        spf_GluSplit_Down = SpF[tuple(htb)][tuple(metb)][(6,99)]['GluSplitDown']['3po2']
#        predGluSplitErr += 0.5*(spf_GluSplit_Up['rTrue'] - spf_GluSplit_Down['rTrue'])*res['results'][tuple(metb)]['central']
#
#        spf_cFrac_Up = SpF[tuple(htb)][tuple(metb)][(6,99)]['cFracUp']['3po2']
#        spf_cFrac_Down = SpF[tuple(htb)][tuple(metb)][(6,99)]['cFracDown']['3po2']
#        predcFracErr += abs(0.5*(spf_cFrac_Up['rTrue'] - spf_cFrac_Down['rTrue'])*res['results'][tuple(metb)]['central'])
#
#        #Control region Poissonian
#        if mode=="data":
#          ref2b = getRefYield("2", htb,[150, 250] , "type1phiMet", 6, c, weight = "weight")
#        if mode=="mc":
#          ref2b = getRefYield("none", htb, [150, 250], "type1phiMet", 6, c, weight = "weightBTag2")
#
#        controlRegionPoissonianVar += (spf[key]*res['results'][tuple(metb)]['central']/sqrt(ref2b))**2
#
#      totVar+= predSFbErr**2
#      totVar+= predSFlErr**2
#      totVar+= predGluSplitErr**2
#      totVar+= predcFracErr**2
#
#      ires = getSampledMetYieldPrediction(exclusiveInDir, '2', ihtb, [metb])
#    #    print htb, metb, "==2b result", res['results'][tuple(metb)]['central']
#
#      #Sampling error from inclusive bin
#      spf = SpF[tuple(ihtb)][tuple(metb)][(6,99)]['SF']['3po2']
#      predSamplingErr = spf['rTrue']*0.5*(ires['results'][tuple(metb)]['varUp'] - ires['results'][tuple(metb)]['varDown'])
#      totVar+=predSamplingErr**2
#
#      predSpFNonClosureErr = SpFDataMCSys[tuple(ihtb)][tuple(metb)]*spf[key]*ires['results'][tuple(metb)]['central']
#      totVar+= predSpFNonClosureErr**2
#
#  #    print totVar, controlRegionPoissonianErr
#      totVarPlusCRP = totVar + controlRegionPoissonianVar
#
#      if mode=="data":
#        print "Result  :", metb, htb, "observed", round(ref,2),"+/-",round(refErr,2),"pred",round(pred,2),"+/-",round(sqrt(totVarPlusCRP),2)
#      else:
#        print "Closure :", metb, htb, "mcTruth",  round(ref,2),"+/-",round(refErr,2),"pred",round(pred,2),"+/-",round(sqrt(totVar),2),"(",round(sqrt(totVarPlusCRP),2),")"
