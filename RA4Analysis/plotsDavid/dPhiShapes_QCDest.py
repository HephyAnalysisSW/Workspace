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
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_fromArtur import *
from Workspace.RA4Analysis.cmgTuples_data_25ns_fromArtur import *
from draw_helpers import *
from math import *
from Workspace.HEPHYPythonTools.user import username
from LpTemplateFit import LpTemplateFit

preprefix = 'QCDestimation/newAntiID/hOverE/normalization/'
wwwDir = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/RunII/Spring15_25ns/'+preprefix+'/'
prefix = 'Lp_singleElectronic'
 
if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

signalRegion = {
#                (3, 4): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}, #3-4jets QCD and W+jets control region
#                                      (500, 750):  {'deltaPhi': 1.0},
#                                      (750, -1):   {'deltaPhi': 1.0}},
#                         (350, 450): {(500, -1):   {'deltaPhi': 1.0},
#                                      (500, -1):   {'deltaPhi': 0.75},
#                                      (500, 750):  {'deltaPhi': 1.0},
#                                      (750, -1):   {'deltaPhi': 1.0}},
#                         (450, -1):  {(500, -1):   {'deltaPhi': 1.0},
#                                      (500, -1):   {'deltaPhi': 0.75},
#                                      (500, 1000): {'deltaPhi': 0.75},
#                                      (1000, -1):  {'deltaPhi': 0.75}}},
#                (4, 5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}, #4-5jets TTbar control region
#                                      (500, 750):  {'deltaPhi': 1.0},
#                                      (750, -1):   {'deltaPhi': 1.0}},
#                         (350, 450): {(500, -1):   {'deltaPhi': 1.0},
#                                      (500, -1):   {'deltaPhi': 0.75},
#                                      (500, 750):  {'deltaPhi': 1.0},
#                                      (750, -1):   {'deltaPhi': 1.0}},
#                         (450, -1):  {(500, -1):   {'deltaPhi': 1.0},
#                                      (500, -1):   {'deltaPhi': 0.75},
#                                      (500, 1000): {'deltaPhi': 0.75},
#                                      (1000, -1):  {'deltaPhi': 0.75}}},
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
#signalRegion = {(3, 4): {(250, -1): {(500, -1):   {'deltaPhi': 0.5}}}} #QCD CR
#                (4, 5): {(250, -1): {(500, -1):   {'deltaPhi': 0.5}}}, #TTbar CR 1b 
#                (5, 5): {(250, -1): {(500, -1):   {'deltaPhi': 0.5}}}, #SR 
#                (6,-1): {(250, -1): {(500, -1):   {'deltaPhi': 0.5}}}} #SR 
btreg = [(0,0)] #1b and 2b estimates are needed for the btag fit

#small = True
small = False

def makeWeight(lumi=4., sampleLumi=3.,debug=False):
  if debug:
    print 'No lumi-reweighting done!!'
    return 'weight', 'weight*weight'
  else:
    weight_str = '(((weight)/'+str(sampleLumi)+')*'+str(lumi)+')'
    weight_err_str = '('+weight_str+'*'+weight_str+')'
    return weight_str, weight_err_str
lumi = 3.
sampleLumi = 1.55
debugReweighting = False
weight_str, weight_err_str = makeWeight(lumi, sampleLumi=sampleLumi, debug=debugReweighting)

def getRCS(c, cut, dPhiCut, useWeight = False, weight = 'weight'):
#  dPhiStr = 'acos((LepGood_pt+met_pt*cos(LepGood_phi-met_phi))/sqrt(LepGood_pt**2+met_pt**2+2*met_pt*LepGood_pt*cos(LepGood_phi-met_phi)))'
  dPhiStr = 'deltaPhi_Wl'
  if useWeight:
    h = getPlotFromChain(c, dPhiStr, [0,dPhiCut,pi], cutString=cut, binningIsExplicit=True, weight = weight)
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
  Lp = ((e['pt']/sqrt(['pt']**2+met**2+2*met*e['pt']*cos(e['phi']-metPhi)))\
       * ((e['pt']+met*cos(e['phi']-metPhi))/sqrt(e['pt']**2+met**2+2*met*e['pt']*cos(e['phi']-metPhi))))
  return Lp

antiSelStr = '(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&abs(LepGood_eta)<=2.5&&LepGood_SPRING15_25ns_v1>=1&&LepGood_SPRING15_25ns_v1<=3)'
SelStr = '(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&LepGood_miniRelIso<0.1&&abs(LepGood_eta)<=2.5&&LepGood_SPRING15_25ns_v1>=4)'
singleElectronVeto = '((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=10)==0)&&(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&abs(LepGood_eta)<=2.5&&!('+SelStr+'))==0))'
singleElectronVetoAnti = '((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=10)==0)&&(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&abs(LepGood_eta)<=2.5&&!('+antiSelStr+'))==0))'
singleHardElectron = '((Sum$('+antiSelStr+'||'+SelStr+')==1)&&LepGood_pt[0]>=25)'

filters = "&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter_fix&&Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter" #strange filter settings!!

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
#       {'name':'TToLeptons_sch', 'sample':TToLeptons_sch, 'legendName':'TToLep sCh', 'color':ROOT.kViolet-5, 'merge':'EWK'},
#       {'name':'TToLeptons_tch', 'sample':TToLeptons_tch, 'legendName':'TToLep tCh', 'color':ROOT.kViolet-7, 'merge':'EWK'},
#       {'name':'T_tWch', 'sample':T_tWch, 'legendName':'TtW', 'color':ROOT.kViolet+1, 'merge':'EWK'},
#       {'name':'TBar_tWch', 'sample':TBar_tWch, 'legendName':'TBartW', 'color':ROOT.kViolet+6, 'merge':'EWK'},
#       {'name':'TTWJetsToLNu_25ns', 'sample':TTWJetsToLNu_25ns, 'legendName':'tt+W', 'color':ROOT.kOrange, 'merge':'EWK'},
#       {'name':'TTWJetsToQQ_25ns', 'sample':TTWJetsToQQ_25ns, 'legendName':'tt+W', 'color':ROOT.kOrange+7, 'merge':'EWK'},
#       {'name':'TTZToLLNuNu_25ns', 'sample':TTZToLLNuNu_25ns, 'legendName':'tt+Z', 'color':ROOT.kOrange+4, 'merge':'EWK'},
#       {'name':'TTZToQQ_25ns', 'sample':TTZToQQ_25ns, 'legendName':'tt+Z', 'color':ROOT.kOrange+4, 'merge':'EWK'},
#       #{'name':'WZ_25ns', 'sample':WZ_25ns, 'legendName':'WZ', 'color':ROOT.kOrange, 'merge':'EWK'},
#       #{'name':'WWTo2L2Nu_25ns', 'sample':WWTo2L2Nu_25ns, 'legendName':'WW', 'color':ROOT.kOrange+7, 'merge':'EWK'},
#       #{'name':'ZZ_25ns', 'sample':ZZ_25ns, 'legendName':'ZZ', 'color':ROOT.kOrange+4, 'merge':'EWK'},
#       {'name':'DYJetsToLL_M_50_HT100to200_25ns', 'sample':DYJetsToLL_M_50_HT100to200_25ns, 'legendName':'DY HT100-200', 'color':ROOT.kRed, 'merge':'EWK'},
#       {'name':'DYJetsToLL_M_50_HT200to400_25ns', 'sample':DYJetsToLL_M_50_HT200to400_25ns, 'legendName':'DY HT200-400', 'color':ROOT.kRed, 'merge':'EWK'},
#       {'name':'DYJetsToLL_M_50_HT400to600_25ns', 'sample':DYJetsToLL_M_50_HT400to600_25ns, 'legendName':'DY HT400-600', 'color':ROOT.kRed, 'merge':'EWK'},
#       {'name':'DYJetsToLL_M_50_HT600toInf_25ns', 'sample':DYJetsToLL_M_50_HT600toInf_25ns, 'legendName':'DY HT600-Inf', 'color':ROOT.kRed, 'merge':'EWK'},
#       {'name':'WJetsToLNu_HT100to200_25ns', 'sample':WJetsToLNu_HT100to200_25ns, 'legendName':'W HT100-200', 'color':ROOT.kGreen+3, 'merge':'EWK'},
#       {'name':'WJetsToLNu_HT200to400_25ns', 'sample':WJetsToLNu_HT200to400_25ns, 'legendName':'W HT200-400', 'color':ROOT.kGreen, 'merge':'EWK'},
#       {'name':'WJetsToLNu_HT400to600_25ns', 'sample':WJetsToLNu_HT400to600_25ns, 'legendName':'W HT400-600', 'color':ROOT.kGreen-3, 'merge':'EWK'},
#       {'name':'WJetsToLNu_HT600to800_25ns', 'sample':WJetsToLNu_HT600to800_25ns, 'legendName':'W HT600-800', 'color':ROOT.kGreen-7, 'merge':'EWK'},
#       {'name':'WJetsToLNu_HT800to1200_25ns', 'sample':WJetsToLNu_HT800to1200_25ns, 'legendName':'W HT800-1200', 'color':ROOT.kGreen-7, 'merge':'EWK'},
#       {'name':'WJetsToLNu_HT1200to2500_25ns', 'sample':WJetsToLNu_HT1200to2500_25ns, 'legendName':'W HT1200-2500', 'color':ROOT.kGreen-7, 'merge':'EWK'},
#       {'name':'WJetsToLNu_HT2500toInf_25ns', 'sample':WJetsToLNu_HT2500toInf_25ns, 'legendName':'W HT2500-Inf', 'color':ROOT.kGreen-7, 'merge':'EWK'},
#       {'name':'TTJets_LO_25ns', 'sample':TTJets_LO_25ns, 'legendName':'t #bar{t}+Jets', 'color':ROOT.kRed, 'merge':'EWK', 'addCut':'&&lheHTIncoming<600'},
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

presel = 'nLep==1&&nVeto==0&&nEl==1&&leptonPt>25&&Jet2_pt>80'
antiSelStr = presel+filters+'&&Selected==-1&&leptonHoverE>0.01'
SelStr = presel+filters+'&&Selected==1'

histos = {}
bins = {}
for srNJet in signalRegion:
  bins[srNJet] = {}
  for stb in signalRegion[srNJet]:
    bins[srNJet][stb] = {}
    for htb in signalRegion[srNJet][stb]:
      bins[srNJet][stb][htb] = {}
      for btb in btreg:
        bins[srNJet][stb][htb][btb] = {}
        for dP in sorted(signalRegion[srNJet][stb][htb]):
          deltaPhiCut = signalRegion[srNJet][stb][htb][dP]['deltaPhi']

          print 'Binning => Ht: ',htb,'Lt: ',stb,'NJet: ',srNJet
          antiSelname, antiSelCut = nameAndCut(stb, htb, srNJet, btb=btb, presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30')
          Selname, SelCut         = nameAndCut(stb, htb, srNJet, btb=btb, presel=SelStr, charge="", btagVar = 'nBJetMediumCSV30')

          histos['QCD']={}
#          histos['EWK']={}
#          histos['DATA']={}
          histos['QCD']['antiSelection']=ROOT.TH1F('QCD_antiSelection','QCD_antiSelection',30,-0.5,2.5)
          histos['QCD']['Selection']=ROOT.TH1F('QCD_Selection','QCD_Selection',30,-0.5,2.5)
#          histos['EWK']['antiSelection']=ROOT.TH1F('EWK_antiSelection','EWK_antiSelection',30,-0.5,2.5)
#          histos['EWK']['Selection']=ROOT.TH1F('EWK_Selection','EWK_Selection',30,-0.5,2.5)
#          histos['DATA']['antiSelection']=ROOT.TH1F('DATA_antiSelection','DATA_antiSelection',30,-0.5,2.5)
#          histos['DATA']['Selection']=ROOT.TH1F('DATA_Selection','DATA_Selection',30,-0.5,2.5)

          Canv = ROOT.TCanvas('Canv','Canv')
#          Canv.SetLogy()
          leg = ROOT.TLegend(0.7,0.8,0.98,0.95)
          leg.SetFillColor(0)
          leg.SetBorderSize(1)
          leg.SetShadowColor(ROOT.kWhite)
          text = ROOT.TLatex()
          text.SetNDC()
          text.SetTextSize(0.045)
          text.SetTextAlign(11)
        
          cQCD.Draw('Lp>>QCD_antiSelection','('+weight_str+')*('+antiSelCut+')')
          cQCD.Draw('Lp>>QCD_Selection','('+weight_str+')*('+SelCut+')')
#          cEWK.Draw('Lp>>EWK_antiSelection','(weight)*('+antiSelCut+')')
#          cEWK.Draw('Lp>>EWK_Selection','(weight)*('+SelCut+')')
#          cData.Draw('Lp>>DATA_antiSelection','('+antiSelCut+trigger+')')
#          cData.Draw('Lp>>DATA_Selection','('+SelCut+trigger+')')

#          for hist in [histos['DATA']['antiSelection'],histos['DATA']['Selection']]:
#            hist.SetStats(0)
#            hist.GetYaxis().SetTitle('# of Events')
#            hist.GetXaxis().SetTitle('L_{p}')
#            hist.SetLineColor(ROOT.kBlack)
#            hist.SetLineStyle(1)
#            hist.SetLineWidth(1)
  
          for hist in [histos['QCD']['antiSelection'],histos['QCD']['Selection']]:#,histos['EWK']['antiSelection'],histos['EWK']['Selection']]:
            hist.SetStats(0)
            hist.GetYaxis().SetTitle('a.u.')
            hist.GetXaxis().SetTitle('L_{p}')
            hist.SetLineWidth(2)
            hist.SetMarkerStyle(20)

          Canv.cd()
          histos['QCD']['antiSelection'].SetLineColor(ROOT.kBlue)
          histos['QCD']['antiSelection'].SetMarkerColor(ROOT.kBlue)
#          histos['QCD']['antiSelection'].SetLineStyle(ROOT.kDashed)
          if histos['QCD']['antiSelection'].Integral()>0: histos['QCD']['antiSelection'].Scale(1./histos['QCD']['antiSelection'].Integral())
          leg.AddEntry(histos['QCD']['antiSelection'],'QCD anti-selected','l')
   
          histos['QCD']['Selection'].SetLineColor(ROOT.kRed)
          histos['QCD']['Selection'].SetMarkerColor(ROOT.kRed)
          if histos['QCD']['Selection'].Integral()>0: histos['QCD']['Selection'].Scale(1./histos['QCD']['Selection'].Integral())
          leg.AddEntry(histos['QCD']['Selection'],'QCD selected','l')
   
          histos['QCD']['antiSelection'].Draw('ep')
          histos['QCD']['Selection'].Draw('same ep')
  
          histos['QCD']['antiSelection'].SetMaximum(1.5*histos['QCD']['antiSelection'].GetMaximum())
          histos['QCD']['Selection'].SetMaximum(1.5*histos['QCD']['Selection'].GetMaximum())
#          histos['QCD']['antiSelection'].SetMinimum(0)
#          histos['QCD']['Selection'].SetMinimum(0)
            
          leg.Draw()
          text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
          text.DrawLatex(0.75,0.96,"#bf{MC (13 TeV)}")
  
          Canv.cd()
          Canv.Print(wwwDir+prefix+Selname+'.png')
          Canv.Print(wwwDir+prefix+Selname+'.root')
          Canv.Print(wwwDir+prefix+Selname+'.pdf')
          Canv.Clear()
  
