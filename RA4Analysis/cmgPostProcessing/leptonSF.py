import ROOT

from Workspace.HEPHYPythonTools.helpers import *
import os

# ele files
eleTrackFile= 'egammaEffi.txt_EGM2D'
eleIDFile   = 'scaleFactors'

# mu files
muTrackFile = 'comingsoon'
muIsoFile   = 'TnP_NUM_MiniIsoTight_DENOM_MediumID_VAR_map_pt_eta'
muSIPFile   = 'TnP_NUM_TightIP3D_DENOM_MediumID_VAR_map_pt_eta'
muMedFile   = 'TnP_NUM_MediumID_DENOM_generalTracks_VAR_map_pt_eta'

class leptonSF:
  def __init__(self):
    self.dataDir = "$CMSSW_BASE/src/Workspace/RA4Analysis/cmgPostProcessing/data/"

    #Muon Track
    muTrackFileName = os.path.join(self.dataDir, muTrackFile+'.root')
    muTrackHistName = "ratio_eta"

    #Muon Isolation
    muIsoFileName = os.path.join(self.dataDir, muIsoFile+'.root')
    muIsoHistName = "SF"
    
    #Muon SIP
    muSIPFileName = os.path.join(self.dataDir, muSIPFile+'.root')
    muSIPHistName = "SF"
    
    #Muon Medium ID
    muMedFileName = os.path.join(self.dataDir, muMedFile+'.root')
    muMedHistName = "SF"

    #Electron ID and Isolation
    eleIDFileName  = os.path.join(self.dataDir, eleIDFile+'.root')
    eleIDHistName  = "GsfElectronToCutBasedSpring15T"
    eleIsoHistName = "MVAVLooseElectronToMini"

    #Electron Track
    eleTrackFileName = os.path.join(self.dataDir, eleTrackFile+'.root')
    eleTrackHistName = "EGamma_SF2D"

    self.medMu = getObjFromFile(os.path.expandvars(muMedFileName), muMedHistName)
    self.isoMu = getObjFromFile(os.path.expandvars(muIsoFileName), muIsoHistName)
    self.sipMu = getObjFromFile(os.path.expandvars(muSIPFileName), muSIPHistName)
    #self.TrackMu = getObjFromFile(os.path.expandvars(muTrackFileName), muTrackHistName)
    
    self.CBIDEle = getObjFromFile(os.path.expandvars(eleIDFileName), eleIDHistName)
    self.isoEle  = getObjFromFile(os.path.expandvars(eleIDFileName), eleIsoHistName)
    self.TrackEle  = getObjFromFile(os.path.expandvars(eleTrackFileName), eleTrackHistName)

    assert self.medMu, "Could not load %s from %s"%(muMedHistName, os.path.expandvars(muMedFileName))
    assert self.isoMu, "Could not load %s from %s"%(muIsoHistName, os.path.expandvars(muIsoFileName))
    assert self.sipMu, "Could not load %s from %s"%(muSIPHistName, os.path.expandvars(muSIPFileName))
    #assert self.TrackMu, "Could not load %s from %s"%(muTrackHistName, os.path.expandvars(muTrackFileName))

    assert self.CBIDEle, "Could not load %s from %s"%(eleIDHistName, os.path.expandvars(eleIDFileName))
    assert self.isoEle, "Could not load %s from %s"%(eleIsoHistName, os.path.expandvars(eleIDFileName))
    assert self.TrackEle, "Could not load %s from %s"%(eleTrackHistName, os.path.expandvars(eleTrackFileName))


    print "Loaded lepton SF file for muons:     %s"%muMedFileName
    print "Loaded lepton SF file for muons:     %s"%muIsoFileName
    print "Loaded lepton SF file for muons:     %s"%muSIPFileName
    #print "Loaded lepton SF file for muons:     %s"%muTrackFileName

    print "Loaded lepton SF file for electrons: %s"%eleIDFileName
    print "Loaded lepton SF file for electrons: %s"%eleTrackFileName
    
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
      TrackSF     = self.TrackEle.GetBinContent(self.TrackEle.FindBin(eta,100))
      TrackSFunc  = self.TrackEle.GetBinError(self.TrackEle.FindBin(eta,100))
      return sqrt((CBIDSFunc/CBIDSF)**2 + (isoSFunc/isoSF)**2 + (TrackSFunc/TrackSF)**2)
    else:
      raise Exception("SF Uncertainty for PdgId %i not known"%pdgId)
      
  def getSF(self, pdgId, pt, eta, sigma=0):
    if abs(pdgId)==13:
      if pt>self.maxPtMu: pt = self.maxPtMu-1
      isoSF = self.isoMu.GetBinContent(self.isoMu.GetXaxis().FindBin(pt), self.isoMu.GetYaxis().FindBin(abs(eta)))
      sipSF = self.sipMu.GetBinContent(self.sipMu.GetXaxis().FindBin(pt), self.sipMu.GetYaxis().FindBin(abs(eta)))
      medSF = self.medMu.GetBinContent(self.medMu.GetXaxis().FindBin(pt), self.medMu.GetYaxis().FindBin(abs(eta)))
      #TrackSF = self.TrackMu.Eval(eta)
      res = (1+self.getSFUnc(pdgId, pt, eta)*sigma) * isoSF * sipSF * medSF# * TrackSF
    elif abs(pdgId)==11:
      if pt>self.maxPtEle: pt = self.maxPtEle-1
      CBIDSF = self.CBIDEle.GetBinContent(self.CBIDEle.GetXaxis().FindBin(pt), self.CBIDEle.GetYaxis().FindBin(abs(eta)))
      isoSF  = self.isoEle.GetBinContent(self.isoEle.GetXaxis().FindBin(pt), self.isoEle.GetYaxis().FindBin(abs(eta)))
      TrackSF  = self.TrackEle.GetBinContent(self.TrackEle.FindBin(eta,100))
      res = (1+self.getSFUnc(pdgId, pt, eta)*sigma) * CBIDSF * isoSF * TrackSF
    else:
      raise Exception("SF for PdgId %i not known"%pdgId)
    if res==0: res=1
    return res
