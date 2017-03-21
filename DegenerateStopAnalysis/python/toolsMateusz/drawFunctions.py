#drawFunctions.py - ROOT Draw Functions
import ROOT
import math
import hashlib
import time
from array import array
from Workspace.DegenerateStopAnalysis.tools.ratioTools import makeCanvasMultiPads
from Workspace.DegenerateStopAnalysis.tools.degTools import decorAxis 

def uniqueHash():
    return hashlib.md5("%s"%time.time()).hexdigest()

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

# Canvas

def drawPlot(plot_, dOpt="hist", isDataPlot = False, legend = None, decor = False, latexText = None, plotMin=False, normalize=False, ratio = (None, None), ratioTitle = "Ratio", ratioLimits=[], unity = True): #ratioNorm=False, verbose=False, 

   ret = {}
   ret['junk'] = []

   plot = plot_.Clone()

   drawRatio = type(ratio) != type(()) or (ratio[0] and ratio[1])

   if drawRatio:
      padRatios=[2,1]
      #else:
      #    padRatios=[2]+[1]*(len(den))
     
      canvs = makeCanvasMultiPads(c1Name = "Canvas_"+plot.GetName(), c1ww=800, c1wh=800, joinPads=True, padRatios=padRatios, pads=[])
      cSave, cMain, cRatio = 0, 1, 2   # indices of the main canvas, lower canvas and canvas to be saved
      canvs[cSave].SetRightMargin(0.03)
      canvs[cMain].SetRightMargin(0.03)
      canvs[cRatio].SetRightMargin(0.03)
      #canvs[cMain].SetLeftMargin(15) 
  
   else:
      canvs = ROOT.TCanvas("Canvas", "Canvas", 800, 800), None, None
      cSave, cMain = 0, 0
  
   canvs[cMain].cd()
   plot.Draw(dOpt) 

   if type(plot) == ROOT.THStack:
      errBarHist = plot.GetStack().Last().Clone()
      errBarHist.SetFillColor(ROOT.kBlue-5)
      errBarHist.SetFillStyle(3001)
      errBarHist.SetMarkerSize(0)
      errBarHist.Draw("E2same")
      ret['junk'].append(errBarHist)

   canvs[cMain].RedrawAxis()
   canvs[cMain].Modified()
   canvs[cMain].Update()
   
   #if isDataPlot:
   #    dataHist=hists[dataList[0]][p]
   #    dataHist.SetMarkerSize(0.9)
   #    dataHist.SetMarkerStyle(20)
   #    dataHist.Draw("E0Psame")
   #    dOpt+=""
   
   if plotMin: plot.SetMinimum(plotMin)
   
   if legend:
      if type(legend) != type([]): legend = [legend]

      ret['leg'] = []
      
      for leg in legend:
         leg_ = leg.Clone() 
         leg_.Draw()
   
         ret['leg'].append(leg_)
   
   if drawRatio:
      canvs[cRatio].cd() 
      canvs[cRatio].SetGridx() 
      canvs[cRatio].SetGridy() 
      

      if type(ratio) == type(()): 
         num = ratio[0].Clone()
         den = ratio[1].Clone()     

         if type(num) == ROOT.THStack: num = num.GetStack().Last().Clone()
         if type(den) == ROOT.THStack: den = den.GetStack().Last().Clone()
         
         num.Sumw2()
         den.Sumw2()

         ratioPlot = num 

         ratioPlot.Divide(den)

      else:
         ratioPlot = ratio.Clone()
 
      ratioPlot.SetFillColor(ROOT.kBlue-8)
      ratioPlot.SetFillStyle(3003)
      ratioPlot.SetMarkerColor(1)
      ratioPlot.SetMarkerStyle(20)
      ratioPlot.SetMarkerSize(1)
      ratioPlot.SetLineWidth(2)
      ratioPlot.Draw("E2") #adds shaded area around error bars
      ratioPlot.Draw("same")
      
      decorAxis(ratioPlot, 'y', ratioTitle, tOffset = 0.6, tSize = 0.1, lSize = 0.08, center = True)
      ret['ratio'] = ratioPlot 
     
      if ratioLimits:
         ratioPlot.SetMinimum(ratioLimits[0])
         ratioPlot.SetMaximum(ratioLimits[1])
   
      if unity:
         lowBin = ratioPlot.GetBinLowEdge(1)
         hiBin  = ratioPlot.GetBinLowEdge(ratioPlot.GetNbinsX()+1)

         func = ROOT.TF1('Func_%s'%uniqueHash(),"[0]",lowBin,hiBin)
         func.SetParameter(0,1)
         #func.SetLineStyle(3)
         func.SetLineColor(1)
         func.SetLineWidth(2)
         func.Draw("same")
         ret['junk'].append(func)
 
      canvs[cRatio].RedrawAxis()
      canvs[cRatio].Modified()
      canvs[cRatio].Update()
   
   canvs[cMain].cd()
   
   if decor:
      if decor.has_key("x"):
         if drawRatio: 
            decorAxis(ratioPlot, 'x', decor['x'], tOffset = 1, tSize = 0.11, lSize = 0.1, center = False)
         else:
            decorAxis(plot, 'x', decor['x'], tOffset = 0.9, tSize = 0.11, center = False)

      if decor.has_key("y"): decorAxis(plot, 'y', decor['y'], tOffset = 0.9, tSize = 0.06)
      if decor.has_key("title"): plot.SetTitle(decor['title'])
      if decor.has_key("log"):
         logx, logy, logz = decor['log']
         if logx : canvs[cMain].SetLogx(1)
         if logy : canvs[cMain].SetLogy(1)
      else:
         logx, logy, logz = 0, 0, 0
  
      if logy:
         plot.SetMaximum(10*plot.GetMaximum())
      else:
         plot.SetMaximum(1.3*plot.GetMaximum())
   
   latex = ROOT.TLatex()
   latex.SetNDC()
   latex.SetTextSize(0.04)
   #latex.SetTextAlign(11)
   
   if not latexText:
      latexText = {}
      latexText['R'] = "\\mathrm{13\, TeV}"
      if isDataPlot: 
         latexText['L'] = "#font[22]{CMS Preliminary}"
      else:
         latexText['L'] = "#font[22]{CMS Simulation}"
       
   if isDataPlot or ratio:
      latex.DrawLatex(0.16,0.92, latexText['L'])
      latex.DrawLatex(0.7,0.92,  latexText['R'])
   else:
      latex.DrawLatex(0.16,0.96, latexText['L'])
      latex.DrawLatex(0.6,0.96,  latexText['R'])

   for c in canvs:      
      c.Modified()
      c.Update()
      
   #canvs[cSave].cd() 
   ret['plot'] = plot 
   ret['canvs'] = canvs

   ROOT.gPad.Modified()
   ROOT.gPad.Update()
 
   return ret

