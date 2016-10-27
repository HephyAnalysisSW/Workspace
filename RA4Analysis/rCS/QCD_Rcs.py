import ROOT
import os, sys, copy, math
import pickle, operator

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from array import array
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed_2 import *

from Workspace.RA4Analysis.cmgTuples_Data25ns_miniAODv2_postprocessed import *
from Workspace.HEPHYPythonTools.user import username

from Workspace.RA4Analysis.rCShelpers import *

from predictionConfig import *

ROOT.gStyle.SetOptStat("")
ROOT.TH1F().SetDefaultSumw2()


triggers = "(HLT_EleHT350||HLT_MuHT350)"
filters = "Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_CSCTightHaloFilter && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter"
presel = "((!isData&&singleLeptonic)||(isData&&"+triggers+"&&((muonDataSet&&singleMuonic)||(eleDataSet&&singleElectronic))&&"+filters+"))"
presel += "&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&st>250&&nJet30>2&&htJet30j>500"
newpresel = presel

totalWeight = 'weight*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*TopPtWeight*0.94*puReweight_true_max4'
QCD = {'name':'QCD', 'chain':getChain(QCDHT_25ns,histname=''), 'color':color('QCD'),'weight':totalWeight, 'niceName':'QCD', 'cut':''}
can = ROOT.TCanvas('can','can',700,700)

deltaPhis = [0.75, 1.]
njets = [(3,3),(4,4),(5,5),(6,7),(8,-1)]
hts = [(500,750),(750,1000),(1000,-1)]
lts = [(250,350),(350,450),(450,-1)]

path = '/afs/hephy.at/user/d/dspitzbart/www/Results2016/QCD_Rcs/QCD_Rcs_0b_'

def getValErrString(val,err, precision=3):
  return str(round(val,precision))+' +/- '+str(round(err,precision))

def printMatrix(matrix, name='MATRIX', precision=5):
  a = matrix.GetNrows()
  b = matrix.GetNcols()
  fmt = ''
  for i in range(b+1):
    fmt += '{'+str(i)+':<12}'
  #rows = []
  rows = name + '\n\n'
  tup = (' ',)
  for i in range(b):
    tup += ('p'+str(i),)
  exec('row=fmt.format'+str(tup))
  rows += row +'\n'
  #print row
  for i in range(a):
    tup = ()
    tup += ('p'+str(i),)
    for j in range(b):
      tup += ("%0.2e"%matrix(i,j),)
    exec('row=fmt.format'+str(tup))
    rows += row + '\n'
    #print row
  return rows


