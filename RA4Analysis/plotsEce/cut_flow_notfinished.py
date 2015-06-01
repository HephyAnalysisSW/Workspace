import ROOT
import pickle
import os,sys
from localInfo import username
import Workspace.HEPHYPythonTools.xsec as xsec
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks
from Workspace.RA4Analysis.cmgTuples_v1_PHYS14V3 import *
from cutFlow_helper import *


path = "/afs/hephy.at/user/e/easilar/www/PHYS14v3/Cut_Flow/"
if not os.path.exists(path):
  os.makedirs(path)

maxN = 1
small = False
if not small : maxN = -1

lepSels = [
  {'cut':OneMu , 'veto':OneMu_lepveto, 'label':'_mu_', 'str':'1 $\\mu$'},\
  {'cut':OneE ,  'veto':OneE_lepveto,  'label':'_ele_','str':'1 $e$'},\
  {'cut':OneLep ,'veto':OneLep_lepveto,'label':'_lep_','str':'1 $lepton$'},\
]

samples=[
  {"sample":"ttJets",       "list":[ttJets_PU20bx25], "tex":"$t\\overline{t}$ + jets"},
  {"sample":"WJetsHTToLNu", "list":[WJetsToLNu_HT100to200_PU20bx25, WJetsToLNu_HT200to400_PU20bx25, WJetsToLNu_HT400to600_PU20bx25, WJetsToLNu_HT600toInf_PU20bx25],"tex":"W + jets"},
  {"sample":"singleTop",    "list":[TBarToLeptons_sChannel_PU20bx25, TBarToLeptons_tChannel_PU20bx25, TToLeptons_sChannel_PU20bx25, TToLeptons_tChannel_PU20bx25, T_tWChannel_PU20bx25,
 TBar_tWChannel_PU20bx25],"tex":"single top"},
  {"sample":"DY",           "list":[DYJetsToLL_M50_HT100to200_PU20bx25, DYJetsToLL_M50_HT200to400_PU20bx25, DYJetsToLL_M50_HT400to600_PU20bx25, DYJetsToLL_M50_HT600toInf_PU20bx25],"tex":"DY + jets"},
  {"sample":"TTV",          "list":[ttWJets_PU20bx25, ttZJets_PU20bx25, ttH_PU20bx25],"tex":"$t\\overline{t}$ + V/H + jets"},
  {"sample":"QCD",          "list":[QCD_HT_250To500_PU20bx25, QCD_HT_500To1000_PU20bx25, QCD_HT_1000ToInf_PU20bx25], "tex":"QCD"},
  {"sample":"signal1200",   "list":[T5qqqqWW_mGo1200_mCh1000_mChi800], "tex":"$m_{gl}$ = 1.2 TeV"},
  {"sample":"signal1500",   "list":[T5qqqqWW_mGo1500_mCh800_mChi100], "tex":"$m_{gl}$ = 1.5 TeV"},
  {"sample":"signal1000",   "list":[T5qqqqWW_mGo1000_mCh800_mChi700], "tex":"$m_{gl}$ = 1.0 TeV"}
]

for lepSel in lepSels:

  cuts = [
    {'cut':'(1)', 'label':'no cut'},\
    {'cut':lepSel['cut'], 'label': lepSel['str']},\
    {'cut':lepSel['cut']+"&&"+lepSel['veto'], 'label':'lepton veto'},\
    {'cut':lepSel['cut']+"&&"+lepSel['veto']+"&&"+njets_30_cut, 'label':'6 jets ($\\geq$ 30 GeV)'},\
    {'cut':lepSel['cut']+"&&"+lepSel['veto']+"&&"+njets_30_cut+"&&"+jets_2_80, 'label':'2 jets ($\\geq$ 80 GeV)'},\
    {'cut':lepSel['cut']+"&&"+lepSel['veto']+"&&"+njets_30_cut+"&&"+jets_2_80+"&&"+ht_cut, 'label':'$H_T >$ 500 GeV'},\
    {'cut':lepSel['cut']+"&&"+lepSel['veto']+"&&"+njets_30_cut+"&&"+jets_2_80+"&&"+ht_cut+"&&"+st, 'label':'$S_T >$ 200 GeV'},\
    {'cut':lepSel['cut']+"&&"+lepSel['veto']+"&&"+njets_30_cut+"&&"+jets_2_80+"&&"+ht_cut+"&&"+st+"&&"+nbjets_30_cut, 'label':'0 b-jets (CSVv2)'},\
    {'cut':lepSel['cut']+"&&"+lepSel['veto']+"&&"+njets_30_cut+"&&"+jets_2_80+"&&"+ht_cut+"&&"+st+"&&"+nbjets_30_cut+"&&"+dPhi_cut, 'label':'$\\Delta\\Phi>1$'},\
  ]
  ofile = file(path+'cut_flow_'+lepSel['label']+'.tex','w')
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
    ofile.write(cut['label'])
    for s in samples:
      tot_yields = 0
      for b in s['list']:
        #print b
        chunk = getChunks(b, treeName="treeProducerSusySingleLepton",maxN=maxN)
        chain = getChain(chunk[0],maxN=maxN,histname="",treeName="tree")
        nEntry = chain.GetEntries()
        print nEntry 
        weight = 4000*xsec.xsec[b['dbsName']]/nEntry
        y_remain = chain.GetEntries(cut['cut'])
        tot_yields += y_remain*weight
      print tot_yields
      line_yield = '&' + str(format(tot_yields, '.1f'))
      ofile.write(line_yield)
    ofile.write('\\\\')

  table_end = '\end{tabular}}\end{center}\caption{CutFlow}\label{tab:CutFlow}\end{table}'
  ofile.write(table_end)
  ofile.write("\n")
  doc_end = '\\end{document}'
  ofile.write(doc_end)
  ofile.close()
  print "Written", ofile.name

