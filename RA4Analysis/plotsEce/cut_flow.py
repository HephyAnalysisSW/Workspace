import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.user import username
import Workspace.HEPHYPythonTools.xsec as xsec
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain
#from Workspace.RA4Analysis.cmgTuples_Data25ns_Moriond2017_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Spring16_Moriond2017_MiniAODv2_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Data25ns_Promtv2_postprocessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_postProcessed import *
#from cutFlow_helper import *
from Workspace.RA4Analysis.general_config import *

path = "/afs/hephy.at/user/e/easilar/www/Moriond2017/cutFlows/"
if not os.path.exists(path):
  os.makedirs(path)

ICHEP = True

lepSels = [
{'cut':'(singleMuonic&&(!isData||(isData&&muonDataSet)))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
# 'chain': getChain(single_mu,histname="",treeName="Events") ,\
  'label':'_mu_', 'str':'1 $\\mu$' , 'trigger': trigger},\
{'cut':'singleElectronic&&(!isData||(isData&&eleDataSet))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
# 'chain': getChain(single_ele,histname="",treeName="Events") ,\
  'label':'_ele_', 'str':'1 $\\e$' , 'trigger': trigger},\
{'cut':'((!isData&&singleLeptonic)||(isData&&((eleDataSet&&singleElectronic)||(muonDataSet&&singleMuonic))))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
# 'chain': getChain([single_ele,single_mu],maxN=maxN,histname="",treeName="Events") ,\
  'label':'_lep_', 'str':'1 $lep$' , 'trigger': trigger}\
]

lepSels = [lepSels[2]]

bkg_samples=[
{'sample':'TTVH',      "weight":"(1)" ,"cut":(0,0),"add_Cut":"(1)","name":TTV ,'tex':'t#bar{t}V','color':ROOT.kOrange-3},
{"sample":"DiBosons",  "weight":"(1)" ,"cut":(0,0),"add_Cut":"(1)","name":diBoson ,"tex":"WW/WZ/ZZ","color":ROOT.kRed+3},
{"sample":"DY",        "weight":"(1)" ,"cut":(0,0),"add_Cut":"(1)","name":DY_HT,"tex":"DY + jets",'color':ROOT.kRed-6},
{"sample":"singleTop", "weight":"(1)" ,"cut":(0,0),"add_Cut":"(1)","name":singleTop_lep,"tex":"t/#bar{t}",'color': ROOT.kViolet+5},
{"sample":"QCD",       "weight":"(1)" ,"cut":(0,0),"add_Cut":"(1)","name":QCDHT, "tex":"QCD","color":ROOT.kCyan-6},
{"sample":"WJets",     "weight":"(1)" ,"cut":(0,0),"add_Cut":"(1)","name":WJetsHTToLNu,"tex":"W + jets","color":ROOT.kGreen-2},
{"sample":"ttJets",    "weight":"(1)" ,"cut":(0,0),"add_Cut":"(lheHTIncoming<=600)","name":TTJets_diLep, "tex":"t#bar{t} ll + jets (HT $<=$ 600)",'color':ROOT.kBlue},
{"sample":"ttJets",    "weight":"(1)" ,"cut":(0,0),"add_Cut":"(Sum$(abs(genTau_grandmotherId)==6&&abs(genTau_motherId)==24)+Sum$(abs(genLep_grandmotherId)==6&&abs(genLep_motherId)==24)==2)","name":TTJets_HTbinned, "tex":"t#bar{t} ll + jets from htbinned samples",'color':ROOT.kBlue},
{"sample":"ttJets",    "weight":"(1)" ,"cut":(0,0),"add_Cut":"(lheHTIncoming<=600)","name":TTJets_semiLep, "tex":"t#bar{t} l + jets (HT $<=$ 600)",'color':ROOT.kBlue},
{"sample":"ttJets",    "weight":"(1)" ,"cut":(0,0),"add_Cut":"(Sum$(abs(genTau_grandmotherId)==6&&abs(genTau_motherId)==24)+Sum$(abs(genLep_grandmotherId)==6&&abs(genLep_motherId)==24)<2)","name":TTJets_HTbinned, "tex":"t#bar{t} l + jets from htbinned samples",'color':ROOT.kBlue},
#{"sample":"ttJets",    "weight":"(1)" ,"cut":(0,0),"add_Cut":"(lheHTIncoming>600)","name":TTJets_HTbinned, "tex":"t#bar{t} + jets (HT$>$600)",'color':ROOT.kBlue},
]

