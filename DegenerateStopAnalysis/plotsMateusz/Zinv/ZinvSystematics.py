# ZinvSystematics.py
# Script combining both Z->mumu and Z->ee channels and calculating the systematics 
# Mateusz Zarucki 2016

import os, sys
import ROOT
import argparse
import pickle
import math
import numpy as np
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import makeSimpleLatexTable, setup_style, makeDir
from Workspace.HEPHYPythonTools import u_float
   
#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--plot", dest = "plot",  help = "Toggle plot", type = int, default = 0)
parser.add_argument("--SR", dest = "SR",  help = "Signal region", type = str, default = "SR1")
parser.add_argument("--lepEta", dest = "lepEta",  help = "Extra soft lepton eta", type = str, default = "2.5")
parser.add_argument("--saveFactors", dest = "saveFactors",  help = "Save factors", type = int, default = 0)
#parser.add_argument("--applyCorrection", dest = "applyCorrection",  help = "Apply Zinv correction", type = int, default = 0)
#parser.add_argument("--channel", dest = "channel",  help = "Channel to be used for correction", type = str, default = "combined") #Zmumu, Zee, combined
parser.add_argument("--makeTables", dest = "makeTables",  help = "Results table", type = int, default = 0)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
plot = args.plot
SR = args.SR
lepEta = args.lepEta
saveFactors = args.saveFactors
#applyCorrection = args.applyCorrection
#channel = args.channel
makeTables = args.makeTables

tag = "8012_mAODv2_v3/80X_postProcessing_v10"

path1 = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/Zinv/Zmumu/lepEta%s/%s"%(tag,lepEta,SR)
path2 = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/Zinv/Zee/lepEta%s/%s"%(tag,lepEta,SR)
path3 = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/Zinv/combined/lepEta%s/%s"%(tag,lepEta,SR)
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/Zinv/systematics/lepEta%s/%s"%(tag,lepEta,SR)
tabledir = savedir + "/tables" 
plotdir = savedir + "/plots"

makeDir(savedir)
makeDir(tabledir)
makeDir(plotdir)
makeDir(path3)

CTs = ['75', '100', '125', '150', '175', '200', '250', '300']
#CTs = ['75', '150', '300']

ZinvRatios = {'Zmumu':{}, 'Zee':{}, 'combined': {}} 
ZinvYields = {'Zmumu':{}, 'Zee':{}, 'combined': {}}
 
for CT2 in CTs:
   ZinvRatios['Zmumu']['CT' + CT2] = pickle.load(open("%s/pickle/peak/ZinvRatios_Zmumu_%s_CT%s_peak.pkl"%(path1,SR,CT2), "r"))
   ZinvRatios['Zee']['CT' + CT2] =   pickle.load(open("%s/pickle/peak/ZinvRatios_Zee_%s_CT%s_peak.pkl"%(path2,SR,CT2), "r"))

   ZinvYields['Zmumu']['CT' + CT2] = pickle.load(open("%s/pickle/peak/ZinvYields_Zmumu_%s_CT%s_peak.pkl"%(path1,SR,CT2), "r"))
   ZinvYields['Zee']['CT' + CT2]   = pickle.load(open("%s/pickle/peak/ZinvYields_Zee_%s_CT%s_peak.pkl"%(path2,SR,CT2), "r"))

