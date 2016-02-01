#redMassTotal.py
import ROOT
import os, sys
#import math
#import copy
#import subprocess
#from optparse import OptionParser
#from DataFormats.FWLite import Events, Handle

#from Workspace.HEPHYPythonTools.helpers import getChain#, getPlotFromChain, getYieldFromChain, getChunks

#ROOT Options
ROOT.gROOT.Reset() #re-initialises ROOT
#ROOT.gROOT.SetStyle("Plain")

ROOT.gStyle.SetOptStat(11) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptFit(1111) #1111 prints fits results on plot
#ROOT.gStyle.SetTitleX(0.15)
#ROOT.gStyle.SetFuncWidth(1)
#ROOT.gStyle.SetFuncColor(9)
#ROOT.gStyle.SetLineWidth(2)
#ROOT.gStyle.SetOptTitle(0) #suppresses title box

ROOT.gStyle.SetPaintTextFormat("4.2f")
#ROOT.gStyle->SetTitleX(0.1)
#ROOT.gStyle->SetTitleW(0.8)

ROOT.gStyle.SetStatX(0.885)
ROOT.gStyle.SetStatW(0.06)
ROOT.gStyle.SetStatY(0.80)
ROOT.gStyle.SetStatH(0.15)

def makeLine():
   line = "\n**********************************************************************************************************************************\n"
   return line

#def makeDoubleLine():
#   line = "\n**********************************************************************************************************************************\n\
#**********************************************************************************************************************************\n"
#   return line
#
#def newLine():
#   print ""
#   return 
#

##Selection function
#def select(varname, cut, option): #option = {>, =, <}
#   sel = "abs(" + varname + option + str(cut) + ")"
#   return sel

#Creates Legend
def makeLegend():
   leg = ROOT.TLegend(0.60,0.70,0.75,0.85)
   leg.SetHeader("#bf{Legend}")
   header = leg.GetListOfPrimitives().First()
   header.SetTextAlign(22)
   return leg 

#Creates Box 
def makeBox():
   box = ROOT.TPaveText(0.775,0.40,0.875,0.65, "NDC") #NB & ARC
   #box.SetHeader("Cuts")
   #header = box.GetListOfPrimitives().First()
   #header.SetTextAlign(22)
   return box 

#def alignStats(hist):
#   st = hist.FindObject("stats")
#   st.SetX1NDC(0.675)
#   st.SetX2NDC(0.775)
#   st.SetY1NDC(0.75)
#   st.SetY2NDC(0.85)

#Cuts 
cuts=({\
'MET' : 120, #MET cut (fixed)
'HT' : 200, #HT cut (fixed)
'HTjetPt' : 40, #Jet pt threshold for HT (fixed)
'HTjetEta' : 3, #Jet eta cut for HT (fixed)

'genMET' : 60, #generated quantity cuts
'genHT' : 160,
'genHTjetPt' : 30, #GenJet pt threshold for HT
'genHTjetEta' : 5 #GenJet eta cut for HT
})

cutString = \
"Preselection cuts: \n\n" + \
"MET cut: " + str(cuts['MET']) + "\n" + \
"HT cut: " + str(cuts['HT']) + "\n" + \
"HT Jets pT cut: " + str(cuts['HTjetPt']) + "\n" + \
"HT Jets eta cut: " + str(cuts['HTjetEta']) + "\n\n" + \
"Generator cuts:" + "\n\n" + \
"Generated MET cut: " + str(cuts['genMET']) + "\n" + \
"Generated HT cut: " + str(cuts['genHT']) + "\n" + \
"Generated HT Jets pT cut: " + str(cuts['genHTjetPt']) + "\n" + \
"Generated HT Jets eta cut: " + str(cuts['genHTjetEta'])

print makeLine()
print cutString
print makeLine()

dir = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/8TeV/HT/genHTonly/filter_%s_%s/"%(str(cuts["genMET"]),str(cuts["genHT"]))

massRanges = ["100to150", "175to225", "250to300", "325to375", "400"]

