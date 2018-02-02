# SoftTriggers_V15:
# HLT_PassThrough_L1_SingleMuOpen_v1
# HLT_Mu3_L1_SingleMuOpen_v1
# HLT_Mu3_PFMET50_L1_ETM30_v1
# HLT_Mu3_PFMET50_L1_SingleMuOpen_v1
# HLT_Mu3_PFMET50_PFHT50_L1_SingleMuOpen_v1
# HLT_Mu3_PFMET50_PFHT70_L1_SingleMuOpen_v1
# HLT_Mu3_PFMET70_PFHT70_L1_SingleMuOpen_v1
# HLT_Mu3_PFMET70_PFHT90_L1_SingleMuOpen_v1
# HLT_Mu3_PFMET90_PFHT90_L1_SingleMuOpen_v1
# HLT_Mu3_IsoVVVL_PFHT70_PFMET70_v1
# HLT_Mu3_IsoVVVL_PFHT90_PFMET90_v1
# HLT_Mu15_IsoVVVL_PFHT450_v12
# HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v12
# HLT_PFMET120_PFMHT120_IDTight_v17
# HLT_PFMET120_PFMHT120_IDTight_PFHT60_v6
# HLT_PFJet500_v18
# HLT_PFJet500_L1_SingleJet90_v1

groupMap = {
    'HLT_PassThrough_L1_SingleMuOpen_v': ['PhysicsUser','PhysicsUserSignal','PhysicsUserSignalNew'],
    'HLT_Mu3_L1_SingleMuOpen_v': ['PhysicsUser','PhysicsUserSignal','PhysicsUserSignalNew'],
    'HLT_Mu3_PFMET50_L1_SingleMuOpen_v': ['PhysicsUser','PhysicsUserSignal','PhysicsUserSignalNew'],
    'HLT_Mu3_PFMET50_L1_ETM30_v': ['PhysicsUser','PhysicsUserSignal','PhysicsUserSignalNew'],
    'HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v': ['PhysicsUser','PhysicsUserSignal'],
    'HLT_PFMET120_PFMHT120_IDTight_v': ['PhysicsUser','PhysicsUserSignal'],
    'HLT_Mu3_PFMET50_PFHT50_L1_SingleMuOpen_v': ['PhysicsUser','PhysicsUserSignal','PhysicsUserSignalNew'],
    'HLT_Mu3_PFMET50_PFHT70_L1_SingleMuOpen_v': ['PhysicsUser','PhysicsUserSignal','PhysicsUserSignalNew'],
    'HLT_Mu3_PFMET70_PFHT70_L1_SingleMuOpen_v': ['PhysicsUser','PhysicsUserSignal','PhysicsUserSignalNew'],
    'HLT_Mu3_PFMET70_PFHT90_L1_SingleMuOpen_v': ['PhysicsUser','PhysicsUserSignal','PhysicsUserSignalNew'],
    'HLT_Mu3_PFMET90_PFHT90_L1_SingleMuOpen_v': ['PhysicsUser','PhysicsUserSignal','PhysicsUserSignalNew'],
    'HLT_Mu3_IsoVVVL_PFHT70_PFMET70_v': ['PhysicsUser','PhysicsUserSignal','PhysicsUserSignalNew'],
    'HLT_Mu3_IsoVVVL_PFHT90_PFMET90_v': ['PhysicsUser','PhysicsUserSignal','PhysicsUserSignalNew'],
    'HLT_Mu15_IsoVVVL_PFHT450_v': ['PhysicsUser','PhysicsUserSignal'],
    'HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v': ['PhysicsUser','PhysicsUserSignal'],
    'HLT_PFMET120_PFMHT120_IDTight_v': ['PhysicsUser','PhysicsUserSignal'],
    'HLT_PFMET120_PFMHT120_IDTight_PFHT60_v': ['PhysicsUser','PhysicsUserSignal'],
    'HLT_PFJet500_v': ['PhysicsUser','PhysicsUserSignal'],
    'HLT_PFJet500_L1_SingleJet90_v': ['PhysicsUser','PhysicsUserSignal'],
    }

