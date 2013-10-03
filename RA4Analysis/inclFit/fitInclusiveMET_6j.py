import ROOT as R
from ROOT import RooFit as RF
import os
import ctypes
from math import *
import pickle
import numpy as np

def useNiceColorPalette(NCont = 255):
    NRGBs = 5
    stops = [ 0.00, 0.34, 0.61, 0.84, 1.00 ]
    c_stops = ((ctypes.c_double)*(len(stops)))(*stops)
    red   = [ 0.00, 0.00, 0.87, 1.00, 0.51 ]
    c_red = ((ctypes.c_double)*(len(red)))(*red)
    green = [ 0.00, 0.81, 1.00, 0.20, 0.00 ]
    c_green = ((ctypes.c_double)*(len(green)))(*green)
    blue  = [ 0.51, 1.00, 0.12, 0.00, 0.00 ]
    c_blue = ((ctypes.c_double)*(len(blue)))(*blue)
    R.TColor.CreateGradientColorTable(NRGBs, c_stops, c_red, c_green, c_blue, NCont)
    R.gStyle.SetNumberContours(NCont)

useNiceColorPalette(NCont = 100)

def scanNLL(nll,var1,var2, hname):
    # scan nll
    #print "nll({0:.2f},{1:.2f}) = {2:.2f}".format(slope_met.getVal(),shape_met.getVal(),nll.getVal())
    min1  = var1.getMin()#40#
    max1  = var1.getMax()#70#
    bins1 = var1.getBins()#30#
    min2  = var2.getMin()#0.0#
    max2  = var2.getMax()#0.3#
    bins2 = var2.getBins()#30#
    init_val1 = var1.getVal()
    init_val2 = var2.getVal()
    h_nll = R.TH2F("h_nll_"+hname+"_"+str(var1.GetName())+"_"+str(var2.GetName()),"h_nll_"+hname+"_"+str(var1.GetName())+"_"+str(var2.GetName()),bins1,min1,max1,bins2,min2,max2)
    minnll = nll.getVal()
    for i in range(bins1):
        for j in range(bins2):
            val1 = min1+(i+0.5)*(max1-min1)/bins1
            val2 = min2+(j+0.5)*(max2-min2)/bins2
#            print "."#str(val1)+","+str(val2)
            var1.setVal(val1)
            var2.setVal(val2)
            nllval = nll.getVal()
            if nllval<minnll: minnll = nllval
            h_nll.SetBinContent(h_nll.FindBin(val1,val2),nllval)
    for i in range(bins1):
        for j in range(bins2):
            val1 = min1+(i+0.5)*(max1-min1)/bins1
            val2 = min2+(j+0.5)*(max2-min2)/bins2
            nllval = h_nll.GetBinContent(h_nll.FindBin(val1,val2))
            h_nll.SetBinContent(h_nll.FindBin(val1,val2),nllval-minnll+1)
    var1.setVal(init_val1)
    var2.setVal(init_val2)
    return h_nll

def plotCanvas(c, path):
    try: os.makedirs(path)
    except: print "-> warning: path "+path+" exists... possibly replacing files!"
    c.SaveAs(path+c.GetName()+".png")
    #c.SaveAs(path+c.GetName()+".pdf")
    c.SaveAs(path+c.GetName()+".root")

def setConst(pars):
    itpar = pars.createIterator()
    par = itpar.Next()
    while (not (par == None)):
        par.setConstant(True)
        par = itpar.Next()

def readFromFile(rootfilename, name, newname = ""):
    if newname == "": newname = name
    f = R.TFile(rootfilename)
    f.cd()
    tmp = f.Get(name)
    R.gDirectory.cd("PyROOT:/")
    cl = tmp.Clone(newname)
    f.Close()
    return cl