#Gets root files
files = []

for i in range(1,19):
   files.append(ROOT.TFile(dir + massRanges[0] + "/redMassScanHTonly_%s_%s_"%(str(cuts["genMET"]),str(cuts["genHT"])) + str(i) + ".root", "read"))

for i in range(19,33):
   files.append(ROOT.TFile(dir + massRanges[1] + "/redMassScanHTonly_%s_%s_"%(str(cuts["genMET"]),str(cuts["genHT"])) + str(i) + ".root", "read"))

for i in range(33,44):
   files.append(ROOT.TFile(dir + massRanges[2] + "/redMassScanHTonly_%s_%s_"%(str(cuts["genMET"]),str(cuts["genHT"])) + str(i) + ".root", "read"))

for i in range(44,57):
   files.append(ROOT.TFile(dir + massRanges[3] + "/redMassScanHTonly_%s_%s_"%(str(cuts["genMET"]),str(cuts["genHT"])) + str(i) + ".root", "read"))

for i in range(57,62):
   files.append(ROOT.TFile(dir + massRanges[4] + "/redMassScanHTonly_%s_%s_"%(str(cuts["genMET"]),str(cuts["genHT"])) + str(i) + ".root", "read"))

#Get histograms and add them
total = ROOT.TH2F("total", "Total Counts", 80, 50, 450, 18, 0, 90)
passed = ROOT.TH2F("passed", "Passed Counts", 80, 50, 450, 18, 0, 90)

for file in files: 
   #print file
   file.ls()
   h1 = file.Get("c1").GetPrimitive("c1_1").GetPrimitive("h1")
   h2 = file.Get("c1").GetPrimitive("c1_2").GetPrimitive("h2")
   total.Add(h1,1)
   passed.Add(h2,1)
#files[1].ls()

#total = files[1].Get("h1")
#passed = files[1].Get("h2")

#Drawing 2D Histograms
   
c1 = ROOT.TCanvas("c1", "Total and Passed Counts", 1800, 1500)
c1.Divide(1,2)

c1.SetGrid() #adds a grid to the canvas
##c1.SetFillColor(42)
#c1.GetFrame().SetFillColor(21)
#c1.GetFrame().SetBorderSize(12)

c1.cd(1)
total.SetTitle("Generated H_{T} Filter: Total Number of Events per Mass Point for  genHT > " + str(cuts['genHT']) + " GeV")
total.GetXaxis().SetTitle("Stop Mass / GeV")
total.GetYaxis().SetTitle("#Deltam_{stop,LSP} / GeV")
total.GetZaxis().SetTitle("Counts")
#total.GetXaxis().SetTitleOffset(1.1)
#total.GetYaxis().SetTitleOffset(1.1)
#total.GetZaxis().SetTitleOffset(1.1)
total.GetXaxis().CenterTitle()
total.GetYaxis().CenterTitle()
total.GetZaxis().CenterTitle()
#total.GetYaxis().SetRangeUser(0, 500)
#total.GetXaxis().SetRangeUser(0, 500)
total.GetZaxis().SetRangeUser(0, 5000000)
#total.SetAxisRange(0, 1000, "X")
#total.SetAxisRange(0, 2E6, "Y") #automatically calls SetMin-/Max-imum()
#total.SetMinimum(0)
#total.SetMaximum(2E7)
total.Draw("COLZ") #CONT1-5 #plots the graph with axes and points

ROOT.gPad.SetLogz()
ROOT.gPad.Update()

#alignStats(total)

