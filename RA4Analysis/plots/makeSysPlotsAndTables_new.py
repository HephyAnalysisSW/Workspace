from math import *
from analysisHelpers import *
from Workspace.RA4Analysis.simplePlotsCommon import *
from simpleStatTools import niceNum
import os, pickle, copy

outDir = "/afs/hephy.at/user/s/schoefbeck/www/summaryPlots2012/"
#mode=""
mode="fine"
maxPlotMet = 800
makePlots = True
printFormat = "TeX"
#printFormat = ""

if mode=="fine":
  sys = pickle.load(file('../results/sysTable_fineBinned.pkl'))
  metbins_3b = [(150, 175), (175, 200), (200, 225), (225, 250), (250, 275), (275, 300), (300, 350), (350, 450), (450, 2500)] 
  metbins_2b = [(250, 275),(275,300), (300,350), (350, 450), (450, 2500)] 
else:
  sys = pickle.load(file('../results/systTableLargeBinning.pkl'))
  metbins_3b = [ (150,250), (250, 350), (350, 450), (450, 2500) ]
  metbins_2b = [ (250, 350), (350, 450), (450, 2500) ]

metBinning_2b = [b[0] for b in  metbins_2b]
metBinning_2b.append( maxPlotMet )
metBinning_3b = [b[0] for b in  metbins_3b]
metBinning_3b.append( maxPlotMet )

cData = getRefChain(mode = "Data")
targetLumi = 19400
defaultLines = [[0.2, 0.9, "#font[22]{CMS Collaboration}"], [0.2,0.85,str(int(round(targetLumi/10.))/100.)+" fb^{-1},  #sqrt{s} = 8 TeV"]]

#2btag regions

hObs_2b = {}
hPred_2b = {}
for htb in [(750,2500), (1000, 2500)]:
  if makePlots:
    hObs_2b [htb] = ROOT.TH1F("ht_"+str(htb[0])+"_"+str(htb[1]), "ht_"+str(htb[0])+"_"+str(htb[1]), len(metBinning_2b) - 1, array('d',metBinning_2b))
    hPred_2b[htb] = ROOT.TH1F("ht_"+str(htb[0])+"_"+str(htb[1]), "ht_"+str(htb[0])+"_"+str(htb[1]), len(metBinning_2b) - 1, array('d',metBinning_2b))
  if printFormat=="TeX":
    print "\hline\multirow{2}{*}{\\twoTag} & \multicolumn{6}{c}{"+("$ {0} < \HT < {1} \GeV $".format(htb[0], htb[1]))+"}\\\\\\cline{2-11}" 
    print " & obs. & pred. & \multicolumn{2}{c}{stat.} & \multicolumn{2}{c}{b-tag} & \multicolumn{2}{c}{sys.} & \multicolumn{2}{|c}{total} \\\\\hline"
  drawObjs = []
  for i, metb in enumerate(metbins_2b):
    binwidth = float(metb[1]-metb[0])
    #prediction
    pred = sys['predicted'][htb][metb]
    #sampling + contr.-reg. Poissonian
    if not len(metbins_2b)==len(sys['predCov'][htb]):
      print "Warning! sampling covariance matrix doesn't have the correct length!"
    samplingVar = sys['predCov'][htb][i][i]
    normRegYieldHighHT = float(sys['observed'][tuple(htb)]['norm'])
    normRegYieldVar = (pred/sqrt(normRegYieldHighHT))**2

    modelVar = (pred*sys['systematics']['MET model'][htb][metb])**2

    xsecVar = pred**2*(sys['systematics']['TT polarization'][htb][metb]**2 + sys['systematics']['TT cross section'][htb][metb]**2 +\
                       sys['systematics']['W+jets cross section'][htb][metb]**2 + sys['systematics']['Wbb cross section'][htb][metb]**2 + 
                       sys['systematics']['DiLep'][htb][metb]**2 + sys['systematics']['Tau'][htb][metb]**2 + 
                       sys['systematics']['non-leading cross section'][htb][metb]**2 )

    erfVar = pred**2*(sys['systematics']['Erf nonlinearity ev0'][htb][metb]**2 + sys['systematics']['Erf nonlinearity ev1'][htb][metb]**2 + sys['systematics']['Erf data/MC'][htb][metb]**2)
    
    jesVar = pred**2*(sys['systematics']['JES'][htb][metb]**2)
    
    btagVar = pred**2*(sys['systematics']['bSF'][htb][metb]**2 + sys['systematics']['lSF'][htb][metb]**2)

    smallVar = pred**2*(sys['systematics']['MuEff1'][htb][metb]**2 + sys['systematics']['MuEff2'][htb][metb]**2 + sys['systematics']['EleEff'][htb][metb]**2 + sys['systematics']['Pileup'][htb][metb]**2)
    
    closureVar = pred**2*sys['systematics']['Closure'][htb][metb]**2

