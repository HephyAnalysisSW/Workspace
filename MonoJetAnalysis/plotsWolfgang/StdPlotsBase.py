import ROOT
import math
import time
from PlotsBase import *
from EventHelper import EventHelper
from LeptonUtilities import *
from KinematicUtilities import *

class StdPlotsBase(PlotsBase):

    def __init__(self,name,preselection=None,elist=None,elistBase="./elists",rebin=None,hardMuon=False):
        PlotsBase.__init__(self,name,preselection,elist=elist,elistBase=elistBase,rebin=rebin)
        self.hardMuon = hardMuon
        self.histogramList = { }
        curdir = ROOT.gDirectory
        if not ROOT.gROOT.Get(name):
            ROOT.gROOT.mkdir(name)
        ROOT.gROOT.cd(name)


        self.charges = [ "Minus", "Plus" ]
#        self.charges = [ "" ]
        for sign in self.charges:
            self.addVariable("isrJetPt"+sign,100,0.,1000.,'l')
            self.addVariable("isrJetEta"+sign,50,0.,5.,'u')
            self.addVariable("jet2Pt"+sign,100,0.,1000.,'u')
            self.addVariable("jet2Eta"+sign,50,0.,5.,'u')
            self.addVariable("jetPtRatio"+sign,50,0.,1.,'u')
            self.addVariable("njet60"+sign,10,-0.5,9.5,'u')
            self.addVariable("njet"+sign,20,-0.5,19.5,'u')
            self.addVariable("met"+sign,100,0.,1000.,'l')
            self.addVariable("ht"+sign,100,0.,1000.,'l')
            self.addVariable("mt"+sign,50,0.,200.,'l')
            if self.hardMuon:
                self.addVariable("softMuPt"+sign,100,0.,250.,'u')
            else:
                self.addVariable("softMuPt"+sign,100,0.,25.,'u')
            self.addVariable("softMuEta"+sign,60,0.,3.,'u')
            self.addVariable("softMuIso"+sign,100,0.,10.,'u')
            self.addVariable("softMuNPix"+sign,10,0.,10.,'u')
            self.addVariable("softMuNTk"+sign,20,0.,20.,'u')
            self.addVariable("softMuDxy"+sign,100,0.,0.1,'u')
            self.addVariable("softMuDz"+sign,100,0.,0.2,'u')
            self.addVariable("npv"+sign,100,0.,100.,'u')
            self.addVariable("jetmuDeltaEta"+sign,50,0.,10.,'l')
            self.addVariable("jetmuDeltaR"+sign,50,0.,10.,'l')
            self.addVariable("mlb"+sign,20,0.,100.,'u')
            self.addVariable("drlb"+sign,20,0.,10.,'u')
            if self.hardMuon:
                self.addVariable("btag1Pt"+sign,50,0.,1000.,'u')
            else:
                self.addVariable("btag1Pt"+sign,50,0.,250.,'u')
            self.addVariable("btag1Eta"+sign,50,0.,2.5,'u')
            self.addVariablePair("met",40,0.,1000.,"ht",40,0.,1000.,suffix=sign)
            self.addVariablePair("met",40,0.,1000.,"muPt",40,0.,1000.,suffix=sign)
            self.addVariablePair("WPt",40,0.,1000.,"met",40,0.,1000.,suffix=sign)
            self.addVariablePair("WPt",40,0.,1000.,"muPt",40,0.,1000.,suffix=sign)

        curdir.cd()

    def fill(self,eh,downscale=1):

        isrJetPt = eh.get("isrJetPt")
        if math.isnan(isrJetPt):
            return

        if self.hardMuon:
            imu = hardestIsolatedMuon(eh,ptmin1=5.,ptmin2=20.,etamax=1.5,reliso=0.5)
            if imu==None:
                return
            softMuPt = eh.get("muPt")[imu]
            if softMuPt<30:
                return
        else:
            softMuPt = eh.get("softIsolatedMuPt")
            if math.isnan(softMuPt):
                return

#        if isrJetPt<350:
#            return

        met = eh.get("type1phiMet")
#        if met<300:
#            return

        if self.hardMuon:
            softMuEta = eh.get("muEta")[imu]
        else:
            softMuEta = eh.get("softIsolatedMuEta")
        if abs(softMuEta)>1.5:
            return

        njet = int(eh.get("njetCount")+0.5)
        jetPts = eh.get("jetPt")
        ht = 0
        for i in range(njet):
            if jetPts[i]>30:
                ht += jetPts[i]
#        if ht<400:
#            return

        if self.hardMuon:
            pdg = eh.get("muPdg")[imu]
        else:
            pdg = eh.get("softIsolatedMuPdg")
        if len(self.charges)==1:
            pdg = 0

        jetEtas = eh.get("jetEta")
        jetBtags = eh.get("jetBtag")
        ib = None
        nb = 0
        for i in range(njet):
