import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.user import username
#import Workspace.HEPHYPythonTools.xsec as xsec
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain
#from Workspace.RA4Analysis.cmgTuples_Spring15_v2 import *
#from Workspace.RA4Analysis.cmgTuples_Data25ns_0l import *
#from Workspace.RA4Analysis.cmgTuples_Spring15 import *
from cutFlow_helper import *
#from localInfo import username
#from Workspace.RA4Analysis.cmgTuples_data_25ns_fromArtur import *
from Workspace.RA4Analysis.cmgTuples_Data25ns_miniAODv2 import *
#path = "/afs/hephy.at/user/e/easilar/www/data/Cut_Flow_metNoHF/"
path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/2p3fb/"


if not os.path.exists(path):
  os.makedirs(path)

maxN = 1
small = False
if not small : maxN = -1
print "maxN:" , maxN

lepSels = [
###  {'cut':OneMu , 'veto':OneMu_lepveto, 'label':'_mu_', 'str':'1 $\\mu$' , 'trigger': '(HLT_MuHT350MET70 || HLT_Mu50NoIso)'},\
#  {'cut':OneE ,  'veto':OneE_lepveto,  'label':'_ele_','str':'1 $e$', 'trigger': '(HLT_EleHT350MET70 || HLT_ElNoIso)'},\
#  {'cut':OneLep ,'veto':OneLep_lepveto,'label':'_lep_','str':'1 $lepton$', 'trigger': '((HLT_EleHT350MET70 || HLT_ElNoIso)||(HLT_MuHT350MET70 || HLT_Mu50NoIso))' },\
###  {'cut':OneLep ,'veto':OneLep_lepveto,'label':'_lep_','str':'1 $lepton$', 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))' },\
{'cut':OneE ,  'veto':OneE_lepveto,  'label':'_ele_','str':'1 $e$', 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'},\
#{'cut':OneMu , 'veto':OneMu_lepveto, 'label':'_mu_', 'str':'1 $\\mu$' , 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'},\
]

samples=[
##  {"sample":"ttJets",       "list":[ttJets_PU20bx25], "tex":"$t\\overline{t}$ + jets"},
##  {"sample":"WJetsHTToLNu", "list":[WJetsToLNu_HT100to200_PU20bx25, WJetsToLNu_HT200to400_PU20bx25, WJetsToLNu_HT400to600_PU20bx25, WJetsToLNu_HT600toInf_PU20bx25],"tex":"W + jets"},
##  {"sample":"singleTop",    "list":[TBarToLeptons_sChannel_PU20bx25, TBarToLeptons_tChannel_PU20bx25, TToLeptons_sChannel_PU20bx25, TToLeptons_tChannel_PU20bx25, T_tWChannel_PU20bx25,TBar_tWChannel_PU20bx25],"tex":"single top"},
##  {"sample":"DY",           "list":[DYJetsToLL_M50_HT100to200_PU20bx25, DYJetsToLL_M50_HT200to400_PU20bx25, DYJetsToLL_M50_HT400to600_PU20bx25, DYJetsToLL_M50_HT600toInf_PU20bx25],"tex":"DY + jets"},
##  {"sample":"TTV",          "list":[ttWJets_PU20bx25, ttZJets_PU20bx25, ttH_PU20bx25],"tex":"$t\\overline{t}$ + V/H + jets"},
##  {"sample":"QCD",          "list":[QCD_HT_100To250_PU20bx25,QCD_HT_250To500_PU20bx25, QCD_HT_500To1000_PU20bx25, QCD_HT_1000ToInf_PU20bx25], "tex":"QCD"},
##  {"sample":"signal1200",   "list":[T5qqqqWW_mGo1200_mCh1000_mChi800], "tex":"$m_{gl}$ = 1.2 TeV"},
##  {"sample":"signal1500",   "list":[T5qqqqWW_mGo1500_mCh800_mChi100], "tex":"$m_{gl}$ = 1.5 TeV"},
##  {"sample":"signal1000",   "list":[T5qqqqWW_mGo1000_mCh800_mChi700], "tex":"$m_{gl}$ = 1.0 TeV"}
  #{"sample":"data_mu" ,   "list":getChunks(data_mu) , "tex":"Single Muon"},
####  {"sample":"data_mu" ,   "list":SingleMuon_Run2015D_PromptReco , "tex":"Single_Muon","color":ROOT.kBlack},
####  {"sample":"data_ele",   "list":SingleElectron_Run2015D_PromptReco , "tex":"Single_Electron", "color":ROOT.kBlack},\
#####{"sample":"data_mu" ,   "list":SingleMuon_Run2015D , "tex":"Single_Muon","color":ROOT.kBlack},\
#{"sample":"data_mu" ,   "list":SingleMuon_Run2015D_v4 , "tex":"Single_Muon","color":ROOT.kBlack},\
#{"sample":"data_mu" ,   "list":SingleMuon_Run2015D_05Oct , "tex":"Single_Muon","color":ROOT.kBlack},\
{"sample":"data_ele",   "list":SingleElectron_Run2015D_v4  , "tex":"Single_Electron", "color":ROOT.kBlack},\
#{"sample":"data_ele",   "list":SingleElectron_Run2015D  , "tex":"Single_Electron", "color":ROOT.kBlack},\
{"sample":"data_ele",   "list":SingleElectron_Run2015D_05Oct  , "tex":"Single_Electron", "color":ROOT.kBlack},\
# {"sample":"data_mu" ,   "list":getChunks(data_mu,maxN=maxN) , "tex":"Single Muon"},
# {"sample":"data_ele",   "list":getChunks(data_ele,maxN=maxN), "tex":"Single Electron"},
# {"sample":"data_ele_17July",   "list":getChunks(data_ele_17July,maxN=maxN), "tex":"Single Electron 17 Jul"},
# {"sample":"data_mu_17July" ,   "list":getChunks(data_mu_17July,maxN=maxN) , "tex":"Single_Muon_17Jul"},
]

