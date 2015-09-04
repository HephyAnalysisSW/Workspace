from Workspace.HEPHYPythonTools.helpers import findClosestObject, deltaR, deltaR2,getVarValue, getObjFromFile,getObjDict
from math import *



def isGoodLepton(lep, ptCut=5, etaCut = 2.5, hybridIso04={"ptSwitch":25,"relIso":0.2,'absIso':5} , dzCut=0.2 , dxyCut=0.05 ,sip3dCut=4.0 ):
  if abs(lep['pdgId'])==13:
    if lep['mediumMuonId']==1 and lep['dz']<dzCut and lep['dxy'] < dxyCut and lep['sip3d'] < sip3dCut and lep['pt'] > ptCut and abs(lep['eta']) < etaCut and hybridIso04ID(lep):
      return True
    else: return False
  elif abs(lep['pdgId'])==11:
    return False

def hybridIso04ID(lep,hybridIso04={"ptSwitch":25,"relIso":0.2,'absIso':5}):
  return (lep["pt"]>=hybridIso04['ptSwitch'] and lep["relIso04"]<hybridIso04['relIso']) or (lep["pt"]<hybridIso04['ptSwitch'] and lep["relIso04"]*lep["pt"]<hybridIso04['absIso'])







#def hybridIso03ID(r, nLep, hybridIso03):
#  return (r.LepGood_pt[nLep]>=hybridIso03['ptSwitch'] and r.LepGood_relIso03[nLep]<hybridIso03['relIso']) or (r.LepGood_pt[nLep]<hybridIso03['ptSwitch'] and r.LepGood_relIso03[nLep]*r.LepGood_pt[nLep]<hybridIso03['absIso'])
#  
   
#def hybridIso04ID(r, nLep, hybridIso04={"ptSwitch":25,"relIso":0.2,'absIso':5}):
#  if lepton=="LepGood":
#    return (r.LepGood_pt[nLep]>=hybridIso04['ptSwitch'] and r.LepGood_relIso04[nLep]<hybridIso04['relIso']) or (r.LepGood_pt[nLep]<hybridIso04['ptSwitch'] and r.LepGood_relIso04[nLep]*r.LepGood_pt[nLep]<hybridIso04['absIso'])
#  if lepton=="LepOther":
#    return (r.LepOther_pt[nLep]>=hybridIso04['ptSwitch'] and r.LepOther_relIso04[nLep]<hybridIso04['relIso']) or (r.LepOther_pt[nLep]<hybridIso04['ptSwitch'] and r.LepOther_relIso04[nLep]*r.LepOther_pt[nLep]<hybridIso04['absIso'])

def ele_ID_eta(r,nLep,ele_MVAID_cuts):
  if abs(r.LepGood_eta[nLep]) < 0.8 and r.LepGood_mvaIdPhys14[nLep] > ele_MVAID_cuts['eta08'] : return True
  elif abs(r.LepGood_eta[nLep]) > 0.8 and abs(r.LepGood_eta[nLep]) < 1.44 and r.LepGood_mvaIdPhys14[nLep] > ele_MVAID_cuts['eta104'] : return True
  elif abs(r.LepGood_eta[nLep]) > 1.57 and r.LepGood_mvaIdPhys14[nLep] > ele_MVAID_cuts['eta204'] : return True
  return False



 
#def cmgLooseMuID(r, nLep, ptCut, absEtaCut, hybridIso03):
#  return r.LepGood_pt[nLep]>=ptCut and abs(r.LepGood_eta[nLep])<absEtaCut and hybridIso03ID(r,nLep,hybridIso03)

def cmgLooseMuID(r, nLep, ptCut, absEtaCut,lepton="LepGood"):
  return r.LepGood_mediumMuonId[nLep]==1 and r.LepGood_miniRelIso[nLep]<0.4 and r.LepGood_sip3d[nLep]<4.0 and r.LepGood_pt[nLep]>=ptCut and abs(r.LepGood_eta[nLep])<absEtaCut

#def cmgLooseEleID(r, nLep, ptCut, absEtaCut):
#  return r.LepGood_pt[nLep]>=ptCut and abs(r.LepGood_eta[nLep])<absEtaCut and hybridIso03ID(r,nLep,hybridIso03)

