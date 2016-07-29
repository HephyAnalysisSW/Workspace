import ROOT

from Workspace.HEPHYPythonTools.helpers import *
import os


tightEleFile = 'sf_el_tightCB_mini01FastSim'
sipMuonFile  = 'sf_mu_tightIP3DFastSim'
isoMuonFile  = 'sf_mu_mediumID_mini02FastSim'
medMuonFile  = 'sf_mu_mediumFastSim'


class leptonFastSimSF:
  def __init__(self):
    self.dataDir = "$CMSSW_BASE/src/Workspace/RA4Analysis/cmgPostProcessing/data/"
    medMuFileName = os.path.join(self.dataDir, medMuonFile+'.root')
    isoMuFileName = os.path.join(self.dataDir, isoMuonFile+'.root')
    sipMuFileName = os.path.join(self.dataDir, sipMuonFile+'.root')
    eleFileName = os.path.join(self.dataDir, tightEleFile+'.root')

    self.medMu2D = getObjFromFile(os.path.expandvars(medMuFileName), "histo2D")
    self.isoMu2D = getObjFromFile(os.path.expandvars(isoMuFileName), "histo2D")
    self.sipMu2D = getObjFromFile(os.path.expandvars(sipMuFileName), "histo2D")
    assert self.medMu2D, "Could not load 'histo2D' from %s"%os.path.expandvars(medMuFileName)
    assert self.isoMu2D, "Could not load 'histo2D' from %s"%os.path.expandvars(isoMuFileName)
    assert self.sipMu2D, "Could not load 'histo2D' from %s"%os.path.expandvars(sipMuFileName)
    self.ele2D = getObjFromFile(os.path.expandvars(eleFileName), "histo2D")
    assert self.ele2D, "Could not load 'histo2D' from %s"%os.path.expandvars(eleFileName)

    print "Loaded lepton SF file for muons:     %s"%medMuFileName
    print "Loaded lepton SF file for muons:     %s"%medMuFileName
    print "Loaded lepton SF file for muons:     %s"%medMuFileName

    print "Loaded lepton SF file for electrons: %s"%eleFileName

  def get2DSFUnc(self, pdgId, pt):
    if abs(pdgId)==13:
      return 0.02
    elif abs(pdgId)==11:
      return 0.02
    else:
      raise Exception("FastSim SF Unc for PdgId %i not known"%pdgId)

  def get2DSF(self, pdgId, pt, eta, nvtx, sigma=0):
    if abs(pdgId)==13:
      isoSF = self.isoMu2D.GetBinContent(self.isoMu2D.GetXaxis().FindBin(pt), self.isoMu2D.GetYaxis().FindBin(abs(eta)))
      sipSF = self.sipMu2D.GetBinContent(self.sipMu2D.GetXaxis().FindBin(pt), self.sipMu2D.GetYaxis().FindBin(abs(eta)))
      medSF = self.medMu2D.GetBinContent(self.medMu2D.GetXaxis().FindBin(pt), self.medMu2D.GetYaxis().FindBin(abs(eta)))
      res = (1+self.get2DSFUnc(pdgId, pt)*sigma)*isoSF*sipSF*medSF
    elif abs(pdgId)==11:
      eleSF = self.ele2D.GetBinContent(self.ele2D.GetXaxis().FindBin(pt), self.ele2D.GetYaxis().FindBin(abs(eta)))
      res = (1+self.get2DSFUnc(pdgId, pt)*sigma)*eleSF
    else:
      raise Exception("FastSim SF for PdgId %i not known"%pdgId)
    if res==0: res=1 #no SF for |eta|>2.19 for electrons? 
    return res

