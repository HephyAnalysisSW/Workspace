import math
from EventHelper import EventHelper
from KinematicUtilities import *
from LeptonUtilities import *
import PreselectionTools as PreTools
        
class PreselSoftMu:

    def accept(self,eh,sample):

        if not PreTools.passesHadronicSelection(eh):
            return False

        leptonInfo = PreTools.selectedLepton(eh,13,mode="soft")
#        ht = eh.get("ht")
#        met = eh.get("type1phiMet")
#        if ht>211.58 and ht<211.59 and met>225.20 and met<225.21:
#            print "ht,met,leptonInfo ",ht,met,leptonInfo

        if leptonInfo==None:
            return False

#        if ht>211.58 and ht<211.59 and met>225.20 and met<225.21:
#            print "ht,met,leptonInfo ",ht,met,leptonInfo

        return True

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
