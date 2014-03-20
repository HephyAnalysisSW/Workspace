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

        
class SR12_MTcentral_Plots(PlotsBase):

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

        self.addVariable("isrJetPtMinus",100,0.,1000.,'l')
        self.addVariable("isrJetEtaMinus",50,0.,5.,'u')
        self.addVariable("jet2PtMinus",100,0.,1000.,'u')
        self.addVariable("jet2EtaMinus",50,0.,5.,'u')
        self.addVariable("jetPtRatioMinus",50,0.,1.,'u')
        self.addVariable("njet60Minus",10,-0.5,9.5,'u')
        self.addVariable("njetMinus",20,-0.5,19.5,'u')
        self.addVariable("metMinus",100,0.,1000.,'l')
        self.addVariable("mtMinus",50,0.,200.,'l')
        self.addVariable("softMuPtMinus",100,0.,25.,'u')
        self.addVariable("softMuEtaMinus",60,0.,3.,'u')
        self.addVariable("jetmuDeltaEtaMinus",50,0.,10.,'l')
        self.addVariable("jetmuDeltaRMinus",50,0.,10.,'l')
        self.addVariable("htmetIndexMinus",6,-112.5,37.5,'')

        self.addVariable("isrJetPtPlus",100,0.,1000.,'l')
        self.addVariable("isrJetEtaPlus",50,0.,5.,'u')
        self.addVariable("jet2PtPlus",100,0.,1000.,'u')
        self.addVariable("jet2EtaPlus",50,0.,5.,'u')
        self.addVariable("jetPtRatioPlus",50,0.,1.,'u')
        self.addVariable("njet60Plus",10,-0.5,9.5,'u')
        self.addVariable("njetPlus",20,-0.5,19.5,'u')
        self.addVariable("metPlus",100,0.,1000.,'l')
        self.addVariable("mtPlus",50,0.,200.,'l')
        self.addVariable("softMuPtPlus",100,0.,25.,'u')
        self.addVariable("softMuEtaPlus",60,0.,3.,'u')
        self.addVariable("jetmuDeltaEtaPlus",50,0.,10.,'l')
        self.addVariable("jetmuDeltaRPlus",50,0.,10.,'l')
        self.addVariable("htmetIndexPlus",6,-112.5,37.5,'')

        self.addVariablePair("met",40,0.,1000.,"ht",40,0.,1000.)

        curdir.cd()

    def fillOne1D(self,name,pdg,value,weight):
        fullname = name
        if pdg>0:
            fullname += "Minus"
        else:
            fullname += "Plus"
        self.histogramList[fullname].Fill(value,weight)

    def fill(self,eh,downscale=1):

        isrJetPt = eh.get("isrJetPt")
        softMuPt = eh.get("softIsolatedMuPt")
        if math.isnan(softMuPt) or math.isnan(isrJetPt):
            return

#        if isrJetPt<350:
#            return


        njet = int(eh.get("njetCount")+0.5)
        jetPts = eh.get("jetPt")
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
        met = eh.get("type1phiMet")
#        if met<300:
#            return
        metphi = eh.get("type1phiMetphi")
        mt = math.sqrt(2*met*softMuPt*(1-math.cos(metphi-softMuPhi)))
        if ( mt < 60 ) or ( mt > 88 ):
            return

        ht = 0
        for i in range(njet):
            if jetPts[i]>30:
                ht += jetPts[i]


        ihtmet = 25
        while True:
            metcut = 300 + ihtmet
            htcut = 400 + ihtmet
            if metcut<0 or htcut<0:
                return
            if met >= metcut and ht >= htcut:
                break
            ihtmet -= 25
        


        self.timers[0].start()
        if self.name!="data":
            w = eh.get("puWeight")*downscale
        else:
            w = 1
        self.timers[0].stop()
        
        pdg = eh.get("softIsolatedMuPdg")

        self.hht_vs_met.Fill(met,ht,w)
        self.fillOne1D("htmetIndex",pdg,ihtmet,w)

        if ihtmet<-100:
            return

        self.fillOne1D("mt",pdg,mt,w)
        
        self.fillOne1D("isrJetPt",pdg,isrJetPt,w)
        self.fillOne1D("isrJetEta",pdg,abs(eh.get("isrJetEta")),w)

        jetPtRatio = 0.
        jet2Pt = 0.
        jet2Eta = 0.
        if njet>1:
#            jetPts = eh.get("jetPt")
            jetPtRatio = jetPts[1]/jetPts[0]
            jet2Pt = jetPts[1]
#            jetEtas = eh.get("jetEta")
            jet2Eta = jetEtas[1]
        self.fillOne1D("jetPtRatio",pdg,jetPtRatio,w)
        self.fillOne1D("jet2Pt",pdg,jet2Pt,w)
        self.fillOne1D("jet2Eta",pdg,jet2Eta,w)

        self.fillOne1D("njet60",pdg,eh.get("njet60"),w)
        self.fillOne1D("njet",pdg,eh.get("njetCount"),w)

        self.fillOne1D("met",pdg,met,w)

        softMuEta = eh.get("softIsolatedMuEta")
        self.fillOne1D("softMuPt",pdg,softMuPt,w)
        self.fillOne1D("softMuEta",pdg,abs(softMuEta),w)
           
        jetPhis = eh.get("jetPhi")
        self.fillOne1D("jetmuDeltaEta",pdg,abs(jetEtas[0]-softMuEta),w)
        self.fillOne1D("jetmuDeltaR",pdg,deltaR(jetPhis[0],jetEtas[0],softMuPhi,softMuEta),w)

    def showTimers(self):
        line = ""
        for t in self.timers:
            line += "{0:14.2f}".format(1000000*t.meanTime())
#            line += " " + str(t.meanTime())
        print line
            
    def histograms(self):
        return self.histogramList
        
