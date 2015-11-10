import ROOT
import os, sys
from ROOT import RooFit as rf

from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
from Workspace.HEPHYPythonTools.user import username
from math import pi, sqrt, isnan
from rCShelpers import *# weight_str , weight_err_str , lumi

from predictionConfig import *

def binnedNBTagsFit(cut, cutname, samples, prefix = "", QCD_dict={0:{'y':0.,'e':0.,'totalY':0.}, 1:{'y':0.,'e':0.,'totalY':0.},2:{'y':0.,'e':0.,'totalY':0.}}):
  #print "LUMI:" , lumi
  #if not os.path.exists(printDir):
  #   os.makedirs(printDir) 
  #if not os.path.exists(templateDir):
  #   os.makedirs(templateDir)
  weight_str, weight_err_str = makeWeight(lumi, sampleLumi)
  cWJets = samples['W']
  cTTJets = samples['TT']
  cRest = samples['Rest']
  cData = samples['Data']
  
  #templateLumi = 1.26
  errorScale = 1
  if errorScale != 1:
    print '############################## DANGER! ERROR IN TEMPLATE DOWNSCALED! DANGER! ##################################################################################'
  
  if isData: w = weight_str
  else: w = 'weight'
  
  hQCD = ROOT.TH1F('hQCD','hQCD',len([0,1,2,3])-1, array('d',[0,1,2,3]))
  for n in range(3):
    if isnan(QCD_dict[n]['y']): QCD_dict[n]['y'] = QCD_dict[n]['totalY']
    hQCD.SetBinContent(n+1,QCD_dict[n]['y']/2) #divide by 2 to split in +/- charge
    if isnan(QCD_dict[n]['e']): qcdErr = QCD_dict[n]['y']
    else: qcdErr = QCD_dict[n]['e']
    hQCD.SetBinError(n+1,qcdErr/2)
  
  #Get histograms binned in b-tag multiplicity
  template_WJets_PosPdg_Dict = getTemplate(cutname, templateDir, 'WJets_PosPdg') #these templates will always be MC, so a reweighting (e.g. b-tagging) should not be used
  if template_WJets_PosPdg_Dict['loadTemp']:
    template_WJets_PosPdg = template_WJets_PosPdg_Dict['hist']
    tempFile_WJets_PosPdg = template_WJets_PosPdg_Dict['file']
  else:
    template_WJets_PosPdg = getPlotFromChain(cWJets, nBTagVar, [0,1,2,3], 'leptonPdg>0&&'+cut, weight_str, binningIsExplicit=True,addOverFlowBin='upper')
    if templateWeights:
      template_WJets_PosPdg.SetBinContent(1,getYieldFromChain(cWJets, cutString = 'leptonPdg>0&&'+cut, weight = weight_str+'*weightBTag0'+templateWeightSuffix))
      template_WJets_PosPdg.SetBinError(1,  errorScale*sqrt(getYieldFromChain(cWJets, cutString = 'leptonPdg>0&&'+cut, weight = weight_err_str+'*weightBTag0'+templateWeightSuffix+'**2')))
      template_WJets_PosPdg.SetBinContent(2,getYieldFromChain(cWJets, cutString = 'leptonPdg>0&&'+cut, weight = weight_str+'*weightBTag1'+templateWeightSuffix))
      template_WJets_PosPdg.SetBinError(2,  errorScale*sqrt(getYieldFromChain(cWJets, cutString = 'leptonPdg>0&&'+cut, weight = weight_err_str+'*weightBTag1'+templateWeightSuffix+'**2')))
      template_WJets_PosPdg.SetBinContent(3,getYieldFromChain(cWJets, cutString = 'leptonPdg>0&&'+cut, weight = weight_str+'*weightBTag2'+templateWeightSuffix))
      template_WJets_PosPdg.SetBinError(3,  errorScale*sqrt(getYieldFromChain(cWJets, cutString = 'leptonPdg>0&&'+cut, weight = weight_err_str+'*weightBTag2'+templateWeightSuffix+'**2')))
    tempFile_WJets_PosPdg = ROOT.TFile(templateDir+cutname+'_WJets_PosPdg.root','new')
    template_WJets_PosPdg.Write()
    #tempFile.Close()

  template_WJets_NegPdg_Dict = getTemplate(cutname, templateDir, 'WJets_NegPdg') #these templates will always be MC, so a reweighting (e.g. b-tagging) should not be used
  if template_WJets_NegPdg_Dict['loadTemp']:
    template_WJets_NegPdg = template_WJets_NegPdg_Dict['hist']
    tempFile_WJets_NegPdg = template_WJets_NegPdg_Dict['file']
  else: 
    template_WJets_NegPdg = getPlotFromChain(cWJets, nBTagVar, [0,1,2,3], 'leptonPdg<0&&'+cut, weight_str, binningIsExplicit=True,addOverFlowBin='upper')
    if templateWeights:
      template_WJets_NegPdg.SetBinContent(1,getYieldFromChain(cWJets, cutString = 'leptonPdg<0&&'+cut, weight = weight_str+'*weightBTag0'+templateWeightSuffix))
      template_WJets_NegPdg.SetBinError(1,  errorScale*sqrt(getYieldFromChain(cWJets, cutString = 'leptonPdg<0&&'+cut, weight = weight_err_str+'*weightBTag0'+templateWeightSuffix+'**2')))
      template_WJets_NegPdg.SetBinContent(2,getYieldFromChain(cWJets, cutString = 'leptonPdg<0&&'+cut, weight = weight_str+'*weightBTag1'+templateWeightSuffix))
      template_WJets_NegPdg.SetBinError(2,  errorScale*sqrt(getYieldFromChain(cWJets, cutString = 'leptonPdg<0&&'+cut, weight = weight_err_str+'*weightBTag1'+templateWeightSuffix+'**2')))
      template_WJets_NegPdg.SetBinContent(3,getYieldFromChain(cWJets, cutString = 'leptonPdg<0&&'+cut, weight = weight_str+'*weightBTag2'+templateWeightSuffix))
      template_WJets_NegPdg.SetBinError(3,  errorScale*sqrt(getYieldFromChain(cWJets, cutString = 'leptonPdg<0&&'+cut, weight = weight_err_str+'*weightBTag2'+templateWeightSuffix+'**2')))
    tempFile_WJets_NegPdg = ROOT.TFile(templateDir+cutname+'_WJets_NegPdg.root','new')
    template_WJets_NegPdg.Write()
    #tempFile.Close()

  template_TTJets_Dict = getTemplate(cutname, templateDir, 'TTJets') #these templates will always be MC, so a reweighting (e.g. b-tagging) should not be used
  if template_TTJets_Dict['loadTemp']:
    template_TTJets = template_TTJets_Dict['hist']
    tempFile_TTJets = template_TTJets_Dict['file']
  else: 
    template_TTJets = getPlotFromChain(cTTJets, nBTagVar, [0,1,2,3], cut, weight_str, binningIsExplicit=True,addOverFlowBin='upper')
    if templateWeights:
      template_TTJets.SetBinContent(1,getYieldFromChain(cTTJets, cutString = cut, weight = weight_str+'*weightBTag0'+templateWeightSuffix))
      template_TTJets.SetBinError(1,  errorScale*sqrt(getYieldFromChain(cTTJets, cutString = cut, weight = weight_err_str+'*weightBTag0'+templateWeightSuffix+'**2')))
      template_TTJets.SetBinContent(2,getYieldFromChain(cTTJets, cutString = cut, weight = weight_str+'*weightBTag1'+templateWeightSuffix))
      template_TTJets.SetBinError(2,  errorScale*sqrt(getYieldFromChain(cTTJets, cutString = cut, weight = weight_err_str+'*weightBTag1'+templateWeightSuffix+'**2')))
      template_TTJets.SetBinContent(3,getYieldFromChain(cTTJets, cutString = cut, weight = weight_str+'*weightBTag2'+templateWeightSuffix))
      template_TTJets.SetBinError(3,  errorScale*sqrt(getYieldFromChain(cTTJets, cutString = cut, weight = weight_err_str+'*weightBTag2'+templateWeightSuffix+'**2')))
    tempFile_TTJets = ROOT.TFile(templateDir+cutname+'_TTJets.root','new')
    template_TTJets.Write()
    #tempFile.Close()

  template_Rest_PosPdg_Dict = getTemplate(cutname, templateDir, 'Rest_PosPdg') #these templates will always be MC, so a reweighting (e.g. b-tagging) should not be used
  if template_Rest_PosPdg_Dict['loadTemp']:
    template_Rest_PosPdg = template_Rest_PosPdg_Dict['hist']
    tempFile_Rest_PosPdg = template_Rest_PosPdg_Dict['file']
  else: 
    template_Rest_PosPdg = getPlotFromChain(cRest, nBTagVar, [0,1,2,3], 'leptonPdg>0&&'+cut, weight_str, binningIsExplicit=True,addOverFlowBin='upper')
    tempFile_Rest_PosPdg = ROOT.TFile(templateDir+cutname+'_Rest_PosPdg.root','new')
    template_Rest_PosPdg.Write()
    #tempFile.Close()

  template_Rest_NegPdg_Dict = getTemplate(cutname, templateDir, 'Rest_NegPdg') #these templates will always be MC, so a reweighting (e.g. b-tagging) should not be used
  if template_Rest_NegPdg_Dict['loadTemp']:
    template_Rest_NegPdg = template_Rest_NegPdg_Dict['hist']
    tempFile_Rest_NegPdg = template_Rest_NegPdg_Dict['file']
  else: 
    template_Rest_NegPdg = getPlotFromChain(cRest, nBTagVar, [0,1,2,3], 'leptonPdg<0&&'+cut, weight_str, binningIsExplicit=True,addOverFlowBin='upper')
    tempFile_Rest_NegPdg = ROOT.TFile(templateDir+cutname+'_Rest_NegPdg.root','new')
    template_Rest_NegPdg.Write()
    #tempFile.Close()

  #template_WJets_PosPdg=getPlotFromChain(cWJets, nBTagVar, [0,1,2,3], 'leptonPdg>0&&'+cut, weight_str, binningIsExplicit=True,addOverFlowBin='upper')
  #template_WJets_NegPdg=getPlotFromChain(cWJets, nBTagVar, [0,1,2,3], 'leptonPdg<0&&'+cut, weight_str, binningIsExplicit=True,addOverFlowBin='upper')
  #template_TTJets=      getPlotFromChain(cTTJets,nBTagVar, [0,1,2,3], cut,                 weight_str, binningIsExplicit=True,addOverFlowBin='upper')
  #template_Rest_PosPdg= getPlotFromChain(cRest,  nBTagVar, [0,1,2,3], 'leptonPdg>0&&'+cut, weight_str, binningIsExplicit=True,addOverFlowBin='upper')
  #template_Rest_NegPdg= getPlotFromChain(cRest,  nBTagVar, [0,1,2,3], 'leptonPdg<0&&'+cut, weight_str, binningIsExplicit=True,addOverFlowBin='upper')

  print "Nominal yields TT:",template_TTJets.Integral(),'WJets_PosPdg',template_WJets_PosPdg.Integral(),'WJets_NegPdg',template_WJets_NegPdg.Integral()
  print "Nominal yields:",'Rest_PosPdg',template_Rest_PosPdg.Integral(),'Rest_NegPdg',template_Rest_NegPdg.Integral()
  
  # use this for fake data
  if useBTagWeights:
    hData_PosPdg = getPlotFromChain(cRest, nBTagVar, [0,1,2,3], 'leptonPdg>0&&'+cut, weight_str, binningIsExplicit=True,addOverFlowBin='upper')
    #hData_PosPdg.Sumw2()
    bin1 = hData_PosPdg.GetBinContent(1)
    bin1Var = (hData_PosPdg.GetBinError(1))**2
    bin1    += getYieldFromChain(cWJets, cutString =   'leptonPdg>0&&'+cut, weight = weight_str+'*weightBTag0'+btagWeightSuffix)
    bin1Var += getYieldFromChain(cWJets, cutString =   'leptonPdg>0&&'+cut, weight = weight_err_str+'*weightBTag0'+btagWeightSuffix+'**2')
    bin1    += getYieldFromChain(cTTJets, cutString =  'leptonPdg>0&&'+cut, weight = weight_str+'*weightBTag0'+btagWeightSuffix)
    bin1Var += getYieldFromChain(cTTJets, cutString =   'leptonPdg>0&&'+cut, weight = weight_err_str+'*weightBTag0'+btagWeightSuffix+'**2')
    hData_PosPdg.SetBinContent(1,bin1)
    hData_PosPdg.SetBinError(1,sqrt(bin1Var))
    
    bin2 = hData_PosPdg.GetBinContent(2)
    bin2Var = (hData_PosPdg.GetBinError(2))**2
    bin2    += getYieldFromChain(cWJets, cutString =   'leptonPdg>0&&'+cut, weight = weight_str+'*weightBTag1'+btagWeightSuffix)
    bin2Var += getYieldFromChain(cWJets, cutString =   'leptonPdg>0&&'+cut, weight = weight_err_str+'*weightBTag1'+btagWeightSuffix+'**2')
    bin2    += getYieldFromChain(cTTJets, cutString =  'leptonPdg>0&&'+cut, weight = weight_str+'*weightBTag1'+btagWeightSuffix)
    bin2Var += getYieldFromChain(cTTJets, cutString =   'leptonPdg>0&&'+cut, weight = weight_err_str+'*weightBTag1'+btagWeightSuffix+'**2')
    hData_PosPdg.SetBinContent(2,bin2)
    hData_PosPdg.SetBinError(2,sqrt(bin2Var))
    
    bin3 = hData_PosPdg.GetBinContent(3)
    bin3Var = (hData_PosPdg.GetBinError(3))**2
    bin3    += getYieldFromChain(cWJets, cutString =   'leptonPdg>0&&'+cut, weight = weight_str+'*weightBTag2'+btagWeightSuffix)
    bin3Var += getYieldFromChain(cWJets, cutString =   'leptonPdg>0&&'+cut, weight = weight_err_str+'*weightBTag2'+btagWeightSuffix+'**2')
    bin3    += getYieldFromChain(cTTJets, cutString =  'leptonPdg>0&&'+cut, weight = weight_str+'*weightBTag2'+btagWeightSuffix)
    bin3Var += getYieldFromChain(cTTJets, cutString =   'leptonPdg>0&&'+cut, weight = weight_err_str+'*weightBTag2'+btagWeightSuffix+'**2')
    hData_PosPdg.SetBinContent(3,bin3)
    hData_PosPdg.SetBinError(3,sqrt(bin3Var))
    #hData_PosPdg.Fill(0,getYieldFromChain(cWJets, cutString =   'leptonPdg>0&&'+cut, weight = weight_str+'*weightBTag0'+btagWeightSuffix))
    #hData_PosPdg.Fill(1,getYieldFromChain(cWJets, cutString =   'leptonPdg>0&&'+cut, weight = weight_str+'*weightBTag1'+btagWeightSuffix))
    #hData_PosPdg.Fill(2,getYieldFromChain(cWJets, cutString =   'leptonPdg>0&&'+cut, weight = weight_str+'*weightBTag2'+btagWeightSuffix))
    #hData_PosPdg.Fill(0,getYieldFromChain(cTTJets, cutString =  'leptonPdg>0&&'+cut, weight = weight_str+'*weightBTag0'+btagWeightSuffix))
    #hData_PosPdg.Fill(1,getYieldFromChain(cTTJets, cutString =  'leptonPdg>0&&'+cut, weight = weight_str+'*weightBTag1'+btagWeightSuffix))
    #hData_PosPdg.Fill(2,getYieldFromChain(cTTJets, cutString =  'leptonPdg>0&&'+cut, weight = weight_str+'*weightBTag2'+btagWeightSuffix))
    
    hData_NegPdg = getPlotFromChain(cRest, nBTagVar, [0,1,2,3], 'leptonPdg<0&&'+cut, weight_str, binningIsExplicit=True,addOverFlowBin='upper')
    #hData_NegPdg.Sumw2()
    bin1 = hData_NegPdg.GetBinContent(1)
    bin1Var = (hData_NegPdg.GetBinError(1))**2
    bin1    += getYieldFromChain(cWJets, cutString =   'leptonPdg<0&&'+cut, weight = weight_str+'*weightBTag0'+btagWeightSuffix)
    bin1Var += getYieldFromChain(cWJets, cutString =   'leptonPdg<0&&'+cut, weight = weight_err_str+'*weightBTag0'+btagWeightSuffix+'**2')
    bin1    += getYieldFromChain(cTTJets, cutString =  'leptonPdg<0&&'+cut, weight = weight_str+'*weightBTag0'+btagWeightSuffix)
    bin1Var += getYieldFromChain(cTTJets, cutString =  'leptonPdg<0&&'+cut, weight = weight_err_str+'*weightBTag0'+btagWeightSuffix+'**2')
    hData_NegPdg.SetBinContent(1,bin1)
    hData_NegPdg.SetBinError(1,sqrt(bin1Var))

    bin2 = hData_NegPdg.GetBinContent(2)
    bin2Var = (hData_NegPdg.GetBinError(2))**2
    bin2    += getYieldFromChain(cWJets, cutString =   'leptonPdg<0&&'+cut, weight = weight_str+'*weightBTag1'+btagWeightSuffix)
    bin2Var += getYieldFromChain(cWJets, cutString =   'leptonPdg<0&&'+cut, weight = weight_err_str+'*weightBTag1'+btagWeightSuffix+'**2')
    bin2    += getYieldFromChain(cTTJets, cutString =  'leptonPdg<0&&'+cut, weight = weight_str+'*weightBTag1'+btagWeightSuffix)
    bin2Var += getYieldFromChain(cTTJets, cutString =  'leptonPdg<0&&'+cut, weight = weight_err_str+'*weightBTag1'+btagWeightSuffix+'**2')
    hData_NegPdg.SetBinContent(2,bin2)
    hData_NegPdg.SetBinError(2,sqrt(bin2Var))

    bin3 = hData_NegPdg.GetBinContent(3)
    bin3Var = (hData_NegPdg.GetBinError(3))**2
    bin3    += getYieldFromChain(cWJets, cutString =   'leptonPdg<0&&'+cut, weight = weight_str+'*weightBTag2'+btagWeightSuffix)
    bin3Var += getYieldFromChain(cWJets, cutString =   'leptonPdg<0&&'+cut, weight = weight_err_str+'*weightBTag2'+btagWeightSuffix+'**2')
    bin3    += getYieldFromChain(cTTJets, cutString =  'leptonPdg<0&&'+cut, weight = weight_str+'*weightBTag2'+btagWeightSuffix)
    bin3Var += getYieldFromChain(cTTJets, cutString =  'leptonPdg<0&&'+cut, weight = weight_err_str+'*weightBTag2'+btagWeightSuffix+'**2')
    hData_NegPdg.SetBinContent(3,bin3)
    hData_NegPdg.SetBinError(3,sqrt(bin3Var))
    #hData_NegPdg.Fill(0,getYieldFromChain(cWJets, cutString =   'leptonPdg<0&&'+cut, weight = weight_str+'*weightBTag0'+btagWeightSuffix))
    #hData_NegPdg.Fill(1,getYieldFromChain(cWJets, cutString =   'leptonPdg<0&&'+cut, weight = weight_str+'*weightBTag1'+btagWeightSuffix))
    #hData_NegPdg.Fill(2,getYieldFromChain(cWJets, cutString =   'leptonPdg<0&&'+cut, weight = weight_str+'*weightBTag2'+btagWeightSuffix))
    #hData_NegPdg.Fill(0,getYieldFromChain(cTTJets, cutString =  'leptonPdg<0&&'+cut, weight = weight_str+'*weightBTag0'+btagWeightSuffix))
    #hData_NegPdg.Fill(1,getYieldFromChain(cTTJets, cutString =  'leptonPdg<0&&'+cut, weight = weight_str+'*weightBTag1'+btagWeightSuffix))
    #hData_NegPdg.Fill(2,getYieldFromChain(cTTJets, cutString =  'leptonPdg<0&&'+cut, weight = weight_str+'*weightBTag2'+btagWeightSuffix))

  ##### use this for DATA
  else:
    hData_PosPdg = getPlotFromChain(cData, nBTagVar, [0,1,2,3], 'leptonPdg>0&&'+cut, w, binningIsExplicit=True,addOverFlowBin='upper')
    hData_NegPdg = getPlotFromChain(cData, nBTagVar, [0,1,2,3], 'leptonPdg<0&&'+cut, w, binningIsExplicit=True,addOverFlowBin='upper')
    hData_PosPdg.Add(hQCD,-1)
    hData_NegPdg.Add(hQCD,-1)
  hData_PosPdg_File = ROOT.TFile(templateDir+cutname+'_PosPdg_DataHist.root','new')
  hData_PosPdg.Write()
  hData_NegPdg_File = ROOT.TFile(templateDir+cutname+'_NegPdg_DataHist.root','new')
  hData_NegPdg.Write()
    
  print "Nominal yields data Pos:", hData_PosPdg.Integral()
  print "Nominal yields data Neg:", hData_NegPdg.Integral()

  #print 'Error in the 0b bin of the data hist, neg PDG:',hData_NegPdg.GetBinError(1)
  #print 'Error in the 0b bin of the data hist, pos PDG:',hData_PosPdg.GetBinError(1)

  #print 'Resetting the errors!'
  #for i in range(1,4):
  #  print 'Yield and error before scaling',hData_NegPdg.GetBinContent(i), hData_NegPdg.GetBinError(i)
  #  hData_NegPdg.SetBinError(i, 10*hData_NegPdg.GetBinError(i))
  #  print 'Yield and error after scaling',hData_NegPdg.GetBinContent(i), hData_NegPdg.GetBinError(i)
  #  hData_PosPdg.SetBinError(i, 10*hData_PosPdg.GetBinError(i))
  

  ##hData_PosPdg=getPlotFromChain(cData,nBTagVar,[0,1,2,3],mTCut+'&&'+nameAndCut(metb,htb,njetb,'pos',btagRequirement='None')[1],weight_str,binningIsExplicit=True,addOverFlowBin='upper')
  ##hData_NegPdg=getPlotFromChain(cData,nBTagVar,[0,1,2,3],mTCut+'&&'+nameAndCut(metb,htb,njetb,'neg',btagRequirement='None')[1],weight_str,binningIsExplicit=True,addOverFlowBin='upper')
  #hData_PosPdg = template_TTJets.Clone()
  #hData_PosPdg.Scale(0.5)
  #hData_PosPdg.Add(template_WJets_PosPdg)
  #hData_PosPdg.Add(template_Rest_PosPdg)
  #hData_NegPdg = template_TTJets.Clone()
  #hData_NegPdg.Scale(0.5)
  #hData_NegPdg.Add(template_WJets_NegPdg)
  #hData_NegPdg.Add(template_Rest_NegPdg)

  print "BEFORE FIT YIELDS Templates before scaling:"
  print "template_WJets_NegPdg:" , template_WJets_NegPdg.Integral() 
  print "template_WJets_PosPdg:" , template_WJets_PosPdg.Integral()
  print "template_TTJets:" ,       template_TTJets.Integral()
  print "template_Rest_PosPdg:" ,  template_Rest_PosPdg.Integral()
  print "template_Rest_NegPdg:" ,  template_Rest_NegPdg.Integral()

  #Normalize histograms
  template_TTJets.Scale(1./template_TTJets.Integral())
  template_WJets_PosPdg.Scale(1./template_WJets_PosPdg.Integral())
  template_WJets_NegPdg.Scale(1./template_WJets_NegPdg.Integral())
  y_Rest_PosPdg = template_Rest_PosPdg.Integral()*lumi/templateLumi
  y_Rest_NegPdg = template_Rest_NegPdg.Integral()*lumi/templateLumi
  template_Rest_PosPdg.Scale(1./template_Rest_PosPdg.Integral())
  template_Rest_NegPdg.Scale(1./template_Rest_NegPdg.Integral())
  #hData_PosPdg.Scale(1./hData_PosPdg.Integral())
  #hData_NegPdg.Scale(1./hData_NegPdg.Integral())
  #Observable
  x=ROOT.RooRealVar(nBTagVar,nBTagVar,0.,3.)

  #import the contents of 'data' ROOT histogram into a RooDataHist object 
  data_PosPdg=ROOT.RooDataHist("data","data",ROOT.RooArgList(x),hData_PosPdg)
  data_NegPdg=ROOT.RooDataHist("data","data",ROOT.RooArgList(x),hData_NegPdg)

  dh_WJets_PosPdg=ROOT.RooDataHist("mcWJets","mcWJets",ROOT.RooArgList(x),template_WJets_PosPdg)
  dh_WJets_NegPdg=ROOT.RooDataHist("mcWJets","mcWJets",ROOT.RooArgList(x),template_WJets_NegPdg)
  dh_TTJets=ROOT.RooDataHist("mcTTJets","mcTTJets",ROOT.RooArgList(x),template_TTJets)
  dh_Rest_PosPdg=ROOT.RooDataHist("mcRest","mcRest",ROOT.RooArgList(x),template_Rest_PosPdg)
  dh_Rest_NegPdg=ROOT.RooDataHist("mcRest","mcRest",ROOT.RooArgList(x),template_Rest_NegPdg)

  rooDataHist_arr = [data_NegPdg , data_PosPdg , dh_WJets_PosPdg , dh_WJets_NegPdg , dh_TTJets , dh_Rest_PosPdg , dh_Rest_NegPdg]
  print "write RooDataHist values bin by bin"
  for hist in rooDataHist_arr:
    print "roo data hist: " , hist.Print()
    for i in range(hist.numEntries()): 
      hist.get(i)
      print "weight :" , hist.weight()

  #Define yields as variable
  yield_TTJets=ROOT.RooRealVar("ttJets_yield","yieldTTJets",0.1,0,10**5)
  yield_WJets_PosPdg = ROOT.RooRealVar("yield_WJets_PosPdg","yield_WJets_PosPdg",0.1,0,10**5)
  yield_WJets_NegPdg = ROOT.RooRealVar("yield_WJets_NegPdg","yield_WJets_NegPdg",0.1,0,10**5)
