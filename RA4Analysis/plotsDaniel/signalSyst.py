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

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--singleGluinoMassPoint", dest="singleMP", default=False, action="store_true", help="small set")
parser.add_option("--mgl", dest="gluinoMass", default=1200, action="store", help="Set gluino mass")

(options, args) = parser.parse_args()

small =False
onlySystematics = True


signalRegions = signalRegions2016

presel = "!isData&&singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&st>250&&nJet30>2&&htJet30j>500"

WSB   = (3,4)
TTSB  = (4,5)

lumi = 12.88

weight = 'weight*('+str(lumi)+'/3.)*puReweight_true_max4*(singleMuonic*0.926+singleElectronic*0.963)*weight_ISR_new*lepton_muSF_HIP*lepton_muSF_mediumID*lepton_muSF_miniIso02*lepton_muSF_sip3d*lepton_eleSF_cutbasedID*lepton_eleSF_miniIso01*lepton_eleSF_gsf'

weight_Central_0b     = weight+'*weightBTag0_SF*reweightLeptonFastSimSF'
weight_Central_1b     = weight+'*weightBTag1_SF*reweightLeptonFastSimSF'

weight_bUp_0b         = weight+'*weightBTag0_SF_b_Up*reweightLeptonFastSimSF'
weight_bDown_0b       = weight+'*weightBTag0_SF_b_Down*reweightLeptonFastSimSF'
weight_lightUp_0b     = weight+'*weightBTag0_SF_light_Up*reweightLeptonFastSimSF'
weight_lightDown_0b   = weight+'*weightBTag0_SF_light_Down*reweightLeptonFastSimSF'

weight_leptonUp_0b    = weight+'*weightBTag0_SF*reweightLeptonFastSimSFUp'
weight_leptonDown_0b  = weight+'*weightBTag0_SF*reweightLeptonFastSimSFDown'

weights = [weight_bUp_0b,weight_bDown_0b,weight_lightUp_0b,weight_lightDown_0b,weight_leptonUp_0b,weight_leptonDown_0b]
#weights = [weight_bUp_0b,weight_bDown_0b,weight_lightUp_0b,weight_lightDown_0b]

#names = ['leptonUp','leptonDown']
names = ['bUp', 'bDown', 'lightUp','lightDown','leptonUp','leptonDown']

pickleDir = '/afs/hephy.at/data/easilar01/Ra40b/pickleDir/T5qqqqWW_mass_nEvents_xsec_pkl'
mass_dict = pickle.load(file(pickleDir))
    
singleMP = options.singleMP
smallSetMGL = int(options.gluinoMass)

