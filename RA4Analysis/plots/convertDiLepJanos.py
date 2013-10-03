import copy, pickle
import ROOT
from simplePlotsCommon import *
from math import *
import sys, os, copy, array, xsec, random, itertools
from xsecSMS import stop8TeV_NLONLL
from RecDiLep_RECO import RecDiLepton, calcSigmaShift
from RecDiLepAnalytic import RecDiLeptonAnalytic
from datetime import datetime

# ====================================================================
SHIFT    = True    # sigma shift
ANALYTIC = False
small    = True
NumOfFiles = 5   # Joining n files (5)
outputDir = "/data/jkancsar/topDiLepton/convertedTuples"
# =============================================================================

minF = 0
maxF = 3500 
if len(sys.argv)>2:
  minF = int(sys.argv[1])
  maxF = int(sys.argv[2])
  print " # Adding Files from >=", minF, "to <",maxF

def deltaPhi( phi1, phi2):
  dphi = phi2-phi1
  if  dphi > pi:
    dphi -= 2.0*pi
  if dphi <= -pi:
    dphi += 2.0*pi
  return abs(dphi)

def minAbsDeltaPhi(phi, phis):
  if len(phis)>0:
    return min([abs(deltaPhi(phi, x)) for x in phis])
  else: return float('inf')

def minAbsPiMinusDeltaPhi(phi, phis):
  if len(phis)>0:
    return min([abs(abs(deltaPhi(phi, x)) - pi) for x in phis])
  else: return float('inf')

def invMassOfLightObjects(p31, p32):
  [px1, py1, pz1] = p31
  [px2, py2, pz2] = p32
  px = px1+px2 
  py = py1+py2
  pz = pz1+pz2
  p1 = sqrt(px1*px1+py1*py1+pz1*pz1)
  p2 = sqrt(px2*px2+py2*py2+pz2*pz2)
  p = sqrt(px*px+py*py+pz*pz) 
  return   sqrt((p1 + p2)*(p1 + p2) - p*p)

def deltaR(l1, l2):
  return sqrt(deltaPhi(l1["phi"], l2["phi"])**2 + (l1["eta"] - l2["eta"])**2)

overwrite = True

targetLumi = 9200.


def goodMuID(c, imu ):
  return getVarValue(c, "muonsPt", imu)>20. and getVarValue(c, "muonsisPF", imu) and getVarValue(c, "muonsisGlobal", imu) and abs(getVarValue(c, "muonsEta", imu)) < 2.4  and getVarValue(c, "muonsPFRelIso", imu)<0.15 and getVarValue(c, "muonsNormChi2", imu)<10. and getVarValue(c, "muonsNValMuonHits", imu)>0 and getVarValue(c, "muonsNumMatchedStadions", imu) > 1 and getVarValue(c, "muonsPixelHits", imu) > 0 and getVarValue(c, "muonsNumtrackerLayerWithMeasurement", imu) > 5 and getVarValue(c, "muonsDxy", imu) < 0.02 and getVarValue(c, "muonsDz", imu) < 0.1

# muonsPFRelIso < 0.12 (SL) < 0.15 (DL)
# muonsDz       < 0.5  (SL) < 0.1  (DL)
# -------------------------------------------

def goodEleID(c, iele, eta = "none"):
  if eta=="none":
    eta = getVarValue(c, "elesEta", iele)
  sietaieta = getVarValue(c, "elesSigmaIEtaIEta", iele)
  dphi = getVarValue(c, "elesDPhi", iele)
  deta = getVarValue(c, "elesDEta", iele)
  HoE = getVarValue(c, "elesHoE", iele)
  isEB = abs(eta)<1.4442
  isEE = abs(eta)>1.566
  relIso = getVarValue(c, "elesPfRelIso", iele)
  pt = getVarValue(c, "elesPt", iele)
  relIsoCut = 0.15
  if isEE and pt<20:
    relIsoCut = 0.10  # ??
  return  pt>20. and ( isEE or isEB) and getVarValue(c, "elesOneOverEMinusOneOverP", iele)< 0.05\
    and ( relIso<relIsoCut )  and getVarValue(c, "elesPassConversionRejection", iele)>0  and (abs(eta)<2.4)\
    and ( (isEB and HoE < 0.12 ) or (isEE and HoE < 0.10))\
    and ( (isEB and sietaieta < 0.01 ) or (isEE and sietaieta < 0.03)) and getVarValue(c, "elesMissingHits", iele) <=1\
    and ( (isEB and dphi<0.15) or (isEE and dphi<0.10)) and ( (isEB and deta<0.007) or (isEE and deta<0.009))  and getVarValue(c, "elesDxy", iele) < 0.02 and getVarValue(c, "elesDz", iele) < 0.1

# eta           < 2.5   (SL?) < 2.4   (DL)
# isEB and dphi < 0.06  (SL)  < 0.15  (DL)
# isEB and deta < 0.004 (SL)  < 0.007 (DL)
# isEE and deta < 0.03  (SL)  < 0.009 (DL)
# -------------------------------------------

def getGoodMuons(c, nmuons ):
  res=[]
  for i in range(0, int(nmuons)):
    if goodMuID(c, i):
      res.append({"pt":getVarValue(c, "muonsPt", i),"eta":getVarValue(c, "muonsEta", i), "phi":getVarValue(c, "muonsPhi", i), "pdg":getVarValue(c, "muonsPdg", i)})
  res = sorted(res, key=lambda k: -k['pt'])
  return res

def getGoodElectrons(c, neles ):
  res=[]
  for i in range(0, int(neles)):
    eta = getVarValue(c, "elesEta", i)
    if goodEleID(c, i, abs(eta)):
      res.append({"pt":getVarValue(c, "elesPt", i),"eta":eta, "phi":getVarValue(c, "elesPhi", i), "pdg":getVarValue(c, "elesPdg", i), "relIso":getVarValue(c, "elesPfRelIso", i)} )
  res = sorted(res, key=lambda k: -k['pt'])
  return res

def getGoodLeptons(c, nmuons, neles ):
  res={}
  res["muons"] = getGoodMuons(c,nmuons)
  res["electrons"] = getGoodElectrons(c, neles)
  leptons = res["muons"] + res["electrons"]
  res["leptons"] = leptons
  return res

#def getBestLeptonPair(allLeptons, chmode):
#  if len(allLeptons)<2:
#    return [] 
#  cands = list(itertools.combinations(allLeptons, 2))
#  goodCands=[]
#  for cand in cands:
#    sumPt = cand[0]["pt"]+cand[1]["pt"]
#    if chmode=="doubleMu"  and abs(cand[0]["pdg"])==13 and abs(cand[1]["pdg"])==13 and cand[0]["pdg"]+cand[1]["pdg"]==0:
#      goodCands.append([cand, sumPt])
#    if chmode=="doubleEle" and abs(cand[0]["pdg"])==11 and abs(cand[1]["pdg"])==11 and cand[0]["pdg"]+cand[1]["pdg"]==0:
#      goodCands.append([cand, sumPt])
#    if chmode=="eleMu"      and ( (abs(cand[0]["pdg"])==11 and abs(cand[1]["pdg"])==13) or (abs(cand[0]["pdg"])==13 and abs(cand[1]["pdg"])==11)) and abs(cand[0]["pdg"]+cand[1]["pdg"])==2:
#      goodCands.append([cand, sumPt])
#  goodCands = sorted(goodCands, key=lambda k: -k[1]) 
#  if not len(goodCands)>0:
#    return []
#  goodCand = goodCands[0][0]
##  if len(goodCands)>1:
##    print "\n", c.GetLeaf(c.GetAlias('run')).GetValue(), c.GetLeaf(c.GetAlias('lumi')).GetValue(), long(c.GetLeaf(c.GetAlias('event')).GetValue())
##    print goodCands
##    print "selected:",sorted(goodCand, key=lambda k: -k['pt'])
#  return sorted(goodCand, key=lambda k: -k['pt'])

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
  return res, bres, ht, nbtags

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
#  print res
  return res

