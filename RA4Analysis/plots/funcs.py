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

def genLeptonMatch(chain):
  lepton_pt = getValue(chain, "leptonPt")
  if lepton_pt==0:
    return False
  lepton_phi = getValue(chain, "leptonPhi")
  lepton_eta = getValue(chain, "leptonEta")
  for i in ["0", "1"]:
    for j in ["0", "1"]:
      sstring = "top"+i+"WDaughter"+j
#      print sstring
      absPdg = abs(getValue(chain, sstring+"Pdg"))
      if absPdg==11 or absPdg==13:
        px = getValue(chain, sstring+"Px") 
        py = getValue(chain, sstring+"Py") 
        pz = getValue(chain, sstring+"Pz")
        pt = sqrt(px*px + py*py) 
        eta = asinh(pz/pt) 
        deltaPhi = (cos(lepton_phi)*px + sin(lepton_phi)*py)/pt
        deltaR = sqrt(deltaPhi**2 + (eta - lepton_eta)**2)
        deltaPt = pt/lepton_pt
        print "Testing",i,j,absPdg, deltaR, deltaPt
        if deltaR<0.1 and abs(1. - deltaPt)<0.1:
          return True
  return False

def getMTGenFunc(mode, sampleName="TTJets"):
  if sampleName.lower().count("ttjets"):
    if mode=="Mu":
      requPdg=13
      nuMuTot=1
      nuEleTot=0

    if mode=="Ele":
      requPdg=11
      nuMuTot=0
      nuEleTot=1

    def mTgen(chain): 
      if nuMuTot != getValue(chain, "antinuMu") + getValue(chain, "nuMu") or nuEleTot != getValue(chain, "antinuE") + getValue(chain, "nuE") or getValue(chain, "antinuTau") + getValue(chain, "nuTau") !=0:
        return float('nan')
      for i in ["0", "1"]:
        for j in ["0", "1"]:
          sstring = "top"+i+"WDaughter"+j
          absPdg = abs(getValue(chain, sstring+"Pdg"))
          if absPdg==requPdg:
            sstringPartner = "top"+i+"WDaughter"+str(1-int(j))
            px1 = getValue(chain, sstring+"Px") 
            py1 = getValue(chain, sstring+"Py") 
            pt1 = sqrt(px1*px1 + py1*py1) 
            px2 = getValue(chain, sstringPartner+"Px") 
            py2 = getValue(chain, sstringPartner+"Py") 
            pt2 = sqrt(px2*px2 + py2*py2)
            mt =  sqrt(2*pt1*pt2*(1-(px1*px2 + py1*py2)/(pt1*pt2)))
            if mt>140.:
              print str(int(getValue(chain, "event")))+":"+str(int(getValue(chain, "lumi")))+":"+str(int(getValue(chain, "run")))+"  # TTJets "+str(mt)
            return mt

      return float('nan')
    return mTgen
  if sampleName.lower().count("wjets"):
    if mode=="Mu":
      requPdg=13
      nuMuTot=1
      nuEleTot=0

    if mode=="Ele":
      requPdg=11
      nuMuTot=0
      nuEleTot=1

    def mTgen(chain): 
      if nuMuTot != getValue(chain, "antinuMu") + getValue(chain, "nuMu") or nuEleTot != getValue(chain, "antinuE") + getValue(chain, "nuE") or getValue(chain, "antinuTau") + getValue(chain, "nuTau") !=0:
        return float('nan')
      absPdg = abs(getValue(chain, "nu0Pdg"))
      if not absPdg==requPdg+1: print "mTGen: Warning! Inconsistency in NeutrinoPdg"
      pt0  = getValue(chain, "nu0Pt") 
      eta0 = getValue(chain, "nu0Eta") 
      phi0 = getValue(chain, "nu0Phi") 
      pt1  = getValue(chain, "l0Pt") 
      eta1 = getValue(chain, "l0Eta") 
      phi1 = getValue(chain, "l0Phi") 
      mt =  sqrt(2*pt0*pt1*(1-cos(phi0-phi1)))
#      if mt>140.:
#        print str(int(getValue(chain, "event")))+":"+str(int(getValue(chain, "lumi")))+":"+str(int(getValue(chain, "run")))+"  # WJets "+str(mt)
      return mt

    return mTgen

def getMGenFunc(mode):
  if mode=="Mu":
    requPdg=13
    nuMuTot=1
    nuEleTot=0

  if mode=="Ele":
    requPdg=11
    nuMuTot=0
    nuEleTot=1

  def mGen(chain): 
    if nuMuTot != getValue(chain, "antinuMu") + getValue(chain, "nuMu") or nuEleTot != getValue(chain, "antinuE") + getValue(chain, "nuE") or getValue(chain, "antinuTau") + getValue(chain, "nuTau") !=0:
      return float('nan')
    for i in ["0", "1"]:
      for j in ["0", "1"]:
        sstring = "top"+i+"WDaughter"+j
        absPdg = abs(getValue(chain, sstring+"Pdg"))
        if absPdg==requPdg:
          sstringPartner = "top"+i+"WDaughter"+str(1-int(j))
          px1 = getValue(chain, sstring+"Px") 
          py1 = getValue(chain, sstring+"Py") 
          pz1 = getValue(chain, sstring+"Pz") 
          p1 = sqrt(px1*px1 + py1*py1 +pz1*pz1 )
          px2 = getValue(chain, sstringPartner+"Px") 
          py2 = getValue(chain, sstringPartner+"Py") 
          pz2 = getValue(chain, sstringPartner+"Pz") 
          p2 = sqrt(px2*px2 + py2*py2 +pz2*pz2) 
          return sqrt((p1+p2)**2 - (px1+px2)**2 - (py1+py2)**2 - (pz1+pz2)**2) 
    return float('nan')
  return mGen

