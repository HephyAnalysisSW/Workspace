import ROOT
import os, sys
from math import sqrt

from Workspace.HEPHYPythonTools.helpers import calcMT, getVarValue

cWJetsHT150v2 = ROOT.TChain("Events")
cWJetsHT150v2.Add("/data/schoef/monoJetTuples_v5/copy/WJetsHT150v2/histo_WJetsHT150v2.root")

data = ROOT.TChain("Events")
data.Add("/data/schoef/monoJetTuples_v5/copy/data/histo_data.root")


#Preselectionw/o soft lepton 

selection = "isrJetPt>110&&type1phiMet>200&&isrJetBTBVetoPassed&&nHardElectrons+nHardMuonsRelIso02+nHardTaus==0&&njet60<=2&&type1phiMet>300.&&Sum$(jetBtag>0.679&&abs(jetEta)<2.4)==0&&ht>400"

def getSoftMuon(c):
  for imu in reversed(range(int(getVarValue(c, 'nmuCount')))):
    relIso = getVarValue(c, 'muRelIso', imu)
    pt = getVarValue(c, 'muPt', imu)
    isGlobal = getVarValue(c, 'muIsGlobal', imu)
    isTracker = getVarValue(c, 'muIsTracker', imu)
    dz = getVarValue(c, 'muDz', imu)
    eta=getVarValue(c, 'muEta', imu)
    if (isGlobal or isTracker) and pt>5. and abs(eta)<2.1 and abs(dz)<0.5:
      if (pt<20. and pt*relIso<10):
        return {'pt':pt, 'eta':eta, 'phi':getVarValue(c, 'muPhi', imu), 'pdg':getVarValue(c, 'muPdg', imu)}

def muRequirement(mu):
  return mu['pt']>5 and abs(mu['eta'])<1.5


from Workspace.MonoJetAnalysis.polSys import calcPolWeights
print selection
for pdgSign in [-1,+1]:
  cut = selection
  res={}
  for j, c in enumerate([cWJetsHT150v2, data]) :
    c.Draw('>>eList', cut) 
    eList = ROOT.gDirectory.Get('eList')
    if j==0:
      y={}
      ye={}
    else:
      y=0
      ye=0
    for i in range(eList.GetN()):
#      if not i%10000: print "At",i,"/",eList.GetN()
      c.GetEntry(eList.GetEntry(i))
      mu = getSoftMuon(c)
      if mu and muRequirement(mu) and pdgSign==mu['pdg']/abs(mu['pdg']):
        mT = calcMT(mu, {'pt':getVarValue(c, 'type1phiMet'), 'phi':getVarValue(c, 'type1phiMetphi')})
        if mT>60 and mT<88:
          if j==0:
            w = getVarValue(c, 'puWeight')
            pol = calcPolWeights(c)
            for k in pol.keys():
              if not y.has_key(k):
                y[k] = w*pol[k] 
                ye[k] = (w*pol[k])**2
              else:
                y[k]  += w*pol[k] 
                ye[k] += (w*pol[k])**2
          else:
            y+=1
            ye+=1
#    res[j]={'v':y,'sigma':sqrt(ye)}
    if j==0:
      keys = pol.keys()
      keys.sort()
      for k in keys:
        print round(y[k],2),"+/-",round(sqrt(ye[k]),2), k
    if j==1:
      print y,"+/-",round(sqrt(ye),2)
