import ROOT
from ROOT import RooFit as rf

import os, sys, copy
import pickle, operator

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *

#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_Spring15_hard import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT400ST200_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Data25ns_0l import *
#from Workspace.RA4Analysis.cmgTuples_Data25ns_Artur import *

#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT400ST200_postProcessed_fromArthur import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT400ST200_postProcessed_btagWeight import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT500ST250_postProcessed_btagWeight import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT500ST250_postProcessed_fromArthur import *
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Data25ns_miniAODv2_postprocessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed_btag import *

#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT400ST200_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_50ns_postProcessed import *
from Workspace.HEPHYPythonTools.user import username

#QCDestimate = pickle.load(file('/data/dspitzbart/Results2016/QCDEstimation/20160212_QCDestimation_MC2p25fb_pkl'))
QCDestimate = pickle.load(file('/data/dspitzbart/Results2016/QCDEstimation/20160212_QCDestimation_data2p25fb_pkl'))

def setNiceBinLabel(hist, signalRegions):
  i = 1
  for njb in sorted(signalRegions):
    for stb in sorted(signalRegions[njb]):
      for htb in sorted(signalRegions[njb][stb]):
        hist.GetXaxis().SetBinLabel(i,'#splitline{'+signalRegions[njb][stb][htb]['njet']+'}{#splitline{'+signalRegions[njb][stb][htb]['LT']+'}{'+signalRegions[njb][stb][htb]['HT']+'}}')
        i += 1

def makeWeight(lumi=4., sampleLumi=3.,debug=False, reWeight='lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*TopPtWeight*0.94'):
  #reWeight = 'lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*TopPtWeight*0.94'
  #reWeight = 'lepton_muSF_mediumID*lepton_muSF_miniIso02*lepton_muSF_sip3d*lepton_eleSF_cutbasedID*lepton_eleSF_miniIso01'
  if debug:
    print 'No lumi-reweighting done!!'
    return 'weight', 'weight*weight'
  else:
    weight_str = '((weight/'+str(sampleLumi)+')*'+str(lumi)+'*'+reWeight+')'
    weight_err_str = '('+weight_str+'*'+weight_str+')'
  return weight_str, weight_err_str

#25ns samples
#WJETS = {'name':'WJets', 'chain':getChain(WJetsHTToLNu_25ns,histname=''), 'color':ROOT.kMagenta,'weight':'weight', 'niceName':'W Jets, MVA ID'}
#WJETSbtagweight = {'name':'WJets', 'chain':getChain(WJetsHTToLNu_25ns_btag,histname=''), 'color':ROOT.kMagenta,'weight':'weight', 'niceName':'W Jets btag'}
WJETS = {'name':'WJets', 'chain':getChain(WJetsHTToLNu_25ns,histname=''), 'color':color('WJets'),'weight':'weight', 'niceName':'W Jets CB ID'}
#TTJETS = {'name':'TTJets', 'chain':getChain(TTJets_25ns,histname=''), 'color':color('TTJets'),'weight':'weight', 'niceName':'t#bar{t} Jets NLO'}
#TTJetsLO = {'name':'TTJets', 'chain':getChain(TTJets_LO_25ns,histname=''), 'color':color('singleTop'),'weight':'weight', 'niceName':'t#bar{t} Jets MVA ID'}
#TTJetsbtagweight = {'name':'TTJets', 'chain':getChain(TTJets_combined_btag,histname=''), 'color':color('TTJets')-2,'weight':'weight', 'niceName':'t#bar{t} Jets btag'}
TTJets = {'name':'TTJets', 'chain':getChain(TTJets_HTLO_25ns,histname=''), 'color':ROOT.kOrange,'weight':'weight', 'niceName':'t#bar{t} Jets HT bin'}
TTJets_com = {'name':'TTJets', 'chain':getChain(TTJets_combined,histname=''), 'color':color('TTJets')-2,'weight':'weight', 'niceName':'t#bar{t} Jets comb'}
DY = {'name':'DY', 'chain':getChain(DY_25ns,histname=''), 'color':color('DY'),'weight':'weight', 'niceName':'Drell Yan'}
singleTop = {'name':'singleTop', 'chain':getChain(singleTop_25ns,histname=''), 'color':color('singleTop'),'weight':'weight', 'niceName':'single Top'}
#QCD = {'name':'QCD', 'chain':getChain(QCDMu_25ns,histname=''), 'color':color('QCD'),'weight':'weight', 'niceName':'QCD'}
QCD = {'name':'QCD', 'chain':getChain(QCDHT_25ns,histname=''), 'color':color('QCD'),'weight':'weight', 'niceName':'QCD'}
TTVH = {'name':'TTVH', 'chain':getChain(TTV_25ns,histname=''), 'color':color('TTV'),'weight':'weight', 'niceName':'TTVH'}
Rest = {'name':'TTVH', 'chain':getChain([TTV_25ns,singleTop_25ns,DY_25ns],histname=''), 'color':color('TTV'),'weight':'weight', 'niceName':'Rest EWK'}
#QCD = {'name':'QCD', 'chain':getChain(QCDEle_25ns,histname=''), 'color':color('QCD'),'weight':'weight', 'niceName':'QCD'}
#diBoson = {'name':'diBoson', 'chain':getChain(diBosons_25ns,histname=''), 'color':ROOT.kMagenta,'weight':'weight', 'niceName':'diboson'}
samples = [WJETS, TTJets_com, Rest, QCD]#, diBoson]

