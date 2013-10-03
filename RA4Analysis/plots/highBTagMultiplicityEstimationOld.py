from analysisHelpers import *
import ROOT
from simplePlotsCommon import *
from simpleStatTools import niceNum
import os, pickle, copy


small = False

sysmode = ""
subDir = "copyMET"
c = ROOT.TChain("Events")
c.Add("/data/schoef/convertedTuples_v13/"+subDir+"/Mu/TTJets-PowHeg/histo_TTJets-PowHeg.root")
c.Add("/data/schoef/convertedTuples_v13/"+subDir+"/Ele/TTJets-PowHeg/histo_TTJets-PowHeg.root")

cData = ROOT.TChain("Events")
cData.Add("/data/schoef/convertedTuples_v13//copyMET/Mu/data/histo_data.root")
cData.Add("/data/schoef/convertedTuples_v13//copyMET/Ele/data/histo_data.root")

cSignal = ROOT.TChain("Events")
cSignal.Add("/data/schoef/convertedTuples_v12/"+subDir+"/Mu/T1tttt_1000_100/histo_T1tttt_1000_100.root")
cSignal.Add("/data/schoef/convertedTuples_v12/"+subDir+"/Ele/T1tttt_1000_100/histo_T1tttt_1000_100.root")

#lumiScale = 20000./(5000. + 6303 + 489)

minNJet = 4

htbins = [\
    [400,450   ],
    [450,500   ],
    [500,550   ],
    [550,600   ],
    [600,650   ],
    [650,700   ],
    [700,750   ],
    [750,800   ],
    [800,1000  ],
    [1000,1200 ],
    [1200,1500 ],
    [1500,2500 ]
  ]

metbins = [\
    [150, 250],
    [250, 350],
    [350, 450],
    [450, 2500]]

if small:
  htbins = htbins[:1]
#  metbins = metbins[3:]

leptonCut = "((singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)||(singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))&&run<=196531"

#btagModes = ["_SF"]
btagModes = ["SF", "SF_b_Up", "SF_b_Down", "SF_light_Up", "SF_light_Down"]
#if small:
#  btagModes = btagModes[:1]

def getBTagCut(s):
  if s[-1]=="p":
    return "nbtags>="+s[0]
  else:
    return "nbtags=="+s[0]

outfile = "/data/schoef/results2012/btagEff/highBTagMultiplicityEstimation_v13_"+sysmode+"_"+str(minNJet)+"j.pkl"
binnedYield = {}
histo={}
for nbtb, btb in enumerate(["2", "3","4p"]):
  histo[btb] = {}
  binnedYield [btb] = {}
  for mode in btagModes:
    binnedYield [btb][mode] = {}
    for htb in htbins:
      binnedYield [btb][mode][tuple(htb)] = {}
      for metb in metbins:
        binnedYield [btb][mode][tuple(htb)][tuple(metb)] = {"MC_sumW":0., "MC_sumW2":0., "MC_count":0, "signal_sumW":0., "signal_sumW2":0., "signal_count":0} 