#  yield_Rest_PosPdg = ROOT.RooRealVar("yield_Rest_PosPdg","yield_Rest_PosPdg",0.1,0,10**5)
#  yield_Rest_NegPdg = ROOT.RooRealVar("yield_Rest_NegPdg","yield_Rest_NegPdg",0.1,0,10**5)
  yield_Rest_PosPdg = ROOT.RooRealVar("yield_Rest_PosPdg","yield_Rest_PosPdg",y_Rest_PosPdg,y_Rest_PosPdg,y_Rest_PosPdg)
  yield_Rest_NegPdg = ROOT.RooRealVar("yield_Rest_NegPdg","yield_Rest_NegPdg",y_Rest_NegPdg,y_Rest_NegPdg,y_Rest_NegPdg)
  yield_Rest_PosPdg.setConstant()
  yield_Rest_NegPdg.setConstant()

  print "BEFORE FIT YIELDS:"
  print "yield_WJets_NegPdg:" , yield_WJets_NegPdg.getVal()
  print "yield_WJets_PosPdg:" , yield_WJets_PosPdg.getVal()
  print "yield_TTJets:" , yield_TTJets.getVal()
  print "yield_Rest_PosPdg:" , yield_Rest_PosPdg.getVal()
  print "yield_Rest_NegPdg:" , yield_Rest_NegPdg.getVal()
  #Make PDF from MC histograms
  model_WJets_PosPdg=ROOT.RooHistPdf("model_WJets_PosPdg","model_WJets_PosPdg",ROOT.RooArgSet(x),dh_WJets_PosPdg)
  model_WJets_NegPdg=ROOT.RooHistPdf("model_WJets_NegPdg","model_WJets_NegPdg",ROOT.RooArgSet(x),dh_WJets_NegPdg)
  model_TTJets=ROOT.RooHistPdf("model_TTJets","model_TTJets",ROOT.RooArgSet(x),dh_TTJets)
  model_Rest_PosPdg=ROOT.RooHistPdf("model_Rest_PosPdg","model_Rest_PosPdg",ROOT.RooArgSet(x),dh_Rest_PosPdg)
  model_Rest_NegPdg=ROOT.RooHistPdf("model_Rest_NegPdg","model_Rest_NegPdg",ROOT.RooArgSet(x),dh_Rest_NegPdg)

  #Make combined PDF of all MC Backgrounds
