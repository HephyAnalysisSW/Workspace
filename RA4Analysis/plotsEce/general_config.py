
##General

sample_lumi = 3000##pb
lumi = 2250##pb
lumi_label = 2.2

btagVarString = 'nBJetMediumCSV30'

##For Data Only

filters = "(Flag_goodVertices && Flag_HBHENoiseFilter && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter && veto_evt_list)"

trigger = "((HLT_EleHT350)||(HLT_MuHT350))"

##Common for Background and Signal
trigger_scale = '0.94'
reweight      = '(weight*'+str(lumi)+')/'+str(sample_lumi)

##For MC only
lepton_Scale  = 'lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID'
topPt         = 'TopPtWeight'
PU            = 'puReweight_true_max4'
weight_str = '*'.join([trigger_scale,lepton_Scale,topPt,PU,reweight])

##For Signal Only
lepton_Scale_signal = 'reweightLeptonFastSimSF'
weight_str_signal_plot = '*'.join([trigger_scale,lepton_Scale_signal,PU,reweight])
weight_str_signal_CV = '*'.join([trigger_scale,lepton_Scale_signal,reweight])