datasetMap = {
    'HLT_PassThrough_L1_SingleMuOpen_v': ['PhysicsUser'],
    'HLT_Mu3_L1_SingleMuOpen_v': ['PhysicsUser'],
    'HLT_Mu3_PFMET50_L1_SingleMuOpen_v': ['PhysicsUser'],
    'HLT_Mu3_PFMET50_L1_ETM30_v': ['PhysicsUser'],
    'HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v': ['PhysicsUser'],
    'HLT_PFMET120_PFMHT120_IDTight_v': ['PhysicsUser'],
    'HLT_Mu3_PFMET50_PFHT50_L1_SingleMuOpen_v': ['PhysicsUser'],
    'HLT_Mu3_PFMET50_PFHT70_L1_SingleMuOpen_v': ['PhysicsUser'],
    'HLT_Mu3_PFMET70_PFHT70_L1_SingleMuOpen_v': ['PhysicsUser'],
    'HLT_Mu3_PFMET70_PFHT90_L1_SingleMuOpen_v': ['PhysicsUser'],
    'HLT_Mu3_PFMET90_PFHT90_L1_SingleMuOpen_v': ['PhysicsUser'],
    'HLT_Mu3_IsoVVVL_PFHT70_PFMET70_v': ['PhysicsUser'],
    'HLT_Mu3_IsoVVVL_PFHT90_PFMET90_v': ['PhysicsUser'],
    'HLT_Mu15_IsoVVVL_PFHT450_v': ['PhysicsUser'],
    'HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v': ['PhysicsUser'],
    'HLT_PFMET120_PFMHT120_IDTight_v': ['PhysicsUser'],
    'HLT_PFMET120_PFMHT120_IDTight_PFHT60_v': ['PhysicsUser'],
    'HLT_PFJet500_v': ['PhysicsUser'],
    'HLT_PFJet500_L1_SingleJet90_v': ['PhysicsUser'],
    }

streamMap = {
    'HLT_PassThrough_L1_SingleMuOpen_v': ['PhysicsUser'],
    'HLT_Mu3_L1_SingleMuOpen_v': ['PhysicsUser'],
    'HLT_Mu3_PFMET50_L1_SingleMuOpen_v': ['PhysicsUser'],
    'HLT_Mu3_PFMET50_L1_ETM30_v': ['PhysicsUser'],
    'HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v': ['PhysicsUser'],
    'HLT_PFMET120_PFMHT120_IDTight_v': ['PhysicsUser'],
    'HLT_Mu3_PFMET50_PFHT50_L1_SingleMuOpen_v': ['PhysicsUser'],
    'HLT_Mu3_PFMET50_PFHT70_L1_SingleMuOpen_v': ['PhysicsUser'],
    'HLT_Mu3_PFMET70_PFHT70_L1_SingleMuOpen_v': ['PhysicsUser'],
    'HLT_Mu3_PFMET70_PFHT90_L1_SingleMuOpen_v': ['PhysicsUser'],
    'HLT_Mu3_PFMET90_PFHT90_L1_SingleMuOpen_v': ['PhysicsUser'],
    'HLT_Mu3_IsoVVVL_PFHT70_PFMET70_v': ['PhysicsUser'],
    'HLT_Mu3_IsoVVVL_PFHT90_PFMET90_v': ['PhysicsUser'],
    'HLT_Mu15_IsoVVVL_PFHT450_v': ['PhysicsUser'],
    'HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v': ['PhysicsUser'],
    'HLT_PFMET120_PFMHT120_IDTight_v': ['PhysicsUser'],
    'HLT_PFMET120_PFMHT120_IDTight_PFHT60_v': ['PhysicsUser'],
    'HLT_PFJet500_v': ['PhysicsUser'],
    'HLT_PFJet500_L1_SingleJet90_v': ['PhysicsUser'],
    }
