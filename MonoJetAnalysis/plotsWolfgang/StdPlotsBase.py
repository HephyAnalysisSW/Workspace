import ROOT
import math
import time
from PlotsBase import *
from EventHelper import EventHelper
from LeptonUtilities import *
from KinematicUtilities import *
from PreselectionTools import *

# from viewWs import viewWs

def floatEqual(a,b):
    tolerance = 1.e-6
    if a==0 and b==0:
        return True
    return abs(a-b)/(a+b)<tolerance

def getTauToEorMu(eh,pdgDaughter):
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

    ilep = None
    for i in range(len(gpPdgs)):
        if gpMo1s[i]==itau and abs(gpPdgs[i])==pdgDaughter:
            ilep = i
            break

    return [ itau, ilep ]

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

    def __init__(self,name,preselection=None,elist=None,elistBase="./elists",rebin=None,leptonPdg=13,hardLepton=False):
        PlotsBase.__init__(self,name,preselection,elist=elist,elistBase=elistBase,rebin=rebin)
        assert leptonPdg==11 or leptonPdg==13
        self.leptonPdg = leptonPdg
        if leptonPdg==11:
            self.leptonPrefix = "el"
            self.leptonMass = 0.000511
        else:
            self.leptonPrefix = "mu"
            self.leptonMass = 0.105
        self.leptonPrefixCap = self.leptonPrefix.capitalize()
        self.hardLepton = hardLepton
        self.histogramList = { }
        curdir = ROOT.gDirectory
        if not ROOT.gROOT.Get(name):
            ROOT.gROOT.mkdir(name)
        ROOT.gROOT.cd(name)


        self.addVariable("preselection",1,0.,1.,"b")
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
            self.addVariable("nel"+sign,20,-0.5,19.5,'u')
            self.addVariable("nmu"+sign,20,-0.5,19.5,'u')
            self.addVariable("nta"+sign,20,-0.5,19.5,'u')
            self.addVariable("met"+sign,100,0.,1000.,'l')
            self.addVariable("ht"+sign,100,0.,1000.,'l')
            self.addVariable("metHtRatio"+sign,100,0.,2.5,'u')
            self.addVariable("metHtProd"+sign,100,0.,250000.,'l')
            self.addVariable("metIsrPtRatio"+sign,100,0.,5.0,'b')
            self.addVariable("htIsrPtRatio"+sign,100,0.,5.0,'b')
            self.addVariable("mt"+sign,50,0.,200.,'u')
            if self.hardLepton:
                self.addVariable("soft"+self.leptonPrefixCap+"Pt"+sign,100,0.,250.,'u')
            else:
                self.addVariable("soft"+self.leptonPrefixCap+"Pt"+sign,100,0.,25.,'u')
            self.addVariable("soft"+self.leptonPrefixCap+"Eta"+sign,60,0.,3.,'u')
            self.addVariable("soft"+self.leptonPrefixCap+"Iso"+sign,100,0.,10.,'u')
            if self.leptonPdg==13:
                self.addVariable("soft"+self.leptonPrefixCap+"NPix"+sign,10,0.,10.,'u')
                self.addVariable("soft"+self.leptonPrefixCap+"NTk"+sign,20,0.,20.,'u')
            self.addVariable("soft"+self.leptonPrefixCap+"Dxy"+sign,100,0.,0.1,'u')
            self.addVariable("soft"+self.leptonPrefixCap+"Dz"+sign,100,0.,0.2,'u')
            self.addVariable("npv"+sign,100,0.,100.,'u')
            self.addVariable("jet"+self.leptonPrefix+"DeltaEta"+sign,50,0.,10.,'l')
            self.addVariable("jet"+self.leptonPrefix+"DeltaPhi"+sign,50,0.,10.,'l')
            self.addVariable("jet"+self.leptonPrefix+"DeltaR"+sign,50,0.,10.,'l')
            self.addVariable("mlb"+sign,20,0.,100.,'u')
            self.addVariable("drlb"+sign,20,0.,10.,'u')
            if self.hardLepton:
                self.addVariable("btag1Pt"+sign,50,0.,1000.,'u')
            else:
                self.addVariable("btag1Pt"+sign,50,0.,250.,'u')
            self.addVariable("btag1Eta"+sign,50,0.,2.5,'u')