def makeRatioHist(hist, curve):
    ratio = R.RooHist(hist.getFitRangeBinW())
    xstart = R.Double(0.)
    xstop  = R.Double(0.)
    y      = R.Double(0.)
    curve.GetPoint(0,xstart,y)
    curve.GetPoint(curve.GetN()-1,xstop,y)
    for i in range(hist.GetN()):
        x     = R.Double(0.)
        point = R.Double(0.)
        hist.GetPoint(i,x,point)
        if (x<xstart or x>xstop): continue
        exl = hist.GetErrorXlow(i)
        exh = hist.GetErrorXhigh(i)
        if (exl<=0 ): exl = hist.GetErrorX(i)
        if (exh<=0 ): exh = hist.GetErrorX(i)
        if (exl<=0 ): exl = 0.5*hist.getNominalBinWidth()
        if (exh<=0 ): exh = 0.5*hist.getNominalBinWidth()
        curve_point = curve.average(x-exl,x+exh)#curve.interpolate(x)
        yy = 0
        if not (curve_point == 0.):
            yy = point/curve_point
        dyl = hist.GetErrorYlow(i)
        dyh = hist.GetErrorYhigh(i)
        if (dyl==0. or dyh==0.):
            print "-> makeRatioHist(", hist.GetName(), ", ", curve.GetName(), ") WARNING: point ",  str(i), " has zero error, setting ratio-error to zero"
        else:
            if not (curve_point == 0.):
                dyh = dyh/curve_point
                dyl = dyl/curve_point
        if (yy>0.): ratio.addBinWithError(x,yy,dyl,dyh)
    return ratio

def relError(errcurve, curve):
    ratio = R.RooCurve()
    x = R.Double(0.)
    xerr = R.Double(0.)
    y = R.Double(0.)
    yerr = R.Double(0.)
    for ierr in range(errcurve.GetN()):
        errcurve.GetPoint(ierr,xerr,yerr)
        i = curve.findPoint(xerr)
        curve.GetPoint(i,x,y)
        if not y: continue
        r = yerr/y
        ratio.addPoint(x,r)
    return ratio

btbin = 0
htmin = 0
htmax = 10000

metcut = 150
metmin = metcut
metmax = 1500
metfitmin = 150
metfitmax = 1500
metbinsize = 25

#htcuts = [400., 500., 600., 700., 800., 900., 1000.]

# path to RooFit dataset
path = "/data/kwolf/RA4Fit2012_6j/fitdata/ds_copyMET_MuonElectron_jet1pt40_intLumi-20p0_convertedTuples_v16_mc_with_weight_weight/"

metaxistitle=""

#metname = "genmet"
#cutMu =  "nbtags==2&&singleMuonic     &&  njets>=2 && nvetoMuons==1 && nvetoElectrons==0 && "+metname+">"+str(metmin)+" && ht>"+str(htmin)+" && ht<"+str(htmax)#+" && nbtags=="+str(btbin)
#cutEle = "nbtags==2&&singleElectronic &&  njets>=2 && nvetoElectrons==1 && nvetoMuons==0 && "+metname+">"+str(metmin)+" && ht>"+str(htmin)+" && ht<"+str(htmax)#+" && nbtags=="+str(btbin)
#prefix = "bt2-for-constraint"

#metname = "genmet"
#cutMu =  "singleMuonic     &&  njets>=2 && nvetoMuons==1 && nvetoElectrons==0 && "+metname+">"+str(metmin)+" && ht>"+str(htmin)+" && ht<"+str(htmax)#+" && nbtags=="+str(btbin)
#cutEle = "singleElectronic &&  njets>=2 && nvetoElectrons==1 && nvetoMuons==0 && "+metname+">"+str(metmin)+" && ht>"+str(htmin)+" && ht<"+str(htmax)#+" && nbtags=="+str(btbin)
#prefix = "only-wjets"
#signal=""