TTandWJets = {'name':'TTJets', 'chain':getChain([TTJets_combined,WJetsHTToLNu_25ns],histname=''), 'color':color('TTJets')-2,'weight':'weight', 'niceName':'t#bar{t}+W Jets '}
#samplesComp = [WJETS, TTJETS, singleTop, DY, QCD]

#EWK = {'name':'EWK', 'chain':getChain([WJetsHT_25ns,TTJets_HTLO_25ns,singleTop_25ns,DY_25ns,TTV_25ns],histname=''), 'color':color('DY'),'weight':'weight', 'niceName':'EWK'}

Data = {'name':'data', 'chain':getChain([single_mu_Run2015D, single_ele_Run2015D],histname=''), 'color':ROOT.kBlack,'weight':'weight', 'niceName':'data', 'cut':False}
#Data = {'name':'data', 'chain':getChain([TTJets_combined,WJetsHTToLNu_25ns,DY_25ns,singleTop_25ns,QCDHT_25ns,TTV_25ns],histname=''), 'color':ROOT.kBlack,'weight':'weight', 'niceName':'data', 'cut':False}


lumi = 2.25
sampleLumi = 3.

MCweight = 'lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*0.94*TopPtWeight'

weight_str, weight_err_str = makeWeight(lumi, sampleLumi, reWeight=MCweight)

dPhiJet1Met = {'name':'acos(cos(Jet_phi[0]-met_phi))', 'binning':[16,0,pi], 'titleX':'#Delta#Phi(j_{1},#slash{E}_{T})', 'titleY':'Events', 'fileName':'dPhiJet1Met'}
mindPhiJetMet2 = {'name':'min(acos(cos(Jet_phi[0]-met_phi)),acos(cos(Jet_phi[1]-met_phi)))', 'binning':[16,0,pi], 'titleX':'min(#Delta#Phi(j_{1,2},#slash{E}_{T}))', 'titleY':'Events', 'fileName':'mindPhiJet12Met'}
mindPhiJetMet3 = {'name':'min(min(acos(cos(Jet_phi[0]-met_phi)),acos(cos(Jet_phi[1]-met_phi))),acos(cos(Jet_phi[2]-met_phi)))', 'binning':[16,0,pi], 'titleX':'min(#Delta#Phi(j_{1,2,3},#slash{E}_{T}))', 'titleY':'Events', 'fileName':'mindPhiJet123Met'}
mindPhiJetMet4 = {'name':'min(min(acos(cos(Jet_phi[0]-met_phi)),acos(cos(Jet_phi[1]-met_phi))),min(acos(cos(Jet_phi[2]-met_phi)),acos(cos(Jet_phi[3]-met_phi))))', 'binning':[16,0,pi], 'titleX':'min(#Delta#Phi(j_{1,2,3,4},#slash{E}_{T}))', 'titleY':'Events', 'fileName':'mindPhiJet1234Met'}

dPhiJet2Met = {'name':'acos(cos(Jet_phi[1]-met_phi))', 'binning':[16,0,pi], 'titleX':'#Delta#Phi(j_{2},#slash{E}_{T})', 'titleY':'Events', 'fileName':'dPhiJet2Met'}
dPhiJet3Met = {'name':'acos(cos(Jet_phi[2]-met_phi))', 'binning':[16,0,pi], 'titleX':'#Delta#Phi(j_{3},#slash{E}_{T})', 'titleY':'Events', 'fileName':'dPhiJet3Met'}
dPhiJet4Met = {'name':'acos(cos(Jet_phi[3]-met_phi))', 'binning':[16,0,pi], 'titleX':'#Delta#Phi(j_{4},#slash{E}_{T})', 'titleY':'Events', 'fileName':'dPhiJet4Met'}

triggers = "(HLT_EleHT350||HLT_MuHT350)"
#filters = "Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_CSCTightHaloFilter && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter"
filters = "Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter && veto_evt_list"
presel = "((!isData&&singleLeptonic)||(isData&&"+triggers+"&&((muonDataSet&&singleMuonic)||(eleDataSet&&singleElectronic))&&"+filters+"))"
presel += "&& nLooseHardLeptons==1 && nTightHardLeptons==1 && nLooseSoftLeptons==0 && Jet_pt[1]>80 && st>250 && nJet30>2 && htJet30j>500"
newpresel = presel

#name, cut = nameAndCut((450,-1),(500,-1),(4,5),btb=(1,1),presel=newpresel)
#cut = {'name':name,'string':cut+'&&singleElectronic&&abs(leptonEta)<2.4&&'+filters,'niceName':'L_{T} [250,350), H_{T} [500,-1)'}

