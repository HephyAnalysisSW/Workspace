sample_path_base = '/afs/hephy.at/data/nrad02/cmgTuples/'
sample_path_tag  = '8025_mAODv2_v7/RunIISummer16MiniAODv2/'

allComponents=[]

import os
if not os.path.isdir(sample_path_base + sample_path_tag):
    sample_path_base = '/data/nrad/cmgTuples/'
    if not os.path.isdir(sample_path_base + sample_path_tag):
        raise Exception("Cannot acces either afs-data or /data ")
sample_path = sample_path_base + sample_path_tag

DYJetsToLL_M50_HT100to200 ={
'cmgName':"DYJetsToLL_M50_HT100to200",
"name" : "DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 181.302,
"ext":['DYJetsToLL_M50_HT100to200', 'DYJetsToLL_M50_HT100to200_ext'],

}
allComponents.append(DYJetsToLL_M50_HT100to200)



DYJetsToLL_M50_HT100to200_ext ={
'cmgName':"DYJetsToLL_M50_HT100to200_ext",
"name" : "DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 181.302,
"ext":['DYJetsToLL_M50_HT100to200_ext', 'DYJetsToLL_M50_HT100to200'],

}
allComponents.append(DYJetsToLL_M50_HT100to200_ext)



DYJetsToLL_M50_HT1200to2500 ={
'cmgName':"DYJetsToLL_M50_HT1200to2500",
"name" : "DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.186222,


}
allComponents.append(DYJetsToLL_M50_HT1200to2500)



DYJetsToLL_M50_HT200to400 ={
'cmgName':"DYJetsToLL_M50_HT200to400",
"name" : "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 50.4177,
"ext":['DYJetsToLL_M50_HT200to400', 'DYJetsToLL_M50_HT200to400_ext'],

}
allComponents.append(DYJetsToLL_M50_HT200to400)



DYJetsToLL_M50_HT200to400_ext ={
'cmgName':"DYJetsToLL_M50_HT200to400_ext",
"name" : "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 50.4177,
"ext":['DYJetsToLL_M50_HT200to400_ext', 'DYJetsToLL_M50_HT200to400'],

}
allComponents.append(DYJetsToLL_M50_HT200to400_ext)



DYJetsToLL_M50_HT2500toInf ={
'cmgName':"DYJetsToLL_M50_HT2500toInf",
"name" : "DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.00438495,


}
allComponents.append(DYJetsToLL_M50_HT2500toInf)



DYJetsToLL_M50_HT400to600 ={
'cmgName':"DYJetsToLL_M50_HT400to600",
"name" : "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 6.98394,
"ext":['DYJetsToLL_M50_HT400to600', 'DYJetsToLL_M50_HT400to600_ext'],

}
allComponents.append(DYJetsToLL_M50_HT400to600)



DYJetsToLL_M50_HT400to600_ext ={
'cmgName':"DYJetsToLL_M50_HT400to600_ext",
"name" : "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 6.98394,
"ext":['DYJetsToLL_M50_HT400to600_ext', 'DYJetsToLL_M50_HT400to600'],

}
allComponents.append(DYJetsToLL_M50_HT400to600_ext)



DYJetsToLL_M50_HT600to800 ={
'cmgName':"DYJetsToLL_M50_HT600to800",
"name" : "DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2",
"chunkString":"DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2",
"dir": sample_path +"/" + "DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2",
"dbsName" : "/DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1.68141,


}
allComponents.append(DYJetsToLL_M50_HT600to800)



DYJetsToLL_M50_HT70to100 ={
'cmgName':"DYJetsToLL_M50_HT70to100",
"name" : "DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 209.592,


}
allComponents.append(DYJetsToLL_M50_HT70to100)



DYJetsToLL_M50_HT800to1200 ={
'cmgName':"DYJetsToLL_M50_HT800to1200",
"name" : "DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.775392,


}
allComponents.append(DYJetsToLL_M50_HT800to1200)



DYJetsToLL_M5to50_HT100to200 ={
'cmgName':"DYJetsToLL_M5to50_HT100to200",
"name" : "DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 224.2,
"ext":['DYJetsToLL_M5to50_HT100to200', 'DYJetsToLL_M5to50_HT100to200_ext'],

}
allComponents.append(DYJetsToLL_M5to50_HT100to200)



DYJetsToLL_M5to50_HT100to200_ext ={
'cmgName':"DYJetsToLL_M5to50_HT100to200_ext",
"name" : "DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 224.2,
"ext":['DYJetsToLL_M5to50_HT100to200_ext', 'DYJetsToLL_M5to50_HT100to200'],

}
allComponents.append(DYJetsToLL_M5to50_HT100to200_ext)



