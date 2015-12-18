import ROOT
import pickle 
import copy, os, sys
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.TH1F().SetDefaultSumw2()
ROOT.setTDRStyle()
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *
from draw_helpers import *
from math import *
from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed_antiSel import *

preprefix = 'QCDestimation/final2p1fb/systematics'
wwwDir = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/RunII/Spring15_25ns/'+preprefix+'/'
prefix = 'QCDsystematics_'
picklePath = '/data/'+username+'/results2015/QCDEstimation/'
picklePresel = '20151216_QCDestimation_MC2p1fb_pkl'
pickleFit    = '20151216_fitResult_MC2p1fb_pkl'
res = pickle.load(file(picklePath+picklePresel))
fitRes = pickle.load(file(picklePath+pickleFit))

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

def makeWeight(lumi=3., sampleLumi=3.,debug=False):
  if debug:
    print 'No lumi-reweighting done!!'
    return 'weight', 'weight*weight'
  else:
    weight_str = '(((weight)/'+str(sampleLumi)+')*'+str(lumi)+')'
    weight_err_str = '('+weight_str+'*'+weight_str+')'
    return weight_str, weight_err_str
lumi = 2.11 
sampleLumi = 2.11
debugReweighting = True
weight_str, weight_err_str = makeWeight(lumi, sampleLumi=sampleLumi, debug=debugReweighting)

def getRCS(c, cut, dPhiCut, useWeight = False, weight = 'weight'):
#  dPhiStr = 'acos((LepGood_pt+met_pt*cos(LepGood_phi-met_phi))/sqrt(LepGood_pt**2+met_pt**2+2*met_pt*LepGood_pt*cos(LepGood_phi-met_phi)))'
  dPhiStr = 'deltaPhi_Wl'
  if useWeight:
    h = getPlotFromChain(c, dPhiStr, [0,dPhiCut,pi], cutString=cut, binningIsExplicit=True, weight =  weight)
  else:
    h = getPlotFromChain(c, dPhiStr, [0,dPhiCut,pi], cutString=cut, binningIsExplicit=True, weight='(1)')
  h.Sumw2()
  if h.GetBinContent(1)>0:
    rcs = h.GetBinContent(2)/h.GetBinContent(1)
    if h.GetBinContent(2)>0:
      rCSE_sim = rcs*sqrt(h.GetBinError(2)**2/h.GetBinContent(2)**2 + h.GetBinError(1)**2/h.GetBinContent(1)**2)
      rCSE_pred = rcs*sqrt(1./h.GetBinContent(2) + 1./h.GetBinContent(1))
      del h
      return {'rCS':rcs, 'rCSE_pred':rCSE_pred, 'rCSE_sim':rCSE_sim}
    else:
      del h
      return {'rCS':rcs, 'rCSE_pred':float('nan'), 'rCSE_sim':float('nan')}
  else:
    del h
    return {'rCS':float('nan'), 'rCSE_pred':float('nan'), 'rCSE_sim':float('nan')}

def getFraction(Bkg, Bkg_err, QCD, QCD_err):
  try: res = QCD/Bkg
  except ZeroDivisionError: res = float('nan')
  try: res_err = res*sqrt(Bkg_err**2/Bkg**2 + QCD_err**2/QCD**2)
  except ZeroDivisionError: res_err = float('nan')
  return res, res_err

#trigger and filters for real Data
trigger = "&&(HLT_EleHT350||HLT_MuHT350)"
#filters = "&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter_fix&&Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter"
#filters = "&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter_fix&&Flag_HBHENoiseIsoFilter&&Flag_goodVertices&&Flag_eeBadScFilter"
filters = "&& Flag_CSCTightHaloFilter && Flag_HBHENoiseFilter_fix && Flag_HBHENoiseIsoFilter && Flag_goodVertices && Flag_eeBadScFilter"

presel = 'nLep==1&&nVeto==0&&nEl==1&&leptonPt>25&&Jet2_pt>80'
antiSelStr = presel+'&&Selected==-1'
SelStr = presel+'&&Selected==1'

cQCD  = getChain(QCDHT_25ns,histname='')
#cEWK  = getChain([WJetsHTToLNu_25ns, TTJets_HTLO_25ns, singleTop_25ns, DY_25ns, TTV_25ns],histname='')
#cData = getChain(data_ele_25ns , histname='')

#define SR
inclusiveTemplate = {(3, 4): {(250,  -1): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}}}} #use inclusive LT,HT region to get the shape for the fit template

fitCR =  {(3, 4): {(250,  -1): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}},
                   (250, 350): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}}, #QCD CR exclusive in LT and inclusive in HT, where the fits are performed
                   (350,  -1): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}},
                   (350, 450): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}},
                   (450,  -1): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}}}}
CR = {
                (3, 4): {(250, 350): {(500, -1):   {(1.0):    {'deltaPhi': 1.0}}, #3-4jets W+jets control region
                                      (500, 750):  {(1.0):    {'deltaPhi': 1.0}},
                                      (750, -1):   {(1.0):    {'deltaPhi': 1.0}}},
                         (350, -1):  {(500, -1):   {(0.75):   {'deltaPhi': 0.75}}},
                         (350, 450): {(500, -1):   {(1.0):    {'deltaPhi': 1.0},
                                                    (0.75):   {'deltaPhi': 0.75}},
                                      (500, 750):  {(1.0):    {'deltaPhi': 1.0}},
                                      (750, -1):   {(1.0):    {'deltaPhi': 1.0}}},
                         (450, -1):  {(500, -1):   {(1.0):    {'deltaPhi': 1.0},
                                                    (0.75):   {'deltaPhi': 0.75}},
                                      (500, 750):  {(0.75):   {'deltaPhi': 0.75}},
                                      (750, -1):   {(0.75):   {'deltaPhi': 0.75}},
                                      (500, 1000): {(0.75):   {'deltaPhi': 0.75}},
                                      (1000, -1):  {(0.75):   {'deltaPhi': 0.75}}}}
}

