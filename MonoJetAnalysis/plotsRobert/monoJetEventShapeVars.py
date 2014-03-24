import ROOT, os, sys
from math import *
paths = ['../../HEPHYCommonTools/python']
for path in [os.path.abspath(p) for p in paths]:
  if not path in sys.path:
    sys.path.insert(1, path)

from helpers import getVarValue, deltaPhi, getJets
import array

def px(obj):
  return obj['pt'] * cos(obj['phi'])

def py(obj):
  return obj['pt'] * sin(obj['phi'])

def pz(obj):
  return obj['pt'] * sinh(obj['eta'])

def psquare(x, y, z):
  return (x * x) + (y * y) + (z * z)

#def calcSphericity(jets):
#  msum = ROOT.TMatrixDSym(3)
#  msum_lin = ROOT.TMatrixDSym(3)
#  p2sum = 0
#  p2sum_lin = 0
#
#  for i in range(3):
#    for j in range(3):
#      msum[i][j] = 0
#      msum_lin[i][j] = 0
#
#  for obj in jets:
#    x = px(obj)
#    y = py(obj)
#    z = pz(obj)
#
#    psq = psquare(x, y, z)
#    p2sum += psq
#    sqrtPsq = sqrt(psq) 
#    p2sum_lin += sqrtPsq
#    msum[0][0] += x * x
#    msum[0][1] += x * y
#    msum[0][2] += x * z
#
#    msum[1][0] += y * x 
#    msum[1][1] += y * y
#    msum[1][2] += y * z
#
#    msum[2][0] += z * x
#    msum[2][1] += z * y
#    msum[2][2] += z * z
#
#    msum_lin[0][0] += x * x / sqrtPsq
#    msum_lin[0][1] += x * y / sqrtPsq
#    msum_lin[0][2] += x * z / sqrtPsq
#
#    msum_lin[1][0] += y * x / sqrtPsq
#    msum_lin[1][1] += y * y / sqrtPsq
#    msum_lin[1][2] += y * z / sqrtPsq
#
#    msum_lin[2][0] += z * x / sqrtPsq
#    msum_lin[2][1] += z * y / sqrtPsq
#    msum_lin[2][2] += z * z / sqrtPsq
#     
###    s = ROOT.TMatrixD(s,ROOT.kPlus,a)
##    for i in range(3):
##      for j in range(3):
##        msum[i][j] = msum[i][j] + a[i][j]
#
#  for n in range(3):
#    for m in range(3):
#      msum[n][m] = msum[n][m] / p2sum
#      msum_lin[n][m] = msum_lin[n][m] / p2sum_lin
#
#  ep = ROOT.TMatrixDSymEigen(msum)
#  ev = ep.GetEigenValues()
#  if len(jets)>2 and (ev[0] < 0 or ev[1] < 0 or ev[2] < 0):
#    print '[Sphericity], Warning: ev < 0, len:',len(jets)
#    print ev[0], ev[1] , ev[2]
#  s = ((ev[2] + ev[1]) * 3) / 2
#
#  ep_lin = ROOT.TMatrixDSymEigen(msum_lin)
#  ev_lin = ep_lin.GetEigenValues()
#  if len(jets)>2 and (ev_lin[0] < 0 or ev_lin[1] < 0 or ev_lin[2] < 0):
#    print '[Sphericity], Warning: ev_lin < 0, len:',len(jets)
#    print ev_lin[0], ev_lin[1] , ev_lin[2]
#  s_lin = ((ev_lin[2] + ev_lin[1]) * 3) / 2
#
#  return {'sphericity':s, "ev":ev, "linSphericity":s_lin, "linEv":ev_lin}
#
#def circularity(ev3D):
#  c = (2 * ev3D[1]) / (ev3D[1] + ev3D[0])
#  return c

def calcCircularity2D(jets):
  msum = ROOT.TMatrixDSym(2)
  msum_lin = ROOT.TMatrixDSym(2)
  for i in range(2):
    for j in range(2):
      msum[i][j] = 0
      msum_lin[i][j] = 0

  p2sum = 0
  p2sum_lin = 0
  for obj in jets:
    x = px(obj)
    y = py(obj)
    psq = (x * x) + (y * y)
    p2sum += psq
    SqrtPsq = sqrt(psq)
    p2sum_lin += SqrtPsq
    msum[0][0] += x * x
    msum[0][1] += x * y
    msum[1][0] += y * x
    msum[1][1] += y * y
    msum_lin[0][0] += x * x / SqrtPsq
    msum_lin[0][1] += x * y / SqrtPsq
    msum_lin[1][0] += y * x / SqrtPsq
    msum_lin[1][1] += y * y / SqrtPsq

  for n in range(2):
    for m in range(2):
      msum[n][m] = msum[n][m] / p2sum
      msum_lin[n][m] = msum_lin[n][m] / p2sum_lin

  ep = ROOT.TMatrixDSymEigen(msum)
  ev = ep.GetEigenValues()
  if ev[0] < 0 or ev[1] < 0:
    print '[circularity2D], Warning: ev < 0, len:',len(jets)
    print ev[0], ev[1] 
  c2D = (2 * ev[1]) / (ev[0] + ev[1])
  ep_lin = ROOT.TMatrixDSymEigen(msum_lin)
  ev_lin = ep_lin.GetEigenValues()
  if ev_lin[0] < 0 or ev_lin[1] < 0:
    print '[circularity2D], Warning: ev_lin < 0, len:',len(jets)
    print ev_lin[0], ev_lin[1] 
  c2D_lin = (2 * ev_lin[1]) / (ev_lin[0] + ev_lin[1])

  return {"c2D":c2D,"linC2D":c2D_lin}

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

