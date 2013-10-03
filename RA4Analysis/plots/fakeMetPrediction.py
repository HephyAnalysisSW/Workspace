import ROOT
from array import array
from math import *
import os, copy, random
from simplePlotsCommon import *
import xsec, types
from funcs import *
small = False

allStacks = []

from defaultMuSamples import *

from defaultHadSamples import *
haddata = HTdata
#haddata["bins"] =['Run2011A-May10ReReco'] 

#for sample in allSamples:
#  sample["dirname"] = "/data/schoef/convertedTuples_v5//copy/Mu/"
#  sample["hasWeight"] = True

if allSamples.count(haddata)==0:
  allSamples.append(haddata)

#if allSamples.count(qcdHad)==0:
#  allSamples.append(qcdHad)

leptonCommonCF = "singleMuonic&&nvetoMuons==1&&nvetoElectrons==0&&barepfmet>60&&ht>350"
hadronicCommonCF = "nvetoMuons==0&&nvetoElectrons==0"
subdir = "pngFake/Step100"
minimum = 10**(-2.5)
prefix = "HTData"


#hadronicCommonCF += "&&run==166699&&lumiblock==902&&event==946140738"

#htvals = [\
#    [300,500,   "(HLTHT160>0||HLTHT240>0)"],
#    [500,700,   "(HLTHT240||HLTHT260||HLTHT300||HLTHT350||HLTHT360||HLTHT400)"],
#    [700,900,   "(HLTHT240||HLTHT260||HLTHT300||HLTHT350||HLTHT360||HLTHT400||HLTHT450||HLTHT500)"],
#    [900,1100,  "(HLTHT240||HLTHT260||HLTHT300||HLTHT350||HLTHT360||HLTHT400||HLTHT450||HLTHT500||HLTHT550)"],
#    [1100,-1,   "(HLTHT240||HLTHT260||HLTHT300||HLTHT350||HLTHT360||HLTHT400||HLTHT450||HLTHT500||HLTHT550)"]
#  ]

htvals = [\
    [350,400,   "(HLTHT160>0||HLTHT240>0)"],
    [400,500,   "(HLTHT160||HLTHT240||HLTHT260)"],
    [500,600,   "(HLTHT240||HLTHT260||HLTHT300||HLTHT350||HLTHT360||HLTHT400)"],
    [600,700,   "(HLTHT240||HLTHT260||HLTHT300||HLTHT350||HLTHT360||HLTHT400||HLTHT450)"],
    [700,800,   "(HLTHT240||HLTHT260||HLTHT300||HLTHT350||HLTHT360||HLTHT400||HLTHT450||HLTHT500)"],
    [800,900,   "(HLTHT240||HLTHT260||HLTHT300||HLTHT350||HLTHT360||HLTHT400||HLTHT450||HLTHT500||HLTHT550||HLTHT600||HLTHT650)"],
    [900,1000,  "(HLTHT240||HLTHT260||HLTHT300||HLTHT350||HLTHT360||HLTHT400||HLTHT450||HLTHT500||HLTHT550||HLTHT600||HLTHT650)"],
    [1000,1100, "(HLTHT240||HLTHT260||HLTHT300||HLTHT350||HLTHT360||HLTHT400||HLTHT450||HLTHT500||HLTHT550||HLTHT600||HLTHT650||HLTHT700||HLTHT750)"],
    [1100,1200, "(HLTHT240||HLTHT260||HLTHT300||HLTHT350||HLTHT360||HLTHT400||HLTHT450||HLTHT500||HLTHT550||HLTHT600||HLTHT650||HLTHT700||HLTHT750)"],
    [1200,1300, "(HLTHT240||HLTHT260||HLTHT300||HLTHT350||HLTHT360||HLTHT400||HLTHT450||HLTHT500||HLTHT550||HLTHT600||HLTHT650||HLTHT700||HLTHT750)"],
    [1300,1400, "(HLTHT240||HLTHT260||HLTHT300||HLTHT350||HLTHT360||HLTHT400||HLTHT450||HLTHT500||HLTHT550||HLTHT600||HLTHT650||HLTHT700||HLTHT750)"],
    [1400,1500, "(HLTHT240||HLTHT260||HLTHT300||HLTHT350||HLTHT360||HLTHT400||HLTHT450||HLTHT500||HLTHT550||HLTHT600||HLTHT650||HLTHT700||HLTHT750)"],
    [1500,-1,   "(HLTHT240||HLTHT260||HLTHT300||HLTHT350||HLTHT360||HLTHT400||HLTHT450||HLTHT500||HLTHT550||HLTHT600||HLTHT650||HLTHT700||HLTHT750)"]
  ]