def writeTrueVal(c, e, swap, bSwap):
  t0d0pdg = getVarValue(c, 'top0WDaughter0Pdg')
  t1d0pdg = getVarValue(c, 'top1WDaughter0Pdg')
  t0d1pdg = getVarValue(c, "top0WDaughter1Pdg")   # just for saving the pdg
  t1d1pdg = getVarValue(c, "top1WDaughter1Pdg")   # just for saving the pdg
  l1ID=-1    #Identify lepton daughter
  l2ID=-1
  if abs(t0d0pdg) == 13 or abs(t0d0pdg) == 11:  # if muon or electron
    l1ID=0
    l1PdgTrue = t0d0pdg
  else:
    l1ID=1
    l1PdgTrue = t0d1pdg
  if abs(t1d0pdg) == 13 or abs(t1d0pdg) == 11:
    l2ID=0
    l2PdgTrue = t1d0pdg
  else:
    l2ID=1
    l2PdgTrue = t1d1pdg
  
  l1pxTrue = getVarValue(c, 'top0WDaughter'+str(l1ID)+'Px')
  l1pyTrue = getVarValue(c, 'top0WDaughter'+str(l1ID)+'Py')
  l1pzTrue = getVarValue(c, 'top0WDaughter'+str(l1ID)+'Pz')
  
  l2pxTrue = getVarValue(c, 'top1WDaughter'+str(l2ID)+'Px')
  l2pyTrue = getVarValue(c, 'top1WDaughter'+str(l2ID)+'Py')
  l2pzTrue = getVarValue(c, 'top1WDaughter'+str(l2ID)+'Pz')

  l1pTrue = sqrt(l1pxTrue*l1pxTrue + l1pyTrue*l1pyTrue + l1pzTrue*l1pzTrue)
  l1ptTrue  = sqrt(l1pxTrue**2 + l1pyTrue**2)
  l1PhiTrue = atan2(l1pyTrue, l1pxTrue)
  l1EtaTrue = acosh(l1pTrue/sqrt(l1pxTrue**2 + l1pyTrue**2))*l1pzTrue/(sqrt(l1pzTrue**2))
  l1ThetaTrue = acos(l1pzTrue/l1pTrue)
  
  l2pTrue = sqrt(l2pxTrue*l2pxTrue + l2pyTrue*l2pyTrue + l2pzTrue*l2pzTrue)
  l2ptTrue  = sqrt(l2pxTrue**2 + l2pyTrue**2)
  l2PhiTrue = atan2(l2pyTrue, l2pxTrue)
  l2EtaTrue = acosh(l2pTrue/sqrt(l2pxTrue**2 + l2pyTrue**2))*l2pzTrue/(sqrt(l2pzTrue**2))
  l2ThetaTrue = acos(l2pzTrue/l2pTrue)
  
  if swap: bID = 1
  else:    bID = 0
  
  b1pxTrue = getVarValue(c, 'top'+str(bID)+'bPx')
  b1pyTrue = getVarValue(c, 'top'+str(bID)+'bPy')
  b1pzTrue = getVarValue(c, 'top'+str(bID)+'bPz')
  b1pTrue = sqrt(b1pxTrue*b1pxTrue + b1pyTrue*b1pyTrue + b1pzTrue*b1pzTrue)
  b1ptTrue  = sqrt(b1pxTrue**2 + b1pyTrue**2)
  b1PhiTrue = atan2(b1pyTrue, b1pxTrue)
  b1EtaTrue = acosh(b1pTrue/sqrt(b1pxTrue**2 + b1pyTrue**2))*b1pzTrue/(sqrt(b1pzTrue**2))
  
  b2pxTrue = getVarValue(c, 'top'+str(1-bID)+'bPx')
  b2pyTrue = getVarValue(c, 'top'+str(1-bID)+'bPy')
  b2pzTrue = getVarValue(c, 'top'+str(1-bID)+'bPz')
  b2pTrue = sqrt(b2pxTrue*b2pxTrue + b2pyTrue*b2pyTrue + b2pzTrue*b2pzTrue)
  b2ptTrue  = sqrt(b2pxTrue**2 + b2pyTrue**2)
  b2PhiTrue = atan2(b2pyTrue, b2pxTrue)
  b2EtaTrue = acosh(b2pTrue/sqrt(b2pxTrue**2 + b2pyTrue**2))*b2pzTrue/(sqrt(b2pzTrue**2))
  
  nu1pxTrue = getVarValue(c, 'top0WDaughter'+str(1-l1ID)+'Px')
  nu1pyTrue = getVarValue(c, 'top0WDaughter'+str(1-l1ID)+'Py')
  nu1pzTrue = getVarValue(c, 'top0WDaughter'+str(1-l1ID)+'Pz')
  nu1ptTrue = sqrt(nu1pxTrue*nu1pxTrue + nu1pyTrue*nu1pyTrue)
  nu1pTrue = sqrt(nu1pxTrue*nu1pxTrue + nu1pyTrue*nu1pyTrue + nu1pzTrue*nu1pzTrue)
  nu1PhiTrue = atan2(nu1pyTrue, nu1pxTrue)
  nu1EtaTrue = acosh(nu1pTrue/sqrt(nu1pxTrue**2 + nu1pyTrue**2))*nu1pzTrue/(sqrt(nu1pzTrue**2))
  
  nu2pxTrue = getVarValue(c, 'top1WDaughter'+str(1-l2ID)+'Px')
  nu2pyTrue = getVarValue(c, 'top1WDaughter'+str(1-l2ID)+'Py')
  nu2pzTrue = getVarValue(c, 'top1WDaughter'+str(1-l2ID)+'Pz')
  nu2ptTrue = sqrt(nu2pxTrue*nu2pxTrue + nu2pyTrue*nu2pyTrue)
  nu2pTrue = sqrt(nu2pxTrue*nu2pxTrue + nu2pyTrue*nu2pyTrue + nu2pzTrue*nu2pzTrue)
  nu2PhiTrue = atan2(nu2pyTrue, nu2pxTrue)
  nu2EtaTrue = acosh(nu2pTrue/sqrt(nu2pxTrue**2 + nu2pyTrue**2))*nu2pzTrue/(sqrt(nu2pzTrue**2))
  
  MExGen = getVarValue(c, 'genmetpx') 
  MEyGen = getVarValue(c, 'genmetpy')