for deltaPhi in deltaPhis:
  rcsH = ROOT.TH1F('rcsH','rcsH',5,0,5)
  for i,njb in enumerate(njets):
    name, cut = nameAndCut((250,-1), (500,-1), njb, btb=(0,0), presel=presel)
    r = getRCS(QCD['chain'], cut, deltaPhi)
    rcsH.SetBinContent(i+1, r['rCS'])
    if math.isnan(r['rCSE_pred']):
      if i>0: rcsH.SetBinError(i+1, 2*rcsH.GetBinError(i))
      else: rcsH.SetBinError(i+1, 0.2)
    else: rcsH.SetBinError(i+1, r['rCSE_pred'])
    rcsH.GetXaxis().SetBinLabel(i+1, nJetBinName(njb))
  
  f1 = ROOT.TF1("f1", "[0]+[1]*x", 0, rcsH.GetNbinsX())
  f1.SetParameters(2,-1)
  f1.SetLineWidth(2)
  res = rcsH.Fit("f1", "S")
  D   = f1.GetParameter(0)
  D_E = f1.GetParError(0)
  K   = f1.GetParameter(1)
  K_E = f1.GetParError(1)

  covMatrix = res.GetCovarianceMatrix()
  corMatrix = res.GetCorrelationMatrix()
  txtFile = file(path+'_njet_matrices_'+str(deltaPhi).replace('.','p')+'.txt','w')
  txt_str = printMatrix(covMatrix, name='Covariance Matrix') + '\n' + printMatrix(corMatrix, name='Correlation Matrix')
  txtFile.write(txt_str)
  txtFile.close()
  
  for i, njet in enumerate(njets):
    v_array = array('d', [1, (i+0.5)])
    v1 = ROOT.TVectorD(2, v_array)
    v2 = ROOT.TVectorD(2, v_array)
    v1*=covMatrix
    variance = v1(0)*v2(0)+v1(1)*v2(1)
    print njet, variance, sqrt(variance)
  
  rcsH.Draw('EH')
  rcsH.SetMaximum(0.1)
  rcsH.SetMinimum(0.)
  rcsH.SetLineWidth(2)
  rcsH.SetMarkerSize(0)

  hint1 = ROOT.TH1F("hint1", "1 sigma", 100, 0, 5)
  hint2 = ROOT.TH1F("hint2", "2 sigma", 100, 0, 5)
  hint1.SetMarkerSize(0)
  hint2.SetMarkerSize(0)
  rcsH.SetStats(False)
  ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(hint1, 0.68)
  ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(hint2, 0.95)
  
  hint1.SetFillColorAlpha(ROOT.kGreen, 0.45)
  hint2.SetFillColorAlpha(ROOT.kYellow, 0.45)
  hint2.Draw("e3 same")
  hint1.Draw("e3 same")
  
  a = covMatrix(0,0)
  b = c = covMatrix(0,1)
  d = covMatrix(1,1)
  f2 = ROOT.TF1("f2", "sqrt([0] + [1]*x + [2]*x**2) + [3] + [4]*x", 0, rcsH.GetNbinsX())
  f2.SetParameters(a,b+c,d, D, K)
  f2.SetLineColor(ROOT.kBlue)
  f2.SetLineWidth(2)
  f2.Draw('same')
  
  f1.Draw('same')
  rcsH.Draw('EH same')

  latex1 = ROOT.TLatex()
  latex1.SetNDC()
  latex1.SetTextSize(0.03)
  latex1.SetTextAlign(11)
  latex1.DrawLatex(0.6,0.86,'linear fit k x + d')
  latex1.DrawLatex(0.6,0.83,'k = '+str(round(K*1000,2))+' #pm '+str(round(K_E*1000,2))+' #times 10^{-3}')
  latex1.DrawLatex(0.6,0.8,'d = '+str(round(D*1000,2))+' #pm '+str(round(D_E*1000,2))+' #times 10^{-3}')

  can.Print(path + '_njet_' + str(deltaPhi).replace('.','p')+'.png')
  can.Print(path + '_njet_' + str(deltaPhi).replace('.','p')+'.root')
  can.Print(path + '_njet_' + str(deltaPhi).replace('.','p')+'.pdf')
  del rcsH, hint1, hint2
  
  for htb in hts:
    rcsH = ROOT.TH1F('rcsH','rcsH',5,0,5)
    for i,njb in enumerate(njets):
      name, cut = nameAndCut((250,-1), htb, njb, btb=(0,0), presel=presel)
      r = getRCS(QCD['chain'], cut, deltaPhi)
      rcsH.SetBinContent(i+1, r['rCS'])
      if math.isnan(r['rCSE_pred']):
        if i>0: rcsH.SetBinError(i+1, 2*rcsH.GetBinError(i))
        else: rcsH.SetBinError(i+1, 0.2)
      else: rcsH.SetBinError(i+1, r['rCSE_pred'])
      rcsH.GetXaxis().SetBinLabel(i+1, nJetBinName(njb))
    
    f1 = ROOT.TF1("f1", "[0]+[1]*x", 0, rcsH.GetNbinsX())
    f1.SetParameters(2,-1)
    f1.SetLineWidth(2)
    rcsH.Fit("f1", "Q")
    D   = f1.GetParameter(0)
    D_E = f1.GetParError(0)
    K   = f1.GetParameter(1)
    K_E = f1.GetParError(1)
    
    rcsH.Draw('EH')
    rcsH.SetMaximum(0.1)
    rcsH.SetMinimum(0.)
    rcsH.SetLineWidth(2)
    rcsH.SetMarkerSize(0)
    rcsH.SetStats(False)

    hint1 = ROOT.TH1F("hint1", "1 sigma", 100, 0, 5)
    hint2 = ROOT.TH1F("hint2", "2 sigma", 100, 0, 5)
    hint1.SetMarkerSize(0)
    hint2.SetMarkerSize(0)
    ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(hint1, 0.68)
    ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(hint2, 0.95)

    hint1.SetFillColorAlpha(ROOT.kGreen, 0.45)
    hint2.SetFillColorAlpha(ROOT.kYellow, 0.45)
    hint2.Draw("e3 same")
    hint1.Draw("e3 same")
    f1.Draw('same')
    rcsH.Draw('EH same')
    
    latex1 = ROOT.TLatex()
    latex1.SetNDC()
    latex1.SetTextSize(0.03)
    latex1.SetTextAlign(11)
    latex1.DrawLatex(0.6,0.86,'linear fit k x + d')
    latex1.DrawLatex(0.6,0.83,'k = '+str(round(K*1000,2))+' #pm '+str(round(K_E*1000,2))+' #times 10^{-3}')
    latex1.DrawLatex(0.6,0.8,'d = '+str(round(D*1000,2))+' #pm '+str(round(D_E*1000,2))+' #times 10^{-3}')
    
    htb_str ='_ht'+str(htb[0])
    if htb[1]>0:
      htb_str += '-'+str(htb[1])
    
    can.Print(path + '_njet_' + str(deltaPhi).replace('.','p')+htb_str+'.png')
    can.Print(path + '_njet_' + str(deltaPhi).replace('.','p')+htb_str+'.root')
    can.Print(path + '_njet_' + str(deltaPhi).replace('.','p')+htb_str+'.pdf')
    del rcsH, hint1, hint2


  #HT stuff to follow
  print
  print "Rcs vs HT"

  rcsH = ROOT.TH1F('rcsH','rcsH',3,0,3)
  for i,htb in enumerate(hts):
    name, cut = nameAndCut((250,-1), htb, (3,-1), btb=(0,0), presel=presel)
    r = getRCS(QCD['chain'], cut, deltaPhi)
    print getValErrString(r['rCS'], r['rCSE_pred'], precision=4)
    rcsH.SetBinContent(i+1, r['rCS'])
    rcsH.SetBinError(i+1, r['rCSE_pred'])
    rcsH.GetXaxis().SetBinLabel(i+1, varBinName(htb,"H_{T}"))
  
  f1 = ROOT.TF1("f1", "[0]+[1]*x", 0, rcsH.GetNbinsX())
  f1.SetParameters(2,-1)
  f1.SetLineWidth(2)
  #rcsH.Fit("f1", "Q")
  res = rcsH.Fit("f1", "S")
  res.Print("V")
  D   = f1.GetParameter(0)
  D_E = f1.GetParError(0)
  K   = f1.GetParameter(1)
  K_E = f1.GetParError(1)

  covMatrix = res.GetCovarianceMatrix()
  corMatrix = res.GetCorrelationMatrix()
  txtFile = file(path+'_HT_matrices_'+str(deltaPhi).replace('.','p')+'.txt','w')
  txt_str = printMatrix(covMatrix, name='Covariance Matrix') + '\n' + printMatrix(corMatrix, name='Correlation Matrix')
  txtFile.write(txt_str)
  txtFile.close()
  
  #covM = ROOT.TMatrixD(2,2)
  #covM.SetMatrixArray(covMatrix.GetMatrixArray())
  for i, ht in enumerate(hts):
    v_array = array('d', [1, (i+0.5)])
    v1 = ROOT.TVectorD(2, v_array)
    v2 = ROOT.TVectorD(2, v_array)
    v1*=covMatrix
    variance = v1(0)*v2(0)+v1(1)*v2(1)
    print ht, variance, sqrt(variance)
  
  rcsH.Draw('EH')
  rcsH.SetMaximum(0.4)
  rcsH.SetMinimum(0.)
  rcsH.SetLineWidth(2)
  rcsH.SetMarkerSize(0)
  rcsH.SetStats(False)

  hint1 = ROOT.TH1F("hint1", "1 sigma", 100, 0, rcsH.GetNbinsX())
  hint2 = ROOT.TH1F("hint2", "2 sigma", 100, 0, rcsH.GetNbinsX())
  hint1.SetMarkerSize(0)
  hint2.SetMarkerSize(0)
  ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(hint1, 0.68)
  ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(hint2, 0.95)

  hint1.SetFillColorAlpha(ROOT.kGreen, 0.45)
  hint2.SetFillColorAlpha(ROOT.kYellow, 0.45)
  hint2.Draw("e3 same")
  hint1.Draw("e3 same")

  a = covMatrix(0,0)
  b = c = covMatrix(0,1)
  d = covMatrix(1,1)  
  f2 = ROOT.TF1("f2", "sqrt([0] + [1]*x + [2]*x**2) + [3] + [4]*x", 0, rcsH.GetNbinsX())
  f2.SetParameters(a,b+c,d, D, K)
  f2.SetLineColor(ROOT.kBlue)
  f2.SetLineWidth(2)
  f2.Draw('same')

  f1.Draw('same')
  rcsH.Draw('EH same')
  
  latex1 = ROOT.TLatex()
  latex1.SetNDC()
  latex1.SetTextSize(0.03)
  latex1.SetTextAlign(11)
  latex1.DrawLatex(0.6,0.86,'linear fit k x + d')
  latex1.DrawLatex(0.6,0.83,'k = '+str(round(K*1000,2))+' #pm '+str(round(K_E*1000,2))+' #times 10^{-3}')
  latex1.DrawLatex(0.6,0.8,'d = '+str(round(D*1000,2))+' #pm '+str(round(D_E*1000,2))+' #times 10^{-3}')
  
  can.Print(path + '_HT_' + str(deltaPhi).replace('.','p')+'.png')
  can.Print(path + '_HT_' + str(deltaPhi).replace('.','p')+'.root')
  can.Print(path + '_HT_' + str(deltaPhi).replace('.','p')+'.pdf')
  del rcsH, hint1, hint2
  
  #LT stuff to follow
  
  rcsH = ROOT.TH1F('rcsH','rcsH',3,0,3)
  for i,ltb in enumerate(lts):
    name, cut = nameAndCut(ltb, (500,-1), (3,-1), btb=(0,0), presel=presel)
    r = getRCS(QCD['chain'], cut, deltaPhi)
    rcsH.SetBinContent(i+1, r['rCS'])
    rcsH.SetBinError(i+1, r['rCSE_pred'])
    rcsH.GetXaxis().SetBinLabel(i+1, varBinName(ltb,"L_{T}"))
  
  f1 = ROOT.TF1("f1", "[0]+[1]*x", 0, rcsH.GetNbinsX())
  f1.SetParameters(2,-1)
  f1.SetLineWidth(2)
  #rcsH.Fit("f1", "Q")
  res = rcsH.Fit("f1", "S")
  D   = f1.GetParameter(0)
  D_E = f1.GetParError(0)
  K   = f1.GetParameter(1)
  K_E = f1.GetParError(1)

  covMatrix = res.GetCovarianceMatrix()
  corMatrix = res.GetCorrelationMatrix()
  txtFile = file(path+'_LT_matrices_'+str(deltaPhi).replace('.','p')+'.txt','w')
  txt_str = printMatrix(covMatrix, name='Covariance Matrix') + '\n' + printMatrix(corMatrix, name='Correlation Matrix')
  txtFile.write(txt_str)
  txtFile.close()
  
  for i, lt in enumerate(lts):
    v_array = array('d', [1, (i+0.5)])
    v1 = ROOT.TVectorD(2, v_array)
    v2 = ROOT.TVectorD(2, v_array)
    v1*=covMatrix
    variance = v1(0)*v2(0)+v1(1)*v2(1)
    print lt, variance, sqrt(variance)
  
  rcsH.Draw('EH')
  rcsH.SetMaximum(0.1)
  rcsH.SetMinimum(0.)
  rcsH.SetLineWidth(2)
  rcsH.SetMarkerSize(0)
  rcsH.SetStats(False)

  hint1 = ROOT.TH1F("hint1", "1 sigma", 100, 0, rcsH.GetNbinsX())
  hint2 = ROOT.TH1F("hint2", "2 sigma", 100, 0, rcsH.GetNbinsX())
  hint1.SetMarkerSize(0)
  hint2.SetMarkerSize(0)
  ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(hint1, 0.68)
  ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(hint2, 0.95)

  hint1.SetFillColorAlpha(ROOT.kGreen, 0.45)
  hint2.SetFillColorAlpha(ROOT.kYellow, 0.45)
  hint2.Draw("e3 same")
  hint1.Draw("e3 same")
  
  a = covMatrix(0,0)
  b = c = covMatrix(0,1)
  d = covMatrix(1,1)
  f2 = ROOT.TF1("f2", "sqrt([0] + [1]*x + [2]*x**2) + [3] + [4]*x", 0, rcsH.GetNbinsX())
  f2.SetParameters(a,b+c,d, D, K)
  f2.SetLineColor(ROOT.kBlue)
  f2.SetLineWidth(2)
  f2.Draw('same')
  
  f1.Draw('same')
  rcsH.Draw('EH same')
  
  latex1 = ROOT.TLatex()
  latex1.SetNDC()
  latex1.SetTextSize(0.03)
  latex1.SetTextAlign(11)
  latex1.DrawLatex(0.6,0.86,'linear fit k x + d')
  latex1.DrawLatex(0.6,0.83,'k = '+str(round(K*1000,2))+' #pm '+str(round(K_E*1000,2))+' #times 10^{-3}')
  latex1.DrawLatex(0.6,0.8,'d = '+str(round(D*1000,2))+' #pm '+str(round(D_E*1000,2))+' #times 10^{-3}')
  
  can.Print(path + '_LT_' + str(deltaPhi).replace('.','p')+'.png')
  can.Print(path + '_LT_' + str(deltaPhi).replace('.','p')+'.root')
  can.Print(path + '_LT_' + str(deltaPhi).replace('.','p')+'.pdf')
  del rcsH, hint1, hint2

