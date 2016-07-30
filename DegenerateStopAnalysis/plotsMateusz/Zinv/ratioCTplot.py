#ratioCTplot.py

import ROOT
import os, sys
import numpy as np
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import setup_style
from Workspace.HEPHYPythonTools import u_float

#Sets TDR style
setup_style()

filename = "/afs/hephy.at/user/m/mzarucki/www/plots/Zinv/SR1/ZinvRatios_peak.txt"

#def my_range(start, end, step):
#    while start <= end:
#        yield start
#        start += step

#CT2 = {'Zpeak_dataMC' = [], 'Zpeak_dataMC_err' = [],
#       'prob_el_dataMC' = [], 'prob_el_dataMC_err' = [],
#       'prob_mu_dataMC' = [], 'prob_mu_dataMC_err' = []}

ratios = {'CT75':{}, 'CT100':{}, 'CT125':{}, 'CT150':{}, 'CT300':{}}

buffer = []

##Gets all file paths with filter results
#for dirname in sorted(os.listdir(path)): 
#   if dirname.startswith("filter"):
#      print dirname
#      buffer = dirname.split("_")
#      filename = 'reductionEfficiency_' + buffer[1] + '_' + buffer[2]  + '.txt'
#      files.append(os.path.join(path,dirname,filename))

#Extraction of data from file

with open(filename, 'r') as infile: #.read() #opens data file
   print "Opening: ", infile.name
   infile.next() 
   infile.next() 
   for line in infile:   
      buffer = line.replace("+-", " ").split()
      #print buffer
      ratios['CT'+ buffer[0]]['Zpeak_dataMC'] = float(buffer[1]) 
      ratios['CT'+ buffer[0]]['Zpeak_dataMC_err'] = float(buffer[2]) 
      ratios['CT'+ buffer[0]]['prob_el_dataMC'] = float(buffer[7]) 
      ratios['CT'+ buffer[0]]['prob_el_dataMC_err'] = float(buffer[8]) 
      ratios['CT'+ buffer[0]]['prob_mu_dataMC'] = float(buffer[13]) 
      ratios['CT'+ buffer[0]]['prob_mu_dataMC_err'] = float(buffer[14]) 
infile.close()

prob_el = {}
prob_mu = {}

#Calculation of ratios
for CT in ratios:
   prob_el[CT] = u_float.u_float(ratios['CT300']['Zpeak_dataMC'], ratios['CT300']['Zpeak_dataMC_err'])*u_float.u_float(ratios[CT]['prob_el_dataMC'], ratios[CT]['prob_el_dataMC_err'])
   prob_mu[CT] = u_float.u_float(ratios['CT300']['Zpeak_dataMC'], ratios['CT300']['Zpeak_dataMC_err'])*u_float.u_float(ratios[CT]['prob_mu_dataMC'], ratios[CT]['prob_mu_dataMC_err'])
   #print prob_el[CT]
   #print prob_mu[CT]

#arrays for plot
CT_arr = []
prob_el_arr = []
prob_el_err_arr = []
prob_mu_arr = []
prob_mu_err_arr = []

for i, CT in enumerate(ratios.keys()):
   CT_arr.append(int(CT.replace("CT",""))) 
   prob_el_arr.append(prob_el[CT].val)
   prob_el_err_arr.append(prob_el[CT].sigma)
   prob_mu_arr.append(prob_mu[CT].val)
   prob_mu_err_arr.append(prob_mu[CT].sigma)

#print "CT: ", CT_arr
#print "El: ", prob_el_arr
#print "El err:", prob_el_err_arr
#print "Mu: ", prob_mu_arr
#print "Mu err:", prob_mu_err_arr

#Canvas 1: MET 1
c1 = ROOT.TCanvas("c1", "ratioCT")
c1.SetGrid() #adds a grid to the canvas
#c1.SetFillColor(42)
c1.GetFrame().SetFillColor(21)
c1.GetFrame().SetBorderSize(12)
 
gr1 = ROOT.TGraphErrors(len(CT_arr), np.array(CT_arr, 'float64'), np.array(prob_el_arr, 'float64'), np.array([0]), np.array(prob_el_err_arr, 'float64')) #graph object with error bars using arrays of data
gr1.SetTitle("Z_{inv} Correction Factors for N_{\nu\nu l}^{ MC}  as a Function C_{T2} Cut")
gr1.SetMarkerColor(ROOT.kBlue)
gr1.SetMarkerStyle(ROOT.kFullCircle)
gr1.SetMarkerSize(1)
gr1.GetXaxis().SetTitle("C_{T2} = min(emulated MET, HT - 100)")
gr1.GetYaxis().SetTitle("R_{\mu\mu}*R_{\mu\mu l/\mu\mu}")
gr1.GetXaxis().CenterTitle()
gr1.GetYaxis().CenterTitle()
gr1.GetXaxis().SetTitleSize(0.04)
gr1.GetYaxis().SetTitleSize(0.04)
gr1.GetXaxis().SetTitleOffset(1.4)
gr1.GetYaxis().SetTitleOffset(1.6)
gr1.SetMinimum(0.5)
gr1.SetMaximum(1.4)

#for x in range(len(cuts)/2):
#   print x
#   print cuts[2*x], cuts[2*x+1]
#   latex = ROOT.TLatex(gr1.GetX()[x] + 0.0005, gr1.GetY()[x] + 0.0005, "(" + cuts[2*x] + "," + cuts[2*x+1] + ")")
#   latex.SetTextSize(0.03)
#   #latex.SetTextColor(ROOT.kRed)
#   gr1.GetListOfFunctions().Add(latex)

gr1.Draw("AP") #plots the graph with axes and points

gr2 = ROOT.TGraphErrors(len(CT_arr), np.array(CT_arr, 'float64'), np.array(prob_mu_arr, 'float64'), np.array([0]), np.array(prob_mu_err_arr, 'float64')) #graph object with error bars using arrays of data
#gr2.SetTitle("Z_{inv} Correction Factors for N_{\nu\nu l}^{ MC}  as a Function C_{T2} Cut")
gr2.SetMarkerColor(ROOT.kRed)
gr2.SetMarkerStyle(ROOT.kFullCircle)
gr2.SetMarkerSize(1)
#gr2.GetXaxis().SetTitle("C_{T2} = min(emulated MET, HT - 100)")
#gr2.GetYaxis().SetTitle("R_{\mu\mu}*R_{\mu\mu l/\mu\mu}")
#gr2.GetXaxis().SetTitleOffset(1.2)
#gr2.GetYaxis().SetTitleOffset(1.3)
#gr2.GetXaxis().CenterTitle()
#gr2.GetYaxis().CenterTitle()
#gr2.SetMinimum(0.5)

gr2.Draw("Psame") #plots the graph with axes and points

l1 = makeLegend2()
l1.AddEntry(gr1, "Electron Channel", "P")
l1.AddEntry(gr2, "Muon Channel", "P")
l1.Draw() 
#Save to Web
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/Zinv"

if not os.path.exists(savedir):
      os.makedirs(savedir)

c1.SaveAs(savedir + "ratioCTplot.png")
c1.SaveAs(savedir + "ratioCTplot.pdf")
c1.SaveAs(savedir + "ratioCTplot.root")
