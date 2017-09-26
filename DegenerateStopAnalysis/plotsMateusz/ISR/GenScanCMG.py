# GenScanCMG.py
# Mateusz Zarucki 2017

import ROOT
import glob
import argparse
import sys, os

from Workspace.DegenerateStopAnalysis.tools.degTools import makeDir

path = "/afs/hephy.at/data/mzarucki01/ISR_GenInfo_NEW"

bins = [x for x in os.listdir(path) if os.path.isdir(path + '/' + x)]

for bin in bins:
   cmgPath = "%s/WJetsToLNu_HT*/treeProducerSusySingleLepton/tree.root"%path
   #cmgPath = "%s/%s/treeProducerSusySingleLepton/tree.root"%(path, bin)
   files = glob.glob(cmgPath)
   t = ROOT.TChain("tree")
   for f in files:
      t.Add(f)

savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/8025_mAODv2_v7/80X_postProcessing_v0/ISR/GenInfo"
makeDir(savedir)

save = True

if save:
   t.SetScanField(0)
   t.GetPlayer().SetScanRedirect(True)
   t.GetPlayer().SetScanFileName(savedir + "/GenInfoScanW_Jet.txt")

t.Scan("evt:Jet_mcFlavour:Jet_pt:Jet_eta:Jet_phi:genPartAll_pt:genPartAll_eta:genPartAll_phi:genPartAll_motherId:genPartAll_pdgId:genPartAll_status:GenPart_pt:GenPart_eta:GenPart_phi:GenPart_pdgId:GenPart_motherId:GenPart_status:GenPart_sourceId", "1")
