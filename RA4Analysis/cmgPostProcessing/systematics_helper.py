from Workspace.RA4Analysis.cmgObjectSelection import cmgLooseLepIndices, splitIndList, get_cmg_jets_fromStruct, splitListOfObjects, cmgTightMuID, cmgTightEleID , get_cmg_genParts_fromStruct , get_cmg_JetsforMEt_fromStruct
from Workspace.HEPHYPythonTools.helpers import *
from btagEfficiency import *
from math import *

def calc_btag_systematics(t,s,r,mcEffDict,sampleKey,maxConsideredBTagWeight,separateBTagWeights, model='', weightName="weightBTag"):
  #separateBTagWeights = False
  zeroTagWeight = 1.
  #print "yes2"
  #print mcEffDict
  mceff = getMCEfficiencyForBTagSF(t, mcEffDict[sampleKey], sms=model)
  #print
  #print mceff["mceffs"]
  mceffW                = getTagWeightDict(mceff["mceffs"], maxConsideredBTagWeight)
  mceffW_SF             = getTagWeightDict(mceff["mceffs_SF"], maxConsideredBTagWeight)
  mceffW_SF_b_Up        = getTagWeightDict(mceff["mceffs_SF_b_Up"], maxConsideredBTagWeight)
  mceffW_SF_b_Down      = getTagWeightDict(mceff["mceffs_SF_b_Down"], maxConsideredBTagWeight)
  mceffW_SF_light_Up    = getTagWeightDict(mceff["mceffs_SF_light_Up"], maxConsideredBTagWeight)
  mceffW_SF_light_Down  = getTagWeightDict(mceff["mceffs_SF_light_Down"], maxConsideredBTagWeight)
  if not separateBTagWeights:
    lweight = s.weight
  else: lweight = 1.
  #if not separateBTagWeights:
  for i in range(1, maxConsideredBTagWeight+2):
    setattr(s, weightName+str(i)+'p', lweight)
    setattr(s, weightName+str(i)+'p_SF', lweight)
    setattr(s, weightName+str(i)+'p_SF_b_Up', lweight)
    setattr(s, weightName+str(i)+'p_SF_b_Down', lweight)
    setattr(s, weightName+str(i)+'p_SF_light_Up', lweight)
    setattr(s, weightName+str(i)+'p_SF_light_Down', lweight)
  for i in range(maxConsideredBTagWeight+1):
    setattr(s, weightName+str(i),                  mceffW[i]*lweight)
    setattr(s, weightName+str(i)+"_SF",            mceffW_SF[i]*lweight)
    setattr(s, weightName+str(i)+"_SF_b_Up",       mceffW_SF_b_Up[i]*lweight)
    setattr(s, weightName+str(i)+"_SF_b_Down",     mceffW_SF_b_Down[i]*lweight)
    setattr(s, weightName+str(i)+"_SF_light_Up",   mceffW_SF_light_Up[i]*lweight)
    setattr(s, weightName+str(i)+"_SF_light_Down", mceffW_SF_light_Down[i]*lweight)
    for j in range(i+1, maxConsideredBTagWeight+2):
      setattr(s, weightName+str(j)+"p",               getattr(s, weightName+str(j)+"p")               - mceffW[i]*lweight) #prob. for >=j b-tagged jets
      setattr(s, weightName+str(j)+"p_SF",            getattr(s, weightName+str(j)+"p_SF")            - mceffW_SF[i]*lweight)
      setattr(s, weightName+str(j)+"p_SF_b_Up",       getattr(s, weightName+str(j)+"p_SF_b_Up")       - mceffW_SF_b_Up[i]*lweight)
      setattr(s, weightName+str(j)+"p_SF_b_Down",     getattr(s, weightName+str(j)+"p_SF_b_Down")     - mceffW_SF_b_Down[i]*lweight)
      setattr(s, weightName+str(j)+"p_SF_light_Up",   getattr(s, weightName+str(j)+"p_SF_light_Up")   - mceffW_SF_light_Up[i]*lweight)
      setattr(s, weightName+str(j)+"p_SF_light_Down", getattr(s, weightName+str(j)+"p_SF_light_Down") - mceffW_SF_light_Down[i]*lweight)
  for i in range (int(r.nJet)+1, maxConsideredBTagWeight+1):
    setattr(s, weightName+str(i),                   0.)
    setattr(s, weightName+str(i)+"_SF",             0.)
    setattr(s, weightName+str(i)+"_SF_b_Up",        0.)
    setattr(s, weightName+str(i)+"_SF_b_Down",      0.)
    setattr(s, weightName+str(i)+"_SF_light_Up",    0.)
    setattr(s, weightName+str(i)+"_SF_light_Down",  0.)
    setattr(s, weightName+str(i)+"p",               0.)
    setattr(s, weightName+str(i)+"p_SF",            0.)
    setattr(s, weightName+str(i)+"p_SF_b_Up",       0.)
    setattr(s, weightName+str(i)+"p_SF_b_Down",     0.)
    setattr(s, weightName+str(i)+"p_SF_light_Up",   0.)
    setattr(s, weightName+str(i)+"p_SF_light_Down", 0.)
  return

