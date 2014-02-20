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

    def accept(self,eh):

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

        return True
