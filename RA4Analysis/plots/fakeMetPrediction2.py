import ROOT
from array import array
from math import *
import os, copy, random
from Workspace.RA4Analysis.simplePlotsCommon import *
import xsec, types, sys
from funcs import *
small = False
maxNJet = 8
allStacks = []
#mode = "Ele"
mode = "Mu"
bjetbin = "b2"

print sys.argv

if len(sys.argv)>1:
  mode = sys.argv[1]
if len(sys.argv)>2:
  bjetbin = sys.argv[2]

print "mode",mode,"bjetbin",bjetbin

runRangeMin = 190456
runRangeMax = 196531

if mode == "Mu":
  from defaultMu2012Samples import *
if mode == "Ele":
  from defaultEle2012Samples import *

from defaultHad2012Samples import *
haddata = HTdata
haddata["hasWeight"] = "False"


bjetbins = {"inc":"(1)", \
            "b0":"(!(btag0>0.679))",
            "b1":"(btag0>0.679&&(!(btag1>0.679)))",
            "b1p":"(btag0>0.679)",
            "b2":"(btag1>0.679)"
            }

#for sample in allSamples:
#  if sample["name"].count("HT")==0:
#    sample["hasWeight"] = True
#    if mode=="Mu":
#      sample["dirname"] = "/data/schoef/convertedTuples_v6//copyInc/Mu/"
#    if mode=="Ele":
#      sample["dirname"] = "/data/schoef/convertedTuples_v6//copyInc/Ele/"

if allSamples.count(haddata)==0:
  allSamples.append(haddata)

#if allSamples.count(qcdHad)==0:
#  allSamples.append(qcdHad)
leptonCommonCF = "(-1)"
if mode == "Mu":
  leptonCommonCF = "singleMuonic&&nvetoMuons==1&&nvetoElectrons==0&&met>100&&ht>350&&"+bjetbins[bjetbin]
if mode == "Ele":
  leptonCommonCF = "singleElectronic&&nvetoMuons==0&&nvetoElectrons==1&&met>100&&ht>350&&"+bjetbins[bjetbin]

hadronicCommonCF = "nvetoMuons==0&&nvetoElectrons==0&&"+bjetbins[bjetbin]
  
subdir = "pngFake2012/"
minimum = 10**(-2.5)

prefix = "HTData_"+mode+"_"+bjetbin
if small:
  prefix+="small_"

htvals = [\
    [350,400,   "HLTHT300"],
    [400,450,   "HLTHT300"],
    [450,500,   "HLTHT350"],
    [500,550,   "HLTHT400"],
    [550,600,   "HLTHT450"],
    [600,650,   "HLTHT500"],
    [650,700,   "HLTHT550"],
    [700,750,   "HLTHT550"],
    [750,800,   "HLTHT650"],
    [800,1000,  "HLTHT650"],
    [1000,1200, "HLTHT750"],
    [1200,1500, "HLTHT750"],
    [1500,2500, "HLTHT750"]
  ]

alltriggers =  [val[2] for val in htvals]

#Construct njet-reweighting Histos to be used for reweighting
def getNJStack(dataCutString, varname = "njets"):
  binning = [20,0,20]
  DATA          = variable(varname, binning, dataCutString)
  DATA.sample   = data
  DATA.color    = dataColor
  DATA.legendText="Data"
  res = [DATA]
  getLinesForStack(res, targetLumi)
  return res


filename = "/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/"+prefix+"data-njet-shapes.root"
nj_stacks = {}
if not os.path.exists(filename):
  print "Constructing njet histos"
  for htval in htvals:
    nj_stacks[str(htval[0])] =  getNJStack( addCutString(leptonCommonCF, getHTBinCutString(htval)) , "njets")
    allStacks.append(nj_stacks[str(htval[0])]) 
  reweightingHistoFile = ""
  execfile("simplePlotsLoopKernel.py")
  for htval in htvals:
    htmp=nj_stacks[str(htval[0])][0].data_histo.Clone()
    integr = htmp.Integral()
    if integr>0:
      htmp.Scale(1./integr)
    else:
      print "DATA is 0"
  tf = ROOT.TFile(filename, "recreate")
  tf.cd()
  for htval in htvals:
    nj_stacks[str(htval[0])][0].data_histo.SetName("njets_ht_"+str(htval[0]))
    nj_stacks[str(htval[0])][0].data_histo.Write()
  tf.Close()
  print "Written njet reweighting histos to", filename
else:
  print "Reading", filename
  rf = ROOT.TFile(filename)
  for htval in htvals:
    rf.cd()
    htmp = rf.Get("njets_ht_"+str(htval[0]))
    ROOT.gDirectory.cd("PyROOT:/")
    nj_stacks[str(htval[0])] = [htmp.Clone("njets_ht_"+str(htval[0])+"_clone")]
    nj_stacks[str(htval[0])][0].SetName("njets_ht_"+str(htval[0]))
    print "Read",nj_stacks[str(htval[0])][0],"from",filename
  rf.Close()