rcs = {}
for deltaPhi in deltaPhis:
  rcs[deltaPhi] = {}
  for htb in [(500,-1),(500,750),(500,1000),(750,1000),(750,-1),(1000,-1)]:
    name, cut = nameAndCut((250,-1), htb, (3,-1), btb=(0,0), presel=presel)
    rcs[deltaPhi][htb] = getRCS(QCD['chain'], cut, deltaPhi)
    for ltb in [(250,350), (350,450), (450,-1)]:
      name, cut = nameAndCut(ltb, htb, (3,-1), btb=(0,0), presel=presel)
      rcs[deltaPhi][htb][ltb] = getRCS(QCD['chain'], cut, deltaPhi)
  for ltb in [(250,350), (350,450), (450,-1)]:
    name, cut = nameAndCut(ltb, (500,-1), (3,-1), btb=(0,0), presel=presel)
    rcs[deltaPhi][ltb] = getRCS(QCD['chain'], cut, deltaPhi)

signalRegions = signalRegion3fb

pickleDir = '/data/dspitzbart/Results2016/Prediction_SFtemplates_fullSR_lep_data_2p3/'

pred = pickle.load(file(pickleDir+'resultsFinal_withSystematics_pkl'))

#res = pickle.load(file(pickleDir+'resultsFinal_withSystematics_pkl'))
QCDpickle = '/data/dspitzbart/Results2016/QCDEstimation/20160212_QCDestimation_data2p25fb_pkl'
QCD_est = pickle.load(file(QCDpickle))

