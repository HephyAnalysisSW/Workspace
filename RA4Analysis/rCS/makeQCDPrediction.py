import ROOT
from ROOT import RooFit as rf
import pickle 
import copy, os, sys
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.TH1F().SetDefaultSumw2()
ROOT.setTDRStyle()
ROOT.gStyle.SetMarkerStyle(1)
ROOT.gStyle.SetOptTitle(0)

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.HEPHYPythonTools.xsec import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed_antiSel import *
#from Workspace.RA4Analysis.cmgTuples_Data_25ns_postProcessed_antiSel import *

from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_antiSel_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Data25ns_Promtv2_antiSel_postprocessed import *

#from draw_helpers import *
from math import *
from Workspace.HEPHYPythonTools.user import username
from LpTemplateFit import LpTemplateFit

isData = False
makeFit = False
getYields = False
getResults = True
isValidation = False

readFit     = '/data/dspitzbart/Results2016/QCDEstimation/20160628_fitResult_2016SR_preapp_MC10fb_pkl'
readYields  = '/data/dspitzbart/Results2016/QCDEstimation/20160628_QCDestimation_2016SR_preapp_MC10fb_pkl'



if isData:
  sampleStr = 'data'
else:
  sampleStr = 'MC'

SRstring = '2016SR_preapp_100p'
if isValidation: SRstring = 'validation'

preprefix = 'QCDestimation/'+SRstring+'_10fb/'+sampleStr
wwwDir = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Results2016B/'+preprefix+'/'
picklePath = '/data/'+username+'/Results2016/QCDEstimation/'
prefix = 'Lp_singleElectronic_'
picklePresel = '20160628_QCDestimation_'+SRstring+'_'+sampleStr+'10fb_pkl'
pickleFit    = '20160628_fitResult_'+SRstring+'_'+sampleStr+'10fb_pkl'

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

mcFileIsHere = False
if isData:
  mcFileIsHere = True
  mcFile = picklePath+'20160628_QCDestimation_2016SR_preapp_MC10fb_pkl'
  try: file(mcFile)
  except IOError: mcFileIsHere = False
  if mcFileIsHere:
    mc_bins = pickle.load(file(mcFile))
    print 'MC file successfully loaded, can assign correct uncertainties'
    mcFileIsHere = True
  else:
    print
    print '! Correct Uncertainty can not get assigned at the end, MC file missing !'
    print

##############################################
###   Define sidebands for QCD estimation  ###
### (3,4) in std est., (3,3) in validation ###
if isValidation: QCD_SB = (3,3)
else: QCD_SB = (3,4)


inclusiveTemplate = {QCD_SB: {(250,  -1): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}}}} #use inclusive LT,HT region to get the shape for the fit template

fitCR =  {QCD_SB: {(250,  -1): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}},
                   (250, 350): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}}, #QCD CR exclusive in LT and inclusive in HT, where the fits are performed
                   (350,  -1): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}}, 
                   (350, 450): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}},
                   (450, -1):  {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}}}}

if isValidation: SRs = validationRegionAll
else:
  #SRs = signalRegion3fb
  SRs = signalRegions2016

signalRegion = makeQCDsignalRegions(SRs, QCDSB=QCD_SB)

btreg = [(0,0), (1,1), (2,-1)] #1b and 2b estimates are needed for the btag fit

def makeWeight(lumi=3., sampleLumi=3.,debug=False):
  #reWeight = 'lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*TopPtWeight*0.94*puReweight_true_max4'
  #reWeight = 'lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*0.94*TopPtWeight'
  reWeight = '(1)'
  if debug:
    print 'No lumi-reweighting done!!'
    return 'weight', 'weight*weight'
  else:
    weight_str = '((weight/'+str(sampleLumi)+')*'+str(lumi)+'*'+reWeight+')'
    weight_err_str = '('+weight_str+'*'+weight_str+')'
  return weight_str, weight_err_str

lumi = 3.99
sampleLumi = 3.0 #post processed sample already produced with 2.25fb-1
weight_str, weight_err_str = makeWeight(lumi, sampleLumi)

