#getSamples.py

import os, sys
import re
import glob
import pprint as pp
import pickle
import ROOT

from Workspace.HEPHYPythonTools.helpers import getChain
from Workspace.DegenerateStopAnalysis.tools.degTools import makeDir 
from Workspace.DegenerateStopAnalysis.tools.Sample import Sample, Samples
from Workspace.DegenerateStopAnalysis.tools.weights import Weight, Weights
from Workspace.DegenerateStopAnalysis.tools.colors import colors
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import lumis, triggers, sample_names 
import  Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo as sampleInfo

sample_names = sampleInfo.sample_names

### Weights ###

weights_= Weights()
def_weights=weights_.def_weights
weights = weights_.weights

### Data Lumi & Triggers ###

lumis     = sampleInfo.lumis
data_runs = sampleInfo.data_runs
triggers  = sampleInfo.triggers
filters  =  sampleInfo.filters

def makeDataSample( runs, sample, tree, triggers, filters , niceName = None, data_runs = data_runs):
    runs    = sorted(runs) 
    runs_name    = "".join(runs)
    if not niceName:
        niceName = "Data" + runs_name
    run_cut_list = []
    for run in runs:
        run_cut = " (run>=%s && run<=%s) "%data_runs[run]['runs']
        run_cut_list.append(run_cut)
    run_cuts = "(%s)"%(" || ".join(run_cut_list))
    total_lumi = sum([data_runs[x]['lumi'] for x in runs] )
    data = {
     'name'     :niceName,           
     'sample'   :sample,      
     'tree'     :tree,      
     'color'    :ROOT.kBlack, 
     'isSignal' :0 , 
     'isData'   :1, 
     "triggers" :triggers, 
     "filters"  : filters, 
     'lumi'     : total_lumi, 
     'cut':     run_cuts,
     'dir':     sample['dir']
    }
    return data, { niceName+"_lumi": total_lumi}
         