DYJetsToLL_M5to50_HT200to400 ={
'cmgName':"DYJetsToLL_M5to50_HT200to400",
"name" : "DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 37.2,
"ext":['DYJetsToLL_M5to50_HT200to400', 'DYJetsToLL_M5to50_HT200to400_ext'],

}
allComponents.append(DYJetsToLL_M5to50_HT200to400)



DYJetsToLL_M5to50_HT200to400_ext ={
'cmgName':"DYJetsToLL_M5to50_HT200to400_ext",
"name" : "DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 37.2,
"ext":['DYJetsToLL_M5to50_HT200to400_ext', 'DYJetsToLL_M5to50_HT200to400'],

}
allComponents.append(DYJetsToLL_M5to50_HT200to400_ext)



DYJetsToLL_M5to50_HT400to600 ={
'cmgName':"DYJetsToLL_M5to50_HT400to600",
"name" : "DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 3.581,
"ext":['DYJetsToLL_M5to50_HT400to600', 'DYJetsToLL_M5to50_HT400to600_ext'],

}
allComponents.append(DYJetsToLL_M5to50_HT400to600)



DYJetsToLL_M5to50_HT400to600_ext ={
'cmgName':"DYJetsToLL_M5to50_HT400to600_ext",
"name" : "DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 3.581,
"ext":['DYJetsToLL_M5to50_HT400to600_ext', 'DYJetsToLL_M5to50_HT400to600'],

}
allComponents.append(DYJetsToLL_M5to50_HT400to600_ext)



DYJetsToLL_M5to50_HT600toInf ={
'cmgName':"DYJetsToLL_M5to50_HT600toInf",
"name" : "DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1.124,
"ext":['DYJetsToLL_M5to50_HT600toInf', 'DYJetsToLL_M5to50_HT600toInf_ext'],

}
allComponents.append(DYJetsToLL_M5to50_HT600toInf)



DYJetsToLL_M5to50_HT600toInf_ext ={
'cmgName':"DYJetsToLL_M5to50_HT600toInf_ext",
"name" : "DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1.124,
"ext":['DYJetsToLL_M5to50_HT600toInf_ext', 'DYJetsToLL_M5to50_HT600toInf'],

}
allComponents.append(DYJetsToLL_M5to50_HT600toInf_ext)



QCD_HT1000to1500 ={
'cmgName':"QCD_HT1000to1500",
"name" : "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1206,
"ext":['QCD_HT1000to1500', 'QCD_HT1000to1500_ext'],

}
allComponents.append(QCD_HT1000to1500)



QCD_HT1000to1500_ext ={
'cmgName':"QCD_HT1000to1500_ext",
"name" : "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1206,
"ext":['QCD_HT1000to1500_ext', 'QCD_HT1000to1500'],

}
allComponents.append(QCD_HT1000to1500_ext)



QCD_HT100to200 ={
'cmgName':"QCD_HT100to200",
"name" : "QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 27850000.0,


}
allComponents.append(QCD_HT100to200)



QCD_HT1500to2000 ={
'cmgName':"QCD_HT1500to2000",
"name" : "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 120.4,
"ext":['QCD_HT1500to2000', 'QCD_HT1500to2000_ext'],

}
allComponents.append(QCD_HT1500to2000)



QCD_HT1500to2000_ext ={
'cmgName':"QCD_HT1500to2000_ext",
"name" : "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 120.4,
"ext":['QCD_HT1500to2000_ext', 'QCD_HT1500to2000'],

}
allComponents.append(QCD_HT1500to2000_ext)



QCD_HT2000toInf ={
'cmgName':"QCD_HT2000toInf",
"name" : "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 25.25,
"ext":['QCD_HT2000toInf', 'QCD_HT2000toInf_ext'],

}
allComponents.append(QCD_HT2000toInf)



QCD_HT2000toInf_ext ={
'cmgName':"QCD_HT2000toInf_ext",
"name" : "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 25.25,
"ext":['QCD_HT2000toInf_ext', 'QCD_HT2000toInf'],

}
allComponents.append(QCD_HT2000toInf_ext)



QCD_HT200to300 ={
'cmgName':"QCD_HT200to300",
"name" : "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1717000,
"ext":['QCD_HT200to300', 'QCD_HT200to300_ext'],

}
allComponents.append(QCD_HT200to300)



QCD_HT200to300_ext ={
'cmgName':"QCD_HT200to300_ext",
"name" : "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1717000,
"ext":['QCD_HT200to300_ext', 'QCD_HT200to300'],

}
allComponents.append(QCD_HT200to300_ext)



