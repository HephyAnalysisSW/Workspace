import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from rCShelpers import *
import math
from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *

from binnedNBTagsFit import *

from predictionConfig import *
#signalRegions = signalRegion3fb

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

weight_str, weight_err_str = makeWeight(lumi, sampleLumi, reWeight=MCweight)

prefix = 'singleLeptonic_Spring15_'

pmc1 = '/data/'+username+'/Results2016/Prediction_SFtemplates_validation_lep_MC_SF_2p3/'
pdata1 = '/data/'+username+'/Results2016/Prediction_SFtemplates_validation_lep_data_2p3/'

data1 = pickle.load(file(pdata1+prefix+'_estimationResults_pkl'))
mc1 = pickle.load(file(pmc1+prefix+'_estimationResults_pkl'))

CRkey = 'fit_srNJet_lowDPhi'
SBkey = 'fit_crNJet_lowDPhi'
keys = [['SB',SBkey],['CR',CRkey]]
keys = [['SB1bTT',SBkey]]#,['CR',CRkey]]

#keys = [['SB',SBkey]]
#keys = [['CR',CRkey]]
bins=39
binning = [39,0,39]

[['3-4j 0b SB, mu, pos PD', 'fit_crNJet_lowDPhi', '&&leptonPdg>0&&abs(leptonPdg)==13']]

performBTagFits = True
if performBTagFits:
  resData = {}
  resMC = {}

pdgs = [{'name':'PosPdg', 'cut':'leptonPdg>0'},{'name':'NegPdg', 'cut':'leptonPdg<0'}]
#pdgs = [{'name':'NegPdg', 'cut':'leptonPdg<0'}]


