import ROOT
from array import array
from math import *
import os, copy, sys
small = False
maxN  = -1 if not small else 1
#ROOT.TH1F().SetDefaultSumw2()
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks
import Workspace.HEPHYPythonTools.xsec as xsec
#from Workspace.RA4Analysis.simplePlotsCommon import *
from Workspace.RA4Analysis.helpers import *

from Workspace.RA4Analysis.cmgTuples_v5_Phys14 import *
#samples=[WJetsToLNu_HT100to200_fromEOS, WJetsToLNu_HT200to400_fromEOS, WJetsToLNu_HT400to600_fromEOS, WJetsToLNu_HT600toInf_fromEOS]
#samples=[ttJets_fromEOS]

samples=[ 
  ["ttJets", [ttJets_PU20bx25],"$t\\overline{t}$ + jets"],
  ["WJetsHTToLNu", [WJetsToLNu_HT100to200_PU20bx25, WJetsToLNu_HT200to400_PU20bx25, WJetsToLNu_HT400to600_PU20bx25, WJetsToLNu_HT600toInf_PU20bx25], "W + jets"],
  ["singleTop",[TBarToLeptons_sChannel_PU20bx25, TBarToLeptons_tChannel_PU20bx25, TToLeptons_sChannel_PU20bx25, TToLeptons_tChannel_PU20bx25, T_tWChannel_PU20bx25, TBar_tWChannel_PU20bx25], "single top"],
  ["DY",[DYJetsToLL_M50_HT100to200_PU20bx25, DYJetsToLL_M50_HT200to400_PU20bx25, DYJetsToLL_M50_HT400to600_PU20bx25, DYJetsToLL_M50_HT600toInf_PU20bx25], "DY + jets"],
  ["TTV", [ttWJets_PU20bx25, ttZJets_PU20bx25, ttH_PU20bx25], "$t\\overline{t}$ + V/H + jets"],
#  ["QCD", [QCD_HT_250To500_PU20bx25, QCD_HT_500To1000_PU20bx25, QCD_HT_1000ToInf_PU20bx25]],
  ["signal1200", [SMS_T5qqqqWW_Gl1200_Chi1000_LSP800], "$m_{gl}$ = 1.2 \\TeV"],
  ["signal1500", [SMS_T5qqqqWW_Gl1500_Chi800_LSP100], "$m_{gl}$ = 1.5 \\TeV"]
]

for s in samples:
  totalYield=0
  for b in s[1]:
    cs=getChunks(b, treeName="treeProducerSusySingleLepton",maxN=maxN)
    b['chain']=getChain(cs[0],maxN=maxN,histname="",treeName="tree")
    nEntry=b['chain'].GetEntries()
    b["weight"]=4000*xsec.xsec[b['dbsName']]/nEntry
    totalYield+=4000*xsec.xsec[b['dbsName']]
    print b["name"],"xsec",xsec.xsec[b['dbsName']],"nEntry",nEntry, "yield:",4000*xsec.xsec[b['dbsName']]
  print "totalYield", totalYield
 
from draw_helpers import *
oneMu     = exactlyOneTightMuon(minPt=25, maxEta=2.4, minID=1, minRelIso=0.12)
looseLep  = looseLeptonVeto(minPt=10, muMultiplicity=1, eleMultiplicity=0)
nj2       = nJetCut(2, minPt=30, maxEta=2.4) 
nj6       = nJetCut(6, minPt=30, maxEta=2.4) 
nj2_80    = nJetCut(2, minPt=80, maxEta=2.4)
st200     = stCut(200, lepton="muon", minPt=25, maxEta=2.4, minID=1, minRelIso=0.12)
ht500     = htCut(500,minPt=30, maxEta=2.4)
nb0       = nBTagCut((0,0), minPt=30, maxEta=2.4, minCMVATag=0.732) 
dPhi1     = dPhiCut(1,lepton="muon", minPt=25, maxEta=2.4, minID=1, minRelIso=0.12)
 