#            self.addVariable("dr"+self.leptonPrefixCap+"GenReco"+sign,500,0.,10.,'u')
#            self.addVariable("ptRatio"+self.leptonPrefixCap+"GenReco"+sign,500,0.,2.,'u')
            self.addVariable("ptTau"+sign,100,0.,50.,'u')
            self.addVariable("deltaPhi"+self.leptonPrefixCap+"Tau"+sign,100,-pi,pi,'b')
            self.addVariable("etaW"+sign,125,0,2.5,'l')
            self.addVariable("costhPol"+sign,100,-1,1,'u')
            self.addVariable("phiPol"+sign,100,0,pi/2,'u')
            self.addVariable("regionIndex"+sign,9,-1.,8.,'b')

            if self.hardLepton:
                self.addVariablePair("ptGenTau",50,0.,1000.,"ptGen"+self.leptonPrefixCap+"",25,0.,250.,suffix=sign)
            else:
                self.addVariablePair("ptGenTau",50,0.,100.,"ptGen"+self.leptonPrefixCap+"",25,0.,25.,suffix=sign)
            self.addVariablePair("mt",25,0.,200.,"ht",40,0.,1000.,suffix=sign)
            self.addVariablePair("met",40,0.,1000.,"ht",40,0.,1000.,suffix=sign)
            self.addVariablePair("met",40,0.,1000.,self.leptonPrefix+"Pt",40,0.,1000.,suffix=sign)
            self.addVariablePair("WPt",40,0.,1000.,"met",40,0.,1000.,suffix=sign)
            self.addVariablePair("WPt",40,0.,1000.,self.leptonPrefix+"Pt",40,0.,1000.,suffix=sign)

        curdir.cd()

    def fill(self,eh,downscale=1):

        self.timers[0].start()
        if self.name!="data":
            w = eh.get("puWeight")*downscale
        else:
            w = 1
        self.timers[0].stop()
        self.fill1DBySign("preselection",0.,0.,w)
#        if self.name=="data":
#            print "Preselected ",int(eh.get("run")),int(eh.get("lumi")),eh.get("event")

        isrJetPt = eh.get("isrJetPt")
        if math.isnan(isrJetPt):
            return

        if self.leptonPdg==11:
            ilep = hardestIsolatedElectron(eh,ptmin=7.,etamax=1.5)
        else:
            ilep = hardestIsolatedMuon(eh,ptmin=5.,etamax=1.5)
        if ilep==None:
            return

        softLepPt = eh.get(self.leptonPrefix+"Pt")[ilep]
        if self.hardLepton:
            if softLepPt<30:
                return
        else:
            if softLepPt>20:
                return

#        if isrJetPt<350:
#            return

        met = eh.get("type1phiMet")
#        if met<300:
#            return

        softLepEta = eh.get(self.leptonPrefix+"Eta")[ilep]
        if abs(softLepEta)>1.5:
            return

        njet = int(eh.get("njetCount")+0.5)
        jetPts = eh.get("jetPt")
        assert len(jetPts)==njet
        ht = eh.get("ht")

#        if met<300 or ht<400:
#            return

#        if self.hardLepton:
#            softLepDxy = eh.get(self.leptonPrefix+"Dxy")[ilep]
#            softLepDz = eh.get(self.leptonPrefix+"Dz")[ilep]
#        else:
#            softLepDxy = eh.get("softIsolated"+self.leptonPrefixCap+"Dxy")
#            softLepDz = eh.get("softIsolated"+self.leptonPrefixCap+"Dz")
#        if abs(softLepDxy)>0.006 or abs(softLepDz)>0.012:
#            return

        pdg = eh.get(self.leptonPrefix+"Pdg")[ilep]
        if len(self.charges)==1:
            pdg = 0

        jetEtas = eh.get("jetEta")
        jetBtags = eh.get("jetBtag")
        ib = None
        nb = 0
        nbs = 0
        for i in range(njet):