metname = "type1phiMet"
cutMu =  "nbtags>=1&&nbtags<=2&&singleMuonic     && leptonPt>30&&abs(leptonEta)<2.1&& njets>=2 && nvetoMuons==1 && nvetoElectrons==0 && "+metname+">"+str(metmin)+" && ht>"+str(htmin)+" && ht<"+str(htmax)#+" && nbtags=="+str(btbin)
cutEle = "nbtags>=1&&nbtags<=2&&singleElectronic && leptonPt>30&&abs(leptonEta)<2.1&& njets>=2 && nvetoElectrons==1 && nvetoMuons==0 && "+metname+">"+str(metmin)+" && ht>"+str(htmin)+" && ht<"+str(htmax)#+" && nbtags=="+str(btbin)
#signal="T1tttt_1100_100"
signal=""
prefix = "bt1+2-lEta21-new-nosignal"

if metname=="genmet": metaxistitle="generator #slash{E}_{T} [GeV]"
else: metaxistitle="#slash{E}_{T} [GeV]"

filename = '/afs/hephy.at/user/s/schoefbeck/www/InclFits2/output/incl_'+prefix+'.pkl'
njbins =  [[2,2],[3,3],[4,4],[5,5],[6,99]]

if os.path.isfile(filename):
  res = pickle.load(file(filename))
