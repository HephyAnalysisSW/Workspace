from Menu_HLT import streamMap as triggersStreamMap
#from Menu_HLT import datasetMap as triggersDatasetMap

datasets_for_corr=[
"NoBPTX",
"DoubleEG",
"SingleElectron",
"SinglePhoton",
"BTagCSV",
"BTagMu",
"DisplacedJet",
"HTMHT",
"JetHT",
"MET",
"Tau",
"Charmonium",
"DoubleMuon",
"DoubleMuonLowMass",
"MuOnia",
"MuonEG",
"SingleMuon",
]

def physicsStreamOK(triggerName):
    result=False
    if triggerName in triggersStreamMap.keys():
        for stream in triggersStreamMap[triggerName]:
            if (stream.startswith("Physics")) and not (stream.startswith("PhysicsHLTPhysics")) and not (stream.startswith("PhysicsZeroBias")) and not (stream.startswith("PhysicsParking")) and not (stream.startswith("PhysicsCommissioning")):
                result = True
    return result

def scoutingStreamOK(triggerName):
    result=False
    if triggerName in triggersStreamMap.keys():
        for stream in triggersStreamMap[triggerName]:
            if (stream.startswith("Scouting")):
                result = True
    return result

def datasetOK(dataset):
    result=False
    if dataset in datasets_for_corr: result=True
    return result
