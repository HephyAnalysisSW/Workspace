from ROOT import *
from math import *
import os, sys, time
import itertools

startM = time.clock()
startC = time.time()

infile = sys.argv[1]
outfile = sys.argv[2]

#sys.argv[3]

skims = {
            'pre1Lep' : { 'nLepGood':1 , 'met':200, 'ht':250 } ,
            'srcr'    : { 'nLepGood':1 , 'met':250, 'ht':250 } ,
        }

selected_skim = "srcr" #sys.argv[3]

selected_skim_cuts = skims[selected_skim]

CUT_NLEPGOOD = selected_skim_cuts['nLepGood']
CUT_MET      = selected_skim_cuts['met']
CUT_HT       = selected_skim_cuts['ht']

print "\n"
print "Skim Cuts", selected_skim_cuts
print "\n"

#script = os.path.expandvars("$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/leptonSFs/FixEleDoubleSF.C")
#gROOT.ProcessLineSync(".L  %s"%script)

def getLeptonSFs(pdgId, pt, eta, ID = "loose", SFs = "FullSim_FastSim", typeSF = '', path = "/afs/hephy.at/user/m/mzarucki/public/results2017/FullFastSFs"):

   if abs(pdgId) == 13:
      lep = 'mu'
   elif abs(pdgId) == 11:
      lep = 'el'
   else:
      print "Object not electron or muon"
      return
  
   if not typeSF in ['central', 'factorised']: 
      print "SFs type has to be either 'central' or 'factorised'. Exiting."
      return

   #print "Getting", typeSF, " ", SFs, "lepton SFs for", lep, "with", ID, "ID", "in:", path

   if SFs == "FullSim_FastSim":
      if typeSF == "central":
         if lep == "mu":
            if ID == "loose":
               filename = "sf_mu_looseID.root"
               histname = "histo2D"
         if lep == "el":
            if ID == "veto":
               filename = "sf_el_vetoCB.root"
               histname = "histo2D"
      
      elif typeSF == "factorised":
         if lep == "mu":
            if ID == "loose":
               filename = "Full-FastSimSFs_2D_mu_HI+IP.root"
               histname = "Full-Fast_ratios_2D"
         if lep == "el":
            if ID == "veto":
               filename = "Full-FastSimSFs_2D_el_HI+IP.root"
               histname = "Full-Fast_ratios_2D"
   
   #elif SFs == "data_FullSim":
   #   if typeSF == "central":
   #      if lep == "mu":
   #         if ID == "loose":
   #            filename = "FullSimSFs_mu_LooseID.root"
   #            histname = "pt_abseta_PLOT_pair_probeMultiplicity_bin0"
   #      if lep == "el":
   #         filename = "FullSimSFs_el.root"
   #         if ID == "veto":
   #            histname = "GsfElectronToVeto"
   
   f = TFile(path + "/" + filename)
   
   if typeSF == "factorised":
      h = f.Get('c5').GetPrimitive(histname)
   else:   
      h = f.Get(histname)

   #print f.ls()

   #   histo = h.Clone()
   #   return histo

   #def getLeptonSF(hist, pt, eta):

   binX = h.GetXaxis().FindBin(pt)
   binY = h.GetYaxis().FindBin(abs(eta))

   if binX < h.GetXaxis().GetFirst():
      #print "pt out of SF range. Using first bin value"
      binX = h.GetXaxis().GetFirst()
   if binX > h.GetXaxis().GetLast():
      #print "pt out of SF range. Using last bin value"
      binX = h.GetXaxis().GetLast()

   if binY > h.GetYaxis().GetLast():
      #print "eta out of SF range. Using last bin value"
      binY = h.GetYaxis().GetLast()

   #bin = h.FindBin(pt,abs(eta)) #NOTE: not modified to take last bin value
   bin = h.GetBin(binX, binY)

   #print "x-bin #:", binX, "y-bin #:", binY,"Global bin #", bin

   if binY < h.GetYaxis().GetFirst():
      print "ybin < first. Something is wrong. Exiting"
      sys.exit(0)

   SF = h.GetBinContent(bin)

   if binY < h.GetYaxis().GetFirst() or not SF:
      print "SF = 0. Something is wrong. Exiting"
      return

   #print "For pt", pt, "and eta", eta, "SF = ", SF
   return SF

f = TFile(infile)
t = f.Get("Events")

g = TFile(outfile,"recreate")
a = t.CloneTree(0)
print 'branches'

strstr = "\
struct newvars_t {\
    Float_t LepGood_FullFastSF[10];\
}"

gROOT.ProcessLine(strstr)
nv = newvars_t()

a.Branch("LepGood_FullFastSF",AddressOf(nv,"LepGood_FullFastSF"),"LepGood_FullFastSF[nLepGood]/F")

SFdir = "/afs/hephy.at/user/m/mzarucki/public/results2017/FullFastSFs"

for i in xrange(t.GetEntries()):
#    if i>10: break
    if(i%100000==0): print i
    t.GetEntry(i)

    nLepGood = t.nLepGood
    if nLepGood < CUT_NLEPGOOD : 
        continue

    met = t.met
    if met < CUT_MET:
        continue

    ht = t.ht_basJet_def
    if ht < CUT_HT:
        continue

    for il in range( nLepGood ):
        lepPdgId    =  t.LepGood_pdgId[il]
        lepPt       =  t.LepGood_pt[il]
        lepEta      =  t.LepGood_eta[il]
        #lepEtaSc    =  t.LepGood_etaSc[il]
        #lepSF       =  t.LepGood_sf[il]

        if abs(lepPdgId) == 13:
           ID = 'loose'
        elif abs(lepPdgId) == 11:
           ID = 'veto'

        sf_central =   getLeptonSFs(lepPdgId, lepPt, lepEta, ID = ID, SFs = "FullSim_FastSim", typeSF = 'central', path = SFdir)
        sf_factorised = getLeptonSFs(lepPdgId, lepPt, lepEta, ID = ID, SFs = "FullSim_FastSim", typeSF = 'factorised', path = SFdir)
        
        tot_sf = sf_central * sf_factorised 

        nv.LepGood_FullFastSF[il] = tot_sf   
    
    a.Fill()
    
g.cd()
a.Write()
g.Close()
f.Close()

endM = time.clock()
endC = time.time()

print "-"*20
print "machine:", (endM-startM), "wall clock:", (endC-startC)
