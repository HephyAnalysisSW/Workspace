import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from Workspace.RA4Analysis.rCShelpers import *
import math
from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *
from Workspace.RA4Analysis.cmgTuples_Data25ns_Moriond2017_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Spring16_Moriond2017_MiniAODv2_postProcessed import *
from Workspace.RA4Analysis.general_config import *

cWJets  = getChain(WJetsHTToLNu,histname='')
cTTJets = getChain(TTJets_Comb,histname='')
cDY = getChain([DY_HT],histname='')#no QCD
csingleTop = getChain(singleTop_lep,histname='')
cTTV=  getChain(TTV,histname='')
cDiboson = getChain(diBoson,histname='')
cDiboson_rest = getChain(diBoson_rest,histname='')
cDiboson_1l = getChain(diBoson_1L1Nu2Q,histname='')
cEWK = getChain([WJetsHTToLNu, TTJets_Comb, singleTop_lep, DY_HT, TTV],histname='')#no QCD
debug = False
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


def divideRCSdict(a,b):
  kappa = a['rCS']/b['rCS']
  kappaErrorPred = (a['rCS']/b['rCS'])*sqrt(a['rCSE_pred']**2/a['rCS']**2+b['rCSE_pred']**2/b['rCS']**2)
  kappaErrorSim = (a['rCS']/b['rCS'])*sqrt(a['rCSE_sim']**2/a['rCS']**2+b['rCSE_sim']**2/b['rCS']**2)
  return {'kappa':kappa, 'kappaE_pred':kappaErrorPred, 'kappaE_sim':kappaErrorSim}

