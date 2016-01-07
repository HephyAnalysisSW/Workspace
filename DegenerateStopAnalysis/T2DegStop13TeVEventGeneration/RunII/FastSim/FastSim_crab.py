#Crab3 Configuration File

from CRABClient.UserUtilities import config
config = config()
#from WMCore.Configuration import Configuration
#config = Configuration()

#config.section_('General')
config.General.requestName   = 'FastSim_300_270'
config.General.transferOutputs = True
config.General.transferLogs = True
#config.General.workArea = 'crab_projects'

#config.section_('JobType')
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'fastSim_cfg.py' #Name of the CMSSW configuration file
config.JobType.outputFiles = ['T2DegStop_300_270_FastSim.root']
config.JobType.generator = 'lhe'

#config.section_('Data')
#config.Data.inputDataset = 'None'
#config.Data.inputDBS = 'global'
config.Data.splitting = 'EventBased'
config.Data.publication = False
config.Data.outputDatasetTag = 'T2DegStop_300_270_FastSim'#This string is used to construct the output dataset name
config.Data.totalUnits = 1500000
config.Data.unitsPerJob = 15000
config.Data.outputPrimaryDataset = 'T2DegStop_300_270_FastSim' #This string determines the primary dataset of the newly-produced outputs.

#config.section_('Site')
config.Site.storageSite = 'T2_AT_Vienna' #Where the output files will be transmitted to
config.Site.whitelist = ['T2_AT_Vienna']
