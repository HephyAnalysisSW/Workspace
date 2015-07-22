import ROOT
import pickle 
import copy, os, sys
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.TH1F().SetDefaultSumw2()
ROOT.setTDRStyle()

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.HEPHYPythonTools.xsec import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.cmgTuples_v1_PHYS14V3 import *
#from Workspace.RA4Analysis.cmgTuples_PHYS14V3 import *
from Workspace.RA4Analysis.signalRegions import *
from draw_helpers import *
from math import *
from localInfo import username
from LpTemplateFit import LpTemplateFit

preprefix = 'QCDestimation'
wwwDir = '/afs/hephy.at/user/d/dhandl/www/pngCMG2/hard/Phys14V3/'+preprefix+'/'
presel = 'RcsQCD_singleElectronic_'

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

#choose bins
#htreg = [(500,-1), (500,750), (750,-1), (500,1000), (1000,-1)]
#streg = [(200,-1),(250,350), (350,450), (450,-1)]
#njreg = [(4,5), (5,5), (6,7), (8,-1)]
CRnjreg = (4,5)
btreg = [(0,0),(1,1),(2,2),(3,-1)]

#small = True
small = False
#doFit = True
#doFit = False

eleVarList = ['pt', 'eta', 'phi', 'pdgId', 'miniRelIso', 'convVeto', 'sip3d', 'mvaIdPhys14', 'charge', 'lostHits']
eleFromW = ['pt', 'eta', 'phi', 'pdgId', 'motherId', 'grandmotherId', 'charge', 'sourceId']

