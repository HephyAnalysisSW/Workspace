import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.user import username
import Workspace.HEPHYPythonTools.xsec as xsec
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain
#from Workspace.RA4Analysis.cmgTuples_Spring15_v2 import *
from Workspace.RA4Analysis.cmgTuples_Data25ns_Promtv2_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_postProcessed import *
#from cutFlow_helper import *
from general_config import *

path = "/afs/hephy.at/user/e/easilar/www/data/Run2016B/2571pb/Tables/"
if not os.path.exists(path):
  os.makedirs(path)

maxN = 1
small = False
if not small : maxN = -1


trigger = "(1)"
lepSels = [
{'cut':'(singleMuonic&&(!isData||(isData&&muonDataSet)))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain(single_mu_Run2016B,maxN=maxN,histname="",treeName="Events") ,\
  'label':'_mu_', 'str':'1 $\\mu$' , 'trigger': trigger},\
{'cut':'singleElectronic&&(!isData||(isData&&eleDataSet))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain(single_ele_Run2016B,maxN=maxN,histname="",treeName="Events") ,\
  'label':'_ele_', 'str':'1 $\\e$' , 'trigger': trigger},\
{'cut':'((!isData&&singleLeptonic)||(isData&&((eleDataSet&&singleElectronic)||(muonDataSet&&singleMuonic))))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain([single_ele_Run2016B,single_mu_Run2016B],maxN=maxN,histname="",treeName="Events") ,\
  'label':'_lep_', 'str':'1 $lep$' , 'trigger': trigger}\
]
bkg_samples=[
{'sample':'TTVH',      "weight":"(1)" ,"cut":(0,0),"add_Cut":"(1)","name":TTV ,'tex':'t#bar{t}V','color':ROOT.kOrange-3},
{"sample":"DiBosons",  "weight":"(1)" ,"cut":(0,0),"add_Cut":"(1)","name":diBoson ,"tex":"WW/WZ/ZZ","color":ROOT.kRed+3},
{"sample":"DY",        "weight":"(1)" ,"cut":(0,0),"add_Cut":"(1)","name":DYHT,"tex":"DY + jets",'color':ROOT.kRed-6},
{"sample":"singleTop", "weight":"(1)" ,"cut":(0,0),"add_Cut":"(1)","name":singleTop_lep,"tex":"t/#bar{t}",'color': ROOT.kViolet+5},
{"sample":"QCD",       "weight":"(1)" ,"cut":(0,0),"add_Cut":"(1)","name":QCDHT, "tex":"QCD","color":ROOT.kCyan-6},
{"sample":"WJets",     "weight":"(1)" ,"cut":(0,0),"add_Cut":"(1)","name":WJetsHTToLNu,"tex":"W + jets","color":ROOT.kGreen-2},
{"sample":"ttJets",    "weight":"(1)" ,"cut":(0,0),"add_Cut":"(1)","name":TTJets_Lep, "tex":"t#bar{t} ll + jets",'color':ROOT.kBlue},
]

for bkg in bkg_samples:
    bkg['chain'] = getChain(bkg['name'],maxN=maxN,histname="",treeName="Events")


for lepSel in lepSels:
  cuts = [
  {'cut':"&&".join(['(1)']), 'label':'no cut'},\
  {'cut':"&&".join([lepSel['cut']]), 'label': lepSel['str']},\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto']]), 'label': lepSel['str']+' veto'},\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5"]), 'label': 'nJet $\\geq$ 5'},\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5","(Jet_pt[1]>80)","(Jet_pt[1]>80)"]), 'label': '2. jets ($\\geq$ 80 GeV)'},\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5","(Jet_pt[1]>80)","(Jet_pt[1]>80)","htJet30j>500"]), 'label':'$H_T >$ 500 GeV'},\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","(Jet_pt[1]>80)"]), 'label':'$L_T >$ 250 GeV'},\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","nBJetMediumCSV30==0","(Jet_pt[1]>80)"]), 'label': '0 b-jets (CSVM)' },\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","nBJetMediumCSV30==0","deltaPhi_Wl>1","(Jet_pt[1]>80)"]), 'label': '\\Delta\\Phi >1' },\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","nBJetMediumCSV30>=1","nJet30>=6","(Jet_pt[1]>80)"]), 'label': 'multi b-jets (CSVM) nJet >=6' },\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","nBJetMediumCSV30>=1","nJet30>=6","(Jet_pt[1]>80)","deltaPhi_Wl>1"]), 'label': '\\Delta\\Phi >1' },\
   ]
  ofile = file(path+'cut_flow_'+str(lumi)+'pb_'+lepSel['label']+'_4jets_.tex','w')
  doc_header = '\\documentclass{article}\\usepackage[english]{babel}\\usepackage{graphicx}\\usepackage[margin=0.5in]{geometry}\\begin{document}'
  ofile.write(doc_header)
  ofile.write("\n")
  table_header = '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{c | c | c | c | c | c | c | c | c | c}'
  ofile.write(table_header)
  ofile.write("\n")
  for s in bkg_samples:
    line = '&' + s['tex'] 
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
      nEntry = chain.GetEntries()
      #print "MC Events:" , chain.GetEntries(cut['cut'])
      y_remain = getYieldFromChain(chain,cutString = cut['cut'],weight = weight_str_plot)
      print tot_yields , y_remain
      tot_yields = y_remain
      line_yield = '&' + str(format(tot_yields, '.1f'))
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