#    print "predicted", round(sys['predicted'][htb][metb],2),\
#          "+/-",round(sqrt(samplingVar + normRegYieldVar),2), "(stat.)",\
#          "+/-",round(sqrt(modelVar),2), "(MET model)",\
#          "+/-",round(sqrt(jesVar),2), "(JES)",\
#          "+/-",round(sqrt(xsecVar),2), "(x-sec)",\
#          "+/-",round(sqrt(erfVar),2), "(erf.)",\
#          "+/-",round(sqrt(btagVar),2), "(b-tag)",\
#          "+/-",round(sqrt(smallVar),2), "(PU+other)"
    
    totVar = samplingVar + normRegYieldVar + btagVar + modelVar + jesVar + xsecVar + erfVar + smallVar + closureVar
    
    if printFormat=="TeX":
      print  "\\rule{0pt}{2.5ex}"+(" ${0} < \ETmiss < {1} \GeV$ & {2} &  {3:.2f} & $\pm$ & {4:.2f}& $\pm$ & {5:.2f} & $\pm$ & {6:.2f} & $\pm$& {7:.2f}\\\\".format(metb[0],metb[1], int(sys['observed'][htb][metb]), pred , sqrt(samplingVar + normRegYieldVar), sqrt(btagVar), sqrt(modelVar + jesVar + xsecVar + erfVar + smallVar + closureVar), sqrt(totVar)))
    else:
      print "2b, htb",htb,"metb",metb,": observed", sys['observed'][htb][metb], "predicted", round(pred,2),\
            "+/-",round(sqrt(samplingVar + normRegYieldVar),2), "(stat.)",\
            "+/-",round(sqrt(btagVar),2), "(b-tag)",\
            "+/-",round(sqrt(modelVar + jesVar + xsecVar + erfVar + smallVar + closureVar),2), "(sys.)",\
            "(-> +/-",round(sqrt(totVar),2), "(tot.))"

    if not makePlots:continue
    b = hObs_2b[htb].FindBin(metb[0])

    hObs_2b [htb].SetBinContent(b, sys['observed'][htb][metb]/(binwidth))
    hObs_2b [htb].SetBinError(b, sqrt(sys['observed'][htb][metb])/(binwidth))
    hObs_2b [htb].SetMarkerColor(ROOT.kBlack)
    hObs_2b [htb].SetMarkerStyle(20)
    hObs_2b [htb].SetLineColor(ROOT.kBlack)

    hPred_2b[htb].SetBinContent(b, pred/(binwidth))
    hPred_2b[htb].SetMarkerColor(ROOT.kBlack)
    hPred_2b[htb].SetMarkerStyle(0)
    hPred_2b[htb].SetLineColor(ROOT.kBlack)

    box = ROOT.TBox(metb[0], (pred - sqrt(totVar))/(binwidth), min(metb[1], maxPlotMet), (pred + sqrt(totVar))/(binwidth))
    box.SetFillStyle(3004)
    box.SetFillColor(ROOT.kRed)
    drawObjs.append(box)

    boxS = ROOT.TBox(metb[0], (pred - sqrt(samplingVar + normRegYieldVar))/(binwidth), min(metb[1], maxPlotMet), (pred + sqrt(samplingVar + normRegYieldVar))/(binwidth))
    boxS.SetFillStyle(3004)
    boxS.SetFillColor(ROOT.kBlue)
    drawObjs.append(boxS)

  if not makePlots:continue
  for logy in [ True, False]:

    l = ROOT.TLegend(0.55,0.5,.95,.95)
    l.SetFillColor(0)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)

    l.AddEntry(hObs_2b [htb], "Data")
    l.AddEntry(hPred_2b [htb], "Prediction")
    hf1 = ROOT.TH1F()
    hf1.SetFillStyle(3004)
    hf1.SetFillColor(ROOT.kBlue)
    hf1.SetLineStyle(4000)
    hf1.SetLineWidth(0)
    hf1.SetMarkerStyle(0)
    hf1.SetLineColor(ROOT.kBlack)
    hf1.SetMarkerColor(ROOT.kBlack)
    l.AddEntry(hf1, "stat. uncertainty")

    hf2 = ROOT.TH1F()
    hf2.SetFillStyle(3004)
    hf2.SetFillColor(ROOT.kRed)
    hf2.SetLineStyle(4000)
    hf2.SetLineWidth(0)
    hf2.SetMarkerStyle(0)
    hf1.SetLineColor(ROOT.kBlack)
    hf1.SetMarkerColor(ROOT.kBlack)
    l.AddEntry(hf2, "total uncertainty")

    c1 = ROOT.TCanvas()
    c1.SetLogy(logy)

    hObs_2b [htb].GetYaxis().SetRangeUser(0.07*logy*10**(-2.5*logy), 10**(2*logy)*1.5*hPred_2b[htb].GetMaximum())
    hObs_2b [htb].GetYaxis().SetTitle("Number of Events / GeV")
    hObs_2b [htb].GetXaxis().SetTitle("#slash{E}_{T} (GeV)")
    hObs_2b [htb].Draw("e1")
    hPred_2b[htb].Draw("same")
    for o in drawObjs:
      o.Draw()
    hObs_2b [htb].Draw("e1same")
    if logy:
      prefix="log_"
    else:
      prefix=""
    if mode=="fine":
      prefix+="fine_"

    l.Draw()
    latex = ROOT.TLatex();
    latex.SetNDC();
    latex.SetTextSize(0.04);
    latex.SetTextAlign(11); # align right
    for line in defaultLines:
      latex.DrawLatex(line[0],line[1],line[2])
    c1.Print(outDir+"/met_2b_"+prefix+"ht_"+str(htb[0])+"_"+str(htb[1])+".png")
    c1.Print(outDir+"/met_2b_"+prefix+"ht_"+str(htb[0])+"_"+str(htb[1])+".pdf")
    c1.Print(outDir+"/met_2b_"+prefix+"ht_"+str(htb[0])+"_"+str(htb[1])+".root")
  print

