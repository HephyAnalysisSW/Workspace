import ROOT
from array import array
import pickle
import os,sys
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getYieldFromChain,getPlotFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from Workspace.RA4Analysis.cmgTuples_Data25ns_miniAODv2_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
from Workspace.RA4Analysis.signalRegions import signalRegion3fb 
from cutFlow_helper import *
from general_config import *
from math import *

ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
maxN = -1
ROOT.gStyle.SetOptStat(0)

all_MB = False
presel = True
SB_w   = False
SB_tt  = False


if all_MB : 
  SR = signalRegion3fb
  btag_weight = "(weightBTag0_SF)"
  nbtag = (0,0)
if presel : 
  SR = {(5,-1):{(250,-1):{(500,-1):{"deltaPhi":1}}}}
  btag_weight = "(weightBTag0_SF)"
  nbtag = (0,0)
if SB_w : 
  SR = {(3,4):{(250,-1):{(500,-1):{"deltaPhi":1}}}}
  btag_weight = "(weightBTag0_SF)"
  nbtag = (0,0)
if SB_tt : 
  SR = {(4,5):{(250,-1):{(500,-1):{"deltaPhi":1}}}}
  btag_weight = "(weightBTag1_SF)"
  nbtag = (1,1)

lepSels = [
{'cut':'(singleMuonic&&(!isData||(isData&&muonDataSet)))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain(single_mu_Run2015D,maxN=maxN,histname="",treeName="Events") ,\
  'label':'_mu_', 'str':'1 $\\mu$' , 'trigger': trigger},\
{'cut':'singleElectronic&&(!isData||(isData&&eleDataSet))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain(single_ele_Run2015D,maxN=maxN,histname="",treeName="Events") ,\
  'label':'_ele_', 'str':'1 $\\e$' , 'trigger': trigger},\
{'cut':'((!isData&&singleLeptonic)||(isData&&((eleDataSet&&singleElectronic)||(muonDataSet&&singleMuonic))))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain([single_ele_Run2015D,single_mu_Run2015D],maxN=maxN,histname="",treeName="Events") ,\
  'label':'_lep_', 'str':'1 $lep$' , 'trigger': trigger}\
]

bkg_samples=[
{'sample':'TTVH',     "weight":btag_weight ,"cut":(0,-1) , "name":TTV_25ns ,'tex':'t#bar{t}V(W/Z/H)','color':ROOT.kOrange-3},
{"sample":"singleTop","weight":btag_weight ,"cut":(0,-1) , "name":singleTop_25ns,"tex":"t/#bar{t}",'color': ROOT.kViolet+5},
{"sample":"DY",       "weight":btag_weight ,"cut":(0,-1) , "name":DY_25ns,"tex":"DY + jets",'color':ROOT.kRed-6},
{"sample":"QCD",      "weight":"(1)"       ,"cut":(1,1)  , "name":QCDHT_25ns, "tex":"QCD","color":ROOT.kCyan-6},
{"sample":"WJets",    "weight":btag_weight ,"cut":(0,-1) , "name":WJetsHTToLNu_25ns,"tex":"W + jets","color":ROOT.kGreen-2},
{"sample":"ttJets",   "weight":btag_weight ,"cut":(0,-1) , "name":TTJets_combined, "tex":"t#bar{t} + jets",'color':ROOT.kBlue-4},
]

for bkg in bkg_samples:
    bkg['chain'] = getChain(bkg['name'],maxN=maxN,histname="",treeName="Events")

signals = [\
{"chain":getChain(T5qqqqVV_mGluino_1000To1075_mLSP_1To950[1000][700],histname='')  ,"name":"s1000","tex":"T5q^{4}WW 1.0/0.7","color":ROOT.kBlack},\
{"chain":getChain(T5qqqqVV_mGluino_1200To1275_mLSP_1to1150[1200][800],histname='') ,"name":"s1200","tex":"T5q^{4}WW 1.2/0.8","color":ROOT.kRed},\
{"chain":getChain(T5qqqqVV_mGluino_1400To1550_mLSP_1To1275[1500][100],histname=''),"name":"s1500","tex":"T5q^{4}WW 1.5/0.1","color":ROOT.kBlue},\
]

plots =[\
{'ndiv':False,'yaxis':'Events','xaxis':'#Delta#Phi(W,l)','logy':'True' , 'var':'deltaPhi_Wl',                 'varname':'deltaPhi_Wl',       'binlabel':1, 'bin':(30,0,3.141)},\
{'ndiv':True,'yaxis':'Events /','xaxis':'L_{T}','logy':'True' , 'var':  'st',                          'varname':'LT',                  'binlabel':20,  'bin':(45,100,1000)},\
{'ndiv':True,'yaxis':'Events /','xaxis':'H_{T}','logy':'True' , 'var':'htJet30j',                    'varname':'htJet30j',            'binlabel':50,  'bin':(44,300,2500)},\
{'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}','logy':'True' , 'var':'nJet30',                      'varname':'nJet30',                   'binlabel':1,  'bin':(15,0,15)},\
{'ndiv':True,'yaxis':'Events /','xaxis':'p_{T}(l)','logy':'True' , 'var':'LepGood_pt[0]',                 'varname':'leptonPt',      'binlabel':15,  'bin':(40,25,625)},\
{'ndiv':False,'yaxis':'Events','xaxis':'N_{bJetsCSV}','logy':'True' , 'var':'nBJetMediumCSV30',           'varname':'nBJetMediumCSV30',      'binlabel':1,  'bin':(8,0,8),       'lowlimit':0,  'limit':8},\
{'ndiv':True,'yaxis':'Events /','xaxis':'p_{T}(leading jet)','logy':'True' , 'var':'Jet_pt[0]',               'varname':'leading_JetPt',  'binlabel':35,  'bin':(20,0,700)},\
{'ndiv':False,'yaxis':'Events','xaxis':'#eta(l)','logy':'True' , 'var':'LepGood_eta[0]',                 'varname':'leptonEta',      'binlabel':25,  'bin':(40,-4,4)},\
{'ndiv':True,'yaxis':'Events /','xaxis':'#slash{E}_{T}','logy':'True' , 'var':'met_pt',                         'varname':'met',         'binlabel':50,  'bin':(28,0,1400)},\
{'ndiv':False,'yaxis':'Events /','xaxis':'#slash{E}_{T} #Phi','logy':'True' , 'var':'met_phi',                         'varname':'met_phi',         'binlabel':50,  'bin':(30,-3.14,3.14)},\
{'ndiv':False,'yaxis':'Events','xaxis':'#phi(l)','logy':'True' , 'var':'LepGood_phi[0]',                 'varname':'leptonPhi',      'binlabel':25,  'bin':(40,-4,4)},\
{'ndiv':False,'yaxis':'Events','xaxis':'miniIso(l)','logy':'True' , 'var':'LepGood_miniRelIso[0]',                 'varname':'leptonminiIso',      'binlabel':30,  'bin':(40,0,0.5)},\
{'ndiv':False,'yaxis':'Events','xaxis':'minDeltaR','logy':'True' , 'var':'Min$(sqrt((abs(Jet_phi-LepGood_phi[0]))**2+(abs(Jet_eta-LepGood_eta[0]))**2))',       'varname':'Min_R_Jet_lepton',      'binlabel':1,  'bin':(50,0,10)},\
{'ndiv':False,'yaxis':'Events','xaxis':'nVert','logy':'True' , 'var':'nVert',       'varname':'nVert',      'binlabel':1,  'bin':(50,0,50)}
  ]

for lepSel in lepSels:
  path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/2p3fb/Tests/"+lepSel['label']
  if not os.path.exists(path):
    os.makedirs(path)
  print lepSel['label']
  print "====== "
  presel = "&&".join([lepSel['cut'],lepSel['veto'],"Jet_pt[1]>80&&abs(LepGood_eta[0])<2.4"])
  sig_presel = "&&".join([lepSel['cut'],lepSel['veto'],"Jet_pt[1]>80&&abs(LepGood_eta[0])<2.4"])
  data_presel = "&&".join([lepSel['cut'],lepSel['veto'],lepSel['trigger'],filters,"Jet_pt[1]>80&&abs(LepGood_eta[0])<2.4"])
  bin = {}
  for srNJet in sorted(SR):
    bin[srNJet]={}
    for stb in sorted(SR[srNJet]):
      bin[srNJet][stb] = {}
      for htb in sorted(SR[srNJet][stb]):
        bin[srNJet][stb][htb] = {}
        deltaPhiCut = SR[srNJet][stb][htb]['deltaPhi']
        Name, Cut = nameAndCut(stb, htb, srNJet , btb=nbtag, presel=presel, btagVar =  btagVarString)
        print Name
        CR_path = path+'/'+Name+'/' 
        if not os.path.exists(CR_path):
          os.makedirs(CR_path)
        for p in plots:
          bin[srNJet][stb][htb][p['varname']] = {}
          for bkg in bkg_samples:
            bla_Name, Cut = nameAndCut(stb, htb, srNJet, btb=bkg['cut'], presel=presel, btagVar =  btagVarString)
            bin[srNJet][stb][htb][p['varname']][bkg['sample']] = getPlotFromChain(bkg['chain'], p['var'], p['bin'], cutString = Cut, weight = "*".join([weight_str , bkg["weight"]]) , binningIsExplicit=False, addOverFlowBin='both')
          bla_Name, Cut = nameAndCut(stb, htb,srNJet, btb=nbtag, presel=sig_presel, btagVar =  btagVarString)
          bin[srNJet][stb][htb][p['varname']]['signals'] = {}
          for sig in signals:
            bin[srNJet][stb][htb][p['varname']]['signals'][sig["name"]] = getPlotFromChain(sig['chain'], p['var'], p['bin'], cutString = Cut , weight = "*".join([weight_str_signal_plot , btag_weight]), binningIsExplicit=False, addOverFlowBin='both') 
          bla_Name, Cut = nameAndCut(stb, htb,srNJet, btb=nbtag, presel=data_presel, btagVar =  btagVarString)
          bin[srNJet][stb][htb][p['varname']]['data'] = getPlotFromChain(lepSel['chain'], p['var'], p['bin'], cutString = Cut , weight = "(1)", binningIsExplicit=False, addOverFlowBin='both')
          bin[srNJet][stb][htb]['label'] = Name         
          bin[srNJet][stb][htb]['path'] = CR_path        

  for p in plots:
    index = 0
    for srNJet in sorted(SR):
      for stb in sorted(SR[srNJet]):
        for htb in sorted(SR[srNJet][stb]):
          index +=1
          print index
          print bin[srNJet][stb][htb]['label']
          cb = ROOT.TCanvas("cb","cb",800,800)
          cb.cd()
          cb.SetRightMargin(3)
          latex = ROOT.TLatex()
          latex.SetNDC()
          latex.SetTextSize(0.04)
          latex.SetTextAlign(11)
          leg = ROOT.TLegend(0.7,0.55,0.93,0.925)
          leg.SetBorderSize(1)
          leg_sig = ROOT.TLegend(0.4,0.75,0.65,0.925)
          leg_sig.SetBorderSize(1)
          Pad1 = ROOT.TPad("Pad1", "Pad1", 0.22, 0.31, 1, 1)
          Pad1.SetLogy()
          Pad1.SetTopMargin(0.06)
          Pad1.SetBottomMargin(0)
          Pad1.SetLeftMargin(0.16)
          Pad1.SetRightMargin(0.05)
          Pad1.Draw()
          Pad1.cd()
          ROOT.gStyle.SetHistMinimumZero()
          h_Stack = ROOT.THStack('h_Stack','h_Stack')
          for bkg in bkg_samples:
            color = bkg['color']
            histo = bin[srNJet][stb][htb][p['varname']][bkg['sample']]
            histo.SetFillColor(color)
            histo.SetLineColor(ROOT.kBlack)
            histo.SetLineWidth(2)
            histo.GetXaxis().SetTitle(p['xaxis'])
            histo.SetTitle("")
            histo.GetYaxis().SetTitleSize(2)
            if p['ndiv']:
               histo.GetXaxis().SetNdivisions(505)
               histo.GetYaxis().SetTitle(p['yaxis']+str(p['binlabel'])+'GeV')
            if not p['ndiv']:
               histo.GetYaxis().SetTitle(p['yaxis'])
            leg.AddEntry(histo, bkg['tex'],"f")
            h_Stack.Add(histo)
            del histo
          h_Stack.Draw("Bar")
          
          stack_hist=ROOT.TH1F("stack_hist","stack_hist",p['bin'][0],p['bin'][1],p['bin'][2])
          stack_hist.Merge(h_Stack.GetHists())

          max_bin = stack_hist.GetMaximum()*100

          h_Stack.SetMaximum(max_bin)
          h_Stack.SetMinimum(0.11)
          
          color = ROOT.kBlack
          h_data = bin[srNJet][stb][htb][p['varname']]['data']
          h_data.SetMarkerStyle(20)
          h_data.SetMarkerSize(1.8)
          h_data.SetLineColor(color)
          h_data.GetXaxis().SetTitle(p['xaxis'])
          h_data.SetTitle("")
          h_data.GetYaxis().SetTitleSize(0.05)
          h_data.GetYaxis().SetLabelSize(0.05)
          h_data.Draw("E1P")
          h_data.SetMaximum(max_bin)
          h_data.SetMinimum(0.11)
          h_Stack.Draw("HistoSame")
          for sig in signals:
            h_sig = bin[srNJet][stb][htb][p['varname']]['signals'][sig["name"]]
            h_sig.SetLineColor(sig["color"])
            h_sig.SetLineWidth(2)
            h_sig.SetTitle("")
            h_sig.Draw("HistoSame")
            leg_sig.AddEntry(h_sig, sig['tex'],"l")
            del h_sig
          h_data.Draw("E1PSame")
          if p['ndiv']:
            h_data.GetXaxis().SetNdivisions(505)
            h_data.GetYaxis().SetTitle(p['yaxis']+str(p['binlabel'])+'GeV')
          if not p['ndiv']:
            h_data.GetYaxis().SetTitle(p['yaxis'])
          print "Integral of BKG:" , stack_hist.Integral()
          print "Integral of Data:" , h_data.Integral()
          leg.AddEntry(h_data, "Data","PL")
          leg.SetFillColor(0)
          leg.SetLineColor(0)
          leg.Draw()
          leg_sig.SetFillColor(0)
          leg_sig.SetLineColor(0)
          leg_sig.Draw()
          latex.DrawLatex(0.16,0.958,"#font[22]{CMS}"+" #font[12]{Preliminary}")
          latex.DrawLatex(0.73,0.958,"#bf{"+str(lumi_label)+" fb^{-1} (13 TeV)}")
          Pad1.RedrawAxis()
          cb.cd()
          Pad2 = ROOT.TPad("Pad2", "Pad2",  0.22, 0, 1, 0.31)
          Pad2.SetTopMargin(0)
          Pad2.SetBottomMargin(0.5)
          Pad2.SetLeftMargin(0.16)
          Pad2.SetRightMargin(0.05)
          Pad2.Draw()
          Pad2.cd()
          Func = ROOT.TF1('Func',"[0]",p['bin'][1],p['bin'][2])
          Func.SetParameter(0,1)
          Func.SetLineColor(ROOT.kBlue)
          h_ratio = h_data.Clone('h_ratio')
          h_ratio.Sumw2()
          h_ratio.SetStats(0)
          h_ratio.Divide(stack_hist)
          rmax = 10
          for b in xrange(1,h_ratio.GetNbinsX()+1):
            if h_ratio.GetBinContent(b) == 0: continue
            rmax = max([ rmax, h_ratio.GetBinContent(b) + 2*h_ratio.GetBinError(b) ])
          h_ratio.SetMinimum(0.0)
          h_ratio.SetMaximum(min(rmax,4.99))
          h_ratio.SetMarkerStyle(20)
          h_ratio.SetMarkerColor(ROOT.kBlack)
          h_ratio.SetTitle("")
          h_ratio.GetYaxis().SetTitle("Data/Pred. ")
          h_ratio.GetYaxis().SetTitleSize(0.1)
          h_ratio.GetXaxis().SetTitle(p['xaxis'])
          h_ratio.GetYaxis().SetTitleFont(42)
          h_ratio.GetYaxis().SetTitleOffset(0.6)
          h_ratio.GetXaxis().SetTitleOffset(1)
          h_ratio.GetYaxis().SetNdivisions(505)
          h_ratio.GetXaxis().SetTitleSize(0.2)
          h_ratio.GetXaxis().SetLabelSize(0.13)
          h_ratio.GetYaxis().SetLabelSize(0.1)
          h_ratio.Draw("E1")
          Func.Draw("same")
          cb.Draw()
          cb.SaveAs(bin[srNJet][stb][htb]['path']+p['varname']+'.png')
          cb.SaveAs(bin[srNJet][stb][htb]['path']+p['varname']+'.pdf')
          cb.SaveAs(bin[srNJet][stb][htb]['path']+p['varname']+'.root')
          cb.Clear()
          del h_Stack