#name, cut = nameAndCut((250,350),(500,-1),(3,4),btb=(0,0),presel=newpresel)
#cut2 = {'name':name,'string':cut,'niceName':'L_{T} [250,350), H_{T} [500,-1)'}
#
#name, cut = nameAndCut((250,-1),(500,-1),(4,5),btb=(1,1),presel=newpresel)
#cut3 = {'name':name,'string':cut,'niceName':'L_{T} [250,350), H_{T} [500,-1)'}
#
#name, cut = nameAndCut((350,450),(500,-1),(4,5),btb=(1,1),presel=newpresel)
#cut4 = {'name':name,'string':cut,'niceName':'L_{T} [250,350), H_{T} [500,-1)'}
#
#name, cut = nameAndCut((450,-1),(500,-1),(4,5),btb=(1,1),presel=newpresel)
#cut5 = {'name':name,'string':cut,'niceName':'L_{T} [250,350), H_{T} [500,-1)'}


#binCut = cut
#varList = [dPhiJet1Met, dPhiJet2Met, dPhiJet3Met, dPhiJet4Met, mindPhiJetMet2, mindPhiJetMet3, mindPhiJetMet4]
varList = [dPhiJet1Met]#, dPhiJet2Met, dPhiJet3Met, mindPhiJetMet2, mindPhiJetMet3]

specialName = ''

printDir = '/afs/hephy.at/user/d/dspitzbart/www/Spring15/25ns/dPhiJetMetFit_v2/'
if not os.path.exists(printDir):
  os.makedirs(printDir)

signalRegions = signalRegion3fb

QCD_LP = ROOT.TH1F('QCD_LP','QCD_LP',13,0,13)
QCD_DPJM = ROOT.TH1F('QCD_DPJM','QCD_DPJM',13,0,13)
one = ROOT.TH1F('one','one',13,0,13)

bins = {}
i = 1