def getRCS(c, cut, dPhiCut, useWeight = False, weight = 'weight'):
#  dPhiStr = 'acos((LepGood_pt+met_pt*cos(LepGood_phi-met_phi))/sqrt(LepGood_pt**2+met_pt**2+2*met_pt*LepGood_pt*cos(LepGood_phi-met_phi)))'
  dPhiStr = 'deltaPhi_Wl'
  if useWeight:
    h = getPlotFromChain(c, dPhiStr, [0,dPhiCut,pi], cutString=cut, binningIsExplicit=True, weight =  weight)
  else:
    h = getPlotFromChain(c, dPhiStr, [0,dPhiCut,pi], cutString=cut, binningIsExplicit=True, weight='(1)')
  h.Sumw2()
  if h.GetBinContent(1)>0:
    rcs = h.GetBinContent(2)/h.GetBinContent(1)
    if h.GetBinContent(2)>0:
      rCSE_sim = rcs*sqrt(h.GetBinError(2)**2/h.GetBinContent(2)**2 + h.GetBinError(1)**2/h.GetBinContent(1)**2)
      rCSE_pred = rcs*sqrt(1./h.GetBinContent(2) + 1./h.GetBinContent(1))
      del h
      return {'rCS':rcs, 'rCSE_pred':rCSE_pred, 'rCSE_sim':rCSE_sim}
    else:
      del h
      return {'rCS':rcs, 'rCSE_pred':float('nan'), 'rCSE_sim':float('nan')}
  else:
    del h
    return {'rCS':float('nan'), 'rCSE_pred':float('nan'), 'rCSE_sim':float('nan')}

def getPseudoRCS(small,smallE,large,largeE): 
  if small>0:
    rcs = large/small
    if large>0:
      rCSE_sim = rcs*sqrt(smallE**2/small**2 + largeE**2/large**2)
      rCSE_pred = rcs*sqrt(1./small + 1./large)
      return {'rCS':rcs, 'rCSE_pred':rCSE_pred, 'rCSE_sim':rCSE_sim}
    else:
      return {'rCS':rcs, 'rCSE_pred':float('nan'), 'rCSE_sim':float('nan')}
  else:
    return {'rCS':float('nan'), 'rCSE_pred':float('nan'), 'rCSE_sim':float('nan')}

#trigger and filters for real Data
trigger = "&&((HLT_EleHT350||HLT_EleHT400)||(HLT_MuHT350||HLT_MuHT400))"
#filters = "&&Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter "#&& veto_evt_list"
filters = "&& (Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_goodVertices && Flag_eeBadScFilter &&  Flag_globalTightHalo2016Filter && Flag_badChargedHadronFilter && Flag_badMuonFilter)"
#filters = "&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter_fix&&Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter"
#filters = "&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter_fix&&Flag_HBHENoiseIsoFilter&&Flag_goodVertices&&Flag_eeBadScFilter"

presel = 'nLep==1&&nVeto==0&&leptonPt>25&&nEl==1&&Jet2_pt>80'
antiSelStr = presel+'&&Selected==(-1)'
SelStr = presel+'&&Selected==1'

#cQCD  = getChain(QCDHT_25ns,histname='')
#cEWK  = getChain([WJetsHTToLNu_25ns, TTJets_combined_2, singleTop_25ns, DY_25ns, TTV_25ns],histname='')

cQCD  = getChain(QCDHT_antiSel,histname='')
cEWK  = getChain([WJetsHTToLNu_antiSel, TTJets_Lep_antiSel, singleTop_lep_antiSel, DY_HT_antiSel, TTV_antiSel],histname='')

if isData:
  cData = getChain(single_ele_Run2016B_antiSel, histname='')
else:
  cData = getChain([QCDHT_antiSel, WJetsHTToLNu_antiSel, TTJets_Lep_antiSel, singleTop_lep_antiSel, DY_HT_antiSel, TTV_antiSel] , histname='')

#get template for fit method
numberOfBins = 30
template_QCD = ROOT.TH1F('template_QCD','template_QCD',numberOfBins,-0.5,2.5)
#print '!!!!!!!!!!!!!!! using sel QCD as template now'
templateName, templateCut = nameAndCut((250,-1), (500,-1), (3,4), (0,0), presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30', stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean') ##changed from anitsel for check!!!

if makeFit:
  if isData:
    cData.Draw('Lp>>template_QCD','('+templateCut+trigger+filters+')','goff')
  else:
    cData.Draw('Lp>>template_QCD','('+weight_str+')*('+templateCut+')','goff')

