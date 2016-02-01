#turnonMHT.py - Imported by filter.py. Plots turn-on curves for HT and MHT, as a function of genHT and genMHT cuts.

def main(genHTcut, genMHTcut): #main function to be imported by filter.py.
   print "\nImporting and executing turnonMHT.py script..."
    
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
   *********************************************************************************************************************************************************************\n"
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
   
   def makehist(varname, nbins = 100, min = 0, max = 1000):
      hist = ROOT.TH1F(varname, varname + " Histogram", nbins, min, max)
      hist.GetYaxis().SetTitle("Counts")
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
   'HT' : 200, #HT cut (fixed)
   'MHT' : 120, #MHT cut (fixed)
   'HTjetPt' : 40, #Jet pt threshold for MHT (fixed)
   'HTjetEta' : 3, #Jet eta cut for MHT (fixed)
   
   'genHT' : genHTcut, #generated quantity cuts
   'genMHT' : genMHTcut,
   'genHTjetPt' : 30, #GenJet pt threshold for MHT
   'genHTjetEta' : 4.5 #GenJet eta cut for MHT
   })
   
   cutString = \
   "Preselection cuts: \n\n" + \
   "HT cut: " + str(cuts['HT']) + "\n" + \
   "MHT cut: " + str(cuts['MHT']) + "\n" + \
   "HT Jets pT cut: " + str(cuts['HTjetPt']) + "\n" + \
   "HT Jets eta cut: " + str(cuts['HTjetEta']) + "\n\n" + \
   "Generator cuts:" + "\n\n" + \
   "Generated HT cut: " + str(cuts['genHT']) + "\n" + \
   "Generated MHT cut: " + str(cuts['genMHT']) + "\n" + \
   "Generated HT Jets pT cut: " + str(cuts['genHTjetPt']) + "\n" + \
   "Generated HT Jets eta cut: " + str(cuts['genHTjetEta'])
   
   print makeLine()
   print cutString
   print makeLine()
    
   #Bin size 
   nbins = 100
   min = 0 #GeV
   max = 1000 #GeV
   
   recoBinHT = int(cuts['HT']*nbins/(max - min)) + 1 #cuts['HT']/(h1.GetXaxis().GetBinWidth(0)) # + 1 to get correct bin
   recoBinMHT = int(cuts['MHT']*nbins/(max - min)) + 1
   
   #Preselection and Generated Particles Filter Selection
   #Variables: met_pt, met_genPt, Jet_pt, GenJet_pt, Jet_eta, GenJet_eta
   
   #HT Selection
   #presel2 = select("met_pt", cuts['HT'], ">") 
   
   #gensel1 = select("met_genPt", cuts['genHT'], ">")
   
   #MHT Selection
   #presel1 = select("mhtJet40", cuts['MHT'], ">")
   
   #presel1 = "Sum$(Jet_pt*(Jet_pt >" + str(cuts['MHTjetPt']) + "&& abs(Jet_eta) <" + str(cuts['MHTjetEta'])+ "&& Jet_id)) >" + str(cuts['MHT']) #MHT = Sum of Jets > 30GeV 
   
   #gensel2 = "Sum$(GenJet_pt*(GenJet_pt >" + str(cuts['genMHTjetPt']) + "&& abs(GenJet_eta) <" + str(cuts['genMHTjetEta'])+ ")) >" + str(cuts['genMHT']) #genMHT = Sum of genJets > 30GeV 
   
   T2DegSample.Draw(">>eList", "")
   elist = ROOT.gDirectory.Get("eList")
   nEvents = elist.GetN()
   
   #Empty histograms
   HT0 = makehist("HT01") # no cuts
   HT02 = makehist("HT02") # both gen cuts
   HT = makehist("HT") #MHT preselection
   HT1 = makehist("HT1") # + genHT
   HT2 = makehist("HT2") # + genMHT
   
   MHT0 = makehist("MHT01") # no cuts
   MHT02 = makehist("MHT02") # both gen cuts
   MHT = makehist("MHT") #HT preselection
   MHT1 = makehist("MHT1") # + genMHT
   MHT2 = makehist("MHT2") # + genHT
    
   
   
   #Event Loop
   for i in range(nEvents):
      #if i == 1000: break
      
      T2DegSample.GetEntry(elist.GetEntry(i))
      
      #Reconstructed Variables 
      recoHT = 0.0
      recoMHT = 0.0
      MHTjetSum = ROOT.TLorentzVector()
      
      nJets = T2DegSample.GetLeaf("nJet40").GetValue()
      
      for jet in range(int(nJets)):
         
         JetPt = T2DegSample.GetLeaf("Jet_pt").GetValue(jet)
         JetEta = T2DegSample.GetLeaf("Jet_eta").GetValue(jet)
         JetPhi = T2DegSample.GetLeaf("Jet_phi").GetValue(jet)
         JetMass = T2DegSample.GetLeaf("Jet_mass").GetValue(jet)
         
         MHTjet = ROOT.TLorentzVector()
          
         if JetPt > cuts['HTjetPt'] and abs(JetEta) < cuts['HTjetEta']:
            recoHT += JetPt #HT
            MHTjet.SetPtEtaPhiM(JetPt, JetEta, JetPhi, JetMass) #MHT
         
         MHTjetSum += MHTjet 
         recoMHT = genMHTjetSum.Pt()
      
      #Generated Variables
      genHT = 0.0
      genMHT = 0.0
      genMHTjetSum = ROOT.TLorentzVector()
      
      nGenJets = T2DegSample.GetLeaf("nGenJet").GetValue()
       
      for jet in range(int(nGenJets)):
         
         GenJetPt = T2DegSample.GetLeaf("GenJet_pt").GetValue(jet)
         GenJetEta = T2DegSample.GetLeaf("GenJet_eta").GetValue(jet)
         GenJetPhi = T2DegSample.GetLeaf("GenJet_phi").GetValue(jet)
         GenJetMass = T2DegSample.GetLeaf("GenJet_mass").GetValue(jet)
         
         genMHTjet = ROOT.TLorentzVector()
          
         if GenJetPt > cuts['genHTjetPt'] and abs(GenJetEta) < cuts['genHTjetEta']:
            genHT += GenJetPt #genHT
            genMHTjet.SetPtEtaPhiM(GenJetPt, GenJetEta, GenJetPhi, GenJetMass) #genMHT
         
         genMHTjetSum += genMHTjet 
         genMHT = genMHTjetSum.Pt()
      
      #Histogram filling   
      
      #HT
      if recoMHT > cuts['MHT']: # MHT preselection
         HT.Fill(recoHT)
         if genHT > cuts['genHT']: # +genHT cut
            HT1.Fill(recoHT)
            if genMHT > cuts['genMHT']: # +genMHT cut
               HT2.Fill(recoHT)
      #MHT 
      if recoHT > cuts['HT']: # HT preselection
         MHT.Fill(recoMHT)
         if genMHT > cuts['genMHT']:
            MHT1.Fill(recoMHT)
            if genHT > cuts['genHT']:
               MHT2.Fill(recoMHT)
   
      HT0.Fill(recoHT) #no cuts
      MHT0.Fill(recoMHT) #no cuts
      
      if genHT > cuts['genHT'] and genMHT > cuts['genMHT']:
         HT02.Fill(recoHT)
         MHT02.Fill(recoMHT)
   
   ################################################################################Canvas 1: HT 1 (single gen cut)#######################################################################################
   
   print makeDoubleLine()
   print "                                                     HT (single generator cut):"
   print makeDoubleLine()
   
   c1 = ROOT.TCanvas("c1", "HT 1", 1800, 1500)
   c1.Divide(1,2)
   
   c1.cd(1)
   HT.SetName("HT")
   HT.SetTitle("Generated H_{T} Filter Effect on Reconstructed H_{T}")
   HT.GetXaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
   HT.GetXaxis().SetTitleOffset(1.2)
   HT.GetYaxis().SetTitleOffset(1.2)
   HT.Draw()
   HT.SetFillColor(ROOT.kRed+1)
   HT.SetLineColor(ROOT.kBlack)
   HT.SetLineWidth(4)
   
   l1 = makeLegend()
   l1.AddEntry("HT", "H_{T} (no generator cuts)", "F")
   
   ROOT.gPad.SetLogy()
   ROOT.gPad.Update()
   
   alignStats(HT)
   
   HT1.SetName("HT1")
   HT1.Draw("same")
   HT1.SetFillColor(0)
   HT1.SetLineColor(ROOT.kAzure+7)
   HT1.SetLineWidth(4)
   
   l1.AddEntry("HT1", "H_{T} (generator cut)", "F")
   l1.Draw()
   
   #Efficiency and Reduction Factor Calculation 
   
   eff1 = HT02.GetEntries()/HT0.GetEntries()
   red1 = HT0.GetEntries()/HT02.GetEntries() # = 1/eff
   
   #Number of Inefficiencies
   box1 = makeBox()
   box1.AddText("Cuts:")
   box1.AddText("#bf{MH_{T} cut: }" + str(cuts['MHT']) + " GeV")
   box1.AddText("#bf{MH_{T} Jets p_{T} cut: }" + str(cuts['HTjetPt']) + " GeV")
   box1.AddText("#bf{MH_{T} Jets #eta cut: }" + str(cuts['HTjetEta']))
   box1.AddText("#bf{Gen. H_{T} cut: }" + str(cuts['genHT']) + " GeV")
   box1.AddText("Filter:")
   box1.AddText("#bf{Total Filter Efficiency: }" + str("%0.3f"%eff1))
   box1.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red1))
   box1.Draw()
   
   ROOT.gPad.Update()
   
   #HT Turnon Plot
   c1.cd(2)
   metTurnon1 = ROOT.TEfficiency(HT1, HT) #(passed, total)
   metTurnon1.SetTitle("H_{T} Turnon Plot (Single Generator Cut) ; Missing Transverse Energy #slash{E}_{T} / GeV ; Counts")
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
   recoEff1_bin = metTurnon1.GetEfficiency(recoBinHT)
   recoEff1_fit = fitFunc(cuts['HT'])
   print "Efficiency at Reco HT cut (bin): ", str("%0.3f"%recoEff1_bin)
   print "Efficiency at Reco HT cut (fit): ", str("%0.3f"%recoEff1_fit)
   
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
   
   ########################################################################################Canvas 2: HT 2 (both gen cuts)################################################################################ 
   print makeDoubleLine()
   print "                                                       HT (both generator cuts):"
   print makeDoubleLine()
   
   c2 = ROOT.TCanvas("c2", "HT 2", 1800, 1500)
   c2.Divide(1,2)
   
   c2.cd(1)
   HT.SetTitle("Generated H_{T} & MH_{T} Filter Effect on Reconstructed HT")
   HT.Draw() 
   HT.SetFillColor(ROOT.kRed+1)
   HT.SetLineColor(ROOT.kBlack)
   HT.SetLineWidth(4)
   
   l2 = makeLegend()
   l2.AddEntry("HT", "H_{T} (no generator cuts)", "F")
   
   ROOT.gPad.SetLogy()
   
   HT2.SetName("HT2")
   HT2.Draw("same")
   HT2.SetFillColor(0)
   HT2.SetLineColor(ROOT.kAzure+7)
   HT2.SetLineWidth(4)
   
   l2.AddEntry("HT2", "H_{T} (both generator cuts)", "F")
   l2.Draw()
   
   eff2 = HT02.GetEntries()/HT0.GetEntries()
   red2 = HT0.GetEntries()/HT02.GetEntries() # = 1/eff
   
   box3 = makeBox()
   box3.AddText("Cuts:")
   box3.AddText("#bf{MHT cut: }" + str(cuts['MHT']) + " GeV")
   box3.AddText("#bf{MHT Jets p_{T} cut: }" + str(cuts['HTjetPt']) + " GeV")
   box3.AddText("#bf{MHT Jets #eta cut: }" + str(cuts['HTjetEta']))
   box3.AddText("#bf{Gen. H_{T} cut: }" + str(cuts['genHT']) + " GeV")
   box3.AddText("#bf{Gen. MH_{T} cut: }" + str(cuts['genMHT']) + " GeV")
   box3.AddText("#bf{Gen. MH_{T} Jets p_{T} cut: }" + str(cuts['genHTjetPt']) + " GeV")
   box3.AddText("#bf{Gen. MH_{T} Jets #eta cut: }" + str(cuts['genHTjetEta']))
   box3.AddText("Filter:")
   box3.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff2))
   box3.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red2))
   box3.Draw()
   
   #HT Turnon Plot
   c2.cd(2)
   metTurnon2 = ROOT.TEfficiency(HT2, HT) #(passed, total)
   metTurnon2.SetTitle("H_{T} Turnon Plot (Both Generator Cuts) ; Missing Transverse Energy #slash{E}_{T} / GeV ; Counts")
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
   recoEff2_fit = fitFunc(cuts['HT'])
   recoEff2_bin = metTurnon2.GetEfficiency(recoBinHT)
   print "Efficiency at Reco HT cut (bin): ", str("%0.3f"%recoEff2_bin) 
   print "Efficiency at Reco HT cut (fit): ", str("%0.3f"%recoEff2_fit)
   
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
   
   ##############################################################################################################################################################################################################
   
   #####################################################################################Canvas 4: MHT 1 (single gen cut)#########################################################################################
   print makeDoubleLine()
   print "                                                    MHT (single generator cut):"
   print makeDoubleLine()
   
   c4 = ROOT.TCanvas("c4", "MHT 1", 1800, 1500)
   c4.Divide(1,2)
   
   c4.cd(1)
   MHT.SetName("MHT")
   MHT.SetTitle("Generated H_{T} Filter Effect on Reconstructed H_{T}")
   MHT.GetXaxis().SetTitle("H_{T} / GeV")
   MHT.Draw()
   MHT.SetFillColor(ROOT.kRed+1)
   MHT.SetLineColor(ROOT.kBlack)
   MHT.SetLineWidth(4)
   
   l4 = makeLegend()
   l4.AddEntry("MHT", "MH_{T} (H_{T} preselection cut)", "F")
   
   ROOT.gPad.SetLogy()
   ROOT.gPad.Update()
   
   alignStats(MHT)
   
   MHT1.SetName("MHT1")
   MHT1.Draw("same")
   MHT1.SetFillColor(0)
   MHT1.SetLineColor(ROOT.kAzure+7)
   MHT1.SetLineWidth(4)
   
   l4.AddEntry("MHT1", "MH_{T} (generator cut)", "F")
   l4.Draw()
   
   #Efficiency and Reduction Factor Calculation 
   eff4 = MHT02.GetEntries()/MHT0.GetEntries()
   red4 = MHT0.GetEntries()/MHT02.GetEntries() # = 1/eff
   
   box7 = makeBox()
   box7.AddText("Cuts:")
   box7.AddText("#bf{H_{T} cut: }" + str(cuts['HT']) + " GeV")
   box7.AddText("#bf{Gen. MH_{T} cut: }" + str(cuts['genMHT']) + " GeV")
   box7.AddText("#bf{Gen. MH_{T} Jets p_{T} cut: }" + str(cuts['genHTjetPt']) + " GeV")
   box7.AddText("#bf{Gen. MH_{T} Jets p_{T} #eta: }" + str(cuts['genHTjetEta']))
   box7.AddText("Filter:")
   box7.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff4))
   box7.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red4))
   box7.Draw()
   
   #Jet Turnon Plot
   c4.cd(2)
   mhtTurnon1 = ROOT.TEfficiency(MHT1, MHT)
   mhtTurnon1.SetTitle("MH_{T} Turnon Plot (Single Generator Cut) ; MH_{T} / GeV ; Counts")
   mhtTurnon1.SetMarkerColor(ROOT.kBlue)
   mhtTurnon1.SetMarkerStyle(33)
   mhtTurnon1.SetMarkerSize(3)
   mhtTurnon1.Draw("AP") 
   mhtTurnon1.SetLineColor(ROOT.kBlack)
   mhtTurnon1.SetLineWidth(2)
   ROOT.gPad.SetGridx()
   ROOT.gPad.SetGridy()
   ROOT.gPad.Update()
   mhtTurnon1.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000)
   mhtTurnon1.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
   mhtTurnon1.GetPaintedGraph().GetXaxis().CenterTitle()
   mhtTurnon1.GetPaintedGraph().GetYaxis().CenterTitle()
   
   #Fitting
   fitFunc.SetParameters(0.45, 70, 20, 0.6) #init: (0.45,60,20,0.6)
   #fitFunc.SetParLimits(1, 0, 120) #init: [0,120]
   mhtTurnon1.Fit(fitFunc)
   
   print makeLine()
   print "Filter Efficiency: " + str("%0.3f"%eff4)
   print "Reduction Factor: " + str("%0.3f"%red4)
   
   #Efficiency at Reco Cut
   recoEff4_bin = mhtTurnon1.GetEfficiency(recoBinMHT)
   recoEff4_fit = fitFunc(cuts['MHT'])
   print "Efficiency at Reco MHT cut (bin): ", str("%0.3f"%recoEff4_bin) 
   print "Efficiency at Reco MHT cut (fit): ", str("%0.3f"%recoEff4_fit)
   
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
   
   ###############################################################################Canvas 5: MHT 2 (both gen cuts)###############################################################################
   print makeDoubleLine()
   print "                                                           MHT (both generator cuts):"
   print makeDoubleLine()
   
   c5 = ROOT.TCanvas("c5", "MHT 2", 1800, 1500)
   c5.Divide(1,2)
   
   c5.cd(1)
   MHT.SetTitle("Generated MH_{T} & H_{T} Filter Effect on Reconstructed H_{T}")
   MHT.GetXaxis().SetTitle("MH_{T} / GeV")
   MHT.Draw() #HT preselection cut
   MHT.SetFillColor(ROOT.kRed+1)
   MHT.SetLineColor(ROOT.kBlack)
   MHT.SetLineWidth(4)
   
   l5 = makeLegend()
   l5.AddEntry("MHT", "MH_{T} (no generator cuts)", "F")
   
   ROOT.gPad.SetLogy()
   
   MHT2.SetName("MHT2")
   MHT2.Draw("same")
   MHT2.SetFillColor(0)
   MHT2.SetLineColor(ROOT.kAzure+7)
   MHT2.SetLineWidth(4)
   
   l5.AddEntry("MHT2", "MH_{T} (both generator cuts)", "F")
   l5.Draw()
   
   #Efficiency and Reduction Factor Calculation 
   eff5 = MHT02.GetEntries()/MHT0.GetEntries()
   red5 = MHT0.GetEntries()/MHT02.GetEntries() # = 1/eff
   
   box9 = makeBox()
   box9.AddText("Cuts:")
   box9.AddText("#bf{H_{T} cut: }" + str(cuts['HT']) + " GeV")
   box9.AddText("#bf{Gen. HT p_{T} cut: }" + str(cuts['genHT']) + " GeV")
   box9.AddText("#bf{Gen. MH_{T} cut: }" + str(cuts['genMHT']) + " GeV")
   box9.AddText("#bf{Gen. MH_{T} Jets p_{T} cut: }" + str(cuts['genHTjetPt']) + " GeV")
   box9.AddText("#bf{Gen. MH_{T} Jets #eta cut: }" + str(cuts['genHTjetEta']))
   box9.AddText("Filter:")
   box9.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff5))
   box9.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red5))
   box9.Draw()
   
   #MHT Turnon Plot
   c5.cd(2)
   mhtTurnon2 = ROOT.TEfficiency(MHT2, MHT) #(passed, total)
   mhtTurnon2.SetTitle("MH_{T} Turnon Plot (Both Generator Cuts) ; MH_{T} / GeV ; Counts")
   mhtTurnon2.SetMarkerColor(ROOT.kBlue)
   mhtTurnon2.SetMarkerStyle(33)
   mhtTurnon2.SetMarkerSize(3)
   mhtTurnon2.Draw("AP") #L/C option for curve | * - Star markers | X - no error bars
   mhtTurnon2.SetLineColor(ROOT.kBlack)
   mhtTurnon2.SetLineWidth(2)
   ROOT.gPad.SetGridx()
   ROOT.gPad.SetGridy()
   ROOT.gPad.Update()
   mhtTurnon2.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000)
   mhtTurnon2.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
   mhtTurnon2.GetPaintedGraph().GetXaxis().CenterTitle()
   mhtTurnon2.GetPaintedGraph().GetYaxis().CenterTitle()
   
   #Fitting
   #fitFunc.SetParameters(0.45, 60, 20, 0.6) #init: (0.45,60,20,0.6)
   #fitFunc.SetParLimits(2, 10, 16)
   mhtTurnon2.Fit(fitFunc)
   
   print makeLine()
   print "Filter Efficiency: " + str("%0.3f"%eff5)
   print "Reduction Factor: " + str("%0.3f"%red5)
   
   #Efficiency at Reco Cut
   recoEff5_bin = mhtTurnon2.GetEfficiency(recoBinMHT)
   recoEff5_fit = fitFunc(cuts['MHT'])
   print "Efficiency at Reco MHT cut (bin): ", str("%0.3f"%recoEff5_bin)
   print "Efficiency at Reco MHT cut (fit): ", str("%0.3f"%recoEff5_fit)
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
    
   #Write to file
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/13TeV/MHT/turnons/filter_%s_%s"%(str(cuts["genHT"]),str(cuts["genMHT"])) #web address: http://www.hephy.at/user/mzarucki/plots/filter/
   
   if not os.path.exists(savedir):
      os.makedirs(savedir)
   
   if not os.path.exists(savedir + "/HT"):
      os.makedirs(savedir + "/HT")
   
   if not os.path.exists(savedir + "/MHT"):
      os.makedirs(savedir + "/MHT")
   
   #Full filter results 
   outfile1 = open(savedir + "/filterResults_%s_%s.txt"%(str(cuts["genHT"]),str(cuts["genMHT"])), "w")
   print >> outfile1, "Generator Filter Results", "\n", makeLine(), "\n", cutString, "\n", makeLine(), "\n", \
   "Filter", "        ", "Filter Efficiency", "   ", "Reduction Factor", "  ", "Efficiency at Reco Cut (bin)","   ", "Efficiency at Reco Cut (fit)", "\n\n", \
   "HT1       ", "    ", eff1, "     ", "         ", red1, "      ", recoEff1_bin, "                ", recoEff1_fit, "\n\n", \
   "HT2       ", "    ", eff2, "     ", "         ", red2, "      ", recoEff2_bin, "                ", recoEff2_fit, "\n\n", \
   "MHT1       ", "    ", eff4, "     ", "         ", red4, "      ", recoEff4_bin, "                ", recoEff4_fit, "\n\n", \
   "MHT2       ", "    ", eff5, "     ", "         ", red5, "      ", recoEff5_bin, "                ", recoEff5_fit, "\n", \
   makeLine(), "\n", \
   "Turn-on fit results:", "\n\n", \
   "Filter", "    ", "Chi-Squared", "   ", fitFunc.GetParName(0), "  ", fitFunc.GetParName(0) + "_Err", "     ", fitFunc.GetParName(1), "       ", \
   fitFunc.GetParName(1) + "_Err", "        ", fitFunc.GetParName(2), "      ", fitFunc.GetParName(2) + "_Err", "   ", \
   fitFunc.GetParName(3), "      ", fitFunc.GetParName(3) + "_Err", "\n\n", \
   "HT1", "  ", fit1[0], "  ", fit1[1], "  ", fit1[2], "  ", fit1[3], "  ", fit1[4], "  ", fit1[5], "  ", fit1[6], "  ", fit1[7], "  ", fit1[8], "\n\n", \
   "HT2", "  ", fit2[0], "  ", fit2[1], "  ", fit2[2], "  ", fit2[3], "  ", fit2[4], "  ", fit2[5], "  ", fit2[6], "  ", fit2[7], "  ", fit2[8], "\n\n", \
   "MHT1", "  ", fit4[0], "  ", fit4[1], "  ", fit4[2], "  ", fit4[3], "  ", fit4[4], "  ", fit4[5], "  ", fit4[6], "  ", fit4[7], "  ", fit4[8], "\n\n", \
   "MHT2", "  ", fit5[0], "  ", fit5[1], "  ", fit5[2], "  ", fit5[3], "  ", fit5[4], "  ", fit5[5], "  ", fit5[6], "  ", fit5[7], "  ", fit5[8], "\n", \
   makeLine(), "\n", \
   "Variable values for various efficiecies:", "\n\n", \
   "Efficiency:        50%           75%            80%           85%           90%           95%           99%          100%", "\n\n", \
   "HT1        ", fit1[9], fit1[10], fit1[11], fit1[12], fit1[13], fit1[14], fit1[15], fit1[16], "\n\n", \
   "HT2        ", fit2[9], fit2[10], fit2[11], fit2[12], fit2[13], fit2[14], fit2[15], fit2[16], "\n\n", \
   "MHT1        ", fit4[9], fit4[10], fit4[11], fit4[12], fit4[13], fit4[14], fit4[15], fit4[16], "\n\n", \
   "MHT2        ", fit5[9], fit5[10], fit5[11], fit5[12], fit5[13], fit5[14], fit5[15], fit5[16]
   outfile1.close()
   
   #fit3[0], " ", fit3[1], " ", fit3[2], " ", fit3[3], " ", fit3[4], " ", fit3[5], " ", fit3[6], " ", fit3[7], " ", fit3[8], "\n\n", \
   #fit6[0], " ", fit6[1], " ", fit6[2], " ", fit6[3], " ", fit6[4], " ", fit6[5], " ", fit6[6], " ", fit6[7], " ", fit6[8], "\n", \
   #"HT 3       ", "    ", eff3, "     ", ineff3, "         ", red3, "      ", recoEff3_bin, "                ", recoEff3_fit, "\n\n", \
   #"MHT 3       ", "    ", eff6, "     ", ineff6, "         ", red6, "      ", recoEff6_bin, "                ", recoEff6_fit, "\n", \
   #"HT 3        ", fit3[9], fit3[10], fit3[11], fit3[12], fit3[13], fit3[14], fit3[15], fit3[16], "\n\n", \
   #"MHT 3        ", fit6[9], fit6[10], fit6[11], fit6[12], fit6[13], fit6[14], fit6[15], fit6[16]
   
   #Condensed filter results 
   outfile2 = open(savedir + "/reductionEfficiency_%s_%s.txt"%(str(cuts["genHT"]),str(cuts["genMHT"])), "w")
   outfile2.write(\
   "genHT Cut" + "   " + "genMHT Cut" + "    " + "HT 1 Red. Factor" + "    " + "HT 1 Reco Eff." + "    " + "HT 2 Red. Factor" + "    " + "HT 2 Reco Eff." + "    " + "MHT 1 Red. Factor" + "    " + "MHT 1 Reco Eff." + "    " + "MHT 2 Red. Factor" + "    " + "MHT 2 Reco Eff." + "\n" +\
   "  " + str(cuts["genHT"]) + "         " + str(cuts["genMHT"]) + "         " + str(red1) + "      " + str(recoEff1_bin) + "      " + str(red2) + "      " + str(recoEff2_bin) + "      " + str(red4) + "      " + str(recoEff4_bin) + "      " + str(red5) + "      " + str(recoEff5_bin)\
   )
   outfile2.close()
   
   #Save to Web
   c1.SaveAs(savedir + "/HT/HT1_%s_%s.root"%( str(cuts['genHT']), str(cuts['genMHT'])))
   c2.SaveAs(savedir + "/HT/HT2_%s_%s.root"%(str(cuts['genHT']), str(cuts['genMHT'])))
   c4.SaveAs(savedir + "/MHT/MHT1_%s_%s.root"%(str(cuts['genHT']), str(cuts['genMHT'])))
   c5.SaveAs(savedir + "/MHT/MHT2_%s_%s.root"%(str(cuts['genHT']), str(cuts['genMHT'])))
   
   c1.SaveAs(savedir + "/HT/HT1_%s_%s.png"%( str(cuts['genHT']), str(cuts['genMHT'])))
   c2.SaveAs(savedir + "/HT/HT2_%s_%s.png"%(str(cuts['genHT']), str(cuts['genMHT'])))
   c4.SaveAs(savedir + "/MHT/MHT1_%s_%s.png"%(str(cuts['genHT']), str(cuts['genMHT'])))
   c5.SaveAs(savedir + "/MHT/MHT2_%s_%s.png"%(str(cuts['genHT']), str(cuts['genMHT'])))
   
   c1.SaveAs(savedir + "/HT/HT1_%s_%s.pdf"%( str(cuts['genHT']), str(cuts['genMHT'])))
   c2.SaveAs(savedir + "/HT/HT2_%s_%s.pdf"%(str(cuts['genHT']), str(cuts['genMHT'])))
   c4.SaveAs(savedir + "/MHT/MHT1_%s_%s.pdf"%(str(cuts['genHT']), str(cuts['genMHT'])))
   c5.SaveAs(savedir + "/MHT/MHT2_%s_%s.pdf"%(str(cuts['genHT']), str(cuts['genMHT'])))

if __name__ == '__main__':
   sys.exit(main(sys.argv[1], sys.argv[2]))
