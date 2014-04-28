import ROOT
import math
import time
from PlotsBase import *
from EventHelper import EventHelper
from LeptonUtilities import *
from KinematicUtilities import *

# from viewWs import viewWs

def getTauToMu(eh):
    gpPdgs = [ int(v) for v in eh.get("gpPdg") ]
    itau = None
    for i,pdg in enumerate(gpPdgs):
        if abs(pdg)==15:
            itau = i
            break
    if itau==None:
        return [ None, None ]

    gpMo1s = [ int(v) for v in eh.get("gpMo1") ]
    if gpMo1s[itau]<0 or abs(gpPdgs[gpMo1s[itau]])!=24:
        return [ None, None ]

    imu = None
    for i in range(len(gpPdgs)):
        if gpMo1s[i]==itau and abs(gpPdgs[i])==13:
            imu = i
            break

    return [ itau, imu ]

#def drawWs(eh,tree):
#    gpPdgs = eh.get("gpPdg")
#    gpPts = eh.get("gpPt")
#    gpPhis = eh.get("gpPhi")
#    gpEtas = eh.get("gpEta")
#    ptmax = 0.
#    for t in tree:
#        i = t[0]
#        l = t[1]
#        if i>=0:
#            pt = gpPts[i]
#        else:
#            pt = t[2] 
#        if pt>ptmax:
#            ptmax = pt

#    cnv = ROOT.TCanvas("viewWs","viewWs",600,600)
#    logptmax = math.log10(ptmax)
#    print "logptmax = ",logptmax
#    cnv.DrawFrame(-1.1*logptmax,-1.1*logptmax,1.1*logptmax,1.1*logptmax)
#    arrows = [ ]
#    paves = [ ]
#    form = '{0:3d} pt={1:5.1f} #eta={2:5.2f} #phi={3:5.2f}'
#    for t in tree:
#        i = t[0]
#        l = t[1]
#        if i>=0:
#            pdg = gpPdgs[i]
#            pt = gpPts[i]
#            phi = gpPhis[i]
#            eta = gpEtas[i]
#        else:
#            pdg = 0
#            pt = t[2]
#            phi = t[3]
#            eta = t[4]
#        px = math.copysign(math.log10(pt)*math.cos(phi),math.cos(phi))
#        py = math.copysign(math.log10(pt)*math.sin(phi),math.sin(phi))
#        arrow = ROOT.TArrow(0.,0.,px,py,0.05) #*gpPts[i]/ptmax)
#        arrow.SetLineWidth(2)
#        arrow.SetLineStyle(l+1)
#        arrow.Draw()
#        arrows.append(arrow)
#        paveCorners = [ -logptmax/20., -logptmax/20., logptmax/20., logptmax/20. ]
#        paveCorners[0] += 1.2*px
#        paveCorners[2] += 1.2*px
#        paveCorners[1] += 1.2*py
#        paveCorners[3] += 1.2*py
#        pave = ROOT.TPaveText(paveCorners[0],paveCorners[1],paveCorners[2],paveCorners[3])
#        pave.SetBorderSize(0)
#        pave.SetTextAlign(22)
#        pave.SetTextSize(0.02)
#        pave.AddText('{0:3d} pt={1:5.1f}'.format(int(pdg),pt))
#        pave.AddText('#eta={0:5.2f} #phi={1:5.2f}'.format(eta,phi))
#        pave.Draw()
#        paves.append(pave)

#    cnv.Update()
#    raw_input("Enter")


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
            self.addVariable("mt"+sign,50,0.,200.,'u')
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
            self.addVariable("jetmuDeltaPhi"+sign,50,0.,10.,'l')
            self.addVariable("jetmuDeltaR"+sign,50,0.,10.,'l')
            self.addVariable("mlb"+sign,20,0.,100.,'u')
            self.addVariable("drlb"+sign,20,0.,10.,'u')
            if self.hardMuon:
                self.addVariable("btag1Pt"+sign,50,0.,1000.,'u')
            else:
                self.addVariable("btag1Pt"+sign,50,0.,250.,'u')
            self.addVariable("btag1Eta"+sign,50,0.,2.5,'u')
#            self.addVariable("drMuGenReco"+sign,500,0.,10.,'u')
#            self.addVariable("ptRatioMuGenReco"+sign,500,0.,2.,'u')
            self.addVariable("ptTau"+sign,100,0.,50.,'u')
            self.addVariable("deltaPhiMuTau"+sign,100,-pi,pi,'b')
            self.addVariable("etaW"+sign,125,0,2.5,'l')
            self.addVariable("costhPol"+sign,100,-1,1,'u')
            self.addVariable("phiPol"+sign,100,0,pi/2,'u')
            if self.hardMuon:
                self.addVariablePair("ptGenTau",50,0.,1000.,"ptGenMu",25,0.,250.,suffix=sign)
            else:
                self.addVariablePair("ptGenTau",50,0.,100.,"ptGenMu",25,0.,25.,suffix=sign)
            self.addVariablePair("mt",25,0.,200.,"ht",40,0.,1000.,suffix=sign)
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
        assert len(jetPts)==njet
        ht = 0
        for i in range(njet):
            if jetPts[i]>30:
                ht += jetPts[i]

