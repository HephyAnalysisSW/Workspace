import ROOT

from Workspace.HEPHYPythonTools.helpers import *
import os

# ele files
eleHIPFile  = 'egammaEffi_txt_SF2D'
eleIDFile   = 'eleScaleFactorsUpdate2607'

# mu files
muHIPFile   = 'ratiosMuonHIP'
muIsoFile   = 'TnP_MuonID_NUM_MiniIsoTight_DENOM_MediumID_VAR_map_pt_eta'
muSIPFile   = 'TnP_MuonID_NUM_TightIP3D_DENOM_MediumID_VAR_map_pt_eta'
muMedFile   = 'TnP_MuonID_NUM_MediumID_DENOM_generalTracks_VAR_map_pt_eta'

class leptonSF:
  def __init__(self):
    self.dataDir = "$CMSSW_BASE/src/Workspace/RA4Analysis/cmgPostProcessing/data/"

    #Muon HIP
    muHIPFileName = os.path.join(self.dataDir, muHIPFile+'.root')
    muHIPHistName = "ratio_eta"

    #Muon Isolation
    muIsoFileName = os.path.join(self.dataDir, muIsoFile+'.root')
    muIsoHistName = "pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_Medium2016_pass"
    
    #Muon SIP
    muSIPFileName = os.path.join(self.dataDir, muSIPFile+'.root')
    muSIPHistName = "pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_Medium2016_pass"
    
    #Muon Medium ID
    muMedFileName = os.path.join(self.dataDir, muMedFile+'.root')
    muMedHistName = "pt_abseta_PLOT_pair_probeMultiplicity_bin0"

    #Electron ID and Isolation
    eleIDFileName  = os.path.join(self.dataDir, eleIDFile+'.root')
    eleIDHistName  = "GsfElectronToTight"
    eleIsoHistName = "MVAVLooseElectronToMini"

    #Electron HIP
    eleHIPFileName = os.path.join(self.dataDir, eleHIPFile+'.root')
    eleHIPHistName = "EGamma_SF2D"

    self.medMu = getObjFromFile(os.path.expandvars(muMedFileName), muMedHistName)
    self.isoMu = getObjFromFile(os.path.expandvars(muIsoFileName), muIsoHistName)
    self.sipMu = getObjFromFile(os.path.expandvars(muSIPFileName), muSIPHistName)
    self.HIPMu = getObjFromFile(os.path.expandvars(muHIPFileName), muHIPHistName)
    
    self.CBIDEle = getObjFromFile(os.path.expandvars(eleIDFileName), eleIDHistName)
    self.isoEle  = getObjFromFile(os.path.expandvars(eleIDFileName), eleIsoHistName)
    self.HIPEle  = getObjFromFile(os.path.expandvars(eleHIPFileName), eleHIPHistName)

    assert self.medMu, "Could not load %s from %s"%(muMedHistName, os.path.expandvars(muMedFileName))
    assert self.isoMu, "Could not load %s from %s"%(muIsoHistName, os.path.expandvars(muIsoFileName))
    assert self.sipMu, "Could not load %s from %s"%(muSIPHistName, os.path.expandvars(muSIPFileName))
    assert self.HIPMu, "Could not load %s from %s"%(muHIPHistName, os.path.expandvars(muHIPFileName))

    assert self.CBIDEle, "Could not load %s from %s"%(eleIDHistName, os.path.expandvars(eleIDFileName))
    assert self.isoEle, "Could not load %s from %s"%(eleIsoHistName, os.path.expandvars(eleIDFileName))
    assert self.HIPEle, "Could not load %s from %s"%(eleHIPHistName, os.path.expandvars(eleHIPFileName))


    print "Loaded lepton SF file for muons:     %s"%muMedFileName
    print "Loaded lepton SF file for muons:     %s"%muIsoFileName
    print "Loaded lepton SF file for muons:     %s"%muSIPFileName
    print "Loaded lepton SF file for muons:     %s"%muHIPFileName

    print "Loaded lepton SF file for electrons: %s"%eleIDFileName
    print "Loaded lepton SF file for electrons: %s"%eleHIPFileName
    
    self.maxPtEle = self.CBIDEle.GetXaxis().GetBinUpEdge(self.CBIDEle.GetNbinsX())
    self.maxPtMu  = self.isoMu.GetXaxis().GetBinUpEdge(self.isoMu.GetNbinsX())
    

  def getSFUnc(self, pdgId, pt, eta):
    if abs(pdgId)==13:
      return 0.03
    elif abs(pdgId)==11:
      CBIDSF    = self.CBIDEle.GetBinContent(self.CBIDEle.GetXaxis().FindBin(pt), self.CBIDEle.GetYaxis().FindBin(abs(eta)))
      CBIDSFunc = self.CBIDEle.GetBinError(self.CBIDEle.GetXaxis().FindBin(pt), self.CBIDEle.GetYaxis().FindBin(abs(eta)))
      isoSF     = self.isoEle.GetBinContent(self.isoEle.GetXaxis().FindBin(pt), self.isoEle.GetYaxis().FindBin(abs(eta)))
      isoSFunc  = self.isoEle.GetBinError(self.isoEle.GetXaxis().FindBin(pt), self.isoEle.GetYaxis().FindBin(abs(eta)))
      HIPSF     = self.HIPEle.GetBinContent(self.HIPEle.FindBin(eta,100))
      HIPSFunc  = self.HIPEle.GetBinError(self.HIPEle.FindBin(eta,100))
      return sqrt((CBIDSFunc/CBIDSF)**2 + (isoSFunc/isoSF)**2 + (HIPSFunc/HIPSF)**2)
    else:
      raise Exception("SF Uncertainty for PdgId %i not known"%pdgId)
      
  def getSF(self, pdgId, pt, eta, sigma=0):
    if abs(pdgId)==13:
      if pt>self.maxPtMu: pt = self.maxPtMu-1
      isoSF = self.isoMu.GetBinContent(self.isoMu.GetXaxis().FindBin(pt), self.isoMu.GetYaxis().FindBin(abs(eta)))
      sipSF = self.sipMu.GetBinContent(self.sipMu.GetXaxis().FindBin(pt), self.sipMu.GetYaxis().FindBin(abs(eta)))
      medSF = self.medMu.GetBinContent(self.medMu.GetXaxis().FindBin(pt), self.medMu.GetYaxis().FindBin(abs(eta)))
      HIPSF = self.HIPMu.Eval(eta)
      res = (1+self.getSFUnc(pdgId, pt, eta)*sigma) * isoSF * sipSF * medSF * HIPSF
    elif abs(pdgId)==11:
      if pt>self.maxPtEle: pt = self.maxPtEle-1
      CBIDSF = self.CBIDEle.GetBinContent(self.CBIDEle.GetXaxis().FindBin(pt), self.CBIDEle.GetYaxis().FindBin(abs(eta)))
      isoSF  = self.isoEle.GetBinContent(self.isoEle.GetXaxis().FindBin(pt), self.isoEle.GetYaxis().FindBin(abs(eta)))
      HIPSF  = self.HIPEle.GetBinContent(self.HIPEle.FindBin(eta,100))
      res = (1+self.getSFUnc(pdgId, pt, eta)*sigma) * CBIDSF * isoSF * HIPSF
    else:
      raise Exception("SF for PdgId %i not known"%pdgId)
    if res==0: res=1
    return res
