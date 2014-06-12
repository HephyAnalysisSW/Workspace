import ROOT
import math
import time
from PlotsBase import *
from EventHelper import EventHelper
from LeptonUtilities import *
from KinematicUtilities import *

# from viewWs import viewWs

def floatEqual(a,b):
    tolerance = 1.e-6
    if a==0 and b==0:
        return True
    return abs(a-b)/(a+b)<tolerance

def getTauToEle(eh):
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

    iele = None
    for i in range(len(gpPdgs)):
        if gpMo1s[i]==itau and abs(gpPdgs[i])==11:
            iele = i
            break

    return [ itau, iele ]

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


class StdPlotsEleBase(PlotsBase):

    def __init__(self,name,preselection=None,elist=None,elistBase="./elists",rebin=None,hardElectron=False):
        PlotsBase.__init__(self,name,preselection,elist=elist,elistBase=elistBase,rebin=rebin)
        self.hardElectron = hardElectron
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
            if self.hardElectron:
                self.addVariable("softElePt"+sign,100,0.,250.,'u')
            else:
                self.addVariable("softElePt"+sign,100,0.,25.,'u')
            self.addVariable("softEleEta"+sign,60,0.,3.,'u')
            self.addVariable("softEleIso"+sign,100,0.,10.,'u')
            self.addVariable("softEleDxy"+sign,100,0.,0.1,'u')
            self.addVariable("softEleDz"+sign,100,0.,0.2,'u')
            self.addVariable("npv"+sign,100,0.,100.,'u')
            self.addVariable("jeteleDeltaEta"+sign,50,0.,10.,'l')
            self.addVariable("jeteleDeltaPhi"+sign,50,0.,10.,'l')
            self.addVariable("jeteleDeltaR"+sign,50,0.,10.,'l')
            self.addVariable("mlb"+sign,20,0.,100.,'u')
            self.addVariable("drlb"+sign,20,0.,10.,'u')
            if self.hardElectron:
                self.addVariable("btag1Pt"+sign,50,0.,1000.,'u')
            else:
                self.addVariable("btag1Pt"+sign,50,0.,250.,'u')
            self.addVariable("btag1Eta"+sign,50,0.,2.5,'u')
#            self.addVariable("drEleGenReco"+sign,500,0.,10.,'u')
#            self.addVariable("ptRatioEleGenReco"+sign,500,0.,2.,'u')
            self.addVariable("ptTau"+sign,100,0.,50.,'u')
            self.addVariable("deltaPhiEleTau"+sign,100,-pi,pi,'b')
            self.addVariable("etaW"+sign,125,0,2.5,'l')
            self.addVariable("costhPol"+sign,100,-1,1,'u')
            self.addVariable("phiPol"+sign,100,0,pi/2,'u')
            if self.hardElectron:
                self.addVariablePair("ptGenTau",50,0.,1000.,"ptGenEle",25,0.,250.,suffix=sign)
            else:
                self.addVariablePair("ptGenTau",50,0.,100.,"ptGenEle",25,0.,25.,suffix=sign)
            self.addVariablePair("mt",25,0.,200.,"ht",40,0.,1000.,suffix=sign)
            self.addVariablePair("met",40,0.,1000.,"ht",40,0.,1000.,suffix=sign)
            self.addVariablePair("met",40,0.,1000.,"elePt",40,0.,1000.,suffix=sign)
            self.addVariablePair("WPt",40,0.,1000.,"met",40,0.,1000.,suffix=sign)
            self.addVariablePair("WPt",40,0.,1000.,"elePt",40,0.,1000.,suffix=sign)

        curdir.cd()

    def fill(self,eh,downscale=1):

        isrJetPt = eh.get("isrJetPt")
        if math.isnan(isrJetPt):
            return

        iele = hardestIsolatedElectron(eh,ptmin=5.,etamax=1.5)
        if iele==None:
            return

        softElePt = eh.get("elPt")[iele]
        if self.hardElectron:
            if softElePt<30:
                return
        else:
            if softElePt>20:
                return

#        if isrJetPt<350:
#            return

        met = eh.get("type1phiMet")
#        if met<300:
#            return

        softEleEta = eh.get("elEta")[iele]
        if abs(softEleEta)>1.5:
            return

        njet = int(eh.get("njetCount")+0.5)
        jetPts = eh.get("jetPt")
        assert len(jetPts)==njet
        ht = eh.get("ht")

#        if met<300 or ht<400:
#            return

