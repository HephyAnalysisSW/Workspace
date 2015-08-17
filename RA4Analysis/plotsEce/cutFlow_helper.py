minPt_Lep = 25  ##hard leptons
minPt_Lep_loose = 10
minPt_e_loose = 10
minPt_e_veto = 10
minPt_mu_veto = 10
minPt_mu_loose = 10
maxEta_e = 2.5
maxEta_mu = 2.5
minPt_Jet = 30
maxEta_Jet = 2.4
ID_mu=1
minID_e=3
minRelIso_lep_loose=0.4
minRelIso_e=0.1
minRelIso_mu=0.2
max_sip3d = 4.0
min_njets = 2
min_st = 250
min_ht = 500
min_DPhi = 1
nbjet = 0
btag_var = 0.890


######muon  selection####

mu_veto       = "(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>="+str(minPt_mu_veto)+"))" #+"&&LepGood_miniRelIso<"+str(minRelIso_lep_loose)+"&&LepGood_mediumMuonId=="+str(ID_mu)+"))"
mu_tight      = "(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>="+str(minPt_Lep)+"&&abs(LepGood_eta)<"+str(maxEta_mu)+"&&LepGood_miniRelIso<"+str(minRelIso_mu)+"&&LepGood_mediumMuonId=="+str(ID_mu)+"&&LepGood_sip3d<"+str(max_sip3d)+"))"



######electron selection#####
ele_MVAID_cuts_loose={'eta08':0.35 , 'eta104':0.20,'eta204': -0.52}
ele_MVAID_cuts_tight={'eta08':0.73 , 'eta104':0.57,'eta204':  0.05}

ele_MVAID_cutstr_loose= "((abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>"+ str(ele_MVAID_cuts_loose['eta08'])+")"\
                       +"||((abs(LepGood_eta)>=0.8&&abs(LepGood_eta)<1.44)&&LepGood_mvaIdPhys14>"+ str(ele_MVAID_cuts_loose['eta104'])+")"\
                       +"||((abs(LepGood_eta)>=1.57)&&LepGood_mvaIdPhys14>"+str(ele_MVAID_cuts_loose['eta204'])+"))"

ele_MVAID_cutstr_tight= "((abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>"+ str(ele_MVAID_cuts_tight['eta08'])+")"\
                       +"||((abs(LepGood_eta)>=0.8&&abs(LepGood_eta)<1.44)&&LepGood_mvaIdPhys14>"+ str(ele_MVAID_cuts_tight['eta104'])+")"\
                       +"||((abs(LepGood_eta)>=1.57)&&LepGood_mvaIdPhys14>"+str(ele_MVAID_cuts_tight['eta204'])+"))"

ele_Eta_acc_cut_str = "((abs(LepGood_eta)<1.44||abs(LepGood_eta)>1.57)&&abs(LepGood_eta)<"+str(maxEta_e)+")"


e_veto        = "(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>="+str(minPt_e_veto)+"))" #+"&&"+ele_Eta_acc_cut_str+"&&LepGood_miniRelIso<"+str(minRelIso_lep_loose)+"&&"+ele_MVAID_cutstr_loose+"))" 
e_tight       = "(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>="+str(minPt_Lep)+"&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<"+str(minRelIso_e)+"&&"+ele_MVAID_cutstr_tight+"&&"+"LepGood_lostHits==0"+"&&"+"LepGood_convVeto"+"&&"+"LepGood_sip3d<"+str(max_sip3d)+"))" 


OneMu = "("+mu_tight+"==1"+")"
OneMu_lepveto = "("+mu_veto+"==1&&"+e_veto+"==0"+")"
OneE = "("+e_tight+"==1"+")"
OneE_lepveto ="("+mu_veto+"==0&&"+e_veto+"==1"+")"
OneLep ="("+mu_tight+"+"+e_tight+"==1"+")"
OneLep_lepveto =  "(("+"abs(LepGood_pdgId)==11&&"+OneE_lepveto+")"+"||"+"("+"abs(LepGood_pdgId)==13&&"+OneMu_lepveto+"))"

####njet and ht definitions###
#njets_30 = "Sum$(Jet_pt>"+str(minPt_Jet)+"&&abs(Jet_eta)<"+str(maxEta_Jet)+"&&Jet_id)"
njets_30 = "Sum$(Jet_pt>"+str(minPt_Jet)+"&&abs(Jet_eta)<"+str(maxEta_Jet)+")"
#nbjets_30 = "Sum$(Jet_pt>"+str(minPt_Jet)+"&&abs(Jet_eta)<"+str(maxEta_Jet)+"&&Jet_id&&Jet_btagCSV>"+str(btag_var)+")"
nbjets_30 = "Sum$(Jet_pt>"+str(minPt_Jet)+"&&abs(Jet_eta)<"+str(maxEta_Jet)+"&&Jet_btagCSV>"+str(btag_var)+")"

#ht = "(Sum$(Jet_pt*(Jet_pt>"+str(minPt_Jet)+"&&abs(Jet_eta)<"+str(maxEta_Jet)+"&&Jet_id)))"
ht = "(Sum$(Jet_pt*(Jet_pt>"+str(minPt_Jet)+"&&abs(Jet_eta)<"+str(maxEta_Jet)+")))"
dPhi = "acos((LepGood_pt[0]+metNoHF_pt*cos(LepGood_phi[0]-metNoHF_phi))/sqrt((LepGood_pt[0]**2)+(metNoHF_pt**2)+(2*metNoHF_pt*LepGood_pt[0]*cos(LepGood_phi[0]-metNoHF_phi))))"
#dPhi = "acos((LepGood_pt+metNoHF_pt*cos(LepGood_phi-metNoHF_phi))/sqrt((LepGood_pt**2)+(metNoHF_pt**2)+(2*metNoHF_pt*LepGood_pt*cos(LepGood_phi-metNoHF_phi))))"


#st = "(Sum$(((LepGood_pt[0]+metNoHF_pt)>"+str(min_st)+")*"+OneLep+")==1)"
st = "(Sum$(((LepGood_pt[0]+metNoHF_pt)>"+str(min_st)+"))==1)"

####njet and ht cuts
njets_30_cut = "(("+njets_30+")>="+str(min_njets)+")"
nbjets_30_cut_zero = "(("+nbjets_30+")=="+str(nbjet)+")"
nbjets_30_cut_multi = "(("+nbjets_30+")>=1)"
jets_2_80 = "(Jet_pt[1]>80)"
#jets_2_80 = "(Jet_pt[1]>80&&abs(Jet_eta)<"+str(maxEta_Jet)+"&&Jet_id))"
ht_cut = "("+ht+">"+str(min_ht)+")"
#dPhi_cut = "("+"Sum$("+dPhi+">"+str(min_DPhi)+")==1)"
dPhi_cut = "("+dPhi+">"+str(min_DPhi)+")"

filters = "(Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_eeBadScFilter)"





