import ROOT
from Workspace.RA4Analysis.simplePlotsCommon import *
from defaultHad2012Samples import *
import copy, os, xsec, types
from math import sqrt
from funcs import metFunc, fakeMet

haddata = HTdata
targetLumi = 19400.
maxNJet = 10
minNJet = 6
small=False
bjetbins = {"inc":"(1)", \
            "b0":"(!(btag0>0.679))",
            "b1":"(btag0>0.679&&(!(btag1>0.679)))",
            "b1p":"(btag0>0.679)",
            "b2":"(btag1>0.679)"
            }

leptonVeto = "(nvetoMuons==0&&nvetoElectrons==0)"

subdir = "pngFake2012"
prefix = "525_20fb_type1phiMet_minNJet"+str(minNJet)

subtractTT = True

binning = [50,0,1000]
if subtractTT:
  prefix = "subtractTT_"+prefix
#prefix = "525_20fb_typeIpfMET_"
cHadFull = ROOT.TChain("Events")
for b in HTdata["bins"]:
  if small:
    print HTdata["dirname"]+"/"+b+"/h*_10_*.root"
    cHadFull.Add(HTdata["dirname"]+"/"+b+"/h*_10_*.root")
  else:
    print HTdata["dirname"]+"/"+b+"/h*.root"
    cHadFull.Add(HTdata["dirname"]+"/"+b+"/h*.root")
#leptonVetoalreadyAppliedToHadData = False

cHad = ROOT.TChain("Events")
cHad.Add("/data/schoef/convertedTuples_v16/copy2JleptVeto/HT/HTData/histo_HTData.root")
leptonVetoalreadyAppliedToHadData = True
if subtractTT:
  cTT = ROOT.TChain("Events")
  cTT.Add("/data/schoef/convertedTuples_v19/copy6JleptVeto/HT/TTJets-PowHeg/histo_TTJets-PowHeg.root")

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

alltriggers =  list(set([val[2] for val in htvals])) + ["HLTHT200", "HLTHT250"]
alltriggers.sort()

###Make a beautiful HT vs. trigger plot
#c1 = ROOT.TCanvas()
#h_ht = {}
#for [i, t] in enumerate(alltriggers):
#  cutFunc = "("+leptonVeto+")*("+t+"*"+t.replace("HLT","pre")+")"
#  print "At", i,"/",len(alltriggers) - 1,"=", t, cutFunc
#  cHad.Draw("ht>>htmp(110,0,5500)", cutFunc)
#  htmp = ROOT.gDirectory.Get("htmp")
#  h_ht[t]=htmp.Clone()
#  del htmp
#
#ROOT.gPad.SetLogy()
#l = ROOT.TLegend(0.61,0.6,.98,.95)
#l.SetFillColor(0)
#l.SetShadowColor(ROOT.kWhite)
#l.SetBorderSize(1)
#
#for [i, t] in enumerate(alltriggers):
#  opt = ""
#  if i>0:
#    opt = "same"
#  else:
#    h_ht[t].GetYaxis().SetRangeUser(0.7, 3*h_ht[t].GetMaximum())
#  h_ht[t].SetLineColor(ROOT_colors[i])
#  h_ht[t].GetXaxis().SetTitle("H_{T} (GeV)")
#  h_ht[t].GetYaxis().SetTitle("Number of Events / 50 GeV")
#  h_ht[t].Draw(opt)
#  l.AddEntry(h_ht[t], t.replace("HLT","HLT_"))
#
#l.Draw()
#
#lines = [[0.61, 0.55, "#font[22]{CMS preliminary}"], [0.61,0.5,str(int(round(targetLumi/100.))/10.)+" fb^{-1},  #sqrt{s} = 8 TeV"]]
#latex = ROOT.TLatex();
#latex.SetNDC();
#latex.SetTextSize(0.04);
#latex.SetTextAlign(11); # align right
#for line in lines:
#  stuff.append(latex.DrawLatex(line[0],line[1],line[2]))
#
#c1.Print(defaultWWWPath+"/"+subdir+"/"+prefix+"ht_HLTtimesPreScale.png")
#c1.Print(defaultWWWPath+"/"+subdir+"/"+prefix+"ht_HLTtimesPreScale.root")
#c1.Print(defaultWWWPath+"/"+subdir+"/"+prefix+"ht_HLTtimesPreScale.pdf")
#
#del c1
#
####get nice yieldPerRun histograms
#runRangeMin = 190456
#runRangeMax = 209000
#c1 = ROOT.TCanvas()
#stuff=[]
#for trigger in alltriggers:
#  ofile = "/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/yieldPerRun_"+trigger+".root"
##  if os.path.isfile(ofile):
##    print "found",ofile,"-> skipping ",trigger
##    continue
#  print "yield per run for ",trigger
#  cHad.Draw("run>>hrunTMP("+str(runRangeMin)+"-"+str(runRangeMax)+", "+str(runRangeMin)+", "+str(runRangeMax)+")",trigger+">0&&"+trigger.replace("HLT","pre")+">0")
#  print trigger+">0&&"+trigger.replace("HLT","pre")+">0"
#  hrun = ROOT.gDirectory.Get("hrunTMP").Clone()
#  stuff.append(hrun)
#  cHad.Draw("run>>hrunPresTMP("+str(runRangeMin)+"-"+str(runRangeMax)+", "+str(runRangeMin)+", "+str(runRangeMax)+")","("+trigger+">0&&"+trigger.replace("HLT","pre")+">0)*"+trigger.replace("HLT","pre"))
#  print "("+trigger+">0&&"+trigger.replace("HLT","pre")+">0)*"+trigger.replace("HLT","pre")
#  hrunPres = ROOT.gDirectory.Get("hrunPresTMP").Clone()
#  stuff.append(hrunPres)
#  hrunPres.SetMinimum(0.7)
#  hrunPres.SetMaximum(1.2*10**8)
#  ym = hrunPres.GetMaximum()
#  hrunPres.SetMaximum(1.5*ym)
#  hrunPres.SetLineColor(ROOT.kBlue)
#  hrunPres.GetXaxis().SetLabelSize(0.02)
#  hrunPres.Draw()
#  ROOT.gPad.SetLogy()
#  hrun.Draw("same")
#  for x in [ 193752, 197770, 198934, 203002]:
#    t = ROOT.TLine(x, hrunPres.GetYaxis().GetXmin(), x, ym)
#    t.SetLineStyle(2)
#    stuff.append(t)
#    t.Draw()
#    tl = ROOT.TLatex()
#    l=[]
#  for m in [["Run2012A", 192000, 8*10**7],["Run2012B", 195200, 8*10**7],["Run2012C-v1", 198550, 8*10**7],["Run2012C-v2", 201000, 3*10**7], ["Run2012D", 205000, 8*10**7]]:
##      tl.SetNDC();
#    tl.SetTextSize(0.025);
#    tl.SetTextAlign(22); # align right
#    l.append(tl.DrawLatex(m[1],m[2],m[0]));
#  for t in l:
#    t.Draw()
#    stuff.append(t)
#  del tl
#  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/"+prefix+"yieldPerRun_"+trigger+".png")
#  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/"+prefix+"yieldPerRun_"+trigger+".root")
#  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/"+prefix+"yieldPerRun_"+trigger+".pdf")
#del c1