c1.cd(2)
passed.SetTitle("Generated H_{T} Filter: Passed Generator Filter Events per Mass Point for genHT > " + str(cuts['genHT']) + " GeV")
passed.GetXaxis().SetTitle("Stop Mass / GeV")
passed.GetYaxis().SetTitle("#Deltam_{stop,LSP} / GeV")
passed.GetZaxis().SetTitle("Counts")
#passed.GetXaxis().SetTitleOffset(1.1)
#passed.GetYaxis().SetTitleOffset(1.1)
#passed.GetZaxis().SetTitleOffset(1.1)
passed.GetXaxis().CenterTitle()
passed.GetYaxis().CenterTitle()
passed.GetZaxis().CenterTitle()
#passed.GetYaxis().SetRangeUser(0, 500)
#passed.GetXaxis().SetRangeUser(0, 500)
passed.GetZaxis().SetRangeUser(0, 5000000)
#passed.SetAxisRange(0, 1000, "X")
#passed.SetAxisRange(0, 2E6, "Y") #automatically calls SetMin-/Max-imum()
#passed.SetMinimum(0)
#passed.SetMaximum(2E7)
passed.Draw("COLZ") #CONT1-5 #plots the graph with axes and points

ROOT.gPad.SetLogz()
ROOT.gPad.Update()

#alignStats(passed)

#Reduction factor as a function of mass point
c2 = ROOT.TCanvas("c2", "Reduction Factor", 1800, 1500)
c2.Divide(1,2)

c2.SetGrid()
#c2.SetFillColor(42)
c2.GetFrame().SetFillColor(21)
c2.GetFrame().SetBorderSize(12)

c2.cd(1)
redFactor = ROOT.TH2F("redFactor", "Generated H_{T} Filter: Reduction Factor per Mass Point Map for genHT > " + str(cuts['genHT']) + " GeV", 80, 50, 450, 18, 0, 90)
redFactor.Divide(total, passed) #quotient
redFactor.GetXaxis().SetTitle("Stop Mass / GeV")
redFactor.GetYaxis().SetTitle("#Deltam_{stop,LSP} / GeV")
redFactor.GetZaxis().SetTitle("Reduction Factor")
#redFactor.GetXaxis().SetTitleOffset(1.1)
#redFactor.GetYaxis().SetTitleOffset(1.1)
#redFactor.GetZaxis().SetTitleOffset(1.1)
redFactor.GetXaxis().CenterTitle()
redFactor.GetYaxis().CenterTitle()
redFactor.GetZaxis().CenterTitle()
#redFactor.GetYaxis().SetRangeUser(0, 500)
#redFactor.GetXaxis().SetRangeUser(0, 500)
#redFactor.GetZaxis().SetRangeUser(0, 10)
#redFactor.SetAxisRange(0, 1000, "X")
#redFactor.SetAxisRange(0, 2E6, "Y") #automatically calls SetMin-/Max-imum()
#redFactor.SetMinimum(0)
#redFactor.SetMaximum(2E7)
redFactor.Draw("COLZTEXT") #CONT1-5 #plots the graph with axes and points

#ROOT.gPad.SetLogz()
ROOT.gPad.Update()

#alignStats(redFactor)

#Plot of reduction factor vs mass point

stopMs = range(100,401,25)
deltaMs = range(10,81,10)
LSPMs = [stopM-deltaM for stopM in stopMs for deltaM in deltaMs]

massPoints = [str(stopM) + "_"+ str(stopM-deltaM) for stopM in stopMs for deltaM in deltaMs]

redFactors = []

for stopM in stopMs: 
   for deltaM in deltaMs:
      #print "Mass point: (",stopM,",",stopM-deltaM,")"
      redFactors.append(redFactor.GetBinContent(stopM/5-10+1,deltaM/5+1)) #5 GeV binsize, 10 bins offset

#for i in massPoints: print i #check consistency