def cmgLooseEleID(r, nLep, ptCut , absEtaCut, ele_MVAID_cuts,lepton="LepGood"):
  if lepton=="LepGood":
    return r.LepGood_pt[nLep]>=ptCut and (abs(r.LepGood_eta[nLep])   <1.44 or abs(r.LepGood_eta[nLep])>1.57) and abs(r.LepGood_eta[nLep])<absEtaCut and r.LepGood_miniRelIso[nLep]<0.4 and ele_ID_eta(r,nLep,ele_MVAID_cuts) and r.LepGood_lostHits[nLep]<=1 and r.LepGood_convVeto[nLep] and r.LepGood_sip3d[nLep] < 4.0 
  if lepton=="LepOther":
    return r.LepOther_pt[nLep]>=ptCut and (abs(r.LepOther_eta[nLep]) <1.44 or abs(r.LepOther_eta[nLep])>1.57) and abs(r.LepOther_eta[nLep])<absEtaCut and r.LepOther_miniRelIso[nLep]<0.4 and ele_ID_eta(r,nLep,ele_MVAID_cuts) and r.LepOther_lostHits[nLep]<=1 and r.LepOther_convVeto[nLep] and r.LepOther_sip3d[nLep] < 4.0 

#def cmgLooseLepID(r, nLep, ptCuts, absEtaCuts, hybridIso03):
#  if abs(r.LepGood_pdgId[nLep])==11: return cmgLooseEleID(r, nLep=nLep, ptCut=ptCuts[0], absEtaCut=absEtaCuts[0],hybridIso03=hybridIso03)
#  elif abs(r.LepGood_pdgId[nLep])==13: return cmgLooseMuID(r, nLep=nLep, ptCut=ptCuts[1], absEtaCut=absEtaCuts[1],hybridIso03=hybridIso03)

def cmgLooseLepID(r, nLep, ptCuts, absEtaCuts, ele_MVAID_cuts,lepton="LepGood"):
  if lepton=="LepGood":
    if abs(r.LepGood_pdgId[nLep])==11: return cmgLooseEleID(r, nLep=nLep, ptCut=ptCuts[0], absEtaCut=absEtaCuts[0], ele_MVAID_cuts=ele_MVAID_cuts,lepton=lepton)
    elif abs(r.LepGood_pdgId[nLep])==13: return cmgLooseMuID(r, nLep=nLep, ptCut=ptCuts[1], absEtaCut=absEtaCuts[1],lepton=lepton)
  elif lepton=="LepOther":
    if abs(r.LepOther_pdgId[nLep])==11: return cmgLooseEleID(r, nLep=nLep, ptCut=ptCuts[0], absEtaCut=absEtaCuts[0], ele_MVAID_cuts=ele_MVAID_cuts,lepton=lepton)
    elif abs(r.LepOther_pdgId[nLep])==13: return cmgLooseMuID(r, nLep=nLep, ptCut=ptCuts[1], absEtaCut=absEtaCuts[1],lepton=lepton)

#def cmgLooseLepIndices(r, ptCuts=(7.,5.), absEtaCuts=(2.4,2.1), hybridIso03={'ptSwitch':25, 'absIso':7.5, 'relIso':0.3}, nMax=8):
#  return [i for i in range(min(nMax, r.nLepGood)) if cmgLooseLepID(r, nLep=i, ptCuts=ptCuts, absEtaCuts=absEtaCuts, hybridIso03=hybridIso03) ]

def cmgLooseLepIndices(r, ptCuts=(7.,5.), absEtaCuts=(2.5,2.4),ele_MVAID_cuts = {'eta08':0.35 , 'eta104':0.20,'eta204': -0.52} , nMax=8,lepton="LepGood"):
  if lepton=="LepGood":
    return [i for i in range(min(nMax, r.nLepGood)) if cmgLooseLepID(r, nLep=i, ptCuts=ptCuts, absEtaCuts=absEtaCuts,ele_MVAID_cuts=ele_MVAID_cuts,lepton=lepton) ]
  elif lepton=="LepOther":
    return [i for i in range(min(nMax, r.nLepOther)) if cmgLooseLepID(r, nLep=i, ptCuts=ptCuts, absEtaCuts=absEtaCuts,ele_MVAID_cuts=ele_MVAID_cuts,lepton=lepton) ]
    
    
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