QCD_HT_100To250_PU20bx25={\
"name" : "QCD_HT_100To250",
"chunkString": "QCD_HT_100To250",
'dir' : "/data/easilar/Phys14_V3/",
'dbsName':'/QCD_HT_100To250_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}

QCD_HT_250To500_PU20bx25={\
"name" : "QCD_HT_250To500",
"chunkString": "QCD_HT_250To500",
'dir' : "/data/easilar/Phys14_V3/",
'dbsName':'/QCD_HT_250To500_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
QCD_HT_500To1000_PU20bx25={\
"name" : "QCD_HT_500To1000",
"chunkString": "QCD_HT_500To1000",
'dir' : "/data/easilar/Phys14_V3/",
'dbsName':'/QCD_HT_500To1000_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
QCD_HT_1000ToInf_PU20bx25={\
"name" : "QCD_HT_1000ToInf",
"chunkString": "QCD_HT_1000ToInf",
'dir' : "/data/easilar/Phys14_V3/",
'dbsName':'/QCD_HT_1000ToInf_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}

target_lumi = 3000 #pb-1
def getWeight(sample,nEvents,target_lumi):
  weight = xsec[sample['dbsName']] * target_lumi/nEvents
  return weight

singleElectronVeto = '((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=5))==0&&'\
                     +'(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&LepGood_miniRelIso<0.4&&((abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>0.35)'\
                     +'||((abs(LepGood_eta)>0.8&&abs(LepGood_eta)<1.479)&&LepGood_mvaIdPhys14>0.2)'\
                     +'||((abs(LepGood_eta)>1.479&&abs(LepGood_eta)<2.4)&&LepGood_mvaIdPhys14>-0.52))&&LepGood_lostHits<=1&&LepGood_convVeto&&LepGood_sip3d<4.0))==1)'

singleElectronVetoAnti = '((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=5))==0&&'\
                         +'(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&LepGood_miniRelIso<0.4&&((abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>0.35)'\
                         +'||((abs(LepGood_eta)>0.8&&abs(LepGood_eta)<1.479)&&LepGood_mvaIdPhys14>0.2)'\
                         +'||((abs(LepGood_eta)>1.479&&abs(LepGood_eta)<2.4)&&LepGood_mvaIdPhys14>-0.52))))==1)'

antiSelStr = '((abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>=0.35&&LepGood_mvaIdPhys14<0.73)||'\
             +'(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)>=0.8&&abs(LepGood_eta)<1.479&&LepGood_mvaIdPhys14>=0.20&&LepGood_mvaIdPhys14<0.57)||'\
             +'(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)>=1.479&&abs(LepGood_eta)<2.4&&LepGood_mvaIdPhys14>=(-0.52)&&LepGood_mvaIdPhys14<0.05))'

SelStr = '((abs(LepGood_pdgId)==11&&LepGood_pt>=25&&LepGood_miniRelIso<0.1&&LepGood_convVeto&&LepGood_sip3d<4.0&&LepGood_lostHits==0&&abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>=0.73)||'\
           +'(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&LepGood_miniRelIso<0.1&&LepGood_convVeto&&LepGood_sip3d<4.0&&LepGood_lostHits==0&&abs(LepGood_eta)>=0.8&&abs(LepGood_eta)<1.479&&LepGood_mvaIdPhys14>=0.57)||'\
           +'(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&LepGood_miniRelIso<0.1&&LepGood_convVeto&&LepGood_sip3d<4.0&&LepGood_lostHits==0&&abs(LepGood_eta)>=1.479&&abs(LepGood_eta)<2.4&&LepGood_mvaIdPhys14>=0.05))'

singleHardElectron = '(Sum$('+antiSelStr+'||'+SelStr+')==1)'

def stCutQCD(stb):
  if type(stb)==type([]) or type(stb)==type(()):
    if len(stb)>1 and stb[1]>=0:
      return   "(Sum$((LepGood_pt+met_pt)*(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.4)>"+str(stb[0])+")==1&&"\
               +"Sum$((LepGood_pt+met_pt)*(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.4)<="+str(stb[1])+")==1 )"
    else:
      return "(Sum$((LepGood_pt+met_pt)*(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.4)>"+str(stb[0])+")==1)"
  else:
    return   "(Sum$((LepGood_pt+met_pt)*(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.4)>"+str(stb)+")==1)"

def getLp(met,metPhi,e):
#  met = c.GetLeaf('met_pt').GetValue()
#  metPhi = c.GetLeaf('met_phi').GetValue()
  
  Lp = e['pt']/sqrt( (e['pt']*cos(e['phi']) + met*cos(metPhi))**2 + (e['pt']*sin(e['phi']) + met*sin(metPhi))**2 )\
       * (e['pt']+met*cos(e['phi']-metPhi))/sqrt(e['pt']**2+met**2+2*met*e['pt']*cos(e['phi']-metPhi))
  return Lp

#attention only use this string after singleElectronic (sel/antiSel) preselection
LpStr = '(LepGood_pt/sqrt((LepGood_pt*cos(LepGood_phi)+met_pt*cos(met_phi))**2+(LepGood_pt*sin(LepGood_phi)+met_pt*sin(met_phi))**2))'\
      +'*(LepGood_pt+met_pt*cos(LepGood_phi-met_phi))/sqrt(LepGood_pt**2+met_pt**2+2*met_pt*LepGood_pt*cos(LepGood_phi-met_phi))'

dPhiStr = "acos((LepGood_pt+met_pt*cos(LepGood_phi-met_phi))/sqrt(LepGood_pt**2+met_pt**2+2*met_pt*LepGood_pt*cos(LepGood_phi-met_phi)))"

Bkg = [{'name':'QCD_HT_100To250_PU20bx25', 'sample':QCD_HT_100To250_PU20bx25, 'legendName':'QCD HT100-250', 'color':ROOT.kCyan+3, 'merge':'QCD'},
       {'name':'QCD_HT_250To500_PU20bx25', 'sample':QCD_HT_250To500_PU20bx25, 'legendName':'QCD HT250-500', 'color':ROOT.kCyan, 'merge':'QCD'},
       {'name':'QCD_HT_500To1000_PU20bx25', 'sample':QCD_HT_500To1000_PU20bx25, 'legendName':'QCD HT500-1000', 'color':ROOT.kCyan-3, 'merge':'QCD'},
       {'name':'QCD_HT_1000ToInf_PU20bx25', 'sample':QCD_HT_1000ToInf_PU20bx25, 'legendName':'QCD HT1000-Inf', 'color':ROOT.kCyan-7, 'merge':'QCD'},
       {'name':'TBarToLeptons_sChannel_PU20bx25', 'sample':TBarToLeptons_sChannel_PU20bx25, 'legendName':'TBarToLep sCh', 'color':ROOT.kViolet, 'merge':'EWK'},
       {'name':'TBarToLeptons_tChannel_PU20bx25', 'sample':TBarToLeptons_tChannel_PU20bx25, 'legendName':'TBarToLep tCh', 'color':ROOT.kViolet-3, 'merge':'EWK'},
       {'name':'TToLeptons_sChannel_PU20bx25', 'sample':TToLeptons_sChannel_PU20bx25, 'legendName':'TToLep sCh', 'color':ROOT.kViolet-5, 'merge':'EWK'},
       {'name':'TToLeptons_tChannel_PU20bx25', 'sample':TToLeptons_tChannel_PU20bx25, 'legendName':'TToLep tCh', 'color':ROOT.kViolet-7, 'merge':'EWK'},
       {'name':'T_tWChannel_PU20bx25', 'sample':T_tWChannel_PU20bx25, 'legendName':'TtW', 'color':ROOT.kViolet+1, 'merge':'EWK'},
       {'name':'TBar_tWChannel_PU20bx25', 'sample':TBar_tWChannel_PU20bx25, 'legendName':'TBartW', 'color':ROOT.kViolet+6, 'merge':'EWK'},
       {'name':'ttWJets_PU20bx25', 'sample':ttWJets_PU20bx25, 'legendName':'tt+W', 'color':ROOT.kOrange, 'merge':'EWK'},
       {'name':'ttZJets_PU20bx25', 'sample':ttZJets_PU20bx25, 'legendName':'tt+Z', 'color':ROOT.kOrange+7, 'merge':'EWK'},
       {'name':'ttH_PU20bx25', 'sample':ttH_PU20bx25, 'legendName':'tt+H', 'color':ROOT.kOrange+4, 'merge':'EWK'},
       {'name':'DYJetsToLL_M50_HT100to200_PU20bx25', 'sample':DYJetsToLL_M50_HT100to200_PU20bx25, 'legendName':'DY HT100-200', 'color':ROOT.kRed, 'merge':'EWK'},
       {'name':'DYJetsToLL_M50_HT200to400_PU20bx25', 'sample':DYJetsToLL_M50_HT200to400_PU20bx25, 'legendName':'DY HT200-400', 'color':ROOT.kRed+2, 'merge':'EWK'},
       {'name':'DYJetsToLL_M50_HT400to600_PU20bx25', 'sample':DYJetsToLL_M50_HT400to600_PU20bx25, 'legendName':'DY HT400-600', 'color':ROOT.kRed-7, 'merge':'EWK'},
       {'name':'DYJetsToLL_M50_HT600toInf_PU20bx25', 'sample':DYJetsToLL_M50_HT600toInf_PU20bx25, 'legendName':'DY HT600-Inf', 'color':ROOT.kRed-8, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT100to200_PU20bx25', 'sample':WJetsToLNu_HT100to200_PU20bx25, 'legendName':'W HT100-200', 'color':ROOT.kGreen+3, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT200to400_PU20bx25', 'sample':WJetsToLNu_HT200to400_PU20bx25, 'legendName':'W HT200-400', 'color':ROOT.kGreen, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT400to600_PU20bx25', 'sample':WJetsToLNu_HT400to600_PU20bx25, 'legendName':'W HT400-600', 'color':ROOT.kGreen-3, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT600toInf_PU20bx25', 'sample':WJetsToLNu_HT600toInf_PU20bx25, 'legendName':'W HT600-Inf', 'color':ROOT.kGreen-7, 'merge':'EWK'},
       {'name':'ttJets_PU20bx25', 'sample':ttJets_PU20bx25, 'legendName':'ttJets', 'color':ROOT.kRed, 'merge':'EWK'},# 'prompt':False},
]

maxN=1 if small else -1

for sample in Bkg:
  sample['chunks'], sample['nEvents'] = getChunks(sample['sample'],treeName='treeProducerSusySingleLepton', maxN=maxN)
  sample['chain'] = ROOT.TChain('tree')
  for chunk in sample['chunks']:
    sample['chain'].Add(chunk['file'])

  sample['weight'] = getWeight(sample['sample'], sample['nEvents'], target_lumi)

histos = {}
bins = {}
for njb in sorted(signalRegion3fb):
  bins[njb] = {}
  for stb in sorted(signalRegion3fb[njb]):
    bins[njb][stb] = {}
    for htb in sorted(signalRegion3fb[njb][stb]):
      bins[njb][stb][htb] = {}
      for btb in btreg:
        dPhiCut = signalRegion3fb[njb][stb][htb]['deltaPhi']
        dPhiBinning = [0,dPhiCut,pi]
        print 'Binning => ht: ',htb,'st: ',stb,'NJet: ',njb,'dPhiCut: ',dPhiCut
        SRname = nameAndCut(stb, htb, njb, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]#use this function only for the name string!!!
        #cut only includes very loose lepton selection, HT cut, NJet cut, Btagging and subleading JetPt>=80!!! St cut applied in the Event Loop!!!
#        cut = '(Sum$(abs(LepGood_pdgId)==11&&abs(LepGood_dxy)<=0.05&&abs(LepGood_dz)<=0.1)+Sum$(abs(LepOther_pdgId)==11&&abs(LepOther_dxy)<=0.05&&abs(LepOther_dz)<=0.1)>=1)&&'+htCut(htb, minPt=30, maxEta=2.4, njCorr=0.)+'&&'+ nBTagCut(btb, minPt=30, maxEta=2.4, minCSVTag=0.814)+'&&'+nJetCut(srNJet, minPt=30, maxEta=2.4)+'&&'+nJetCut(2, minPt=80, maxEta=2.4)
        SelCut = singleElectronVeto+'&&'+singleHardElectron+'&&(Sum$('+SelStr+')==1)&&'+stCutQCD(stb)+'&&'+htCut(htb, minPt=30, maxEta=2.4, njCorr=0.)+'&&'+ nBTagCut(btb, minPt=30, maxEta=2.4, minCSVTag=0.814)\
                 +'&&'+nJetCut(njb, minPt=30, maxEta=2.4)+'&&'+nJetCut(2, minPt=80, maxEta=2.4)
        antiSelCut = singleElectronVetoAnti+'&&'+singleHardElectron+'&&(Sum$('+antiSelStr+')==1)&&'+stCutQCD(stb)+'&&'+htCut(htb, minPt=30, maxEta=2.4, njCorr=0.)+'&&'+ nBTagCut(btb, minPt=30, maxEta=2.4, minCSVTag=0.814)\
                     +'&&'+nJetCut(njb, minPt=30, maxEta=2.4)+'&&'+nJetCut(2, minPt=80, maxEta=2.4)

        histos['merged_QCD']={}
        histos['merged_EWK']={}
        histos['merged_QCD']['antiSelection']=ROOT.TH1F('merged_QCD_antiSelection','merged_QCD_antiSelection',len(dPhiBinning)-1, array('d', dPhiBinning))
        histos['merged_QCD']['Selection']=ROOT.TH1F('merged_QCD_Selection','merged_QCD_Selection',len(dPhiBinning)-1, array('d', dPhiBinning))
        histos['merged_EWK']['antiSelection']=ROOT.TH1F('merged_EWK_antiSelection','merged_EWK_antiSelection',len(dPhiBinning)-1, array('d', dPhiBinning))
        histos['merged_EWK']['Selection']=ROOT.TH1F('merged_EWK_Selection','merged_EWK_Selection',len(dPhiBinning)-1, array('d', dPhiBinning))

        for sample in Bkg:
          histos[sample['name']] = {}
          histos[sample['name']]['antiSelection'] = ROOT.TH1F(sample['name']+'_antiSelection', sample['name']+'_antiSelection',len(dPhiBinning)-1, array('d', dPhiBinning))
          histos[sample['name']]['Selection'] = ROOT.TH1F(sample['name']+'_Selection', sample['name']+'_Selection',len(dPhiBinning)-1, array('d', dPhiBinning))

          sample['chain'].Draw(dPhiStr+'>>'+sample['name']+'_antiSelection',str(sample['weight'])+'*('+antiSelCut+')','goff')
          sample['chain'].Draw(dPhiStr+'>>'+sample['name']+'_Selection',str(sample['weight'])+'*('+SelCut+')','goff')
          
          if sample['merge']=='QCD':
            histos['merged_QCD']['antiSelection'].Add(histos[sample['name']]['antiSelection'])
            histos['merged_QCD']['Selection'].Add(histos[sample['name']]['Selection'])
        
          elif sample['merge']=='EWK':
            histos['merged_EWK']['antiSelection'].Add(histos[sample['name']]['antiSelection'])
            histos['merged_EWK']['Selection'].Add(histos[sample['name']]['Selection'])

        nEWKSel_err = ROOT.Double()
        nEWKSel = histos['merged_EWK']['Selection'].IntegralAndError(0,histos['merged_EWK']['Selection'].GetNbinsX(),nEWKSel_err)
        nEWKAntiSel_err = ROOT.Double()
        nEWKAntiSel = histos['merged_EWK']['antiSelection'].IntegralAndError(0,histos['merged_EWK']['antiSelection'].GetNbinsX(),nEWKAntiSel_err)
        nQCDSel_err = ROOT.Double()
        nQCDSel =  histos['merged_QCD']['Selection'].IntegralAndError(0,histos['merged_QCD']['Selection'].GetNbinsX(),nQCDSel_err)
        nQCDAntiSel_err = ROOT.Double()
        nQCDAntiSel = histos['merged_QCD']['antiSelection'].IntegralAndError(0,histos['merged_QCD']['antiSelection'].GetNbinsX(),nQCDAntiSel_err)
        NdataSel = nEWKSel + nQCDSel
        NdataSel_err = sqrt(nEWKSel_err**2 + nQCDSel_err**2)
        NdataAntiSel =  nEWKAntiSel + nQCDAntiSel
        NdataAntiSel_err = sqrt(nEWKAntiSel_err**2 + nQCDAntiSel_err**2)

        #Event yields in low and high dPhi region
        nQCDSel_lowdPhi = histos['merged_QCD']['Selection'].GetBinContent(1)
        nQCDSel_lowdPhi_err = histos['merged_QCD']['Selection'].GetBinError(1)
        nQCDSel_highdPhi = histos['merged_QCD']['Selection'].GetBinContent(2)
        nQCDSel_highdPhi_err = histos['merged_QCD']['Selection'].GetBinError(2)
    

        rd = {
              'NdataSel':NdataSel, 'NdataSel_err':float(NdataSel_err),\
              'NdataAntiSel':NdataAntiSel, 'NdataAntiSel_err':float(NdataAntiSel_err),\
              'NEWKSelMC':nEWKSel, 'NEWKSelMC_err':float(nEWKSel_err),\
              'NEWKAntiSelMC':nEWKAntiSel, 'NEWKAntiSelMC_err':float(nEWKAntiSel_err),\
              'NQCDSelMC':nQCDSel, 'NQCDSelMC_err':float(nQCDSel_err),\
              'NQCDSelLowdPhi':nQCDSel_lowdPhi, 'NQCDSelLowdPhi_err':nQCDSel_lowdPhi_err,\
              'NQCDSelHighdPhi':nQCDSel_highdPhi, 'NQCDSelHighdPhi_err':nQCDSel_highdPhi_err,\
              'NQCDAntiSelMC':nQCDAntiSel, 'NQCDAntiSelMC_err':float(nQCDAntiSel_err)}        

        if histos['merged_QCD']['Selection'].GetBinContent(1)>0 and histos['merged_QCD']['Selection'].GetBinContent(2)>0:
          RcsQCDsel = histos['merged_QCD']['Selection'].GetBinContent(2)/histos['merged_QCD']['Selection'].GetBinContent(1)
          RcsQCDselErr_sim = RcsQCDsel*sqrt((histos['merged_QCD']['Selection'].GetBinError(1)**2/histos['merged_QCD']['Selection'].GetBinContent(1)**2)\
                                         + (histos['merged_QCD']['Selection'].GetBinError(2)**2/histos['merged_QCD']['Selection'].GetBinContent(2)**2) ) 
          RcsQCDselErr_pred = RcsQCDsel*sqrt((1./histos['merged_QCD']['Selection'].GetBinContent(1)) + (1./histos['merged_QCD']['Selection'].GetBinContent(2))) 
        else:
          RcsQCDsel = float('nan')
          RcsQCDselErr_sim = float('nan')
          RcsQCDselErr_pred = float('nan')

        if histos['merged_EWK']['Selection'].GetBinContent(1)>0 and histos['merged_EWK']['Selection'].GetBinContent(2)>0:
          RcsEWKsel = histos['merged_EWK']['Selection'].GetBinContent(2)/histos['merged_EWK']['Selection'].GetBinContent(1)
          RcsEWKselErr_sim = RcsEWKsel*sqrt((histos['merged_EWK']['Selection'].GetBinError(1)**2/histos['merged_EWK']['Selection'].GetBinContent(1)**2)\
                                         + (histos['merged_EWK']['Selection'].GetBinError(2)**2/histos['merged_EWK']['Selection'].GetBinContent(2)**2) ) 
          RcsEWKselErr_pred = RcsEWKsel*sqrt((1./histos['merged_EWK']['Selection'].GetBinContent(1)) + (1./histos['merged_EWK']['Selection'].GetBinContent(2))) 
        else:
          RcsEWKsel = float('nan')
          RcsEWKselErr_sim = float('nan')
          RcsEWKselErr_pred = float('nan')

        if (histos['merged_QCD']['antiSelection'].GetBinContent(1) + histos['merged_EWK']['antiSelection'].GetBinContent(1))>0 and\
           (histos['merged_QCD']['antiSelection'].GetBinContent(2) + histos['merged_EWK']['antiSelection'].GetBinContent(2))>0:
          RcsQCDantisel = (histos['merged_QCD']['antiSelection'].GetBinContent(2)+histos['merged_EWK']['antiSelection'].GetBinContent(2))/\
                          (histos['merged_QCD']['antiSelection'].GetBinContent(1)+histos['merged_EWK']['antiSelection'].GetBinContent(1))
          RcsQCDantiselErr_sim = RcsQCDantisel*sqrt((histos['merged_QCD']['antiSelection'].GetBinError(1)**2+histos['merged_EWK']['antiSelection'].GetBinError(1)**2)/(histos['merged_QCD']['antiSelection'].GetBinContent(1)+histos['merged_EWK']['antiSelection'].GetBinContent(1))**2\
                                                    +(histos['merged_QCD']['antiSelection'].GetBinError(2)**2+histos['merged_EWK']['antiSelection'].GetBinError(2)**2)/(histos['merged_QCD']['antiSelection'].GetBinContent(2)+histos['merged_EWK']['antiSelection'].GetBinContent(2))**2)
          RcsQCDantiselErr_pred = RcsQCDantisel*sqrt(1./(histos['merged_QCD']['antiSelection'].GetBinContent(1)+histos['merged_EWK']['antiSelection'].GetBinContent(1))\
                                                   + 1./(histos['merged_QCD']['antiSelection'].GetBinContent(2)+histos['merged_EWK']['antiSelection'].GetBinContent(2)))
        else:
          RcsQCDantisel = float('nan')
          RcsQCDantiselErr_sim = float('nan')
          RcsQCDantiselErr_pred = float('nan')

        if (histos['merged_QCD']['Selection'].GetBinContent(1) + histos['merged_EWK']['Selection'].GetBinContent(1))>0 and\
           (histos['merged_QCD']['Selection'].GetBinContent(2) + histos['merged_EWK']['Selection'].GetBinContent(2))>0:
          RcsSel = (histos['merged_QCD']['Selection'].GetBinContent(2)+histos['merged_EWK']['Selection'].GetBinContent(2))/\
                   (histos['merged_QCD']['Selection'].GetBinContent(1)+histos['merged_EWK']['Selection'].GetBinContent(1))
          RcsSelErr_sim = RcsSel*sqrt((histos['merged_QCD']['Selection'].GetBinError(1)**2+histos['merged_EWK']['Selection'].GetBinError(1)**2)/(histos['merged_QCD']['Selection'].GetBinContent(1)+histos['merged_EWK']['Selection'].GetBinContent(1))**2\
                                             +(histos['merged_QCD']['Selection'].GetBinError(2)**2+histos['merged_EWK']['Selection'].GetBinError(2)**2)/(histos['merged_QCD']['Selection'].GetBinContent(2)+histos['merged_EWK']['Selection'].GetBinContent(2))**2)
          RcsSelErr_pred = RcsSel*sqrt(1./(histos['merged_QCD']['Selection'].GetBinContent(1)+histos['merged_EWK']['Selection'].GetBinContent(1))\
                                            + 1./(histos['merged_QCD']['Selection'].GetBinContent(2)+histos['merged_EWK']['Selection'].GetBinContent(2)))
        else:
          RcsSel = float('nan')
          RcsSelErr_sim = float('nan')
          RcsSelErr_pred = float('nan')

        rd.update({'RcsQCDsel':RcsQCDsel,         'RcsQCDselErr_sim':RcsQCDselErr_sim,         'RcsQCDselErr_pred':RcsQCDselErr_pred,\
                   'RcsEWKsel':RcsEWKsel,         'RcsEWKselErr_sim':RcsEWKselErr_sim,         'RcsEWKselErr_pred':RcsEWKselErr_pred,\
                   'RcsSel':RcsSel,               'RcsSelErr_sim':RcsSelErr_sim,               'RcsSelErr_pred':RcsSelErr_pred,\
                   'RcsQCDantisel':RcsQCDantisel, 'RcsQCDantiselErr_sim':RcsQCDantiselErr_sim, 'RcsQCDantiselErr_pred':RcsQCDantiselErr_pred})

        bins[njb][stb][htb][btb] = rd
        print rd

path = '/data/'+username+'/results2015/rCS_0b/'
if not os.path.exists(path):
  os.makedirs(path)
pickle.dump(bins, file(path+'RcsQCD_'+str(target_lumi/1000)+'fb-1_pkl','w'))