else: 
  os.system("root -l -q -b load.cc")
  R.gSystem.Load("/afs/cern.ch/cms/slc5_amd64_gcc462/external/boost/1.51.0/lib/libboost_math_tr1.so")
  R.gSystem.Load("RooMinuitSumW2_cxx.so")
  R.gSystem.Load("RooSkewErf_cxx.so")
  R.gSystem.Load("RooPareto_cxx.so")
  R.gSystem.Load("RooMETConv_cxx.so")
  R.gStyle.SetOptTitle(0)

  R.RooAbsReal.defaultIntegratorConfig().getConfigSection("RooIntegrator1D").setRealValue("maxSteps",30);

  f_setup = open(path+"setup_dataset.pkl","r")
  setup = pickle.load(f_setup)
  print setup
  arg_vars = setup["vars"]
  weight = arg_vars.find(setup["weight"])#"weightLumi"
  met = arg_vars.find(metname)
  ht = arg_vars.find("ht")

  #for nj in [[6,99]]:#,[3,3],[4,4],[5,5],[6,99]]:
  res={}
  for mode in ["mc", "data"]:
    if mode=="data" and metname=="genmet":continue
    res[mode]={}
    for nj in njbins:
      if mode=="mc":
        title = "simulation"
      else:
        title = "data"
      res[mode][tuple(nj)]={}
      dataset = R.RooDataSet( "dataset", "dataset", arg_vars, RF.WeightVar(weight) )
      ##bg_wjets = R.RooDataSet( "bg_wjets", "bg_wjets", arg_vars, RF.WeightVar(weight) )
      #data = R.RooDataSet( "data", "data", arg_vars, RF.WeightVar(weight) )
      if mode=="mc":

        f_ds_WJetsCombined_mu = R.TFile.Open(path+"bg/dataset_Mu_WJetsCombined.root","READ")                                
        WJetsCombined_mu = f_ds_WJetsCombined_mu.Get("dataset_Mu_WJetsCombined")
        WJetsCombined_mu_cut = WJetsCombined_mu.reduce(cutMu+"&&njets>="+str(nj[0])+"&&njets<="+str(nj[1]))
        dataset.append(WJetsCombined_mu_cut)#FIXME

        f_ds_WJetsCombined_ele = R.TFile.Open(path+"bg/dataset_Ele_WJetsCombined.root","READ")
        WJetsCombined_ele = f_ds_WJetsCombined_ele.Get("dataset_Ele_WJetsCombined")
        WJetsCombined_ele_cut = WJetsCombined_ele.reduce(cutEle+"&&njets>="+str(nj[0])+"&&njets<="+str(nj[1]))
        dataset.append(WJetsCombined_ele_cut)

        if not mode=="only-wjets":
          f_ds_ttjets_mu = R.TFile.Open(path+"bg/dataset_Mu_TTJets-PowHeg.root","READ")                                
          ttjets_mu = f_ds_ttjets_mu.Get("dataset_Mu_TTJets-PowHeg")
          ttjets_mu_cut = ttjets_mu.reduce(cutMu+"&&njets>="+str(nj[0])+"&&njets<="+str(nj[1]))
          dataset.append(ttjets_mu_cut)

          f_ds_ttjets_ele = R.TFile.Open(path+"bg/dataset_Ele_TTJets-PowHeg.root","READ")
          ttjets_ele = f_ds_ttjets_ele.Get("dataset_Ele_TTJets-PowHeg")
          ttjets_ele_cut = ttjets_ele.reduce(cutEle+"&&njets>="+str(nj[0])+"&&njets<="+str(nj[1]))
          dataset.append(ttjets_ele_cut)

          f_ds_singleTop_mu = R.TFile.Open(path+"bg/dataset_Mu_singleTop.root","READ")                                
          singleTop_mu = f_ds_singleTop_mu.Get("dataset_Mu_singleTop")
          singleTop_mu_cut = singleTop_mu.reduce(cutMu+"&&njets>="+str(nj[0])+"&&njets<="+str(nj[1]))
          dataset.append(singleTop_mu_cut)#FIXME

          f_ds_singleTop_ele = R.TFile.Open(path+"bg/dataset_Ele_singleTop.root","READ")
          singleTop_ele = f_ds_singleTop_ele.Get("dataset_Ele_singleTop")
          singleTop_ele_cut = singleTop_ele.reduce(cutEle+"&&njets>="+str(nj[0])+"&&njets<="+str(nj[1]))
          dataset.append(singleTop_ele_cut)

        if signal!="":
          f_ds_signal_mu = R.TFile.Open(path+"signal/dataset_Mu_"+signal+".root","READ")                                
          signal_mu = f_ds_signal_mu.Get("dataset_Mu_"+signal)
          signal_mu_cut = signal_mu.reduce(cutMu+"&&njets>="+str(nj[0])+"&&njets<="+str(nj[1]))
          dataset.append(signal_mu_cut)

          f_ds_signal_ele = R.TFile.Open(path+"signal/dataset_Ele_"+signal+".root","READ")
          signal_ele = f_ds_signal_ele.Get("dataset_Ele_"+signal)
          signal_ele_cut = signal_ele.reduce(cutEle+"&&njets>="+str(nj[0])+"&&njets<="+str(nj[1]))
          dataset.append(signal_ele_cut)

      if mode=="data":
        f_ds_singleLepton_mu = R.TFile.Open(path+"data/dataset_Mu_singleMuData.root","READ")                                
        singleLepton_mu = f_ds_singleLepton_mu.Get("dataset_Mu_singleMuData")
        singleLepton_mu_cut = singleLepton_mu.reduce(cutMu+"&&njets>="+str(nj[0])+"&&njets<="+str(nj[1]))
        dataset.append(singleLepton_mu_cut)

        f_ds_singleLepton_ele = R.TFile.Open(path+"data/dataset_Ele_singleEleData.root","READ")
        singleLepton_ele = f_ds_singleLepton_ele.Get("dataset_Ele_singleEleData")
        singleLepton_ele_cut = singleLepton_ele.reduce(cutEle+"&&njets>="+str(nj[0])+"&&njets<="+str(nj[1]))
        dataset.append(singleLepton_ele_cut)

      ###################
      # fit
      ###################
      met.setBins((metmax-metmin)/metbinsize)
      met.setRange("normRange",metmin,metmax)
      met.setRange("fitRange",metfitmin,metfitmax)
      met.setRange("plotRange",metmin,metmax)


      met_min = R.RooRealVar("met_min","met_min",metcut)

      a_ttjets = R.RooRealVar("a_met_ttjets","#alpha",45.,15.,85.)
      a_ttjets.setBins(50)
      b_ttjets = R.RooRealVar("b_met_ttjets","#beta",0.05,0.0001,0.5)
      b_ttjets.setBins(50)

      met_pdf_ttjets      = R.RooPareto("met_pdf_ttjets"     ,"met_pdf_ttjets"     ,met,met_min,a_ttjets,b_ttjets)
      #met_pdf_ttjets.fitTo(bg_ttjets, RF.Range("fitRange"),RF.Save(True), RF.SumW2Error(True))
      addnll = R.RooArgSet()
      nll_ttjets = met_pdf_ttjets.createNLL(dataset, RF.Range("fitRange"))
      addnll.add(nll_ttjets)

      nll = R.RooAddition("nll","nll", addnll)

      minuit = R.RooMinuitSumW2(nll)
      minuit.setStrategy(1)
      minuit.setPrintEvalErrors(-1)
      minuit.setPrintLevel(3)
      minuit.optimizeConst(False)

      minuit.hesse(False)
      minuit.migrad(False)
      minuit.hesse(True)
      fitres = minuit.save("fitres","fitres")
      fitres.Print()

      #line_ttjets_a = R.TLine(htcuts[0], a_ttjets.getVal(), htcuts[-1], a_ttjets.getVal())
      #line_b_ttjets = R.TLine(htcuts[0], b_ttjets.getVal(), htcuts[-1], b_ttjets.getVal())

      n_met_ttjets = dataset.sumEntries(metname+">"+str(metmin)+"&&"+metname+"<"+str(metmax))
      f_met_ttjets = met.frame(metmin,metmax,(metmax-metmin)/metbinsize)
      dataset.plotOn(f_met_ttjets, RF.Name("data_ttjets"),RF.Title(title))
      met_pdf_ttjets.plotOn(f_met_ttjets, RF.Name("fit_ttjets_error"), RF.Precision(10.e-07), RF.Range("plotRange"), RF.NormRange("normRange"), RF.Normalization(n_met_ttjets,R.RooAbsReal.NumEvent), RF.FillColor(R.kBlack), RF.FillStyle(3002), RF.VisualizeError(fitres,1,True))
      met_pdf_ttjets.plotOn(f_met_ttjets, RF.Name("fit_ttjets"),RF.Title("Fit"), RF.Precision(10.e-07), RF.Range("plotRange"), RF.NormRange("normRange"), RF.Normalization(n_met_ttjets,R.RooAbsReal.NumEvent), RF.LineColor(R.kBlack))
      dataset.plotOn(f_met_ttjets, RF.Name("data_ttjets"))


      h_metNLL = scanNLL(nll,a_ttjets,b_ttjets, "h_metNLL")
      #metNLLProfile = nll.createProfile(R.RooArgSet(a_ttjets,b_ttjets))
      #h_metNLL = metNLLProfile.createHistogram("h_metNLL", a_ttjets, RF.YVar(b_ttjets))

      f_ab_met = R.RooPlot(a_ttjets,b_ttjets)
      f_ab_met.SetTitle("NLL of f(#slash{E}_{T},#alpha_{#slash{E}_{T}},#beta_{#slash{E}_{T}})")
      fitres.plotOn(f_ab_met, a_ttjets, b_ttjets, "ME12")


      ###################
      # draw
      ###################
      line_ratio = R.TLine(metmin,1.,metmax,1.)

      xlow = R.Double(0)
      ylow = R.Double(0)
      xhi = R.Double(0)
      yhi = R.Double(0)

      r = 0.3
      fac_size = 1.3

      c_met = R.TCanvas("c_met_{0:.0f}_met_{1:.0f}".format(metfitmin,metfitmax),"c_met_{0:.0f}_met_{1:.0f}".format(metfitmin,metfitmax),800,600)
      pad = c_met.cd()
      pad.GetPadPar(xlow,ylow,xhi,yhi)
      pad_plot = R.TPad("pad_plot", "pad_plot", xlow, ylow+(yhi-ylow)*r, xhi, yhi)
      pad_plot.Draw()
      pad_plot.cd()
      f_met_ttjets.SetMinimum(5e-3)
      f_met_ttjets.SetMaximum(2e4)
      f_met_ttjets.Draw()
      xaxis = f_met_ttjets.GetXaxis()
      xaxis.SetTitle(metaxistitle)
      xaxis.SetTitleSize(xaxis.GetTitleSize()*fac_size)
      xaxis.SetLabelSize(xaxis.GetLabelSize()*fac_size)
      yaxis = f_met_ttjets.GetYaxis()
      yaxis.SetTitle("Events / {0:.0f} GeV".format(metbinsize))
      yaxis.SetTitleSize(yaxis.GetTitleSize()*fac_size)
      yaxis.SetLabelSize(yaxis.GetLabelSize()*fac_size)

      R.gPad.SetLogy()

      txt = R.TLatex()
      txt.SetNDC()
      txt.SetTextSize(txt.GetTextSize()*fac_size)
      txt.DrawLatex(0.2,0.8,"CMS Simulation")
      txt.DrawLatex(0.2,0.7, "19.4 fb^{-1}, #sqrt{s} = 8 TeV")
      txt.DrawLatex(0.65,0.65, str(nj[0])+"#leq n-jets #leq"+str(nj[1]))
      txt.DrawLatex(0.65,0.58, "a = "+str(round(a_ttjets.getVal(), 2))+" #pm "+ str(round(a_ttjets.getError(), 2)))
      txt.DrawLatex(0.65,0.51, "b = "+str(round(b_ttjets.getVal(), 3))+" #pm "+ str(round(b_ttjets.getError(), 3)))

      leg = R.TLegend(0.6,0.75,1-R.gStyle.GetPadRightMargin(),1-R.gStyle.GetPadTopMargin())
      leg.SetFillColor(R.kWhite)

      hist_ttjets = f_met_ttjets.getHist("data_ttjets")
      curve_ttjets = f_met_ttjets.getCurve("fit_ttjets")
      leg.AddEntry(hist_ttjets,title,"pl")
      leg.AddEntry(curve_ttjets,"fit","l")
      leg.Draw()

      f_met_ttjets_ratio = met.frame( RF.Range(metmin,metmax), RF.Bins((metmax-metmin)/metbinsize), RF.Title("") )
      curve_ttjets_error = f_met_ttjets.getCurve("fit_ttjets_error")
      ratio_ttjets = makeRatioHist(hist_ttjets, curve_ttjets)
      ratio_ttjets.SetLineColor(R.kBlack)
      ratio_ttjets.SetLineWidth(2)
      ratio_ttjets.SetMarkerColor(R.kBlack)
      ratio_ttjets.SetMarkerStyle(20)
      ratio_ttjets_error = relError(curve_ttjets_error, curve_ttjets)
      ratio_ttjets_error.SetFillColor(R.kBlack)
      ratio_ttjets_error.SetFillStyle(3002);
      f_met_ttjets_ratio.addPlotable(ratio_ttjets_error,"f")
      f_met_ttjets_ratio.addPlotable(ratio_ttjets,"pe");
      c_met.cd()
      pad_ratio = R.TPad("pad_ratio", "pad_ratio", xlow, ylow, xhi, ylow+(yhi-ylow)*r)
      pad_ratio.Draw()
      pad_ratio.cd()
      f_met_ttjets_ratio.SetMinimum(0)
      f_met_ttjets_ratio.SetMaximum(2.25)
      f_met_ttjets_ratio.Draw()
      xaxis = f_met_ttjets_ratio.GetXaxis()
      xaxis.SetTitle(metaxistitle)
      xaxis.SetLabelSize(xaxis.GetLabelSize()*((1-r)/r)*fac_size)
      xaxis.SetTitleSize(xaxis.GetTitleSize()*((1-r)/r)*fac_size)

      yaxis = f_met_ttjets_ratio.GetYaxis()
      yaxis.SetTitle("Ratio")
      yaxis.SetNdivisions(505)
      yaxis.SetLabelSize(yaxis.GetLabelSize()*((1-r)/r)*fac_size)
      yaxis.SetTitleSize(yaxis.GetTitleSize()*((1-r)/r)*fac_size)
      yaxis.SetTitleOffset(yaxis.GetTitleOffset()/((1-r)/r))


      pad_ratio.SetBottomMargin(pad_plot.GetBottomMargin()*((1-r)/r)*fac_size)
      pad_plot.SetBottomMargin(0.001)
      pad_ratio.SetTopMargin(0.001)

      line_ratio.Draw("same")


      c_met.Update()
      plotCanvas(c_met, "/afs/hephy.at/user/s/schoefbeck/www/InclFits2/output/incl_"+prefix+"_"+mode+"_njets_"+str(nj[0])+"_"+str(nj[1])+"_"+metname+"_fits/")

      c_nll = R.TCanvas("c_nll_{0:.0f}_met_{1:.0f}".format(metfitmin,metfitmax),"c_nll_{0:.0f}_met_{1:.0f}".format(metfitmin,metfitmax),800,400)
      f_ab_met.Draw()
      h_metNLL.Draw("cont1Zsame")
      R.gPad.SetLogz()
      xaxis = f_ab_met.GetXaxis()
      xaxis.SetLabelSize(xaxis.GetLabelSize()*1.5)
      xaxis.SetTitleSize(xaxis.GetTitleSize()*1.5)
      yaxis = f_ab_met.GetYaxis()
      yaxis.SetLabelSize(yaxis.GetLabelSize()*1.5)
      yaxis.SetTitleSize(yaxis.GetTitleSize()*1.5)

      c_nll.Update()
      plotCanvas(c_nll, "/afs/hephy.at/user/s/schoefbeck/www/InclFits2/output/incl_"+prefix+"_"+mode+"_njets_"+str(nj[0])+"_"+str(nj[1])+"_"+metname+"_fits/")

      res[mode][tuple(nj)]['fitRes'] = fitres.Clone()
      res[mode][tuple(nj)]['a'] = a_ttjets.getVal()
      res[mode][tuple(nj)]['sigma_a'] = a_ttjets.getError()
      res[mode][tuple(nj)]['b'] = b_ttjets.getVal()
      res[mode][tuple(nj)]['sigma_b'] = b_ttjets.getError()

  pickle.dump(res, file(filename,'w'))

