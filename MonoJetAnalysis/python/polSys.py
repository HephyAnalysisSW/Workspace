import ROOT
from Workspace.MonoJetAnalysis.helpers import getVarValue
ROOT.gROOT.ProcessLine('.L ../../HEPHYPythonTools/scripts/root/WPolarizationVariation.C+')
def calcPolWeights(c):
  #find gen W
  ngp = int(getVarValue(c, 'ngp'))
  for gpLep in range(ngp):
    pdgLep = getVarValue(c, 'gpPdg', gpLep)
    staLep = getVarValue(c, 'gpSta', gpLep)
    if staLep==3 and (abs(pdgLep)==11 or abs(pdgLep)==13 or abs(pdgLep)==15):
      gpW = int(getVarValue(c, 'gpMo1', gpLep))
      if abs(getVarValue(c, 'gpPdg', int(gpW)))==24: 
#        print 'pdg',pdgLep,'sta',getVarValue(c, 'gpSta', gpLep),"gpW",gpW,getVarValue(c, 'gpPdg', int(gpW))
        plus = pdgLep<0
        WPt =getVarValue(c, "gpPt",   gpW)
        WEta =getVarValue(c, "gpEta", gpW)
        WPhi =getVarValue(c, "gpPhi", gpW)
        genp4_W_ = ROOT.TLorentzVector()
        genp4_W_.SetPtEtaPhiM(WPt, WEta, WPhi, 80.4)
        LepPt =getVarValue(c, "gpPt", gpLep)
        LepEta =getVarValue(c, "gpEta", gpLep)
        LepPhi =getVarValue(c, "gpPhi", gpLep)
        genp4_l_ = ROOT.TLorentzVector()
        genp4_l_.SetPtEtaPhiM(LepPt, LepEta, LepPhi, 0.)
#        genp4_W_.Print()
#        genp4_l_.Print()
        WPol1Plus10_weight_flfr = 1
        WPol1Minus10_weight_flfr = 1
        WPol2PlusPlus5_weight_flfr = 1
        WPol2PlusMinus5_weight_flfr = 1
        WPol2MinusPlus5_weight_flfr = 1
        WPol2MinusMinus5_weight_flfr = 1
        WPol3Plus10_weight_flfr = 1
        WPol3Minus10_weight_flfr = 1
        if plus:
          WPol1Plus10_weight_flfr        = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_W_,genp4_l_,10,1);
          WPol1Minus10_weight_flfr       = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_W_,genp4_l_,-10,1);
          WPol2PlusPlus5_weight_flfr        = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_W_,genp4_l_,5,1);
          WPol2PlusMinus5_weight_flfr        = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_W_,genp4_l_,-5,1);
          WPol3Plus10_weight_f0        = ROOT.GetWeightWjetsPolarizationF0(genp4_W_,genp4_l_,+10,1);
          WPol3Minus10_weight_f0        = ROOT.GetWeightWjetsPolarizationF0(genp4_W_,genp4_l_,-10,1);
        else:
          WPol1Plus10_weight_flfr        = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_W_,genp4_l_,10,0);
          WPol1Minus10_weight_flfr       = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_W_,genp4_l_,-10,0);
          WPol2MinusPlus5_weight_flfr        = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_W_,genp4_l_,5,0);
          WPol2MinusMinus5_weight_flfr        = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_W_,genp4_l_,-5,0);
          WPol3Plus10_weight_f0        = ROOT.GetWeightWjetsPolarizationF0(genp4_W_,genp4_l_,+10,0);
          WPol3Minus10_weight_f0        = ROOT.GetWeightWjetsPolarizationF0(genp4_W_,genp4_l_,-10,0);
        res = {\
          "WPol1Plus10_weight_flfr":WPol1Plus10_weight_flfr,
          "WPol1Minus10_weight_flfr":WPol1Minus10_weight_flfr,
          "WPol2PlusPlus5_weight_flfr":WPol2PlusPlus5_weight_flfr,
          "WPol2PlusMinus5_weight_flfr":WPol2PlusMinus5_weight_flfr,
          "WPol2MinusPlus5_weight_flfr":WPol2MinusPlus5_weight_flfr,
          "WPol2MinusMinus5_weight_flfr":WPol2MinusMinus5_weight_flfr,
          "WPol3Plus10_weight_f0":WPol3Plus10_weight_f0,
          "WPol3Minus10_weight_f0":WPol3Minus10_weight_f0
        }

        return res 

#c = ROOT.TChain('Events')
#c.Add('/data/schoef/monoJetTuples_v5/copy/WJetsHT150v2/histo_WJetsHT150v2.root')
#c.GetEntry(1)
#print calcPolWeights(c)

#
