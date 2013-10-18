import ROOT
from math import *

def getVarValue(c, var, n=0):         #A general method to get the value of a variable from a chain after chain.GetEntry(i) has been called
  varNameHisto = var
  #leaf = var
  leaf = c.GetAlias(varNameHisto)
  if leaf!='':
    return c.GetLeaf(leaf).GetValue(n)
  else:
    return float('nan')

def deltaPhi( phi1, phi2):
  Pi = ROOT.TMath.Pi()
  dphi = phi2-phi1
  if  dphi > Pi:
    dphi -= 2.0*Pi
  if dphi <= -Pi:
    dphi += 2.0*Pi
  return abs(dphi)

def deltaR(l1, l2):
  return ROOT.TMath.Sqrt(deltaPhi(l1["phi"],l2["phi"]**2 + (l1["eta"] - l2["eta"])**2.0))

def getGoodJets(c, crosscleanobjects):
  njets = getVarValue(c, "nsoftjets")   # jet.pt() > 10.
  res=[]
  bres=[]
  ht = 0.
  nbtags = 0
  for i in range(int(njets)):
    eta = getVarValue(c, "jetsEta", i)
    pt  = getVarValue(c, "jetsPt", i)
    if abs(eta)<=2.4 and getVarValue(c, "jetsID", i) and pt>=40.: # FIXME abs(eta)<3.0 (?)
      phi = getVarValue(c, "jetsPhi", i)
      parton = int(abs(getVarValue(c, "jetsParton", i)))
      jet = {"pt":pt, "eta":eta,"phi":phi, 'pdg':parton}
      isolated = True
      for obj in crosscleanobjects:
        if deltaR(jet, obj)<0.3:  # FIXME <0.4 (?)
          isolated = False
#          print "Not this one!", jet, obj, deltaR(jet, obj)
          break
      if isolated:
        ht+=jet["pt"]
        btag = getVarValue(c, "jetsBtag", i)
        jet["btag"] = btag
        res.append(jet)
        if btag >= 0.679:   # bjets
          bres.append(jet)
          nbtags = nbtags+1

  res= sorted(res, key=lambda k: -k['pt'])
  bres= sorted(bres, key=lambda k: -k['pt'])
#  print
#  for j in res:
#    print j
#  print '----- b ---------'
#  for b in bres:
#    print b
  return res, bres #, ht, nbtags

def getGoodBJets(c):
  njets = getVarValue(c, "nsoftjets")
  res=[]
  for i in range(int(njets)):
    eta = getVarValue(c, "jetsEta", i)
    pt  = getVarValue(c, "jetsPt", i)
    btagged = getVarValue(c, "jetsBtag", i)>0.679
    if btagged and abs(eta)<2.4 and getVarValue(c, "jetsID", i) and pt>40. and getVarValue(c, "jetsEleCleaned", i) and getVarValue(c, "jetsMuCleaned", i):
      phi = getVarValue(c, "jetsPhi", i)
      parton = int(abs(getVarValue(c, "jetsParton", i)))
      jet = {"pt":pt, "eta":eta,"phi":phi, "pdg":parton}
      res.append(jet)
  res= sorted(res, key=lambda k: -k['pt'])
  return res



def goodMuID(c, imu):
  pt                                = getVarValue(c,"muonsPt", imu)
  if pt >= 20.:
    isPF                            = getVarValue(c,"muonsisPF", imu)
    isGlobal                        = getVarValue(c,"muonsisGlobal", imu)
    eta                             = getVarValue(c,"muonsEta", imu)
    eta = abs(eta)
    chi2                            = getVarValue(c,"muonsNormChi2", imu)
    nValMuHits                      = getVarValue(c,"muonsNValMuonHits", imu)
    numMatchedStadions              = getVarValue(c,"muonsNumMatchedStadions", imu)
    numMatchedStations              = getVarValue(c,"muonsNumMatchedStations", imu)
    if not numMatchedStations<float('inf'):
      numMatchedStations = numMatchedStadions
    pixelHits                       = getVarValue(c,"muonsPixelHits", imu)
    numTrackerLayersWithMeasurement = getVarValue(c,"muonsNumtrackerLayerWithMeasurement", imu)
    dz                              = getVarValue(c,"muonsDz", imu)
    pfDeltaPt                       = getVarValue(c,"muonsPFDeltaPT", imu)
    pfDeltaPt = abs(pfDeltaPt)
    relIso                          = getVarValue(c,"muonsPFRelIso", imu)    # < 0.12
    dxy                             = getVarValue(c,"muonsDxy", imu)         # < 0.02, control region: > 0.01 

    return ((eta <= 2.4) and \
      (isPF) and  (isGlobal) and \
      (pfDeltaPt < 5) and \
      (chi2 <= 10) and \
      (nValMuHits > 0) and \
      (numMatchedStations > 1) and \
      (pixelHits > 0) and \
      (numTrackerLayersWithMeasurement > 5) and \
      (relIso <= 0.12) and\
      (dxy <= 0.02) and\
      (dz < 0.5))

  else: return False

