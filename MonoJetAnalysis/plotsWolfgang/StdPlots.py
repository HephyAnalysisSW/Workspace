import ROOT
import math
import time
from PlotsBase import *
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

        
class StdPlots(PlotsBase):

    def addHistogram1D(self,name,nbins,xmin,xmax):
        assert name.isalnum()
        h1d = ROOT.TH1F(name,name,nbins,xmin,xmax)
        self.histogramList.append(h1d)
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
        self.addVariable("softMuPt",100,0.,25.,'u')
        self.addVariable("softMuEta",60,0.,3.,'u')
        self.addVariable("jetmuDeltaEta",50,0.,10.,'l')
        self.addVariable("mlb",20,0.,100.,'u')
        self.addVariable("drlb",20,0.,10.,'u')

        curdir.cd()

    def fill(self,eh,downscale=1):

        self.timers[0].start()
        w = eh.get("puWeight")*downscale
        self.timers[0].stop()
        
        isrJetPt = eh.get("isrJetPt")
        if isrJetPt<350:
            return

        met = eh.get("type1phiMet")
        if met<250:
            return

        softMuPt = eh.get("softIsolatedMuPt")
        softMuEta = eh.get("softIsolatedMuEta")

        if math.isnan(softMuPt) or math.isnan(isrJetPt):
            return
        
        self.hisrJetPt.Fill(isrJetPt,w)
        self.hisrJetEta.Fill(abs(eh.get("isrJetEta")),w)

        jetPtRatio = 0.
        jet2Pt = 0.
        jet2Eta = 0.
        njet = int(eh.get("njetCount")+0.5)
        jetPts = eh.get("jetPt")
        jetEtas = eh.get("jetEta")
        jetBtags = eh.get("jetBtag")
        if njet>1:
#            jetPts = eh.get("jetPt")
            jetPtRatio = jetPts[1]/jetPts[0]
            jet2Pt = jetPts[1]
#            jetEtas = eh.get("jetEta")
            jet2Eta = jetEtas[1]
        self.hjetPtRatio.Fill(jetPtRatio,w)
        self.hjet2Pt.Fill(jet2Pt,w)
        self.hjet2Eta.Fill(jet2Eta,w)

        self.hnjet60.Fill(eh.get("njet60"),w)
        self.hnjet.Fill(eh.get("njetCount"),w)

        self.hmet.Fill(met,w)

        self.hsoftMuPt.Fill(softMuPt,w)
        self.hsoftMuEta.Fill(abs(softMuEta),w)
           
        ib = None
        for i in range(njet):
            if jetPts[i]>30 and jetPts[i]<60 and jetBtags[i]>0.679:
                ib = i
                break
        if ib!=None:
            softMuPhi = eh.get("softIsolatedMuPhi")
            jetPhis = eh.get("jetPhi")
            p4mu = ROOT.TLorentzVector()
            p4mu.SetPtEtaPhiM(softMuPt,softMuEta,softMuPhi,0.105)
            p4b = ROOT.TLorentzVector()
            p4b.SetPtEtaPhiM(jetPts[ib],jetEtas[ib],jetPhis[ib],5.)
            self.hmlb.Fill((p4mu+p4b).M(),w)
            self.hdrlb.Fill(p4mu.DeltaR(p4b),w)

        self.hjetmuDeltaEta.Fill(abs(jetEtas[0]-softMuEta),w)

    def showTimers(self):
        line = ""
        for t in self.timers:
            line += "{0:14.2f}".format(1000000*t.meanTime())
#            line += " " + str(t.meanTime())
        print line
            
    def histograms(self):
        return self.histogramList
        
