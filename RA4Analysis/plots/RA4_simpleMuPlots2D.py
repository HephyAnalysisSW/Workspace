import ROOT
from array import array
from math import *
import os, copy

from simplePlotsCommon import *
import xsec
small = False

from defaultMuSamples import *

presel = "pf-3j40"
subdir = "/png2011/"
chainstring = "empty"
commoncf = "(0)"
prefix="empty_"
targetLumi = 1000.
binningHT = [77,0,1540]
binningMET = [52,0,1040]
binningkMs = [80,0,20]
additionalCut = ""
preprefix = ""

if presel == "pf-3j40":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet1pt>40&&jet2pt>40&&lepton_pt>15&&singleMuonic"


if additionalCut != "":
  commoncf = commoncf + "&&" +  additionalCut
if preprefix != "":
  prefix = preprefix + "_"+presel
else:
  prefix = presel

allVars=[]

############################################################### HT vs. kinMetSig

data_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
data_ht.sample   = data
data_ht.color    = dataColor
data_ht.legendText="Data"
data_kinMetSig          = variable(":kinMetSig;S_{MET};Number of Events",binningkMs, commoncf )
data_kinMetSig.sample   = data
data_kinMetSig.color    = dataColor
data_kinMetSig.legendText="Data"
data_htVSkinMetSig = variable2D(data_ht,data_kinMetSig)
allVars.append(data_htVSkinMetSig)

mc_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
mc_ht.sample   = mc
mc_ht.color    = dataColor 
mc_ht.legendText="Data"
mc_kinMetSig          = variable(":kinMetSig;S_{MET};Number of Events",binningkMs, commoncf )
mc_kinMetSig.sample   = mc
mc_kinMetSig.color    = dataColor 
mc_kinMetSig.legendText="Data"
mc_htVSkinMetSig = variable2D(mc_ht,mc_kinMetSig)
allVars.append(mc_htVSkinMetSig)

ttbar_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
ttbar_ht.sample   = ttbar
ttbar_ht.color    = dataColor 
ttbar_ht.legendText="Data"
ttbar_kinMetSig          = variable(":kinMetSig;S_{MET};Number of Events",binningkMs, commoncf )
ttbar_kinMetSig.sample   = ttbar
ttbar_kinMetSig.color    = dataColor 
ttbar_kinMetSig.legendText="Data"
ttbar_htVSkinMetSig = variable2D(ttbar_ht,ttbar_kinMetSig)
allVars.append(ttbar_htVSkinMetSig)

wjets_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
wjets_ht.sample   = wjets
wjets_ht.color    = dataColor 
wjets_ht.legendText="Data"
wjets_kinMetSig          = variable(":kinMetSig;S_{MET};Number of Events",binningkMs, commoncf )
wjets_kinMetSig.sample   = wjets
wjets_kinMetSig.color    = dataColor 
wjets_kinMetSig.legendText="Data"
wjets_htVSkinMetSig = variable2D(wjets_ht,wjets_kinMetSig)
allVars.append(wjets_htVSkinMetSig)

lm9_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT , commoncf+"&&ht>0")
lm9_ht.sample   = getSignal(9)
lm9_ht.color    = dataColor 
lm9_ht.legendText="Data"
lm9_kinMetSig          = variable(":kinMetSig;S_{MET};Number of Events",binningkMs, commoncf )
lm9_kinMetSig.sample   = getSignal(9)
lm9_kinMetSig.color    = dataColor 
lm9_kinMetSig.legendText="Data"
lm9_htVSkinMetSig = variable2D(lm9_ht,lm9_kinMetSig)
allVars.append(lm9_htVSkinMetSig)

lm8_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
lm8_ht.sample   = getSignal(8)
lm8_ht.color    = dataColor 
lm8_ht.legendText="Data"
lm8_kinMetSig          = variable(":kinMetSig;S_{MET};Number of Events",binningkMs, commoncf )
lm8_kinMetSig.sample   = getSignal(8)
lm8_kinMetSig.color    = dataColor 
lm8_kinMetSig.legendText="Data"
lm8_htVSkinMetSig = variable2D(lm8_ht,lm8_kinMetSig)
allVars.append(lm8_htVSkinMetSig)

data_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
data_ht.sample   = data
data_ht.color    = dataColor
data_ht.legendText="Data"
data_kinMetSig          = variable(":kinMetSig;S_{MET};Number of Events",binningkMs, commoncf )
data_kinMetSig.sample   = data
data_kinMetSig.color    = dataColor
data_kinMetSig.legendText="Data"
data_htVSkinMetSig = variable2D(data_ht,data_kinMetSig)
allVars.append(data_htVSkinMetSig)

