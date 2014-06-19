import math
from EventHelper import EventHelper
from KinematicUtilities import *
from LeptonUtilities import *

isrJetPtMin = 110
njet60Max = 2
type1phiMetMin = 200.
isrJetBTBVeto = True
softIsolatedPtMin = ( 7., 5. )
softIsolatedPtMax = ( 20., 20. )
hardIsolatedPtMin = ( 30., 30. )
softIsolatedEtaMax = ( 999., 999. )

def passesHadronicSelection(eh):
    isrJetPt = eh.get("isrJetPt")
    if math.isnan(isrJetPt) or isrJetPt<isrJetPtMin:
        return False

    met = eh.get("type1phiMet")
    if math.isnan(isrJetPt) or met<type1phiMetMin:
        return False

    if eh.get("njet60")>njet60Max:
        return False

#
# match with HT-binned W+jets sample
#
    if eh.get("ht")<200:
        return False

    assert not math.isnan(eh.get("isrJetBTBVetoPassed"))
    if isrJetBTBVeto and eh.get("isrJetBTBVetoPassed")==0:
        return False

    return True

def selectedLepton(eh,leptonPdg,hardLepton):
    leptons = ( ( 11, "el" ) , ( 13, "mu" ) )
    leptonIndex = None
    for i,l in enumerate(leptons):
        if abs(leptonPdg)==l[0]:
            leptonIndex = i
            leptonPrefix = l[1]
            break
    assert leptonIndex!=None

    if eh.get("nHardTaus")>0:
        return None

    if abs(leptonPdg)==11:
        if eh.get("nHardMuonsMediumWP")>0:
            return None
        ileptons = isolatedElectrons(eh,ptmin=softIsolatedPtMin[leptonIndex], \
                                         etamax=softIsolatedEtaMax[leptonIndex])
    else:
        if eh.get("nHardElectrons")>0:
            return None
#        mediumMuIndex = int(eh.get("mediumMuIndex"))
#        if mediumMuIndex<0:
#            return None
        ileptons = isolatedMuons(eh,ptmin=softIsolatedPtMin[leptonIndex], \
                                     etamax=softIsolatedEtaMax[leptonIndex])

    if len(ileptons)==0:
        return None
    ilepton = ileptons[0]

    leptonEtas = eh.get(leptonPrefix+"Eta")
    if abs(leptonEtas[ilepton])>softIsolatedEtaMax[leptonIndex]:
        return None

    leptonPts = eh.get(leptonPrefix+"Pt")
    leptonPt = leptonPts[ilepton]
    if hardLepton:
        if leptonPt<hardIsolatedPtMin[leptonIndex]:
            return None
        if len(ileptons)>1 and leptonPts[ileptons[1]]>softIsolatedPtMax[leptonIndex]:
            return None
    else:
        if leptonPt<softIsolatedPtMin[leptonIndex] or leptonPt>softIsolatedPtMax[leptonIndex]:
            return None
    
    return ( ilepton, leptonPrefix )

def signalRegion(eh,ilepton,leptonPrefix):    
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
        if eh.get("type1phiMet")>300 and eh.get("isrJetPt")>325:
            return "SR1"
        
    # SR2/3
    if nball==0 and eh.get("type1phiMet")>300 and eh.get("ht")>400:
#                mt = eh.get("softIsolatedMT")
#                if mt<60 or mt>88:
#                    return False
        return "SR2"

    return None
