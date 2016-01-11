import os
import subprocess



TTJets = [
     "TTJets_LO",
     "TTJets_LO_HT600to800",
     "TTJets_LO_HT800to1200",
     "TTJets_LO_HT1200to2500",
     "TTJets_LO_HT2500toInf",
        ]
WJetsInc = [
    "WJetsToLNu"
    ]
WJetsHT  = [
    "WJetsToLNu_HT100to200",
    "WJetsToLNu_HT200to400",
    "WJetsToLNu_HT400to600",
    "WJetsToLNu_HT600toInf",
    "WJetsToLNu_HT600to800",
    "WJetsToLNu_HT800to1200",
    "WJetsToLNu_HT1200to2500" ,
    "WJetsToLNu_HT2500toInf",
    ]

WJets= WJetsInc+WJetsHT


ZJetsHT  = [
    "ZJetsToNuNu_HT100to200",
    "ZJetsToNuNu_HT200to400",
    "ZJetsToNuNu_HT400to600",
    "ZJetsToNuNu_HT600toInf"
    ]

QCDHT = [
    "QCD_HT200to300",
    "QCD_HT300to500",
    "QCD_HT500to700",
    "QCD_HT700to1000",
    "QCD_HT1000to1500",
    "QCD_HT1500to2000",
    "QCD_HT2000toInf",
    ]


Signals=[
    "T2DegStop_300_270",
    "T2DegStop_300_290FS",
    "T2DegStop_300_240FS",
    "T2DegStop_300_270FS",
]


#sample=ZJetsHT
sampleToUse=WJets

nPJobs=10
tag = "7412pass2_v4_012016_v0"
cmgTuple='Data_25ns'


small= True
overwrite=True
lepSel="inc"
processTracks=True
log="INFO"


opts=[]
if overwrite: opts.append("--overwriteOutputFiles")
if lepSel: opts.append("--leptonSelection=%s"%lepSel)
if small: opts.append("--runSmallSample")
if log: opts.append("--logLevel=%s"%log)
if cmgTuple: opts.append("--cmgTuples=%s"%cmgTuple )
opts.append("--processingTag=%s"%tag)
if processTracks: opts.append("--processTracks")
#if sample: opts.append("--processSamples=%s"%sample )


print opts






command=[]
test=True
if test:
    command.append("echo")

command.extend(["python", "cmgPostProcessing_v1.py"]+opts)

for sample in sampleToUse:
    sampleCommand = command + ["--processSamples=%s"%sample, '&']    
    subprocess.call(sampleCommand)


