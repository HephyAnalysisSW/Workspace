import ROOT
import math
import time
from PlotsBase import *
from EventHelper import EventHelper
from myPolSys import calcPolWeights
from LeptonUtilities import *

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

        
class LP_plots(PlotsBase):

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

        self.htLimits = ( 300., 400., 550. )
        nHtLimits = len(self.htLimits)
        self.muPtMetLimits = ( 150., 200., 300., )
        nMuPtMetLimits = len(self.muPtMetLimits)

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
            self.addVariable("softMuPt"+sign,100,0.,500.,'u')
            self.addVariable("softMuEta"+sign,60,0.,3.,'u')
            self.addVariable("jetmuDeltaEta"+sign,50,0.,10.,'l')
            self.addVariable("jetmuDeltaR"+sign,50,0.,10.,'l')
            self.addVariable("htmetIndex"+sign,6,-112.5,37.5,'b')
            self.addVariable("ht"+sign,24,0.,600.,'b')
            self.addVariable("lp"+sign,100,-1.,1.,'b')
            self.addVariable("count"+sign,1,-0.5,1.5,'b')
            self.addVariable("muPtMetIndex"+sign,nHtLimits*nMuPtMetLimits**2, \
                                 -0.5,nHtLimits*nMuPtMetLimits**2-0.5,'b')
            self.addVariablePair("met",40,0.,1000.,"muPt",40,0.,1000.,suffix=sign)


        self.addVariablePair("met",40,0.,1000.,"ht",40,0.,1000.)

        curdir.cd()

    def fillOne1D(self,name,pdg,value,weight):
        fullname = name
        if pdg>0:
            fullname += "Minus"
        else:
            fullname += "Plus"
        self.histogramList[fullname].Fill(value,weight)

    def fillOne2D(self,name,pdg,xvalue,yvalue,weight):
        fullname = name + "_"
        if pdg>0:
            fullname += "Minus"
        else:
            fullname += "Plus"
        self.histogramList[fullname].Fill(xvalue,yvalue,weight)

    def findBin(self,value,limits):
        if len(limits)==0:
            return None
        for i in range(len(limits)-1,-1,-1):
            if value>=limits[i]:
                return i
        return None

    def fill(self,eh,downscale=1):

        isrJetPt = eh.get("isrJetPt")
        if math.isnan(isrJetPt):
            return

        imus = isolatedMuons(eh,ptmin1=5.,etamax=1.5,ptmin2=20.,reliso=0.5)
        if len(imus)!=1:
            return False
        imu = imus[0]

        muPdgs = eh.get("muPdg")
        muPts = eh.get("muPt")
        muEtas = eh.get("muEta")
        muPhis = eh.get("muPhi")
        if muPts[imu]<20:
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

        softMuPt = muPts[imu]
        softMuPhi = muPhis[imu]
        softMuEta = muEtas[imu]
        met = eh.get("type1phiMet")
#        if met<300:
#            return
        metphi = eh.get("type1phiMetphi")
        mt = math.sqrt(2*met*softMuPt*(1-math.cos(metphi-softMuPhi)))
#        mt = eh.get("softIsolatedMT")
#        if ( mt < 60 ) or ( mt > 88 ):
#            return

#        ht = 0
#        for i in range(njet):
#            if jetPts[i]>30:
#                ht += jetPts[i]
        ht = eh.get("ht")

        ihtmet = 25
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
        
        pdg = muPdgs[imu]

        if met>300 and ht>400:
            if pdg>0:
                self.hcountMinus.Fill(0.,w)
            else:
                self.hcountPlus.Fill(0.,w)

        self.hht_vs_met.Fill(met,ht,w)
        self.fillOne1D("htmetIndex",pdg,ihtmet,w)

        self.fillOne2D("muPt_vs_met",pdg,met,softMuPt,w)
        iHt = self.findBin(ht,self.htLimits)
        if iHt!=None:
            iMet = self.findBin(met,self.muPtMetLimits)
            if iMet!=None:
                iMuPt = self.findBin(softMuPt,self.muPtMetLimits)
                if iMuPt!=None:
                    self.fillOne1D("muPtMetIndex",pdg,
                                   len(self.muPtMetLimits)**2*iHt+len(self.muPtMetLimits)*iMet+iMuPt,w)


        self.fillOne1D("ht",pdg,ht,w)
        self.fillOne1D("met",pdg,met,w)

#        if ihtmet<-100:
#            return

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


        self.fillOne1D("softMuPt",pdg,softMuPt,w)
        self.fillOne1D("softMuEta",pdg,abs(softMuEta),w)
           
        jetPhis = eh.get("jetPhi")
        self.fillOne1D("jetmuDeltaEta",pdg,abs(jetEtas[0]-softMuEta),w)
        self.fillOne1D("jetmuDeltaR",pdg,deltaR(jetPhis[0],jetEtas[0],softMuPhi,softMuEta),w)

        muPx = softMuPt*math.cos(softMuPhi)
        muPy = softMuPt*math.sin(softMuPhi)
        wPx = met*math.cos(metphi) + muPx
        wPy = met*math.sin(metphi) + muPy
        lp = (muPx*wPx+muPy*wPy)/(wPx*wPx+wPy*wPy)
        self.fillOne1D("lp",pdg,lp,w)

    def showTimers(self):
        line = ""
        for t in self.timers:
            line += "{0:14.2f}".format(1000000*t.meanTime())
#            line += " " + str(t.meanTime())
        print line
            
    def histograms(self):
        return self.histogramList
        