# ---- Top True ---
  t1pxTrue = b1pxTrue + l1pxTrue + nu1pxTrue
  t1pyTrue = b1pyTrue + l1pyTrue + nu1pyTrue
  t1pzTrue = b1pzTrue + l1pzTrue + nu1pzTrue
  
  t2pxTrue = b2pxTrue + l2pxTrue + nu2pxTrue
  t2pyTrue = b2pyTrue + l2pyTrue + nu2pyTrue
  t2pzTrue = b2pzTrue + l2pzTrue + nu2pzTrue

  t1ptTrue = sqrt(t1pxTrue**2 + t1pyTrue**2)
  t1pTrue  = sqrt(t1pxTrue**2 + t1pyTrue**2 + t1pzTrue**2)
  t1EtaTrue = acosh(t1pTrue/sqrt(t1pxTrue**2 + t1pyTrue**2))*t1pzTrue/(sqrt(t1pzTrue**2))
  t1PhiTrue = atan2(t1pyTrue, t1pxTrue)
  cosT1ThetaTrue = t1pzTrue/t1pTrue

  t2ptTrue = sqrt(t2pxTrue**2 + t2pyTrue**2)
  t2pTrue = sqrt(t2pxTrue**2 + t2pyTrue**2 + t2pzTrue**2)
  t2EtaTrue = acosh(t2pTrue/sqrt(t2pxTrue**2 + t2pyTrue**2))*t2pzTrue/(sqrt(t2pzTrue**2))
  t2PhiTrue = atan2(t2pyTrue, t2pxTrue)
  cosT2ThetaTrue = t2pzTrue/t2pTrue
  # ---- TTBar True ----
  ttpxTrue = t1pxTrue + t2pxTrue
  ttpyTrue = t1pyTrue + t2pyTrue
  ttpzTrue = t1pzTrue + t2pzTrue

  ttptTrue = sqrt(ttpxTrue**2 + ttpyTrue**2)
  ttpTrue  = sqrt(ttpxTrue**2 + ttpyTrue**2 + ttpzTrue**2)
  ttEtaTrue = acosh(ttpTrue/sqrt(ttpxTrue**2 + ttpyTrue**2))*ttpzTrue/(sqrt(ttpzTrue**2))
  ttPhiTrue = atan2(ttpyTrue, ttpxTrue)
  costtThetaTrue = ttpzTrue/ttpTrue
  # --- Lp ---  FIXME
  W1pxTrue = l1pxTrue + nu1pxTrue
  W1pyTrue = l1pyTrue + nu1pyTrue
  LP1True = (l1pxTrue*W1pxTrue + l1pyTrue*W1pyTrue)/(W1pxTrue**2 + W1pyTrue**2)

  WpxTrue = l2pxTrue + nu2pxTrue
  WpyTrue = l2pyTrue + nu2pyTrue
  LPTrue = (l2pxTrue*WpxTrue + l2pyTrue*WpyTrue)/(WpxTrue**2 + WpyTrue**2)

  deltaPhiTrue = deltaPhi(t1PhiTrue, t2PhiTrue)

  ht1True = getVarValue(c, 'ht')
  ht2True = ht1True
  ht1True_g10 = ht1True
  ht2True_g10 = ht1True

  if l1ptTrue > 40 and abs(l1EtaTrue) < 2.4:
    ht1True = ht1True + l1ptTrue
    ht1True_g10 = ht1True_g10 + l1ptTrue*random.gauss(1, 0.1)
  if nu1ptTrue > 40 and abs(nu1EtaTrue) < 2.4:
    ht1True = ht1True + nu1ptTrue
    ht1True_g10 = ht1True_g10 + nu1ptTrue*random.gauss(1, 0.1)

  if l2ptTrue > 40 and abs(l2EtaTrue) < 2.4:
    ht2True = ht2True + l2ptTrue
    ht2True_g10 = ht2True_g10 + l2ptTrue*random.gauss(1, 0.1)
  if nu2ptTrue > 40 and abs(nu2EtaTrue) < 2.4:
    ht2True = ht2True + nu2ptTrue
    ht2True_g10 = ht2True_g10 + nu2ptTrue*random.gauss(1, 0.1)

  e['MExGen'] = MExGen
  e['MEyGen'] = MEyGen
  e['ht1True']= ht1True
  e['ht2True']= ht2True
  e['ht1True_g10']= ht1True_g10
  e['ht2True_g10']= ht2True_g10

  e['LPTrue'] = LPTrue
  e['deltaPhiTrue'] = deltaPhiTrue
  
  e['l1pxTrue']  = l1pxTrue
  e['l1pyTrue']  = l1pyTrue
  e['l1pzTrue']  = l1pzTrue
  e['l1pTrue']   = l1pTrue
  e['l1ptTrue']  = l1ptTrue
  e['l1PhiTrue'] = l1PhiTrue
  e['l1EtaTrue'] = l1EtaTrue
  e['l1ThetaTrue'] = l1ThetaTrue
  e['l1PdgTrue']   = l1PdgTrue

  e['l2pxTrue']  = l2pxTrue
  e['l2pyTrue']  = l2pyTrue
  e['l2pzTrue']  = l2pzTrue
  e['l2pTrue']   = l2pTrue
  e['l2ptTrue']  = l2ptTrue
  e['l2PhiTrue'] = l2PhiTrue
  e['l2EtaTrue'] = l2EtaTrue
  e['l2Theta']   = l2ThetaTrue
  e['l2PdgTrue'] = l2PdgTrue

  e['b1pxTrue']  = b1pxTrue
  e['b1pyTrue']  = b1pyTrue
  e['b1pzTrue']  = b1pzTrue
  e['b1pTrue']   = b1pTrue
  e['b1ptTrue']  = b1ptTrue
  e['b1PhiTrue'] = b1PhiTrue
  e['b1EtaTrue'] = b1EtaTrue

  e['b2pxTrue']  = b2pxTrue
  e['b2pyTrue']  = b2pyTrue
  e['b2pzTrue']  = b2pzTrue
  e['b2pTrue']   = b2pTrue
  e['b2ptTrue']  = b2ptTrue
  e['b2PhiTrue'] = b2PhiTrue
  e['b2EtaTrue'] = b2EtaTrue

  e['nu1pxTrue']  = nu1pxTrue
  e['nu1pyTrue']  = nu1pyTrue
  e['nu1pzTrue']  = nu1pzTrue
  e['nu1pTrue']   = nu1pTrue
  e['nu1ptTrue']  = nu1ptTrue
  e['nu1PhiTrue'] = nu1PhiTrue
  e['nu1EtaTrue'] = nu1EtaTrue

  e['nu2pxTrue']  = nu2pxTrue
  e['nu2pyTrue']  = nu2pyTrue
  e['nu2pzTrue']  = nu2pzTrue
  e['nu2pTrue']   = nu2pTrue
  e['nu2ptTrue']  = nu2ptTrue
  e['nu2PhiTrue'] = nu2PhiTrue
  e['nu2EtaTrue'] = nu2EtaTrue

  e['t1pxTrue']  = t1pxTrue
  e['t1pyTrue']  = t1pyTrue
  e['t1pzTrue']  = t1pzTrue
  e['t1pTrue']   = t1pTrue
  e['t1ptTrue']  = t1ptTrue
  e['t1PhiTrue'] = t1PhiTrue
  e['t1EtaTrue'] = t1EtaTrue
  e['t1ThetaTrue'] = acos(cosT1ThetaTrue)

  e['t2pxTrue']  = t2pxTrue
  e['t2pyTrue']  = t2pyTrue
  e['t2pzTrue']  = t2pzTrue
  e['t2pTrue']   = t2pTrue
  e['t2ptTrue']  = t2ptTrue
  e['t2PhiTrue'] = t2PhiTrue
  e['t2EtaTrue'] = t2EtaTrue
  e['t2ThetaTrue'] = acos(cosT2ThetaTrue)

  e['ttpxTrue']  = ttpxTrue
  e['ttpyTrue']  = ttpyTrue
  e['ttpzTrue']  = ttpzTrue
  e['ttpTrue']   = ttpTrue
  e['ttptTrue']  = ttptTrue
  e['ttPhiTrue'] = ttPhiTrue
  e['ttEtaTrue'] = ttEtaTrue
  e['ttThetaTrue'] = acos(costtThetaTrue)

  return e