QCD_LT = {}
QCD_HT = {}

frac = {}

for srNJet in sorted(signalRegions):
  QCD_LT[srNJet] = {}
  QCD_HT[srNJet] = {}
  frac[srNJet] = {}
  for stb in sorted(signalRegions[srNJet]):
    QCD_LT[srNJet][stb] = {}
    QCD_HT[srNJet][stb] = {}
    frac[srNJet][stb] = {}
    for htb in sorted(signalRegions[srNJet][stb]):
      deltaPhi = signalRegions[srNJet][stb][htb]['deltaPhi']
      print
      print '#################################################'
      print '## Prediction for SR',str(srNJet),str(stb),str(htb)
      print '## Using a dPhi cut value of',str(deltaPhi)
      print '#################################################'
      QCD_y = QCD_est[srNJet][stb][htb][(0,0)][deltaPhi]['NQCDpred']
      QCD_err = QCD_est[srNJet][stb][htb][(0,0)][deltaPhi]['NQCDpred_err']
      if math.isnan(QCD_err):
        QCD_err = QCD_y
      QCD_highDPhi_upper_LTbinned = getPropagatedError([rcs[deltaPhi][stb]['rCS'], QCD_y], [rcs[deltaPhi][stb]['rCSE_sim'], QCD_err], (1+rcs[deltaPhi][stb]['rCS']), rcs[deltaPhi][stb]['rCSE_sim'], returnCalcResult=True)
      QCD_highDPhi_upper_HTbinned = getPropagatedError([rcs[deltaPhi][htb]['rCS'], QCD_y], [rcs[deltaPhi][htb]['rCSE_sim'], QCD_err], (1+rcs[deltaPhi][htb]['rCS']), rcs[deltaPhi][htb]['rCSE_sim'], returnCalcResult=True)
      
      QCD_frac_LTbinned = getPropagatedError(QCD_highDPhi_upper_LTbinned[0],QCD_highDPhi_upper_LTbinned[1],pred[srNJet][stb][htb]['tot_pred_final'], pred[srNJet][stb][htb]['tot_pred_final_err'], returnCalcResult=True)
      QCD_frac_HTbinned = getPropagatedError(QCD_highDPhi_upper_HTbinned[0],QCD_highDPhi_upper_HTbinned[1],pred[srNJet][stb][htb]['tot_pred_final'], pred[srNJet][stb][htb]['tot_pred_final_err'], returnCalcResult=True)
      
      QCD_LT[srNJet][stb][htb] = {'y':QCD_highDPhi_upper_LTbinned, 'frac':QCD_frac_LTbinned, 'Rcs':rcs[deltaPhi][stb]}
      QCD_HT[srNJet][stb][htb] = {'y':QCD_highDPhi_upper_HTbinned, 'frac':QCD_frac_HTbinned, 'Rcs':rcs[deltaPhi][htb]}
      
      print 'Rcs', getValErrString(rcs[deltaPhi][stb]['rCS'], rcs[deltaPhi][stb]['rCSE_sim'], precision=4)
      print 'tot QCD', getValErrString(QCD_y, QCD_err, precision=3)
      print 'QCD pred (antisel Rcs)', getValErrString(QCD_est[srNJet][stb][htb][(0,0)][deltaPhi]['NQCDpred_highdPhi'], QCD_est[srNJet][stb][htb][(0,0)][deltaPhi]['NQCDpred_highdPhi_err'], precision=3)
      print 'QCD in SR (upper bound)', getValErrString(QCD_highDPhi_upper_LTbinned[0], QCD_highDPhi_upper_LTbinned[1], precision=3)
      print 'Fraction wrt to total Bkg', getValErrString(QCD_frac_LTbinned[0],QCD_frac_LTbinned[1])


      #QCD fractions in sideband and CR
      QCD_TT_SB_lowDPhi = QCD_est[(4,5)][stb][htb][(1,1)][deltaPhi]['NQCDpred_lowdPhi']
      QCD_TT_SB_lowDPhi_err = QCD_est[(4,5)][stb][htb][(1,1)][deltaPhi]['NQCDpred_lowdPhi_err']
      if math.isnan(QCD_TT_SB_lowDPhi_err): QCD_TT_SB_lowDPhi_err = QCD_est[(4,5)][stb][htb][(1,1)][deltaPhi]['NQCDpred_err']
      if math.isnan(QCD_TT_SB_lowDPhi_err): QCD_TT_SB_lowDPhi_err = QCD_TT_SB_lowDPhi

      QCD_TT_SB_highDPhi = QCD_est[(4,5)][stb][htb][(1,1)][deltaPhi]['NQCDpred_highdPhi']
      QCD_TT_SB_highDPhi_err = QCD_est[(4,5)][stb][htb][(1,1)][deltaPhi]['NQCDpred_highdPhi_err']
      if math.isnan(QCD_TT_SB_highDPhi_err): QCD_TT_SB_highDPhi_err = QCD_TT_SB_highDPhi

      QCD_CR = QCD_est[srNJet][stb][htb][(0,0)][deltaPhi]['NQCDpred_lowdPhi']
      QCD_CR_err = QCD_est[srNJet][stb][htb][(0,0)][deltaPhi]['NQCDpred_lowdPhi_err']
      if math.isnan(QCD_CR_err): QCD_CR_err = QCD_est[srNJet][stb][htb][(0,0)][deltaPhi]['NQCDpred_err']
      
      y_CR = pred[srNJet][stb][htb]['yTT_srNJet_0b_lowDPhi'] + pred[srNJet][stb][htb]['yW_srNJet_0b_lowDPhi'] + pred[srNJet][stb][htb]['yRest_srNJet_0b_lowDPhi_truth'] + QCD_CR
      y_CR_err = sqrt(pred[srNJet][stb][htb]['yTT_Var_srNJet_0b_lowDPhi'] + pred[srNJet][stb][htb]['yW_Var_srNJet_0b_lowDPhi'] + pred[srNJet][stb][htb]['yRest_Var_srNJet_0b_lowDPhi_truth'] + QCD_CR_err**2)

      y_TT_SB_CR = pred[srNJet][stb][htb]['y_crNJet_1b_lowDPhi']
      y_TT_SB_CR_err = pred[srNJet][stb][htb]['y_Var_crNJet_1b_lowDPhi']
      
      y_TT_SB_SR = pred[srNJet][stb][htb]['y_crNJet_1b_highDPhi']
      y_TT_SB_SR_err = pred[srNJet][stb][htb]['y_Var_crNJet_1b_highDPhi']

      QCD_frac_CR = getPropagatedError(QCD_CR, QCD_CR_err, y_CR, y_CR_err, returnCalcResult=True)
      QCD_frac_TT_SB_CR = getPropagatedError(QCD_TT_SB_lowDPhi, QCD_TT_SB_lowDPhi_err, y_TT_SB_CR, y_TT_SB_CR_err, returnCalcResult=True)
      QCD_frac_TT_SB_SR = getPropagatedError(QCD_TT_SB_highDPhi, QCD_TT_SB_highDPhi_err, y_TT_SB_SR, y_TT_SB_SR_err, returnCalcResult=True)

      print 'fraction of QCD in CR', getValErrString(QCD_frac_CR[0], QCD_frac_CR[1])
      print 'fraction of QCD in low DPhi of tt SB', getValErrString(QCD_frac_TT_SB_CR[0], QCD_frac_TT_SB_CR[1])
      print 'fraction of QCD in high DPhi of tt SB', getValErrString(QCD_frac_TT_SB_SR[0], QCD_frac_TT_SB_SR[1])
      
      frac[srNJet][stb][htb] = {'CR':QCD_frac_CR[0], 'CR_err':QCD_frac_CR[1], 'TT_SB_CR':QCD_frac_TT_SB_CR[0], 'TT_SB_CR_err':QCD_frac_TT_SB_CR[1], 'TT_SB_SR':QCD_frac_TT_SB_SR[0], 'TT_SB_SR_err':QCD_frac_TT_SB_SR[1]}

