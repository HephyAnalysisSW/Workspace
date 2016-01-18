import ROOT
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getYieldFromChain,getPlotFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from Workspace.RA4Analysis.cmgTuples_Data25ns_miniAODv2_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
from Workspace.RA4Analysis.signalRegions import signalRegion3fb
from cutFlow_helper import *
from math import *
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
maxN = -1
ROOT.gStyle.SetOptStat(0)
lumi = 2250##pb

path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/2p3fb/diLep_syst_study_results/"
if not os.path.exists(path):
  os.makedirs(path)

signalRegion3fbReduced = {(0, -1):  {(0, -1): {(0, -1):  {'deltaPhi': 1.0}}}}

#SR = signalRegion3fbReduced
SR = signalRegion3fb
btagVarString = 'nBJetMediumCSV30'

lepSels = [
{'cut':'nTightHardLeptons==2' , 'veto':'nLooseHardLeptons==2&&nLooseSoftLeptons==0',\
 'chain': getChain([single_ele_Run2015D,single_mu_Run2015D],maxN=maxN,histname="",treeName="Events") ,\
 'trigWeight': "0.94" ,\
  'label':'_lep_', 'str':'1 $lep$' , 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'}\
]

bkg_samples=[
{'sample':'TTVH',     "weight":"(1)"            ,"cut":(0,0) , "name":TTV_25ns ,'tex':'t#bar{t}+W/Z/H','color':ROOT.kOrange-3},
{"sample":"singleTop","weight":"(1)"            ,"cut":(0,0) , "name":singleTop_25ns,"tex":"single top",'color': ROOT.kViolet+5},
{"sample":"DY",       "weight":"(1)"            ,"cut":(0,0) , "name":DY_25ns,"tex":"DY + jets",'color':ROOT.kRed-6},
{"sample":"QCD",      "weight":"(1)"            ,"cut":(0,0) , "name":QCDHT_25ns, "tex":"QCD","color":ROOT.kCyan-6},
{"sample":"WJets",    "weight":"weightBTag0_SF" ,"cut":(0,-1) , "name":WJetsHTToLNu_25ns,"tex":"W + jets","color":ROOT.kGreen-2},
]

for bkg in bkg_samples:
    bkg['chain'] = getChain(bkg['name'],maxN=maxN,histname="",treeName="Events")

c_tt = {"sample":"ttJets", "chain":getChain(TTJets_combined, maxN=maxN,histname="",treeName="Events"),  "weight":"weightBTag0_SF" ,"cut":(0,-1) , "name":TTJets_combined, "tex":"ttbar + jets",'color':ROOT.kBlue-4}
c_tt_diLep = c_tt
c_tt_diLep["tex"] = "tt diLep"
c_tt_diLep["color"] = ROOT.kCyan-10
plots =[\
{'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}+lost','logy':False , 'var':'DL_nJet_lepToKeep_AddLep1ov3Met',                      'varname':'nJet30',                   'binlabel':1,  'bin':(6,3,9)},\
{'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}+lost','logy':False , 'var':'DL_nJet_lepToDiscard_AddLep1ov3Met',                      'varname':'nJet30',                   'binlabel':1,  'bin':(6,3,9)},\
  ]

diLep = "(ngenLep+ngenTau)==2"
not_diLep = "(ngenLep+ngenTau)!=2"
delta_Phi = "deltaPhi_Wl<0.5"
diLep_presel = "DL_HT_lepToKeep_AddLep1ov3Met>500&&DL_ST_lepToKeep_AddLep1ov3Met>250&&DL_nJet_lepToKeep_AddLep1ov3Met>=4"
diLep_presel_1 = "DL_HT_lepToDiscard_AddLep1ov3Met>500&&DL_ST_lepToDiscard_AddLep1ov3Met>250&&DL_nJet_lepToDiscard_AddLep1ov3Met>=4"
lepSel = lepSels[0]
presel = "&&".join([lepSel['cut'],lepSel['veto'],filters,diLep_presel])  
presel_1 = "&&".join([lepSel['cut'],lepSel['veto'],filters,diLep_presel_1])  
data_presel = "&&".join([lepSel['cut'],lepSel['veto'],lepSel['trigger'],filters,diLep_presel])
data_presel_1 = "&&".join([lepSel['cut'],lepSel['veto'],lepSel['trigger'],filters,diLep_presel_1])
nbTags = (0,0) 
nJet = (4,-1)
htbin = (0,-1)
bin = {}
for srNJet in sorted(SR):
  bin[srNJet]={}
  for stb in sorted(SR[srNJet]):
    bin[srNJet][stb] = {}
    for htb in sorted(SR[srNJet][stb]):
      bin[srNJet][stb][htb] = {}
      deltaPhiCut = SR[srNJet][stb][htb]['deltaPhi']
      Name, bla_Cut = nameAndCut(stb, htb, srNJet, btb=(0,0), presel="(1)", btagVar =  btagVarString)
      p = plots[0]
      bin[srNJet][stb][htb][p['varname']] = {}
      for bkg in bkg_samples:
        bla_Name, Cut = nameAndCut(stb, htbin, nJet, btb=bkg['cut'], presel="(1)", btagVar =  btagVarString, stVar ='DL_ST_lepToKeep_AddLep1ov3Met')
        weight_str = lepSel['trigWeight']+"*"+bkg['weight']+"*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*puReweight_true_max4*TopPtWeight*"
        bin[srNJet][stb][htb][p['varname']][bkg['sample']] = getPlotFromChain(bkg['chain'], p['var'], p['bin'], cutString = "&&".join([presel,Cut]), weight = weight_str+"weight*"+str(lumi)+"/3000", binningIsExplicit=False, addOverFlowBin='both')
        bla_Name, Cut_1 = nameAndCut(stb, htbin, nJet, btb=bkg['cut'], presel="(1)", btagVar =  btagVarString, stVar ='DL_ST_lepToDiscard_AddLep1ov3Met')
        bin[srNJet][stb][htb][p['varname']][bkg['sample']+"+1"] = getPlotFromChain(bkg['chain'], plots[1]['var'], p['bin'], cutString = "&&".join([presel_1,Cut_1]), weight = weight_str+"weight*"+str(lumi)+"/3000", binningIsExplicit=False, addOverFlowBin='both')
      bla_Name, Cut = nameAndCut(stb, htbin, nJet, btb=c_tt['cut'], presel="(1)", btagVar =  btagVarString,stVar ='DL_ST_lepToKeep_AddLep1ov3Met')
      bla_Name, Cut_1 = nameAndCut(stb, htbin, nJet, btb=c_tt['cut'], presel="(1)", btagVar =  btagVarString,stVar ='DL_ST_lepToDiscard_AddLep1ov3Met')
      weight_str = lepSel['trigWeight']+"*"+bkg['weight']+"*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*puReweight_true_max4*TopPtWeight*"
      bin[srNJet][stb][htb][p['varname']][c_tt['sample']] = getPlotFromChain(c_tt['chain'], p['var'], p['bin'], cutString = "&&".join([presel,not_diLep,Cut]), weight = weight_str+"weight*"+str(lumi)+"/3000", binningIsExplicit=False, addOverFlowBin='both')
      bin[srNJet][stb][htb][p['varname']][c_tt['sample']+"+1"] = getPlotFromChain(c_tt['chain'], plots[1]['var'], p['bin'], cutString = "&&".join([presel_1,not_diLep,Cut_1]), weight = weight_str+"weight*"+str(lumi)+"/3000", binningIsExplicit=False, addOverFlowBin='both')
      bin[srNJet][stb][htb][p['varname']][c_tt['sample']+'diLep'] = getPlotFromChain(c_tt['chain'], p['var'], p['bin'], cutString = "&&".join([presel,diLep,Cut]), weight = weight_str+"weight*"+str(lumi)+"/3000", binningIsExplicit=False, addOverFlowBin='both')
      bin[srNJet][stb][htb][p['varname']][c_tt['sample']+'diLep+1'] = getPlotFromChain(c_tt['chain'], plots[1]['var'], p['bin'], cutString = "&&".join([presel_1,diLep,Cut_1]), weight = weight_str+"weight*"+str(lumi)+"/3000", binningIsExplicit=False, addOverFlowBin='both')
      bla_Name, Cut = nameAndCut(stb, htbin, nJet, btb=(0,0), presel="(1)", btagVar =  btagVarString , stVar ='DL_ST_lepToKeep_AddLep1ov3Met')
      bla_Name, Cut_1 = nameAndCut(stb, htbin, nJet, btb=(0,0), presel="(1)", btagVar =  btagVarString , stVar ='DL_ST_lepToDiscard_AddLep1ov3Met')
      print "data Cut:" , "&&".join([data_presel,Cut])
      bin[srNJet][stb][htb][p['varname']]['data'] = getPlotFromChain(lepSel['chain'], p['var'], p['bin'], cutString = "&&".join([data_presel,Cut]) , weight = "(1)", binningIsExplicit=False, addOverFlowBin='both')
      bin[srNJet][stb][htb][p['varname']]['data+1'] = getPlotFromChain(lepSel['chain'], plots[1]['var'], p['bin'], cutString = "&&".join([data_presel_1,Cut_1]) , weight = "(1)", binningIsExplicit=False, addOverFlowBin='both')
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
        #histo = bin[srNJet][stb][htb][p['varname']][bkg['sample']+"+1"]
        #histo.SetFillColor(color)
        #h_Stack.Add(histo)
        #del histo
        histo = bin[srNJet][stb][htb][p['varname']][bkg['sample']]
        histo.Add(bin[srNJet][stb][htb][p['varname']][bkg['sample']+"+1"])
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
      #histo = bin[srNJet][stb][htb][p['varname']][c_tt['sample']+"+1"]
      #histo.SetFillColor(ROOT.kBlue-4)
      #h_Stack.Add(histo)
      #del histo
      histo = bin[srNJet][stb][htb][p['varname']][c_tt['sample']]
      histo.Add(bin[srNJet][stb][htb][p['varname']][c_tt['sample']+"+1"])
      histo.SetFillColor(ROOT.kBlue-4)
      histo.SetLineColor(ROOT.kBlack)
      histo.SetLineWidth(2)
      histo.GetXaxis().SetTitle(p['xaxis'])
      histo.SetTitle("")
      histo.GetYaxis().SetTitleSize(2) 
      h_Stack.Add(histo)
      leg.AddEntry(histo, 'tt rest',"f")
      del histo
      #histo = bin[srNJet][stb][htb][p['varname']][c_tt['sample']+'diLep+1']
      #histo.SetFillColor(c_tt_diLep['color'])
      #h_Stack.Add(histo)
      #del histo
      histo = bin[srNJet][stb][htb][p['varname']][c_tt['sample']+'diLep']
      histo.Add(bin[srNJet][stb][htb][p['varname']][c_tt['sample']+'diLep+1'])
      histo.SetFillColor(c_tt_diLep['color'])
      histo.SetLineColor(ROOT.kBlack)
      histo.SetLineWidth(2)
      histo.GetXaxis().SetTitle(p['xaxis'])
      histo.SetTitle("")
      histo.GetYaxis().SetTitleSize(2) 
      h_Stack.Add(histo)
      leg.AddEntry(histo, 'tt diLep',"f")
      h_Stack.Draw("Bar")
      #h_Stack.SetAxisRange(0.11,(h_Stack.GetMaximum())*(5),"Y")
      maximum = h_Stack.GetMaximum()*5
      h_Stack.SetMaximum(maximum)
      h_Stack.SetMinimum(0.11)
      color = ROOT.kBlack
      h_data_1 = bin[srNJet][stb][htb][p['varname']]['data+1']
      h_data = bin[srNJet][stb][htb][p['varname']]['data']
      h_data.Add(h_data_1)
      h_data.SetMarkerStyle(20)
      h_data.SetMarkerSize(1.8)
      h_data.SetLineColor(color)
      h_data.GetXaxis().SetTitle(p['xaxis'])
      h_data.SetTitle("")
      h_data.GetYaxis().SetTitleSize(0.05)
      h_data.GetYaxis().SetLabelSize(0.05)
      h_data.Draw("E1P")
      print "data mean:" , h_data.GetMean()
      h_data.SetAxisRange(0.11,(h_Stack.GetMaximum())*(5),"Y")
      #h_data.SetMaximum(200)
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
      latex.DrawLatex(0.75,0.958,"#bf{L=2.3 fb^{-1} (13 TeV)}")
      #if nJet[1] == -1: latex.DrawLatex(0.6,0.83,"N_{Jets}#geq"+str(nJet[0]))
      #if nJet[1] != -1: latex.DrawLatex(0.6,0.83,str(nJet[0])+"#leqN_{Jets}#leq"+str(nJet[1]))
      latex.DrawLatex(0.6,0.88,"#bf{N_{bjets}="+str(nbTags[0])+"}")
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
      h_ratio.SetMaximum(4)
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
      h_ratio.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_allWeights_diLep_4_Ratio.root')
      Func.Draw("same")
      cb.Draw()
      cb.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_allWeights_diLep_4_.png')
      cb.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_allWeights_diLep_4_.pdf')
      cb.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_allWeights_diLep_4_.root')
      cb.Clear()
      del h_Stack
            


