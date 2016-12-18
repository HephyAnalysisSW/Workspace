import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from rCShelpers import *
import math
from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *
from Workspace.RA4Analysis.cmgTuples_Data25ns_Moriond2017_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Spring16_Moriond2017_MiniAODv2_postProcessed import *
from Workspace.RA4Analysis.general_config import *

ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.gStyle.SetOptStat(0)

cWJets  = getChain(WJetsHTToLNu,histname='')
cTTJets = getChain(TTJets_Comb,histname='')
cDY = getChain([DY_HT],histname='')#no QCD
maxN = -1
#lumi = 2.6
def getRCS(c, cut, dPhiCut, weight="weight"):
  #h = getPlotFromChain(c, "deltaPhi_Wl", [0,dPhiCut,pi], cutString=cut, binningIsExplicit=True,weight="weight*weightBTag0_SF")
  h = getPlotFromChain(c, "deltaPhi_Wl", [0,dPhiCut,pi], cutString=cut, binningIsExplicit=True,weight=weight)
  if h.GetBinContent(1)>0 and h.GetBinContent(2)>0:
    rcs = h.GetBinContent(2)/h.GetBinContent(1)
    rCSE_sim = rcs*sqrt(h.GetBinError(2)**2/h.GetBinContent(2)**2 + h.GetBinError(1)**2/h.GetBinContent(1)**2)
    rCSE_pred = rcs*sqrt(1./h.GetBinContent(2) + 1./h.GetBinContent(1))
    del h
    return {'rCS':rcs, 'rCSE_pred':rCSE_pred, 'rCSE_sim':rCSE_sim}
  else : return {'rCS':'Nan', 'rCSE_pred':'Nan', 'rCSE_sim':'Nan'}
  del h

