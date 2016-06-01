#drawFunctions.py - ROOT Draw Functions
import ROOT
#import array
def makeLine():
   line = "\n************************************************************************************************************************************************************************\n"
   return line

def makeDoubleLine():
   line = "\n************************************************************************************************************************************************************************\n\
*********************************************************************************************************************************************************************\n"
   return line

def newLine():
   print ""
   return

#Histograms
def emptyHist(varname, nbins = 100, min = 0, max = 1000):
   hist = ROOT.TH1F("hist", "Histogram", nbins, min, max)
   hist.GetXaxis().SetTitle(varname)
   hist.GetYaxis().SetTitle("Counts")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   hist.GetXaxis().SetTitleOffset(1.2) 
   hist.GetYaxis().SetTitleOffset(1.2) 
   hist.SetFillColor(ROOT.kBlue-9)
   hist.SetLineColor(ROOT.kBlack)
   hist.SetLineWidth(3)
   return hist

def emptyHistVarBins(varname, xbins):
   hist = ROOT.TH1F("hist", "Histogram", len(xbins)-1, xbins)
   hist.GetXaxis().SetTitle(varname)
   hist.GetYaxis().SetTitle("Counts")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   hist.GetXaxis().SetTitleOffset(1.2) 
   hist.GetYaxis().SetTitleOffset(1.2) 
   hist.SetFillColor(ROOT.kBlue-9)
   hist.SetLineColor(ROOT.kBlack)
   hist.SetLineWidth(3)
   return hist

def makeHist(sample, varname, sel = "", nbins = 100, min = 0, max = 1000):
   hist = ROOT.TH1F("hist", "Histogram", nbins, min, max)
   sample.Draw(varname + ">>hist", sel, "goff")
   hist.SetTitle(varname + " Plot")
   hist.GetXaxis().SetTitle(varname)
   hist.GetYaxis().SetTitle("Counts")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   hist.GetXaxis().SetTitleOffset(1.2) 
   hist.GetYaxis().SetTitleOffset(1.2) 
   hist.SetFillColor(ROOT.kBlue-9)
   hist.SetLineColor(ROOT.kBlack)
   hist.SetLineWidth(3)
   return hist

def makeHistVarBins(sample, varname, sel, xbins): # xbins = array('d', [range(xmin,xmax,5)])
   hist = ROOT.TH1F("hist", "Histogram", len(xbins)-1, xbins)
   sample.Draw(varname + ">>hist", sel, "goff")
   hist.SetTitle(varname + " Plot")
   hist.GetXaxis().SetTitle(varname)
   hist.GetYaxis().SetTitle("Counts")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   hist.GetXaxis().SetTitleOffset(1.2) 
   hist.GetYaxis().SetTitleOffset(1.2) 
   hist.SetFillColor(ROOT.kBlue-9)
   hist.SetLineColor(ROOT.kBlack)
   hist.SetLineWidth(3)
   return hist

def make2DHist(sample, var1, var2, sel = "", nbins1 = 100, min1 = 0, max1 = 1000, nbins2 = 100, min2 = 0, max2 = 1000):
   hist = ROOT.TH2F("hist", "Histogram", nbins1, min1, max1, nbins2, min2, max2)
   sample.Draw(var2 + ":" + var1 + ">>hist", sel, "goff") # (y:x>>hist)
   hist.SetTitle(var1 + " and " + var2 + " Distribution")
   hist.GetXaxis().SetTitle(var1)
   hist.GetYaxis().SetTitle(var2)
   hist.GetZaxis().SetTitle("Counts")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   hist.GetZaxis().CenterTitle()
   hist.GetXaxis().SetTitleOffset(1.2) 
   hist.GetYaxis().SetTitleOffset(1.2) 
   hist.GetZaxis().SetTitleOffset(1.2) 
   return hist

#Efficiency
def makeEffPlot(passed,total):
   eff = ROOT.TEfficiency(passed,total)
   eff.SetTitle("Efficiency Plot")
   eff.SetMarkerStyle(33)
   eff.SetMarkerSize(2)
   eff.SetLineWidth(2)
   return eff

def setupEffPlot(eff):
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   ROOT.gPad.SetGridx()
   ROOT.gPad.SetGridy()
   eff.GetPaintedGraph().GetYaxis().SetTitle("Efficiency")
   eff.GetPaintedGraph().SetMinimum(0)
   eff.GetPaintedGraph().SetMaximum(1)
   eff.GetPaintedGraph().GetXaxis().CenterTitle()
   eff.GetPaintedGraph().GetYaxis().CenterTitle()
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()

def makeEffPlot2(passed,total): #When ratio > 1
   eff = passed
   eff.Divide(total)
   eff.SetTitle("Efficiency Plot")
   eff.SetMarkerStyle(33)
   eff.SetMarkerSize(2)
   eff.SetLineWidth(2)
   return eff

def setupEffPlot2(eff):
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   ROOT.gPad.SetGridx()
   ROOT.gPad.SetGridy()
   eff.GetYaxis().SetTitle("Efficiency")
   eff.SetMinimum(0)
   eff.SetMaximum(1)
   eff.GetXaxis().CenterTitle()
   eff.GetYaxis().CenterTitle()
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()

#Legend
def makeLegend(x1=0.775,x2=0.875,y1=0.45,y2= 0.65):
   leg = ROOT.TLegend(x1,y1,x2,y2)
   leg.SetHeader("#bf{Legend}")
   header = leg.GetListOfPrimitives().First()
   header.SetTextAlign(22)
   return leg

#Box 
def makeBox(x1=0.775,x2=0.875,y1=0.2,y2=0.4):
   box = ROOT.TPaveText(x1,y1,x2,y2, "NDC") #NB & ARC
   #box.SetHeader("Header")
   #header = box.GetListOfPrimitives().First()
   #header.SetTextAlign(22)
   return box

#Align
def alignStats(hist,x1=0.775,x2=0.875,y1=0.7,y2=0.85):
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   st = hist.FindObject("stats")
   st.SetX1NDC(x1)
   st.SetX2NDC(x2)
   st.SetY1NDC(y1)
   st.SetY2NDC(y2)
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()

def alignLegend(leg,x1=0.775,x2=0.875,y1=0.2,y2=0.4):
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   leg.SetX1NDC(x1)
   leg.SetX2NDC(x2)
   leg.SetY1NDC(y1)
   leg.SetY2NDC(y2)
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()

##Variable bin size
#nSec = 3
#lenSec = (max - min)/nSec
#bins = []
#for l in [range(min + (x-1)*lenSec, min + x*lenSec, 2*i) for x in range(1, nSec+1)]: bins += map(float,l)
#xbins = array('d', bins)