### Make Data/MC comparison of had. QCD events
#
#qcdHad["dirname"] = "/data/schoef/convertedTuples_v9//copy2JleptVeto/HT/"
#qcdHad["name"] = "had. QCD"
#qcdHad["bins"] =  ["QCDHad"]
#qcdHad["hasWeight"] = True 
#
#haddata["dirname"] = "/data/schoef/convertedTuples_v9//copy2JleptVeto/HT/"
#haddata["name"] = "HT Data"
#haddata["bins"] =  ["HTData"]
#haddata["hasWeight"] = True 
#
#def getQCDStack(varname, binning, commoncf_, triggerFac_, htbin, varfunc=""):
#  htCut = "(ht>"+str(htbin[0])+"&&ht<"+str(htbin[1])+")"
#  DATA          = variable(varname, binning, "("+commoncf_.replace(leptonVeto,"(1)")+"&&"+htCut+")*"+triggerFac) #FIXME: Remove removal of leptonVeto once converted QCD stores nvetoLepton!
#  DATA.sample   = haddata
#  DATA.color    = dataColor
#  DATA.legendText="HT triggered data"
#  DATA.style = "l12"
##  MC = variable(varname, binning, commoncf_+"&&"+htCut) 
#  MC = variable(varname, binning, commoncf_.replace(leptonVeto,"(1)")+"&&"+htCut) #FIXME: Remove removal of leptonVeto once converted QCD stores nvetoLepton!
#  MC.sample = qcdHad
#  MC.color = myBlue
#  MC.style = "f"
#  MC.legendText = "QCD had. (area normalized)"
#  MC.normalizeTo = DATA
#  MC.legendCoordinates = [0.41,0.7,.98,.95]
#  MC.lines = [[0.41, 0.65, str(htval[0])+" < H_{T} < "+str(htval[1])+" GeV"], [0.41, 0.6, "#font[22]{CMS preliminary}"], [0.41,0.55,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 8 TeV"]]
#  MC.dataMCRatio = [DATA, MC]
#  MC.ratioVarName = "Data / MC"
#  res = [MC, DATA]
#  if varfunc!="":
#    for var in res:
#      var.varfunc = varfunc
#
#  return res
#
#allStacks = []
#allSamples = [haddata, qcdHad]
#met_stack = {}
#ngoodVertices_stack = {}
#ht_stack = {}
#htvals = [[350, 2500, "HLTHT300"]] #+  htvals
#for htval in htvals: 
#  t = htval[2]
#  commoncf = "("+leptonVeto+")&&jet2pt>40"
#  triggerFac = "("+t+"*"+t.replace("HLT","pre")+")"
#  met_stack[htval[0]] = getQCDStack(":met;#slash{E}_{T} (GeV);Number of Events / 20 GeV",[52,0,1040], commoncf, triggerFac, htval, metFunc)
#  met_stack[htval[0]][0].addOverFlowBin = "upper"
#  allStacks.append(met_stack[htval[0]])
#
#  ngoodVertices_stack[htval[0]] = getQCDStack(":ngoodVertices;ngoodVertices;Number of Events",[25,0,25], commoncf, triggerFac, htval)
#  ngoodVertices_stack[htval[0]][0].addOverFlowBin = "upper"
#  allStacks.append(ngoodVertices_stack[htval[0]])
#
#  nbins = int( (htval[1]-htval[0]) / 12.5)
#  ht_stack[htval[0]]  = getQCDStack(":ht;H_{T} (GeV);Number of Events / 12.5 GeV",[nbins,htval[0],htval[0]+nbins*12.5 ], commoncf, triggerFac, htval)
#  ht_stack[htval[0]][0].addOverFlowBin = "upper"
#  allStacks.append(ht_stack[htval[0]])
#
##reweightingHistoFile = "reweightingHisto_Summer2012Private.root"
#reweightingHistoFile = ""
#execfile("simplePlotsLoopKernel.py")
#
#for htval in htvals:
#  for stack in allStacks:
#    stack[0].maximum = 10.*stack[-1].data_histo.GetMaximum()
#    stack[0].logy = True
#    stack[0].minimum = 0.7
#  preprefix = "ht-"+str(htval[0])+"-"+str(htval[1])+"_"+htval[2]+"_"
#  drawNMStacks(1,1,[met_stack[htval[0]]],             subdir+"/"+prefix+preprefix+"met", False)
#  drawNMStacks(1,1,[ngoodVertices_stack[htval[0]]],   subdir+"/"+prefix+preprefix+"ngoodVertices", False)
#  drawNMStacks(1,1,[ht_stack[htval[0]]],              subdir+"/"+prefix+preprefix+"ht", False)
#  for stack in allStacks:
#    stack[0].maximum = 1.3*stack[-1].data_histo.GetMaximum()
#    stack[0].logy = False
#    stack[0].minumum=0
#  drawNMStacks(1,1,[met_stack[htval[0]]],             subdir+"/"+prefix+preprefix+"met_lin", False)
#  drawNMStacks(1,1,[ngoodVertices_stack[htval[0]]],   subdir+"/"+prefix+preprefix+"ngoodVertices_lin", False)
#  drawNMStacks(1,1,[ht_stack[htval[0]]],              subdir+"/"+prefix+preprefix+"ht_lin", False)

#get NJ distributions
leptonCommonCF = {}
leptonCommonCF["Mu"] =  "jet2pt>40&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)&&type1phiMet>150&&ht>350"
leptonCommonCF["Ele"]=  "jet2pt>40&&(singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)&&type1phiMet>150&&ht>350"


def getNJStack(dataCutString, sample_, varname = "njets"):
  binning = [20,0,20]
  DATA          = variable(varname, binning, dataCutString)
  DATA.sample   = sample_
  DATA.color    = dataColor
  DATA.legendText=sample_["name"]
  res = [DATA]
  return res

