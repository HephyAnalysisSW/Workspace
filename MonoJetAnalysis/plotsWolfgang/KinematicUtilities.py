from math import sqrt,pi

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
