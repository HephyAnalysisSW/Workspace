from Workspace.HEPHYPythonTools.helpers import findClosestObject, deltaR, deltaR2,getVarValue, getObjFromFile,getObjDict
from math import *
def hybridIso03ID(r, nLep, hybridIso03):
  return (r.LepGood_pt[nLep]>=hybridIso03['ptSwitch'] and r.LepGood_relIso03[nLep]<hybridIso03['relIso']) or (r.LepGood_pt[nLep]<hybridIso03['ptSwitch'] and r.LepGood_relIso03[nLep]*r.LepGood_pt[nLep]<hybridIso03['absIso'])

def cmgMVAEleID(r,nLep,mva_cuts):
  aeta = abs(r.LepGood_eta[nLep])
  for abs_e, mva in mva_cuts.iteritems():
    if aeta>=abs_e[0] and aeta<abs_e[1] and r.LepGood_mvaIdSpring15[nLep]>mva: return True
  return False
  
#ele_MVAID_cuts_loose = {(0,0.8):0.35 , (0.8, 1.44):0.20, (1.57, 999): -0.52}
#ele_MVAID_cuts_vloose = {(0,0.8):-0.11 , (0.8, 1.44):-0.35, (1.57, 999): -0.55}
#ele_MVAID_cuts_tight = {(0,0.8):0.73 , (0.8, 1.44):0.57, (1.57, 999):  0.05}
ele_MVAID_cuts_vloose = {(0,0.8):-0.11 , (0.8, 1.44):-0.55, (1.57, 999): -0.74}   ###from desy people !!!!
ele_MVAID_cuts_tight = {(0,0.8):0.73 , (0.8, 1.44):0.57, (1.57, 999):  0.05}

def cmgLooseMuID(r, nLep):
  return r.LepGood_miniRelIso[nLep]<0.4 and r.LepGood_pt[nLep]>=10 and abs(r.LepGood_eta[nLep])<=2.4

def cmgTightMuID(r, nLep):
  return r.LepGood_pt[nLep]>=25 and abs(r.LepGood_eta[nLep])<=2.4\
     and r.LepGood_miniRelIso[nLep]<0.2\
     and r.LepGood_mediumMuonId[nLep]\
     and abs(r.LepGood_sip3d[nLep])<4

def cmgLooseEleID(r, nLep):
  return r.LepGood_pt[nLep]>=10 and abs(r.LepGood_eta[nLep])<=2.4 #and r.LepGood_miniRelIso[nLep]<0.4 and cmgMVAEleID(r,nLep,ele_MVAID_cuts_vloose) 

def cmgTightEleID(r, nLep):
  return r.LepGood_pt[nLep]>=10 and abs(r.LepGood_eta[nLep])<=2.4\
    and  r.LepGood_miniRelIso[nLep]<0.1  \
    and  r.LepGood_eleCutIdSpring15_25ns_v1[nLep]==4 

#def cmgTightEleID(r, nLep):
#  return r.LepGood_pt[nLep]>=25 and abs(r.LepGood_eta[nLep])<2.5\
#    and  r.LepGood_miniRelIso[nLep]<0.1  \
#    and cmgMVAEleID(r,nLep,ele_MVAID_cuts_tight) \
#    and r.LepGood_lostHits[nLep]<=0 and r.LepGood_convVeto[nLep] and abs(r.LepGood_sip3d[nLep])<4

#and r.LepGood_lostHits[nLep]<=0 and r.LepGood_convVeto[nLep] 

#def cmgLooseLepID(r, nLep, ptCuts, absEtaCuts, hybridIso03):
#  if abs(r.LepGood_pdgId[nLep])==11: return cmgLooseEleID(r, nLep=nLep, ptCut=ptCuts[0], absEtaCut=absEtaCuts[0],hybridIso03=hybridIso03)
#  elif abs(r.LepGood_pdgId[nLep])==13: return cmgLooseMuID(r, nLep=nLep, ptCut=ptCuts[1], absEtaCut=absEtaCuts[1],hybridIso03=hybridIso03)

def cmgLooseLepID(r, nLep):
  if abs(r.LepGood_pdgId[nLep])==11: return cmgLooseEleID(r, nLep=nLep)
  elif abs(r.LepGood_pdgId[nLep])==13: return cmgLooseMuID(r, nLep=nLep)

