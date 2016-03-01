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
def Draw_CMS_header():
   tex = ROOT.TLatex()
   tex.SetNDC()
   tex.SetTextAlign(31)
   tex.SetTextFont(42)
   tex.SetTextSize(0.05)
   tex.SetLineWidth(2)
   tex.DrawLatex(0.96,0.96,"2.2 fb^{-1} (13 TeV)")
   tex = ROOT.TLatex()
   tex.SetNDC()
   tex.SetTextFont(61)
   tex.SetTextSize(0.05)
   tex.SetLineWidth(2)
   tex.DrawLatex(0.18,0.96,"CMS")
   tex = ROOT.TLatex()
   tex.SetNDC()
   tex.SetTextFont(52)
   tex.SetTextSize(0.05)
   tex.SetLineWidth(2)
   tex.DrawLatex(0.2736,0.96,"Preliminary")
   return
def Set_axis_pad2(histo):
   histo.GetXaxis().SetLabelFont(42)
   histo.GetXaxis().SetLabelOffset(0.007)
   histo.GetXaxis().SetLabelSize(0.11)
   histo.GetXaxis().SetTitleSize(0.14)
   histo.GetXaxis().SetTitleOffset(0.9)
   histo.GetXaxis().SetTitleFont(42)
   histo.GetYaxis().SetTitle("Data/Pred.")
   histo.GetYaxis().SetDecimals()
   histo.GetYaxis().SetNdivisions(505)
   histo.GetYaxis().SetLabelFont(42)
   histo.GetYaxis().SetLabelOffset(0.007)
   histo.GetYaxis().SetLabelSize(0.11)
   histo.GetYaxis().SetTitleSize(0.14)
   histo.GetYaxis().SetTitleOffset(0.52)
   histo.GetYaxis().SetTitleFont(42)
   histo.GetZaxis().SetLabelFont(42)
   histo.GetZaxis().SetLabelOffset(0.007)
   histo.GetZaxis().SetLabelSize(0.05)
   histo.GetZaxis().SetTitleSize(0.06)
   histo.GetZaxis().SetTitleFont(42)
   return

def Set_axis_pad1(histo):
   histo.GetXaxis().SetLabelFont(42)
   histo.GetXaxis().SetLabelOffset(0.007)
   histo.GetXaxis().SetLabelSize(0.05)
   histo.GetXaxis().SetTitleSize(0.06)
   histo.GetXaxis().SetTitleOffset(0.9)
   histo.GetXaxis().SetTitleFont(42)
   histo.GetYaxis().SetLabelFont(42)
   histo.GetYaxis().SetLabelOffset(0.007)
   histo.GetYaxis().SetLabelSize(0.05)
   histo.GetYaxis().SetTitleSize(0.06)
   histo.GetYaxis().SetTitleOffset(1.35)
   histo.GetYaxis().SetTitleFont(42)
   histo.GetZaxis().SetLabelFont(42)
   histo.GetZaxis().SetLabelOffset(0.007)
   histo.GetZaxis().SetLabelSize(0.05)
   histo.GetZaxis().SetTitleSize(0.06)
   histo.GetZaxis().SetTitleFont(42)
   return

ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
maxN = -1
ROOT.gStyle.SetOptStat(0)

all_MB = False
presel = True
SB_w   = False
SB_tt  = False

