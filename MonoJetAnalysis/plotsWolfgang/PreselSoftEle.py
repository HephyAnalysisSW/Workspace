import math
from EventHelper import EventHelper
from KinematicUtilities import *
from LeptonUtilities import *

class PreselSoftEle:

    def __init__(self):
        self.isrJetPtMin = 110
        self.isrJetBTBVeto = True
        self.softIsolatedElePtMin = 7.
        self.softIsolatedElePtMax = 20.
        self.njet60Max = 2
        self.type1phiMetMin = 200.
        self.softIsolatedEleEtaMax = 999.

    def accept(self,eh,sample):

        isrJetPt = eh.get("isrJetPt")
        if math.isnan(isrJetPt) or isrJetPt<self.isrJetPtMin:
            return False

        met = eh.get("type1phiMet")
        if math.isnan(isrJetPt) or met<self.type1phiMetMin:
            return False

#        mediumMuIndex = int(eh.get("mediumMuIndex"))
#        if mediumMuIndex<0:
#            return False
        iele = hardestIsolatedElectron(eh,ptmin=self.softIsolatedElePtMin,etamax=self.softIsolatedEleEtaMax)
        if iele==None:
            return False

        elePts = eh.get("elPt")
        isolatedElePt = elePts[iele]
        if isolatedElePt<self.softIsolatedElePtMin or isolatedElePt>self.softIsolatedElePtMax:
            return False

        eleEtas = eh.get("elEta")
        if eleEtas[iele]>self.softIsolatedEleEtaMax:
            return False

        imu = hardestIsolatedMuon(eh,ptmin=20.,etamax=1.5)
        if imu!=None:
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

        #
        # SR veto
        #
        if sample.isData():
            # btags
            nball = 0
            nbsoft = 0
            njet = int(eh.get("njetCount")+0.5)
            jetPts = eh.get("jetPt")
            jetEtas = eh.get("jetEta")
            jetBtags = eh.get("jetBtag")
            for i in range(njet):
                if jetPts[i]>30 and abs(jetEtas[i])<2.4 and jetBtags[i]>0.679:
                    nball += 1
                    if jetPts[i]<60:
                        nbsoft += 1
            # SR1
            if nbsoft>0 and nbsoft==nball:
                if met>300 and isrJetPt>325:
                    return False
            # SR2/3
            if nball==0 and met>300 and eh.get("ht")>400:
#                mt = eh.get("softIsolatedMT")
#                if mt<60 or mt>88:
#                    return False
                return False

        return True
