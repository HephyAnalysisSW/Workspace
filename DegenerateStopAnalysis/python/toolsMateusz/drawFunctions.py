#drawFunctions.py - ROOT Draw Functions
import ROOT
import hashlib
import time
from math import sqrt
from array import array
from Workspace.DegenerateStopAnalysis.tools.ratioTools import makeCanvasMultiPads
from Workspace.DegenerateStopAnalysis.tools.degTools import decorAxis, setup_style 
from Workspace.HEPHYPythonTools import u_float

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

def drawPlot(plot_, dataHist = None, lumi = None, dOpt="hist", legend = None, decor = False, latexText = None, plotMin=None, plotMax=None, normalize=False, ratio = (None, None), ratioTitle = "Ratio", ratioLimits=[0, 2], unity = True, drawSysErr = None): #ratioNorm=False, verbose=False, 
   setup_style()
   ret = {}
   ret['junk'] = []

   plot = plot_.Clone()

   if ratio: 
      drawRatio = type(ratio) != type(()) or (ratio[0] and ratio[1])
   elif dataHist:
      drawRatio = True
   else:
      drawRatio = False

   if drawRatio:
      padRatios=[2,1]
      #else:
      #    padRatios=[2]+[1]*(len(den))
     
      canvs = makeCanvasMultiPads(c1Name = "Canvas_" + plot.GetName(), c1ww=800, c1wh=800, joinPads=True, padRatios=padRatios, pads=[])
      cSave, cMain, cRatio = 0, 1, 2   # indices of the main canvas, lower canvas and canvas to be saved
      canvs[cSave].SetRightMargin(0.03)
      canvs[cMain].SetRightMargin(0.03)
      canvs[cRatio].SetRightMargin(0.03)
      #canvs[cMain].SetLeftMargin(15) 
  
   else:
      canvs = ROOT.TCanvas("Canvas_" + plot.GetName(), "Canvas_" + plot.GetName(), 800, 800), None, None
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
   
   #if plotMin or plotMax:
   #   if type(plot) == ROOT.THStack:
   #      if not plotMin: plotMin = 0.1
   #      if plotMax:
   #         plot.GetYaxis().SetRangeUser(plotMin,plotMax)
   #   else:
   if plotMin: plot.SetMinimum(plotMin)
   if plotMax: plot.SetMaximum(plotMax)

   canvs[cMain].RedrawAxis()
   canvs[cMain].Modified()
   canvs[cMain].Update()
   
   if dataHist:
       dataHist.SetMarkerSize(0.9)
       dataHist.SetMarkerStyle(20)
       dataHist.Draw("E0Psame")
  
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

      if ratio and type(ratio) != type(()):    
         ratioPlot = ratio.Clone()
      else:
         if type(ratio) == type(()): 
            num = ratio[0].Clone()
            den = ratio[1].Clone()     
         elif dataHist:
            ratioTitle = "data/MC"
            num = dataHist.Clone()
            den = plot.Clone()

         if type(num) == ROOT.THStack: num = num.GetStack().Last().Clone()
         if type(den) == ROOT.THStack: den = den.GetStack().Last().Clone()
         
         num.Sumw2()
         den.Sumw2()

         ratioPlot = num 

         ratioPlot.Divide(den)
 
      ratioPlot.SetFillColor(ROOT.kBlue-8)
      ratioPlot.SetFillStyle(3003)
      ratioPlot.SetMarkerColor(1)
      ratioPlot.SetMarkerStyle(20)
      ratioPlot.SetMarkerSize(1)
      ratioPlot.SetLineWidth(2)
      ratioPlot.Draw("E2") #adds shaded area around error bars
      ratioPlot.Draw("Esame")

      #if addSysErr:
      #   n = finalHists['estimate'].GetNbinsX()

      #   #w1 = finalHists['estimate'][basePlot].GetBinWidth(1)

      #   TF = {}
      #   est = {}
      #   est_err = {}

      #   for i in range(n):
      #      i += 1
      #      a = finalHists['estimate'].GetBinLowEdge(i)
      #      w = finalHists['estimate'].GetBinWidth(i)

      #   finalHists['estimate'].SetBinContent(i, est[str(i)])
      #   finalHists['estimate'].SetBinError(i, est_err[str(i)])
 
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
 
      if not plotMax: 
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
      if lumi: 
         latexText['R'] = "\\mathrm{%0.1f\, fb^{-1} (13\, TeV)}"%(round(lumi/1000.,2))
      else:
         latexText['R'] = "\\mathrm{13\, TeV}"
      if dataHist: 
         latexText['L'] = "#font[22]{CMS Preliminary}"
      else:
         latexText['L'] = "#font[22]{CMS Simulation}"
       
   if dataHist or ratio:
      latex.DrawLatex(0.16,0.92, latexText['L'])
      latex.DrawLatex(0.7,0.92,  latexText['R'])
   else:
      latex.DrawLatex(0.16,0.96, latexText['L'])
      latex.DrawLatex(0.6,0.96,  latexText['R'])

   for c in canvs:
      if c: 
         c.Modified()
         c.Update()
      
   #canvs[cSave].cd() 
   ret['plot'] = plot 
   ret['canvs'] = canvs

   ROOT.gPad.Modified()
   ROOT.gPad.Update()
 
   return ret