lepSels = [
{'cut':'((!isData&&singleLeptonic)||(isData&&((eleDataSet&&singleElectronic)||(muonDataSet&&singleMuonic))))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain([single_ele,single_mu],maxN=maxN,histname="",treeName="Events") ,\
  'label':'_lep_', 'str':'1 $lep$' , 'trigger': trigger}\
]

#add_cut = ["(1)","no_isoVeto"]
add_cut = ["(iso_Veto)","_isoVeto"]
#add_cut = "(1)"
lepSel = lepSels[0]
presel = "&&".join([lepSel['cut'],lepSel['veto'],"Jet_pt[1]>80&&abs(LepGood_eta[0])<2.4",add_cut[0]])
data_presel = "&&".join([lepSel['cut'],lepSel['veto'],lepSel['trigger'],filters,"Jet_pt[1]>80&&abs(LepGood_eta[0])<2.4",add_cut[0]])

weights = [
{'var':'weight','label':'original'},\
]

diLep = "((ngenLep+ngenTau)==2)"
semiLep = "((ngenLep+ngenTau)==1)"
suffix = ""
max_plot = 0.1
plot_dilep = True
plot_semilep = False
plot_WJets = False
plot_ttJets = True
if plot_dilep:
  presel = presel+"&&"+diLep
  suffix = "_diLep"
  max_plot = 1
if plot_semilep:
  presel = presel+"&&"+semiLep
  suffix = "_semiLep"
  max_plot = 0.05

prefix = 'singleLeptonic_Spring16_'
path = '/afs/hephy.at/user/e/easilar/www/Moriond2017/plots/rCS/'
if not os.path.exists(path):
  os.makedirs(path)
btagString = 'nBJetMediumCSV30'
#weight_str, weight_err_str = makeWeight(lumi, sampleLumi=3.)
btagVarString = 'nBJetMediumCSV30'

######## data rCS plots ######
##nJet = (4,5)
##nbTags = (1,1)
###nbtag = [(1,1),(2,2)]
##ht = 500
###                                         (1000, -1):  {'deltaPhi': 0.75}}}}
##

SR = {(3,-1):{(250,-1):{(500,-1):{"deltaPhi":1}}}}

#sideBand3fb = signalRegion3fbReduced
sideBand3fb = SR
##bin = {}
##for srNJet in sorted(sideBand3fb):
##  bin[srNJet]={}
##  for stb in sorted(sideBand3fb[srNJet]):
##    bin[srNJet][stb] = {}
##    for htb in sorted(sideBand3fb[srNJet][stb]):
##      bin[srNJet][stb][htb] = {}
##      deltaPhiCut = sideBand3fb[srNJet][stb][htb]['deltaPhi']
##      #rCS_Name_1b, rCS_Cut_1b = nameAndCut(stb, htb, nJet, btb=nbTags, presel=data_presel, btagVar = btagVarString)
##      rCS_Name_1b, rCS_Cut_1b = nameAndCut(stb, htb,srNJet, btb=(1,1), presel=presel, btagVar = btagVarString)
##      rCS_Name_2b, rCS_Cut_2b = nameAndCut(stb, htb,srNJet, btb=(0,0), presel=presel, btagVar = btagVarString)
##      rCS_Name_1b_45, rCS_Cut_1b_45 = nameAndCut(stb, htb,nJet, btb=(1,1), presel=presel, btagVar = btagVarString)
##      rCS_Name_2b_45, rCS_Cut_2b_45 = nameAndCut(stb, htb,nJet, btb=(0,0), presel=presel, btagVar = btagVarString)
##      rCS_Name_1b_45_b, rCS_Cut_1b_45_b = nameAndCut(stb, htb,nJet, btb=(1,1), presel=presel, btagVar = btagVarString)
##      s , bla = nameAndCut(stb, htb, srNJet, btb=(1,1), presel=presel, btagVar = btagVarString) 
##      name = "".join(s.split('_')[:-1])
##      print rCS_Name_1b
##      #print rCS_Name_2b
##      #rCS_data = getRCS(cData, rCS_Cut_1b,  deltaPhiCut)
##      rCS_data = getRCS(cTTJets, rCS_Cut_1b,  deltaPhiCut)
##      rCS_bkg = getRCS(cTTJets, rCS_Cut_2b,  deltaPhiCut)
##      rCS_bkg1 = getRCS(cTTJets, rCS_Cut_1b_45,  deltaPhiCut)
##      rCS_bkg2 = getRCS(cTTJets, rCS_Cut_2b_45,  deltaPhiCut)
##      rCS_bkg3 = getRCS(cBkg, rCS_Cut_1b_45_b,  deltaPhiCut)
##      #rCS_2b = getRCS(cData, rCS_Cut_2b,  deltaPhiCut)
##      if not  rCS_data['rCS']=='Nan':
##        print "rCS 1b :" , rCS_data['rCS'] ,"+-" ,rCS_data['rCSE_sim']
##      print "rCS 2b :" , rCS_bkg['rCS'] ,"+-" ,rCS_bkg['rCSE_sim']
##      #print "rCS 2b/1b : " , rCS_2b['rCS'] / rCS_1b['rCS']
##      bin[srNJet][stb][htb]['label'] = name
##      bin[srNJet][stb][htb]['rCS_1b'] = rCS_data
##      bin[srNJet][stb][htb]['rCS_2b'] = rCS_bkg
##      bin[srNJet][stb][htb]['rCS_1b_1'] = rCS_bkg1
##      bin[srNJet][stb][htb]['rCS_1b_2'] = rCS_bkg2
##      bin[srNJet][stb][htb]['rCS_1b_bkg'] = rCS_bkg3
##      #bin[srNJet][stb][htb]['rCS_1b']['label'] = 'data' #nBTagBinName((1,1))
##      #bin[srNJet][stb][htb]['rCS_2b']['label'] = 'WJets'   #nBTagBinName((2,2))
##
##print bin
##cb = ROOT.TCanvas("cb","cb",800,800)
##cb.cd()
###cb.SetLeftMargin(2)
###cb.SetBottomMargin(10)
####cb.SetGrid()
##latex = ROOT.TLatex()
##latex.SetNDC()
##latex.SetTextSize(0.04)
##latex.SetTextAlign(11)
##leg = ROOT.TLegend(0.55,0.65,0.9,0.9)
##leg.SetBorderSize(1)
##Pad1 = ROOT.TPad("Pad1", "Pad1", 0, 0.35, 1, 0.9)
##Pad1.SetTopMargin(0.06)
##Pad1.SetBottomMargin(0)
##Pad1.SetLeftMargin(0.16)
##Pad1.SetRightMargin(0.15)
##Pad1.Draw()
##Pad1.cd()
##ROOT.gStyle.SetHistMinimumZero()
##h0 = ROOT.TH1F("h0","h0",12,0,12)
##h1 = ROOT.TH1F("h1","h1",12,0,12)
##h2 = ROOT.TH1F("h2","h2",12,0,12)
##h3 = ROOT.TH1F("h3","h3",12,0,12)
##h4 = ROOT.TH1F("h4","h4",12,0,12)
##h5 = ROOT.TH1F("h5","h5",12,0,12)
##h0.SetMarkerColor(ROOT.kBlack)
##h0.SetLineColor(ROOT.kBlack)
##h0.SetLineWidth(1)
##h2.SetMarkerColor(ROOT.kBlue)
##h2.SetLineColor(ROOT.kBlue)
##h2.SetLineWidth(1)
##h1.SetMarkerColor(ROOT.kRed)
##h1.SetLineColor(ROOT.kRed)
##h3.SetMarkerColor(ROOT.kBlue)
##h3.SetLineColor(ROOT.kBlue)
##h3.SetLineWidth(1)
##h4.SetMarkerColor(ROOT.kGreen)
##h4.SetLineColor(ROOT.kGreen)
##h4.SetLineWidth(1)
##h5.SetMarkerColor(ROOT.kGray)
##h5.SetLineColor(ROOT.kGray)
##h5.SetLineWidth(1)
##h0.SetMaximum(0.2)
##h1.SetMaximum(0.2)
##h1.SetMinimum(0)
##h0.SetMinimum(0)
##index = 0
##for srNJet in sorted(sideBand3fb):
##  for stb in sorted(sideBand3fb[srNJet]):
##    for htb in sorted(sideBand3fb[srNJet][stb]):
##      print bin[srNJet][stb][htb]['label']
##      index +=1
##      h3.SetBinContent(index,         bin[srNJet][stb][htb]['rCS_1b_1']['rCS'])
##      h3.SetBinError(index,           bin[srNJet][stb][htb]['rCS_1b_1']['rCSE_sim'])
##      h3.GetXaxis().SetLabelSize(0.02)
##      h3.GetXaxis().SetBinLabel(index,bin[srNJet][stb][htb]['label'])
##      h5.SetBinContent(index,         bin[srNJet][stb][htb]['rCS_1b_bkg']['rCS'])
##      h5.SetBinError(index,           bin[srNJet][stb][htb]['rCS_1b_bkg']['rCSE_sim'])
##      h5.GetXaxis().SetLabelSize(0.02)
##      h5.GetXaxis().SetBinLabel(index,bin[srNJet][stb][htb]['label'])
##      h4.SetBinContent(index,         bin[srNJet][stb][htb]['rCS_1b_2']['rCS'])
##      h4.SetBinError(index,           bin[srNJet][stb][htb]['rCS_1b_2']['rCSE_sim'])
##      h4.GetXaxis().SetLabelSize(0.02)
##      h4.GetXaxis().SetBinLabel(index,bin[srNJet][stb][htb]['label'])
##      if not bin[srNJet][stb][htb]['rCS_1b']['rCS']=='Nan':
##        h0.SetBinContent(index,         bin[srNJet][stb][htb]['rCS_1b']['rCS'])
##        h0.SetBinError(index,           bin[srNJet][stb][htb]['rCS_1b']['rCSE_sim'])
##      h0.GetXaxis().SetBinLabel(index,bin[srNJet][stb][htb]['label'])
##      h0.GetXaxis().SetLabelSize(0.02)
##      h1.SetBinContent(index,         bin[srNJet][stb][htb]['rCS_2b']['rCS'])
##      h1.SetBinError(index,           bin[srNJet][stb][htb]['rCS_2b']['rCSE_sim'])
##      h1.GetXaxis().SetLabelSize(0.02)
##      h1.GetXaxis().SetBinLabel(index,bin[srNJet][stb][htb]['label'])
##      h2.SetBinContent(index,1 )
##      h2.SetBinError(index, 0)
##      h2.GetXaxis().SetBinLabel(index,bin[srNJet][stb][htb]['label'])
##      
##h0.GetYaxis().SetTitle("R_{CS}")
##h1.GetYaxis().SetTitle("R_{CS}")
##h0.Draw("EH1")
##h4.Draw("EH1 same")
##h5.Draw("EH1 same")
##h1.Draw("EH1 same")
##h3.Draw("EH1 same")
###leg.AddEntry(h0, "Single Muon Data Set" ,"l")
##leg.AddEntry(h0, "tt Jets 1b" ,"l")
##leg.AddEntry(h1, "tt Jets 0b" ,"l")
##leg.AddEntry(h3, "tt Jets 1b njet:4,5" ,"l")
##leg.AddEntry(h4, "tt Jets 0b njet:4,5" ,"l")
##leg.AddEntry(h5, "Bkg 1b njet:4,5" ,"l")
##leg.SetFillColor(0)
##leg.SetLineColor(0)
##leg.Draw()
##latex.DrawLatex(0.16,0.958,"#font[22]{CMS}"+" #font[12]{Preliminary}")
##latex.DrawLatex(0.68,0.958,"#bf{L=3 fb^{-1} (13 TeV)}")
###latex.DrawLatex(0.6,0.9,"H_{T}>"+str(ht))
###latex.DrawLatex(0.6,0.85,"4 #leq N_{Jets} #leq5" )
###latex.DrawLatex(0.6,0.85,str(nJet[0])+"#leq N_{Jets} #leq"+str(nJet[1]) )
###latex.DrawLatex(0.6,0.8,"N_{bTags}=1")
###latex.DrawLatex(0.6,0.8,"N_{bTags}="+str(nbTags[0]))
###latex.DrawLatex(0.6,0.8,"Run 2015D")
###latex.DrawLatex(0.3,0.8,"Semi Lepton")
##Pad1.RedrawAxis()
##cb.cd()
##Pad2 = ROOT.TPad("Pad2", "Pad2",  0, 0.04, 1, 0.35)
##Pad2.SetTopMargin(0)
##Pad2.SetBottomMargin(0.5)
##Pad2.SetLeftMargin(0.16)
##Pad2.SetRightMargin(0.15)
##Pad2.Draw()
##Pad2.cd()
###Func = ROOT.TF1('Func',"[0]",0,13)
###Func.SetParameter(0,1)
###Func.SetLineColor(2)
##h_ratio = h3.Clone('h_ratio')
##h_ratio.SetMinimum(0.0)
##h_ratio.SetMaximum(3)
##h2.SetMinimum(0.0)
##h2.SetMaximum(3)
##h_ratio.Sumw2()
##h_ratio.Divide(h1)
##h_ratio.SetMarkerStyle(20)
##h_ratio.SetMarkerColor(ROOT.kBlack)
##h_ratio.SetTitle("")
##h_ratio.GetYaxis().SetTitle("Data/MC ")
##h_ratio.GetYaxis().SetTitleSize(0.1)
##h_ratio.GetXaxis().SetTitle("")
##h_ratio.GetYaxis().SetTitleFont(42)
##h_ratio.GetYaxis().SetTitleOffset(0.6)
##h_ratio.GetXaxis().SetTitleOffset(1)
##h_ratio.GetYaxis().SetNdivisions(505)
##h_ratio.GetXaxis().SetTitleSize(0.2)
##h_ratio.GetXaxis().SetLabelSize(0.1)
##h_ratio.GetXaxis().SetLabelOffset(0.03)
##h_ratio.GetYaxis().SetLabelSize(0.1)
##h2.GetYaxis().SetTitle("Blue/Red ")
##h2.GetYaxis().SetTitleSize(0.1)
##h2.GetXaxis().SetTitle("")
##h2.GetYaxis().SetTitleFont(42)
##h2.GetYaxis().SetTitleOffset(0.6)
##h2.GetXaxis().SetTitleOffset(1)
##h2.GetYaxis().SetNdivisions(505)
##h2.GetXaxis().SetTitleSize(0.2)
##h2.GetXaxis().SetLabelSize(0.1)
##h2.GetXaxis().SetLabelOffset(0.03)
##h2.GetYaxis().SetLabelSize(0.1)
##h2.Draw()
##h_ratio.Draw("E1 same")
##cb.Draw()
###cb.SaveAs('~/www/Spring15/25ns/rCS_Plots/cTTJets_rCS_'+str(nJet[0])+str(nJet[1])+'_'+str(nbTags[0])+'b.png')
###cb.SaveAs('~/www/Spring15/25ns/rCS_Plots/cTTJets_rCS_'+str(nJet[0])+str(nJet[1])+'_'+str(nbTags[0])+'b.pdf')
###cb.SaveAs('~/www/Spring15/25ns/rCS_Plots/cTTJets_rCS_'+str(nJet[0])+str(nJet[1])+'_'+str(nbTags[0])+'b.root')
##
##cb.SaveAs('~/www/Spring15/25ns/rCS_Plots/cTTJets_old_rCS_compare_'+str(nbTags[0])+'b.png')
##cb.SaveAs('~/www/Spring15/25ns/rCS_Plots/cTTJets_old_rCS_compare_'+str(nbTags[0])+'b.pdf')
##cb.SaveAs('~/www/Spring15/25ns/rCS_Plots/cTTJets_old_rCS_compare_'+str(nbTags[0])+'b.root')

####### WJets rCS Plots ##### 
if plot_WJets:
  ht = 500
  signalRegion3fb = {(3, 3): {(250, 350): {(ht, -1):   {'deltaPhi': 1.0}},\
                              (350, 450): {(ht, -1):   {'deltaPhi': 1.0}},\
                              (450, 650): {(ht, -1):   {'deltaPhi': 0.75}},\
                              (650, -1):  {(ht, -1):    {'deltaPhi': 0.5}}},\
                     (4, 4): {(250, 350): {(ht, -1):   {'deltaPhi': 1.0}},\
                              (350, 450): {(ht, -1):   {'deltaPhi': 1.0}},\
                              (450, 650): {(ht, -1):   {'deltaPhi': 0.75}},\
                              (650, -1):  {(ht, -1):    {'deltaPhi': 0.5}}},\
                     (5, 5): {(250, 350): {(ht, -1):   {'deltaPhi': 1.0}},\
                              (350, 450): {(ht, -1):   {'deltaPhi': 1.0}},\
                              (450, 650): {(ht, -1):   {'deltaPhi': 0.75}},\
                              (650, -1):  {(ht, -1):    {'deltaPhi': 0.5}}},\
                     (6, 7): {(250, 350): {(ht, -1):  {'deltaPhi': 1.0}},\
                              (350, 450): {(ht, -1):  {'deltaPhi': 1.0}},\
                              (450, 650): {(ht, -1):   {'deltaPhi': 0.75}},\
                              (650, -1):  {(ht, -1):    {'deltaPhi': 0.5}}},\
                     (8, -1): {(250, 350):{(ht, -1): {'deltaPhi': 1.0}},
                               (350, 450):{(ht, -1):  {'deltaPhi': 1.0}},
                              (450, 650): {(ht, -1):   {'deltaPhi': 0.75}},\
                              (650, -1):  {(ht, -1):    {'deltaPhi': 0.5}}}}

  bin = {}
  signalRegions = signalRegion3fb
  for srNJet in signalRegions:
    bin[srNJet]={}
    for stb in signalRegions[srNJet]:
      bin[srNJet][stb] = {}
      for htb in signalRegions[srNJet][stb]:
        bin[srNJet][stb][htb] = {}
        deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
        rCS_Name , rCS_Cut = nameAndCut(stb, htb, srNJet, btb=(0,-1), presel=presel, btagVar = btagVarString)
        print rCS_Cut
        print rCS_Name
        rCS = getRCS(cWJets, rCS_Cut ,  deltaPhiCut,weight = "weight*weightBTag0_SF")
        print "rCS 0b from function:" , rCS['rCS'] , rCS['rCSE_sim']
        bin[srNJet][stb][htb]['rCS'] = rCS
        bin[srNJet][stb][htb]['label'] = nJetBinName(srNJet)

  print bin
  cb = ROOT.TCanvas("cb","cb",800,800)
  cb.cd()
  ##cb.SetGrid()
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextSize(0.04)
  latex.SetTextAlign(11)
  leg = ROOT.TLegend(0.6,0.7,0.95,0.8)
  leg.SetBorderSize(1)
  ROOT.gStyle.SetHistMinimumZero()
  h0 = ROOT.TH1F("h0","h0",5,0,5)
  h1 = ROOT.TH1F("h1","h1",5,0,5)
  h2 = ROOT.TH1F("h2","h2",5,0,5)
  h3 = ROOT.TH1F("h3","h3",5,0,5)
  h0.SetMarkerColor(ROOT.kRed)
  h0.SetLineColor(ROOT.kRed)
  h1.SetMarkerColor(ROOT.kBlue)
  h1.SetLineColor(ROOT.kBlue)
  h2.SetMarkerColor(ROOT.kGreen)
  h2.SetLineColor(ROOT.kGreen)
  h3.SetMarkerColor(ROOT.kBlack)
  h3.SetLineColor(ROOT.kBlack)
  #h0b.SetMaximum(0.2)
  h0.SetMaximum(0.1)
  h1.SetMaximum(0.1)
  h2.SetMaximum(0.1)
  h3.SetMaximum(0.1)
  for i , srNJet in enumerate(sorted(bin)):
      h0.SetBinContent(i+1,         bin[srNJet][(250,350)][(ht,-1)]['rCS']['rCS'])
      h0.SetBinError(i+1,           bin[srNJet][(250,350)][(ht,-1)]['rCS']['rCSE_sim'])
      h0.GetXaxis().SetBinLabel(i+1,bin[srNJet][(250,350)][(ht,-1)]['label'])
      h1.SetBinContent(i+1,         bin[srNJet][(350,450)][(ht,-1)]['rCS']['rCS'])
      h1.SetBinError(i+1,           bin[srNJet][(350,450)][(ht,-1)]['rCS']['rCSE_sim'])
      h1.GetXaxis().SetBinLabel(i+1,bin[srNJet][(350,450)][(ht,-1)]['label'])
      h2.SetBinContent(i+1,         bin[srNJet][(450,650)][(ht,-1)]['rCS']['rCS'])
      h2.SetBinError(i+1,           bin[srNJet][(450,650)][(ht,-1)]['rCS']['rCSE_sim'])
      h2.GetXaxis().SetBinLabel(i+1,bin[srNJet][(450,650)][(ht,-1)]['label'])
      h3.SetBinContent(i+1,         bin[srNJet][(650,-1)][(ht,-1)]['rCS']['rCS'])
      h3.SetBinError(i+1,           bin[srNJet][(650,-1)][(ht,-1)]['rCS']['rCSE_sim'])
      h3.GetXaxis().SetBinLabel(i+1,bin[srNJet][(650,-1)][(ht,-1)]['label'])

  h0.GetYaxis().SetTitle("R_{CS}")
  h1.GetYaxis().SetTitle("R_{CS}")
  h2.GetYaxis().SetTitle("R_{CS}")
  h3.GetYaxis().SetTitle("R_{CS}")
  h0.Draw("EH1")
  h1.Draw("EH1 same")
  h2.Draw("EH1 same")
  h3.Draw("EH1 same")
  leg.AddEntry(h0, "250 #leq L_{T} #leq350" ,"l")
  leg.AddEntry(h1, "350 #leq L_{T} #leq450" ,"l")
  leg.AddEntry(h2, "450 #leq L_{T} #leq650" ,"l")
  leg.AddEntry(h3, "650 #leq L_{T}" ,"l")
  leg.SetFillColor(0)
  leg.SetLineColor(0)
  leg.Draw()
  latex.DrawLatex(0.16,0.958,"#font[22]{CMS}"+" #font[12]{Simulation}")
  latex.DrawLatex(0.68,0.958,"#bf{L=2.1 fb^{-1} (13 TeV)}")
  latex.DrawLatex(0.6,0.9,"H_{T}>"+str(ht))
  latex.DrawLatex(0.6,0.85,"W+Jets")
  #latex.DrawLatex(0.3,0.8,"Semi Lepton")
  cb.Draw()
  cb.SaveAs(path+'/WJets_rCS_btagged_HT'+str(ht)+add_cut[1]+'.png')
  cb.SaveAs(path+'/WJets_rCS_btagged_HT'+str(ht)+add_cut[1]+'.pdf')
  cb.SaveAs(path+'/WJets_rCS_btagged_HT'+str(ht)+add_cut[1]+'.root')

########TTJets RCS Plots######
if plot_ttJets :
  signalRegion3fb = {(4, -1): {(250, 350): {(500, -1 ):   {'deltaPhi': 1.0}}}}
  bin = {}
  nJetbins = [(4,4),(5,5),(6,7),(8,-1)]
  #signalRegions = signalRegion3fbReduced
  signalRegions = signalRegion3fb
  for srNJet in signalRegions:
    bin[srNJet] = {}
    for stb in signalRegions[srNJet]:
      bin[srNJet][stb] = {}
      for htb in signalRegions[srNJet][stb]:
        bin[srNJet][stb][htb] = {}
        deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
        for crNJet in nJetbins:
          deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
          bin[srNJet][stb][htb]['deltaPhi'] = deltaPhiCut
          rCS_crLowNJet_Name_2b, rCS_crLowNJet_Cut_2b = nameAndCut(stb, htb, crNJet, btb=(0,-1), presel=presel, btagVar = btagVarString)
          rCS_crLowNJet_Name_1b, rCS_crLowNJet_Cut_1b = nameAndCut(stb, htb, crNJet, btb=(0,-1), presel=presel, btagVar = btagVarString)
          rCS_crLowNJet_Name_0b, rCS_crLowNJet_Cut_0b = nameAndCut(stb, htb, crNJet, btb=(0,-1), presel=presel, btagVar = btagVarString)
          print rCS_crLowNJet_Name_1b
          rCS_2b = getRCS(cTTJets , rCS_crLowNJet_Cut_2b,  deltaPhiCut,weight = "weight*(weightBTag2_SF)")
          rCS_1b = getRCS(cTTJets , rCS_crLowNJet_Cut_1b,  deltaPhiCut,weight = "weight*weightBTag1_SF")
          rCS_0b = getRCS(cTTJets , rCS_crLowNJet_Cut_0b,  deltaPhiCut,weight = "weight*weightBTag0_SF")
          print "rCS 2b from function:" , rCS_2b['rCS'] ,"+-",rCS_2b['rCSE_sim']
          print "rCS 1b from function:" , rCS_1b['rCS'] ,"+-",rCS_1b['rCSE_sim']
          print "rCS 0b from function:" , rCS_0b['rCS'] ,"+-",rCS_0b['rCSE_sim']
          bin[srNJet][stb][htb][crNJet] = {\
          'label':  nJetBinName(crNJet),\
          '2b_value': rCS_2b['rCS'],\
          '2b_error': rCS_2b['rCSE_sim'],\
          '1b_value': rCS_1b['rCS'],\
          '1b_error': rCS_1b['rCSE_sim'],\
          '0b_value': rCS_0b['rCS'],\
          '0b_error': rCS_0b['rCSE_sim'],\
          }
  print bin
  for srNJet in signalRegions:
    for stb in signalRegions[srNJet]:
      for htb in signalRegions[srNJet][stb]:
        njet_dict = bin[srNJet][stb][htb]
        cb = ROOT.TCanvas("cb","cb",800,800)
        cb.cd()
        ##cb.SetGrid()
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.04)
        latex.SetTextAlign(11)
        leg = ROOT.TLegend(0.3,0.6,0.6,0.7)
        leg.SetBorderSize(1)
        ROOT.gStyle.SetHistMinimumZero()
        h2b = ROOT.TH1F("h2b","h2b",4,0,4)
        h2b.SetMarkerColor(ROOT.kGreen)
        h2b.SetLineColor(ROOT.kGreen)
        h2b.SetLineWidth(2)
        h2b.SetBarWidth(1)
        h2b.SetBarOffset(0)
        h2b.SetStats(0)
        h2b.SetMinimum(0)
        h2b.SetMaximum(max_plot)
        #h2b.SetMaximum(0.05) 
        for i , crNJet in enumerate(nJetbins):
            h2b.SetBinContent(i+1, njet_dict[crNJet]['2b_value'])
            h2b.SetBinError(i+1, njet_dict[crNJet]['2b_error'])
        #   h2b.SetBinContent(i+1, d_35_0[i])
            h2b.GetXaxis().SetBinLabel(i+1,njet_dict[crNJet]['label'])
        leg.AddEntry(h2b, "n_{b_tag} = 2" ,"l")
        h2b.GetYaxis().SetTitle("R_{CS}")
        h2b.Draw("EH1")
        h1b = ROOT.TH1F("h1b","h1b",4,0,4)
        h1b.SetMarkerColor(ROOT.kBlue) 
        h1b.SetLineColor(ROOT.kBlue) 
        h1b.SetBarWidth(1)
        h1b.SetBarOffset(0)
        h1b.SetStats(0)
        h1b.SetMinimum(0) 
        h1b.SetMaximum(max_plot) 
        #h1b.SetMaximum(0.05) 
        for i , crNJet in enumerate(nJetbins):
            h1b.SetBinContent(i+1, njet_dict[crNJet]['1b_value']) 
            h1b.SetBinError(i+1, njet_dict[crNJet]['1b_error']) 
        #   h1b.SetBinContent(i+1, d_35_0[i])
            h1b.GetXaxis().SetBinLabel(i+1,njet_dict[crNJet]['label'])
        leg.AddEntry(h1b, "n_{b_tag} = 1" ,"l") 
        h1b.GetYaxis().SetTitle("R_{CS}")
        h1b.Draw("EH1 same")
        h0b = ROOT.TH1F("h0b","h0b",4,0,4)
        h0b.SetMarkerColor(ROOT.kRed)
        h0b.SetLineColor(ROOT.kRed)  
        h0b.SetBarWidth(1)
        h0b.SetBarOffset(0)
        h0b.SetStats(0)
        h0b.SetMinimum(0)
        h0b.SetMaximum(max_plot)
        #h0b.SetMaximum(0.05)
        for i , crNJet in enumerate(nJetbins):
            h0b.SetBinContent(i+1, njet_dict[crNJet]['0b_value'])
            h0b.SetBinError(i+1, njet_dict[crNJet]['0b_error'])
        #   h0b.SetBinContent(i+1, d_35_0[i])
            h0b.GetXaxis().SetBinLabel(i+1,njet_dict[crNJet]['label'])
        leg.AddEntry(h0b, "n_{b_tag} = 0" ,"l")
        h0b.GetYaxis().SetTitle("R_{CS}")
        h0b.Draw("EH1 same")
        leg.SetFillColor(0)
        leg.SetLineColor(0)
        leg.Draw()
        latex.DrawLatex(0.16,0.958,"#font[22]{CMS}"+" #font[12]{Simulation}")
        latex.DrawLatex(0.72,0.958,"#bf{(13 TeV)}")
        lt = varBinName(stb,'L_{T}')
        ht = varBinName(htb,'H_{T}')
        latex.DrawLatex(0.6,0.85,ht)
        latex.DrawLatex(0.6,0.8,lt)
        #latex.DrawLatex(0.6,0.8,nJetBinName(srNJet))
        #latex.DrawLatex(0.6,0.75,"#Delta#Phi cut:"+str(njet_dict['deltaPhi']))
        latex.DrawLatex(0.3,0.85,"ttjets"+suffix)
        #latex.DrawLatex(0.3,0.8,"di-Lepton")
        cb.Draw()
        cb.SaveAs(path+'/TTJets_rCS_LT'+str(stb[0])+str(stb[1])+'_HT'+str(htb[0])+str(htb[1])+'_nJET'+str(srNJet[0])+str(srNJet[1])+'btagW_'+suffix+add_cut[1]+'_with2bSB.png')
        cb.SaveAs(path+'/TTJets_rCS_LT'+str(stb[0])+str(stb[1])+'_HT'+str(htb[0])+str(htb[1])+'_nJET'+str(srNJet[0])+str(srNJet[1])+'btagW_'+suffix+add_cut[1]+'_with2bSB.pdf')
        cb.SaveAs(path+'/TTJets_rCS_LT'+str(stb[0])+str(stb[1])+'_HT'+str(htb[0])+str(htb[1])+'_nJET'+str(srNJet[0])+str(srNJet[1])+'btagW_'+suffix+add_cut[1]+'_with2bSB.root')

