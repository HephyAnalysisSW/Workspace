import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.navidTools.Sample import Sample, Samples
from Workspace.DegenerateStopAnalysis.colors import colors
from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2 import cmgTuplesPostProcessed
import Workspace.DegenerateStopAnalysis.weights as weights
import pickle

mc_path     = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2_v6/7412pass2_SMSScan_v1/RunIISpring15DR74_25ns"
signal_path = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2_v6/7412pass2_SMSScan_v1/RunIISpring15DR74_25ns"
data_path   = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2_v6/7412pass2_SMSScan_v1/Data_25ns"
#in cmgTuplesPostProcessed_mAODv2
cmgPP = cmgTuplesPostProcessed(mc_path, signal_path, data_path)

mass_dict_pickle = "/data/nrad/cmgTuples/7412pass2_mAODv2_v6/RunIISpring15MiniAODv2/mass_dict.pkl"
#mass_dict_all = "/afs/hephy.at/user/n/nrad/CMSSW/fork/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/cmgPostProcessing/mass_dict_all.pkl"
mass_dict = pickle.load(open(mass_dict_pickle,"r"))

skim='presel'

ISRweight = 1 #9.5e-5

lumis = {'lumi_mc':10000., 
         'lumi_target':2300., 
         'lumi_data_blind':2245.386, 
         'lumi_data_unblind':139.63}

print makeLine()
for l in lumis: print l, ": ", lumis[l]
print makeLine()

