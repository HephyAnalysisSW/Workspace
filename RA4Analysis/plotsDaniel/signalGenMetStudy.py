import ROOT
import os, sys, copy
import pickle, operator

from math import *
from array import array
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed_2 import *

from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_postProcessed import *

small = True


signalRegions = signalRegions2016

presel = "!isData&&singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&st>250&&nJet30>2&&htJet30j>500"

presel_mod = "!isData&&singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&nJet30>2&&htJet30j>500&&(leptonPt+met_genPt)>250"
deltaPhiGenMet = "acos((leptonPt+met_genPt*cos(leptonPhi-met_genPhi))/sqrt(leptonPt**2+met_genPt**2+2*met_genPt*leptonPt*cos(leptonPhi-met_genPhi)))"

WSB   = (3,4)
TTSB  = (4,5)

lumi = 12.88

weight = 'weight*'+str(lumi)+'/3.'

weight_Central_0b     = weight+'*weightBTag0_SF*reweightLeptonFastSimSF'
weight_Central_1b     = weight+'*weightBTag1_SF*reweightLeptonFastSimSF'


pickleDir = '/afs/hephy.at/data/easilar01/Ra40b/pickleDir/T5qqqqWW_mass_nEvents_xsec_pkl'
mass_dict = pickle.load(file(pickleDir))

smallSetMGL = 1200

if small: mass_dict = {smallSetMGL:mass_dict[smallSetMGL]}

if small:
  signalRegions = {(5,5): {(350, 450): {(500, -1): {'deltaPhi': 1.}},
                            (450, -1):  {(500, -1): {'deltaPhi': .75}}},
                    (6,-1):{(350, 450): {(500, -1): {'deltaPhi': 1.}},
                            (450, -1):  {(500, -1): {'deltaPhi': .75}}}
                   }

bins = ['MB_CR', 'MB_SR', 'SB_W_CR', 'SB_W_SR', 'SB_TT_CR', 'SB_TT_SR']

unc = {}
for srNJet in sorted(signalRegions):
  unc[srNJet] = {}
  for stb in sorted(signalRegions[srNJet]):
    unc[srNJet][stb] = {}
    for htb in sorted(signalRegions[srNJet][stb]):
      unc[srNJet][stb][htb] = {}
      dPhi = signalRegions[srNJet][stb][htb]['deltaPhi']

      print
      print '#################################################'
      print '## Uncertainties for SR',str(srNJet),str(stb),str(htb)
      print '## Using a dPhi cut value of',str(dPhi)
      print '#################################################'
      print

      nameMB, cutMB     = nameAndCut(stb, htb, srNJet, btb=None, presel = presel)
      nameWSB, cutWSB   = nameAndCut(stb, htb, WSB, btb=None, presel = presel)
      nameTTSB, cutTTSB = nameAndCut(stb, htb, TTSB, btb=None, presel = presel)
      
      nameMB, cutMBgen     = nameAndCut(stb, htb, srNJet, btb=None, presel = presel_mod, stVar = '(leptonPt+met_genPt)')
      nameWSB, cutWSBgen   = nameAndCut(stb, htb, WSB, btb=None, presel = presel_mod, stVar = '(leptonPt+met_genPt)')
      nameTTSB, cutTTSBgen = nameAndCut(stb, htb, TTSB, btb=None, presel = presel_mod, stVar = '(leptonPt+met_genPt)')

      #loop over signal points
      for mGl in mass_dict:
        unc[srNJet][stb][htb][mGl] = {}
        print
        print 'Gluino mass', mGl
        for mLSP in mass_dict[mGl]:
          unc[srNJet][stb][htb][mGl][mLSP] = {}

          print 'LSP mass', mLSP

          c = getChain(allSignals[0][mGl][mLSP], histname='')
          
          uncBin = {}
          # get central yields
          d = [
          {'name':'MB', 'cut':cutMB, 'dPhiVar':'deltaPhi_Wl', 'weight':weight_Central_0b},
          {'name':'SB_W', 'cut':cutWSB, 'dPhiVar':'deltaPhi_Wl', 'weight':weight_Central_0b},
          {'name':'SB_TT', 'cut':cutTTSB, 'dPhiVar':'deltaPhi_Wl', 'weight':weight_Central_1b},

          {'name':'gen_MB', 'cut':cutMBgen, 'dPhiVar':deltaPhiGenMet, 'weight':weight_Central_0b},
          {'name':'gen_SB_W', 'cut':cutWSBgen, 'dPhiVar':deltaPhiGenMet, 'weight':weight_Central_0b},
          {'name':'gen_SB_TT', 'cut':cutTTSBgen, 'dPhiVar':deltaPhiGenMet, 'weight':weight_Central_1b},
          ]
          for job in d:
            h = getPlotFromChain(c, job['dPhiVar'], [0,dPhi,3.2], cutString = job['cut'], weight = job['weight'], binningIsExplicit=True)
            uncBin['yield_'+job['name']+'_CR'] = h.GetBinContent(1)
            uncBin['yield_'+job['name']+'_CR'] = h.GetBinError(1)
            uncBin['yield_'+job['name']+'_SR'] = h.GetBinContent(2)
            uncBin['yield_'+job['name']+'_SR'] = h.GetBinError(2)
            del h
          
          for b in bins:
            uncBin['mod_yield_'+b] = (uncBin['yield_gen_'+b] + uncBin['yield_'+b])/2.
            uncBin['mod_err_'+b]   = abs(uncBin['yield_gen_'+b] - uncBin['yield_'+b])/2.
          
          unc[srNJet][stb][htb][mGl][mLSP] = uncBin
          del c