mc = {}
mc["Mu"]   = {"name":"MuMC",  "hasWeight": True, "bins": ["TTJets-PowHeg", "WJetsHT250", "singleTop", "DY", "QCD"], "dirname":"/data/schoef/convertedTuples_v16/copyMET/Mu/", "Chain":"Events", "specialCuts":[]}
mc["Ele"]  = {"name":"EleMC", "hasWeight": True, "bins": ["TTJets-PowHeg", "WJetsHT250", "singleTop", "DY", "QCD"], "dirname":"/data/schoef/convertedTuples_v16/copyMET/Ele/", "Chain":"Events", "specialCuts":[]}

data = {}
data["Mu"]={}
data["Mu"]["name"]     = "dataMu";
data["Mu"]["dirname"] = "/data/schoef/convertedTuples_v16/copyMET/Mu/"
data["Mu"]["bins"]    = [ 'data']
data["Mu"]["Chain"] = "Events"
data["Mu"]["hasWeight"] = True
data["Ele"]={}
data["Ele"]["name"]     = "dataEle";
data["Ele"]["dirname"] = "/data/schoef/convertedTuples_v16/copyMET/Ele/"
data["Ele"]["bins"]    = [ 'data']
data["Ele"]["Chain"] = "Events"
data["Ele"]["hasWeight"] = True

allSamples = [data["Mu"], data["Ele"], mc['Mu'], mc['Ele']]
allStacks=[]

filename = "/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/"+prefix+"data_njet-shapes.root"
nj_stacks = {}
nj_mc_stacks = {}
if not os.path.exists(filename):
  for mode in ["Ele", "Mu"]:
    nj_stacks[mode]={}
    nj_mc_stacks[mode]={}
    for bmode in bjetbins.keys():
      cut = leptonCommonCF[mode]+"&&("+bjetbins[bmode]+")&&njets>="+str(minNJet)
      nj_stacks[mode][bmode]={}
      nj_mc_stacks[mode][bmode]={}
      print "Constructing njet histos for", mode," in bjetbin",bmode,"using", cut
      for htval in htvals:
        nj_stacks[mode][bmode][str(htval[0])] =  getNJStack( addCutString(cut, getHTBinCutString(htval)) , data[mode], "njets")
        allStacks.append(nj_stacks[mode][bmode][str(htval[0])])
        nj_mc_stacks[mode][bmode][str(htval[0])] =  getNJStack( addCutString(cut, getHTBinCutString(htval)) , mc[mode], "njets")
        allStacks.append(nj_mc_stacks[mode][bmode][str(htval[0])])
  
#'h_mean'       reweightingHistoFile = "reweightingHisto_Summer2012Private.root"
  execfile("simplePlotsLoopKernel.py")
  #Adding for EleMu
  nj_stacks["EleMu"]={}
  nj_mc_stacks["EleMu"]={}
  for bmode in bjetbins.keys():
    nj_stacks["EleMu"][bmode]={}
    nj_mc_stacks["EleMu"][bmode]={}
    for htval in htvals:
      nj_stacks["EleMu"][bmode][str(htval[0])] = copy.deepcopy(nj_stacks["Mu"][bmode][str(htval[0])])
      nj_stacks["EleMu"][bmode][str(htval[0])][0].data_histo.Add(nj_stacks["Ele"][bmode][str(htval[0])][0].data_histo)
      nj_mc_stacks["EleMu"][bmode][str(htval[0])] = copy.deepcopy(nj_mc_stacks["Mu"][bmode][str(htval[0])])
      nj_mc_stacks["EleMu"][bmode][str(htval[0])][0].data_histo.Add(nj_mc_stacks["Ele"][bmode][str(htval[0])][0].data_histo)
  tf = ROOT.TFile(filename, "recreate")
  tf.cd()
  for mode in ["Ele", "Mu", "EleMu"]:
    for bmode in bjetbins.keys():
      for htval in htvals:
        hname = "njets_"+mode+"_"+bmode+"_ht_"+str(htval[0])
        nj_stacks[mode][bmode][str(htval[0])][0].data_histo.SetName(hname)
        nj_stacks[mode][bmode][str(htval[0])][0].data_histo.Write()
        hname = "njets_mc_"+mode+"_"+bmode+"_ht_"+str(htval[0])
        nj_mc_stacks[mode][bmode][str(htval[0])][0].data_histo.SetName(hname)
        nj_mc_stacks[mode][bmode][str(htval[0])][0].data_histo.Write()
  tf.Close()
  print "Written njet reweighting histos to", filename
else:
  print "Reading", filename
  rf = ROOT.TFile(filename)
  for mode in ["Ele", "Mu", "EleMu"]:
    nj_stacks[mode]={}
    nj_mc_stacks[mode]={}
    for bmode in bjetbins.keys():
      nj_stacks[mode][bmode]={}
      nj_mc_stacks[mode][bmode]={}
      for htval in htvals:
        rf.cd()
        hname = "njets_"+mode+"_"+bmode+"_ht_"+str(htval[0])
        htmp = rf.Get(hname)
        ROOT.gDirectory.cd("PyROOT:/")
        nj_stacks[mode][bmode][str(htval[0])] = [htmp.Clone(hname+"_clone")]
        nj_stacks[mode][bmode][str(htval[0])][0].SetName(hname)
        print "Read",nj_stacks[mode][bmode][str(htval[0])][0],"from",filename
      for htval in htvals:
        rf.cd()
        hname = "njets_mc_"+mode+"_"+bmode+"_ht_"+str(htval[0])
        htmp = rf.Get(hname)
        ROOT.gDirectory.cd("PyROOT:/")
        nj_mc_stacks[mode][bmode][str(htval[0])] = [htmp.Clone(hname+"_clone")]
        nj_mc_stacks[mode][bmode][str(htval[0])][0].SetName(hname)
        print "Read",nj_mc_stacks[mode][bmode][str(htval[0])][0],"from",filename
  rf.Close()


##Construct 1l fake MET templates

cQCDHad = ROOT.TChain("Events")
cQCDHad.Add("/data/schoef/convertedTuples_v16//copy2JleptVeto/HT/QCDHad/h*.root")

