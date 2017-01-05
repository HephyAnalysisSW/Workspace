import ROOT
from array import array
import pickle
import os,sys
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getYieldFromChain,getPlotFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision, varBinNamewithUnit
from Workspace.RA4Analysis.cmgTuples_Data25ns_Moriond2017_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Spring16_Moriond2017_MiniAODv2_postProcessed import *
from Workspace.RA4Analysis.signalRegions import * 
from cutFlow_helper import *
from Workspace.RA4Analysis.general_config import *
from math import *

all_MB = False
presel = True
SB_w   = False 
SB_tt  = False
new_SB_tt  = False
presel_1b = False
test = False
unblind = False
draw_signal = True
blind = True
#add_cut = ["(1)","no_isoVeto"]
add_cut = ["(iso_Veto)","_isoVeto"]
#add_cut = "(1)"

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--iplot", dest="iplot", default=0, action="store", help="enter numbers 0,1,2..11 this the order of plot you want to plot 0 is deltaphi")
#parser.add_option("--top_index", dest="top_index", default=0, action="store", help="enter numbers 0,1,2 this the order oftopPt weight")
parser.add_option("--lepSel_index", dest="lepSel_index", default=0, action="store", help="enter numbers 0,1,2 this the order oftopPt weight")
(options, args) = parser.parse_args()

exec("tmp_iplot="+options.iplot)
print type(tmp_iplot)
iplot = tmp_iplot
#iplot = 0

#exec("tmp_topindex="+options.top_index)
#print type(tmp_topindex)
#top_index = tmp_topindex
#top_index = 1

exec("tmp_lepsel="+options.lepSel_index)
lepSel_index = tmp_lepsel


if all_MB : 
  #SR = signalRegions2016
  SR = signalRegions_tests
  SR = {(5,5):{(250,350):{(500,-1):{"deltaPhi":1.0}}}}
  btag_weight = "(weightBTag0_SF)"
  nbtag = (0,0)
  signal_suffix = ""
if presel : 
  SR = {(5,-1):{(250,-1):{(500,-1):{"deltaPhi":1}}}}
  #btag_weight = "(weightBTag0_SF)"
  btag_weight = "(1)"
  #btagVarString = "("+nbjets_30+")"
  nbtag = (0,0)
  signal_suffix = "x10"
if SB_w : 
  SR = {(3,4):{(250,-1):{(500,-1):{"deltaPhi":1}}}}
  btag_weight = "(1)"
  nbtag = (0,0)
  signal_suffix = ""
if SB_tt : 
  SR = {(4,5):{(250,-1):{(500,-1):{"deltaPhi":1}}}}
  #btag_weight = "(weightBTag1_SF)"
  btag_weight = "(1)"
  nbtag = (1,1)
  signal_suffix = ""
if new_SB_tt : 
  SR = {(4,5):{(250,-1):{(500,-1):{"deltaPhi":1}}}}
  #btag_weight = "(weightBTag1p_SF)"
  btag_weight = "(1)"
  nbtag = (1,-1)
  signal_suffix = ""
if test :
  SR = {(6,7):{(450,-1):{(500,1000):{"deltaPhi":1}}}}
  btag_weight = "(weightBTag0_SF)"
  nbtag = (0,0)
  signal_suffix = "x10"
if presel_1b : 
  #add_cut = "(deltaPhi_Wl<0.5)"
  SR = {(5,-1):{(250,-1):{(500,-1):{"deltaPhi":1}}}}
  btag_weight = "(1)"#"(weightBTag0_SF)"
  nbtag = (0,-1)
  signal_suffix = "x10"

if blind: 
  add_cut = [add_cut[0]+"&&"+"(deltaPhi_Wl<0.5)","dPhiltp5"+add_cut[1]]

 
#'label':'_mu_', 'str':'1 $\\mu$' ,'trigger': trigger,'trigger_xor':"((METDataSet&&%s&&!(%s)))"%(trigger_or_met,trigger_or_mu) },\
lepSels = [
{'cut':'singleMuonic' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain([single_ele,single_mu,met],histname="",treeName="Events"),\
  'label':'_mu_', 'str':'1 $\\mu$' ,'trigger': trigger,'trigger_xor':trigger_xor },\
{'cut':'singleElectronic' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain([single_ele,single_mu,met],histname="",treeName="Events") ,\
  'label':'_ele_', 'str':'1 $\\e$' , 'trigger': trigger, 'trigger_xor': trigger_xor},\
{'cut':'singleLeptonic' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain([single_ele,single_mu,met],histname="",treeName="Events") ,\
  'label':'_lep_', 'str':'1 $\\lep$' , 'trigger': trigger, 'trigger_xor': trigger_xor},\
]