def calc_LeptonScale_factors_and_systematics(s,histos_LS):
  mu_mediumID_histo   = histos_LS['mu_mediumID_histo']
  mu_looseID_histo    = histos_LS['mu_looseID_histo']
  mu_miniIso02_histo  = histos_LS['mu_miniIso02_histo']
  mu_sip3d_histo      = histos_LS['mu_sip3d_histo']
  mu_HIP_histo        = histos_LS['mu_HIP_histo']
  ele_cutbased_histo  = histos_LS['ele_cutbased_histo']
  ele_miniIso01_histo = histos_LS['ele_miniIso01_histo']
  ele_gsf_histo       = histos_LS['ele_gsf_histo']
  if s.singleMuonic and s.leptonPt<120:
    s.lepton_muSF_mediumID      = mu_mediumID_histo.GetBinContent(mu_mediumID_histo.FindBin(s.leptonPt,abs(s.leptonEta)))
    s.lepton_muSF_looseID       = mu_looseID_histo.GetBinContent(mu_looseID_histo.FindBin(s.leptonPt,abs(s.leptonEta)))
    s.lepton_muSF_miniIso02     = mu_miniIso02_histo.GetBinContent(mu_miniIso02_histo.FindBin(s.leptonPt,abs(s.leptonEta)))         
    s.lepton_muSF_sip3d         = mu_sip3d_histo.GetBinContent(mu_sip3d_histo.FindBin(s.leptonPt,abs(s.leptonEta)))
    #s.lepton_muSF_HIP           = mu_HIP_histo.GetBinContent(mu_HIP_histo.FindBin(s.leptonEta))
    s.lepton_muSF_HIP           = mu_HIP_histo.Eval(s.leptonEta)
    s.lepton_muSF_mediumID_err  = mu_mediumID_histo.GetBinError(mu_mediumID_histo.FindBin(s.leptonPt,abs(s.leptonEta)))
    s.lepton_muSF_looseID_err   = mu_looseID_histo.GetBinError(mu_looseID_histo.FindBin(s.leptonPt,abs(s.leptonEta)))
    s.lepton_muSF_miniIso02_err = mu_miniIso02_histo.GetBinError(mu_miniIso02_histo.FindBin(s.leptonPt,abs(s.leptonEta)))       
    s.lepton_muSF_sip3d_err     = mu_sip3d_histo.GetBinError(mu_sip3d_histo.FindBin(s.leptonPt,abs(s.leptonEta)))
    #s.lepton_muSF_HIP_err       = mu_HIP_histo.GetBinError(mu_HIP_histo.FindBin(s.leptonEta))
    s.lepton_muSF_systematic    = 0.03
  if s.singleMuonic and s.leptonPt>=120:
    s.lepton_muSF_mediumID      = mu_mediumID_histo.GetBinContent(mu_mediumID_histo.FindBin(119,abs(s.leptonEta)))
    s.lepton_muSF_looseID       = mu_looseID_histo.GetBinContent(mu_looseID_histo.FindBin(119,abs(s.leptonEta)))
    s.lepton_muSF_miniIso02     = mu_miniIso02_histo.GetBinContent(mu_miniIso02_histo.FindBin(119,abs(s.leptonEta)))
    s.lepton_muSF_sip3d         = mu_sip3d_histo.GetBinContent(mu_sip3d_histo.FindBin(119,abs(s.leptonEta)))
    #s.lepton_muSF_HIP           = mu_HIP_histo.GetBinContent(mu_HIP_histo.FindBin(s.leptonEta))
    s.lepton_muSF_HIP           = mu_HIP_histo.Eval(s.leptonEta)
    s.lepton_muSF_mediumID_err  = mu_mediumID_histo.GetBinError(mu_mediumID_histo.FindBin(119,abs(s.leptonEta)))
    s.lepton_muSF_looseID_err   = mu_looseID_histo.GetBinError(mu_looseID_histo.FindBin(119,abs(s.leptonEta)))
    s.lepton_muSF_miniIso02_err = mu_miniIso02_histo.GetBinError(mu_miniIso02_histo.FindBin(119,abs(s.leptonEta)))
    #s.lepton_muSF_HIP_err       = mu_HIP_histo.GetBinError(mu_HIP_histo.FindBin(s.leptonEta))
    s.lepton_muSF_systematic    = 0.03
  if s.singleElectronic and s.leptonEt<200:
    s.lepton_eleSF_cutbasedID     = ele_cutbased_histo.GetBinContent(ele_cutbased_histo.FindBin(s.leptonEt,abs(s.leptonEta)))      
    s.lepton_eleSF_miniIso01      = ele_miniIso01_histo.GetBinContent(ele_miniIso01_histo.FindBin(s.leptonEt,abs(s.leptonEta)))
    s.lepton_eleSF_gsf            = ele_gsf_histo.GetBinContent(ele_gsf_histo.FindBin(s.leptonEta,100)) ##pt independent
    s.lepton_eleSF_cutbasedID_err = ele_cutbased_histo.GetBinError(ele_cutbased_histo.FindBin(s.leptonEt,abs(s.leptonEta)))
    s.lepton_eleSF_miniIso01_err  = ele_miniIso01_histo.GetBinError(ele_miniIso01_histo.FindBin(s.leptonEt,abs(s.leptonEta)))
    s.lepton_eleSF_gsf_err        = ele_gsf_histo.GetBinError(ele_gsf_histo.FindBin(s.leptonEta,100)) ##pt independent
  if s.singleElectronic and s.leptonEt>=200:
    s.lepton_eleSF_cutbasedID     = ele_cutbased_histo.GetBinContent(ele_cutbased_histo.FindBin(199,abs(s.leptonEta)))
    s.lepton_eleSF_miniIso01      = ele_miniIso01_histo.GetBinContent(ele_miniIso01_histo.FindBin(199,abs(s.leptonEta)))
    s.lepton_eleSF_gsf            = ele_gsf_histo.GetBinContent(ele_gsf_histo.FindBin(s.leptonEta,100)) ##pt independent
    s.lepton_eleSF_cutbasedID_err = ele_cutbased_histo.GetBinError(ele_cutbased_histo.FindBin(199,abs(s.leptonEta)))
    s.lepton_eleSF_miniIso01_err  = ele_miniIso01_histo.GetBinError(ele_miniIso01_histo.FindBin(199,abs(s.leptonEta)))
    s.lepton_eleSF_gsf_err        = ele_gsf_histo.GetBinError(ele_gsf_histo.FindBin(s.leptonEta,100)) ##pt independent
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