def writeSelection(swap):
  if len(swap) == 2:
    s1 = swap[0] 
    s2 = swap[1]
    event4 = s1+s2 # make one list 
  else:
    event4 = swap[0]

  for f in event4:
    f['Flag_t1ptMin'] = 0
    f['Flag_t2ptMin'] = 0
    f['Flag_ttptMin'] = 0
    f['Flag_chi2Min'] = 0
    f['Flag_sigma1']  = 0
    f['Flag_sigma2']  = 0

  event4 = sorted(event4, key = lambda e: abs(e['ttptMin']))
  event = event4[0] # sort SMALLEST
  event['Flag_ttptMin'] = 1

  event4 = sorted(event4, key = lambda e: abs(e['t1ptMin']))
  event = event4[0] # sort SMALLEST
  event['Flag_t1ptMin'] = 1

  event4 = sorted(event4, key = lambda e: abs(e['t2ptMin']))
  event = event4[0] # sort SMALLEST
  event['Flag_t2ptMin'] = 1

  event4 = sorted(event4, key = lambda e: abs(e['chi2Min']))
  event = event4[0] # sort SMALLEST
  event['Flag_chi2Min'] = 1

  if SHIFT:
    event4 = sorted(event4, key = lambda e: abs(e['sigma_nu1ptMin']))
    event = event4[0] # sort SMALLEST
    event['Flag_sigma1'] = 1

    event4 = sorted(event4, key = lambda e: abs(e['sigma_nu2ptMin']))
    event = event4[0] # sort SMALLEST
    event['Flag_sigma2'] = 1

  return swap

# ======================================================================================
chainstring = "empty"
reweightingHistoFile = "reweightingHisto_Summer2012Private.root"
#reweightingHistoFile = "reweightingHisto_Summer2012-53X.root"

#Variables to be copied from the tuple
variables = ["weight", "run","lumi", "met",  "ht", "genmet", "genmetpx","genmetpy", "njets", "nbtags",  "nvetoMuons", "nvetoElectrons", "ngoodMuons", "ngoodElectrons", "ngoodVertices", "jet0pt", "jet1pt", "jet2pt", "jet3pt"]

#Variables I'll fill myself
extraVariables = ['sign1', 'sign2', 'Reco', 'deltaPhiMin', 'chi2Min', 'swap',
                  'MEx', 'MEy',
                  'ht1Min',  'ht2Min', 'ht1Min_g10', 'ht2Min_g10',
                  'Flag_t1ptMin', 'Flag_t2ptMin', 'Flag_ttptMin', 'Flag_chi2Min',
                  'Flag_sigma1', 'Flag_sigma2', 'sigma_nu1ptMin', 'sigma_nu2ptMin',
                  'nu1ptMin',  'nu1EtaMin',
                  'nu2ptMin',  'nu2EtaMin',
                  'l1px', 'l1py', 'l1pz', 'l1pt', 'l1p', 'l1Eta', 'l1Phi', 'l1Theta', 'l1Pdg',
                  'l2px', 'l2py', 'l2pz', 'l2pt', 'l2p', 'l2Eta', 'l2Phi', 'l2Theta', 'l2Pdg',
                  'b1px', 'b1py', 'b1pz', 'b1pt', 'b1p', 'b1Eta', 'b1Phi',
                  'b2px', 'b2py', 'b2pz', 'b2pt', 'b2p', 'b2Eta', 'b2Phi',
                  't1pxMin',  't1pyMin',  't1pzMin',  't1ptMin',  't1pMin',  't1EtaMin',  't1PhiMin',  't1ThetaMin',
                  't2pxMin',  't2pyMin',  't2pzMin',  't2ptMin',  't2pMin',  't2EtaMin',  't2PhiMin',  't2ThetaMin',
                  'ttpxMin',  'ttpyMin',  'ttpzMin',  'ttptMin',  'ttpMin',  'ttEtaMin',  'ttPhiMin',  'ttThetaMin']

TrueVar =        ['MExGen', 'MEyGen',
                  'ht1True', 'ht2True', 'ht1True_g10', 'ht2True_g10', 'deltaPhiTrue',
                  'nu1ptTrue', 'nu1EtaTrue', 'nu1PhiTrue',
                  'nu2ptTrue', 'nu2EtaTrue', 'nu2PhiTrue',
                  't1pxTrue', 't1pyTrue', 't1pzTrue', 't1ptTrue', 't1pTrue', 't1EtaTrue', 't1PhiTrue', 't1ThetaTrue',
                  't2pxTrue', 't2pyTrue', 't2pzTrue', 't2ptTrue', 't2pTrue', 't2EtaTrue', 't2PhiTrue', 't2ThetaTrue',
                  'ttpxTrue', 'ttpyTrue', 'ttpzTrue', 'ttptTrue', 'ttpTrue', 'ttEtaTrue', 'ttPhiTrue', 'ttThetaTrue'] 

AnalyticVar =    ['nu1ptAna',  'nu1EtaAna',
                  'nu2ptAna',  'nu2EtaAna',
                  'ht1Ana',  'ht2Ana',
                  't1pxAna',  't1pyAna',  't1pzAna',  't1ptAna',  't1pAna',  't1EtaAna',  't1PhiAna',  't1ThetaAna',
                  't2pxAna',  't2pyAna',  't2pzAna',  't2ptAna',  't2pAna',  't2EtaAna',  't2PhiAna',  't2ThetaAna',
                  'ttpxAna',  'ttpyAna',  'ttpzAna',  'ttptAna',  'ttpAna',  'ttEtaAna',  'ttPhiAna',  'ttThetaAna']

extraVariables += TrueVar
#extraVariables += AnalyticVar

Cut   = "ht>100 && nbtags==2" # get electrons and muons   # FIXME SL selection

# ======================================================================================

def getVarValue(c, var, n=0):
  varNameHisto = var
  leaf = c.GetAlias(varNameHisto)
  if leaf!='':
    return c.GetLeaf(leaf).GetValue(n)
  else:
    return float('nan')

structString = "struct MyStruct{ULong_t event;"
for var in variables:
  structString +="Float_t "+var+";"

for var in extraVariables:
  structString +="Float_t "+var+";"

structString   +="};"
ROOT.gROOT.ProcessLine(structString)

from ROOT import MyStruct

s = MyStruct()

