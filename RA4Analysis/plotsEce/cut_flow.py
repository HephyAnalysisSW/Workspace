import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.user import username
import Workspace.HEPHYPythonTools.xsec as xsec
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain
from Workspace.RA4Analysis.cmgTuples_Spring15_v2 import *
from cutFlow_helper import *


path = "/afs/hephy.at/user/e/easilar/www/Spring15/Cut_Flow/"
if not os.path.exists(path):
  os.makedirs(path)

maxN = 1
small = False
if not small : maxN = -1

lumi = 42 #pb-1

lepSels = [
#  {'cut':OneMu , 'veto':OneMu_lepveto, 'label':'_mu_', 'str':'1 $\\mu$' , 'trigger': '(HLT_MuHT350MET70 || HLT_Mu50)'},\
#  {'cut':OneE ,  'veto':OneE_lepveto,  'label':'_ele_','str':'1 $e$', 'trigger': '(HLT_EleHT350MET70 || HLT_Ele105)'},\
  {'cut':OneLep ,'veto':OneLep_lepveto,'label':'_lep_','str':'1 $lepton$', 'trigger': '((HLT_EleHT350MET70 || HLT_Ele105)||(HLT_MuHT350MET70 || HLT_Mu50))' },\
]


samples=[
{"sample":"DY",           "list":[DY_HT200to400,DY_HT400to600,DY_HT600toInf],"tex":"DY + jets",'color':ROOT.kRed-6},
{"sample":"singleTop",    "list":[T_tWch,TBar_tWch,TToLeptons_tch],"tex":"single top",'color': ROOT.kViolet+5},
#{"sample":"QCD",          "list":[QCD_HT200to300,QCD_HT300to500,QCD_HT500to700,QCD_HT700to1000,QCD_HT1000to1500,QCD_HT1500to2000,QCD_HT2000toInf], "tex":"QCD","color":ROOT.kCyan-6},        
{"sample":"WJets",        "list":[WJets],"tex":"W + jets","color":ROOT.kGreen-2},
{"sample":"ttJets",       "list":[TTJets], "tex":"ttbar + jets",'color':ROOT.kBlue-4},
]

for lepSel in lepSels:
  cuts = [
    {'cut':'(1)', 'label':'no cut'},\
    {'cut':lepSel['cut'], 'label':lepSel['str']},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto']]), 'label':'lepton veto'},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut]), 'label':'$H_T >$ 500 GeV'},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st]), 'label':'$L_T >$ 250 GeV'},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut]), 'label':'2 jets ($\\geq$ 30 GeV)'},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut,jets_2_80]), 'label':'2. jets ($\\geq$ 80 GeV)'},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_zero]), 'label':'0 b-jets (CSVv2)'},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_zero,filters]), 'label':'Filters'},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_multi]), 'label':'$>=1 b-jets (CSVv2)$'},\
    {'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_multi,filters]), 'label':'Filters'},\
  ]
  ofile = file(path+'cut_flow_'+str(lumi)+'pb_'+lepSel['label']+'_4jets_.tex','w')
  doc_header = '\\documentclass{article}\\usepackage[english]{babel}\\usepackage{graphicx}\\usepackage[margin=0.5in]{geometry}\\begin{document}'
  ofile.write(doc_header)
  ofile.write("\n")
  table_header = '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{c | c | c | c | c | c | c | c | c | c}'
  ofile.write(table_header)
  ofile.write("\n")
  for s in samples:
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
    for s in samples:
      tot_yields = 0
      for b in s['list']:
        #print b
        #chunk = getChunks(b, treeName="treeProducerSusySingleLepton",maxN=maxN)
        chunk = getChunks(b,maxN=maxN)
        chain = getChain(chunk[0],maxN=maxN,histname="",treeName="tree")
        #nEntry = chain.GetEntries()
        nEntry = chunk[1]
        #print nEntry 
        #weight = lumi*xsec.xsec[b['dbsName']]/nEntry
        #weight = 1 ##count the MC events
        print "MC Events:" , chain.GetEntries(cut['cut'])
        #y_remain = chain.GetEntries(cut['cut'])
        y_remain = getYieldFromChain(chain,cutString = cut['cut'],weight = "(((xsec*genWeight)*"+str(lumi)+")/"+str(nEntry)+")")
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