def weightsForDLttBar(s):
        wmean = 6.4 - 0.5
        constant = (1.22,0.036)
        slope    = (-0.044,0.019)
        constVariation = sqrt((1-constant[0])**2+(constant[1])**2) 
        slopevariation = sqrt((slope[0])**2+(slope[1])**2)
        if (s.ngenLep+s.ngenTau) == 2:
            s.DilepNJetCorr          = constant[0]+slope[0]*(s.nJet30-wmean)
            s.DilepNJetWeightConstUp = 1-constVariation
            s.DilepNJetWeightSlopeUp = 1+ (s.nJet30-wmean)*slopevariation
            s.DilepNJetWeightConstDn = 1+constVariation
            s.DilepNJetWeightSlopeDn = 1- (s.nJet30-wmean)*slopevariation
        else:
            s.DilepNJetCorr          = 1.
            s.DilepNJetWeightConstUp = 1.
            s.DilepNJetWeightSlopeUp = 1.
            s.DilepNJetWeightConstDn = 1.
            s.DilepNJetWeightSlopeDn = 1.
  


def calcDLDictionary(s,r,keepIdx , discardIdx ,tightHardLep):
   out_dict = {}

   met_4vec = ROOT.TLorentzVector()
   met_4vec.SetPtEtaPhiM(r.met_pt,r.met_eta,r.met_phi,r.met_mass)
   met_2vec = ROOT.TVector2(met_4vec.Px(),met_4vec.Py())
   lepToDiscard4D = ROOT.TLorentzVector()
   lepToDiscard4D.SetPtEtaPhiM(tightHardLep[discardIdx]['pt'],tightHardLep[discardIdx]['eta'],tightHardLep[discardIdx]['phi'],tightHardLep[discardIdx]['mass'])
   lepToKeep4D = ROOT.TLorentzVector()
   lepToKeep4D.SetPtEtaPhiM(tightHardLep[keepIdx]['pt'],tightHardLep[keepIdx]['eta'],tightHardLep[keepIdx]['phi'],tightHardLep[keepIdx]['mass'])

   lepToDiscard2D = ROOT.TVector2(lepToDiscard4D.Px(),lepToDiscard4D.Py())
   lepToKeep2D = ROOT.TVector2(lepToKeep4D.Px(),lepToKeep4D.Py())

   Met2D_AddFull = met_2vec + lepToDiscard2D #adding lost lepton pt to met
   Met2D_AddThird = met_2vec + (1/3.*lepToDiscard2D)
   LepToKeep_pt = lepToKeep2D.Mod()

   DL_dPhiLepW = {}
   DL_ST = {}
   DL_HT = {}
   DL_nJet = {}

   recoWp4 = lepToKeep2D + met_2vec
   DL_dPhiLepW["notAddLepMet"] = lepToKeep2D.DeltaPhi(recoWp4) # [0]: not adding leptons to MET
   DL_ST["notAddLepMet"] = lepToKeep2D.Mod() + met_2vec.Mod()
   DL_HT["notAddLepMet"] = s.htJet30j
   DL_nJet["notAddLepMet"] = s.nJet30

   recoWp4_AddFull = lepToKeep2D + Met2D_AddFull
   DL_dPhiLepW["AddLepMet"] = lepToKeep2D.DeltaPhi(recoWp4_AddFull) # [0]: adding lost lepton pt to met
   DL_ST["AddLepMet"] = lepToKeep2D.Mod() + Met2D_AddFull.Mod()
   dlht = s.htJet30j + (lepToDiscard2D.Mod() if lepToDiscard2D.Mod()>30. else 0.)
   DL_HT["AddLepMet"] = dlht
   njet_new = s.nJet30 + (1 if lepToDiscard2D.Mod()>30. else 0.)
   DL_nJet["AddLepMet"] = njet_new

   recoWp4_AddThird = lepToKeep2D + Met2D_AddThird
   DL_dPhiLepW["AddLep1ov3Met"] = lepToKeep2D.DeltaPhi(recoWp4_AddThird) # [2]: adding 1/3 of lepton ptto met 
   DL_ST["AddLep1ov3Met"] = lepToKeep2D.Mod() + Met2D_AddThird.Mod()
   dlht = s.htJet30j + (2/3.*lepToDiscard2D.Mod() if 2/3.*lepToDiscard2D.Mod()>30 else 0.)
   DL_HT["AddLep1ov3Met"] = dlht
   njet_new = s.nJet30 + (1 if 2/3.*lepToDiscard2D.Mod()>30 else 0.)
   DL_nJet["AddLep1ov3Met"] = njet_new

   out_dict["l1l2ovMET"]    =  (tightHardLep[0]['pt'] + tightHardLep[1]['pt'])/met_4vec.Pt()
   out_dict["Vecl1l2ovMET"] = (lepToKeep2D + lepToDiscard2D).Mod()/met_4vec.Pt()
   out_dict["DPhil1l2"]     = lepToKeep2D.DeltaPhi(lepToDiscard2D)


   out_dict["DL_dPhiLepW"] = DL_dPhiLepW
   out_dict["DL_ST"] = DL_ST
   out_dict["DL_HT"] = DL_HT
   out_dict["DL_nJet"] = DL_nJet

   out_dict["LepToKeep_pt"] = LepToKeep_pt

   #print out_dict

   return out_dict


