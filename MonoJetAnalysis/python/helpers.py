import ROOT
from math import pi, sqrt, cos

def getObjFromFile(fname, hname):
  f = ROOT.TFile(fname)
  assert not f.IsZombie()
  f.cd()
  htmp = f.Get(hname)
  if not htmp:  return htmp
  ROOT.gDirectory.cd('PyROOT:/')
  res = htmp.Clone()
  f.Close()
  return res


def passPUJetID(flag, level="Tight"): #Medium, #Loose,  kTight  = 0,   kMedium = 1,   kLoose  = 2
  if type(level)==type(0):
    return ( flag & (1 << level) ) != 0
  if level=="Tight":
    l=0
  if level=="Medium":
    l=1
  if level=="Loose":
    l=2
  return ( flag & (1 << l) ) != 0

def getVarValue(c, var, n=0):
  varNameHisto = var
  leaf = c.GetAlias(varNameHisto)
  if leaf!='':
    return c.GetLeaf(leaf).GetValue(n)
  else:
    l = c.GetLeaf(var)
    if l:return l.GetValue(n)
    return float('nan')

#def getValue(chain, varname):
#  alias = chain.GetAlias(varname)
#  if alias!='':
#    return chain.GetLeaf( alias ).GetValue()
#  else:
#    return chain.GetLeaf( varname ).GetValue()
#

def deltaPhi(phi1, phi2):
  dphi = phi2-phi1
  if  dphi > pi:
    dphi -= 2.0*pi
  if dphi <= -pi:
    dphi += 2.0*pi
  return abs(dphi)

def minAbsDeltaPhi(phi, phis):
  if len(phis) > 0:
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
  return sqrt(deltaPhi(l1['phi'], l2['phi'])**2 + (l1['eta'] - l2['eta'])**2)

def getJets(c):
  njets = int(c.GetLeaf('njetCount').GetValue())
  jets =[]
  for i in range(njets):
    jets.append({'pt':getVarValue(c, 'jetPt', i), 'eta':getVarValue(c, 'jetEta', i), 'phi':getVarValue(c, 'jetPhi', i)})
  return jets

def calcHTRatio(jets, metPhi):
  htRatio = -1
  den=0.
  num=0.
  for j in jets:
    den+=j["pt"]
    if abs(deltaPhi(metPhi, j["phi"])) <= pi/2:
      num+=j["pt"]
  if len(jets)>0:
    htRatio = num/den
  return htRatio

def calcHTRatio(jets, metPhi):
  htRatio = -1
  den=0.
  num=0.
  for j in jets:
    den+=j["pt"]
    if abs(deltaPhi(metPhi, j["phi"])) <= pi/2:
      num+=j["pt"]
  if len(jets)>0:
    htRatio = num/den
  return htRatio


def htRatio(c):
  jets = getJets(c)
  metPhi = c.GetLeaf('type1phiMetphi').GetValue()
#  print calcHTRatio(jets, metPhi)
  return calcHTRatio(jets, metPhi)

def KolmogorovDistance(s0, s1): #Kolmogorov distance from two list of values (unbinned, discrete)
  from fractions import Fraction, gcd

  s0.sort()
  s1.sort()

  tot = [[x,0] for x in s0] + [[x,1] for x in s1]
  tot.sort()
  F={}
  lenS={}
  lenS[0] = len(s0)
  lenS[1] = len(s1)
  F[0] = 0
  F[1] = 0
  l = len(tot)
#  print tot
  maxDist = Fraction(0,1)
  for i, t in enumerate(tot):
#    print "Now",F
    F[t[1]]+=1#lenS[t[1]]
#    print "...",F
    if i+1<l and tot[i+1][0]==t[0]:
      continue
#    print "Calc dist..."
    dist= abs(Fraction(F[0],lenS[0])-Fraction(F[1],lenS[1]))
    if dist>maxDist:
      maxDist=dist
#    print dist, maxDist
  return maxDist

def KolmogorovProbability(s0, s1):
  ksDist = float(KolmogorovDistance(s0, s1))
  return ROOT.TMath.KolmogorovProb(ksDist*sqrt(len(s0)*len(s1)/float(len(s0)+len(s1))))