print 

#3btag regions
SpF = pickle.load(file('../results/copyMET_fullMC_v19_GluSplitFixed_jackKnifeSpF.pkl'))
SpFJESPlus  = pickle.load(file('../results/copyMET_JES+_minimal_jackKnifeSpF.pkl'))
SpFJESMinus = pickle.load(file('../results/copyMET_JES-_minimal_jackKnifeSpF.pkl'))
SpFDataMCSys = pickle.load(file('../results/SpillFactorDataMCSys.pkl'))

hObs_3b = {}
hPred_3b = {}
for htb in [(400,2500), (750,2500), (1000,2500)]:
  if makePlots:
    hObs_3b [htb] = ROOT.TH1F("ht_"+str(htb[0])+"_"+str(htb[1]), "ht_"+str(htb[0])+"_"+str(htb[1]), len(metBinning_3b) - 1, array('d',metBinning_3b))
    hPred_3b[htb] = ROOT.TH1F("ht_"+str(htb[0])+"_"+str(htb[1]), "ht_"+str(htb[0])+"_"+str(htb[1]), len(metBinning_3b) - 1, array('d',metBinning_3b))
  drawObjs = []
  if printFormat=="TeX":
    print "\hline\multirow{2}{*}{$\geq 3$ b-tag} & \multicolumn{10}{c}{"+("$ {0} < \HT < {1} \GeV $".format(htb[0], htb[1]))+"}\\\\\\cline{2-11}" 
    print " & obs. & pred. & \multicolumn{2}{c}{stat.} & \multicolumn{2}{c}{b-tag} & \multicolumn{2}{c}{sys.} & \multicolumn{2}{|c}{total} \\\\\hline"
  for i, metb in enumerate(metbins_3b):
    binwidth = float(metb[1]-metb[0])
    #prediction
    isInNormRegion = (metb[0]>=150 and metb[1]<=250)
    if isInNormRegion:
      pred = int(getRefYield('2', htb, metb, 'type1phiMet', 6, cData))*SpF[tuple(htb)][(150,250)][(6,99)]['SF']['3po2']['rForData']
    else:
      pred = sys['predicted'][tuple(htb)][metb] *SpF[tuple(htb)][metb][(6,99)]['SF']['3po2']['rForData']

    #sampling + contr.-reg. Poissonian
    if isInNormRegion:
      samplingVar=0. 
    else:
      if not len(metbins_2b)==len(sys['predCov'][htb]):
        print "Warning! sampling covariance matrix doesn't have the correct length!"
      if mode=="fine":
        samplingVar = SpF[tuple(htb)][metb][(6,99)]['SF']['3po2']['rForData']**2*sys['predCov'][htb][i-4][i-4]#FIXME
      else:
        samplingVar = SpF[tuple(htb)][metb][(6,99)]['SF']['3po2']['rForData']**2*sys['predCov'][htb][i-1][i-1]#FIXME

    normRegYieldHighHT = float(sys['observed'][tuple(htb)]['norm'])
    normRegYieldVar = (pred/sqrt(normRegYieldHighHT))**2

    spfRef = SpF[htb][metb][(6,99)]['SF']['3po2']['rForData']
    spfJESPlus = SpFJESPlus[htb][metb][(6,99)]['SF']['3po2']['rForData']
    spfJESMinus = SpFJESMinus[htb][metb][(6,99)]['SF']['3po2']['rForData']
    spfSFbPlus = SpF[htb][metb][(6,99)]['SF_b_Up']['3po2']['rForData']
    spfSFbMinus = SpF[htb][metb][(6,99)]['SF_b_Down']['3po2']['rForData']
    spfSFlPlus = SpF[htb][metb][(6,99)]['SF_light_Up']['3po2']['rForData']
    spfSFlMinus = SpF[htb][metb][(6,99)]['SF_light_Down']['3po2']['rForData']
    spfcFracPlus = SpF[htb][metb][(6,99)]['cFracUp']['3po2']['rForData']
    spfcFracMinus = SpF[htb][metb][(6,99)]['cFracDown']['3po2']['rForData']
    spfgluSplitPlus = SpF[htb][metb][(6,99)]['GluSplitUp']['3po2']['rForData']
    spfgluSplitMinus = SpF[htb][metb][(6,99)]['GluSplitDown']['3po2']['rForData']

    SpFJES = 0.5*(spfJESPlus - spfJESMinus)/spfRef
    SpFSFb = 0.5*(spfSFbPlus - spfSFbMinus)/spfRef
    SpFSFl = 0.5*(spfSFlPlus - spfSFlMinus)/spfRef
    SpFcFrac     = 0.5*(spfcFracPlus - spfcFracMinus)/spfRef
    SpFgluSplit  = 0.5*(spfgluSplitPlus - spfgluSplitMinus)/spfRef
    SpFnonC = SpFDataMCSys[htb][metb]
    SpFStat = SpF[htb][metb][(6,99)]['SF']['3po2']['sigmaForData'] 
    if not isInNormRegion:
      modelVar = (pred*sys['systematics']['MET model'][htb][metb])**2
    
      xsecVar = pred**2*(sys['systematics']['TT polarization'][htb][metb]**2 + sys['systematics']['TT cross section'][htb][metb]**2 +\
                         sys['systematics']['W+jets cross section'][htb][metb]**2 + sys['systematics']['Wbb cross section'][htb][metb]**2 + 
                         sys['systematics']['DiLep'][htb][metb]**2 + sys['systematics']['Tau'][htb][metb]**2 + 
                         sys['systematics']['non-leading cross section'][htb][metb]**2 )
    
      erfVar = pred**2*(sys['systematics']['Erf nonlinearity ev0'][htb][metb]**2 + sys['systematics']['Erf nonlinearity ev1'][htb][metb]**2 + sys['systematics']['Erf data/MC'][htb][metb]**2)
      spfJesVar = 0.5*(SpFJESPlus[tuple(htb)][(150,250)][(6,99)]['SF']['3po2']['rForData'] - SpFJESMinus[tuple(htb)][(150,250)][(6,99)]['SF']['3po2']['rForData'])/SpF[tuple(htb)][(150,250)][(6,99)]['SF']['3po2']['rForData']
      jesVar = pred**2*(-1 + (1+sys['systematics']['JES'][htb][metb])*(1+SpFJES))**2
      btagVar = pred**2*( ( -1 + ( 1 + sys['systematics']['bSF'][htb][metb])*(1+SpFSFb))**2 + (-1 + (1 + sys['systematics']['lSF'][htb][metb])*(1+SpFSFl))**2 \
                         + SpFcFrac**2 + SpFgluSplit**2 + SpFnonC**2 + SpFStat**2)
      smallVar = pred**2*(sys['systematics']['MuEff1'][htb][metb]**2 + sys['systematics']['MuEff2'][htb][metb]**2 + sys['systematics']['EleEff'][htb][metb]**2 + sys['systematics']['Pileup'][htb][metb]**2)
      closureVar = pred**2*sys['systematics']['Closure'][htb][metb]**2

    else:
      modelVar = 0
      xsecVar = 0
      erfVar = 0
      jesVar = pred**2*SpFJES**2
      btagVar = pred**2*(SpFSFb**2 + SpFSFl**2 + SpFcFrac**2 + SpFgluSplit**2 + SpFnonC**2 + SpFStat**2)
      smallVar = 0
      closureVar = 0 

    totVar = samplingVar + normRegYieldVar + btagVar + modelVar + jesVar + xsecVar + erfVar + smallVar + closureVar
    
    obs = int(getRefYield('3', tuple(htb), tuple(metb), 'type1phiMet', 6, cData))

    if printFormat=="TeX":
      print  "\\rule{0pt}{2.5ex}"+(" ${0} < \ETmiss < {1} \GeV$ & {2} &  {3:.2f} & $\pm$ & {4:.2f}& $\pm$ & {5:.2f} & $\pm$ & {6:.2f} & $\pm$& {7:.2f}\\\\".format(metb[0],metb[1], int(obs), pred , sqrt(samplingVar + normRegYieldVar), sqrt(btagVar), sqrt(modelVar + jesVar + xsecVar + erfVar + smallVar + closureVar), sqrt(totVar)))
    else:
      print "3b, htb",htb,"metb",metb,": observed ",obs,"predicted", round(pred,2),\
            "+/-",round(sqrt(samplingVar),2), "(sampling)",\
            "+/-",round(sqrt(normRegYieldVar),2), "(normRegYield)",\
            "+/-",round(sqrt(btagVar), 2),"(b-tag)",\
            "+/-",round(sqrt(modelVar + jesVar + xsecVar + erfVar + smallVar + closureVar),2), "(sys.)",\
            "(-> +/-",round(sqrt(totVar),2), "(tot.))"

    if not makePlots:continue
    b = hObs_3b[htb].FindBin(metb[0])
    hObs_3b [htb].SetBinContent(b, obs/(binwidth/10.))
    hObs_3b [htb].SetBinError(b, sqrt(obs)/(binwidth/10.))
    hObs_3b [htb].SetMarkerColor(ROOT.kBlack)
    hObs_3b [htb].SetMarkerStyle(20)
    hObs_3b [htb].SetLineColor(ROOT.kBlack)
    hPred_3b[htb].SetBinContent(b, pred/(binwidth/10.))
    hPred_3b[htb].SetMarkerColor(ROOT.kBlack)
    hPred_3b[htb].SetMarkerStyle(0)
    hPred_3b[htb].SetLineColor(ROOT.kBlack)

    box = ROOT.TBox(metb[0], (pred - sqrt(totVar))/(binwidth/10.), min(metb[1], maxPlotMet), (pred + sqrt(totVar))/(binwidth/10.))
    box.SetFillStyle(3004)
    box.SetFillColor(ROOT.kRed)
    drawObjs.append(box)

    boxS = ROOT.TBox(metb[0], (pred - sqrt(samplingVar + normRegYieldVar))/(binwidth/10.), min(metb[1], maxPlotMet), (pred + sqrt(samplingVar + normRegYieldVar))/(binwidth/10.))
    boxS.SetFillStyle(3004)
    boxS.SetFillColor(ROOT.kBlue)
    drawObjs.append(boxS)

  if not makePlots:continue
  for logy in [ True, False]:

    l = ROOT.TLegend(0.55,0.5,.95,.95)
    l.SetFillColor(0)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)

    l.AddEntry(hObs_3b [htb], "Data")
    l.AddEntry(hPred_3b [htb], "Prediction")
    hf1 = ROOT.TH1F()
    hf1.SetFillStyle(3004)
    hf1.SetFillColor(ROOT.kBlue)
    hf1.SetLineStyle(4000)
    hf1.SetLineWidth(0)
    hf1.SetMarkerStyle(0)
    hf1.SetLineColor(ROOT.kBlack)
    hf1.SetMarkerColor(ROOT.kBlack)
    l.AddEntry(hf1, "stat. uncertainty")
    hf2 = ROOT.TH1F()
    hf2.SetFillStyle(3004)
    hf2.SetFillColor(ROOT.kRed)
    hf2.SetLineStyle(4000)
    hf2.SetLineWidth(0)
    hf2.SetMarkerStyle(0)
    hf1.SetLineColor(ROOT.kBlack)
    hf1.SetMarkerColor(ROOT.kBlack)
    l.AddEntry(hf2, "total uncertainty")

    c1 = ROOT.TCanvas()
    c1.SetLogy(logy)
    hObs_3b [htb].GetYaxis().SetRangeUser(0.07*logy*10**(-2*logy), 10**logy*1.8*hPred_3b[htb].GetMaximum())
    if htb==(1000,2500):
      hObs_3b [htb].GetYaxis().SetRangeUser(0.07*logy*10**(-2*logy), 10**logy*2.0*hPred_3b[htb].GetMaximum())
  
    hObs_3b [htb].GetYaxis().SetTitle("Number of Events / GeV")
    hObs_3b [htb].GetXaxis().SetTitle("#slash{E}_{T} (GeV)")
    hObs_3b [htb].Draw("e1")
    hPred_3b[htb].Draw("same")
    for o in drawObjs:
      o.Draw()
    hObs_3b [htb].Draw("e1same")
    if logy:
      prefix="log_"
    else:
      prefix=""
    if mode=="fine":
      prefix+="fine_"
    l.Draw()
    latex = ROOT.TLatex();
    latex.SetNDC();
    latex.SetTextSize(0.04);
    latex.SetTextAlign(11); # align right
    for line in defaultLines:
      latex.DrawLatex(line[0],line[1],line[2])
    c1.Print(outDir+"/met_3b_"+prefix+"ht_"+str(htb[0])+"_"+str(htb[1])+".png")
    c1.Print(outDir+"/met_3b_"+prefix+"ht_"+str(htb[0])+"_"+str(htb[1])+".pdf")
    c1.Print(outDir+"/met_3b_"+prefix+"ht_"+str(htb[0])+"_"+str(htb[1])+".root")
  print