#s = samples[0]
#chunk = s['list']
#chain = getChain(chunk[0],maxN=maxN,histname="",treeName="tree")
###chunks = []
for s in samples:
  print "SLIST: " , s['list']
  s['chunk'] , s['norm']  = getChunks(s['list'],maxN=maxN)
  print s['chunk']
  print s['norm']  
  ###chunks.append(s['list'])
  ###print chunks
#data = getChain([chunks[0][0][0],chunks[1][0][0]],maxN=maxN,histname="",treeName="tree")
data = getChain(samples[1]['chunk']+samples[0]['chunk'],maxN=maxN,histname="",treeName="tree")
###data = getChain(samples[0]['chunk'],maxN=maxN,histname="",treeName="tree")
print data.GetEntries()
for lepSel in lepSels:
  cuts = [
    {'cut':'(1)', 'label':'no cut'},\
    #{'cut':"&&".join([ht_cut]), 'label':'$H_T >$ 500 GeV'},\
    {'cut':"&&".join([lepSel['cut']]), 'label': lepSel['str']},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto']]), 'label': lepSel['str']+"_veto" },\
    #{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lep_hard]), 'label': lepSel['str']+"_hard"},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto'],lep_hard,"((HLT_EleHT350)||(HLT_MuHT350))"]), 'label': 'Trigger'},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto'],lep_hard,"((HLT_EleHT350)||(HLT_MuHT350))",njets_30+">=5"]), 'label': 'nJet $\\geq$ 5'},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto'],lep_hard,"((HLT_EleHT350)||(HLT_MuHT350))",njets_30+">=5",jets_2_80]), 'label': '2. jets ($\\geq$ 80 GeV)'},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto'],lep_hard,"((HLT_EleHT350)||(HLT_MuHT350))",njets_30+">=5",jets_2_80,ht_cut]), 'label': '$H_T >$ 500 GeV'},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto'],lep_hard,"((HLT_EleHT350)||(HLT_MuHT350))",njets_30+">=5",jets_2_80,ht_cut,jets_2_80,st]), 'label': '$L_T >$ 250 GeV'},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto'],lep_hard,"((HLT_EleHT350)||(HLT_MuHT350))",njets_30+">=5",jets_2_80,ht_cut,jets_2_80,st,filters]), 'label': 'filters'},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto'],lep_hard,"((HLT_EleHT350)||(HLT_MuHT350))",njets_30+">=5",jets_2_80,ht_cut,jets_2_80,st,filters,nbjets_30_cut_zero,jets_2_80]), 'label': '0 b-jets (CSVv2)'},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto'],lep_hard,"((HLT_EleHT350)||(HLT_MuHT350))",njets_30+">=5",jets_2_80,ht_cut,jets_2_80,st,filters,nbjets_30_cut_multi,jets_2_80]), 'label': '$>=1 b-jets (CSVv2)$'},\
  ]
  ofile = file(path+'cut_flow_'+lepSel['label']+'data_2p25_.tex','w')
  doc_header = '\\documentclass{article}\\usepackage[english]{babel}\\usepackage{graphicx}\\usepackage[margin=0.5in]{geometry}\\begin{document}'
  ofile.write(doc_header)
  ofile.write("\n")
  table_header = '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{c | c | c | c | c | c | c | c | c | c}'
  ofile.write(table_header)
  ofile.write("\n")
  #for s in samples:
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
    #for s in samples:
    tot_yields = 0
    #for b in s['list']:
    #print b
    #chunk = getChunks(b, treeName="treeProducerSusySingleLepton",maxN=maxN)
    nEntry = data.GetEntries()
    #nEntry = chunk[1]
    print nEntry 
    #weight = lumi*xsec.xsec[b['dbsName']]/nEntry
    y_remain = data.GetEntries(cut['cut'])
    #y_remain = getYieldFromChain(data,cutString = cut['cut'],weight = "(1)")
    tot_yields += y_remain
    print tot_yields
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
