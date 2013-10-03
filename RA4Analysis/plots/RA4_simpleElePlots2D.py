import ROOT
from array import array
from math import *
import os, copy

from simplePlotsCommon import *
import xsec
small = False

from defaultEleSamples import *

presel = "pf-4j30"
subdir = "/png2011/"
chainstring = "empty"
commoncf = "(0)"
prefix="empty_"

#mode = "WA"
mode = "PAS"
binningHT = -1  
binningkMs = -1 
preprefix = ""
prefix=presel+"_"

if mode == "PAS":
  binningHT = [70,50,1450]
  binningkMs = [80,0,20]

if mode ==  "WA":
  binningHT = [40,0,1000]
  binningkMs = [80,0,20]


if presel == "pf-4j30":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "RA4Events.jet1pt>30&&RA4Events.jet3pt>30&&RA4Events.lepton_pt>20&&RA4Events.singleElectronic"

if presel == "pf-4j30-l25":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "RA4Events.jet1pt>30&&RA4Events.jet3pt>30&&RA4Events.lepton_pt>25&&RA4Events.singleElectronic"
if preprefix != "":
  prefix = preprefix + "_"+presel

allVars=[]

#data_met          = variable(":met;#slash{E}_{T} (GeV);Number of Events / 3 GeV",[77,0,231], commoncf )
#data_met.sample   = data
#data_met.color    = dataColor 
#data_met.legendText="Data"
#data_mT          = variable(":mT;m_{T} (GeV);Number of Events / 3 GeV",[77,0,231], commoncf )
#data_mT.sample   = data
#data_mT.color    = dataColor 
#data_mT.legendText="Data"
#data_metVSmT = variable2D(data_met,data_mT)
#allVars.append(data_metVSmT)

data_ht          = variable(":ht;H_{T} (GeV);Number of Events / 16 GeV",binningHT, commoncf+"&&ht>0")
data_ht.sample   = data
data_ht.color    = dataColor
data_ht.legendText="Data"
data_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",binningkMs, commoncf )
data_kinMetSig.sample   = data
data_kinMetSig.color    = dataColor
data_kinMetSig.legendText="Data"
data_htVSkinMetSig = variable2D(data_ht,data_kinMetSig)
allVars.append(data_htVSkinMetSig)

#data_low_ht          = variable(":ht;H_{T} (GeV);Number of Events / 16 GeV",[50,0,500], commoncf+"&&ht>0")
#data_low_ht.sample   = data
#data_low_ht.color    = dataColor
#data_low_ht.legendText="Data"
#data_low_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",[52,0,27], commoncf )
#data_low_kinMetSig.sample   = data
#data_low_kinMetSig.color    = dataColor
#data_low_kinMetSig.legendText="Data"
#data_low_htVSkinMetSig = variable2D(data_low_ht,data_low_kinMetSig)
#allVars.append(data_low_htVSkinMetSig)

