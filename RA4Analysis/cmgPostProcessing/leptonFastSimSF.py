import ROOT

from Workspace.HEPHYPythonTools.helpers import *
import os


tightEleFile = 'sf_el_tightCB_mini01'
looseEleFile = 'sf_el_looseCB_mini04'
medMuonFile  = 'sf_mu_mediumID_mini02'

#tightEle3D  = getObjFromFile(tightEleDir, "histo3D")
#looseEle3D  = getObjFromFile(looseEleDir, "histo3D")
#medMuon3D   = getObjFromFile(medMuonDir, "histo3D")


class leptonFastSimSF:
  def __init__(self):
    self.dataDir = "$CMSSW_BASE/src/Workspace/RA4Analysis/cmgPostProcessing/data/"
    muFileName = os.path.join(self.dataDir, medMuonFile+'.root')
    eleFileName = os.path.join(self.dataDir, tightEleFile+'.root')

    self.mu3D = getObjFromFile(os.path.expandvars(muFileName), "histo3D")
    assert self.mu3D, "Could not load 'histo3D' from %s"%os.path.expandvars(muFileName)
    self.ele3D = getObjFromFile(os.path.expandvars(eleFileName), "histo3D")
    assert self.ele3D, "Could not load 'histo3D' from %s"%os.path.expandvars(eleFileName)
    print "Loaded lepton SF file for muons:     %s"%muFileName
    print "Loaded lepton SF file for electrons: %s"%eleFileName

  def get3DSFUnc(self, pdgId, pt):
    if abs(pdgId)==13:
      return 0.01
    elif abs(pdgId)==11:
      if pt<30:
        return 0.08
      else:
        return 0.05
    else:
      raise Exception("FastSim SF Unc for PdgId %i not known"%pdgId)

  def get3DSF(self, pdgId, pt, eta, nvtx, sigma=0):
    if abs(pdgId)==13:
      res = (1+self.get3DSFUnc(pdgId, pt)*sigma)*self.mu3D.GetBinContent(self.mu3D.GetXaxis().FindBin(pt), self.mu3D.GetYaxis().FindBin(abs(eta)), self.mu3D.GetZaxis().FindBin(nvtx))
    elif abs(pdgId)==11:
      res = (1+self.get3DSFUnc(pdgId, pt)*sigma)*self.ele3D.GetBinContent(self.mu3D.GetXaxis().FindBin(pt), self.mu3D.GetYaxis().FindBin(abs(eta)), self.mu3D.GetZaxis().FindBin(nvtx))
    else:
      raise Exception("FastSim SF for PdgId %i not known"%pdgId)
    if res==0: res=1 #no SF for |eta|>2.19 for electrons? 
    return res