cuts=[["no cut", "(1)"],
      ["==1 $\\mu$", oneMu],
      ["lepton veto", "&&".join([oneMu, looseLep])],
      ["2 jets ($\\geq$ 30 \\GeV)", "&&".join([oneMu, looseLep, nj2])],
      ["6 jets ($\\geq$ 30 \\GeV)", "&&".join([oneMu, looseLep, nj6])],
      ["2 jets ($\\geq$ 80 \\GeV)", "&&".join([oneMu, looseLep, nj6, nj2_80])],
      ["$H_T >$ 500 \\GeV", "&&".join([oneMu, looseLep, nj6, nj2_80, ht500])],
      ["$S_T >$ 200 \\GeV", "&&".join([oneMu, looseLep, nj6, nj2_80, ht500, st200])],
      ["n(b-tag)= 0", "&&".join([oneMu, looseLep, nj6, nj2_80, ht500, st200, nb0])],
      ["$\\Delta\\phi>1$", "&&".join([oneMu, looseLep, nj6, nj2_80, ht500, st200, nb0, dPhi1])],
      ]

yields={}
for sname, s, lname in samples:
  yields[sname]={}
  for cname, c in cuts:
    y=0.
    count=0
    for b in s:
      n= b['chain'].GetEntries(c)
      count+=n
      y+= n*b['weight']
    yields[sname][cname]=y
    print sname,cname, "events:",y, "count:",count

#yields = {'QCD': {'n-btag>=1': 0.0, 'ST>200': 0.0, '2 jets (pt 30)': 107451.92307692308, 'dPhi>1': 0.0, 'no Cut': 2792038800.0, 'HT>500': 0.0, '6 jets (pt 30)': 0.0, 'veto lep': 163719.40772338034, '2 jets (pt 80)': 0.0, '1 lep': 163719.40772338034}, 'TTV': {'n-btag>=1': 77.72942148121383, 'ST>200': 88.77723348004596, '2 jets (pt 30)': 959.6223148857894, 'dPhi>1': 8.630621409368022, 'no Cut': 8118.799999999999, 'HT>500': 281.07626192682125, '6 jets (pt 30)': 400.20663328609976, 'veto lep': 969.8624510424913, '2 jets (pt 80)': 343.61540293998667, '1 lep': 1293.3206845107525}, 'WJetsHTToLNu': {'n-btag>=1': 180.09927050991135, 'ST>200': 761.1714196395089, '2 jets (pt 30)': 1087427.3069931122, 'dPhi>1': 9.708896349139739, 'no Cut': 11626058.399999999, 'HT>500': 2764.533437858311, '6 jets (pt 30)': 4313.934372775511, 'veto lep': 2027230.7184400917, '2 jets (pt 80)': 3755.490888172776, '1 lep': 2036674.4756328405}, 'ttJets': {'n-btag>=1': 3889.0468847008874, 'ST>200': 4472.403917406021, '2 jets (pt 30)': 343921.37950371514, 'dPhi>1': 259.2697923133925, 'no Cut': 3236400.0, 'HT>500': 15296.917746490157, '6 jets (pt 30)': 30204.930804510226, 'veto lep': 366477.8514349803, '2 jets (pt 80)': 21389.75786585488, '1 lep': 442703.1703751177}, 'DY': {'n-btag>=1': 16.84047112651602, 'ST>200': 45.87666109435823, '2 jets (pt 30)': 67971.496553245, 'dPhi>1': 0.4429942971485743, 'no Cut': 1296746.2000000002, 'HT>500': 207.67413012693783, '6 jets (pt 30)': 334.83173997065376, 'veto lep': 127331.21743973542, '2 jets (pt 80)': 276.1557485141982, '1 lep': 217369.3829360436}, 'singleTop': {'n-btag>=1': 168.81132518174527, 'ST>200': 201.82155718437411, '2 jets (pt 30)': 56137.67789344566, 'dPhi>1': 10.694023650399092, 'no Cut': 580780.48, 'HT>500': 549.2916707081143, '6 jets (pt 30)': 939.2253278360361, 'veto lep': 91444.91577481016, '2 jets (pt 80)': 744.2756214570812, '1 lep': 99034.89121077233}}

print
def getNumString(n,ne, acc=2):
  return str(round(n,acc))+'&$\pm$&'+str(round(ne,acc))

print "& "+ " & ".join([s[2] for s in samples])+'\\\\\\hline'
for c in cuts:
  print " & ".join([c[0]] + [str(round(yields[s[0]][c[0]],1)) for s in samples])+'\\\\'