rowsNJet = {}
rowsSt = {}
for srNJet in sorted(signalRegions):
  rowsNJet[srNJet] = {}
  rowsSt[srNJet] = {}
  rows = 0
  for stb in sorted(signalRegions[srNJet]):
    rows += len(signalRegions[srNJet][stb])
    rowsSt[srNJet][stb] = {'n':len(signalRegions[srNJet][stb])}
  rowsNJet[srNJet] = {'nST':len(signalRegions[srNJet]), 'n':rows}


print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|}\\hline'
print ' \\njet     & \LT & \HT     & \multicolumn{3}{c|}{EWK} & \multicolumn{9}{c|}{QCD}\\\%\hline'
print ' & $[$GeV$]$ & $[$GeV$]$ & \multicolumn{3}{c|}{pred} & \multicolumn{3}{c}{yield}&\multicolumn{3}{c}{frac. wrt EWK} & \multicolumn{3}{c|}{$R_{CS}$} \\\\\hline'

secondLine = False
for srNJet in sorted(signalRegions):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(pred[srNJet][stb][htb]['tot_pred_final'], pred[srNJet][stb][htb]['tot_pred_final_err'])\
           +' & '+getNumString(QCD_LT[srNJet][stb][htb]['y'][0], QCD_LT[srNJet][stb][htb]['y'][1], 3)\
           +' & '+getNumString(QCD_LT[srNJet][stb][htb]['frac'][0], QCD_LT[srNJet][stb][htb]['frac'][1])\
           +' & '+getNumString(QCD_LT[srNJet][stb][htb]['Rcs']['rCS'], QCD_LT[srNJet][stb][htb]['Rcs']['rCSE_sim'],4) +'\\\\'
      if htb[1] == -1 : print '\\cline{2-15}'