for bkg in bkg_samples:
    bkg['chain'] = getChain(bkg['name'],histname="",treeName="Events")


for lepSel in lepSels:
  cuts = [
  {'cut':"&&".join(['(1)']), 'label':'no cut'},\
  {'cut':"&&".join([lepSel['cut']]), 'label': lepSel['str']},\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto']]), 'label': lepSel['str']+' veto'},\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5"]), 'label': 'nJet $\\geq$ 5'},\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5","(Jet_pt[1]>80)","(Jet_pt[1]>80)"]), 'label': '2. jets ($\\geq$ 80 GeV)'},\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5","(Jet_pt[1]>80)","(Jet_pt[1]>80)","htJet30j>500"]), 'label':'$H_T >$ 500 GeV'},\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","(Jet_pt[1]>80)"]), 'label':'$L_T >$ 250 GeV'},\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","(Jet_pt[1]>80)","iso_Veto"]), 'label': 'iso Veto' },\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","nBJetMediumCSV30==0","iso_Veto","(Jet_pt[1]>80)"]), 'label': '0 b-jets (CSVM)' },\
  #{'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","nBJetMediumCSV30==0","deltaPhi_Wl>1","(Jet_pt[1]>80)"]), 'label': '\\Delta\\Phi >' },\
  #{'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","nBJetMediumCSV30>=1","nJet30>=6","(Jet_pt[1]>80)"]), 'label': 'multi b-jets (CSVM) nJet >=6' },\
  #{'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","nBJetMediumCSV30>=1","nJet30>=6","(Jet_pt[1]>80)","deltaPhi_Wl>1"]), 'label': '\\Delta\\Phi >1' },\
   ]
  if ICHEP: ofile = file(path+'cut_flow_'+lepSel['label']+'_ICHEP_.tex','w')
  else: ofile = file(path+'cut_flow_'+lepSel['label']+'_reweightOnly_.tex','w')
  doc_header = '\\documentclass{article}\\usepackage[english]{babel}\\usepackage{graphicx}\\usepackage[margin=0.5in]{geometry}\\begin{document}'
  ofile.write(doc_header)
  ofile.write("\n")
  table_header = '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{c | c | c | c | c | c | c | c | c | c | c | c | c | c}'
  ofile.write(table_header)
  ofile.write("\n")
  sum_tt = []
  sum_all = []
  for s in bkg_samples:
    line = '&' + s['tex'] 
    ofile.write(line)
    ofile.write("\n")
  line = '& sum t#bar{t} + jets'
  ofile.write(line)
  ofile.write("\n")
  line = '& sum all'
  ofile.write(line)
  ofile.write("\n")
  line_end = '\\\ \\hline'
  ofile.write(line_end)
  ofile.write("\n")
  for cut in cuts:
    print cut['label']
    print cut['cut']
    ofile.write(cut['label'])
    for s in bkg_samples:
      tot_yields = 0
      chain = s['chain']
      #nEntry = chain.GetEntries()
      #nEntry = chain.GetEntries("&&".join([s["add_Cut"],cut['cut']]))
      #print "MC Events:" , nEntry
      y_remain = getYieldFromChain(chain,cutString = "&&".join([s["add_Cut"],cut['cut']]) , weight = reweight)
      print tot_yields , y_remain
      tot_yields = y_remain
      #tot_yields = nEntry
      if ICHEP : tot_yields = (tot_yields*12880)/36450 
      if s["sample"] == "ttJets": sum_tt.append(tot_yields)  
      sum_all.append(tot_yields)  
      line_yield = '&' + str(format(tot_yields, '.1f'))
      #line_yield = '&' + str(format(nEntry, '.1f'))
      ofile.write(line_yield)
    line_yield = '&' + str(format(sum(sum_tt), '.1f'))
    ofile.write(line_yield)
    line_yield = '&' + str(format(sum(sum_all), '.1f'))
    sum_tt = []
    sum_all = []
    ofile.write(line_yield)
    ofile.write('\\\\')
    ofile.write('\n')

  table_end = '\end{tabular}}\end{center}\caption{CutFlow}\label{tab:CutFlow}\end{table}'
  ofile.write(table_end)
  ofile.write("\n")
  doc_end = '\\end{document}'
  ofile.write(doc_end)
  ofile.close()
  print "Written", ofile.name

