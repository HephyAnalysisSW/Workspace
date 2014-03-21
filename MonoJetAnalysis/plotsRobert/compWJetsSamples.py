import ROOT
import os, sys
from math import sqrt

paths = ['../python']
#path = os.path.abspath('../../HEPHYCommonTools/python')
for path in [os.path.abspath(p) for p in paths]:
  if not path in sys.path:
    sys.path.insert(1, path)


from helpers import calcMT, getVarValue

cWJetsHT150v2 = ROOT.TChain("Events")
cWJetsHT150v2.Add("/data/schoef/monoJetTuples_v5/copy/WJetsHT150v2/histo_WJetsHT150v2.root")
cWNJets = ROOT.TChain("Events")
cWNJets.Add("/data/schoef/monoJetTuples_v5/copy/W1JetsToLNu/histo_W1JetsToLNu.root")
cWNJets.Add("/data/schoef/monoJetTuples_v5/copy/W2JetsToLNu/histo_W2JetsToLNu.root")
cWNJets.Add("/data/schoef/monoJetTuples_v5/copy/W3JetsToLNu/histo_W3JetsToLNu.root")
cWNJets.Add("/data/schoef/monoJetTuples_v5/copy/W4JetsToLNu/histo_W4JetsToLNu.root")

data = ROOT.TChain("Events")
data.Add("/data/schoef/monoJetTuples_v5/copy/data/histo_data.root")

##Preselection and selections according to tuple
#selection = "isrJetPt>110&&type1phiMet>200&&isrJetBTBVetoPassed&&nHardElectrons+nHardMuonsRelIso02+nHardTaus==0&&njet60<=2&&type1phiMet>300.&&Sum$(jetBtag>0.679&&abs(jetEta)<2.4)==0"
#selection+="&&softIsolatedMuPt>5&&abs(softIsolatedMuEta)<1.5&&ht>400."
#selection+="&&softIsolatedMT>60.&&softIsolatedMT<88"
##selection+="&&Sum$(abs(gpPdg)==15&&gpSta==3)==0"
#print selection
##for sc in ["softIsolatedMuPdg>0","softIsolatedMuPdg<0"]:
#for sc in ["softIsolatedMuPdg>0"]:
#  cut = selection+"&&"+sc
#  res={}
#  for j, c in enumerate([cWJetsHT250, cWNJets]) :
#    c.Draw('>>eList', cut) 
#    eList = ROOT.gDirectory.Get('eList')
#    y=0.
#    ye=0.
#    for i in range(eList.GetN()):
##      if not i%10000: print "At",i,"/",eList.GetN()
#      c.GetEntry(eList.GetEntry(i))
#      w = getVarValue(c,'puWeight')
#      y+=w
#      ye+=w**2
##    print y,"+/-",sqrt(ye)
#    res[j]={'v':y,'sigma':sqrt(ye)}
#
#  r = res[0]['v']/res[1]['v']
#  rErr = res[0]['v']/res[1]['v']*sqrt(res[0]['sigma']**2/res[0]['v']**2 + res[1]['sigma']**2/res[1]['v']**2 )
#
#  print sc, "yields:",round(res[0]['v'],2),"+/-",round(res[0]['sigma']),'(HT250)',round(res[1]['v'],2),"+/-",round(res[1]['sigma'],2),'(WNJets)',"Ratio",round(r,2),"+/-",round(rErr,2),"(deviation:",round((1-r)/rErr,2),"sigma)"

def countPartons(c):
  f = ROOT.TTreeFormula('f', "Sum$((abs(gpPdg)<6||gpPdg==21)&&gpMo1==4&&gpMo2==5)", c)
  res= f.EvalInstance()
  del f
  return res

def rescalePartonWeight(c):
  n = countPartons(c)
  if n==4:
    return 65/85.
  return 1

#Preselectionw/o soft lepton 

selection = "isrJetPt>110&&type1phiMet>200&&isrJetBTBVetoPassed&&nHardElectrons+nHardMuonsRelIso02+nHardTaus==0&&njet60<=2&&type1phiMet>300.&&Sum$(jetBtag>0.679&&abs(jetEta)<2.4)==0&&ht>400"
#selection+="&&softIsolatedMuPt>5&&abs(softIsolatedMuEta)<1.5"
#selection+="&&softIsolatedMT>60.&&softIsolatedMT<88"
#selection+="&&Sum$(abs(gpPdg)==15&&gpSta==3)==0"
#selection = "isrJetPt>110&&type1phiMet>200&&isrJetBTBVetoPassed&&nHardElectrons+nHardMuonsRelIso02+nHardTaus==0&&njet60<=2&&type1phiMet>300.&&Sum$(jetBtag>0.679&&abs(jetEta)<2.4)==0&&ht>400"
#selection = "isrJetPt>110&&isrJetBTBVetoPassed&&nHardElectrons+nHardMuonsRelIso02+nHardTaus==0&&njet60<=2&&type1phiMet>300.&&Sum$(jetBtag>0.679&&abs(jetEta)<2.4)==0&&ht>400&&Sum$((abs(gpPdg)<6||gpPdg==21)&&gpMo1==4&&gpMo2==5)<4"


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

