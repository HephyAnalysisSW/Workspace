import copy, os, sys
#dir  = '/data/easilar/cmgTuples/postProcessed_miniAODv2_fix//HT500LT250/hard/'
#dir = '/data/easilar/cmgTuples/postProcessed_miniAODv2_2100pb/HT500LT250/hard/'
#dir = '/data/easilar/cmgTuples/postProcessed_data_miniAODv2_2100pb_vetoEventsFix/'
#dir = '/data/easilar/cmgTuples/postProcessing_data_2p2fb/HT500LT250/'
#dir = '/data/easilar/cmgTuples/postProcessing_Data_with_filters_v2/HT500LT250Skim/'
#dir = '/data/easilar/cmgTuples/postProcessing_Data_Jecv7_forApproval/'
#dir = '/data/easilar/cmgTuples/postProcessing_data_2p2fb_diLep/HT500LT250/'
#dir = '/data/easilar/cmgTuples/postProcessing_Data_Jecv7_v2/'
dir ='/data/easilar/cmgTuples/postProcessing_Spring16/HT500LT250Skim/'

single_mu_Run2016B = {\
"name" : "SingleMuon_Run2016B_PromptReco_v2_HT500ST250",
"bins" : [
"SingleMuon_Run2016B_PromptReco_v2",
],
'dir' : dir,
}


single_ele_Run2016B = {\
"name" : "SingleElectron_Run2016B_PromptReco_v2_HT500ST250",
"bins" : [
"SingleElectron_Run2016B_PromptReco_v2",
],
'dir' : dir,
}