def calc_diLep_contributions(s,r,tightHardLep,rand_input):
  if s.nTightHardLeptons==2:
    #print "n lepton :" , s.nTightHardLeptons
    passSel = False
    lep1_vec = ROOT.TLorentzVector()
    lep1_vec.SetPtEtaPhiM(tightHardLep[0]['pt'],tightHardLep[0]['eta'],tightHardLep[0]['phi'],tightHardLep[0]['mass'])
    lep2_vec = ROOT.TLorentzVector()
    lep2_vec.SetPtEtaPhiM(tightHardLep[1]['pt'],tightHardLep[1]['eta'],tightHardLep[1]['phi'],tightHardLep[1]['mass'])
    ll_vec = lep1_vec+lep2_vec
    #print tightHardLep[0]['pdgId'] , lep1_vec.M() , lep2_vec.M() , lep2_vec.Pt() ,ll_vec.M()
    if tightHardLep[0]['charge'] != tightHardLep[1]['charge']: passSel = True
    if (tightHardLep[0]['pdgId'] == -tightHardLep[1]['pdgId']) and abs(ll_vec.M()-91.2)<10. : passSel = False
    if passSel:
      random = ROOT.TRandom2(int(rand_input))
      uniform01 = random.Rndm()
      #print "uniform:" , uniform01
      lepToKeep = int(uniform01>0.5)
      #print "leptokeep: " , lepToKeep
      s.LepToKeep_pdgId = tightHardLep[lepToKeep]["pdgId"]
      lepToDiscard = int(not lepToKeep)
      aktions = ["notAddLepMet" , "AddLepMet" , "AddLep1ov3Met"]
      var_DLs = ["ST","HT","dPhiLepW","nJet"]
      keepIdx=lepToDiscard
      discardIdx=lepToKeep
      outdict = calcDLDictionary(s,r, keepIdx ,discardIdx ,tightHardLep)
      #print "after the fuction:" , outdict
      for action in aktions:
        for var_DL in var_DLs :
          #print "s.DL_"+var_DL+"_lepToDiscard_"+action
          exec("s.DL_"+var_DL+"_lepToDiscard_"+action+"="+str(outdict["DL_"+var_DL][action]))

      s.l1l2ovMET_lepToDiscard   = outdict["l1l2ovMET"]
      s.Vecl1l2ovMET_lepToDiscard = outdict["Vecl1l2ovMET"]
      s.DPhil1l2_lepToDiscard  = outdict["DPhil1l2"]

      keepIdx=lepToKeep
      discardIdx=lepToDiscard
      outdict = calcDLDictionary(s,r, keepIdx ,discardIdx ,tightHardLep)
      for action in aktions:
        for var_DL in var_DLs :
          #print "s.DL_"+var_DL+"_lepToKeep_"+action
          exec("s.DL_"+var_DL+"_lepToKeep_"+action+"="+str(outdict["DL_"+var_DL][action]))

      s.l1l2ovMET_lepToKeep   = outdict["l1l2ovMET"]
      s.Vecl1l2ovMET_lepToKeep= outdict["Vecl1l2ovMET"]
      s.DPhil1l2_lepToKeep    = outdict["DPhil1l2"]

      s.LepToKeep_pt = outdict["LepToKeep_pt"]

  return