if not os.path.isfile(outfile):
  print "Not found",outfile,"-> calculate"
  for nbtb, btb in enumerate(["2", "3","4p"]):
    for mode in btagModes:
      print "At btb",btb,"mode",mode
      mmode = mode
      if mode!="":
        mmode = "_"+mode
      cut = "weightBTag"+btb+mmode+"*(njets>="+str(minNJet)+"&&ht>400&&met>150&&"+leptonCut+")"
      c.Draw("met>>hmetBT"+btb+mmode+"(21,0,1050)", cut)
      histo[btb][mode] = ROOT.gDirectory.Get("hmetBT"+btb+mmode)
      histo[btb][mode].SetLineColor(ROOT_colors[nbtb])
      histo[btb][mode].SetLineStyle(0)
      histo[btb][mode].SetLineWidth(0)
      histo[btb][mode].SetMarkerColor(ROOT_colors[nbtb])
      histo[btb][mode].SetMarkerStyle(0);
      histo[btb][mode].GetXaxis().SetTitle("#slash{E}_{T} (GeV)")
      histo[btb][mode].GetYaxis().SetTitle("Number of Events / 50 GeV")

  c1 = ROOT.TCanvas()
  c1.SetLogy()
  for nmode, mode in enumerate(btagModes):
    mmode = mode
    if mode!="":
      mmode = "_"+mode
    l = ROOT.TLegend(0.5,0.7,1,1.0)
    l.SetFillColor(0)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    compH = histo["2"][mode].Clone("compH")
    histo["2"][mode].Draw()
    compH.Scale(histo["3"][mode].Integral()/compH.Integral())
    compH.SetLineStyle(2)
    stuff.append(compH.DrawClone("same"))
    l.AddEntry(histo["2"][mode], "weightBTag2"+mmode)
    histo["3"][mode].Draw("same")
    
    compH.Scale(histo["4p"][mode].Integral()/compH.Integral())
    compH.SetLineStyle(2)
    stuff.append(compH.DrawClone("same"))
    l.AddEntry(histo["3"][mode], "weightBTag3"+mmode)
    histo["4p"][mode].Draw("same")
    l.AddEntry(histo["4p"][mode], "weightBTag4p"+mmode)
    l.Draw()
    thisfile = "/afs/hephy.at/user/s/schoefbeck/www/pngBTag/highBTagMETShapes_"+str(minNJet)+"j_"+mmode+".png"
    print "Writing ",thisfile
    c1.Print(thisfile)

  for chain in [c, cSignal]:
    chain.Draw(">>eList","(njets>="+str(minNJet)+"&&ht>400&&met>150&&"+leptonCut+")")
    elist = ROOT.gDirectory.Get("eList")
    number_events = elist.GetN()
    ntot = chain.GetEntries()
  #  if small:
  #    if number_events>200:
  #      number_events=200
    for i in range(0, number_events):
      if (i%10000 == 0) and i>0 : 
        print i,"/",number_events 
    #      # Update all the Tuples
      if elist.GetN()>0 and ntot>0:
        chain.GetEntry(elist.GetEntry(i))
        for nbtb, btb in enumerate(["2", "3","4p"]):
          for mode in btagModes:
            mmode = mode
            if mode!="":
              mmode = "_"+mode
            weight = chain.GetLeaf("weightBTag"+btb+mmode).GetValue()
            if btb=="4p" and weight<0.: weight = 0.
    #        print "weightBTag"+btb+mode, weight
            ht = chain.GetLeaf("ht").GetValue()
            met = chain.GetLeaf("met").GetValue()
            for metb in metbins:
              if met>=metb[0] and met<metb[1]:
                for htb in htbins:
                  if ht>=htb[0] and ht<htb[1]:
                    if chain==c:
                      binnedYield[btb][mode][tuple(htb)][tuple(metb)]["MC_count"] += 1
                      binnedYield[btb][mode][tuple(htb)][tuple(metb)]["MC_sumW"]  += (weight*lumiScale)
                      binnedYield[btb][mode][tuple(htb)][tuple(metb)]["MC_sumW2"] += (weight*lumiScale)**2
                    if chain==cSignal:
                      binnedYield[btb][mode][tuple(htb)][tuple(metb)]["signal_count"] += 1
                      binnedYield[btb][mode][tuple(htb)][tuple(metb)]["signal_sumW"]  += (weight*lumiScale)
                      binnedYield[btb][mode][tuple(htb)][tuple(metb)]["signal_sumW2"] += (weight*lumiScale)**2
  del elist
  if not small:
    pickle.dump([histo, binnedYield], file(outfile, "w"))
  else:
    print "No saving when small!"
else:
  print "Found",outfile,"-> load results."
  histo, binnedYield = pickle.load(file(outfile))

#SpF = pickle.load(file('/data/schoef/results2012/btagEff/SpF.pkl'))
SpF = pickle.load(file('/data/schoef/results2012/btagEff/SpF_HT400MET150_11fb.pkl'))