alltriggers =  [  "HLTHT240", "HLTHT260", "HLTHT300", "HLTHT350", "HLTHT360", "HLTHT400", "HLTHT450", "HLTHT500", "HLTHT550", "HLTHT600", "HLTHT650", "HLTHT700", "HLTHT750"]

def getHTLowerEdge(ht):
  for htval in reversed(htvals):
    if ht>=htval[0]:
      return htval[0]
  return -1

#Construct njet-reweighting Histos to be used for reweighting
def getNJStack(qcdCutString, dataCutString):
  binning = [20,0,20]
  QCD_DATA          = variable("njets", binning, qcdCutString)
  QCD_DATA.sample   = haddata
  QCD_DATA.color    = myBlue
  QCD_DATA.legendText="QCD Data"
  DATA          = variable("njets", binning, dataCutString)
  DATA.sample   = data
  DATA.color    = dataColor
  DATA.legendText="Data"
  res = [DATA, QCD_DATA]
  getLinesForStack(res, targetLumi)
  return res


njetsReweightStacks={}
filename = "/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/"+prefix+"njet_reweighting_shapes.root"
if not os.path.exists(filename):
  print "Constructing njet reweighting histos"
  nj_stacks = {}
  for htval in htvals:
    nj_stacks[str(htval[0])] =  getNJStack(\
        addCutString(hadronicCommonCF, addCutString(htval[2], getHTBinCutString(htval))), 
        addCutString(leptonCommonCF, getHTBinCutString(htval))
        )
    allStacks.append(nj_stacks[str(htval[0])]) 
  execfile("simplePlotsKernel.py")
  for htval in htvals:
    htmp=nj_stacks[str(htval[0])][0].data_histo.Clone()
    integr = htmp.Integral()
    if integr>0:
      htmp.Scale(1./integr)
    else:
      print "DATA is 0"
    htmp2 = nj_stacks[str(htval[0])][1].data_histo.Clone() 
    integr = htmp2.Integral()
    if integr>0:
      htmp2.Scale(1./integr)
    else:
      print "QCD is 0"
    htmp.Divide(htmp2)
    njetsReweightStacks[str(htval[0])] = htmp.Clone()
    del htmp
    del htmp2
  tf = ROOT.TFile(filename, "recreate")
  tf.cd()
  for htval in htvals:
    njetsReweightStacks[str(htval[0])].SetName("njets_ht_"+str(htval[0]))
    njetsReweightStacks[str(htval[0])].Write()
  tf.Close()
  print "Written njet reweighting histos to", filename
else:
  rf = ROOT.TFile(filename)
  for htval in htvals:
    rf.cd()
    htmp = rf.Get("njets_ht_"+str(htval[0]))
    print htmp
    ROOT.gDirectory.cd("PyROOT:/")
    print htmp
    njetsReweightStacks[str(htval[0])] = htmp.Clone("njets_ht_"+str(htval[0])+"_clone")
    print htmp
    print "Read",njetsReweightStacks[str(htval[0])],"from",filename
  rf.Close()

#njet&prescale reweighting functor

def findHighestTrigger(c):
  for trigger in reversed(alltriggers):
    tres = getValue(c, trigger)
    if tres==1:
      return trigger
  return "None" 

