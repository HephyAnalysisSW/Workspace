import ROOT
import copy, os, sys
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from math import *

cut = '(nLepGood>0||nLepOther>0)'
#small = True
small = False
eleVarList = ['pt', 'eta', 'phi', 'pdgId', 'miniRelIso', 'convVeto', 'sip3d', 'mvaIdPhys14']

def antiSel(e):
# return (e['pt']>25 and abs(e['eta'])<2.4 and abs(e['pdgId'])==11 and e['miniRelIso']<0.4 and e['mvaIdPhys14']>(-0.52) and e['mvaIdPhys14']<0.05)
 return (e['pt']>25 and abs(e['eta'])<2.4 and abs(e['pdgId'])==11 and e['miniRelIso']<0.4 and e['mvaIdPhys14']<0.05)

def Sel(e):
  return (e['pt']>25 and abs(e['eta'])<2.4 and abs(e['pdgId'])==11 and e['miniRelIso']<0.1 and e['convVeto']==1 and e['sip3d']<4.0 and e['mvaIdPhys14']>0.05)

def getLp(c,e):
  met = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  Lp = e['pt']/sqrt( (e['pt']*cos(e['phi']) + met*cos(metPhi))**2 + (e['pt']*sin(e['phi']) + met*sin(metPhi))**2 )\
       * cos(acos((e['pt']+met*cos(e['phi']-metPhi))/sqrt(e['pt']**2+met**2+2*met*e['pt']*cos(e['phi']-metPhi))))
  return Lp

QCD_HT_100To250_PU20bx25={\
"name" : "QCD_HT_100To250",
"chunkString": "QCD_HT_100To250",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/QCD_HT_100To250",
'dbsName':'/QCD_HT_100To250_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
QCD_HT_250To500_PU20bx25={\
"name" : "QCD_HT_250To500",
"chunkString": "QCD_HT_250To500",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/QCD_HT_250To500/",
'dbsName':'/QCD_HT_250To500_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
QCD_HT_500To1000_PU20bx25={\
"name" : "QCD_HT_500To1000",
"chunkString": "QCD_HT_500To1000",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/QCD_HT_500To1000",
'dbsName':'/QCD_HT_500To1000_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}
QCD_HT_1000ToInf_PU20bx25={\
"name" : "QCD_HT_1000ToInf",
"chunkString": "QCD_HT_1000ToInf",
'dir' : "/data/easilar/cmgTuples/crab_cmg_v1/test2/QCD_HT_1000ToInf",
'dbsName':'/QCD_HT_1000ToInf_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
}

chunks, nEvents = getChunks(QCD_HT_100To250_PU20bx25,treeName='treeProducerSusySingleLepton', maxN=-1)
#chunks, nEvents = getChunks(QCD_HT_250To500_PU20bx25,treeName='treeProducerSusySingleLepton', maxN=-1)
#chunks, nEvents = getChunks(QCD_HT_500To1000_PU20bx25,treeName='treeProducerSusySingleLepton', maxN=-1)
#chunks, nEvents = getChunks(QCD_HT_1000ToInf_PU20bx25,treeName='treeProducerSusySingleLepton', maxN=-1)

print nEvents

cQCD = ROOT.TChain('tree')
for i, c in enumerate(chunks):
  cQCD.Add(chunks[i]['file'])

cQCD.Draw('>>eList',cut)
elist = ROOT.gDirectory.Get('eList')
number_events = elist.GetN() if not small else 100

print "Sample ",cQCD,": Will loop over", number_events,"events"

antihisto=ROOT.TH1F('antihisto','antihisto',12,-1,2)
selhisto=ROOT.TH1F('selhisto','selhisto',12,-1,2)
leptons = []
antiSelected_e = []
Selected_e =[]
for i in range(number_events):
  cQCD.GetEntry(elist.GetEntry(i))
  #print i, getVarValue(cQCD,'nLepGood'), getVarValue(cQCD,'nLepOther')

  ele = [getObjDict(cQCD, 'LepGood_', eleVarList, j) for j in range(int(cQCD.GetLeaf('nLepGood').GetValue()))]\
      + [getObjDict(cQCD, 'LepOther_', eleVarList, j) for j in range(int(cQCD.GetLeaf('nLepOther').GetValue()))]
  
  antiSelected_e = (filter(antiSel, ele))
  Selected_e = (filter(Sel, ele))
  
  if not len(antiSelected_e)==1:continue
  if not len(Selected_e)==1:continue

  antiVal = getLp(cQCD,antiSelected_e[0])  
  selVal = getLp(cQCD,Selected_e[0])
  antihisto.Fill(antiVal)
  selhisto.Fill(selVal)
#  antiSelected_e = filter(lambda x: not len(x)>0, antiSelected_e)
#  Selected_e = filter(lambda x: not len(x)>0, Selected_e)
  
#  if int(cQCD.GetLeaf('nLepGood').GetValue()) > 0:
#    good = [getObjDict(cQCD, 'LepGood_', eleVarList, j) for j in range(int(cQCD.GetLeaf('nLepGood').GetValue()))]
#    antiSelected_e.append([antiSel(good[j]) for j in range(len(good))])
#    Selected_e.append([Sel(good[j]) for j in range(len(good))])
#    leptons.append(good)
#  elif int(cQCD.GetLeaf('nLepOther').GetValue()) > 0:
#    other = [getObjDict(cQCD, 'LepOther_', eleVarList, j) for j in range(int(cQCD.GetLeaf('nLepOther').GetValue()))]
#    antiSelected_e.append([antiSel(other[j]) for j in range(len(other))])
#    Selected_e.append([Sel(other[j]) for j in range(len(other))])
#    leptons.append(other)
del elist 

print 'Number of anti selected events:',len(antiSelected_e)
print 'Number of selected events:',len(Selected_e)

antihisto.Draw()
selhisto.Draw('same')
#antiSelected_e = filter(antiSel(leptons),leptons)
#if not len(antiSelected_e)==1:continue

