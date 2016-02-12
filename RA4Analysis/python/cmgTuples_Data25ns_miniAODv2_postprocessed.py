import copy, os, sys
#dir  = '/data/easilar/cmgTuples/postProcessed_miniAODv2_fix//HT500LT250/hard/'
#dir = '/data/easilar/cmgTuples/postProcessed_miniAODv2_2100pb/HT500LT250/hard/'
#dir = '/data/easilar/cmgTuples/postProcessed_data_miniAODv2_2100pb_vetoEventsFix/'
#dir = '/data/easilar/cmgTuples/postProcessing_data_2p2fb/HT500LT250/'
#dir = '/data/easilar/cmgTuples/postProcessing_Data_with_filters_v2/HT500LT250Skim/'
dir = '/data/easilar/cmgTuples/postProcessing_Data_Jecv7_forApproval/'
single_mu_Run2015D = {\
"name" : "single_mu_Run215D",
"bins" : [
"SingleMuon_Run2015D_05Oct",
"SingleMuon_Run2015D_v4",
],
'dir' : dir,
}


single_ele_Run2015D = {\
"name" : "single_ele_Run215D",
"bins" : [
"SingleElectron_Run2015D_05Oct",
"SingleElectron_Run2015D_v4",
],
'dir' : dir,
}