def goodEleID(c, iele, eta = "none"):

  if eta=="none": eta     = getVarValue(c,"elesEta", iele)
  eta = abs(eta)
  pt                      = getVarValue(c,"elesPt", iele)
  if pt >= 20.:
    sigmaIEtaIEta         = getVarValue(c,"elesSigmaIEtaIEta", iele)
    DPhi                  = getVarValue(c,"elesDPhi", iele)
    DPhi = abs(DPhi)
    DEta                  = getVarValue(c,"elesDEta", iele)
    DEta = abs(DEta)
    HoE                   = getVarValue(c,"elesHoE", iele)
    oneOverEMinusOneOverP = getVarValue(c,"elesOneOverEMinusOneOverP", iele)
    passConvRejection     = getVarValue(c,"elesPassConversionRejection", iele)
    missingHits           = getVarValue(c,"elesMissingHits", iele)
    dz                    = getVarValue(c,"elesDz", iele)
    dxy                   = getVarValue(c,"elesDxy", iele)
    pfDeltaPt             = getVarValue(c,"elesPFDeltaPT", iele)
    relIso                = getVarValue(c,"elesPfRelIso", iele)
    isBarrel              = eta < 1.4442
    isEndcap              = (eta > 1.566) and (eta < 2.5)

    return ( (eta <= 2.5) and (isBarrel or isEndcap) and \
      (oneOverEMinusOneOverP < 0.05) and \
      (  (isBarrel and (sigmaIEtaIEta < 0.01)) or (isEndcap and (sigmaIEtaIEta < 0.03)) ) and \
      (  (isBarrel and (HoE < 0.12)) or (isEndcap and (HoE < 0.10)) ) and \
      (  (isBarrel and (DPhi < 0.06)) or (isEndcap and (DPhi < 0.03)) ) and \
      (  (isBarrel and (DEta < 0.004)) or (isEndcap and (DEta < 0.007)) ) and \
      ( pfDeltaPt < 10. ) and \
      ( missingHits <= 1 ) and \
      ( relIso <= 0.15 ) and \
      ( dxy <= 0.02 ) and \
      ( dz < 0.1 ) and \
      ( passConvRejection > 0))
  else: return False


def getGoodMuons(c,nmuons):
  res=[]
  for i in range(0, int(nmuons)):
    if goodMuID(c, i):
      relIso      = getVarValue(c,"muonsPFRelIso", i)
      dxy         = getVarValue(c,"muonsDxy", i)
      pt          = getVarValue(c,"muonsPt", i)
      eta         = getVarValue(c,"muonsEta", i)
      phi         = getVarValue(c,"muonsPhi", i)
      pdg         = getVarValue(c,"muonsPdg", i)
      res.append({'relIso'  : relIso,
                  'dxy'     : dxy,
                  'pt'      : pt,
                  'eta'     : eta,
                  'phi'     : phi,
                  'pdg'     : pdg          })
  res = sorted(res, key=lambda k: -k['pt'])
  return res

def getGoodElectrons(c, neles):
  res=[]
  for i in range(0, int(neles)):
    if goodEleID(c, i):
      relIso   = getVarValue(c,'elesPfRelIso', i)
      dxy      = getVarValue(c,'elesDxy', i)
      pt       = getVarValue(c,'elesPt',  i)
      eta      = getVarValue(c,'elesEta', i)
      phi      = getVarValue(c,'elesPhi', i)
      pdg      = getVarValue(c,'elesPdg', i)
      res.append({'relIso'  : relIso,
                  'pt'      : pt,
                  'eta'     : eta,
                  'phi'     : phi,
                  'pdg'     : pdg,       
                  'dxy'     : dxy        }) 
  res= sorted(res, key=lambda k: -k['pt'])
  return res

def getGoodLeptons(c, nmuons, neles ):
  res={}
  res["muons"] = getGoodMuons(c, nmuons)
  res["electrons"] = getGoodElectrons(c, neles)
  leptons = res["muons"] + res["electrons"]
  res["leptons"] = leptons
  return res