for CT2 in CTs:
   ZinvRatios['combined']['CT' + CT2] = {}   
   ZinvYields['combined']['CT' + CT2] = {'Zpeak':{}, 'Nel':{}, 'Nmu':{}}   
   ZinvYields['combined']['CT' + CT2]['Zpeak']['data'] = ZinvYields['Zmumu']['CT' + CT2]['Zpeak']['data'] + ZinvYields['Zee']['CT' + CT2]['Zpeak']['data']
   ZinvYields['combined']['CT' + CT2]['Zpeak']['dy'] =   ZinvYields['Zmumu']['CT' + CT2]['Zpeak']['dy']   + ZinvYields['Zee']['CT' + CT2]['Zpeak']['dy']
   ZinvYields['combined']['CT' + CT2]['Zpeak']['tt'] =   ZinvYields['Zmumu']['CT' + CT2]['Zpeak']['tt']   + ZinvYields['Zee']['CT' + CT2]['Zpeak']['tt']
   ZinvYields['combined']['CT' + CT2]['Zpeak']['vv'] =   ZinvYields['Zmumu']['CT' + CT2]['Zpeak']['vv']   + ZinvYields['Zee']['CT' + CT2]['Zpeak']['vv']
   ZinvYields['combined']['CT' + CT2]['Nel']['data'] =   ZinvYields['Zmumu']['CT' + CT2]['Nel']['data']   + ZinvYields['Zee']['CT' + CT2]['Nel']['data']
   ZinvYields['combined']['CT' + CT2]['Nel']['dy'] =     ZinvYields['Zmumu']['CT' + CT2]['Nel']['dy']     + ZinvYields['Zee']['CT' + CT2]['Nel']['dy']
   ZinvYields['combined']['CT' + CT2]['Nel']['tt'] =     ZinvYields['Zmumu']['CT' + CT2]['Nel']['tt']     + ZinvYields['Zee']['CT' + CT2]['Nel']['tt']
   ZinvYields['combined']['CT' + CT2]['Nel']['vv'] =     ZinvYields['Zmumu']['CT' + CT2]['Nel']['vv']     + ZinvYields['Zee']['CT' + CT2]['Nel']['vv']
   ZinvYields['combined']['CT' + CT2]['Nmu']['data'] =   ZinvYields['Zmumu']['CT' + CT2]['Nmu']['data']   + ZinvYields['Zee']['CT' + CT2]['Nmu']['data']
   ZinvYields['combined']['CT' + CT2]['Nmu']['dy'] =     ZinvYields['Zmumu']['CT' + CT2]['Nmu']['dy']     + ZinvYields['Zee']['CT' + CT2]['Nmu']['dy']
   ZinvYields['combined']['CT' + CT2]['Nmu']['tt'] =     ZinvYields['Zmumu']['CT' + CT2]['Nmu']['tt']     + ZinvYields['Zee']['CT' + CT2]['Nmu']['tt']
   ZinvYields['combined']['CT' + CT2]['Nmu']['vv'] =     ZinvYields['Zmumu']['CT' + CT2]['Nmu']['vv']     + ZinvYields['Zee']['CT' + CT2]['Nmu']['vv']

   if not os.path.isfile("%s/ZinvYields_combined.txt"%(path3)):
      outfile = open("%s/ZinvYields_combined.txt"%(path3), "w")
      outfile.write("Combined Zinv Estimation Yields\n")
      outfile.write("CT       Zpeak_data          Zpeak_DY           Zpeak_TT           Zpeak_VV           Nel_data           Nel_DY           Nel_TT           Nel_VV           Nmu_data           Nmu_DY            Nmu_TT          Nmu_VV\n")

   with open("%s/ZinvYields_combined.txt"%(path3), "a") as outfile:
      outfile.write(CT2.ljust(7) +\
      str(ZinvYields['combined']['CT' + CT2]['Zpeak']['data'].round(2)).ljust(18) +\
      str(ZinvYields['combined']['CT' + CT2]['Zpeak']['dy'].round(2)).ljust(18) +\
      str(ZinvYields['combined']['CT' + CT2]['Zpeak']['tt'].round(2)).ljust(18) +\
      str(ZinvYields['combined']['CT' + CT2]['Zpeak']['vv'].round(2)).ljust(18) +\
      str(ZinvYields['combined']['CT' + CT2]['Nel']['data'].round(2)).ljust(18) +\
      str(ZinvYields['combined']['CT' + CT2]['Nel']['dy'].round(2)).ljust(18) +\
      str(ZinvYields['combined']['CT' + CT2]['Nel']['tt'].round(2)).ljust(18) +\
      str(ZinvYields['combined']['CT' + CT2]['Nel']['vv'].round(2)).ljust(18) +\
      str(ZinvYields['combined']['CT' + CT2]['Nmu']['data'].round(2)).ljust(18) +\
      str(ZinvYields['combined']['CT' + CT2]['Nmu']['dy'].round(2)).ljust(18) +\
      str(ZinvYields['combined']['CT' + CT2]['Nmu']['tt'].round(2)).ljust(18) +\
      str(ZinvYields['combined']['CT' + CT2]['Nmu']['vv'].round(2)) + "\n")

   #Z xsec
   ZinvRatios['combined']['CT' + CT2]['Zpeak_dataMC'] = ((ZinvYields['combined']['CT' + CT2]['Zpeak']['data'] - (ZinvYields['combined']['CT' + CT2]['Zpeak']['tt'] + ZinvYields['combined']['CT' + CT2]['Zpeak']['vv']))/
                                                        (ZinvYields['combined']['CT' + CT2]['Zpeak']['dy']))

   #probability of extra leptons
   if ZinvYields['combined']['CT' + CT2]['Zpeak']['data'].val:
      ZinvRatios['combined']['CT' + CT2]['prob_el_data'] = ((ZinvYields['combined']['CT' + CT2]['Nel']['data'] - (ZinvYields['combined']['CT' + CT2]['Nel']['tt'] +   ZinvYields['combined']['CT' + CT2]['Nel']['vv']))/
                                                           (ZinvYields['combined']['CT' + CT2]['Zpeak']['data'] - (ZinvYields['combined']['CT' + CT2]['Zpeak']['tt'] + ZinvYields['combined']['CT' + CT2]['Zpeak']['vv'])))
      
      ZinvRatios['combined']['CT' + CT2]['prob_mu_data'] = ((ZinvYields['combined']['CT' + CT2]['Nmu']['data'] - (ZinvYields['combined']['CT' + CT2]['Nmu']['tt'] +   ZinvYields['combined']['CT' + CT2]['Nmu']['vv']))/
                                                           (ZinvYields['combined']['CT' + CT2]['Zpeak']['data'] - (ZinvYields['combined']['CT' + CT2]['Zpeak']['tt'] + ZinvYields['combined']['CT' + CT2]['Zpeak']['vv'])))

   #probability of observing electron
   if ZinvYields['combined']['CT' + CT2]['Zpeak']['dy'].val:
      ZinvRatios['combined']['CT' + CT2]['prob_el_MC'] = (ZinvYields['combined']['CT' + CT2]['Nel']['dy']/ZinvYields['combined']['CT' + CT2]['Zpeak']['dy'])
   
   if ZinvRatios['combined']['CT' + CT2]['prob_el_MC'].val:
      ZinvRatios['combined']['CT' + CT2]['prob_el_dataMC'] = ZinvRatios['combined']['CT' + CT2]['prob_el_data']/ZinvRatios['combined']['CT' + CT2]['prob_el_MC']
   else:
      ZinvRatios['combined']['CT' + CT2]['prob_el_dataMC'] = u_float.u_float(0,0)

   #probability of observing muon
   if ZinvYields['combined']['CT' + CT2]['Zpeak']['dy'].val:
      ZinvRatios['combined']['CT' + CT2]['prob_mu_MC'] = (ZinvYields['combined']['CT' + CT2]['Nmu']['dy']/ZinvYields['combined']['CT' + CT2]['Zpeak']['dy'])

   if ZinvRatios['combined']['CT' + CT2]['prob_mu_MC'].val:
      ZinvRatios['combined']['CT' + CT2]['prob_mu_dataMC'] = ZinvRatios['combined']['CT' + CT2]['prob_mu_data']/ZinvRatios['combined']['CT' + CT2]['prob_mu_MC']
   else:
      ZinvRatios['combined']['CT' + CT2]['prob_mu_dataMC'] = u_float.u_float(0,0)

   #double ratios
   ZinvRatios['combined']['CT' + CT2]['ratio_el'] = (ZinvRatios['combined']['CT' + CT2]['Zpeak_dataMC']*ZinvRatios['combined']['CT' + CT2]['prob_el_dataMC'])
   ZinvRatios['combined']['CT' + CT2]['ratio_mu'] = (ZinvRatios['combined']['CT' + CT2]['Zpeak_dataMC']*ZinvRatios['combined']['CT' + CT2]['prob_mu_dataMC'])

   #Pickle results 
   pickleFile1 = open("%s/ZinvYields_combined_%s.pkl"%(path3, SR), "w")
   pickle.dump(ZinvYields, pickleFile1)
   pickleFile1.close()

   pickleFile2 = open("%s/ZinvRatios_combined_%s.pkl"%(path3, SR), "w")
   pickle.dump(ZinvRatios, pickleFile2)
   pickleFile2.close()

   if not os.path.isfile("%s/ZinvRatios_combined_%s.txt"%(path3, SR)):
      outfile = open("%s/ZinvRatios_combined_%s.txt"%(path3, SR), "w")
      outfile.write("Combined Zinv Estimation Ratios\n")
      outfile.write("CT        Zpeak_data_MC           prob_el_data            prob_el_MC           prob_el_data_MC           prob_mu_data          prob_mu_MC          prob_mu_data_MC           Ratio_el          Ratio_mu\n")

   with open("%s/ZinvRatios.txt"%(path3), "a") as outfile:
      outfile.write(CT2.ljust(10) +\
      str(ZinvRatios['combined']['CT' + CT2]['Zpeak_dataMC'].round(3)).ljust(23) +\
      str(ZinvRatios['combined']['CT' + CT2]['prob_el_data'].round(4)).ljust(23) +\
      str(ZinvRatios['combined']['CT' + CT2]['prob_el_MC'].round(4)).ljust(24) +\
      str(ZinvRatios['combined']['CT' + CT2]['prob_el_dataMC'].round(3)).ljust(25) +\
      str(ZinvRatios['combined']['CT' + CT2]['prob_mu_data'].round(4)).ljust(22) +\
      str(ZinvRatios['combined']['CT' + CT2]['prob_mu_MC'].round(4)).ljust(22) +\
      str(ZinvRatios['combined']['CT' + CT2]['prob_mu_dataMC'].round(3)).ljust(22) +\
      str(ZinvRatios['combined']['CT' + CT2]['ratio_el'].round(3)).ljust(21) +\
      str(ZinvRatios['combined']['CT' + CT2]['ratio_mu'].round(3)).ljust(21)+ "\n")

