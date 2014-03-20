import ROOT
import ctypes
from math import *

class DrawWithFOM:

    def __init__(self,options):
        self.systematics = 0.05
        if options.fom!=None:
            self.fom = options.fom.lower()
        else:
            self.fom = options.fom
        
    def getIntegralWithError(self,h):
        sum = 0.
        esum = 0.
        for i in range(h.GetNbinsX()+1):
            sum += h.GetBinContent(i)
            esum += h.GetBinError(i)**2
        return ( sum, sqrt(esum) )
        
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

    def getDoMC(self,h1,h2):
        hr = h1.Clone(h1.GetName()+"DoMC")
        if h2.InheritsFrom(ROOT.THStack.Class()):
            hsum = h2.GetStack().Last().Clone()
        else:
            hsum = h2.Clone()
        hr.Reset()
        for i in range(1,hr.GetNbinsX()+1):
            d = h1.GetBinContent(i)
            ed = h1.GetBinError(i)
            b = hsum.GetBinContent(i)
            eb = hsum.GetBinError(i)
            if b>0:
                hr.SetBinContent(i,d/b)
                hr.SetBinError(i,sqrt((ed)**2+(eb*d/b)**2)/b)
        return hr


    def drawStack1D(self, samples, histograms, pad=None):

        if pad!=None:
            pad.cd()

        data = None
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
                if s.hatch:
                    h.SetFillStyle(s.hatch)
            else:
                h.SetLineColor(s.color)
                if s.hatch:
                    h.SetFillStyle(s.hatch)
                else:
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
                integ, einteg = self.getIntegralWithError(h)
                print "   ",h.GetName().ljust(10),s.name.ljust(20),"{0:8.2f} +- {1:7.2f}".format(integ,einteg)
#                print "Adding to background ",s.name,h.GetName(),opt
#                if s.name.startswith("W"):
#                    print s.name," contents ",h.GetSumOfWeights()
            elif s.isSignal():
                sigs.append(h)
#                print "Adding to signal ",s.name,h.GetName()
            elif s.isData():
                data = h
                h.SetMarkerStyle(20)
                h.SetLineColor(s.color)
                h.SetMarkerColor(s.color)
                
#                print "Adding to signal ",s.name,h.GetName()
            if s.fill:
                opt = "F"
            else:
                opt = "L"
            if s.isData():
                opt = "P"
            if bkgs!=None:
                bkgs.SetMinimum(0.1)
            legend.AddEntry(h,s.name,opt)       

        bkgs.Draw()
        bkgs.GetYaxis().SetTitle("Events / bin")
        for s in sigs:
            s.Draw("same hist")
        if data:
            data.Draw("same")
        legend.Draw()
        legend.SetBit(ROOT.kCanDelete)
#        ROOT.gPad.SetLogy(1)

        if pad!=None:
            pad.Update()

        print data, bkgs, sigs, legend 
        return ( data, bkgs, sigs, legend )

    def drawStack2D(self, samples, histograms, pad=None):

        if pad!=None:
            currpad = pad
            pad.cd()
        else:
            currpad = ROOT.gPad

        bkgs = None
        sigs = [ ]
#        legend = ROOT.TLegend(0.60,0.75,0.90,0.89)
#        legend.SetBorderSize(0)
#        legend.SetFillColor(10)
#        legend.SetFillStyle(0)
        for i,s in enumerate(samples):
            if s.isData():
                continue
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
#                    legend.AddEntry(bkgs,"Backgrounds","")
                else:
                    bkgs.Add(h)
                    print "Adding bkg histo for ",s.name,h.GetName()
#                legend.SetHeader("Backgrounds")
            elif s.isSignal():
                h.SetLineColor(s.color)
                h.SetLineWidth(1)
                sigs.append(h)
                h.SetTitle(s.name)
#                legend.AddEntry(h,s.name,"L")
                print "Sig histo from ",s.name,h.GetName()
#                print "Adding to signal ",s.name,h.GetName()
#            if s.fill:
#                opt = "F"
#            else:
#                opt = "L"

        ipads = [ ]
        nsig = 0
        for s in samples:
            if s.isSignal():  
                nsig += 1
                ipads.append(nsig+1)
            else:
                ipads.append(1)
        nsub = int(sqrt(nsig+1))
        if nsub**2<(nsig+1):
            nsub += 1
        currpad.Divide(nsub,nsub)
        latexs = [ ]
        latex = ROOT.TLatex()
        latex.SetNDC(1)
        latex.SetTextSize(0.04)

        currpad.cd(1)
        ROOT.gPad.SetRightMargin(0.15)
        bkgmax = bkgs.GetMaximum()
        bkgs.SetMaximum(bkgmax/0.85)
        bkgs.SetMinimum(0.1)
        print "bkgmax = ",bkgmax
        bkgs.Draw("zcol")
        latexs.append(latex.DrawLatex(0.40,0.15,"Backgrounds"))
#        bkgs.GetYaxis().SetTitle("Events / bin")
#        contlist = [ bkgmax/0.85*10**(-i) for i in range(2,5) ]
#        c_contlist = ((ctypes.c_double)*(len(contlist)))(*contlist)
#        legend.Draw()
#        legend.SetBit(ROOT.kCanDelete)
        ROOT.gPad.SetLogz(1)
        for i,s in enumerate(sigs):
##            s.SetMaximum(bkgmax/0.85)
##            s.SetMinimum(0.1)
##            s.SetContour(len(contlist),c_contlist)
##            s.SetLineWidth(2)
##            s.Draw("cont3 same")
            currpad.cd(i+2)
            ROOT.gPad.SetRightMargin(0.15)
#            bkgs.DrawClone("zcol")
            s.SetMaximum(bkgmax/0.85)
            s.SetMinimum(0.1)
            s.Draw("zcol")
            latexs.append(latex.DrawLatex(0.40,0.15,s.GetTitle()))
            ROOT.gPad.SetLogz(1)
            print "Drawing signal index ",i,currpad.GetPad(i+2)

        if pad!=None:
            pad.Update()

        currpad.cd()
        currpad.Update()

        return ( bkgs, sigs , latexs )

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

    def drawDoMC(self, data, bkgs, pad=None):

        assert data!=None and bkgs!=None

        if pad!=None:
            pad.cd()

        opt = ""
        hr = self.getDoMC(data,bkgs)
        print hr,hr.GetBinContent(10),hr.GetBinError(10)
        hr.SetMinimum(0.)
        hr.SetMaximum(2.)
        hr.GetYaxis().SetTitle("data/MC")
        hr.GetYaxis().SetTitleSize(0.08)
        hr.SetMarkerStyle(20)
        hr.SetMarkerColor(1)
        hr.SetLineColor(1)
        hr.DrawCopy()
        ROOT.gPad.SetGridx(1)
        ROOT.gPad.SetGridy(1)

        pad.Update()
