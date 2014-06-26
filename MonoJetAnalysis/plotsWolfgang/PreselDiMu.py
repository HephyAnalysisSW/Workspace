import ROOT
import math
from EventHelper import EventHelper
from KinematicUtilities import *
from LeptonUtilities import *
import PreselectionTools as PreTools
        
class PreselDiMu:

    def accept(self,eh,sample):

        imu0,imu1 = diMuon(eh)
        if imu0==None:
            return False

        isrJetPt = eh.get("isrJetPt")
        if math.isnan(isrJetPt) or isrJetPt<110.:
            return False

        mupts = eh.get("muPt")
        muetas = eh.get("muEta")
        muphis = eh.get("muPhi")
        mu0p4 = ROOT.TLorentzVector()
        mu0p4.SetPtEtaPhiM(mupts[imu0],muetas[imu0],muphis[imu0],0.105)
        mu1p4 = ROOT.TLorentzVector()
        mu1p4.SetPtEtaPhiM(mupts[imu1],muetas[imu1],muphis[imu1],0.105)
        if (mu0p4+mu1p4).M()<55.:
            return False
#        zpt = (mu0p4+mu1p4).Pt()
#        if not PreTools.passesHadronicSelection(eh,recalculatedMet=zpt):
#            return False

        return True

