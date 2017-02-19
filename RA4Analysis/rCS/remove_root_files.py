import pickle
import ROOT

pickleDir = '/afs/hephy.at/data/easilar01/Results2017/'
#est = 'Prediction_Spring16_templates_aggr_Moriond2017_v1_lep_data_36p5/'
#est = 'Prediction_Spring16_templates_SR_Moriond2017_newTT_lep_data_36p5/'
#est = 'Prediction_Spring16_templates_SR_ICHEP2016_newTT_lep_MC_SF_36p5/'
#est = 'Prediction_Spring16_templates_aggr_Moriond2017_v2_lep_MC_SF_36p5/'
est = 'Prediction_Spring16_templates_SR_Moriond2017_Summer16_lep_MC_SF_36p5/'
pickleDir+=est
res = pickle.load(file(pickleDir+"singleLeptonic_Spring16_iso_Veto_ISRforttJets_NEWttJetsSB_addDiBoson_withSystematics_pkl"))

for nJet in res.keys():
  for lt in res[nJet].keys():
    for ht in res[nJet][lt].keys():
      for fit in res[nJet][lt][ht].keys():
        if "fit_" in fit:
          for rm_file in res[nJet][lt][ht][fit].keys():
            del res[nJet][lt][ht][fit][rm_file]['file']
            del res[nJet][lt][ht][fit][rm_file]['template']

pickle.dump(res, file(pickleDir+'resultsFinal_withSystematics_Filesremoved_pkl','w'))
print "pickle withut files saved here :" , pickleDir+'resultsFinal_withSystematics_Filesremoved_pkl'




