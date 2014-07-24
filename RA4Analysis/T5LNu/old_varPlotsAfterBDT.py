import ROOT
import pickle
from localConfig import afsUser, nfsUser, localPlotDir
from array import array
import os, sys
from math import sqrt

for path in [os.path.abspath(p) for p in ['../../HEPHYCommonTools/mva', 'HEPHYCommonTools/cardFileWriter/', '../python', '../../HEPHYCommonTools/cardFileWriter']]:
  if not path in sys.path:
      sys.path.insert(1, path)

from nnAnalysisHelpers import getObjFromFile, constructDataset, getYieldFromChain, getFOMPlot, fillMVAHisto, fillHistoAfterMVA

preprefix = 'MonoJet_stopDeltaM30FastSim_BkgMix_0_nTrees400_nCuts_-1_maxDepth_1_maxDepthComparison'
#allVars = ["type1phiMet",'isrJetPt', 'softIsolatedMuPt', 'softIsolatedMuEta', 'softIsolatedMuCharge',  'njet' ]
allVars = [ "softIsolatedMT", "type1phiMet",  'isrJetPt',  'softIsolatedMuPt', 'softIsolatedMuCharge', 'njet' ]

plotVars = [ \
  [ "softIsolatedMT", [20,0,200]], 
  [ "type1phiMet",[20,0,1000]],
  [ 'isrJetPt', [20,0,1000]],
  [ 'softIsolatedMuPt',[20,0,20]],
  [ 'softIsolatedMuCharge',[3, -1.5, 1.5]],
  [ 'njet', [6,0,6]]
  ]

prefix=preprefix+'_'+"_".join(allVars)
setup=pickle.load(file('/data/'+nfsUser+'/MonoJetNNAnalysis/MVA_Analyzer/'+prefix+'.pkl'))
#  canv = getObjFromFile(setup['plotDir']+'/'+setup['plotSubDir']+'/nnValidation.root', 'mlpa_canvas')  
#  toPlot.append([canv.FindObject('MVA_BDT_maxDepth1_rejBvsS').Clone(), omitted])
#  del canv

reader = ROOT.TMVA.Reader()
for var in setup['mvaInputVars']:
  var_i  = array('f',[0])
  reader.AddVariable(var, var_i)
classifier = 'BDT_maxDepth1'
found = False
method = None
for m in setup['methodConfigs']:
  if not m['name']==classifier:
    continue
  method = m
  reader.BookMVA(m['name'],setup['weightDir']+'/TMVAClassification_'+m['name']+'.weights.xml')
  found = True
if not found:
  print "Classifier",classifier,"not found!" 
