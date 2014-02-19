import ROOT
from math import *

class DrawWithFOM:

    def __init__(self):
        self.systematics = 0.05
        
    def ssqrtb(self,h1,h2,scut,syst=0.):
        hr = h1.Clone(h1.GetName()+"R")
        hr.Reset()
        if(scut=="u"): 
            i1,i2,i3,ioff = 1,h1.GetNbinsX(),1,1
        elif(scut=="l"): 
            i1,i2,i3,ioff = h1.GetNbinsX()-1,0,-1,0
        s, b = 0, 0
        es, eb = 0, 0
        if h2.InheritsFrom(ROOT.THStack.Class()):
            hsum = h2.GetStack().Last().Clone()
        else:
            hsum = h2.Clone()
        lastFOM = None
        show = h1.GetName().find("njet60")>-1
        for i in range(i1,i2,i3):
            s += h1.GetBinContent(i)
            es += h1.GetBinError(i)**2
            b += hsum.GetBinContent(i)
            eb += hsum.GetBinError(i)**2
            if b>1.e-9:
                if syst<1.e-9:
                    hr.SetBinContent(i+ioff,s/sqrt(b))
                else:
                    hr.SetBinContent(i+ioff,s/sqrt(b+pow(syst*b,2)))
                lastFOM =  hr.GetBinContent(i+ioff)
#                hr.SetBinContent(i+ioff,s/b)
#                hr.SetBinError(i+ioff,sqrt(es**2+(eb*s/b)**2)/b)
        print "***",hr.GetName()," total SSQRTB = ",lastFOM
        print h1.GetSumOfWeights(),hsum.GetSumOfWeights()
        return hr

    def sb(self,h1,h2,scut,syst=0.):
        hr = h1.Clone(h1.GetName()+"R")
        hr.Reset()
        if(scut=="u"): 
            i1,i2,i3,ioff = 1,h1.GetNbinsX(),1,1
        elif(scut=="l"): 
            i1,i2,i3,ioff = h1.GetNbinsX()-1,0,-1,0
        elif(scut=="b"): 
            i1,i2,i3,ioff = 1,h1.GetNbinsX(),1,0
        s, b = 0, 0
        es, eb = 0, 0
        if h2.InheritsFrom(ROOT.THStack.Class()):
            hsum = h2.GetStack().Last().Clone()
        else:
            hsum = h2.Clone()
        lastFOM = None
        show = h1.GetName().find("njet60")>-1
        for i in range(i1,i2,i3):
            if scut=="b":
                s = 0
                es = 0
                b = 0
                eb = 0
            s += h1.GetBinContent(i)
            es += h1.GetBinError(i)**2
            b += hsum.GetBinContent(i)
            eb += hsum.GetBinError(i)**2
            if b>1.e-9:
                hr.SetBinContent(i+ioff,s/b)
                lastFOM =  hr.GetBinContent(i+ioff)
#                hr.SetBinContent(i+ioff,s/b)
#                hr.SetBinError(i+ioff,sqrt(es**2+(eb*s/b)**2)/b)
        print "***",hr.GetName()," total SoB = ",lastFOM
        print h1.GetSumOfWeights(),hsum.GetSumOfWeights()
        return hr

    def drawStack(self, samples, histograms, pad=None):

        if pad!=None:
            pad.cd()

        bkgs = None
        sigs = [ ]
        legend = ROOT.TLegend(0.60,0.75,0.90,0.99)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        for i,s in enumerate(samples):
            h = histograms[i]
            if s.fill:
                h.SetFillStyle(1001)
                h.SetFillColor(s.color)
            else:
                h.SetLineColor(s.color)
                h.SetLineWidth(3)
            if s.isBackground():
                if bkgs==None:
                    print "Defining background ",s.name,h.GetName()
                    bkgs = ROOT.THStack()
                    bkgs.SetNameTitle(h.GetName(),h.GetTitle())
                opt = "hist "
                if s.fill:
                    opt += "F"
                print s.name,h.GetName(),opt
                bkgs.Add(h,opt)
                print "Adding to background ",s.name,h.GetName(),opt
                if s.name.startswith("W"):
                    print s.name," contents ",h.GetSumOfWeights()
            elif s.isSignal():
                sigs.append(h)
                print "Adding to signal ",s.name,h.GetName()
            if s.fill:
                opt = "F"
            else:
                opt = "L"
            if bkgs!=None:
                bkgs.SetMinimum(0.1)
            legend.AddEntry(h,s.name,opt)       

        bkgs.Draw()
        bkgs.GetYaxis().SetTitle("Events / bin")
        for s in sigs:
            s.Draw("same hist")
        legend.Draw()
        legend.SetBit(ROOT.kCanDelete)
#        ROOT.gPad.SetLogy(1)

        return ( bkgs, sigs , legend )

    def drawSoSqrtB(self, bkgs, sigs, scut='l', pad=None):

        assert bkgs!=None

#        cnv = ROOT.TCanvas(bkgs.GetName(),bkgs.GetName(),700,700)

#        p1 = ROOT.TPad("p1","", 0, 0.28, 1, 0.95)
#        p1.SetTopMargin(1e-7)
#        p1.Draw()
#        p2 = ROOT.TPad("p2","", 0, 0, 1, 0.3)
#        p2.SetTopMargin(1e-7)
#        p2.Draw()

#        p1.cd()
#        bkgs.Draw()
#        bkgs.GetYaxis().SetTitle("Events / bin")
#        for s in sigs:
#            s.Draw("same hist")
#        p1.SetLogy(1)

        if pad!=None:
            pad.cd()

        opt = ""
        hrs = [ ]
        hrmax = 0.
        for s in sigs:
            hr = self.ssqrtb(s,bkgs,scut,0.05)
            hrs.append(hr)
            if hr.GetMaximum()>hrmax:
                hrmax = hr.GetMaximum()
            if opt=="":
                hr.GetYaxis().SetTitle("S/B")
                hr.GetYaxis().SetTitleSize(0.08)
            hr.DrawCopy(opt+"hist")
            opt = "same "
        if len(hrs)>0:
            hrs[0].SetMaximum(hrmax/0.85)

#        cnv.cd()
#        cnv.Update()
#        return cnv

    def drawSoB(self, bkgs, sigs, scut='l', pad=None):

        assert bkgs!=None

#        cnv = ROOT.TCanvas(bkgs.GetName(),bkgs.GetName(),700,700)

#        p1 = ROOT.TPad("p1","", 0, 0.28, 1, 0.95)
#        p1.SetTopMargin(1e-7)
#        p1.Draw()
#        p2 = ROOT.TPad("p2","", 0, 0, 1, 0.3)
#        p2.SetTopMargin(1e-7)
#        p2.Draw()

#        p1.cd()
#        bkgs.Draw()
#        bkgs.GetYaxis().SetTitle("Events / bin")
#        for s in sigs:
#            s.Draw("same hist")
#        p1.SetLogy(1)

        if pad!=None:
            pad.cd()

        opt = ""
        hrs = [ ]
        hrmax = 0.
        for s in sigs:
            hr = self.sb(s,bkgs,scut)
            hrs.append(hr)
            if hr.GetMaximum()>hrmax:
                hrmax = hr.GetMaximum()
            if opt=="":
                hr.GetYaxis().SetTitle("S/B")
                hr.GetYaxis().SetTitleSize(0.08)
            hr.DrawCopy(opt+"hist")
            opt = "same "
        if len(hrs)>0:
            hrs[0].SetMaximum(hrmax/0.85)

#        cnv.cd()
#        cnv.Update()
#        return cnv
