#turnon.py - Imported by filter.py. Plots turn-on curves for MET and ISR pt, as a function of genMET and genISRpt cuts.

def main(genMETcut, genISRcut): #main function to be imported by filter.py.
   print "\nImporting and executing turnon.py script..."
    
   import ROOT
   import os, sys
   
   from Workspace.HEPHYPythonTools.helpers import getChain#, getPlotFromChain, getYieldFromChain, getChunks
   
   #ROOT Options
   ROOT.gROOT.Reset() #re-initialises ROOT
   #ROOT.gROOT.SetStyle("Plain")
   
   ROOT.gStyle.SetOptStat(1111) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
   ROOT.gStyle.SetOptFit(1111) #1111 prints fits results on plot
   #ROOT.gStyle.SetOptTitle(0) #suppresses title box
   #ROOT.gStyle.SetFuncWidth(1)
   #ROOT.gStyle.SetFuncColor(9)
   #ROOT.gStyle.SetLineWidth(2)
   
   ROOT.gStyle.SetPaintTextFormat("4.2f")
   #ROOT.gStyle->SetTitleX(0.1)
   #ROOT.gStyle->SetTitleW(0.8)
   
   ROOT.gStyle.SetStatX(0.75)
   ROOT.gStyle.SetStatY(0.65)
   ROOT.gStyle.SetStatW(0.1)
   ROOT.gStyle.SetStatH(0.15)
   
   
   def makeLine():
      line = "\n************************************************************************************************************************************************************************\n"
      return line
   
   def makeDoubleLine():
      line = "\n************************************************************************************************************************************************************************\n\
************************************************************************************************************************************************************************\n"
      return line
   
   def newLine():
      print ""
      return 
   
   #13 TeV Signal Sample 
   dir = "/afs/hephy.at/work/n/nrad/cmgTuples/RunII/T2DegStop_300_270_RunII_withMotherRef"
   
   signal=({\
   "name" : "treeProducerSusySingleLepton",
   "bins" : ["treeProducerSusySingleLepton"],
   "dir" : dir
   })
   
   T2DegSample = getChain(signal, histname='',treeName="tree")
   
   print makeLine()
   print "Sample: ", signal['name']
   print makeLine()
   
   def drawhist(sample, varname, sel, nbins = 100, min = 0, max = 1000):
      hist = ROOT.TH1F("hist", "Histogram", nbins, min, max)
      sample.Draw(varname + ">>hist", sel, "goff")
      hist.SetTitle(varname + " Plot")
      hist.GetXaxis().SetTitle(varname + "/ GeV")
      hist.GetYaxis().SetTitle("Counts")
      hist.GetXaxis().CenterTitle()
      hist.GetYaxis().CenterTitle()
      return hist 
   
   #Selection function
   def select(varname, cut, option): #option = {>, =, <}
     if option == ">" or options == "=" or option == "<": 
         sel = "abs(" + varname + option + str(cut) + ")"
     return sel
   
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
   
   def alignStats(hist):
      st = hist.FindObject("stats")
      st.SetX1NDC(0.775)
      st.SetX2NDC(0.875)
      st.SetY1NDC(0.7)
      st.SetY2NDC(0.85)
   
   #Fit Function
   fitFunc = ROOT.TF1("f1", "[0]*TMath::Erf((x-[1])/[2]) + [3]", 0, 1000) #Error function scaled to [0,1]
   fitFunc.SetParNames("Normalisation", "Edge", "Resolution", "Y-Offset")
   #fitFunc.SetParameter(0, 0.5)
   #fitFunc.SetParameter(1, 150)
   #fitFunc.SetParameter(2, 50)  
   #fitFunc.SetParLimits(0, 0.4, 0.65) 
   fitFunc.SetParLimits(1, 0, 200) #init: [0,200]
   fitFunc.SetParLimits(2, 0, 60) #init: [0,60]
   fitFunc.SetParLimits(3, 0.45, 0.8) #init: [0.45,0.8]
  
   #Cuts 
   cuts=({\
   'MET' : 200, #MET cut (fixed)
   'ISR' : 110, #ISRpt cut (fixed)
   'ISReta' : 2.4, #ISReta cut (fixed)
   
   'genMET' : genMETcut, #generated quantity cuts
   'genISRpt' : genISRcut,
   'genISReta' : 2.5 #slightly looser than reco
   })
  
   cutString = \
   "Preselection cuts: \n\n" + \
   "MET cut: " + str(cuts['MET']) + "\n" \
   "ISR Jet pT cut: " + str(cuts['ISR']) + "\n" \
   "ISR Jet Eta cut: " + str(cuts['ISReta']) + "\n\n" + \
   "Generator cuts:" + "\n" + \
   "Generated MET cut: " + str(cuts['genMET']) + "\n" \
   "Generated ISR Jet pT cut: " + str(cuts['genISRpt']) + "\n" \
   "Generated ISR Jet Eta cut: " + str(cuts['genISReta']) 
   
   print makeLine()
   print cutString
   print makeLine()
    
   #Bin size 
   nbins = 100
   min = 0 #GeV
   max = 1000 #GeV
   
   recoBinMET = int(cuts['MET']*nbins/(max - min)) + 1 #cuts['MET']/(h1.GetXaxis().GetBinWidth(0)) # + 1 to get correct bin
   recoBinISR = int(cuts['ISR']*nbins/(max - min)) + 1 #cuts['ISR']/(h1.GetXaxis().GetBinWidth(0))
   
   #Preselection and Generated Particles Filter Selection
   #Variables: met_pt, met_genPt, Jet_pt, GenJet_pt, Jet_eta, GenJet_eta
   
   #MET Selection
   preSel1 = "Max$(Jet_pt*(abs(Jet_eta)<" + str(cuts['ISReta']) + "))" + ">" + str(cuts['ISR']) #MaxIf also option 
   
   genSel1 = select("met_genPt", cuts['genMET'], ">")
   
   #ISR Jet Pt Selection
   preSel2 = select("met_pt", cuts['MET'], ">") 
   
   genSel2 = "Max$(GenJet_pt*(abs(GenJet_eta)<" + str(cuts['genISReta']) + "))" + ">" + str(cuts['genISRpt']) #MaxIf also option
 
  
   ################################################################################Canvas 1: MET 1 (single gen cut)#######################################################################################
  
   print makeDoubleLine()
   print "                                                     MET (single generator cut):"
   print makeDoubleLine()
   
   c1 = ROOT.TCanvas("c1", "MET 1", 1800, 1500)
   c1.Divide(1,2)
   
   var = "met_pt" #Reco MET
   
   c1.cd(1)
   h1 = drawhist(T2DegSample, var, preSel1, nbins, min, max) #ISR preselection cut
   h1.SetName("MET")
   h1.SetTitle("Generated MET Filter Effect on Reconstructed MET")
   h1.GetXaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
   h1.GetXaxis().SetTitleOffset(1.2)
   h1.GetYaxis().SetTitleOffset(1.2)
   h1.Draw()
   h1.SetFillColor(ROOT.kRed+1)
   h1.SetLineColor(ROOT.kBlack)
   h1.SetLineWidth(4)
   
   l1 = makeLegend()
   l1.AddEntry("MET", "MET (no generator cuts)", "F")
   
   ROOT.gPad.SetLogy()
   ROOT.gPad.Update()
   
   alignStats(h1)
   
   h2 = drawhist(T2DegSample, var, preSel1 + "&&" + genSel1) # + genMET cut
   h2.SetName("MET1")
   h2.Draw("same")
   h2.SetFillColor(0)
   h2.SetLineColor(ROOT.kAzure+7)
   h2.SetLineWidth(4)
   
   l1.AddEntry("h2", "MET (generator cut)", "F")
   l1.Draw()
   
   #Efficiency and Reduction Factor Calculation 
   var = "met_genPt" #genMET
   
   h3 = drawhist(T2DegSample, var, "") #no cuts  
   h4 = drawhist(T2DegSample, var, genSel1) #genMET cut
      
   eff1 = h4.GetEntries()/h3.GetEntries()
   red1 = h3.GetEntries()/h4.GetEntries() # = 1/eff
   
   #Number of Inefficiencies
   box1 = makeBox()
   box1.AddText("Cuts:")
   box1.AddText("#bf{ISR Jet p_{T} cut: }" + str(cuts['ISR']) + " GeV")
   box1.AddText("#bf{ISR Jet #eta cut: }" + str(cuts['ISReta']))
   box1.AddText("#bf{Gen. MET p_{T} cut: }" + str(cuts['genMET']) + " GeV")
   box1.AddText("Filter:")
   box1.AddText("#bf{Total Filter Efficiency: }" + str("%0.3f"%eff1))
   box1.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red1))
   box1.Draw()
   
   ROOT.gPad.Update()
   
   #MET Turnon Plot
   c1.cd(2)
   metTurnon1 = ROOT.TEfficiency(h2, h1) #(passed, total)
   metTurnon1.SetTitle("MET Turnon Plot (Single Generator Cut) ; Missing Transverse Energy #slash{E}_{T} / GeV ; Counts")
   metTurnon1.SetMarkerColor(ROOT.kBlue)
   metTurnon1.SetMarkerStyle(33)
   metTurnon1.SetMarkerSize(3)
   metTurnon1.Draw("AP") 
   metTurnon1.SetLineColor(ROOT.kBlack)
   metTurnon1.SetLineWidth(2)
   ROOT.gPad.SetGridx()
   ROOT.gPad.SetGridy()
   ROOT.gPad.Update()
   metTurnon1.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000)
   metTurnon1.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
   metTurnon1.GetPaintedGraph().GetXaxis().CenterTitle()
   metTurnon1.GetPaintedGraph().GetYaxis().CenterTitle()
   
   #Fitting
   fitFunc.SetParameters(0.55, 135, 35, 0.5) #init: (0.5, 140, 40, 0.5)
   metTurnon1.Fit(fitFunc)
   
   print makeLine()
   print "Filter Efficiency: " + str("%0.3f"%eff1)
   print "Reduction Factor: " + str("%0.3f"%red1)
   
   #Efficiency at Reco Cut Level
   recoEff1_bin = metTurnon1.GetEfficiency(recoBinMET)
   recoEff1_fit = fitFunc(cuts['MET'])
   print "Efficiency at Reco MET cut (bin): ", str("%0.3f"%recoEff1_bin)
   print "Efficiency at Reco MET cut (fit): ", str("%0.3f"%recoEff1_fit)
   
   #Fit Parameter Extraction
   fit1 = []
   #fitFunc.GetParameters(fit1)
   fit1.append(fitFunc.GetChisquare())
   for x in xrange(0, 4):
      fit1.append(fitFunc.GetParameter(x))
      fit1.append(fitFunc.GetParError(x))
   
   fit1.append(fitFunc.GetX(0.5))
   fit1.append(fitFunc.GetX(0.75))
   fit1.append(fitFunc.GetX(0.80))
   fit1.append(fitFunc.GetX(0.85))
   fit1.append(fitFunc.GetX(0.90))
   fit1.append(fitFunc.GetX(0.95))
   fit1.append(fitFunc.GetX(0.99))
   fit1.append(fitFunc.GetX(1))
   
   box2 = ROOT.TPaveText(box1)
   box2.AddText("#bf{Efficiency at Reco Cut (bin): }" + str("%0.3f"%recoEff1_bin))
   box2.AddText("#bf{Efficiency at Reco Cut (fit): }" + str("%0.3f"%recoEff1_fit))
   box2.Draw()
   
   c1.Modified()
   c1.Update()
   
   ########################################################################################Canvas 2: MET 2 (both gen cuts)################################################################################ 
   print makeDoubleLine()
   print "                                                       MET (both generator cuts):"
   print makeDoubleLine()
   
   c2 = ROOT.TCanvas("c2", "MET 2", 1800, 1500)
   c2.Divide(1,2)
   
   var = "met_pt" #Reco MET
   
   c2.cd(1)
   h5 = h1.Clone() #same total histogram as MET 1
   h5.SetName("MET")
   h5.SetTitle("Generated MET & ISR Jet p_{T} Filter Effect on Reconstructed MET")
   h5.Draw() 
   h5.SetFillColor(ROOT.kRed+1)
   h5.SetLineColor(ROOT.kBlack)
   h5.SetLineWidth(4)
   
   l2 = makeLegend()
   l2.AddEntry("MET", "MET (no generator cuts)", "F")
   
   ROOT.gPad.SetLogy()
   
   h6 = drawhist(T2DegSample, var, preSel1 + "&&" + genSel1 + "&&" + genSel2) # + ISR generator cuts
   h6.SetName("MET2")
   h6.Draw("same")
   h6.SetFillColor(0)
   h6.SetLineColor(ROOT.kAzure+7)
   h6.SetLineWidth(4)
   
   l2.AddEntry("MET2", "MET (both generator cuts)", "F")
   l2.Draw()
   
   #Efficiency and Reduction Factor Calculation 
   var = "met_genPt" #genMET
   
   h7 = drawhist(T2DegSample, var, "") #no cuts 
   h8 = drawhist(T2DegSample, var, genSel1 + "&&" + genSel2) #both gen cuts
   
   eff2 = h8.GetEntries()/h7.GetEntries()
   red2 = h7.GetEntries()/h8.GetEntries() # = 1/eff
   
   box3 = makeBox()
   box3.AddText("Cuts:")
   box3.AddText("#bf{ISR Jet p_{T} cut: }" + str(cuts['ISR']) + " GeV")
   box3.AddText("#bf{ISR Jet #eta cut: }" + str(cuts['ISReta']))
   box3.AddText("#bf{Gen. MET p_{T} cut: }" + str(cuts['genMET']) + " GeV")
   box3.AddText("#bf{Gen. ISR Jet p_{T} cut: }" + str(cuts['genISRpt']) + " GeV")
   box3.AddText("#bf{Gen. ISR Jet #eta cut: }" + str(cuts['genISReta']))
   box3.AddText("Filter:")
   box3.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff2))
   box3.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red2))
   box3.Draw()
   
   #MET Turnon Plot
   c2.cd(2)
   metTurnon2 = ROOT.TEfficiency(h6, h5) #(passed, total)
   metTurnon2.SetTitle("MET Turnon Plot (Both Generator Cuts) ; Missing Transverse Energy #slash{E}_{T} / GeV ; Counts")
   metTurnon2.SetMarkerColor(ROOT.kBlue)
   metTurnon2.SetMarkerStyle(33)
   metTurnon2.SetMarkerSize(3)
   metTurnon2.Draw("AP") 
   metTurnon2.SetLineColor(ROOT.kBlack)
   metTurnon2.SetLineWidth(2)
   ROOT.gPad.SetGridx()
   ROOT.gPad.SetGridy()
   ROOT.gPad.Update()
   metTurnon2.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000) 
   metTurnon2.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
   metTurnon2.GetPaintedGraph().GetXaxis().CenterTitle()
   metTurnon2.GetPaintedGraph().GetYaxis().CenterTitle()
   
   #Fitting
   metTurnon2.Fit(fitFunc)
   
   print makeLine()
   print "Filter Efficiency: " + str("%0.3f"%eff2)
   print "Reduction Factor: " + str("%0.3f"%red2)
   
   #Efficiency at Reco Cut
   recoEff2_fit = fitFunc(cuts['MET'])
   recoEff2_bin = metTurnon2.GetEfficiency(recoBinMET)
   print "Efficiency at Reco MET cut (bin): ", str("%0.3f"%recoEff2_bin) 
   print "Efficiency at Reco MET cut (fit): ", str("%0.3f"%recoEff2_fit)
   
   #Fit Parameter Extraction
   fit2 = []
   #fitFunc.GetParameters(fit2)
   fit2.append(fitFunc.GetChisquare())
   for x in xrange(0, 4):
      fit2.append(fitFunc.GetParameter(x))
      fit2.append(fitFunc.GetParError(x))
   
   fit2.append(fitFunc.GetX(0.5))
   fit2.append(fitFunc.GetX(0.75))
   fit2.append(fitFunc.GetX(0.80))
   fit2.append(fitFunc.GetX(0.85))
   fit2.append(fitFunc.GetX(0.90))
   fit2.append(fitFunc.GetX(0.95))
   fit2.append(fitFunc.GetX(0.99))
   fit2.append(fitFunc.GetX(1))
   
   box4 = ROOT.TPaveText(box3)
   box4.AddText("#bf{Efficiency at Reco Cut (bin): }" + str("%0.3f"%recoEff2_bin))
   box4.AddText("#bf{Efficiency at Reco Cut (fit): }" + str("%0.3f"%recoEff2_fit))
   box4.Draw()
   
   c2.Modified()
   c2.Update()
   
   ##########################################################################Canvas 3: MET 3 (both gen cuts with gen cut in total)#####################################################################
   #print makeDoubleLine()
   #print "                                                       MET (both generator cuts + gen cut in total):"
   #print makeDoubleLine()
   #
   #c3 = ROOT.TCanvas("c3", "MET 3", 1800, 1500)
   #c3.Divide(1,2)
   #
   #var = "met_pt"
   #
   #c3.cd(1)
   #h9 = drawhist(T2DegSample, var, preSel1 + "&&" + genSel1) #ISR preselection cut & MET generator cut
   #h9.SetName("MET3-1")
   #h9.SetTitle("Generated MET & ISR Jet p_{T} Filter Effect on Reconstructed MET")
   #h9.GetXaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
   #h9.Draw() 
   #h9.SetFillColor(ROOT.kRed+1)
   #h9.SetLineColor(ROOT.kBlack)
   #h9.SetLineWidth(4)
   #
   #l3 = makeLegend()
   #l3.AddEntry("MET3-1", "MET (MET generator cut)", "F")
   #
   #ROOT.gPad.SetLogy()
   #ROOT.gPad.Update()
   #
   #alignStats(h9)
   #
   #h10 = drawhist(T2DegSample, var, preSel1 + "&&" + genSel1 + "&&" + genSel2) # + ISR generator cut
   #h10.SetName("MET3-2")
   #h10.Draw("same")
   #h10.SetFillColor(0)
   #h10.SetLineColor(ROOT.kAzure+7)
   #h10.SetLineWidth(4)
   #
   #l3.AddEntry("MET3-2", "MET (both generator cuts)", "F")
   #l3.Draw()
   #
   ##Efficiency and Reduction Factor Calculation 
   ##h11 = drawhist(T2DegSample, var, "") #no cuts 
   ##h12 = drawhist(T2DegSample, var, genSel1 + "&&" + genSel2) #both gen cuts
   #
   ##eff3 = h12.GetEntries()/h11.GetEntries()
   ##red3 = h11.GetEntries()/h12.GetEntries() # = 1/eff
   #
   #eff3 = eff2
   #red3 = red2
   #
   #box5 = makeBox()
   #box5.AddText("Cuts:")
   #box5.AddText("#bf{ISR Jet p_{T} cut: }" + str(cuts['ISR']) + " GeV")
   #box5.AddText("#bf{ISR Jet #eta cut: }" + str(cuts['ISReta']))
   #box5.AddText("#bf{Gen. MET p_{T} cut: }" + str(cuts['genMET']) + " GeV")
   #box5.AddText("#bf{Gen. ISR Jet p_{T} cut: }" + str(cuts['genISRpt']) + " GeV")
   #box5.AddText("#bf{Gen. ISR Jet #eta cut: }" + str(cuts['genISReta']))
   #box5.AddText("Filter:")
   #box5.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff3))
   #box5.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red3))
   #box5.Draw()
   #
   ##MET Turnon Plot
   #c3.cd(2)
   #metTurnon3 = ROOT.TEfficiency(h10, h9) #(passed, total)
   #metTurnon3.SetTitle("MET Turnon Plot (Both Generator Cuts) ; Missing Transverse Energy #slash{E}_{T} / GeV ; Counts")
   #metTurnon3.SetMarkerColor(ROOT.kBlue)
   #metTurnon3.SetMarkerStyle(33)
   #metTurnon3.SetMarkerSize(3)
   #metTurnon3.Draw("AP") 
   #metTurnon3.SetLineColor(ROOT.kBlack)
   #metTurnon3.SetLineWidth(2)
   #ROOT.gPad.SetGridx()
   #ROOT.gPad.SetGridy()
   #ROOT.gPad.Update()
   #metTurnon3.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000)
   #metTurnon3.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
   #metTurnon3.GetPaintedGraph().GetXaxis().CenterTitle()
   #metTurnon3.GetPaintedGraph().GetYaxis().CenterTitle()
   #
   ##Fitting
   #metTurnon3.Fit(fitFunc)
   #
   #print makeLine()
   #print "Filter Efficiency: " + str("%0.3f"%eff3)
   #print "Inefficiencies Fraction: " + str("%0.3f"%ineff3)
   #print "Reduction Factor: " + str("%0.3f"%red3)
   #
   ##Efficiency at Reco Cut
   #recoEff3_fit = fitFunc(cuts['MET'])
   #recoEff3_bin = metTurnon3.GetEfficiency(recoBinMET)
   #print "Efficiency at Reco MET cut (bin): ", str("%0.3f"%recoEff3_bin) 
   #print "Efficiency at Reco MET cut (fit): ", str("%0.3f"%recoEff3_fit)
   #
   ##Fit Parameter Extraction
   #fit3 = []
   ##fitFunc.GetParameters(fit3)
   #fit3.append(fitFunc.GetChisquare())
   #for x in xrange(0, 4):
   #   fit3.append(fitFunc.GetParameter(x))
   #   fit3.append(fitFunc.GetParError(x))
   #
   #fit3.append(fitFunc.GetX(0.5))
   #fit3.append(fitFunc.GetX(0.75))
   #fit3.append(fitFunc.GetX(0.80))
   #fit3.append(fitFunc.GetX(0.85))
   #fit3.append(fitFunc.GetX(0.90))
   #fit3.append(fitFunc.GetX(0.95))
   #fit3.append(fitFunc.GetX(0.99))
   #fit3.append(fitFunc.GetX(1))
   #
   #box6 = ROOT.TPaveText(box5)
   #box6.AddText("#bf{Efficiency at Reco Cut (bin): }" + str("%0.3f"%recoEff3_bin))
   #box6.AddText("#bf{Efficiency at Reco Cut (fit): }" + str("%0.3f"%recoEff3_fit))
   #box6.Draw()
   #
   #c3.Modified()
   #c3.Update()
   #
   ##############################################################################################################################################################################################################
   
   #####################################################################################Canvas 4: ISR 1 (single gen cut)#########################################################################################
   print makeDoubleLine()
   print "                                              ISR Jet pT (single generator cut):"
   print makeDoubleLine()
   
   c4 = ROOT.TCanvas("c4", "ISR 1", 1800, 1500)
   c4.Divide(1,2)
   
   var = "Max$(Jet_pt*(abs(Jet_eta)<" + str(cuts['ISReta']) + "))" #ISRpt = reco pT of leading jet with eta < 2.4
   
   #nbins = 100
   #min = 0
   #max = 1000
   
   c4.cd(1)
   h13 = drawhist(T2DegSample, var, preSel2) #MET preselection cut
   h13.SetName("ISR")
   h13.SetTitle("Generated ISR Jet p_{T} Filter Effect on Reconstructed ISR Jet p_{T}")
   h13.GetXaxis().SetTitle("ISR Jet p_{T} / GeV")
   h13.Draw()
   h13.SetFillColor(ROOT.kRed+1)
   h13.SetLineColor(ROOT.kBlack)
   h13.SetLineWidth(4)
   
   l4 = makeLegend()
   l4.AddEntry("ISR", "ISR Jet p_{T} (MET preselection cut)", "F")
   
   ROOT.gPad.SetLogy()
   ROOT.gPad.Update()
   
   alignStats(h13)
   
   h14 = drawhist(T2DegSample, var, preSel2 + "&&" + genSel2) # + ISR generator cut
   h14.SetName("ISR1")
   h14.Draw("same")
   h14.SetFillColor(0)
   h14.SetLineColor(ROOT.kAzure+7)
   h14.SetLineWidth(4)
   
   l4.AddEntry("ISR1", "ISR Jet p_{T} (generator cut)", "F")
   l4.Draw()
   
   #Efficiency and Reduction Factor Calculation 
   var = "Max$(GenJet_pt*(abs(GenJet_eta)<" + str(cuts['ISReta']) + "))" #genISRpt = gen pT of leading jet with eta < 2.4
   h15 = drawhist(T2DegSample, var, "") #no cuts 
   h16 = drawhist(T2DegSample, var, genSel2) #genISRpt cut
   
   eff4 = h16.GetEntries()/h15.GetEntries()
   red4 = h15.GetEntries()/h16.GetEntries() # = 1/eff
   
   box7 = makeBox()
   box7.AddText("Cuts:")
   box7.AddText("#bf{MET p_{T} cut: }" + str(cuts['MET']) + " GeV")
   box7.AddText("#bf{Gen. ISR Jet p_{T} cut: }" + str(cuts['genISRpt']) + " GeV")
   box7.AddText("#bf{Gen. ISR Jet #eta cut: }" + str(cuts['genISReta']))
   box7.AddText("Filter:")
   box7.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff4))
   box7.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red4))
   box7.Draw()
   
   #Jet Turnon Plot
   c4.cd(2)
   isrTurnon1 = ROOT.TEfficiency(h14, h13)
   isrTurnon1.SetTitle("ISR Jet p_{T} Turnon Plot (Single Generator Cut) ; ISR Jet p_{T} / GeV ; Counts")
   isrTurnon1.SetMarkerColor(ROOT.kBlue)
   isrTurnon1.SetMarkerStyle(33)
   isrTurnon1.SetMarkerSize(3)
   isrTurnon1.Draw("AP") 
   isrTurnon1.SetLineColor(ROOT.kBlack)
   isrTurnon1.SetLineWidth(2)
   ROOT.gPad.SetGridx()
   ROOT.gPad.SetGridy()
   ROOT.gPad.Update()
   isrTurnon1.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000)
   isrTurnon1.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
   isrTurnon1.GetPaintedGraph().GetXaxis().CenterTitle()
   isrTurnon1.GetPaintedGraph().GetYaxis().CenterTitle()
   
   #Fitting
   fitFunc.SetParameters(0.45, 70, 20, 0.6) #init: (0.45,60,20,0.6)
   #fitFunc.SetParLimits(1, 0, 120) #init: [0,120]
   isrTurnon1.Fit(fitFunc)
   
   print makeLine()
   print "Filter Efficiency: " + str("%0.3f"%eff4)
   print "Reduction Factor: " + str("%0.3f"%red4)
   
   #Efficiency at Reco Cut
   recoEff4_bin = isrTurnon1.GetEfficiency(recoBinISR)
   recoEff4_fit = fitFunc(cuts['ISR'])
   print "Efficiency at Reco ISR Jet pT cut (bin): ", str("%0.3f"%recoEff4_bin) 
   print "Efficiency at Reco ISR Jet pT cut (fit): ", str("%0.3f"%recoEff4_fit)
   
   #Fit Parameter Extraction
   fit4 = []
   #fitFunc.GetParameters(fit4)
   fit4.append(fitFunc.GetChisquare())
   for x in xrange(0, 4):
      fit4.append(fitFunc.GetParameter(x))
      fit4.append(fitFunc.GetParError(x))
   
   fit4.append(fitFunc.GetX(0.5))
   fit4.append(fitFunc.GetX(0.75))
   fit4.append(fitFunc.GetX(0.80))
   fit4.append(fitFunc.GetX(0.85))
   fit4.append(fitFunc.GetX(0.90))
   fit4.append(fitFunc.GetX(0.95))
   fit4.append(fitFunc.GetX(0.99))
   fit4.append(fitFunc.GetX(1))
   
   box8 = ROOT.TPaveText(box7)
   box8.AddText("#bf{Efficiency at Reco Cut (bin): }" + str("%0.3f"%recoEff4_bin))
   box8.AddText("#bf{Efficiency at Reco Cut (fit): }" + str("%0.3f"%recoEff4_fit))
   box8.Draw()
   
   c4.Modified()
   c4.Update() 
   
   ###############################################################################Canvas 5: ISR 2 (both gen cuts)###############################################################################
   print makeDoubleLine()
   print "                                                         ISR Jet pT (both generator cuts):"
   print makeDoubleLine()
   
   c5 = ROOT.TCanvas("c5", "ISR 2", 1800, 1500)
   c5.Divide(1,2)
   
   var = "Max$(Jet_pt*(abs(Jet_eta)<" + str(cuts['ISReta']) + "))" #ISRpt = reco pT of leading jet with eta < 2.4 
   
   c5.cd(1)
   h17 = h13.Clone() #same as ISR1
   h17.SetName("ISR")
   h17.SetTitle("Generated ISR Jet p_{T} & MET Filter Effect on Reconstructed ISR Jet p_{T}")
   h17.GetXaxis().SetTitle("ISR Jet p_{T} / GeV")
   h17.Draw() #MET preselection cut
   h17.SetFillColor(ROOT.kRed+1)
   h17.SetLineColor(ROOT.kBlack)
   h17.SetLineWidth(4)
   
   l5 = makeLegend()
   l5.AddEntry("ISR", "ISR Jet p_{T} (no generator cuts)", "F")
   
   ROOT.gPad.SetLogy()
   
   h18 = drawhist(T2DegSample, var, preSel2 + "&&" + genSel2 + "&&" + genSel1) # + MET generator cut
   h18.SetName("ISR2")
   h18.Draw("same")
   h18.SetFillColor(0)
   h18.SetLineColor(ROOT.kAzure+7)
   h18.SetLineWidth(4)
   
   l5.AddEntry("ISR2", "ISR Jet p_{T} (both generator cuts)", "F")
   l5.Draw()
   
   #Efficiency and Reduction Factor Calculation 
   var = "Max$(GenJet_pt*(abs(GenJet_eta)<" + str(cuts['ISReta']) + "))" #genISRpt = gen pT of leading jet with eta < 2.4 
   h19 = drawhist(T2DegSample, var, "") #no cuts
   h20 = drawhist(T2DegSample, var, genSel2 + "&&" + genSel1) #both gen cuts
   
   eff5 = h20.GetEntries()/h19.GetEntries()
   red5 = h19.GetEntries()/h20.GetEntries() # = 1/eff
   
   box9 = makeBox()
   box9.AddText("Cuts:")
   box9.AddText("#bf{MET p_{T} cut: }" + str(cuts['MET']) + " GeV")
   box9.AddText("#bf{Gen. MET p_{T} cut: }" + str(cuts['genMET']) + " GeV")
   box9.AddText("#bf{Gen. ISR Jet p_{T} cut: }" + str(cuts['genISRpt']) + " GeV")
   box9.AddText("#bf{Gen. ISR Jet #eta cut: }" + str(cuts['genISReta']))
   box9.AddText("Filter:")
   box9.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff5))
   box9.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red5))
   box9.Draw()
   
   #ISR Turnon Plot
   c5.cd(2)
   isrTurnon2 = ROOT.TEfficiency(h18, h17) #(passed, total)
   isrTurnon2.SetTitle("ISR Jet p_{T} Turnon Plot (Both Generator Cuts) ; ISR Jet p_{T} / GeV ; Counts")
   isrTurnon2.SetMarkerColor(ROOT.kBlue)
   isrTurnon2.SetMarkerStyle(33)
   isrTurnon2.SetMarkerSize(3)
   isrTurnon2.Draw("AP") #L/C option for curve | * - Star markers | X - no error bars
   isrTurnon2.SetLineColor(ROOT.kBlack)
   isrTurnon2.SetLineWidth(2)
   ROOT.gPad.SetGridx()
   ROOT.gPad.SetGridy()
   ROOT.gPad.Update()
   isrTurnon2.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000)
   isrTurnon2.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
   isrTurnon2.GetPaintedGraph().GetXaxis().CenterTitle()
   isrTurnon2.GetPaintedGraph().GetYaxis().CenterTitle()
   
   #Fitting
   #fitFunc.SetParameters(0.45, 60, 20, 0.6) #init: (0.45,60,20,0.6)
   #fitFunc.SetParLimits(2, 10, 16)
   isrTurnon2.Fit(fitFunc)
   
   print makeLine()
   print "Filter Efficiency: " + str("%0.3f"%eff5)
   print "Reduction Factor: " + str("%0.3f"%red5)
   
   #Efficiency at Reco Cut
   recoEff5_bin = isrTurnon2.GetEfficiency(recoBinISR)
   recoEff5_fit = fitFunc(cuts['ISR'])
   print "Efficiency at Reco ISR Jet pT cut (bin): ", str("%0.3f"%recoEff5_bin)
   print "Efficiency at Reco ISR Jet pT cut (fit): ", str("%0.3f"%recoEff5_fit)
   print makeLine()
   
   #Fit Parameter Extraction
   fit5 = []
   #fitFunc.GetParameters(fit4)
   fit5.append(fitFunc.GetChisquare())
   for x in xrange(0, 4):
      fit5.append(fitFunc.GetParameter(x))
      fit5.append(fitFunc.GetParError(x))
   
   fit5.append(fitFunc.GetX(0.5))
   fit5.append(fitFunc.GetX(0.75))
   fit5.append(fitFunc.GetX(0.80))
   fit5.append(fitFunc.GetX(0.85))
   fit5.append(fitFunc.GetX(0.90))
   fit5.append(fitFunc.GetX(0.95))
   fit5.append(fitFunc.GetX(0.99))
   fit5.append(fitFunc.GetX(1))
   
   #box8.Copy(box1)
   box10 = ROOT.TPaveText(box9)
   box10.AddText("#bf{Efficiency at Reco Cut (bin): }" + str("%0.3f"%recoEff5_bin))
   box10.AddText("#bf{Efficiency at Reco Cut (fit): }" + str("%0.3f"%recoEff5_fit))
   box10.Draw()
   
   c5.Modified()
   c5.Update()
    
   ###############################################################################Canvas 6: ISR 3 (both gen cuts + gen cut in total)#########################################################################
   #print makeDoubleLine()
   #print "                                                         ISR Jet pT (both generator cuts and gen cut in total):"
   #print makeDoubleLine()
   #
   #c6 = ROOT.TCanvas("c6", "ISR 3", 1800, 1500)
   #c6.Divide(1,2)
   #
   #var = "Max$(Jet_pt*(abs(Jet_eta)<" + str(cuts['ISReta']) + "))" #ISRpt = reco pT of leading jet with eta < 2.4 
   #
   #c6.cd(1)
   #h21 = drawhist(T2DegSample, var, preSel2 + "&&" + genSel2) #MET preselection cut + ISR generator cut
   #h21.SetName("ISR3-1")
   #h21.SetTitle("Generated ISR Jet p_{T} & MET Filter Effect on Reconstructed ISR Jet p_{T}")
   #h21.GetXaxis().SetTitle("ISR Jet p_{T} / GeV")
   #h21.Draw() #MET preselection cut
   #h21.SetFillColor(ROOT.kRed+1)
   #h21.SetLineColor(ROOT.kBlack)
   #h21.SetLineWidth(4)
   #
   #l6 = makeLegend()
   #l6.AddEntry("ISR3-1", "ISR Jet p_{T} (preselection + genISRpt cut)", "F")
   #
   #ROOT.gPad.SetLogy()
   #ROOT.gPad.Update()
   #
   #alignStats(h21)
   #
   #h22 = drawhist(T2DegSample, var, preSel2 + "&&" + genSel2 + "&&" + genSel1) # + MET generator cut
   #h22.SetName("ISR3-2")
   #h22.Draw("same")
   #h22.SetFillColor(0)
   #h22.SetLineColor(ROOT.kAzure+7)
   #h22.SetLineWidth(4)
   #
   #l6.AddEntry("ISR3-2", "ISR Jet p_{T} (both generator cuts)", "F")
   #l6.Draw()
   #
   ##Efficiency and Reduction Factor Calculation 
   ##h23 = drawhist(T2DegSample, var, "") #no cuts
   ##h24 = drawhist(T2DegSample, var, genSel2 + "&&" + genSel1) #both gen cuts
   #
   ##eff6 = h24.GetEntries()/h23.GetEntries()
   ##red6 = h23.GetEntries()/h24.GetEntries() # = 1/eff
   #
   #eff6 = eff5
   #red6 = red5
   #
   #box11 = makeBox()
   #box11.AddText("Cuts:")
   #box11.AddText("#bf{MET p_{T} cut: }" + str(cuts['MET']) + " GeV")
   #box11.AddText("#bf{Gen. MET p_{T} cut: }" + str(cuts['genMET']) + " GeV")
   #box11.AddText("#bf{Gen. ISR Jet p_{T} cut: }" + str(cuts['genISRpt']) + " GeV")
   #box11.AddText("#bf{Gen. ISR Jet #eta cut: }" + str(cuts['genISReta']))
   #box11.AddText("Filter:")
   #box11.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff6))
   #box11.AddText("#bf{Inefficiencies Fraction }" + str("%0.3f"%ineff6))
   #box11.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red6))
   #box11.Draw()
   #
   ##Jet Turnon Plot
   #c6.cd(2)
   #isrTurnon3 = ROOT.TEfficiency(h22, h21) #(passed, total)
   #isrTurnon3.SetTitle("ISR Jet p_{T} Turnon Plot (Both Generator Cuts) ; ISR Jet p_{T} / GeV ; Counts")
   #isrTurnon3.SetMarkerColor(ROOT.kBlue)
   #isrTurnon3.SetMarkerStyle(33)
   #isrTurnon3.SetMarkerSize(3)
   #isrTurnon3.Draw("AP") #L/C option for curve | * - Star markers #X - no error bars
   #isrTurnon3.SetLineColor(ROOT.kBlack)
   #isrTurnon3.SetLineWidth(2)
   #ROOT.gPad.SetGridx()
   #ROOT.gPad.SetGridy()
   #ROOT.gPad.Update()
   #isrTurnon3.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000)
   #isrTurnon3.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
   #isrTurnon3.GetPaintedGraph().GetXaxis().CenterTitle()
   #isrTurnon3.GetPaintedGraph().GetYaxis().CenterTitle()
   #
   ##Fitting
   ##fitFunc.SetParameters(0.45, 60, 20, 0.6) #init: (0.45,60,20,0.6)
   ##fitFunc.SetParLimits(2, 10, 16)
   #isrTurnon3.Fit(fitFunc)
   #
   #print makeLine()
   #print "Filter Efficiency: " + str("%0.3f"%eff6)
   #print "Reduction Factor: " + str("%0.3f"%red6)
   #
   ##Efficiency at Reco Cut
   #recoEff6_bin = isrTurnon3.GetEfficiency(recoBinISR)
   #recoEff6_fit = fitFunc(cuts['ISR'])
   #print "Efficiency at Reco ISR Jet pT cut (bin): ", str("%0.3f"%recoEff6_bin)
   #print "Efficiency at Reco ISR Jet pT cut (fit): ", str("%0.3f"%recoEff6_fit)
   #print makeLine()
   #
   ##Fit Parameter Extraction
   #fit6 = []
   ##fitFunc.GetParameters(fit4)
   #fit6.append(fitFunc.GetChisquare())
   #for x in xrange(0, 4):
   #   fit6.append(fitFunc.GetParameter(x))
   #   fit6.append(fitFunc.GetParError(x))
   #
   #fit6.append(fitFunc.GetX(0.5))
   #fit6.append(fitFunc.GetX(0.75))
   #fit6.append(fitFunc.GetX(0.80))
   #fit6.append(fitFunc.GetX(0.85))
   #fit6.append(fitFunc.GetX(0.90))
   #fit6.append(fitFunc.GetX(0.95))
   #fit6.append(fitFunc.GetX(0.99))
   #fit6.append(fitFunc.GetX(1))
   #
   ##box12.Copy(box1)
   #box12 = ROOT.TPaveText(box7)
   #box12.AddText("#bf{Efficiency at Reco Cut (bin): }" + str("%0.3f"%recoEff6_bin))
   #box12.AddText("#bf{Efficiency at Reco Cut (fit): }" + str("%0.3f"%recoEff6_fit))
   #box12.Draw()
   #
   #c6.Modified()
   #c6.Update() 
   #
   #Write to file
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/final/13TeV/ISR/turnons/filter_%s_%s"%(str(cuts["genMET"]),str(cuts["genISRpt"])) #web address: http://www.hephy.at/user/mzarucki/plots/filter/
   
   if not os.path.exists(savedir):
      os.makedirs(savedir)
   
   if not os.path.exists(savedir + "/MET"):
      os.makedirs(savedir + "/MET")
   
   if not os.path.exists(savedir + "/ISR"):
      os.makedirs(savedir + "/ISR")
   
   #Full filter results 
   outfile1 = open(savedir + "/filterResults_%s_%s.txt"%(str(cuts["genMET"]),str(cuts["genISRpt"])), "w")
   print >> outfile1, "Generator Filter Results", "\n", makeLine(), "\n", cutString, "\n", makeLine(), "\n", \
   "Filter", "        ", "Filter Efficiency", "   ", "Reduction Factor", "  ", "Efficiency at Reco Cut (bin)","   ", "Efficiency at Reco Cut (fit)", "\n\n", \
   "MET1       ", "    ", eff1, "     ", "         ", red1, "      ", recoEff1_bin, "                ", recoEff1_fit, "\n\n", \
   "MET2       ", "    ", eff2, "     ", "         ", red2, "      ", recoEff2_bin, "                ", recoEff2_fit, "\n\n", \
   "ISR1       ", "    ", eff4, "     ", "         ", red4, "      ", recoEff4_bin, "                ", recoEff4_fit, "\n\n", \
   "ISR2       ", "    ", eff5, "     ", "         ", red5, "      ", recoEff5_bin, "                ", recoEff5_fit, "\n", \
   makeLine(), "\n", \
   "Turn-on fit results:", "\n\n", \
   "Filter", "    ", "Chi-Squared", "   ", fitFunc.GetParName(0), "  ", fitFunc.GetParName(0) + "_Err", "     ", fitFunc.GetParName(1), "       ", \
   fitFunc.GetParName(1) + "_Err", "        ", fitFunc.GetParName(2), "      ", fitFunc.GetParName(2) + "_Err", "   ", \
   fitFunc.GetParName(3), "      ", fitFunc.GetParName(3) + "_Err", "\n\n", \
   "MET1", "  ", fit1[0], "  ", fit1[1], "  ", fit1[2], "  ", fit1[3], "  ", fit1[4], "  ", fit1[5], "  ", fit1[6], "  ", fit1[7], "  ", fit1[8], "\n\n", \
   "MET2", "  ", fit2[0], "  ", fit2[1], "  ", fit2[2], "  ", fit2[3], "  ", fit2[4], "  ", fit2[5], "  ", fit2[6], "  ", fit2[7], "  ", fit2[8], "\n\n", \
   "ISR1", "  ", fit4[0], "  ", fit4[1], "  ", fit4[2], "  ", fit4[3], "  ", fit4[4], "  ", fit4[5], "  ", fit4[6], "  ", fit4[7], "  ", fit4[8], "\n\n", \
   "ISR2", "  ", fit5[0], "  ", fit5[1], "  ", fit5[2], "  ", fit5[3], "  ", fit5[4], "  ", fit5[5], "  ", fit5[6], "  ", fit5[7], "  ", fit5[8], "\n", \
   makeLine(), "\n", \
   "Variable values for various efficiecies:", "\n\n", \
   "Efficiency:        50%           75%            80%           85%           90%           95%           99%          100%", "\n\n", \
   "MET1        ", fit1[9], fit1[10], fit1[11], fit1[12], fit1[13], fit1[14], fit1[15], fit1[16], "\n\n", \
   "MET2        ", fit2[9], fit2[10], fit2[11], fit2[12], fit2[13], fit2[14], fit2[15], fit2[16], "\n\n", \
   "ISR1        ", fit4[9], fit4[10], fit4[11], fit4[12], fit4[13], fit4[14], fit4[15], fit4[16], "\n\n", \
   "ISR2        ", fit5[9], fit5[10], fit5[11], fit5[12], fit5[13], fit5[14], fit5[15], fit5[16]
   outfile1.close()
   
   #fit3[0], " ", fit3[1], " ", fit3[2], " ", fit3[3], " ", fit3[4], " ", fit3[5], " ", fit3[6], " ", fit3[7], " ", fit3[8], "\n\n", \
   #fit6[0], " ", fit6[1], " ", fit6[2], " ", fit6[3], " ", fit6[4], " ", fit6[5], " ", fit6[6], " ", fit6[7], " ", fit6[8], "\n", \
   #"MET 3       ", "    ", eff3, "     ", ineff3, "         ", red3, "      ", recoEff3_bin, "                ", recoEff3_fit, "\n\n", \
   #"ISR 3       ", "    ", eff6, "     ", ineff6, "         ", red6, "      ", recoEff6_bin, "                ", recoEff6_fit, "\n", \
   #"MET 3        ", fit3[9], fit3[10], fit3[11], fit3[12], fit3[13], fit3[14], fit3[15], fit3[16], "\n\n", \
   #"ISR 3        ", fit6[9], fit6[10], fit6[11], fit6[12], fit6[13], fit6[14], fit6[15], fit6[16]
   
   #Condensed filter results 
   outfile2 = open(savedir + "/reductionEfficiency_%s_%s.txt"%(str(cuts["genMET"]),str(cuts["genISRpt"])), "w")
   outfile2.write(\
   "genMET Cut" + "   " + "genISRpt Cut" + "    " + "MET 1 Red. Factor" + "    " + "MET 1 Reco Eff." + "    " + "MET 2 Red. Factor" + "    " + "MET 2 Reco Eff." + "    " + "ISR 1 Red. Factor" + "    " + "ISR 1 Reco Eff." + "    " + "ISR 2 Red. Factor" + "    " + "ISR 2 Reco Eff." + "\n" +\
   "  " + str(cuts["genMET"]) + "         " + str(cuts["genISRpt"]) + "         " + str(red1) + "      " + str(recoEff1_bin) + "      " + str(red2) + "      " + str(recoEff2_bin) + "      " + str(red4) + "      " + str(recoEff4_bin) + "      " + str(red5) + "      " + str(recoEff5_bin)\
   )
   outfile2.close()
   
   #Save to Web
   c1.SaveAs(savedir + "/MET/MET1_%s_%s.root"%( str(cuts['genMET']), str(cuts['genISRpt'])))
   c2.SaveAs(savedir + "/MET/MET2_%s_%s.root"%(str(cuts['genMET']), str(cuts['genISRpt'])))
   #c3.SaveAs(savedir + "/MET/MET3_%s_%s.root"%(str(cuts['genMET']), str(cuts['genISRpt'])))
   c4.SaveAs(savedir + "/ISR/ISR1_%s_%s.root"%(str(cuts['genMET']), str(cuts['genISRpt'])))
   c5.SaveAs(savedir + "/ISR/ISR2_%s_%s.root"%(str(cuts['genMET']), str(cuts['genISRpt'])))
   #c6.SaveAs(savedir + "/ISR/ISR3_%s_%s.root"%(str(cuts['genMET']), str(cuts['genISRpt'])))
   
   c1.SaveAs(savedir + "/MET/MET1_%s_%s.png"%( str(cuts['genMET']), str(cuts['genISRpt'])))
   c2.SaveAs(savedir + "/MET/MET2_%s_%s.png"%(str(cuts['genMET']), str(cuts['genISRpt'])))
   #c3.SaveAs(savedir + "/MET/MET3_%s_%s.png"%(str(cuts['genMET']), str(cuts['genISRpt'])))
   c4.SaveAs(savedir + "/ISR/ISR1_%s_%s.png"%(str(cuts['genMET']), str(cuts['genISRpt'])))
   c5.SaveAs(savedir + "/ISR/ISR2_%s_%s.png"%(str(cuts['genMET']), str(cuts['genISRpt'])))
   #c6.SaveAs(savedir + "/ISR/ISR3_%s_%s.png"%(str(cuts['genMET']), str(cuts['genISRpt'])))
   
   c1.SaveAs(savedir + "/MET/MET1_%s_%s.pdf"%( str(cuts['genMET']), str(cuts['genISRpt'])))
   c2.SaveAs(savedir + "/MET/MET2_%s_%s.pdf"%(str(cuts['genMET']), str(cuts['genISRpt'])))
   #c3.SaveAs(savedir + "/MET/MET3_%s_%s.pdf"%(str(cuts['genMET']), str(cuts['genISRpt'])))
   c4.SaveAs(savedir + "/ISR/ISR1_%s_%s.pdf"%(str(cuts['genMET']), str(cuts['genISRpt'])))
   c5.SaveAs(savedir + "/ISR/ISR2_%s_%s.pdf"%(str(cuts['genMET']), str(cuts['genISRpt'])))
   #c6.SaveAs(savedir + "/ISR/ISR3_%s_%s.pdf"%(str(cuts['genMET']), str(cuts['genISRpt'])))

if __name__ == '__main__':
   sys.exit(main(sys.argv[1], sys.argv[2]))
