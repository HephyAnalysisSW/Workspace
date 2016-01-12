from btagEfficiency import *
from math import *

def calc_btag_systematics(t,s,r,mcEffDict,sampleKey,maxConsideredBTagWeight,separateBTagWeights):
  #separateBTagWeights = False
  zeroTagWeight = 1.
  mceff = getMCEfficiencyForBTagSF(t, mcEffDict[sampleKey], sms='')
  #print
  #print mceff["mceffs"]
  mceffW                = getTagWeightDict(mceff["mceffs"], maxConsideredBTagWeight)
  mceffW_SF             = getTagWeightDict(mceff["mceffs_SF"], maxConsideredBTagWeight)
  mceffW_SF_b_Up        = getTagWeightDict(mceff["mceffs_SF_b_Up"], maxConsideredBTagWeight)
  mceffW_SF_b_Down      = getTagWeightDict(mceff["mceffs_SF_b_Down"], maxConsideredBTagWeight)
  mceffW_SF_light_Up    = getTagWeightDict(mceff["mceffs_SF_light_Up"], maxConsideredBTagWeight)
  mceffW_SF_light_Down  = getTagWeightDict(mceff["mceffs_SF_light_Down"], maxConsideredBTagWeight)
  if not separateBTagWeights:
    lweight = str(s.weight)
  else: lweight = "(1.)"
  #if not separateBTagWeights:
  for i in range(1, maxConsideredBTagWeight+2):
    exec("s.weightBTag"+str(i)+"p="+lweight)
    exec("s.weightBTag"+str(i)+"p_SF="+lweight)
    exec("s.weightBTag"+str(i)+"p_SF_b_Up="+lweight)
    exec("s.weightBTag"+str(i)+"p_SF_b_Down="+lweight)
    exec("s.weightBTag"+str(i)+"p_SF_light_Up="+lweight)
    exec("s.weightBTag"+str(i)+"p_SF_light_Down="+lweight)
  for i in range(maxConsideredBTagWeight+1):
    exec("s.weightBTag"+str(i)+"="              +str(mceffW[i])+'*'+lweight)
    exec("s.weightBTag"+str(i)+"_SF="           +str(mceffW_SF[i])+'*'+lweight)
    exec("s.weightBTag"+str(i)+"_SF_b_Up="      +str(mceffW_SF_b_Up[i])+'*'+lweight)
    exec("s.weightBTag"+str(i)+"_SF_b_Down="    +str(mceffW_SF_b_Down[i])+'*'+lweight)
    exec("s.weightBTag"+str(i)+"_SF_light_Up="  +str(mceffW_SF_light_Up[i])+'*'+lweight)
    exec("s.weightBTag"+str(i)+"_SF_light_Down="+str(mceffW_SF_light_Down[i])+'*'+lweight)
    for j in range(i+1, maxConsideredBTagWeight+2):
      exec("s.weightBTag"+str(j)+"p               -="+str(mceffW[i])+'*'+lweight) #prob. for >=j b-tagged jets
      exec("s.weightBTag"+str(j)+"p_SF            -="+str(mceffW_SF[i])+'*'+lweight)
      exec("s.weightBTag"+str(j)+"p_SF_b_Up       -="+str(mceffW_SF_b_Up[i])+'*'+lweight)
      exec("s.weightBTag"+str(j)+"p_SF_b_Down     -="+str(mceffW_SF_b_Down[i])+'*'+lweight)
      exec("s.weightBTag"+str(j)+"p_SF_light_Up   -="+str(mceffW_SF_light_Up[i])+'*'+lweight)
      exec("s.weightBTag"+str(j)+"p_SF_light_Down -="+str(mceffW_SF_light_Down[i])+'*'+lweight)
  for i in range (int(r.nJet)+1, maxConsideredBTagWeight+1):
    exec("s.weightBTag"+str(i)+"               = 0.")
    exec("s.weightBTag"+str(i)+"_SF            = 0.")
    exec("s.weightBTag"+str(i)+"_SF_b_Up       = 0.")
    exec("s.weightBTag"+str(i)+"_SF_b_Down     = 0.")
    exec("s.weightBTag"+str(i)+"_SF_light_Up   = 0.")
    exec("s.weightBTag"+str(i)+"_SF_light_Down = 0.")
    exec("s.weightBTag"+str(i)+"p              = 0.")
    exec("s.weightBTag"+str(i)+"p_SF           = 0.")
    exec("s.weightBTag"+str(i)+"p_SF_b_Up      = 0.")
    exec("s.weightBTag"+str(i)+"p_SF_b_Down    = 0.")
    exec("s.weightBTag"+str(i)+"p_SF_light_Up  = 0.")
    exec("s.weightBTag"+str(i)+"p_SF_light_Down= 0.")
  return