#data_ht2had          = variable(":ht2;H_{T2}^{had.} (GeV);Number of Events / 16 GeV",binningHT, commoncf+"&&ht2>0")
#data_ht2had.sample   = data
#data_ht2had.color    = dataColor
#data_ht2had.legendText="Data"
#data_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",binningkMs, commoncf )
#data_kinMetSig.sample   = data
#data_kinMetSig.color    = dataColor
#data_kinMetSig.legendText="Data"
#data_ht2hadVSkinMetSig = variable2D(data_ht2had,data_kinMetSig)
#allVars.append(data_ht2hadVSkinMetSig)
#
#data_low_ht2had          = variable(":ht2;H_{T2}^{had.} (GeV);Number of Events / 16 GeV",[50,0,500], commoncf+"&&ht2>0")
#data_low_ht2had.sample   = data
#data_low_ht2had.color    = dataColor
#data_low_ht2had.legendText="Data"
#data_low_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",[52,0,27], commoncf )
#data_low_kinMetSig.sample   = data
#data_low_kinMetSig.color    = dataColor
#data_low_kinMetSig.legendText="Data"
#data_low_ht2hadVSkinMetSig = variable2D(data_low_ht2had,data_low_kinMetSig)
#allVars.append(data_low_ht2hadVSkinMetSig)
#
#
#data_ht2          = variable(":ht2+lepton_pt;H_{T2} (GeV);Number of Events / 5 GeV",[105,0,525], commoncf+"&&ht2>0" )
#data_ht2.sample   = data
#data_ht2.color    = dataColor 
#data_ht2.legendText="Data"
#data_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",[27,0,27], commoncf )
#data_kinMetSig.sample   = data
#data_kinMetSig.color    = dataColor 
#data_kinMetSig.legendText="Data"
#data_ht2VSkinMetSig = variable2D(data_ht2,data_kinMetSig)
#allVars.append(data_ht2VSkinMetSig)
#
#mc_met          = variable(":met;#slash{E}_{T} (GeV);Number of Events / 3 GeV",[77,0,231], commoncf )
#mc_met.sample   = mc
#mc_met.color    = dataColor 
#mc_met.legendText="Data"
#mc_mT          = variable(":mT;m_{T} (GeV);Number of Events / 3 GeV",[77,0,231], commoncf )
#mc_mT.sample   = mc
#mc_mT.color    = dataColor 
#mc_mT.legendText="Data"
#mc_metVSmT = variable2D(mc_met,mc_mT)
#allVars.append(mc_metVSmT)

mc_ht          = variable(":ht;H_{T} (GeV);Number of Events / 5 GeV",binningHT, commoncf+"&&ht>0")
mc_ht.sample   = mc
mc_ht.color    = dataColor 
mc_ht.legendText="Data"
mc_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",binningkMs, commoncf )
mc_kinMetSig.sample   = mc
mc_kinMetSig.color    = dataColor 
mc_kinMetSig.legendText="Data"
mc_htVSkinMetSig = variable2D(mc_ht,mc_kinMetSig)
allVars.append(mc_htVSkinMetSig)

#mc_low_ht          = variable(":ht;H_{T} (GeV);Number of Events / 16 GeV",[50,0,500], commoncf+"&&ht>0")
#mc_low_ht.sample   = mc
#mc_low_ht.color    = dataColor 
#mc_low_ht.legendText="Data"
#mc_low_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",[52,0,27], commoncf )
#mc_low_kinMetSig.sample   = mc
#mc_low_kinMetSig.color    = dataColor 
#mc_low_kinMetSig.legendText="Data"
#mc_low_htVSkinMetSig = variable2D(mc_low_ht,mc_low_kinMetSig)
#allVars.append(mc_low_htVSkinMetSig)


ttbar_ht          = variable(":ht;H_{T} (GeV);Number of Events / 5 GeV",binningHT, commoncf+"&&ht>0")
ttbar_ht.sample   = ttbar
ttbar_ht.color    = dataColor 
ttbar_ht.legendText="Data"
ttbar_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",binningkMs, commoncf )
ttbar_kinMetSig.sample   = ttbar
ttbar_kinMetSig.color    = dataColor 
ttbar_kinMetSig.legendText="Data"
ttbar_htVSkinMetSig = variable2D(ttbar_ht,ttbar_kinMetSig)
allVars.append(ttbar_htVSkinMetSig)

#ttbar_low_ht          = variable(":ht;H_{T} (GeV);Number of Events / 16 GeV",[50,0,500], commoncf+"&&ht>0")
#ttbar_low_ht.sample   = ttbar
#ttbar_low_ht.color    = dataColor 
#ttbar_low_ht.legendText="Data"
#ttbar_low_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",[52,0,27], commoncf )
#ttbar_low_kinMetSig.sample   = ttbar
#ttbar_low_kinMetSig.color    = dataColor 
#ttbar_low_kinMetSig.legendText="Data"
#ttbar_low_htVSkinMetSig = variable2D(ttbar_low_ht,ttbar_low_kinMetSig)
#allVars.append(ttbar_low_htVSkinMetSig)


