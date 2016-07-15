import copy, os, sys
#dirData ='/data/dspitzbart/cmgTuples/postProcessed_2016B_antiSelection_21062016/none/'
dirData ='/data/dspitzbart/cmgTuples/postProcessed_2016B_antiSelection_28062016/none/'
dirMuon = '/data/dspitzbart/cmgTuples/postProcessing_Run2016BC_JECv6_antiSelection/HT500/'
dirElectron = '/afs/hephy.at/data/dspitzbart01/cmgTuples/ppRun2016BC_AS/HT500/'


single_mu_Run2016B_antiSel_1 = {\
"name" : "SingleMuon_Run2016B_PromptReco_v2_1",
"bins" : [
"SingleMuon_Run2016B-PromptReco-v2",
],
'dir' : dirMuon+'SingleMuon_Run2016B-PromptReco-v2/',
}

single_mu_Run2016B_antiSel_2 = {\
"name" : "SingleMuon_Run2016B_PromptReco_v2_2",
"bins" : [
"SingleMuon_Run2016B-PromptReco-v2",
],
'dir' : dirMuon+'SingleMuon_Run2016B-PromptReco-v2_1/',
}

single_mu_Run2016B_antiSel_3 = {\
"name" : "SingleMuon_Run2016B_PromptReco_v2_3",
"bins" : [
"SingleMuon_Run2016B-PromptReco-v2",
],
'dir' : dirMuon+'SingleMuon_Run2016B-PromptReco-v2_1_a/',
}

single_mu_Run2016B_antiSel_4 = {\
"name" : "SingleMuon_Run2016B_PromptReco_v2_4",
"bins" : [
"SingleMuon_Run2016B-PromptReco-v2",
],
'dir' : dirMuon+'SingleMuon_Run2016B-PromptReco-v2_1_b/',
}

single_mu_Run2016B_antiSel_5 = {\
"name" : "SingleMuon_Run2016B_PromptReco_v2_5",
"bins" : [
"SingleMuon_Run2016B-PromptReco-v2",
],
'dir' : dirMuon+'SingleMuon_Run2016B-PromptReco-v2_2/',
}

single_mu_Run2016C_antiSel = {\
"name" : "SingleMuon_Run2016C_PromptReco_v2",
"bins" : [
"SingleMuon_Run2016C-PromptReco-v2",
],
'dir' : dirMuon+'SingleMuon_Run2016C-PromptReco-v2/',
}




single_ele_Run2016B_antiSel_1 = {\
"name" : "SingleElectron_Run2016B_PromptReco_v2_1",
"bins" : [
"SingleElectron_Run2016B-PromptReco-v2",
],
'dir' : dirElectron+"SingleElectron_Run2016B-PromptReco-v2/",
}

single_ele_Run2016B_antiSel_2 = {\
"name" : "SingleElectron_Run2016B_PromptReco_v2_2",
"bins" : [
"SingleElectron_Run2016B-PromptReco-v2",
],
'dir' : dirElectron+"SingleElectron_Run2016B-PromptReco-v2_1/",
}

single_ele_Run2016B_antiSel_3 = {\
"name" : "SingleElectron_Run2016B_PromptReco_v2_3",
"bins" : [
"SingleElectron_Run2016B-PromptReco-v2",
],
'dir' : dirElectron+"SingleElectron_Run2016B-PromptReco-v2_1_a/",
}

single_ele_Run2016B_antiSel_4 = {\
"name" : "SingleElectron_Run2016B_PromptReco_v2_4",
"bins" : [
"SingleElectron_Run2016B-PromptReco-v2",
],
'dir' : dirElectron+"SingleElectron_Run2016B-PromptReco-v2_1_b/",
}

single_ele_Run2016B_antiSel_5 = {\
"name" : "SingleElectron_Run2016B_PromptReco_v2_5",
"bins" : [
"SingleElectron_Run2016B-PromptReco-v2",
],
'dir' : dirElectron+"SingleElectron_Run2016B-PromptReco-v2_2/",
}

single_ele_Run2016C_antiSel = {\
"name" : "SingleElectron_Run2016C_PromptReco_v2",
"bins" : [
"SingleElectron_Run2016B-PromptReco-v2",
],
'dir' : dirElectron + "SingleElectron_Run2016B-PromptReco-v2/",
}