def calcFoxWolframMoments(jets):
  psum = 0  
  for obj in jets:
    pt = obj['pt']
    psum += pt
    
#  ht0 = 0
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
#      P0 = 1
      P1 = ctheta
      P2 = ((3 * ctheta * ctheta) - 1) / 2. 
      P3 = ((5 * ctheta * ctheta * ctheta) - (3 * ctheta)) / 2. 
      P4 = ((35 * ctheta * ctheta * ctheta * ctheta) - (30 * ctheta * ctheta) + 3) / 8.
 
#      ht0 += wt * P0
      ht1 += wt * P1
      ht2 += wt * P2
      ht3 += wt * P3
      ht4 += wt * P4

#  return  {"FWMT0":ht0,"FWMT1":ht1,"FWMT2":ht2,"FWMT3":ht3,"FWMT4":ht4}
  return  {"FWMT1":ht1,"FWMT2":ht2,"FWMT3":ht3,"FWMT4":ht4}

#def calcHTRatio(jets, metPhi):
#  htRatio = -1
#  den=0.
#  num=0.
#  for j in jets:
#    den+=j["pt"]
#    if abs(deltaPhi(metPhi, j["phi"])) <= pi/2:
#      num+=j["pt"]
#  if len(jets)>0:
#    htRatio = num/den
#  return htRatio

ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/Thrust.C+")

def calcThrust(jets, l, m):
  p_x = [cos(l["phi"])*l["pt"]] + [cos(m["phi"])*m["pt"]] + [cos(j['phi'])*j['pt'] for j in jets]
  p_y = [sin(l["phi"])*l["pt"]] + [sin(m["phi"])*m["pt"]] + [sin(j['phi'])*j['pt'] for j in jets]

  ht = 0.
  thrust = ROOT.Thrust(2+len(jets), array.array('d', p_x), array.array('d', p_y))
  th = thrust.thrust()
  thPhi = thrust.thrustPhi()
  thEta = thrust.thrustEta()
  if thEta>0.1:
      print "transversal thrust.eta() not zero?", th.thrust(), "jets",jets,"lepton",l,"met",m
  if cos(l['phi'] - thPhi)>0:
    sign = 1
  else:
    sign=-1
  htThrustLepSide = 0.
  for j in jets:
    ht+=j['pt']
    if sign*cos(thPhi - j['phi'])>0:
      htThrustLepSide+=j['pt']

  if cos(m['phi'] - thPhi)>0:
    sign = 1
  else:
    sign=-1
  htThrustMetSide = 0.
  for j in jets:
    if sign*cos(thPhi - j['phi'])>0:
      htThrustMetSide+=j['pt']
  return {'thrust':th, 'htThrustLepSide':htThrustLepSide/ht, 'htThrustMetSide':htThrustMetSide/ht}  


def getRelevantObjects(c):
  return {'jets':getJets(c), \
          'mu':{'pt':getVarValue(c, 'softIsolatedMuPt'), 'phi':getVarValue(c, 'softIsolatedMuPhi')},
          'met':{'pt':getVarValue(c, 'type1phiMet'), 'phi':getVarValue(c, 'type1phiMetphi')} }

def foxWolframMoments(c):
  objs = getRelevantObjects(c)
  return calcFoxWolframMoments(objs['jets'] + [objs['mu']] + [objs['met']])

def circularity2D(c):
  objs = getRelevantObjects(c)
  return calcCircularity2D(objs['jets'] + [objs['mu']] + [objs['met']])

def thrust(c):
  objs = getRelevantObjects(c)
  return calcThrust(objs['jets'], objs['mu'], objs['met'])

#def htRatio(c):
#  objs = getRelevantObjects(c)
##  print objs['jets'], objs['met']['phi']
#  return calcHTRatio(objs['jets'], objs['met']['phi'])
