# getLeptonSFs.py
# Script which gets the lepton SFs from central root files 
# Mateusz Zarucki 2016

import ROOT

def getLeptonSFs(pt, eta, lepton = "muon", id = "loose", SFs = "FullSim_FastSim"):
   
   print "Getting", SFs, " lepton SFs for", lepton, "with id:", id
 
   dir1 = "/afs/hephy.at/data/mzarucki01/leptonSFs/" + SFs
 
   if SFs == "data_FullSim":
      if lepton == "muon":
         if id == "loose": 
            filename = "FullSimSFs_mu_LooseID.root"
            histname = "pt_abseta_PLOT_pair_probeMultiplicity_bin0" 
      if lepton == "electron":
         filename = "FullSimSFs_el.root"
         if id == "veto":
            histname = "GsfElectronToVeto" 
   elif SFs == "FullSim_FastSim":
      if lepton == "muon":
         if id == "loose": 
            filename = "Full-FastSimSFs_mu_LooseID.root"
            histname = "histo2D" 
      if lepton == "electron":
         if id == "veto":
            filename = "Full-FastSimSFs_el_VetoID.root"
            histname = "histo2D" 

   f = ROOT.TFile(dir1 + "/" + filename)
   h = f.Get(histname)
   
   #print f.ls()
   
   #   histo = h.Clone()
   #   return histo
     
   #def getLeptonSF(hist, pt, eta):
   
   binX = h.GetXaxis().FindBin(pt)
   binY = h.GetYaxis().FindBin(abs(eta))
   
   if binX < h.GetXaxis().GetFirst():
      print "pt out of SF range. Using first bin value"
      binX = h.GetXaxis().GetFirst()
   if binX > h.GetXaxis().GetLast():
      print "pt out of SF range. Using last bin value"
      binX = h.GetXaxis().GetLast()
   
   if binY > h.GetYaxis().GetLast():
      print "eta out of SF range. Using last bin value"
      binY = h.GetYaxis().GetLast()
   
   #bin = h.FindBin(pt,abs(eta)) #NOTE: not modified to take last bin value
   bin = h.GetBin(binX, binY)
   
   print "x-bin #:", binX, "y-bin #:", binY,"Global bin #", bin
   
   if binY < h.GetYaxis().GetFirst():
      print "ybin < first. Something is wrong. Exiting"
      sys.exit(0)
  
   SF = h.GetBinContent(bin) 
   
   if binY < h.GetYaxis().GetFirst() or not SF:
      print "SF = 0. Something is wrong. Exiting"
      sys.exit(0)
   
   print "For pt", pt, "and eta", eta, "SF = ", SF
   return SF 