#            if jetPts[i]>30 and jetPts[i]<60 and jetBtags[i]>0.679:
            if jetPts[i]>30 and abs(jetEtas[i])<2.4 and jetBtags[i]>0.679:
                if ib==None:
                    ib = i
                nb += 1
                if jetPts[i]<60:
                    nbs += 1
        if ib!=None:
            return
        
        softLepPhi = eh.get(self.leptonPrefix+"Phi")[ilep]
        metphi = eh.get("type1phiMetphi")
        mt = math.sqrt(2*met*softLepPt*(1-math.cos(metphi-softLepPhi)))
        if self.leptonPdg==13:
            assert floatEqual(mt,eh.get(self.leptonPrefix+"MT")[ilep])
#        if mt<60 or mt>88:
#            return

        region = -1
        sr = signalRegion(eh,ilep,self.leptonPrefix)
        if self.name=="data" and sr!=None:
            return

        
        if sr!=None:
            region = regionIndices[sr]
        else:
            cr = controlRegion(eh,ilep,self.leptonPrefix)
            if cr!=None:
                region = regionIndices[cr]
        self.fill1DBySign("regionIndex",pdg,region,w)

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
#                dr = deltaR(softLepPhi,softLepEta,gpPhis[i],gpEtas[i])
#                if dr<drmin:
#                    drmin = dr
#                    dptmin = softLepPt/gpPts[i]
#        
#        self.fill1DBySign("drMuGenReco",pdg,drmin,w)
#        self.fill1DBySign("ptRatioMuGenReco",pdg,dptmin,w)
#        if drmin>0.1 or abs(dptmin-1)>0.1:
#            return

        npv = eh.get("ngoodVertices")
        self.fill1DBySign("npv",pdg,npv,w)

        softLepIso = eh.get(self.leptonPrefix+"RelIso")[ilep]*softLepPt
        softLepDxy = eh.get(self.leptonPrefix+"Dxy")[ilep]
        softLepDz = eh.get(self.leptonPrefix+"Dz")[ilep]
        self.fill1DBySign("soft"+self.leptonPrefixCap+"Iso",pdg,softLepIso,w)
        self.fill1DBySign("soft"+self.leptonPrefixCap+"Dxy",pdg,softLepDxy,w)
        self.fill1DBySign("soft"+self.leptonPrefixCap+"Dz",pdg,softLepDz,w)
        if self.leptonPdg==13:
            softLepNPix = eh.get(self.leptonPrefix+"PixelHits")[ilep]
            softLepNTk = eh.get(self.leptonPrefix+"NumtrackerLayerWithMeasurement")[ilep]
            self.fill1DBySign("soft"+self.leptonPrefixCap+"NPix",pdg,softLepNPix,w)
            self.fill1DBySign("soft"+self.leptonPrefixCap+"NTk",pdg,softLepNTk,w)

        self.fill1DBySign("metHtRatio",pdg,met/ht,w)
        self.fill1DBySign("metHtProd",pdg,met*ht,w)
        self.fill2DBySign("ht_vs_met",pdg,met,ht,w)
        self.fill2DBySign(self.leptonPrefix+"Pt_vs_met",pdg,met,softLepPt,w)

        wPx = softLepPt*math.cos(softLepPhi) + met*math.cos(metphi)
        wPy = softLepPt*math.sin(softLepPhi) + met*math.sin(metphi)
        wPt = math.sqrt(wPx**2+wPy**2)
        self.fill2DBySign("met_vs_WPt",pdg,wPt,met,w)
        self.fill2DBySign(self.leptonPrefix+"Pt_vs_WPt",pdg,wPt,softLepPt,w)

        self.fill1DBySign("ht",pdg,ht,w)
        self.fill1DBySign("mt",pdg,mt,w)
        self.fill2DBySign("ht_vs_mt",pdg,mt,ht,w)
        
        self.fill1DBySign("isrJetPt",pdg,isrJetPt,w)
        self.fill1DBySign("isrJetEta",pdg,abs(eh.get("isrJetEta")),w)

        self.fill1DBySign("metIsrPtRatio",pdg,met/isrJetPt,w)
        self.fill1DBySign("htIsrPtRatio",pdg,ht/isrJetPt,w)

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

        self.fill1DBySign("nel",pdg,eh.get("nel"),w)
        self.fill1DBySign("nmu",pdg,eh.get("nmu"),w)
        self.fill1DBySign("nta",pdg,eh.get("nta"),w)

        self.fill1DBySign("met",pdg,met,w)

        self.fill1DBySign("soft"+self.leptonPrefixCap+"Pt",pdg,softLepPt,w)
        self.fill1DBySign("soft"+self.leptonPrefixCap+"Eta",pdg,abs(softLepEta),w)
           
        p4lep = ROOT.TLorentzVector()
        p4lep.SetPtEtaPhiM(softLepPt,softLepEta,softLepPhi,self.leptonMass)

        jetPhis = eh.get("jetPhi")
        if ib!=None:
            p4b = ROOT.TLorentzVector()
            p4b.SetPtEtaPhiM(jetPts[ib],jetEtas[ib],jetPhis[ib],5.)
            self.fill1DBySign("mlb",pdg,(p4lep+p4b).M(),w)
            self.fill1DBySign("drlb",pdg,p4lep.DeltaR(p4b),w)

        self.fill1DBySign("jet"+self.leptonPrefix+"DeltaEta",pdg,abs(jetEtas[0]-softLepEta),w)
        self.fill1DBySign("jet"+self.leptonPrefix+"DeltaPhi",pdg,deltaPhi(jetPhis[0],softLepPhi),w)
        self.fill1DBySign("jet"+self.leptonPrefix+"DeltaR",pdg,deltaR(jetPhis[0],jetEtas[0],softLepPhi,softLepEta),w)

