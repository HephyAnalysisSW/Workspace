import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getYieldFromChain,getPlotFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from Workspace.RA4Analysis.cmgTuples_Data25ns_Promtv2_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_postProcessed import *
from Workspace.RA4Analysis.signalRegions import signalRegion3fb
from cutFlow_helper import *
from general_config import *

from math import *
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
maxN = -1
ROOT.gStyle.SetOptStat(0)
sample_lumi =3000
#lumi = 804##pb
#lumi_label = 2.571
reweight      = '(weight*'+str(lumi)+')/'+str(sample_lumi)
filters = "(Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter)"
weight_str = weight_str_plot
path = "/afs/hephy.at/user/e/easilar/www/data/Run2016B/2571pb/diLep_syst_study_results/"
if not os.path.exists(path):
  os.makedirs(path)

presel = True

if presel :
  #btag_weight =  "(weightBTag1p_SF)"
  #btag_weight =  "(weightBTag0_SF)"
  btagVarString = 'nBJetMediumCSV30'
  SR = {(3,-1):{(250,-1):{(500,-1):{"deltaPhi":1}}}}
  nbtag = (0,0)

lepSels = [
{'cut':'nTightHardLeptons==2' , 'veto':'nLooseHardLeptons==2&&nLooseSoftLeptons==0',\
 'chain': getChain([single_ele_Run2016B,single_mu_Run2016B],maxN=maxN,histname="",treeName="Events") ,\
  'label':'_lep_', 'str':'1 $lep$' , 'trigger': trigger}\
]

ngenTau = "Sum$(abs(genTau_grandmotherId)==6&&abs(genTau_motherId)==24)"
ngenLep = "Sum$(abs(genLep_grandmotherId)==6&&abs(genLep_motherId)==24)"

bkg_samples=[
{'sample':'TTVH',           "weight":"(1)" ,"cut":nbtag,"add_Cut":"(1)","name":TTV ,'tex':'t#bar{t}V','color':ROOT.kOrange-3},
{"sample":"DiBosons",       "weight":"(1)" ,"cut":nbtag ,"add_Cut":"(1)","name":diBoson ,"tex":"WW/WZ/ZZ","color":ROOT.kRed+3},
{"sample":"DY",             "weight":"(1)" ,"cut":nbtag ,"add_Cut":"(1)","name":DY_madgraph,"tex":"DY + jets",'color':ROOT.kRed-6},
{"sample":"singleTop",      "weight":"(1)" ,"cut":nbtag ,"add_Cut":"(1)","name":singleTop_lep,"tex":"t/#bar{t}",'color': ROOT.kViolet+5},
{"sample":"QCD",            "weight":"(1)" ,"cut":nbtag ,"add_Cut":"(1)","name":QCDHT, "tex":"QCD","color":ROOT.kCyan-6},
{"sample":"WJets",          "weight":"(1)" ,"cut":nbtag ,"add_Cut":"(1)","name":WJetsHTToLNu,"tex":"W + jets","color":ROOT.kGreen-2},
{"sample":"ttJets_diLep",   "weight":"(1)" ,"cut":nbtag ,"add_Cut":"(("+ngenLep+"+"+ngenTau+")==2)","name":TTJets_Lep, "tex":"t#bar{t} ll + jets",'color':ROOT.kBlue},
{"sample":"ttJets_semiLep", "weight":"(1)" ,"cut":nbtag ,"add_Cut":"(!(("+ngenLep+"+"+ngenTau+")==2))","name":TTJets_Lep, "tex":"t#bar{t} l + jets",'color':ROOT.kBlue-7}        
]

for bkg in bkg_samples:
    bkg['chain'] = getChain(bkg['name'],maxN=maxN,histname="",treeName="Events")

plots =[\
{'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}+lost','logy':False , 'var':'DL_nJet_lepToKeep_AddLep1ov3Met',     'stVar':'DL_ST_lepToKeep_AddLep1ov3Met',     'htVar':'DL_HT_lepToKeep_AddLep1ov3Met',                   'varname':'nJet30',                   'binlabel':1,  'bin':(7,3,10)},\
#{'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}+lost','logy':False , 'var':'DL_nJet_lepToKeep_notAddLepMet',      'stVar':'DL_ST_lepToKeep_notAddLepMet',      'htVar':'DL_HT_lepToKeep_notAddLepMet',                    'varname':'nJet30',                   'binlabel':1,  'bin':(6,4,10)},\
#{'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}+lost','logy':False , 'var':'DL_nJet_lepToKeep_AddLepMet',         'stVar':'DL_ST_lepToKeep_AddLepMet',         'htVar':'DL_HT_lepToKeep_AddLepMet',                       'varname':'nJet30',                   'binlabel':1,  'bin':(6,4,10)},\
{'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}+lost','logy':False , 'var':'DL_nJet_lepToDiscard_AddLep1ov3Met',  'stVar':'DL_ST_lepToDiscard_AddLep1ov3Met',  'htVar':'DL_HT_lepToDiscard_AddLep1ov3Met',                'varname':'nJet30',                   'binlabel':1,  'bin':(7,3,10)},\
#{'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}+lost','logy':False , 'var':'DL_nJet_lepToDiscard_notAddLepMet',   'stVar':'DL_ST_lepToDiscard_notAddLepMet',   'htVar':'DL_HT_lepToDiscard_notAddLepMet',                 'varname':'nJet30',                   'binlabel':1,  'bin':(6,4,10)},\
#{'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}+lost','logy':False , 'var':'DL_nJet_lepToDiscard_AddLepMet',      'stVar':'DL_ST_lepToDiscard_AddLepMet',      'htVar':'DL_HT_lepToDiscard_AddLepMet',                    'varname':'nJet30',                   'binlabel':1,  'bin':(6,4,10)},\
  ]

