import ROOT
import sys
from DataFormats.FWLite import Events, Handle
from math import *
import array

def isAncestor(a,p) :
        if a == p : 
                return True
        for i in xrange(0,p.numberOfMothers()) :
                if isAncestor(a,p.mother(i)) :
                         return True
        return False

def find(x,lp):
  if x in lp:
    return lp.index(x)
  else:
    return -1


print ' '

events = Events (['file:/data/imikulec/gen15/T2ttDeg_mStop350_mChi330_4bodydec.MINIAODSIM00.root'])

handlePruned  = Handle ("std::vector<reco::GenParticle>")
handlePacked  = Handle ("std::vector<pat::PackedGenParticle>")
labelPruned = ("prunedGenParticles")
labelPacked = ("packedGenParticles")

# loop over events
count= 0
for event in events:
    event.getByLabel (labelPacked, handlePacked)
    event.getByLabel (labelPruned, handlePruned)
    # get the product
    packed = handlePacked.product()
    pruned = handlePruned.product()
    
    print "pruned", "-"*40
    lp = []
    for p in pruned: lp.append(p)
    for ip,p in enumerate(pruned):
        print '{10:>3d} {0:>3d} {1:>10d} {2:>12.2f} {3:>12.2f} {4:>12.2f} {5:>12.2f} {6:>5d} {7:>5d} {8:>5d} {9:>5d}'.\
                       format(p.status(),p.pdgId(),p.pt(),p.eta(),p.phi(),p.energy(),find(p.mother(0),lp),find(p.mother(max(p.numberOfMothers()-1,0)),lp),\
                                                                        find(p.daughter(0),lp),find(p.daughter(max(p.numberOfDaughters()-1,0)),lp),ip)
'''    
    print "packed", "-"*40
    lp = []
    for p in packed: lp.append(p)
    for ip,p in enumerate(packed):
        print '{9:>3d} {0:>3d} {1:>10d} {2:>12.2f} {3:>12.2f} {4:>12.2f} {5:>5d} {6:>5d} {7:>5d} {8:>5d}'.\
                       format(p.status(),p.pdgId(),p.pt(),p.eta(),p.phi(),find(p.mother(0),lp),find(p.mother(max(p.numberOfMothers()-1,0)),lp),\
                                                                        find(p.daughter(0),lp),find(p.daughter(max(p.numberOfDaughters()-1,0)),lp),ip)
    

    

   
    
        if abs(p.pdgId()) > 500 and abs(p.pdgId()) < 600 :
                print "PdgId : %s   pt : %s  eta : %s   phi : %s" %(p.pdgId(),p.pt(),p.eta(),p.phi())    
                print "     daughters"
                for pa in packed:
                        mother = pa.mother(0)
                        if mother and isAncestor(p,mother) :
                              print "     PdgId : %s   pt : %s  eta : %s   phi : %s" %(pa.pdgId(),pa.pt(),pa.eta(),pa.phi())
'''