wjets_ht          = variable(":ht;H_{T} (GeV);Number of Events / 5 GeV",binningHT, commoncf+"&&ht>0")
wjets_ht.sample   = wjets
wjets_ht.color    = dataColor 
wjets_ht.legendText="Data"
wjets_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",binningkMs, commoncf )
wjets_kinMetSig.sample   = wjets
wjets_kinMetSig.color    = dataColor 
wjets_kinMetSig.legendText="Data"
wjets_htVSkinMetSig = variable2D(wjets_ht,wjets_kinMetSig)
allVars.append(wjets_htVSkinMetSig)

#wjets_low_ht          = variable(":ht;H_{T} (GeV);Number of Events / 16 GeV",[50,0,500], commoncf+"&&ht>0")
#wjets_low_ht.sample   = wjets
#wjets_low_ht.color    = dataColor 
#wjets_low_ht.legendText="Data"
#wjets_low_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",[52,0,27], commoncf )
#wjets_low_kinMetSig.sample   = wjets
#wjets_low_kinMetSig.color    = dataColor 
#wjets_low_kinMetSig.legendText="Data"
#wjets_low_htVSkinMetSig = variable2D(wjets_low_ht,wjets_low_kinMetSig)
#allVars.append(wjets_low_htVSkinMetSig)

lm0_ht          = variable(":ht;H_{T} (GeV);Number of Events / 5 GeV",binningHT, commoncf+"&&ht>0")
lm0_ht.sample   = getSignal(0)
lm0_ht.color    = dataColor 
lm0_ht.legendText="Data"
lm0_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",binningkMs, commoncf )
lm0_kinMetSig.sample   = getSignal(0)
lm0_kinMetSig.color    = dataColor 
lm0_kinMetSig.legendText="Data"
lm0_htVSkinMetSig = variable2D(lm0_ht,lm0_kinMetSig)
allVars.append(lm0_htVSkinMetSig)

#lm0_low_ht          = variable(":ht;H_{T} (GeV);Number of Events / 16 GeV",[50,0,500], commoncf+"&&ht>0")
#lm0_low_ht.sample   = getSignal(0)
#lm0_low_ht.color    = dataColor 
#lm0_low_ht.legendText="Data"
#lm0_low_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",[52,0,27], commoncf )
#lm0_low_kinMetSig.sample   = getSignal(0)
#lm0_low_kinMetSig.color    = dataColor 
#lm0_low_kinMetSig.legendText="Data"
#lm0_low_htVSkinMetSig = variable2D(lm0_low_ht,lm0_low_kinMetSig)
#allVars.append(lm0_low_htVSkinMetSig)


lm1_ht          = variable(":ht;H_{T} (GeV);Number of Events / 5 GeV",binningHT, commoncf+"&&ht>0")
lm1_ht.sample   = getSignal(1)
lm1_ht.color    = dataColor 
lm1_ht.legendText="Data"
lm1_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",binningkMs, commoncf )
lm1_kinMetSig.sample   = getSignal(1)
lm1_kinMetSig.color    = dataColor 
lm1_kinMetSig.legendText="Data"
lm1_htVSkinMetSig = variable2D(lm1_ht,lm1_kinMetSig)
allVars.append(lm1_htVSkinMetSig)

#lm1_low_ht          = variable(":ht;H_{T} (GeV);Number of Events / 16 GeV",[50,0,500], commoncf+"&&ht>0")
#lm1_low_ht.sample   = getSignal(1)
#lm1_low_ht.color    = dataColor 
#lm1_low_ht.legendText="Data"
#lm1_low_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",[52,0,27], commoncf )
#lm1_low_kinMetSig.sample   = getSignal(1)
#lm1_low_kinMetSig.color    = dataColor 
#lm1_low_kinMetSig.legendText="Data"
#lm1_low_htVSkinMetSig = variable2D(lm1_low_ht,lm1_low_kinMetSig)
#allVars.append(lm1_low_htVSkinMetSig)

#mc_ht2          = variable(":ht2+lepton_pt;H_{T2} (GeV);Number of Events / 16 GeV",binningHT, commoncf+"&&ht2>0")
#mc_ht2.sample   = mc
#mc_ht2.color    = dataColor 
#mc_ht2.legendText="Data"
#mc_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",binningkMs, commoncf )
#mc_kinMetSig.sample   = mc
#mc_kinMetSig.color    = dataColor 
#mc_kinMetSig.legendText="Data"
#mc_ht2VSkinMetSig = variable2D(mc_ht2,mc_kinMetSig)
#allVars.append(mc_ht2VSkinMetSig)

