from analysisHelpers import *
import ROOT
from Workspace.RA4Analysis.simplePlotsCommon import *
from simpleStatTools import niceNum
import os, pickle, copy

sanityPlotDir = "/sanityModelPlots/"

dataDirectory = "/data/schoef/convertedTuples_v14/copyMET_separateBTagweights/"
mcDirectory = "/data/schoef/convertedTuples_v14/copyMET/"
mcDirectory_separateBTagWeights = "/data/schoef/convertedTuples_v14/copyMET_separateBTagWeights/"
jesPlusDirectory = "/data/schoef/convertedTuples_v14/copyMET_JES+/"
jesMinusDirectory = "/data/schoef/convertedTuples_v14/copyMET_JES-/"

cData       = getRefChain(dataDirectory, "Data")
cMC         = getRefChain(mcDirectory, "MC")
cMC_sep     = getRefChain(mcDirectory_separateBTagWeights, "MC")
cMCJESPlus  = getRefChain(jesPlusDirectory, "MC")
cMCJESMinus = getRefChain(jesMinusDirectory,"MC")
  
leptonCut = "((singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)||(singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))"
njetCut = "njets>=4"

metBinning = [(1500-150)/25,150,1500]

def makeSimpleCompPlot(histos, name, binning = defMetBinning, xLabel = "#slash{E}_{T} (GeV)", yLabel = "Events / 25 GeV", doRatio = True):
#  c1 = ROOT.TCanvas()
#  c1.SetLogy()
  stack = []
  for h in histos  :
    if h.has_key("takeBinningAndRangeFrom"):
      print "Hello"
      if h["histo"].GetBinWidth(1) == h["takeBinningAndRangeFrom"].GetBinWidth(1):
        htmp = h["histo"].Clone()
        h["histo"]= h["takeBinningAndRangeFrom"].Clone()
        h["histo"].Reset()
        for i in range(0,histos[0]["histo"].GetNbinsX()+1):
          tBin = htmp.FindBin(h["histo"].GetBinCenter(i))
          h["histo"].SetBinContent(i, htmp.GetBinContent(tBin))
          h["histo"].SetBinError(i,   htmp.GetBinError(tBin))
    v = variable(":xxx;"+xLabel+";"+yLabel,binning,"")
    v.data_histo = h["histo"]
    v.logy = "True"
    stack.append(v)
    for k in ["color", "style", "legendText", "ratioVarName"]: #copy attributes to variable
      if h.has_key(k):
        exec("v."+k+" = h['"+k+"']")
  if doRatio:
    stack[0].dataMCRatio = [stack[1], stack[0]]
  else:
    stack[0].dataMCRatio = "" 
  
  drawNMStacks(1,1,[stack],  sanityPlotDir+"/"+name)
#  c1.Print(sanityPlotDir+"/"+name+".png") 
#  c1.Print(sanityPlotDir+"/"+name+".pdf") 
#  c1.Print(sanityPlotDir+"/"+name+".root") 
  return stack