met_template_nj={}
met_shapes={}
met_mc_template_nj={}
met_mc_shapes={}
fullrootfilename = "/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/"+prefix+"templates.root"
if not os.path.isfile(  fullrootfilename ):
  print "Constructing templates"
  met_template_nj={}
  met_mc_template_nj={}
  for bmode in bjetbins.keys():
    met_template_nj[bmode]={}
    met_mc_template_nj[bmode]={}
    for htval in htvals:
      trigger = htval[2]
      met_template_nj[bmode][htval[0]] = {}
      met_mc_template_nj[bmode][htval[0]] = {}
      for nj in range(minNJet,maxNJet):
        if subtractTT:
          #TTJets correction
          cut = addCutString("jet1pt>40&&"+leptonVeto+"&&"+bjetbins[bmode]+"&&njets=="+str(nj), getHTBinCutString(htval))
          print "Getting TT correction (ht, njet) met template for nj",nj, htval, bmode, cut
          htmp = ROOT.TH1F("hnjTMP", "hnjTMP", *binning)
          htmp.Sumw2()
          cTT.Draw("type1phiMet>>hnjTMP", "weight*("+cut+")")
          met_tt_template_nj = htmp.Clone()
          del htmp

        #Data nj templates
        precut = addCutString("jet1pt>40&&"+leptonVeto+"&&"+bjetbins[bmode]+"&&njets=="+str(nj), getHTBinCutString(htval))
        if leptonVetoalreadyAppliedToHadData:
          precut = addCutString("jet1pt>40&&"+bjetbins[bmode]+"&&njets=="+str(nj), getHTBinCutString(htval))
        cut = "("+precut+"&&"+trigger+">0&&"+trigger.replace("HLT","pre")+">0)*"+trigger.replace("HLT","pre")
        print "Getting Data (ht, njet) met template for nj",nj, htval, bmode, cut
        htmp = ROOT.TH1F("hnjTMP", "hnjTMP", *binning)
        htmp.Sumw2()
        cHad.Draw("type1phiMet>>hnjTMP", cut)
        met_template_nj[bmode][htval[0]][nj] = htmp.Clone()
        if subtractTT:
          met_tt_template_nj.Scale(-1)
          met_template_nj[bmode][htval[0]][nj].Add(met_tt_template_nj)
          for b in range(1, 1+met_template_nj[bmode][htval[0]][nj].GetNbinsX()):
            if met_template_nj[bmode][htval[0]][nj].GetBinContent(b)<0.: met_template_nj[bmode][htval[0]][nj].SetBinContent(b, 0.)

        integr = met_template_nj[bmode][htval[0]][nj].Integral()
        if integr>0:
          met_template_nj[bmode][htval[0]][nj].Scale(1./integr)
        hname = "met_shape_"+bmode+"_ht_"+str(htval[0])+"_"+str(htval[1])+"_njet_"+str(nj)
        met_template_nj[bmode][htval[0]][nj].SetName(hname)
        del htmp

        #MC templates
        cut = addCutString("jet1pt>40&&"+leptonVeto+"&&"+bjetbins[bmode]+"&&njets=="+str(nj), getHTBinCutString(htval))
        print "Getting MC (ht, njet) met template for nj",nj, htval, bmode, cut
        htmp2 = ROOT.TH1F("hnjTMP", "hnjTMP", *binning)
        htmp2.Sumw2()
        cQCDHad.Draw("type1phiMet>>hnjTMP", "weight*("+cut+")")
        met_mc_template_nj[bmode][htval[0]][nj] = htmp2.Clone()
        integr = met_mc_template_nj[bmode][htval[0]][nj].Integral()
        if integr>0:
          met_mc_template_nj[bmode][htval[0]][nj].Scale(1./integr)
        hname = "met_mc_shape_"+bmode+"_ht_"+str(htval[0])+"_"+str(htval[1])+"_njet_"+str(nj)
        met_mc_template_nj[bmode][htval[0]][nj].SetName(hname)
        del htmp2

  for mode in ["Ele", "Mu", "EleMu"]:
    met_shapes[mode]={}
    met_mc_shapes[mode]={}
    for bmode in bjetbins.keys():
      met_shapes[mode][bmode]={}
      met_mc_shapes[mode][bmode]={}
      for htval in htvals:
        hres = met_template_nj[bmode][htvals[0][0]][minNJet].Clone() #Get a met histo of the same type as the nj histos
        hres.Reset()
        hres_mc = hres.Clone()
        nj = nj_stacks[mode][bmode][str(htval[0])][0]
        nj_mc = nj_mc_stacks[mode][bmode][str(htval[0])][0]
        if not type(nj)==type(ROOT.TH1F()):#I construct them as var but I store them as histo, hence, when reloading njets distributions they are histos, otherwise vars. I want histos here
          nj = nj.data_histo
        if not type(nj_mc)==type(ROOT.TH1F()):#I construct them as var but I store them as histo, hence, when reloading nj_mcets distributions they are histos, otherwise vars. I want histos here
          nj_mc = nj_mc.data_histo
        for i in range(minNJet, maxNJet): #Adding up templates
          njetweight = nj.GetBinContent(nj.FindBin(i))
          htmp = met_template_nj[bmode][htval[0]][i].Clone()
          htmp.Scale(njetweight)
          hres.Add(htmp)
          njetweight = nj_mc.GetBinContent(nj_mc.FindBin(i))
          htmp = met_mc_template_nj[bmode][htval[0]][i].Clone()
          htmp.Scale(njetweight)
          hres_mc.Add(htmp)
        
        #FIXME Add TT template correction here! 

        integr = hres.Integral()
        if integr>0:
          hres.Scale(1./integr)
        integr = hres_mc.Integral()
        if integr>0:
          hres_mc.Scale(1./integr)
        met_shapes[mode][bmode][htval[0]] = hres.Clone()
        hname = "met_shape_"+mode+"_"+bmode+"_ht_"+str(htval[0])+"_"+str(htval[1])
        met_shapes[mode][bmode][htval[0]].SetName(hname)
        met_mc_shapes[mode][bmode][htval[0]] = hres_mc.Clone()
        hname = "met_mc_shape_"+mode+"_"+bmode+"_ht_"+str(htval[0])+"_"+str(htval[1])
        met_mc_shapes[mode][bmode][htval[0]].SetName(hname)
  print "(Over-)writing ROOT file",fullrootfilename
  tf = ROOT.TFile(fullrootfilename, "RECREATE")
  tf.cd()
  for htval in htvals:
    for bmode in bjetbins.keys():
      for nj in met_template_nj[bmode][htval[0]].keys():
        met_template_nj[bmode][htval[0]][nj].Write()
        met_mc_template_nj[bmode][htval[0]][nj].Write()
      for mode in ["Ele", "Mu", "EleMu"]:
        met_shapes[mode][bmode][htval[0]].Write()
        met_mc_shapes[mode][bmode][htval[0]].Write()
        if not type(nj_stacks[mode][bmode][str(htval[0])][0])==type(ROOT.TH1F()):
          nj_stacks[mode][bmode][str(htval[0])][0].data_histo.Write()
          nj_mc_stacks[mode][bmode][str(htval[0])][0].data_histo.Write()
        else:
          nj_stacks[mode][bmode][str(htval[0])][0].Write()
          nj_mc_stacks[mode][bmode][str(htval[0])][0].Write()

  tf.Close()
  print "Written", fullrootfilename