mc_ht          = variable(":ht;H_{T} (GeV);Number of Events / 16 GeV",binningHT, commoncf+"&&ht>0")
mc_ht.sample   = mc
mc_ht.color    = dataColor 
mc_ht.legendText="Data"
mc_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",binningkMs, commoncf )
mc_kinMetSig.sample   = mc
mc_kinMetSig.color    = dataColor 
mc_kinMetSig.legendText="Data"
mc_htVSkinMetSig = variable2D(mc_ht,mc_kinMetSig)
allVars.append(mc_htVSkinMetSig)

#mc_leptonpt          = variable(":lepton_pt;p_{T, lep.} (GeV);Number of Events / 16 GeV",binningHT, commoncf)
#mc_leptonpt.sample   = mc
#mc_leptonpt.color    = dataColor 
#mc_leptonpt.legendText="Data"
#mc_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",binningkMs, commoncf )
#mc_kinMetSig.sample   = mc
#mc_kinMetSig.color    = dataColor 
#mc_kinMetSig.legendText="Data"
#mc_leptonptVSkinMetSig = variable2D(mc_leptonpt,mc_kinMetSig)
#allVars.append(mc_leptonptVSkinMetSig)

#mc_ht2had          = variable(":ht2;H_{T2}^{had.} (GeV);Number of Events / 5 GeV",binningHT, commoncf+"&&ht2>0")
#mc_ht2had.sample   = mc
#mc_ht2had.color    = dataColor
#mc_ht2had.legendText="Data"
#mc_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",binningkMs, commoncf )
#mc_kinMetSig.sample   = mc
#mc_kinMetSig.color    = dataColor
#mc_kinMetSig.legendText="Data"
#mc_ht2hadVSkinMetSig = variable2D(mc_ht2had,mc_kinMetSig)
#allVars.append(mc_ht2hadVSkinMetSig)
#
#mc_low_ht2had          = variable(":ht2;H_{T2}^{had.} (GeV);Number of Events / 16 GeV",[50,0,500], commoncf+"&&ht2>0")
#mc_low_ht2had.sample   = mc
#mc_low_ht2had.color    = dataColor
#mc_low_ht2had.legendText="Data"
#mc_low_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",[52,0,27], commoncf )
#mc_low_kinMetSig.sample   = mc
#mc_low_kinMetSig.color    = dataColor
#mc_low_kinMetSig.legendText="Data"
#mc_low_ht2hadVSkinMetSig = variable2D(mc_low_ht2had,mc_low_kinMetSig)
#allVars.append(mc_low_ht2hadVSkinMetSig)
#
#
#ttbar_ht2had          = variable(":ht2;H_{T2}^{had.} (GeV);Number of Events / 5 GeV",binningHT, commoncf+"&&ht2>0")
#ttbar_ht2had.sample   = ttbar
#ttbar_ht2had.color    = dataColor
#ttbar_ht2had.legendText="Data"
#ttbar_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",binningkMs, commoncf )
#ttbar_kinMetSig.sample   = ttbar
#ttbar_kinMetSig.color    = dataColor
#ttbar_kinMetSig.legendText="Data"
#ttbar_ht2hadVSkinMetSig = variable2D(ttbar_ht2had,ttbar_kinMetSig)
#allVars.append(ttbar_ht2hadVSkinMetSig)
#
#ttbar_low_ht2had          = variable(":ht2;H_{T2}^{had.} (GeV);Number of Events / 16 GeV",[50,0,500], commoncf+"&&ht2>0")
#ttbar_low_ht2had.sample   = ttbar
#ttbar_low_ht2had.color    = dataColor
#ttbar_low_ht2had.legendText="Data"
#ttbar_low_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",[52,0,27], commoncf )
#ttbar_low_kinMetSig.sample   = ttbar
#ttbar_low_kinMetSig.color    = dataColor
#ttbar_low_kinMetSig.legendText="Data"
#ttbar_low_ht2hadVSkinMetSig = variable2D(ttbar_low_ht2had,ttbar_low_kinMetSig)
#allVars.append(ttbar_low_ht2hadVSkinMetSig)
#
#wjets_ht2had          = variable(":ht2;H_{T2}^{had.} (GeV);Number of Events / 5 GeV",binningHT, commoncf+"&&ht2>0")
#wjets_ht2had.sample   = wjets
#wjets_ht2had.color    = dataColor
#wjets_ht2had.legendText="Data"
#wjets_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",binningkMs, commoncf )
#wjets_kinMetSig.sample   = wjets
#wjets_kinMetSig.color    = dataColor
#wjets_kinMetSig.legendText="Data"
#wjets_ht2hadVSkinMetSig = variable2D(wjets_ht2had,wjets_kinMetSig)
#allVars.append(wjets_ht2hadVSkinMetSig)
#
#wjets_low_ht2had          = variable(":ht2;H_{T2}^{had.} (GeV);Number of Events / 16 GeV",[50,0,500], commoncf+"&&ht2>0")
#wjets_low_ht2had.sample   = wjets
#wjets_low_ht2had.color    = dataColor
#wjets_low_ht2had.legendText="Data"
#wjets_low_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",[52,0,27], commoncf )
#wjets_low_kinMetSig.sample   = wjets
#wjets_low_kinMetSig.color    = dataColor
#wjets_low_kinMetSig.legendText="Data"
#wjets_low_ht2hadVSkinMetSig = variable2D(wjets_low_ht2had,wjets_low_kinMetSig)
#allVars.append(wjets_low_ht2hadVSkinMetSig)
#
#lm0_ht2had          = variable(":ht2;H_{T2}^{had.} (GeV);Number of Events / 5 GeV",binningHT, commoncf+"&&ht2>0")
#lm0_ht2had.sample   = getSignal(0)
#lm0_ht2had.color    = dataColor
#lm0_ht2had.legendText="Data"
#lm0_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",binningkMs, commoncf )
#lm0_kinMetSig.sample   = getSignal(0)
#lm0_kinMetSig.color    = dataColor
#lm0_kinMetSig.legendText="Data"
#lm0_ht2hadVSkinMetSig = variable2D(lm0_ht2had,lm0_kinMetSig)
#allVars.append(lm0_ht2hadVSkinMetSig)
#
#lm0_low_ht2had          = variable(":ht2;H_{T2}^{had.} (GeV);Number of Events / 16 GeV",[50,0,500], commoncf+"&&ht2>0")
#lm0_low_ht2had.sample   = getSignal(0)
#lm0_low_ht2had.color    = dataColor
#lm0_low_ht2had.legendText="Data"
#lm0_low_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",[52,0,27], commoncf )
#lm0_low_kinMetSig.sample   = getSignal(0)
#lm0_low_kinMetSig.color    = dataColor
#lm0_low_kinMetSig.legendText="Data"
#lm0_low_ht2hadVSkinMetSig = variable2D(lm0_low_ht2had,lm0_low_kinMetSig)
#allVars.append(lm0_low_ht2hadVSkinMetSig)
#
#
#lm1_ht2had          = variable(":ht2;H_{T2}^{had.} (GeV);Number of Events / 5 GeV",binningHT, commoncf+"&&ht2>0")
#lm1_ht2had.sample   = getSignal(1)
#lm1_ht2had.color    = dataColor
#lm1_ht2had.legendText="Data"
#lm1_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",binningkMs, commoncf )
#lm1_kinMetSig.sample   = getSignal(1)
#lm1_kinMetSig.color    = dataColor
#lm1_kinMetSig.legendText="Data"
#lm1_ht2hadVSkinMetSig = variable2D(lm1_ht2had,lm1_kinMetSig)
#allVars.append(lm1_ht2hadVSkinMetSig)
#
#lm1_low_ht2had          = variable(":ht2;H_{T2}^{had.} (GeV);Number of Events / 16 GeV",[50,0,500], commoncf+"&&ht2>0")
#lm1_low_ht2had.sample   = getSignal(1)
#lm1_low_ht2had.color    = dataColor
#lm1_low_ht2had.legendText="Data"
#lm1_low_kinMetSig          = variable(":kinMetSig;S_{MET} ( #sqrt{GeV} );Number of Events",[52,0,27], commoncf )
#lm1_low_kinMetSig.sample   = getSignal(1)
#lm1_low_kinMetSig.color    = dataColor
#lm1_low_kinMetSig.legendText="Data"
#lm1_low_ht2hadVSkinMetSig = variable2D(lm1_low_ht2had,lm1_low_kinMetSig)
#allVars.append(lm1_low_ht2hadVSkinMetSig)


