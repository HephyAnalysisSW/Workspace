from cardFileWriter import cardFileWriter
from limit_helper import plotsignif , plotLimit , signal_bins_3fb , signal_bins_3fb_table
from math import exp
import os,sys
import ROOT
import pickle
import array
import numpy as n
from Workspace.RA4Analysis.signalRegions import *


ROOT.gROOT.LoadMacro("/afs/hephy.at/work/e/easilar/Working_directory/CMSSW_7_1_5/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()

path = "/afs/hephy.at/user/e/easilar/www/PHYS14v3/limit_results/singleLeptonic/combined_bin_tests/"

if not os.path.exists(path):
  os.makedirs(path)


#bin_yields2 = pickle.load(file('/data/dspitzbart/lumi3.0yields_pkl_newOpt'))
bin_yields2 = pickle.load(file('/data/dspitzbart/lumi3.0yields_pkl_final'))


text_path = "text_files"
if not os.path.exists(text_path):
  os.makedirs(text_path)

options = ['signif' , 'limit']
#option = options[1]

#lumi_bins = [1,2,3,4,5,6,7,8,9,10]
#lumi_bins = [1,2,3,4]
lumi_bins = [3]
lumi_origin = 3

signals = [
          {'color': ROOT.kBlue ,'name': 'S1500' ,'label': 'T5q^{4} 1.5/0.8/0.1'}, \
          {'color': ROOT.kRed  ,'name': 'S1200' ,'label': 'T5q^{4} 1.2/1.0/0.8'}, \
          {'color': ROOT.kBlack ,'name': 'S1000' ,'label': 'T5q^{4} 1.0/0.8/0.7'}, \
         ]


signal_bins = signal_bins_3fb_table()

for option in options:
  print "OPTION:" , option
  for njetbin in signal_bins:
    for stbin in njetbin['STbin']:
      search_bins = []
      for htbin in stbin['HTbin']:
        search_bins.append({'HT': htbin , 'ST': stbin['ST'] , 'nJet': njetbin['nJets'], 'dphi': stbin['dPhi']}) 

      print 'searching :' , search_bins


      found_bin = [bin_yield for bin_yield in bin_yields2 for search_bin in search_bins if (bin_yield['HT'] == search_bin['HT'] and bin_yield['ST'] == search_bin['ST'] and bin_yield['nJet'] == search_bin['nJet'])]
      print "FOUND BIN"
      print found_bin
      #signal = signals[2]
      for signal in signals:
        for lum in lumi_bins:
          print "lum:" , lum
          print "lumi:" , lum*1000
          c = cardFileWriter()
          c.defWidth=12
          c.precision=6
          c.addUncertainty('Lumi', 'lnN')
          c.specifyFlatUncertainty('Lumi', 1.20)
          c.addUncertainty('JES', 'lnN')
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

            c.specifyUncertainty('JES', bkg_Y['name'], 'bkg', 1.3)
          #####End of Bin loop######

          c.writeToFile('text_files/combination'+str(len(search_bins))+'_'+str(lum)+'.txt')

          if option == 'limit' :
            limit = c.calcLimit()
            print 'limit:' ,  limit
            limit_med = limit['0.500']
            print "limit median :" , limit_med
            y_2min = limit['0.025']
            y_1min = limit['0.160']
            y_s   = limit_med
            y_1max = limit['0.840']
            y_2max = limit['0.975']
            x_s = int(lum)

          if option == 'signif' :
            limit = c.calcSignif()
            limit_sig = limit['-1.000']
            #print "significance :" , limit_sig
            #if lum == lumi_origin : sigma = limit_sig
            y_s = limit_sig
            x_s = int(lum)
            y_2min=0
            y_1min=0
            y_2max=0
            y_1max=0

        stbin[signal['name']+option] = {'label':signal['label'] , 'color':signal['color'] , 'y_m':y_s, 'x': x_s , 'y1_min':y_1min,'y2_min': y_2min ,'y1_max': y_1max ,'y2_max':y_2max }

print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
print "Final :"  , signal_bins

pickle.dump(signal_bins, file(path+option+str(lumi_origin)+'_pkl','w'))

print "wrtten:" , path+option+str(lumi_origin)+'_pkl'