corr = {'Zmumu':{}, 'Zee':{}, 'combined':{}}

#Calculation of ratios
for Zchannel in corr:
   print makeLine()
   print "Using ", Zchannel, " channel."

   for CT2 in CTs:
      corr[Zchannel]['CT' + CT2] = {}
      corr[Zchannel]['CT' + CT2]['electrons'] = ZinvRatios[Zchannel]['CT300']['Zpeak_dataMC']*ZinvRatios[Zchannel]['CT' + CT2]['prob_el_dataMC']
      corr[Zchannel]['CT' + CT2]['muons'] =     ZinvRatios[Zchannel]['CT300']['Zpeak_dataMC']*ZinvRatios[Zchannel]['CT' + CT2]['prob_mu_dataMC']
      print "CT", CT2, " Correction el: ",       corr[Zchannel]['CT' + CT2]['electrons']
      print "CT", CT2, " Correction mu: ",       corr[Zchannel]['CT' + CT2]['muons']
      
pickleFile3 = open("%s/ZinvCorrections_%s.pkl"%(savedir, SR), "w")
pickle.dump(corr, pickleFile3)
pickleFile3.close()

if saveFactors:

   publicdir = "/afs/hephy.at/user/m/mzarucki/public/Zinv"
   makeDir(publicdir)
 
   regions = ['SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']
   
   ZinvSF_electrons_stat = {}
   ZinvSF_muons_stat = {}
   ZinvSF_electrons_sys = {}
   ZinvSF_muons_sys = {}
   
   for reg in regions:
      ZinvSF_electrons_stat[reg]  = corr['combined']['CT75']['electrons']
      ZinvSF_muons_stat[reg]  =     corr['combined']['CT75']['muons']
      
      ZinvSF_electrons_sys[reg]  = u_float.u_float(corr['combined']['CT75']['electrons'].val, 0.5*corr['combined']['CT75']['electrons'].val)
      ZinvSF_muons_sys[reg]  =     u_float.u_float(corr['combined']['CT75']['muons'].val, 0.5*corr['combined']['CT75']['muons'].val)
   
   pickleFile5 = open("%s/ZinvSFs_electrons_stat.pkl"%(publicdir), "w")
   pickle.dump(ZinvSF_electrons_stat, pickleFile5)
   pickleFile5.close()
   
   pickleFile6 = open("%s/ZinvSFs_electrons_sys.pkl"%(publicdir), "w")
   pickle.dump(ZinvSF_electrons_sys, pickleFile6)
   pickleFile6.close()
   
   pickleFile7 = open("%s/ZinvSFs_muons_stat.pkl"%(publicdir), "w")
   pickle.dump(ZinvSF_muons_stat, pickleFile7)
   pickleFile7.close()
   
   pickleFile8 = open("%s/ZinvSFs_muons_sys.pkl"%(publicdir), "w")
   pickle.dump(ZinvSF_muons_sys, pickleFile8)
   pickleFile8.close()