QCD_HT300to500 ={
'cmgName':"QCD_HT300to500",
"name" : "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 351300,
"ext":['QCD_HT300to500', 'QCD_HT300to500_ext'],

}
allComponents.append(QCD_HT300to500)



QCD_HT300to500_ext ={
'cmgName':"QCD_HT300to500_ext",
"name" : "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 351300,
"ext":['QCD_HT300to500_ext', 'QCD_HT300to500'],

}
allComponents.append(QCD_HT300to500_ext)



QCD_HT500to700 ={
'cmgName':"QCD_HT500to700",
"name" : "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 31630,
"ext":['QCD_HT500to700', 'QCD_HT500to700_ext'],

}
allComponents.append(QCD_HT500to700)



QCD_HT500to700_ext ={
'cmgName':"QCD_HT500to700_ext",
"name" : "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2",
"chunkString":"QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2",
"dir": sample_path +"/" + "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2",
"dbsName" : "/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 31630,
"ext":['QCD_HT500to700_ext', 'QCD_HT500to700'],

}
allComponents.append(QCD_HT500to700_ext)



QCD_HT50to100 ={
'cmgName':"QCD_HT50to100",
"name" : "QCD_HT50to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"QCD_HT50to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "QCD_HT50to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/QCD_HT50to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 246400000.0,


}
allComponents.append(QCD_HT50to100)



QCD_HT700to1000 ={
'cmgName':"QCD_HT700to1000",
"name" : "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 6802,
"ext":['QCD_HT700to1000', 'QCD_HT700to1000_ext'],

}
allComponents.append(QCD_HT700to1000)



QCD_HT700to1000_ext ={
'cmgName':"QCD_HT700to1000_ext",
"name" : "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 6802,
"ext":['QCD_HT700to1000_ext', 'QCD_HT700to1000'],

}
allComponents.append(QCD_HT700to1000_ext)






TBar_tWch_ext ={
'cmgName':"TBar_tWch_ext",
"name" : "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 35.6,


}
allComponents.append(TBar_tWch_ext)



TBar_tch_powheg ={
'cmgName':"TBar_tch_powheg",
"name" : "ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 136.02,


}
allComponents.append(TBar_tch_powheg)



TTGJets ={
'cmgName':"TTGJets",
"name" : "TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 3.697,


}
allComponents.append(TTGJets)



TTJets ={
'cmgName':"TTJets",
"name" : "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 831.76,


}
allComponents.append(TTJets)



TTJets_DiLepton ={
'cmgName':"TTJets_DiLepton",
"name" : "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 87.31483776,
"ext":['TTJets_DiLepton', 'TTJets_DiLepton_ext'],

}
allComponents.append(TTJets_DiLepton)



TTJets_DiLepton_ext ={
'cmgName':"TTJets_DiLepton_ext",
"name" : "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 87.31483776,
"ext":['TTJets_DiLepton_ext', 'TTJets_DiLepton'],

}
allComponents.append(TTJets_DiLepton_ext)



TTJets_LO_HT1200to2500_ext ={
'cmgName':"TTJets_LO_HT1200to2500_ext",
"name" : "TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.1987479092,


}
allComponents.append(TTJets_LO_HT1200to2500_ext)



TTJets_LO_HT2500toInf_ext ={
'cmgName':"TTJets_LO_HT2500toInf_ext",
"name" : "TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.00236841258463,


}
allComponents.append(TTJets_LO_HT2500toInf_ext)



TTJets_LO_HT600to800_ext ={
'cmgName':"TTJets_LO_HT600to800_ext",
"name" : "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 2.66653444843,


}
allComponents.append(TTJets_LO_HT600to800_ext)



TTJets_LO_HT800to1200_ext ={
'cmgName':"TTJets_LO_HT800to1200_ext",
"name" : "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1.09808219833,


}
allComponents.append(TTJets_LO_HT800to1200_ext)



TTJets_SingleLeptonFromT ={
'cmgName':"TTJets_SingleLeptonFromT",
"name" : "TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 182.17540224,
"ext":['TTJets_SingleLeptonFromT', 'TTJets_SingleLeptonFromT_ext'],

}
allComponents.append(TTJets_SingleLeptonFromT)



TTJets_SingleLeptonFromT_ext ={
'cmgName':"TTJets_SingleLeptonFromT_ext",
"name" : "TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 182.17540224,
"ext":['TTJets_SingleLeptonFromT_ext', 'TTJets_SingleLeptonFromT'],

}
allComponents.append(TTJets_SingleLeptonFromT_ext)



TTJets_SingleLeptonFromTbar ={
'cmgName':"TTJets_SingleLeptonFromTbar",
"name" : "TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 182.17540224,
"ext":['TTJets_SingleLeptonFromTbar', 'TTJets_SingleLeptonFromTbar_ext'],

}
allComponents.append(TTJets_SingleLeptonFromTbar)