#def getSoftIsolatedMuon(c):
#    return {'pt':getVarValue(c, 'softIsolatedMuPt', imu), 'eta':eta, 'phi':getVarValue(c, 'muPhi', imu), 'pdg':getVarValue(c, 'muPdg', imu)}

def getSoftGenMuon(c):
  for igp in range(int(getVarValue(c, 'ngp'))):
    pdg=getVarValue(c, 'gpPdg', igp)
    if abs(pdg)==13:
      pt = getVarValue(c, 'gpPt', igp)
      if pt>5 and pt<20: 
        eta=getVarValue(c, 'gpEta', igp)
        if abs(eta)<2.1:
          phi=getVarValue(c, 'gpPhi', igp)
          return {'pt':pt, 'eta':eta, 'phi':phi, 'pdg':pdg}

def getSoftGenElectron(c):
  for igp in range(int(getVarValue(c, 'ngp'))):
    pdg=getVarValue(c, 'gpPdg', igp)
    if abs(pdg)==11:
      pt = getVarValue(c, 'gpPt', igp)
      if pt>5 and pt<20: 
        eta=getVarValue(c, 'gpEta', igp)
        if abs(eta)<2.1:
          phi=getVarValue(c, 'gpPhi', igp)
          return {'pt':pt, 'eta':eta, 'phi':phi, 'pdg':pdg}

def muRequirement(mu):
  return mu['pt']>5 and abs(mu['eta'])<1.5

#print selection
#for pdgSign in [-1,+1]:
#  cut = selection
#  res={}
#  for j, c in enumerate([cWJetsHT150v2, cWNJets]) :
#    c.Draw('>>eList', cut) 
#    eList = ROOT.gDirectory.Get('eList')
#    y=0.
#    ye=0.
#    for i in range(eList.GetN()):
#      if not i%10000: print "At",i,"/",eList.GetN()
#      c.GetEntry(eList.GetEntry(i))
#      mu = getSoftMuon(c)
##      mu = getSoftGenElectron(c)
##      mu = getSoftGenMuon(c)
##      print mu
#      if mu and muRequirement(mu) and pdgSign==mu['pdg']/abs(mu['pdg']):
#        mT = calcMT(mu, {'pt':getVarValue(c, 'type1phiMet'), 'phi':getVarValue(c, 'type1phiMetphi')})
##        if mT-getVarValue(c, 'softIsolatedMT')>10:
##          print getVarValue(c,'event'), getVarValue(c,'lumi'), mT-getVarValue(c, 'softIsolatedMT')
#        if mT>60 and mT<88:
#          w = getVarValue(c, 'puWeight')
##          if j==1:
##            resc = rescalePartonWeight(c)
##            w*=resc
#          y+=w
#          ye+=w**2
##    print y,"+/-",sqrt(ye)
#    res[j]={'v':y,'sigma':sqrt(ye)}
#
#  r = res[0]['v']/res[1]['v']
#  rErr = res[0]['v']/res[1]['v']*sqrt(res[0]['sigma']**2/res[0]['v']**2 + res[1]['sigma']**2/res[1]['v']**2 )
#
#  print 'sign(pdg)==',pdgSign, "yields:",round(res[0]['v'],2),"+/-",round(res[0]['sigma']),'(HT150v2)',round(res[1]['v'],2),"+/-",round(res[1]['sigma'],2),'(WNJets)',"Ratio",round(r,2),"+/-",round(rErr,2),"(deviation:",round((1-r)/rErr,2),"sigma)"

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
#      mu = getSoftMuon(c)
#      mu = getSoftGenElectron(c)
#      mu = getSoftGenMuon(c)
#      print mu
#      if mu and muRequirement(mu) and pdgSign==mu['pdg']/abs(mu['pdg']):
      pdg_ = getVarValue(c, 'softIsolatedMuPdg') 

      if  pdgSign*pdg_>0:
        mT = getVarValue(c, 'softIsolatedMT')
#        if mT-getVarValue(c, 'softIsolatedMT')>10:
#          print getVarValue(c,'event'), getVarValue(c,'lumi'), mT-getVarValue(c, 'softIsolatedMT')
#        if mT>0 and mT<60:
#        if mT>88:# and mT<60:
#        if mT>88:# and mT<60:
        if mT>60 and mT<88:
#          if j==1:
#            resc = rescalePartonWeight(c)
#            w*=resc
          if j==0:
            w = getVarValue(c, 'puWeight')
            
            if not y.has_key('central'):
              y['central'] = w 
              ye['central'] = (w)**2
            else:
              y['central']  += w 
              ye['central'] += (w)**2
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
      keys = y.keys()
      keys.sort()
      for k in keys:
        print round(y[k],2),"+/-",round(sqrt(ye[k]),2), k
    if j==1:
      print y,"+/-",round(sqrt(ye),2)
