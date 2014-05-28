from EventHelper import EventHelper

def isolatedMuons(eh,ptmin=5.,etamax=1.5,wp="medium"):
  imus = [ ]
  nmu = int(eh.get("nmuCount")+0.5)
  mupts = eh.get("muPt")
  assert len(mupts)==nmu
  muetas = eh.get("muEta")
  murelisos = eh.get("muRelIso")

  relabstransition = 25.
  if wp.lower().startswith("loose"):
    relisomax = 0.4
  elif wp.lower().startswith("medium"):
    relisomax = 0.2
  elif wp.lower().startswith("tight"):
    relisomax = 0.12
  else:
    raise ValueError("unknown working point "+wp)

  for i in range(nmu):
    if mupts[i]<ptmin:
      continue
    if abs(muetas[i])>etamax:
      continue
    absiso = murelisos[i]*mupts[i]
#    absisomax = reliso
    if mupts[i]<relabstransition:
      absisomax = relisomax*relabstransition
    else:
      absisomax = relisomax*mupts[i]
    if absiso<absisomax:
      imus.append(i)
  return imus

def hardestIsolatedMuon(eh,ptmin=5.,etamax=1.5,wp="medium"):
  imus = isolatedMuons(eh,ptmin,etamax,wp)
  if len(imus)>0:
    return imus[0]
  return None
