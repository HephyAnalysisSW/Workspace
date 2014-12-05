maxNLep = 2
def cmgLooseLepID(r, nLep, ptCut=10., absEtaCut=2.4, relIso03Cut=0.3):
  if nLep>=maxNLep: return False
  return r.LepGood_relIso03[nLep]<relIso03Cut and  r.LepGood_pt[nLep]>ptCut and abs(r.LepGood_eta[nLep])<absEtaCut
#  if abs(r.LepGood_pdgId[nLep])==13: return cmgLooseMuId(r, nLep, ptCut, absEtaCut)
#  elif abs(r.LepGood_pdgId[nLep])==11: return cmgLooseEleId(r, nLep, ptCut, absEtaCut)

def cmgGoodLepID(r,  nLep, ptCut=10., absEtaCut=2.4, relIso03Cut=0.3):
  return cmgLooseLepID(r, nLep, ptCut, absEtaCut, relIso03Cut) and r.LepGood_tightId[nLep]

def cmgLooseLepIndices(r, ptCut=10, absEtaCut=2.4, relIso03Cut=0.3):
  return [i for i in range(r.nLepGood) if cmgLooseLepID(r, i, ptCut, absEtaCut, relIso03Cut) ]

#def cmgGetLeptonAtIndex(r, i):
#  return {'pt':r.LepGood_pt[i], 'phi':r.LepGood_phi[i], 'pdg':r.LepGood_pdgId[i], 'eta':r.LepGood_eta[i], 'relIso03':r.LepGood_relIso03[i], 'tightID':r.LepGood_tightId[i]}
    

