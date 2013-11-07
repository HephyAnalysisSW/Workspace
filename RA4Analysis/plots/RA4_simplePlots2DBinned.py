import ROOT
from array import array
from math import *
import os, copy

from simplePlotsCommon import *
#execfile("simplePlotsCommon.py")
import xsec
small = False

allSamples=[]

#data={}
#data["name"]     = "Data";
#data["dirname"] = "/scratch/schoef/pat_101203/Mu/383/"
##data["bins"]    = ['Run2010A-Nov4ReReco','Run2010B-Nov4ReReco', 'Run2010B-Nov4ReReco-2e32']
#data["bins"]    = ['Run2010A-Nov4ReReco', 'Run2010B-Nov4ReReco-2e32']
#data["specialCuts"] = []
#allSamples.append(data)

targetLumi = 3.18 + 14.53 #+ 18.44 #101203


mc={}
mc["name"]     = "MC";
mc["dirname"] = "/scratch/schoef/pat_101203/Mu/383/"
mc["specialCuts"] = []
QCD_Bins =  ["QCD_Pt20to30_MuPt5Enriched",  "QCD_Pt30to50_MuPt5Enriched", "QCD_Pt50to80_MuPt5Enriched",  "QCD_Pt80to120_MuPt5Enriched", "QCD_Pt120to150_MuPt5Enriched", "QCD_Pt150_MuPt5Enriched"]
WJets_Bins = ["W1Jets_ptW-0to100","W1Jets_ptW-100to300","W1Jets_ptW-300to800","W1Jets_ptW-800to1600","W2Jets_ptW-0to100","W2Jets_ptW-100to300","W2Jets_ptW-300to800","W2Jets_ptW-800to1600","W3Jets_ptW-0to100","W3Jets_ptW-100to300","W3Jets_ptW-300to800","W3Jets_ptW-800to1600","W4Jets_ptW-0to100","W4Jets_ptW-100to300","W4Jets_ptW-300to800","W4Jets_ptW-800to1600","W5Jets_ptW-0to100","W5Jets_ptW-100to300","W5Jets_ptW-300to800","W5Jets_ptW-800to1600"]
#WJets_Bins = ["WJets"]
ZJets_Bins = ["ZJets"]
mc["bins"] =  ["TTJets"]
mc["bins"].extend(QCD_Bins)
mc["bins"].extend(WJets_Bins)
mc["bins"].extend(ZJets_Bins)
allSamples.append(mc)

ttbar = copy.deepcopy(mc)
ttbar["bins"] = ["TTJets"]

wjets = copy.deepcopy(mc)
wjets["bins"] = WJets_Bins

lm0={}
lm0["name"]     = "LM0";
lm0["dirname"] = "/scratch/schoef/pat_101203/Mu/383/"
lm0["bins"]    = ["LM0"]
allSamples.append(lm0)

lm1={}
lm1["name"]     = "LM1";
lm1["dirname"] = "/scratch/schoef/pat_101203/Mu/383/"
lm1["bins"]    = ["LM1"]
allSamples.append(lm1)

presel = "4j30"
#presel = "2j503j30"
#presel = "2j503j20"
#presel = "2j504j20"
subdir = "/png2D/"
chainstring = "empty"
commoncf = "(0)"
prefix="empty_"

if presel == "4j30":
  chainstring = "RA4Analyzer/Events"
  commoncf = "RA4Events.jet1pt>30&&RA4Events.jet3pt>30&&RA4Events.lepton_pt>15&&RA4Events.singleMuonic"
if presel == "pf-4j30":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "RA4Events.jet1pt>30&&RA4Events.jet3pt>30&&RA4Events.lepton_pt>15&&RA4Events.singleMuonic"
if presel == "2j503j30":
  chainstring = "RA4Analyzer/Events"
  commoncf = "RA4Events.jet1pt>50&&RA4Events.jet2pt>30&&RA4Events.lepton_pt>15&&RA4Events.singleMuonic"
if presel == "2j503j20":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "RA4Events.jet1pt>50&&RA4Events.jet2pt>20&&RA4Events.lepton_pt>15&&RA4Events.singleMuonic"
if presel == "2j504j20":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "RA4Events.jet1pt>50&&RA4Events.jet3pt>20&&RA4Events.lepton_pt>15&&RA4Events.singleMuonic"

prefix=presel+"_"

allVars=[]

htbins = [[100,200],[200,300],[300,400],[400,500], [500, 600], [600, -1]]

def cutString(thisbin):
  if thisbin[1]>0:
    return "&&"+str(thisbin[0])+"<ht&&ht<"+str(thisbin[1])
  else:
    return "&&ht>"+str(thisbin[0])
  

def binFix(thisbin):
  return "_ht_"+str(thisbin[0])+"to"+str(thisbin[1])

ttbar_plots = {}
wjets_plots = {}

