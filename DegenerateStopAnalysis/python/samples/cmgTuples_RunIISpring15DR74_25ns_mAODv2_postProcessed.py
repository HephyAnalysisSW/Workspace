""" CMG post-processed ntuples from RunIISpring15DR74 MC production at 25 ns for the degenerate stop analysis.
 
Each set of ntuples is produced with a git tag of HephySusySW.Workspace repository and 
and is saved in a directory 
    {path}/cmgTuples/{processingEra}/{processingTag}/{campaign}/{inc/soft/...}
where    
    processingEra: postProcessed_mAODv2 (starts always with "postProcessed_")
    processingTag: git tag of HephySusySW.Workspace
    campaign:
        MC production campaign for MC samples  (e.g. RunIISpring15DR74, with _25ns added as additional identification)
        Energy, reconstruction tag, era for data (e.g. 13TeV_PromptReco_Collisions15_25ns, taken 
            from JSON name file)
    
The corresponding py sample files are called 
    cmgTuples_RunIISpring15DR74_25ns_mAODv2_postProcessed.py
    cmgTuples_Data_25ns_mAODv2_postProcessed.py

"""

# available ntuple directories 

# no Workspace tag exists for this set
dir_cmgPostProcessing_Aug21 = '/afs/hephy.at/work/n/nrad/cmgTuplesPostProcessed/Spring15_v1' 

# Workspace tag: cmgPostProcessing_Oct1
#dir_cmgPostProcessing_Oct1 = '/data/nrad/cmgTuples/cmgPostProcessing_Oct1/RunIISpring15DR74'
dir_cmgPostProcessing_Oct1 = '/data/nrad/cmgTuples/postProcessed_Spring15_vasile_v1/inc'

dir_cmgPostProcessing_v0 = \
    '/afs/hephy.at/user/v/vghete/vghete01/cmgTuples/postProcessed_mAODv2/v0/RunIISpring15DR74_25ns/inc'

dir_cmgPostProcessing_7412pass2_v4_022116_sync_v0 = \
    '/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_v4_022116_sync_v0/RunIISpring15DR74_25ns/inc'


# set the actual ntuple directory 
#
ntuple_directory = dir_cmgPostProcessing_7412pass2_v4_022116_sync_v0


# definition of samples
#

ntupleAvailable = True
if ntupleAvailable:
    TTJets_LO={\
        "name" : "TTJets_LO",
        "bins" : [
            "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1"
            ],
        'dir' : ntuple_directory,
        'sampleId' : 10,
        }

ntupleAvailable = True
if ntupleAvailable:
    WJetsToLNu_HT={\
        "name" : "WJetsToLNu_HT",
        "bins" : [
            "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",            
            "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            "WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1",
            ],
        'dir' : ntuple_directory,
        'sampleId' : 20,
        }


ntupleAvailable = False
if ntupleAvailable:
    QCD_HT = {
        "name" : "QCD_HT",
        "bins" : [
            "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
            "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
            "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
            "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
            "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
            "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
            "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1",
            ],
        'dir' : ntuple_directory,
        'sampleId' : 30
        }


ntupleAvailable = True
if ntupleAvailable:
    T2DegStop={\
        "name" : "T2DegStop",
        "bins" : [
            "T2DegStop_300_270",
            ],
        'dir' : ntuple_directory,
        'sampleId' : 0,
        }
    
# keep also the old-style signal definition    

allSignalStrings=[\
        "T2DegStop_300_270",
        ]

def getSignalSample(signal):
    if signal in allSignalStrings:
        return {
                "name" : signal,
                'bins':[signal],
                'dir' : ntuple_directory,
                }
    else:
        print "Signal ", signal, " unknown. Available signal samples: ",", ".join(allSignalStrings)

allSignals=[]
for s in allSignalStrings:
    sm = getSignalSample(s)
    exec(s+"=sm")
    exec("allSignals.append(s)")