#        if self.hardElectron:
#            softEleDxy = eh.get("elDxy")[iele]
#            softEleDz = eh.get("elDz")[iele]
#        else:
#            softEleDxy = eh.get("softIsolatedEleDxy")
#            softEleDz = eh.get("softIsolatedEleDz")
#        if abs(softEleDxy)>0.006 or abs(softEleDz)>0.012:
#            return

        pdg = eh.get("elPdg")[iele]
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
        
        softElePhi = eh.get("elPhi")[iele]
        metphi = eh.get("type1phiMetphi")
        mt = math.sqrt(2*met*softElePt*(1-math.cos(metphi-softElePhi)))
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
#        igeneles = [ ]
#        for i,pdg in enumerate(pdgs[:ngp]):
#            if abs(int(pdg))==11:
#                igeneles.append(i)
#        
#        drmin = 9.999
#        dptmin = 0.
#        if igeneles:
#            gpPts = eh.get("gpPt")
#            gpEtas = eh.get("gpEta")
#            gpPhis = eh.get("gpPhi")
#            for i in igeneles:
#                dr = deltaR(softElePhi,softEleEta,gpPhis[i],gpEtas[i])
#                if dr<drmin:
#                    drmin = dr
#                    dptmin = softElePt/gpPts[i]
#        
#        self.fill1DBySign("drEleGenReco",pdg,drmin,w)
#        self.fill1DBySign("ptRatioEleGenReco",pdg,dptmin,w)
#        if drmin>0.1 or abs(dptmin-1)>0.1:
#            return

        npv = eh.get("ngoodVertices")
        self.fill1DBySign("npv",pdg,npv,w)

        softEleIso = eh.get("elRelIso")[iele]*softElePt
        softEleDxy = eh.get("elDxy")[iele]
        softEleDz = eh.get("elDz")[iele]
        self.fill1DBySign("softEleIso",pdg,softEleIso,w)
        self.fill1DBySign("softEleDxy",pdg,softEleDxy,w)
        self.fill1DBySign("softEleDz",pdg,softEleDz,w)

        self.fill2DBySign("ht_vs_met",pdg,met,ht,w)
        self.fill2DBySign("elePt_vs_met",pdg,met,softElePt,w)

        wPx = softElePt*math.cos(softElePhi) + met*math.cos(metphi)
        wPy = softElePt*math.sin(softElePhi) + met*math.sin(metphi)
        wPt = math.sqrt(wPx**2+wPy**2)
        self.fill2DBySign("met_vs_WPt",pdg,wPt,met,w)
        self.fill2DBySign("elePt_vs_WPt",pdg,wPt,softElePt,w)

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

        self.fill1DBySign("softElePt",pdg,softElePt,w)
        self.fill1DBySign("softEleEta",pdg,abs(softEleEta),w)
           
        p4ele = ROOT.TLorentzVector()
        p4ele.SetPtEtaPhiM(softElePt,softEleEta,softElePhi,0.0005)

        jetPhis = eh.get("jetPhi")
        if ib!=None:
            p4b = ROOT.TLorentzVector()
            p4b.SetPtEtaPhiM(jetPts[ib],jetEtas[ib],jetPhis[ib],5.)
            self.fill1DBySign("mlb",pdg,(p4ele+p4b).M(),w)
            self.fill1DBySign("drlb",pdg,p4ele.DeltaR(p4b),w)

        self.fill1DBySign("jeteleDeltaEta",pdg,abs(jetEtas[0]-softEleEta),w)
        self.fill1DBySign("jeteleDeltaPhi",pdg,deltaPhi(jetPhis[0],softElePhi),w)
        self.fill1DBySign("jeteleDeltaR",pdg,deltaR(jetPhis[0],jetEtas[0],softElePhi,softEleEta),w)

#        if self.name.startswith("WJets") and self.name.endswith("NoTau"):
#            print self.name
#            print deltaR(jetPhis[0],jetEtas[0],softElePhi,softEleEta),deltaPhi(jetPhis[0],softElePhi)
#            tree = viewWs(eh)
#            tree.append( ( -1, 0, jetPts[0], jetPhis[0], jetEtas[0] ) )
#            drawWs(eh,tree)

        ws = wSolutions(met,metphi,softElePt,softElePhi,softEleEta)
        ws.sort(key=lambda x: abs(x.Eta()))
        self.fill1DBySign("etaW",pdg,abs(ws[0].Eta()),w)
        toPolFrame(ws[0],p4ele)
        if self.name.startswith("WJets"):
            itau, iele = getTauToEle(eh)
            if itau!=None:
                gpPts = eh.get("gpPt")
                if iele!=None:
                    self.fill2DBySign("ptGenEle_vs_ptGenTau",pdg,gpPts[itau],gpPts[iele],w)
                    gpPhis = eh.get("gpPhi")
                    self.fill1DBySign("deltaPhiEleTau",pdg,deltaPhi(gpPhis[itau],gpPhis[iele]),w)
                else:
                    self.fill2DBySign("ptGenEle_vs_ptGenTau",pdg,gpPts[itau],0.,w)

        p4elePol = toPolFrame(ws[0],p4ele)
        self.fill1DBySign("costhPol",pdg,p4elePol.Pz()/p4elePol.P(),w)
        self.fill1DBySign("phiPol",pdg,abs(abs(p4elePol.Phi())-pi),w)
#        p4ele = ROOT.TLorentzVector()
#        p4ele.SetPtEtaPhiM(softElePt,softEleEta,softElePhi,0.0005)
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
        