R.gROOT.ProcessLine(".L ../../Scripts/aclic/tdrstyle.C")
R.setTDRStyle()

aData = R.TH1F("aData","aData", 4, 1.5, 5.5)
bData = R.TH1F("bData","bData", 4, 1.5, 5.5)
aMC = R.TH1F("aMC","aMC", 4, 1.5, 5.5)
bMC = R.TH1F("bMC","bMC", 4, 1.5, 5.5)

for nj in njbins:
  bin = aData.FindBin(0.5*(nj[0]+nj[1])) 
  aData.SetBinContent(bin, res["data"][tuple(nj)]['a'])
  aData.SetBinError(bin, res["data"][tuple(nj)]['sigma_a'])
  bData.SetBinContent(bin, res["data"][tuple(nj)]['b'])
  bData.SetBinError(bin, res["data"][tuple(nj)]['sigma_b'])
  aMC.SetBinContent(bin, res["mc"][tuple(nj)]['a'])
  aMC.SetBinError(bin, 0.)
  bMC.SetBinContent(bin, res["mc"][tuple(nj)]['b'])
  bMC.SetBinError(bin, 0)

c1 = R.TCanvas()
aData.GetYaxis().SetRangeUser(25, 65)
aData.GetYaxis().SetTitle("#alpha")
aData.GetXaxis().SetTitle("nr. of jets")
aData.GetXaxis().SetBinLabel(1,"2");
aData.GetXaxis().SetBinLabel(2,"3");
aData.GetXaxis().SetBinLabel(3,"4");
aData.GetXaxis().SetBinLabel(4,"5");
aData.GetXaxis().SetLabelSize(0.08);