#for btb in [0,1,2]:
#  htb = [400,2500]
#  metb = [150, 2500]
#  cut = njetCut+"&&"+leptonCut+"&&ht>"+str(htb[0])+"&&ht<"+str(htb[1])+"&&met>"+str(metb[0])+"&&met<"+str(metb[1])+"&&"+btbCut[btb]
#
#  res   = getPredictionFromSamplingDirectory(goodDirectories['MC_central'], btb = btb, htb = htb, metb = metb, metvar = "met")
#
#  #Sanity Check: Input Histograms and Fit Result
#  hP = res['predictedShape']
##  hP.Scale(12./20.)
#  hMC = getRefMetHisto(cMC,cut) 
#  makeSimpleCompPlot([  {"histo":hP, "color":dataColor, "legendText":"prediction", "ratioVarName":"ratio","takeBinningAndRangeFrom":hMC},\
#                        {"histo":hMC,"color":ROOT.kBlue, "style":"l02","legendText":"MC truth", "ratioVarName":"ratio"}], 
#                      name="predictedShapeMC_vs_MC_btb_"+str(btb))
#  
#  #Sanity Check: JES fit results and MC reference 
#  resJes            = getUncertaintyFromSamplingDirectory(goodDirectories["JESRef"], goodDirectories["JESPlus"], goodDirectories["JESMinus"], res['predictedShape'], btb = btb, htb = htb, metb = metb, metvar = "met")
#  makeSimpleCompPlot([  {"histo":hP, "color":ROOT.kGray,"style":"l02", "legendText":"MC central", "ratioVarName":"ratio"},\
#                        {"histo":resJes["refShape"],   "color":ROOT.kBlack,"style":"l02", "legendText":"JES ref.", "ratioVarName":"ratio"},\
#                        {"histo":resJes["plusShape"],  "color":ROOT.kBlue, "style":"l02", "legendText":"JES+ ", "ratioVarName":"ratio"},
#                        {"histo":resJes["minusShape"], "color":ROOT.kRed,  "style":"l02", "legendText":"JES- ", "ratioVarName":"ratio"}] ,
#                      name="predictedShapeMC_vs_MC_JES_fitResults_btb_"+str(btb))
#
#  #Sanity Check: JES input plots
#  hMCJESPlus = getRefMetHisto(cMCJESPlus,cut) 
#  hMCJESMinus = getRefMetHisto(cMCJESMinus,cut) 
#  makeSimpleCompPlot([  {"histo":hP, "color":ROOT.kGray,"style":"l02", "legendText":"MC central", "ratioVarName":"ratio"},\
#                        {"histo":hMCJESPlus,  "color":ROOT.kBlue, "style":"l02", "legendText":"JES+ ", "ratioVarName":"ratio"},
#                        {"histo":hMCJESMinus, "color":ROOT.kRed,  "style":"l02", "legendText":"JES- ", "ratioVarName":"ratio"}] ,
#                      name="predictedShapeMC_vs_MC_JES_inputData_btb_"+str(btb))
  
#btag_SF_b_res     = getUncertaintyFromSamplingDirectory(goodDirectories["BTag_SF"], goodDirectories["BTag_SF_b_Up"]     , goodDirectories["BTag_SF_b_Down"]    , res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
#btag_SF_light_res = getUncertaintyFromSamplingDirectory(goodDirectories["BTag_SF"], goodDirectories["BTag_SF_light_Up"] , goodDirectories["BTag_SF_light_Down"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
#DiLep_res    = getUncertaintyFromSamplingDirectory(goodDirectories["DiLepRef"], goodDirectories["DiLepPlus"] , goodDirectories["DiLepMinus"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
#PU_res       = getUncertaintyFromSamplingDirectory(goodDirectories["PURef"], goodDirectories["PUPlus"] , goodDirectories["PUMinus"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
#TTPol_res    = getUncertaintyFromSamplingDirectory(goodDirectories["TTPolRef"], goodDirectories["TTPolPlus"] , goodDirectories["TTPolMinus"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")
#TTXSec_res    = getUncertaintyFromSamplingDirectory(goodDirectories["TTXSecRef"], goodDirectories["TTXSecPlus"] , goodDirectories["TTXSecMinus"], res["predictedShape"] , btb = btb, htb = htb, metb = metb, metvar = "met")

#option="data"
#c1 = makeNicePlot(goodDirectories, btb, htb, metb, option = option)
#c1.Print(defaultWWWPath+"/sanityResults2012/"+option+"_btb_"+str(btb)+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_metb_"+str(metb[0])+"_"+str(metb[0])+".png")
#c1.Print(defaultWWWPath+"/sanityResults2012/"+option+"_btb_"+str(btb)+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_metb_"+str(metb[0])+"_"+str(metb[0])+".pdf")
#c1.Print(defaultWWWPath+"/sanityResults2012/"+option+"_btb_"+str(btb)+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_metb_"+str(metb[0])+"_"+str(metb[0])+".root")

#checking sampling directory 

##MC
#inDir = "/data/schoef/RA4Fit2012/output/Results_copyMET_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121220_0653" 
#referenceDir = mcDirectory
#refWeight = "weight"
#mode="MC"

##MC using BTag SF
inDir = "/data/schoef/RA4Fit2012/output/Results_copyMET_separateBTagWeights_BTag_SF_fitMC_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121220_2014/"
referenceDir = mcDirectory_separateBTagWeights
refWeight = "weightBTag_SF"
mode = "MC"

