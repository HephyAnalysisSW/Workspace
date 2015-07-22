from cardFileWriter import cardFileWriter
from limit_helper import plotsignif , plotLimit , signal_bins_3fb
from math import exp
import os,sys
import ROOT
import pickle
import array
import numpy as n
from Workspace.RA4Analysis.signalRegions import *


ROOT.gROOT.LoadMacro("/afs/hephy.at/work/e/easilar/Working_directory/CMSSW_7_1_5/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()

path = "/afs/hephy.at/user/e/easilar/www/PHYS14v3/limit_results/singleLeptonic/combined_bin_tests_Pred_error/"

#path = "/afs/hephy.at/user/e/easilar/www/PHYS14v3/limit_results/singleMuonic/combined_bin_JJ/"
if not os.path.exists(path):
  os.makedirs(path)

path_table = "/afs/hephy.at/user/e/easilar/www/PHYS14v3/limit_results/singleLeptonic/combined_bin_tests/tables/"
if not os.path.exists(path_table):
  os.makedirs(path_table)


text_path = "text_files"
if not os.path.exists(text_path):
  os.makedirs(text_path)

options = ['signif' , 'limit']
option = options[1]

lumi_bins = [1,2,3,4,5,6,7,8,9,10]
#lumi_bins = [1,2,3,4]
#lumi_bins = [3,10]
lumi_origin = 3


#bin_yields2 = pickle.load(file('/data/dspitzbart/lumi3.0yields_pkl_newOpt'))
#bin_yields2 = pickle.load(file('/data/dspitzbart/lumi3.0yields_pkl_final'))
#res = pickle.load(file('/data/easilar/PHYS14v3/withCSV/rCS_0b_3.0fbSlidingWcorrectionMuonChannel/singleLeptonic_Phys14V3__estimationResults_pkl_updated'))
res = pickle.load(file('/data/dspitzbart/PHYS14v3/withCSV/rCS_0b_3.0fbSlidingWcorrectionMuonChannel/singleLeptonic_Phys14V3__estimationResults_pkl_updated'))

#pdg = 'pos'
#pdg = 'neg'
#pdg = 'both'

for pdg in ['split','both']:

  #sigbins = signal_bins_3fb()


  signals = [
            {'color': ROOT.kBlue ,'name': 'S1500' ,'label': 'T5q^{4} 1.5/0.8/0.1'}, \
            {'color': ROOT.kRed  ,'name': 'S1200' ,'label': 'T5q^{4} 1.2/1.0/0.8'}, \
            {'color': ROOT.kBlack ,'name': 'S1000' ,'label': 'T5q^{4} 1.0/0.8/0.7'}, \
           ]

  #signal = signals[2]


  signal_signif = []
  for signal in signals:
    print signal

##  if pdg == 'both' :
##    found_bin = [\
##    {'closure': res[(6, 7)][(450, -1)][(500, 1000)]['tot_clos']         ,'Berror':res[(6, 7)][(450, -1)][(500, 1000)]['tot_pred_err'] ,'B': res[(6, 7)][(450, -1)][(500, 1000)]['tot_pred'], 'nJet': (6, 7), 'S1000': res[(6, 7)][(450, -1)][(500, 1000)]['T5q^{4} 1.0/0.8/0.7_yield'], 'HT': (500, 1000), 'ST': (450, -1), 'S1500': res[(6, 7)][(450, -1)][(500, 1000)]['T5q^{4} 1.5/0.8/0.1_yield'], 'deltaPhi': 0.75, 'S1200': res[(6, 7)][(450, -1)][(500, 1000)]['T5q^{4} 1.2/1.0/0.8_yield']},\
##    {'closure': res[(6, 7)][(450, -1)][(1000, -1)]['tot_clos']         ,'Berror':res[(6, 7)][(450, -1)][(1000, -1)]['tot_pred_err'], 'B': res[(6, 7)][(450, -1)][(1000,-1)]['tot_pred'], 'nJet': (6, 7), 'S1000': res[(6, 7)][(450, -1)][(1000,-1)]['T5q^{4} 1.0/0.8/0.7_yield'], 'HT': (1000,-1), 'ST': (450, -1), 'S1500': res[(6, 7)][(450, -1)][(1000,-1)]['T5q^{4} 1.5/0.8/0.1_yield'], 'deltaPhi': 0.75, 'S1200': res[(6, 7)][(450, -1)][(1000,-1)]['T5q^{4} 1.2/1.0/0.8_yield']},\
##    ]
##  if pdg == 'pos' :
##    found_bin = [\
##    {'closure': res[(6, 7)][(450, -1)][(500, 1000)]['tot_clos_PosPdg']  ,'Berror':res[(6, 7)][(450, -1)][(500, 1000)]['tot_PosPdg_pred_err'] ,'B': res[(6, 7)][(450, -1)][(500, 1000)]['tot_PosPdg_pred'], 'nJet': (6, 7), 'S1000': res[(6, 7)][(450, -1)][(500, 1000)]['T5q^{4} 1.0/0.8/0.7_yield_PosPdg'], 'HT': (500, 1000), 'ST': (450, -1), 'S1500': res[(6, 7)][(450, -1)][(500, 1000)]['T5q^{4} 1.5/0.8/0.1_yield_PosPdg'], 'deltaPhi': 0.75, 'S1200': res[(6, 7)][(450, -1)][(500, 1000)]['T5q^{4} 1.2/1.0/0.8_yield_PosPdg']},\
##    {'closure': res[(6, 7)][(450, -1)][(1000, -1)]['tot_clos_PosPdg']  ,'Berror':res[(6, 7)][(450, -1)][(1000, -1)]['tot_PosPdg_pred_err'], 'B': res[(6, 7)][(450, -1)][(1000,-1)]['tot_PosPdg_pred'], 'nJet': (6, 7), 'S1000': res[(6, 7)][(450, -1)][(1000,-1)]['T5q^{4} 1.0/0.8/0.7_yield_PosPdg'], 'HT': (1000,-1), 'ST': (450, -1), 'S1500': res[(6, 7)][(450, -1)][(1000,-1)]['T5q^{4} 1.5/0.8/0.1_yield_PosPdg'], 'deltaPhi': 0.75, 'S1200': res[(6, 7)][(450, -1)][(1000,-1)]['T5q^{4} 1.2/1.0/0.8_yield_PosPdg']},\
##    ]
##  if pdg == 'neg' :
##    found_bin = [\
##    {'closure': res[(6, 7)][(450, -1)][(500, 1000)]['tot_clos_NegPdg']  ,'Berror':res[(6, 7)][(450, -1)][(500, 1000)]['tot_NegPdg_pred_err'] ,'B': res[(6, 7)][(450, -1)][(500, 1000)]['tot_NegPdg_pred'], 'nJet': (6, 7), 'S1000': res[(6, 7)][(450, -1)][(500, 1000)]['T5q^{4} 1.0/0.8/0.7_yield_NegPdg'], 'HT': (500, 1000), 'ST': (450, -1), 'S1500': res[(6, 7)][(450, -1)][(500, 1000)]['T5q^{4} 1.5/0.8/0.1_yield_NegPdg'], 'deltaPhi': 0.75, 'S1200': res[(6, 7)][(450, -1)][(500, 1000)]['T5q^{4} 1.2/1.0/0.8_yield_NegPdg']},\
##    {'closure': res[(6, 7)][(450, -1)][(1000, -1)]['tot_clos_NegPdg']  ,'Berror':res[(6, 7)][(450, -1)][(1000, -1)]['tot_NegPdg_pred_err'], 'B': res[(6, 7)][(450, -1)][(1000,-1)]['tot_NegPdg_pred'], 'nJet': (6, 7), 'S1000': res[(6, 7)][(450, -1)][(1000,-1)]['T5q^{4} 1.0/0.8/0.7_yield_NegPdg'], 'HT': (1000,-1), 'ST': (450, -1), 'S1500': res[(6, 7)][(450, -1)][(1000,-1)]['T5q^{4} 1.5/0.8/0.1_yield_NegPdg'], 'deltaPhi': 0.75, 'S1200': res[(6, 7)][(450, -1)][(1000,-1)]['T5q^{4} 1.2/1.0/0.8_yield_NegPdg']},\
##    ]


    found_bin = []
    
    njets = res.keys()
    for njet in njets:
      for st in res[njet].keys():
        for ht in res[njet][st].keys():
    
          if pdg == 'both' :
            found_bin.append(\
            {'closure': res[njet][st][ht]['tot_clos']  ,'Berror':res[njet][st][ht]['tot_pred_err'] ,'B': res[njet][st][ht]['tot_pred'], 'nJet': (6, 7), 'S1000': res[njet][st][ht]['T5q^{4} 1.0/0.8/0.7_yield'], 'HT': ht, 'ST': st, 'S1500': res[njet][st][ht]['T5q^{4} 1.5/0.8/0.1_yield'], 'deltaPhi': 0.75, 'S1200': res[njet][st][ht]['T5q^{4} 1.2/1.0/0.8_yield']},\
                          )
    
          if pdg == 'split' : 
              found_bin.append(\
                {'closure': res[njet][st][ht]['tot_clos_PosPdg']  ,'Berror':res[njet][st][ht]['tot_PosPdg_pred_err'] ,'B': res[njet][st][ht]['tot_PosPdg_pred'], 'nJet': njet, 'S1000': res[njet][st][ht]['T5q^{4} 1.0/0.8/0.7_yield_PosPdg'], 'HT': ht, 'ST': st, 'S1500': res[njet][st][ht]['T5q^{4} 1.5/0.8/0.1_yield_PosPdg'], 'deltaPhi': 0.75, 'S1200': res[njet][st][ht]['T5q^{4} 1.2/1.0/0.8_yield_PosPdg']},\
                          ) 
              found_bin.append(\
                {'closure': res[njet][st][ht]['tot_clos_NegPdg']  ,'Berror':res[njet][st][ht]['tot_NegPdg_pred_err'] ,'B': res[njet][st][ht]['tot_NegPdg_pred'], 'nJet': njet, 'S1000': res[njet][st][ht]['T5q^{4} 1.0/0.8/0.7_yield_NegPdg'], 'HT': ht, 'ST': st, 'S1500': res[njet][st][ht]['T5q^{4} 1.5/0.8/0.1_yield_NegPdg'], 'deltaPhi': 0.75, 'S1200': res[njet][st][ht]['T5q^{4} 1.2/1.0/0.8_yield_NegPdg']},\
                          )
    
    
    print found_bin

    x_s = n.zeros(11, dtype=float)
    y_s = n.zeros(11, dtype=float)
    y_1min = n.zeros(11, dtype=float)
    y_2min = n.zeros(11, dtype=float)
    y_1max = n.zeros(11, dtype=float)
    y_2max = n.zeros(11, dtype=float)
    for lum in lumi_bins:
      print "lum:" , lum
      print "lumi:" , lum*1000
      c = cardFileWriter()
      c.defWidth=12
      c.precision=6
      #c.addUncertainty('Lumi', 'lnN')
      #c.specifyFlatUncertainty('Lumi', 1.20)
      c.addUncertainty('JES', 'lnN')
      #c.addUncertainty('closure', 'lnN')
      c.addUncertainty('predUnc', 'lnN')
      c.addUncertainty('SigAcc', 'lnN')
      for i , bin in enumerate(found_bin):
        #print i ,bin['HT'],bin['ST'] ,bin['nJet'],bin['B'] , bin['S1500']

        bkg_Y = { 'name': 'bin_'+str(i), 'value': float(bin['B'])/float(lumi_origin), 'label': 'ttJets+WJets'}

        signal.update({'value': float(bin[signal['name']])/float(lumi_origin)})
        #print signal

        c.addBin(bkg_Y['name'], ['bkg'], bkg_Y['name'])


        #print "Bin"+str(i), y
        c.specifyObservation(bkg_Y['name'], int(signal['value']*lum))
        c.specifyExpectation(bkg_Y['name'], 'bkg', bkg_Y['value']*lum)
        c.specifyExpectation(bkg_Y['name'], 'signal', signal['value']*lum)

        c.specifyUncertainty('JES', bkg_Y['name'], 'bkg', 1.2)
        #c.specifyUncertainty('closure', bkg_Y['name'], 'bkg', 1+bin['closure'])
        c.specifyUncertainty('predUnc', bkg_Y['name'], 'bkg', 1+bin['Berror'])
        c.specifyUncertainty('SigAcc', bkg_Y['name'], 'signal', 1.2)
      #####End of Bin loop######


      if option == 'limit' :
     
        limit = c.calcLimit()
        print 'limit:' ,  limit
        limit_med = limit['0.500']
        print "limit median :" , limit_med
        y_2min[int(lum)] = limit['0.025']
        y_1min[int(lum)] = limit['0.160']
        y_s[int(lum)]    = limit_med
        y_1max[int(lum)] = limit['0.840']
        y_2max[int(lum)] = limit['0.975']
        x_s[int(lum)] = int(lum)


    signal_signif.append({'label':signal['label'] ,'name':signal['name'],'color':signal['color'] , 'y_m':y_s[1:] , 'x': x_s[1:] , 'y1_min':y_1min[1:],'y2_min': y_2min[1:] ,'y1_max': y_1max[1:] ,'y2_max':y_2max[1:] })

  print signal_signif

  for signal in signal_signif:
     plotLimit(signal,path,option+pdg+'_fullbin_'+str(lumi_origin),lumi_origin)