test = False
if test :
  presel = True

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
{'sample':'TTVH',           "weight":btag_weight ,"cut":(0,-1) ,"add_Cut":"(1)","name":TTV_25ns ,'tex':'t#bar{t}V','color':ROOT.kOrange-3},
{"sample":"DY",             "weight":btag_weight ,"cut":(0,-1) ,"add_Cut":"(1)","name":DY_25ns,"tex":"DY + jets",'color':ROOT.kRed-6},
{"sample":"singleTop",      "weight":btag_weight ,"cut":(0,-1) ,"add_Cut":"(1)","name":singleTop_25ns,"tex":"t/#bar{t}",'color': ROOT.kViolet+5},
{"sample":"QCD",            "weight":"(1)"       ,"cut":nbtag  ,"add_Cut":"(1)","name":QCDHT_25ns, "tex":"QCD","color":ROOT.kCyan-6},
{"sample":"WJets",          "weight":btag_weight ,"cut":(0,-1) ,"add_Cut":"(1)","name":WJetsHTToLNu_25ns,"tex":"W + jets","color":ROOT.kGreen-2},
{"sample":"ttJets_diLep",   "weight":btag_weight ,"cut":(0,-1) ,"add_Cut":"((ngenLep+ngenTau)==2)","name":TTJets_combined, "tex":"t#bar{t} ll + jets",'color':ROOT.kBlue},
{"sample":"ttJets_semiLep", "weight":btag_weight ,"cut":(0,-1) ,"add_Cut":"(!((ngenLep+ngenTau)==2))","name":TTJets_combined, "tex":"t#bar{t} l + jets",'color':ROOT.kBlue-7}
]

for bkg in bkg_samples:
    bkg['chain'] = getChain(bkg['name'],maxN=maxN,histname="",treeName="Events")

signals = [\
{"chain":getChain(T5qqqqVV_mGluino_1000To1075_mLSP_1To950[1000][700],histname='')  ,"name":"s1000","tex":"x10 T5q^{4}WW 1.0/0.7","color":ROOT.kAzure+9},\
{"chain":getChain(T5qqqqVV_mGluino_1200To1275_mLSP_1to1150[1200][800],histname='') ,"name":"s1200","tex":"x10 T5q^{4}WW 1.2/0.8","color":ROOT.kMagenta+2},\
{"chain":getChain(T5qqqqVV_mGluino_1400To1550_mLSP_1To1275[1500][100],histname=''),"name":"s1500","tex":"x10 T5q^{4}WW 1.5/0.1","color":ROOT.kRed+1},\
]
dPhiBins  = array('d', [float(x)/1000. for x in range(0,500,100)+range(500,700,200)+range(700,1000,300)+range(1000,2000,500)+range(2000,3141,1141)+range(3141,4141,1000)])
plots =[\
{'ndiv':False,'yaxis':'Events','xaxis':'#Delta#Phi(W,l)','logy':'True' , 'var':'deltaPhi_Wl',        'bin_set':True,          'varname':'deltaPhi_Wl',       'binlabel':1, 'bin':(len(dPhiBins)-1,dPhiBins)},\
{'ndiv':True,'yaxis':'Events /','xaxis':'L_{T}','logy':'True' , 'var':  'st',                        'bin_set':False,          'varname':'LT',                  'binlabel':25,  'bin':(30,250,1000)},\
{'ndiv':True,'yaxis':'Events /','xaxis':'H_{T}','logy':'True' , 'var':'htJet30j',                    'bin_set':False,          'varname':'htJet30j',            'binlabel':50,  'bin':(40,500,2500)},\
{'ndiv':False,'yaxis':'Events','xaxis':'n_{jet}','logy':'True' , 'var':'nJet30',                     'bin_set':False,          'varname':'nJet30',                   'binlabel':1,  'bin':(15,0,15)},\
{'ndiv':True,'yaxis':'Events /','xaxis':'p_{T}(l)','logy':'True' , 'var':'LepGood_pt[0]',            'bin_set':False,          'varname':'leptonPt',      'binlabel':15,  'bin':(40,25,625)},\
{'ndiv':False,'yaxis':'Events','xaxis':'n_{b-tag}','logy':'True' , 'var':'nBJetMediumCSV30',         'bin_set':False,          'varname':'nBJetMediumCSV30',      'binlabel':1,  'bin':(8,0,8),       'lowlimit':0,  'limit':8},\
{'ndiv':True,'yaxis':'Events /','xaxis':'p_{T}(leading jet)','logy':'True' , 'var':'Jet_pt[0]',      'bin_set':False,          'varname':'leading_JetPt',  'binlabel':35,  'bin':(20,0,700)},\
{'ndiv':False,'yaxis':'Events','xaxis':'#eta(l)','logy':'True' , 'var':'LepGood_eta[0]',             'bin_set':False,          'varname':'leptonEta',      'binlabel':25,  'bin':(40,-4,4)},\
{'ndiv':True,'yaxis':'Events /','xaxis':'#slash{E}_{T}','logy':'True' , 'var':'met_pt',              'bin_set':False,          'varname':'met',         'binlabel':50,  'bin':(28,0,1400)},\
{'ndiv':False,'yaxis':'Events /','xaxis':'#slash{E}_{T} #Phi','logy':'True' , 'var':'met_phi',       'bin_set':False,          'varname':'met_phi',         'binlabel':50,  'bin':(30,-3.14,3.14)},\
{'ndiv':False,'yaxis':'Events','xaxis':'#phi(l)','logy':'True' , 'var':'LepGood_phi[0]',             'bin_set':False,          'varname':'leptonPhi',      'binlabel':25,  'bin':(40,-4,4)},\
{'ndiv':False,'yaxis':'Events','xaxis':'miniIso(l)','logy':'True' , 'var':'LepGood_miniRelIso[0]',   'bin_set':False,          'varname':'leptonminiIso',      'binlabel':30,  'bin':(40,0,0.5)},\
#{'ndiv':False,'yaxis':'Events','xaxis':'minDeltaR','logy':'True' , 'var':'Min$(sqrt((abs(Jet_phi-LepGood_phi[0]))**2+(abs(Jet_eta-LepGood_eta[0]))**2))',       'varname':'Min_R_Jet_lepton',      'binlabel':1,  'bin':(50,0,10)},\
{'ndiv':False,'yaxis':'Events','xaxis':'Nvert','logy':'True' , 'var':'nVert',                        'bin_set':False,          'varname':'nVert',      'binlabel':1,  'bin':(50,0,50)}
  ]