def getNew_METandLT_WithJEC(s,r, corrJEC = "central"):

   # jet pT threshold for MET
   minJpt = 15

   jforMET_list = ['rawPt','pt', 'eta', 'phi', 'mass' ,'id','hadronFlavour','btagCSV', 'btagCMVA','corr_JECUp','corr_JECDown','corr']

   oldjets = get_cmg_JetsforMEt_fromStruct(r,jforMET_list)

   newjets = oldjets

   oldjets = filter(lambda j:j['pt']>minJpt , oldjets)
   for jet in oldjets: 
      jet['4vec'] = ROOT.TLorentzVector()
      jet['4vec'].SetPtEtaPhiM(jet['pt'],jet['eta'],jet['phi'],jet['mass'])

   # vectorial sum of jets for MET
   deltaJetP4 = ROOT.TLorentzVector(0,0,0,0)
   for jet in oldjets: deltaJetP4 += jet['4vec']

   if corrJEC == "central":
       for jet in newjets: jet['pt'] = jet['rawPt'] * jet['corr']
   elif corrJEC == "up":
       for jet in newjets: jet['pt'] = jet['rawPt'] * jet['corr_JECUp']
   elif corrJEC == "down":
       for jet in newjets: jet['pt'] = jet['rawPt'] * jet['corr_JECDown']

   # filter jets
   newjets = filter(lambda j:j['pt']>minJpt , newjets)

   for jet in newjets:
    jet['4vec'] = ROOT.TLorentzVector()
    jet['4vec'].SetPtEtaPhiM(jet['pt'],jet['eta'],jet['phi'],jet['mass'])
   #print "new Jets " , len(newjets)
   # vectorial sum of jets to substruct
   for jet in newjets: deltaJetP4 -= jet['4vec']  ###now deltaJetP4 is the difference 

   met_4vec = ROOT.TLorentzVector()
   met_4vec.SetPtEtaPhiM(r.met_pt,r.met_eta,r.met_phi,r.met_mass)

   newMET = met_4vec - deltaJetP4
   newLT = s.leptonPt + newMET.Pt()
   newDeltaPhi_Wl = acos((s.leptonPt+newMET.Pt()*cos(s.leptonPhi-newMET.Phi()))/sqrt(s.leptonPt**2+newMET.Pt()**2+2*newMET.Pt()*s.leptonPt*cos(s.leptonPhi-newMET.Phi())))
    
   #print "OLD MET:", met_4vec.Pt() ,"MET diff = ", deltaJetP4.Pt() , "NEW MET:" , newMET.Pt() 
   return {"MeT": newMET.Pt(), "LT": max(0,newLT) ,'deltaPhi_Wl': max(0,newDeltaPhi_Wl)}