#        if self.name.startswith("WJets") and self.name.endswith("NoTau"):
#            print self.name
#            print deltaR(jetPhis[0],jetEtas[0],softLepPhi,softLepEta),deltaPhi(jetPhis[0],softLepPhi)
#            tree = viewWs(eh)
#            tree.append( ( -1, 0, jetPts[0], jetPhis[0], jetEtas[0] ) )
#            drawWs(eh,tree)

        ws = wSolutions(met,metphi,softLepPt,softLepPhi,softLepEta)
        ws.sort(key=lambda x: abs(x.Eta()))
        self.fill1DBySign("etaW",pdg,abs(ws[0].Eta()),w)
        toPolFrame(ws[0],p4lep)
        if self.name.startswith("WJets"):
            itau, iltau = getTauToEorMu(eh,self.leptonPdg)
            if itau!=None:
                gpPts = eh.get("gpPt")
                if iltau!=None:
                    self.fill2DBySign("ptGen"+self.leptonPrefixCap+"_vs_ptGenTau",pdg,gpPts[itau],gpPts[iltau],w)
                    gpPhis = eh.get("gpPhi")
                    self.fill1DBySign("deltaPhi"+self.leptonPrefixCap+"Tau",pdg,deltaPhi(gpPhis[itau],gpPhis[iltau]),w)
                else:
                    self.fill2DBySign("ptGen"+self.leptonPrefixCap+"_vs_ptGenTau",pdg,gpPts[itau],0.,w)

        p4lepPol = toPolFrame(ws[0],p4lep)
        self.fill1DBySign("costhPol",pdg,p4lepPol.Pz()/p4lepPol.P(),w)
        self.fill1DBySign("phiPol",pdg,abs(abs(p4lepPol.Phi())-pi),w)
#        p4lep = ROOT.TLorentzVector()
#        p4lep.SetPtEtaPhiM(softLepPt,softLepEta,softLepPhi,self.leptonMass)
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
        