aData.Draw()
aMC.SetMarkerStyle(0)
aMC.SetMarkerColor(R.kRed)
aMC.SetLineColor(R.kRed)
aMC.SetMarkerSize(0)

l = R.TLegend(0.55,0.75,.95,.95)
l.SetFillColor(0)
l.SetShadowColor(R.kWhite)
l.SetBorderSize(1)
l.AddEntry(aMC, "Simulation")
l.AddEntry(aData, "Data")
l.Draw()

drawObjs = []
for nj in njbins[:-1]:
  bin = aData.FindBin(0.5*(nj[0]+nj[1])) 
  box = R.TBox(nj[0]-0.5, res["mc"][tuple(nj)]['a'] - res["mc"][tuple(nj)]['sigma_a'], nj[0]+0.5, res["mc"][tuple(nj)]['a'] + res["mc"][tuple(nj)]['sigma_a'])
#  box.SetFillStyle(3004)
  box.SetFillColor(R.kYellow)
  drawObjs.append(box)

for o in drawObjs:
  o.Draw()

aMC.Draw("E0same")
aData.Draw("same")
c1.Print("/afs/hephy.at/user/s/schoefbeck/www/InclFits2/plots/a_"+prefix+".png")
c1.Print("/afs/hephy.at/user/s/schoefbeck/www/InclFits2/plots/a_"+prefix+".pdf")
c1.Print("/afs/hephy.at/user/s/schoefbeck/www/InclFits2/plots/a_"+prefix+".root")
bData.GetYaxis().SetRangeUser(0, 0.3)
bData.GetYaxis().SetTitle("#beta")
bData.GetXaxis().SetTitle("nr. of jets")
bData.GetXaxis().SetBinLabel(1,"2");
bData.GetXaxis().SetBinLabel(2,"3");
bData.GetXaxis().SetBinLabel(3,"4");
bData.GetXaxis().SetBinLabel(4,"5");
bData.GetXaxis().SetLabelSize(0.08);