def getNew_JetVars_WithJEC(r ,corrJEC = "central"):

   ##jet collection has 20 GeV cut  
   j_list = ['rawPt','pt', 'eta', 'phi', 'mass' ,'id','btagCSV', 'btagCMVA','corr_JECUp','corr_JECDown','corr']
   jets = get_cmg_jets_fromStruct(r,j_list) 
   newjets = jets
   if corrJEC == "central":
       for jet in newjets: jet['pt'] = jet['rawPt'] * jet['corr']
   elif corrJEC == "up":
       for jet in newjets: jet['pt'] = jet['rawPt'] * jet['corr_JECUp']
   elif corrJEC == "down":
       for jet in newjets: jet['pt'] = jet['rawPt'] * jet['corr_JECDown'] 
   
   ##filter new Jets to calculate new Vars
   newjets = filter(lambda j:j['pt']>30 and abs(j['eta'])<2.4 and j['id'] , newjets)
   newHT = sum([x['pt'] for x in jets])
   newNJet = len(newjets)
   newlightJets,  newbJetsCSV = splitListOfObjects('btagCSV', 0.890, newjets)
   newNBtags = len(newbJetsCSV)
   #print {"ht": newHT , "nJet": newNJet , "nBJet": newNBtags }
   return {"ht": newHT , "nJet": newNJet , "nBJet": newNBtags } 


def fill_branch_WithJEC(s,r):

  corr = ["central", "up", "down"]
  vars_corr = ["ht","nJet","nBJet"]
  vars_corr_1 = ["LT","MeT","deltaPhi_Wl"]
  for corrJEC_str in corr:
    central_jet_vars_metLT = getNew_METandLT_WithJEC(s,r, corrJEC = corrJEC_str) 
    central_jet_vars_jetVars = getNew_JetVars_WithJEC(r ,corrJEC = corrJEC_str)
    for vars_str in vars_corr:
      exec("s.jec_"+vars_str+"_"+corrJEC_str+"="+str(central_jet_vars_jetVars[vars_str]))
    for vars_str in vars_corr_1:
      #print vars_str , corrJEC_str , central_jet_vars_metLT[vars_str]
      if central_jet_vars_metLT[vars_str] >1000000  : continue
      #print "s.jec_"+vars_str+"_"+corrJEC_str+"="+str(central_jet_vars_metLT[vars_str])
      exec("s.jec_"+vars_str+"_"+corrJEC_str+"="+str(central_jet_vars_metLT[vars_str]))

  return