metControlBin = metbins[0]
yieldDefDict = {"data":0,"MC":0., "Var_MC":0., "signal":0.,"Var_signal":0.,\
  "MC_predictedYield_fromb2_METshapeSpFCorr":0., 
  "MC_predictedYield_fromb2_METshapeSpFUncorr":0., 
  "Var_MC_predictedYield_fromb2_METshapeSpFCorr":0.,   
  "Var_MC_predictedYield_fromb2_METshapeSpFUncorr":0.,
  "MC_predictedYield_frombtb_METshapeSpFCorr":0., 
  "MC_predictedYield_frombtb_METshapeSpFUncorr":0.,
  "data_predictedYield_fromb2_METshapeSpFCorr":0., 
  "data_predictedYield_fromb2_METshapeSpFUncorr":0., 
  "data_predictedYield_frombtb_METshapeSpFCorr":0., 
  "data_predictedYield_frombtb_METshapeSpFUncorr":0.,
}

#Calculating estimation in 2b bin
def calcY(h, m):
  return h.Integral(h.FindBin(m[0]), h.FindBin(m[1]))

def getMetRatioFromWK(inDir, htb, contBin, sigBin, retMetShape=False):
  btb = "bt3"
#  metShapeF = ROOT.TFile('/afs//hephy.at/scratch/k/kwolf/CMSSW_5_2_3_patch1/src/Workspace/RA4Fit2012/output/Results_fitMC_MuonElectron_jet3pt40_intLumi-11p792_121108_1747/h_conv_sumcharge_sumpdf_met_ht_'+str(htb[0])+'_'+str(htb[1])+'_'+btb+'__met.root')
  print "indir", inDir
#  metShapeF = ROOT.TFile(inputDir[sysmode]+'/h_conv_sumcharge_sumpdf_met_ht_'+str(htb[0])+'_'+str(htb[1])+'_'+btb+'__met.root')
#  htmp = metShapeF.Get('h_conv_sumcharge_sumpdf_met_ht_'+str(htb[0])+'_'+str(htb[1])+'_'+btb+'__met')
  metShape = getObjFromFile(inDir+'/h_conv_sumcharge_sumpdf_met_ht_'+str(htb[0])+'_'+str(htb[1])+'_'+btb+'__met.root', 'h_conv_sumcharge_sumpdf_met_ht_'+str(htb[0])+'_'+str(htb[1])+'_'+btb+'__met')
  res =  calcY(metShape, sigBin)/calcY(metShape, contBin)
  if retMetShape:
    return res, metShape
  del metShape
  return res 

controlYield = {}
yields = {}
for btb in ["3", "4p"]:
  spfBin = btb+"o2"
  controlYield[btb] = {}
  yields      [btb] = {}
  for mode in btagModes:
    controlYield[btb][mode] = {}
    yields      [btb][mode] = {}
    for htb in htbins:
      controlYield[btb][mode][htb[0]] = {"data":0., "MC_predictedYield_from2b":0., "MC":0.}
      yields      [btb][mode][htb[0]] = {}
      for metb in metbins:
        yields[btb][mode][htb[0]][metb[0]] = copy.deepcopy(yieldDefDict)

#        print "ht",htb,"metb", metb, MetRatioUncorr_MC , getMetRatioFromWK(htb, metControlBin, metb)
#        MetRatioUncorr_MC = binnedYield["2"][mode][tuple(htb)][tuple(metb)]["MC_sumW"] / binnedYield["2"][mode][tuple(htb)][tuple(metControlBin)]["MC_sumW"]
        MetRatioUncorr_MC = getMetRatioFromWK(goodDirectories['MC_central'], htb, metControlBin, metb) 
        MetRatioCorr_MC = MetRatioUncorr_MC
        corrfac = SpF[tuple(htb)][tuple(metb)][-1][mode][spfBin]['rTrue']/SpF[tuple(htb)][tuple(metControlBin)][-1][mode][spfBin]['rTrue']
        if corrfac<float('inf'):
          MetRatioCorr_MC = MetRatioUncorr_MC*corrfac