def getSamples(wtau=False, sampleList=['w','tt','z','sig'], useHT=False, getData=False, blinded=True, scan=True, skim='presel', cmgPP=cmgPP, 
               lumi_target = lumis['lumi_target'], lumi_mc = lumis['lumi_mc'], lumi_data_blind = lumis['lumi_data_blind'], lumi_data_unblind = lumis['lumi_data_unblind']):

    data_filters = "Flag_METFILTERS && Flag_Veto_Event_List"
    data_triggers= "HLT_PFMET170_JetIdCleaned"

    sampleDict = {}
    htString = "HT" if useHT else "Inc"
    
    if any([x in sampleList for x in ["s30", "s30FS","s10FS","s60FS" , "t2tt30FS"]]):
        sampleDict.update({
           "s30":{'sample':cmgPP.T2DegStop_300_270[skim], 'name':'S300_270', 'color':colors["s30"], 'isSignal':1, 'isData':0, "lumi":lumi_mc, "weight":weights.isrWeight(ISRweight)},
           "s60FS":{'sample':cmgPP.T2DegStop_300_240_FastSim[skim], 'name':'S300_240Fast', 'color':colors["s60FS"], 'isSignal':1, 'isData':0, "lumi":lumi_mc, "triggers":"", "filters":"", "weight":"(weight*0.3520*(%s))"%weights.isrWeight(ISRweight)},
           "s30FS":{'sample':cmgPP.T2DegStop_300_270_FastSim[skim], 'name':'S300_270Fast', 'color':colors["s30FS"], 'isSignal':1, 'isData':0, "lumi":lumi_mc, "triggers":"", "filters":"", "weight":"(weight*0.2647*(%s))"%weights.isrWeight(ISRweight)},
           "s10FS":{'sample':cmgPP.T2DegStop_300_290_FastSim[skim], 'name':'S300_290Fast', 'color':colors["s10FS"], 'isSignal':1, 'isData':0, "lumi":lumi_mc, "triggers":"", "filters":"", "weight":"(weight*0.2546*(%s))"%weights.isrWeight(ISRweight)},
           "t2tt30FS":{'sample':cmgPP.T2tt_300_270_FastSim[skim], 'name':'T2tt300_270Fast', 'color':colors["t2tt30FS"], 'isSignal':1 , 'isData':0, "lumi":lumi_mc, "triggers":"", "filters":"", "weight":"(weight*0.2783*(%s))"%weights.isrWeight(ISRweight)}})
    if "w" in sampleList:
        WJetsSample     = cmgPP.WJetsHT[skim] if useHT else cmgPP.WJetsInc[skim]
        sampleDict.update({'w':{'sample':WJetsSample, 'name':'WJets', 'color':colors['w'], 'isSignal':0 , 'isData':0, "lumi":lumi_mc}})
    if "z" in sampleList:
        sampleDict.update({'z':{'sample':cmgPP.ZJetsHT[skim], 'name':'ZJetsInv', 'color':colors['z'], 'isSignal':0, 'isData':0, "lumi":lumi_mc}})

    if "tt" in sampleList:
       if useHT:
           TTJetsHTLowChain = getChain(cmgPP.TTJetsHTLow[skim], histname='')
           TTJetsHTHighChain = getChain(cmgPP.TTJetsHTHigh[skim], histname='')
           TTJetsHTRestChain = getChain(cmgPP.TTJetsHTRest[skim], histname='')
           TTJetsHTRestChain.Add(cmgPP.TTJetsHTLowChain)
           TTJetsHTRestChain.Add(cmgPP.TTJetsHTHighChain)
           
           sampleDict.update({'tt':{'tree':TTJetsHTRestChain, 'sample':cmgPP.TTJetsHTRest[skim], 'name':'TTJets', 'color':colors['tt'], 'isSignal':0, 'isData':0, "lumi":lumi_mc}})

       else:
           sampleDict.update({'tt':{'sample':cmgPP.TTJetsInc[skim], 'name':'TTJets', 'color':colors['tt'], 'isSignal':0, 'isData':0, "lumi":lumi_mc }})

    if "qcd" in sampleList:
        sampleDict.update({'qcd':{'sample':cmgPP.QCD[skim], 'name':'QCD', 'color':colors['qcd'], 'isSignal':0 ,'isData':0, "lumi":lumi_mc}})

    if "d" in sampleList or "dblind" in sampleList:
        if blinded:
          METDataOct05 = getChain(cmgPP.MET_Oct05[skim],histname='')
          METDataUnblind = METDataOct05.CopyTree("run<=257599")
          METDataBlind = getChain(cmgPP.MET_v4[skim],histname='')
          METDataBlind.Add(METDataOct05)
          sampleDict.update(
             {"d":{'tree':METDataUnblind, "sample":cmgPP.MET_Oct05[skim], 'name':"DataUnblind", 'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":"", "filters":"", "weight":"(1)", 'lumi': lumi_data_unblinded},
              "dblind":{'tree':METDataBlind, "sample":cmgPP.MET_v4[skim], 'name':"DataBlind", 'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":data_triggers, "filters":"", "weight":"(1)", 'lumi':lumi_data_blinded}})
        else:
            assert False

    if wtau:
        print "Getting the Tau and Non-Tau components of WJets"
        WJetsTauSample = cmgPP.WJetsTauHT[skim] if useHT else cmgPP.WJetsTauInc[skim]
        WJetsNoTauSample = cmgPP.WJetsNoTauHT[skim] if useHT else cmgPP.WJetsNoTauInc[skim]
        
        sampleDict.update({
           'wtau':{'sample':WJetsTauSample, 'name':'WTau%s'%htString, 'color':colors['wtau'], 'isSignal':0 , 'isData':0, "lumi":lumi_mc},
           'wnotau':{'sample':WJetsNoTauSample, 'name':'WNoTau%s'%htString, 'color':colors['wnotau'], 'isSignal':0 , 'isData':0, "lumi":lumi_mc}})

    if scan:
        icolor = 1
        #skim = "inc"
        for mstop in mass_dict:
            for mlsp in mass_dict[mstop]:
               if mstop == 475 and mlsp == 395: continue #missing
               #icolor += 1 
               sampleDict.update({'s%s_%s'%(mstop,mlsp):{'sample':getattr(cmgPP,"SMS_T2_4bd_mStop_%s_mLSP_%s"%(mstop,mlsp))[skim], 'name':'T2_4bd%s_%s'%(mstop,mlsp), "weight":"(weight*(%s))"%weights.isrWeight(ISRweight) , 'color': icolor, 'isSignal':1 , 'isData':0, "lumi":lumi_mc}})
    
    sampleDict2 = {}
    for samp in sampleDict:
      sampleDict2[samp]=Sample(**sampleDict[samp])
    samples = Samples(**sampleDict2)
      
    for s in samples: samples[s].weight = "weight" #removes ISR reweighting from official mass scan signal samples
    
    print makeLine()
    print "Reweighting to target luminosity of " + str(lumi_target) + " with factor: " + str(lumi_target/lumi_mc)
    print makeLine()
    samples.addWeight(lumi_target/lumi_mc) # scale to the target luminosity

    return samples
