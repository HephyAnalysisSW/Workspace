import ROOT
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
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns import *
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_fromArtur import *
#from Workspace.RA4Analysis.cmgTuples_Data25ns_0l import *
from Workspace.RA4Analysis.cmgTuples_data_25ns_fromArtur import *
from draw_helpers import *
from math import *
from Workspace.HEPHYPythonTools.user import username
from LpTemplateFit import LpTemplateFit

preprefix = 'QCDestimation/TupelsFromArtur/CB_ID'
wwwDir = '/afs/hephy.at/user/d/dhandl/www/RunII/Spring15_25ns/'+preprefix+'/'
picklePath = '/data/'+username+'/results2015/QCDEstimation/'
presel = 'Lp_singleElectronic_'
picklePresel = '20151102_QCDestimation_reducedSR_pkl'

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

signalRegion = {(3, 4): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}, #3-4jets QCD and W+jets control region
                                      (500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (350, 450): {(500, -1):   {'deltaPhi': 1.0},
                                      (500, -1):   {'deltaPhi': 0.75},
                                      (500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (450, -1):  {(500, -1):   {'deltaPhi': 1.0},
                                      (500, -1):   {'deltaPhi': 0.75},
                                      (500, 1000): {'deltaPhi': 0.75},
                                      (1000, -1):  {'deltaPhi': 0.75}}},
                (4, 5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}, #4-5jets TTbar control region
                                      (500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (350, 450): {(500, -1):   {'deltaPhi': 1.0},
                                      (500, -1):   {'deltaPhi': 0.75},
                                      (500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (450, -1):  {(500, -1):   {'deltaPhi': 1.0},
                                      (500, -1):   {'deltaPhi': 0.75},
                                      (500, 1000): {'deltaPhi': 0.75},
                                      (1000, -1):  {'deltaPhi': 0.75}}},
                (5, 5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}},  #signal regions
                         (350, 450): {(500, -1):   {'deltaPhi': 1.0}},
                         (450, -1):  {(500, -1):   {'deltaPhi': 1.0}}},
                (6, 7): {(250, 350): {(500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (350, 450): {(500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                          (450, -1): {(500, 1000): {'deltaPhi': 0.75},
                                      (1000, -1):  {'deltaPhi': 0.75}}},
                (8, -1): {(250, 350):{(500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                          (350, 450):{(500, -1):   {'deltaPhi': 0.75}},
                          (450, -1): {(500, -1):   {'deltaPhi': 0.75}}}
}

#signalRegion = {(3, 4): {(250, -1): {(500, -1):   {'deltaPhi': 0.5}}}, #QCD CR
#                (4, 5): {(250, -1): {(500, -1):   {'deltaPhi': 0.5}}}, #TTbar CR 1b 
#                (5, 5): {(250, -1): {(500, -1):   {'deltaPhi': 0.5}}}, #SR 
#                (6,-1): {(250, -1): {(500, -1):   {'deltaPhi': 0.5}}}} #SR 
btreg = [(0,0), (1,1), (2,2)] #1b and 2b estimates are needed for the btag fit

#small = True
small = False
doFit = True
#doFit = False

eleVarList = ['pt', 'eta', 'phi', 'pdgId', 'miniRelIso', 'convVeto', 'sip3d', 'mvaIdPhys14', 'charge', 'lostHits']
eleFromW = ['pt', 'eta', 'phi', 'pdgId', 'motherId', 'grandmotherId', 'charge', 'sourceId']

def getMatch(genLep,recoLep):
  return ( (genLep['charge']==recoLep['charge']) and deltaR(genLep,recoLep)<0.1 and (abs(genLep['pt']-recoLep['pt'])/genLep['pt'])<0.5)

targetLumi = 1260 #pb-1
def getWeight(nEvents,targetLumi,sample=''):
#  weight = xsec[sample['dbsName']] * targetLumi/nEvents
  weight = targetLumi/nEvents
  return weight

def getRCS(c, cut, dPhiCut, useWeight = False):
  dPhiStr = 'acos((LepGood_pt+met_pt*cos(LepGood_phi-met_phi))/sqrt(LepGood_pt**2+met_pt**2+2*met_pt*LepGood_pt*cos(LepGood_phi-met_phi)))'
  if useWeight:
    h = getPlotFromChain(c, dPhiStr, [0,dPhiCut,pi], cutString=cut, binningIsExplicit=True)
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
trigger = "&&(HLT_EleHT350||HLT_MuHT350)"
filters = "&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter_fix&&Flag_HBHENoiseIsoFilter&&Flag_goodVertices&&Flag_eeBadScFilter"

#e_tight       = "(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&abs(LepGood_eta)<=2.5&&LepGood_miniRelIso<0.1&&LepGood_SPRING15_25ns_v1==4)" 
#n_tight_e =  "(Sum$("+e_tight+"))"
#e_veto = "(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&abs(LepGood_eta)<=2.5&&!("+e_tight+"))"
#n_veto_e ="(Sum$("+e_veto+"))"

###OneLep = "("+mu_tight+"+"+e_tight+"==1"+")"
#OneLep = "("+n_tight_mu+"+"+n_tight_e+"==1)" 
#OneMu = "("+n_tight_mu+"==1"+")"
#OneMu_lepveto = "("+n_veto_mu+"==0&&"+n_veto_e+"==0&&"+n_tight_e+"==0"+")"
#OneE = "("+n_tight_e+"==1"+")"
#OneE_lepveto = "("+n_veto_e+"==0&&"+n_veto_mu+"==0&&"+n_tight_mu+"==0"+")"
#lep_hard  = "LepGood_pt[0]>25"
#OneLep_lepveto = "("+e_veto+"==0&&"+mu_veto+"==0)"

#singleElectronVeto = '((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=5)==0)&&'\
#                     +'(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&LepGood_miniRelIso<0.4&&((abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>(-0.16))'\
#                     +'||((abs(LepGood_eta)>0.8&&abs(LepGood_eta)<1.479)&&LepGood_mvaIdPhys14>(-0.65))'\
#                     +'||((abs(LepGood_eta)>1.479&&abs(LepGood_eta)<2.5)&&LepGood_mvaIdPhys14>(-0.74)))&&LepGood_lostHits<=1&&LepGood_convVeto&&LepGood_sip3d<4.0)==1))'
#
#singleElectronVetoAnti = '((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=5)==0)&&'\
#                         +'(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&LepGood_miniRelIso<0.4&&((abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>(-0.16))'\
#                         +'||((abs(LepGood_eta)>0.8&&abs(LepGood_eta)<1.479)&&LepGood_mvaIdPhys14>(-0.65))'\
#                         +'||((abs(LepGood_eta)>1.479&&abs(LepGood_eta)<2.5)&&LepGood_mvaIdPhys14>(-0.74))))==1))'
#
#antiSelStr = '((abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>=(-0.16)&&LepGood_mvaIdPhys14<0.87)||'\
#             +'(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)>=0.8&&abs(LepGood_eta)<1.479&&LepGood_mvaIdPhys14>=(-0.65)&&LepGood_mvaIdPhys14<0.60)||'\
#             +'(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)>=1.479&&abs(LepGood_eta)<2.5&&LepGood_mvaIdPhys14>=(-0.74)&&LepGood_mvaIdPhys14<0.17))'
#
#SelStr = '((abs(LepGood_pdgId)==11&&LepGood_pt>=25&&LepGood_miniRelIso<0.1&&LepGood_convVeto&&LepGood_sip3d<4.0&&LepGood_lostHits<=0&&abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>=0.87)||'\
#         +'(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&LepGood_miniRelIso<0.1&&LepGood_convVeto&&LepGood_sip3d<4.0&&LepGood_lostHits<=0&&abs(LepGood_eta)>=0.8&&abs(LepGood_eta)<1.479&&LepGood_mvaIdPhys14>=0.60)||'\
#         +'(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&LepGood_miniRelIso<0.1&&LepGood_convVeto&&LepGood_sip3d<4.0&&LepGood_lostHits<=0&&abs(LepGood_eta)>=1.479&&abs(LepGood_eta)<2.5&&LepGood_mvaIdPhys14>=0.17))'

antiSelStr = '(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&abs(LepGood_eta)<=2.5&&LepGood_SPRING15_25ns_v1>=1&&LepGood_SPRING15_25ns_v1<3)'

SelStr = '(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&LepGood_miniRelIso<0.1&&abs(LepGood_eta)<=2.5&&LepGood_SPRING15_25ns_v1>=4)'

singleElectronVeto = '((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=10)==0)&&(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&abs(LepGood_eta)<=2.5&&!('+SelStr+'))==0))'

singleElectronVetoAnti = '((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=10)==0)&&(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&abs(LepGood_eta)<=2.5&&!('+antiSelStr+'))==0))'

singleHardElectron = '((Sum$('+antiSelStr+'||'+SelStr+')==1)&&LepGood_pt[0]>=25)'

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
  
  Lp = ((e['pt']/sqrt(['pt']**2+met**2+2*met*e['pt']*cos(e['phi']-metPhi)))\
       * ((e['pt']+met*cos(e['phi']-metPhi))/sqrt(e['pt']**2+met**2+2*met*e['pt']*cos(e['phi']-metPhi))))
  return Lp

#attention only use this string after singleElectronic (sel/antiSel) preselection
LpStr = '((LepGood_pt[0]/sqrt(LepGood_pt[0]**2+met_pt**2+2*met_pt*LepGood_pt[0]*cos(LepGood_phi[0]-met_phi)))'\
      +'*((LepGood_pt[0]+met_pt*cos(LepGood_phi[0]-met_phi))/sqrt(LepGood_pt[0]**2+met_pt**2+2*met_pt*LepGood_pt[0]*cos(LepGood_phi[0]-met_phi))))'

dPhiStr = 'acos((LepGood_pt[0]+met_pt*cos(LepGood_phi[0]-met_phi))/sqrt(LepGood_pt[0]**2+met_pt**2+2*met_pt*LepGood_pt[0]*cos(LepGood_phi[0]-met_phi)))'

Bkg = [
       #{'name':'QCD_HT100to200_25ns', 'sample':QCD_HT100to200_25ns, 'legendName':'QCD HT100-200', 'color':ROOT.kCyan+3, 'merge':'QCD'},
       {'name':'QCD_HT200to300_25ns', 'sample':QCD_HT200to300_25ns, 'legendName':'QCD HT200-300', 'color':ROOT.kCyan+3, 'merge':'QCD'},
       {'name':'QCD_HT300to500_25ns', 'sample':QCD_HT300to500_25ns, 'legendName':'QCD HT300-500', 'color':ROOT.kCyan, 'merge':'QCD'},
       {'name':'QCD_HT500to700_25ns', 'sample':QCD_HT500to700_25ns, 'legendName':'QCD HT500-700', 'color':ROOT.kCyan-3, 'merge':'QCD'},
       {'name':'QCD_HT700to1000_25ns', 'sample':QCD_HT700to1000_25ns, 'legendName':'QCD HT700-1000', 'color':ROOT.kCyan-3, 'merge':'QCD'},
       {'name':'QCD_HT1000to1500_25ns', 'sample':QCD_HT1000to1500_25ns, 'legendName':'QCD HT1000-1500', 'color':ROOT.kCyan-3, 'merge':'QCD'},
       {'name':'QCD_HT1500to2000_25ns', 'sample':QCD_HT1500to2000_25ns, 'legendName':'QCD HT1500-2000', 'color':ROOT.kCyan-3, 'merge':'QCD'},
       {'name':'QCD_HT2000toInf_25ns', 'sample':QCD_HT2000toInf_25ns, 'legendName':'QCD HT2000-Inf', 'color':ROOT.kCyan-7, 'merge':'QCD'},
       #{'name':'TBarToLeptons_sChannel_PU20bx25', 'sample':TBarToLeptons_sChannel_PU20bx25, 'legendName':'TBarToLep sCh', 'color':ROOT.kViolet, 'merge':'EWK'},
       #{'name':'TBarToLeptons_tChannel_PU20bx25', 'sample':TBarToLeptons_tChannel_PU20bx25, 'legendName':'TBarToLep tCh', 'color':ROOT.kViolet-3, 'merge':'EWK'},
       {'name':'TToLeptons_sch', 'sample':TToLeptons_sch, 'legendName':'TToLep sCh', 'color':ROOT.kViolet-5, 'merge':'EWK'},
       {'name':'TToLeptons_tch', 'sample':TToLeptons_tch, 'legendName':'TToLep tCh', 'color':ROOT.kViolet-7, 'merge':'EWK'},
       {'name':'T_tWch', 'sample':T_tWch, 'legendName':'TtW', 'color':ROOT.kViolet+1, 'merge':'EWK'},
       {'name':'TBar_tWch', 'sample':TBar_tWch, 'legendName':'TBartW', 'color':ROOT.kViolet+6, 'merge':'EWK'},
       {'name':'TTWJetsToLNu_25ns', 'sample':TTWJetsToLNu_25ns, 'legendName':'tt+W', 'color':ROOT.kOrange, 'merge':'EWK'},
       {'name':'TTWJetsToQQ_25ns', 'sample':TTWJetsToQQ_25ns, 'legendName':'tt+W', 'color':ROOT.kOrange+7, 'merge':'EWK'},
       {'name':'TTZToLLNuNu_25ns', 'sample':TTZToLLNuNu_25ns, 'legendName':'tt+Z', 'color':ROOT.kOrange+4, 'merge':'EWK'},
       {'name':'TTZToQQ_25ns', 'sample':TTZToQQ_25ns, 'legendName':'tt+Z', 'color':ROOT.kOrange+4, 'merge':'EWK'},
       #{'name':'WZ_25ns', 'sample':WZ_25ns, 'legendName':'WZ', 'color':ROOT.kOrange, 'merge':'EWK'},
       #{'name':'WWTo2L2Nu_25ns', 'sample':WWTo2L2Nu_25ns, 'legendName':'WW', 'color':ROOT.kOrange+7, 'merge':'EWK'},
       #{'name':'ZZ_25ns', 'sample':ZZ_25ns, 'legendName':'ZZ', 'color':ROOT.kOrange+4, 'merge':'EWK'},
       {'name':'DYJetsToLL_M_50_HT100to200_25ns', 'sample':DYJetsToLL_M_50_HT100to200_25ns, 'legendName':'DY HT100-200', 'color':ROOT.kRed, 'merge':'EWK'},
       {'name':'DYJetsToLL_M_50_HT200to400_25ns', 'sample':DYJetsToLL_M_50_HT200to400_25ns, 'legendName':'DY HT200-400', 'color':ROOT.kRed, 'merge':'EWK'},
       {'name':'DYJetsToLL_M_50_HT400to600_25ns', 'sample':DYJetsToLL_M_50_HT400to600_25ns, 'legendName':'DY HT400-600', 'color':ROOT.kRed, 'merge':'EWK'},
       {'name':'DYJetsToLL_M_50_HT600toInf_25ns', 'sample':DYJetsToLL_M_50_HT600toInf_25ns, 'legendName':'DY HT600-Inf', 'color':ROOT.kRed, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT100to200_25ns', 'sample':WJetsToLNu_HT100to200_25ns, 'legendName':'W HT100-200', 'color':ROOT.kGreen+3, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT200to400_25ns', 'sample':WJetsToLNu_HT200to400_25ns, 'legendName':'W HT200-400', 'color':ROOT.kGreen, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT400to600_25ns', 'sample':WJetsToLNu_HT400to600_25ns, 'legendName':'W HT400-600', 'color':ROOT.kGreen-3, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT600to800_25ns', 'sample':WJetsToLNu_HT600to800_25ns, 'legendName':'W HT600-800', 'color':ROOT.kGreen-7, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT800to1200_25ns', 'sample':WJetsToLNu_HT800to1200_25ns, 'legendName':'W HT800-1200', 'color':ROOT.kGreen-7, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT1200to2500_25ns', 'sample':WJetsToLNu_HT1200to2500_25ns, 'legendName':'W HT1200-2500', 'color':ROOT.kGreen-7, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT2500toInf_25ns', 'sample':WJetsToLNu_HT2500toInf_25ns, 'legendName':'W HT2500-Inf', 'color':ROOT.kGreen-7, 'merge':'EWK'},
       {'name':'TTJets_LO_25ns', 'sample':TTJets_LO_25ns, 'legendName':'t #bar{t}+Jets', 'color':ROOT.kRed, 'merge':'EWK', 'addCut':'&&lheHTIncoming<600'},
#       {'name':'TTJets_LO_HT600to800_25ns', 'sample':TTJets_LO_HT600to800_25ns, 'legendName':'t #bar{t}+Jets HT600-800', 'color':ROOT.kRed, 'merge':'EWK'},
#       {'name':'TTJets_LO_HT800to1200_25ns', 'sample':TTJets_LO_HT800to1200_25ns, 'legendName':'t #bar{t}+Jets HT800-1200', 'color':ROOT.kRed, 'merge':'EWK'},
#       {'name':'TTJets_LO_HT1200to2500_25ns', 'sample':TTJets_LO_HT1200to2500_25ns, 'legendName':'t #bar{t}+Jets HT1200-2500', 'color':ROOT.kRed, 'merge':'EWK'},
#       {'name':'TTJets_LO_HT2500toInf_25ns', 'sample':TTJets_LO_HT2500toInf_25ns, 'legendName':'t #bar{t}+Jets HT2500-Inf', 'color':ROOT.kRed, 'merge':'EWK'}
]

Data = [{'name':'SingleElectron_Run2015D_v4', 'sample':SingleElectron_Run2015D_v4, 'LegendName':'Data', 'merge':'Data'},
        {'name':'SingleElectron_Run2015D', 'sample':SingleElectron_Run2015D_05Oct, 'LegendName':'Data', 'merge':'Data'}
        #{'name':'SingleMuon_Run2015D', 'sample':SingleMuon_Run2015D_v4, 'LegendName':'Data', 'merge':'Data'}
        #{'name':'JetHT_Run2015D', 'sample':JetHT_Run2015D_v4, 'LegendName':'Data', 'merge':'Data'}
]

maxN=2 if small else -1

for sample in Bkg:
  sample['chunks'], sample['norm'] = getChunks(sample['sample'], maxN=maxN)
  sample['chain'] = ROOT.TChain('tree')
  for chunk in sample['chunks']:
    sample['chain'].Add(chunk['file'])

  sample['weight'] = getWeight(sample['norm'], targetLumi)

dataChain = ROOT.TChain('tree')
for sample in Data:
  sample['chunks'], sample['norm'] = getChunks(sample['sample'], maxN=maxN)
  for chunk in sample['chunks']:
    dataChain.Add(chunk['file'])

histos = {}
bins = {}
for srNJet in signalRegion:
  bins[srNJet] = {}
  for stb in signalRegion[srNJet]:
    bins[srNJet][stb] = {}
    for htb in signalRegion[srNJet][stb]:
      bins[srNJet][stb][htb] = {}
      for btb in btreg:
        deltaPhiCut = signalRegion[srNJet][stb][htb]['deltaPhi']

        print 'Binning => Ht: ',htb,'Lt: ',stb,'NJet: ',srNJet
        SRname = nameAndCut(stb, htb, srNJet, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]#use this function only for the name string!!!
        #cut only includes very loose lepton selection, HT cut, NJet cut, Btagging and subleading JetPt>=80!!! St cut applied in the Event Loop!!!
#        cut = '(Sum$(abs(LepGood_pdgId)==11&&abs(LepGood_dxy)<=0.05&&abs(LepGood_dz)<=0.1)+Sum$(abs(LepOther_pdgId)==11&&abs(LepOther_dxy)<=0.05&&abs(LepOther_dz)<=0.1)>=1)&&'+htCut(htb, minPt=30, maxEta=2.4, njCorr=0.)+'&&'+ nBTagCut(btb, minPt=30, maxEta=2.4, minCSVTag=0.814)+'&&'+nJetCut(srNJet, minPt=30, maxEta=2.4)+'&&'+nJetCut(2, minPt=80, maxEta=2.4)
        SelCut = '('+singleElectronVeto+'&&'+singleHardElectron+'&&(Sum$('+SelStr+')==1)&&'+stCutQCD(stb)+'&&'+htCut(htb, minPt=30, maxEta=2.4, njCorr=0.)+'&&'+ nBTagCut(btb, minPt=30, maxEta=2.4, minCSVTag=0.890)\
                 +'&&'+nJetCut(srNJet, minPt=30, maxEta=2.4)+'&&'+nJetCut(2, minPt=80, maxEta=2.4)+')'
        antiSelCut = '('+singleElectronVetoAnti+'&&'+singleHardElectron+'&&(Sum$('+antiSelStr+')==1)&&'+stCutQCD(stb)+'&&'+htCut(htb, minPt=30, maxEta=2.4, njCorr=0.)+'&&'+ nBTagCut(btb, minPt=30, maxEta=2.4, minCSVTag=0.890)\
                     +'&&'+nJetCut(srNJet, minPt=30, maxEta=2.4)+'&&'+nJetCut(2, minPt=80, maxEta=2.4)+')'


        histos['merged_QCD']={}
        histos['merged_EWK']={}
        histos['merged_DATA']={}
        histos['merged_QCD']['antiSelection']=ROOT.TH1F('merged_QCD_antiSelection','merged_QCD_antiSelection',30,-0.5,2.5)
        histos['merged_QCD']['Selection']=ROOT.TH1F('merged_QCD_Selection','merged_QCD_Selection',30,-0.5,2.5)
        histos['merged_EWK']['antiSelection']=ROOT.TH1F('merged_EWK_antiSelection','merged_EWK_antiSelection',30,-0.5,2.5)
        histos['merged_EWK']['Selection']=ROOT.TH1F('merged_EWK_Selection','merged_EWK_Selection',30,-0.5,2.5)
        histos['merged_DATA']['antiSelection']=ROOT.TH1F('merged_DATA_antiSelection','merged_DATA_antiSelection',30,-0.5,2.5)
        histos['merged_DATA']['Selection']=ROOT.TH1F('merged_DATA_Selection','merged_DATA_Selection',30,-0.5,2.5)

#        canv = ROOT.TCanvas('canv','canv')
#        canv.SetLogy()
#        l = ROOT.TLegend(0.7,0.75,0.98,0.95)
#        l.SetFillColor(0)
#        l.SetBorderSize(1)
#        l.SetShadowColor(ROOT.kWhite)
        
        text = ROOT.TLatex()
        text.SetNDC()
        text.SetTextSize(0.045)
        text.SetTextAlign(11)
        
        first = True
        antiMax=0
        selMax=0
       
        for sample in Bkg:
          histos[sample['name']] = {}
          histos[sample['name']]['antiSelection'] = ROOT.TH1F(sample['name']+'_antiSelection', sample['name']+'_antiSelection',30,-0.5,2.5)
          histos[sample['name']]['Selection'] = ROOT.TH1F(sample['name']+'_Selection', sample['name']+'_Selection',30,-0.5,2.5)

#          if sample.has_key('addCut'):
#            SelCut = '('+SelCut+sample['addCut']+')'
#            antiSelCut = '('+antiSelCut+sample['addCut']+')'
#          if sample['chain'].GetLeaf('nLepGood').GetValue()>1: 
#            print 'ATTENTION: this should not have happened!'
#            run = sample['chain'].GetLeaf('run').GetValue()
#            evt = sample['chain'].GetLeaf('evt').GetValue()
#            lumi = sample['chain'].GetLeaf('lumi').GetValue()
#            print sample['name'], run, lumi, evt

          sample['chain'].Draw(LpStr+'>>'+sample['name']+'_antiSelection','('+str(sample['weight'])+')*xsec*(genWeight)*('+antiSelCut+')')
          sample['chain'].Draw(LpStr+'>>'+sample['name']+'_Selection','('+str(sample['weight'])+')*xsec*(genWeight)*('+SelCut+')')

          histos[sample['name']]['antiSelection'].SetLineColor(sample['color'])
          histos[sample['name']]['antiSelection'].SetLineStyle(ROOT.kDashed)
          histos[sample['name']]['antiSelection'].SetLineWidth(2)
          histos[sample['name']]['antiSelection'].GetYaxis().SetTitle('# of Events')
          histos[sample['name']]['antiSelection'].GetXaxis().SetTitle('L_{p}')
          histos[sample['name']]['Selection'].SetLineColor(sample['color'])
          histos[sample['name']]['Selection'].SetLineWidth(2)
          histos[sample['name']]['Selection'].GetYaxis().SetTitle('# of Events')
          histos[sample['name']]['Selection'].GetXaxis().SetTitle('L_{P}')
#          l.AddEntry(histos[sample['name']]['antiSelection'], sample['legendName']+' anti-selected')
#          l.AddEntry(histos[sample['name']]['Selection'], sample['legendName']+' selected')
        
          if sample['merge']=='QCD':
#            histos[sample['name']]['normTemplate'] = ROOT.TH1F(sample['name']+'_normTemplate',sample['name']+'_normTemplate',30,-0.5,2.5)
            #normalized Template used for 'Pseudo-data': same as selected collection except an inclusive ST bin 
#            normCut = singleElectronVeto+'&&'+singleHardElectron+'&&(Sum$('+SelStr+')==1)&&'+stCutQCD((200,-1))+'&&'+htCut(htb, minPt=30, maxEta=2.4, njCorr=0.)+'&&'+ nBTagCut(btb, minPt=30, maxEta=2.4, minCSVTag=0.814)\
#                 +'&&'+nJetCut(srNJet, minPt=30, maxEta=2.4)+'&&'+nJetCut(2, minPt=80, maxEta=2.4)
#           sample['chain'].Draw(LpStr+'>>'+sample['name']+'_normTemplate',str(sample['weight'])+'*('+normCut+')')
            histos['merged_QCD']['antiSelection'].Add(histos[sample['name']]['antiSelection'])
            histos['merged_QCD']['Selection'].Add(histos[sample['name']]['Selection'])
#            histos['normTemplate_QCD']['Selection'].Add(histos[sample['name']]['normTemplate'])        

          elif sample['merge']=='EWK':
            histos['merged_EWK']['antiSelection'].Add(histos[sample['name']]['antiSelection'])
            histos['merged_EWK']['Selection'].Add(histos[sample['name']]['Selection'])
       
#          if first:
#            histos[sample['name']]['antiSelection'].Draw('hist')
#            histos[sample['name']]['Selection'].Draw('hist same')
#            first = False
#          else:
#            histos[sample['name']]['antiSelection'].Draw('hist same')
#            histos[sample['name']]['Selection'].Draw('hist same')
        
#          if histos[sample['name']]['antiSelection'].GetMaximum() > antiMax:
#            antiMax = histos[sample['name']]['antiSelection'].GetMaximum()
#          if histos[sample['name']]['Selection'].GetMaximum() > selMax:
#            selMax = histos[sample['name']]['Selection'].GetMaximum()

#        for sample in Bkg:
#          histos[sample['name']]['antiSelection'].SetMaximum(1.5*antiMax)
#          histos[sample['name']]['antiSelection'].SetMinimum(0)
#          histos[sample['name']]['Selection'].SetMaximum(1.5*selMax)
#          histos[sample['name']]['Selection'].SetMinimum(0)

#        l.Draw() 
#        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
#        text.DrawLatex(0.6,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")
 
#        canv.cd()
#        canv.Print(wwwDir+presel+SRname+'_subBkg.png')
#        canv.Print(wwwDir+presel+SRname+'_subBkg.root')
#        canv.Print(wwwDir+presel+SRname+'_subBkg.pdf')

        mergeCanv = ROOT.TCanvas('merged Canv','merged Canv')
        #mergeCanv.SetLogy()
        leg = ROOT.TLegend(0.7,0.75,0.98,0.95)
        leg.SetFillColor(0)
        leg.SetBorderSize(1)
        leg.SetShadowColor(ROOT.kWhite)

        dataChain.Draw(LpStr+'>>merged_DATA_antiSelection','('+antiSelCut+trigger+filters+')')
        dataChain.Draw(LpStr+'>>merged_DATA_Selection','('+SelCut+trigger+filters+')')

        rCSanti = getRCS(dataChain, antiSelCut, deltaPhiCut)
        rCSsel = getRCS(dataChain, SelCut, deltaPhiCut)

        for hist in [histos['merged_DATA']['antiSelection'],histos['merged_DATA']['Selection']]:
          hist.SetStats(0)
          hist.GetYaxis().SetTitle('# of Events')
          hist.GetXaxis().SetTitle('L_{p}')
          hist.SetLineColor(ROOT.kBlack)
          hist.SetLineStyle(1)
          hist.SetLineWidth(1)

        for hist in [histos['merged_QCD']['antiSelection'],histos['merged_QCD']['Selection'],histos['merged_EWK']['antiSelection'],histos['merged_EWK']['Selection']]:
          hist.SetStats(0)
          hist.GetYaxis().SetTitle('# of Events')
          hist.GetXaxis().SetTitle('L_{p}')
          hist.SetLineWidth(2)
          hist.SetMarkerStyle(1)

        nEWKSel_err = ROOT.Double()
        nEWKSel = histos['merged_EWK']['Selection'].IntegralAndError(0,histos['merged_EWK']['Selection'].GetNbinsX(),nEWKSel_err)
        nEWKAntiSel_err = ROOT.Double()
        nEWKAntiSel = histos['merged_EWK']['antiSelection'].IntegralAndError(0,histos['merged_EWK']['antiSelection'].GetNbinsX(),nEWKAntiSel_err)
        nQCDSel_err = ROOT.Double()
        nQCDSel =  histos['merged_QCD']['Selection'].IntegralAndError(0,histos['merged_QCD']['Selection'].GetNbinsX(),nQCDSel_err) 
        nQCDAntiSel_err = ROOT.Double()
        nQCDAntiSel = histos['merged_QCD']['antiSelection'].IntegralAndError(0,histos['merged_QCD']['antiSelection'].GetNbinsX(),nQCDAntiSel_err)
        nDATASel_err = ROOT.Double()
        nDATASel = histos['merged_DATA']['Selection'].IntegralAndError(0,histos['merged_DATA']['Selection'].GetNbinsX(),nDATASel_err)
        nDATAAntiSel_err = ROOT.Double()
        nDATAAntiSel = histos['merged_DATA']['antiSelection'].IntegralAndError(0,histos['merged_DATA']['antiSelection'].GetNbinsX(),nDATAAntiSel_err)

        bins[srNJet][stb][htb][btb] = {'NDATASel':nDATASel, 'NDATASel_err':float(nDATASel_err),\
                                       'NDATAAntiSel':nDATAAntiSel, 'NDATAAntiSel_err':float(nDATAAntiSel_err),\
                                       'NEWKSelMC':nEWKSel, 'NEWKSelMC_err':float(nEWKSel_err),\
                                       'NEWKAntiSelMC':nEWKAntiSel, 'NEWKAntiSelMC_err':float(nEWKAntiSel_err),\
                                       'NQCDSelMC':nQCDSel, 'NQCDSelMC_err':float(nQCDSel_err),\
                                       'NQCDAntiSelMC':nQCDAntiSel, 'NQCDAntiSelMC_err':float(nQCDAntiSel_err),\
                                       'deltaPhiCut':deltaPhiCut, 'rCSselectedDATA':rCSsel, 'rCSantiSelectedDATA':rCSanti}
#        print bins[srNJet][stb][htb][btb]

        mergeCanv.cd()
#        if histos['merged_QCD']['antiSelection'].Integral()>0:
#          histos['merged_QCD']['antiSelection'].Scale(1./histos['merged_QCD']['antiSelection'].Integral())
        histos['merged_QCD']['antiSelection'].SetLineColor(ROOT.kRed)
        histos['merged_QCD']['antiSelection'].SetLineStyle(ROOT.kDashed)
        leg.AddEntry(histos['merged_QCD']['antiSelection'],'QCD anti-selected','l')
 
#        if histos['merged_QCD']['Selection'].Integral()>0:
#          histos['merged_QCD']['Selection'].Scale(1./histos['merged_QCD']['Selection'].Integral())      
        histos['merged_QCD']['Selection'].SetLineColor(ROOT.kRed)
        leg.AddEntry(histos['merged_QCD']['Selection'],'QCD selected','l')
 
#        if histos['merged_EWK']['antiSelection'].Integral()>0:
#          histos['merged_EWK']['antiSelection'].Scale(1./histos['merged_EWK']['antiSelection'].Integral())       
        histos['merged_EWK']['antiSelection'].SetLineColor(ROOT.kBlack)
        histos['merged_EWK']['antiSelection'].SetLineStyle(ROOT.kDashed)
        leg.AddEntry(histos['merged_EWK']['antiSelection'],'EWK anti-selected','l')
 
#        if histos['merged_EWK']['Selection'].Integral()>0:
#          histos['merged_EWK']['Selection'].Scale(1./histos['merged_EWK']['Selection'].Integral())             
        histos['merged_EWK']['Selection'].SetLineColor(ROOT.kBlack)
        leg.AddEntry(histos['merged_EWK']['Selection'],'EWK selected','l')

        histos['merged_DATA']['antiSelection'].SetMarkerStyle(24)
        histos['merged_DATA']['Selection'].SetMarkerStyle(20)
        leg.AddEntry(histos['merged_DATA']['antiSelection'],'Data anti-selected')
        leg.AddEntry(histos['merged_DATA']['Selection'],'Data selected') 
      
        histos['merged_QCD']['antiSelection'].Draw('hist e')
        histos['merged_QCD']['Selection'].Draw('hist same e')
        histos['merged_EWK']['antiSelection'].Draw('hist same e')
        histos['merged_EWK']['Selection'].Draw('hist same e')
        histos['merged_DATA']['antiSelection'].Draw('same ep')
        histos['merged_DATA']['Selection'].Draw('same ep')

        histos['merged_QCD']['antiSelection'].SetMaximum(1.5*histos['merged_QCD']['antiSelection'].GetMaximum())
        histos['merged_QCD']['Selection'].SetMaximum(1.5*histos['merged_QCD']['Selection'].GetMaximum())
        histos['merged_EWK']['antiSelection'].SetMaximum(1.5*histos['merged_EWK']['antiSelection'].GetMaximum())
        histos['merged_EWK']['Selection'].SetMaximum(1.5*histos['merged_EWK']['Selection'].GetMaximum())
        histos['merged_DATA']['antiSelection'].SetMaximum(1.5*histos['merged_DATA']['antiSelection'].GetMaximum())
        histos['merged_DATA']['Selection'].SetMaximum(1.5*histos['merged_DATA']['Selection'].GetMaximum())
          
        leg.Draw()
        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.6,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")

        mergeCanv.cd()
        mergeCanv.Print(wwwDir+presel+SRname+'.png')
        mergeCanv.Print(wwwDir+presel+SRname+'.root')
        mergeCanv.Print(wwwDir+presel+SRname+'.pdf')
        mergeCanv.Clear()

        #do the template fit:
        #Scale normTemplate to the nominal yield in in the corresponding binning
#        histos['normTemplate_QCD']['Selection'].Scale(1./histos['normTemplate_QCD'].Integral())
#        histos['normTemplate_QCD']['Selection'].Scale(histos['merged_QCD']['Selection'].Integral())

        if doFit:
          LpTemplates = {'DATAantiSel':histos['merged_DATA']['antiSelection'], 'DATAsel':histos['merged_DATA']['Selection'],\
                         'EWKantiSel':histos['merged_EWK']['antiSelection'], 'EWKsel':histos['merged_EWK']['Selection'],\
                         'QCDantiSel':histos['merged_QCD']['antiSelection'], 'QCDsel':histos['merged_QCD']['Selection']}
          fit_QCD = LpTemplateFit(LpTemplates, prefix=presel+SRname, printDir=wwwDir+'templateFit')
          bins[srNJet][stb][htb][btb].update(fit_QCD)
          try: F_ratio = fit_QCD['QCD']['yield']/nDATAAntiSel
          except ZeroDivisionError: F_ratio = float('nan')
          try: F_ratio_err = F_ratio*sqrt(fit_QCD['QCD']['yieldVar']/fit_QCD['QCD']['yield']**2 + nDATAAntiSel_err**2/nDATAAntiSel**2)
          except ZeroDivisionError: F_ratio_err = float('nan')
          bins[srNJet][stb][htb][btb].update({'F_seltoantisel':F_ratio, 'F_seltoantisel_err':F_ratio_err})

        ROOT.setTDRStyle()
        if not os.path.exists(picklePath):
          os.makedirs(picklePath)
        pickle.dump(bins, file(picklePath+picklePresel,'w'))

#derive N_QCD(dPhi<x) and N_QCD(dPhi>x)
for srNJet in signalRegion:
  for stb in signalRegion[srNJet]:
    for htb in signalRegion[srNJet][stb]:
      for btb in btreg:
        deltaPhiCut = signalRegion[srNJet][stb][htb]['deltaPhi']
        Fsta = bins[(3,4)][stb][htb][(0,0)]['F_seltoantisel']
        Fsta_err = bins[(3,4)][stb][htb][(0,0)]['F_seltoantisel_err']
        Nanti = bins[srNJet][stb][htb][btb]['NDATAAntiSel']
        Nanti_err = bins[srNJet][stb][htb][btb]['NDATAAntiSel_err']
        RcsAnti = bins[srNJet][stb][htb][btb]['rCSantiSelectedDATA']['rCS']
        RcsAnti_err = bins[srNJet][stb][htb][btb]['rCSantiSelectedDATA']['rCSE_pred']
        NQCD = Fsta * Nanti
        NQCD_err = sqrt(Fsta_err**2*Nanti**2+Nanti_err**2*Fsta**2)
        try: NQCD_lowDPhi = NQCD/(RcsAnti+1)
        except ZeroDivisionError: NQCD_lowDPhi = float('nan') 
        try: NQCD_lowDPhi_err = NQCD_lowDPhi*sqrt((NQCD_err/NQCD)**2 + (RcsAnti_err/(RcsAnti+1))**2)
        except ZeroDivisionError: NQCD_lowDPhi_err = float('nan')
        NQCD_highDPhi = NQCD - NQCD_lowDPhi
        NQCD_highDPhi_err = sqrt(RcsAnti_err**2*NQCD_lowDPhi**2 + RcsAnti**2*NQCD_lowDPhi_err**2)
        bins[srNJet][stb][htb][btb].update({'NQCDpred':NQCD, 'NQCDpred_err':NQCD_err, 'NQCDpred_lowdPhi':NQCD_lowDPhi, 'NQCDpred_lowdPhi_err':NQCD_lowDPhi_err, 'NQCDpred_highdPhi':NQCD_highDPhi, 'NQCDpred_highdPhi_err':NQCD_highDPhi_err})
        pickle.dump(bins, file(picklePath+picklePresel,'w'))

#          #Get the event list 'eList' which has all the events satisfying the cut
#          sample["chain"].Draw(">>eList",cut)
#          elist = ROOT.gDirectory.Get("eList")
#          number_events = elist.GetN()
#          print "Sample ",sample['name'],": Will loop over", number_events,"events"
#        
#          #Event Loop
#          for i in range(number_events):
#            if i%10000==0:
#              print "At %i of %i for sample %s"%(i,number_events,sample['name'])
#            sample['chain'].GetEntry(elist.GetEntry(i))
#        
#            eles = [getObjDict(sample['chain'], 'LepGood_', eleVarList, j) for j in range(int(sample['chain'].GetLeaf('nLepGood').GetValue()))]
##                 + [getObjDict(sample['chain'], 'LepOther_', eleVarList, j) for j in range(int(sample['chain'].GetLeaf('nLepOther').GetValue()))]
#        
#            genEle = [getObjDict(sample['chain'], 'genLep_', eleFromW, j) for j in range(int(sample['chain'].GetLeaf('ngenLep').GetValue()))] 
#        
#            met=sample['chain'].GetLeaf('met_pt').GetValue()
#            metPhi=sample['chain'].GetLeaf('met_phi').GetValue()
#        
#            eles = filter(lambda e:abs(e['pdgId'])==11, eles) 
#            eles = filter(lambda e:e['pt']>=25, eles) 
#            eles = filter(lambda e:e['miniRelIso']<0.4, eles) #require relIso
#            eles = filter(lambda e:abs(e['eta'])<2.4, eles) 
#        
#            eles = filter(lambda e:(e['pt']+met)>=stb[0], eles) 
#
#            if stb[1]>0:
#              eles = filter(lambda e:(e['pt']+met)<stb[1], eles)
#
#            for e in eles:
#              e["antiSel"] =  antiSel(e) 
#              e["sel"] =  sel(e) 
#
#            elesSelected = filter(lambda e:e['sel'],eles)
#            elesAntiSelected = filter(lambda e:e['antiSel'],eles)
#            nElesSelected = len(elesSelected)
#            nElesAntiSelected = len(elesAntiSelected)
#
#            if not nElesSelected+nElesAntiSelected==1:continue
#            #print "nElesSelected %i nElesAntiSelected %i"%(nElesSelected,nElesAntiSelected)
#            if nElesSelected==1:
#              recoEle = elesSelected[0]
#              isSelected = True 
#            else:
#              recoEle = elesAntiSelected[0]
#              isSelected = False 
#
#            #gen Electrons        
#            genEle = filter(lambda e:abs(e['pdgId'])==11, genEle)
#            genEle = filter(lambda e:e['pt']>=10, genEle)
#
##            if len(eles)>1:
##        #      print len(eles), len(genEle)
##              continue
#
#            if len(eles)==0:print "Should never happen"
# 
##            if sample.has_key('prompt'):
##              if sample['prompt']:
##                for reco in eles:
##                  hasMatch=False
##                  for gen in genEle:
##                    if getMatch(gen,reco):
##                      if reco["antiSel"]:
##                        antiVal = getLp(met,metPhi,reco) 
##                        histos[sample['name']]['antiSelection'].Fill(antiVal,sample['weight'])
##                      if sel(reco):
##                        selVal = getLp(met,metPhi,reco)
##                        histos[sample['name']]['Selection'].Fill(selVal,sample['weight'])
##                    hasMatch=True
##        #          if not hasMatch:
##        #            if antiSel(reco):
##        #              antiVal = getLp(sample['chain'],reco)
##        #              histos[sample['name']]['antiSelection'].Fill(antiVal,sample['weight'])
##        #            elif Sel(reco):
##        #              selVal = getLp(sample['chain'],reco)
##        #              histos[sample['name']]['Selection'].Fill(selVal,sample['weight'])  
##        
##            else:
#        #      print len(eles)
##            for reco in eles:
#            lp = getLp(met,metPhi,recoEle)
#            if isSelected:
#              histos[sample['name']]['Selection'].Fill(lp,sample['weight'])
#            else: 
#              histos[sample['name']]['antiSelection'].Fill(lp,sample['weight'])
#        
#          del elist 
        
        