def getSamples(wtau=False, sampleList=['w','tt','z','sig'], 
               useHT=False, getData=False, blinded=True, scan=True, massPoints=[], skim='skimPresel', cmgPP=None, do8tev=False,
               weights = weights, def_weights = def_weights,
               triggers = triggers,
               mc_filters   = filters, 
               data_filters = filters, 
               kill_low_qcd_ht = False,
               lumis = lumis, 
               applyMCTriggers = False, # "data_met",
               ):
   
   if not cmgPP:
      print "cmgPP not specified. Exiting."
      sys.exit()
   
   lumis["MC_lumi"] = cmgPP.lumi
   
   htString = "HT" if useHT else "Inc"
   
   sampleDict = {}
   
   if getData:
      if "djet" in sampleList or "djetBlind" in sampleList:
         JetHTDataBlind = getChain(cmgPP.JetHT[skim],histname='')
         JetHTDataUnblind  = JetHTDataBlind#.CopyTree("run<=274240") #instead cut on run # is applied
         sampleDict.update({
               "djet":     {'name':"JetHTDataUnblind", 'sample':cmgPP.JetHT[skim], 'tree':JetHTDataUnblind, 'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":triggers['data_jet'], "filters":data_filters, 'lumi': lumis['DataUnblind_lumi'], 'cut':"run<=275073"},
               "djetBlind":{'name':"JetHTDataBlind",   'sample':cmgPP.JetHT[skim], 'tree':JetHTDataBlind,   'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":triggers['data_jet'], "filters":data_filters, 'lumi': lumis['JetHTDataBlind_lumi']},
            })
      
      elif "d1mu" in sampleList or "d1muBlind" in sampleList:
         SingleMuDataBlind = getChain(cmgPP.SingleMu[skim],histname='')
         SingleMuDataUnblind  = SingleMuDataBlind#.CopyTree("run<=274240") #instead cut on run # is applied
         sampleDict.update({
               "d1mu":     {'name':"SingleMuDataUnblind", 'sample':cmgPP.SingleMu[skim], 'tree':SingleMuDataUnblind, 'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":triggers['data_mu'], "filters":data_filters, 'lumi': lumis['DataUnblind_lumi'], 'cut':"run<=275073"},
               "d1muBlind":{'name':"SingleMuDataBlind",   'sample':cmgPP.SingleMu[skim], 'tree':SingleMuDataBlind,   'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":triggers['data_mu'], "filters":data_filters, 'lumi': lumis['SingleMuDataBlind_lumi']},
            })

      elif "d1el" in sampleList or "d1elBlind" in sampleList:
         SingleElDataBlind = getChain(cmgPP.SingleEl[skim],histname='')
         SingleElDataUnblind  = SingleElDataBlind#.CopyTree("run<=274240") #instead cut on run # is applied
         sampleDict.update({
               "d1el":     {'name':"SingleElDataUnblind", 'sample':cmgPP.SingleEl[skim], 'tree':SingleElDataUnblind, 'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":triggers['data_el'], "filters":data_filters, 'lumi': lumis['DataUnblind_lumi'], 'cut':"run<=275073"},
               "d1elBlind":{'name':"SingleElDataBlind",   'sample':cmgPP.SingleEl[skim], 'tree':SingleElDataBlind,   'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":triggers['data_el'], "filters":data_filters, 'lumi': lumis['SingleElDataBlind_lumi']},
            })
      
      elif "d1lep" in sampleList or "d1lepBlind" in sampleList:
         SingleLepDataBlind = ROOT.TChain("Events", "Events")
         SingleMuDataBlind = getChain(cmgPP.SingleMu[skim],histname='')
         SingleElDataBlind = getChain(cmgPP.SingleEl[skim],histname='')
         SingleLepDataBlind.Add(SingleElDataBlind)
       
         ## removing duplicate events from SingleMu PD which also pass the electron trigger 
         #removeDuplicates = True
         #if removeDuplicates:
         #   print "Removing duplicates from d1lepBlind data sample"
         #   baseDir = "/afs/hephy.at/data/mzarucki01/tuples"
         #   baseDir += '/%s/%s'%(cmgPP.mc_path.split('/')[7], cmgPP.mc_path.split('/')[8])
         #   makeDir(baseDir)
         #   fileName = "%s/SingleElDataBlind_noOverlap"%baseDir

         #   if ROOT.TFile.Open('%s.root'%fileName):
         #      print "Opening", '%s.root'%fileName 
         #      #f = ROOT.TFile('%s.root'%fileName, 'read', fileName)
         #      #SingleElDataBlind = f.Get('Events')
         #      SingleLepDataBlind.Add('%s.root'%fileName)
         #   else:
         #      print "Creating", '%s.root'%fileName 
         #      f = ROOT.TFile('%s.root'%fileName, 'create', fileName)
         #      SingleElDataBlind_ = getChain(cmgPP.SingleEl[skim],histname='')

         #      #print "Removing duplicate events from d1lep dataset"
         #      cut = "(!(%s&&%s))"%(triggers['data_el'], triggers['data_lep_mu'])
         #      SingleElDataBlind = SingleElDataBlind_.CopyTree(cut).Clone()
         #      #print "Removed duplicate events from d1lep dataset"
         # 
         #      f.Write() 
         #      #f.Print() 
         #      f.Close()            
         # 
         #else:    
         #   SingleElDataBlind = getChain(cmgPP.SingleEl[skim],histname='')
         #   SingleLepDataBlind.Add(SingleElDataBlind)
         
         SingleLepDataBlind.Add(SingleMuDataBlind)
        
         sampleDict.update({
               "d1lepBlind":{'name':"SingleLepDataBlind",   'sample':None, 'tree':SingleLepDataBlind,   'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":triggers['data_lep'], "filters":data_filters, 'lumi': lumis['SingleLepDataBlind_lumi']},
               #"d1lep":     {'name':"SingleLepDataUnblind", 'sample':None, 'tree':SingleLepDataUnblind.Clone(), 'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":triggers['data_lep'], "filters":data_filters, 'lumi': lumis['DataUnblind_lumi'], 'cut':"run<=275073"},
            })
 
      else: # "d" in sampleList or "dblind" in sampleList:
         
         cmgDataPP   = getattr(cmgPP, "MET_03Feb", None)#[skim] 
         if not cmgDataPP:
            cmgDataPP = getattr(cmgPP, "MET" )
         cmgDataPP   = cmgDataPP[skim]
         METDataBlind= getChain( cmgDataPP , histname='')

         data_sets_to_make = [\
           ['dichep'  ,  ['B','C','D']        ,'DataICHEP'],
           ['dbcdef'  ,  ['B','C','D','E','F'], None]  ,
           ['dbcde'   ,  ['B','C','D','E' ], None]  ,
           ['dgh'     ,  ['G', 'H'], None]  ,
         ]

         for shortName, data_sets, niceName in data_sets_to_make:
            d, l = makeDataSample(data_sets, cmgDataPP , METDataBlind, triggers['data_met'], data_filters, niceName)
            sampleDict.update({
                     shortName: d
                     })
            lumis.update(l)

         sampleDict.update({
               "d":             {'name':"DataUnblind",         'sample':cmgDataPP,      'tree':METDataBlind,      'color':ROOT.kBlack, 'isSignal':0 , 'isData':1,   "triggers":triggers['data_met'], "filters":data_filters, 'lumi': lumis['DataUnblind_lumi'], 'cut':"run<=275073"},
               "dblind":        {'name':"DataBlind",           'sample':cmgDataPP,      'tree':METDataBlind,      'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":triggers['data_met'], "filters":data_filters, 'lumi': lumis['DataBlind_lumi']},
            })

   if "w" in sampleList or any([x.startswith("w") for x in sampleList]):
      if "w_lo" in sampleList and hasattr(cmgPP, "WJets_LO"):
             sampleDict.update({
                'w_lo'  :{'name':'WJets_LO',   'sample':cmgPP.WJets_LO[skim], 'color':colors['w']   , 'isSignal':0, 'isData':0, 'lumi':lumis["MC_lumi"]},
             })

      elif "w_nlo" in sampleList and hasattr(cmgPP, "WJets_NLO"):
             sampleDict.update({
                'w_nlo' :{'name':'WJets_NLO',  'sample':cmgPP.WJets_NLO[skim], 'color':colors['w']   , 'isSignal':0, 'isData':0, 'lumi':lumis["MC_lumi"]},
             })

      elif useHT:
         WJetsSample     = cmgPP.WJetsHT[skim]
         sampleDict.update({
            'w'     :{'name':'WJets',      'sample':WJetsSample, 'color':colors['w']   , 'isSignal':0, 'isData':0, 'lumi':lumis["MC_lumi"]},
            'wtau'  :{'name':'WJetsTau',   'sample':WJetsSample, 'color':colors['wtau'], 'isSignal':0, 'isData':0, 'lumi':lumis["MC_lumi"] ,'cut':"Sum$(abs(GenPart_pdgId)==15)"},
            'wnotau':{'name':'WJetsNoTau', 'sample':WJetsSample, 'color':colors['wnotau'], 'isSignal':0, 'isData':0, 'lumi':lumis["MC_lumi"] ,'cut':"Sum$(abs(GenPart_pdgId)==15)==0"},
         })
         
         wxsecs = [
                   1627.449951171875,
                   435.23699951171875,
                   59.18109893798828,
                   14.580499649047852,
                   6.656209945678711,
                   1.6080900430679321,
                   0.03891360014677048,
                  ]

         wxsecs.sort(reverse=True)
         
         if False:
            for ihtbin , xsec in enumerate(wxsecs,1):
              xseccut = "abs(xsec-%s)<1E-5"%xsec
              sampleDict['w%s'%ihtbin]={'name':'WJetsHT%s'%ihtbin, 'cut':xseccut   ,  'sample':WJetsSample, 'color':colors['w%s'%ihtbin]   , 'isSignal':0, 'isData':0, 'lumi':lumis["MC_lumi"]}
   
      else:
         WJetsSample     = cmgPP.WJetsPt[skim] # cmgPP.WJets_LO[skim] cmgPP.WJetsInc[skim]
         sampleDict.update({
            'w_pt'     :{'name':'WJets',      'sample':WJetsSample, 'color':colors['w']   , 'isSignal':0, 'isData':0, 'lumi':lumis["MC_lumi"]},
         })
      
   if "tt" in sampleList or 'tt_pow' in sampleList or 'tt_1l' in sampleList or 'tt_2l' in sampleList:
      #if useHT:
      if False:
         TTJetsHTRestChain = getChain(cmgPP.TTJetsHTRest[skim], histname='')
         TTJetsHTRestChain.Add(getChain(cmgPP.TTJetsHTLow[skim], histname=''))
         TTJetsHTRestChain.Add(getChain(cmgPP.TTJetsHTHigh[skim], histname=''))
         sampleDict.update({
            'tt':{'name':'TTJets', 'sample':cmgPP.TTJetsHTRest[skim], 'tree':TTJetsHTRestChain, 'color':colors['tt'], 'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"]},
         })
      #else:
      #if hasattr(cmgPP, "TT_pow"):
      #   sampleDict.update({
      #         #'tt':{'name':'TTJets', 'sample':cmgPP.TTJetsInc[skim], 'color':colors['tt'], 'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"]},
      #         'tt_pow':{'name':'TT_pow', 'sample':cmgPP.TT_pow[skim], 'color':colors['tt'], 'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"]},
      #      })
      
      splitTT = True

      if splitTT:
         sampleDict.update({
               #'tt':{'name':'TTJets', 'sample':cmgPP.TTJetsInc[skim], 'color':colors['tt'], 'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"]},
               'tt_1l':{'name':'TT_1l', 'sample':cmgPP.TTJets_SingleLepton[skim], 'color':colors['tt'] + 1, 'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"]},
               'tt_2l':{'name':'TT_2l', 'sample':cmgPP.TTJets_DiLepton[skim],    'color':colors['tt'] - 3, 'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"]},
            })
      
         #TT splitting based on gen
         #
         #semiLep = "(Sum$((abs(GenPart_pdgId) == 13 || abs(GenPart_pdgId) == 11) && GenPart_isPromptHard) < 2)"
         #diLep =   "(Sum$((abs(GenPart_pdgId) == 13 || abs(GenPart_pdgId) == 11) && GenPart_isPromptHard) == 2)"
         #
         #sampleDict.update({ 
         #      'tt_1l':{'name':'TT_1l', 'sample':cmgPP.TTJetsHTRest[skim], 'tree':TTJetsHTRestChain.Clone(), 'color':colors['tt'] + 2, 'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"], 'cut': semiLep}, # NOTE: includes 0l # cloning tree is required 
         #      'tt_2l':{'name':'TT_2l', 'sample':cmgPP.TTJetsHTRest[skim], 'tree':TTJetsHTRestChain.Clone(), 'color':colors['tt'] + 4, 'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"], 'cut': diLep}, # cloning tree is required
         #   })
         #sampleDict.update({
      #      'ttInc_FS':{'name':'TTJets_FastSim', 'sample':cmgPP.TTJetsInc_FS[skim], 'color':ROOT.kViolet+10, 'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"]},
      #   })
   
   if "z" in sampleList:
      sampleDict.update({
         'z':{'name':sample_names['z'], 'sample':cmgPP.ZJetsHT[skim], 'color':colors['z'], 'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"]},
      })
   
   if "qcd" in sampleList:
      if kill_low_qcd_ht:
         print "WARNING: Removing low HT QCD bins:" ,
         pp.pprint([x for x in  cmgPP.QCD[skim]['bins'] if ("200to300" in x or "300to500" in x)])
         cmgPP.QCD[skim]['bins'] = filter(lambda x: not ("200to300" in x or "300to500" in x), cmgPP.QCD[skim]['bins'])    
         print "WARNING: Reducing QCD bins to:", 
         pp.pprint( cmgPP.QCD[skim]['bins'] )
      
      sampleDict.update({
            'qcd':   {'name':'QCD',   'sample':cmgPP.QCD[skim]     , 'color':colors['qcd'],   'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"]},
      })
   
   if "dy" in sampleList or "dy5to50" in sampleList:
      #DYJetsSample = getChain(cmgPP.DYJetsM5to50HT[skim],histname='')
      sampleDict.update({
            'dy':         {'name':sample_names['dy'], 'sample':cmgPP.DYJetsM50HT[skim],    'color':colors['dy'],         'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"]},
            'dy5to50':    {'name':'DYJetsM5to50',     'sample':cmgPP.DYJetsM5to50[skim], 'color':colors['dy5to50'],    'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"]},
            #'dy5to50Inc':{'name':'DYJetsM5to50Inc',  'sample':cmgPP.DYJetsM5to50[skim],   'color':colors['dy5to50Inc'], 'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"]},
            #'dyInv':     {'name':'DYJetsInv',        'sample':cmgPP.DYJetsToNuNu[skim],   'color':colors['dyInv'],      'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"]},
      }) 
   
   if "vv" in sampleList:
      sampleDict.update({
            'vv': {'name':sample_names['vv'], 'sample':cmgPP.VV[skim], 'color':colors['vv'], 'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"]},
   }) 
   
   if "ttx" in sampleList:
      sampleDict.update({
            'ttx': {'name':sample_names['ttx'], 'sample':cmgPP.TTX[skim], 'color':colors['ttx'], 'isSignal':0 , 'isData':0, 'lumi':lumis["MC_lumi"]},
   }) 
   
   if any (["st" in samp for samp in sampleList]):
      sampleDict.update({
            #'st_tch_lep':{'name':'ST_tch_lep',       'sample':cmgPP.ST_tch_Lep[skim], 'color':colors['st_tch_lep'], 'isSignal':0, 'isData':0, 'lumi':lumis["MC_lumi"]},
            #'st_tch':    {'name':'ST_tch',           'sample':cmgPP.ST_tch[skim],     'color':colors['st_tch'],     'isSignal':0, 'isData':0, 'lumi':lumis["MC_lumi"]},
            #'st_wch':    {'name':'ST_wch',           'sample':cmgPP.ST_wch[skim],     'color':colors['st_wch'],     'isSignal':0, 'isData':0, 'lumi':lumis["MC_lumi"]},
            'st':        {'name':sample_names['st'], 'sample':cmgPP.ST[skim],         'color':colors['st'],         'isSignal':0, 'isData':0, 'lumi':lumis["MC_lumi"]},
            #'st_tch_lep':{'name':'ST_tch_lep',       'sample':cmgPP.ST_tch_Lep[skim], 'color':colors['st_tch_lep'], 'isSignal':0, 'isData':0, 'lumi':lumis["MC_lumi"]},
      }) 
   
   if wtau:
      print "Getting the Tau and Non-Tau components of WJets"
      WJetsTauSample = cmgPP.WJetsTauHT[skim] if useHT else cmgPP.WJetsTauInc[skim]
      WJetsNoTauSample = cmgPP.WJetsNoTauHT[skim] if useHT else cmgPP.WJetsNoTauInc[skim]
      sampleDict.update({
          'wtau':  {'name':'WTau%s'%htString,   'sample':WJetsTauSample,   'color':colors['wtau'],   'isSignal':0, 'isData':0, 'lumi':lumis["MC_lumi"]},
          'wnotau':{'name':'WNoTau%s'%htString, 'sample':WJetsNoTauSample, 'color':colors['wnotau'], 'isSignal':0, 'isData':0, 'lumi':lumis["MC_lumi"]}, 
      })
   
   if any( [x in sampleList for x in ["s30", "s30FS","s10FS","s60FS" , "t2tt30FS"]] ):
      sampleDict.update({
         "s30":     {'name':'S300_270',        'sample':cmgPP.T2DegStop_300_270[skim],         'color':colors["s30"],      'isSignal':2 , 'isData':0, 'lumi':lumis["MC_lumi"]},# ,'sumWeights':T2Deg[1], 'xsec':8.51615}, "weight":weights.isrWeight(9.5e-5)
         "s60FS":   {'name':'S300_240Fast',    'sample':cmgPP.T2DegStop_300_240_FastSim[skim], 'color':colors["s60FS"],    'isSignal':2 , 'isData':0, 'lumi':lumis["MC_lumi"]},# ,"weight":"(weight*0.3520)"},#, 'sumWeights':T2Deg[1], 'xsec':8.51615},
         "s30FS":   {'name':'S300_270Fast',    'sample':cmgPP.T2DegStop_300_270_FastSim[skim], 'color':colors["s30FS"],    'isSignal':2 , 'isData':0, 'lumi':lumis["MC_lumi"]},# ,"weight":"(weight*0.2647)"},#, 'sumWeights':T2Deg[1], 'xsec':8.51615},
         "s10FS":   {'name':'S300_290Fast',    'sample':cmgPP.T2DegStop_300_290_FastSim[skim], 'color':colors["s10FS"],    'isSignal':2 , 'isData':0, 'lumi':lumis["MC_lumi"]},# ,"weight":"(weight*0.2546)"},#, 'sumWeights':T2Deg[1], 'xsec':8.51615},
         "t2tt30FS":{'name':'T2tt300_270Fast', 'sample':cmgPP.T2tt_300_270_FastSim[skim],      'color':colors["t2tt30FS"], 'isSignal':2 , 'isData':0, 'lumi':lumis["MC_lumi"]},# ,"weight":"(weight*0.2783)"},#, 'sumWeights':T2Deg[1], 'xsec':8.51615},
      })
  
   # FullSim Signal Points 
   if any([x for x in sampleList if 'FullSim' in x]):
      sampleDict.update({
         "FullSim_275_205":{'name':'S275_205', 'sample':cmgPP.SMS_T2_4bd_275_205_FullSim[skim], 'color':colors["s30"],   'isSignal':3 , 'isData':0, 'lumi':lumis["MC_lumi"]},
         "FullSim_350_330":{'name':'S350_330', 'sample':cmgPP.SMS_T2_4bd_350_330_FullSim[skim], 'color':colors["s30FS"], 'isSignal':3 , 'isData':0, 'lumi':lumis["MC_lumi"]},
         "FullSim_400_350":{'name':'S400_350', 'sample':cmgPP.SMS_T2_4bd_400_350_FullSim[skim], 'color':colors["s60FS"], 'isSignal':3 , 'isData':0, 'lumi':lumis["MC_lumi"]},
      })
         
      if 'allFullSim' in sampleList:
         allFullSim = getChain(cmgPP.SMS_T2_4bd_275_205_FullSim[skim], histname='')
         allFullSim.Add(getChain(cmgPP.SMS_T2_4bd_350_330_FullSim[skim], histname=''))
         allFullSim.Add(getChain(cmgPP.SMS_T2_4bd_400_350_FullSim[skim], histname=''))

         sampleDict.update({
            'allFullSim':{'name':'allFullSim', 'sample':None, 'tree':allFullSim, 'color':colors['s30'], 'isSignal':3 , 'isData':0, 'lumi':lumis["MC_lumi"]},
         })
   
   if scan:
       
      icolor = 1
      signals_info = cmgPP.signals_info

      for signal_name, signal_info in signals_info.items():
            #sampleId              = signal_info['scanId']
            signal_mass_dict      = signal_info['pkl']
            mass_template         = signal_info['mass_template']
            mass_dict_pickle_file = signal_info['mass_dict']
 
            if not os.path.isfile(mass_dict_pickle_file) and not massPoints: 
                print 'No mass dict %s file found'%mass_dict_pickle_file
            else:
                mass_dict = pickle.load(file(mass_dict_pickle_file))
                print 'Found mass dict', signal_name, mass_dict.keys() 
        
            mstops_mlsps_dict = {} 
            if not massPoints:
               mstops = mass_dict.keys()
               for mstop in mstops:
                  mstops_mlsps_dict[mstop] = mass_dict[mstop].keys()  
            else:
               mstops = [x[0] for x in massPoints]

               for mstop in mstops:
                   mstops_mlsps_dict[mstop] = [] 
               for x in massPoints:
                   mstops_mlsps_dict[x[0]].append(x[1]) 
            
            for mstop in mstops:
               mlsps = mstops_mlsps_dict[mstop]

               for mlsp in mlsps:

                  if '74' in cmgPP.mc_path:
                      s = getattr(cmgPP,"SMS_T2_4bd_mStop_%s_mLSP_%s"%(mstop,mlsp), None )
                      signal_cut  = "(1)"
                      sigPostFix  = "74X"
                  else:
                      #s = getattr(cmgPP,"SMS_T2tt_mStop_%s_mLSP_%s"%(mstop,mlsp), None )
                      s = getattr(cmgPP, mass_template%(mstop,mlsp), None )
                      signal_cut = "Flag_veto_event_fastSimJets"
                      sigPostFix = ""
                  
                  if s and glob.glob("%s/%s/*.root"%(s[skim]['dir'],s[skim]['name'])):
                      sampleDict.update({
                         signal_info['shortName']%(mstop,mlsp):{'name':signal_info['niceName']%(mstop,mlsp), 'sample':s[skim], 'cut':signal_cut , 'color':colors['%s_%s'%(mstop,mlsp)], 'isSignal':1 , 'isData':0, 'lumi':lumis["MC_lumi"]},
                       })
                  else: 
                      print "!!! Sample %s not found !!!"%mass_template%(mstop,mlsp)
      
   if do8tev:
      sampleDir_8tev = "/data/imikulec/monoJetTuples_v8/copyfiltered/"
      get8TevSample = lambda mstop, mlsp : sampleDir_8tev  +"/"+"T2DegStop_{mstop}_{mlsp}/histo_T2DegStop_{mstop}_{mlsp}.root".format(mstop=mstop, mlsp=mlsp)
      icolor = 1
      for mstop in mass_dict:
         for mlsp in mass_dict[mstop]:
            name = "T2Deg8TeV_%s_%s"%(mstop,mlsp)
            rootfile = get8TevSample(mstop,mlsp)
            if os.path.isfile( rootfile):
               sampleDict.update({
                  's8tev%s_%s'%(mstop,mlsp):{'name':name, 'tree':getChain({'file':rootfile, 'name':name}), 'color':icolor, 'isSignal':3, 'isData':0, 'lumi':19700} ,
               })
      
      bkgDir_8tev = "/data/imikulec/monoJetTuples_v8/copy/"
      wjetDir = bkgDir_8tev+"/WJetsHT150v2/"
      wfiles = wjetDir
      sampleDict.update({
         'w8tev':{'name':'WJets8TeV', 'tree':getChain({'file': wjetDir+"/*.root", 'name':"wjets"}), 'color':colors['w'], 'isSignal':0 , 'isData':0, 'lumi':19700}, #'sumWeights':WJets[1] ,'xsec':20508.9*3},
      })
      
      ttjetDir = bkgDir_8tev+"/TTJetsPowHeg/"
      sampleDict.update({
         'tt8tev':{'name':'TTJets8TeV', 'tree':getChain({'file':ttjetDir+"/*.root", 'name':"ttjets"}), 'color':colors['tt'], 'isSignal':0 , 'isData':0, 'lumi':19700},
      })
   
   sampleDict2 = {}
   
   oldWeights = not type(def_weights)==type([])     
   
   if oldWeights:
       def_weights.update({'lumis':lumis})

   for samp in sampleDict:
      if oldWeights:
            if weights.has_key(samp):
               sampleDict[samp]["weights"] = Weight( weights[samp].weight_dict , def_weights )
            #elif scan and re.match("s\d\d\d_\d\d\d|s\d\d\d_\d\d|",samp).group():
            #   sampleDict[samp]["weights"] = weights["sigScan"]
            elif do8tev and re.match("s8tev\d\d\d_\d\d\d|s8tev\d\d\d_\d\d|",samp).group():                
               sampleDict[samp]["weights"] = weights["sigScan_8tev"]
            else:
               sampleDict[samp]["weights"] = Weight({}, def_weights)
      
      sampleDict2[samp] = Sample(**sampleDict[samp])
   
   samples = Samples(**sampleDict2)
   
   #applying filters
   for samp_name, sample in samples.iteritems():
       if not sample.isData:
          sample.filters = mc_filters 
       if applyMCTriggers and not sample.isData and not sample.isSignal:
          sample.triggers = triggers[applyMCTriggers] 
         
   return samples