def getReweightingHisto(filename=""):
  if filename=="":
    return ""
  rf = ROOT.TFile(filename)
  htmp = rf.Get("ngoodVertices_Data")
  ROOT.gDirectory.cd("PyROOT:/")
  rwHisto = htmp.Clone()
  rf.Close()
  return rwHisto


from defaultMu2012Samples import dy, wjetsInc, ttbar, ttbarPowHeg,  stop, getSignal

T1tttt = {}
T1tttt['Chain'] = 'Events'
T1tttt['specialCuts'] = []
T1tttt['dirname'] = '/data/mhickel/pat_121012/sms/'
T1tttt['bins'] = ['8-TeV-T1tttt']
T1tttt['name'] =  '8-TeV-T1tttt' 
T1tttt['additionalCut'] = 'osetMgl==1000 && osetMN==100'
T1tttt['reweightingHistoFile'] = ''

Matchingup = {}
Matchingup["name"]     = "matchingup";
Matchingup["dirname"] = "/data/mhickel/pat_120917/mc8TeV/"
Matchingup["bins"]    = [ '8TeV-TTJets_matchingup_TuneZ2star']
Matchingup["Chain"] = "Events"
Matchingup["Counter"] = "bool_EventCounter_passed_PAT.obj"

Matchingdown = {}
Matchingdown["name"]     = "matchingdown";
Matchingdown["dirname"] = "/data/mhickel/pat_120917/mc8TeV/"
Matchingdown["bins"]    = [ '8TeV-TTJets_matchingdown_TuneZ2star']
Matchingdown["Chain"] = "Events"
Matchingdown["Counter"] = "bool_EventCounter_passed_PAT.obj"

Scaleup = {}
Scaleup["name"]     = "scaleup";
Scaleup["dirname"] = "/data/mhickel/pat_120917/mc8TeV/"
Scaleup["bins"]    = [ '8TeV-TTJets_scaleup_TuneZ2star']
Scaleup["Chain"] = "Events"
Scaleup["Counter"] = "bool_EventCounter_passed_PAT.obj"

Scaledown = {}
Scaledown["name"]     = "scaledown";
Scaledown["dirname"] = "/data/mhickel/pat_120917/mc8TeV/"
Scaledown["bins"]    = [ '8TeV-TTJets_scaledown_TuneZ2star']
Scaledown["Chain"] = "Events"
Scaledown["Counter"] = "bool_EventCounter_passed_PAT.obj"

doubleMuData={}
doubleMuData["name"]     = "doubleMuData";
doubleMuData["dirname"] = "/data/schoef/pat_120908/data8TeV/"
doubleMuData["bins"]    = [ 'DoubleMu-Run2012A-13Jul2012', 'DoubleMu-Run2012B-13Jul2012', 'DoubleMu-Run2012C-PromptReco', 'DoubleMu-Run2012C-PromptReco-v2']
doubleMuData["Chain"] = "Events"
doubleMuData["Counter"] = "bool_EventCounter_passed_PAT.obj"

doubleEleData={}
doubleEleData["name"]     = "doubleEleData";
doubleEleData["dirname"] = "/data/schoef/pat_120908/data8TeV/"
doubleEleData["bins"]    = [ 'DoubleElectron-Run2012A-13Jul2012', 'DoubleElectron-Run2012B-13Jul2012', 'DoubleElectron-Run2012C-PromptReco', 'DoubleElectron-Run2012C-PromptReco-v2']
doubleEleData["Chain"] = "Events"
doubleEleData["Counter"] = "bool_EventCounter_passed_PAT.obj"

eleMuData={}
eleMuData["name"]     = "eleMuData";
eleMuData["dirname"] = "/data/schoef/pat_120908/data8TeV/"
eleMuData["bins"]    = [ 'MuEG-Run2012A-13Jul2012', 'MuEG-Run2012B-13Jul2012', 'MuEG-Run2012C-PromptReco', 'MuEG-Run2012C-PromptReco-v2']
eleMuData["Chain"] = "Events"
eleMuData["Counter"] = "bool_EventCounter_passed_PAT.obj"

for sample in [dy, wjetsInc, ttbar, ttbarPowHeg,  stop]:
  sample["reweightingHistoFile"] = reweightingHistoFile 

#T6bbzzEv2Samples = []
#T6bbzzEv2 = {}
##for msq in [200, 250, 300, 350, 400, 450, 500, 550, 600]:
#for msq in [175]:
#  T6bbzzEv2[msq]= {}
##  for mN in [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]:
#  for mN in [0]:
#    if msq - mN >= 100:
#      T6bbzzEv2[msq][mN]= {}
#      T6bbzzEv2[msq][mN]["bins"] = ["T6bbzzE_v2"]
#      T6bbzzEv2[msq][mN]["dirname"] = "/data/walten/excess/"
#      T6bbzzEv2[msq][mN]["name"] = "T6bbzzEv2_"+str(msq)+"_"+str(mN)
#      T6bbzzEv2[msq][mN]["additionalCut"] = "(msq=="+str(msq)+"&&mN=="+str(mN)+"&&mC=="+str(mN+70)+")"
##      T6bbzzEv2[msq][mN]["additionalCut"] = "(1)"
#      T6bbzzEv2[msq][mN]["reweightingHistoFile"] = ""
#      T6bbzzEv2[msq][mN]["Chain"] = "Events"
#      T6bbzzEv2Samples.append(T6bbzzEv2[msq][mN])

# ===========================================================================
#for chmode in ['doubleMuData', 'doubleEleData', 'eleMuData']:
for chmode in ['Powheg']:
#for chmode in ['Signal']:
#for chmode in ['MatchingUp', 'MatchingDown', 'ScaleUp', 'ScaleDown']:
# ===========================================================================
#    allSamples = [dy,  wjetsInc, ttbar, ttbarPowHeg,   stop]
  allSamples = []
  if chmode == 'Powheg':
    allSamples = [ttbarPowHeg]
  if chmode == 'Signal':
    allSamples = [T1tttt]

  if chmode == 'MatchingUp':
    allSamples = [Matchingup]
  if chmode == 'MatchingDown':
    allSamples = [Matchingdown]
  if chmode == 'ScaleUp':
    allSamples = [Scaleup]
  if chmode == 'ScaleDown':
    allSamples = [Scaledown]

  if chmode=='doubleMuData':  # FIXME
    allSamples.append(doubleMuData)
  if chmode=='doubleEleData':
    allSamples.append(doubleEleData)
  if chmode=='eleMuData':
    allSamples.append(eleMuData)

