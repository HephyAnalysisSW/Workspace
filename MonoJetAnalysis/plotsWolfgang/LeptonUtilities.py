from EventHelper import EventHelper

def isolatedMuons(eh,ptmin1=5.,etamax=1.5,ptmin2=30.,reliso=0.2):
  imus = [ ]
  nmu = int(eh.get("nmu")+0.5)
  mupts = eh.get("muPt")
  muetas = eh.get("muEta")
  murelisos = eh.get("muRelIso")
  for i in range(nmu):
    if mupts[i]<ptmin1:
      continue
    if abs(muetas[i])>etamax:
      continue
    relisomax = reliso
    if mupts[i]<ptmin2:
      relisomax *= mupts[i]
    if murelisos[i]<relisomax:
      imus.append(i)
  return imus

def hardestIsolatedMuon(eh,ptmin1=5.,etamax=1.5,ptmin2=30.,reliso=0.2):
  imus = isolatedMuons(eh,ptmin1,etamax,ptmin2,reliso)
  if len(imus)>0:
    return imus[0]
  return None