def getMTOSGenFunc(mode):
  if mode=="Mu":
    requPdg=13
    nuMuTot=1
    nuEleTot=0

  if mode=="Ele":
    requPdg=11
    nuMuTot=0
    nuEleTot=1
  osFunc = getMGenFunc(mode)
  def mTgen(chain): 
    if nuMuTot != getValue(chain, "antinuMu") + getValue(chain, "nuMu") or nuEleTot != getValue(chain, "antinuE") + getValue(chain, "nuE") or getValue(chain, "antinuTau") + getValue(chain, "nuTau") !=0:
      return float('nan')
    for i in ["0", "1"]:
      for j in ["0", "1"]:
        sstring = "top"+i+"WDaughter"+j
        absPdg = abs(getValue(chain, sstring+"Pdg"))
        if absPdg==requPdg:
          sstringPartner = "top"+i+"WDaughter"+str(1-int(j))
          px1 = getValue(chain, sstring+"Px") 
          py1 = getValue(chain, sstring+"Py") 
          pt1 = sqrt(px1*px1 + py1*py1) 
          px2 = getValue(chain, sstringPartner+"Px") 
          py2 = getValue(chain, sstringPartner+"Py") 
          pt2 = sqrt(px2*px2 + py2*py2)
          mt =  sqrt(2*pt1*pt2*(1-(px1*px2 + py1*py2)/(pt1*pt2)))
          m = osFunc(chain)
          if mt>140.:
            print str(int(getValue(chain, "event")))+":"+str(int(getValue(chain, "lumi")))+":"+str(int(getValue(chain, "run")))+"  # mT "+str(mt)+" m "+str(m)
          if abs(m-80.4)<5.:
            return mt

    return float('nan')
  return mTgen


#  return False

def mTGenMet(chain):
#  chain.GetEntry(ievt)
#  print chain, ievt
#  met = getValue(chain, "barepfmet")
#  met = getValue(chain, "met")
  lepton_pt = getValue(chain, "leptonPt")
  lepton_phi = getValue(chain, "leptonPhi")
  metx = getValue(chain, "genmetpx")
  mety = getValue(chain, "genmetpy")
  met = sqrt(metx**2 + mety**2)
#  metx = getValue(chain, "metpx")
#  mety = getValue(chain, "metpy")
  return ROOT.sqrt(2*lepton_pt*(met - (metx*cos(lepton_phi) + mety*sin(lepton_phi))))

def matchedMTtrue(chain):
  if not genLeptonMatch(chain):
    return float('nan')
  lepton_pt = getValue(chain, "leptonPt")
  lepton_phi = getValue(chain, "leptonPhi")
  metx = getValue(chain, "genmetpx")
  mety = getValue(chain, "genmetpy")
  met = sqrt(metx**2 + mety**2)
#  metx = getValue(chain, "metpx")
#  mety = getValue(chain, "metpy")
  return ROOT.sqrt(2*lepton_pt*(met - (metx*cos(lepton_phi) + mety*sin(lepton_phi))))

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
  return ((lPt*cosLepPhi + mpx)*cosLepPhi + (lPt*sinLepPhi + mpy)*sinLepPhi )/pW

  

def cleanMTFunc(cutVal):
  def cleanMT(chain):
    cosDeltaPhi = cosDeltaPhiLepMET(chain)
    if cosDeltaPhi > - cutVal:
      return  getValue(chain, "mT")
    else:
      return float('nan')
  return cleanMT

def rawMET(chain):
  metx = getValue(chain, "rawMetpx")
  mety = getValue(chain, "rawMetpy")
  return ROOT.sqrt(metx**2+mety**2)

def mTbare(chain):
#  chain.GetEntry(ievt)
#  print chain, ievt
#  met = getValue(chain, "barepfmet")
#  met = getValue(chain, "met")
  lepton_pt = getValue(chain, "leptonPt")
  lepton_phi = getValue(chain, "leptonPhi")
  metx = getValue(chain, "rawMetpx")
  mety = getValue(chain, "rawMetpy")
  met = sqrt(metx**2 + mety**2)
#  metx = getValue(chain, "metpx")
#  mety = getValue(chain, "metpy")
  return ROOT.sqrt(2*lepton_pt*(met - (metx*cos(lepton_phi) + mety*sin(lepton_phi))))