print '\\hline\end{tabular}}\end{center}\caption{Estimated QCD contamination in the SRs for $R_{CS}$(QCD) measured in $L_T$ bins, 2.25fb$^{-1}$}\label{tab:0b_QCD_SR_upper_LT}\end{table}'

print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|}\\hline'
print ' \\njet     & \LT & \HT     & \multicolumn{3}{c|}{EWK} & \multicolumn{9}{c|}{QCD}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c|}{pred} & \multicolumn{3}{c}{yield}&\multicolumn{3}{c}{frac. wrt EWK} & \multicolumn{3}{c|}{$R_{CS}$} \\\\\hline'

secondLine = False
for srNJet in sorted(signalRegions):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(pred[srNJet][stb][htb]['tot_pred_final'], pred[srNJet][stb][htb]['tot_pred_final_err'])\
           +' & '+getNumString(QCD_HT[srNJet][stb][htb]['y'][0],        QCD_HT[srNJet][stb][htb]['y'][1], 3)\
           +' & '+getNumString(QCD_HT[srNJet][stb][htb]['frac'][0],     QCD_HT[srNJet][stb][htb]['frac'][1])\
           +' & '+getNumString(QCD_HT[srNJet][stb][htb]['Rcs']['rCS'],  QCD_HT[srNJet][stb][htb]['Rcs']['rCSE_sim'],4) +'\\\\'
      if htb[1] == -1 : print '\\cline{2-15}'
