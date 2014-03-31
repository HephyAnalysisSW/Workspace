from math import sqrt, cos, sin
import ROOT
from Workspace.HEPHYPythonTools.helpers import getVarValue

def deltaPhi( phi1, phi2):
  dphi = phi2-phi1
  if  dphi > pi:
    dphi -= 2.0*pi
  if dphi <= -pi:
    dphi += 2.0*pi
  return abs(dphi)

def cosDeltaPhiLepMET(chain):
  lepton_pt = getVarValue(chain, "leptonPt")
  met = getVarValue(chain, "met")
  mT = getVarValue(chain, "mT")
  res =  1. - mT**2/(2.*met*lepton_pt)
  return res

def cosDeltaPhiLepW(chain):
  lPt = getVarValue(chain, "leptonPt")
  lPhi = getVarValue(chain, "leptonPhi")
  mpx = getVarValue(chain, "type1phiMetpx")
  mpy = getVarValue(chain, "type1phiMetpy")
  cosLepPhi = cos(lPhi)
  sinLepPhi = sin(lPhi)
  pW = sqrt((lPt*cosLepPhi + mpx)**2 + (lPt*sinLepPhi + mpy)**2)

  return ((lPt*cosLepPhi + mpx)*cosLepPhi + (lPt*sinLepPhi + mpy)*sinLepPhi )/pW

  