#Data
#inDir = "/data/schoef/RA4Fit2012/output/Results_copyMET_separateBTagWeights_fitData_MuonElectron_jet3pt40_150.0-met-400.0_400.0-ht-750.0_intLumi-20p0_121219_2255/"
#referenceDir = mcDirectory
#mode="data"

SpF_4j = pickle.load(file('/data/schoef/results2012/btagEff/SpF_HT400MET150_11fb.pkl'))

refChain = getRefChain(referenceDir, mode)
higherBTagShape = {'3':{}, '4p':{}}

#cross check spill factors with b-tag SF weighted events in ttbar:
#ttOnlyRefChain = getRefChain(referenceDir, "MC", onlyTT = True)
#SpF_4j[(400,450)][tuple(metNormReg)][-1]['SF']['3o2']['rTrue'] == getRefYield(-1, [400, 450], metNormReg, "met", ttOnlyRefChain, weight="weightBTag3_SF") / getRefYield(-1, [400, 450], metNormReg, "met", ttOnlyRefChain, weight="weightBTag2_SF")

for btb in [0,1,2]:
  htb = [400,2500]
  cut = njetCut+"&&"+leptonCut+"&&ht>="+str(htb[0])+"&&ht<"+str(htb[1])+"&&"+btbCut[btb]
  hRef = getRefMetHisto(refChain, cut, weight = refWeight)
  sumNormRegYield = 0.
  sumNormRegYieldRef = 0.
  print "\n\nChecking SamplingDirectory vs. binned results: htb:",htb,"btb", btb,"\n\n[Check] Inclusive NormRegYield wrt. to Ref: btb",btb,"htb",htb,"metb",metNormReg,", getNormRegYieldFromSamplingDirectory",getNormRegYieldFromSamplingDirectory(inDir, btb, htb), ", getRefMetHisto(Ref)", histIntegral(hRef, 150, 250), "getRefYield(refChain)", getRefYield(btb, htb, metNormReg, "met", refChain, weight = refWeight)
  predictedSumShape = ""
  for htb2 in htbins:
    if htb2[0]>=htb[0] and htb2[1]<=htb[1]:
      nRY = getNormRegYield(inDir, btb, htb2 )
      mcT = getRefYield(btb, htb2, metNormReg, "met", refChain, weight = refWeight)
      sumNormRegYield    += nRY[0]
      sumNormRegYieldRef +=mcT 
      binnedShape = getPredictedMetShape(inDir, btb, htb2)
      scaleFac = nRY[0]/histIntegral(binnedShape, metNormReg[0], metNormReg[1])
      binnedShape.Scale(scaleFac)
      if predictedSumShape=="":
        predictedSumShape = binnedShape
      else:
        predictedSumShape.Add(binnedShape)
      print "[Check] contained htb", htb2, ",getNormRegYield", nRY, ",getRefTruthYield", mcT, "scaleFac"
      
      if btb==2:
        for btk in ['SF_b_Down', 'SF_b_Up', 'SF_light_Down', 'SF', 'SF_light_Up']:
          if mode.lower()=="data": 
            spfk = 'rForData'
          else:
            spfk = 'rTrue'
          nRY_b3  = nRY[0]*SpF_4j[tuple(htb2)][tuple(metNormReg)][-1][btk]['3o2'][spfk]
          nRY_b4p = nRY[0]*SpF_4j[tuple(htb2)][tuple(metNormReg)][-1][btk]['4po2'][spfk]
          binnedShape_b3 = binnedShape.Clone()
          binnedShape_b3.Scale(nRY_b3/nRY[0])
          binnedShape_b4p = binnedShape.Clone()
          binnedShape_b4p.Scale(nRY_b4p/nRY[0])
          if not higherBTagShape['3'].has_key(btk):
            higherBTagShape['3'][btk] = binnedShape_b3.Clone("prediction_b3_ht_"+str(htb[0])+"_"+str(htb[1]) )
          else:
            higherBTagShape['3'][btk].Add(binnedShape_b3)
            
          if not higherBTagShape['4p'].has_key(btk):
            higherBTagShape['4p'][btk] = binnedShape_b4p.Clone("prediction_b3_ht_"+str(htb[0])+"_"+str(htb[1]) )
          else:
            higherBTagShape['4p'][btk].Add(binnedShape_b4p)
            
  normYieldPredictedSumShape = histIntegral(predictedSumShape, metNormReg[0], metNormReg[1])
  print "[Check] Sum of HT bins: NormRegYield",sumNormRegYield,"Ref:",sumNormRegYieldRef,"sumShape NormRegYield", normYieldPredictedSumShape,"\n\n"
  samplingRes = getPredictionFromSamplingDirectory(inDir, btb = btb, htb = htb, metb = metNormReg, metvar = "met")
  samplingRes["predictedShape"].Draw()
  predictedSumShape.Draw("same")
  fname = "checkSamplingDir_vs_binnedDir_ht_"+str(htb[0])+"_"+str(htb[1])+"_btb"+str(btb)
  makeSimpleCompPlot([  {"histo":samplingRes["predictedShape"],        "color":ROOT.kGray,  "style":"l02", "legendText":"pred. from sampling"},\
                        {"histo":hRef, "color":ROOT.kRed,  "style":"l02", "legendText":"Input from Ref dir."},
                        {"histo":predictedSumShape,  "color":ROOT.kBlack, "style":"l02", "legendText":"pred. from summing HT bins"}
#                        {"histo":dataShapeFromSamplingDir.GetHistogram(), "color":ROOT.kBlue,  "style":"l02", "legendText":"Input from sampling dir."}
                      ] , name=fname, doRatio = False)
  if btb==2:
    cut_no_b_requirement = njetCut+"&&"+leptonCut+"&&ht>="+str(htb[0])+"&&ht<"+str(htb[1])
    hRef_b3  = getRefMetHisto(refChain, cut_no_b_requirement+"&&nbtags==3", weight = refWeight)
    fname = "higherBshape_ht_"+str(htb[0])+"_"+str(htb[1])+"_btb"
    makeSimpleCompPlot([  {"histo":higherBTagShape['3']['SF'],  "color":ROOT.kBlack,  "style":"l02", "legendText":"3b prediction"},\
                          {"histo":hRef_b3, "color":ROOT.kRed,  "style":"l02", "legendText":"3b shape"}
  #                        {"histo":dataShapeFromSamplingDir.GetHistogram(), "color":ROOT.kBlue,  "style":"l02", "legendText":"Input from sampling dir."}
                        ] , name=fname+"_b3", doRatio = False)
    hRef_b4p = getRefMetHisto(refChain, cut_no_b_requirement+"&&nbtags>=4", weight = refWeight)
    makeSimpleCompPlot([  
                          {"histo":higherBTagShape['4p']['SF'],       "color":ROOT.kBlack,  "style":"l02", "legendText":"#geq 4b prediction"},\
                          {"histo":higherBTagShape['4p']['SF_b_Up'],  "color":ROOT.kGray,  "style":"l02", "legendText":"#geq 4b prediction, b_Up"},\
                          {"histo":higherBTagShape['4p']['SF_b_Down'],  "color":ROOT.kGray,  "style":"l02", "legendText":"#geq 4b prediction, b_Down"},\
#                          {"histo":higherBTagShape['4p']['SF_light_Up'],  "color":ROOT.kGray,  "style":"l02", "legendText":"#geq 4b prediction, l_Up"},\
#                          {"histo":higherBTagShape['4p']['SF_light_Down'],  "color":ROOT.kGray,  "style":"l02", "legendText":"#geq 4b prediction, l_Down"},\
                          {"histo":hRef_b4p, "color":ROOT.kRed,  "style":"l02", "legendText":"#geq 4b shape"}
  #                        {"histo":dataShapeFromSamplingDir.GetHistogram(), "color":ROOT.kBlue,  "style":"l02", "legendText":"Input from sampling dir."}
                        ] , name=fname+"_b4p", doRatio = False)
  

#  c1 = ROOT.TCanvas()
#  c1.cd()
#  c1.SetLogy()
#  hFit = dataShapeFromSamplingDir.GetHistogram()
#  dataShapeFromSamplingDir.Draw()
#  hMC.SetLineColor(ROOT.kRed)
#  hMC.Draw()
#  hFit.Draw("same")
#  dataShapeFromSamplingDir = getDataMetShapeFromSamplingDirectory(inDir, btb, htb)
#  c1.Print(defaultWWWPath+"/"+sanityPlotDir+"/MC_inputVSsamplingDir_"+fname+".png")