histos = {}
if makeFit:
  fitRes = {}
  #perform the fits in QCD CR
  print 'Performing fits in the QCD CRs'
  
  for crNJet in sorted(fitCR):
    fitRes[crNJet] = {}
    for ltb in sorted(fitCR[crNJet]):
      fitRes[crNJet][ltb] = {} 
      for htb in sorted(fitCR[crNJet][ltb]):
        deltaPhiCut = 1.0
        print '#########################################'
        print '## CR',str(crNJet),str(ltb),str(htb)
        print '#########################################'
        antiSelname, antiSelCut = nameAndCut(ltb, htb, crNJet, btb=(0,0), presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30', stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean')
        Selname, SelCut         = nameAndCut(ltb, htb, crNJet, btb=(0,0), presel=SelStr, charge="", btagVar = 'nBJetMediumCSV30', stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean')      
        
        histos['QCD']={}
        histos['EWK']={}
        histos['DATA']={}
        histos['QCD']['antiSelection']=ROOT.TH1F('QCD_antiSelection','QCD_antiSelection',numberOfBins,-0.5,2.5)
        histos['QCD']['Selection']=ROOT.TH1F('QCD_Selection','QCD_Selection',numberOfBins,-0.5,2.5)
        histos['EWK']['antiSelection']=ROOT.TH1F('EWK_antiSelection','EWK_antiSelection',numberOfBins,-0.5,2.5)
        histos['EWK']['Selection']=ROOT.TH1F('EWK_Selection','EWK_Selection',numberOfBins,-0.5,2.5)
        histos['DATA']['antiSelection']=ROOT.TH1F('DATA_antiSelection','DATA_antiSelection',numberOfBins,-0.5,2.5)
        histos['DATA']['Selection']=ROOT.TH1F('DATA_Selection','DATA_Selection',numberOfBins,-0.5,2.5)
  
        Canv = ROOT.TCanvas('Canv','Canv')
        #mergeCanv.SetLogy()
        leg = ROOT.TLegend(0.7,0.75,0.98,0.95)
        leg.SetFillColor(0)
        leg.SetBorderSize(1)
        leg.SetShadowColor(ROOT.kWhite)
        text = ROOT.TLatex()
        text.SetNDC()
        text.SetTextSize(0.045)
        text.SetTextAlign(11)
  
        cQCD.Draw('Lp>>QCD_antiSelection','('+weight_str+')*('+antiSelCut+')')
        cQCD.Draw('Lp>>QCD_Selection','('+weight_str+')*('+SelCut+')')
        cEWK.Draw('Lp>>EWK_antiSelection','('+weight_str+')*('+antiSelCut+')')
        cEWK.Draw('Lp>>EWK_Selection','('+weight_str+')*('+SelCut+')')
        if isData:
          cData.Draw('Lp>>DATA_antiSelection','('+antiSelCut+trigger+filters+')')
          cData.Draw('Lp>>DATA_Selection','('+SelCut+trigger+filters+')')
        else:
          cData.Draw('Lp>>DATA_antiSelection','('+weight_str+')*('+antiSelCut+')')
          cData.Draw('Lp>>DATA_Selection','('+weight_str+')*('+SelCut+')')
  ##      cData.Draw('Lp>>DATA_antiSelection','('+antiSelCut+trigger+filters+')')
  #      cData.Draw('Lp>>DATA_antiSelection','('+weight_str+')*('+antiSelCut+')')
  ##      cData.Draw('Lp>>DATA_Selection','('+SelCut+trigger+filters+')')
  #      cData.Draw('Lp>>DATA_Selection','('+weight_str+')*('+SelCut+')')
  
        if isData:
          rCSanti = getRCS(cData, antiSelCut+trigger+filters, deltaPhiCut, useWeight = False, weight = weight_str)
          rCSsel = getRCS(cData, SelCut+trigger+filters, deltaPhiCut, useWeight = False, weight = weight_str)
        else:
          rCSanti = getRCS(cData, antiSelCut, deltaPhiCut, useWeight = True, weight = weight_str)
          rCSsel = getRCS(cData, SelCut, deltaPhiCut, useWeight = True, weight = weight_str)
  ##      rCSanti = getRCS(cData, antiSelCut+trigger+filters, deltaPhiCut, useWeight = False, weight = weight_str)
  ##      rCSsel = getRCS(cData, SelCut+trigger+filters, deltaPhiCut, useWeight = False, weight = weight_str)
  #      rCSanti = getRCS(cData, antiSelCut, deltaPhiCut, useWeight = True, weight = weight_str)
  #      rCSsel = getRCS(cData, SelCut, deltaPhiCut, useWeight = True, weight = weight_str)
  
        for hist in [histos['DATA']['antiSelection'],histos['DATA']['Selection']]:
          hist.SetStats(0)
          hist.GetYaxis().SetTitle('# of Events')
          hist.GetXaxis().SetTitle('L_{p}')
          hist.SetLineColor(ROOT.kBlack)
          hist.SetLineStyle(1)
          hist.SetLineWidth(1)
  
        for hist in [histos['QCD']['antiSelection'],histos['QCD']['Selection'],histos['EWK']['antiSelection'],histos['EWK']['Selection']]:
          hist.SetStats(0)
          hist.GetYaxis().SetTitle('# of Events')
          hist.GetXaxis().SetTitle('L_{p}')
          hist.SetLineWidth(2)
          hist.SetMarkerStyle(1)
  
        nEWKSel_err = ROOT.Double()
        nEWKSel = histos['EWK']['Selection'].IntegralAndError(0,histos['EWK']['Selection'].GetNbinsX(),nEWKSel_err)
        nEWKAntiSel_err = ROOT.Double()
        nEWKAntiSel = histos['EWK']['antiSelection'].IntegralAndError(0,histos['EWK']['antiSelection'].GetNbinsX(),nEWKAntiSel_err)
        nQCDSel_err = ROOT.Double()
        nQCDSel =  histos['QCD']['Selection'].IntegralAndError(0,histos['QCD']['Selection'].GetNbinsX(),nQCDSel_err)
        nQCDAntiSel_err = ROOT.Double()
        nQCDAntiSel = histos['QCD']['antiSelection'].IntegralAndError(0,histos['QCD']['antiSelection'].GetNbinsX(),nQCDAntiSel_err)
        nDATASel_err = ROOT.Double()
        nDATASel = histos['DATA']['Selection'].IntegralAndError(0,histos['DATA']['Selection'].GetNbinsX(),nDATASel_err)
        nDATAAntiSel_err = ROOT.Double()
        nDATAAntiSel = histos['DATA']['antiSelection'].IntegralAndError(0,histos['DATA']['antiSelection'].GetNbinsX(),nDATAAntiSel_err)
  
        fitRes[crNJet][ltb][htb] = {'NDATASel':nDATASel, 'NDATASel_err':float(nDATASel_err),\
                                    'NDATAAntiSel':nDATAAntiSel, 'NDATAAntiSel_err':float(nDATAAntiSel_err),\
                                    'NEWKSelMC':nEWKSel, 'NEWKSelMC_err':float(nEWKSel_err),\
                                    'NEWKAntiSelMC':nEWKAntiSel, 'NEWKAntiSelMC_err':float(nEWKAntiSel_err),\
                                    'NQCDSelMC':nQCDSel, 'NQCDSelMC_err':float(nQCDSel_err),\
                                    'NQCDAntiSelMC':nQCDAntiSel, 'NQCDAntiSelMC_err':float(nQCDAntiSel_err),\
                                    'deltaPhiCut':deltaPhiCut, 'rCSselectedDATA':rCSsel, 'rCSantiSelectedDATA':rCSanti}
  
        Canv.cd()
        histos['QCD']['antiSelection'].SetLineColor(ROOT.kRed)
        histos['QCD']['antiSelection'].SetLineStyle(ROOT.kDashed)
        leg.AddEntry(histos['QCD']['antiSelection'],'QCD anti-selected','l')
  
        histos['QCD']['Selection'].SetLineColor(ROOT.kRed)
        leg.AddEntry(histos['QCD']['Selection'],'QCD selected','l')
  
        histos['EWK']['antiSelection'].SetLineColor(ROOT.kBlack)
        histos['EWK']['antiSelection'].SetLineStyle(ROOT.kDashed)
        leg.AddEntry(histos['EWK']['antiSelection'],'EWK anti-selected','l')
  
        histos['EWK']['Selection'].SetLineColor(ROOT.kBlack)
        leg.AddEntry(histos['EWK']['Selection'],'EWK selected','l')
  
        histos['DATA']['antiSelection'].SetMarkerStyle(24)
        histos['DATA']['Selection'].SetMarkerStyle(20)
        leg.AddEntry(histos['DATA']['antiSelection'],'Data anti-selected')
        leg.AddEntry(histos['DATA']['Selection'],'Data selected')
  
        histos['QCD']['antiSelection'].Draw('hist e')
        histos['QCD']['Selection'].Draw('hist same e')
        histos['EWK']['antiSelection'].Draw('hist same e')
        histos['EWK']['Selection'].Draw('hist same e')
        histos['DATA']['antiSelection'].Draw('same ep')
        histos['DATA']['Selection'].Draw('same ep')
  
        histos['QCD']['antiSelection'].SetMaximum(1.5*histos['QCD']['antiSelection'].GetMaximum())
        histos['QCD']['Selection'].SetMaximum(1.5*histos['QCD']['Selection'].GetMaximum())
        histos['EWK']['antiSelection'].SetMaximum(1.5*histos['EWK']['antiSelection'].GetMaximum())
        histos['EWK']['Selection'].SetMaximum(1.5*histos['EWK']['Selection'].GetMaximum())
        histos['DATA']['antiSelection'].SetMaximum(1.5*histos['DATA']['antiSelection'].GetMaximum())
        histos['DATA']['Selection'].SetMaximum(1.5*histos['DATA']['Selection'].GetMaximum())
  
        leg.Draw()
        if isData:
          text.DrawLatex(0.16,.96,"CMS #bf{#it{Preliminary}}")
        else:
          text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
  ##      text.DrawLatex(0.16,.96,"CMS #bf{#it{Preliminary}}")
  #      text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
        text.DrawLatex(0.62,0.96,"#bf{L="+str(lumi)+" fb^{-1} (13 TeV)}")
  
        Canv.cd()
        Canv.Print(wwwDir+prefix+Selname+'.png')
        Canv.Print(wwwDir+prefix+Selname+'.root')
        Canv.Print(wwwDir+prefix+Selname+'.pdf')
        Canv.Clear()
  
        LpTemplates = {'DATAantiSel':template_QCD, 'DATAsel':histos['DATA']['Selection'],\
                       'EWKantiSel':histos['EWK']['antiSelection'], 'EWKsel':histos['EWK']['Selection'],\
                       'QCDantiSel':histos['QCD']['antiSelection'], 'QCDsel':histos['QCD']['Selection']}
        fit_QCD = LpTemplateFit(LpTemplates, prefix=prefix+Selname, printDir=wwwDir+'templateFit')
        fitRes[crNJet][ltb][htb].update(fit_QCD)
        try: F_ratio = fit_QCD['QCD']['yield']/nDATAAntiSel
        except ZeroDivisionError: F_ratio = float('nan')
        try: F_ratio_err = F_ratio*sqrt(fit_QCD['QCD']['yieldVar']/fit_QCD['QCD']['yield']**2 + nDATAAntiSel_err**2/nDATAAntiSel**2)
        except ZeroDivisionError: F_ratio_err = float('nan')
        fitRes[crNJet][ltb][htb].update({'F_seltoantisel':F_ratio, 'F_seltoantisel_err':F_ratio_err})
  
        ROOT.setTDRStyle()
        if not os.path.exists(picklePath):
          os.makedirs(picklePath)
        pickle.dump(fitRes, file(picklePath+pickleFit,'w'))
else:
  fitRes = pickle.load(file(readFit))


if getYields:
  bins = {}
  for srNJet in sorted(signalRegion):
    bins[srNJet] = {}
    for stb in sorted(signalRegion[srNJet]):
      bins[srNJet][stb] = {}
      for htb in sorted(signalRegion[srNJet][stb]):
        bins[srNJet][stb][htb] = {}
        for btb in btreg:
          bins[srNJet][stb][htb][btb] = {}
          for dP in sorted(signalRegion[srNJet][stb][htb]):
            deltaPhiCut = signalRegion[srNJet][stb][htb][dP]['deltaPhi']
  
            print 'Binning => Ht: ',htb,'Lt: ',stb,'NJet: ',srNJet
            antiSelname, antiSelCut = nameAndCut(stb, htb, srNJet, btb=btb, presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30', stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean')
            Selname, SelCut         = nameAndCut(stb, htb, srNJet, btb=btb, presel=SelStr, charge="", btagVar = 'nBJetMediumCSV30', stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean')
  
            histos['QCD']={}
            histos['EWK']={}
            histos['DATA']={}
            histos['QCD']['antiSelection']=ROOT.TH1F('QCD_antiSelection','QCD_antiSelection',numberOfBins,-0.5,2.5)
            histos['QCD']['Selection']=ROOT.TH1F('QCD_Selection','QCD_Selection',numberOfBins,-0.5,2.5)
            histos['EWK']['antiSelection']=ROOT.TH1F('EWK_antiSelection','EWK_antiSelection',numberOfBins,-0.5,2.5)
            histos['EWK']['Selection']=ROOT.TH1F('EWK_Selection','EWK_Selection',numberOfBins,-0.5,2.5)
            histos['DATA']['antiSelection']=ROOT.TH1F('DATA_antiSelection','DATA_antiSelection',numberOfBins,-0.5,2.5)
            histos['DATA']['Selection']=ROOT.TH1F('DATA_Selection','DATA_Selection',numberOfBins,-0.5,2.5)
  
            Canv = ROOT.TCanvas('Canv','Canv')
            #mergeCanv.SetLogy()
            leg = ROOT.TLegend(0.7,0.75,0.98,0.95)
            leg.SetFillColor(0)
            leg.SetBorderSize(1)
            leg.SetShadowColor(ROOT.kWhite)
            text = ROOT.TLatex()
            text.SetNDC()
            text.SetTextSize(0.045)
            text.SetTextAlign(11)
          
            cQCD.Draw('Lp>>QCD_antiSelection','('+weight_str+')*('+antiSelCut+')')
            cQCD.Draw('Lp>>QCD_Selection','('+weight_str+')*('+SelCut+')')
            cEWK.Draw('Lp>>EWK_antiSelection','('+weight_str+')*('+antiSelCut+')')
            cEWK.Draw('Lp>>EWK_Selection','('+weight_str+')*('+SelCut+')')
            if isData:
              cData.Draw('Lp>>DATA_antiSelection','('+antiSelCut+trigger+filters+')')
              cData.Draw('Lp>>DATA_Selection','('+SelCut+trigger+filters+')')
            else:
              cData.Draw('Lp>>DATA_antiSelection','('+weight_str+')*('+antiSelCut+')')
              cData.Draw('Lp>>DATA_Selection','('+weight_str+')*('+SelCut+')')
  ##          cData.Draw('Lp>>DATA_antiSelection','('+antiSelCut+trigger+filters+')')
  #          cData.Draw('Lp>>DATA_antiSelection','('+weight_str+')*('+antiSelCut+')')
  ##          cData.Draw('Lp>>DATA_Selection','('+SelCut+trigger+filters+')')
  #          cData.Draw('Lp>>DATA_Selection','('+weight_str+')*('+SelCut+')')
  
            if isData:
              rCSanti = getRCS(cData, antiSelCut+trigger+filters, deltaPhiCut, useWeight = False, weight = weight_str)
              rCSsel = getRCS(cData, SelCut+trigger+filters, deltaPhiCut, useWeight = False, weight = weight_str)
            else:
              rCSanti = getRCS(cData, antiSelCut, deltaPhiCut, useWeight = True, weight = weight_str)
              rCSsel = getRCS(cData, SelCut, deltaPhiCut, useWeight = True, weight = weight_str)
  ##          rCSanti = getRCS(cData, antiSelCut+trigger+filters, deltaPhiCut, useWeight = False, weight = weight_str)
  ##          rCSsel = getRCS(cData, SelCut+trigger+filters, deltaPhiCut, useWeight = False, weight = weight_str)
  #          rCSanti = getRCS(cData, antiSelCut, deltaPhiCut, useWeight = True, weight = weight_str)
  #          rCSsel = getRCS(cData, SelCut, deltaPhiCut, useWeight = True, weight = weight_str)
  
            for hist in [histos['DATA']['antiSelection'],histos['DATA']['Selection']]:
              hist.SetStats(0)
              hist.GetYaxis().SetTitle('# of Events')
              hist.GetXaxis().SetTitle('L_{p}')
              hist.SetLineColor(ROOT.kBlack)
              hist.SetLineStyle(1)
              hist.SetLineWidth(1)
    
            for hist in [histos['QCD']['antiSelection'],histos['QCD']['Selection'],histos['EWK']['antiSelection'],histos['EWK']['Selection']]:
              hist.SetStats(0)
              hist.GetYaxis().SetTitle('# of Events')
              hist.GetXaxis().SetTitle('L_{p}')
              hist.SetLineWidth(2)
              hist.SetMarkerStyle(1)
  
            nEWKSel_err = ROOT.Double()
            nEWKSel = histos['EWK']['Selection'].IntegralAndError(0,histos['EWK']['Selection'].GetNbinsX(),nEWKSel_err)
            nEWKAntiSel_err = ROOT.Double()
            nEWKAntiSel = histos['EWK']['antiSelection'].IntegralAndError(0,histos['EWK']['antiSelection'].GetNbinsX(),nEWKAntiSel_err)
            nQCDSel_err = ROOT.Double()
            nQCDSel =  histos['QCD']['Selection'].IntegralAndError(0,histos['QCD']['Selection'].GetNbinsX(),nQCDSel_err) 
            nQCDAntiSel_err = ROOT.Double()
            nQCDAntiSel = histos['QCD']['antiSelection'].IntegralAndError(0,histos['QCD']['antiSelection'].GetNbinsX(),nQCDAntiSel_err)
            nDATASel_err = ROOT.Double()
            nDATASel = histos['DATA']['Selection'].IntegralAndError(0,histos['DATA']['Selection'].GetNbinsX(),nDATASel_err)
            nDATAAntiSel_err = ROOT.Double()
            nDATAAntiSel = histos['DATA']['antiSelection'].IntegralAndError(0,histos['DATA']['antiSelection'].GetNbinsX(),nDATAAntiSel_err)
  
            bins[srNJet][stb][htb][btb][dP] = {'NDATASel':nDATASel, 'NDATASel_err':float(nDATASel_err),\
                                               'NDATAAntiSel':nDATAAntiSel, 'NDATAAntiSel_err':float(nDATAAntiSel_err),\
                                               'NEWKSelMC':nEWKSel, 'NEWKSelMC_err':float(nEWKSel_err),\
                                               'NEWKAntiSelMC':nEWKAntiSel, 'NEWKAntiSelMC_err':float(nEWKAntiSel_err),\
                                               'NQCDSelMC':nQCDSel, 'NQCDSelMC_err':float(nQCDSel_err),\
                                               'NQCDAntiSelMC':nQCDAntiSel, 'NQCDAntiSelMC_err':float(nQCDAntiSel_err),\
                                               'deltaPhiCut':deltaPhiCut, 'rCSselectedDATA':rCSsel, 'rCSantiSelectedDATA':rCSanti}
    
            Canv.cd()
            histos['QCD']['antiSelection'].SetLineColor(ROOT.kRed)
            histos['QCD']['antiSelection'].SetLineStyle(ROOT.kDashed)
            leg.AddEntry(histos['QCD']['antiSelection'],'QCD anti-selected','l')
     
            histos['QCD']['Selection'].SetLineColor(ROOT.kRed)
            leg.AddEntry(histos['QCD']['Selection'],'QCD selected','l')
     
            histos['EWK']['antiSelection'].SetLineColor(ROOT.kBlack)
            histos['EWK']['antiSelection'].SetLineStyle(ROOT.kDashed)
            leg.AddEntry(histos['EWK']['antiSelection'],'EWK anti-selected','l')
     
            histos['EWK']['Selection'].SetLineColor(ROOT.kBlack)
            leg.AddEntry(histos['EWK']['Selection'],'EWK selected','l')
    
            histos['DATA']['antiSelection'].SetMarkerStyle(24)
            histos['DATA']['Selection'].SetMarkerStyle(20)
            leg.AddEntry(histos['DATA']['antiSelection'],'Data anti-selected')
            leg.AddEntry(histos['DATA']['Selection'],'Data selected') 
          
            histos['QCD']['antiSelection'].Draw('hist e')
            histos['QCD']['Selection'].Draw('hist same e')
            histos['EWK']['antiSelection'].Draw('hist same e')
            histos['EWK']['Selection'].Draw('hist same e')
            histos['DATA']['antiSelection'].Draw('same ep')
            histos['DATA']['Selection'].Draw('same ep')
    
            histos['QCD']['antiSelection'].SetMaximum(1.5*histos['QCD']['antiSelection'].GetMaximum())
            histos['QCD']['Selection'].SetMaximum(1.5*histos['QCD']['Selection'].GetMaximum())
            histos['EWK']['antiSelection'].SetMaximum(1.5*histos['EWK']['antiSelection'].GetMaximum())
            histos['EWK']['Selection'].SetMaximum(1.5*histos['EWK']['Selection'].GetMaximum())
            histos['DATA']['antiSelection'].SetMaximum(1.5*histos['DATA']['antiSelection'].GetMaximum())
            histos['DATA']['Selection'].SetMaximum(1.5*histos['DATA']['Selection'].GetMaximum())
              
            leg.Draw()
            if isData:
              text.DrawLatex(0.16,.96,"CMS #bf{#it{Preliminary}}")
            else:
              text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
  ##          text.DrawLatex(0.16,.96,"CMS #bf{#it{Preliminary}}")
  #          text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
            text.DrawLatex(0.62,0.96,"#bf{L="+str(lumi)+" fb^{-1} (13 TeV)}")
    
            Canv.cd()
            Canv.Print(wwwDir+prefix+Selname+'.png')
            Canv.Print(wwwDir+prefix+Selname+'.root')
            Canv.Print(wwwDir+prefix+Selname+'.pdf')
            Canv.Clear()
    
            ROOT.setTDRStyle()
            if not os.path.exists(picklePath):
              os.makedirs(picklePath)
            pickle.dump(bins, file(picklePath+picklePresel,'w'))
else:
  bins = pickle.load(file(readYields))

#derive N_QCD(dPhi<x) and N_QCD(dPhi>x)
for srNJet in sorted(signalRegion):
  for stb in sorted(signalRegion[srNJet]):
    for htb in sorted(signalRegion[srNJet][stb]):
      for btb in btreg:
        for dP in sorted(signalRegion[srNJet][stb][htb]):
          deltaPhiCut = signalRegion[srNJet][stb][htb][dP]['deltaPhi']
          sys         = signalRegion[srNJet][stb][htb][dP]['sys']
          Fsta        = fitRes[inclusiveTemplate.keys()[0]][stb][(500,-1)]['F_seltoantisel']
          Fsta_err    = fitRes[inclusiveTemplate.keys()[0]][stb][(500,-1)]['F_seltoantisel_err']
          Nanti       = bins[srNJet][stb][htb][btb][dP]['NDATAAntiSel']
          Nanti_err   = bins[srNJet][stb][htb][btb][dP]['NDATAAntiSel_err']
          RcsAnti     = bins[srNJet][stb][htb][btb][dP]['rCSantiSelectedDATA']['rCS']
          RcsAnti_err = bins[srNJet][stb][htb][btb][dP]['rCSantiSelectedDATA']['rCSE_pred']
          NQCD        = Fsta * Nanti
          NQCD_err    = sqrt( (Fsta_err**2*Nanti**2+Nanti_err**2*Fsta**2) + (sys)**2 )
          NQCD_truth  = bins[srNJet][stb][htb][btb][dP]['NQCDSelMC']
          if isData and mcFileIsHere: #apply the relative uncertainty determined in MC to data
            NQCD_err_rel  = mc_bins[srNJet][stb][htb][btb][dP]['NQCDpred_err_rel']
            NQCD_err_rel  = 1.
            NQCD_err      = NQCD_err_rel*NQCD
          elif isData and not mcFileIsHere:
            NQCD_err_rel  = 'Uncertainty not correct!!'
            NQCD_err      = NQCD_err
          else: #In MC, get the max of the determined error of the method and the non-closure
            print NQCD_err, NQCD, NQCD_truth, NQCD
            NQCD_err_rel  = max([NQCD_err/NQCD, abs(1-NQCD_truth/NQCD)])
            NQCD_err_rel  = 1.
            print round(NQCD_err_rel,3)
            NQCD_err      = NQCD_err_rel*NQCD
          try: NQCD_lowDPhi = NQCD/(RcsAnti+1)
          except ZeroDivisionError: NQCD_lowDPhi = float('nan') 
          try: NQCD_lowDPhi_err = NQCD_lowDPhi*sqrt((NQCD_err/NQCD)**2 + (RcsAnti_err/(RcsAnti+1))**2)
          except ZeroDivisionError: NQCD_lowDPhi_err = float('nan')
          NQCD_highDPhi = NQCD - NQCD_lowDPhi
          NQCD_highDPhi_err = sqrt(RcsAnti_err**2*NQCD_lowDPhi**2 + RcsAnti**2*NQCD_lowDPhi_err**2)
          bins[srNJet][stb][htb][btb][dP].update({'NQCDpred':NQCD, 'NQCDpred_err':NQCD_err, 'NQCDpred_err_rel':NQCD_err_rel, 'NQCDpred_lowdPhi':NQCD_lowDPhi, 'NQCDpred_lowdPhi_err':NQCD_lowDPhi_err, 'NQCDpred_highdPhi':NQCD_highDPhi, 'NQCDpred_highdPhi_err':NQCD_highDPhi_err})
          pickle.dump(bins, file(picklePath+picklePresel,'w'))