#  model_PosPdg=ROOT.RooAddPdf("model_PosPdg","model_PosPdg",ROOT.RooArgList(model_WJets_PosPdg, model_TTJets),ROOT.RooArgList(yield_WJets_PosPdg, yield_TTJets))
#  model_NegPdg=ROOT.RooAddPdf("model_NegPdg","model_NegPdg",ROOT.RooArgList(model_WJets_NegPdg, model_TTJets),ROOT.RooArgList(yield_WJets_NegPdg, yield_TTJets))
  model_PosPdg=ROOT.RooAddPdf("model_PosPdg","model_PosPdg",ROOT.RooArgList(model_WJets_PosPdg, model_TTJets, model_Rest_PosPdg),ROOT.RooArgList(yield_WJets_PosPdg, yield_TTJets, yield_Rest_PosPdg))
  model_NegPdg=ROOT.RooAddPdf("model_NegPdg","model_NegPdg",ROOT.RooArgList(model_WJets_NegPdg, model_TTJets, model_Rest_NegPdg),ROOT.RooArgList(yield_WJets_NegPdg, yield_TTJets, yield_Rest_NegPdg))
  #CombinesmyMCsintoonePDFmodel

  #Plot the imported histogram(s)
  dframe=x.frame(rf.Title("Data"))
  data_PosPdg.plotOn(dframe)
  data_NegPdg.plotOn(dframe)

  frame_WJets_PosPdg=x.frame(rf.Title("WJets PosPdg"))
  model_WJets_PosPdg.plotOn(frame_WJets_PosPdg)
  frame_WJets_NegPdg=x.frame(rf.Title("WJets NegPdg"))
  model_WJets_NegPdg.plotOn(frame_WJets_NegPdg)

  frame_TTJets=x.frame(rf.Title("TTJets"))
  model_TTJets.plotOn(frame_TTJets)

  frame_Rest_PosPdg=x.frame(rf.Title("Rest PosPdg"))
  model_Rest_PosPdg.plotOn(frame_Rest_PosPdg)
  frame_Rest_NegPdg=x.frame(rf.Title("Rest NegPdg"))
  model_Rest_NegPdg.plotOn(frame_Rest_NegPdg)

  

