from math import *
import ROOT
from simplePlotsCommon import getValue

def deltaPhi( phi1, phi2):
  dphi = phi2-phi1
  if  dphi > pi:
    dphi -= 2.0*pi
  if dphi <= -pi:
    dphi += 2.0*pi
  return abs(dphi)

def cosDeltaPhiLepMET(chain):
  lepton_pt = getValue(chain, "leptonPt")
  met = getValue(chain, "met")
  mT = getValue(chain, "mT")
  res =  1. - mT**2/(2.*met*lepton_pt)
  return res

def cosDeltaPhiLepW(chain):
  lPt = getValue(chain, "leptonPt")
  lPhi = getValue(chain, "leptonPhi")
  mpx = getValue(chain, "type1phiMetpx")
  mpy = getValue(chain, "type1phiMetpy")
  cosLepPhi = cos(lPhi)
  sinLepPhi = sin(lPhi)
  pW = sqrt((lPt*cosLepPhi + mpx)**2 + (lPt*sinLepPhi + mpy)**2)

  return ((lPt*cosLepPhi + mpx)*cosLepPhi + (lPt*sinLepPhi + mpy)*sinLepPhi )/pW

  