#      allSamples = []#T6bbzzEv2Samples
#      allSamples = T6bbzzEv2Samples 
#      if chmode == "doubleMu":
#        allSamples.append(doubleMuData)
#      if chmode == "doubleEle":
#        allSamples.append(doubleEleData)
#      if chmode == "eleMu":
#        allSamples.append(eleMuData)
  for sample in allSamples:
    sample["filenames"]={}
    sample["weight"]={}
    for bin in sample["bins"]:
      subdirname = sample["dirname"]+"/"+bin+"/"
      if sample["bins"]==[""]:
        subdirname = sample["dirname"]+"/"
      c = ROOT.TChain("Events")
      d = ROOT.TChain("Runs")
      sample["filenames"][bin]=[]
      if small:
        filelist=os.listdir(subdirname)
        counter = NumOfFiles   #Joining n files
        for tfile in filelist:
          if os.path.isfile(subdirname+tfile) and tfile[-5:]==".root" and tfile.count("histo")==1:
            sample["filenames"][bin].append(subdirname+tfile)
  #          c.Add(sample["dirname"]+tfile)
            if counter==0:
              break
            counter=counter-1
      else:
        sample["filenames"][bin] = [subdirname+"/h*.root"]
      for tfile in sample["filenames"][bin]:
        c.Add(tfile)
        d.Add(tfile)
      nevents = 0
      nruns = d.GetEntries()
      for i in range(0, nruns):
        d.GetEntry(i)
        nevents += getValue(d,"uint_EventCounter_runCounts_PAT.obj")
      weight = 1.
      if bin == "T6bbzz_v5" or bin == "T6bbzzE_v2" or bin=="T6bbzzB_v1":
        msq = int(sample["name"].split("_")[1])
        mN = int(sample["name"].split("_")[2])
        xsec.xsec[bin] = stop8TeV_NLONLL[msq]
        nevents = c.GetEntries("msq=="+str(msq)+"&&mN=="+str(mN))
        print "Using xsec",stop8TeV_NLONLL[msq],"for",bin,T6bbzzEv2[msq][mN]["name"], "nevents", nevents
      xbin = bin.replace('-pdf', '')
      if xsec.xsec.has_key(xbin):
        if nevents>0:
          weight = xsec.xsec[xbin]*targetLumi/nevents
        else:
          weight = 0.
      print "Sample", sample["name"], "bin", bin, "n-events",nevents,"weight",weight
      
      if sample['name'] == T1tttt['name'] and bin in T1tttt['bins']:
        T1Xsec = 0.0243547     # referenceXSecs.root (1000, 100)
        T1EventCounts = 49998  # just events from (1000, 100)
        weight = T1Xsec*targetLumi/T1EventCounts
      
      sample["weight"][bin]=weight
      del c
      del d

  presel = "None"
  prefixString = ""
  commoncf = "0"
#  commoncf =  "(met>100)"
  commoncf =  Cut
#  if chmode=="doubleMuData":
#    commoncf+="&&nmuons>=2"
#  if chmode=="doubleEleData":
#    commoncf+="&&neles>=2"
#  if chmode=="eleMuData":
#    commoncf+="&&neles+nmuons>=2"
  if chmode=="Powheg":
    commoncf+="&&neles+nmuons>0"

  print "chmode", chmode, sample["name"], "commoncf", commoncf

  if not os.path.isdir(outputDir+"/"+chmode):
    os.system("mkdir "+outputDir+"/"+chmode)
  for sample in allSamples:
    if not os.path.isdir("mkdir "+outputDir+"/"+chmode+"/"+sample["name"]):
      os.system("mkdir "+outputDir+"/"+chmode+"/"+sample["name"])
    else:
      print "Directory", outputDir+"/"+chmode+"/"+sample["name"], "already found"
    t = ROOT.TTree( "Events", "Events", 1 )
    t.Branch("event", ROOT.AddressOf(s, "event"), "event/l")
    for var in variables:
      t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')
    for var in extraVariables:
      t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')
    ofile = outputDir+"/"+chmode+"/"+sample["name"]+"/histo_"+sample["name"]+'_'+str(minF)+'_'+str(maxF)+".root"
    if os.path.isfile(ofile) and overwrite:
      print "Warning! will overwrite",ofile
    if os.path.isfile(ofile) and not overwrite:
      print ofile, "already there! Skipping!!!" 
      continue
    rwHisto = ""
    if sample.has_key("reweightingHistoFile"):
      rwHisto=getReweightingHisto(sample["reweightingHistoFile"])
    if rwHisto!="":
      print "Using reweightingHisto", sample["reweightingHistoFile"], rwHisto,"for sample",sample["name"]
    else:
      print "Using no reweightingHisto for sample",sample["name"]
    for bin in sample["bins"]:
      c = ROOT.TChain(sample["Chain"])
# =======================================================================================
      if small:
        for thisfile in sample["filenames"][bin]:
          c.Add(thisfile)
      else:
        subdirname = sample["dirname"]+"/"+bin+"/"
        if sample["bins"]==[""]:
          subdirname = sample["dirname"]+"/"
        filelist=os.listdir(subdirname)
  
        j = 0
        for thisfile in filelist:
          if os.path.isfile(subdirname + thisfile) and thisfile[-5:]==".root":
             num = int(thisfile.split("_")[1])
             if num>=minF and num<maxF:
               j += 1
               c.Add(subdirname + thisfile)
        print '\033[1;34m #', j, 'Files added\033[1;m ('+str(minF)+'-'+str(maxF)+')'
# =======================================================================================

      ntot = c.GetEntries()
      if ntot>0:
        thiscommoncf = commoncf
        if sample.has_key("additionalCut"):
          thiscommoncf = commoncf+"&&"+sample["additionalCut"]
        c.Draw(">>eList", thiscommoncf)
        elist = ROOT.gDirectory.Get("eList")
        number_events = elist.GetN()
        print "Reading: ", sample["name"], bin, '('+str(minF)+'-'+str(maxF)+')',"with",number_events,"Events using cut", thiscommoncf
        if small:
          if number_events>1000:
            number_events=1000
        for i in range(0, number_events):
          if (i%10000 == 0) and i>0:
            print i, '('+str(number_events)+')'
    #      # Update all the Tuples
          if elist.GetN()>0 and ntot>0:
            c.GetEntry(elist.GetEntry(i))
            nvtxWeight = 1.
            if rwHisto!="" and xsec.xsec.has_key(bin):
              nvtxWeight = rwHisto.GetBinContent(rwHisto.FindBin(getVarValue(c, "ngoodVertices")))
    #                print "nvtx:", c.GetLeaf( "ngoodVertices" ).GetValue(), "bin", rwHisto.FindBin(c.GetLeaf( "ngoodVertices" ).GetValue()),"weight",nvtxWeight
            for var in variables[1:]:
              getVar = var
              if prefixString!="":
                getVar = prefixString+"_"+var
              exec("s."+var+"="+str(getVarValue(c, getVar)).replace("nan","float('nan')"))
#                if bin.count("Run"):
#                  if not checkLumi(s.run, s.lumi):
#  #                  print s.run, s.lumi
#                    continue
            s.weight  = sample["weight"][bin]*nvtxWeight
            s.event = long(c.GetLeaf(c.GetAlias('event')).GetValue())

            for var in extraVariables:
              exec("s."+var+"=float('nan')")

            nmuons = getVarValue(c, "nmuons")
            neles = getVarValue(c, "neles")
            #if (chmode=="doubleMu" and nmuons>=2) or (chmode=="doubleEle" and neles>=2) or (chmode=="eleMu" and nmuons>=1 and neles>=1):
            if (chmode=="Powheg" or chmode == 'Signal' or (chmode=="doubleMuData" and nmuons>=2) or (chmode=="doubleEleData" and neles>=2) or (chmode=="eleMuData" and nmuons>=1 and neles>=1) or 'Matching' in chmode or 'Scale' in chmode):
              allGoodLeptons = getGoodLeptons(c, nmuons, neles)
              goodJets, bjets , s.ht, s.nbtags = getGoodJets(c, allGoodLeptons["leptons"])
              s.njets = len(goodJets)