def calc_LeptonScale_factors_and_systematics(s,histos_LS):
  mu_mediumID_histo   =histos_LS['mu_mediumID_histo']
  mu_looseID_histo    =histos_LS['mu_looseID_histo']
  mu_miniIso02_histo  =histos_LS['mu_miniIso02_histo']
  mu_sip3d_histo      =histos_LS['mu_sip3d_histo']
  ele_cutbased_histo  =histos_LS['ele_cutbased_histo']
  ele_miniIso01_histo =histos_LS['ele_miniIso01_histo']
  if s.singleMuonic and s.leptonPt<120:
    bin_lepton_muSF_mediumID = mu_mediumID_histo.FindBin(s.leptonPt,abs(s.leptonEta))
    s.lepton_muSF_mediumID =  mu_mediumID_histo.GetBinContent(bin_lepton_muSF_mediumID)
    s.lepton_muSF_looseID =  mu_looseID_histo.GetBinContent(mu_looseID_histo.FindBin(s.leptonPt,abs(s.leptonEta)))
    s.lepton_muSF_miniIso02 =  mu_miniIso02_histo.GetBinContent(mu_miniIso02_histo.FindBin(s.leptonPt,abs(s.leptonEta)))         
    s.lepton_muSF_sip3d =  mu_sip3d_histo.GetBinContent(mu_sip3d_histo.FindBin(s.leptonPt,abs(s.leptonEta)))
    s.lepton_muSF_mediumID_err =  mu_mediumID_histo.GetBinError(mu_mediumID_histo.FindBin(s.leptonPt,abs(s.leptonEta)))
    s.lepton_muSF_looseID_err =  mu_looseID_histo.GetBinError(mu_looseID_histo.FindBin(s.leptonPt,abs(s.leptonEta)))
    s.lepton_muSF_miniIso02_err =  mu_miniIso02_histo.GetBinError(mu_miniIso02_histo.FindBin(s.leptonPt,abs(s.leptonEta)))       
    s.lepton_muSF_sip3d_err =  mu_sip3d_histo.GetBinError(mu_sip3d_histo.FindBin(s.leptonPt,abs(s.leptonEta)))
  if s.singleMuonic and s.leptonPt>=120:
    bin_lepton_muSF_mediumID = mu_mediumID_histo.FindBin(119,abs(s.leptonEta))
    s.lepton_muSF_mediumID =  mu_mediumID_histo.GetBinContent(bin_lepton_muSF_mediumID)
    s.lepton_muSF_looseID =  mu_looseID_histo.GetBinContent(mu_looseID_histo.FindBin(119,abs(s.leptonEta)))
    s.lepton_muSF_miniIso02 =  mu_miniIso02_histo.GetBinContent(mu_miniIso02_histo.FindBin(119,abs(s.leptonEta)))
    s.lepton_muSF_sip3d =  mu_sip3d_histo.GetBinContent(mu_sip3d_histo.FindBin(119,abs(s.leptonEta)))
    s.lepton_muSF_mediumID_err =  mu_mediumID_histo.GetBinError(mu_mediumID_histo.FindBin(119,abs(s.leptonEta)))
    s.lepton_muSF_looseID_err =  mu_looseID_histo.GetBinError(mu_looseID_histo.FindBin(119,abs(s.leptonEta)))
    s.lepton_muSF_miniIso02_err =  mu_miniIso02_histo.GetBinError(mu_miniIso02_histo.FindBin(119,abs(s.leptonEta)))
  if s.singleElectronic:
    s.lepton_eleSF_cutbasedID = ele_cutbased_histo.GetBinContent(ele_cutbased_histo.FindBin(s.leptonEt,abs(s.leptonEta)))      
    s.lepton_eleSF_miniIso01 = ele_miniIso01_histo.GetBinContent(ele_miniIso01_histo.FindBin(s.leptonEt,abs(s.leptonEta)))
    s.lepton_eleSF_cutbasedID_err = ele_cutbased_histo.GetBinError(ele_cutbased_histo.FindBin(s.leptonEt,abs(s.leptonEta)))
    s.lepton_eleSF_miniIso01_err = ele_miniIso01_histo.GetBinError(ele_miniIso01_histo.FindBin(s.leptonEt,abs(s.leptonEta)))
  return


def calc_TopPt_Weights(s,genParts):
  genTops = filter(lambda g:abs(g['pdgId'])==6, genParts)
  s.nGenTops = len(genTops)
  GenAntiTopIdx = -999
  GenTopIdx = -999
  for i_part, genPart in enumerate(genParts):
    if genPart['pdgId'] ==  6:
          s.GenTopPt = genPart['pt']
          GenTopIdx = i_part
    if genPart['pdgId'] == -6:
          s.GenAntiTopPt = genPart['pt']
          GenAntiTopIdx = i_part

  if s.GenTopPt!=-999 and s.GenAntiTopPt!=-999 and s.nGenTops==2:
    #print "genTop" , s.GenTopPt
    SFTop     = exp(0.156    -0.00137*s.GenTopPt    )
    SFAntiTop = exp(0.156    -0.00137*s.GenAntiTopPt)
    #print "SFTOP" , SFTop
    s.TopPtWeight = sqrt(SFTop*SFAntiTop)
    if s.TopPtWeight<0.5: s.TopPtWeight=0.5

    if GenAntiTopIdx!=-999 and GenTopIdx!=-999:
      genTop_vec = ROOT.TLorentzVector()
      genTop_vec.SetPtEtaPhiM(genParts[GenTopIdx]['pt'],genParts[GenTopIdx]['eta'],genParts[GenTopIdx]['phi'],genParts[GenTopIdx]['mass'])
      genAntiTop_vec = ROOT.TLorentzVector()
      genAntiTop_vec.SetPtEtaPhiM(genParts[GenAntiTopIdx]['pt'],genParts[GenAntiTopIdx]['eta'],genParts[GenAntiTopIdx]['phi'],genParts[GenAntiTopIdx]['mass'])
      GenTTBarp4 = genTop_vec + genAntiTop_vec
      s.GenTTBarPt = GenTTBarp4.Pt()
      if s.GenTTBarPt>120: s.GenTTBarWeight= 0.95
      if s.GenTTBarPt>150: s.GenTTBarWeight= 0.90
      if s.GenTTBarPt>250: s.GenTTBarWeight= 0.80
      if s.GenTTBarPt>400: s.GenTTBarWeight= 0.70 
      #print s.GenTTBarPt , s.GenTTBarWeight
  return
