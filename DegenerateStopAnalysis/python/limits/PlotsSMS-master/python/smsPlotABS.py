import ROOT as rt
from array import *
from sms import *
from color import *

class smsPlotABS(object):
    # modelname is the sms name (see sms.py)
    # histo is the 2D xsec map
    # obsLimits is a list of opbserved limits [NOMINAL, +1SIGMA, -1SIGMA]
    # expLimits is a list of expected limits [NOMINAL, +1SIGMA, -1SIGMA]
    # label is a label referring to the analysis (e.g. RA1, RA2, RA2b, etc)

    def __init__(self, modelname, histo, obsLimits, expLimits, energy, lumi, preliminary, label):
        self.standardDef(modelname, histo, obsLimits, expLimits, energy, lumi, preliminary)
        self.LABEL = label
        self.c = rt.TCanvas("cABS_%s" %label,"cABS_%s" %label,300,300)
        self.histo = histo

    def standardDef(self, modelname, histo, obsLimits, expLimits, energy, lumi, preliminary, analysis=None):
        # which SMS?
        self.model = sms(modelname)
        self.dmplot = getattr(self.model, 'dmplot',False)
        self.OBS = obsLimits
        self.EXP = expLimits
        self.lumi = lumi
        self.energy = energy
        self.preliminary = preliminary
        self.analysis = analysis
        # create the reference empty histo
        self.emptyhisto = self.emptyHistogramFromModel()

    def emptyHistogramFromModel(self):
        self.emptyHisto = rt.TH2D("emptyHisto", "", 1, self.model.Xmin, self.model.Xmax, 1, self.model.Ymin, self.model.Ymax)
        
    # define the plot canvas
    def setStyle(self):
        # canvas style
        rt.gStyle.SetOptStat(0)
        rt.gStyle.SetOptTitle(0)        

        if not getattr( self.model, 'signifPlot', False):
            self.c.SetLogz()
        self.c.SetTickx(1)
        self.c.SetTicky(1)

        self.c.SetRightMargin(0.19)
        self.c.SetTopMargin(0.08)
        self.c.SetLeftMargin(0.14)
        self.c.SetBottomMargin(0.14)

        # set x axis
        self.emptyHisto.GetXaxis().SetLabelFont(42)
        self.emptyHisto.GetXaxis().SetLabelSize(0.04)
        self.emptyHisto.GetXaxis().SetTitleFont(42)
        self.emptyHisto.GetXaxis().SetTitleSize(0.05)
        self.emptyHisto.GetXaxis().SetTitleOffset(1.2)
        self.emptyHisto.GetXaxis().SetTitle(self.model.sParticle)
        #self.emptyHisto.GetXaxis().CenterTitle(True)

        # set y axis
        self.emptyHisto.GetYaxis().SetLabelFont(42)
        self.emptyHisto.GetYaxis().SetLabelSize(0.04)
        self.emptyHisto.GetYaxis().SetTitleFont(42)
        self.emptyHisto.GetYaxis().SetTitleSize(0.05)
        self.emptyHisto.GetYaxis().SetTitleOffset(1.35)
        self.emptyHisto.GetYaxis().SetTitle(self.model.LSP)
        #self.emptyHisto.GetYaxis().CenterTitle(True)
                
    def DrawText(self):
        #redraw axes
        self.c.RedrawAxis()
        # white background
        graphWhite = rt.TGraph(5)
        graphWhite.SetName("white")
        graphWhite.SetTitle("white")
        graphWhite.SetFillColor(rt.kWhite)
        graphWhite.SetFillStyle(1001)
        graphWhite.SetLineColor(rt.kBlack)
        graphWhite.SetLineStyle(1)
        graphWhite.SetLineWidth(3)
        graphWhite.SetPoint(0,self.model.Xmin, self.model.Ymax)
        graphWhite.SetPoint(1,self.model.Xmax, self.model.Ymax)
#        graphWhite.SetPoint(2,self.model.Xmax, self.model.Ymax*0.75)
#        graphWhite.SetPoint(3,self.model.Xmin, self.model.Ymax*0.75)
        #if self.dmplot:
        #    graphWhite.SetPoint(2,self.model.Xmax, self.model.Ymax*0.715)
        #    graphWhite.SetPoint(3,self.model.Xmin, self.model.Ymax*0.715)
        #else:
        if not getattr( self.model, 'signifPlot', False):
            graphWhite.SetPoint(2,self.model.Xmax, self.model.Ymax*0.80)
            graphWhite.SetPoint(3,self.model.Xmin, self.model.Ymax*0.80)
        else:
            graphWhite.SetPoint(2,self.model.Xmax, self.model.Ymax*0.89)
            graphWhite.SetPoint(3,self.model.Xmin, self.model.Ymax*0.89)
                
        graphWhite.SetPoint(4,self.model.Xmin, self.model.Ymax)
        graphWhite.Draw("FSAME")
        graphWhite.Draw("LSAME")
        self.c.graphWhite = graphWhite
        
        # CMS LABEL