diLep = "(Sum$(abs(genTau_grandmotherId)==6&&abs(genTau_motherId)==24)+Sum$(abs(genLep_grandmotherId)==6&&abs(genLep_motherId)==24)==2)"
semiLep = "(Sum$(abs(genTau_grandmotherId)==6&&abs(genTau_motherId)==24)+Sum$(abs(genLep_grandmotherId)==6&&abs(genLep_motherId)==24)<2)"

bkg_samples=[
{'sample':'TTVH',           "weight":btag_weight ,"cut":nbtag ,"add_Cut":"(1)","name":TTV ,'tex':'t#bar{t}V','color':ROOT.kOrange-3},
{"sample":"DiBosons",       "weight":btag_weight ,"cut":nbtag ,"add_Cut":"(1)","name":diBoson ,"tex":"WW/WZ/ZZ","color":ROOT.kRed+3},
{"sample":"DY",             "weight":btag_weight ,"cut":nbtag ,"add_Cut":"(1)","name":DY_HT,"tex":"DY + jets",'color':ROOT.kRed-6},
{"sample":"singleTop",      "weight":btag_weight ,"cut":nbtag ,"add_Cut":"(1)","name":singleTop_lep,"tex":"t/#bar{t}",'color': ROOT.kViolet+5},
{"sample":"QCD",            "weight":"(1)"       ,"cut":nbtag ,"add_Cut":"(1)","name":QCDHT, "tex":"QCD","color":ROOT.kCyan-6},
{"sample":"WJets",          "weight":btag_weight ,"cut":nbtag ,"add_Cut":"(1)","name":WJetsHTToLNu,"tex":"W + jets","color":ROOT.kGreen-2},
{"sample":"ttJets_diLep",   "weight":"(1.071)","cut":nbtag ,"add_Cut":diLep,"name":[TTJets_diLep,TTJets_HTbinned], "tex":"t#bar{t} ll + jets",'color':ROOT.kBlue},
{"sample":"ttJets_semiLep", "weight":"(1.071)","cut":nbtag ,"add_Cut":semiLep,"name":[TTJets_semiLep,TTJets_HTbinned], "tex":"t#bar{t} l + jets",'color':ROOT.kBlue-7}
]

for bkg in bkg_samples:
    bkg['chain'] = getChain(bkg['name'],maxN=maxN,histname="",treeName="Events")

signals = [\
{"chain":getChain(SMS_T5qqqqVV_TuneCUETP8M1[1500][1000],histname=''),"name":"s1500_1000","tex":"T5q^{4}WW 1.5/1.0 "+signal_suffix,"color":ROOT.kAzure+9},\
{"chain":getChain(SMS_T5qqqqVV_TuneCUETP8M1[1900][100],histname=''),"name":"s1900_100","tex":"T5q^{4}WW 1.9/0.1 "+signal_suffix,"color":ROOT.kMagenta+2},\
]