def getPrescaleVal(c):
#  for trigger in reversed(alltriggers):
#    print "getPrescaleVal:",trigger,c.GetLeaf(trigger).GetValue(),"pre",c.GetLeaf(trigger.replace("HLT", "pre")).GetValue()
  trig = findHighestTrigger(c)
  if trig!="None":
#   print "Found ",trig,"with ",c.GetLeaf(trig).GetValue(),"pre:", c.GetLeaf(trig.replace("HLT", "pre")).GetValue()
    return getValue(c, trig.replace("HLT", "pre"))
  return float('nan')

def njetPrescaleReweightFactor(c): 
  htval =  getHTLowerEdge(getValue(c, "ht"))
  njetReweightingHist = njetsReweightStacks[str(htval)]
  njets = getValue(c, "njets")
  reweightFac = njetReweightingHist.GetBinContent(njetReweightingHist.FindBin(njets))
  prescaleVal = getPrescaleVal(c)
#  print "reweightFactor: ht",c.GetLeaf("ht").GetValue(),"->",htval,", njet ",njets,"->",reweightFac
#  print "Result: prescale = ",prescaleVal,"run", c.GetLeaf("run").GetValue(), "lumi", c.GetLeaf("lumiblock").GetValue(), "event", c.GetLeaf("event").GetValue()
  return reweightFac*prescaleVal

def htOfTriggerFunctor(trigger):
  def getHT(c):
    if findHighestTrigger(c)==trigger:
      return getValue(c, "ht")
    else:
      return float('nan')
  return getHT

#a nice HT stack with the different triggers ... The Functor returns a function which returns NAN if the trigger is different from the highest HT Trigger
allStacks = []
allHT          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV", [100,0,2000], "-1")
allHT.sample   = {"name":"None"} 
allHT.color    = dataColor
allHT.legendText = "Sum" 
allHT.style = "l02"
htstack = [allHT]
for ntrigger in range(len(alltriggers)):
  trigger = alltriggers[ntrigger]
  DATA          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV", [100,0,2000], "ht>0", False, htOfTriggerFunctor(trigger))
  DATA.reweightVar = getPrescaleVal 
  DATA.sample   = haddata
#  DATA.color    = ROOT.kGray
  DATA.color    = ROOT_colors[ntrigger%(len(ROOT_colors)-1)+1]
  DATA.legendText = trigger
  DATA.add = []
  DATA.style = "l0"
  htstack[0].add.append(DATA)
  htstack.append(DATA)

allStacks.append(htstack)

##################### Comparison of MC 1l-fake MET with Had MET, Constructing templates

def getStack(binning, leptonicVar, hadronicVar, leptonicCutString, hadronicCutString, lepFunc = ""):
  DATA          = variable(hadronicVar, binning, hadronicCutString)
  DATA.sample   = haddata