else:
  data = constructDataset(setup, None, None, False)
  sigCut = setup['preselection']+'&&type1phiMet>150&&softIsolatedMuCharge==-1&&type==1&&mlsp==270&&mstop==300'
  bkgCut = setup['preselection']+'&&type1phiMet>150&&softIsolatedMuCharge==-1&&type==0'
  sigCutPresel = setup['preselection']+'&&type==1&&mlsp==270&&mstop==300'
  bkgCutPresel = setup['preselection']+'&&type==0'
  for disc in [0.3, 0.35, 0.42, 0.48, 0.55]:
    for var, binning in plotVars:
      sigVar = ROOT.TH1F('Var', 'Var', *binning)
      bkgVar = ROOT.TH1F('Var', 'Var', *binning)
      sigVarInc= ROOT.TH1F('Var', 'VarInc', *binning)
      bkgVarInc= ROOT.TH1F('Var', 'VarInc', *binning)
      fillHistoAfterMVA(data['allTestEvents'],setup, reader, method, sigCut, var, sigVar, mvaBin=[disc, 999], weightFunc = lambda c:c.GetLeaf('weight').GetValue()*c.GetLeaf('testSampleScaleFac').GetValue())
      fillHistoAfterMVA(data['allTestEvents'],setup, reader, method, bkgCut, var, bkgVar, mvaBin=[disc, 999], weightFunc = lambda c:c.GetLeaf('weight').GetValue()*c.GetLeaf('testSampleScaleFac').GetValue())
      fillHistoAfterMVA(data['allTestEvents'],setup, reader, method, sigCutPresel, var, sigVarInc, mvaBin=[-999, 999], weightFunc = lambda c:c.GetLeaf('weight').GetValue()*c.GetLeaf('testSampleScaleFac').GetValue())
      fillHistoAfterMVA(data['allTestEvents'],setup, reader, method, bkgCutPresel, var, bkgVarInc, mvaBin=[-999, 999], weightFunc = lambda c:c.GetLeaf('weight').GetValue()*c.GetLeaf('testSampleScaleFac').GetValue())
      sigVarInc.GetYaxis().SetRangeUser(0.07, sigVarInc.GetMaximum()*2) 
      bkgVarInc.GetYaxis().SetRangeUser(0.07, bkgVarInc.GetMaximum()*2) 
      sigVarInc.GetXaxis().SetTitle(var) 
      bkgVarInc.GetXaxis().SetTitle(var) 
      sigYield = sigVar.Integral()
      bkgYield = bkgVar.Integral()
      sigYieldInc = sigVarInc.Integral()
      bkgYieldInc = bkgVarInc.Integral()
  #    sigVar.Add(bkgVar)
      sigVar.SetLineColor(ROOT.kRed)
      sigVarInc.SetLineColor(ROOT.kRed)
      sigVarInc.SetLineStyle(ROOT.kDashed)
      bkgVarInc.SetLineStyle(ROOT.kDashed)
      print "SigEff",sigYield/sigYieldInc,"bkgEff",bkgYield/bkgYieldInc
    #  sigDisc = ROOT.TH1F('sig', 'sig', 2000, -1.5, 1.5)
    #  bkgDisc = ROOT.TH1F('sig', 'sig', 2000, -1.5, 1.5)
    #  fillMVAHisto(data['allTestEvents'],setup, reader, method, sigCut, sigDisc, weightFunc = lambda c:c.GetLeaf('weight').GetValue()*c.GetLeaf('testSampleScaleFac').GetValue())
    #  fillMVAHisto(data['allTestEvents'],setup, reader, method, bkgCut, bkgDisc, weightFunc = lambda c:c.GetLeaf('weight').GetValue()*c.GetLeaf('testSampleScaleFac').GetValue())

      print "fom(0.05):",sigYield/sqrt(bkgYield + (0.05*bkgYield)**2) 
      c1 = ROOT.TCanvas()
      c1.SetLogy()
      bkgVarInc.Draw()
      sigVarInc.Draw("same")
      bkgVar.Draw("same")
      sigVar.Draw("same")
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngMJ/shapeAfterBDT_"+var+"_disc"+str(disc)+".png")
      del c1
  for d in data.values():
    del d
  del data
del reader