dPhiBins  = array('d', [float(x)/1000. for x in range(0,500,100)+range(500,700,200)+range(700,1000,300)+range(1000,2000,500)+range(2000,3141,1141)+range(3141,4141,1000)])
#hTBins  = [500, 750, 1000, 1250, 2500]
#lTBins = [250,350,450,600,950]
lTBins  = array('d', [float(x) for x in range(250,450,100)+range(450,600,150)+range(600,950,350)+range(950,2500,1550)])
hTBins  = array('d', [float(x) for x in range(500,1250,250)+range(1250,2500,1250)+range(2500,4500,2000)])
plots =[\
{'ndiv':False,'yaxis':'< Events / 0.1>','xaxis':'#Delta#Phi(W,l)','logy':'True' , 'var':'deltaPhi_Wl',        'bin_set':(True,0.1),          'varname':'deltaPhi_Wl',       'binlabel':1, 'bin':(len(dPhiBins)-1,dPhiBins)},\
{'ndiv':True,'yaxis':'< Events / 100 GeV >','xaxis':'L_{T} [GeV]','logy':'True' , 'var':  'st',                          'bin_set':(True,100),          'varname':'LT',                  'binlabel':"",  'bin':(len(lTBins)-1,lTBins)},\
{'ndiv':True,'yaxis':'< Events / 250 GeV >','xaxis':'H_{T}','logy':'True' , 'var':'htJet30j',                              'bin_set':(True,250),        'varname':'htJet30j',            'binlabel':"",  'bin':(len(hTBins)-1,hTBins)},\
{'ndiv':True,'yaxis':'Events / ','xaxis':'L_{T} [GeV]','logy':'True' , 'var':  'st',                        'bin_set':(False,25),          'varname':'LT_binned',                  'binlabel':25,  'bin':(40,250,1250)},\
{'ndiv':True,'yaxis':'Events / ','xaxis':'H_{T} [GeV]','logy':'True' , 'var':'htJet30j',                    'bin_set':(False,25),          'varname':'htJet30j_binned',            'binlabel':50,  'bin':(50,500,3000)},\
{'ndiv':False,'yaxis':'Events','xaxis':'n_{jet}','logy':'True' , 'var':'nJet30',                               'bin_set':(False,25),         'varname':'nJet30',                   'binlabel':1,  'bin':(15,0,15)},\
{'ndiv':True,'yaxis':'Events / ','xaxis':'p_{T}(l)','logy':'True' , 'var':'leptonPt',                      'bin_set':(False,25),          'varname':'leptonPt',      'binlabel':15,  'bin':(65,25,2275)},\
{'ndiv':True,'yaxis':'Events / ','xaxis':'mt2','logy':'True' , 'var':'iso_MT2','bin_set':(False,25),          'varname':'iso_MT2',      'binlabel':25,  'bin':(40,0,1000)},\
{'ndiv':False,'yaxis':'Events','xaxis':'n_{b-tag}','logy':'True' , 'var':'nBJetMediumCSV30',                   'bin_set':(False,25),          'varname':'nBJetMediumCSV30',      'binlabel':1,  'bin':(8,0,8),       'lowlimit':0,  'limit':8},\
#{'ndiv':False,'yaxis':'Events','xaxis':'LepGood_eleCBID_SPRING15_25ns_ConvVetoDxyDz','logy':'True' , 'var':'LepGood_eleCBID_SPRING15_25ns_ConvVetoDxyDz',                   'bin_set':(False,25),          'varname':'LepGood_eleCBID_SPRING15_25ns_ConvVetoDxyDz',      'binlabel':1,  'bin':(8,0,8),       'lowlimit':0,  'limit':8},\
{'ndiv':True,'yaxis':'Events / ','xaxis':'p_{T}(leading jet)','logy':'True' , 'var':'Jet_pt[0]',                'bin_set':(False,25),          'varname':'leading_JetPt',  'binlabel':35,  'bin':(20,0,700)},\
{'ndiv':False,'yaxis':'Events','xaxis':'#eta(l)','logy':'True' , 'var':'LepGood_eta[0]',                       'bin_set':(False,25),          'varname':'leptonEta',      'binlabel':25,  'bin':(40,-4,4)},\
{'ndiv':True,'yaxis':'Events / ','xaxis':'#slash{E}_{T}','logy':'True' , 'var':'met_pt',                        'bin_set':(False,25),          'varname':'met',         'binlabel':50,  'bin':(28,0,1400)},\
{'ndiv':False,'yaxis':'Events / ','xaxis':'#slash{E}_{T} #Phi','logy':'True' , 'var':'met_phi',                 'bin_set':(False,25),          'varname':'met_phi',         'binlabel':50,  'bin':(30,-3.14,3.14)},\
{'ndiv':False,'yaxis':'Events','xaxis':'#phi(l)','logy':'True' , 'var':'LepGood_phi[0]',                       'bin_set':(False,25),          'varname':'leptonPhi',      'binlabel':25,  'bin':(40,-4,4)},\
{'ndiv':False,'yaxis':'Events','xaxis':'miniIso(l)','logy':'True' , 'var':'LepGood_miniRelIso[0]',           'bin_set':(False,25),          'varname':'leptonminiIso',      'binlabel':30,  'bin':(40,0,0.5)},\
{'ndiv':False,'yaxis':'Events','xaxis':'minDeltaR','logy':'True' , 'var':'Min$(sqrt((abs(Jet_phi-LepGood_phi[0]))**2+(abs(Jet_eta-LepGood_eta[0]))**2))', 'bin_set':False  ,    'varname':'Min_R_Jet_lepton',      'binlabel':1,  'bin':(50,0,10)},\
{'ndiv':False,'yaxis':'Events','xaxis':'Nvert','logy':'True' , 'var':'nVert',                               'bin_set':(False,25),          'varname':'nVert',      'binlabel':1,  'bin':(50,0,50)},\
{'ndiv':False,'yaxis':'Events','xaxis':'Jet_btagCSV','logy':'True' , 'var':'Jet_btagCSV',                             'bin_set':(False,25),          'varname':'Jet_btagCSV',      'binlabel':1,  'bin':(50,0,2)},\
#{'ndiv':False,'yaxis':'Events','xaxis':'#Delta#Phi(met,l)','logy':'True' , 'var':'acos(cos(met_phi-LepGood_phi[0]))', 'bin_set':False  ,    'varname':'deltaPhi_metl',      'binlabel':1,  'bin':(50,0,3.14)},\
  ]