signalRegion = {
                (3, 4): {(250,  -1): {(500,  -1)},  #QCD inclusive template
                         (250, 350): {(500,  -1),  #3-4jets W+jets control region inclusive in LT
                                      (500, 750), 
                                      (750,  -1)},  
                         (350, -1):  {(500,  -1)},
                         (350, 450): {(500,  -1),  
                                      (500, 750), 
                                      (750,  -1)},  
                         (450, -1):  {(500,  -1),  
                                      (500, 750), 
                                      (750,  -1)}},  
                (4, 5): {(250, 350): {(500,  -1),  #4-5jets TTbar control region
                                      (500, 750), 
                                      (750,  -1)},  
                         (350, -1):  {(500,  -1)},  
                         (350, 450): {(500,  -1),  
                                      (500, 750), 
                                      (750,  -1)}},  
                         (450, -1):  {(500, -1),  
                                      (500, 750), 
                                      (750, -1)},  
                (5, 5): {(250, 350): {(500, -1)},   #signal regions
                         (350, 450): {(500, -1)},  
                         (450,  -1): {(500, -1)}}, 
                (6, 7): {(250, 350): {(500, 750), 
                                      (750,  -1)},  
                         (350, 450): {(500, 750), 
                                      (750,  -1)},  
                          (450, -1): {(500, 750), 
                                      (750,  -1)}},  
                (8, -1): {(250, 350):{(500, 750),
                                      (750,  -1)},
                          (350, -1): {(500, -1)}},
}

signalRegionInclusiveLT = {
                (3, 4): {(250,  -1): {(500,  -1):{'btb':(0,0), 'label':['LTi','HTi','NB0','NJ34'], 'sys':0.25},  
                                      (500, 750):{'btb':(0,0), 'label':['LTi','HT1','NB0','NJ34'], 'sys':0.25}, #3-4jets W+jets control region inclusive in LT 
                                      (750,  -1):{'btb':(0,0), 'label':['LTi','HT2i','NB0','NJ34'], 'sys':0.5}}},  
                (4, 5): {(250,  -1): {(500,  -1):{'btb':(1,1), 'label':['LTi','HTi','NB1','NJ45'], 'sys':0.25},  #4-5jets TTbar control region
                                      (500, 750):{'btb':(1,1), 'label':['LTi','HT1','NB1','NJ45'], 'sys':0.25}, 
                                      (750,  -1):{'btb':(1,1), 'label':['LTi','HT2i','NB1','NJ45'], 'sys':0.5}}},  
                (5, 5): {(250,  -1): {(500,  -1):{'btb':(0,0), 'label':['LTi','HTi','NB0','NJ5'], 'sys':0.25}}},   #signal regions
                (6, 7): {(250,  -1): {(500, 750):{'btb':(0,0), 'label':['LTi','HT1','NB0','NJ67'], 'sys':0.5}, 
                                      (750,  -1):{'btb':(0,0), 'label':['LTi','HT2i','NB0','NJ67'], 'sys':0.5}}},  
                (8, -1):{(250,  -1): {(500,  -1):{'btb':(0,0), 'label':['LTi','HTi','NB0','NJ8i'], 'sys':1.},
                                      (500, 750):{'btb':(0,0), 'label':['LTi','HT1','NB0','NJ8i'], 'sys':1.},
                                      (750,  -1):{'btb':(0,0), 'label':['LTi','HT2i','NB0','NJ8i'], 'sys':1.}}}
}

njreg = [(3,3),(4,4),(5,5),(6,6),(7,7),(8,-1)]
SRnjreg = [(3,4),(5,5),(6,7),(8,-1)]
ltreg = [(250,-1)]
htreg = [(500,750),(750,1000),(1000,-1)]
btreg = [(0,0)]#, (1,1), (2,2)] #1b and 2b estimates are needed for the btag fit

ROOT_colors = [ROOT.kBlack, ROOT.kRed-4, ROOT.kBlue, ROOT.kGreen+2, ROOT.kOrange+1, ROOT.kAzure+6, ROOT.kCyan+3, ROOT.kOrange , ROOT.kRed-10]
text = ROOT.TLatex()
text.SetNDC()
text.SetTextSize(0.04)
text.SetTextAlign(11)

canv = ROOT.TCanvas('canv','canv',1200,600)
leg = ROOT.TLegend(0.65,0.8,0.8,0.85)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetShadowColor(ROOT.kWhite)

drawOption = 'hist ][ e1'
drawOptionSame = drawOption + 'same'
#
sysXErr = []
sysYErr = []
sysX = []
sysY = []

Fhist=ROOT.TH1F('Fhist','Fhist',13,0,13)
Fhist.SetLineWidth(2)