#        textCMS = rt.TLatex(0.22,0.98,"CMS %s, %s fb^{-1}, #sqrt{s} = %s TeV" %(self.preliminary, self.lumi, self.energy))
        textCMS = rt.TLatex(0.805,0.975,"%s fb^{-1} (%s TeV)" %(self.lumi, self.energy))
        textCMS.SetNDC()
        textCMS.SetTextAlign(33)
        textCMS.SetTextFont(42)
        textCMS.SetTextSize(0.038)
        textCMS.Draw()
        self.c.textCMS = textCMS
        # Large CMS label
        xRange = self.model.Xmax-self.model.Xmin
        yRange = self.model.Ymax-self.model.Ymin
        if self.dmplot:
            textCMSlarge = rt.TLatex(0.15 , 0.965 ,"#font[61]{CMS} #font[52]{%s}" %(self.preliminary))
            textCMSlarge.SetNDC()
            textCMSlarge.SetTextAlign(13)
            textCMSlarge.SetTextFont(42)
            textCMSlarge.SetTextSize(0.038)
            textCMSlarge.Draw()
            self.c.textCMSlarge = textCMSlarge

        else:
            textCMSlarge = rt.TLatex(self.model.Xmin+4*xRange/100, self.model.Ymax-3.00*yRange/100*10,"#font[61]{CMS} #font[52]{%s}" %(self.preliminary))