if makeTables:

   #Ratios
   for channel in corr:
      ZinvRows = []
      listTitle = ['CT', 'Zpeak_data', 'Zpeak_dy', 'Zpeak_tt', 'Zpeak_vv', 'Nel_data', 'Nel_dy', 'Nel_tt', 'Nel_vv', 'Nmu_data', 'Nmu_dy', 'Nmu_tt', 'Nmu_vv']
      ZinvRows.append(listTitle)
      for CT2 in CTs:
         ZinvRow = [CT2, 
         ZinvYields[channel]['CT' + CT2]['Zpeak']['data'].round(4), 
         ZinvYields[channel]['CT' + CT2]['Zpeak']['dy'].round(4), 
         ZinvYields[channel]['CT' + CT2]['Zpeak']['tt'].round(4), 
         ZinvYields[channel]['CT' + CT2]['Zpeak']['vv'].round(4), 
         ZinvYields[channel]['CT' + CT2]['Nel']['data'].round(4), 
         ZinvYields[channel]['CT' + CT2]['Nel']['dy'].round(4), 
         ZinvYields[channel]['CT' + CT2]['Nel']['tt'].round(4), 
         ZinvYields[channel]['CT' + CT2]['Nel']['vv'].round(4), 
         ZinvYields[channel]['CT' + CT2]['Nmu']['data'].round(4), 
         ZinvYields[channel]['CT' + CT2]['Nmu']['dy'].round(4), 
         ZinvYields[channel]['CT' + CT2]['Nmu']['tt'].round(4), 
         ZinvYields[channel]['CT' + CT2]['Nmu']['vv'].round(4)] 
         ZinvRows.append(ZinvRow)
      
      makeSimpleLatexTable(ZinvRows, "ZinvYields_" + channel, tabledir)

      ZinvRows = []
      listTitle = ['CT', 'Zpeak_dataMC', 'prob_el_data', 'prob_el_MC', 'prob_el_dataMC', 'prob_mu_data', 'prob_mu_MC', 'prob_mu_dataMC']
      #listTitle.extend(ZinvRatios[channel]['CT' + CT2].keys())
      ZinvRows.append(listTitle)
      for CT2 in CTs:
         ZinvRow = [CT2, ZinvRatios[channel]['CT' + CT2]['Zpeak_dataMC'].round(4), 
                         ZinvRatios[channel]['CT' + CT2]['prob_el_data'].round(4), ZinvRatios[channel]['CT' + CT2]['prob_el_MC'].round(4), ZinvRatios[channel]['CT' + CT2]['prob_el_dataMC'].round(4),   
                         ZinvRatios[channel]['CT' + CT2]['prob_mu_data'].round(4), ZinvRatios[channel]['CT' + CT2]['prob_mu_MC'].round(4), ZinvRatios[channel]['CT' + CT2]['prob_mu_dataMC'].round(4)]
         #ZinvRow.extend([x.round(4) for x in ZinvRatios[channel]['CT' + CT2].values()])
         ZinvRows.append(ZinvRow)
      
      makeSimpleLatexTable(ZinvRows, "ZinvRatios_" + channel, tabledir)
      
      ZinvRows = []
      listTitle = ['CT', 'Correction electrons', 'Correction muons']
      ZinvRows.append(listTitle)
      for CT2 in CTs:
         ZinvRow = [CT2, corr[channel]['CT' + CT2]['electrons'].round(3), corr[channel]['CT' + CT2]['muons'].round(3)]
         #ZinvRow.extend([x.round(4) for x in ZinvRatios[channel]['CT' + CT2].values()])
         ZinvRows.append(ZinvRow)
      
      makeSimpleLatexTable(ZinvRows, "ZinvCorrections_" + channel, tabledir)
   