def getHistContents(hist_, varBinsYield = False):

   hist = hist_.Clone()
   
   a = {}
   w = {}  

   value = {}
   error = {}
   uFloat = {}
 
   n = hist.GetNbinsX()

   for i in range(n):
      i += 1
      a[i] = hist.GetBinLowEdge(i)
      w[i] = hist.GetBinWidth(i)

      if not varBinsYield: # Simply gets bin contents
         value[i] = hist.GetBinContent(i)
         error[i] = hist.GetBinError(i)
         uFloat[i] = u_float.u_float(value[i], error[i])
      else: # Gets yield by multiplying by the reciprocal of the variable bin normalisation factor 
         if i == 1: w1 = hist.GetBinWidth(1) # NOTE: assumes variable bins normalised to first bin
         value[i] = hist.GetBinContent(i)*w[i]/w1
         error[i] = hist.GetBinError(i)*w[i]/w1
         uFloat[i] = u_float.u_float(value[i], error[i])

   return uFloat, a, w

def setErrSqrtN(hist, varBins = False):
   n = hist.GetNbinsX()

   val = {}
   err = {}
   newErr = {}
   
   a = {}
   w = {}
   A = {}

   for i in range(n):
      i += 1

      if varBins:
         a[i] = hist.GetBinLowEdge(i)
         w[i] = hist.GetBinWidth(i)

      val[i] = hist.GetBinContent(i+1)
      err[i] = hist.GetBinError(i+1)

      #print "Bin: ", i
      #print "Value: ", val[i]
      #print "Error: ", err[i]
      
      if not varBins:
         newErr[i] = sqrt(val[i]) #sqrt(N)
      else: 
         if i == 1: w1 = hist.GetBinWidth(1) # NOTE: assumes variable bins normalised to first bin
         A[i] = w[i]/w1
         #print "A: ", A[i]
         if A[i] > 0. and val[i] > 0.:
            newErr[i] = sqrt((val[i]/A[i])) #sqrt(N/A) where A = variable bins normalisation factor
            hist.SetBinError(i+1, newErr[i])
         else:
            print "Value or A <= 0. Keeping error unchanged." 
            #newErr[i] = 0.

      #print "New error: ", hist.GetBinError(i+1)

   return

def setErrZero(hist):
   n = hist.GetNbinsX()

   val = {}
   err = {}
   newErr = {}

   for i in range(n):
      #a = int(hist.GetBinLowEdge(i+1))
      #w = int(hist.GetBinWidth(i+1))

      val[i] = hist.GetBinContent(i+1)
      err[i] = hist.GetBinError(i+1)

      #print "Bin: ", i
      #print "Value: ", val[i]
      #print "Error: ", err[i]

      newErr[i] = 0. #sqrt(N)

      hist.SetBinError(i+1, newErr[i])

      #print "New error: ", hist.GetBinError(i+1)

   return