c = ROOT.TChain("Events")
c1 = ROOT.TCanvas()
stuff=[]
for bin in HTdata["bins"]:
  if small:
    c.Add(HTdata["dirname"]+"/"+bin+"/histo_10_*.root")
  else:
    c.Add(HTdata["dirname"]+"/"+bin+"/histo_*.root")
for trigger in alltriggers:
    ofile = "/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/runYield_"+trigger+".root"
    if os.path.isfile(ofile):
      print "found",ofile,"-> skipping ",trigger
      continue
    print "yield per run for ",trigger
    c.Draw("run>>hrunTMP("+str(runRangeMin)+"-"+str(runRangeMax)+", "+str(runRangeMin)+", "+str(runRangeMax)+")",trigger+">0&&"+trigger.replace("HLT","pre")+">0")
    print trigger+">0&&"+trigger.replace("HLT","pre")+">0"
    hrun = ROOT.gDirectory.Get("hrunTMP").Clone()
    stuff.append(hrun)
    c.Draw("run>>hrunPresTMP("+str(runRangeMin)+"-"+str(runRangeMax)+", "+str(runRangeMin)+", "+str(runRangeMax)+")","("+trigger+">0&&"+trigger.replace("HLT","pre")+">0)*"+trigger.replace("HLT","pre"))
    print "("+trigger+">0&&"+trigger.replace("HLT","pre")+">0)*"+trigger.replace("HLT","pre")
    hrunPres = ROOT.gDirectory.Get("hrunPresTMP").Clone()
    stuff.append(hrunPres)
    hrunPres.SetMinimum(0.7)
    hrunPres.SetMaximum(1.2*10**8)
    ym = hrunPres.GetMaximum()
    hrunPres.SetMaximum(1.5*ym)
    
    hrunPres.SetLineColor(ROOT.kBlue)
    hrunPres.GetXaxis().SetLabelSize(0.02)
    hrunPres.Draw()
    ROOT.gPad.SetLogy()
    
    hrun.Draw("same")
    for x in [163869,170000,172619,175800]:
      t = ROOT.TLine(x, hrunPres.GetYaxis().GetXmin(), x, ym)
      t.SetLineStyle(2)
      stuff.append(t)
      t.Draw()
#    tl = ROOT.TLatex()
#    l=[]
#    for m in [["May10", 0.21, 0.9],["Prompt-v4", 0.37, 0.9],["Aug5", 0.58, 0.9],["Prompt-v6", 0.68, 0.9],["2011B", 0.85, 0.9]]:
#      tl.SetNDC();
#      tl.SetTextSize(0.025);
#      tl.SetTextAlign(11); # align right
#      l.append(tl.DrawLatex(m[1],m[2],m[0]));
#    for t in l:
#      t.Draw()
#      stuff.append(t)
#    del tl
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/runYield_"+trigger+".png")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/runYield_"+trigger+".root")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/runYield_"+trigger+".pdf")
del c1

template_nj={}
met_shapes={}
fullrootfilename = "/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/"+prefix+"_templates.root"
if not os.path.isfile(  fullrootfilename ):
  print "Constructing templates"
  for htval in htvals:
    trigger = htval[2]
    template_nj[htval[0]] = {}
    for nj in range(2,maxNJet):
      precut = addCutString("jet1pt>40&&"+hadronicCommonCF+"&&njets=="+str(nj), getHTBinCutString(htval))
      cut = "("+precut+"&&"+trigger+">0&&"+trigger.replace("HLT","pre")+">0)*"+trigger.replace("HLT","pre")
      print "At", cut
      htmp = ROOT.TH1F("hnjTMP", "hnjTMP", 50,0,1000)
      htmp.Sumw2()
      c.Draw("met>>hnjTMP", cut)
      template_nj[htval[0]][nj] = htmp.Clone()
      integr = template_nj[htval[0]][nj].Integral()
      if integr>0:
        template_nj[htval[0]][nj].Scale(1./integr)
      template_nj[htval[0]][nj].SetName("met_shape_ht_"+str(htval[0])+"_"+str(htval[1])+"_njet_"+str(nj))
      del htmp
  for htval in htvals:
    hres = template_nj[htvals[0][0]][3].Clone()
    hres.Reset()
    nj = nj_stacks[str(htval[0])][0]
    if not type(nj)==type(ROOT.TH1F()):
      nj = nj.data_histo
    for i in range(3, maxNJet):
      njetweight = nj.GetBinContent(nj.FindBin(i))
      htmp = template_nj[htval[0]][i].Clone()
      htmp.Scale(njetweight)
      hres.Add(htmp)
    integr = hres.Integral()
    if integr>0:
      hres.Scale(1./integr)
    met_shapes[htval[0]] = hres.Clone()
    met_shapes[htval[0]].SetName("met_shape_ht_"+str(htval[0])+"_"+str(htval[1]))
  print "(Over-)writing ROOT file",fullrootfilename
  tf = ROOT.TFile(fullrootfilename, "RECREATE")
  tf.cd()
  for htval in htvals:
    met_shapes[htval[0]].Write()
    if not type(nj_stacks[str(htval[0])][0])==type(ROOT.TH1F()):
      nj_stacks[str(htval[0])][0].data_histo.Write()
    else:
      nj_stacks[str(htval[0])][0].Write()
    for nj in template_nj[htval[0]].keys():
      template_nj[htval[0]][nj].Write()
  tf.Close()
  print "Written", fullrootfilename
