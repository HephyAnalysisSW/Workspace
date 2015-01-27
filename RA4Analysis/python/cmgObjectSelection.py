from Workspace.HEPHYPythonTools.helpers import findClosestObject, deltaR, deltaR2,getVarValue, getObjFromFile
from math import *
from math import *

def hybridIso03ID(r, nLep, hybridIso03):
  return (r.LepGood_pt[nLep]>hybridIso03['ptSwitch'] and r.LepGood_relIso03[nLep]<hybridIso03['relIso']) or (r.LepGood_pt[nLep]<hybridIso03['ptSwitch'] and r.LepGood_relIso03[nLep]*r.LepGood_pt[nLep]<hybridIso03['absIso'])

def cmgLooseMuID(r, nLep, ptCut, absEtaCut, hybridIso03):
  return r.LepGood_pt[nLep]>ptCut and abs(r.LepGood_eta[nLep])<absEtaCut and hybridIso03ID(r,nLep,hybridIso03)

def cmgLooseEleID(r, nLep, ptCut, absEtaCut, hybridIso03):
  return r.LepGood_pt[nLep]>ptCut and abs(r.LepGood_eta[nLep])<absEtaCut and hybridIso03ID(r,nLep,hybridIso03)

def cmgLooseLepID(r, nLep, ptCuts, absEtaCuts, hybridIso03):
  if abs(r.LepGood_pdgId[nLep])==11: return cmgLooseEleID(r, nLep=nLep, ptCut=ptCuts[0], absEtaCut=absEtaCuts[0],hybridIso03=hybridIso03)
  elif abs(r.LepGood_pdgId[nLep])==13: return cmgLooseMuID(r, nLep=nLep, ptCut=ptCuts[1], absEtaCut=absEtaCuts[1],hybridIso03=hybridIso03)

def cmgLooseLepIndices(r, ptCuts=(10.,5.), absEtaCuts=(2.4,2.1), hybridIso03={'ptSwitch':25, 'absIso':7.5, 'relIso':0.3}, nMax=8):
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

def getGood_cmg_JetsStage2(c):
  njets = getVarValue(c, 'nJet')
  res = []
  for i in range(int(njets)):
    res.append( {"eta":getVarValue(c, 'Jet_eta', i),\
          "pt" :getVarValue(c, 'Jet_pt', i),
          "phi":getVarValue(c, 'Jet_phi', i),
          'btag':getVarValue(c, 'Jet_btagCSV', i),
          'partonId':getVarValue(c, 'Jet_partonId', i)
      })

  return res

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
  ngenLep = getVarValue(c, 'ngenLep')
  res = []
  for i in range(int(ngenLep)):
    res.append( {"eta":getVarValue(c, 'genLep_eta', i),\
        "pt" :getVarValue(c, 'genLep_pt', i),
        "phi":getVarValue(c, 'genLep_phi', i),
        'charge':getVarValue(c, 'genLep_charge', i),
        'pdgId':getVarValue(c, 'genLep_pdgId', i),
        'sourceId':getVarValue(c, 'genLep_sourceId', i)
    })
  return res

def get_cmg_recoMuons(c):
  nLepGood = getVarValue(c, 'nLepGood')
  res = []
  for i in range(int(nLepGood)):
    id = getVarValue(c, 'LepGood_pdgId', i)
    if abs(id) == 13:
      res.append( {"eta":getVarValue(c, 'LepGood_eta', i),\
          "pt" :getVarValue(c, 'LepGood_pt', i),
          "phi":getVarValue(c, 'LepGood_phi', i),
          'charge':getVarValue(c, 'LepGood_charge', i),
          'dxy':getVarValue(c, 'LepGood_dxy', i),
          'dz':getVarValue(c, 'LepGood_dz', i),
          'relIso03':getVarValue(c, 'LepGood_relIso03', i),
          'pdgId':getVarValue(c, 'LepGood_pdgId', i),
          'isLoose': getVarValue(c, 'LepGood_looseIdSusy', i),
          'isTight': getVarValue(c, 'LepGood_tightId', i)
        })
  return res

# def get_cmg_recoMuon(c,i):
#   id = getVarValue(c, 'LepGood_pdgId', i)
#   res = []
#   if id == 13:
#     res.append( {"eta":getVarValue(c, 'LepGood_eta', i),\
#         "pt" :getVarValue(c, 'LepGood_pt', i),
#         "phi":getVarValue(c, 'LepGood_phi', i),
#         'charge':getVarValue(c, 'LepGood_charge', i),
#         'dxy':getVarValue(c, 'LepGood_dxy', i),
#         'dz':getVarValue(c, 'LepGood_dz', i),
#         'relIso03':getVarValue(c, 'LepGood_relIso03', i),
#         'pdgId':getVarValue(c, 'LepGood_pdgId', i),
#         'isLoose': getVarValue(c, 'LepGood_looseIdSusy', i),
#         'isTight': getVarValue(c, 'LepGood_tightId', i)
#       })
#   return res




#def cmgGoodLepID(r,  nLep, ptCut=10., absEtaCut=2.4, relIso03Cut=0.3):
#  return cmgLooseLepID(r, nLep, ptCut, absEtaCut, relIso03Cut) and r.LepGood_tightId[nLep]
#
#def cmgLooseLepIndices(r, ptCut=10, absEtaCut=2.4, relIso03Cut=0.3):
#  return [i for i in range(r.nLepGood) if cmgLooseLepID(r, i, ptCut, absEtaCut, relIso03Cut) ]
#
#def cmgGetLeptonAtIndex(r, i):
#  return {'pt':r.LepGood_pt[i], 'phi':r.LepGood_phi[i], 'pdg':r.LepGood_pdgId[i], 'eta':r.LepGood_eta[i], 'relIso03':r.LepGood_relIso03[i], 'tightID':r.LepGood_tightId[i]}