lepSels = [
{'cut':'((!isData&&singleLeptonic)||(isData&&((eleDataSet&&singleElectronic)||(muonDataSet&&singleMuonic))))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain([single_ele,single_mu],maxN=maxN,histname="",treeName="Events") ,\
  'label':'_lep_', 'str':'1 $lep$' , 'trigger': trigger}\
]

#add_cut = ["(1)","no_isoVeto"]
add_cut = ["(iso_Veto)","_isoVeto"]
lepSel = lepSels[0]
presel = "&&".join([lepSel['cut'],lepSel['veto'],"Jet_pt[1]>80&&abs(LepGood_eta[0])<2.4",add_cut[0]])
data_presel = "&&".join([lepSel['cut'],lepSel['veto'],lepSel['trigger'],filters,"Jet_pt[1]>80&&abs(LepGood_eta[0])<2.4",add_cut[0]])
weight_str = weight_str_plot 

diLep = "((ngenLep+ngenTau)==2)"
semiLep = "((ngenLep+ngenTau)==1)"
suffix = ""
max_plot = 0.1
plot_dilep = False
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
path = '/afs/hephy.at/user/e/easilar/www/Moriond2017/plots/kappa/'
if not os.path.exists(path):
  os.makedirs(path)
btagString = 'nBJetMediumCSV30'
btagVarString = 'nBJetMediumCSV30'


###### data kappa plots ######

sideBand3fb = signalRegions_Moriond2017 

nJet = (4,5)
nbTags = (0,0)

bin = {}
for srNJet in sorted(sideBand3fb):
  bin[srNJet]={}
  for stb in sorted(sideBand3fb[srNJet]):
    bin[srNJet][stb] = {}
    for htb in sorted(sideBand3fb[srNJet][stb]):
      bin[srNJet][stb][htb] = {}
      dPhiCut = sideBand3fb[srNJet][stb][htb]['deltaPhi']
      cname2bCRtt, cut2bCRtt = nameAndCut(stb,htb,nJet, btb=(1,-1) ,presel=presel, btagVar = btagVarString)
      cname1bCRtt, cut1bCRtt = nameAndCut(stb,htb,nJet, btb=(1,1) ,presel=presel, btagVar = btagVarString)
      cname0bCRtt, cut0bCRtt = nameAndCut(stb,htb,nJet, btb=(0,0) ,presel=presel, btagVar = btagVarString)
      ewk_samples_1b = [{'chain':cWJets,       'cut':cut1bCRtt,   'weight':weight_str},\
                         {'chain':cTTJets,     'cut':cut1bCRtt,   'weight':weight_str+"*1.071"},\
                         {'chain':cDY,         'cut':cut1bCRtt,   'weight':weight_str},\
                         {'chain':cTTV,        'cut':cut1bCRtt,   'weight':weight_str},\
                         {'chain':csingleTop,  'cut':cut1bCRtt,   'weight':weight_str},\
                         {'chain':cDiboson,    'cut':cut1bCRtt,   'weight':weight_str},\
                         ]

      ewk_samples_1pb = [{'chain':cWJets,     'cut':cut2bCRtt,   'weight':weight_str},\
                         {'chain':cTTJets,    'cut':cut2bCRtt,   'weight':weight_str+"*1.071"},\
                         {'chain':cDY,        'cut':cut2bCRtt,   'weight':weight_str},\
                         {'chain':cTTV,       'cut':cut2bCRtt,   'weight':weight_str},\
                         {'chain':csingleTop, 'cut':cut2bCRtt,   'weight':weight_str},\
                         {'chain':cDiboson,   'cut':cut2bCRtt,   'weight':weight_str},\
                          ]

      ttJets_samples_0b =[{'chain':cTTJets,     'cut':cut0bCRtt,'weight':weight_str+"*1.071"}]
      #rcs1bCRewk = getRCS(cEWK, cut1bCRtt, dPhiCut, weight_str+"*"+"weightBTag1_SF")
      rcs1bCRewk = combineRCS(ewk_samples_1b, dPhiCut)
      #rcs2bCRewk = getRCS(cEWK, cut2bCRtt, dPhiCut, weight_str+"*"+"weightBTag1p_SF")
      rcs2bCRewk = combineRCS(ewk_samples_1pb, dPhiCut)
      #rcs0bCRtt  = getRCS(cEWK, cut0bCRtt, dPhiCut)
      #rcs1bCRtt  = getRCS(cEWK, cut1bCRtt, dPhiCut)
      #rcs0bCRtt  = getRCS(cTTJets, cut0bCRtt, dPhiCut, weight_str+"*"+"weightBTag0_SF")
      rcs0bCRtt  = combineRCS(ttJets_samples_0b, dPhiCut)
      #rcs1bCRtt  = getRCS(cTTJets, cut1bCRtt, dPhiCut, weight_str+"*"+"weightBTag1_SF")
      if debug:
        yield1b = getYieldFromChain(cTTJets,cut1bCRtt)
        yield2b = getYieldFromChain(cTTJets,cut2bCRtt)
        print "1b:" , yield1b ,"2b:" , yield2b
      #Kappa now calculated only in the SB bin (4,5) jets 1b allEWK MC vs 0b tt MC - no fit applied for the moment!
      kappaTT10 = divideRCSdict(rcs0bCRtt,rcs1bCRewk)
      kappaTT21 = divideRCSdict(rcs0bCRtt,rcs2bCRewk)
      s , bla = nameAndCut(stb, htb, srNJet, btb=(1,1), presel=presel, btagVar = btagVarString) 
      name = "".join(s.split('_')[:-1])
      bin[srNJet][stb][htb]['label'] = name
      bin[srNJet][stb][htb]['kappa_10b'] = kappaTT10
      bin[srNJet][stb][htb]['kappa_21b'] = kappaTT21 

print bin
cb = ROOT.TCanvas("cb","cb",1000,800)
cb.cd()
#cb.SetLeftMargin(2)
#cb.SetBottomMargin(10)
##cb.SetGrid()
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.SetTextAlign(11)
leg = ROOT.TLegend(0.55,0.65,0.8,0.75)
leg.SetBorderSize(1)
Pad1 = ROOT.TPad("Pad1", "Pad1", 0, 0.35, 1, 0.9)
Pad1.SetTopMargin(0.06)
Pad1.SetBottomMargin(0)
Pad1.SetLeftMargin(0.16)
Pad1.SetRightMargin(0.15)
Pad1.Draw()
Pad1.cd()
ROOT.gStyle.SetHistMinimumZero()
h0 = ROOT.TH1F("h0","h0",28,0,28)
h1 = ROOT.TH1F("h1","h1",28,0,28)
h2 = ROOT.TH1F("h2","h2",28,0,28)
h0.SetMarkerColor(ROOT.kBlack)
h0.SetLineColor(ROOT.kBlack)
h0.SetLineWidth(1)
h2.SetMarkerColor(ROOT.kBlue)
h2.SetLineColor(ROOT.kBlue)
h2.SetLineWidth(1)
h1.SetMarkerColor(ROOT.kRed)
h1.SetLineColor(ROOT.kRed)
h0.SetMaximum(5)
h1.SetMaximum(5)
h1.SetMinimum(0)
h0.SetMinimum(0)
index = 0
for srNJet in sorted(sideBand3fb):
  for stb in sorted(sideBand3fb[srNJet]):
    for htb in sorted(sideBand3fb[srNJet][stb]):
      print bin[srNJet][stb][htb]['label']
      index +=1
      h0.SetBinContent(index,         bin[srNJet][stb][htb]['kappa_10b']['kappa'])
      h0.SetBinError(index,           bin[srNJet][stb][htb]['kappa_10b']['kappaE_sim'])
      h0.GetXaxis().SetBinLabel(index,bin[srNJet][stb][htb]['label'])
      h0.GetXaxis().SetLabelSize(0.02)
      h1.SetBinContent(index,         bin[srNJet][stb][htb]['kappa_21b']['kappa'])
      h1.SetBinError(index,           bin[srNJet][stb][htb]['kappa_21b']['kappaE_sim'])
      h1.GetXaxis().SetLabelSize(0.02)
      h1.GetXaxis().SetBinLabel(index,bin[srNJet][stb][htb]['label'])
      h2.SetBinContent(index,1 )
      h2.SetBinError(index, 0)
      h2.GetXaxis().SetBinLabel(index,bin[srNJet][stb][htb]['label'])
      
h0.GetYaxis().SetTitle("kappa tt")
h1.GetYaxis().SetTitle("kappa tt")
h0.Draw("EH1")
h1.Draw("EH1 same")
leg.AddEntry(h0, "kappa 0b/1b" ,"l")
leg.AddEntry(h1, "kappa 0b/1pb" ,"l")
leg.SetFillColor(0)
leg.SetLineColor(0)
leg.Draw()
latex.DrawLatex(0.16,0.958,"#font[22]{CMS}"+" #font[12]{Simulation}")
latex.DrawLatex(0.75,0.958,"#bf{(13 TeV)}")
#latex.DrawLatex(0.6,0.9,"H_{T}>"+str(ht))
#latex.DrawLatex(0.6,0.85,"4 #leq N_{Jets} #leq5" )
latex.DrawLatex(0.6,0.85,str(nJet[0])+"#leq N_{Jets} #leq"+str(nJet[1]) )
#latex.DrawLatex(0.6,0.8,"N_{bTags}=1")
#latex.DrawLatex(0.6,0.8,"N_{bTags}="+str(nbTags[0]))
#latex.DrawLatex(0.6,0.8,"Run 2015D")
#latex.DrawLatex(0.3,0.8,"Semi Lepton")
Pad1.RedrawAxis()
cb.cd()
Pad2 = ROOT.TPad("Pad2", "Pad2",  0, 0.04, 1, 0.35)
Pad2.SetTopMargin(0)
Pad2.SetBottomMargin(0.5)
Pad2.SetLeftMargin(0.16)
Pad2.SetRightMargin(0.15)
Pad2.Draw()
Pad2.cd()
#Func = ROOT.TF1('Func',"[0]",0,13)
#Func.SetParameter(0,1)
#Func.SetLineColor(2)
h_ratio = h0.Clone('h_ratio')
h_ratio.SetMinimum(0.0)
h_ratio.SetMaximum(3)
h2.SetMinimum(0.0)
h2.SetMaximum(2)
h_ratio.Sumw2()
h_ratio.Divide(h1)
h_ratio.SetMarkerStyle(20)
h_ratio.SetMarkerColor(ROOT.kBlack)
h_ratio.SetTitle("")
h_ratio.GetYaxis().SetTitle("black/red ")
h_ratio.GetYaxis().SetTitleSize(0.1)
h_ratio.GetXaxis().SetTitle("")
h_ratio.GetYaxis().SetTitleFont(42)
h_ratio.GetYaxis().SetTitleOffset(0.6)
h_ratio.GetXaxis().SetTitleOffset(1)
h_ratio.GetYaxis().SetNdivisions(505)
h_ratio.GetXaxis().SetTitleSize(0.2)
h_ratio.GetXaxis().SetLabelSize(0.03)
h_ratio.GetXaxis().SetLabelOffset(0.03)
h_ratio.GetYaxis().SetLabelSize(0.1)
h2.GetYaxis().SetTitle("black/red ")
h2.GetYaxis().SetTitleSize(0.1)
h2.GetXaxis().SetTitle("")
h2.GetYaxis().SetTitleFont(42)
h2.GetYaxis().SetTitleOffset(0.6)
h2.GetXaxis().SetTitleOffset(1)
h2.GetYaxis().SetNdivisions(505)
h2.GetXaxis().SetTitleSize(0.2)
h2.GetXaxis().SetLabelSize(0.1)
h2.GetXaxis().SetLabelOffset(0.03)
h2.GetYaxis().SetLabelSize(0.1)
h2.Draw()
h_ratio.Draw("E1 same")
cb.Draw()
cb.SaveAs(path+'/kappa_tt_'+str(nJet[0])+str(nJet[1])+'_nobtagweight_ISR_diboson_included'+add_cut[1]+'.png')
cb.SaveAs(path+'/kappa_tt_'+str(nJet[0])+str(nJet[1])+'_nobtagweight_ISR_diboson_included'+add_cut[1]+'.pdf')
cb.SaveAs(path+'/kappa_tt_'+str(nJet[0])+str(nJet[1])+'_nobtagweight_ISR_diboson_included'+add_cut[1]+'.root')