#        if met<300 or ht<400:
#            return

#        if self.hardMuon:
#            softMuDxy = eh.get("muDxy")[imu]
#            softMuDz = eh.get("muDz")[imu]
#        else:
#            softMuDxy = eh.get("softIsolatedMuDxy")
#            softMuDz = eh.get("softIsolatedMuDz")
#        if abs(softMuDxy)>0.006 or abs(softMuDz)>0.012:
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
        
#        ngp = int(eh.get("ngp"))
#        pdgs = eh.get("gpPdg")
#        igenmus = [ ]
#        for i,pdg in enumerate(pdgs[:ngp]):
#            if abs(int(pdg))==13:
#                igenmus.append(i)
#        
#        drmin = 9.999
#        dptmin = 0.
#        if igenmus:
#            gpPts = eh.get("gpPt")
#            gpEtas = eh.get("gpEta")
#            gpPhis = eh.get("gpPhi")
#            for i in igenmus:
#                dr = deltaR(softMuPhi,softMuEta,gpPhis[i],gpEtas[i])
#                if dr<drmin:
#                    drmin = dr
#                    dptmin = softMuPt/gpPts[i]
#        
#        self.fill1DBySign("drMuGenReco",pdg,drmin,w)
#        self.fill1DBySign("ptRatioMuGenReco",pdg,dptmin,w)
#        if drmin>0.1 or abs(dptmin-1)>0.1:
#            return

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
        self.fill2DBySign("ht_vs_mt",pdg,mt,ht,w)
        
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
           
        p4mu = ROOT.TLorentzVector()
        p4mu.SetPtEtaPhiM(softMuPt,softMuEta,softMuPhi,0.105)

        jetPhis = eh.get("jetPhi")
        if ib!=None:
            p4b = ROOT.TLorentzVector()
            p4b.SetPtEtaPhiM(jetPts[ib],jetEtas[ib],jetPhis[ib],5.)
            self.fill1DBySign("mlb",pdg,(p4mu+p4b).M(),w)
            self.fill1DBySign("drlb",pdg,p4mu.DeltaR(p4b),w)

        self.fill1DBySign("jetmuDeltaEta",pdg,abs(jetEtas[0]-softMuEta),w)
        self.fill1DBySign("jetmuDeltaPhi",pdg,deltaPhi(jetPhis[0],softMuPhi),w)
        self.fill1DBySign("jetmuDeltaR",pdg,deltaR(jetPhis[0],jetEtas[0],softMuPhi,softMuEta),w)

#        if self.name.startswith("WJets") and self.name.endswith("NoTau"):
#            print self.name
#            print deltaR(jetPhis[0],jetEtas[0],softMuPhi,softMuEta),deltaPhi(jetPhis[0],softMuPhi)
#            tree = viewWs(eh)
#            tree.append( ( -1, 0, jetPts[0], jetPhis[0], jetEtas[0] ) )
#            drawWs(eh,tree)

        ws = wSolutions(met,metphi,softMuPt,softMuPhi,softMuEta)
        ws.sort(key=lambda x: abs(x.Eta()))
        self.fill1DBySign("etaW",pdg,abs(ws[0].Eta()),w)
        toPolFrame(ws[0],p4mu)
        if self.name.startswith("WJets"):
            itau, imu = getTauToMu(eh)
            if itau!=None:
                gpPts = eh.get("gpPt")
                if imu!=None:
                    self.fill2DBySign("ptGenMu_vs_ptGenTau",pdg,gpPts[itau],gpPts[imu],w)
                    gpPhis = eh.get("gpPhi")
                    self.fill1DBySign("deltaPhiMuTau",pdg,deltaPhi(gpPhis[itau],gpPhis[imu]),w)
                else:
                    self.fill2DBySign("ptGenMu_vs_ptGenTau",pdg,gpPts[itau],0.,w)

        p4muPol = toPolFrame(ws[0],p4mu)
        self.fill1DBySign("costhPol",pdg,p4muPol.Pz()/p4muPol.P(),w)
        self.fill1DBySign("phiPol",pdg,abs(abs(p4muPol.Phi())-pi),w)
#        p4mu = ROOT.TLorentzVector()
#        p4mu.SetPtEtaPhiM(softMuPt,softMuEta,softMuPhi,0.105)
#        p4b = ROOT.TLorentzVector()
#        p4b.SetPtEtaPhiM(jetPts[ib],jetEtas[ib],jetPhis[ib],5.)
            

    def showTimers(self):
        line = ""
        for t in self.timers:
            line += "{0:14.2f}".format(1000000*t.meanTime())
#            line += " " + str(t.meanTime())
        print line
            
    def histograms(self):
        return self.histogramList
        