#if applyCorrection:
#
##   if not combineChannels and channel == "combined":
##      print "Error: combineChannels set to False. Cannot use combined results"
##      sys.exit(0)
#
#   path = "/afs/hephy.at/user/m/mzarucki/public/Yields_12864pbm1_PreApp_Mt95_Inccharge_LepAll_lep_pu_SF_presel_BinsSummary.pkl"
#  
#   allYields = pickle.load(open(path, "r"))
#   
#   regions = ['SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']
#
#   R_el =       {'Zmumu':{}, 'Zee':{}, 'combined':{}}
#   R_mu =       {'Zmumu':{}, 'Zee':{}, 'combined':{}}
#   Zcorrected = {'Zmumu':{}, 'Zee':{}, 'combined':{}}
#
#   for Zchannel in Zcorrected.keys():
#      print "Applying correction determined from ", Zchannel
#      R_el[Zchannel] = u_float.u_float(corr[Zchannel]['CT75']['electrons'].val, math.sqrt(corr[Zchannel]['CT75']['electrons'].sigma**2 + (0.5*corr[Zchannel]['CT75']['electrons'].val)**2)) #50% sys. on final estimate
#      R_mu[Zchannel] = u_float.u_float(corr[Zchannel]['CT75']['muons'].val,     math.sqrt(corr[Zchannel]['CT75']['electrons'].sigma**2 + (0.5*corr[Zchannel]['CT75']['muons'].val)**2)) #50% sys. on final estimate
#   
#      for reg in regions:
#         print "Region: ", reg
#         print "Combined correction: ", ((R_mu[Zchannel] + R_el[Zchannel])/2) 
#         Zcorrected[Zchannel][reg] = allYields.yieldDictFull['z'][reg] * ((R_mu[Zchannel] + R_el[Zchannel])/2)
#         print "Before correction: ", allYields.yieldDictFull['z'][reg]
#         print "After correction: ", Zcorrected[Zchannel][reg]
# 
#         pickleFile4 = open("%s/correctedZinvYields_%s.pkl"%(savedir, Zchannel), "w")
#         pickle.dump(Zcorrected, pickleFile4)
#         pickleFile4.close()