bData.Draw()
bMC.SetMarkerStyle(0)
bMC.SetMarkerColor(R.kRed)
bMC.SetLineColor(R.kRed)
bMC.SetMarkerSize(0)

l = R.TLegend(0.55,0.75,.95,.95)
l.SetFillColor(0)
l.SetShadowColor(R.kWhite)
l.SetBorderSize(1)
l.AddEntry(bMC, "Simulation")
l.AddEntry(bData, "Data")
l.Draw()

drawObjs = []
for nj in njbins[:-1]:
  bin = bData.FindBin(0.5*(nj[0]+nj[1])) 
  box = R.TBox(nj[0]-0.5, res["mc"][tuple(nj)]['b'] - res["mc"][tuple(nj)]['sigma_b'], nj[0]+0.5, res["mc"][tuple(nj)]['b'] + res["mc"][tuple(nj)]['sigma_b'])
#  box.SetFillStyle(3004)
  box.SetFillColor(R.kYellow)
  drawObjs.append(box)

for o in drawObjs:
  o.Draw()

bMC.Draw("E0same")

bData.Draw("same")
c1.Print("/afs/hephy.at/user/s/schoefbeck/www/InclFits2/plots/b_"+prefix+".png")
c1.Print("/afs/hephy.at/user/s/schoefbeck/www/InclFits2/plots/b_"+prefix+".pdf")
c1.Print("/afs/hephy.at/user/s/schoefbeck/www/InclFits2/plots/b_"+prefix+".root")
del c1

