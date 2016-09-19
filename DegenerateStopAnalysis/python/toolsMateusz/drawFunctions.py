#drawFunctions.py - ROOT Draw Functions
import ROOT
import math

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
def emptyHist(title, nbins = 100, min = 0, max = 1000):
   hist = ROOT.TH1D("hist", "Histogram", nbins, min, max)
   hist.GetXaxis().SetTitle(title)
   hist.GetYaxis().SetTitle("Events")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   hist.GetXaxis().SetTitleOffset(1.2) 
   hist.GetYaxis().SetTitleOffset(1.2) 
   hist.SetFillColor(ROOT.kBlue-9)
   hist.SetLineColor(ROOT.kBlack)
   hist.SetLineWidth(3)
   return hist

def emptyHistVarBins(varname, xbins):
   hist = ROOT.TH1D("hist", "Histogram", len(xbins)-1, xbins)
   hist.GetXaxis().SetTitle(varname)
   hist.GetYaxis().SetTitle("Events")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   hist.GetXaxis().SetTitleOffset(1.2) 
   hist.GetYaxis().SetTitleOffset(1.2) 
   hist.SetFillColor(ROOT.kBlue-9)
   hist.SetLineColor(ROOT.kBlack)
   hist.SetLineWidth(3)
   return hist

def makeHist(sample, varname, sel = "", nbins = 100, min = 0, max = 1000):
   hist = ROOT.TH1D("hist", "Histogram", nbins, min, max)
   sample.Draw(varname + ">>hist", sel, "goff")
   hist.SetTitle(varname + " Plot")
   hist.GetXaxis().SetTitle(varname)
   hist.GetYaxis().SetTitle("Events")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   hist.GetXaxis().SetTitleOffset(1.2) 
   hist.GetYaxis().SetTitleOffset(1.2) 
   hist.SetFillColor(ROOT.kBlue-9)
   hist.SetLineColor(ROOT.kBlack)
   hist.SetLineWidth(3)
   return hist

def makeHistVarBins(sample, varname, sel, xbins): # xbins = array('d', [range(xmin,xmax,5)])
   hist = ROOT.TH1D("hist", "Histogram", len(xbins)-1, xbins)
   sample.Draw(varname + ">>hist", sel, "goff")
   hist.SetTitle(varname + " Plot")
   hist.GetXaxis().SetTitle(varname)
   hist.GetYaxis().SetTitle("Events")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   hist.GetXaxis().SetTitleOffset(1.2) 
   hist.GetYaxis().SetTitleOffset(1.2) 
   hist.SetFillColor(ROOT.kBlue-9)
   hist.SetLineColor(ROOT.kBlack)
   hist.SetLineWidth(3)
   return hist

def make2DHist(sample, var1, var2, sel = "", nbins1 = 100, min1 = 0, max1 = 1000, nbins2 = 100, min2 = 0, max2 = 1000):
   hist = ROOT.TH2D("hist", "Histogram", nbins1, min1, max1, nbins2, min2, max2)
   sample.Draw(var2 + ":" + var1 + ">>hist", sel, "goff") # (y:x>>hist)
   hist.SetTitle(var1 + " and " + var2 + " Distribution")
   hist.GetXaxis().SetTitle(var1)
   hist.GetYaxis().SetTitle(var2)
   hist.GetZaxis().SetTitle("Events")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   hist.GetZaxis().CenterTitle()
   hist.GetXaxis().SetTitleOffset(1.2) 
   hist.GetYaxis().SetTitleOffset(1.2) 
   hist.GetZaxis().SetTitleOffset(1.2) 
   return hist

def make2DHistVarBins(sample, var1, var2, sel, xbins, ybins):
   hist = ROOT.TH2D("hist", "Histogram", len(xbins)-1, xbins, len(ybins)-1, ybins)
   sample.Draw(var2 + ":" + var1 + ">>hist", sel, "goff") # (y:x>>hist)
   hist.SetTitle(var1 + " and " + var2 + " Distribution")
   hist.GetXaxis().SetTitle(var1)
   hist.GetYaxis().SetTitle(var2)
   hist.GetZaxis().SetTitle("Events")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   hist.GetZaxis().CenterTitle()
   hist.GetXaxis().SetTitleOffset(1.2) 
   hist.GetYaxis().SetTitleOffset(1.2) 
   hist.GetZaxis().SetTitleOffset(1.2) 
   return hist

#Efficiency
def makeEffPlot(passed,total):
   a = passed.Clone()
   b = total.Clone()
   eff = ROOT.TEfficiency(a,b)
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
   a = passed.Clone()
   b = total.Clone()
   a.Divide(b)
   a.SetTitle("Efficiency Plot")
   a.SetMarkerStyle(33)
   a.SetMarkerSize(2)
   a.SetLineWidth(2)
   return a

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
def makeLegend2(x1=0.725,x2=0.875,y1=0.45,y2= 0.65):
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

