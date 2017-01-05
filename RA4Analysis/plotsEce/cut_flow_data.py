import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.user import username
import Workspace.HEPHYPythonTools.xsec as xsec
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain
from Workspace.RA4Analysis.cmgTuples_Data25ns_Moriond2017_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Spring16_Moriond2017_MiniAODv2_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Data25ns_Promtv2_postprocessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_postProcessed import *
#from cutFlow_helper import *
from Workspace.RA4Analysis.general_config import *

path = "/afs/hephy.at/user/e/easilar/www/Moriond2017/cutFlows/"
if not os.path.exists(path):
  os.makedirs(path)

ICHEP = False

lepSels = [
{'cut':'singleElectronic' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain(single_mu,histname="",treeName="Events") ,\
  'label':'_mu_', 'str':'1 $\\mu$' , 'trigger': trigger_or_mu , "trigger_xor": trigger_xor_mu},\
{'cut':'singleElectronic' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain(single_ele,histname="",treeName="Events") ,\
  'label':'_ele_', 'str':'1 $\\e$' , 'trigger': trigger_or_ele , "trigger_xor": trigger_xor_ele},\
{'cut':'singleElectronic' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain(met,maxN=maxN,histname="",treeName="Events") ,\
  'label':'_met_', 'str':'1 $lep from MET$' , 'trigger': trigger_or_met, 'trigger_xor': trigger_xor_met},\
{'cut':'singleLeptonic' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain([single_ele,single_mu,met],maxN=maxN,histname="",treeName="Events") ,\
  'label':'_lep_', 'str':'1 $lep$' , 'trigger': trigger, 'trigger_xor': trigger_xor}\
]

lepSels = [lepSels[3]]

if ICHEP: ofile = file(path+'cut_flow_'+lepSel['label']+'_ICHEP.tex','w')
else: ofile = file(path+'cut_flow_data_test.tex','w')
doc_header = '\\documentclass{article}\\usepackage[english]{babel}\\usepackage{graphicx}\\usepackage[margin=0.5in]{geometry}\\begin{document}'
ofile.write(doc_header)

for lepSel in lepSels:
  cuts = [
 #{'cut':"&&".join(['(1)']), 'label':'no cut'},\
 #{'cut':"&&".join([lepSel['cut']]), 'label': lepSel['str']},\
 #{'cut':"&&".join([lepSel['cut'],lepSel['veto']]), 'label': lepSel['str']+' veto'},\
 #{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel["trigger_xor"]]), 'label': 'trigger xor'},\
 #{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel["trigger_xor"],filters]), 'label': 'filters'},\
 #{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel["trigger_xor"],filters,"iso_Veto"]), 'label': 'iso Veto' },\
 #{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel["trigger_xor"],filters,"iso_Veto","nJet30>=5"]), 'label': 'nJet $\\geq$ 5'},\
 #{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel["trigger_xor"],filters,"iso_Veto","nJet30>=5","(Jet_pt[1]>80)","(Jet_pt[1]>80)"]), 'label': '2. jets ($\\geq$ 80 GeV)'},\
 #{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel["trigger_xor"],filters,"iso_Veto","nJet30>=5","(Jet_pt[1]>80)","(Jet_pt[1]>80)","htJet30j>500"]), 'label':'$H_T >$ 500 GeV'},\
 #{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel["trigger_xor"],filters,"iso_Veto","nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","(Jet_pt[1]>80)"]), 'label':'$L_T >$ 250 GeV'},\
 ##{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel["trigger_xor"],filters,"iso_Veto","nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","nBJetMediumCSV30>=0","iso_Veto","(Jet_pt[1]>80)"]), 'label': '0 b-jets (CSVM)' },\
 ##{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel["trigger_xor"],filters,"iso_Veto","nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","nBJetMediumCSV30>=0","deltaPhi_Wl<0.5","(Jet_pt[1]>80)"]), 'label': '\\Delta\\Phi < 0.5' },\
 #{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel["trigger_xor"],filters,"iso_Veto","nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","nBJetMediumCSV30>=1","(Jet_pt[1]>80)"]), 'label': 'multi b-jets (CSVM)' },\
 #{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel["trigger_xor"],filters,"iso_Veto","nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","nBJetMediumCSV30>=1","nJet30>=6","(Jet_pt[1]>80)"]), 'label': 'multi b-jets (CSVM) nJet >=6' },\
 #{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel["trigger_xor"],filters,"iso_Veto","nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","nBJetMediumCSV30>=1","nJet30>=6","deltaPhi_Wl<0.5","(Jet_pt[1]>80)"]), 'label': '\\Delta\\Phi < 0.5' },\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel["trigger_xor"],filters,"iso_Veto","nJet30>=4&&nJet30<=5","(Jet_pt[1]>80)","htJet30j>500","st>250","nBJetMediumCSV30>=1","(Jet_pt[1]>80)"]), 'label': 'multi b + nJet 45' },\
 ##{'cut':"&&".join([lepSel['cut'],lepSel['veto'],"nJet30>=5","(Jet_pt[1]>80)","htJet30j>500","st>250","nBJetMediumCSV30>=1","nJet30>=6","(Jet_pt[1]>80)","deltaPhi_Wl>1"]), 'label': '\\Delta\\Phi >1' },\
   ]
  ofile.write("\n")
  table_header = '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{c | c | c | c | c | c | c | c | c | c | c | c | c | c}'
  ofile.write(table_header)
  ofile.write("\n")
  line = '& data all'
  ofile.write(line)
  ofile.write("\n")
  line_end = '\\\ \\hline'
  ofile.write(line_end)
  ofile.write("\n")
  for cut in cuts:
    print cut['label']
    print cut['cut']
    ofile.write(cut['label'])
    d_chain = lepSel["chain"] 
    y_remain = d_chain.GetEntries(cut['cut']) 
    print  y_remain
    line_yield = '&' + str(format(y_remain , '.1f'))
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