#            textCMSlarge.SetNDC()
            textCMSlarge.SetTextAlign(13)
            textCMSlarge.SetTextFont(42)
            textCMSlarge.SetTextSize(0.050)
            textCMSlarge.Draw()
            self.c.textCMSlarge = textCMSlarge
        # Analysis label
        if self.analysis:
            textAnalysis = rt.TLatex(self.model.Xmin+4*xRange/100, self.model.Ymax-3.75*yRange/100*10,"%s" %(self.analysis))
            textAnalysis.SetTextAlign(13)
            textAnalysis.SetTextFont(42)
            textAnalysis.SetTextSize(0.035)
            textAnalysis.Draw()
            self.c.textAnalysis = textAnalysis
        # MODEL LABEL
        #textModelLabel= rt.TLatex(0.16,0.90,"%s  NLO+NLL exclusion" %self.model.label)
        textModelLabel= rt.TLatex(0.16,0.90,"%s" %self.model.label)
        textModelLabel.SetNDC()
        textModelLabel.SetTextAlign(13)
        textModelLabel.SetTextFont(42)
        textModelLabel.SetTextSize(0.038)
        textModelLabel.Draw()
        self.c.textModelLabel = textModelLabel

        # NLO NLL XSEC
        if not getattr(self.model, "signifPlot", False):
            textNLONLL= rt.TLatex(0.66,0.90,"NLO-NLL")
            textNLONLL.SetNDC()
            textNLONLL.SetTextAlign(13)
            textNLONLL.SetTextFont(42)
            textNLONLL.SetTextSize(0.035)
            textNLONLL.Draw()
            self.c.textNLONLL = textNLONLL
            textExclusion= rt.TLatex(0.66,0.87,"exclusion")
            textExclusion.SetNDC()
            textExclusion.SetTextAlign(13)
            textExclusion.SetTextFont(42)
            textExclusion.SetTextSize(0.035)
            textExclusion.Draw()
            self.c.textExclusion = textExclusion
        if "t2bw" in self.model.modelname.lower():
            if self.dmplot:
                chipmpos = [0.48,0.24]
            else:
                chipmpos = [0.48,0.24]
            textChiPM = rt.TLatex(chipmpos[0],chipmpos[1], self.model.extraText)
            textChiPM.SetNDC()
            textChiPM.SetTextAlign(13)
            textChiPM.SetTextFont(42)
            textChiPM.SetTextSize(0.033)
            textChiPM.Draw()
            self.c.textChiPM = textChiPM

    def Save(self,label):
        # save the output
        self.c.SaveAs("%s.png" %label)
        self.c.SaveAs("%s.pdf" %label)
        self.c.SaveAs("%s.root" %label)
        
    def DrawLegend(self):
        xRange = self.model.Xmax-self.model.Xmin
        yRange = self.model.Ymax-self.model.Ymin
        
        LObs = rt.TGraph(2)
        LObs.SetName("LObs")
        LObs.SetTitle("LObs")
        LObs.SetLineColor(color(self.OBS['colorLine']))
        LObs.SetLineStyle(1)
        LObs.SetLineWidth(4)
        LObs.SetMarkerStyle(20)
        LObs.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.35*yRange/100*10)
        LObs.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.35*yRange/100*10)

        LObsP = rt.TGraph(2)
        LObsP.SetName("LObsP")
        LObsP.SetTitle("LObsP")
        LObsP.SetLineColor(color(self.OBS['colorLine']))
        LObsP.SetLineStyle(1)
        LObsP.SetLineWidth(2)
        LObsP.SetMarkerStyle(20)
        LObsP.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.20*yRange/100*10)
        LObsP.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.20*yRange/100*10)

        LObsM = rt.TGraph(2)
        LObsM.SetName("LObsM")
        LObsM.SetTitle("LObsM")
        LObsM.SetLineColor(color(self.OBS['colorLine']))
        LObsM.SetLineStyle(1)
        LObsM.SetLineWidth(2)
        LObsM.SetMarkerStyle(20)
        LObsM.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.50*yRange/100*10)
        LObsM.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.50*yRange/100*10)

        textObs = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-1.50*yRange/100*10, "Observed #pm 1 #sigma (theory)")
        textObs.SetTextFont(42)
        textObs.SetTextSize(0.038)
        textObs.Draw()
        self.c.textObs = textObs

        LExpP = rt.TGraph(2)
        LExpP.SetName("LExpP")
        LExpP.SetTitle("LExpP")
        LExpP.SetLineColor(color(self.EXP['colorLine']))
        LExpP.SetLineStyle(7)
        LExpP.SetLineWidth(2)  
        LExpP.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.85*yRange/100*10)
        LExpP.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.85*yRange/100*10)
        
        LExp = rt.TGraph(2)
        LExp.SetName("LExp")
        LExp.SetTitle("LExp")
        LExp.SetLineColor(color(self.EXP['colorLine']))
        LExp.SetLineStyle(7)
        LExp.SetLineWidth(4)
        LExp.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.00*yRange/100*10)
        LExp.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.00*yRange/100*10)
        
        LExpM = rt.TGraph(2)
        LExpM.SetName("LExpM")
        LExpM.SetTitle("LExpM")
        LExpM.SetLineColor(color(self.EXP['colorLine']))
        LExpM.SetLineStyle(7)
        LExpM.SetLineWidth(2)  
        LExpM.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.15*yRange/100*10)
        LExpM.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.15*yRange/100*10)

        textExp = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-2.15*yRange/100*10, "Expected #pm 1 #sigma (experiment)")
        textExp.SetTextFont(42)
        textExp.SetTextSize(0.038)
        textExp.Draw()
        self.c.textExp = textExp

        LObs.Draw("LSAME")
        LObsM.Draw("LSAME")
        LObsP.Draw("LSAME")
        LExp.Draw("LSAME")
        LExpM.Draw("LSAME")
        LExpP.Draw("LSAME")
        
        self.c.LObs = LObs
        self.c.LObsM = LObsM
        self.c.LObsP = LObsP
        self.c.LExp = LExp
        self.c.LExpM = LExpM
        self.c.LExpP = LExpP

    def DrawDiagonal(self):
        diagonal = rt.TGraph(3, self.model.diagX, self.model.diagY)
        diagonal.SetName("diagonal")
        diagonal.SetFillColor(rt.kWhite)
        diagonal.SetLineColor(rt.kGray)
        diagonal.SetLineStyle(2)
        diagonal.Draw("FSAME")
        diagonal.Draw("LSAME")
        self.c.diagonal = diagonal
        
    def DrawLines(self):
        # observed
        self.OBS['nominal'].SetLineColor(color(self.OBS['colorLine']))
        self.OBS['nominal'].SetLineStyle(1)
        self.OBS['nominal'].SetLineWidth(4)
        # observed + 1sigma
        self.OBS['plus'].SetLineColor(color(self.OBS['colorLine']))
        self.OBS['plus'].SetLineStyle(1)
        self.OBS['plus'].SetLineWidth(2)        
        # observed - 1sigma
        self.OBS['minus'].SetLineColor(color(self.OBS['colorLine']))
        self.OBS['minus'].SetLineStyle(1)
        self.OBS['minus'].SetLineWidth(2)        
        # expected + 1sigma
        self.EXP['plus'].SetLineColor(color(self.EXP['colorLine']))
        self.EXP['plus'].SetLineStyle(7)
        self.EXP['plus'].SetLineWidth(2)                
        # expected
        self.EXP['nominal'].SetLineColor(color(self.EXP['colorLine']))
        self.EXP['nominal'].SetLineStyle(7)
        self.EXP['nominal'].SetLineWidth(4)        
        # expected - 1sigma
        self.EXP['minus'].SetLineColor(color(self.EXP['colorLine']))
        self.EXP['minus'].SetLineStyle(7)
        self.EXP['minus'].SetLineWidth(2)                        
        # DRAW LINES
        self.EXP['nominal'].Draw("LSAME")
        self.EXP['plus'].Draw("LSAME")
        self.EXP['minus'].Draw("LSAME")
        self.OBS['nominal'].Draw("LSAME")
        self.OBS['plus'].Draw("LSAME")
        self.OBS['minus'].Draw("LSAME")        

        