mc_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
mc_ht.sample   = mc
mc_ht.color    = dataColor 
mc_ht.legendText="Data"
mc_kinMetSig          = variable(":kinMetSig;S_{MET};Number of Events",binningkMs, commoncf )
mc_kinMetSig.sample   = mc
mc_kinMetSig.color    = dataColor 
mc_kinMetSig.legendText="Data"
mc_htVSkinMetSig = variable2D(mc_ht,mc_kinMetSig)
allVars.append(mc_htVSkinMetSig)

ttbar_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
ttbar_ht.sample   = ttbar
ttbar_ht.color    = dataColor 
ttbar_ht.legendText="Data"
ttbar_kinMetSig          = variable(":kinMetSig;S_{MET};Number of Events",binningkMs, commoncf )
ttbar_kinMetSig.sample   = ttbar
ttbar_kinMetSig.color    = dataColor 
ttbar_kinMetSig.legendText="Data"
ttbar_htVSkinMetSig = variable2D(ttbar_ht,ttbar_kinMetSig)
allVars.append(ttbar_htVSkinMetSig)

wjets_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
wjets_ht.sample   = wjets
wjets_ht.color    = dataColor 
wjets_ht.legendText="Data"
wjets_kinMetSig          = variable(":kinMetSig;S_{MET};Number of Events",binningkMs, commoncf )
wjets_kinMetSig.sample   = wjets
wjets_kinMetSig.color    = dataColor 
wjets_kinMetSig.legendText="Data"
wjets_htVSkinMetSig = variable2D(wjets_ht,wjets_kinMetSig)
allVars.append(wjets_htVSkinMetSig)

lm9_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT , commoncf+"&&ht>0")
lm9_ht.sample   = getSignal(9)
lm9_ht.color    = dataColor 
lm9_ht.legendText="Data"
lm9_kinMetSig          = variable(":kinMetSig;S_{MET};Number of Events",binningkMs, commoncf )
lm9_kinMetSig.sample   = getSignal(9)
lm9_kinMetSig.color    = dataColor 
lm9_kinMetSig.legendText="Data"
lm9_htVSkinMetSig = variable2D(lm9_ht,lm9_kinMetSig)
allVars.append(lm9_htVSkinMetSig)

lm8_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
lm8_ht.sample   = getSignal(8)
lm8_ht.color    = dataColor 
lm8_ht.legendText="Data"
lm8_kinMetSig          = variable(":kinMetSig;S_{MET};Number of Events",binningkMs, commoncf )
lm8_kinMetSig.sample   = getSignal(8)
lm8_kinMetSig.color    = dataColor 
lm8_kinMetSig.legendText="Data"
lm8_htVSkinMetSig = variable2D(lm8_ht,lm8_kinMetSig)
allVars.append(lm8_htVSkinMetSig)

############################################################################
############################################################### HT vs. MET

data_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
data_ht.sample   = data
data_ht.color    = dataColor
data_ht.legendText="Data"
data_met          = variable(":met;#slash{E}_{T} (GeV);Number of Events",binningMET, commoncf )
data_met.sample   = data
data_met.color    = dataColor
data_met.legendText="Data"
data_htVSmet = variable2D(data_met,data_ht)
allVars.append(data_htVSmet)

mc_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
mc_ht.sample   = mc
mc_ht.color    = dataColor 
mc_ht.legendText="Data"
mc_met          = variable(":met;#slash{E}_{T} (GeV);Number of Events",binningMET, commoncf )
mc_met.sample   = mc
mc_met.color    = dataColor 
mc_met.legendText="Data"
mc_htVSmet = variable2D(mc_met,mc_ht)
allVars.append(mc_htVSmet)

ttbar_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
ttbar_ht.sample   = ttbar
ttbar_ht.color    = dataColor 
ttbar_ht.legendText="Data"
ttbar_met          = variable(":met;#slash{E}_{T} (GeV);Number of Events",binningMET, commoncf )
ttbar_met.sample   = ttbar
ttbar_met.color    = dataColor 
ttbar_met.legendText="Data"
ttbar_htVSmet = variable2D(ttbar_met,ttbar_ht)
allVars.append(ttbar_htVSmet)

wjets_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
wjets_ht.sample   = wjets
wjets_ht.color    = dataColor 
wjets_ht.legendText="Data"
wjets_met          = variable(":met;#slash{E}_{T} (GeV);Number of Events",binningMET, commoncf )
wjets_met.sample   = wjets
wjets_met.color    = dataColor 
wjets_met.legendText="Data"
wjets_htVSmet = variable2D(wjets_met,wjets_ht)
allVars.append(wjets_htVSmet)