#      MetRatioUncorr_MCVar = MetRatioUncorr_MC**2*(binnedYield["2"][mode][tuple(htb)][tuple(metb)]["MC_sumW2"]/binnedYield["2"][mode][tuple(htb)][tuple(metb)]["MC_sumW"]**2 + binnedYield["2"][mode][tuple(htb)][tuple(metControlBin)]["MC_sumW2"]/binnedYield["2"][mode][tuple(htb)][tuple(metControlBin)]["MC_sumW"]**2) 
#        MetRatioCorr_MCVar = MetRatioCorr_MC**2*(MetRatioUncorr_MCVar/MetRatioUncorr_MC**2 + SpF[tuple(htb)][tuple(metb)][-1][mode][spfBin]['RMS']**2 / SpF[tuple(htb)][tuple(metb)][-1][mode][spfBin]['rTrue']**2 + SpF[tuple(htb)][tuple(metControlBin)][-1][mode][spfBin]['RMS']**2 / SpF[tuple(htb)][tuple(metControlBin)][-1][mode][spfBin]['rTrue']**2)

        b2_normRegYield_MC  = binnedYield["2"][mode][tuple(htb)][tuple(metControlBin)]["MC_sumW"]                              #2b control region yield
        btb_fromb2_normRegYield_MC  = b2_normRegYield_MC*SpF[tuple(htb)][tuple(metControlBin)][-1][mode][spfBin]['rTrue']   #btb control region yield from 2b bin
        varStat_btb_fromb2_normRegYield_MC  = b2_normRegYield_MC*SpF[tuple(htb)][tuple(metControlBin)][-1][mode][spfBin]['rTrue']**2   #btb control region yield from 2b bin
        btb_normRegYield_MC        = binnedYield[btb][mode][tuple(htb)][tuple(metControlBin)]["MC_sumW"]   #btb control region yield
        
        print "\nMC Truth","\nht/met:",htb, metb, "mode", mode,"btb",btb
        print "Normalization region yield:                            true:",binnedYield[btb][mode][tuple(htb)][tuple(metControlBin)]["MC_sumW"], "est. from SpF:", btb_fromb2_normRegYield_MC , "(using in 2b:",b2_normRegYield_MC,")" 
        print "MetRatio prediction using 2b contr. reg.: uncorr. met-ratio:", btb_fromb2_normRegYield_MC*MetRatioUncorr_MC, \
                                                                    " corr:", btb_fromb2_normRegYield_MC*MetRatioCorr_MC, "MC truth:", binnedYield[btb][mode][tuple(htb)][tuple(metb)]["MC_sumW"]
#        print "sigma(MetRatio) uncorr.",sqrt(MetRatioUncorr_MCVar)#,"corr.",sqrt(MetRatioCorr_MCVar)

        #DATA
        MetRatioCorr_data = MetRatioCorr_MC 
        MetRatioUncorr_data = MetRatioUncorr_MC
        sigRegYield_data = cData.GetEntries(leptonCut+"&&ht>="+str(htb[0])+"&&ht<"+str(htb[1])+"&&met>="+str(metb[0])+"&&met<"+str(metb[1])+"&&njets>="+str(minNJet)+"&&"+getBTagCut(btb)) 
         
        b2_normRegYield_data          = cData.GetEntries(leptonCut+"&&ht>="+str(htb[0])+"&&ht<"+str(htb[1])+"&&met>="+str(metControlBin[0])+"&&met<"+str(metControlBin[1])+"&&njets>="+str(minNJet)+"&&nbtags==2") 
        btb_fromb2_normRegYield_data   = b2_normRegYield_data*SpF[tuple(htb)][tuple(metControlBin)][-1][mode][spfBin]['rTrue'] 
        btb_normRegYield_data         = cData.GetEntries(leptonCut+"&&ht>="+str(htb[0])+"&&ht<"+str(htb[1])+"&&met>="+str(metControlBin[0])+"&&met<"+str(metControlBin[1])+"&&njets>="+str(minNJet)+"&&"+getBTagCut(btb)) 
