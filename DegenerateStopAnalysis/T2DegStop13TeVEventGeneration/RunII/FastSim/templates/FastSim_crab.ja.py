#Crab3 Configuration File

lspmass={{LSPMASS}}
postfix="{{POSTFIX}}"
lhetag="{{LHETAG}}"

from CRABClient.UserUtilities import config
config = config()
#from WMCore.Configuration import Configuration
#config = Configuration()

#config.section_('General')
config.General.requestName   = 'T2tt_300_%s_CMSSW_7_4_4_FastSim_PU25ns_MCRUN2_74_V9_%s'%(lspmass,lhetag) + postfix
config.General.transferOutputs = True
config.General.transferLogs = True
#config.General.workArea = 'crab_projects'

#config.section_('JobType')
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'FastSim_filtered_%s_cfg.py'%lhetag #Name of the CMSSW configuration file
#config.JobType.outputFiles = ['T2DegStop_300_%s_11p8M_FastSim_%s.root'%(lspmass,lhetag)]
config.JobType.outputFiles = ['T2tt_300_%s_11p8M_FastSim_%s.root'%(lspmass,lhetag)]
config.JobType.generator = 'lhe'
config.JobType.maxMemoryMB=2500
#config.section_('Data')
#config.Data.inputDataset = 'None'
#config.Data.inputDBS = 'global'
config.Data.splitting = 'EventBased'
config.Data.publication = True
config.Data.outputDatasetTag = 'CMSSW_7_4_4_FastSim_PU25ns_MCRUN2_74_V9_AODSIM'#This string is used to construct the output dataset name
config.Data.totalUnits = 100000
config.Data.unitsPerJob = 10000
config.Data.outputPrimaryDataset = 'T2tt_stop300_LSP%s'%lspmass +postfix#This string determines the primary dataset of the newly-produced outputs.

#config.section_('Site')
config.Site.storageSite = 'T2_AT_Vienna' #Where the output files will be transmitted to
#config.Site.whitelist = ['T2_AT_Vienna']