lm9_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT , commoncf+"&&ht>0")
lm9_ht.sample   = getSignal(9)
lm9_ht.color    = dataColor 
lm9_ht.legendText="Data"
lm9_met          = variable(":met;#slash{E}_{T} (GeV);Number of Events",binningMET, commoncf )
lm9_met.sample   = getSignal(9)
lm9_met.color    = dataColor 
lm9_met.legendText="Data"
lm9_htVSmet = variable2D(lm9_met,lm9_ht)
allVars.append(lm9_htVSmet)

lm8_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
lm8_ht.sample   = getSignal(8)
lm8_ht.color    = dataColor 
lm8_ht.legendText="Data"
lm8_met          = variable(":met;#slash{E}_{T} (GeV);Number of Events",binningMET, commoncf )
lm8_met.sample   = getSignal(8)
lm8_met.color    = dataColor 
lm8_met.legendText="Data"
lm8_htVSmet = variable2D(lm8_met,lm8_ht)
allVars.append(lm8_htVSmet)

############################################################################# HT vs GENMET

mc_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
mc_ht.sample   = mc
mc_ht.color    = dataColor 
mc_ht.legendText="Data"
mc_met          = variable(":genmet;gen-#slash{E}_{T} (GeV);Number of Events",binningMET, commoncf )
mc_met.sample   = mc
mc_met.color    = dataColor 
mc_met.legendText="Data"
mc_htVSgenMet = variable2D(mc_met,mc_ht)
allVars.append(mc_htVSgenMet)

ttbar_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
ttbar_ht.sample   = ttbar
ttbar_ht.color    = dataColor 
ttbar_ht.legendText="Data"
ttbar_met          = variable(":genmet;gen-#slash{E}_{T} (GeV);Number of Events",binningMET, commoncf )
ttbar_met.sample   = ttbar
ttbar_met.color    = dataColor 
ttbar_met.legendText="Data"
ttbar_htVSgenMet = variable2D(ttbar_met,ttbar_ht)
allVars.append(ttbar_htVSgenMet)

wjets_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
wjets_ht.sample   = wjets
wjets_ht.color    = dataColor 
wjets_ht.legendText="Data"
wjets_met          = variable(":genmet;gen-#slash{E}_{T} (GeV);Number of Events",binningMET, commoncf )
wjets_met.sample   = wjets
wjets_met.color    = dataColor 
wjets_met.legendText="Data"
wjets_htVSgenMet = variable2D(wjets_met,wjets_ht)
allVars.append(wjets_htVSgenMet)

lm9_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT , commoncf+"&&ht>0")
lm9_ht.sample   = getSignal(9)
lm9_ht.color    = dataColor 
lm9_ht.legendText="Data"
lm9_met          = variable(":genmet;gen-#slash{E}_{T} (GeV);Number of Events",binningMET, commoncf )
lm9_met.sample   = getSignal(9)
lm9_met.color    = dataColor 
lm9_met.legendText="Data"
lm9_htVSgenMet = variable2D(lm9_met,lm9_ht)
allVars.append(lm9_htVSgenMet)

lm8_ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",binningHT, commoncf+"&&ht>0")
lm8_ht.sample   = getSignal(8)
lm8_ht.color    = dataColor 
lm8_ht.legendText="Data"
lm8_met          = variable(":genmet;gen-#slash{E}_{T} (GeV);Number of Events",binningMET, commoncf )
lm8_met.sample   = getSignal(8)
lm8_met.color    = dataColor 
lm8_met.legendText="Data"
lm8_htVSgenMet = variable2D(lm8_met,lm8_ht)
allVars.append(lm8_htVSgenMet)

for sample in allSamples:
  sample["Chain"] = chainstring

for var in allVars:
  var.logy=True
  var.lines = [[0.17,0.963,'#sqrt{s} = 7TeV'], [0.36,0.963,"#font[22]{CMS simulation}"], [0.69, 0.963, str(int(round(targetLumi)))+" pb^{-1}"]]

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
        htmp.Sumw2()
        c.Draw(var.var2.name+":"+var.var1.name+">>htmp",str(sample["weight"][bin])+"*("+var.cutfunc+")")
        htmp=ROOT.gDirectory.Get("htmp")
        var.data_histo.Add(htmp.Clone())
        print "At variable",var.name, "Sample",sample["name"],"bin",bin, "adding",htmp.Integral(),str(sample["weight"][bin])+"*("+var.cutfunc+")"
        del htmp
    del c