#        print btb_fromb2_normRegYield_data, btb_normRegYield_data
        print "Data"
        print "Normalization region yield:                                :", btb_normRegYield_data, "est. from SpF:", btb_fromb2_normRegYield_data , "(using in 2b:",b2_normRegYield_data,")" 
        print "MetRatio prediction using 2b contr. reg.: uncorr. met-ratio:", btb_fromb2_normRegYield_data*MetRatioUncorr_data, \
                                                                    " corr:", btb_fromb2_normRegYield_data*MetRatioCorr_data
        if metb == metControlBin:
          for htb2 in htbins:
            if htb[0]>=htb2[0]:
              controlYield[btb][mode][htb2[0]]["data"]                += sigRegYield_data
              controlYield[btb][mode][htb2[0]]["MC_predictedYield_from2b"]  += btb_fromb2_normRegYield_MC
              controlYield[btb][mode][htb2[0]]["MC"]                  += binnedYield[btb][mode][tuple(htb)][tuple(metControlBin)]["MC_sumW"]
        for htb2 in htbins:
          if htb[0]>=htb2[0]:
            for metb2 in metbins:
              if metb[0]>=metb2[0]:
                print "btb", btb, "Adding ",htb,metb, "to bin ht>=", htb2[0], "met>=", metb2[0]
                yields[btb][mode][htb2[0]][metb2[0]]["data"]       += sigRegYield_data
                yields[btb][mode][htb2[0]][metb2[0]]["MC"]         += binnedYield[btb][mode][tuple(htb)][tuple(metb)]["MC_sumW"]
                yields[btb][mode][htb2[0]][metb2[0]]["Var_MC"]     += binnedYield[btb][mode][tuple(htb)][tuple(metb)]["MC_sumW2"]
                yields[btb][mode][htb2[0]][metb2[0]]["signal"]     += binnedYield[btb][mode][tuple(htb)][tuple(metb)]["signal_sumW"]
                yields[btb][mode][htb2[0]][metb2[0]]["Var_signal"] += binnedYield[btb][mode][tuple(htb)][tuple(metb)]["signal_sumW2"]

                yields[btb][mode][htb2[0]][metb2[0]]["MC_predictedYield_fromb2_METshapeSpFCorr"]    += btb_fromb2_normRegYield_MC*MetRatioCorr_MC  
                yields[btb][mode][htb2[0]][metb2[0]]["MC_predictedYield_fromb2_METshapeSpFUncorr"]  += btb_fromb2_normRegYield_MC*MetRatioUncorr_MC  
                yields[btb][mode][htb2[0]][metb2[0]]["Var_MC_predictedYield_fromb2_METshapeSpFCorr"]    += varStat_btb_fromb2_normRegYield_MC*MetRatioCorr_MC**2 
                yields[btb][mode][htb2[0]][metb2[0]]["Var_MC_predictedYield_fromb2_METshapeSpFUncorr"]  += varStat_btb_fromb2_normRegYield_MC*MetRatioUncorr_MC**2

                yields[btb][mode][htb2[0]][metb2[0]]["MC_predictedYield_frombtb_METshapeSpFCorr"]   += btb_normRegYield_MC*MetRatioCorr_MC  
                yields[btb][mode][htb2[0]][metb2[0]]["MC_predictedYield_frombtb_METshapeSpFUncorr"] += btb_normRegYield_MC*MetRatioUncorr_MC  
                yields[btb][mode][htb2[0]][metb2[0]]["data_predictedYield_fromb2_METshapeSpFCorr"]    += btb_fromb2_normRegYield_data*MetRatioCorr_data  
                yields[btb][mode][htb2[0]][metb2[0]]["data_predictedYield_fromb2_METshapeSpFUncorr"]  += btb_fromb2_normRegYield_data*MetRatioUncorr_data  
                yields[btb][mode][htb2[0]][metb2[0]]["data_predictedYield_frombtb_METshapeSpFCorr"]   += btb_normRegYield_data*MetRatioCorr_data  
                yields[btb][mode][htb2[0]][metb2[0]]["data_predictedYield_frombtb_METshapeSpFUncorr"] += btb_normRegYield_data*MetRatioUncorr_data  

#res, shape = getMetRatioFromWK([400,450], metControlBin, [250,350], True)
#true_s = shape.Clone()
#true_s.Reset()
#true_s.SetName("hmtrue")
#true_s.SetTitle("hmtrue")
##c.Draw("met>>hmtrue", "weightBTag2_SF*((singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)&&ht>400&&ht<450)")
#c.Draw("met>>hmtrue", "weightBTag2_SF*((singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)&&ht>400&&ht<450)")
#hmtrue = ROOT.gDirectory.Get("hmtrue")
#shape.Scale(1./shape.Integral())
#hmtrue.Scale(1./hmtrue.Integral())
#hmtrue.SetLineColor(ROOT.kRed)
#shape.Draw()
#hmtrue.Draw("same")