else:
  print "Reading", fullrootfilename
  rf = ROOT.TFile(fullrootfilename)
  for mode in ["Ele", "Mu", "EleMu"]:
    met_shapes[mode]={}
    met_mc_shapes[mode]={}
    for bmode in bjetbins.keys():
      met_shapes[mode][bmode]={}
      met_mc_shapes[mode][bmode]={}
      for htval in htvals:
        hname = "met_shape_"+mode+"_"+bmode+"_ht_"+str(htval[0])+"_"+str(htval[1])
        htmp = rf.Get(hname)
        ROOT.gDirectory.cd("PyROOT:/")
        met_shapes[mode][bmode][htval[0]] = htmp.Clone(hname)
        print "Read",met_shapes[mode][bmode][htval[0]],"=",hname,"from",fullrootfilename
        rf.cd()
        hname = "met_mc_shape_"+mode+"_"+bmode+"_ht_"+str(htval[0])+"_"+str(htval[1])
        htmp = rf.Get(hname)
        ROOT.gDirectory.cd("PyROOT:/")
        met_mc_shapes[mode][bmode][htval[0]] = htmp.Clone(hname)
        print "Read",met_mc_shapes[mode][bmode][htval[0]],"=",hname,"from",fullrootfilename
  for bmode in bjetbins.keys():
    met_template_nj[bmode] = {}
    met_mc_template_nj[bmode] = {}
    for htval in htvals:
      met_template_nj[bmode][htval[0]] = {}
      met_mc_template_nj[bmode][htval[0]] = {}
      for nj in range(minNJet, maxNJet):
        hname = "met_shape_"+bmode+"_ht_"+str(htval[0])+"_"+str(htval[1])+"_njet_"+str(nj)
        htmp = rf.Get(hname)
        ROOT.gDirectory.cd("PyROOT:/")
        met_template_nj[bmode][htval[0]][nj] = htmp.Clone()
        print "Read", met_template_nj[bmode][htval[0]][nj],"=",hname,"from",fullrootfilename
        hname = "met_mc_shape_"+bmode+"_ht_"+str(htval[0])+"_"+str(htval[1])+"_njet_"+str(nj)
        htmp = rf.Get(hname)
        ROOT.gDirectory.cd("PyROOT:/")
        met_mc_template_nj[bmode][htval[0]][nj] = htmp.Clone()
        print "Read", met_mc_template_nj[bmode][htval[0]][nj],"=",hname,"from",fullrootfilename


  rf.Close()

#htbins = [x[0] for x in htvals]+[htvals[-1][1]]
#h_mean = {}
#h_scale = {}
#h_mc_mean = {}
#h_mc_scale = {}
#for mode in ["Ele", "Mu", "EleMu"]:
#  h_mean[mode]={}
#  h_scale[mode]={}
#  h_mc_mean[mode]={}
#  h_mc_scale[mode]={}
#  for bmode in bjetbins.keys():
#    h_mean[mode][bmode]={}
#    h_scale[mode][bmode]={}
#    h_mc_mean[mode][bmode]={}
#    h_mc_scale[mode][bmode]={}
#    for nj in range(minNJet, maxNJet):
#      h_mean[mode][bmode][nj]     =ROOT.TH1F('h_mean'     , 'h_mean'     , len(htbins)-1, array('d', htbins)) 
#      h_scale[mode][bmode][nj]    =ROOT.TH1F('h_scale'    , 'h_scale'    , len(htbins)-1, array('d', htbins))
#      h_mc_mean[mode][bmode][nj]  =ROOT.TH1F('h_mc_mean'  , 'h_mc_mean'  , len(htbins)-1, array('d', htbins))
#      h_mc_scale[mode][bmode][nj] =ROOT.TH1F('h_mc_scale' , 'h_mc_scale' , len(htbins)-1, array('d', htbins))
#      for htval in htvals:
#        ibin = h_mean[mode][bmode][nj].FindBin(.5*(htval[0] + htval[1]))
#        h_mean[mode][bmode][nj].SetBinContent(ibin,       met_template_nj[bmode][htval[0]][nj].GetMean())
#        h_mean[mode][bmode][nj].SetBinError(ibin,         met_template_nj[bmode][htval[0]][nj].GetMeanError())
#        h_scale[mode][bmode][nj].SetBinContent(ibin,      met_template_nj[bmode][htval[0]][nj].GetRMS())
#        h_scale[mode][bmode][nj].SetBinError(ibin,        met_template_nj[bmode][htval[0]][nj].GetRMSError())
#        h_mc_mean[mode][bmode][nj].SetBinContent(ibin,    met_mc_template_nj[bmode][htval[0]][nj].GetMean())
#        h_mc_mean[mode][bmode][nj].SetBinError(ibin,      met_mc_template_nj[bmode][htval[0]][nj].GetMeanError())
#        h_mc_scale[mode][bmode][nj].SetBinContent(ibin,   met_mc_template_nj[bmode][htval[0]][nj].GetRMS())
#        h_mc_scale[mode][bmode][nj].SetBinError(ibin,     met_mc_template_nj[bmode][htval[0]][nj].GetRMSError())
#
#c1 = ROOT.TCanvas()
#for mode in ["Ele", "Mu", "EleMu"]:
#  for bmode in bjetbins.keys():
#    l = ROOT.TLegend(0.61,0.15,.98,.4)
#    l.SetFillColor(0)
#    l.SetShadowColor(ROOT.kWhite)
#    l.SetBorderSize(1)
#    for nj in range(minNJet, maxNJet-1):
#      h_mean[mode][bmode][nj].SetLineColor(ROOT_colors[nj - minNJet])
#      h_mean[mode][bmode][nj].SetMarkerColor(ROOT_colors[nj - minNJet])
#      l.AddEntry(h_mean[mode][bmode][nj], "n-jet "+str(nj) )
#      if nj==minNJet:
#        h_mean[mode][bmode][nj].GetYaxis().SetRangeUser(0, 65)
#        h_mean[mode][bmode][nj].Draw()
#      else:
#        h_mean[mode][bmode][nj].Draw("same")
#    l.Draw()
#    c1.Print(defaultWWWPath+"/"+subdir+"/"+prefix+"_mean_"+mode+"_"+bmode+".png")
#    c1.Print(defaultWWWPath+"/"+subdir+"/"+prefix+"_mean_"+mode+"_"+bmode+".pdf")
#    l = ROOT.TLegend(0.61,0.15,.98,.4)
#    l.SetFillColor(0)
#    l.SetShadowColor(ROOT.kWhite)
#    l.SetBorderSize(1)
#    for nj in range(minNJet, maxNJet-1):
#      h_scale[mode][bmode][nj].SetLineColor(ROOT_colors[nj - minNJet])
#      h_scale[mode][bmode][nj].SetMarkerColor(ROOT_colors[nj - minNJet])
#      l.AddEntry(h_scale[mode][bmode][nj], "n-jet "+str(nj) )
#      if nj==minNJet:
#        h_scale[mode][bmode][nj].GetYaxis().SetRangeUser(0, 65)
#        h_scale[mode][bmode][nj].Draw()
#      else:
#        h_scale[mode][bmode][nj].Draw("same")
#    l.Draw()
#    c1.Print(defaultWWWPath+"/"+subdir+"/"+prefix+"_scale_"+mode+"_"+bmode+".png")
#    c1.Print(defaultWWWPath+"/"+subdir+"/"+prefix+"_scale_"+mode+"_"+bmode+".pdf")
#    l = ROOT.TLegend(0.61,0.15,.98,.4)
#    l.SetFillColor(0)
#    l.SetShadowColor(ROOT.kWhite)
#    l.SetBorderSize(1)
#    for nj in range(minNJet, maxNJet-1):
#      h_mc_mean[mode][bmode][nj].SetLineColor(ROOT_colors[nj - minNJet])
#      h_mc_mean[mode][bmode][nj].SetMarkerColor(ROOT_colors[nj - minNJet])
#      l.AddEntry(h_mc_mean[mode][bmode][nj], "n-jet "+str(nj) )
#      if nj==minNJet:
#        h_mc_mean[mode][bmode][nj].GetYaxis().SetRangeUser(0, 65)
#        h_mc_mean[mode][bmode][nj].Draw()
#      else:
#        h_mc_mean[mode][bmode][nj].Draw("same")
#    l.Draw()
#    c1.Print(defaultWWWPath+"/"+subdir+"/"+prefix+"_mc_mean_"+mode+"_"+bmode+".png")
#    c1.Print(defaultWWWPath+"/"+subdir+"/"+prefix+"_mc_mean_"+mode+"_"+bmode+".pdf")
#    l = ROOT.TLegend(0.61,0.15,.98,.4)
#    l.SetFillColor(0)
#    l.SetShadowColor(ROOT.kWhite)
#    l.SetBorderSize(1)
#    for nj in range(minNJet, maxNJet-1):
#      h_mc_scale[mode][bmode][nj].SetLineColor(ROOT_colors[nj - minNJet])
#      h_mc_scale[mode][bmode][nj].SetMarkerColor(ROOT_colors[nj - minNJet])
#      l.AddEntry(h_mc_scale[mode][bmode][nj], "n-jet "+str(nj) )
#      if nj==minNJet:
#        h_mc_scale[mode][bmode][nj].GetYaxis().SetRangeUser(0, 65)
#        h_mc_scale[mode][bmode][nj].Draw()
#      else:
#        h_mc_scale[mode][bmode][nj].Draw("same")
#    l.Draw()
#    c1.Print(defaultWWWPath+"/"+subdir+"/"+prefix+"_mc_scale_"+mode+"_"+bmode+".png")
#    c1.Print(defaultWWWPath+"/"+subdir+"/"+prefix+"_mc_scale_"+mode+"_"+bmode+".pdf")