# Histograms
def emptyHist(title, nbins = 100, min = 0, max = 1000):
   hist = ROOT.TH1D("hist_"+title, "Histogram", nbins, min, max)
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

def makeHistVarBins(sample, varname, sel, xbins, variableBinning = (False, 0)): 
   hist = ROOT.TH1D("hist", "Histogram", len(xbins)-1, array('d', xbins))
   sample.Draw(varname + ">>hist", sel, "goff")

   if variableBinning[0]: 
      if variableBinning[1]: hist.Scale(variableBinning[1], "width") #scales each bin to value and wrt. bin width 
      else:                  hist.Scale(xbins[1]-xbins[0],  "width") #scales each bin to first bin width and wrt. bin width
 
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

def empty2Dhist(nbins1 = 100, min1 = 0, max1 = 1000, nbins2 = 100, min2 = 0, max2 = 1000):
   hist = ROOT.TH2D("hist", "Histogram", nbins1, min1, max1, nbins2, min2, max2)
   hist.GetZaxis().SetTitle("Events")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   hist.GetZaxis().CenterTitle()
   hist.GetXaxis().SetTitleOffset(1.2) 
   hist.GetYaxis().SetTitleOffset(1.2) 
   hist.GetZaxis().SetTitleOffset(1.2) 
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

def divideHists(passed,total): #When ratio > 1
   a = passed.Clone()
   b = total.Clone()
   a.Divide(b)
   a.SetTitle("Efficiency Plot")
   a.SetName("ratio")
   #a.SetMarkerStyle(33)
   #a.SetMarkerSize(2)
   #a.SetLineWidth(2)
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
   
      #print 'i: ', i, 'a: ', a, 'w: ', w
   
      v1 = h1.GetBinContent(i+1)
      e1 = h1.GetBinError(i+1)
      
      v2 = h2.GetBinContent(i+1)
      e2 = h2.GetBinError(i+1)
      
      #print 'v1: ', v1, 'e1: ', e1, 'v2: ', v2, 'e2: ', e2
      
      v = v1*v2
      
      if v == 0: 
         e = 0. 
      else:
         e = v*math.sqrt(pow(e1/v1,2)+pow(e2/v2,2))
      
      #print 'Value : ', v, '+=: ', e
      
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

def unity(hist):# unity histogram
   unity = hist.Clone()
   unity.Reset()

   nBins = unity.GetNbinsX()
   for i in range(nBins):
      unity.SetBinContent(i+1,1)
   return unity

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

##Variable bin size
#nSec = 3
#lenSec = (max - min)/nSec
#bins = []
#for l in [range(min + (x-1)*lenSec, min + x*lenSec, 2*i) for x in range(1, nSec+1)]: bins += map(float,l)
#xbins = array('d', bins)