for srNJet in sorted(signalRegions):
  bins[srNJet] = {}
  Qname, Qcut = nameAndCut((250,-1),(500,-1),(4,-1),btb=(0,-1),presel=newpresel)
  QCDcut = {'name':Qname,'string':Qcut+'&&singleElectronic&&abs(leptonEta)<2.4','niceName':'L_{T} [250,350), H_{T} [500,-1)'}
  varQ = varList[0]
  template_QCD = getPlotFromChain(QCD['chain'], varQ['name'], varQ['binning'], QCDcut['string'], weight_str)
  y_QCD = template_QCD.Integral()
  if template_QCD.Integral()>0: template_QCD.Scale(1./template_QCD.Integral())
  for stb in sorted(signalRegions[srNJet]):
    bins[srNJet][stb] ={}
    for htb in sorted(signalRegions[srNJet][stb]):
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      name, cut = nameAndCut(stb,htb,srNJet,btb=(0,0),presel=newpresel)
      cut = {'name':name,'string':cut+'&&singleElectronic&&abs(leptonEta)<2.4','niceName':'L_{T} [250,350), H_{T} [500,-1)'}
      binCut = cut
      bins[srNJet][stb][htb] = {}

      for var in varList:
        template_TTJets = getPlotFromChain(TTJets_com['chain'], var['name'], var['binning'], binCut['string'], weight_str)
        template_TTandWJets = getPlotFromChain(TTandWJets['chain'], var['name'], var['binning'], binCut['string'], weight_str)
        template_WJets = getPlotFromChain(WJETS['chain'], var['name'], var['binning'], binCut['string'], weight_str)
        #template_WJets_PosPdg = getPlotFromChain(WJETS['chain'], var['name'], var['binning'], binCut['string']+'&&leptonPdg>0', weight_str)
        #template_WJets_NegPdg = getPlotFromChain(WJETS['chain'], var['name'], var['binning'], binCut['string']+'&&leptonPdg<0', weight_str)
        
        #template_QCD = getPlotFromChain(QCD['chain'], var['name'], var['binning'], binCut['string'], weight_str)
        #template_QCD_PosPdg = getPlotFromChain(QCD['chain'], var['name'], var['binning'], binCut['string'], weight_str)
        #template_QCD_PosPdg.Scale(0.5)
        #template_QCD_NegPdg = template_QCD_PosPdg
        
        template_Rest = getPlotFromChain(Rest['chain'], var['name'], var['binning'], binCut['string'], weight_str)
        #template_Rest_PosPdg = getPlotFromChain(Rest['chain'], var['name'], var['binning'], binCut['string']+'&&leptonPdg>0', weight_str)
        #template_Rest_NegPdg = getPlotFromChain(Rest['chain'], var['name'], var['binning'], binCut['string']+'&&leptonPdg<0', weight_str)
        
        hData = getPlotFromChain(Data['chain'], var['name'], var['binning'], binCut['string'])
        #hData_PosPdg = getPlotFromChain(Data['chain'], var['name'], var['binning'], binCut['string']+'&&leptonPdg>0')
        #hData_NegPdg = getPlotFromChain(Data['chain'], var['name'], var['binning'], binCut['string']+'&&leptonPdg<0')
        
        
        print 'Total MC truth yields:'
        print 'ttbar+Jets:',template_TTJets.Integral()
        print 'W+Jets:',template_WJets.Integral()
        print 'Rest EWK:', template_Rest.Integral()
        print 'QCD:', template_QCD.Integral()
        
        y_TTJets = template_TTJets.Integral()
        y_TTandWJets = template_TTandWJets.Integral()
        y_WJets = template_WJets.Integral()
        #y_QCD = template_QCD.Integral()
        y_Rest = template_Rest.Integral()
        #y_Rest_PosPdg = template_Rest_PosPdg.Integral()
        #y_Rest_NegPdg = template_Rest_NegPdg.Integral()
        
        #tt = ROOT.TH1F()
        #w = ROOT.TH1F()
        #template_TTJets.Copy(tt)
        #template_WJets.Copy(w)
      
        #template_WJets.Add(tt)
        #template_TTJets.Add(w,-1)
        
        template_TTJets.Scale(1./template_TTJets.Integral())
        template_TTandWJets.Scale(1./template_TTandWJets.Integral())
        template_WJets.Scale(1./template_WJets.Integral())
        #template_WJets_PosPdg.Scale(1./template_WJets_PosPdg.Integral())
        #template_WJets_NegPdg.Scale(1./template_WJets_NegPdg.Integral())
        
        template_Rest.Scale(1./template_Rest.Integral())
        #template_Rest_PosPdg.Scale(1./template_Rest_PosPdg.Integral())
        #template_Rest_NegPdg.Scale(1./template_Rest_NegPdg.Integral())
        #if template_QCD.Integral()>0: template_QCD.Scale(1./template_QCD.Integral())
        #template_QCD_PosPdg.Scale(1./template_QCD_PosPdg.Integral())
        #template_QCD_NegPdg.Scale(1./template_QCD_NegPdg.Integral())
        
        x=ROOT.RooRealVar(var['name'],var['name'],0.,pi)
        
        data=ROOT.RooDataHist("data","data",ROOT.RooArgList(x),hData)
        #data_PosPdg=ROOT.RooDataHist("data_PosPdg","data_PosPdg",ROOT.RooArgList(x),hData_PosPdg)
        #data_NegPdg=ROOT.RooDataHist("data_NegPdg","data_NegPdg",ROOT.RooArgList(x),hData_NegPdg)
        
        dh_WJets=ROOT.RooDataHist("mcWJets","mcWJets",ROOT.RooArgList(x),template_WJets)
        #dh_WJets_PosPdg=ROOT.RooDataHist("mcWJets_PosPdg","mcWJets_PosPdg",ROOT.RooArgList(x),template_WJets_PosPdg)
        #dh_WJets_NegPdg=ROOT.RooDataHist("mcWJets_NegPdg","mcWJets_NegPdg",ROOT.RooArgList(x),template_WJets_NegPdg)
        
        dh_TTJets=ROOT.RooDataHist("mcTTJets","mcTTJets",ROOT.RooArgList(x),template_TTJets)
        dh_TTandWJets=ROOT.RooDataHist("mcTTandWJets","mcTTandWJets",ROOT.RooArgList(x),template_TTandWJets)
        #dh_TTJets_AllPdg=ROOT.RooDataHist("mcTTJets_AllPdg","mcTTJets_AllPdg",ROOT.RooArgList(x),template_TTJets)
        
        dh_Rest=ROOT.RooDataHist("mcRest","mcRest",ROOT.RooArgList(x),template_Rest)
        #dh_Rest_PosPdg=ROOT.RooDataHist("mcRest_PosPdg","mcRest_PosPdg",ROOT.RooArgList(x),template_Rest_PosPdg)
        #dh_Rest_NegPdg=ROOT.RooDataHist("mcRest_NegPdg","mcRest_NegPdg",ROOT.RooArgList(x),template_Rest_NegPdg)
        
        dh_QCD=ROOT.RooDataHist("mcQCD","mcQCD",ROOT.RooArgList(x),template_QCD)
        #dh_QCD_PosPdg=ROOT.RooDataHist("mcQCD_PosPdg","mcQCD_PosPdg",ROOT.RooArgList(x),template_QCD_PosPdg)
        #dh_QCD_NegPdg=ROOT.RooDataHist("mcQCD_NegPdg","mcQCD_NegPdg",ROOT.RooArgList(x),template_QCD_NegPdg)
        
        rooDataHist_arr = [data, dh_WJets, dh_TTJets , dh_Rest, dh_QCD]
        
        
        yield_TTJets=ROOT.RooRealVar("ttJets_yield","yieldTTJets",0.1,0,10**5)
        yield_TTandWJets=ROOT.RooRealVar("ttandWJets_yield","yieldTTandWJets",0.1,0,10**5)
        #yield_TTJets_AllPdg=ROOT.RooRealVar("ttJets_yield_AllPdg","yieldTTJets_AllPdg",0.,0,10**5)
        
        yield_WJets=ROOT.RooRealVar("WJets_yield","yieldWJets",0.1,0,10**5)
        #yield_WJets_PosPdg=ROOT.RooRealVar("WJets_yield_PosPdg","yieldWJets_PosPdg",0.,0,10**5)
        #yield_WJets_NegPdg=ROOT.RooRealVar("WJets_yield_NegPdg","yieldWJets_NegPdg",0.,0,10**5)
        
        #yield_Rest=ROOT.RooRealVar("Rest_yield","yieldRest",0.1,0,10**5)
        yield_Rest=ROOT.RooRealVar("Rest_yield","yieldRest",y_Rest,y_Rest,y_Rest)
        #yield_Rest_PosPdg=ROOT.RooRealVar("Rest_yield_PosPdg","yieldRest_PosPdg",y_Rest_PosPdg,y_Rest_PosPdg,y_Rest_PosPdg)
        #yield_Rest_NegPdg=ROOT.RooRealVar("Rest_yield_NegPdg","yieldRest_NegPdg",y_Rest_NegPdg,y_Rest_NegPdg,y_Rest_NegPdg)
        
        yield_QCD=ROOT.RooRealVar("QCD_yield","yieldQCD",0.1,0,10**5)
        #yield_QCD_PosPdg=ROOT.RooRealVar("QCD_yield_PosPdg","yieldQCD_PosPdg",0.1,0,10**5)
        #yield_QCD_NegPdg=ROOT.RooRealVar("QCD_yield_NegPdg","yieldQCD_NegPdg",0.1,0,10**5)
        
        
        model_TTJets=ROOT.RooHistPdf("model_TTJets","model_TTJets",ROOT.RooArgSet(x),dh_TTJets)
        model_TTandWJets=ROOT.RooHistPdf("model_TTandWJets","model_TTandWJets",ROOT.RooArgSet(x),dh_TTandWJets)
        #model_TTJets_AllPdg=ROOT.RooHistPdf("model_TTJets_AllPdg","model_TTJets_AllPdg",ROOT.RooArgSet(x),dh_TTJets_AllPdg)
        
        model_WJets=ROOT.RooHistPdf("model_WJets","model_WJets",ROOT.RooArgSet(x),dh_WJets)
        #model_WJets_PosPdg=ROOT.RooHistPdf("model_WJets_PosPdg","model_WJets_PosPdg",ROOT.RooArgSet(x),dh_WJets_PosPdg)
        #model_WJets_NegPdg=ROOT.RooHistPdf("model_WJets_NegPdg","model_WJets_NegPdg",ROOT.RooArgSet(x),dh_WJets_NegPdg)
        
        model_Rest=ROOT.RooHistPdf("model_Rest","model_Rest",ROOT.RooArgSet(x),dh_Rest)
        #model_Rest_PosPdg=ROOT.RooHistPdf("model_Rest_PosPdg","model_Rest_PosPdg",ROOT.RooArgSet(x),dh_Rest_PosPdg)
        #model_Rest_NegPdg=ROOT.RooHistPdf("model_Rest_NegPdg","model_Rest_NegPdg",ROOT.RooArgSet(x),dh_Rest_NegPdg)
        
        model_QCD=ROOT.RooHistPdf("model_QCD","model_QCD",ROOT.RooArgSet(x),dh_QCD)
        #model_QCD_PosPdg=ROOT.RooHistPdf("model_QCD_PosPdg","model_QCD_PosPdg",ROOT.RooArgSet(x),dh_QCD_PosPdg)
        #model_QCD_NegPdg=ROOT.RooHistPdf("model_QCD_NegPdg","model_QCD_NegPdg",ROOT.RooArgSet(x),dh_QCD_NegPdg)
        
        
        model=ROOT.RooAddPdf("model","model",ROOT.RooArgList(model_WJets, model_TTJets, model_Rest, model_QCD),ROOT.RooArgList(yield_WJets, yield_TTJets, yield_Rest, yield_QCD))
        #model=ROOT.RooAddPdf("model","model",ROOT.RooArgList(model_TTandWJets, model_Rest, model_QCD),ROOT.RooArgList(yield_TTandWJets, yield_Rest, yield_QCD))
        #model_PosPdg=ROOT.RooAddPdf("model","model",ROOT.RooArgList(model_WJets_PosPdg, model_TTJets_AllPdg, model_Rest_PosPdg, model_QCD_PosPdg),ROOT.RooArgList(yield_WJets_PosPdg, yield_TTJets_AllPdg, yield_Rest_PosPdg, yield_QCD_PosPdg))
        #model_NegPdg=ROOT.RooAddPdf("model","model",ROOT.RooArgList(model_WJets_NegPdg, model_TTJets_AllPdg, model_Rest_NegPdg, model_QCD_NegPdg),ROOT.RooArgList(yield_WJets_NegPdg, yield_TTJets_AllPdg, yield_Rest_NegPdg, yield_QCD_NegPdg))
        
        
        
        dframe=x.frame(rf.Title("Data"))
        #dframe_Pdg=x.frame(rf.Title("Data Charge split"))
        
        data.plotOn(dframe)
        #data_PosPdg.plotOn(dframe_Pdg)
        #data_NegPdg.plotOn(dframe_Pdg)
        
        frame_WJets=x.frame(rf.Title("WJets"))
        model_WJets.plotOn(frame_WJets)
        #frame_WJets_PosPdg=x.frame(rf.Title("WJets PosPdg"))
        #model_WJets_PosPdg.plotOn(frame_WJets_PosPdg)
        #frame_WJets_NegPdg=x.frame(rf.Title("WJets NegPdg"))
        #model_WJets_NegPdg.plotOn(frame_WJets_NegPdg)
        
        frame_TTJets=x.frame(rf.Title("TTJets"))
        model_TTJets.plotOn(frame_TTJets)
        #frame_TTandWJets=x.frame(rf.Title("TTandWJets"))
        #model_TTandWJets.plotOn(frame_TTandWJets)
        #frame_TTJets_AllPdg=x.frame(rf.Title("TTJets Pdg"))
        #model_TTJets_AllPdg.plotOn(frame_TTJets_AllPdg)
        
        frame_Rest=x.frame(rf.Title("Rest"))
        model_Rest.plotOn(frame_Rest)
        #frame_Rest_PosPdg=x.frame(rf.Title("Rest PosPdg"))
        #model_Rest_PosPdg.plotOn(frame_Rest_PosPdg)
        #frame_Rest_NegPdg=x.frame(rf.Title("Rest NegPdg"))
        #model_Rest_NegPdg.plotOn(frame_Rest_NegPdg)
        
        frame_QCD=x.frame(rf.Title("QCD"))
        model_QCD.plotOn(frame_QCD)
        #frame_QCD_PosPdg=x.frame(rf.Title("QCD PosPdg"))
        #model_QCD_PosPdg.plotOn(frame_QCD_PosPdg)
        #frame_QCD_NegPdg=x.frame(rf.Title("QCD NegPdg"))
        #model_QCD_NegPdg.plotOn(frame_QCD_NegPdg)
        
        print "starting to perform fit !!!!"
        
        #model.fitTo(data)#It is this fitTo command that gives the statistical output
        nllComponents = ROOT.RooArgList("nllComponents")
        nll=model.createNLL(data,rf.NumCPU(1))
        nllComponents.add(nll)
        
        #nll_PosPdg=model_PosPdg.createNLL(data_PosPdg,rf.NumCPU(1))
        #nll_NegPdg=model_NegPdg.createNLL(data_NegPdg,rf.NumCPU(1))
        #nllComponents.add(nll_PosPdg)
        #nllComponents.add(nll_NegPdg)
        
        #pll_phi=nll.createProfile(r.RooArgSet(mc1_yield))#anotherwayofdoingthefitTo
        sumNLL = ROOT.RooAddition("sumNLL","sumNLL", nllComponents)
        
        ROOT.RooMinuit(sumNLL).migrad()
        ROOT.RooMinuit(sumNLL).hesse()
        ROOT.RooMinuit(sumNLL).minos()#optional
        
        ##myPdf->paramOn(frame,Layout(xmin,ymin,ymax))
        #fitFrame_PosPdg=x.frame(rf.Bins(50),rf.Title("FitModel"))
        #model_PosPdg.paramOn(fitFrame_PosPdg,rf.Layout(0.42,0.9,0.9))
        #data_PosPdg.plotOn(fitFrame_PosPdg,rf.LineColor(ROOT.kRed))
        #model_PosPdg.plotOn(fitFrame_PosPdg,rf.LineStyle(ROOT.kDashed))
        #model_PosPdg.plotOn(fitFrame_PosPdg,rf.Components("model_WJets_PosPdg"),rf.LineColor(ROOT.kGreen))
        #model_PosPdg.plotOn(fitFrame_PosPdg,rf.Components("model_TTJets_AllPdg"),rf.LineColor(ROOT.kBlue))
        #model_PosPdg.plotOn(fitFrame_PosPdg,rf.Components("model_Rest_PosPdg"),rf.LineColor(ROOT.kOrange+7))
        #model_PosPdg.plotOn(fitFrame_PosPdg,rf.Components("model_QCD_PosPdg"),rf.LineColor(color('QCD')))
        
        #fitFrame_NegPdg=x.frame(rf.Bins(50),rf.Title("FitModel"))
        #model_NegPdg.paramOn(fitFrame_NegPdg,rf.Layout(0.42,0.9,0.9))
        #data_NegPdg.plotOn(fitFrame_NegPdg,rf.LineColor(ROOT.kRed))
        #model_NegPdg.plotOn(fitFrame_NegPdg,rf.LineStyle(ROOT.kDashed))
        #model_NegPdg.plotOn(fitFrame_NegPdg,rf.Components("model_WJets_NegPdg"),rf.LineColor(ROOT.kGreen))
        #model_NegPdg.plotOn(fitFrame_NegPdg,rf.Components("model_TTJets_AllPdg"),rf.LineColor(ROOT.kBlue))
        #model_NegPdg.plotOn(fitFrame_NegPdg,rf.Components("model_Rest_NegPdg"),rf.LineColor(ROOT.kOrange+7))
        #model_NegPdg.plotOn(fitFrame_NegPdg,rf.Components("model_QCD_NegPdg"),rf.LineColor(color('QCD')))
        
        #myPdf->paramOn(frame,Layout(xmin,ymin,ymax))
        fitFrame=x.frame(rf.Bins(50),rf.Title("FitModel"))
        model.paramOn(fitFrame,rf.Layout(0.42,0.9,0.9))
        data.plotOn(fitFrame,rf.LineColor(ROOT.kRed))
        model.plotOn(fitFrame,rf.LineStyle(ROOT.kDashed))
        model.plotOn(fitFrame,rf.Components("model_WJets"),rf.LineColor(ROOT.kGreen))
        model.plotOn(fitFrame,rf.Components("model_TTJets"),rf.LineColor(ROOT.kBlue))
        #model.plotOn(fitFrame,rf.Components("model_TTandWJets"),rf.LineColor(ROOT.kBlue))
        model.plotOn(fitFrame,rf.Components("model_Rest"),rf.LineColor(ROOT.kOrange+7))
        model.plotOn(fitFrame,rf.Components("model_QCD"),rf.LineColor(color('QCD')))
        
        print "** Fit results **"
        print "yield_WJets:" , yield_WJets.getVal()
        print "yield_TTJets:" , yield_TTJets.getVal()
        print "yield_Rest:" , yield_Rest.getVal()
        print "yield_QCD:", yield_QCD.getVal()
        print
        print "yield_TTandWJets:" , yield_TTandWJets.getVal()
        fit_total = yield_WJets.getVal()+yield_TTJets.getVal()+yield_Rest.getVal()+yield_QCD.getVal()
        
        QCD_LP.SetBinContent(i, QCDestimate[srNJet][stb][htb][(0,0)][deltaPhiCut]['NQCDpred'])
        QCD_LP.SetBinError(i, QCDestimate[srNJet][stb][htb][(0,0)][deltaPhiCut]['NQCDpred_err'])
        QCD_DPJM.SetBinContent(i, yield_QCD.getVal())
        QCD_DPJM.SetBinError(i, yield_QCD.getError())
