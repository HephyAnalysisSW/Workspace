import math
from EventHelper import EventHelper
from KinematicUtilities import *
from LeptonUtilities import *
        
class PreselHardMu:

    def __init__(self):
        self.isrJetPtMin = 110
        self.isrJetBTBVeto = True
        self.softIsolatedMuPtMin = 5.
        self.softIsolatedMuPtMax = 20.
        self.hardIsolatedMuPtMin = 30.
        self.njet60Max = 2
        self.type1phiMetMin = 200.
        self.softIsolatedMuEtaMax = 999.

    def accept(self,eh,sample):

        isrJetPt = eh.get("isrJetPt")
        if math.isnan(isrJetPt) or isrJetPt<self.isrJetPtMin:
            return False

        met = eh.get("type1phiMet")
        if math.isnan(isrJetPt) or met<self.type1phiMetMin:
            return False

        mediumMuIndex = int(eh.get("mediumMuIndex"))
        if mediumMuIndex<0:
            return False
        imus = isolatedMuons(eh,ptmin=self.softIsolatedMuPtMin,etamax=self.softIsolatedMuEtaMax)
        if len(imus)==0:
            return False
        imu = imus[0]
        #
        # require one muon with pt>30 and no other muon with pt>20
        #
        muPts = eh.get("muPt")
        if muPts[imu]<self.hardIsolatedMuPtMin:
            return False
        if len(imus)>1 and muPts[imus[1]]>self.softIsolatedMuPtMax:
            return False

        if eh.get("nHardElectrons")>0:
            return False
        if eh.get("nHardTaus")>0:
            return False

        if eh.get("njet60")>self.njet60Max:
            return False

        assert not math.isnan(eh.get("isrJetBTBVetoPassed"))
        if self.isrJetBTBVeto and eh.get("isrJetBTBVetoPassed")==0:
            return False

        #
        # match with HT-binned W+jets sample
        #
        if eh.get("ht")<200:
            return False

###        #
###        # SR veto
###        #
###        if sample.isData() and muPts[imu]<20.:
###            # btags
###            nball = 0
###            nbsoft = 0
###            njet = int(eh.get("njetCount")+0.5)
###            jetPts = eh.get("jetPt")
###            jetEtas = eh.get("jetEta")
###            jetBtags = eh.get("jetBtag")
###            for i in range(njet):
###                if jetPts[i]>30 and abs(jetEtas[i])<2.4 and jetBtags[i]>0.679:
###                    nball += 1
###                    if jetPts[i]<60:
###                        nbsoft += 1
###            # SR1
###            if nbsoft>0 and nbsoft==nball:
###                if met>300 and isrJetPt>325:
###                    return False
###            # SR2/3
###            if nball==0 and met>300 and eh.get("ht")>400:
###                mt = eh.get("softIsolatedMT")
###                if mt<60 or mt>88:
###                    return False

        return True
