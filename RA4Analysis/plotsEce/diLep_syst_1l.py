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
lumi = 2300##pb

path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/2p3fb/diLep_syst_study_results/"
if not os.path.exists(path):
  os.makedirs(path)

#signalRegion3fbReduced = {(4, -1):  {(250, -1): {(500, -1):  {'deltaPhi': 1.0}}}}

SR = signalRegion3fb
btagVarString = 'nBJetMediumCSV30'

lepSels = [
{'cut':'((!isData&&singleLeptonic)||(isData&&((eleDataSet&&singleElectronic)||(muonDataSet&&singleMuonic))))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain([single_ele_Run2015D,single_mu_Run2015D],maxN=maxN,histname="",treeName="Events") ,\
 'trigWeight': "0.94" ,\
  'label':'_lep_', 'str':'1 $lep$' , 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'},\
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
{'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}','logy':False , 'var':'nJet30',                      'varname':'nJet30',                   'binlabel':1,  'bin':(6,3,9)},\
  ]
diLep = "(ngenLep+ngenTau)==2"
not_diLep = "(ngenLep+ngenTau)!=2"
delta_Phi = "deltaPhi_Wl<0.5"
lepSel = lepSels[0]
presel = "&&".join([lepSel['cut'],lepSel['veto'],filters])  
data_presel = "&&".join([lepSel['cut'],lepSel['veto'],lepSel['trigger'],filters])
nbTags = (0,0) 
nJet = (4,-1)
htbin = (500,-1)
bin = {}
for srNJet in sorted(SR):
  print srNJet
  bin[srNJet]={}
  for stb in sorted(SR[srNJet]):
    bin[srNJet][stb] = {}
    for htb in sorted(SR[srNJet][stb]):
      bin[srNJet][stb][htb] = {}
      deltaPhiCut = SR[srNJet][stb][htb]['deltaPhi']
      Name, bla_Cut = nameAndCut(stb, htb, srNJet, btb=nbTags, presel="(1)", btagVar =  btagVarString)
      for p in plots:
        bin[srNJet][stb][htb][p['varname']] = {}
        for bkg in bkg_samples:
          bla_Name, Cut = nameAndCut(stb, htbin, nJet, btb=bkg['cut'], presel="(1)", btagVar =  btagVarString)
          weight_str = lepSel['trigWeight']+"*"+bkg['weight']+"*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*puReweight_true_max4*TopPtWeight*"
          bin[srNJet][stb][htb][p['varname']][bkg['sample']] = getPlotFromChain(bkg['chain'], p['var'], p['bin'], cutString = "&&".join([presel,Cut,"deltaPhi_Wl<"+str(deltaPhiCut)]), weight = weight_str+"weight*"+str(lumi)+"/3000", binningIsExplicit=False, addOverFlowBin='both')
        bla_Name, Cut = nameAndCut(stb, htbin, nJet, btb=c_tt['cut'], presel="(1)", btagVar =  btagVarString)
        weight_str = lepSel['trigWeight']+"*"+c_tt['weight']+"*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*puReweight_true_max4*TopPtWeight*"
        bin[srNJet][stb][htb][p['varname']][c_tt['sample']] = getPlotFromChain(c_tt['chain'], p['var'], p['bin'], cutString = "&&".join([presel,Cut,not_diLep,"deltaPhi_Wl<"+str(deltaPhiCut)]), weight = weight_str+"weight*"+str(lumi)+"/3000", binningIsExplicit=False, addOverFlowBin='both')
        bin[srNJet][stb][htb][p['varname']][c_tt['sample']+'diLep'] = getPlotFromChain(c_tt['chain'], p['var'], p['bin'], cutString = "&&".join([presel,Cut,diLep,"deltaPhi_Wl<"+str(deltaPhiCut)]), weight = weight_str+"weight*"+str(lumi)+"/3000", binningIsExplicit=False, addOverFlowBin='both')
        bla_Name, Cut = nameAndCut(stb, htbin, nJet, btb=nbTags, presel="(1)", btagVar =  btagVarString)
        print "data cut:" , Cut
        bin[srNJet][stb][htb][p['varname']]['data'] = getPlotFromChain(lepSel['chain'], p['var'], p['bin'], cutString = "&&".join([data_presel,Cut,"deltaPhi_Wl<"+str(deltaPhiCut)]) , weight = "(1)", binningIsExplicit=False, addOverFlowBin='both')
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
        histo = bin[srNJet][stb][htb][p['varname']][c_tt['sample']]
        histo.SetFillColor(ROOT.kBlue-4)
        histo.SetLineColor(ROOT.kBlack)
        histo.SetLineWidth(2)
        histo.GetXaxis().SetTitle(p['xaxis'])
        histo.SetTitle("")
        histo.GetYaxis().SetTitleSize(2) 
        h_Stack.Add(histo)
        leg.AddEntry(histo, 'tt rest',"f")
        del histo
        histo = bin[srNJet][stb][htb][p['varname']][c_tt['sample']+'diLep']
        histo.SetFillColor(c_tt_diLep['color'])
        histo.SetLineColor(ROOT.kBlack)
        histo.SetLineWidth(2)
        histo.GetXaxis().SetTitle(p['xaxis'])
        histo.SetTitle("")
        histo.GetYaxis().SetTitleSize(2) 
        h_Stack.Add(histo)
        leg.AddEntry(histo, 'tt diLep',"f")
        h_Stack.Draw("Bar")
        h_Stack.SetMaximum(2500)
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
        print "data mean :" , h_data.GetMean()
        h_data.SetMaximum(2500)
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
        latex.DrawLatex(0.75,0.958,"#bf{L=2.3 fb^{-1} (13 TeV)}")
        #if nJet[1] == -1: latex.DrawLatex(0.6,0.83,"N_{Jets}#geq"+str(nJet[0]))
        #if nJet[1] != -1: latex.DrawLatex(0.6,0.83,str(nJet[0])+"#leqN_{Jets}#leq"+str(nJet[1]))
        latex.DrawLatex(0.6,0.80,"#bf{N_{bjets}="+str(nbTags[0])+"}")
        latex.DrawLatex(0.6,0.75,"#Delta#Phi<"+str(SR[srNJet][stb][htb]['deltaPhi']))
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
        print "mean :" , h_ratio.GetMean()
        h_ratio.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_allWeights_Ratio_4.root')
        Func.Draw("same")
        cb.Draw()
        cb.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_allWeights_4.png')
        cb.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_allWeights_4.pdf')
        cb.SaveAs(bin[srNJet][stb][htb]['path']+'_'+p['varname']+'_allWeights_4.root')
        cb.Clear()
        del h_Stack
            


