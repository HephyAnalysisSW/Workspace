import ROOT
from array import array
from math import *
import os, copy, sys
small=True
maxN = -1 if not small else 1
#ROOT.TH1F().SetDefaultSumw2()
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks
import Workspace.HEPHYPythonTools.xsec as xsec
#from Workspace.RA4Analysis.simplePlotsCommon import *
from Workspace.RA4Analysis.helpers import *

from Workspace.RA4Analysis.cmgTuples_v5_Phys14 import *
#samples=[WJetsToLNu_HT100to200_fromEOS, WJetsToLNu_HT200to400_fromEOS, WJetsToLNu_HT400to600_fromEOS, WJetsToLNu_HT600toInf_fromEOS]
#samples=[ttJets_fromEOS]

from Workspace.RA4Analysis.cmgTuples_v5_Phys14 import WJetsToLNu_HT100to200_fromEOS, WJetsToLNu_HT200to400_fromEOS, WJetsToLNu_HT400to600_fromEOS, WJetsToLNu_HT600toInf_fromEOS, ttJets_fromEOS
#samples=[WJetsToLNu_HT100to200_fromEOS, WJetsToLNu_HT200to400_fromEOS, WJetsToLNu_HT400to600_fromEOS, WJetsToLNu_HT600toInf_fromEOS]
samples=[ttJets_fromEOS]

totalYield=0
for s in samples:
  cs=getChunks(s, treeName="treeProducerSusySingleLepton")
  s.update(cs[0][0])
  s['chain']=ROOT.TChain('tree')
  s['chain'].Add(s['file'])
  s["weight"]=4000*xsec.xsec[s['dbsName']]/float(cs[1])
  nEntry=s['chain'].GetEntries()
  totalYield+=4000*xsec.xsec[s['dbsName']]/float(cs[1])*nEntry
  print s["name"],"xsec",xsec.xsec[s['dbsName']],"NSim",cs[1],"nEntry",nEntry, "yield:",4000*xsec.xsec[s['dbsName']]/float(cs[1])*nEntry
print "totalYield", totalYield


from draw_helpers import *
oneMu     = exactlyOneTightMuon(minPt=25, maxEta=2.4, minID=1, minRelIso=0.12)
looseLep  = looseLeptonVeto(minPt=10, muMultiplicity=1, eleMultiplicity=0)
nj2       = nJetCut(2, minPt=30, maxEta=2.4) 
nj6       = nJetCut(6, minPt=30, maxEta=2.4) 
nj2_80    = nJetCut(2, minPt=80, maxEta=2.4)
st200     = stCut(200, lepton="muon", minPt=25, maxEta=2.4, minID=1, minRelIso=0.12)
ht500     = htCut(500,minPt=30, maxEta=2.4)
nb1       = nBTagCut(1, minPt=30, maxEta=2.4, minCMVATag=0.732) 
dPhi1     = dPhiCut(1,lepton="muon", minPt=25, maxEta=2.4, minID=1, minRelIso=0.12)
 
cuts=[["no Cut", "(1)"],
      ["1 lep", oneMu],
      ["veto lep", "&&".join([oneMu, looseLep])],
      ["2 jets (pt 30)", "&&".join([oneMu, looseLep, nj2])],
      ["6 jets (pt 30)", "&&".join([oneMu, looseLep, nj6])],
      ["2 jets (pt 80)", "&&".join([oneMu, looseLep, nj6, nj2_80])],
      ["HT>500", "&&".join([oneMu, looseLep, nj6, nj2_80, ht500])],
      ["ST>200", "&&".join([oneMu, looseLep, nj6, nj2_80, ht500, st200])],
      ["n-btag>=1", "&&".join([oneMu, looseLep, nj6, nj2_80, ht500, st200, nb1])],
      ["dPhi>1", "&&".join([oneMu, looseLep, nj6, nj2_80, ht500, st200, nb1, dPhi1])],

      ]
for name, c in cuts:
  y=0.
  count=0
#  print c
  for s in samples:
    n= s['chain'].GetEntries(c)
    count+=n
    y+= n*s['weight']
  print name, "events:",y, "count:",count

