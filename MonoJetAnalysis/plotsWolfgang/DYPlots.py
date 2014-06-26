import ROOT
import math
import time
from PlotsBase import *
from EventHelper import EventHelper
from LeptonUtilities import *
#from KinematicUtilities import *

# from viewWs import viewWs

def floatEqual(a,b):
    tolerance = 1.e-6
    if a==0 and b==0:
        return True
    return abs(a-b)/(a+b)<tolerance

class DYPlots(PlotsBase):

    def __init__(self,name,preselection=None,elist=None,elistBase="./elists",rebin=None):
        PlotsBase.__init__(self,name,preselection,elist=elist,elistBase=elistBase,rebin=rebin)
        self.leptonPrefixCap = "Mu"
        self.histogramList = { }
        curdir = ROOT.gDirectory
        if not ROOT.gROOT.Get(name):
            ROOT.gROOT.mkdir(name)
        ROOT.gROOT.cd(name)


#        self.charges = [ "Minus", "Plus" ]
        self.charges = [ "" ]
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
            self.addVariable("zm"+sign,100,0.,500.,'b')
            self.addVariable("zpt"+sign,100,0.,1000.,'b')
            self.addVariable("zeta"+sign,50,0.,5.,'b')
            self.addVariable("mt"+sign,50,0.,200.,'u')
            for i in range(2):
                self.addVariable("hardMu"+str(i)+"Pt"+sign,100,0.,500.,'b')
                self.addVariable("hardMu"+str(i)+"Eta"+sign,60,0.,3.,'b')
                self.addVariable("hardMu"+str(i)+"RelIso"+sign,100,0.,0.25,'b')
                self.addVariable("hardMu"+str(i)+"Dxy"+sign,150,0.,0.15,'b')
            self.addVariable("soft"+self.leptonPrefixCap+"Pt"+sign,100,0.,250.,'u')
            self.addVariable("soft"+self.leptonPrefixCap+"Eta"+sign,60,0.,3.,'u')
            self.addVariable("soft"+self.leptonPrefixCap+"RelIso"+sign,100,0.,10.,'u')
            self.addVariable("soft"+self.leptonPrefixCap+"Iso"+sign,100,0.,1000.,'u')
            self.addVariable("soft"+self.leptonPrefixCap+"Dxy"+sign,150,0.,0.15,'u')

            self.addVariablePair("isrJetPt",100,0.,1000.,"thirdMuon",2,-0.5,1.5,suffix=sign)
            self.addVariablePair("njet60",10,-0.5,9.5,"thirdMuon",2,-0.5,1.5,suffix=sign)
            self.addVariablePair("njet",20,-0.5,19.5,"thirdMuon",2,-0.5,1.5,suffix=sign)
            self.addVariablePair("zpt",100,0.,1000.,"thirdMuon",2,-0.5,1.5,suffix=sign)

        curdir.cd()

    def fill(self,eh,downscale=1):

        isrJetPt = eh.get("isrJetPt")
        if math.isnan(isrJetPt):
            return

        imu0,imu1 = diMuon(eh)
        if imu0==None:
            return

        mupts = eh.get("muPt")
        muetas = eh.get("muEta")
        muphis = eh.get("muPhi")
        murelisos = eh.get("muRelIso")
        mu0p4 = ROOT.TLorentzVector()
        mu0p4.SetPtEtaPhiM(mupts[imu0],muetas[imu0],muphis[imu0],0.105)
        mu1p4 = ROOT.TLorentzVector()
        mu1p4.SetPtEtaPhiM(mupts[imu1],muetas[imu1],muphis[imu1],0.105)
        zp4 = mu0p4 + mu1p4
        zpt = (mu0p4+mu1p4).Pt()
        if zpt<200:
            return

        if abs(zp4.M()-91.2)>15:
            return
        njet60 = eh.get("njet60")
        if njet60>2:
            return

#        imusall = isolatedMuons(eh,ptmin=5.,etamax=1.5)
        imusall = range(len(mupts))
        imusother = [ ]
        for i in imusall:
            if i!=imu0 and i!=imu1:
                imusother.append(i)
        imu = None if len(imusother)==0 else imusother[0]
        if imu!=None and ( mupts[imu]<5. or mupts[imu]>20. ):
            return

        met = eh.get("type1phiMet")

        njet = int(eh.get("njetCount")+0.5)
        jetPts = eh.get("jetPt")
        assert len(jetPts)==njet
        ht = eh.get("ht")
        if ht<200:
            return

        pdg = 0
        if len(self.charges)>1 and imu!=None:
            pdg = eh.get("muPdg")[imu]

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

        

        self.timers[0].start()
        if self.name!="data":
            w = eh.get("puWeight")*downscale
        else:
            w = 1
        self.timers[0].stop()        

        mudxys = eh.get("muDxy")
        for i,j in enumerate([imu0,imu1]):
            self.fill1DBySign("hardMu"+str(i)+"Pt",pdg,mupts[j],w)
            self.fill1DBySign("hardMu"+str(i)+"Eta",pdg,abs(muetas[j]),w)
            self.fill1DBySign("hardMu"+str(i)+"RelIso",pdg,murelisos[j],w)
            self.fill1DBySign("hardMu"+str(i)+"Dxy",pdg,mudxys[j],w)

        self.fill1DBySign("isrJetPt",pdg,isrJetPt,w)
        self.fill2DBySign("thirdMuon_vs_isrJetPt",pdg,isrJetPt,float(imu!=None),w)
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
        self.fill1DBySign("njet60",pdg,eh.get("njet60"),w)
        self.fill2DBySign("thirdMuon_vs_njet60",pdg,njet60,float(imu!=None),w)
        self.fill1DBySign("njet",pdg,eh.get("njetCount"),w)
        self.fill2DBySign("thirdMuon_vs_njet",pdg,njet,float(imu!=None),w)

        self.fill1DBySign("met",pdg,met,w)
        self.fill1DBySign("ht",pdg,ht,w)

        self.fill1DBySign("zm",pdg,zp4.M(),w)
        self.fill1DBySign("zpt",pdg,zp4.Pt(),w)
        self.fill1DBySign("zeta",pdg,zp4.Eta(),w)
        self.fill2DBySign("thirdMuon_vs_zpt",pdg,zpt,float(imu!=None),w)

        mt = 0.
        softMuPt = 0.
        if imu!=None:
            softMuPt = mupts[imu]
            softMuPhi = muphis[imu]
            softMuEta = muetas[imu]
#            metphi = eh.get("type1phiMetphi")
            mt = math.sqrt(2*zp4.Pt()*softMuPt*(1-math.cos(zp4.Phi()-softMuPhi)))
            softMuIso = murelisos[imu]*mupts[imu]
        self.fill1DBySign("mt",pdg,mt,w)
        self.fill1DBySign("softMuPt",pdg,softMuPt,w)
        if imu!=None:
            self.fill1DBySign("softMuEta",pdg,abs(softMuEta),w)
            if softMuPt<25.:
                self.fill1DBySign("softMuIso",pdg,softMuIso,w)
            else:
                self.fill1DBySign("softMuRelIso",pdg,murelisos[imu],w)
            self.fill1DBySign("softMuDxy",pdg,mudxys[imu],w)


    def showTimers(self):
        line = ""
        for t in self.timers:
            line += "{0:14.2f}".format(1000000*t.meanTime())
#            line += " " + str(t.meanTime())
        print line
            
    def histograms(self):
        return self.histogramList
        