TTJets_SingleLeptonFromTbar_ext ={
'cmgName':"TTJets_SingleLeptonFromTbar_ext",
"name" : "TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 182.17540224,
"ext":['TTJets_SingleLeptonFromTbar_ext', 'TTJets_SingleLeptonFromTbar'],

}
allComponents.append(TTJets_SingleLeptonFromTbar_ext)



TTWToLNu_ext ={
'cmgName':"TTWToLNu_ext",
"name" : "TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v3",
"chunkString":"TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v3",
"dir": sample_path +"/" + "TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v3",
"dbsName" : "/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v3/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.2043,
'ext':["TTWToLNu_ext", "TTWToLNu_ext2" ]

}
allComponents.append(TTWToLNu_ext)



TTWToLNu_ext2 ={
'cmgName':"TTWToLNu_ext2",
"name" : "TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1",
"chunkString":"TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1",
"dir": sample_path +"/" + "TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1",
"dbsName" : "/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.2043,
'ext':["TTWToLNu_ext", "TTWToLNu_ext2" ]


}
allComponents.append(TTWToLNu_ext2)



TTWToQQ ={
'cmgName':"TTWToQQ",
"name" : "TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.4062,


}
allComponents.append(TTWToQQ)



TTW_LO ={
'cmgName':"TTW_LO",
"name" : "ttWJets_13TeV_madgraphMLM_RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"ttWJets_13TeV_madgraphMLM_RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "ttWJets_13TeV_madgraphMLM_RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/ttWJets_13TeV_madgraphMLM/RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.6105,


}
allComponents.append(TTW_LO)



TTZToLLNuNu_m1to10 ={
'cmgName':"TTZToLLNuNu_m1to10",
"name" : "TTZToLL_M-1to10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"TTZToLL_M-1to10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "TTZToLL_M-1to10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/TTZToLL_M-1to10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.0493,


}
allComponents.append(TTZToLLNuNu_m1to10)



TTZToQQ ={
'cmgName':"TTZToQQ",
"name" : "TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.5297,


}
allComponents.append(TTZToQQ)



TTZ_LO ={
'cmgName':"TTZ_LO",
"name" : "ttZJets_13TeV_madgraphMLM_RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"ttZJets_13TeV_madgraphMLM_RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "ttZJets_13TeV_madgraphMLM_RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/ttZJets_13TeV_madgraphMLM/RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.765462427746,


}
allComponents.append(TTZ_LO)



TT_pow ={
'cmgName':"TT_pow",
"name" : "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 831.762,
"ext":["TT_pow", "TT_pow_backup" ]
}
allComponents.append(TT_pow)



TT_pow_backup ={
'cmgName':"TT_pow_backup",
"name" : "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 831.762,
"ext":["TT_pow", "TT_pow_backup" ]
}
allComponents.append(TT_pow_backup)



T_tWch_ext ={
'cmgName':"T_tWch_ext",
"name" : "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 35.6,


}
allComponents.append(T_tWch_ext)



T_tch_powheg ={
'cmgName':"T_tch_powheg",
"name" : "ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 136.02,


}
allComponents.append(T_tch_powheg)



WJetsToLNu ={
'cmgName':"WJetsToLNu",
"name" : "WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 61526.7,


}
allComponents.append(WJetsToLNu)



WJetsToLNu_HT100to200 ={
'cmgName':"WJetsToLNu_HT100to200",
"name" : "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1627.45,
"ext":['WJetsToLNu_HT100to200_ext', 'WJetsToLNu_HT100to200', "WJetsToLNu_HT100to200_ext2"],

}
allComponents.append(WJetsToLNu_HT100to200)



WJetsToLNu_HT100to200_ext ={
'cmgName':"WJetsToLNu_HT100to200_ext",
"name" : "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1627.45,
"ext":['WJetsToLNu_HT100to200_ext', 'WJetsToLNu_HT100to200', "WJetsToLNu_HT100to200_ext2"],

}
allComponents.append(WJetsToLNu_HT100to200_ext)



WJetsToLNu_HT100to200_ext2 ={
'cmgName':"WJetsToLNu_HT100to200_ext2",
"name" : "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1",
"chunkString":"WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1",
"dbsName" : "/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1627.45,
"ext":['WJetsToLNu_HT100to200_ext', 'WJetsToLNu_HT100to200', "WJetsToLNu_HT100to200_ext2"],


}
allComponents.append(WJetsToLNu_HT100to200_ext2)