lepSel = lepSels[0]
presel = "&&".join([lepSel['cut'],lepSel['veto'],"Jet_pt[1]>80"])
data_presel = "&&".join([lepSel['cut'],lepSel['veto'],lepSel['trigger'],filters,"Jet_pt[1]>80"])
bin = {}
for srNJet in sorted(SR):
  bin[srNJet]={}
  for stb in sorted(SR[srNJet]):
    bin[srNJet][stb] = {}
    for htb in sorted(SR[srNJet][stb]):
      bin[srNJet][stb][htb] = {}
      deltaPhiCut = SR[srNJet][stb][htb]['deltaPhi']
      Name, bla_Cut = nameAndCut(stb, htb, srNJet, btb=nbtag, presel="(1)", btagVar =  btagVarString)
      bin[srNJet][stb][htb][plots[0]['varname']] = {}
      for i,p in enumerate(plots):
        for bkg in bkg_samples:
          print bkg['name']
          bla_Name, Cut = nameAndCut(stb, htb, srNJet, btb=bkg['cut'], presel=presel, btagVar =  btagVarString, stVar =p['stVar'], htVar = p['htVar'], njetVar= p['var'])
          bin[srNJet][stb][htb][p['varname']][bkg['sample']+str(i)] = getPlotFromChain(bkg['chain'], p['var'], p['bin'], cutString = "&&".join([presel,bkg["add_Cut"],Cut]), weight = "*".join([weight_str,bkg["weight"]]), binningIsExplicit=False, addOverFlowBin='both')
          print bkg['sample']+str(i)
      for i,p in enumerate(plots):
        bla_Name, Cut = nameAndCut(stb, htb, srNJet, btb=nbtag, presel=data_presel, btagVar =  btagVarString ,stVar =p['stVar'], htVar = p['htVar'], njetVar= p['var'])
        print 'data'+str(i)
        print "data Cut:" , "&&".join([data_presel,Cut])
        bin[srNJet][stb][htb][p['varname']]['data'+str(i)] = getPlotFromChain(lepSel['chain'], p['var'], p['bin'], cutString = Cut , weight = "(1)", binningIsExplicit=False, addOverFlowBin='both')
      bin[srNJet][stb][htb]['label'] = Name
      bin[srNJet][stb][htb]['path'] = path+Name


#for p in plots:
p = plots[0]
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
        histo = bin[srNJet][stb][htb][p['varname']][bkg['sample']+str(0)]
        for i in range(len(plots)-1) : 
          histo.Add(bin[srNJet][stb][htb][p['varname']][bkg['sample']+str(i+1)])
        #histo.Scale(2)
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
      maximum = h_Stack.GetMaximum()*1.2
      maximum = 200
      h_Stack.SetMaximum(maximum)
      h_Stack.SetMinimum(0.11)
      color = ROOT.kBlack
      h_data = bin[srNJet][stb][htb][p['varname']]['data'+str(0)]
      for i in range(len(plots)-1) :
        h_data_1 = bin[srNJet][stb][htb][p['varname']]['data'+str(i+1)]
        h_data.Add(h_data_1)
        del h_data_1
      h_data.SetMarkerStyle(20)
      h_data.SetMarkerSize(1.2)
      h_data.SetLineColor(color)
      h_data.GetXaxis().SetTitle(p['xaxis'])
      h_data.SetTitle("")
      h_data.GetYaxis().SetTitleSize(0.05)
      h_data.GetYaxis().SetLabelSize(0.05)
      h_data.Draw("E1P")
      print "data mean:" , h_data.GetMean()
      #h_data.SetAxisRange(0.11,(h_Stack.GetMaximum())*(1.2),"Y")
      h_data.SetMaximum(maximum)
      #h_data.SetMinimum(0.11)
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
      latex.DrawLatex(0.75,0.958,"#bf{L=2.6 fb^{-1} (13 TeV)}")
      #if nJet[1] == -1: latex.DrawLatex(0.6,0.83,"N_{Jets}#geq"+str(nJet[0]))
      #if nJet[1] != -1: latex.DrawLatex(0.6,0.83,str(nJet[0])+"#leqN_{Jets}#leq"+str(nJet[1]))
      latex.DrawLatex(0.6,0.88,"#bf{N_{bjets}==0}")
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
      print "mean:" , h_ratio.GetMean()
      h_ratio.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_allWeights_diLep_Ratio_eq0b.root')
      Func.Draw("same")
      cb.Draw()
      cb.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_diLep_eq0b_nJet3_.png')
      cb.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_diLep_eq0b_nJet3_.pdf')
      cb.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_diLep_eq0b_nJet3_.root')
      #cb.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_diLep_lg1b_nJet4_skim350_.png')
      #cb.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_diLep_lg1b_nJet4_skim350_.pdf')
      #cb.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_diLep_lg1b_nJet4_skim350_.root')
      cb.Clear()
      del h_Stack
            


