import ROOT
import math
import time
from PlotsBase import *
from EventHelper import EventHelper

def deltaPhi(phi1,phi2):
    result = phi2 - phi1
    if result<-math.pi:
        result += 2*math.pi
    if result>math.pi:
        result -= 2*math.pi
    return result

def deltaR(phi1,eta1,phi2,eta2):
    dphi = deltaPhi(phi1,phi2)
    deta = eta2 - eta1
    return math.sqrt(dphi*dphi+deta*deta)

        
class StdPlots(PlotsBase):

#    def addHistogram1D(self,name,nbins,xmin,xmax):
#        assert name.isalnum()
#        h1d = ROOT.TH1F(name,name,nbins,xmin,xmax)
#        self.histogramList.append(h1d)
        setattr(self,"h"+name,h1d)
        
    def __init__(self,name,preselection=None,elist=None,elistBase="./elists",rebin=None):
        PlotsBase.__init__(self,name,preselection,elist=elist,elistBase=elistBase,rebin=rebin)
        self.histogramList = { }
        curdir = ROOT.gDirectory
        if not ROOT.gROOT.Get(name):
            ROOT.gROOT.mkdir(name)
        ROOT.gROOT.cd(name)

        self.addVariable("isrJetPt",100,0.,1000.,'l')
        self.addVariable("isrJetEta",50,0.,5.,'u')
        self.addVariable("jet2Pt",100,0.,1000.,'u')
        self.addVariable("jet2Eta",50,0.,5.,'u')
        self.addVariable("jetPtRatio",50,0.,1.,'u')
        self.addVariable("njet60",10,-0.5,9.5,'u')
        self.addVariable("njet",20,-0.5,19.5,'u')
        self.addVariable("met",100,0.,1000.,'l')
        self.addVariable("ht",100,0.,1000.,'l')
        self.addVariable("mt",50,0.,200.,'l')
        self.addVariable("softMuPt",100,0.,25.,'u')
        self.addVariable("softMuEta",60,0.,3.,'u')
        self.addVariable("jetmuDeltaEta",50,0.,10.,'l')
        self.addVariable("jetmuDeltaR",50,0.,10.,'l')
        self.addVariable("mlb",20,0.,100.,'u')
        self.addVariable("drlb",20,0.,10.,'u')
        self.addVariable("btag1Pt",50,0.,1000.,'u')
        self.addVariable("btag1Eta",50,0.,2.5,'u')
        self.addVariablePair("met",40,0.,1000.,"ht",40,0.,1000.)

        curdir.cd()

    def fill(self,eh,downscale=1):

        isrJetPt = eh.get("isrJetPt")
        softMuPt = eh.get("softIsolatedMuPt")
        if math.isnan(softMuPt) or math.isnan(isrJetPt):
            return

#        if isrJetPt<350:
#            return

        met = eh.get("type1phiMet")
        if met<300:
            return

        softMuEta = eh.get("softIsolatedMuEta")
#        if abs(softMuEta)>1.5:
#            return

        njet = int(eh.get("njetCount")+0.5)
        jetPts = eh.get("jetPt")
        ht = 0
        for i in range(njet):
            if jetPts[i]>30:
                ht += jetPts[i]
#        if ht<400:
#            return
        if njet>1 or ht>400:
            return
        if eh.get("softIsolatedMuPdg")<0:
            return

        jetEtas = eh.get("jetEta")
        jetBtags = eh.get("jetBtag")
        ib = None
        for i in range(njet):
#            if jetPts[i]>30 and jetPts[i]<60 and jetBtags[i]>0.679:
            if jetPts[i]>30 and abs(jetEtas[i])<2.4 and jetBtags[i]>0.679:
                ib = i
                break
        if ib!=None:
            return
        
        softMuPhi = eh.get("softIsolatedMuPhi")
        metphi = eh.get("type1phiMetphi")
        mt = math.sqrt(2*met*softMuPt*(1-math.cos(metphi-softMuPhi)))
#        if mt<60 or mt>88:
#            return


        self.timers[0].start()
        if self.name!="data":
            w = eh.get("puWeight")*downscale
        else:
            w = 1
        self.timers[0].stop()
        
        self.hht_vs_met.Fill(met,ht,w)

        self.hht.Fill(ht,w)
        self.hmt.Fill(mt,w)
        
        self.hisrJetPt.Fill(isrJetPt,w)
        self.hisrJetEta.Fill(abs(eh.get("isrJetEta")),w)

        jetPtRatio = 0.
        jet2Pt = 0.
        jet2Eta = 0.
        if njet>1:
#            jetPts = eh.get("jetPt")
            jetPtRatio = jetPts[1]/jetPts[0]
            jet2Pt = jetPts[1]
#            jetEtas = eh.get("jetEta")
            jet2Eta = jetEtas[1]
        self.hjetPtRatio.Fill(jetPtRatio,w)
        self.hjet2Pt.Fill(jet2Pt,w)
        self.hjet2Eta.Fill(jet2Eta,w)


        btag1Pt = 0.
        btag1Eta = 0.
        for i in range(njet):
            if jetPts[i]>30 and abs(jetEtas[i])<2.4 and jetBtags[i]>0.679:
                btag1Pt = jetPts[i]
                btag1Eta = jetEtas[i]
                break
        self.hbtag1Pt.Fill(btag1Pt,w)
        self.hbtag1Eta.Fill(abs(btag1Eta),w)

        self.hnjet60.Fill(eh.get("njet60"),w)
        self.hnjet.Fill(eh.get("njetCount"),w)

        self.hmet.Fill(met,w)

        self.hsoftMuPt.Fill(softMuPt,w)
        self.hsoftMuEta.Fill(abs(softMuEta),w)
           
        jetPhis = eh.get("jetPhi")
        if ib!=None:
            p4mu = ROOT.TLorentzVector()
            p4mu.SetPtEtaPhiM(softMuPt,softMuEta,softMuPhi,0.105)
            p4b = ROOT.TLorentzVector()
            p4b.SetPtEtaPhiM(jetPts[ib],jetEtas[ib],jetPhis[ib],5.)
            self.hmlb.Fill((p4mu+p4b).M(),w)
            self.hdrlb.Fill(p4mu.DeltaR(p4b),w)

        self.hjetmuDeltaEta.Fill(abs(jetEtas[0]-softMuEta),w)
        self.hjetmuDeltaR.Fill(deltaR(jetPhis[0],jetEtas[0],softMuPhi,softMuEta),w)

    def showTimers(self):
        line = ""
        for t in self.timers:
            line += "{0:14.2f}".format(1000000*t.meanTime())
#            line += " " + str(t.meanTime())
        print line
            
    def histograms(self):
        return self.histogramList
        
