import os, sys, ROOT
from math import cos, sin, sqrt

def getValue(chain, varname):
  alias = chain.GetAlias(varname)
  if alias!="":
    return chain.GetLeaf( alias ).GetValue()
  else:
    return chain.GetLeaf( varname ).GetValue()

def softIsolatedMT(chain):
  lepton_pt   = getValue(chain, "softIsolatedMuPt")
  lepton_phi  = getValue(chain, "softIsolatedMuPhi")
  metphi      = getValue(chain, "type1phiMetphi")
  met         = getValue(chain, "type1phiMet")
  return ROOT.sqrt(2*lepton_pt*met*(1.-cos(lepton_phi - metphi)))

def cosDeltaPhiLepW(chain):
  lPt = getValue(chain, "softIsolatedMuPt")
  lPhi = getValue(chain, "softIsolatedMuPhi")
  metphi = getValue(chain, "type1phiMetphi")
  met = getValue(chain, "type1phiMet")
  cosLepPhi = cos(lPhi)
  sinLepPhi = sin(lPhi)
  mpx = met*cos(metphi)
  mpy = met*sin(metphi)
  pW = sqrt((lPt*cosLepPhi + mpx)**2 + (lPt*sinLepPhi + mpy)**2)

  return ((lPt*cosLepPhi + mpx)*cosLepPhi + (lPt*sinLepPhi + mpy)*sinLepPhi )/pW