#compare means and widths 

##Write text files for smoothing
#outDir = "/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/toBeSmoothed/"
#def writeFakeMETTemplatesToTXT(dirName = outDir):
#  for ck in met_shapes.keys():
#    for bk in met_shapes[ck].keys():
#      for htk in met_shapes[ck][bk].keys():
#        h = met_shapes[ck][bk][htk]
#        name = h.GetName()
#        fname = dirName+'/'+name+".txt"
#        print fname
#        tf = file(fname, "w")
#        for i in range(1, h.GetNbinsX()+1):
#          tf.write(str(h.GetBinLowEdge(i))+" "+str(h.GetBinLowEdge(i)+h.GetBinWidth(i))+" "+str( h.GetBinContent(i))+"\n")
#        tf.close()
#  for ck in met_mc_shapes.keys():
#    for bk in met_mc_shapes[ck].keys():
#      for htk in met_mc_shapes[ck][bk].keys():
#        h = met_mc_shapes[ck][bk][htk]
#        name = h.GetName()
#        fname = dirName+'/'+name.replace("met_shape","met_mc_shape")+".txt"
#        print fname
#        tf = file(fname, "w")
#        for i in range(1, h.GetNbinsX()+1):
#          tf.write(str(h.GetBinLowEdge(i))+" "+str(h.GetBinLowEdge(i)+h.GetBinWidth(i))+" "+str( h.GetBinContent(i))+"\n")
#        tf.close()
##          print h.GetBinLowEdge(i), h.GetBinLowEdge(i) + h.GetBinWidth(i), h.GetBinContent(i)
#inDir = "/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/smoothed/"
#def readFakeMETTemplatesFromTXT(dirName = inDir):
#  outfileSmoothed  = ROOT.TFile(dirName+"/smoothedTemplates.root","recreate")
#  for ck in met_shapes.keys():
#    for bk in met_shapes[ck].keys():
#      for htk in met_shapes[ck][bk].keys():
#        h = met_shapes[ck][bk][htk]
#        name = h.GetName()
#        fname = dirName+'/'+name+".txt"
#        tf = file(fname)
#        print fname
#        smoothTemplate = met_shapes[ck][bk][htk].Clone(name)
#        smoothTemplate.Reset()
#        for line in tf.readlines():
#          lines = line.replace('\n','').split()
#          xmin = float(lines[0])
#          xmax = float(lines[1])
#          val = float(lines[2])
#          smoothTemplate.Fill(.5*(xmin+xmax), val)
#        outfileSmoothed.cd()
#        smoothTemplate.Write()
#        tf.close()
#  for ck in met_mc_shapes.keys():
#    for bk in met_mc_shapes[ck].keys():
#      for htk in met_mc_shapes[ck][bk].keys():
#        h = met_mc_shapes[ck][bk][htk]
#        name = h.GetName()
#        fname = dirName+'/'+name.replace("met_shape","met_mc_shape")+".txt"
#        tf = file(fname)
#        print fname
#        smoothTemplate = met_shapes[ck][bk][htk].Clone(name)
#        smoothTemplate.Reset()
#        for line in tf.readlines():
#          lines = line.replace('\n','').split()
#          xmin = float(lines[0])
#          xmax = float(lines[1])
#          val = float(lines[2])
#          smoothTemplate.Fill(.5*(xmin+xmax), val)
#        outfileSmoothed.cd()
#        smoothTemplate.Write()
#        tf.close()
#  outfileSmoothed.Close()
#  print "Written",dirName+"/smoothedTemplates.root"
#
##parametrize fake MET templates
#outDir = "/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/smoothed/"
##[1] alpha
#m = 'EleMu'
#b = 'b2'
#ht = 1500
#binWidth = met_shapes[m][b][ht].GetBinWidth(1)
##chi2 + tail, continuation
#chi2AndTail = str(binWidth)+"/(1. + (2.*exp(-.5 - [1]/2.))/(-1. + [1]))*((x<sqrt(1.+[1])*[0])*(x/[0]**2*exp(-x**2/(2.*[0]**2))) + (x>=sqrt(1.+[1])*[0])*(1./[0]**2*exp(-.5*(1.+[1]))*x**(-[1])*((1+[1])*[0]**2)**(.5*(1+[1]))))"
##chi2 equivalent
##funcString = str(binWidth)+"*x/[0]**2*exp(-x**2/(2.*[0]**2))"
##chi2 + tail, fixed mu
#
#def chi2AndTailFixedMu(mu):
#  return str(binWidth)+"/(1. + exp(-"+str(mu)+"**2/(2.*[0]**2))*(-1. + "+str(mu)+"**2/(([1]-1)*[0]**2)))*((x<"+str(mu)+")*(x/[0]**2*exp(-x**2/(2.*[0]**2))) + (x>="+str(mu)+")*(1./[0]**2*exp(-"+str(mu)+"**2/(2.*[0]**2))*"+str(mu)+"*("+str(mu)+"/x)**[1]))"
#
##chi2 + tail, variable mu
#chi2AndTailFloatingMu = str(binWidth)+"/(1. + exp(-[2]**2/(2.*[0]**2))*(-1. + [2]**2/(([1]-1)*[0]**2)))*((x<[2])*(x/[0]**2*exp(-x**2/(2.*[0]**2))) + (x>=[2])*(1./[0]**2*exp(-[2]**2/(2.*[0]**2))*[2]*([2]/x)**[1]))"
#
##chi2 + tail, 
#def chi2FixedMuTailContinuation(mu):
#  return str(binWidth)+"/(2.*[0]**2+exp("+str(mu)+"**2/(2.*[0]**2))*("+str(mu)+"**2-2.*[0]**2))*("+str(mu)+"**2-2.*[0]**2)*((x<"+str(mu)+")*(x/[0]**2*exp(-(x**2-"+str(mu)+"**2)/(2.*[0]**2))) + (x>="+str(mu)+")*(1./[0]**2*x*(x/"+str(mu)+")**(-"+str(mu)+"**2/[0]**2)))"
#
#specialFuncs={\
## ('Mu', 'b1p', 1200) : {"func":chi2AndTailFixedMu(200),"fitRange":[40,1000]},
### ('Mu', 'b1p', 1000) : {"func":chi2AndTail, "fitRange":[100,300]},
## ('Mu', 'b1p', 1000) : {"func":chi2FixedMuTailContinuation(90), "fitRange":[0,1000]},
## ('Mu', 'b1p', 1500) : {"func":chi2AndTail, "fitRange":[40,1000]},
## ('Ele', 'b0', 1200) : {"func":chi2FixedMuTailContinuation(90), "fitRange":[0,1000]},
###
#}
#
#def getFit(ms, ck, bk, htk, sf):
#  h = ms[ck][bk][htk]
#  frmin=0
#  frmax=1000
#  if not sf.has_key((ck,bk,htk)):
#    func = ROOT.TF1("nf", chi2AndTail, 0, 1000)
#  else:
#    func = ROOT.TF1("nf", sf[(ck,bk,htk)]['func'], 0, 1000)
#    print "using special", sf[(ck,bk,htk)]
#    if sf[(ck,bk,htk)].has_key('fitRange'):
#      frmin=sf[(ck,bk,htk)]['fitRange'][0]
#      frmax=sf[(ck,bk,htk)]['fitRange'][1]
#      print "Using fitRange",sf[(ck,bk,htk)]['fitRange']
#    
#  func.SetParameter(0,20)
#  func.SetParameter(1,5)
#  func.SetParameter(2,50)
#  smoothed = ROOT.TH1F(ms[ck][bk][htk].GetName(), ms[ck][bk][htk].GetName(),2500,0,2500)
#  mc = ms[ck][bk][htk].Clone(ms[ck][bk][htk].GetName()+"_orig")
#  mc.Fit(func, "", "", frmin, frmax)
#  for i in range(1, smoothed.GetNbinsX()+1):
#    smoothed.SetBinContent(i, func.Eval(smoothed.GetBinCenter(i)))
#  return mc, smoothed
#
#def writeParametrizedFakeMETTemplates(dirName = outDir):
#  rf = ROOT.TFile(outDir+"/parametrizedTemplates.root", "recreate")
#  for ck in met_shapes.keys():
#    for bk in met_shapes[ck].keys():
#      for htk in met_shapes[ck][bk].keys():
#        mc, smoothed = getFit(met_shapes, ck, bk, htk, specialFuncs )
#        mc.Write()
#        smoothed.Write()
#  for ck in met_mc_shapes.keys():
#    for bk in met_mc_shapes[ck].keys():
#      for htk in met_mc_shapes[ck][bk].keys():
#        h = met_mc_shapes[ck][bk][htk]
#        if not specialFuncs.has_key((ck,bk,htk)):
#          func = ROOT.TF1("nf", chi2AndTail, 20, 1000)
#        else:
#          func = ROOT.TF1("nf", specialFuncs[(ck,bk,htk)], 20, 1000)
#        func.SetParameter(0,20)
#        func.SetParameter(1,5)
#        func.SetParameter(2,50)
#        smoothed = ROOT.TH1F(met_mc_shapes[ck][bk][htk].GetName(), met_mc_shapes[ck][bk][htk].GetName(),2500,0,2500)
#        mc = met_shapes[ck][bk][htk].Clone(met_mc_shapes[ck][bk][htk].GetName()+"_orig")#FIXME!!!!!!!!!!!!!!!!!!!11
#        mc.Fit(func)
#        mc.Write()
#        for i in range(1, smoothed.GetNbinsX()+1):
#          smoothed.SetBinContent(i, func.Eval(smoothed.GetBinCenter(i)))
#        smoothed.Write()
#  rf.Close()
#
#writeParametrizedFakeMETTemplates()

