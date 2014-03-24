import math
from EventHelper import EventHelper

def deltaPhi(phi1,phi2):
    result = phi2 - phi1
    if result<-pi:
        result += 2*pi
    if result>pi:
        result -= 2*pi
    return result

def deltaR(phi1,eta1,phi2,eta2):
    dphi = deltaPhi(phi1,phi2)
    deta = eta2 - eta1
    return sqrt(dphi*dphi+deta*deta)

        
class Preselection:

    def __init__(self):
        self.isrJetPtMin = 110
        self.isrJetBTBVeto = True
        self.softIsolatedMuPtMin = 5
        self.njet60Max = 2
        self.type1phiMetMin = 150
        self.softIsolatedMuEtaMax = 1.5

    def accept(self,eh,sample):

        isrJetPt = eh.get("isrJetPt")
        if math.isnan(isrJetPt) or isrJetPt<self.isrJetPtMin:
            return False

        met = eh.get("type1phiMet")
        if math.isnan(isrJetPt) or met<self.type1phiMetMin:
            return False

        softIsolatedMuPt = eh.get("softIsolatedMuPt")
        if math.isnan(softIsolatedMuPt) or softIsolatedMuPt<self.softIsolatedMuPtMin:
            return False

        if abs(eh.get("softIsolatedMuEta"))>self.softIsolatedMuEtaMax:
            return False

        if eh.get("nHardElectrons")>0:
            return False
        if eh.get("nHardMuonsRelIso02")>0:
            return False
        if eh.get("nHardTaus")>0:
            return False

        if eh.get("njet60")>self.njet60Max:
            return False

        assert not math.isnan(eh.get("isrJetBTBVetoPassed"))
        if self.isrJetBTBVeto and eh.get("isrJetBTBVetoPassed")==0:
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
                mt = eh.get("softIsolatedMT")
                if mt<60 or mt>88:
                    return False

        return True
