from EventHelper import EventHelper

def isolatedMuons(eh,ptmin=5.,etamax=1.5,wp="medium"):
  imus = [ ]
  nmu = int(eh.get("nmuCount")+0.5)
  mupts = eh.get("muPt")
  assert len(mupts)==nmu
  muetas = eh.get("muEta")
  murelisos = eh.get("muRelIso")
  mudxys = eh.get("muDxy")

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
    if abs(mudxys[i])>0.02:
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

def isolatedElectrons(eh,ptmin=7.,etamax=1.5,wp="medium"):
  ieles = [ ]
  nele = int(eh.get("nelCount")+0.5)
  elepts = eh.get("elPt")
  assert len(elepts)==nele
  eleetas = eh.get("elEta")
  elerelisos = eh.get("elRelIso")

  relabstransition = 25.
  if wp.lower().startswith("loose"):
    relisomax = 0.30
  elif wp.lower().startswith("medium"):
    relisomax = 0.15
  elif wp.lower().startswith("tight"):
    relisomax = 0.10
  else:
    raise ValueError("unknown working point "+wp)

  for i in range(nele):
    if elepts[i]<ptmin:
      continue
    if abs(eleetas[i])>etamax:
      continue
    absiso = elerelisos[i]*elepts[i]
#    absisomax = reliso
    if elepts[i]<relabstransition:
      absisomax = relisomax*relabstransition
    else:
      absisomax = relisomax*elepts[i]
    if absiso<absisomax:
      ieles.append(i)
  return ieles

def hardestIsolatedElectron(eh,ptmin=7.,etamax=1.5,wp="medium"):
  ieles = isolatedElectrons(eh,ptmin,etamax,wp)
  if len(ieles)>0:
    return ieles[0]
  return None
