import random
from math import sqrt
def jerEtaBin(eta):
  aeta = abs(eta)
  if aeta<=.5 : return 0
  if aeta>.5 and aeta<=1.1: return 1
  if aeta>1.1 and aeta<=1.7: return 2
  if aeta>1.7 and aeta<=2.3: return 3
  if aeta>2.3 and aeta<=2.8: return 4
  if aeta>2.8 and aeta<=3.2: return 5
  if aeta>3.2 and aeta<=5.0: return 6
  return -1

def jerDifferenceScaleFactor( eta, jermode = "none"): #https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetResolution
  if jermode.lower()=="none": return 1.
  etab = jerEtaBin(eta)
  if jermode.lower()=="down":
    if etab== 0: return  1.053 
    if etab== 1: return  1.071 
    if etab== 2: return  1.092
    if etab== 3: return  1.162 
    if etab== 4: return  1.192 
    if etab== 5: return  1.332 
    if etab== 6: return  1.0 
  if jermode.lower()=="central":
    if etab== 0: return 1.079
    if etab== 1: return 1.099
    if etab== 2: return 1.121
    if etab== 3: return 1.208
    if etab== 4: return 1.254
    if etab== 5: return 1.395
    if etab== 6: return 1.056
  if jermode.lower()=="up":
    if etab== 0: return 1.105  
    if etab== 1: return 1.127 
    if etab== 2: return 1.150 
    if etab== 3: return 1.254 
    if etab== 4: return 1.316 
    if etab== 5: return 1.458 
    if etab== 6: return 1.247
  return 1.

sigmaMCDict =\
 {0:{'N':-0.34921, 'S':  0.29783, 'C':  0., 'm':  0.47112},
  1:{'N':-0.49974, 'S':  0.33639, 'C':  0., 'm':  0.43069},
  2:{'N':-0.56165, 'S':  0.42029, 'C':  0., 'm':  0.3924 },
  3:{'N':-1.12329, 'S':  0.65789, 'C':  0., 'm':  0.1396 },
  4:{'N': 1.04792, 'S':  0.46676, 'C':  0., 'm':  0.19314},
  5:{'N': 1.89961, 'S':  0.33432, 'C':  0., 'm':  0.36541},
  6:{'N': 1.66267, 'S':  0.3778 , 'C':  0., 'm':  0.43943},
  7:{'N': 1.50961, 'S':  0.22757, 'C':  0., 'm':  0.60094},
  8:{'N': 0.99052, 'S':  0.27026, 'C':  0., 'm':  0.46273},
  9:{'N': 1.37916, 'S':  0.28933, 'C':  0., 'm':  0.6123 }
  }
def sigmaMCParams(eta):
  aeta=abs(eta)
  return sigmaMCDict[min([int(aeta/0.5),9])]

def jerSigmaMCRel(pt, eta):
  p = sigmaMCParams(abs(eta))
  return sqrt(p['N']*abs(p['N'])/pt**2 + p['S']**2*pt**(p['m']-1) + p['C']**2)

def getJetSmearScaleFactor(pt,eta, jermode='central'):
  c_jet = jerDifferenceScaleFactor(eta, jermode)
  sigmaMCRel = jerSigmaMCRel(pt, eta)
  sigma = sqrt(c_jet**2 - 1)*sigmaMCRel
  scale = random.gauss(1,sigma)
  return scale
