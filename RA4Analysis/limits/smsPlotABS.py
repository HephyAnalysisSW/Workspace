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

    def standardDef(self, modelname, histo, obsLimits, expLimits, energy, lumi, preliminary):
        # which SMS?
        self.model = sms(modelname)
        self.OBS = obsLimits
        self.EXP = expLimits
        self.lumi = lumi
        self.energy = energy
        self.preliminary = preliminary
        # create the reference empty histo
        self.emptyhisto = self.emptyHistogramFromModel()

    def emptyHistogramFromModel(self):
        self.emptyHisto = rt.TH2D("emptyHisto", "", 1, self.model.Xmin, self.model.Xmax, 1, self.model.Ymin, self.model.Ymax)
        
        
    # define the plot canvas
    def setStyle(self):
        # canvas style
        rt.gStyle.SetOptStat(0)
        rt.gStyle.SetOptTitle(0)        
        
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
        if self.model.modelname == "T1tttt":
            self.emptyHisto.GetXaxis().SetNdivisions(405)

        # set y axis
        self.emptyHisto.GetYaxis().SetLabelFont(42)
        self.emptyHisto.GetYaxis().SetLabelSize(0.04)
        self.emptyHisto.GetYaxis().SetTitleFont(42)
        self.emptyHisto.GetYaxis().SetTitleSize(0.05)
        if self.model.modelname == "T5tttt":
            self.emptyHisto.GetYaxis().SetTitleOffset(1.45)
        else:
            self.emptyHisto.GetYaxis().SetTitleOffset(1.35)
        self.emptyHisto.GetYaxis().SetTitle(self.model.LSP)
        #self.emptyHisto.GetYaxis().CenterTitle(True)


	# set z axis to have no title
	self.emptyHisto.GetZaxis().SetTitle("")          
	self.histo.GetZaxis().SetTitle("")     
 
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
        graphWhite.SetPoint(2,self.model.Xmax, self.model.Ymax*0.75)
        graphWhite.SetPoint(3,self.model.Xmin, self.model.Ymax*0.75)
        graphWhite.SetPoint(4,self.model.Xmin, self.model.Ymax)
        graphWhite.Draw("FSAME")
        graphWhite.Draw("LSAME")
        self.c.graphWhite = graphWhite
        
        # CMS LABEL
        textCMS = rt.TLatex(0.22,0.98,"CMS %s, %s fb^{-1}, #sqrt{s} = %s TeV" %(self.preliminary, self.lumi, self.energy))
        textCMS.SetNDC()
        textCMS.SetTextAlign(13)
        textCMS.SetTextFont(42)
        textCMS.SetTextSize(0.038)
        textCMS.Draw()
        self.c.textCMS = textCMS
        # MODEL LABEL
        if self.model.modelname == "T1tttt":
            textModelLabel= rt.TLatex(0.16,0.90,"%s  NLO+NLL exclusion" %self.model.label)
        elif self.model.modelname == "T5tttt" or self.model.modelname == "T1t1t":
            textModelLabel= rt.TLatex(0.16,0.905,"#splitline{%s}{NLO+NLL exclusion}" %self.model.label)
        textModelLabel.SetNDC()
        textModelLabel.SetTextAlign(13)
        textModelLabel.SetTextFont(42)
        textModelLabel.SetTextSize(0.040)
        textModelLabel.Draw()
        self.c.textModelLabel = textModelLabel
        # NLO NLL XSEC
        textNLONLL= rt.TLatex(0.16,0.32,"NLO-NLL exclusion")
        textNLONLL.SetNDC()
        textNLONLL.SetTextAlign(13)
        textNLONLL.SetTextFont(42)
        textNLONLL.SetTextSize(0.040)
        textNLONLL.Draw()
        #self.c.textNLONLL = textNLONLL

	# ***Added for RA4 LS
        if self.model.modelname == "T1tttt":
            searchLabel1= rt.TLatex(0.25,0.37,"Single-Lepton")
        elif self.model.modelname == "T5tttt":
            searchLabel1= rt.TLatex(0.18,0.41,"Single-Lepton")
        elif self.model.modelname == "T1t1t":
            searchLabel1= rt.TLatex(0.20,0.65,"Single-Lepton")
        searchLabel1.SetNDC()
        searchLabel1.SetTextAlign(13)
        searchLabel1.SetTextFont(42)
        searchLabel1.SetTextSize(0.040)
        searchLabel1.Draw()
        self.c.searchLabel1 = searchLabel1

        if self.model.modelname == "T1tttt":
            searchLabel2= rt.TLatex(0.25,0.335,"H_{T}, #slash{E}_{T} search")
        elif self.model.modelname == "T5tttt":
            searchLabel2= rt.TLatex(0.18,0.375,"H_{T}, #slash{E}_{T} search")
        elif self.model.modelname == "T1t1t":
            searchLabel2= rt.TLatex(0.20,0.615,"H_{T}, #slash{E}_{T} search")
        searchLabel2.SetNDC()
        searchLabel2.SetTextAlign(13)
        searchLabel2.SetTextFont(42)
        searchLabel2.SetTextSize(0.040)
        searchLabel2.Draw()
        self.c.searchLabel2 = searchLabel2

        if self.model.modelname == "T1tttt":
            searchLabel3= rt.TLatex(0.25,0.27,"#slash{E}_{T} templates")
        elif self.model.modelname == "T5tttt":
            searchLabel3= rt.TLatex(0.18,0.31,"#slash{E}_{T} templates")
        elif self.model.modelname == "T1t1t":
            searchLabel3= rt.TLatex(0.20,0.55,"#slash{E}_{T} templates")
        searchLabel3.SetNDC()
        searchLabel3.SetTextAlign(13)
        searchLabel3.SetTextFont(42)
        searchLabel3.SetTextSize(0.040)
        searchLabel3.Draw()
        self.c.searchLabel3 = searchLabel3

        if self.model.modelname == "T1tttt":
            searchLabel4= rt.TLatex(0.25,0.205,"N#scale[0.2]{ }_{jet}#geq6, N#scale[0.2]{ }_{b}=2,#geq3")
        elif self.model.modelname == "T5tttt":
            searchLabel4= rt.TLatex(0.18,0.245,"N#scale[0.2]{ }_{jet}#geq6, N#scale[0.2]{ }_{b}=2,#geq3")
        elif self.model.modelname == "T1t1t":
            searchLabel4= rt.TLatex(0.20,0.485,"N#scale[0.2]{ }_{jet}#geq6, N#scale[0.2]{ }_{b}=2,#geq3")
        searchLabel4.SetNDC()
        searchLabel4.SetTextAlign(13)
        searchLabel4.SetTextFont(42)
        searchLabel4.SetTextSize(0.040)
        searchLabel4.Draw()
        self.c.searchLabel4 = searchLabel4



    def Save(self,label):
        # save the output
        self.c.SaveAs("%s.pdf" %label)
        
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
        if self.model.modelname == "T1tttt":
            LObs.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.35*yRange/100*10)
            LObs.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.35*yRange/100*10)
        elif self.model.modelname == "T5tttt" or self.model.modelname == "T1t1t":
            LObs.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.80*yRange/100*10)
            LObs.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.80*yRange/100*10)

        LObsP = rt.TGraph(2)
        LObsP.SetName("LObsP")
        LObsP.SetTitle("LObsP")
        LObsP.SetLineColor(color(self.OBS['colorLine']))
        LObsP.SetLineStyle(1)
        LObsP.SetLineWidth(2)
        LObsP.SetMarkerStyle(20)
        if self.model.modelname == "T1tttt":
            LObsP.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.20*yRange/100*10)
            LObsP.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.20*yRange/100*10)
        elif self.model.modelname == "T5tttt" or self.model.modelname == "T1t1t":
            LObsP.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.65*yRange/100*10)
            LObsP.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.65*yRange/100*10)
        
        LObsM = rt.TGraph(2)
        LObsM.SetName("LObsM")
        LObsM.SetTitle("LObsM")
        LObsM.SetLineColor(color(self.OBS['colorLine']))
        LObsM.SetLineStyle(1)
        LObsM.SetLineWidth(2)
        LObsM.SetMarkerStyle(20)
        if self.model.modelname == "T1tttt":
            LObsM.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.50*yRange/100*10)
            LObsM.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.50*yRange/100*10)
        elif self.model.modelname == "T5tttt" or self.model.modelname == "T1t1t":
            LObsM.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.95*yRange/100*10)
            LObsM.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.95*yRange/100*10)

        if self.model.modelname == "T1tttt":
            textObs = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-1.50*yRange/100*10, "Observed #pm 1 #sigma_{theory}")
        elif self.model.modelname == "T5tttt" or self.model.modelname == "T1t1t":
            textObs = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-1.95*yRange/100*10, "Observed #pm 1 #sigma_{theory}")
        textObs.SetTextFont(42)
        textObs.SetTextSize(0.040)
        textObs.Draw()
        self.c.textObs = textObs

        LExpP = rt.TGraph(2)
        LExpP.SetName("LExpP")
        LExpP.SetTitle("LExpP")
        LExpP.SetLineColor(color(self.EXP['colorLine']))
        LExpP.SetLineStyle(7)
        LExpP.SetLineWidth(2)
        if self.model.modelname == "T1tttt":
            LExpP.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.85*yRange/100*10)
            LExpP.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.85*yRange/100*10)
        elif self.model.modelname == "T5tttt" or self.model.modelname == "T1t1t":
            LExpP.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.30*yRange/100*10)
            LExpP.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.30*yRange/100*10)
        
        LExp = rt.TGraph(2)
        LExp.SetName("LExp")
        LExp.SetTitle("LExp")
        LExp.SetLineColor(color(self.EXP['colorLine']))
        LExp.SetLineStyle(7)
        LExp.SetLineWidth(4)
        if self.model.modelname == "T1tttt":
            LExp.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.00*yRange/100*10)
            LExp.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.00*yRange/100*10)
        elif self.model.modelname == "T5tttt" or self.model.modelname == "T1t1t":
            LExp.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.45*yRange/100*10)
            LExp.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.45*yRange/100*10)
        
        LExpM = rt.TGraph(2)
        LExpM.SetName("LExpM")
        LExpM.SetTitle("LExpM")
        LExpM.SetLineColor(color(self.EXP['colorLine']))
        LExpM.SetLineStyle(7)
        LExpM.SetLineWidth(2)
        if self.model.modelname == "T1tttt":
            LExpM.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.15*yRange/100*10)
            LExpM.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.15*yRange/100*10)
        elif self.model.modelname == "T5tttt" or self.model.modelname == "T1t1t":
            LExpM.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.60*yRange/100*10)
            LExpM.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.60*yRange/100*10)

        if self.model.modelname == "T1tttt":
            textExp = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-2.15*yRange/100*10, "Expected #pm 1 #sigma_{experiment}")
        elif self.model.modelname == "T5tttt" or self.model.modelname == "T1t1t":
            textExp = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-2.60*yRange/100*10, "Expected #pm 1 #sigma_{experiment}")
        textExp.SetTextFont(42)
        textExp.SetTextSize(0.040)
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
        #diagonal = rt.TGraph(3, self.model.diagX, self.model.diagY)
        diagonal = rt.TGraph(2, self.model.diagX, self.model.diagY)
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

        