#        print 'yield QCD pred',QCDestimate[(4,5)][stb][htb][(1,1)][deltaPhiCut]['NQCDpred']
        one.SetBinContent(i,1)
        i = i+1
        fit = {'WJets':yield_WJets.getVal(), 'TTJets':yield_TTJets.getVal(), 'Rest':yield_Rest.getVal(), 'QCD':yield_QCD.getVal(), 'QCDerr':yield_QCD.getError(), 'TTandWJetsComb':yield_TTandWJets.getVal()}
        fit_frac = {}
        for key in fit:
          fit_frac[key] = fit[key]/fit_total
        
        print
        print "** MC truth **"
        print "WJets:" , y_WJets
        print "TTJets:" , y_TTJets
        print "Rest:" , y_Rest
        print "QCD:", y_QCD
        print
        print "TT and WJets:" , y_WJets+y_TTJets
        
        truth_total = y_WJets+y_TTJets+y_Rest+y_QCD
        
        truth = {'WJets':y_WJets, 'TTJets':y_TTJets, 'Rest':y_Rest, 'QCD':y_QCD, 'TTandWJetsComb':y_WJets+y_TTJets}
        truth_frac = {}
        for key in truth:
          truth_frac[key] = truth[key]/truth_total
      
        bins[srNJet][stb][htb][var['fileName']] = {'MCtruth':truth, 'MCtruth_frac':truth_frac, 'fit':fit, 'fit_frac':fit_frac}
                
        c2=ROOT.TCanvas("c2","FitModel",650,500)
        ROOT.gROOT.SetStyle("Plain")
        ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
        ROOT.gPad.SetLeftMargin(0.15)
        fitFrame.GetYaxis().SetTitleOffset(1.4)
        fitFrame.GetXaxis().SetTitle(var['titleX'])
        fitFrame.Draw()
        
        #c1=ROOT.TCanvas("c1","FitModel",650,1000)
        #ROOT.gROOT.SetStyle("Plain")
        #c1.Divide(1,2)
        #c1.cd(1)
        #ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
        #ROOT.gPad.SetLeftMargin(0.15)
        #fitFrame_PosPdg.GetYaxis().SetTitleOffset(1.4)
        #fitFrame_PosPdg.GetXaxis().SetTitle(var['titleX'])
        #fitFrame_PosPdg.Draw()
        #
        #c1.cd(2)
        #ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
        #ROOT.gPad.SetLeftMargin(0.15)
        #fitFrame_NegPdg.GetYaxis().SetTitleOffset(1.4)
        #fitFrame_NegPdg.GetXaxis().SetTitle(var['titleX'])
        #fitFrame_NegPdg.Draw()
        
        ROOT.setTDRStyle()
        ROOT.gStyle.SetPalette(1)
        c3=ROOT.TCanvas("c3","templates",650,650)
        allTemplates = [template_TTJets, template_WJets, template_QCD, template_Rest]
        template_TTJets.SetLineColor(color('ttjets')-2)
        template_TTJets.GetXaxis().SetTitle('#Delta#Phi(j_{1},#slash{E}_{T})')
        template_TTJets.GetYaxis().SetTitle('a.u.')
        template_TTJets.SetMaximum(0.4)
        template_WJets.SetLineColor(color('wjets'))
        template_QCD.SetLineColor(color('qcd'))
        template_Rest.SetLineColor(color('dy'))
        #template_TTandWJets.SetLineColor(ROOT.kMagenta)
        for temp in allTemplates:
          temp.SetLineWidth(2)
          temp.SetMarkerSize(0)
        template_TTJets.Draw('hist e1')
        template_WJets.Draw('hist e1 same')
        template_QCD.Draw('hist e1 same')
        template_Rest.Draw('hist e1 same')
        
        leg = ROOT.TLegend(0.16,0.75,0.4,0.95)
        leg.SetFillColor(ROOT.kWhite)
        leg.SetShadowColor(ROOT.kWhite)
        leg.SetBorderSize(1)
        leg.SetTextSize(0.04)
        leg.AddEntry(template_TTJets, 'W+jets', 'l')
        leg.AddEntry(template_WJets, 't#bar{t}+jets', 'l')
        leg.AddEntry(template_QCD, 'QCD', 'l')
        leg.AddEntry(template_Rest, 'other', 'l')

        leg.Draw()
        
        latex1 = ROOT.TLatex()
        latex1.SetNDC()
        latex1.SetTextSize(0.04)
        latex1.SetTextAlign(11)
        
        latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{Simulation}}')
        latex1.DrawLatex(0.85,0.96,"(13TeV)")



        ROOT.setTDRStyle()
        ROOT.gStyle.SetPalette(1)
        c4=ROOT.TCanvas("c4","correlation",650,500)
        res = model.fitTo(data, rf.Save())
        resH = res.correlationHist()
        resH.SetMarkerSize(2)
        
        pad1=ROOT.TPad("pad1","MyTitle",0.,0.,1.,1.)
        pad1.SetLeftMargin(0.15)
        pad1.SetBottomMargin(0.1)
        pad1.SetRightMargin(0.15)
        pad1.Draw()
        pad1.cd()
        
        resH.GetXaxis().SetBinLabel(1,'QCD')
        resH.GetXaxis().SetBinLabel(2,'W+jets')
        resH.GetXaxis().SetBinLabel(3,'t#bar{t}+jets')
        resH.GetXaxis().SetBinLabel(4,'Rest EWK')
        
        resH.GetYaxis().SetBinLabel(4,'QCD')
        resH.GetYaxis().SetBinLabel(3,'W+jets')
        resH.GetYaxis().SetBinLabel(2,'t#bar{t}+jets')
        resH.GetYaxis().SetBinLabel(1,'Rest EWK')
        resH.Draw('colz text')
        
        
        c2.Print(printDir+specialName+name+'_'+var['fileName']+'_fit.png')
        c2.Print(printDir+specialName+name+'_'+var['fileName']+'_fit.root')
        c3.Print(printDir+specialName+name+'_'+var['fileName']+'_templates.png')
        c3.Print(printDir+specialName+name+'_'+var['fileName']+'_templates.pdf')
        c3.Print(printDir+specialName+name+'_'+var['fileName']+'_templates.root')
        c4.Print(printDir+specialName+name+'_'+var['fileName']+'_correlation.png')

