import ROOT
import math
import time
from PlotsBase import *
from EventHelper import EventHelper
from LeptonUtilities import *
from myPolSys import calcPolWeights

polVar = None
#polVar = "WPol1Plus10_weight_flfr"
#polVar = "WPol1Minus10_weight_flfr"
#polVar = "WPol2PlusPlus5_weight_flfr"
#polVar = "WPol2PlusMinus5_weight_flfr"
#polVar = "WPol2MinusPlus5_weight_flfr"
#polVar = "WPol2MinusMinus5_weight_flfr"
#polVar = "WPol3Plus10_weight_f0"
#polVar = "WPol3Minus10_weight_f0"


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

        
class SR12_MTcentral_Plots_HardMu(PlotsBase):

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

        for sign in [ "Minus", "Plus" ]:
            self.addVariable("isrJetPt"+sign,100,0.,1000.,'l')
            self.addVariable("isrJetEta"+sign,50,0.,5.,'u')
            self.addVariable("jet2Pt"+sign,100,0.,1000.,'u')
            self.addVariable("jet2Eta"+sign,50,0.,5.,'u')
            self.addVariable("jetPtRatio"+sign,50,0.,1.,'u')
            self.addVariable("njet60"+sign,10,-0.5,9.5,'u')
            self.addVariable("njet"+sign,20,-0.5,19.5,'u')
            self.addVariable("met"+sign,100,0.,1000.,'l')
            self.addVariable("mt"+sign,50,0.,200.,'l')
            self.addVariable("softMuPt"+sign,100,0.,25.,'u')
            self.addVariable("softMuEta"+sign,60,0.,3.,'u')
            self.addVariable("jetmuDeltaEta"+sign,50,0.,10.,'l')
            self.addVariable("jetmuDeltaR"+sign,50,0.,10.,'l')
            self.addVariable("htmetIndex"+sign,4,-100,0,'b')
            self.addVariable("ht"+sign,24,0.,600.,'b')
            self.addVariable("count"+sign,1,-0.5,1.5,'b')
            self.addVariablePair("muabsiso",50,0.,10.,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("mudxy",50,0.,0.2,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("mudz",50,0.,0.5,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("mupix",5,0.,5.,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("isrJetPt",50,0.,1000.,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("isrJetEta",25,0.,5.,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("njet60",10,-0.5,9.5,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("njet",20,-0.5,19.5,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("softMuPt",50,0.,25.,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("softMuEta",30,0.,3.,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("jetmuDeltaEta",25,0.,10.,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("jetmuDeltaR",25,0.,10.,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("softEle",10,0.,10.,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("softTau",10,0.,10.,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("softB",10,0.,10.,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("softMuIsGlob",2,0.,2.,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("softMuIsTk",2,0.,2.,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("softMuNValMu",10,0.,10.,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("softMuNormChi2",10,0.,20.,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("softMuNMatched",20,0.,20.,"htmet",4,-100,0,suffix=sign)
            self.addVariablePair("softMuNTkLayer",20,0.,20.,"htmet",4,-100,0,suffix=sign)


        self.addVariablePair("met",40,0.,1000.,"ht",40,0.,1000.)

        curdir.cd()

    def fill(self,eh,downscale=1):

        imu = hardestIsolatedMuon(eh,ptmin1=5.,ptmin2=20.,etamax=1.5,reliso=0.5)
        isrJetPt = eh.get("isrJetPt")
        if imu==None or math.isnan(isrJetPt):
            return

#        softMuPt = eh.get("softIsolatedMuPt")
        softMuPt = eh.get("muPt")[imu]
        if math.isnan(softMuPt) or math.isnan(isrJetPt):
            return
        if softMuPt<30:
            return

#        if isrJetPt<350:
#            return


        njet = int(eh.get("njetCount")+0.5)
#        if njet>3:
#            return

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

#        softMuPhi = eh.get("softIsolatedMuPhi")
        softMuPhi = eh.get("muPhi")[imu]
        met = eh.get("type1phiMet")
        if met<300:
            return
        metphi = eh.get("type1phiMetphi")
        mt = math.sqrt(2*met*softMuPt*(1-math.cos(metphi-softMuPhi)))
#        mt = eh.get("softIsolatedMT")
        if ( mt < 60 ) or ( mt > 88 ):
            return

#        ht = 0
#        for i in range(njet):
#            if jetPts[i]>30:
#                ht += jetPts[i]
        ht = eh.get("ht")
        if ht<400:
            return

        ihtmet = -25
        while True:
            metcut = 300 + ihtmet
            htcut = 400 + ihtmet
#            if metcut<0 or htcut<0:
#                return
            if met >= metcut and ht >= htcut:
                break
            ihtmet -= 25
        


        self.timers[0].start()
        if self.name!="data":
            w = eh.get("puWeight")*downscale
        else:
            w = 1
        self.timers[0].stop()

        if self.name.startswith("WJets") and polVar!=None:
            polVars = calcPolWeights(eh)
            w *= polVars[polVar]
        
#        pdg = eh.get("softIsolatedMuPdg")
        pdg = eh.get("muPdg")[imu]

        if met>300 and ht>400:
            if pdg>0:
                self.hcountMinus.Fill(0.,w)
            else:
                self.hcountPlus.Fill(0.,w)

        self.hht_vs_met.Fill(met,ht,w)
        self.fill1DBySign("htmetIndex",pdg,ihtmet,w)

        if ihtmet<-100:
            return

        self.fill1DBySign("ht",pdg,ht,w)
        self.fill1DBySign("met",pdg,met,w)

        self.fill1DBySign("mt",pdg,mt,w)
        
        self.fill1DBySign("isrJetPt",pdg,isrJetPt,w)
        self.fill2DBySign("htmet_vs_isrJetPt",pdg,isrJetPt,ihtmet,w)
        self.fill1DBySign("isrJetEta",pdg,abs(eh.get("isrJetEta")),w)
        self.fill2DBySign("htmet_vs_isrJetEta",pdg,abs(eh.get("isrJetEta")),ihtmet,w)

#        softMuIso = eh.get("softIsolatedMuRelIso")
        softMuIso = eh.get("muRelIso")[imu]
        self.fill2DBySign("htmet_vs_muabsiso",pdg,softMuIso*softMuPt,ihtmet,w)

#        softMuDxy = eh.get("softIsolatedMuDxy")
        softMuDxy = eh.get("muDxy")[imu]
        self.fill2DBySign("htmet_vs_mudxy",pdg,softMuDxy,ihtmet,w)

#        softMuDz = eh.get("softIsolatedMuDz")
        softMuDz = eh.get("muDz")[imu]
        self.fill2DBySign("htmet_vs_mudz",pdg,softMuDz,ihtmet,w)

#        softMuPix = eh.get("softIsolatedMuPixelHits")
        softMuPix = eh.get("muPixelHits")[imu]
        self.fill2DBySign("htmet_vs_mupix",pdg,softMuPix,ihtmet,w)

#        softMuIsGlob = eh.get("softIsolatedMuIsGlobal")
        softMuIsGlob = eh.get("muIsGlobal")[imu]
        self.fill2DBySign("htmet_vs_softMuIsGlob",pdg,softMuIsGlob,ihtmet,w)

#        softMuIsTk = eh.get("softIsolatedMuIsTracker")
        softMuIsTk = eh.get("muIsTracker")[imu]
        self.fill2DBySign("htmet_vs_softMuIsTk",pdg,softMuIsTk,ihtmet,w)

#        softMuNValMu = eh.get("softIsolatedMuNValMuonHits")
        softMuNValMu = eh.get("muNValMuonHits")[imu]
        self.fill2DBySign("htmet_vs_softMuNValMu",pdg,softMuNValMu,ihtmet,w)

#        softMuNormChi2 = eh.get("softIsolatedMuNormChi2")
        softMuNormChi2 = eh.get("muNormChi2")[imu]
        self.fill2DBySign("htmet_vs_softMuNormChi2",pdg,softMuNormChi2,ihtmet,w)

#        softMuNMatched = eh.get("softIsolatedMuNumMatchedStations")
        softMuNMatched = eh.get("muNumMatchedStations")[imu]
        self.fill2DBySign("htmet_vs_softMuNMatched",pdg,softMuNMatched,ihtmet,w)

#        softMuNTkLayer = eh.get("softIsolatedMuNumtrackerLayerWithMeasurement")
        softMuNTkLayer = eh.get("muNumtrackerLayerWithMeasurement")[imu]
        self.fill2DBySign("htmet_vs_softMuNTkLayer",pdg,softMuNTkLayer,ihtmet,w)

        self.fill2DBySign("htmet_vs_softEle",pdg,eh.get("nSoftElectrons"),ihtmet,w)
        self.fill2DBySign("htmet_vs_softTau",pdg,eh.get("nSoftTaus"),ihtmet,w)
        self.fill2DBySign("htmet_vs_softB",pdg,eh.get("nSoftbtags"),ihtmet,w)

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

        self.fill1DBySign("njet60",pdg,eh.get("njet60"),w)
        self.fill2DBySign("htmet_vs_njet60",pdg,eh.get("njet60"),ihtmet,w)
        self.fill1DBySign("njet",pdg,eh.get("njetCount"),w)
        self.fill2DBySign("htmet_vs_njet",pdg,eh.get("njetCount"),ihtmet,w)


#        softMuEta = eh.get("softIsolatedMuEta")
        softMuEta = eh.get("muEta")[imu]
        self.fill1DBySign("softMuPt",pdg,softMuPt,w)
        self.fill2DBySign("htmet_vs_softMuPt",pdg,softMuPt,ihtmet,w)
        self.fill1DBySign("softMuEta",pdg,abs(softMuEta),w)
        self.fill2DBySign("htmet_vs_softMuEta",pdg,abs(softMuEta),ihtmet,w)
           
        jetPhis = eh.get("jetPhi")
        self.fill1DBySign("jetmuDeltaEta",pdg,abs(jetEtas[0]-softMuEta),w)
        self.fill2DBySign("htmet_vs_jetmuDeltaEta",pdg,abs(jetEtas[0]-softMuEta),ihtmet,w)
        self.fill1DBySign("jetmuDeltaR",pdg,deltaR(jetPhis[0],jetEtas[0],softMuPhi,softMuEta),w)
        self.fill2DBySign("htmet_vs_jetmuDeltaR",pdg,deltaR(jetPhis[0],jetEtas[0],softMuPhi,softMuEta),ihtmet,w)

    def showTimers(self):
        line = ""
        for t in self.timers:
            line += "{0:14.2f}".format(1000000*t.meanTime())
#            line += " " + str(t.meanTime())
        print line
            
    def histograms(self):
        return self.histogramList
        
