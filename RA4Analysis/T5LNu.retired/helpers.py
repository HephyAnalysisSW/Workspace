import ROOT
from Workspace.HEPHYPythonTools.helpers import getVarValue
from math import cos, sin, sqrt

def nameAndCut(metb, htb, njetb, pdg, btagRequirement='def'):
  cut='nbtags==0'
  if btagRequirement.lower()=='none':
    cut='(1)'
  if btagRequirement.lower()=='noloose':
    cut='(Sum$(jetBtag>0.244)==0)'
  if btagRequirement.lower()=='notight':
    cut='(Sum$(jetBtag>0.898)==0)'
  cut+='&&nTightMuons+nTightElectrons==1'
  cut+='&&type1phiMet>='+str(metb[0])
  name='met'+str(metb[0])
  if metb[1]>0:
    cut+='&&type1phiMet<'+str(metb[1])
    name+='-'+str(metb[1])
  cut+='&&ht>='+str(htb[0])
  name+='_ht'+str(htb[0])
  if htb[1]>0:
    cut+='&&ht<'+str(htb[1])
    name+='-'+str(htb[1])
  cut+='&&njets>='+str(njetb[0])
  name+='_njet'+str(njetb[0])
  if len(njetb)>1 and njetb[1]>0:
    cut+='&&njets<='+str(njetb[1])
    name+='-'+str(njetb[1])
  if pdg.lower()=='pos':
    cut+='&&leptonPdg>0'
    name+='_posPdg'
  if pdg.lower()=='neg':
    cut+='&&leptonPdg<0'
    name+='_negPdg'
  return [name, cut]

def nameAndCutLShape(shape, njetb, pdg, btagRequirement='def'):
  cut='nbtags==0'
  if btagRequirement.lower()=='none':
    cut='(1)'
  if btagRequirement.lower()=='noloose':
    cut='(Sum$(jetBtag>0.244)==0)'
  if btagRequirement.lower()=='notight':
    cut='(Sum$(jetBtag>0.898)==0)'
  cut+='&&nTightMuons+nTightElectrons==1'
  if not shape[0]=="L":return
  n = int(shape[1])
  htL = 400+n*70
  htH = 400+(n+1)*70
  metL =150 +n*40
  metH =150 +(n+1)*40
  cut+='&&(ht>='+str(htL)+'&&type1phiMet>'+str(metL)+')&&(!(ht>='+str(htH)+'&&type1phiMet>='+str(metH)+'))'
  name=shape
  name+='_njet'+str(njetb[0])
  cut+='&&njets>='+str(njetb[0])
  if len(njetb)>1 and njetb[1]>0:
    cut+='&&njets<='+str(njetb[1])
    name+='-'+str(njetb[1])
  if pdg.lower()=='pos':
    cut+='&&leptonPdg>0'
    name+='_posPdg'
  if pdg.lower()=='neg':
    cut+='&&leptonPdg<0'
    name+='_negPdg'
  return [name, cut]

def wRecoPt(chain):
  lPt = getVarValue(chain, "leptonPt")
  lPhi = getVarValue(chain, "leptonPhi")
  metphi = getVarValue(chain, "type1phiMetphi")
  met = getVarValue(chain, "type1phiMet")
  cosLepPhi = cos(lPhi)
  sinLepPhi = sin(lPhi)
  mpx = met*cos(metphi)
  mpy = met*sin(metphi)
  return sqrt((lPt*cosLepPhi + mpx)**2 + (lPt*sinLepPhi + mpy)**2)

def wGenPt(c):
  res=[]
  for i in range(c.ngp):
    if abs(c.gpPdg[i])==24:
      res.append([c.gpM[i], c.gpPt[i]])
  res.sort() 
  if len(res)>0:
    return res[0][1]
  else:
    return float('nan') 


