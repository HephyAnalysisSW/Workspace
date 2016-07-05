
##General

sample_lumi = 3000##pb
lumi = 3990 #2300##pb
lumi_label = 4
scale = '(1)'
btagVarString = 'nBJetMediumCSV30'

##For Data Only

#filters = "(Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter)" # && veto_evt_list)"
filters = "(Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_goodVertices && Flag_eeBadScFilter &&  Flag_globalTightHalo2016Filter && Flag_badChargedHadronFilter && Flag_badMuonFilter)"

trigger = "((HLT_EleHT350||HLT_EleHT400)||(HLT_MuHT350||HLT_MuHT400))"

##Common for Background and Signal
trigger_scale = '((eleDataSet&&0.963)||(muonDataSet&&0.926))'
reweight      = '(weight*'+str(lumi)+')/'+str(sample_lumi)
weight_0b     = 'weightBTag0_SF'
weight_1b     = 'weightBTag1_SF'

##For MC only
lepton_Scale  = 'lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID'
topPt         = 'TopPtWeight'
PU            = 'puReweight_true_max4'
weight_str_plot = '*'.join([reweight,topPt,trigger_scale,PU])
#weight_str_plot = '*'.join([trigger_scale,lepton_Scale,topPt,PU,reweight])
#weight_str_CV   = '*'.join([trigger_scale,lepton_Scale,topPt,reweight])
weight_str_CV   = reweight

##For Signal Only
lepton_Scale_signal = 'reweightLeptonFastSimSF'
weight_str_signal_plot = '*'.join([trigger_scale,lepton_Scale_signal,PU,reweight])
weight_str_signal_CV = '*'.join([trigger_scale,lepton_Scale_signal,reweight])