WJetsToLNu_HT1200to2500 ={
'cmgName':"WJetsToLNu_HT1200to2500",
"name" : "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1.60809,
"ext":['WJetsToLNu_HT1200to2500', 'WJetsToLNu_HT1200to2500_ext'],

}
allComponents.append(WJetsToLNu_HT1200to2500)



WJetsToLNu_HT1200to2500_ext ={
'cmgName':"WJetsToLNu_HT1200to2500_ext",
"name" : "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1.60809,
"ext":['WJetsToLNu_HT1200to2500_ext', 'WJetsToLNu_HT1200to2500'],

}
allComponents.append(WJetsToLNu_HT1200to2500_ext)



WJetsToLNu_HT200to400 ={
'cmgName':"WJetsToLNu_HT200to400",
"name" : "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 435.237,
"ext":['WJetsToLNu_HT200to400_ext', 'WJetsToLNu_HT200to400', "WJetsToLNu_HT200to400_ext2"],

}
allComponents.append(WJetsToLNu_HT200to400)



WJetsToLNu_HT200to400_ext ={
'cmgName':"WJetsToLNu_HT200to400_ext",
"name" : "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 435.237,
"ext":['WJetsToLNu_HT200to400_ext', 'WJetsToLNu_HT200to400', "WJetsToLNu_HT200to400_ext2"],
}
allComponents.append(WJetsToLNu_HT200to400_ext)



WJetsToLNu_HT200to400_ext2 ={
'cmgName':"WJetsToLNu_HT200to400_ext2",
"name" : "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1",
"chunkString":"WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1",
"dbsName" : "/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 435.237,
"ext":['WJetsToLNu_HT200to400_ext', 'WJetsToLNu_HT200to400', "WJetsToLNu_HT200to400_ext2"],
}
allComponents.append(WJetsToLNu_HT200to400_ext2)



WJetsToLNu_HT2500toInf ={
'cmgName':"WJetsToLNu_HT2500toInf",
"name" : "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.0389136,
"ext":['WJetsToLNu_HT2500toInf', 'WJetsToLNu_HT2500toInf_ext'],

}
allComponents.append(WJetsToLNu_HT2500toInf)



WJetsToLNu_HT2500toInf_ext ={
'cmgName':"WJetsToLNu_HT2500toInf_ext",
"name" : "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.0389136,
"ext":['WJetsToLNu_HT2500toInf_ext', 'WJetsToLNu_HT2500toInf'],

}
allComponents.append(WJetsToLNu_HT2500toInf_ext)



WJetsToLNu_HT400to600 ={
'cmgName':"WJetsToLNu_HT400to600",
"name" : "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 59.1811,
"ext":['WJetsToLNu_HT400to600', 'WJetsToLNu_HT400to600_ext'],

}
allComponents.append(WJetsToLNu_HT400to600)



WJetsToLNu_HT400to600_ext ={
'cmgName':"WJetsToLNu_HT400to600_ext",
"name" : "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 59.1811,
"ext":['WJetsToLNu_HT400to600_ext', 'WJetsToLNu_HT400to600'],

}
allComponents.append(WJetsToLNu_HT400to600_ext)



WJetsToLNu_HT600to800 ={
'cmgName':"WJetsToLNu_HT600to800",
"name" : "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 14.5805,
"ext":['WJetsToLNu_HT600to800', 'WJetsToLNu_HT600to800_ext'],

}
allComponents.append(WJetsToLNu_HT600to800)



WJetsToLNu_HT600to800_ext ={
'cmgName':"WJetsToLNu_HT600to800_ext",
"name" : "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 14.5805,
"ext":['WJetsToLNu_HT600to800_ext', 'WJetsToLNu_HT600to800'],

}
allComponents.append(WJetsToLNu_HT600to800_ext)



WJetsToLNu_HT70to100 ={
'cmgName':"WJetsToLNu_HT70to100",
"name" : "WJetsToLNu_HT-70To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"WJetsToLNu_HT-70To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-70To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/WJetsToLNu_HT-70To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1637.13,


}
allComponents.append(WJetsToLNu_HT70to100)



WJetsToLNu_HT800to1200 ={
'cmgName':"WJetsToLNu_HT800to1200",
"name" : "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 6.65621,
"ext":['WJetsToLNu_HT800to1200', 'WJetsToLNu_HT800to1200_ext'],
}
allComponents.append(WJetsToLNu_HT800to1200)



WJetsToLNu_HT800to1200_ext ={
'cmgName':"WJetsToLNu_HT800to1200_ext",
"name" : "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 6.65621,
"ext":['WJetsToLNu_HT800to1200_ext', 'WJetsToLNu_HT800to1200'],

}
allComponents.append(WJetsToLNu_HT800to1200_ext)