if plot:
   for Zchannel in corr.keys():
      #Sets TDR style
      setup_style()
      
      #arrays for plot
      CT_arr = [int(x) for x in CTs]
      corr_el_arr = []
      corr_el_err_arr = []
      corr_mu_arr = []
      corr_mu_err_arr = []
      
      for i, CT in enumerate(CTs):
         corr_el_arr.append(corr[Zchannel]['CT' + CT]['electrons'].val)
         corr_el_err_arr.append(corr[Zchannel]['CT' + CT]['electrons'].sigma)
         corr_mu_arr.append(corr[Zchannel]['CT' + CT]['muons'].val)
         corr_mu_err_arr.append(corr[Zchannel]['CT' + CT]['muons'].sigma)
      
      c1 = ROOT.TCanvas("c1", "ratioCT")
      c1.SetGrid() #adds a grid to the canvas
      #c1.SetFillColor(42)
      c1.GetFrame().SetFillColor(21)
      c1.GetFrame().SetBorderSize(12)
      
      gr1 = ROOT.TGraphErrors(len(CT_arr), np.array(CT_arr, 'float64'), np.array(corr_el_arr, 'float64'), np.array([0]), np.array(corr_el_err_arr, 'float64')) #graph object with error bars using arrays of data
      gr1.SetTitle("Z_{inv} Correction Factors for N_{\nu\nu l}^{ MC}  as a Function C_{T2} Cut")
      gr1.SetMarkerColor(ROOT.kBlue)
      gr1.SetMarkerStyle(ROOT.kFullCircle)
      gr1.SetMarkerSize(1)
      gr1.GetXaxis().SetTitle("Lower Cut on C_{T1} = min(emulated #slash{E}_{T}, H_{T} - 100 GeV)")
      if Zchannel == "Zmumu": gr1.GetYaxis().SetTitle("\\mathrm{R}_{\mu\mu \\mathscr{l}} = R_{\mu\mu}*R_{\mu\mu \\mathscr{l}/\mu\mu}")
      elif Zchannel == "Zee": gr1.GetYaxis().SetTitle("\\mathrm{R_{ee \\mathscr{l}} = R_{ee}*R_{ee \\mathscr{l}/ee}}")
      else: gr1.GetYaxis().SetTitle("\\mathscr{\\mathrm{R}_{ll l} = \\mathrm{R}_{ll}*\\mathrm{R}_{ll l/ll}}")
      gr1.GetXaxis().CenterTitle()
      gr1.GetYaxis().CenterTitle()
      gr1.GetXaxis().SetTitleSize(0.04)
      gr1.GetYaxis().SetTitleSize(0.04)
      gr1.GetYaxis().SetNdivisions(512);
      gr1.GetXaxis().SetTitleOffset(1.4)
      gr1.GetYaxis().SetTitleOffset(1.6)
      gr1.SetMinimum(0.2)
      gr1.SetMaximum(2.7)
      gr1.Draw("AP") #plots the graph with axes and points
      
      gr2 = ROOT.TGraphErrors(len(CT_arr), np.array(CT_arr, 'float64'), np.array(corr_mu_arr, 'float64'), np.array([0]), np.array(corr_mu_err_arr, 'float64')) #graph object with error bars using arrays of data
      gr2.SetMarkerColor(ROOT.kRed)
      gr2.SetMarkerStyle(ROOT.kFullCircle)
      gr2.SetMarkerSize(1)
      gr2.Draw("Psame")
      
      leg = ROOT.TLegend(0.20, 0.8, 0.55, 0.925) #x1,y1,x2,y2
      #leg = ROOT.TLegend(0.600, 0.8, 0.95, 0.925) #x1,y1,x2,y2
      leg.AddEntry(gr1, "Electron Channel", "P")
      leg.AddEntry(gr2, "Muon Channel", "P")
      leg.SetTextSize(0.03)
      leg.Draw()

      #Save to Web
      c1.SaveAs("%s/ratioCTplot_%s.png"%(plotdir, Zchannel))
      c1.SaveAs("%s/ratioCTplot_%s.pdf"%(plotdir, Zchannel))
      c1.SaveAs("%s/ratioCTplot_%s.root"%(plotdir, Zchannel))