if test :
  plots = [plots[1]]
  lepSels = [lepSels[2]]

for lepSel in lepSels:
  path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/2p25fb/toAN_latest_Style/"+lepSel['label']
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
            bla_Name, Cut = nameAndCut(stb, htb, srNJet, btb=bkg['cut'], presel="&&".join([bkg["add_Cut"],presel]), btagVar =  btagVarString)
            bin[srNJet][stb][htb][p['varname']][bkg['sample']] = getPlotFromChain(bkg['chain'], p['var'], p['bin'], cutString = Cut, weight = "*".join([weight_str_plot , bkg["weight"]]) , binningIsExplicit=False ,addOverFlowBin='both',variableBinning=p["bin_set"])
          bla_Name, Cut = nameAndCut(stb, htb,srNJet, btb=nbtag, presel=sig_presel, btagVar =  btagVarString)
          bin[srNJet][stb][htb][p['varname']]['signals'] = {}
          for sig in signals:
            bin[srNJet][stb][htb][p['varname']]['signals'][sig["name"]] = getPlotFromChain(sig['chain'], p['var'], p['bin'], cutString = Cut , weight = "*".join([weight_str_signal_plot , btag_weight]), binningIsExplicit=False ,addOverFlowBin='both',variableBinning=p["bin_set"]) 
          bla_Name, Cut = nameAndCut(stb, htb,srNJet, btb=nbtag, presel=data_presel, btagVar =  btagVarString)
          bin[srNJet][stb][htb][p['varname']]['data'] = getPlotFromChain(lepSel['chain'], p['var'], p['bin'], cutString = Cut , weight = "(1)", binningIsExplicit=False,addOverFlowBin='both',variableBinning=p["bin_set"])
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
          cb = ROOT.TCanvas("cb","cb",564,232,600,600)
          cb.SetHighLightColor(2)
          cb.Range(0,0,1,1)
          cb.SetFillColor(0)
          cb.SetBorderMode(0)
          cb.SetBorderSize(2)
          cb.SetTickx(1)
          cb.SetTicky(1)
          cb.SetLeftMargin(0.18)
          cb.SetRightMargin(0.04)
          cb.SetTopMargin(0.05)
          cb.SetBottomMargin(0.13)
          cb.SetFrameFillStyle(0)
          cb.SetFrameBorderMode(0)
          cb.SetFrameFillStyle(0)
          cb.SetFrameBorderMode(0)
          cb.cd()
          
          #cb.SetRightMargin(3)
          #latex = ROOT.TLatex()
          #latex.SetNDC()
          #latex.SetTextSize(0.025)
          #latex.SetTextAlign(11)
          
          leg = ROOT.TLegend(0.7,0.55,0.93,0.925)
          leg.SetBorderSize(1)
          leg_sig = ROOT.TLegend(0.4,0.75,0.65,0.925)
          leg_sig.SetBorderSize(1)
          Pad1 = ROOT.TPad("Pad1", "Pad1", 0,0.31,1,1)
          Pad1.Draw()
          Pad1.cd()
          #Pad1.Range(-0.7248462,-1.30103,3.302077,3.159352)
          Pad1.SetFillColor(0)
          Pad1.SetBorderMode(0)
          Pad1.SetBorderSize(2)
          Pad1.SetLogy()
          Pad1.SetTickx(1)
          Pad1.SetTicky(1)
          Pad1.SetLeftMargin(0.18)
          Pad1.SetRightMargin(0.04)
          Pad1.SetTopMargin(0.055)
          Pad1.SetBottomMargin(0)
          Pad1.SetFrameFillStyle(0)
          Pad1.SetFrameBorderMode(0)
          Pad1.SetFrameFillStyle(0)
          Pad1.SetFrameBorderMode(0)
          Pad1.SetLogy()
          #Pad1.Draw()
          #Pad1.cd()
          #ROOT.gStyle.SetHistMinimumZero()
          ROOT.gStyle.SetErrorX(.5)
          h_Stack = ROOT.THStack('h_Stack','h_Stack')
          for bkg in bkg_samples:
            color = bkg['color']
            histo = bin[srNJet][stb][htb][p['varname']][bkg['sample']]
            histo.SetFillColor(color)
            histo.SetLineColor(ROOT.kBlack)
            histo.SetLineWidth(1)
            Set_axis_pad1(histo)
            #histo.GetXaxis().SetTitle(p['xaxis'])
            #histo.SetTitle("")
            #histo.GetYaxis().SetTitleSize(2)
            if p['ndiv']:
               histo.GetXaxis().SetNdivisions(505)
               histo.GetYaxis().SetTitle(p['yaxis']+str(p['binlabel'])+'GeV')
            if not p['ndiv']:
               histo.GetYaxis().SetTitle(p['yaxis'])
            leg.AddEntry(histo, bkg['tex'],"f")
            h_Stack.Add(histo)
            del histo
          #h_Stack.Draw("Bar")
          
          if p["bin_set"]: stack_hist=ROOT.TH1F("stack_hist","stack_hist", p['bin'][0],p['bin'][1]) 
          else: stack_hist=ROOT.TH1F("stack_hist","stack_hist",p['bin'][0],p['bin'][1],p['bin'][2])
          stack_hist.Merge(h_Stack.GetHists())

          max_bin = stack_hist.GetMaximum()*100

          h_Stack.SetMaximum(max_bin)
          h_Stack.SetMinimum(0.11)
          
          color = ROOT.kBlack
          h_data = bin[srNJet][stb][htb][p['varname']]['data']
          h_data.SetMarkerStyle(20)
          h_data.SetMarkerSize(1.1)
          h_data.SetLineColor(color)
          h_data.GetXaxis().SetTitle(p['xaxis'])
          h_data.SetTitle("")
          #h_data.GetYaxis().SetTitleSize(0.05)
          #h_data.GetYaxis().SetLabelSize(0.05)
          Set_axis_pad1(h_data)
          h_data.Draw("E1")
          h_data.SetMaximum(max_bin)
          h_data.SetMinimum(0.11)
          h_Stack.Draw("HistoSame")
          for sig in signals:
            h_sig = bin[srNJet][stb][htb][p['varname']]['signals'][sig["name"]]
            if presel:
              h_sig.Scale(10)
            h_sig.SetLineColor(sig["color"])
            h_sig.SetLineWidth(2)
            h_sig.SetTitle("")
            h_sig.Draw("HistoSame")
            leg_sig.AddEntry(h_sig, sig['tex'],"l")
            del h_sig
          h_data.Draw("E1 Same")
          if p['ndiv']:
            h_data.GetXaxis().SetNdivisions(505)
            h_data.GetYaxis().SetTitle(p['yaxis']+str(p['binlabel'])+' GeV')
          if not p['ndiv']:
            h_data.GetYaxis().SetTitle(p['yaxis'])
          print "Integral of BKG:" , stack_hist.Integral()
          print "Integral of Data:" , h_data.Integral()
          leg.AddEntry(h_data, "Data","EPL")
          leg.SetFillColor(0)
          leg.SetLineColor(0)
          leg.Draw()
          leg_sig.SetFillColor(0)
          leg_sig.SetLineColor(0)
          leg_sig.Draw()
          #latex.DrawLatex(0.18,0.97,"#font[22]{CMS}"+" #font[12]{Preliminary}")
          #latex.DrawLatex(0.96,0.97,"#bf{"+str(lumi_label)+" fb^{-1} (13 TeV)}")
          Draw_CMS_header()
          Pad1.RedrawAxis()
          cb.cd()
          Pad2 = ROOT.TPad("Pad2", "Pad2",  0, 0, 1, 0.31)
          Pad2.Draw()
          Pad2.cd()
          #Pad2.Range(-0.7248462,-0.8571429,3.302077,2)
          Pad2.SetFillColor(0)
          Pad2.SetFillStyle(4000)
          Pad2.SetBorderMode(0)
          Pad2.SetBorderSize(2)
          Pad2.SetTickx(1)
          Pad2.SetTicky(1)
          Pad2.SetLeftMargin(0.18)
          Pad2.SetRightMargin(0.04)
          Pad2.SetTopMargin(0)
          Pad2.SetBottomMargin(0.3)
          Pad2.SetFrameFillStyle(0)
          Pad2.SetFrameBorderMode(0)
          Pad2.SetFrameFillStyle(0)
          Pad2.SetFrameBorderMode(0)
          if p["bin_set"] : Func = ROOT.TF1('Func',"[0]",p['bin'][1][0],p['bin'][1][-1])
          else: Func = ROOT.TF1('Func',"[0]",p['bin'][1],p['bin'][2])
          Func.SetParameter(0,1)
          Func.SetLineColor(58)
          Func.SetLineWidth(2)
          h_ratio = h_data.Clone('h_ratio')
          h_ratio.Sumw2()
          h_ratio.SetStats(0)
          h_ratio.Divide(stack_hist)
          rmax = 2
          for b in xrange(1,h_ratio.GetNbinsX()+1):
            if h_ratio.GetBinContent(b) == 0: continue
            rmax = max([ rmax, h_ratio.GetBinContent(b) + 2*h_ratio.GetBinError(b) ])
          print rmax
          h_ratio.SetMinimum(0.0)
          h_ratio.SetMaximum(min(rmax,4.99))
          h_ratio.SetMarkerStyle(20)
          h_ratio.SetMarkerSize(1.1)
          h_ratio.SetMarkerColor(ROOT.kBlack)
          h_ratio.SetTitle("")
          Set_axis_pad2(h_ratio)
          h_ratio.GetYaxis().SetTitle("Data/Pred. ")
          h_ratio.GetXaxis().SetTitle(p['xaxis'])
          h_ratio.GetYaxis().SetNdivisions(505)
          h_ratio.Draw("E1")
          Func.Draw("same")
          h_ratio.Draw("E1 Same")
          cb.Draw()
          cb.SaveAs(bin[srNJet][stb][htb]['path']+p['varname']+'.png')
          cb.SaveAs(bin[srNJet][stb][htb]['path']+p['varname']+'.pdf')
          cb.SaveAs(bin[srNJet][stb][htb]['path']+p['varname']+'.root')
          if test:
            cb.SaveAs("/afs/cern.ch/user/e/easilar/public/html/Notes/notes/SUS-15-006/trunk/fig/zerob/LT_zerob.pdf")
          cb.Clear()
          del h_Stack