if singleMP: mass_dict = {smallSetMGL:mass_dict[smallSetMGL]}

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

      #loop over signal points
      for mGl in mass_dict:
        unc[srNJet][stb][htb][mGl] = {}
        print
        print 'Gluino mass', mGl
        if small: mLSPs = [500]
        else: mLSPs = mass_dict[mGl]
        for mLSP in mLSPs:
          unc[srNJet][stb][htb][mGl][mLSP] = {}
          
          print 'LSP mass', mLSP
          
          c = getChain(allSignals[0][mGl][mLSP], histname='')
          
          # get central yields
          if not onlySystematics:
            unc[srNJet][stb][htb][mGl][mLSP]['yield_MB_CR'], unc[srNJet][stb][htb][mGl][mLSP]['err_MB_CR'] = getYieldFromChain(c, cutString = cutMB+'&&deltaPhi_Wl<'+str(dPhi), weight = weight_Central_0b, returnError =True)
            unc[srNJet][stb][htb][mGl][mLSP]['yield_SB_W_CR'], unc[srNJet][stb][htb][mGl][mLSP]['err_SB_W_CR'] = getYieldFromChain(c, cutString = cutWSB+'&&deltaPhi_Wl<'+str(dPhi), weight = weight_Central_0b, returnError =True)
            unc[srNJet][stb][htb][mGl][mLSP]['yield_SB_W_SR'], unc[srNJet][stb][htb][mGl][mLSP]['err_SB_W_SR'] = getYieldFromChain(c, cutString = cutWSB+'&&deltaPhi_Wl>='+str(dPhi), weight = weight_Central_0b, returnError =True)
            unc[srNJet][stb][htb][mGl][mLSP]['yield_SB_tt_CR'], unc[srNJet][stb][htb][mGl][mLSP]['err_SB_tt_CR'] = getYieldFromChain(c, cutString = cutTTSB+'&&deltaPhi_Wl<'+str(dPhi), weight = weight_Central_1b, returnError =True)
            unc[srNJet][stb][htb][mGl][mLSP]['yield_SB_tt_SR'], unc[srNJet][stb][htb][mGl][mLSP]['err_SB_tt_SR'] = getYieldFromChain(c, cutString = cutTTSB+'&&deltaPhi_Wl>='+str(dPhi), weight = weight_Central_1b, returnError =True)


          unc[srNJet][stb][htb][mGl][mLSP]['yield_MB_SR'], unc[srNJet][stb][htb][mGl][mLSP]['err_MB_SR'] = getYieldFromChain(c, cutString = cutMB+'&&deltaPhi_Wl>='+str(dPhi), weight = weight_Central_0b, returnError =True)
          
          val_highDPhi = {}
          unc_highDPhi = {}
          for iw, w in enumerate(weights):
            val_highDPhi[names[iw]] = getYieldFromChain(c, cutString = cutMB+'&&deltaPhi_Wl>='+str(dPhi), weight = w)
          
          # calculate deltas
          for i in range(0,len(weights)):
            if unc[srNJet][stb][htb][mGl][mLSP]['yield_MB_SR']>0:
              unc_highDPhi[names[i]+'_MB_SR'] = (unc[srNJet][stb][htb][mGl][mLSP]['yield_MB_SR'] - val_highDPhi[names[i]]) / unc[srNJet][stb][htb][mGl][mLSP]['yield_MB_SR']
            else:
              unc_highDPhi[names[i]+'_MB_SR'] = val_highDPhi[names[i]]
              print 'Central value was zero!!'
              print val_highDPhi[names[i]]
            
            #print 'Var '+names[i]+':', unc_highDPhi
            #unc[srNJet][stb][htb][mGl][mLSP][names[i]+'_MB_SR'] = unc_highDPhi
          
          #unc[srNJet][stb][htb][mGl][mLSP]['sys_b_MB_SR']       = (abs(unc_highDPhi['bUp_MB_SR'])       + abs(unc_highDPhi['bDown_MB_SR']))/2 #asymmetric - take max?
          #unc[srNJet][stb][htb][mGl][mLSP]['sys_light_MB_SR']   = (abs(unc_highDPhi['lightUp_MB_SR'])   + abs(unc_highDPhi['lightDown_MB_SR']))/2 #asymmetric - take max?
          unc[srNJet][stb][htb][mGl][mLSP]['sys_b_MB_SR']       = max([abs(unc_highDPhi['bUp_MB_SR']), abs(unc_highDPhi['bDown_MB_SR'])]) #asymmetric - take max?
          unc[srNJet][stb][htb][mGl][mLSP]['sys_light_MB_SR']   = max([abs(unc_highDPhi['lightUp_MB_SR']), abs(unc_highDPhi['lightDown_MB_SR'])]) #asymmetric - take max?
          unc[srNJet][stb][htb][mGl][mLSP]['sys_lepton_MB_SR']  = (abs(unc_highDPhi['leptonUp_MB_SR'])  + abs(unc_highDPhi['leptonDown_MB_SR']))/2 #symmetric, so take average
          del c


picklePath = '/afs/hephy.at/data/dspitzbart01/Results2016/signal_uncertainties/'
pickleName = 'SF_unc_'

if singleMP: pickleName+='mgl'+str(smallSetMGL)
else: pickleName+='mgl_all'

pickle.dump(unc, file(picklePath+pickleName+'_pkl','w'))
print
print 'saved results in',picklePath+pickleName+'_pkl'