def getISRWeight(s,genParts):
  #print "ISR old  yes !!!"
  #genGluino = filter(lambda g:abs(g['pdgId'])==1000021, genParts)
  genGluino = [genPart for genPart in genParts if abs(genPart['pdgId'])==1000021]
  s.ngenGluino = len(genGluino)
  if s.ngenGluino == 2:
    genGluino1_vec = ROOT.TLorentzVector() 
    genGluino2_vec = ROOT.TLorentzVector()
    genGluino1_vec.SetPtEtaPhiM(genGluino[0]['pt'],genGluino[0]['eta'],genGluino[0]['phi'],genGluino[0]['mass'])
    genGluino2_vec.SetPtEtaPhiM(genGluino[1]['pt'],genGluino[1]['eta'],genGluino[1]['phi'],genGluino[1]['mass'])
    gluglu_vec = genGluino1_vec+genGluino2_vec
    s.genGluGlu_pt = gluglu_vec.Pt()
    if s.genGluGlu_pt <= 400: s.ISRSigUp = 1.0; s.ISRSigDown = 1.0
    if s.genGluGlu_pt > 400: s.ISRSigUp = 1.15; s.ISRSigDown = 0.85
    if s.genGluGlu_pt > 600: s.ISRSigUp = 1.30; s.ISRSigDown = 0.70

  return


def getISRWeight_new(s,nisrJets):
  #print "ISR new YES"
  #if not nisrJets==0: print nisrJets
  weight_dict = {
                0:{"weight":1    ,"sys":1,"stat":1},\
                1:{"weight":0.920,"sys":0.040,"stat":0.005},\
                2:{"weight":0.821,"sys":0.090,"stat":0.006},\
                3:{"weight":0.715,"sys":0.143,"stat":0.009},\
                4:{"weight":0.662,"sys":0.169,"stat":0.016},\
                5:{"weight":0.561,"sys":0.219,"stat":0.027},\
                6:{"weight":0.511,"sys":0.244,"stat":0.041}
                }
  if nisrJets < 6:
      s.weight_ISR_new        =   weight_dict[nisrJets]["weight"]
      s.ISRSigUp_stat_new     = 1+weight_dict[nisrJets]["stat"]
      s.ISRSigDown_stat_new   = 1-weight_dict[nisrJets]["stat"] 
      s.ISRSigUp_sys_new      = 1+weight_dict[nisrJets]["sys"]
      s.ISRSigDown_sys_new    = 1-weight_dict[nisrJets]["sys"]
  if nisrJets >= 6: 
      s.weight_ISR_new      = weight_dict[6]["weight"]
      s.ISRSigUp_stat_new   = 1+weight_dict[6]["stat"]
      s.ISRSigDown_stat_new = 1-weight_dict[6]["stat"] 
      s.ISRSigUp_sys_new    = 1+weight_dict[6]["sys"]
      s.ISRSigDown_sys_new  = 1-weight_dict[6]["sys"]
      
  return

def filter_crazy_jets(jets,genParts):
    ismatched = True
    for jet in jets:
      ismatched = True
      if not (abs(jet["eta"])<2.5 and jet["pt"]>20): continue
      for genPart in genParts:
        if not ismatched :  break
        dR = deltaR(jet,genPart)
        if dR >= 0.3 and jet["chHEF"]<0.1:
          #print dR , jet["chHEF"]
          ismatched = False
    return ismatched