WJetsToLNu_LO ={
'cmgName':"WJetsToLNu_LO",
"name" : "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 61526.7,


}
allComponents.append(WJetsToLNu_LO)



WJetsToLNu_Pt_100to250 ={
'cmgName':"WJetsToLNu_Pt_100to250",
"name" : "WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 626.3,
"ext":['WJetsToLNu_Pt_100to250', 'WJetsToLNu_Pt_100to250_ext'],

}
allComponents.append(WJetsToLNu_Pt_100to250)



WJetsToLNu_Pt_100to250_ext ={
'cmgName':"WJetsToLNu_Pt_100to250_ext",
"name" : "WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 626.3,
"ext":['WJetsToLNu_Pt_100to250_ext', 'WJetsToLNu_Pt_100to250'],

}
allComponents.append(WJetsToLNu_Pt_100to250_ext)



WJetsToLNu_Pt_250to400 ={
'cmgName':"WJetsToLNu_Pt_250to400",
"name" : "WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 21.82,
"ext":['WJetsToLNu_Pt_250to400', 'WJetsToLNu_Pt_250to400_ext'],

}
allComponents.append(WJetsToLNu_Pt_250to400)



WJetsToLNu_Pt_250to400_ext ={
'cmgName':"WJetsToLNu_Pt_250to400_ext",
"name" : "WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 21.82,
"ext":['WJetsToLNu_Pt_250to400_ext', 'WJetsToLNu_Pt_250to400'],

}
allComponents.append(WJetsToLNu_Pt_250to400_ext)



WJetsToLNu_Pt_400to600 ={
'cmgName':"WJetsToLNu_Pt_400to600",
"name" : "WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 2.68,
"ext":['WJetsToLNu_Pt_400to600', 'WJetsToLNu_Pt_400to600_ext'],

}
allComponents.append(WJetsToLNu_Pt_400to600)



WJetsToLNu_Pt_400to600_ext ={
'cmgName':"WJetsToLNu_Pt_400to600_ext",
"name" : "WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 2.68,
"ext":['WJetsToLNu_Pt_400to600_ext', 'WJetsToLNu_Pt_400to600'],

}
allComponents.append(WJetsToLNu_Pt_400to600_ext)



WJetsToLNu_Pt_600toInf ={
'cmgName':"WJetsToLNu_Pt_600toInf",
"name" : "WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.4109,
"ext":['WJetsToLNu_Pt_600toInf', 'WJetsToLNu_Pt_600toInf_ext'],

}
allComponents.append(WJetsToLNu_Pt_600toInf)



WJetsToLNu_Pt_600toInf_ext ={
'cmgName':"WJetsToLNu_Pt_600toInf_ext",
"name" : "WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.4109,
"ext":['WJetsToLNu_Pt_600toInf_ext', 'WJetsToLNu_Pt_600toInf'],

}
allComponents.append(WJetsToLNu_Pt_600toInf_ext)



WW ={
'cmgName':"WW",
"name" : "WW_TuneCUETP8M1_13TeV-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"WW_TuneCUETP8M1_13TeV-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "WW_TuneCUETP8M1_13TeV-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 115.0422,


}
allComponents.append(WW)



WZ ={
'cmgName':"WZ",
"name" : "WZ_TuneCUETP8M1_13TeV-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"WZ_TuneCUETP8M1_13TeV-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "WZ_TuneCUETP8M1_13TeV-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 47.13,


}
allComponents.append(WZ)

###


###





ZJetsToNuNu_HT100to200 ={
'cmgName':"ZJetsToNuNu_HT100to200",
"name" : "ZJetsToNuNu_HT-100To200_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"ZJetsToNuNu_HT-100To200_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "ZJetsToNuNu_HT-100To200_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/ZJetsToNuNu_HT-100To200_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 344.9781,
"ext":['ZJetsToNuNu_HT100to200', 'ZJetsToNuNu_HT100to200_ext'],

}
allComponents.append(ZJetsToNuNu_HT100to200)



ZJetsToNuNu_HT100to200_ext ={
'cmgName':"ZJetsToNuNu_HT100to200_ext",
"name" : "ZJetsToNuNu_HT-100To200_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"ZJetsToNuNu_HT-100To200_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "ZJetsToNuNu_HT-100To200_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/ZJetsToNuNu_HT-100To200_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 344.9781,
"ext":['ZJetsToNuNu_HT100to200_ext', 'ZJetsToNuNu_HT100to200'],

}
allComponents.append(ZJetsToNuNu_HT100to200_ext)



