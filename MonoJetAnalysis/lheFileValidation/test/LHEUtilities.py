import ROOT
from math import sqrt


class LHEParticle:

    def __init__(self,index,pdgId,px,py,pz,e,m,mo1=None,mo2=None,da1=None,da2=None):
        self.index = index
        self.pdgId = pdgId
        self.px = px
        self.py = py
        self.pz = pz
        self.e = e
        self.m = m 
#        if abs(sqrt(px*px+py*py+pz*pz+m*m)/e-1)>1.e-3:
#            print "Inconsistency in particle data, index, pdgId = ",index,pdgId
#            print px,py,pz,m,e
#            print sqrt(px*px+py*py+pz*pz+m*m)
#        assert abs(sqrt(px*px+py*py+pz*pz+m*m)/e-1)<1.e-3
        self.mothers = [ ]
        if mo1!=None and mo1>=0:
            m1 = mo1
            m2 = mo2 if ( mo2!=None and mo2>=0 ) else mo1
            assert m2>=m1
            self.mothers = range(m1,m2+1)
        self.daughters = [ ]
        if da1!=None and da1>=0:
            d1 = da1
            d2 = da2 if ( da2!=None and da2>=0 ) else da1
            assert d2>=d1
            self.daughters = range(d1,d2+1)
        self.p4_ = None

    def __str__(self):
        result = "Index: "+str(self.index)+" pdgId: "+str(self.pdgId)+"\n"
        if abs(self.px)<0.001 and abs(self.py)<0.001:
            result += "Pt: "+str(0)+" Eta: "
            if self.pz>0:
                result += "+"
            else:
                result += "-"
            result += "inf"
        else:
            result += "Pt: "+str(self.p4().Pt())+" Eta: "+str(self.p4().Eta())
        result += " M: "+str(self.m)+"\n"
        result += "  Indices of mothers:"
        for i in self.mothers:
            result += " "+str(i)
        result += "\n"
        result += "  Indices of daughters :"
        for i in self.daughters:
            result += " "+str(i)
        result += "\n"
        return result

    def addMother(self,mother):
        assert not mother in self.mothers
        self.mothers.append(mother)
        self.mothers.sort()

    def addDaughters(self,da1,da2=None):
        if da1!=None and da1>=0:
            d1 = da1
            d2 = da2 if ( da2!=None and da2>=0 ) else da1
            assert d2>=d1
            for d in range(d1,d2+1):
                assert not d in self.daughters
                self.daughters.append(d)
        self.daughters.sort()

    def isIncoming(self):
        return not self.mothers

    def isStable(self):
        return not self.daughters

    def p4(self):
        if self.p4_==None:
            self.p4_ = ROOT.TLorentzVector(self.px,self.py,self.pz,self.e)
        return self.p4_

class LHEEvent:

    def __init__(self,lines):
        npexp = 0
        self.particles = [ ]
        #
        # loop over lines of one event and create list of particles
        #
        linefields = [ ]
        firstline = True
        for l in lines:
            l1 = l
            # remove comments
            ind = l1.find("#")
            if ind==0:
                continue
            elif ind>0:
                l1 = l1[:ind-1]
            # strip leading and trailing white space
            l1 = l.strip()
            # split in fields
            fields = l.split()
            if not fields:
                continue
            # first (summary) line?
            if firstline:
                assert len(fields)==6
                npexp = int(fields[0])
                firstline = False
            else:
                assert len(fields)==13
                p = LHEParticle(len(self.particles),int(fields[0]),
                                float(fields[6]),float(fields[7]),float(fields[8]),
                                float(fields[9]),float(fields[10]), 
                                int(fields[2])-1,int(fields[3])-1)
                self.particles.append(p)
#TEMPORARY#        assert len(self.particles)==npexp
        #
        # establish links to daughters
        #
        for ip,p in enumerate(self.particles):
            for im in p.mothers:
                self.particles[im].addDaughters(ip)

        
    def incomingParticles(self):
        result = [ ]
        for p in self.particles:
            if not p.mothers():
                result.append(p)
        return result

    def findDescendants(self,particle):
        assert particle in self.particles
        results = [ particle ]
        iread = 0
        while ( iread<len(results) ):
            p = results[iread]
            for d in p.daughters:
                results.append(self.particles[d])
            iread += 1
        return results[1:]

    def findAscendants(self,particle):
        assert particle in self.particles
        results = [ particle ]
        iread = 0
        while ( iread<len(results) ):
            p = results[iread]
            for m in p.mothers:
                results.append(self.particles[m])
            iread += 1
        return results[1:]

    def findDaughters(self,particle):
        assert particle in self.particles
        result = [ ]
        for d in particle.daughters:
            result.append(self.particles[d])
        return result

    def findMothers(self,particle):
        assert particle in self.particles
        result = [ ]
        for m in particle.mothers:
            result.append(self.particles[m])
        return result

    def findIncoming(self):
        return filterIncoming(self.particles)

    def findOutgoing(self):
        return filterOutgoing(self.particles)

    def findPrimaries(self):
        return filterPrimaries(self.particles)

    def findStables(self):
        return filterStables(self.particles)

def matchAnyPdgId(particle,pdgIds,invert,sign):
    particleId = particle.pdgId
    if not sign:
        particleId = abs(particleId)
    for id in pdgIds:
#        print "checking ",particleId,"vs",id,invert,sign
        if particleId==id:
            if not invert:
                return True
            else:
                return False
    return invert

def filterByPdgIds(particles,pdgIds,invert=False,sign=False):
    return filter( lambda p: matchAnyPdgId(p,pdgIds,invert,sign), particles )

def filterByPdgId(particles,pdgId,invert=False,sign=False):
    return filterByPdgIds(particles,[pdgId],invert,sign)

def filterIncoming(particles):
    return filter( lambda p: p.isIncoming(), particles )

def filterOutgoing(particles):
    return filter( lambda p: not p.isIncoming(), particles )

def filterStable(particles):
    return filter( lambda p: p.isStable(), particles )

def filterPrimaries(particles):
    indices = [ ]
    for p in filterIncoming(particles):
        for d in p.daughters:
            if not d in indices:
                indices.append(d)
    indices.sort()
    return [ particles[i] for i in indices ]

def sumP4(particles):
    result = None
    for p in particles:
        if result==None:
            result = ROOT.TLorentzVector(p.p4())
        else:
            result += p.p4()
#            if abs(result.Px())<0.001 and abs(result.Py())<0.001:
#                print [ ( x.index, x.pdgId ) for x in particles ]
#                print result.Px(),result.Py(),result.Pz(),result.E()
#            assert abs(result.Px())>0.001 or abs(result.Py())>0.001
    return result