def getGenWandLepton(c):
  genPartAll = [getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex'], j) for j in range(int(c.GetLeaf('nGenPart').GetValue()))]
  lepton = filter(lambda l:abs(l['pdgId']) in [11,13,15], genPartAll)
  if len(lepton)==0:
    print "no generated lepton found (hadronic ttjets event)!"
    p4w=False
    p4lepton=False
    return p4w, p4lepton
  lFromW = filter(lambda w:abs(w['motherId'])==24, lepton)
  if len(lFromW)==0:
    test = filter(lambda w:w['motherId']==24, lepton)
    if len(test)==0: print 'No lepton from W found (hadronic ttjets event)!'
    p4w=False
    p4lepton=False
    return p4w, p4lepton
  elif len(lFromW)>0:
    Ws = []
    leps = []
    for i in range(len(lFromW)):
      if abs(lFromW[i]['motherId'])!=24: print '4)this should not have happened'
      genW = getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex'], int(lFromW[i]['motherIndex']))
      if abs(genW['pdgId'])!=24: '5)this should not have happened'
      W = ROOT.TLorentzVector()
      W.SetPtEtaPhiM(genW['pt'],genW['eta'],genW['phi'],genW['mass'])
      lep = ROOT.TLorentzVector()
      lep.SetPtEtaPhiM(lFromW[i]['pt'],lFromW[i]['eta'],lFromW[i]['phi'],lFromW[i]['mass'])
      p4lepton = ROOT.LorentzVector(lep.Px(),lep.Py(),lep.Pz(),lep.E())
      p4w = ROOT.LorentzVector(W.Px(),W.Py(),W.Pz(),W.E())
      Ws.append(p4w)
      leps.append(p4lepton)
    if len(lFromW)>2:
      print '3)this should not have happened'
  return Ws, leps

def getGenTopWLepton(c):
  genPartAll = [getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','charge','motherId','motherIndex'], j) for j in range(int(c.GetLeaf('nGenPart').GetValue()))]
  lepton = filter(lambda l:abs(l['pdgId']) in [11,13,15], genPartAll)
  if len(lepton)==0:
    p4t=False
    p4w=False
    p4lepton=False
    return p4t, p4w, p4lepton
  lFromW = filter(lambda w:abs(w['motherId'])==24, lepton)
  if len(lFromW)>0:
    if len(lFromW)==1:
      if abs(lFromW[0]['motherId'])!=24: print '1)this should not have happened'
      genW = getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','charge','motherId','motherIndex'], int(lFromW[0]['motherIndex']))
      if abs(genW['pdgId'])!=24: '2)this should not have happened'
      genTop = getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','charge','motherId','motherIndex'], int(genW['motherIndex']))
      lep = ROOT.TLorentzVector()
      lep.SetPtEtaPhiM(lFromW[0]['pt'],lFromW[0]['eta'],lFromW[0]['phi'],lFromW[0]['mass'])
    elif len(lFromW)==2:
      match = False
      leadLep = getObjDict(c, 'LepGood_', ['pt','eta','phi','mass','pdgId','charge'], 0)
      for l in lFromW:
        if leadLep['charge'] == l['charge']:
          match = True
          genW = getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','charge','motherId','motherIndex'], int(l['motherIndex']))
          genTop = getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','charge','motherId','motherIndex'], int(genW['motherIndex']))
          lep = ROOT.TLorentzVector()
          lep.SetPtEtaPhiM(l['pt'],l['eta'],l['phi'],l['mass'])
      if not match:
        print 'No match at all!'
        p4t=False
        p4w=False
        p4lepton=False
        return p4t, p4w, p4lepton
  elif len(lFromW)>2 or len(lFromW)==0:
    print "8) this should not have happened"
    p4t=False
    p4w=False
    p4lepton=False
    return p4t, p4w, p4lepton
  t = ROOT.TLorentzVector()
  W = ROOT.TLorentzVector()
  W.SetPtEtaPhiM(genW['pt'],genW['eta'],genW['phi'],genW['mass'])
  t.SetPtEtaPhiM(genTop['pt'],genTop['eta'],genTop['phi'],genTop['mass'])
  p4lepton = ROOT.LorentzVector(lep.Px(),lep.Py(),lep.Pz(),lep.E())
  p4w = ROOT.LorentzVector(W.Px(),W.Py(),W.Pz(),W.E())
  p4t = ROOT.LorentzVector(t.Px(),t.Py(),t.Pz(),t.E())
  return p4t, p4w, p4lepton


