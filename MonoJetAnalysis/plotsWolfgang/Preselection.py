import math
from EventHelper import EventHelper
from KinematicUtilities import *
from LeptonUtilities import *
#
# general ISR preselection (no lepton requirements)
#
class Preselection:

    def __init__(self):
        self.isrJetPtMin = 110
        self.isrJetBTBVeto = True
        self.njet60Max = 2
        self.type1phiMetMin = 200.

    def accept(self,eh,sample):

        isrJetPt = eh.get("isrJetPt")
        if math.isnan(isrJetPt) or isrJetPt<self.isrJetPtMin:
            return False

        met = eh.get("type1phiMet")
        if math.isnan(isrJetPt) or met<self.type1phiMetMin:
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

        return True