j=2
antiSelname, antiSelCut = nameAndCut((250,-1),(500,-1),(3,4),(0,0), presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30')
Selname, SelCut         = nameAndCut((250,-1),(500,-1),(3,4),(0,0), presel=SelStr, charge="", btagVar = 'nBJetMediumCSV30')
nSel,nSel_err           = getYieldFromChain(cQCD, SelCut, weight = weight_str, returnError=True)
nAntiSel,nAntiSel_err   = getYieldFromChain(cQCD, antiSelCut, weight = weight_str, returnError=True)
X=nSel/nAntiSel
X_err= X*sqrt(nSel_err**2/nSel**2+nAntiSel_err**2/nAntiSel**2)
Fhist.SetBinContent(1,0.1)
Fhist.SetBinError(1,X_err)
Fhist.GetXaxis().SetBinLabel(1, '#splitline{#splitline{LTi}{HTi}}{#splitline{NB0}{NJ34}}')
for i_njb, njb in enumerate(sorted(signalRegionInclusiveLT)):
  for i_ltb, ltb in enumerate(sorted(signalRegionInclusiveLT[njb])):
    for i_htb,htb in enumerate(sorted(signalRegionInclusiveLT[njb][ltb])):
      sysUnc = signalRegionInclusiveLT[njb][ltb][htb]['sys'] 
      btb = signalRegionInclusiveLT[njb][ltb][htb]['btb'] 
      label = signalRegionInclusiveLT[njb][ltb][htb]['label'] 
      antiSelname, antiSelCut = nameAndCut(ltb, htb, njb, btb, presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30')
      Selname, SelCut         = nameAndCut(ltb, htb, njb, btb, presel=SelStr, charge="", btagVar = 'nBJetMediumCSV30')
      nSel,nSel_err           = getYieldFromChain(cQCD, SelCut, weight = weight_str, returnError=True)
      nAntiSel,nAntiSel_err   = getYieldFromChain(cQCD, antiSelCut, weight = weight_str, returnError=True)
      try: F=nSel/nAntiSel
      except ZeroDivisionError: F = 0
      try: F_err= F*sqrt(nSel_err**2/nSel**2+nAntiSel_err**2/nAntiSel**2)
      except ZeroDivisionError: F_err = 0
      Fhist.SetBinContent(j,F)
      Fhist.SetBinError(j,F_err)
      sysYErr.append(X*sysUnc)
      sysXErr.append(0.5)
      sysY.append(X)
      sysX.append(j-0.5)
#      Fhist.GetXaxis().SetBinLabel(j, '#splitline{HT'+str(i_htb)+'}{NJ'+str(i_njb)+'}')
      Fhist.GetXaxis().SetBinLabel(j, '#splitline{#splitline{'+label[0]+'}{'+label[1]+'}}{#splitline{'+label[2]+'}{'+label[3]+'}}')
      Fhist.GetYaxis().SetTitle('QCD_{sel.}/QCD_{antisel.}')
      j+=1

Fhist.Draw('L')
Fhist.SetMinimum(0.)
Fhist.SetMaximum(0.35)
Fhist.SetLabelSize(0.03)
#leg.AddEntry(Fhist,nBTagBinName((0,0)))
#text.DrawLatex(0.16,.96,"CMS #bf{#it{Preliminary}}")
text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
text.DrawLatex(0.85,0.96,"#bf{MC (13 TeV)}")
#text.DrawLatex(0.2,0.86,"#bf{incl. L_{T}>250}")

ax = array('d',sysX)
ay = array('d',sysY)
aexh = array('d',sysXErr)
aexl = array('d',sysXErr)
aeyh = array('d',sysYErr)
aeyl = array('d',sysYErr)
sys_err = ROOT.TGraphAsymmErrors(12, ax, ay, aexl, aexh, aeyl, aeyh)
sys_err.SetFillColor(ROOT.kGray+1)
sys_err.SetFillStyle(3244)
sys_err.Draw('2 same')
leg.AddEntry(sys_err,'sys. unc.','f')

l = ROOT.TLine(0,0.1,13,0.1)
l.SetLineColor(ROOT.kBlack)
l.SetLineStyle(7)
l.Draw()
line = ROOT.TLine(1,0,1,0.35)
line.SetLineColor(ROOT.kBlack)
line.SetLineStyle(ROOT.kDashed)
line.Draw()
line5 = ROOT.TLine(4,0,4,0.35)
line5.SetLineColor(ROOT.kBlack)
line5.SetLineStyle(ROOT.kDashed)
line5.Draw()
line2 = ROOT.TLine(7,0,7,0.35)
line2.SetLineColor(ROOT.kBlack)
line2.SetLineStyle(7)
line2.Draw()
line3 = ROOT.TLine(8,0,8,0.35)
line3.SetLineColor(ROOT.kBlack)
line3.SetLineStyle(ROOT.kDashed)
line3.Draw()
line4 = ROOT.TLine(10,0,10,0.35)
line4.SetLineColor(ROOT.kBlack)
line4.SetLineStyle(ROOT.kDashed)
line4.Draw()
leg.Draw()
text.DrawLatex(0.65,0.87,"#bf{QCD electrons systematic}")
canv.Print(wwwDir+prefix+'.png')
canv.Print(wwwDir+prefix+'.pdf')
canv.Print(wwwDir+prefix+'.root')

#canv2 = ROOT.TCanvas('canv2','canv2',600,600)
#ClosureHist=ROOT.TH1F('ClosureHist','ClosureHist',5,0,5)
#ClosureHist.SetLineWidth(2)
#k=0
#for i_CR, ltb in enumerate(sorted(fitCR[(3,4)])):
#  for i_htb,htb in enumerate(sorted(fitCR[(3,4)][ltb])):
#    for i_dP,dP in enumerate(sorted(fitCR[(3,4)][ltb][htb])):
#      k+=1
#      Selname, SelCut = nameAndCut(ltb, htb, (3,4), btb=(0,0), presel=SelStr, charge="", btagVar = 'nBJetMediumCSV30')
#      nSel,nSel_err   = getYieldFromChain(cQCD, SelCut, weight = weight_str, returnError=True)
#      result, result_err = getFraction(nSel,nSel_err,fitRes[(3,4)][ltb][htb]['QCD']['yield'],sqrt(fitRes[(3,4)][ltb][htb]['QCD']['yieldVar']))
#      print result,result_err
#      ClosureHist.SetBinContent(k,result)
#      ClosureHist.SetBinError(k,result_err)
#      ClosureHist.GetXaxis().SetBinLabel(i_CR+1, varBinName(ltb,'L_{T}'))
#      ClosureHist.GetYaxis().SetTitle('N^{pred}_{QCD}/N^{MC}_{QCD}')
#
#ClosureHist.Draw('L')
#ClosureHist.SetMinimum(0.)
#ClosureHist.SetMaximum(2.)
#text.DrawLatex(0.16,.96,"CMS #bf{#it{Preliminary}}")
##text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
#text.DrawLatex(0.65,0.96,"#bf{L="+str(lumi)+"fb^{-1} (13 TeV)}")
#
#line = ROOT.TLine()
#line.SetY1(1.0)
#line.SetX2(5)
#line.SetHorizontal()
#line.SetLineColor(ROOT.kBlack)
#line.SetLineStyle(ROOT.kDashed)
#line.Draw()
#
#canv2.Print(wwwDir+prefix+'FitClosure_inFitCR.png')
#canv2.Print(wwwDir+prefix+'FitClosure_inFitCR.pdf')
#canv2.Print(wwwDir+prefix+'FitClosure_inFitCR.root')

#canv2 = ROOT.TCanvas('canv2','canv2',600,600)
#
#ClosureHist=ROOT.TH1F('ClosureHist','ClosureHist',14,0,14)
#ClosureHist.SetLineWidth(2)
#k=0
#for i_CR, ltb in enumerate(sorted(CR[(3,4)])):
#  for i_htb,htb in enumerate(sorted(CR[(3,4)][ltb])):
#    for i_dP,dP in enumerate(sorted(CR[(3,4)][ltb][htb])):
#      k+=1
#      result, result_err = getFraction(res[(3,4)][ltb][htb][(0,0)][dP]['NQCDSelMC'],res[(3,4)][ltb][htb][(0,0)][dP]['NQCDSelMC_err'],res[(3,4)][ltb][htb][(0,0)][dP]['NQCDpred'],res[(3,4)][ltb][htb][(0,0)][dP]['NQCDpred_err'])
#      ClosureHist.SetBinContent(k,result)
#      ClosureHist.SetBinError(k,result_err)
#      ClosureHist.GetXaxis().SetBinLabel(k,str(k))
#      ClosureHist.GetYaxis().SetTitle('N^{pred}_{QCD}/N^{MC}_{QCD}')
#
#ClosureHist.Draw('L')
#ClosureHist.SetMinimum(0.)
#ClosureHist.SetMaximum(2.)
#text.DrawLatex(0.16,.96,"CMS #bf{#it{Preliminary}}")
##text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
#text.DrawLatex(0.7,0.96,"#bf{L="+str(lumi)+"fb^{-1} (13 TeV)}")
#
#line = ROOT.TLine()
#line.SetY1(1.0)
#line.SetX2(14)
#line.SetHorizontal()
#line.SetLineColor(ROOT.kBlack)
#line.SetLineStyle(ROOT.kDashed)
#line.Draw()
#
#canv2.Print(wwwDir+prefix+'FitClosure_inCR.png')
#canv2.Print(wwwDir+prefix+'FitClosure_inCR.pdf')
#canv2.Print(wwwDir+prefix+'FitClosure_inCR.root')

#canv3 = ROOT.TCanvas('canv3','canv3',600,600)
#
#ClosureHistSR=ROOT.TH1F('ClosureHistSR','ClosureHistSR',17,0,17)
#ClosureHistSR.SetLineWidth(2)
#k=0
#for i_njb, njb in enumerate(sorted(signalRegion)):
#  for i_CR, ltb in enumerate(sorted(signalRegion[njb])):
#    for i_htb,htb in enumerate(sorted(signalRegion[njb][ltb])):
#      for i_dP,dP in enumerate(sorted(signalRegion[njb][ltb][htb])):
#        k+=1
#        result, result_err = getFraction(res[njb][ltb][htb][(0,0)][dP]['NQCDSelMC'],res[njb][ltb][htb][(0,0)][dP]['NQCDSelMC_err'],res[njb][ltb][htb][(0,0)][dP]['NQCDpred'],res[njb][ltb][htb][(0,0)][dP]['NQCDpred_err'])
#        ClosureHistSR.SetBinContent(k,result)
#        ClosureHistSR.SetBinError(k,result_err)
#        ClosureHistSR.GetXaxis().SetBinLabel(k,str(k))
#        ClosureHistSR.GetYaxis().SetTitle('N^{pred}_{QCD}/N^{MC}_{QCD}')
#
#ClosureHistSR.Draw('L')
#ClosureHistSR.SetMinimum(0.)
#ClosureHistSR.SetMaximum(2.)
#text.DrawLatex(0.16,.96,"CMS #bf{#it{Preliminary}}")
##text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
#text.DrawLatex(0.65,0.96,"#bf{L="+str(lumi)+"fb^{-1} (13 TeV)}")
#
#line = ROOT.TLine()
#line.SetY1(1.0)
#line.SetX2(17)
#line.SetHorizontal()
#line.SetLineColor(ROOT.kBlack)
#line.SetLineStyle(ROOT.kDashed)
#line.Draw()
#
#canv3.Print(wwwDir+prefix+'FitClosure_inSR.png')
#canv3.Print(wwwDir+prefix+'FitClosure_inSR.pdf')
#canv3.Print(wwwDir+prefix+'FitClosure_inSR.root')


#plot F_sel-to-antisel binned in HT for SR Njets
#ratio_ht={}
#for stb in ltreg:
#  ratio_ht[stb]={}
#  first = True
#  canv = ROOT.TCanvas('canv','canv',600,600)
#  #canv.SetLogy()
#  l = ROOT.TLegend(0.65,0.85,0.98,0.95)
#  l.SetFillColor(0)
#  l.SetBorderSize(1)
#  l.SetShadowColor(ROOT.kWhite)
#  
#  t=ROOT.TLatex()
#  t.SetNDC()
#  t.SetTextSize(0.04)
#  t.SetTextAlign(11)
#  for i_njb, njb in enumerate(SRnjreg):
#    ratio_ht[stb][njb]={}
#    for btb in btreg:
#      ratio_ht[stb][njb][btb]=ROOT.TH1F('ratio_htHist','ratio_htHist',len(htreg),0,len(htreg))
#      ratio_ht[stb][njb][btb].SetLineColor(ROOT_colors[i_njb])
#      ratio_ht[stb][njb][btb].SetMarkerColor(ROOT_colors[i_njb])
#      ratio_ht[stb][njb][btb].SetLineWidth(2)
#      for i_htb, htb in enumerate(htreg):
#        antiSelname, antiSelCut = nameAndCut(stb, htb, njb, btb=btb, presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30')
#        Selname, SelCut         = nameAndCut(stb, htb, njb, btb=btb, presel=SelStr, charge="", btagVar = 'nBJetMediumCSV30')
#        nSel,nSel_err = getYieldFromChain(cQCD, SelCut, weight = weight_str, returnError=True)
#        nAntiSel,nAntiSel_err = getYieldFromChain(cQCD, antiSelCut, weight = weight_str, returnError=True)
#        try: F=nSel/nAntiSel
#        except ZeroDivisionError: F=float('nan')
#        try: F_err= F*sqrt(nSel_err**2/nSel**2+nAntiSel_err**2/nAntiSel**2)
#        except ZeroDivisionError: F_err=0
#        try:
#          ratio_ht[stb][njb][btb].SetBinContent(i_htb+1,F)
#          ratio_ht[stb][njb][btb].SetBinError(i_htb+1,F_err)
#        except KeyError: pass
#        ratio_ht[stb][njb][btb].GetXaxis().SetBinLabel(i_htb+1, varBinName(htb,'H_{T}'))
#        ratio_ht[stb][njb][btb].GetYaxis().SetTitle('F_{sel-to-antisel}')
#        ratio_ht[stb][njb][btb].GetYaxis().SetRangeUser(0.0,0.5)
##          ratio_ht[stb][njb].GetXaxis().SetTitle('F_{sel-to-antisel}')
#      l.AddEntry(ratio_ht[stb][njb][btb], nJetBinName(njb))
#      if first:
#        ratio_ht[stb][njb][btb].Draw()
#        first = False
#      else:
#        ratio_ht[stb][njb][btb].Draw('same') 
#      l.Draw()
#      t.DrawLatex(0.2,0.85,'#bf{'+varBinName(stb,'L_{T}')+'}')
#      text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
#      text.DrawLatex(0.75,0.96,"#bf{MC (13 TeV)}")
#      canv.Print(wwwDir+prefix+'FsaMC_ht_'+nameAndCut(stb, None, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
#      canv.Print(wwwDir+prefix+'FsaMC_ht_'+nameAndCut(stb, None, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
#      canv.Print(wwwDir+prefix+'FsaMC_ht_'+nameAndCut(stb, None, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')


#plot F_sel-to-antisel binned in ST for all Njets
#ratio_st={}
#for htb in htreg:
#  ratio_st[htb]={}
#  first = True
#  canv2= ROOT.TCanvas('canv2','canv2',600,600)
#  #canv.SetLogy()
#  l2 = ROOT.TLegend(0.65,0.85,0.95,0.95)
#  l2.SetFillColor(0)
#  l2.SetBorderSize(1)
#  l2.SetShadowColor(ROOT.kWhite)
#  
#  t=ROOT.TLatex()
#  t.SetNDC()
#  t.SetTextSize(0.04)
#  t.SetTextAlign(11)
#  for i_njb, njb in enumerate(njreg):
#    ratio_st[htb][njb]={}
#    for btb in btreg:
#      ratio_st[htb][njb][btb]=ROOT.TH1F('ratio_stHist','ratio_stHist',len(streg),0,len(streg))
#      ratio_st[htb][njb][btb].SetLineColor(ROOT_colors[i_njb])
#      ratio_st[htb][njb][btb].SetLineWidth(2)
#      for i_stb, stb in enumerate(streg):
#        nQCDsel = bins[njb][stb][htb][btb]['nQCDSelected'] 
#        nQCDselVar = bins[njb][stb][htb][btb]['nQCDSelectedVar'] 
#        nQCDantisel = bins[njb][stb][htb][btb]['nAntiSelected'] 
#        nQCDantiselVar = bins[njb][stb][htb][btb]['nAntiSelectedVar'] 
##          print nQCDsel, nQCDantisel
#        if nQCDantisel>0:
#          F=nQCDsel/nQCDantisel
#          print 'F_sel-to-anti-sel('+str(stb)+','+str(njb)+','+str(htb)+'):',F
#          if F>0:
#            F_err= F*sqrt(nQCDselVar/nQCDsel**2+nQCDantiselVar/nQCDantisel**2)
#            ratio_st[htb][njb][btb].SetBinContent(i_stb+1,F)
#            ratio_st[htb][njb][btb].SetBinError(i_stb+1,F_err)
#            print 'F_sel-to-anti-sel Error('+str(stb)+','+str(njb)+','+str(htb)+'):',F_err
#        ratio_st[htb][njb][btb].GetXaxis().SetBinLabel(i_stb+1, varBinName(stb,'S_{T}'))
#        ratio_st[htb][njb][btb].GetYaxis().SetTitle('F_{sel-to-antisel}')
#        ratio_st[htb][njb][btb].GetYaxis().SetRangeUser(0.0,1.0)
##        ratio_st[htb][njb].GetXaxis().SetTitle('F_{sel-to-antisel}')
#      l2.AddEntry(ratio_st[htb][njb][btb], nJetBinName(njb))
#      if first:
#        ratio_st[htb][njb][btb].Draw()
#        first = False
#      else:
#        ratio_st[htb][njb][btb].Draw('same') 
#      l2.Draw()
#      t.DrawLatex(0.175,0.85,varBinName(htb,'H_{T}'))
#      text.DrawLatex(0.15,.96,"CMS Simulation")
#      text.DrawLatex(0.65,0.96,"L="+str(targetLumi/1000)+" fb^{-1} (13 TeV)")
#      canv2.Print(wwwDir+presel+'Fsa_st_'+nameAndCut(None, htb, njetb=None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
#      canv2.Print(wwwDir+presel+'Fsa_st_'+nameAndCut(None, htb, njetb=None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
#      canv2.Print(wwwDir+presel+'Fsa_st_'+nameAndCut(None, htb, njetb=None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')

#plot F_sel-to-antisel binned in ST vs HT
#ratio_2d={}
#for njb in njreg:
#  ratio_2d[njb]={}
#  canv3= ROOT.TCanvas('canv3','canv3',600,600)
#  #canv.SetLogy()
##  l3 = ROOT.TLegend(0.65,0.75,0.95,0.95)
##  l3.SetFillColor(0)
##  l3.SetBorderSize(1)
##  l3.SetShadowColor(ROOT.kWhite)
#  
#  t=ROOT.TLatex()
#  t.SetNDC()
#  t.SetTextSize(0.04)
#  t.SetTextAlign(11)
#  for btb in btreg:
#    ratio_2d[njb][btb]={}
#    ratio_2d[njb][btb]=ROOT.TH2F('ratio_2dHist','ratio_2dHist',len(htreg),0,len(htreg),len(streg),0,len(streg))
#    for i_htb, htb in enumerate(htreg):
#      ratio_2d[njb][btb].GetXaxis().SetBinLabel(i_htb+1,varBinName(htb,'H_{T}'))
#    for i_stb, stb in enumerate(streg):
#      ratio_2d[njb][btb].GetYaxis().SetBinLabel(i_stb+1,varBinName(stb,'S_{T}'))
#
#    for i_htb, htb in enumerate(htreg):
#      for i_stb, stb in enumerate(streg):
#        nQCDsel = bins[njb][stb][htb][btb]['nQCDSelected'] 
#        nQCDselVar = bins[njb][stb][htb][btb]['nQCDSelectedVar'] 
#        nQCDantisel = bins[njb][stb][htb][btb]['nAntiSelected'] 
#        nQCDantiselVar = bins[njb][stb][htb][btb]['nAntiSelectedVar'] 
##          print nQCDsel, nQCDantisel
#        if nQCDantisel>0:
#          F=nQCDsel/nQCDantisel
#          print 'F_sel-to-anti-sel('+str(stb)+','+str(njb)+','+str(htb)+'):',F
#          if F>0:
#            F_err= F*sqrt(nQCDselVar/nQCDsel**2+nQCDantiselVar/nQCDantisel**2)
#            ratio_2d[njb][btb].SetBinContent(i_htb+1,i_stb+1,F)
#            ratio_2d[njb][btb].SetBinError(i_htb+1,i_stb+1,F_err)
#            print 'F_sel-to-anti-sel Error('+str(stb)+','+str(njb)+','+str(htb)+'):',F_err
##      l.AddEntry(ratio_2d[htb][njb][btb], nJetBinName(njb))
#        ratio_2d[njb][btb].Draw('COLZ TEXTE')
#      t.DrawLatex(0.175,0.85,nJetBinName(njb))
#      text.DrawLatex(0.15,.96,"CMS Simulation")
#      text.DrawLatex(0.65,0.96,"L="+str(targetLumi/1000)+" fb^{-1} (13 TeV)") 
#      canv3.Print(wwwDir+presel+'st_vs_ht_'+nameAndCut(None, None, njetb=njb, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
#      canv3.Print(wwwDir+presel+'st_vs_ht_'+nameAndCut(None, None, njetb=njb, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
#      canv3.Print(wwwDir+presel+'st_vs_ht_'+nameAndCut(None, None, njetb=njb, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')

#plot F_sel-to-antisel binned in nJets for all ST bins
#ratio_nj={}
#for htb in [(500,-1)]:
#  ratio_nj[htb]={}
#  first = True
#  canv4 = ROOT.TCanvas('canv','canv',600,600)
#  #canv.SetLogy()
#  l3 = ROOT.TLegend(0.65,0.80,0.98,0.95)
#  l3.SetFillColor(0)
#  l3.SetBorderSize(1)
#  l3.SetShadowColor(ROOT.kWhite)
#  text = ROOT.TLatex()
#  text.SetNDC()
#  text.SetTextSize(0.04)
#  text.SetTextAlign(11)
#  t3=ROOT.TLatex()
#  t3.SetNDC()
#  t3.SetTextSize(0.04)
#  t3.SetTextAlign(11)
#  for i_stb, stb in enumerate(ltreg):
#    ratio_nj[htb][stb]={}
#    for btb in btreg:
#      ratio_nj[htb][stb][btb]=ROOT.TH1F('ratio_njHist','ratio_njHist',len(njreg),0,len(njreg))
#      ratio_nj[htb][stb][btb].SetLineColor(ROOT_colors[i_stb])
#      ratio_nj[htb][stb][btb].SetMarkerColor(ROOT_colors[i_stb])
#      ratio_nj[htb][stb][btb].SetLineWidth(2)
#      for i_njb, njb in enumerate(njreg):
#        antiSelname, antiSelCut = nameAndCut(stb, htb, njb, btb=btb, presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30')
#        Selname, SelCut         = nameAndCut(stb, htb, njb, btb=btb, presel=SelStr, charge="", btagVar = 'nBJetMediumCSV30')
#        nSel,nSel_err = getYieldFromChain(cQCD, SelCut, weight = weight_str, returnError=True)
#        nAntiSel,nAntiSel_err = getYieldFromChain(cQCD, antiSelCut, weight = weight_str, returnError=True)
##        rcs = getRCS(cQCD, antiSelCut, 0.75, useWeight = True, weight = 'weight')
##        if rcs['rCS']!=float('nan') and rcs['rCS']> 0.: 
##          ratio_nj[htb][stb][btb].SetBinContent(i_njb+1,rcs['rCS'])
##          ratio_nj[htb][stb][btb].SetBinError(i_njb+1,rcs['rCSE_sim'])
#        try: F=nSel/nAntiSel
#        except ZeroDivisionError: F=float('nan')
#        try: F_err= F*sqrt(nSel_err**2/nSel**2+nAntiSel_err**2/nAntiSel**2)
#        except ZeroDivisionError: F_err=0
#        ratio_nj[htb][stb][btb].SetBinContent(i_njb+1,F)
#        ratio_nj[htb][stb][btb].SetBinError(i_njb+1,F_err)
#        ratio_nj[htb][stb][btb].GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb))
#        ratio_nj[htb][stb][btb].GetYaxis().SetTitle('F_{sel-to-antisel}')
##        ratio_nj[htb][stb][btb].GetYaxis().SetTitle('R^{antisel}_{CS}')
#        ratio_nj[htb][stb][btb].GetYaxis().SetRangeUser(0.0,0.5)
#      #l3.AddEntry(ratio_nj[htb][stb][btb], varBinName(stb,'L_{T}'))
#      if first:
#        ratio_nj[htb][stb][btb].Draw()
#        first = False
#      else:
#        ratio_nj[htb][stb][btb].Draw('same') 
#      #l3.Draw()
#      t3.DrawLatex(0.2,0.85,'#bf{'+varBinName(htb,'H_{T}')+'}')
#      t3.DrawLatex(0.2,0.8,'#bf{'+varBinName(stb,'L_{T}')+'}')
#      text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
#      text.DrawLatex(0.75,0.96,"#bf{MC (13 TeV)}")     
#      canv4.Print(wwwDir+prefix+'FsaMC_nj_'+nameAndCut(None, htb, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
#      canv4.Print(wwwDir+prefix+'FsaMC_nj_'+nameAndCut(None, htb, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
#      canv4.Print(wwwDir+prefix+'FsaMC_nj_'+nameAndCut(None, htb, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')

#plot F_sel-to-antisel binned in ST for all Njets
#ratio_st={}
#for htb in [(500,-1)]:
#  ratio_st[htb]={}
#  first = True
#  canv2= ROOT.TCanvas('canv2','canv2',600,600)
#  #canv.SetLogy()
#  l2 = ROOT.TLegend(0.65,0.85,0.98,0.95)
#  l2.SetFillColor(0)
#  l2.SetBorderSize(1)
#  l2.SetShadowColor(ROOT.kWhite)
#  
#  t=ROOT.TLatex()
#  t.SetNDC()
#  t.SetTextSize(0.04)
#  t.SetTextAlign(11)
#  for i_njb, njb in enumerate(SRnjreg):
#    ratio_st[htb][njb]={}
#    for btb in btreg:
#      ratio_st[htb][njb][btb]=ROOT.TH1F('ratio_stHist','ratio_stHist',3,0,3)
#      ratio_st[htb][njb][btb].SetLineColor(ROOT_colors[i_njb])
#      ratio_st[htb][njb][btb].SetMarkerColor(ROOT_colors[i_njb])
#      ratio_st[htb][njb][btb].SetLineWidth(2)
#      for i_stb, stb in enumerate([(250,350),(350,450),(450,-1)]):
#        antiSelname, antiSelCut = nameAndCut(stb, htb, njb, btb=btb, presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30')
#        rcs = getRCS(cQCD, antiSelCut, 0.75, useWeight = True, weight = 'weight')
#        if rcs['rCS']!=float('nan') and rcs['rCS']> 0.: 
#          ratio_st[htb][njb][btb].SetBinContent(i_stb+1,rcs['rCS'])
#          ratio_st[htb][njb][btb].SetBinError(i_stb+1,rcs['rCSE_sim'])
#        ratio_st[htb][njb][btb].GetXaxis().SetBinLabel(i_stb+1, varBinName(stb,'L_{T}'))
#        ratio_st[htb][njb][btb].GetYaxis().SetTitle('R^{antisel.}_{CS}')
#        ratio_st[htb][njb][btb].GetYaxis().SetRangeUser(0.0,0.05)
##        ratio_st[htb][njb].GetXaxis().SetTitle('F_{sel-to-antisel}')
#      l2.AddEntry(ratio_st[htb][njb][btb], nJetBinName(njb))
#      if first:
#        ratio_st[htb][njb][btb].Draw()
#        first = False
#      else:
#        ratio_st[htb][njb][btb].Draw('same') 
#      l2.Draw()
#      t.DrawLatex(0.2,0.85,'#bf{'+varBinName(htb,'H_{T}')+'}')
#      text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
#      text.DrawLatex(0.75,0.96,"#bf{MC (13 TeV)}")
#      canv2.Print(wwwDir+prefix+'rCS_lt_deltaPhi075'+nameAndCut(None, htb, njetb=None, btb=btb, presel="deltaPhiGT075", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
#      canv2.Print(wwwDir+prefix+'rCS_lt_deltaPhi075'+nameAndCut(None, htb, njetb=None, btb=btb, presel="deltaPhiGT075", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
#      canv2.Print(wwwDir+prefix+'rCS_lt_deltaPhi075'+nameAndCut(None, htb, njetb=None, btb=btb, presel="deltaPhiGT075", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')

#plot F_sel-to-antisel binned in nJets for all ST bins
#ratio_nj={}
#for htb in [(500,-1)]:
#  ratio_nj[htb]={}
#  first = True
#  canv4 = ROOT.TCanvas('canv','canv',600,600)
#  #canv.SetLogy()
#  l3 = ROOT.TLegend(0.65,0.80,0.98,0.95)
#  l3.SetFillColor(0)
#  l3.SetBorderSize(1)
#  l3.SetShadowColor(ROOT.kWhite)
#  text = ROOT.TLatex()
#  text.SetNDC()
#  text.SetTextSize(0.04)
#  text.SetTextAlign(11)
#  t3=ROOT.TLatex()
#  t3.SetNDC()
#  t3.SetTextSize(0.04)
#  t3.SetTextAlign(11)
#  for i_stb, stb in enumerate(ltreg):
#    ratio_nj[htb][stb]={}
#    for btb in btreg:
#      ratio_nj[htb][stb][btb]=ROOT.TH1F('ratio_njHist','ratio_njHist',len(njreg),0,len(njreg))
#      ratio_nj[htb][stb][btb].SetLineColor(ROOT_colors[i_stb])
#      ratio_nj[htb][stb][btb].SetMarkerColor(ROOT_colors[i_stb])
#      ratio_nj[htb][stb][btb].SetLineWidth(2)
#      for i_njb, njb in enumerate(njreg):
#        antiSelname, antiSelCut = nameAndCut(stb, htb, njb, btb=btb, presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30')
#        Selname, SelCut         = nameAndCut(stb, htb, njb, btb=btb, presel=SelStr, charge="", btagVar = 'nBJetMediumCSV30')
#        nSel,nSel_err = getYieldFromChain(cQCD, SelCut, weight = weight_str, returnError=True)
#        nAntiSel,nAntiSel_err = getYieldFromChain(cQCD, antiSelCut, weight = weight_str, returnError=True)
#        rcs = getRCS(cQCD, antiSelCut, 0.75, useWeight = True, weight = 'weight')
#        if rcs['rCS']!=float('nan') and rcs['rCS']> 0.: 
#          ratio_nj[htb][stb][btb].SetBinContent(i_njb+1,rcs['rCS'])
#          ratio_nj[htb][stb][btb].SetBinError(i_njb+1,rcs['rCSE_sim'])
##        try: F=nSel/nAntiSel
##        except ZeroDivisionError: F=float('nan')
##        try: F_err= F*sqrt(nSel_err**2/nSel**2+nAntiSel_err**2/nAntiSel**2)
##        except ZeroDivisionError: F_err=0
##        ratio_nj[htb][stb][btb].SetBinContent(i_njb+1,F)
##        ratio_nj[htb][stb][btb].SetBinError(i_njb+1,F_err)
#        ratio_nj[htb][stb][btb].GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb))
##        ratio_nj[htb][stb][btb].GetYaxis().SetTitle('F_{sel-to-antisel}')
#        ratio_nj[htb][stb][btb].GetYaxis().SetTitle('R^{antisel}_{CS}')
#        ratio_nj[htb][stb][btb].GetYaxis().SetRangeUser(0.0,0.1)
#      l3.AddEntry(ratio_nj[htb][stb][btb], varBinName(stb,'L_{T}'))
#      if first:
#        ratio_nj[htb][stb][btb].Draw()
#        first = False
#      else:
#        ratio_nj[htb][stb][btb].Draw('same') 
#      l3.Draw()
#      t3.DrawLatex(0.2,0.85,'#bf{'+varBinName(htb,'H_{T}')+'}')
#      text.DrawLatex(0.16,.96,"CMS #bf{#it{Simulation}}")
#      text.DrawLatex(0.75,0.96,"#bf{MC (13 TeV)}")     
#      canv4.Print(wwwDir+prefix+'rCS_nj_deltaPhi075'+nameAndCut(None, htb, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.png')
#      canv4.Print(wwwDir+prefix+'rCS_nj_deltaPhi075'+nameAndCut(None, htb, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.pdf')
#      canv4.Print(wwwDir+prefix+'rCS_nj_deltaPhi075'+nameAndCut(None, htb, None, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'.root')

