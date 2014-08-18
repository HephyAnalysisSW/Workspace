from WMCore.Configuration import Configuration
config = Configuration()

#config.section_("<section-name>")
#config.<section-name>.<parameter-name> = <parameter-value>

config.section_("General")
config.General.requestName = "TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_Spring14miniaod-PU_S14_POSTLS170_V6-v1_MINIAODSIM"
config.General.workArea = "miniAODTuple_180814" #full or relative path to working directory
config.General.transferOutput = True #whether to transfer
config.General.saveLogs = False #1MB still available
#config.General.failureLimit =  #0.1 or 10% (which?) fraction of tolerated failures

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName   = '../defaultMINIAODTupelizer_cfg.py'
config.JobType.pyCfgParams   = [ 'keep=*_genMetTrue_*_*,*_pfMet_*_*,*_packedPFCandidates_*_*,*_prunedGenParticles_*_*,*_packedGenParticles_*_*', 'GT=POSTLS170_V5::All']
config.section_("Data")
config.Data.inputDataset   = '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU_S14_POSTLS170_V6-v1/MINIAODSIM'
#config.Data.inputDataset   = '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM'
config.Data.splitting   = 'FileBased'
config.Data.unitsPerJob = 1
#config.Data.totalUnits = 

config.section_("Site")
config.Site.storageSite = 'T2_AT_Vienna'