def getHistContents(hist_, varBinsYield = False):

   hist = hist_.Clone()
   
   a = {}
   w = {}  

   value = {}
   error = {}
   uFloat = {}
 
   n = hist.GetNbinsX()

   for i in range(n):
      i += 1
      a[i] = hist.GetBinLowEdge(i)
      w[i] = hist.GetBinWidth(i)

      if not varBinsYield: # Simply gets bin contents
         value[i] = hist.GetBinContent(i)
         error[i] = hist.GetBinError(i)
         uFloat[i] = u_float.u_float(value[i], error[i])
      else: # Gets yield by multiplying by the reciprocal of the variable bin normalisation factor 
         if i == 1: w1 = hist.GetBinWidth(1) # NOTE: assumes variable bins normalised to first bin
         value[i] = hist.GetBinContent(i)*w[i]/w1
         error[i] = hist.GetBinError(i)*w[i]/w1
         uFloat[i] = u_float.u_float(value[i], error[i])

   return uFloat, a, w

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

def makeHist(sample, varname, sel = "", nbins = 100, min = 0, max = 1000, addOverFlowBin = ''):
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
  
   res = hist.Clone()
   hist.Delete()
   del hist
 
   if addOverFlowBin.lower() == "upper" or addOverFlowBin.lower() == "both":
      nbins = res.GetNbinsX()
      res.SetBinContent(nbins, res.GetBinContent(nbins) + res.GetBinContent(nbins + 1))
      res.SetBinError(nbins, sqrt(res.GetBinError(nbins)**2 + res.GetBinError(nbins + 1)**2))
   if addOverFlowBin.lower() == "lower" or addOverFlowBin.lower() == "both":
      res.SetBinContent(1, res.GetBinContent(0) + res.GetBinContent(1))
      res.SetBinError(1, sqrt(res.GetBinError(0)**2 + res.GetBinError(1)**2))

   return res

def makeHistVarBins(sample, varname, sel, xbins, variableBinning = (False, 0), addOverFlowBin = ''): 
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
   
   res = hist.Clone()
   hist.Delete()
   del hist
 
   if addOverFlowBin.lower() == "upper" or addOverFlowBin.lower() == "both":
      nbins = res.GetNbinsX()
      res.SetBinContent(nbins, res.GetBinContent(nbins) + res.GetBinContent(nbins + 1))
      res.SetBinError(nbins, sqrt(res.GetBinError(nbins)**2 + res.GetBinError(nbins + 1)**2))
   if addOverFlowBin.lower() == "lower" or addOverFlowBin.lower() == "both":
      res.SetBinContent(1, res.GetBinContent(0) + res.GetBinContent(1))
      res.SetBinError(1, sqrt(res.GetBinError(0)**2 + res.GetBinError(1)**2))

   return res

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
   hist = ROOT.TH2D("hist", "Histogram", len(xbins)-1, array('d', xbins), len(ybins)-1, array('d', ybins))
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
   a.Sumw2()
   b.Sumw2()
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
   #leg.SetHeader("#bf{Legend}")
   #header = leg.GetListOfPrimitives().First()
   #header.SetTextAlign(22)
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
          u = v*sqrt(pow(u1/v1,2)+pow(u2/v2,2))
          d = v*sqrt(pow(d1/v1,2)+pow(d2/v2,2))
      
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
         e = v*sqrt(pow(e1/v1,2)+pow(e2/v2,2))
      
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
      e = sqrt(pow(e1,2)+pow(sys/100.*v1,2))
      
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
#          u = v*sqrt(pow(u1/v1,2)+pow(u2/v2,2))
#          d = v*sqrt(pow(d1/v1,2)+pow(d2/v2,2))
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
