def hybridIso03ID(r, nLep, hybridIso03):
  return (r.LepGood_pt[nLep]>hybridIso03[1] and r.LepGood_relIso03[nLep]<hybridIso03[0]) or (r.LepGood_pt[nLep]<hybridIso03[1] and r.LepGood_relIso03[nLep]*r.LepGood_pt[nLep]<hybridIso03[2])

def cmgLooseMuID(r, nLep, ptCut, absEtaCut, relIso03):
  return r.LepGood_pt[nLep]>ptCut and abs(r.LepGood_eta[nLep])<absEtaCut and hybridIso03ID(r,nLep,relIso03)

def cmgLooseEleID(r, nLep, ptCut, absEtaCut, relIso03):
  return r.LepGood_pt[nLep]>ptCut and abs(r.LepGood_eta[nLep])<absEtaCut and hybridIso03ID(r,nLep,relIso03)

def cmgLooseLepID(r, nLep, ptCuts, absEtaCuts, hybridIso03):
  if abs(r.LepGood_pdgId[nLep])==11: return cmgLooseEleID(r, nLep, ptCuts[0], absEtaCuts[0],hybridIso03)
  elif abs(r.LepGood_pdgId[nLep])==13: return cmgLooseMuID(r, nLep, ptCuts[1], absEtaCuts[1],hybridIso03)

def cmgLooseLepIndices(r, ptCuts=(10.,5.), absEtaCuts=(2.4,2.1), hybridIso03=(0.3,25.), maxN=2):
  return [i for i in range(min(maxN, r.nLepGood)) if cmgLooseLepID(r, i, ptCuts, absEtaCuts, hybridIso03) ]

def splitIndList(var, l, val):
  resLow = []
  resHigh = []
  for x in l:
    if var[x]>val:
      resHigh.append(x)
    else:
      resLow.append(x)
  return resLow, resHigh


#def cmgGoodLepID(r,  nLep, ptCut=10., absEtaCut=2.4, relIso03Cut=0.3):
#  return cmgLooseLepID(r, nLep, ptCut, absEtaCut, relIso03Cut) and r.LepGood_tightId[nLep]
#
#def cmgLooseLepIndices(r, ptCut=10, absEtaCut=2.4, relIso03Cut=0.3):
#  return [i for i in range(r.nLepGood) if cmgLooseLepID(r, i, ptCut, absEtaCut, relIso03Cut) ]
#
#def cmgGetLeptonAtIndex(r, i):
#  return {'pt':r.LepGood_pt[i], 'phi':r.LepGood_phi[i], 'pdg':r.LepGood_pdgId[i], 'eta':r.LepGood_eta[i], 'relIso03':r.LepGood_relIso03[i], 'tightID':r.LepGood_tightId[i]}