#calculating control region yield in ==2 bin
controlYield["2"] = {}
for mode in btagModes:
  controlYield["2"][mode] = {}
  for htb in htbins:
    controlYield["2"][mode][htb[0]] = {}
    controlYield["2"][mode][htb[0]]["data"] = 0 
    controlYield["2"][mode][htb[0]]["MC"] = 0.
    for htb2 in htbins:
      if htb[0]>=htb2[0]:
        print "Adding ",htb,metb, "to", htb2[0],metb2[0]
        dataCut = leptonCut+"&&ht>="+str(htb[0])+"&&ht<"+str(htb[1])+"&&met>="+str(metControlBin[0])+"&&met<"+str(metControlBin[1])+"&&jet2pt>40&&nbtags==2"
        controlYield["2"][mode][htb[0]]["data"] += cData.GetEntries(dataCut) 
        controlYield["2"][mode][htb[0]]["MC"]   += binnedYield["2"][mode][tuple(htb2)][tuple(metControlBin)]["MC_sumW"]

htbins_table = [400, 750, 1000]
if small:
  htbins_table = htb[:1]

for btb in ["3", "4p"]:
  for htb in htbins_table:
    if btb=="3":
      print "\\hline\\multicolumn{15}{c}{$\\HT>"+str(htb)+"$, \\threeTag}\\\\\\hline"
    if btb=="4p":
      print "\\hline\\multicolumn{15}{c}{$\\HT>"+str(htb)+"$, \\fourTag}\\\\\\hline"
    for metb in [150, 250, 350, 450]:
#      md = "MC_predictedYield_fromb2_METshapeSpFUncorr"
      suffix = "Uncorr"
      md = "MC_predictedYield_fromb2_METshapeSpF"+suffix
      res               = yields[btb]["SF"][htb][metb][md]
      sysErr_b_Up       = yields[btb]["SF_b_Up"][htb][metb][md] - res
      sysErr_b_Down     = yields[btb]["SF_b_Down"][htb][metb][md] - res
      sysErr_light_Up   = yields[btb]["SF_light_Up"][htb][metb][md] - res
      sysErr_light_Down = yields[btb]["SF_light_Down"][htb][metb][md] - res
      sigmaStat    = sqrt(yields[btb]["SF"][htb][metb]["Var_MC_predictedYield_fromb2_METshapeSpFCorr"])
      sstring =  "$"+niceNum(res).rstrip()+"$&${}^{"+niceNum(sysErr_b_Up,2,True)+"}_{"+niceNum(sysErr_b_Down,2,True)+"}$"
      sstring += "&${}^{"+niceNum(sysErr_light_Up,2,True)+"}_{"+niceNum(sysErr_light_Down,2,True)+"}$&$\pm$&$"+niceNum(sigmaStat, 2)+"$"
      #predicted from higher btb bin
      md = "MC_predictedYield_frombtb_METshapeSpF"+suffix
      res = yields[btb]["SF"][htb][metb][md]
      relStatErr = 1./sqrt(controlYield[btb][mode][htb]["MC"]) 
      sstring+="&$"+niceNum(res)+"$&$\pm$&$"+niceNum(res*relStatErr, 2)+"$"
      #MC truth yield
      sstring+="&$"+niceNum(yields[btb]["SF"][htb][metb]["MC"])+"$&$\pm$&$"+niceNum(sqrt(yields[btb]["SF"][htb][metb]["Var_MC"]), 2)+"$"
      #signal yield
      sstring+="&$"+niceNum(yields[btb]["SF"][htb][metb]["signal"])+"$&$\pm$&$"+niceNum(sqrt(yields[btb]["SF"][htb][metb]["Var_signal"]), 2)+"$\\\\"
      print "$\\ETmiss>"+str(metb)+"$&"+sstring