else:
  print "Reading", fullrootfilename
  rf = ROOT.TFile(fullrootfilename)
  for htval in htvals:
    rf.cd()
    name = "met_shape_ht_"+str(htval[0])+"_"+str(htval[1])
    htmp = rf.Get(name)
    ROOT.gDirectory.cd("PyROOT:/")
    met_shapes[htval[0]] = htmp.Clone(name)
    print "Read",met_shapes[htval[0]],"=",name,"from",fullrootfilename
  rf.Close()
  

##################### Comparison of MC 1l-fake MET with Had MET, Constructing templates
allStacks = []
def getStack(binning, leptonicVar,  leptonicCutString, lepFunc = ""):

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
  MC_TTJETS.style              = "f0"
  MC_TTJETS.color              = ROOT.kRed - 3
  MC_ZJETS.legendText          = "DY + Jets"
  MC_ZJETS.style               = "f0"
  MC_ZJETS.add                 = [MC_TTJETS]
  MC_ZJETS.color               = ROOT.kGreen + 3
  MC_STOP.legendText          = "single Top"
  MC_STOP.style               = "f0"
  MC_STOP.add                 = [MC_ZJETS]
  MC_STOP.color               = ROOT.kOrange + 4
  MC_QCD.color                 = myBlue
  MC_QCD.legendText            = "QCD"
  MC_QCD.style                 = "f0"
  MC_QCD.add                   = [MC_STOP]
  MC_WJETS.legendText          = "W + Jets"
  MC_WJETS.style               = "f0"
  MC_WJETS.add                 = [MC_QCD]
  MC_WJETS.color               = ROOT.kYellow
  res=[]
  if True:
    res = [MC_TTJETS, MC_WJETS, MC_QCD, MC_STOP, MC_ZJETS]
    MC_TTJETS.add=[MC_WJETS]
    MC_ZJETS.add=[]

  res[0].style = "f"

  getLinesForStack(res, targetLumi)
  return res

fakemet_stacks={}
for htval in htvals:
  binning = [50,0,1000]
#  leptonicVar = ":sqrt((metpxUncorr-genmetpx)**2+(metpyUncorr-genmetpy)**2);fake-#slash{E}_{T} (GeV);Number of Events / 10 GeV" 
  leptonicVar = ":xxx;fake-#slash{E}_{T} (GeV);Number of Events / 10 GeV" 
  fakemet_stacks[str(htval[0])] = getStack(binning, leptonicVar, addCutString("jet2pt>40&&"+leptonCommonCF, getHTBinCutString(htval)), fakeMet)
  allStacks.append(fakemet_stacks[str(htval[0])])

#  fakemet_nj_stacks[str(htval[0])]={}
#  for nj in [2,3,4,5]:
#    fakemet_nj_stacks[str(htval[0])][str(nj)] = getStack(binning, leptonicVar, hadronicVar, \
#      addCutString("njets=="+str(nj), addCutString(leptonCommonCF, getHTBinCutString(htval))),
#      addCutString("njets=="+str(nj), addCutString(hadronicCommonCF, addCutString(htval[2], getHTBinCutString(htval)))),
#      fakeMet )
#    allStacks.append(fakemet_nj_stacks[str(htval[0])][str(nj)])
reweightingHistoFile = "reweightingHisto_Summer2012Private.root"
execfile("simplePlotsLoopKernel.py")
for kstacks in fakemet_stacks.keys():
  var = variable(":xx;fake-#slash{E}_{T} (GeV);Number of Events / 20 GeV", [50,0,1000], "")
  var.color    = dataColor
  var.data_histo    =  met_shapes[int(kstacks)]
  var.legendText="Prediction"
  fakemet_stacks[kstacks].append(var)

for stack in allStacks:
    stack[-1].normalizeTo = stack[0]

for stack in allStacks:
  stack[0].maximum = 30.*stack[0].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].minimum = 10**(-.5)
  stack[0].logx = True
  stack[0].legendCoordinates=[0.7,0.95 - 0.05*5,.98,.95]
  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]

#htstack[0].logx = False
#htstack[0].maximum = 30000000.*stack[0].data_histo.GetMaximum()
#htstack[0].data_histo.GetXaxis().SetLabelSize(0.03)
#drawNMStacks(1,1,[htstack], subdir+"/"+prefix+"all_ht", False)
#
for htval in htvals:
  drawNMStacks(1,1,[fakemet_stacks[str(htval[0])]], subdir+"/"+prefix+"fakemet_ht_"+str(htval[0])+"_"+str(htval[1]), False)

