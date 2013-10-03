import ROOT
from array import array
from math import *
import os, copy
from simpleStatTools import niceNum
from simplePlotsCommon import *
import xsec

small = False
maxEvents = -1
if small:
  maxEvents = 100
mode = "Ele"

if mode == "Mu":
  from defaultMuSamples import *
if mode == "Ele":
  from defaultEleSamples import *

presel = "pf-3j40"
subdir = "/pngBM/"
scanpath = "/scratch/schoef/pat_110924/"
chainstring = "empty"
commoncf = "(0)"
prefix="empty_"

binningHT = [300, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1500]
binningkinMetSig = [0, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
bjetbins = {"binc":"(1)", \
            "b0":"(!(btag0>1.74))",
            "b1":"(btag0>1.74&&(!(btag1>1.74)))",
            "b2":"(btag1>1.74)"
            }
bjetbinsPy = {}
for bj in bjetbins.keys():
  bjetbinsPy[bj] = bjetbins[bj].replace("&&"," and ").replace("!", " not ")

samples = {"mc":mc, \
           "data":data}
allSamples = samples.values() 

additionalCut = ""
preprefix = mode

if mode == "Mu":
  if presel == "pf-3j40":
    chainstring = "pfRA4Analyzer/Events"
    commoncf = "jet1pt>40&&jet2pt>40&&lepton_pt>20&&singleMuonic&&nvetoElectrons==0&&nvetoMuons==1"
if mode == "Ele":
  if presel == "pf-3j40":
    chainstring = "pfRA4Analyzer/Events"
    commoncf = "jet1pt>40&&jet2pt>40&&lepton_pt>20&&singleElectronic&&nvetoElectrons==1&&nvetoMuons==0"

if additionalCut != "":
  commoncf = commoncf + "&&" +  additionalCut
if preprefix != "":
  prefix = preprefix + "_"+presel
else:
  prefix = presel

allVars=[]

############################################################### HT vs. kinMetSig

htVSkinMetSig={}
for sample in samples.keys():
  htVSkinMetSig[sample]={}
  for bjb in bjetbins.keys():
    ht          = variable(":ht;H_{T} (GeV);Number of Events / 20 GeV",[77,0,1540], commoncf+"&&"+bjetbins[bjb])
    ht.sample   = samples[sample]
    ht.color    = dataColor
    ht.legendText="Data"
    kinMetSig          = variable(":barepfmet/sqrt(ht);Y_{#slash{E}_{T}} (GeV);Number of Events",[26,0,26], commoncf+"&&"+bjetbins[bjb] )
    kinMetSig.sample   = samples[sample]
    kinMetSig.color    = dataColor
    kinMetSig.legendText="Data"
    htVSkinMetSig2DVar = variable2D(kinMetSig,ht)
    allVars.append(htVSkinMetSig2DVar)
    htVSkinMetSig[sample][bjb] = htVSkinMetSig2DVar

for sample in allSamples:
  sample["Chain"] = chainstring

for var in allVars:
  var.logy=True
  var.lines = [[0.17,0.963,'#sqrt{s} = 7TeV'], [0.36,0.963,"#font[22]{CMS simulation}"], [0.69, 0.963, str(int(round(targetLumi)))+" pb^{-1}"]]
  print var.data_histo
  var.data_histo.SetBins(len(binningkinMetSig) - 1, array('d',binningkinMetSig), len(binningHT) - 1, array('d',binningHT))

res={}
resErr={}
filename = "/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/"+prefix+"_allData.py"
if not os.path.exists(filename):
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
        for thisfile in filelist:
          if os.path.isfile(subdirname+thisfile) and thisfile[-5:]==".root" and thisfile.count("histo")==1: 
            sample["filenames"][bin].append(subdirname+thisfile)
  #          c.Add(sample["dirname"]+file)
            if counter==0:
              break
            counter=counter-1
      else:
        sample["filenames"][bin] = [subdirname+"/h*.root"]
      for thisfile in sample["filenames"][bin]:
        c.Add(thisfile)
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
      for thisfile in sample["filenames"][bin]:
        c.Add(thisfile)
      c.GetEntries()
      for var in allVars:
        if var.sample["name"] == sample["name"] and var.sample["bins"].count(bin)==1:
          htmp=ROOT.TH2F("htmp","htmp",*(var.binning))
          htmp.SetBins(len(binningkinMetSig) - 1, array('d',binningkinMetSig), len(binningHT) - 1, array('d',binningHT))
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
    var.data_histo.GetZaxis().SetRangeUser(10**(-2.9), 90)
  #  var.lines = [[0.17,0.963,'#sqrt{s} = 7TeV'], [0.36,0.963,"#font[22]{CMS simulation}"]] 
  #  var.lines = [[0.17,0.963,'#sqrt{s} = 7TeV'], [0.36,0.963,"#font[22]{CMS simulation}"] ,[0.69, 0.963, str(int(round(targetLumi)))+" pb^{-1}"], [0.4, 0.27, 'A', 0.07], [0.7, 0.27, 'B', 0.07], [0.4, 0.80, 'C', 0.07], [0.7, 0.80, 'D', 0.07]]
    var.lines = [[0.17,0.963,'#sqrt{s} = 7TeV'], [0.36,0.963,"#font[22]{CMS simulation}"] ,[0.69, 0.963, str(int(round(targetLumi)))+" pb^{-1}"]]

  #store results for all samples in res (data, mc, lm...)
  for sample in samples.keys():
    res[sample]={}
    resErr[sample]={}
    for bjb in bjetbins.keys():
  #    mc_htVSkinMetSig[bjb].data_histo.Scale(data_htVSkinMetSig[bjb].data_histo.Integral()/mc_htVSkinMetSig[bjb].data_histo.Integral())
      res[sample][bjb] = {}
      resErr[sample][bjb] = {}
      var = htVSkinMetSig[sample][bjb] 
      for hbin in binningHT[:-1]:
        res[sample][bjb][hbin]={}
        resErr[sample][bjb][hbin]={}
        for mbin in binningkinMetSig[:-1]:
          res[sample][bjb][hbin][mbin] = var.data_histo.GetBinContent(var.data_histo.FindBin(mbin, hbin))
          resErr[sample][bjb][hbin][mbin] = var.data_histo.GetBinError(var.data_histo.FindBin(mbin, hbin))
  #calculate prediction
  res["pred"] = {}
  resErr["pred"] = {}
  for bjb in bjetbins.keys():
    res["pred"][bjb] = {}
    resErr["pred"][bjb] = {}
    d0 = res["data"][bjb][binningHT[0]][binningkinMetSig[0]]/res["mc"][bjb][binningHT[0]][binningkinMetSig[0]]
    d0Err = d0*sqrt(1./res["data"][bjb][binningHT[0]][binningkinMetSig[0]] + 1./res["mc"][bjb][binningHT[0]][binningkinMetSig[0]])
    for hbin in binningHT[1:-1]:
      res["pred"][bjb][hbin] = {}
      resErr["pred"][bjb][hbin] = {}
      keys = res["mc"][bjb][hbin].keys()
      keys.sort()
      g=1.
      gErr=0.  #FIXME: Too simple treatment of empty bins
      if res["mc"][bjb][hbin][keys[0]]>0 and res["data"][bjb][hbin][keys[0]]>0:
        g = res["data"][bjb][hbin][keys[0]] / res["mc"][bjb][hbin][keys[0]]
        gErr = g*sqrt(1./res["data"][bjb][hbin][keys[0]] + 1./res["mc"][bjb][hbin][keys[0]])
      for mbin in binningkinMetSig[1:-1]:
        keys = res["mc"][bjb].keys()
        keys.sort()
    #    print "Found",res["mc"][bjb][keys[0]][mbin], "in data in mbin",mbin
    #    print "Found",res["mc"][bjb][keys[0]][mbin], "in mc in mbin",mbin
        h = 1.
        hErr = 0.
        if res["mc"][bjb][keys[0]][mbin]>0 and res["data"][bjb][keys[0]][mbin]>0:    
          h = res["data"][bjb][keys[0]][mbin]/res["mc"][bjb][keys[0]][mbin]
          hErr = h*sqrt(1./res["data"][bjb][keys[0]][mbin] + 1./res["mc"][bjb][keys[0]][mbin])
        corrFac = g*h/d0**2 
        corrFacErr = corrFac*sqrt(gErr**2/g**2 + hErr**2/h**2 + 4*d0Err**2/d0**2)
        res["pred"][bjb][hbin][mbin] = corrFac*res["mc"][bjb][hbin][mbin]
        resErr["pred"][bjb][hbin][mbin] = sqrt(corrFac**2*resErr["mc"][bjb][hbin][mbin]**2 + corrFacErr**2*res["mc"][bjb][hbin][mbin]**2)

    htVSkinMetSig["mc"][bjb].lines = [[0.17,0.963,'#sqrt{s} = 7TeV'], [0.36,0.963,"#font[22]{CMS simulation}"] ,[0.69, 0.963, str(int(round(targetLumi)))+" pb^{-1}"]]
    htVSkinMetSig["data"][bjb].lines = [[0.17,0.963,'#sqrt{s} = 7TeV'], [0.36,0.963,"#font[22]{CMS simulation}"] ,[0.69, 0.963, str(int(round(targetLumi)))+" pb^{-1}"]]
    for hbin in binningHT[:-1]:
      for mbin in binningkinMetSig[:-1]:
        h = htVSkinMetSig["mc"][bjb].data_histo
        xbin = h.GetXaxis().FindBin(mbin)
        ybin = h.GetYaxis().FindBin(hbin)
        rescale = h.GetXaxis().GetBinWidth(xbin)*h.GetYaxis().GetBinWidth(ybin)
        h.SetBinContent(h.FindBin(mbin, hbin), h.GetBinContent(h.FindBin(mbin, hbin)) / rescale )
        h = htVSkinMetSig["data"][bjb].data_histo
        h.SetBinContent(h.FindBin(mbin, hbin), h.GetBinContent(h.FindBin(mbin, hbin)) / rescale )

        metpos = var.data_histo.GetXaxis().GetBinCenter(var.data_histo.GetXaxis().FindBin(mbin))
        hpos = var.data_histo.GetYaxis().GetBinCenter(var.data_histo.GetYaxis().FindBin(hbin))
        if hbin>binningHT[0] and mbin>binningkinMetSig[0]:
          htVSkinMetSig["mc"][bjb].lines.append([metpos,hpos,"#splitline{"+str(niceNum(res["mc"][bjb][hbin][mbin])).replace(" ","")+"}{("+str(niceNum(res["pred"][bjb][hbin][mbin])).replace(" ","")+")}",0.02,22,False])
#          print "Appending MC",hbin,mbin,"#splitline{"+str(niceNum(res["mc"][bjb][hbin][mbin])).replace(" ","")+"}{("+str(niceNum(res["pred"][bjb][hbin][mbin])).replace(" ","")+")}"
          htVSkinMetSig["data"][bjb].lines.append([metpos,hpos,"#splitline{"+str(niceNum(res["data"][bjb][hbin][mbin])).replace(" ","")+"}{("+str(niceNum(res["pred"][bjb][hbin][mbin])).replace(" ","")+")}",0.02,22,False])
#          print "Appending Data",hbin,mbin,"#splitline{"+str(niceNum(res["data"][bjb][hbin][mbin])).replace(" ","")+"}{("+str(niceNum(res["pred"][bjb][hbin][mbin])).replace(" ","")+")}"
        else:
          htVSkinMetSig["mc"][bjb].lines.append([metpos,hpos,  str(niceNum(res["mc"][bjb][hbin][mbin])).replace(" ",""),0.02,22,False])
#          print "Appending MC",hbin,mbin,str(niceNum(res["mc"][bjb][hbin][mbin])).replace(" ","")
          htVSkinMetSig["data"][bjb].lines.append([metpos,hpos,  str(niceNum(res["data"][bjb][hbin][mbin])).replace(" ",""),0.02,22,False])
#          print "Appending Data",hbin,mbin,str(niceNum(res["data"][bjb][hbin][mbin])).replace(" ","")

    draw2D(htVSkinMetSig["mc"][bjb],           subdir+prefix+"mc_htVSkinMetSig_"+bjb+".png"   )
    draw2D(htVSkinMetSig["data"][bjb],           subdir+prefix+"data_htVSkinMetSig_"+bjb+".png"   )

  ofile = open(filename, "w")
  ofile.write(repr(res)+"\n")
  ofile.write(repr(resErr)+"\n")
  ofile.close()
  print "Written",filename
else:
  ifile   = open(filename, "r")
  res     = eval(ifile.readline())
  resErr  = eval(ifile.readline())
  ifile.close()
  print "Read",filename

prediction = {}
predictionError = {}
data = {}

for bj in bjetbins.keys():
  prediction[bj] = {}
  predictionError[bj] = {}
  data[bj] = {}
  for lhbin in binningHT[1:-1]:
    prediction[bj][lhbin] = {}
    predictionError[bj][lhbin] = {}
    data[bj][lhbin] = {}
    for lmbin in binningkinMetSig[1:-1]:
      prediction[bj][lhbin][lmbin] = 0
      predictionError[bj][lhbin][lmbin] = 0
      data[bj][lhbin][lmbin] = 0
      for hhbin in binningHT[1:-1]:
        for hmbin in binningkinMetSig[1:-1]:
          if hmbin>=lmbin and hhbin>=lhbin:
            prediction[bj][lhbin][lmbin]+=res['pred'][bj][hhbin][hmbin]
            predictionError[bj][lhbin][lmbin]+=resErr['pred'][bj][hhbin][hmbin]**2
            data[bj][lhbin][lmbin]+=res['data'][bj][hhbin][hmbin]
      predictionError[bj][lhbin][lmbin] = ROOT.sqrt(predictionError[bj][lhbin][lmbin])
filename = "/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/"+prefix+"_res.py"
ofile = open(filename, "w")
ofile.write("commoncf = "+repr(commoncf)+"\n")
ofile.write("targetLumi = "+repr(targetLumi)+"\n")
ofile.write("prediction = "+repr(prediction)+"\n")
ofile.write("predictionError = "+repr(predictionError)+"\n")
ofile.write("data = "+repr(data)+"\n")
ofile.close()
print "Written",filename

#Calculating msugra efficiencies
binningMET = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
from msugraxsec import msugraxsec 
from msugraCount import msugraCount
filename = "/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/"+prefix+"_msugraEfficiencies.py"
efficiencykinMetSig = {}
efficiency = {}
if not os.path.exists(filename):
  c = ROOT.TChain("pfRA4Analyzer/Events")
  files = "*.root"
  if small:
    files = "histo_1_*.root"
  if mode == "Mu":
    c.Add(scanpath+"/Mu/msugra/"+files)
  if mode == "Ele":
    c.Add(scanpath+"/EG/msugra/"+files)
#  cutstring = commoncf+"&&"+bjetbins[bj]+"&&"+addCutString("ht>"+str(lhbin),"kinMetSig>"+str(lmbin))
  for bj in bjetbins.keys():
    efficiencykinMetSig[bj]={}
    efficiency[bj]={}
    for lhbin in binningHT[:-1]:
      efficiencykinMetSig[bj][lhbin]={}
      efficiency[bj][lhbin]={}
      for lmbin in binningkinMetSig[:-1]:
        efficiencykinMetSig[bj][lhbin][lmbin]={}
      for lmbin in binningMET[:-1]:
        efficiency[bj][lhbin][lmbin]={}
  print "Mode",mode,"...Chaining...msugraScan", commoncf
  c.Draw(">>eList", commoncf)
  eList = ROOT.gROOT.Get("eList")
  print "Total # of Events in Scan:",eList.GetN()

  nev = eList.GetN()
  if maxEvents>0:
    nev = min(maxEvents, eList.GetN())
  for nEvent in range(0, nev):
    if (nEvent%10000 == 0) and i>0 :
      print nEvent

    c.GetEntry(eList.GetEntry(nEvent))
    m0      = c.GetLeaf("msugra_m0").GetValue()
    m12     = c.GetLeaf("msugra_m12").GetValue()
    tanb    = c.GetLeaf("msugra_tanbeta").GetValue()
    A0      = c.GetLeaf("msugra_A0").GetValue()
    signMu  = c.GetLeaf("msugra_signMu").GetValue()
    btag0   = c.GetLeaf("btag0").GetValue()
    btag1   = c.GetLeaf("btag0").GetValue()
    ht =    c.GetLeaf("ht").GetValue()
    kinMetSig =    c.GetLeaf("barepfmet").GetValue()/ROOT.sqrt(c.GetLeaf("ht").GetValue())
    barepfMet =    c.GetLeaf("barepfmet").GetValue()
    sstring = getMSUGRAShortString(m0, m12, tanb, A0, signMu)
    for bj in bjetbins.keys():
      for lhbin in binningHT[:-1]:
        for lmbin in binningkinMetSig[:-1]:
          if not efficiencykinMetSig[bj][lhbin][lmbin].has_key(sstring):
            efficiencykinMetSig[bj][lhbin][lmbin][sstring] = 0
          if eval(bjetbinsPy[bj]) and ht>lhbin and kinMetSig>lmbin:
            efficiencykinMetSig[bj][lhbin][lmbin][sstring]+=1
        #    print sstring, "xsec", msugraxsec[sstring], "counts", msugraCount[sstring]
        for lmbin in binningMET[:-1]:
          if not efficiency[bj][lhbin][lmbin].has_key(sstring):
            efficiency[bj][lhbin][lmbin][sstring] = 0
          if eval(bjetbinsPy[bj]) and ht>lhbin and barepfMet>lmbin:
            efficiency[bj][lhbin][lmbin][sstring]+=1
        #    print sstring, "xsec", msugraxsec[sstring], "counts", msugraCount[sstring]

  for bj in bjetbins.keys():
    for lhbin in binningHT[:-1]:
      for lmbin in binningkinMetSig[:-1]:
        for key in  efficiencykinMetSig[bj][lhbin][lmbin].keys():
          efficiencykinMetSig[bj][lhbin][lmbin][key] = efficiencykinMetSig[bj][lhbin][lmbin][key]/float(msugraCount[key])
      for lmbin in binningMET[:-1]:
        for key in  efficiency[bj][lhbin][lmbin].keys():
          efficiency[bj][lhbin][lmbin][key] = efficiency[bj][lhbin][lmbin][key]/float(msugraCount[key])
  del eList
  del c

  ofile = open(filename, "w")
  ofile.write("commoncf = "+repr(commoncf)+"\n")
  ofile.write("targetLumi = "+repr(targetLumi)+"\n")
  ofile.write("efficiency = "+repr(efficiency)+"\n")
  ofile.write("efficiencykinMetSig = "+repr(efficiencykinMetSig)+"\n")
  ofile.close()
  print "Written",filename
else:
  execfile(filename)
  print "Loaded",filename