for sample in allSamples:
  sample["Chain"] = chainstring

for var in allVars:
  var.logy=True
  var.lines = [[0.17,0.963,'#sqrt{s} = 7TeV'], [0.36,0.963,"#font[22]{CMS simulation}"], [0.69, 0.963, str(int(round(targetLumi)))+" pb^{-1}"]]
#  var.lines = [[0.17,0.963,'#sqrt{s} = 7TeV'], [0.36,0.963,"#font[22]{CMS simulation 2010}"], [0.80, 0.963, "L = "+str(targetLumi)+" pb^{-1}"]]

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
ROOT.gROOT.ProcessLine(".L ../scripts/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)

for var in allVars:
  var.data_histo.GetYaxis().SetLabelSize(0.04)
  var.data_histo.GetXaxis().SetLabelSize(0.04)
  var.data_histo.GetZaxis().SetRangeUser(10**(-3.9), .9)
  var.lines = [[0.17,0.963,'#sqrt{s} = 7TeV'], [0.36,0.963,"#font[22]{CMS simulation}"], [0.69, 0.963, str(int(round(targetLumi)))+" pb^{-1}"], [0.4, 0.27, 'A', 0.07], [0.7, 0.27, 'B', 0.07], [0.4, 0.80, 'C', 0.07], [0.7, 0.80, 'D', 0.07]]

data_htVSkinMetSig.data_histo.GetZaxis().SetRangeUser(10**(-2), 9)
#data_htVSkinMetSig.data_histo.GetZaxis().SetRangeUser(10**(-2), 9)

#data_htVSkinMetSig.lines = [[0.17,0.963,'#sqrt{s} = 7TeV'], [0.36,0.963,"#font[22]{CMS preliminary}"], [0.69, 0.963, str(int(round(targetLumi)))+" pb^{-1}"]]
#mc_htVSkinMetSig.lines = [[0.17,0.963,'#sqrt{s} = 7TeV'], [0.36,0.963,"#font[22]{CMS simulation}"], [0.69, 0.963, str(int(round(targetLumi)))+" pb^{-1}"], [0.4, 0.27, 'A', 0.07], [0.7, 0.27, 'B', 0.07], [0.4, 0.7, 'C', 0.07], [0.7, 0.7, 'D', 0.07]]

#draw2D(mc_htVSkinMetSig,           subdir+prefix+"mc_htVSkinMetSig")
draw2D(data_htVSkinMetSig,         subdir+prefix+"Ele_data_htVSkinMetSig" ,  True, [[300,650,650],[2.5,5.5,5.5]])
draw2D(mc_htVSkinMetSig,           subdir+prefix+"Ele_mc_htVSkinMetSig",     True, [[300,650,650],[2.5,5.5,5.5]])
draw2D(ttbar_htVSkinMetSig,        subdir+prefix+"Ele_ttbar_htVSkinMetSig" , True, [[300,650,650],[2.5,5.5,5.5]])
draw2D(wjets_htVSkinMetSig,        subdir+prefix+"Ele_wjets_htVSkinMetSig" , True, [[300,650,650],[2.5,5.5,5.5]])
draw2D(lm0_htVSkinMetSig,          subdir+prefix+"Ele_lm0_htVSkinMetSig"   , True, [[300,650,650],[2.5,5.5,5.5]])
draw2D(lm1_htVSkinMetSig,          subdir+prefix+"Ele_lm1_htVSkinMetSig"   , True, [[300,650,650],[2.5,5.5,5.5]])

