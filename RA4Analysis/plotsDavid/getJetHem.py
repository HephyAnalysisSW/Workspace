import ROOT
import operator
from math import *
from array import array
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.eventShape import *

def getJetHem(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  jetList = []
  for i in jets:
    rd = {}
    jetX = sum([cos(j['phi'])*j['pt'] for j in jets if cos(i['phi'] - j['phi'])>0.])
    jetY = sum([sin(j['phi'])*j['pt'] for j in jets if cos(i['phi'] - j['phi'])>0.])
    rd.update({\
                'Jet_pt':sqrt( (jetX * jetX) + (jetY * jetY) ),\
                'Jet_phi':atan2(jetX,jetY),\
                'dPhiMetJet':deltaPhi(c.GetLeaf('met_phi').GetValue(),atan2(jetX,jetY)),\
                'dPhiLepJet':deltaPhi(c.GetLeaf('leptonPhi').GetValue(),atan2(jetX,jetY)),\
              })
    jetList.append(rd)
  jetList.sort(key=operator.itemgetter('Jet_pt'), reverse=True)
  return jetList

def missingHT(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  jetX = sum([px(j) for j in jets])
  jetY = sum([py(j) for j in jets])

  return sqrt((jetX * jetX) + (jetY * jetY))

def dPhiMHTMET(c):
  jets = cmgGetJets(c)
  jetX = sum([cos(j['phi'])*j['pt'] for j in jets])
  jetY = sum([sin(j['phi'])*j['pt'] for j in jets])
  mhtPhi = atan2(jetX,jetY)
  metPhi = c.GetLeaf('met_phi').GetValue()
  return deltaPhi(mhtPhi,metPhi)

ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/Thrust.C+")
def calcThrust(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  lPhi = c.GetLeaf('leptonPhi').GetValue()
  lPt = c.GetLeaf('leptonPt').GetValue()
  mPhi = c.GetLeaf('met_phi').GetValue()
  mPt = c.GetLeaf('met_pt').GetValue()
  p_x = [cos(lPhi)*lPt] + [cos(mPhi)*mPt] + [cos(j['phi'])*j['pt'] for j in jets]
  p_y = [sin(lPhi)*lPt] + [sin(mPhi)*mPt] + [sin(j['phi'])*j['pt'] for j in jets]

  thrust = ROOT.Thrust(2+len(jets), array('d', p_x), array('d', p_y))
  th = thrust.thrust()
  return th
