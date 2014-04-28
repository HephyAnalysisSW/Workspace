import ROOT
from math import sqrt,pi,cos,sin

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

def computeMT(met,phiMet,ptMu,phiMu):
    return sqrt(2*met*ptMu*(1-cos(phiMet-phiMu)))

def wSolutions(met,phiMet,ptMu,phiMu,etaMu):
    mW = 80.4
    modmet = met
    mt = computeMT(met,phiMet,ptMu,phiMu)
    if mt>mW:
        modmet *= (mW/mt)**2
    a = (mW*mW/2+modmet*ptMu*cos(phiMet-phiMu))
    b = a*a - modmet**2*ptMu**2
    if b<0:
        b = 0
    p4mu = ROOT.TLorentzVector()
    p4mu.SetPtEtaPhiM(ptMu,etaMu,phiMu,0.)
    pmu = p4mu.P()
    pzmu = p4mu.Pz()
    pzn1 = (a*pzmu+sqrt(b)*pmu)/ptMu**2
    pzn2 = (a*pzmu-sqrt(b)*pmu)/ptMu**2
    p4n1 = ROOT.TLorentzVector()
    p4n1.SetPxPyPzE(modmet*cos(phiMet),modmet*sin(phiMet),pzn1,sqrt(modmet*modmet+pzn1*pzn1))
    p4n2 = ROOT.TLorentzVector()
    p4n2.SetPxPyPzE(modmet*cos(phiMet),modmet*sin(phiMet),pzn2,sqrt(modmet*modmet+pzn2*pzn2))
    assert abs((p4mu+p4n1).M()-mW)<0.001,abs((p4mu+p4n2).M()-mW)<0.001
    return [ p4mu+p4n1, p4mu+p4n2 ]
    
def toPolFrame(p4Parent,p4Daughter):
    # boost to rest frame of parent
    boost = p4Parent.BoostVector()
    boost *= -1.
    p4Dmod = p4Daughter.Clone()
    p4Dmod.Boost(boost)
    # rotate (new z-axis || p3Parent; new x-axis || p3Parent x global z-axis)
    rot = ROOT.TRotation()
    p3Parent = p4Parent.Vect()
    rot.SetZAxis(p3Parent,p3Parent.Cross(ROOT.TVector3(0.,0.,1.)))
    rot.Invert()
    p4Dmod.Transform(rot)
#    p4Dmod.Print()
    return p4Dmod