for htbin in htbins:
  ttbar_met          = variable(":met;#slash{E}_{T} [GeV];Number of Events / 10 GeV",[52,0,520], commoncf + cutString(htbin) )
  ttbar_met.sample   = ttbar
  ttbar_met.color    = dataColor 
  ttbar_met.legendText="Data"
  ttbar_kinMetSig          = variable(":kinMetSig;S_{MET};Number of Events",[52,0,27], commoncf +cutString(htbin) )
  ttbar_kinMetSig.sample   = ttbar
  ttbar_kinMetSig.color    = dataColor
  ttbar_kinMetSig.legendText="Data"
  ttbar_ht2hadVSkinMetSig = variable2D(ttbar_met,ttbar_kinMetSig)
  ttbar_metVSmT = variable2D(ttbar_met,ttbar_kinMetSig)
  allVars.append(ttbar_metVSmT)
  ttbar_plots[binFix(htbin)] = ttbar_metVSmT

  wjets_met          = variable(":met;#slash{E}_{T} [GeV];Number of Events / 10 GeV",[52,0,520], commoncf + cutString(htbin) )
  wjets_met.sample   = wjets
  wjets_met.color    = dataColor 
  wjets_met.legendText="Data"
  wjets_kinMetSig          = variable(":kinMetSig;S_{MET};Number of Events",[52,0,27], commoncf +cutString(htbin) )
  wjets_kinMetSig.sample   = wjets
  wjets_kinMetSig.color    = dataColor
  wjets_kinMetSig.legendText="Data"
  wjets_ht2hadVSkinMetSig = variable2D(wjets_met,wjets_kinMetSig)
  wjets_metVSmT = variable2D(wjets_met,wjets_kinMetSig)
  allVars.append(wjets_metVSmT)
  wjets_plots[binFix(htbin)] = wjets_metVSmT

for sample in allSamples:
  sample["Chain"] = chainstring

for var in allVars:
  var.logy=True

for sample in allSamples:
  sample["filenames"]={}
  sample["weight"]={}
  if not sample.has_key("bins"):
    sample["bins"]=[""]
  for bin in sample["bins"]:
    subdirname = sample["dirname"]+"/"+bin+"/"
    if sample["bins"]==[""]:
      subdirname = sample["dirname"]+"/"
    c = ROOT.TChain("countingHLTFilter/CountTree")
    sample["filenames"][bin]=[]
    if small:
      filelist=os.listdir(subdirname)
      counter = 1   #Joining n files
      for file in filelist:
        if os.path.isfile(subdirname+file) and file[-5:]==".root" and file.count("histo")==1: 
          sample["filenames"][bin].append(subdirname+file)
#          c.Add(sample["dirname"]+file)
          if counter==0:
            break
          counter=counter-1
    else:
      sample["filenames"][bin] = [subdirname+"/h*.root"]
    for file in sample["filenames"][bin]:
      c.Add(file)
    nevents = c.GetEntries()
    weight = 1.
    if xsec.xsec.has_key(bin):
      if nevents>0:
        weight = xsec.xsec[bin]*targetLumi/nevents
      else:
        weight = 0.
    print sample["name"], bin, nevents,"weight",weight
    sample["weight"][bin]=weight
    del c

for var in allVars:
  var.data_histo.Reset("M")
for sample in allSamples:
  for bin in sample["bins"]:
    chainstring = "recoJetAnalyzer/Events"
    if sample.has_key("Chain"):
      chainstring = sample["Chain"]
    c = ROOT.TChain(chainstring)
    for file in sample["filenames"][bin]:
      c.Add(file)
    c.GetEntries()
    for var in allVars:
      if var.sample["name"] == sample["name"] and var.sample["bins"].count(bin)==1:
        htmp=ROOT.TH2F("htmp","htmp",*(var.binning))
        c.Draw(var.var2.name+":"+var.var1.name+">>htmp",str(sample["weight"][bin])+"*("+var.commoncf+")")
        htmp=ROOT.gDirectory.Get("htmp")
        var.data_histo.Add(htmp.Clone())
        print "At variable",var.name, "Sample",sample["name"],"bin",bin, "adding",htmp.Integral(),str(sample["weight"][bin])+"*("+var.commoncf+")"
        del htmp
    del c

ROOT.gStyle.SetOptStat(0)
ROOT.setTDRStyle()
#ROOT.gStyle.SetPadRightMargin(0.10);
if type(ROOT.tdrStyle)!=type(ROOT.gStyle):
  del ROOT.tdrStyle
  ROOT.setTDRStyle()

ROOT.tdrStyle.SetPadRightMargin(0.16)
ROOT.gROOT.ProcessLine(".L ../../EarlyMETAnalysis/aclic/useNiceColorPalette.C+")
ROOT.useNiceColorPalette(255)

for var in allVars:
  var.data_histo.GetYaxis().SetLabelSize(0.04)
  var.data_histo.GetXaxis().SetLabelSize(0.04)
#  var.data_histo.GetZaxis().SetRangeUser(10**(-3), 10)

for thisbin in htbins:
  c1 = ROOT.TCanvas("ROOT.c1","drawHistos",200,10,500,500)
#  ttbar_plots[binFix(thisbin)].data_histo.SetMarkerSize(0)
  ttbar_plots[binFix(thisbin)].data_histo.Draw("COLZ")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/"+subdir+prefix+"metVSkinMetSig_ttbar"+binFix(thisbin)+".png")
#  ttbar_plots[binFix(thisbin)].data_histo.GetZaxis().SetRangeUser(0,100)
#  wjets_plots[binFix(thisbin)].data_histo.SetMarkerColor(ROOT.kRed)
#  wjets_plots[binFix(thisbin)].data_histo.SetMarkerSize(0)
  wjets_plots[binFix(thisbin)].data_histo.Draw("COLZ")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/"+subdir+prefix+"metVSkinMetSig_wjets"+binFix(thisbin)+".png")
  del c1

#for plot in plots:
#  draw2D(plot[0],                  )