# ===============================================================================================
              ht = s.ht
              #print "I calculate something!"
              #bjets = getGoodBJets(c)
              #print 'btags: ', s.nbtags, 'len(bjets)', len(bjets), 'goodJets btags:', getVarValue(c, 'nbtags')
              if len(bjets) != 2:
                print 'btags do not match! Found:', len(bjets)
                continue
              if not len(allGoodLeptons['leptons']) == 2:
                continue
              if chmode=='doubleEleData' and not len(allGoodLeptons['electrons']) == 2:
                continue
              if chmode=='doubleMuData' and not len(allGoodLeptons['muons']) == 2:
                continue
              if chmode=='eleMuData' and (not len(allGoodLeptons['muons']) == 1) and (not len(allGoodLeptons['electrons']) == 1):
                continue

              l1Pdg = allGoodLeptons['leptons'][0]['pdg']
              l2Pdg = allGoodLeptons['leptons'][1]['pdg']
            
              signL1 = l1Pdg/abs(l1Pdg)
              signL2 = l2Pdg/abs(l2Pdg)
            
              if signL1 == signL2:    # NOT opposite sign
                #print ' # Event', int(getVarValue(c, 'event')), '\033[1;31mNot opposite sign\033[1;m'
                continue

# ===============================================================================================

              swapEventsRec = [] # Reset
              swapEventsGen = [] # Reset
              for swap in [0,1]: # swap Beauty
              #for swap in [0]: # FIXME
                if not (chmode=='doubleMuData' or chmode=='doubleEleData' or chmode=='eleMuData' or chmode=='Signal'):
                  t0d0pdg = getVarValue(c, "top0WDaughter0Pdg")
                  t1d0pdg = getVarValue(c, "top1WDaughter0Pdg")
                  t0d1pdg = getVarValue(c, "top0WDaughter1Pdg")   # just for saving the pdg
                  t1d1pdg = getVarValue(c, "top1WDaughter1Pdg")   # just for saving the pdg
                  l1ID=-1    # Identify lepton daughter
                  l2ID=-1
                  if abs(t0d0pdg) == 13 or abs(t0d0pdg) == 11:  # if muon or electron
                    l1ID=0
                    l1PdgTrue = t0d0pdg
                  else:
                    l1ID=1
                    l1PdgTrue = t0d1pdg
                  if abs(t1d0pdg) == 13 or abs(t1d0pdg) == 11:
                    l2ID=0
                    l2PdgTrue = t1d0pdg
                  else:
                    l2ID=1
                    l2PdgTrue = t1d1pdg

                  l1pxTrue = getVarValue(c, "top0WDaughter"+str(l1ID)+"Px")
                  l1pyTrue = getVarValue(c, "top0WDaughter"+str(l1ID)+"Py")
                  l1pzTrue = getVarValue(c, "top0WDaughter"+str(l1ID)+"Pz")
            
                  l2pxTrue = getVarValue(c, "top1WDaughter"+str(l2ID)+"Px")
                  l2pyTrue = getVarValue(c, "top1WDaughter"+str(l2ID)+"Py")
                  l2pzTrue = getVarValue(c, "top1WDaughter"+str(l2ID)+"Pz")

                  l1pTrue   = sqrt(l1pxTrue**2 + l1pyTrue**2 + l1pzTrue**2)
                  l1ptTrue  = sqrt(l1pxTrue**2 + l1pyTrue**2)
                  l1PhiTrue = atan2(l1pyTrue, l1pxTrue)
                  l1EtaTrue = acosh(l1pTrue/sqrt(l1pxTrue**2 + l1pyTrue**2))*l1pzTrue/(sqrt(l1pzTrue**2))
                  l1ThetaTrue = acos(l1pzTrue/l1pTrue)

                  l2pTrue   = sqrt(l2pxTrue**2 + l2pyTrue**2 + l2pzTrue**2)
                  l2ptTrue  = sqrt(l2pxTrue**2 + l2pyTrue**2)
                  l2PhiTrue = atan2(l2pyTrue, l2pxTrue)
                  l2EtaTrue = acosh(l2pTrue/sqrt(l2pxTrue**2 + l2pyTrue**2))*l2pzTrue/(sqrt(l2pzTrue**2))
                  l2ThetaTrue = acos(l2pzTrue/l2pTrue)
            
                  if swap: bID = 1
                  else:    bID = 0
                  
                  b1pxTrue = getVarValue(c, "top"+str(bID)+"bPx")
                  b1pyTrue = getVarValue(c, "top"+str(bID)+"bPy")
                  b1pzTrue = getVarValue(c, "top"+str(bID)+"bPz")
                  b1pTrue = sqrt(b1pxTrue*b1pxTrue + b1pyTrue*b1pyTrue + b1pzTrue*b1pzTrue)
                  b1ptTrue  = sqrt(b1pxTrue**2 + b1pyTrue**2)
                  b1PhiTrue = atan2(b1pyTrue, b1pxTrue)
                  b1EtaTrue = acosh(b1pTrue/sqrt(b1pxTrue**2 + b1pyTrue**2))*b1pzTrue/(sqrt(b1pzTrue**2))
            
                  b2pxTrue = getVarValue(c, "top"+str(1-bID)+"bPx")
                  b2pyTrue = getVarValue(c, "top"+str(1-bID)+"bPy")
                  b2pzTrue = getVarValue(c, "top"+str(1-bID)+"bPz")
                  b2pTrue = sqrt(b2pxTrue*b2pxTrue + b2pyTrue*b2pyTrue + b2pzTrue*b2pzTrue)
                  b2ptTrue  = sqrt(b2pxTrue**2 + b2pyTrue**2)
                  b2PhiTrue = atan2(b2pyTrue, b2pxTrue)
                  b2EtaTrue = acosh(b2pTrue/sqrt(b2pxTrue**2 + b2pyTrue**2))*b2pzTrue/(sqrt(b2pzTrue**2))
            
                  nu1pxTrue = getVarValue(c, "top0WDaughter"+str(1-l1ID)+"Px")
                  nu1pyTrue = getVarValue(c, "top0WDaughter"+str(1-l1ID)+"Py")
                  nu1pzTrue = getVarValue(c, "top0WDaughter"+str(1-l1ID)+"Pz")
                  nu1ptTrue = sqrt(nu1pxTrue*nu1pxTrue + nu1pyTrue*nu1pyTrue)
                  nu1pTrue = sqrt(nu1pxTrue*nu1pxTrue + nu1pyTrue*nu1pyTrue + nu1pzTrue*nu1pzTrue)
                  nu1PhiTrue = atan2(nu1pyTrue, nu1pxTrue)
                  nu1EtaTrue = acosh(nu1pTrue/sqrt(nu1pxTrue**2 + nu1pyTrue**2))*nu1pzTrue/(sqrt(nu1pzTrue**2))
            
                  nu2pxTrue = getVarValue(c, "top1WDaughter"+str(1-l2ID)+"Px")
                  nu2pyTrue = getVarValue(c, "top1WDaughter"+str(1-l2ID)+"Py")
                  nu2pzTrue = getVarValue(c, "top1WDaughter"+str(1-l2ID)+"Pz")
                  nu2ptTrue = sqrt(nu2pxTrue*nu2pxTrue + nu2pyTrue*nu2pyTrue)
                  nu2pTrue = sqrt(nu2pxTrue*nu2pxTrue + nu2pyTrue*nu2pyTrue + nu2pzTrue*nu2pzTrue)
                  nu2PhiTrue = atan2(nu2pyTrue, nu2pxTrue)
                  nu2EtaTrue = acosh(nu2pTrue/sqrt(nu2pxTrue**2 + nu2pyTrue**2))*nu2pzTrue/(sqrt(nu2pzTrue**2))
            
                  MExGen = getVarValue(c, "genmetpx") 
                  MEyGen = getVarValue(c, "genmetpy")
