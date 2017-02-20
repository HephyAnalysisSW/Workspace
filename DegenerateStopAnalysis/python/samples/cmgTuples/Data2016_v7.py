sample_path_base = '/afs/hephy.at/data/nrad02/cmgTuples/'
sample_path_tag  = '/8025_mAODv2_v7/Data25ns' 

allComponents=[]

import os
if not os.path.isdir(sample_path_base + sample_path_tag):
    sample_path_base = '/data/nrad/cmgTuples/'
    if not os.path.isdir(sample_path_base + sample_path_tag):
        raise Exception("Cannot acces either afs-data or /data ")
sample_path = sample_path_base + sample_path_tag


allComponents=[] 


JetHT_Run2016B_23Sep2016 ={
'cmgName':"JetHT_Run2016B_23Sep2016",
"name" : "JetHT_Run2016B-23Sep2016-v3",
"chunkString":"JetHT_Run2016B-23Sep2016-v3",
"dir": sample_path +"/" + "JetHT_Run2016B-23Sep2016-v3",
"dbsName" : "/JetHT/Run2016B-23Sep2016-v3/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(JetHT_Run2016B_23Sep2016)



JetHT_Run2016C_23Sep2016 ={
'cmgName':"JetHT_Run2016C_23Sep2016",
"name" : "JetHT_Run2016C-23Sep2016-v1",
"chunkString":"JetHT_Run2016C-23Sep2016-v1",
"dir": sample_path +"/" + "JetHT_Run2016C-23Sep2016-v1",
"dbsName" : "/JetHT/Run2016C-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(JetHT_Run2016C_23Sep2016)



JetHT_Run2016D_23Sep2016 ={
'cmgName':"JetHT_Run2016D_23Sep2016",
"name" : "JetHT_Run2016D-23Sep2016-v1",
"chunkString":"JetHT_Run2016D-23Sep2016-v1",
"dir": sample_path +"/" + "JetHT_Run2016D-23Sep2016-v1",
"dbsName" : "/JetHT/Run2016D-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(JetHT_Run2016D_23Sep2016)



JetHT_Run2016E_23Sep2016 ={
'cmgName':"JetHT_Run2016E_23Sep2016",
"name" : "JetHT_Run2016E-23Sep2016-v1",
"chunkString":"JetHT_Run2016E-23Sep2016-v1",
"dir": sample_path +"/" + "JetHT_Run2016E-23Sep2016-v1",
"dbsName" : "/JetHT/Run2016E-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(JetHT_Run2016E_23Sep2016)



JetHT_Run2016F_23Sep2016 ={
'cmgName':"JetHT_Run2016F_23Sep2016",
"name" : "JetHT_Run2016F-23Sep2016-v1",
"chunkString":"JetHT_Run2016F-23Sep2016-v1",
"dir": sample_path +"/" + "JetHT_Run2016F-23Sep2016-v1",
"dbsName" : "/JetHT/Run2016F-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(JetHT_Run2016F_23Sep2016)



JetHT_Run2016G_23Sep2016 ={
'cmgName':"JetHT_Run2016G_23Sep2016",
"name" : "JetHT_Run2016G-23Sep2016-v1",
"chunkString":"JetHT_Run2016G-23Sep2016-v1",
"dir": sample_path +"/" + "JetHT_Run2016G-23Sep2016-v1",
"dbsName" : "/JetHT/Run2016G-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(JetHT_Run2016G_23Sep2016)



JetHT_Run2016H_PromptReco_v2 ={
'cmgName':"JetHT_Run2016H_PromptReco_v2",
"name" : "JetHT_Run2016H-PromptReco-v2",
"chunkString":"JetHT_Run2016H-PromptReco-v2",
"dir": sample_path +"/" + "JetHT_Run2016H-PromptReco-v2",
"dbsName" : "/JetHT/Run2016H-PromptReco-v2/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(JetHT_Run2016H_PromptReco_v2)



JetHT_Run2016H_PromptReco_v3 ={
'cmgName':"JetHT_Run2016H_PromptReco_v3",
"name" : "JetHT_Run2016H-PromptReco-v3",
"chunkString":"JetHT_Run2016H-PromptReco-v3",
"dir": sample_path +"/" + "JetHT_Run2016H-PromptReco-v3",
"dbsName" : "/JetHT/Run2016H-PromptReco-v3/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(JetHT_Run2016H_PromptReco_v3)



MET_Run2016B_23Sep2016 ={
'cmgName':"MET_Run2016B_23Sep2016",
"name" : "MET_Run2016B-23Sep2016-v3",
"chunkString":"MET_Run2016B-23Sep2016-v3",
"dir": sample_path +"/" + "MET_Run2016B-23Sep2016-v3",
"dbsName" : "/MET/Run2016B-23Sep2016-v3/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(MET_Run2016B_23Sep2016)



MET_Run2016C_23Sep2016 ={
'cmgName':"MET_Run2016C_23Sep2016",
"name" : "MET_Run2016C-23Sep2016-v1",
"chunkString":"MET_Run2016C-23Sep2016-v1",
"dir": sample_path +"/" + "MET_Run2016C-23Sep2016-v1",
"dbsName" : "/MET/Run2016C-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(MET_Run2016C_23Sep2016)



MET_Run2016D_23Sep2016 ={
'cmgName':"MET_Run2016D_23Sep2016",
"name" : "MET_Run2016D-23Sep2016-v1",
"chunkString":"MET_Run2016D-23Sep2016-v1",
"dir": sample_path +"/" + "MET_Run2016D-23Sep2016-v1",
"dbsName" : "/MET/Run2016D-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(MET_Run2016D_23Sep2016)



MET_Run2016E_23Sep2016 ={
'cmgName':"MET_Run2016E_23Sep2016",
"name" : "MET_Run2016E-23Sep2016-v1",
"chunkString":"MET_Run2016E-23Sep2016-v1",
"dir": sample_path +"/" + "MET_Run2016E-23Sep2016-v1",
"dbsName" : "/MET/Run2016E-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(MET_Run2016E_23Sep2016)



MET_Run2016F_23Sep2016 ={
'cmgName':"MET_Run2016F_23Sep2016",
"name" : "MET_Run2016F-23Sep2016-v1",
"chunkString":"MET_Run2016F-23Sep2016-v1",
"dir": sample_path +"/" + "MET_Run2016F-23Sep2016-v1",
"dbsName" : "/MET/Run2016F-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(MET_Run2016F_23Sep2016)



MET_Run2016G_23Sep2016 ={
'cmgName':"MET_Run2016G_23Sep2016",
"name" : "MET_Run2016G-23Sep2016-v1",
"chunkString":"MET_Run2016G-23Sep2016-v1",
"dir": sample_path +"/" + "MET_Run2016G-23Sep2016-v1",
"dbsName" : "/MET/Run2016G-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(MET_Run2016G_23Sep2016)



MET_Run2016H_PromptReco_v2 ={
'cmgName':"MET_Run2016H_PromptReco_v2",
"name" : "MET_Run2016H-PromptReco-v2",
"chunkString":"MET_Run2016H-PromptReco-v2",
"dir": sample_path +"/" + "MET_Run2016H-PromptReco-v2",
"dbsName" : "/MET/Run2016H-PromptReco-v2/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(MET_Run2016H_PromptReco_v2)



MET_Run2016H_PromptReco_v3 ={
'cmgName':"MET_Run2016H_PromptReco_v3",
"name" : "MET_Run2016H-PromptReco-v3",
"chunkString":"MET_Run2016H-PromptReco-v3",
"dir": sample_path +"/" + "MET_Run2016H-PromptReco-v3",
"dbsName" : "/MET/Run2016H-PromptReco-v3/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(MET_Run2016H_PromptReco_v3)



SingleElectron_Run2016B_23Sep2016 ={
'cmgName':"SingleElectron_Run2016B_23Sep2016",
"name" : "SingleElectron_Run2016B-23Sep2016-v3",
"chunkString":"SingleElectron_Run2016B-23Sep2016-v3",
"dir": sample_path +"/" + "SingleElectron_Run2016B-23Sep2016-v3",
"dbsName" : "/SingleElectron/Run2016B-23Sep2016-v3/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(SingleElectron_Run2016B_23Sep2016)



SingleElectron_Run2016C_23Sep2016 ={
'cmgName':"SingleElectron_Run2016C_23Sep2016",
"name" : "SingleElectron_Run2016C-23Sep2016-v1",
"chunkString":"SingleElectron_Run2016C-23Sep2016-v1",
"dir": sample_path +"/" + "SingleElectron_Run2016C-23Sep2016-v1",
"dbsName" : "/SingleElectron/Run2016C-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(SingleElectron_Run2016C_23Sep2016)



SingleElectron_Run2016D_23Sep2016 ={
'cmgName':"SingleElectron_Run2016D_23Sep2016",
"name" : "SingleElectron_Run2016D-23Sep2016-v1",
"chunkString":"SingleElectron_Run2016D-23Sep2016-v1",
"dir": sample_path +"/" + "SingleElectron_Run2016D-23Sep2016-v1",
"dbsName" : "/SingleElectron/Run2016D-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(SingleElectron_Run2016D_23Sep2016)



SingleElectron_Run2016E_23Sep2016 ={
'cmgName':"SingleElectron_Run2016E_23Sep2016",
"name" : "SingleElectron_Run2016E-23Sep2016-v1",
"chunkString":"SingleElectron_Run2016E-23Sep2016-v1",
"dir": sample_path +"/" + "SingleElectron_Run2016E-23Sep2016-v1",
"dbsName" : "/SingleElectron/Run2016E-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(SingleElectron_Run2016E_23Sep2016)



SingleElectron_Run2016F_23Sep2016 ={
'cmgName':"SingleElectron_Run2016F_23Sep2016",
"name" : "SingleElectron_Run2016F-23Sep2016-v1",
"chunkString":"SingleElectron_Run2016F-23Sep2016-v1",
"dir": sample_path +"/" + "SingleElectron_Run2016F-23Sep2016-v1",
"dbsName" : "/SingleElectron/Run2016F-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(SingleElectron_Run2016F_23Sep2016)



SingleElectron_Run2016G_23Sep2016 ={
'cmgName':"SingleElectron_Run2016G_23Sep2016",
"name" : "SingleElectron_Run2016G-23Sep2016-v1",
"chunkString":"SingleElectron_Run2016G-23Sep2016-v1",
"dir": sample_path +"/" + "SingleElectron_Run2016G-23Sep2016-v1",
"dbsName" : "/SingleElectron/Run2016G-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(SingleElectron_Run2016G_23Sep2016)



SingleElectron_Run2016H_PromptReco_v2 ={
'cmgName':"SingleElectron_Run2016H_PromptReco_v2",
"name" : "SingleElectron_Run2016H-PromptReco-v2",
"chunkString":"SingleElectron_Run2016H-PromptReco-v2",
"dir": sample_path +"/" + "SingleElectron_Run2016H-PromptReco-v2",
"dbsName" : "/SingleElectron/Run2016H-PromptReco-v2/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(SingleElectron_Run2016H_PromptReco_v2)



SingleElectron_Run2016H_PromptReco_v3 ={
'cmgName':"SingleElectron_Run2016H_PromptReco_v3",
"name" : "SingleElectron_Run2016H-PromptReco-v3",
"chunkString":"SingleElectron_Run2016H-PromptReco-v3",
"dir": sample_path +"/" + "SingleElectron_Run2016H-PromptReco-v3",
"dbsName" : "/SingleElectron/Run2016H-PromptReco-v3/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(SingleElectron_Run2016H_PromptReco_v3)



SingleMuon_Run2016B_23Sep2016 ={
'cmgName':"SingleMuon_Run2016B_23Sep2016",
"name" : "SingleMuon_Run2016B-23Sep2016-v3",
"chunkString":"SingleMuon_Run2016B-23Sep2016-v3",
"dir": sample_path +"/" + "SingleMuon_Run2016B-23Sep2016-v3",
"dbsName" : "/SingleMuon/Run2016B-23Sep2016-v3/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(SingleMuon_Run2016B_23Sep2016)



SingleMuon_Run2016C_23Sep2016 ={
'cmgName':"SingleMuon_Run2016C_23Sep2016",
"name" : "SingleMuon_Run2016C-23Sep2016-v1",
"chunkString":"SingleMuon_Run2016C-23Sep2016-v1",
"dir": sample_path +"/" + "SingleMuon_Run2016C-23Sep2016-v1",
"dbsName" : "/SingleMuon/Run2016C-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(SingleMuon_Run2016C_23Sep2016)



SingleMuon_Run2016D_23Sep2016 ={
'cmgName':"SingleMuon_Run2016D_23Sep2016",
"name" : "SingleMuon_Run2016D-23Sep2016-v1",
"chunkString":"SingleMuon_Run2016D-23Sep2016-v1",
"dir": sample_path +"/" + "SingleMuon_Run2016D-23Sep2016-v1",
"dbsName" : "/SingleMuon/Run2016D-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(SingleMuon_Run2016D_23Sep2016)



SingleMuon_Run2016E_23Sep2016 ={
'cmgName':"SingleMuon_Run2016E_23Sep2016",
"name" : "SingleMuon_Run2016E-23Sep2016-v1",
"chunkString":"SingleMuon_Run2016E-23Sep2016-v1",
"dir": sample_path +"/" + "SingleMuon_Run2016E-23Sep2016-v1",
"dbsName" : "/SingleMuon/Run2016E-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(SingleMuon_Run2016E_23Sep2016)



SingleMuon_Run2016F_23Sep2016 ={
'cmgName':"SingleMuon_Run2016F_23Sep2016",
"name" : "SingleMuon_Run2016F-23Sep2016-v1",
"chunkString":"SingleMuon_Run2016F-23Sep2016-v1",
"dir": sample_path +"/" + "SingleMuon_Run2016F-23Sep2016-v1",
"dbsName" : "/SingleMuon/Run2016F-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(SingleMuon_Run2016F_23Sep2016)



SingleMuon_Run2016G_23Sep2016 ={
'cmgName':"SingleMuon_Run2016G_23Sep2016",
"name" : "SingleMuon_Run2016G-23Sep2016-v1",
"chunkString":"SingleMuon_Run2016G-23Sep2016-v1",
"dir": sample_path +"/" + "SingleMuon_Run2016G-23Sep2016-v1",
"dbsName" : "/SingleMuon/Run2016G-23Sep2016-v1/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(SingleMuon_Run2016G_23Sep2016)



SingleMuon_Run2016H_PromptReco_v2 ={
'cmgName':"SingleMuon_Run2016H_PromptReco_v2",
"name" : "SingleMuon_Run2016H-PromptReco-v2",
"chunkString":"SingleMuon_Run2016H-PromptReco-v2",
"dir": sample_path +"/" + "SingleMuon_Run2016H-PromptReco-v2",
"dbsName" : "/SingleMuon/Run2016H-PromptReco-v2/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(SingleMuon_Run2016H_PromptReco_v2)



SingleMuon_Run2016H_PromptReco_v3 ={
'cmgName':"SingleMuon_Run2016H_PromptReco_v3",
"name" : "SingleMuon_Run2016H-PromptReco-v3",
"chunkString":"SingleMuon_Run2016H-PromptReco-v3",
"dir": sample_path +"/" + "SingleMuon_Run2016H-PromptReco-v3",
"dbsName" : "/SingleMuon/Run2016H-PromptReco-v3/MINIAOD",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": True,
"xsec": None,


}
allComponents.append(SingleMuon_Run2016H_PromptReco_v3)

