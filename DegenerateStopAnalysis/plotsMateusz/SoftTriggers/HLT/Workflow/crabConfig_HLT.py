#Crab3 Configuration File

from CRABClient.UserUtilities import config
config = config()
#from WMCore.Configuration import Configuration
#config = Configuration()

menuVersion = 'V18'
sampName = 'TT_SoftTriggers-%s_HLT'%menuVersion

#config.section_('General')
config.General.requestName = sampName 
config.General.transferOutputs = True
config.General.transferLogs = True
#config.General.workArea = 'crab_projects'

#config.section_('JobType')
#config.JobType.inputFiles = ['/afs/hephy.at/data/mzarucki02/gridpacks/%s'%gridpack]
config.JobType.pyCfgParams = ['menuVersion='+menuVersion]
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'SoftTriggers_HLT.py' # Name of the CMSSW configuration file
config.JobType.outputFiles = ['%s.root'%sampName]
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 8000 # 2000*numCores 
#config.JobType.generator = 'lhe'

#config.section_('Data')
#config.Data.inputDataset = '/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_SUS01_92X_upgrade2017_realistic_v10-v1/GEN-SIM-RAW' 
config.Data.inputDataset = '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/GEN-SIM-RAW'
config.Data.inputDBS = 'global'
#config.Data.userInputFiles = [x.strip() for x in open('inputFiles_GEN-SIM.txt').readlines()] #NOTE: careful that the string is not too long
config.Data.outputDatasetTag = sampName # This string is used to construct the output dataset name
#config.Data.outputPrimaryDataset = sampName # This string determines the primary dataset of the newly-produced outputs.
config.Data.splitting = 'FileBased'
config.Data.publication = False
config.Data.totalUnits = 100 #300000
config.Data.unitsPerJob = 1 #NOTE: if FileBased splitting, # files per job
config.Data.ignoreLocality = True # Set to True to allow the jobs to run at sites regardless of where the input dataset is hosted (this parameter has effect only when Data.inputDataset is used). The parameter Site.whitelist is mandatory and Site.blacklist can also be used and it is respected. This parameter is useful to allow the jobs to run on other sites when for example a dataset is hosted only on sites which are not running CRAB jobs. 

#config.section_('Site')
config.Site.storageSite = 'T2_AT_Vienna' #Where the output files will be transmitted to
config.Site.whitelist = ['T2_*'] #['CH_CERN','T2_AT_Vienna']

#if __name__ == '__main__':
#    from CRABAPI.RawCommand import crabCommand
#    crabCommand('submit', config = config)