for keyName, fitkey in keys:
  for pdg in pdgs:
    w_H_pos     = ROOT.TH1F('w_H_pos','W+jets',*binning)
    tt_H_pos    = ROOT.TH1F('tt_H_pos','t#bar{t}+jets',*binning)
    rest_H_pos  = ROOT.TH1F('rest_H_pos','Rest',*binning)
    
    w_H_pos.SetFillColor(color('WJETS'))
    tt_H_pos.SetFillColor(color('TTJETS')-2)
    rest_H_pos.SetFillColor(color('TTVH'))

    i = 0
    predX_W_Pos_Err = []
    predY_W_Pos_Err = []
    predX_W_Pos = []
    predY_W_Pos = []
    
    predX_TT_Pos_Err = []
    predY_TT_Pos_Err = []
    predX_TT_Pos = []
    predY_TT_Pos_2 = []
    predY_TT_Pos = []
    
    predX_Rest_Pos_Err = []
    predY_Rest_Pos_Err = []
    predX_Rest_Pos = []
    predY_Rest_Pos = []
    for srNJet in sorted(signalRegions):
      if performBTagFits:
        resData[srNJet] = {}
        resMC[srNJet] = {}
      for stb in sorted(signalRegions[srNJet]):
        if performBTagFits:
          resData[srNJet][stb] = {}
          resMC[srNJet][stb] = {}
        for htb in sorted(signalRegions[srNJet][stb]):
          if keyName == 'SB': njb=(3,4)
          if keyName == 'SB1bTT': njb=(4,5)
          else: njb=srNJet
          name, cut = nameAndCut(stb,htb,njb, (0,0), presel)
          name_ib, cut_ib = nameAndCut(stb,htb,njb, (0,-1), presel)
          dPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
          if performBTagFits:
            resData[srNJet][stb][htb] = {}
            resMC[srNJet][stb][htb] = {}

          print
          print '#############################################'
          print 'bin: \t njet \t\t LT \t\t HT'
          if len(str(srNJet))<7:
            print '\t',srNJet,'\t\t',stb,'\t',htb
          else:
            print '\t',srNJet,'\t',stb,'\t',htb
          print '#############################################'
          print
          
          
          if performBTagFits:
            useBTagWeights = True #True for weighted fake data, false for data
            btagWeightSuffix = '_SF'
            isData = False
            fit_MC = binnedNBTagsFit(cut_ib+"&&"+dPhiStr+"<"+str(dPhiCut), name_ib+'_dPhi'+str(dPhiCut), samples={'W':cWJets, 'TT':cTTJets, 'Rest':cRest, 'Bkg':cBkg, 'Data': cBkg}, prefix = name_ib)
            useBTagWeights = False #True for weighted fake data, false for data
            btagWeightSuffix = '_SF'
            QCD0b_lowDPhi  = {'y':QCDestimate[(4,5)][stb][htb][(0,0)][dPhiCut]['NQCDpred_lowdPhi'],  'e':QCDestimate[(4,5)][stb][htb][(0,0)][dPhiCut]['NQCDpred_lowdPhi_err']}

            QCD1b_lowDPhi  = {'y':QCDestimate[(4,5)][stb][htb][(1,1)][dPhiCut]['NQCDpred_lowdPhi'],  'e':QCDestimate[(4,5)][stb][htb][(1,1)][dPhiCut]['NQCDpred_lowdPhi_err']}
            QCD1b_highDPhi = {'y':QCDestimate[(4,5)][stb][htb][(1,1)][dPhiCut]['NQCDpred_highdPhi'], 'e':QCDestimate[(4,5)][stb][htb][(1,1)][dPhiCut]['NQCDpred_highdPhi_err']}

            QCD2b_lowDPhi  = {'y':QCDestimate[(4,5)][stb][htb][(2,-1)][dPhiCut]['NQCDpred_lowdPhi'],  'e':QCDestimate[(4,5)][stb][htb][(2,-1)][dPhiCut]['NQCDpred_lowdPhi_err']}
            QCD2b_highDPhi = {'y':QCDestimate[(4,5)][stb][htb][(2,-1)][dPhiCut]['NQCDpred_highdPhi'], 'e':QCDestimate[(4,5)][stb][htb][(2,-1)][dPhiCut]['NQCDpred_highdPhi_err']}
            isData = True
            fit_data = binnedNBTagsFit(cut_ib+"&&"+dPhiStr+"<"+str(dPhiCut), name_ib+'_dPhi'+str(dPhiCut), samples={'W':cWJets, 'TT':cTTJets, 'Rest':cRest, 'Bkg':cBkg, 'Data': cData}, prefix = name_ib, QCD_dict={0:QCD0b_lowDPhi, 1:QCD1b_lowDPhi,2:QCD2b_lowDPhi})
            resData[srNJet][stb][htb][fitkey] = fit_data
            resMC[srNJet][stb][htb][fitkey] = fit_MC
          else:
            fit_MC = mc1[srNJet][stb][htb][fitkey]
            #truth = mc1[srNJet][stb][htb]
            fit_data = data1[srNJet][stb][htb][fitkey] #change this
          myFits = [fit_data, fit_MC]
          j = 1
          fitbin = 2 #1 for 0b, 2 for 1b etc
          for f in myFits:
            fit = f
            ttkey = 'TT_AllPdg'
            wkey = 'W_'+pdg['name']
            restkey = 'Rest_'+pdg['name']
            
            print ttkey, wkey, restkey
            
            #get yields in 1b from fit in low dphi (otherwise looking into 0b search bin), QCD is already taken care of in fit
            y_Pos =fit[ttkey]['template'].GetBinContent(fitbin)*fit[ttkey]['yield']*0.5+fit[wkey]['template'].GetBinContent(fitbin)*fit[wkey]['yield']+fit[restkey]['template'].GetBinContent(fitbin)*fit[restkey]['yield']
            y_Pos_Err = sqrt((fit[ttkey]['template'].GetBinError(fitbin)*fit[ttkey]['yield']*0.5)**2 + (fit[wkey]['template'].GetBinError(fitbin)*fit[wkey]['yield'])**2 + (fit[restkey]['template'].GetBinError(fitbin)*fit[restkey]['yield'])**2)
            
            #obtain the fit fractions in data
            fitFracTT_Pos = getPropagatedError([fit[ttkey]['template'].GetBinContent(fitbin),fit[ttkey]['yield']*0.5], [fit[ttkey]['template'].GetBinError(fitbin),sqrt(fit[ttkey]['yieldVar'])],y_Pos, sqrt(y_Pos), returnCalcResult=True)
            fitFracW_Pos = getPropagatedError([fit[wkey]['template'].GetBinContent(fitbin),fit[wkey]['yield']], [fit[wkey]['template'].GetBinError(fitbin),sqrt(fit[wkey]['yieldVar'])],y_Pos, sqrt(y_Pos), returnCalcResult=True)
            fitFracRest_Pos = getPropagatedError([fit[restkey]['template'].GetBinContent(fitbin),fit[restkey]['yield']], [fit[restkey]['template'].GetBinError(fitbin),sqrt(fit[restkey]['yieldVar'])],y_Pos, sqrt(y_Pos), returnCalcResult=True)
            
            w_H_pos.SetBinContent(i*3+j,    fitFracW_Pos[0])
            w_H_pos.SetBinError(i*3+j,      fitFracW_Pos[1])
            tt_H_pos.SetBinContent(i*3+j,   fitFracTT_Pos[0])
            tt_H_pos.SetBinError(i*3+j,     fitFracTT_Pos[1])
            rest_H_pos.SetBinContent(i*3+j, fitFracRest_Pos[0])
            rest_H_pos.SetBinError(i*3+j,   fitFracRest_Pos[1])

            w_fit = getPropagatedError([fit[wkey]['yield']*fit[wkey]['template'].GetBinContent(fitbin)], [fit[wkey]['yield']*fit[wkey]['template'].GetBinError(fitbin)],y_Pos, y_Pos_Err, returnCalcResult=True)
            print w_fit[0], w_fit[1], y_Pos, y_Pos_Err, w_fit[1]/y_Pos
            predY_W_Pos_Err.append(w_fit[1])
            predX_W_Pos_Err.append(0.5)
            predY_W_Pos.append(w_fit[0])
            predX_W_Pos.append(i*3+j-0.5)

            tt_fit = getPropagatedError([fit[ttkey]['yield']*0.5*fit[ttkey]['template'].GetBinContent(fitbin)], [fit[ttkey]['yield']*0.5*fit[ttkey]['template'].GetBinError(fitbin)],y_Pos, y_Pos_Err, returnCalcResult=True)
            print tt_fit[0], tt_fit[1], y_Pos, tt_fit[1]/y_Pos
            predY_TT_Pos_Err.append(tt_fit[1])
            predX_TT_Pos_Err.append(0.5)
            predY_TT_Pos.append((w_fit[0]+tt_fit[0]))
            predY_TT_Pos_2.append(tt_fit[0])
            predX_TT_Pos.append(i*3+j-0.5)

            rest_fit = getPropagatedError([fit[restkey]['yield']*fit[restkey]['template'].GetBinContent(fitbin)], [fit[restkey]['yield']*fit[restkey]['template'].GetBinError(fitbin)],y_Pos, y_Pos_Err, returnCalcResult=True)
            print rest_fit[0], rest_fit[1], y_Pos, rest_fit[1]/y_Pos
            predY_Rest_Pos_Err.append(rest_fit[1])
            predX_Rest_Pos_Err.append(0.5)
            predY_Rest_Pos.append(1)
            predX_Rest_Pos.append(i*3+j-0.5)

            j += 1

          Cut = '&&deltaPhi_Wl<'+str(dPhiCut)+'&&'+pdg['cut']

          #calc truth and fill an 3rd pos
          y_TT_Pos = getYieldFromChain(cTTJets, cut_ib+Cut, weight=weight_str+'*weightBTag1_SF',returnError=True)

          y_W_Pos = getYieldFromChain(cWJets, cut_ib+Cut, weight=weight_str+'*weightBTag1_SF',returnError=True)

          y_Rest_Pos = getYieldFromChain(cRest, cut_ib+Cut, weight=weight_str+'*weightBTag1_SF',returnError=True)

          y_Pos = (y_TT_Pos[0]+y_W_Pos[0]+y_Rest_Pos[0], sqrt(y_TT_Pos[1]**2+y_W_Pos[1]**2+y_Rest_Pos[1]**2))
          
          
          truthFracTT_Pos   = getPropagatedError(y_TT_Pos[0], y_TT_Pos[1], y_Pos[0], y_Pos[1], returnCalcResult=True)
          truthFracW_Pos    = getPropagatedError(y_W_Pos[0], y_W_Pos[1], y_Pos[0], y_Pos[1], returnCalcResult=True)
          truthFracRest_Pos = getPropagatedError(y_Rest_Pos[0], y_Rest_Pos[1], y_Pos[0], y_Pos[1], returnCalcResult=True)

          j=3
          w_H_pos.SetBinContent(i*3+j,    truthFracW_Pos[0])
          w_H_pos.SetBinError(i*3+j,      truthFracW_Pos[1])
          tt_H_pos.SetBinContent(i*3+j,   truthFracTT_Pos[0])
          tt_H_pos.SetBinError(i*3+j,     truthFracTT_Pos[1])
          rest_H_pos.SetBinContent(i*3+j, truthFracRest_Pos[0])
          rest_H_pos.SetBinError(i*3+j,   truthFracRest_Pos[1])


          predY_W_Pos_Err.append(truthFracW_Pos[1])
          predX_W_Pos_Err.append(0.5)
          predY_W_Pos.append(truthFracW_Pos[0])
          predX_W_Pos.append(i*3+j-0.5)
          
          predY_TT_Pos_Err.append(truthFracTT_Pos[1])
          predX_TT_Pos_Err.append(0.5)
          predY_TT_Pos.append(truthFracTT_Pos[0]+truthFracW_Pos[0])
          predX_TT_Pos.append(i*3+j-0.5)

          predY_TT_Pos_2.append(truthFracTT_Pos[0])

          predY_Rest_Pos_Err.append(truthFracRest_Pos[1])
          predX_Rest_Pos_Err.append(0.5)
          predY_Rest_Pos.append(1)
          predX_Rest_Pos.append(i*3+j-0.5)
          
          i += 1

    can = ROOT.TCanvas('can','can',700,700)
    h_Stack = ROOT.THStack('h_Stack','Stack')
    for h in [w_H_pos, tt_H_pos, rest_H_pos]:
      h_Stack.Add(h)
    h_Stack.Draw('hist')
    
    ax_W_Pos  = array('d',predX_W_Pos)
    ay_W_Pos  = array('d',predY_W_Pos)
    axh_W_Pos = array('d',predX_W_Pos_Err)
    axl_W_Pos = array('d',predX_W_Pos_Err)
    ayh_W_Pos = array('d',predY_W_Pos_Err)
    ayl_W_Pos = array('d',predY_W_Pos_Err)
    
    ax_Rest_Pos  = array('d',predX_Rest_Pos)
    ay_Rest_Pos  = array('d',predY_Rest_Pos)
    axh_Rest_Pos = array('d',predX_Rest_Pos_Err)
    axl_Rest_Pos = array('d',predX_Rest_Pos_Err)
    ayh_Rest_Pos = array('d',predY_Rest_Pos_Err)
    ayl_Rest_Pos = array('d',predY_Rest_Pos_Err)
    
    ax_TT_Pos  = array('d',predX_TT_Pos)
    ay_TT_Pos_2  = array('d',predY_TT_Pos_2)
    ay_TT_Pos  = array('d',predY_TT_Pos)
    axh_TT_Pos = array('d',predX_TT_Pos_Err)
    axl_TT_Pos = array('d',predX_TT_Pos_Err)
    ayh_TT_Pos = array('d',predY_TT_Pos_Err)
    ayl_TT_Pos = array('d',predY_TT_Pos_Err)
    
    pred_err_W_Pos = ROOT.TGraphAsymmErrors(bins, ax_W_Pos, ay_W_Pos, axl_W_Pos, axh_W_Pos, ayl_W_Pos, ayh_W_Pos)
    pred_err_W_Pos.SetFillColor(ROOT.kBlack)
    pred_err_W_Pos.SetFillStyle(3244)
    pred_err_W_Pos.Draw('2 same')
    
    pred_err_TT_Pos = ROOT.TGraphAsymmErrors(bins, ax_TT_Pos, ay_TT_Pos, axl_TT_Pos, axh_TT_Pos, ayl_TT_Pos, ayh_TT_Pos)
    pred_err_TT_Pos.SetFillColor(ROOT.kBlack)
    pred_err_TT_Pos.SetFillStyle(3244)
    pred_err_TT_Pos.Draw('2 same')
    
    pred_err_TT_Pos_2 = ROOT.TGraphAsymmErrors(bins, ax_TT_Pos, ay_TT_Pos_2, axl_TT_Pos, axh_TT_Pos, ayl_TT_Pos, ayh_TT_Pos)
    pred_err_TT_Pos_2.SetFillColor(ROOT.kBlack)
    pred_err_TT_Pos_2.SetFillStyle(3244)
    
    pred_err_Rest_Pos = ROOT.TGraphAsymmErrors(bins, ax_Rest_Pos, ay_Rest_Pos, axl_Rest_Pos, axh_Rest_Pos, ayl_Rest_Pos, ayh_Rest_Pos)
    pred_err_Rest_Pos.SetFillColor(ROOT.kBlack)
    pred_err_Rest_Pos.SetFillStyle(3244)
    pred_err_Rest_Pos.Draw('2 same')
    
    labels = []
    for srNJet in sorted(signalRegions):
      for stb in sorted(signalRegions[srNJet]):
        for htb in sorted(signalRegions[srNJet][stb]):
          labels.append({1:signalRegions[srNJet][stb][htb]['njet'],2:signalRegions[srNJet][stb][htb]['LT'],3:signalRegions[srNJet][stb][htb]['HT']})
    
    j=0
    for i in range(1,42):
      if (i%3)==0:
        
        h_Stack.GetXaxis().SetBinLabel(i-1,'#splitline{'+labels[j][1]+'}{#splitline{'+labels[j][2]+'}{'+labels[j][3]+'}}')
        j += 1
    
    h_Stack.GetXaxis().LabelsOption('h')
    h_Stack.GetXaxis().SetLabelSize(0.04)
    h_Stack.GetYaxis().SetTitle('fractions after fit')
    h_Stack.GetYaxis().SetTitleSize(0.04)
    h_Stack.GetYaxis().SetLabelSize(0.04)
    
    h_Stack.SetMaximum(1.2)
    h_Stack.SetMinimum(0)
    
    binH = ROOT.TH1F('binH','binH',*binning)
    constH = ROOT.TH1F('constH','constH',*binning)
    constH2 = ROOT.TH1F('constH2','constH2',*binning)
    
    binH.SetLineWidth(2)
    binH.SetLineStyle(2)
    constH.SetLineWidth(2)
    constH2.SetLineWidth(2)
    
    v = 1
    switch = True
    for i in range(39):
      if (i%3)==0:
        if switch: switch=False
        else: switch=True 
      if switch: v = 1
      else: v = 0
      #print i, v
      binH.SetBinContent(i+1, v)
      constH.SetBinContent(i+1,1)
      constH2.SetBinContent(i+1,0)
    
    binH.Draw('hist same')
    constH.Draw('hist same')
    constH2.Draw('hist same')
    
    leg = ROOT.TLegend(0.75,0.83,0.98,0.95)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetShadowColor(ROOT.kWhite)
    leg.SetBorderSize(1)
    leg.SetTextSize(0.035)
    leg.AddEntry(w_H_pos,'','f')
    leg.AddEntry(tt_H_pos,'','f')
    leg.AddEntry(rest_H_pos,'','f')
    
    leg.Draw()
    
    latex1 = ROOT.TLatex()
    latex1.SetNDC()
    latex1.SetTextSize(0.04)
    latex1.SetTextAlign(11)
    latex1.DrawLatex(0.17,0.96,'CMS #bf{#it{preliminary}}')
    latex1.DrawLatex(0.7,0.96,"L="+printlumi+"fb^{-1} (13TeV)")
    
    latex2 = ROOT.TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.03)
    latex2.SetTextAlign(11)
    latex2.DrawLatex(0.22,0.87,"#bf{data fit/MC fit/MC truth}")
    latex2.DrawLatex(0.22,0.84,"#bf{"+keyName+" 0b, "+pdg['name']+"}")
    
    can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016/fitFractions/'+keyName+'_0b_'+pdg['name']+'_2p25fb.png')
    can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016/fitFractions/'+keyName+'_0b_'+pdg['name']+'_2p25fb.pdf')
    can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016/fitFractions/'+keyName+'_0b_'+pdg['name']+'_2p25fb.root')
    del can, h_Stack

    j=0
    for i in range(1,42):
      if (i%3)==0:

        w_H_pos.GetXaxis().SetBinLabel(i-1,'#splitline{'+labels[j][1]+'}{#splitline{'+labels[j][2]+'}{'+labels[j][3]+'}}')
        tt_H_pos.GetXaxis().SetBinLabel(i-1,'#splitline{'+labels[j][1]+'}{#splitline{'+labels[j][2]+'}{'+labels[j][3]+'}}')
        j += 1
    
    can2 = ROOT.TCanvas('can2','can2',700,700)
    w_H_pos.GetXaxis().LabelsOption('h')
    w_H_pos.GetXaxis().SetLabelSize(0.04)
    w_H_pos.GetYaxis().SetTitle('fractions after fit')
    w_H_pos.GetYaxis().SetTitleSize(0.04)
    w_H_pos.GetYaxis().SetLabelSize(0.04)
    w_H_pos.SetMaximum(1.2)
    w_H_pos.SetMinimum(0)
    w_H_pos.Draw('hist')

    pred_err_W_Pos.Draw('2 same')
    binH.Draw('hist same')
    constH.Draw('hist same')
    constH2.Draw('hist same')
    
    latex1.DrawLatex(0.17,0.96,'CMS #bf{#it{preliminary}}')
    latex1.DrawLatex(0.7,0.96,"L="+printlumi+"fb^{-1} (13TeV)")
    latex2.DrawLatex(0.22,0.87,"#bf{data fit/MC fit/MC truth}")
    latex2.DrawLatex(0.22,0.84,"#bf{"+keyName+" 0b, "+pdg['name']+"}")
    latex2.DrawLatex(0.7,0.87,"#bf{W+jets}")
    
    can2.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016/fitFractions/'+keyName+'_0b_W_'+pdg['name']+'_2p25fb.png')
    can2.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016/fitFractions/'+keyName+'_0b_W_'+pdg['name']+'_2p25fb.pdf')
    can2.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016/fitFractions/'+keyName+'_0b_W_'+pdg['name']+'_2p25fb.root')
    
    can3 = ROOT.TCanvas('can3','can3',700,700)
    tt_H_pos.GetXaxis().LabelsOption('h')
    tt_H_pos.GetXaxis().SetLabelSize(0.04)
    tt_H_pos.GetYaxis().SetTitle('fractions after fit')
    tt_H_pos.GetYaxis().SetTitleSize(0.04)
    tt_H_pos.GetYaxis().SetLabelSize(0.04)
    tt_H_pos.SetMaximum(1.2)
    tt_H_pos.SetMinimum(0)
    tt_H_pos.Draw('hist')

    pred_err_TT_Pos_2.Draw('2 same')
    binH.Draw('hist same')
    constH.Draw('hist same')
    constH2.Draw('hist same')

    latex1.DrawLatex(0.17,0.96,'CMS #bf{#it{preliminary}}')
    latex1.DrawLatex(0.7,0.96,"L="+printlumi+"fb^{-1} (13TeV)")
    latex2.DrawLatex(0.22,0.87,"#bf{data fit/MC fit/MC truth}")
    latex2.DrawLatex(0.22,0.84,"#bf{"+keyName+" 0b, "+pdg['name']+"}")
    latex2.DrawLatex(0.7,0.87,"#bf{t#bar{t}+jets}")
    
    can3.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016/fitFractions/'+keyName+'_0b_tt_'+pdg['name']+'_2p25fb.png')
    can3.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016/fitFractions/'+keyName+'_0b_tt_'+pdg['name']+'_2p25fb.pdf')
    can3.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016/fitFractions/'+keyName+'_0b_tt_'+pdg['name']+'_2p25fb.root')


    del can2, can3, tt_H_pos, w_H_pos, rest_H_pos