#def cmgLooseLepIndices(r, ptCuts=(7.,5.), absEtaCuts=(2.4,2.1), hybridIso03={'ptSwitch':25, 'absIso':7.5, 'relIso':0.3}, nMax=8):
#  return [i for i in range(min(nMax, r.nLepGood)) if cmgLooseLepID(r, nLep=i, ptCuts=ptCuts, absEtaCuts=absEtaCuts, hybridIso03=hybridIso03) ]
def cmgLooseLepIndices(r, nMax=8):
  return [i for i in range(min(nMax, r.nLepGood)) if cmgLooseLepID(r, nLep=i) ]

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

def get_cmg_jets(c):
  return [getObjDict(c, 'Jet_', ['eta','pt','phi','btagCMVA','btagCSV','mcMatchFlav' ,'partonId', 'id'], i) for i in range(int(getVarValue(c, 'nJet')))]
def get_cmg_jets_fromStruct(r,j_list):
  return [{p:getattr(r, 'Jet'+'_'+p)[i] for p in j_list} for i in range(r.nJet)]
def get_cmg_JetsforMEt_fromStruct(r,jforMET_list):
  return [{p:getattr(r, 'JetForMET'+'_'+p)[i] for p in jforMET_list} for i in range(r.nJetForMET)]
def get_cmg_fatJets(c):
  return [getObjDict(c, 'FatJet_', ['eta','pt','phi','btagCMVA','btagCSV','mcPt','mcFlavour' ,'prunedMass','tau2', 'tau1'], i) for i in range(int(getVarValue(c, 'nFatJet')))]
def get_cmg_index_and_DR(objs,objPhi,objEta):
  obj = findClosestObject(objs,{'phi':objPhi, 'eta':objEta})
  if obj and obj['index']<10:
    index = obj['index']
    dr =sqrt(obj['distance'])
  else:
    index=-1
    dr=float('nan')
  return index , dr


def get_cmg_genLeps(c):
  return [getObjDict(c, 'genLep_', ['eta','pt','phi','charge', 'pdgId', 'sourceId'], i) for i in range(int(getVarValue(c, 'ngenLep')))]

def get_cmg_genParts(c):
  return [getObjDict(c, 'GenPart_', ['eta','pt','phi','charge', 'pdgId', 'motherId', 'grandmotherId'], i) for i in range(int(getVarValue(c, 'nGenPart')))]

def get_cmg_genParts_fromStruct(r,g_list):
  return [{p:getattr(r, 'GenPart'+'_'+p)[i] for p in g_list} for i in range(r.nGenPart)]

def get_cmg_genPartsAll(c):
  return [getObjDict(c, 'genPartAll_', ['eta','pt','phi','charge', 'pdgId', 'motherId', 'grandmotherId'], i) for i in range(int(getVarValue(c, 'ngenPartAll')))]

def get_cmg_recoMuons(c):
  res = [getObjDict(c, 'LepGood_', ['eta','pt','phi','charge', 'dxy', 'dz', 'relIso03','tightId', 'pdgId'], i) for i in range(int(getVarValue(c, 'nLepGood')))]
  return filter(lambda m:abs(m['pdgId'])==13, res)



#def cmgGoodLepID(r,  nLep, ptCut=10., absEtaCut=2.4, relIso03Cut=0.3):
#  return cmgLooseLepID(r, nLep, ptCut, absEtaCut, relIso03Cut) and r.LepGood_tightId[nLep]
#
#def cmgLooseLepIndices(r, ptCut=10, absEtaCut=2.4, relIso03Cut=0.3):
#  return [i for i in range(r.nLepGood) if cmgLooseLepID(r, i, ptCut, absEtaCut, relIso03Cut) ]
#
#def cmgGetLeptonAtIndex(r, i):
#  return {'pt':r.LepGood_pt[i], 'phi':r.LepGood_phi[i], 'pdg':r.LepGood_pdgId[i], 'eta':r.LepGood_eta[i], 'relIso03':r.LepGood_relIso03[i], 'tightID':r.LepGood_tightId[i]}
