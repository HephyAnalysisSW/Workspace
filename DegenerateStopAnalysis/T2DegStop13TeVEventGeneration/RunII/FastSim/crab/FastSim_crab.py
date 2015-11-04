from WMCore.Configuration import Configuration
config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.section_('JobType')
config.JobType.psetName = 'FastSim_cfg.py'
config.JobType.pluginName = 'privateMC'
config.JobType.outputFiles = ['T2DegStop_300_270_FASTSIM.root']
config.JobType.generator = 'lhe'
config.section_('Data')
config.Data.inputDataset = 'None'
config.Data.totalUnits = 1500000
config.Data.unitsPerJob = 5000
config.Data.splitting = 'EventBased'
config.Data.publishDataName = 'T2DegStop_300_270'
config.Data.publication = True
config.section_('User')
config.section_('Site')
config.Site.whitelist = ['T2_AT_Vienna']
config.Site.storageSite = 'T2_AT_Vienna'
