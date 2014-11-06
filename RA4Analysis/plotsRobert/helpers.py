import ROOT
from Workspace.HEPHYPythonTools.helpers import getVarValue
from math import cos, sin, sqrt, acos

def stage2MT(c):
  met=c.GetLeaf('met').GetValue()
  leptonPt=c.GetLeaf('leptonPt').GetValue()
  metphi=c.GetLeaf('metPhi').GetValue()
  leptonPt=c.GetLeaf('leptonPt').GetValue()
  leptonPhi=c.GetLeaf('leptonPhi').GetValue()
  return sqrt(2.*leptonPt*met*(1.-cos(leptonPhi-metphi)))
def stage2DPhi(c):
  met=c.GetLeaf('met').GetValue()
  leptonPt=c.GetLeaf('leptonPt').GetValue()
  metphi=c.GetLeaf('metPhi').GetValue()
  leptonPt=c.GetLeaf('leptonPt').GetValue()
  leptonPhi=c.GetLeaf('leptonPhi').GetValue()
  cdp  = cos(leptonPhi-metphi)
  return acos((leptonPt+met*cdp)/sqrt(leptonPt**2+met**2+2*met*leptonPt*cdp)) 
def cmgMT(c):
  met=c.GetLeaf('met_pt').GetValue()
  leptonPt=c.GetLeaf('leptonPt').GetValue()
  metphi=c.GetLeaf('met_phi').GetValue()
  leptonPt=c.GetLeaf('leptonPt').GetValue()
  leptonPhi=c.GetLeaf('leptonPhi').GetValue()
  return sqrt(2.*leptonPt*met*(1.-cos(leptonPhi-metphi)))
def cmgDPhi(c):
  met=c.GetLeaf('met_pt').GetValue()
  leptonPt=c.GetLeaf('leptonPt').GetValue()
  metphi=c.GetLeaf('met_phi').GetValue()
  leptonPhi=c.GetLeaf('leptonPhi').GetValue()
  cdp  = cos(leptonPhi-metphi)
  return acos((leptonPt+met*cdp)/sqrt(leptonPt**2+met**2+2*met*leptonPt*cdp)) 
def cmgST(c):
  met=c.GetLeaf('met_pt').GetValue()
  leptonPt=c.GetLeaf('leptonPt').GetValue()
  return  met+leptonPt 

def nJetBinName(njb):
  n=str(list(njb)[0])+"#leq n_{jet}"
  if len(njb)>1 and njb[1]>-1:
    n+='#leq '+str(njb[1])
  return n
def nBTagBinName(btb):
  n=str(list(btb)[0])+"#leq n_{b-tag}"
  if len(btb)>1 and btb[1]>-1:
    n+='#leq '+str(btb[1])
  return n
def varBinName(vb, var):
  n=str(list(vb)[0])+"< "+var
  if len(vb)>1 and vb[1]>0:
    n+='< '+str(vb[1])
  return n
  

def nameAndCut(stb, htb, njetb, btb=None, presel="(1)", charge="", btagVar = 'nBJetMedium40'):
  cut=presel
  name=""
  if stb:
    cut+='&&st>='+str(stb[0])
    name+='st'+str(stb[0])
    if stb[1]>0:
      cut+='&&st<'+str(stb[1])
      name+='-'+str(stb[1])
  if htb:
    cut+='&&htJet40ja>='+str(htb[0])
    name+='_ht'+str(htb[0])
    if htb[1]>0:
      cut+='&&htJet40ja<'+str(htb[1])
      name+='-'+str(htb[1])
  if njetb:
    cut+='&&nJet40a>='+str(njetb[0])
    name+='_njet'+str(njetb[0])
    if len(njetb)>1 and njetb[1]>=0:
      cut+='&&nJet40a<='+str(njetb[1])
      name+='-'+str(njetb[1])
  if btb:
    cut+='&&'+btagVar+'>='+str(btb[0])
    name+='_nbtag'+str(btb[0])
    if len(btb)>1 and btb[1]>=0:
      cut+='&&'+btagVar+'<='+str(btb[1])
      name+='-'+str(btb[1])
  if charge.lower()=='pos':
    cut+='&&leptonPdg<0'
    name+='_posCharge'
  if charge.lower()=='neg':
    cut+='&&leptonPdg>0'
    name+='_negCharge'
  if name.startswith('_'):name=name[1:]
  return [name, cut]


#def wRecoPt(chain):
#  lPt = getVarValue(chain, "leptonPt")
#  lPhi = getVarValue(chain, "leptonPhi")
#  metphi = getVarValue(chain, "type1phiMetphi")
#  met = getVarValue(chain, "type1phiMet")
#  cosLepPhi = cos(lPhi)
#  sinLepPhi = sin(lPhi)
#  mpx = met*cos(metphi)
#  mpy = met*sin(metphi)
#  return sqrt((lPt*cosLepPhi + mpx)**2 + (lPt*sinLepPhi + mpy)**2)
#
#def wGenPt(c):
#  res=[]
#  for i in range(c.ngp):
#    if abs(c.gpPdg[i])==24:
#      res.append([c.gpM[i], c.gpPt[i]])
#  res.sort() 
#  if len(res)>0:
#    return res[0][1]
#  else:
#    return float('nan') 