#  c=ROOT.TCanvas("roofit_example","RooFitFractionFitExample",800,1200)
#  c.Divide(1,3)
#  ROOT.gROOT.SetStyle("Plain")#Removes gray background from plots
#  c.cd(1)
#  ROOT.gPad.SetLeftMargin(0.15)
#  dframe.GetYaxis().SetTitleOffset(1.4)
#  dframe.Draw()
#  c.cd(2)
#  ROOT.gPad.SetLeftMargin(0.15)
#  frame_WJets_PosPdg.GetYaxis().SetTitleOffset(1.4)
#  frame_WJets_PosPdg.Draw()
#  frame_WJets_NegPdg.Draw('same')
#  c.cd(3)
#  ROOT.gPad.SetLeftMargin(0.15)
#  frame_TTJets.GetYaxis().SetTitleOffset(1.4)
#  frame_TTJets.Draw()


  #nll=model.createNLL(data,rf.NumCPU(1)) #From other example, looks like
  ##pll_phi=nll.createProfile(ROOT.RooArgSet(mc1_yield))#another way of doing the fitTo
  #
  #ROOT.RooMinuit(nll).migrad()
  #ROOT.RooMinuit(nll).hesse()
  #ROOT.RooMinuit(nll).minos()#optional
  
  print "starting to perform fit !!!!"

  #model.fitTo(data)#It is this fitTo command that gives the statistical output
  nllComponents = ROOT.RooArgList("nllComponents")
  nll_PosPdg=model_PosPdg.createNLL(data_PosPdg,rf.NumCPU(1))
  nll_NegPdg=model_NegPdg.createNLL(data_NegPdg,rf.NumCPU(1))
  nllComponents.add(nll_PosPdg)
  nllComponents.add(nll_NegPdg)

  #pll_phi=nll.createProfile(r.RooArgSet(mc1_yield))#anotherwayofdoingthefitTo
  sumNLL = ROOT.RooAddition("sumNLL","sumNLL", nllComponents)

  ROOT.RooMinuit(sumNLL).migrad()
  ROOT.RooMinuit(sumNLL).hesse()
  ROOT.RooMinuit(sumNLL).minos()#optional

  #myPdf->paramOn(frame,Layout(xmin,ymin,ymax))
  fitFrame_PosPdg=x.frame(rf.Bins(50),rf.Title("FitModel"))
  model_PosPdg.paramOn(fitFrame_PosPdg,rf.Layout(0.42,0.9,0.9))
  data_PosPdg.plotOn(fitFrame_PosPdg,rf.LineColor(ROOT.kRed))
  model_PosPdg.plotOn(fitFrame_PosPdg,rf.LineStyle(ROOT.kDashed))
  model_PosPdg.plotOn(fitFrame_PosPdg,rf.Components("model_WJets_PosPdg"),rf.LineColor(ROOT.kGreen))
  model_PosPdg.plotOn(fitFrame_PosPdg,rf.Components("model_TTJets"),rf.LineColor(ROOT.kBlue))
  model_PosPdg.plotOn(fitFrame_PosPdg,rf.Components("model_Rest_PosPdg"),rf.LineColor(ROOT.kOrange+7))

  fitFrame_NegPdg=x.frame(rf.Bins(50),rf.Title("FitModel"))
  model_NegPdg.paramOn(fitFrame_NegPdg,rf.Layout(0.42,0.9,0.9))
  data_NegPdg.plotOn(fitFrame_NegPdg,rf.LineColor(ROOT.kRed))
  model_NegPdg.plotOn(fitFrame_NegPdg,rf.LineStyle(ROOT.kDashed))
  model_NegPdg.plotOn(fitFrame_NegPdg,rf.Components("model_WJets_NegPdg"),rf.LineColor(ROOT.kGreen))
  model_NegPdg.plotOn(fitFrame_NegPdg,rf.Components("model_TTJets"),rf.LineColor(ROOT.kBlue))
  model_NegPdg.plotOn(fitFrame_NegPdg,rf.Components("model_Rest_NegPdg"),rf.LineColor(ROOT.kOrange+7))

  print "After Fitting:"
  for data_hists in [data_NegPdg , data_PosPdg]:
    print "data_hists:" , data_hists
    for i in range(data_hists.numEntries()):
      data_hists.get(i)
      print  "weight :" , data_hists.weight() 

  print "AFTER FIT YIELDS:"
  print "yield_WJets_NegPdg:" , yield_WJets_NegPdg.getVal()
  print "yield_WJets_PosPdg:" , yield_WJets_PosPdg.getVal()
  print "yield_TTJets:" , yield_TTJets.getVal()
  print "yield_Rest_PosPdg:" , yield_Rest_PosPdg.getVal()
  print "yield_Rest_NegPdg:" , yield_Rest_NegPdg.getVal()


  c1=ROOT.TCanvas("c1","FitModel",800,1200)
  ROOT.gROOT.SetStyle("Plain")
  c1.Divide(1,2)
  c1.cd(1)
  ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
  ROOT.gPad.SetLeftMargin(0.15)
  fitFrame_PosPdg.GetYaxis().SetTitleOffset(1.4)
  fitFrame_PosPdg.GetXaxis().SetTitle(nBTagVar)
  fitFrame_PosPdg.Draw()

  c1.cd(2)
  ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
  ROOT.gPad.SetLeftMargin(0.15)
  fitFrame_NegPdg.GetYaxis().SetTitleOffset(1.4)
  fitFrame_NegPdg.GetXaxis().SetTitle(nBTagVar)
  fitFrame_NegPdg.Draw()

  c1.Print(printDir+'/'+prefix+'_nBTagFitRes.png')
  c1.Print(printDir+'/'+prefix+'_nBTagFitRes.pdf')
  c1.Print(printDir+'/'+prefix+'_nBTagFitRes.root')

  
  del c1
  del nllComponents

  res = {'TT_AllPdg':{'template':template_TTJets, 'yield':2*yield_TTJets.getVal(), 'yield_high':2*(yield_TTJets.getVal()+yield_TTJets.getErrorHi()), 'yield_low':2*(yield_TTJets.getVal()+yield_TTJets.getErrorLo()), 
                      'yieldVar':(yield_TTJets.getErrorHi()-yield_TTJets.getErrorLo())**2, 'file':tempFile_TTJets},
         'W_PosPdg':{'template':template_WJets_PosPdg,'yield':yield_WJets_PosPdg.getVal(), 'yield_high':yield_WJets_PosPdg.getVal()+yield_WJets_PosPdg.getErrorHi(), 'yield_low':yield_WJets_PosPdg.getVal()+yield_WJets_PosPdg.getErrorLo(),
                     'yieldVar':(0.5*(yield_WJets_PosPdg.getErrorHi()-yield_WJets_PosPdg.getErrorLo()))**2, 'file':tempFile_WJets_PosPdg},
         'W_NegPdg':{'template':template_WJets_NegPdg,'yield':yield_WJets_NegPdg.getVal(), 'yield_high':yield_WJets_NegPdg.getVal()+yield_WJets_NegPdg.getErrorHi(), 'yield_low':yield_WJets_NegPdg.getVal()+yield_WJets_NegPdg.getErrorLo(),
                     'yieldVar':(0.5*(yield_WJets_NegPdg.getErrorHi()-yield_WJets_NegPdg.getErrorLo()))**2, 'file':tempFile_WJets_NegPdg},
         'Rest_PosPdg':{'template':template_Rest_PosPdg, 'yield':yield_Rest_PosPdg.getVal(), 'yield_high':yield_Rest_PosPdg.getVal()+yield_Rest_PosPdg.getErrorHi(), 'yield_low':yield_Rest_PosPdg.getVal()+yield_Rest_PosPdg.getErrorLo(),
                     'yieldVar':(0.5*(yield_Rest_PosPdg.getErrorHi()-yield_Rest_PosPdg.getErrorLo()))**2, 'file':tempFile_Rest_PosPdg},
         'Rest_NegPdg':{'template':template_Rest_NegPdg, 'yield':yield_Rest_NegPdg.getVal(), 'yield_high':yield_Rest_NegPdg.getVal()+yield_Rest_NegPdg.getErrorHi(), 'yield_low':yield_Rest_NegPdg.getVal()+yield_Rest_NegPdg.getErrorLo(),
                     'yieldVar':(0.5*(yield_Rest_NegPdg.getErrorHi()-yield_Rest_NegPdg.getErrorLo()))**2, 'file':tempFile_Rest_NegPdg},
        }
  del model_NegPdg, model_PosPdg, data_PosPdg,  data_NegPdg,sumNLL
  return res
  


#cWJets  = getChain(WJetsHTToLNu)
#cTTJets = getChain(ttJetsCSA1450ns)
#streg = [[(250, 350), 1.], [(350, -1), 1.]]
#htreg = [(400,500),(500,750),(750, -1)]
##njreg = [(2,2),(3,3),(4,4),(5,-1),(6,-1)]
#
#stb = streg[0][0]
#htb = htreg[1]
#njb = (2,3)
#
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0"
#cname, cut = nameAndCut(stb,htb,njb, btb=None, presel=presel)
#
#res = binnedNBTagsFit(cut, samples = {'W':cWJets, 'TT':cTTJets}, nBTagVar = 'nBJetMedium25', prefix=cname)
