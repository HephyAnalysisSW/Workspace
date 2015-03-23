from WMCore.Configuration import Configuration
config = Configuration()

#config.section_("<section-name>")
#config.<section-name>.<parameter-name> = <parameter-value>


config.section_("General")
config.General.requestName = "pfCand"
config.General.workArea = "pfCand"
config.General.transferOutputs = True #whether to transfer
config.General.transferLogs = True #1MB still available
#config.General.failureLimit =  #0.1 or 10% (which?) fraction of tolerated failures

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName   = 'miniAODAndTupelizer.py'
#config.JobType.pyCfgParams   = [ 'keep=*_genMetTrue_*_*,*_pfMet_*_*,*_packedPFCandidates_*_*,*_prunedGenParticles_*_*,*_packedGenParticles_*_*', 'GT=POSTLS170_V6::All']
config.section_("Data")
#config.Data.dbsUrl = 'phys03'
config.Data.inputDataset   = '/DYToMuMu_M-50_Tune4C_13TeV-pythia8/Phys14DR-PU20bx25_tsg_castor_PHYS14_25_V1-v1/GEN-SIM-RECO'
config.Data.splitting   = 'FileBased'
config.Data.unitsPerJob = 1
#config.Data.totalUnits = 
config.section_("Site")
config.Site.storageSite = 'T2_AT_Vienna'