#def divideEff(e1,e2):
#   res = e1.GetTotalHistogram().Clone()
#   res.Reset()
#   
#   n = res.GetNbinsX()
#   
#   #print 'n: ', n
#   
#   for i in range(n):
#      a = res.GetBinLowEdge(i+1)
#      w = res.GetBinWidth(i+1)
#   
#      #print 'a: ', a, 'w: ', w
#   
#      v1 = e1.GetEfficiency(i+1)
#      u1 = e1.GetEfficiencyErrorUp(i+1)
#      d1 = e1.GetEfficiencyErrorLow(i+1)
#      
#      v2 = e2.GetEfficiency(i+1)
#      u2 = e2.GetEfficiencyErrorUp(i+1)
#      d2 = e2.GetEfficiencyErrorLow(i+1)
#      
#      if v1*v2 == 0:
#          v = 0.
#          u = 0.
#          d = 0.
#      
#      else:
#          v = v1/v2 if v2>0. else 0.
#          u = v*math.sqrt(pow(u1/v1,2)+pow(u2/v2,2))
#          d = v*math.sqrt(pow(d1/v1,2)+pow(d2/v2,2))
#      
#      #print i,v,u,d
#      
#      res.SetBinContent(i+1,v)
#      res.SetBinError(i+1, u)
#      res.SetLineWidth(2)
# 
#   return res

def divideEff(e1,e2): #VarBins
   
   n = e1.GetTotalHistogram().GetNbinsX()

   #print 'n: ', n

   res = ROOT.TGraphAsymmErrors(n)
   
   for i in range(n):
      a = e1.GetTotalHistogram().GetBinLowEdge(i+1)
      w = e1.GetTotalHistogram().GetBinWidth(i+1)
   
      #print 'a: ', a, 'w: ', w
   
      v1 = e1.GetEfficiency(i+1)
      u1 = e1.GetEfficiencyErrorUp(i+1)
      d1 = e1.GetEfficiencyErrorLow(i+1)
      
      v2 = e2.GetEfficiency(i+1)
      u2 = e2.GetEfficiencyErrorUp(i+1)
      d2 = e2.GetEfficiencyErrorLow(i+1)
      
      if v1*v2 == 0:
          v = 0.
          u = 0.
          d = 0.
      
      else:
          v = v1/v2 if v2>0. else 0.
          u = v*math.sqrt(pow(u1/v1,2)+pow(u2/v2,2))
          d = v*math.sqrt(pow(d1/v1,2)+pow(d2/v2,2))
      
      #print i,v,u,d
      
      x = a+w*0.5
      res.SetPoint(i,x,v)
      res.SetPointError(i,0.5*w,0.5*w,d,u)
      res.SetLineWidth(2)
 
   return res

def multiplyHists(h1,h2):
   res = h1.Clone()
   res.Reset()
   
   n = res.GetNbinsX()
   
   #print 'n: ', n
   
   for i in range(n):
      a = res.GetBinLowEdge(i+1)
      w = res.GetBinWidth(i+1)
   
      #print 'a: ', a, 'w: ', w
   
      v1 = h1.GetBinContent(i+1)
      e1 = h1.GetBinError(i+1)
      
      v2 = h2.GetBinContent(i+1)
      e2 = h2.GetBinError(i+1)
      
      if v1*v2 == 0:
          v = 0.
          u = 0.
          d = 0.
      
      else:
          v = v1*v2 if v2>0. else 0.
          e = v*math.sqrt(pow(e1,2)+pow(e2,2))
      
      #print i,v,u,d
      
      res.SetBinContent(i+1,v)
      res.SetBinError(i+1, e)
      res.SetLineWidth(2)
 
   return res

def addSystematicHist(h1,sys):
   res = h1.Clone()
   
   n = res.GetNbinsX()
   
   #print 'n: ', n
   
   for i in range(n):
      a = res.GetBinLowEdge(i+1)
      w = res.GetBinWidth(i+1)
   
      #print 'a: ', a, 'w: ', w
   
      v1 = h1.GetBinContent(i+1)
      e1 = h1.GetBinError(i+1)
     
      print sys/100. 
      e = math.sqrt(pow(e1,2)+pow(sys/100.*v1,2))
      
      res.SetBinError(i+1, e)
      res.SetLineWidth(2)
 
   return res

#def divideEff(e1,e2):
#   
#   n = e1.GetTotalHistogram().GetNbinsX()
#   a = e1.GetTotalHistogram().GetBinLowEdge(1)
#   w = e1.GetTotalHistogram().GetBinWidth(1)
#   
#   #print 'n: ', n, 'a: ', a, 'w: ', w
#   
#   res = ROOT.TGraphAsymmErrors(n)
#   
#   for i in range(n):
#      v1 = e1.GetEfficiency(i+1)
#      u1 = e1.GetEfficiencyErrorUp(i+1)
#      d1 = e1.GetEfficiencyErrorLow(i+1)
#      
#      v2 = e2.GetEfficiency(i+1)
#      u2 = e2.GetEfficiencyErrorUp(i+1)
#      d2 = e2.GetEfficiencyErrorLow(i+1)
#      
#      if v1*v2 == 0:
#          v = 0.
#          u = 0.
#          d = 0.
#      
#      else:
#          v = v1/v2 if v2>0. else 0.
#          u = v*math.sqrt(pow(u1/v1,2)+pow(u2/v2,2))
#          d = v*math.sqrt(pow(d1/v1,2)+pow(d2/v2,2))
#      
#      #print i,v,u,d
#      
#      x = a+(i+0.5)*w
#      res.SetPoint(i,x,v)
#      res.SetPointError(i,0.5*w,0.5*w,d,u)
#      res.SetLineWidth(2)
#   
#   return res


##Variable bin size
#nSec = 3
#lenSec = (max - min)/nSec
#bins = []
#for l in [range(min + (x-1)*lenSec, min + x*lenSec, 2*i) for x in range(1, nSec+1)]: bins += map(float,l)
#xbins = array('d', bins)
