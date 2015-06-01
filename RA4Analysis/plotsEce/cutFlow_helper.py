minPt_Lep = 25  ##hard leptons
minPt_Lep_loose = 10
maxEta_e = 2.5
maxEta_mu = 2.4
minPt_Jet = 30
maxEta_Jet = 2.4
ID_mu=1
minID_e=3
minRelIso_lep_loose=0.4
minRelIso_e=0.1
minRelIso_mu=0.2
max_sip3d = 4.0
min_njets = 6
min_st = 200
min_ht = 500
min_DPhi = 1
nbjet = 0
btag_var = 0.814

ele_MVAID_cuts_loose={'eta08':0.35 , 'eta104':0.20,'eta204': -0.52}
ele_MVAID_cuts_tight={'eta08':0.73 , 'eta104':0.57,'eta204':  0.05}

ele_MVAID_cutstr_loose= "Sum$((abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>"+ str(ele_MVAID_cuts_loose['eta08'])+")"\
                       +"||((abs(LepGood_eta)>0.8&&abs(LepGood_eta)<1.44)&&LepGood_mvaIdPhys14>"+ str(ele_MVAID_cuts_loose['eta104'])+")"\
                       +"||((abs(LepGood_eta)>1.57)&&LepGood_mvaIdPhys14>"+str(ele_MVAID_cuts_loose['eta204'])+"))"

ele_MVAID_cutstr_tight= "Sum$((abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>"+ str(ele_MVAID_cuts_tight['eta08'])+")"\
                       +"||((abs(LepGood_eta)>0.8&&abs(LepGood_eta)<1.44)&&LepGood_mvaIdPhys14>"+ str(ele_MVAID_cuts_tight['eta104'])+")"\
                       +"||((abs(LepGood_eta)>1.57)&&LepGood_mvaIdPhys14>"+str(ele_MVAID_cuts_tight['eta204'])+"))"
ele_Eta_acc_cut_str = "Sum$((abs(LepGood_eta)<1.44||abs(LepGood_eta)>1.57)&&abs(LepGood_eta)<"+str(maxEta_e)+")"

mu_tight = "(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>"+str(minPt_Lep)+"&&abs(LepGood_eta)<"+str(maxEta_mu)+"&&LepGood_tightId=="+str(ID_mu)+"&&LepGood_sip3d<"+str(max_sip3d)+"&&LepGood_miniRelIso<"+str(minRelIso_mu)+"))"
mu_loose = "(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>"+str(minPt_Lep_loose)+"&&LepGood_miniRelIso<"+str(minRelIso_lep_loose)+"&&LepGood_mediumMuonId=="+str(ID_mu)+"))"

e_tight  = "(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>"+str(minPt_Lep)+"&&"+ele_Eta_acc_cut_str+"&&LepGood_tightId>="+str(minID_e)+"&&LepGood_miniRelIso<"+str(minRelIso_e)+"&&"+ele_MVAID_cutstr_tight+"))" 
e_loose  = "(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>"+str(minPt_Lep_loose)+"&&"+ele_Eta_acc_cut_str+"&&LepGood_miniRelIso<"+str(minRelIso_lep_loose)+"&&"+ele_MVAID_cutstr_loose+"))" 

njets_30 = "Sum$(Jet_pt>"+str(minPt_Jet)+"&&abs(Jet_eta)<"+str(maxEta_Jet)+"&&Jet_id)"
nbjets_30 = "Sum$(Jet_pt>"+str(minPt_Jet)+"&&abs(Jet_eta)<"+str(maxEta_Jet)+"&&Jet_id&&Jet_btagCSV>"+str(btag_var)+")"
st = "(Sum$((LepGood_pt+met_pt)>"+str(min_st)+")==1)"
ht = "Sum$(Jet_pt*(Jet_pt>"+str(minPt_Jet)+"&&abs(Jet_eta)<"+str(maxEta_Jet)+"&&Jet_id))"
dPhi = "acos((LepGood_pt+met_pt*cos(LepGood_phi-met_phi))/sqrt(LepGood_pt**2+met_pt**2+2*met_pt*LepGood_pt*cos(LepGood_phi-met_phi)))"

OneLep ="("+mu_tight+"+"+e_tight+"==1"+")"
OneLep_lepveto ="(("+mu_loose+"+"+e_loose+")==1"+")"
OneMu = "("+mu_tight+"==1"+")"
OneMu_lepveto = "("+mu_loose+"==1&&"+e_loose+"==0"+")"
OneE = "("+e_tight+"==1"+")"
OneE_lepveto ="("+mu_loose+"==0&&"+e_loose+"==1"+")"
njets_30_cut = "("+njets_30+")>="+str(min_njets)
nbjets_30_cut = "("+nbjets_30+")=="+str(nbjet)
jets_2_80 = "(Jet_pt[1]>80)"
ht_cut = "("+ht+">"+str(min_ht)+")"
dPhi_cut = "("+"Sum$("+dPhi+">"+str(min_DPhi)+")==1)"