#  DATA.color    = ROOT.kGray
  DATA.color    = dataColor
  DATA.legendText="Data"

  MC_QCD = ""
  if type(lepFunc) == types.FunctionType:
    MC_QCD                       = variable(leptonicVar, binning, leptonicCutString, False, lepFunc)
  else:
    MC_QCD                       = variable(leptonicVar, binning, leptonicCutString)
  MC_QCD.minimum               = 10**(-1)

  MC_TTJETS                    = copy.deepcopy(MC_QCD)
  MC_WJETS                     = copy.deepcopy(MC_QCD)
  MC_ZJETS                     = copy.deepcopy(MC_QCD)
  MC_STOP                      = copy.deepcopy(MC_QCD)

  MC_QCD.minimum               = 5*10**(-1)
  MC_QCD.sample                = copy.deepcopy(mc)
  MC_QCD.sample["bins"]        = QCD_Bins
  MC_TTJETS                    = copy.deepcopy(MC_QCD)
  MC_TTJETS.sample             = copy.deepcopy(mc)
  MC_TTJETS.sample["bins"]     = ["TTJets"]
  MC_ZJETS                     = copy.deepcopy(MC_QCD)
  MC_ZJETS.sample              = copy.deepcopy(mc)
  MC_ZJETS.sample["bins"]      = ZJets_Bins

  MC_WJETS                     = copy.deepcopy(MC_QCD)
  MC_WJETS.sample              = copy.deepcopy(mc)
  MC_WJETS.sample["bins"]      = WJets_Bins
  MC_STOP                     = copy.deepcopy(MC_QCD)
  MC_STOP.sample              = copy.deepcopy(mc)
  MC_STOP.sample["bins"]      = singleTop_Bins

  MC_TTJETS.legendText         = "t#bar{t} + Jets"
  MC_TTJETS.style              = "f"
  MC_TTJETS.color              = ROOT.kRed - 3
  MC_WJETS.legendText          = "W + Jets"
  MC_WJETS.style               = "f"
  MC_WJETS.add                 = [MC_TTJETS]
  MC_WJETS.color               = ROOT.kYellow
  MC_STOP.legendText          = "single Top"
  MC_STOP.style               = "f"
  MC_STOP.add                 = [MC_WJETS]
  MC_STOP.color               = ROOT.kOrange + 4
  MC_QCD.color                 = myBlue
  MC_QCD.legendText            = "QCD"
  MC_QCD.style                 = "f"
  MC_QCD.add                   = [MC_STOP]
  MC_ZJETS.legendText          = "DY + Jets"
  MC_ZJETS.style               = "f"
  MC_ZJETS.add                 = [MC_QCD]
  MC_ZJETS.color               = ROOT.kGreen + 3

  res = [MC_ZJETS, MC_QCD, MC_STOP, MC_WJETS, MC_TTJETS]
  getLinesForStack(res, targetLumi)
  res = []
  nhistos = len(res)
  res.append(DATA)
  return res


fakemet_stacks={}
fakemet_nj_stacks={}
#ht_stacks={}
for htval in htvals:
  binning = [100,0,1000]
  leptonicVar = ":sqrt((metpxUncorr-genmetpx)**2+(metpyUncorr-genmetpy)**2);fake-#slash{E}_{T} (GeV);Number of Events / 10 GeV" #FIXME
  leptonicVar = ":sqrt((metpxUncorr)**2+(metpyUncorr)**2);fake-#slash{E}_{T} (GeV);Number of Events / 10 GeV"
  hadronicVar = ":barepfmet;fake-#slash{E}_{T} (GeV);Number of Events / 10 GeV"
  fakemet_stacks[str(htval[0])] = getStack(binning, leptonicVar, hadronicVar, \
    addCutString("jet2pt>40&&"+leptonCommonCF, getHTBinCutString(htval)), 
    addCutString("jet2pt>40&&"+hadronicCommonCF, addCutString(htval[2], getHTBinCutString(htval))), fakeMet )#FIXME

  fakemet_stacks[str(htval[0])][-1].reweightVar = njetPrescaleReweightFactor
#  fakemet_stacks[str(htval[0])][-1].reweightVar = "njets"
#  fakemet_stacks[str(htval[0])][-1].reweightHisto = njetsReweightStacks[str(htval[0])]
  allStacks.append(fakemet_stacks[str(htval[0])])
  fakemet_nj_stacks[str(htval[0])]={}
  for nj in [2,3,4,5]:
    fakemet_nj_stacks[str(htval[0])][str(nj)] = getStack(binning, leptonicVar, hadronicVar, \
      addCutString("njets=="+str(nj), addCutString(leptonCommonCF, getHTBinCutString(htval))), 
      addCutString("njets=="+str(nj), addCutString(hadronicCommonCF, addCutString(htval[2], getHTBinCutString(htval)))),
      fakeMet )
    allStacks.append(fakemet_nj_stacks[str(htval[0])][str(nj)])
    
for stack in allStacks:
  stack[0].minimum = minimum