c2.cd(2)
redFactorPlot = ROOT.TH1F("redFactorPlot", "Generated H_{T} Filter: Reduction Factor vs. Mass Point Plot for genHT > " + str(cuts['genHT']) + " GeV", 105, 0, 105)
#redFactorPlot.SetTitle("Reduction Factor vs. Mass Point")
redFactorPlot.GetXaxis().SetTitle("Mass Point")
redFactorPlot.GetYaxis().SetTitle("Reduction Factor")
redFactorPlot.GetXaxis().SetTitleOffset(2)
#redFactorPlot.GetYaxis().SetTitleOffset(1.1)
redFactorPlot.GetXaxis().CenterTitle()
redFactorPlot.GetYaxis().CenterTitle()
#redFactorPlot.GetYaxis().SetRangeUser(0, 500)
#redFactorPlot.GetXaxis().SetRangeUser(0, 500)
#redFactorPlot.SetAxisRange(0, 1000, "X")
#redFactorPlot.SetAxisRange(0, 2E6, "Y") #automatically calls SetMin-/Max-imum()
#redFactorPlot.SetMinimum(0)
#redFactorPlot.SetMaximum(2E7)
redFactorPlot.SetMarkerColor(ROOT.kBlue)
redFactorPlot.SetMarkerStyle(ROOT.kFullCircle)
redFactorPlot.SetMarkerSize(1)
redFactorPlot.GetXaxis().SetNdivisions(560,0)
#redFactorPlot.GetYaxis()->SetTicks("-"); //sets x-axis ticks
ROOT.gPad.SetGrid() #adds a grid to the canvas
redFactorPlot.SetStats(0)

for i in range(1,len(stopMs)*len(deltaMs)+1):
   redFactorPlot.SetBinContent(i, redFactors[i-1])
   redFactorPlot.GetXaxis().SetBinLabel(i, massPoints[i-1])#.c_str())

redFactorPlot.Draw("P") #b, bar, bar0, bar1, bar2, bar3, bar4

ROOT.gPad.Update()

#alignStats(redFactorPlot)

#Separate plots
c3 = ROOT.TCanvas("c3", "Reduction Factor 1", 1800, 1500)

c3.SetGrid()
#c3.SetFillColor(42)
c3.GetFrame().SetFillColor(21)
c3.GetFrame().SetBorderSize(12)

redFactor.Draw("COLZTEXT")

#Reduction factor as a function of mass point
c4 = ROOT.TCanvas("c4", "Reduction Factor 2", 1800, 1500)

c4.SetGrid()
#c4.SetFillColor(42)
c4.GetFrame().SetFillColor(21)
c4.GetFrame().SetBorderSize(12)

redFactorPlot.Draw("P")

#Write to file
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/8TeV/HT/genHTonly/filter_%s_%s/"%(str(cuts["genMET"]),str(cuts["genHT"])) #web directory http://www.hephy.at/user/mzarucki/plots/filter/

if not os.path.exists(savedir):
   os.makedirs(savedir)

c1.SaveAs(savedir + "redMassScanTotal1_gHT_%s"%(str(cuts['genHT'])) + ".root")
c1.SaveAs(savedir + "redMassScanTotal1_gHT_%s"%(str(cuts['genHT'])) + ".png")
c1.SaveAs(savedir + "redMassScanTotal1_gHT_%s"%(str(cuts['genHT'])) + ".pdf")

c2.SaveAs(savedir + "redMassScanTotal2_gHT_%s"%(str(cuts['genHT'])) + ".root")
c2.SaveAs(savedir + "redMassScanTotal2_gHT_%s"%(str(cuts['genHT'])) + ".png")
c2.SaveAs(savedir + "redMassScanTotal2_gHT_%s"%(str(cuts['genHT'])) + ".pdf")

c3.SaveAs(savedir + "redMassScanTotalMap_gHT_%s"%(str(cuts['genHT'])) + ".root")
c3.SaveAs(savedir + "redMassScanTotalMap_gHT_%s"%(str(cuts['genHT'])) + ".root")
c3.SaveAs(savedir + "redMassScanTotalMap_gHT_%s"%(str(cuts['genHT'])) + ".png")

c4.SaveAs(savedir + "redMassScanTotalPlot_gHT_%s"%(str(cuts['genHT'])) + ".pdf")
c4.SaveAs(savedir + "redMassScanTotalPlot_gHT_%s"%(str(cuts['genHT'])) + ".png")
c4.SaveAs(savedir + "redMassScanTotalPlot_gHT_%s"%(str(cuts['genHT'])) + ".pdf")