#      res = yields[btb]["SF"][htb][metb]["corr"]
#      print "\nHT/MET >= ", htb, metb,"nControl(data, btb=2)", controlYield[htb]['SF']["2"]["data"],  "nControl(data, btb="+btb+")", controlYield[htb]['SF'][btb]["data"], "nSig(data)", yields[htb][mode][btb][metb]["data"]
#      print "high sys.  low stat:",niceNum(res)+"+/-"+niceNum(max(deltap), 3)+"+/-"+niceNum(res* 1./sqrt(max(1, controlYield[htb]['SF']["2"]["data"])),3)
#      print "high stat. low sys :",niceNum(res)+"+/-"+niceNum(res* 1./sqrt(max(1, controlYield[htb]['SF'][btb]["data"])),3)

#c1 = ROOT.TCanvas()
#c1.SetLogy()
#for htb in htbins:
#  l = ROOT.TLegend(0.5,0.7,1,1.0)
#  l.SetFillColor(0)
#  l.SetShadowColor(ROOT.kWhite)
#  l.SetBorderSize(1)
#  c.Draw("met>>hmetMC(21,0,1050)",str(lumiScale)+"*weightBTag2_SF*("+leptonCut+"&&ht>"+str(htb[0])+"&&met>150&&jet2pt>40)")
#  ROOT.hmetMC.SetLineColor(ROOT.kRed)
#  ROOT.hmetMC.GetXaxis().SetTitle("#slash{E}_{T} (GeV)")
#  ROOT.hmetMC.GetYaxis().SetTitle("Number of Events / 50 GeV")
#  ROOT.hmetMC.Draw()
#  cData.Draw("met>>hData","("+leptonCut+"&&ht>"+str(htb[0])+"&&met>150&&jet2pt>40&&nbtags==2)","same")
#  l.AddEntry(ROOT.hmetMC, "MC ==2 btags") 
#  l.AddEntry(ROOT.hData, "Data ==2 btags") 
#  l.Draw()
#  c1.Print(defaultWWWPath+"/pngBTag/metShape_ht"+str(htb[0])+"_b2.png")
#  l = ROOT.TLegend(0.5,0.7,1,1.0)
#  l.SetFillColor(0)
#  l.SetShadowColor(ROOT.kWhite)
#  l.SetBorderSize(1)
#  c.Draw("met>>hmetMC",str(lumiScale)+"*weightBTag3_SF*("+leptonCut+"&&ht>"+str(htb[0])+"&&met>150&&jet2pt>40)")
#  ROOT.hmetMC.SetLineColor(ROOT.kRed)
#  ROOT.hmetMC.Draw()
#  cData.Draw("met","("+leptonCut+"&&ht>"+str(htb[0])+"&&met>150&&jet2pt>40&&nbtags==3)","same")
#  l.AddEntry(ROOT.hmetMC, "MC ==3 btags") 
#  l.AddEntry(ROOT.hData, "Data ==3 btags") 
#  l.Draw()
#  c1.Print(defaultWWWPath+"/pngBTag/metShape_ht"+str(htb[0])+"_b3.png")
#  l = ROOT.TLegend(0.5,0.7,1,1.0)
#  l.SetFillColor(0)
#  l.SetShadowColor(ROOT.kWhite)
#  l.SetBorderSize(1)
#  c.Draw("met>>hmetMC",str(lumiScale)+"*weightBTag4p_SF*("+leptonCut+"&&ht>"+str(htb[0])+"&&met>150&&jet2pt>40)")
#  ROOT.hmetMC.SetLineColor(ROOT.kRed)
#  ROOT.hmetMC.Draw()
#  cData.Draw("met","("+leptonCut+"&&ht>"+str(htb[0])+"&&met>150&&jet2pt>40&&nbtags>=4)","same")
#  l.AddEntry(ROOT.hmetMC, "MC >=4 btags") 
#  l.AddEntry(ROOT.hData, "Data >=4 btags") 
#  l.Draw()
#  c1.Print(defaultWWWPath+"/pngBTag/metShape_ht"+str(htb[0])+"_b4p.png")
#  del ROOT.hmetMC
#  del ROOT.hData