print '\\hline\end{tabular}}\end{center}\caption{Estimated QCD contamination in the SRs for $R_{CS}$(QCD) measured in $H_T$ bins, 2.25fb$^{-1}$}\label{tab:0b_QCD_SR_upper_HT}\end{table}'



#fraction of QCD in CR and SB
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|}\\hline'
print ' \\njet     & \LT & \HT     & \multicolumn{6}{c|}{4-5jets, 1b} & \multicolumn{3}{c|}{CR 0b}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c}{\DF$<$x} & \multicolumn{3}{c|}{\DF$>$x}&\multicolumn{3}{c|}{\DF$<$x} \\\\\hline'

secondLine = False
for srNJet in sorted(signalRegions):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(frac[srNJet][stb][htb]['TT_SB_CR'], frac[srNJet][stb][htb]['TT_SB_CR_err'])\
           +' & '+getNumString(frac[srNJet][stb][htb]['TT_SB_SR'], frac[srNJet][stb][htb]['TT_SB_SR_err'])\
           +' & '+getNumString(frac[srNJet][stb][htb]['CR'], frac[srNJet][stb][htb]['CR_err']) +'\\\\'
      if htb[1] == -1 : print '\\cline{2-12}'
print '\\hline\end{tabular}}\end{center}\caption{Estimated QCD contamination in the sideband and control regions, 2.25fb$^{-1}$}\label{tab:0b_QCD_fractions}\end{table}'