#            if jetPts[i]>30 and jetPts[i]<60 and jetBtags[i]>0.679:
            if jetPts[i]>30 and abs(jetEtas[i])<2.4 and jetBtags[i]>0.679:
                if ib==None:
                    ib = i
                nb += 1
        if ib!=None:
            return
        
        if self.hardMuon:
            softMuPhi = eh.get("muPhi")[imu]
        else:
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
        
        npv = eh.get("ngoodVertices")
        self.fill1DBySign("npv",pdg,npv,w)

        if self.hardMuon:
            softMuIso = eh.get("muRelIso")[imu]*softMuPt
            softMuNPix = eh.get("muPixelHits")[imu]
            softMuNTk = eh.get("muNumtrackerLayerWithMeasurement")[imu]
            softMuDxy = eh.get("muDxy")[imu]
            softMuDz = eh.get("muDz")[imu]
        else:
            softMuIso = eh.get("softIsolatedMuRelIso")*softMuPt
            softMuNPix = eh.get("softIsolatedMuPixelHits")
            softMuNTk = eh.get("softIsolatedMuNumtrackerLayerWithMeasurement")
            softMuDxy = eh.get("softIsolatedMuDxy")
            softMuDz = eh.get("softIsolatedMuDz")
        self.fill1DBySign("softMuIso",pdg,softMuIso,w)
        self.fill1DBySign("softMuNPix",pdg,softMuNPix,w)
        self.fill1DBySign("softMuNTk",pdg,softMuNTk,w)
        self.fill1DBySign("softMuDxy",pdg,softMuDxy,w)
        self.fill1DBySign("softMuDz",pdg,softMuDz,w)

        self.fill2DBySign("ht_vs_met",pdg,met,ht,w)
        self.fill2DBySign("muPt_vs_met",pdg,met,softMuPt,w)

        wPx = softMuPt*math.cos(softMuPhi) + met*math.cos(metphi)
        wPy = softMuPt*math.sin(softMuPhi) + met*math.sin(metphi)
        wPt = math.sqrt(wPx**2+wPy**2)
        self.fill2DBySign("met_vs_WPt",pdg,wPt,met,w)
        self.fill2DBySign("muPt_vs_WPt",pdg,wPt,softMuPt,w)

        self.fill1DBySign("ht",pdg,ht,w)
        self.fill1DBySign("mt",pdg,mt,w)
        
        self.fill1DBySign("isrJetPt",pdg,isrJetPt,w)
        self.fill1DBySign("isrJetEta",pdg,abs(eh.get("isrJetEta")),w)

        jetPtRatio = 0.
        jet2Pt = 0.
        jet2Eta = 0.
        if njet>1:
#            jetPts = eh.get("jetPt")
            jetPtRatio = jetPts[1]/jetPts[0]
            jet2Pt = jetPts[1]
#            jetEtas = eh.get("jetEta")
            jet2Eta = jetEtas[1]
        self.fill1DBySign("jetPtRatio",pdg,jetPtRatio,w)
        self.fill1DBySign("jet2Pt",pdg,jet2Pt,w)
        self.fill1DBySign("jet2Eta",pdg,jet2Eta,w)


        btag1Pt = 0.
        btag1Eta = 0.
        for i in range(njet):
            if jetPts[i]>30 and abs(jetEtas[i])<2.4 and jetBtags[i]>0.679:
                btag1Pt = jetPts[i]
                btag1Eta = jetEtas[i]
                break
        self.fill1DBySign("btag1Pt",pdg,btag1Pt,w)
        self.fill1DBySign("btag1Eta",pdg,abs(btag1Eta),w)

        self.fill1DBySign("njet60",pdg,eh.get("njet60"),w)
        self.fill1DBySign("njet",pdg,eh.get("njetCount"),w)

        self.fill1DBySign("met",pdg,met,w)

        self.fill1DBySign("softMuPt",pdg,softMuPt,w)
        self.fill1DBySign("softMuEta",pdg,abs(softMuEta),w)
           
        jetPhis = eh.get("jetPhi")
        if ib!=None:
            p4mu = ROOT.TLorentzVector()
            p4mu.SetPtEtaPhiM(softMuPt,softMuEta,softMuPhi,0.105)
            p4b = ROOT.TLorentzVector()
            p4b.SetPtEtaPhiM(jetPts[ib],jetEtas[ib],jetPhis[ib],5.)
            self.fill1DBySign("mlb",pdg,(p4mu+p4b).M(),w)
            self.fill1DBySign("drlb",pdg,p4mu.DeltaR(p4b),w)

        self.fill1DBySign("jetmuDeltaEta",pdg,abs(jetEtas[0]-softMuEta),w)
        self.fill1DBySign("jetmuDeltaR",pdg,deltaR(jetPhis[0],jetEtas[0],softMuPhi,softMuEta),w)

    def showTimers(self):
        line = ""
        for t in self.timers:
            line += "{0:14.2f}".format(1000000*t.meanTime())
#            line += " " + str(t.meanTime())
        print line
            
    def histograms(self):
        return self.histogramList
        