ROOT.gStyle.SetOptStat(0)
ROOT.setTDRStyle()
#ROOT.gStyle.SetPadRightMargin(0.10);
if type(ROOT.tdrStyle)!=type(ROOT.gStyle):
  del ROOT.tdrStyle
  ROOT.setTDRStyle()

ROOT.tdrStyle.SetPadRightMargin(0.16)
ROOT.gROOT.ProcessLine(".L ../../Scripts/aclic/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)

for var in allVars:
  var.data_histo.GetYaxis().SetLabelSize(0.04)
  var.data_histo.GetXaxis().SetLabelSize(0.04)
  var.data_histo.GetZaxis().SetRangeUser(10**(-2.9), 90)
#  var.lines = [[0.17,0.963,'#sqrt{s} = 7TeV'], [0.36,0.963,"#font[22]{CMS simulation}"]] 
#  var.lines = [[0.17,0.963,'#sqrt{s} = 7TeV'], [0.36,0.963,"#font[22]{CMS simulation}"] ,[0.69, 0.963, str(int(round(targetLumi)))+" pb^{-1}"], [0.4, 0.27, 'A', 0.07], [0.7, 0.27, 'B', 0.07], [0.4, 0.80, 'C', 0.07], [0.7, 0.80, 'D', 0.07]]
  var.lines = [[0.17,0.963,'#sqrt{s} = 7TeV'], [0.36,0.963,"#font[22]{CMS simulation}"] ,[0.69, 0.963, str(int(round(targetLumi)))+" pb^{-1}"]]

data_htVSkinMetSig.data_histo.GetZaxis().SetRangeUser(10**(-2), 150)
data_htVSmet.data_histo.GetZaxis().SetRangeUser(10**(-2), 150)

#draw2D(data_htVSkinMetSig,         subdir+prefix+"Mu_data_htVSkinMetSig" ,  True, [[300,650,650],[2.5,5.5,5.5]])
#draw2D(mc_htVSkinMetSig,           subdir+prefix+"Mu_mc_htVSkinMetSig",     True, [[300,650,650],[2.5,5.5,5.5]])
#draw2D(ttbar_htVSkinMetSig,        subdir+prefix+"Mu_ttbar_htVSkinMetSig" , True, [[300,650,650],[2.5,5.5,5.5]])
#draw2D(wjets_htVSkinMetSig,        subdir+prefix+"Mu_wjets_htVSkinMetSig" , True, [[300,650,650],[2.5,5.5,5.5]])
#draw2D(lm9_htVSkinMetSig,          subdir+prefix+"Mu_lm9_htVSkinMetSig"   , True, [[300,650,650],[2.5,5.5,5.5]])
#draw2D(lm8_htVSkinMetSig,          subdir+prefix+"Mu_lm8_htVSkinMetSig"   , True, [[300,650,650],[2.5,5.5,5.5]])

draw2D(data_htVSkinMetSig,         subdir+prefix+"Mu_data_htVSkinMetSig" )
draw2D(mc_htVSkinMetSig,           subdir+prefix+"Mu_mc_htVSkinMetSig"   )
draw2D(ttbar_htVSkinMetSig,        subdir+prefix+"Mu_ttbar_htVSkinMetSig")
draw2D(wjets_htVSkinMetSig,        subdir+prefix+"Mu_wjets_htVSkinMetSig")
draw2D(lm9_htVSkinMetSig,          subdir+prefix+"Mu_lm9_htVSkinMetSig"  )
draw2D(lm8_htVSkinMetSig,          subdir+prefix+"Mu_lm8_htVSkinMetSig"  )

draw2D(data_htVSmet,         subdir+prefix+"Mu_data_htVSmet" )
draw2D(mc_htVSmet,           subdir+prefix+"Mu_mc_htVSmet"   )
draw2D(ttbar_htVSmet,        subdir+prefix+"Mu_ttbar_htVSmet")
draw2D(wjets_htVSmet,        subdir+prefix+"Mu_wjets_htVSmet")
draw2D(lm9_htVSmet,          subdir+prefix+"Mu_lm9_htVSmet"  )
draw2D(lm8_htVSmet,          subdir+prefix+"Mu_lm8_htVSmet"  )

draw2D(mc_htVSgenMet,           subdir+prefix+"Mu_mc_htVSgenMet"   )
draw2D(ttbar_htVSgenMet,        subdir+prefix+"Mu_ttbar_htVSgenMet")
draw2D(wjets_htVSgenMet,        subdir+prefix+"Mu_wjets_htVSgenMet")
draw2D(lm9_htVSgenMet,          subdir+prefix+"Mu_lm9_htVSgenMet"  )
draw2D(lm8_htVSgenMet,          subdir+prefix+"Mu_lm8_htVSgenMet"  )