QCD_DPJM.Divide(QCD_LP)

c5=ROOT.TCanvas("c5","ratio",650,650)
QCD_DPJM.SetMaximum(5.)
QCD_DPJM.SetMinimum(0.)
QCD_DPJM.SetLineColor(ROOT.kAzure+9)
QCD_DPJM.SetMarkerColor(ROOT.kAzure+9)

QCD_DPJM.GetYaxis().SetTitle('QCD_{fit}(#Delta#Phi(j_{1},#slash{E}_{T}))/QCD_{fit}(L_{P})')

QCD_DPJM.GetYaxis().SetTitleSize(0.045)
QCD_DPJM.GetYaxis().SetTitleOffset(1.7)

QCD_DPJM.GetYaxis().SetLabelSize(0.045)
QCD_DPJM.GetXaxis().SetLabelSize(0.04)

setNiceBinLabel(QCD_DPJM, signalRegions)

QCD_DPJM.Draw('E0P')
one.Draw('hist same')

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{Preliminary}}')
latex1.DrawLatex(0.75,0.96,"2.2fb^{-1}(13TeV)")

c5.Print(printDir+specialName+'MB_data_'+var['fileName']+'_ratio.png')
c5.Print(printDir+specialName+'MB_data_'+var['fileName']+'_ratio.root')
c5.Print(printDir+specialName+'MB_data_'+var['fileName']+'_ratio.pdf')