def px(obj):
  return obj['pt'] * cos(obj['phi'])

def py(obj):
  return obj['pt'] * sin(obj['phi'])

def pz(obj):
  return obj['pt'] * sinh(obj['eta'])

def psquare(x, y, z):
  return (x * x) + (y * y) + (z * z)

def sphericity(jets):
  msum = ROOT.TMatrixDSym(3)
  p2sum = 0

  for i in range(3):
    for j in range(3):
      msum[i][j] = 0

  for obj in jets:
    x = px(obj)
    y = py(obj)
    z = pz(obj)

    p2sum += psquare(x, y, z)

    msum[0][0] += x * x
    msum[0][1] += x * y
    msum[0][2] += x * z

    msum[1][0] += y * x 
    msum[1][1] += y * y
    msum[1][2] += y * z

    msum[2][0] += z * x
    msum[2][1] += z * y
    msum[2][2] += z * z
     
##    s = ROOT.TMatrixD(s,ROOT.kPlus,a)
#    for i in range(3):
#      for j in range(3):
#        msum[i][j] = msum[i][j] + a[i][j]

  for n in range(3):
    for m in range(3):
      msum[n][m] = msum[n][m] / p2sum

  eigenproblem = ROOT.TMatrixDSymEigen(msum)
  eigenvalue = eigenproblem.GetEigenValues()
  if eigenvalue[0] < 0 or eigenvalue[1] < 0 or eigenvalue[2] < 0:
    print 'Warning: eigenvalue < 0'
#    print eigenvalue[0], eigenvalue[1] , eigenvalue[2]
  s = ((eigenvalue[2] + eigenvalue[1]) * 3) / 2

  return {'sphericity':s, "eigenvalues":eigenvalue}

def circularity(eigenvalues3D):
  c = (2 * eigenvalues3D[2]) / (eigenvalues3D[1] + eigenvalues3D[2])
  return c

def circularity2D(jets):
  msum = ROOT.TMatrixDSym(2)
  for i in range(2):
    for j in range(2):
      msum[i][j] = 0

  p2sum = 0

  for obj in jets:
    x = px(obj)
    y = py(obj)
    p2sum += (x * x) + (y * y) 
    msum[0][0] += x * x
    msum[0][1] += x * y
    msum[1][0] += y * x
    msum[1][1] += y * y

  for n in range(2):
    for m in range(2):
      msum[n][m] = msum[n][m] / p2sum

  eigenproblem = ROOT.TMatrixDSymEigen(msum)
  eigenvalue = eigenproblem.GetEigenValues()
#  print eigenvalue
  if eigenvalue[0] < 0 or eigenvalue[1]<0:
    print 'Warning: eigenvalue < 0'
  c2D = (2 * eigenvalue[1]) / (eigenvalue[0] + eigenvalue[1])

  return c2D

#def WT(obj):
#  for i in obj[0]:
#    pt = obj[0][i]['pt']
#    psum += pt
#
#  for i in obj[0]:
#    pt1 = obj[0][i]['pt']
#    for j in obj[0]:
#      pt2 = obj[0][j]['pt']
#      wt = (pt1 * pt2) / (psum * psum)
#  return wt

#def theta(obj):
#  return 2 * atan(exp(-(obj['eta'])))

def foxWolframMoments(jets):
  psum = 0  
  for obj in jets:
    pt = obj['pt']
    psum += pt
    
  ht0 = 0
  ht1 = 0
  ht2 = 0
  ht3 = 0
  ht4 = 0

  for obj1 in jets:
    pt1 = obj1['pt']
    for obj2 in jets:
      pt2 = obj2['pt']
      wt = (pt1 * pt2) / (psum * psum)
      ctheta = cos(obj1['phi'] - obj2['phi'])      
      P0 = 1
      P1 = ctheta
      P2 = ((3 * ctheta * ctheta) - 1) / 2. 
      P3 = ((5 * ctheta * ctheta * ctheta) - (3 * ctheta)) / 2. 
      P4 = ((35 * ctheta * ctheta * ctheta * ctheta) - (30 * ctheta * ctheta) + 3) / 8.
 
      ht0 += wt * P0
      ht1 += wt * P1
      ht2 += wt * P2
      ht3 += wt * P3
      ht4 += wt * P4

  return  {"FWMT0":ht0,"FWMT1":ht1,"FWMT2":ht2,"FWMT3":ht3,"FWMT4":ht4}


