from Workspace.HEPHYPythonTools.helpers import findClosestObject, deltaR, deltaR2,getVarValue, getObjFromFile
from math import *
def hybridIso03ID(r, nLep, hybridIso03):
  return (r.LepGood_pt[nLep]>=hybridIso03['ptSwitch'] and r.LepGood_relIso03[nLep]<hybridIso03['relIso']) or (r.LepGood_pt[nLep]<hybridIso03['ptSwitch'] and r.LepGood_relIso03[nLep]*r.LepGood_pt[nLep]<hybridIso03['absIso'])

def cmgLooseMuID(r, nLep, ptCut, absEtaCut, hybridIso03):
  return r.LepGood_pt[nLep]>=ptCut and abs(r.LepGood_eta[nLep])<absEtaCut and hybridIso03ID(r,nLep,hybridIso03)

def cmgLooseEleID(r, nLep, ptCut, absEtaCut, hybridIso03):
  return r.LepGood_pt[nLep]>=ptCut and abs(r.LepGood_eta[nLep])<absEtaCut and hybridIso03ID(r,nLep,hybridIso03)

def cmgLooseLepID(r, nLep, ptCuts, absEtaCuts, hybridIso03):
  if abs(r.LepGood_pdgId[nLep])==11: return cmgLooseEleID(r, nLep=nLep, ptCut=ptCuts[0], absEtaCut=absEtaCuts[0],hybridIso03=hybridIso03)
  elif abs(r.LepGood_pdgId[nLep])==13: return cmgLooseMuID(r, nLep=nLep, ptCut=ptCuts[1], absEtaCut=absEtaCuts[1],hybridIso03=hybridIso03)

def cmgLooseLepIndices(r, ptCuts=(7.,5.), absEtaCuts=(2.4,2.1), hybridIso03={'ptSwitch':25, 'absIso':7.5, 'relIso':0.3}, nMax=8):
  return [i for i in range(min(nMax, r.nLepGood)) if cmgLooseLepID(r, nLep=i, ptCuts=ptCuts, absEtaCuts=absEtaCuts, hybridIso03=hybridIso03) ]

def splitIndList(var, l, val):
  resLow = []
  resHigh = []
  for x in l:
    if var[x]>val:
      resHigh.append(x)
    else:
      resLow.append(x)
  return resLow, resHigh

def splitListOfObjects(var, val, s):
  resLow = []
  resHigh = []
  for x in s:
    if x[var]<val:
      resLow.append(x)
    else:
      resHigh.append(x)
  return resLow, resHigh

def getObjDict(c, prefix, variables, i):
 return {var: c.GetLeaf(prefix+'_'+var).GetValue(i) for var in variables}

def get_cmg_jets(c):
  return [getObjDict(c, 'Jet', ['eta','pt','phi','btagCMVA', 'partonId', 'id'], i) for i in range(int(getVarValue(c, 'nJet')))]
def get_cmg_jets_fromStruct(r):
  return [{p:getattr(r, 'Jet'+'_'+p)[i] for p in ['eta','pt','phi','btagCMVA', 'partonId', 'id']} for i in range(r.nJet)]

def get_cmg_index_and_DR(objs,leptonPhi,leptonEta):
  obj = findClosestObject(objs,{'phi':leptonPhi, 'eta':leptonEta})
  if obj and obj['index']<10:
    index = obj['index']
    dr =sqrt(obj['distance'])
  else:
    index=-1
    dr=float('nan')
  return index , dr

def get_cmg_genLeps(c):
  return [getObjDict(c, 'genLep', ['eta','pt','phi','charge', 'pdgId', 'sourceId'], i) for i in range(int(getVarValue(c, 'ngenLep')))]

def get_cmg_recoMuons(c):
  res = [getObjDict(c, 'LepGood', ['eta','pt','phi','charge', 'dxy', 'dz', 'relIso03','tightId', 'pdgId'], i) for i in range(int(getVarValue(c, 'nLepGood')))]
  return filter(lambda m:abs(m['pdgId'])==13, res)



#def cmgGoodLepID(r,  nLep, ptCut=10., absEtaCut=2.4, relIso03Cut=0.3):
#  return cmgLooseLepID(r, nLep, ptCut, absEtaCut, relIso03Cut) and r.LepGood_tightId[nLep]
#
#def cmgLooseLepIndices(r, ptCut=10, absEtaCut=2.4, relIso03Cut=0.3):
#  return [i for i in range(r.nLepGood) if cmgLooseLepID(r, i, ptCut, absEtaCut, relIso03Cut) ]
#
#def cmgGetLeptonAtIndex(r, i):
#  return {'pt':r.LepGood_pt[i], 'phi':r.LepGood_phi[i], 'pdg':r.LepGood_pdgId[i], 'eta':r.LepGood_eta[i], 'relIso03':r.LepGood_relIso03[i], 'tightID':r.LepGood_tightId[i]}