#data = constructDataset(setup, None, None, False)
#sigCut = setup['preselection']+'&&type==1&&mlsp==270&&mstop==300'
#bkgCut = setup['preselection']+'&&type==0'
##Use last one (=='None', i.e. no omission)  to compute S/sqrt(B) ==const contours
#nPreS = getYieldFromChain(data['allTestEvents'], sigCut, 'weight*testSampleScaleFac' ) 
#nPreB = getYieldFromChain(data['allTestEvents'], bkgCut, 'weight*testSampleScaleFac' ) 
#print nPreS, nPreB
#
#toPlotFOMTGraphErrors = {}
#for relSys in [0.05, 0.08]:
#  toPlotFOMTGraphErrors[relSys] = []
#  for t in toPlotTGraphErrors:
#    zeros = array('d', [0. for x in range(t[0].GetN())])
#    bufX = t[0].GetX()
#    bufY = t[0].GetY()
#    sigEff = [bufX[n] for n in range(t[0].GetN())]
#    bkgEff = [1.-bufY[n] for n in range(t[0].GetN())]
#    significance=[]
#    for i in  range(t[0].GetN()):
#      if bkgEff[i]>0:
#        significance.append(nPreS*sigEff[i]/sqrt(nPreB*bkgEff[i] + (relSys*nPreB*bkgEff[i])**2))
#      else:
#        significance.append(0.)
#    toPlotFOMTGraphErrors[relSys].append([ROOT.TGraphErrors(t[0].GetN(), array('d', sigEff), array('d', significance), zeros, zeros), t[1]])
#
#
#def getConstSoverSqrtBFunc(nPreB, nPreS, relSys, sigLevel):
#  formula =  '1. + 0.5*1./(nPreB*sys**2) - sqrt(0.25/nPreB**2/sys**4 + nPreS**2*x**2/(sig*nPreB*sys)**2)'
#  replacements = [['nPreB', str(nPreB)], ['nPreS', str(nPreS)], ['sys', str(relSys)], ['sig', str(sigLevel)]]
#  for a,b in replacements:
#    formula = formula.replace(a,b)
#  print formula
#  return ROOT.TF1('func', formula, 0, 1)
#
#
#for d in data.values():
#  del d
#del data
#
#f2_05=getConstSoverSqrtBFunc(nPreB=nPreB, nPreS=nPreS,relSys=0.05,sigLevel=2)
#f3_05=getConstSoverSqrtBFunc(nPreB=nPreB, nPreS=nPreS,relSys=0.05,sigLevel=3)
#f2_10=getConstSoverSqrtBFunc(nPreB=nPreB, nPreS=nPreS,relSys=0.1,sigLevel=2)
#f3_10=getConstSoverSqrtBFunc(nPreB=nPreB, nPreS=nPreS,relSys=0.1,sigLevel=3)
#
#f2_10.SetLineStyle(ROOT.kDashed)
#f3_10.SetLineStyle(ROOT.kDashed)
#
#colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kGreen-4, ROOT.kMagenta, ROOT.kCyan, ROOT.kYellow+3, ROOT.kOrange, ROOT.kGreen + 3, ROOT.kRed - 7, ROOT.kGray + 2]
#
#xRange = [0., 0.2]
#yRange = [0.975, 1.0]
#
#l = ROOT.TLegend(.16, .13, 0.63, 0.55)
#l.SetFillColor(ROOT.kWhite)
#l.SetShadowColor(ROOT.kWhite)
#l.SetBorderSize(1)
#c = ROOT.TCanvas()
#drawopt="al"
#for i,[h,n] in enumerate(reversed(toPlotTGraphErrors)):
#  h.SetLineColor(colors[i])
#  h.GetXaxis().SetLabelSize(0.04)
#  h.GetYaxis().SetLabelSize(0.04)
#  h.SetMarkerColor(colors[i])
#  h.SetMarkerStyle(0)
#  h.SetMarkerSize(0)
#  h.GetXaxis().SetRangeUser(*xRange)
#  h.GetYaxis().SetRangeUser(*yRange)
#  h.GetYaxis().SetTitle("Background rejection")
#  h.GetXaxis().SetTitle("Signal efficiency")
#  h.Draw(drawopt)
#  drawopt="lsame"
#  l.AddEntry(h, n, "LP")
#
#toPlotTGraphErrors[-1][0].Draw('lsame')
#
#l.Draw()
#
#f2_05.SetLineWidth(1)
#f3_05.SetLineWidth(1)
#f2_10.SetLineWidth(1)
#f3_10.SetLineWidth(1)
#f2_05.Draw('same')
#f3_05.Draw('same')
#f2_10.Draw('same')
#f3_10.Draw('same')
#c.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMJ/Comparison_'+prefix+'.png')
#
#for relSys in [0.05, 0.08]:
#  yRange = [0.5, 4.0]
#  l = ROOT.TLegend(.6, .6, 1.0, 1.0)
#  l.SetFillColor(ROOT.kWhite)
#  l.SetShadowColor(ROOT.kWhite)
#  l.SetBorderSize(1)
#  c = ROOT.TCanvas()
#  drawopt="al"
#  for i,[h,n] in enumerate(reversed(toPlotFOMTGraphErrors[relSys])):
#    h.SetLineColor(colors[i])
#    h.GetXaxis().SetLabelSize(0.04)
#    h.GetYaxis().SetLabelSize(0.04)
#    h.SetMarkerColor(colors[i])
#    h.SetMarkerStyle(0)
#    h.SetMarkerSize(0)
#    h.GetXaxis().SetRangeUser(*xRange)
#    h.GetYaxis().SetRangeUser(*yRange)
#    h.GetYaxis().SetTitle("FOM")
#    h.GetXaxis().SetTitle("Signal efficiency")
#    h.Draw(drawopt)
#    drawopt="lsame"
#    l.AddEntry(h, n, "LP")
#  toPlotFOMTGraphErrors[relSys][-1][0].Draw('lsame')
#  l.Draw()
#  c.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMJ/ComparisonFOM_'+str(relSys)+'_'+prefix+'.png')