#Closure plots for fake MET templates

ttbar = {}
wjets = {}
stop = {}
dy = {}
qcd = {}
for mode in ["Ele", "Mu"]:
  ttbar[mode] = {"name":"TTJets"+mode}
  wjets[mode] = {"name":"WJets"+mode}
  stop[mode]  = {"name":"Stop"+mode}
  dy[mode]    = {"name":"DY"+mode}
  qcd[mode]   = {"name":"QCD"+mode}
  ttbar[mode]["bins"] = ["TTJets-PowHeg"]
  wjets[mode]["bins"] = ["WJetsHT250"]
  stop[mode]["bins"] = ["singleTop"]
  dy[mode]["bins"]  = ["DY"]
  qcd[mode]["bins"] = ["QCD"]
  ttbar[mode]["dirname"] = "/data/schoef/convertedTuples_v16//copyMET/"+mode+"/"
  wjets[mode]["dirname"] = "/data/schoef/convertedTuples_v16//copyMET/"+mode+"/"
  stop[mode]["dirname"]  = "/data/schoef/convertedTuples_v16//copyMET/"+mode+"/"
  dy[mode]["dirname"]    = "/data/schoef/convertedTuples_v16//copyMET/"+mode+"/"
  qcd[mode]["dirname"]   = "/data/schoef/convertedTuples_v16//copyMET/"+mode+"/"