def type1phiMT(chain):
  lepton_pt = getValue(chain, "leptonPt")
  lepton_phi = getValue(chain, "leptonPhi")
  metx = getValue(chain, "type1phiMetpx")
  mety = getValue(chain, "type1phiMetpy")
  met = sqrt(metx**2 + mety**2)
#  metx = getValue(chain, "metpx")
#  mety = getValue(chain, "metpy")
  return ROOT.sqrt(2*lepton_pt*(met - (metx*cos(lepton_phi) + mety*sin(lepton_phi))))

def nljets(chain):
  return getValue(chain, "njets") - getValue(chain, "nbtags")

def metFunc(chain):
  metpx = getValue(chain, "metpx")
  metpy = getValue(chain, "metpy")
  return sqrt(metpx**2 + metpy**2) 

def typeIMetOverPFMet(chain):
  met = getValue(chain, "met")
  barepfmet = getValue(chain, "barepfmet")
  return met/barepfmet 

def kinMetSigbare(chain):
  met = getValue(chain, "barepfmet")
  ht = getValue(chain, "ht")
  return met/ROOT.sqrt(ht)

def kinMetSig(chain):
  met = getValue(chain, "met")
  ht = getValue(chain, "ht")
  return met/ROOT.sqrt(ht)

def top_m0_p(chain):
  pt = getValue(chain, "top_m0_pt")
  pz = getValue(chain, "top_m0_pz")
  return ROOT.sqrt(pt*pt+pz*pz)

def s_inv_m(chain):
  pt0 = getValue(chain, "top_m0_pt")
  pz0 = getValue(chain, "top_m0_pz")
  pt1 = getValue(chain, "top_m1_pt")
  pz1 = getValue(chain, "top_m1_pz")
  xa = ROOT.sqrt(pt0*pt0+pz0*pz0)/3500
  xb = ROOT.sqrt(pt1*pt1+pz1*pz1)/3500

  return xa*xb*7000**2 

def deltaPhiLepMet(chain):
  leptonPhi = getValue(chain, "leptonPhi")
  metpx    = getValue(chain, "metpxUncorr")
  metpy    = getValue(chain, "metpyUncorr")
  metPhi = atan(metpy/metpx)
  return abs( (leptonPhi - metPhi) % (2*3.1415926) )

def fakeMet(chain):
  metpx = getValue(chain, "type1phiMetpx")
  metpy = getValue(chain, "type1phiMetpy")
  genmetpx = getValue(chain, "genmetpx")
  genmetpy = getValue(chain, "genmetpy")
#  print "met px", metpx, "met py", metpy, "genmet x", genmetpx, "genmet y", genmetpx, "ht", getValue(chain, "ht").GetValue(), chain.GetLeaf("jet2pt")
  return ROOT.sqrt((metpx - genmetpx)**2 + (metpy - genmetpy)**2)
#def s_inv_t(chain):
#  pt0 = getValue(chain, "top_0_pt")
#  pz0 = getValue(chain, "top_0_pz")
#  E0= ROOT.sqrt(pt0**2+pz0**2)
#  pt1 = getValue(chain, "top_1_pt")
#  pz1 = getValue(chain, "top_1_pz")
#  E1 = ROOT.sqrt(pt1**2+pz1**2)
#
#
#  return 

def htThrustLepRatio(chain):
  ht = getValue(chain, "ht")
  htThrustLepSide = getValue(chain, "htThrustLepSide")
  return htThrustLepSide/ht

def htThrustOppRatio(chain):
  ht = getValue(chain, "ht")
  htThrustOppSide = getValue(chain, "htThrustOppSide")
  return htThrustOppSide/ht

def minDeltaPhiOverPi(chain):
  return getValue(chain, "minDeltaPhi")/ROOT.TMath.Pi()

def genLP(chain):
  lepton_pt = getValue(chain,"leptonPt")
  lepton_phi = getValue(chain,"leptonPhi")
  metpx = getValue(chain,"genmetpx")
  metpy = getValue(chain,"genmetpy")

  lp_var = -1 + 2*((lepton_pt*cos(lepton_phi) + metpx)*(lepton_pt*cos(lepton_phi)) + (lepton_pt*sin(lepton_phi) + metpy)*(lepton_pt*sin(lepton_phi)) )/((lepton_pt*cos(lepton_phi) + metpx)**2 + (lepton_pt*sin(lepton_phi) + metpy)**2)

  return lp_var

def recoLP(chain):
  lepton_pt = getValue(chain,"leptonPt")
  lepton_phi = getValue(chain,"leptonPhi")
  metpx = getValue(chain,"metpx")
  metpy = getValue(chain,"metpy")

  lp_var = -1 + 2*((lepton_pt*cos(lepton_phi) + metpx)*(lepton_pt*cos(lepton_phi)) + (lepton_pt*sin(lepton_phi) + metpy)*(lepton_pt*sin(lepton_phi)) )/((lepton_pt*cos(lepton_phi) + metpx)**2 + (lepton_pt*sin(lepton_phi) + metpy)**2)

  return lp_var

  