ZJetsToNuNu_HT1200to2500 ={
'cmgName':"ZJetsToNuNu_HT1200to2500",
"name" : "ZJetsToNuNu_HT-1200To2500_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"ZJetsToNuNu_HT-1200To2500_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "ZJetsToNuNu_HT-1200To2500_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/ZJetsToNuNu_HT-1200To2500_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.441078,
"ext":['ZJetsToNuNu_HT1200to2500', 'ZJetsToNuNu_HT1200to2500_ext'],

}
allComponents.append(ZJetsToNuNu_HT1200to2500)



ZJetsToNuNu_HT1200to2500_ext ={
'cmgName':"ZJetsToNuNu_HT1200to2500_ext",
"name" : "ZJetsToNuNu_HT-1200To2500_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"ZJetsToNuNu_HT-1200To2500_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "ZJetsToNuNu_HT-1200To2500_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/ZJetsToNuNu_HT-1200To2500_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.441078,
"ext":['ZJetsToNuNu_HT1200to2500_ext', 'ZJetsToNuNu_HT1200to2500'],

}
allComponents.append(ZJetsToNuNu_HT1200to2500_ext)



ZJetsToNuNu_HT200to400 ={
'cmgName':"ZJetsToNuNu_HT200to400",
"name" : "ZJetsToNuNu_HT-200To400_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"ZJetsToNuNu_HT-200To400_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "ZJetsToNuNu_HT-200To400_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/ZJetsToNuNu_HT-200To400_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 96.3828,
"ext":['ZJetsToNuNu_HT200to400', 'ZJetsToNuNu_HT200to400_ext'],

}
allComponents.append(ZJetsToNuNu_HT200to400)



ZJetsToNuNu_HT200to400_ext ={
'cmgName':"ZJetsToNuNu_HT200to400_ext",
"name" : "ZJetsToNuNu_HT-200To400_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"ZJetsToNuNu_HT-200To400_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "ZJetsToNuNu_HT-200To400_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/ZJetsToNuNu_HT-200To400_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 96.3828,
"ext":['ZJetsToNuNu_HT200to400_ext', 'ZJetsToNuNu_HT200to400'],

}
allComponents.append(ZJetsToNuNu_HT200to400_ext)



ZJetsToNuNu_HT2500toInf ={
'cmgName':"ZJetsToNuNu_HT2500toInf",
"name" : "ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 0.01008969,


}
allComponents.append(ZJetsToNuNu_HT2500toInf)



ZJetsToNuNu_HT400to600 ={
'cmgName':"ZJetsToNuNu_HT400to600",
"name" : "ZJetsToNuNu_HT-400To600_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"ZJetsToNuNu_HT-400To600_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "ZJetsToNuNu_HT-400To600_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/ZJetsToNuNu_HT-400To600_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 13.4562,
"ext":['ZJetsToNuNu_HT400to600', 'ZJetsToNuNu_HT400to600_ext'],

}
allComponents.append(ZJetsToNuNu_HT400to600)



ZJetsToNuNu_HT400to600_ext ={
'cmgName':"ZJetsToNuNu_HT400to600_ext",
"name" : "ZJetsToNuNu_HT-400To600_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"chunkString":"ZJetsToNuNu_HT-400To600_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dir": sample_path +"/" + "ZJetsToNuNu_HT-400To600_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1",
"dbsName" : "/ZJetsToNuNu_HT-400To600_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 13.4562,
"ext":['ZJetsToNuNu_HT400to600_ext', 'ZJetsToNuNu_HT400to600'],

}
allComponents.append(ZJetsToNuNu_HT400to600_ext)



ZJetsToNuNu_HT600to800 ={
'cmgName':"ZJetsToNuNu_HT600to800",
"name" : "ZJetsToNuNu_HT-600To800_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"ZJetsToNuNu_HT-600To800_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "ZJetsToNuNu_HT-600To800_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/ZJetsToNuNu_HT-600To800_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 3.96183,
}
allComponents.append(ZJetsToNuNu_HT600to800)



ZJetsToNuNu_HT800to1200 ={
'cmgName':"ZJetsToNuNu_HT800to1200",
"name" : "ZJetsToNuNu_HT-800To1200_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"ZJetsToNuNu_HT-800To1200_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "ZJetsToNuNu_HT-800To1200_13TeV-madgraph_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/ZJetsToNuNu_HT-800To1200_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1.81302,
}
allComponents.append(ZJetsToNuNu_HT800to1200)






ZZ ={
'cmgName':"ZZ",
"name" : "ZZ_TuneCUETP8M1_13TeV-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"ZZ_TuneCUETP8M1_13TeV-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "ZZ_TuneCUETP8M1_13TeV-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 16.523,


}
allComponents.append(ZZ)


## Signals