#reweightingHistoFile = "reweightingHisto_Summer2011.root" #FIXME
reweightingHistoFile = ""
execfile("simplePlotsLoopKernel.py")
for stack in allStacks:
  for var in stack[:-1]:
    var.normalizeTo = stack[-1]
    var.normalizeWhat = stack[0]
  stack[-1].normalizeTo=""
  stack[-1].normalizeWhat=""
for var in htstack:
  var.normalizeTo = ""
  var.normalizeWhat = ""

for stack in allStacks:
  stack[0].maximum = 30.*stack[0].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].minimum = 10**(-.5)
  stack[0].logx = True
  stack[0].legendCoordinates=[0.7,0.95 - 0.05*5,.98,.95]
  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]

htstack[0].logx = False
htstack[0].maximum = 30000000.*stack[0].data_histo.GetMaximum()
htstack[0].data_histo.GetXaxis().SetLabelSize(0.03)
drawNMStacks(1,1,[htstack], subdir+"/"+prefix+"all_ht", False)

for htval in htvals:
  drawNMStacks(1,1,[fakemet_stacks[str(htval[0])]], subdir+"/"+prefix+"fakemet_ht_"+str(htval[0])+"_"+str(htval[1]), False)
  for nj in [2,3,4,5]:
    drawNMStacks(1,1,[fakemet_nj_stacks[str(htval[0])][str(nj)]], subdir+"/"+prefix+"fakemet_ht_"+str(htval[0])+"_"+str(htval[1])+"_nj"+str(nj), False)
nj_stacks={}
nj_colors = [ROOT.kBlack, myBlue,ROOT.kRed - 3, ROOT.kGreen + 3, ROOT.kOrange + 4]
for htval in htvals:
  inclusive = copy.deepcopy(fakemet_stacks[str(htval[0])][-1])
  inclusive.data_histo = fakemet_stacks[str(htval[0])][-1].data_histo.Clone()
  inclusive.legendText = "inclusive"
  inclusive.color = ROOT.kBlack
  inclusive.style = "l02" 
  nj_stacks[str(htval[0])] = []
  for nj in [2,3,4,5]:
    var = copy.deepcopy(fakemet_nj_stacks[str(htval[0])][str(nj)][-1])
    var.data_histo = fakemet_nj_stacks[str(htval[0])][str(nj)][-1].data_histo.Clone()
    var.legendText = str(nj)+" Jets"
    var.color = nj_colors[nj-2]  
    nj_stacks[str(htval[0])].append(var)
  nj_stacks[str(htval[0])] .append(inclusive)
  for var in nj_stacks[str(htval[0])]:
    var.logx = True
    var.lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]
    var.maximum = 10
    var.minimum = 10**(-4.9)
    var.legendCoordinates=[0.76,0.95 - 0.05*6,.98,.95]
    integr = var.data_histo.Integral();
    if integr>0:
      var.data_histo.Scale(1./integr) 

for htval in htvals:
  drawNMStacks(1,1,[nj_stacks[str(htval[0])]], subdir+"/"+prefix+"fakemet_nj_ht_"+str(htval[0])+"_"+str(htval[1]), False)

#Saving templates
if not small:
  fullrootfilename = "/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/"+prefix+"_templates.root"
  print "(Over-)writing ROOT file",fullrootfilename
  tf = ROOT.TFile(fullrootfilename, "RECREATE")
  tf.cd()
  for htval in htvals:
    fakemet_stacks[str(htval[0])][-1].data_histo.SetName("met_shape_ht_"+str(htval[0])+"_"+str(htval[1]))
    fakemet_stacks[str(htval[0])][-1].data_histo.Write()
    for nj in [2,3,4,5]:
      fakemet_nj_stacks[str(htval[0])][str(nj)][-1].data_histo.SetName("met_shape_ht_"+str(htval[0])+"_"+str(htval[1])+"_nj_"+str(nj))
      fakemet_nj_stacks[str(htval[0])][str(nj)][-1].data_histo.Write()
  tf.Close()
  print "... Done!"