if test :
  plots = [plots[0]]
  lepSels = [lepSels[2]]

#if presel_1b :
#  #plots = [plots[0]]
#  #lepSels = [lepSels[2]]

if not draw_signal :
  signals = []
topWeight = [("TopPtWeight","topPt"),(top_ISR_weight,"ISR"),("(1)","non")]
#weight_str_plot = reweight
#print topWeight[top_index][1]
plots = [plots[iplot]]
lepSels = [lepSels[lepSel_index]]
if unblind : 
  reweight      = '(weight*12900)/3000'
  lepSels[0]["chain"] = getChain([single_ele_unblind,single_mu_unblind],histname="",treeName="Events")
  #weight_str_plot = reweight
  #weight_str_signal_plot = reweight

for lepSel in lepSels:
  path = "/afs/hephy.at/user/e/easilar/www/Moriond2017/plots/"+lepSel['label']+add_cut[1]
  if not os.path.exists(path):
    os.makedirs(path)
  print lepSel['label']
  print "====== "
  presel = "&&".join([lepSel['cut'],lepSel['veto'],"Jet_pt[1]>80",bkg_filters,add_cut[0]])
  sig_presel = "&&".join([lepSel['cut'],lepSel['veto'],"Jet_pt[1]>80",add_cut[0]]) #"flag_crazy_jets"
  data_presel = "&&".join([lepSel['cut'],lepSel['veto'],lepSel['trigger_xor'],filters,"Jet_pt[1]>80",add_cut[0]])
  print "DATA Presel" , data_presel
  print "MC presel " , presel
  print "Signal presel " , sig_presel
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
          tmp_yield = 0
          for bkg in bkg_samples:
            bla_Name, Cut = nameAndCut(stb, htb, srNJet, btb=bkg['cut'], presel="&&".join([bkg["add_Cut"],presel]), btagVar =  btagVarString)
            print 8*"*"
            print bkg["sample"], Cut
            print "WEIGHT : " ,  "*".join([weight_str_plot , bkg["weight"]])
            bin[srNJet][stb][htb][p['varname']][bkg['sample']] = getPlotFromChain(bkg['chain'], p['var'], p['bin'], cutString = Cut, weight = "*".join([weight_str_plot , bkg["weight"]]) , binningIsExplicit=False ,addOverFlowBin='both',variableBinning=p["bin_set"])
            tmp_yield += bin[srNJet][stb][htb][p['varname']][bkg['sample']].Integral()
          tot_yield = tmp_yield
          bla_Name, Cut = nameAndCut(stb, htb,srNJet, btb=nbtag, presel=sig_presel, btagVar =  btagVarString)
          bin[srNJet][stb][htb][p['varname']]['signals'] = {}
          for sig in signals:
            bin[srNJet][stb][htb][p['varname']]['signals'][sig["name"]] = getPlotFromChain(sig['chain'], p['var'], p['bin'], cutString = Cut , weight = "*".join([weight_str_signal_plot , btag_weight]), binningIsExplicit=False ,addOverFlowBin='both',variableBinning=p["bin_set"]) 
          bla_Name, Cut = nameAndCut(stb, htb,srNJet, btb=nbtag, presel=data_presel, btagVar =  btagVarString)
          print "Data" , Cut
          bin[srNJet][stb][htb][p['varname']]['data'] = getPlotFromChain(lepSel['chain'], p['var'], p['bin'], cutString = Cut , weight = "(1)", binningIsExplicit=False,addOverFlowBin='both',variableBinning=p["bin_set"])
          data_yield = bin[srNJet][stb][htb][p['varname']]['data'].Integral()
          print data_yield , tot_yield
          if tot_yield > 0.0 : bin[srNJet][stb][htb]['scale_fac'] = float(data_yield)/float(tot_yield)
          else : bin[srNJet][stb][htb]['scale_fac'] = 1 
          print "scale factor is :" , bin[srNJet][stb][htb]['scale_fac']
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
          latex = ROOT.TLatex()
          latex.SetNDC()
          latex.SetTextSize(0.05)
          latex.SetTextAlign(11)
          
          leg = ROOT.TLegend(0.65,0.5,0.93,0.925)
          leg.SetBorderSize(1)
          leg_sig = ROOT.TLegend(0.3,0.8,0.6,0.925)
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
            #if "ttjets" in bkg["sample"].lower() : histo.Scale(bin[srNJet][stb][htb]['scale_fac'])
            histo.Scale(bin[srNJet][stb][htb]['scale_fac'])
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
               #histo.GetYaxis().SetTitle(p['yaxis'])
            if not p['ndiv']:
               histo.GetYaxis().SetTitle(p['yaxis'])
            #leg.AddEntry(histo, bkg['tex'],"f")
            h_Stack.Add(histo)
            del histo
          #h_Stack.Draw("Bar")
          
          if p["bin_set"][0]: stack_hist=ROOT.TH1F("stack_hist","stack_hist", p['bin'][0],p['bin'][1]) 
          else: stack_hist=ROOT.TH1F("stack_hist","stack_hist",p['bin'][0],p['bin'][1],p['bin'][2])
          stack_hist.Merge(h_Stack.GetHists())

          max_bin = stack_hist.GetMaximum()*10000

          h_Stack.SetMaximum(max_bin)
          h_Stack.SetMinimum(0.00001)
          #h_Stack.SetMinimum(0.11)
          
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
            h_sig.SetLineWidth(3)
            h_sig.SetTitle("")
            h_sig.Draw("HistoSame")
            leg_sig.AddEntry(h_sig, sig['tex'],"l")
            del h_sig
          h_data.Draw("E1 Same")
          if p['ndiv']:
            h_data.GetXaxis().SetNdivisions(505)
            #h_data.GetYaxis().SetTitle(p['yaxis']+str(p['binlabel'])+' GeV')
            h_data.GetYaxis().SetTitle(p['yaxis'])
          if not p['ndiv']:
            h_data.GetYaxis().SetTitle(p['yaxis'])
          print "Integral of BKG:" , stack_hist.Integral()
          print "Integral of BKG over 200:" , stack_hist.Integral(20,100)
          print "Integral of DATA:" , h_data.Integral()

          leg.AddEntry(h_data, "Data","PL")
          for bkg in reversed(bkg_samples):
            color = bkg['color']
            histo = bin[srNJet][stb][htb][p['varname']][bkg['sample']]
            histo.SetFillColor(color)
            histo.SetLineColor(ROOT.kBlack)
            histo.SetLineWidth(1)
            leg.AddEntry(histo, bkg['tex'],"f")
 
          leg.SetFillColor(0)
          leg.SetLineColor(0)
          leg.Draw()
          leg_sig.SetFillColor(0)
          leg_sig.SetLineColor(0)
          leg_sig.Draw()
          if all_MB or test:
            latex.DrawLatex(0.32,0.6 ,nJetBinName(srNJet))
            latex.DrawLatex(0.32,0.55,varBinNamewithUnit(stb,'L_{T}',"GeV"))
            latex.DrawLatex(0.32,0.5 ,varBinNamewithUnit(htb,'H_{T}',"GeV"))
          latex.DrawLatex(0.65,0.4 ,"Scale Factor:"+str(round(bin[srNJet][stb][htb]['scale_fac'],2)))
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
          if p["bin_set"][0] : Func = ROOT.TF1('Func',"[0]",p['bin'][1][0],p['bin'][1][-1])
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
          h_ratio.SetMinimum(0.01)
          #h_ratio.SetMaximum(min(rmax,4.99))
          h_ratio.SetMaximum(min(rmax,1.9))
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
          cb.SaveAs(bin[srNJet][stb][htb]['path']+p['varname']+'_withMET.png')
          cb.SaveAs(bin[srNJet][stb][htb]['path']+p['varname']+'_withMET.pdf')
          cb.SaveAs(bin[srNJet][stb][htb]['path']+p['varname']+'_withMET.root')
          if test:
            #cb.SaveAs("/afs/cern.ch/user/e/easilar/public/html/Notes/notes/SUS-15-006/trunk/fig/zerob/LT_zerob.pdf")
            #cb.SaveAs("/afs/cern.ch/user/e/easilar/public/html/Notes/notes/SUS-15-006/trunk/fig/zerob/"+p['varname']+".pdf")
            cb.SaveAs("/afs/cern.ch/user/e/easilar/public/html/Notes/notes/SUS-15-006/trunk/TwikiPlots/dPhi_st450_ht500-1000_njet6-7_nbtagEq0.pdf")
            cb.SaveAs("/afs/cern.ch/user/e/easilar/public/html/Notes/notes/SUS-15-006/trunk/TwikiPlots/dPhi_st450_ht500-1000_njet6-7_nbtagEq0.root")
          cb.Clear()
          del h_Stack

