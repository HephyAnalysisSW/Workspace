import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getYieldFromChain,getPlotFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from Workspace.RA4Analysis.cmgTuples_Data25ns_miniAODv2_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed_1 import *
from Workspace.RA4Analysis.signalRegions import signalRegion3fb
from cutFlow_helper import *
from general_config import *

from math import *
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
maxN = -1
ROOT.gStyle.SetOptStat(0)

path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/2p25fb/diLep_syst_study_results/"
if not os.path.exists(path):
  os.makedirs(path)

presel = True

if presel :
  SR = {(3,-1):{(250,-1):{(500,-1):{"deltaPhi":1}}}}
  #btag_weight = "(weightBTag0_SF)"
  btag_weight =  "(weightBTag1p_SF)"
  btagVarString = 'nBJetMediumCSV30'
  #nbtag = (0,0)
  nbtag = (1,-1)


lepSels = [
{'cut':'((!isData&&singleLeptonic)||(isData&&((eleDataSet&&singleElectronic)||(muonDataSet&&singleMuonic))))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain([single_ele_Run2015D,single_mu_Run2015D],maxN=maxN,histname="",treeName="Events") ,\
 'trigWeight': "0.94" ,\
  'label':'_lep_', 'str':'1 $lep$' , 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'},\
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

plots =[\
{'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}','logy':False , 'var':'nJet30',                      'varname':'nJet30',                   'binlabel':1,  'bin':(7,3,10)},\
  ]

lepSel = lepSels[0]
presel = "&&".join([lepSel['cut'],lepSel['veto'],"Jet_pt[1]>80&&abs(LepGood_eta[0])<2.4","deltaPhi_Wl<0.75"])
data_presel = "&&".join([lepSel['cut'],lepSel['veto'],lepSel['trigger'],filters,"Jet_pt[1]>80&&abs(LepGood_eta[0])<2.4","deltaPhi_Wl<0.75"])
weight_str = weight_str_CV

bin = {}
for srNJet in sorted(SR):
  print srNJet
  bin[srNJet]={}
  for stb in sorted(SR[srNJet]):
    bin[srNJet][stb] = {}
    for htb in sorted(SR[srNJet][stb]):
      bin[srNJet][stb][htb] = {}
      deltaPhiCut = SR[srNJet][stb][htb]['deltaPhi']
      Name, bla_Cut = nameAndCut(stb, htb, srNJet, btb=nbtag, presel="(1)", btagVar =  btagVarString)
      for p in plots:
        bin[srNJet][stb][htb][p['varname']] = {}
        for bkg in bkg_samples:
          bla_Name, Cut = nameAndCut(stb, htb, srNJet, btb=bkg['cut'],  presel="&&".join([bkg["add_Cut"],presel]) , btagVar =  btagVarString)
          bin[srNJet][stb][htb][p['varname']][bkg['sample']] = getPlotFromChain(bkg['chain'], p['var'], p['bin'], cutString = Cut, weight = "*".join([weight_str,bkg['weight']]), binningIsExplicit=False, addOverFlowBin='both')
        bla_Name, Cut = nameAndCut(stb, htb, srNJet, btb=nbtag, presel=data_presel, btagVar =  btagVarString)
        print "data cut:" , Cut
        bin[srNJet][stb][htb][p['varname']]['data'] = getPlotFromChain(lepSel['chain'], p['var'], p['bin'], cutString = Cut, weight = "(1)", binningIsExplicit=False, addOverFlowBin='both')
      bin[srNJet][stb][htb]['label'] = Name
      bin[srNJet][stb][htb]['path'] = path+Name

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
  #      leg = ROOT.TLegend(0.45,0.8,0.65,0.94)
        leg = ROOT.TLegend(0.75,0.6,0.9,0.9)
        leg.SetBorderSize(1)
        Pad1 = ROOT.TPad("Pad1", "Pad1", 0, 0.35, 1, 0.9)
        #Pad1.SetLogy()
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
        h_Stack.SetMaximum(1500)
        h_Stack.SetMinimum(0.11)
        color = ROOT.kBlack
        h_data = bin[srNJet][stb][htb][p['varname']]['data']
        h_data.SetMarkerStyle(20)
        h_data.SetMarkerSize(1.2)
        h_data.SetLineColor(color)
        h_data.GetXaxis().SetTitle(p['xaxis'])
        h_data.SetTitle("")
        h_data.GetYaxis().SetTitleSize(0.05)
        h_data.GetYaxis().SetLabelSize(0.05)
        h_data.Draw("E1P")
        print "data mean :" , h_data.GetMean()
        bin[srNJet][stb][htb]['data_mean'] = h_data.GetMean() 
        h_data.SetMaximum(1500)
        h_data.SetMinimum(0.11)
        h_Stack.Draw("HistoSame")
        h_data.Draw("E1PSame")
        if p['ndiv']:
          h_data.GetXaxis().SetNdivisions(505)
          h_data.GetYaxis().SetTitle(p['yaxis']+str(p['binlabel'])+'GeV')
        if not p['ndiv']:
          h_data.GetYaxis().SetTitle(p['yaxis'])
        stack_hist=ROOT.TH1F("stack_hist","stack_hist",p['bin'][0],p['bin'][1],p['bin'][2])
        stack_hist.Merge(h_Stack.GetHists())
        print "Integral of BKG:" , stack_hist.Integral()
        print "Integral of Data:" , h_data.Integral()
        leg.AddEntry(h_data, "data","PL")
        leg.SetFillColor(0)
        leg.Draw()
        latex.DrawLatex(0.16,0.958,"#font[22]{CMS}"+" #font[12]{Preliminary}")
        latex.DrawLatex(0.75,0.958,"#bf{L=2.2 fb^{-1} (13 TeV)}")
        #if nJet[1] == -1: latex.DrawLatex(0.6,0.83,"N_{Jets}#geq"+str(nJet[0]))
        #if nJet[1] != -1: latex.DrawLatex(0.6,0.83,str(nJet[0])+"#leqN_{Jets}#leq"+str(nJet[1]))
        latex.DrawLatex(0.6,0.80,"#bf{N_{bjets}>="+str(nbtag[0])+"}")
        latex.DrawLatex(0.6,0.75,"#Delta#Phi<0.75")
        Pad1.RedrawAxis()
        cb.cd()
        Pad2 = ROOT.TPad("Pad2", "Pad2",  0, 0.04, 1, 0.35)
        Pad2.SetTopMargin(0)
        Pad2.SetBottomMargin(0.5)
        Pad2.SetLeftMargin(0.16)
        Pad2.SetRightMargin(0.05)
        Pad2.Draw()
        Pad2.cd()
        Func = ROOT.TF1('Func',"[0]",p['bin'][1],p['bin'][2])
        Func.SetParameter(0,1)
        Func.SetLineColor(2)
        h_ratio = h_data.Clone('h_ratio')
        h_ratio.SetMinimum(0.0)
        h_ratio.SetMaximum(2)
        h_ratio.Sumw2()
        h_ratio.SetStats(0)
        h_ratio.Divide(stack_hist)
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
        print "mean :" , h_ratio.GetMean()
        h_ratio.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_allWeights_Ratio_4_lg1b.root')
        Func.Draw("same")
        cb.Draw()
        cb.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_lg1b_0p75.png')
        cb.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_lg1b_0p75.pdf')
        cb.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_lg1b_0p75.root')
        cb.Clear()
        del h_Stack
            
pickle.dump(bin,file('/data/easilar/Spring15/25ns/data_mean_25Feb_0p75_lg1b_pkl','w'))