#def getHadStack(binning, mcVar, dataVar, mcCutString, dataCutString):
#  DATA          = variable(dataVar, binning, dataCutString)
#  DATA.sample   = haddata
##  DATA.color    = ROOT.kGray
#  DATA.color    = dataColor
#  DATA.legendText="Data"
#
#  MC_QCD                       = variable(mcVar, binning, mcCutString)
#  MC_QCD.minimum               = 5*10**(-1)
#  MC_QCD.sample                = copy.deepcopy(qcdHad)
#  MC_QCD.color                 = myBlue
#  MC_QCD.legendText            = "QCD had."
#  MC_QCD.style                 = "f"
#
#  res = [MC_QCD]
#
#  getLinesForStack(res, targetLumi)
#  res.append(DATA)
#  return res
#
#fakemet_stacks={}
#fakemet_nj_stacks={}
##ht_stacks={}
#for htval in htvals:
#  binning = [100,0,1000]
#  mcVar = ":barepfmet;fake-#slash{E}_{x} (GeV);Number of Events / 10 GeV"
#  dataVar = ":barepfmet;fake-#slash{E}_{x} (GeV);Number of Events / 10 GeV"
#  fakemet_stacks[str(htval[0])] = getHadStack(binning, mcVar, dataVar, \
#    addCutString("jet2pt>40&&"+hadronicCommonCF, getHTBinCutString(htval)), 
#    addCutString("jet2pt>40&&"+hadronicCommonCF, addCutString(htval[2], getHTBinCutString(htval)))
#    )
#  allStacks.append(fakemet_stacks[str(htval[0])])
#  fakemet_nj_stacks[str(htval[0])]={}
#  for nj in [2,3,4,5]:
#    fakemet_nj_stacks[str(htval[0])][str(nj)] = getHadStack(binning, mcVar, dataVar, \
#      addCutString("njets=="+str(nj), addCutString(hadronicCommonCF, getHTBinCutString(htval))), 
#      addCutString("njets=="+str(nj), addCutString(hadronicCommonCF, addCutString(htval[2], getHTBinCutString(htval))))
#      )
#    allStacks.append(fakemet_nj_stacks[str(htval[0])][str(nj)])
#    
#
#for stack in allStacks:
#  stack[0].minimum = minimum
#
#reweightingHistoFile = "reweightingHisto_Summer2011.root"
#execfile("simplePlotsLoopKernel.py")
#for stack in allStacks:
#  for var in stack[:-1]:
#    var.normalizeTo = stack[-1]
#    var.normalizeWhat = stack[0]
#  stack[-1].normalizeTo=""
#  stack[-1].normalizeWhat=""
#
#for stack in allStacks:
#  stack[0].maximum = 30.*stack[0].data_histo.GetMaximum()
#  stack[0].logy = True
#  stack[0].minimum = 10**(-.5)
#  stack[0].logx = True
#  stack[0].legendCoordinates=[0.7,0.95 - 0.05*2,.98,.95]
##  stack[0].lines = [[0.61, 0.48, "#font[22]{CMS preliminary}"], [0.61,0.43,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]
#  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]
#
#for htval in htvals:
#  drawNMStacks(1,1,[fakemet_stacks[str(htval[0])]], subdir+"/"+prefix+"fakemet_VS_QCD_ht_"+str(htval[0])+"_"+str(htval[1]), False)
#  for nj in [2,3,4,5]:
#    drawNMStacks(1,1,[fakemet_nj_stacks[str(htval[0])][str(nj)]], subdir+"/"+prefix+"fakemet_VS_QCD_ht_"+str(htval[0])+"_"+str(htval[1])+"_nj"+str(nj), False)
##  drawNMStacks(1,1,[ht_stacks(str(htval[0]))], subdir+prefix+"ht_"+str(htval[0])+"_"+str(htval[1])+"_lin.png", False)