# ====================================================================
                l1pt  = allGoodLeptons['leptons'][0]['pt']
                l1Phi = allGoodLeptons['leptons'][0]['phi']
                l1Eta = allGoodLeptons['leptons'][0]['eta']
                l1Pdg = allGoodLeptons['leptons'][0]['pdg']
                
                l2pt  = allGoodLeptons['leptons'][1]['pt']
                l2Phi = allGoodLeptons['leptons'][1]['phi']
                l2Eta = allGoodLeptons['leptons'][1]['eta']
                l2Pdg = allGoodLeptons['leptons'][1]['pdg']
            
                MEx = getVarValue(c, "metpx") 
                MEy = getVarValue(c, "metpy")

                if swap: bSwap = 1
                else:    bSwap = 0
            
                b1pt  = bjets[bSwap]['pt']
                b1Phi = bjets[bSwap]['phi']
                b1Eta = bjets[bSwap]['eta']
            
                b2pt  = bjets[1-bSwap]['pt']
                b2Phi = bjets[1-bSwap]['phi']
                b2Eta = bjets[1-bSwap]['eta']
            
# ====================================================================
# =============================================================================
                for Reco in [0,1]:
                #for Reco in [1]:  # FIXME
                  if Reco:
                    if (chmode=='doubleMuData' or chmode=='doubleEleData' or chmode=='eleMuData' or chmode=='Signal'):  # FIXME
                      continue
                    l1pt  = l1ptTrue
                    l1Phi = l1PhiTrue
                    l1Eta = l1EtaTrue
                    l1Pdg = l1PdgTrue
                    l2pt  = l2ptTrue
                    l2Phi = l2PhiTrue
                    l2Eta = l2EtaTrue
                    l2Pdg = l2PdgTrue

                    b1pt  = b1ptTrue
                    b1Phi = b1PhiTrue
                    b1Eta = b1EtaTrue
                    b2pt  = b2ptTrue
                    b2Phi = b2PhiTrue
                    b2Eta = b2EtaTrue

                    MEx = MExGen
                    MEy = MEyGen

                  e4 = []
                  for sign1 in [-1, +1]:
                    for sign2 in [-1, +1]:
                      e = RecDiLepton(ht, MEx, MEy, l1pt, l1Phi, l1Eta, l2pt, l2Phi, l2Eta, b1pt, b1Phi, b1Eta, b2pt, b2Phi, b2Eta, sign1, sign2)
                      if len(e):
                        if SHIFT:
                          shift = calcSigmaShift(e, ht, MEx, MEy, l1pt, l1Phi, l1Eta, l2pt, l2Phi, l2Eta, b1pt, b1Phi, b1Eta, b2pt, b2Phi, b2Eta, sign1, sign2)  # FIXME
                          e.update(shift) # add sigma value

                        e['swap']  = swap
                        e['event'] = getVarValue(c, 'event')
                        e['run']   = getVarValue(c, 'run')
                        e['lumi']  = getVarValue(c, 'lumi')
                        e['ht']    = getVarValue(c, 'ht')
                        e['Reco']  = 1 - Reco
                        e['l1Pdg'] = l1Pdg
                        e['l2Pdg'] = l2Pdg

                        if not (chmode=='doubleMuData' or chmode=='doubleEleData' or chmode=='eleMuData' or chmode=='Signal'):  # FIXME
                          e = writeTrueVal(c, e, swap, bSwap)

                        #print 'event', e['event'], 'nu1ptMin/nu1ptTrue', e['nu1ptMin']/e['nu1ptTrue'],'(',e['sigma_nu1ptMin'],')', 'nu2ptMin/nu2ptTrue', e['nu2ptMin']/e['nu2ptTrue'],'(',e['sigma_nu2ptMin'],')'

                      if len(e):  e4.append(e)
                    # sign2
                  # sign1
                  # ------------------------------
                  if ANALYTIC:
                    print '---------------------------------- Reco ',1-Reco,'Swap ',swap,'--------------------------------------------------------'
                    #for e in e4:
                    #  print 'event', getVarValue(c, 'event'), 'nu1px :', e['nu1pxMin'], e['nu1pxTrue']

                    ana4 = RecDiLeptonAnalytic(ht, MEx, MEy, l1pt, l1Phi, l1Eta, l1Pdg, l2pt, l2Phi, l2Eta, l2Pdg, b1pt, b1Phi, b1Eta, b2pt, b2Phi, b2Eta, sign1, sign2)
                    if len(ana4):
                      for a in ana4:
                        print 'event', getVarValue(c, 'event'), 'analytic(nu1px,nu2px):', a['nu1pxAna'], a['nu2pxAna']
                  # ------------------------------
                  if (1-Reco):
                    if len(e4): swapEventsRec.append(e4) # append Reco (2) and Swap (2)
                  else:
                    if len(e4): swapEventsGen.append(e4) # append Reco (2) and Swap (2)
                # end Reco
              # end swap
              sys.exit()  # FIXME

# -----------------------------------------------------------------------------------------------
              if len(swapEventsRec):
                swapEventsRec = writeSelection(swapEventsRec) # write (Flag_t1ptMin, Flag_t2ptMin, Flag_ttptMin, Flag_chi2Min, Flag_sigma1, Flag_sigma2)
              if len(swapEventsGen):
                swapEventsGen = writeSelection(swapEventsGen) # write (Flag_t1ptMin, Flag_t2ptMin, Flag_ttptMin, Flag_chi2Min, Flag_sigma1, Flag_sigma2)

              swapEvents = swapEventsRec + swapEventsGen

              for e4 in swapEvents: # e4 -> e8(Rec(4)+Gen(4))
                for e in e4:
                  for var in extraVariables:
                    if not ((chmode=='doubleMuData' or chmode=='doubleEleData' or chmode=='eleMuData' or chmode=='Signal') and var in TrueVar):   # if Data: no TrueVar
                      exec("s."+var+"="+str(e[var]))
                  t.Fill()
              #sys.exit(0)
      
# ===============================================================================================
        del elist
      else:
        print "Zero entries in", bin, sample["name"]
      del c
    if not small:
      f = ROOT.TFile(ofile, "recreate")
      t.Write()
      f.Close()
      print "Written",ofile
    elif small:
      print '\033[1;31mNo saving when small!\033[1;m', '(', ofile, ')'
    del t
    date = datetime.now()
    print str(date.day)+'.'+str(date.month)+'.'+str(date.year)+' '+str(date.hour)+':'+str(date.minute)