SMS_T2tt_genHT_160_genMET_80_mStop_275_mLSP_205 ={
'cmgName':"SMS_T2tt_genHT_160_genMET_80_mStop_275_mLSP_205",
"name" : "SMS-T2-4bd_genMET-80_mStop-275_mLSP-205_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"SMS-T2-4bd_genMET-80_mStop-275_mLSP-205_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "SMS-T2-4bd_genMET-80_mStop-275_mLSP-205_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/SMS-T2-4bd_genMET-80_mStop-275_mLSP-205_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 13.32,


}
allComponents.append(SMS_T2tt_genHT_160_genMET_80_mStop_275_mLSP_205)



SMS_T2tt_genHT_160_genMET_80_mStop_350_mLSP_330 ={
'cmgName':"SMS_T2tt_genHT_160_genMET_80_mStop_350_mLSP_330",
"name" : "SMS-T2-4bd_genMET-80_mStop-350_mLSP-330_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"SMS-T2-4bd_genMET-80_mStop-350_mLSP-330_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "SMS-T2-4bd_genMET-80_mStop-350_mLSP-330_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/SMS-T2-4bd_genMET-80_mStop-350_mLSP-330_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 3.786,


}
allComponents.append(SMS_T2tt_genHT_160_genMET_80_mStop_350_mLSP_330)



SMS_T2tt_genHT_160_genMET_80_mStop_400_mLSP_350 ={
'cmgName':"SMS_T2tt_genHT_160_genMET_80_mStop_400_mLSP_350",
"name" : "SMS-T2-4bd_genMET-80_mStop-400_mLSP-350_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"chunkString":"SMS-T2-4bd_genMET-80_mStop-400_mLSP-350_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dir": sample_path +"/" + "SMS-T2-4bd_genMET-80_mStop-400_mLSP-350_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1",
"dbsName" : "/SMS-T2-4bd_genMET-80_mStop-400_mLSP-350_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1.835,


}
allComponents.append(SMS_T2tt_genHT_160_genMET_80_mStop_400_mLSP_350)


# FastSIM Scans



SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1 ={
"mass_template":"SMS_T2bW_X05_mStop_%s_mLSP_%s_mWMin0p1",
'massVars':['GenSusyMStop', 'GenSusyMNeutralino'],
'cmgName':"SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1",
"name" : "SMS-T2bW_X05_dM-10to80_genHT-160_genMET-80_mWMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"chunkString":"SMS-T2bW_X05_dM-10to80_genHT-160_genMET-80_mWMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_path +"/" + "SMS-T2bW_X05_dM-10to80_genHT-160_genMET-80_mWMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/SMS-T2bW_X05_dM-10to80_genHT-160_genMET-80_mWMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1,
"isFastSim":True,
}
allComponents.append(SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1)



SMS_T2tt_dM_10to80_genHT_160_genMET_80 ={
"mass_template":"SMS_T2tt_mStop_%s_mLSP_%s",
'massVars':['GenSusyMStop', 'GenSusyMNeutralino'],
'cmgName':"SMS_T2tt_dM_10to80_genHT_160_genMET_80",
"name" : "SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"chunkString":"SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_path +"/" + "SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1,
"isFastSim":True,
}
allComponents.append(SMS_T2tt_dM_10to80_genHT_160_genMET_80)



SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1 ={
"mass_template":"SMS_T2tt_mStop_%s_mLSP_%s_mWMin0p1",
'massVars':['GenSusyMStop', 'GenSusyMNeutralino'],
'cmgName':"SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1",
"name" : "SMS-T2tt_dM-10to80_genHT-160_genMET-80_mWMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"chunkString":"SMS-T2tt_dM-10to80_genHT-160_genMET-80_mWMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dir": sample_path +"/" + "SMS-T2tt_dM-10to80_genHT-160_genMET-80_mWMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1",
"dbsName" : "/SMS-T2tt_dM-10to80_genHT-160_genMET-80_mWMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
"rootFileLocation":"tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
"isData": False,
"xsec": 1,
"isFastSim":True,
}
allComponents.append(SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1)



### Signal ###





signals = [SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1 , SMS_T2tt_dM_10to80_genHT_160_genMET_80, SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1]
for sig in signals:
    sig['mass_dict'] = sample_path + "/%s_mass_dict.pkl"%sig['cmgName']


def makeGetChainFunc(comp):
    def getChainFunc():
        import Workspace.HEPHYPythonTools.helpers as helpers
        chunks, sumWeights = helpers.getChunks(comp)
        chain  = helpers.getChain( chunks , histname='', treeName='tree')
        chain.sumWeights = sumWeights
        return chain
    return getChainFunc

def addGetChain():
    for comp in allComponents:
        comp['getChain'] = makeGetChainFunc(comp)
