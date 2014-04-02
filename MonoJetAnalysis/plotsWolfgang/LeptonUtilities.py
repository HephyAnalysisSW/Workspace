from EventHelper import EventHelper

def isolatedMuons(eh,ptmin1=5.,etamax=1.5,ptmin2=20.,reliso=0.5):
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
    absiso = murelisos[i]*mupts[i]
#    absisomax = reliso
    if mupts[i]<ptmin2:
      absisomax = reliso*ptmin2
    else:
      absisomax = reliso*mupts[i]
    if absiso<absisomax:
      imus.append(i)
  return imus

def hardestIsolatedMuon(eh,ptmin1=5.,etamax=1.5,ptmin2=20.,reliso=0.5):
  imus = isolatedMuons(eh,ptmin1,etamax,ptmin2,reliso)
  if len(imus)>0:
    return imus[0]
  return None
