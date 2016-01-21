#ROOT Draw Functions
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

def emptyHist(varname, nbins = 100, min = 0, max = 1000):
   hist = ROOT.TH1F("hist", varname + " Histogram", nbins, min, max)
   hist.GetYaxis().SetTitle("Counts")
   hist.GetXaxis().SetTitle(varname)
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   hist.SetFillColor(ROOT.kAzure+2)
   hist.SetLineColor(ROOT.kBlack)
   hist.SetLineWidth(3)
   return hist

def emptyHistVarBins(varname, xbins):
   hist = ROOT.TH1F("hist", varname + " Histogram", len(xbins)-1, xbins)
   hist.GetXaxis().SetTitle(varname)
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().SetTitle("Counts")
   hist.GetYaxis().CenterTitle()
   hist.SetFillColor(ROOT.kAzure+2)
   hist.SetLineColor(ROOT.kBlack)
   hist.SetLineWidth(3)
   return hist


def makeHist(sample, varname, sel = "", nbins = 100, min = 0, max = 1000):
   hist = ROOT.TH1F("hist", varname + " Histogram", nbins, min, max)
   sample.Draw(varname + ">>hist", sel, "goff")
   hist.SetTitle(varname + " Plot")
   hist.GetXaxis().SetTitle(varname)
   hist.GetYaxis().SetTitle("Counts")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   hist.SetFillColor(ROOT.kAzure+2)
   hist.SetLineColor(ROOT.kBlack)
   hist.SetLineWidth(3)
   return hist

def makeHistVarBins(sample, varname, sel, xbins):
   # = array('d', [range(xmin,xmax,5)])
   hist = ROOT.TH1F("hist", varname +  "Histogram", len(xbins)-1, xbins)
   sample.Draw(varname + ">>hist", sel, "goff")
   hist.SetTitle(varname + " Plot")
   hist.GetXaxis().SetTitle(varname)
   hist.GetYaxis().SetTitle("Counts")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   hist.SetFillColor(ROOT.kAzure+2)
   hist.SetLineColor(ROOT.kBlack)
   hist.SetLineWidth(3)
   return hist

#Creates Legend
def makeLegend():
   leg = ROOT.TLegend(0.775,0.45,0.875,0.65)
   leg.SetHeader("#bf{Legend}")
   header = leg.GetListOfPrimitives().First()
   header.SetTextAlign(22)
   return leg

#Creates Box 
def makeBox():
   box = ROOT.TPaveText(0.775,0.20,0.875,0.40, "NDC") #NB & ARC
   #box.SetHeader("Cuts")
   #header = box.GetListOfPrimitives().First()
   #header.SetTextAlign(22)
   return box

def alignStats(hist):
   st = hist.FindObject("stats")
   st.SetX1NDC(0.775)
   st.SetX2NDC(0.875)
   st.SetY1NDC(0.7)
   st.SetY2NDC(0.85)

##Variable bin size
#nSec = 3
#lenSec = (max - min)/nSec
#bins = []
#for l in [range(min + (x-1)*lenSec, min + x*lenSec, 2*i) for x in range(1, nSec+1)]: bins += map(float,l)
#xbins = array('d', bins)
