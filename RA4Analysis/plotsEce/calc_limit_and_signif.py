from cardFileWriter import cardFileWriter
from math import exp
import os,sys
import ROOT
import pickle
import array
import numpy as n
ROOT.gROOT.LoadMacro("/afs/hephy.at/scratch/e/easilar/CMSSW_7_2_3/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()

path = "/afs/hephy.at/user/e/easilar/www/PHYS14v3/limit_results/singleLeptonic/combined_bin/"
#path = "/afs/hephy.at/user/e/easilar/www/PHYS14v3/limit_results/singleMuonic/combined_bin_JJ/"
if not os.path.exists(path):
  os.makedirs(path)

text_path = "text_files"
if not os.path.exists(text_path):
  os.makedirs(text_path)

#h_limit = ROOT.TH2F("h_limit","h_limit",100,0,10,100,0,10)



options = ['signif' , 'limit']
option = options[0]

lumi_bins = [1,2,3,4,5,6,7,8,9,10]
lumi_origin = 4

#bin_yields1 , bin_yields2 = pickle.load(file('/data/easilar/PHYS14v3/SRfinder/singleLeptonic_SRfinder_pkl'))
#bin_yields1 , bin_yields2 = pickle.load(file('/data/dhandl/results2015/SRfinder/singleMuonic_SRfinder_Phys14V3_adddPhiJJcut_pkl'))
#bin_yields1 , bin_yields2 = pickle.load(file('/data/dhandl/results2015/SRfinder/singleMuonic_SRfinder_Phys14V3_pkl'))
bin_yields1 , bin_yields2 , bin_yields3 = pickle.load(file('/data/easilar/results2015/SRfinder/singleLeptonic_SRfinder_Phys14V3_pkl'))

search_bins = [\
             {'HT': (1250 , -1)   , 'ST': (450,-1) , 'nJet': (8,-1)},\
             {'HT': (1250 , -1)   , 'ST': (450,-1) , 'nJet': (6,7)},\
             {'HT': (1250 , -1)   , 'ST': (450,-1) , 'nJet': (5,5)},\
             ###{'HT': (1250 , -1)   , 'ST': (350,450) , 'nJet': (8,-1)},\
             {'HT': (1250 , -1) , 'ST': (450,-1) , 'nJet': (5,5)},\
             #{'HT': (1000 , 1250) , 'ST': (450,-1) , 'nJet': (5,5)},\
             {'HT': (1000 , 1250) , 'ST': (450,-1) , 'nJet': (6,7)},\
             ##{'HT': (1000 , 1250) , 'ST': (450,-1) , 'nJet': (8,-1)},\
            #{'HT': (750 , 1000) , 'ST': (450,-1) , 'nJet': (8,-1)},\
            #{'HT': (750 , 1000) , 'ST': (250,350) , 'nJet': (8,-1)},\
            #{'HT': (750 , 1000) , 'ST': (450,-1) , 'nJet': (6,7)},\
            #{'HT': (500 , 750) , 'ST': (450,-1) , 'nJet': (6,7)},\
            #{'HT': (500 , 750) , 'ST': (350,450) , 'nJet': (6,7)},\
             ##{'HT': (750 , 1000) , 'ST': (350,450) , 'nJet': (8,-1)},\
            ]

found_bin = [bin_yield for bin_yield in bin_yields2 for search_bin in search_bins if (bin_yield['HT'] == search_bin['HT'] and bin_yield['ST'] == search_bin['ST'] and bin_yield['nJet'] == search_bin['nJet'])]
print "FOUND BIN"
print found_bin

signals = [
          {'name': 'S1500' ,'label': 'T5q^{4} 1.5_0.8_0.1'}, \
          {'name': 'S1200' ,'label': 'T5q^{4} 1.2_1.0_0.8'}, \
          {'name': 'S1000' ,'label': 'T5q^{4} 1.0_0.8_0.7'}, \
         ]
signal = signals[0]
print signal
tot_b_Y = sum(bin['B'] for bin in found_bin)
tot_s_Y = sum(bin[signal['name']] for bin in found_bin)

sigma = 0  
x_s = n.zeros(11, dtype=float)
y_s = n.zeros(11, dtype=float)
for lum in lumi_bins:
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
    limit_med = limit['0.500']
    print "limit median :" , limit_med
    y_s[int(lum)] = limit_med
    x_s[int(lum)] = int(lum)

  if option == 'signif' :
    limit = c.calcSignif()
    limit_sig = limit['-1.000']
    print "significance :" , limit_sig
    if lum == 4 : sigma = limit_sig
    y_s[int(lum)] = limit_sig
    x_s[int(lum)] = int(lum)


can = ROOT.TCanvas("can","can",600,600)
can.cd()
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.035)
latex.SetTextAlign(11)
leg = ROOT.TLegend(0.55,0.2,0.95,0.3)
leg.SetFillColor(0)

g_limit = ROOT.TGraph(len(x_s),x_s,y_s)
g_limit.SetTitle("")
g_limit.SetLineColor(2)
g_limit.SetLineWidth(2)
g_limit.SetMarkerSize(1.5)
g_limit.GetXaxis().SetTitle("Lumi fb^{-1}")
g_limit.GetYaxis().SetTitle("#sigma")
g_limit.GetYaxis().SetRangeUser(0,6)
g_limit.Draw("AC*")
leg.AddEntry(g_limit,signal['label'] ,"l")
#leg.AddEntry(g_limit, "T5q^{4} 1.5_0.8_0.1" ,"l")
leg.Draw()
latex.DrawLatex(0.16,0.96,"CMS Simulation")
latex.DrawLatex(0.71,0.96,"L=4 fb^{-1} (13 TeV)")
latex.DrawLatex(0.55,0.31,"bkg yield:"+str(round(tot_b_Y,2)))
latex.DrawLatex(0.55,0.35,"signal yield:"+str(round(tot_s_Y,2)))
latex.DrawLatex(0.55,0.39,"#sigma:"+str(round(sigma,2)))

#can.SaveAs(path+"significance_"+signal['name']+".root")
#can.SaveAs(path+"significance_"+signal['name']+".png")
can.SaveAs(path+option+signal['label'].split('}')[1].replace(' ','_')+"_"+str(len(search_bins))+".png")
can.SaveAs(path+option+signal['label'].split('}')[1].replace(' ','_')+"_"+str(len(search_bins))+".root")

