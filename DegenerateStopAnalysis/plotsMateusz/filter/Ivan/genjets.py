from ROOT import *
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

def drawhh(hname):
    exec('hh{0}1.Draw()'.format(hname))
    exec('hh{0}2.SetLineColor(2)'.format(hname))
    exec('hh{0}2.Draw("same")'.format(hname))
    exec('hh{0}3.SetLineColor(3)'.format(hname))
    exec('hh{0}3.Draw("same")'.format(hname))
    gPad.Update()

def writeevent(iev,all,jets,genjets,met,genmet):
    gg = file("out"+str(iev)+".dat","w")
    
    print >>gg, "met =",met
    print >>gg, "genmet =",genmet
    print >>gg, "jets", "-"*40
    for ij,j in enumerate(jets):
        genpt = 0 if not j.genJet() else j.genJet().pt()
        print >>gg, ij, j.pt(), j.eta(), j.phi(), j.mass(), genpt
    print >>gg, "genjets", "-"*40
    for ij,j in enumerate(genjets):
        print >>gg, ij, j.pt(), j.eta(), j.phi(), j.mass()
    print >>gg, "all", "-"*40
    lp = []
    for p in all: lp.append(p)
    for ip,p in enumerate(all):
        print >>gg, '{10:>3d} {0:>3d} {1:>10d} {2:>12.2f} {3:>12.2f} {4:>12.2f} {5:>12.2f} {6:>5d} {7:>5d} {8:>5d} {9:>5d}'.\
                       format(p.status(),p.pdgId(),p.pt(),p.eta(),p.phi(),p.energy(),find(p.mother(0),lp),find(p.mother(max(p.numberOfMothers()-1,0)),lp),\
                                                                        find(p.daughter(0),lp),find(p.daughter(max(p.numberOfDaughters()-1,0)),lp),ip)
    gg.close()

def getjetpt(jets,etacut):
    for jet in jets:
        if abs(jet.eta())<etacut:
            return jet.pt()
    return 0.


print ' '

events = Events (['/data/gen15/miniAODwithGP/T2DegStop2j_300_270_miniAOD_2_1_4pm.root','/data/gen15/miniAODwithGP/T2DegStop2j_300_270_miniAOD_3_1_5V0.root'])

handleAll  = Handle ("std::vector<reco::GenParticle>")
labelAll = ("genParticles")

handleGenJets = Handle("std::vector<reco::GenJet>")
labelGenJets = ("slimmedGenJets")

handleJets = Handle("std::vector<pat::Jet>")
labelJets = ("slimmedJets")

handleMets = Handle("std::vector<pat::MET>")
labelMets = ("slimmedMETs")

g = TFile("out.root","RECREATE")

for rg in ['r','g']:
    for var in ['jpt','met']:
        for i in range(1,5):
            hname = "hh"+rg+var+str(i)
            exec('{0} = TH1F("{0}","",1000,0,1000)'.format(hname))

# loop over events
count = 0
for event in events:

    event.getByLabel (labelAll, handleAll)
    all = handleAll.product()
    
    event.getByLabel(labelGenJets,handleGenJets)
    genjets = handleGenJets.product()
    
    event.getByLabel(labelJets,handleJets)
    jets = handleJets.product()
    
    event.getByLabel(labelMets,handleMets)
    mets = handleMets.product()
    

#    print "all", "-"*40
#    lp = []
#    for p in all: lp.append(p)
#    for ip,p in enumerate(all):
#        print '{10:>3d} {0:>3d} {1:>10d} {2:>12.2f} {3:>12.2f} {4:>12.2f} {5:>12.2f} {6:>5d} {7:>5d} {8:>5d} {9:>5d}'.\
#                       format(p.status(),p.pdgId(),p.pt(),p.eta(),p.phi(),p.energy(),find(p.mother(0),lp),find(p.mother(max(p.numberOfMothers()-1,0)),lp),\
#                                                                        find(p.daughter(0),lp),find(p.daughter(max(p.numberOfDaughters()-1,0)),lp),ip)

#    print count
#    for ij,j in enumerate(genjets):
#        print ij, j.pt()

#    for ij,j in enumerate(jets):
#        if j.genJet():
#            hh1.Fill(j.pt()-j.genJet().pt())
#            if j.pt()>110: hh2.Fill(j.pt()-j.genJet().pt())

#    for ij,j in enumerate(mets):
#        print ij, j.pt()
        
    psum =  TLorentzVector(1e-9,1e-9,1e-9,1e-9)
    for ip,p in enumerate(all):
        mom = 0 if not p.mother(0) else p.mother(0).pdgId()
        if p.status()==1 and p.pdgId() in [12,14,16,1000022] and abs(mom)==1000006:
            aux = TLorentzVector(1e-9,1e-9,1e-9,1e-9)
            aux.SetPtEtaPhiM(p.pt(),p.eta(),p.phi(),p.mass())            
            psum += aux
    genmet = psum.Pt()
    met = mets[0].pt()
        
    leadinggenpt = getjetpt(genjets,2.5)
    leadingpt = getjetpt(jets,2.4)
        
    hhrjpt1.Fill(leadingpt)
    hhgjpt1.Fill(leadinggenpt)
    hhrmet1.Fill(met)
    hhgmet1.Fill(genmet)      
        
    if leadingpt>110.:
        hhgjpt2.Fill(leadinggenpt)
        hhgmet2.Fill(genmet)
        if met>200.:
            hhgjpt3.Fill(leadinggenpt)
            hhgmet3.Fill(genmet)
    if met>200.:
        hhgjpt4.Fill(leadinggenpt)
        hhgmet4.Fill(genmet)

    if leadinggenpt>100.:
        hhrjpt2.Fill(leadingpt)
        hhrmet2.Fill(met)
        if genmet>110.:
            hhrjpt3.Fill(leadingpt)
            hhrmet3.Fill(met)
    if genmet>110.:
        hhrjpt4.Fill(leadingpt)
        hhrmet4.Fill(met)


    if met>200 and leadingpt>110 and not (genmet>110 and leadinggenpt>100):
        writeevent(count,all,jets,genjets,met,genmet)
    count += 1
    
#    if count>1000: break

#drawhh("gjpt")
g.Write()
g.Close()