allSamples  = [ttbar["Mu"], wjets["Mu"], dy["Mu"], stop["Mu"], qcd["Mu"]]
allSamples += [ttbar["Ele"], wjets["Ele"], dy["Ele"], stop["Ele"], qcd["Ele"]]

for sample in allSamples:
  sample["hasWeight"] = True
  sample["Chain"] = "Events"

allStacks = []

def getStack(binning, leptonicVar,  leptonicCutString, mode, lepFunc = ""):

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
  MC_QCD.sample                = qcd[mode]
  MC_TTJETS                    = copy.deepcopy(MC_QCD)
  MC_TTJETS.sample             = ttbar[mode]
  MC_WJETS                     = copy.deepcopy(MC_QCD)
  MC_WJETS.sample              = wjets[mode]
  MC_ZJETS                     = copy.deepcopy(MC_QCD)
  MC_ZJETS.sample              = dy[mode]
  MC_STOP                     = copy.deepcopy(MC_QCD)
  MC_STOP.sample              = stop[mode]

  MC_ZJETS.legendText          = "DY + Jets"
  MC_ZJETS.style               = "f0"
  MC_ZJETS.add                 = []
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
  MC_TTJETS.legendText         = "t#bar{t} + Jets"
  MC_TTJETS.style              = "f"
  MC_TTJETS.color              = ROOT.kRed - 3
  MC_TTJETS.add=[MC_WJETS]

  res = [MC_TTJETS, MC_WJETS, MC_QCD, MC_STOP, MC_ZJETS]
#  res = [MC_TTJETS, MC_WJETS, MC_QCD, MC_ZJETS]
  return res

fakemet_stacks={}
for mode in ["Ele", "Mu"]:
  fakemet_stacks[mode]={}
  for bmode in bjetbins.keys():
    fakemet_stacks[mode][bmode]={}
    for htval in htvals:
      binning = [50,0,1000]
    #  leptonicVar = ":sqrt((metpxUncorr-genmetpx)**2+(metpyUncorr-genmetpy)**2);fake-#slash{E}_{T} (GeV);Number of Events / 10 GeV" 
      leptonicVar = ":xxx;fake-#slash{E}_{T} (GeV);Number of Events / 10 GeV"
      fakemet_stacks[mode][bmode][htval[0]] = getStack(binning, leptonicVar, "njets>="+str(minNJet)+"&&"+leptonCommonCF[mode]+"&&"+bjetbins[bmode]+"&&"+getHTBinCutString(htval), mode, fakeMet)
      allStacks.append(fakemet_stacks[mode][bmode][htval[0]])

reweightingHistoFile = ""
execfile("simplePlotsLoopKernel.py")

fakemet_stacks["EleMu"] = {}
for bmode in bjetbins.keys():
  fakemet_stacks["EleMu"][bmode] = {}
  for htbin in fakemet_stacks["Mu"][bmode].keys():
    fakemet_stacks["EleMu"][bmode][htbin] = copy.deepcopy(fakemet_stacks["Mu"][bmode][htbin])
    for i in  range(len(fakemet_stacks["EleMu"][bmode][htbin])):
      fakemet_stacks["EleMu"][bmode][htbin][i].data_histo = fakemet_stacks["Mu"][bmode][htbin][i].data_histo.Clone()
      fakemet_stacks["EleMu"][bmode][htbin][i].data_histo.Add(fakemet_stacks["Ele"][bmode][htbin][i].data_histo.Clone())
    allStacks.append(fakemet_stacks["EleMu"][bmode][htbin])

for mode in ["Ele", "Mu", "EleMu"]:
  for bmode in bjetbins.keys():
    for htbin in fakemet_stacks[mode][bmode].keys():
      var = variable(":xx;fake-#slash{E}_{T} (GeV);Number of Events / 20 GeV", [50,0,1000], "")
      var.color    = myBlue
      var.data_histo    = met_mc_shapes[mode][bmode][htbin]
      var.legendText="pred. from MC"
      fakemet_stacks[mode][bmode][htbin].append(var)

      var = variable(":xx;fake-#slash{E}_{T} (GeV);Number of Events / 20 GeV", [50,0,1000], "")
      var.color    = dataColor
      var.data_histo    = met_shapes[mode][bmode][htbin]
      var.legendText="pred. from Data"
      fakemet_stacks[mode][bmode][htbin].append(var)


for stack in allStacks:
    stack[-1].normalizeTo = stack[0]
    stack[-2].normalizeTo = stack[0]

for stack in allStacks:
  stack[0].maximum = 30.*stack[0].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].minimum = 10**(-.5)
#  stack[0].logx = True
  stack[0].data_histo.GetXaxis().SetRangeUser(0,300)
  stack[0].legendCoordinates=[0.7,0.95 - 0.07*5,.98,.95]
  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi/100.))/10.)+" fb^{-1},  #sqrt{s} = 8 TeV"]]
#  stack[0].dataMCRatio = [stack[-1], stack[0]]
#  stack[0].ratioVarName = "pred. / truth"

#htstack[0].logx = False
#htstack[0].maximum = 30000000.*stack[0].data_histo.GetMaximum()
#htstack[0].data_histo.GetXaxis().SetLabelSize(0.03)
#drawNMStacks(1,1,[htstack], subdir+"/"+prefix+"all_ht", False)
#
for mode in ["Ele", "Mu", "EleMu"]:
  for bmode in bjetbins.keys():
    for htval in htvals:
      drawNMStacks(1,1,[fakemet_stacks[mode][bmode][htval[0]]], subdir+"/"+prefix+"closure_"+mode+"_"+bmode+"_ht_"+str(htval[0])+"_"+str(htval[1]), False)

