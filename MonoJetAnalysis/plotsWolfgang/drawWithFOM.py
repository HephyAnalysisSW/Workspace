import ROOT
from math import *

class DrawWithFOM:

    def __init__(self,fom):
        self.systematics = 0.05
        if fom!=None:
            self.fom = fom.lower()
        else:
            self.fom = fom
        
    def getFom(self,h1,h2,scut,syst=0.):
        hr = h1.Clone(h1.GetName()+"R")
        hr.Reset()
        if scut=="u": 
            i1,i2,i3,ioff = 1,h1.GetNbinsX(),1,1
        elif scut=="l": 
            i1,i2,i3,ioff = h1.GetNbinsX()-1,0,-1,0
        elif scut=="b": 
            i1,i2,i3,ioff = 1,h1.GetNbinsX(),1,0
        s, b, es, eb = [ 0 ]*4
        if h2.InheritsFrom(ROOT.THStack.Class()):
            hsum = h2.GetStack().Last().Clone()
        else:
            hsum = h2.Clone()
        lastFOM = None
        show = h1.GetName().find("njet60")>-1
        for i in range(i1,i2,i3):
            if scut=="b":
                s, b, es, eb = [ 0 ]*4
            s += h1.GetBinContent(i)
            es += h1.GetBinError(i)**2
            b += hsum.GetBinContent(i)
            eb += hsum.GetBinError(i)**2
            fom = None
            if b>1.e-9:
                if self.fom=="sob":
                    fom = s/b
                elif self.fom=="sosqrtb":
                    if syst<1.e-9:
                        fom = s/sqrt(b)
                    else:
                        fom = s/sqrt(b+pow(syst*b,2))
            if fom!=None:
                hr.SetBinContent(i+ioff,fom)
                lastFOM = fom
#                hr.SetBinContent(i+ioff,s/b)
#                hr.SetBinError(i+ioff,sqrt(es**2+(eb*s/b)**2)/b)

        btot, ebtot = 0, 0
        stot, estot = 0, 0
        for i in range(h1.GetNbinsX()+2):
            btot += hsum.GetBinContent(i)
            ebtot += hsum.GetBinError(i)**2
            stot += h1.GetBinContent(i)
            estot += h1.GetBinError(i)**2
        ebtot = sqrt(ebtot)
        estot = sqrt(estot)
        line = "*** "+hr.GetName().ljust(20)
#        line += " s,b {0:7.2f} {1:7.2f}".format(h1.GetSumOfWeights(),hsum.GetSumOfWeights())
        line += " s {0:7.2f} +- {1:5.2f}".format(stot,estot)
        line += " b {0:7.2f} +- {1:5.2f}".format(btot,ebtot)
        if lastFOM!=None:
            line += " total "+self.fom+" = {0:7.3f}".format(lastFOM)
        print line
#        print h1.GetSumOfWeights(),hsum.GetSumOfWeights()
        return hr


    def drawStack1D(self, samples, histograms, pad=None):

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
#                    print "Defining background ",s.name,h.GetName()
                    bkgs = ROOT.THStack()
                    bkgs.SetNameTitle(h.GetName(),h.GetTitle())
                opt = "hist "
                if s.fill:
                    opt += "F"
#                print s.name,h.GetName(),opt
                bkgs.Add(h,opt)
#                print "Adding to background ",s.name,h.GetName(),opt
#                if s.name.startswith("W"):
#                    print s.name," contents ",h.GetSumOfWeights()
            elif s.isSignal():
                sigs.append(h)
#                print "Adding to signal ",s.name,h.GetName()
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

        if pad!=None:
            pad.Update()

        return ( bkgs, sigs , legend )

    def drawStack2D(self, samples, histograms, pad=None):

        if pad!=None:
            pad.cd()

        bkgs = None
        sigs = [ ]
        legend = ROOT.TLegend(0.60,0.75,0.90,0.89)
        legend.SetBorderSize(0)
        legend.SetFillColor(10)
#        legend.SetFillStyle(0)
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
#                    print "Defining background ",s.name,h.GetName()
                    bkgs = h.Clone()
                    print "Cloning bkg histo from ",s.name,h.GetName()
                    legend.AddEntry(bkgs,"Backgrounds","")
                else:
                    bkgs.Add(h)
                    print "Adding bkg histo for ",s.name,h.GetName()
#                legend.SetHeader("Backgrounds")
            elif s.isSignal():
                h.SetLineColor(s.color)
                h.SetLineWidth(1)
                sigs.append(h)
                legend.AddEntry(h,s.name,"L")
                print "Sig histo from ",s.name,h.GetName()
#                print "Adding to signal ",s.name,h.GetName()
#            if s.fill:
#                opt = "F"
#            else:
#                opt = "L"

        bkgmax = bkgs.GetMaximum()
        bkgs.SetMaximum(bkgmax/0.85)
        bkgs.SetMinimum(0.1)
        print "bkgmax = ",bkgmax
        bkgs.Draw("zcol")
#        bkgs.GetYaxis().SetTitle("Events / bin")
        for s in sigs:
#            s.SetMaximum(bkgmax/0.85)
#            s.SetMinimum(0.1)
            s.SetContour(3)
            s.Draw("cont3 same")
        legend.Draw()
        legend.SetBit(ROOT.kCanDelete)
#        ROOT.gPad.SetLogy(1)

        if pad!=None:
            pad.Update()

        return ( bkgs, sigs , legend )

    def drawFom(self, bkgs, sigs, scut='l', pad=None):

        if self.fom==None:
            return

        assert bkgs!=None

        if pad!=None:
            pad.cd()

        opt = ""
        hrs = [ ]
        hrmax = 0.
        for s in sigs:
            hr = self.getFom(s,bkgs,scut,self.systematics)
#            hrs.append(hr)
            if hr.GetMaximum()>hrmax:
                hrmax = hr.GetMaximum()
            if opt=="":
                hr.GetYaxis().SetTitle("S/B")
                hr.GetYaxis().SetTitleSize(0.08)
            hrs.append(hr.DrawCopy(opt+"hist"))
            opt = "same "
        if len(hrs)>0:
            hrs[0].SetMaximum(hrmax/0.85)

        pad.Update()
